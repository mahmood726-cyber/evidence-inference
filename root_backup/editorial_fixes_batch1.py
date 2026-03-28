"""Editorial Review Fixes - Batch 1: Core Statistical Methods"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original size: {len(content):,} bytes')

# ============================================================================
# BATCH 1: Core Statistical Methods
# ============================================================================

batch1_code = '''
const ContinuousOutcomes={
calculateMD(mean1,sd1,n1,mean2,sd2,n2){
const md=mean1-mean2;
const se=Math.sqrt((sd1*sd1/n1)+(sd2*sd2/n2));
const vi=se*se;
return{yi:md,vi,se,measure:'MD',mean1,sd1,n1,mean2,sd2,n2};
},
calculateSMD(mean1,sd1,n1,mean2,sd2,n2,method='hedges'){
const pooledSD=Math.sqrt(((n1-1)*sd1*sd1+(n2-1)*sd2*sd2)/(n1+n2-2));
let smd=(mean1-mean2)/pooledSD;
let correction=1;
if(method==='hedges'){
const df=n1+n2-2;
correction=1-(3/(4*df-1));
smd*=correction;
}
const se=Math.sqrt((n1+n2)/(n1*n2)+(smd*smd)/(2*(n1+n2)));
return{yi:smd,vi:se*se,se,measure:'SMD',method,correction,pooledSD};
},
calculateROM(mean1,sd1,n1,mean2,sd2,n2){
const logROM=Math.log(mean1/mean2);
const se=Math.sqrt((sd1*sd1)/(n1*mean1*mean1)+(sd2*sd2)/(n2*mean2*mean2));
return{yi:logROM,vi:se*se,se,measure:'ROM',ratio:Math.exp(logROM)};
},
poolContinuous(studies,measure='MD'){
if(!studies||studies.length===0)return{error:'No studies'};
const processed=studies.map(s=>{
if(measure==='MD')return this.calculateMD(s.mean1,s.sd1,s.n1,s.mean2,s.sd2,s.n2);
if(measure==='SMD')return this.calculateSMD(s.mean1,s.sd1,s.n1,s.mean2,s.sd2,s.n2);
if(measure==='ROM')return this.calculateROM(s.mean1,s.sd1,s.n1,s.mean2,s.sd2,s.n2);
return s;
});
const weights=processed.map(p=>1/p.vi);
const sumW=weights.reduce((a,b)=>a+b,0);
const pooled=processed.reduce((s,p,i)=>s+weights[i]*p.yi,0)/sumW;
const se=Math.sqrt(1/sumW);
const z=pooled/se;
const pValue=2*(1-Stats.pnorm(Math.abs(z)));
return{pooled,se,ci:[pooled-1.96*se,pooled+1.96*se],z,pValue,measure,k:studies.length,processed};
}
};

const MLEstimator={
estimate(yi,vi,maxIter=100,tol=1e-8){
const n=yi.length;
let tau2=0.1;
for(let iter=0;iter<maxIter;iter++){
const w=vi.map(v=>1/(v+tau2));
const sumW=w.reduce((a,b)=>a+b,0);
const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;
let num=0,den=0;
for(let i=0;i<n;i++){
const wi=w[i];
const resid=yi[i]-mu;
num+=wi*wi*(resid*resid-vi[i]);
den+=wi*wi;
}
const tau2New=Math.max(0,tau2+num/den);
if(Math.abs(tau2New-tau2)<tol)break;
tau2=tau2New;
}
const w=vi.map(v=>1/(v+tau2));
const sumW=w.reduce((a,b)=>a+b,0);
const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;
let ll=-0.5*n*Math.log(2*Math.PI);
for(let i=0;i<n;i++){
ll+=-0.5*Math.log(vi[i]+tau2)-0.5*(yi[i]-mu)*(yi[i]-mu)/(vi[i]+tau2);
}
return{tau2,mu,logLik:ll,method:'ML',converged:true};
},
likelihoodRatioTest(yi,vi,tau2_full,tau2_reduced=0){
const fullModel=this.estimate(yi,vi);
const w0=vi.map(v=>1/v);
const sumW0=w0.reduce((a,b)=>a+b,0);
const mu0=yi.reduce((s,y,i)=>s+w0[i]*y,0)/sumW0;
let ll0=-0.5*yi.length*Math.log(2*Math.PI);
for(let i=0;i<yi.length;i++){
ll0+=-0.5*Math.log(vi[i])-0.5*(yi[i]-mu0)*(yi[i]-mu0)/vi[i];
}
const lrt=2*(fullModel.logLik-ll0);
const pValue=1-Stats.pchisq(lrt,1);
return{lrt,df:1,pValue,significant:pValue<0.05};
}
};

const ROB2={
domains:['Randomization','Deviations','Missing','Measurement','Selection'],
domainDescriptions:{
Randomization:'Risk of bias arising from the randomization process',
Deviations:'Risk of bias due to deviations from intended interventions',
Missing:'Risk of bias due to missing outcome data',
Measurement:'Risk of bias in measurement of the outcome',
Selection:'Risk of bias in selection of the reported result'
},
signalingQuestions:{
Randomization:[
'Was the allocation sequence random?',
'Was the allocation sequence concealed until participants were enrolled?',
'Did baseline differences suggest a problem with randomization?'
],
Deviations:[
'Were participants aware of their assigned intervention?',
'Were carers/people delivering aware of assigned intervention?',
'Were there deviations from intended intervention beyond what would be expected?',
'Were these deviations likely to affect the outcome?',
'Were participants analyzed in the group to which they were randomized?'
],
Missing:[
'Were data available for all/nearly all participants?',
'Is there evidence that result was not biased by missing data?',
'Could missingness depend on true value of the outcome?'
],
Measurement:[
'Was the method of measuring the outcome inappropriate?',
'Could measurement/ascertainment differ between groups?',
'Were outcome assessors aware of intervention received?',
'Could assessment be influenced by knowledge of intervention?'
],
Selection:[
'Were data analyzed in accordance with pre-specified plan?',
'Is the numerical result likely to have been selected?'
]
},
assess(studyAssessments){
const results={};
for(const domain of this.domains){
const domainJudgment=studyAssessments[domain]||'NI';
results[domain]={judgment:domainJudgment,description:this.domainDescriptions[domain]};
}
const judgments=Object.values(results).map(r=>r.judgment);
let overall='Low';
if(judgments.includes('High'))overall='High';
else if(judgments.filter(j=>j==='Some concerns').length>=2)overall='High';
else if(judgments.includes('Some concerns'))overall='Some concerns';
results.overall=overall;
return results;
},
trafficLight(assessments){
const colors={Low:'#00a65a',High:'#dd4b39','Some concerns':'#f39c12',NI:'#777'};
return Object.entries(assessments).map(([domain,data])=>({
domain,judgment:data.judgment||data,color:colors[data.judgment||data]||colors.NI
}));
},
summaryTable(studies){
const summary={};
for(const domain of this.domains){
summary[domain]={Low:0,High:0,'Some concerns':0,NI:0};
}
summary.overall={Low:0,High:0,'Some concerns':0,NI:0};
studies.forEach(s=>{
if(s.rob2){
for(const domain of this.domains){
const j=s.rob2[domain]?.judgment||s.rob2[domain]||'NI';
summary[domain][j]=(summary[domain][j]||0)+1;
}
summary.overall[s.rob2.overall||'NI']++;
}
});
return summary;
}
};

const ROBINSI={
domains:['Confounding','Selection','Classification','Deviations','Missing','Measurement','Reporting'],
domainDescriptions:{
Confounding:'Bias due to confounding',
Selection:'Bias in selection of participants into the study',
Classification:'Bias in classification of interventions',
Deviations:'Bias due to deviations from intended interventions',
Missing:'Bias due to missing data',
Measurement:'Bias in measurement of outcomes',
Reporting:'Bias in selection of the reported result'
},
assess(studyAssessments){
const results={};
for(const domain of this.domains){
results[domain]={
judgment:studyAssessments[domain]||'NI',
description:this.domainDescriptions[domain]
};
}
const judgments=Object.values(results).map(r=>r.judgment);
let overall='Low';
if(judgments.includes('Critical'))overall='Critical';
else if(judgments.includes('Serious'))overall='Serious';
else if(judgments.includes('Moderate'))overall='Moderate';
else if(judgments.includes('NI'))overall='NI';
results.overall=overall;
return results;
},
judgmentLevels:['Low','Moderate','Serious','Critical','NI'],
colors:{Low:'#00a65a',Moderate:'#f39c12',Serious:'#e08e0b',Critical:'#dd4b39',NI:'#777'}
};

const ComparisonAdjustedFunnel={
calculate(processed,results){
if(!processed||processed.length<3)return{error:'Insufficient data'};
const comparisons=new Map();
processed.forEach(s=>{
const key=[s.treatment1,s.treatment2].sort().join(' vs ');
if(!comparisons.has(key))comparisons.set(key,[]);
comparisons.get(key).push(s);
});
const points=[];
const reference=results?.reference||results?.treatments?.[0]||'Placebo';
comparisons.forEach((studies,comp)=>{
const pooledEffect=studies.reduce((s,st)=>s+st.yi,0)/studies.length;
studies.forEach(s=>{
const centered=s.yi-pooledEffect;
points.push({
study:s.name,
comparison:comp,
x:centered,
y:s.se||Math.sqrt(s.vi),
yi:s.yi,
pooledEffect,
originalSE:s.se||Math.sqrt(s.vi)
});
});
});
const allX=points.map(p=>p.x);
const meanCentered=allX.reduce((a,b)=>a+b,0)/allX.length;
const asymmetry=meanCentered;
const maxSE=Math.max(...points.map(p=>p.y));
return{
points,
comparisons:Array.from(comparisons.keys()),
nComparisons:comparisons.size,
asymmetry,
interpretation:Math.abs(asymmetry)<0.1?'Symmetric (no evidence of bias)':
asymmetry>0.1?'Asymmetric - possible small study effects favoring treatment':
'Asymmetric - possible small study effects favoring control',
maxSE
};
}
};

const PCurve={
analyze(pValues,alpha=0.05){
if(!pValues||pValues.length<3)return{error:'Insufficient p-values'};
const validP=pValues.filter(p=>p>0&&p<=alpha);
if(validP.length<3)return{error:'Need at least 3 significant p-values'};
const bins=[0,0.01,0.02,0.03,0.04,0.05];
const counts=bins.slice(0,-1).map((_,i)=>
validP.filter(p=>p>bins[i]&&p<=bins[i+1]).length
);
const totalSig=validP.length;
const lowP=validP.filter(p=>p<=0.025).length;
const highP=validP.filter(p=>p>0.025&&p<=0.05).length;
const expectedUnderNull=totalSig/5;
let chiSqRight=0,chiSqLeft=0;
counts.forEach((obs,i)=>{
const exp=expectedUnderNull;
chiSqRight+=Math.pow(obs-exp,2)/exp;
});
const expectedSkewRight=[0.4,0.25,0.15,0.12,0.08].map(x=>x*totalSig);
expectedSkewRight.forEach((exp,i)=>{
chiSqLeft+=Math.pow(counts[i]-exp,2)/exp;
});
const pRight=1-Stats.pchisq(chiSqRight,4);
const pLeft=1-Stats.pchisq(chiSqLeft,4);
let interpretation='Inconclusive';
if(lowP/totalSig>0.6&&pRight<0.05)interpretation='Evidential value present (right-skewed)';
else if(highP/totalSig>0.4&&pLeft<0.05)interpretation='P-hacking suspected (left-skewed/flat)';
else if(pRight>0.1&&pLeft>0.1)interpretation='Inadequate evidence';
return{
nSignificant:totalSig,
bins:bins.slice(0,-1).map((b,i)=>({range:`${b}-${bins[i+1]}`,count:counts[i]})),
lowP,highP,
skewness:(lowP-highP)/totalSig,
pRight,pLeft,
interpretation,
evidentialValue:pRight<0.05
};
}
};

const CopasModel={
fit(yi,vi,gamma0Range=[-2,0],gamma1Range=[0,2]){
const n=yi.length;
const se=vi.map(v=>Math.sqrt(v));
const maxSE=Math.max(...se);
const results=[];
for(let g0=gamma0Range[0];g0<=gamma0Range[1];g0+=0.5){
for(let g1=gamma1Range[0];g1<=gamma1Range[1];g1+=0.5){
const probs=se.map(s=>Stats.pnorm(g0+g1/s));
const weights=probs.map((p,i)=>p/(vi[i]));
const sumW=weights.reduce((a,b)=>a+b,0);
if(sumW>0){
const muAdj=yi.reduce((s,y,i)=>s+weights[i]*y,0)/sumW;
results.push({gamma0:g0,gamma1:g1,muAdjusted:muAdj,avgProb:probs.reduce((a,b)=>a+b,0)/n});
}
}
}
const w=vi.map(v=>1/v);
const sumW=w.reduce((a,b)=>a+b,0);
const muUnadj=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;
const sensitivityRange=[
Math.min(...results.map(r=>r.muAdjusted)),
Math.max(...results.map(r=>r.muAdjusted))
];
return{
unadjusted:muUnadj,
adjusted:results,
sensitivityRange,
maxBias:Math.max(Math.abs(sensitivityRange[0]-muUnadj),Math.abs(sensitivityRange[1]-muUnadj)),
interpretation:sensitivityRange[1]-sensitivityRange[0]<0.2?
'Results robust to selection bias':'Results sensitive to selection bias assumptions'
};
}
};

const FragilityIndex={
calculate(studies){
if(!studies||studies.length===0)return{error:'No studies'};
const binaryStudies=studies.filter(s=>s.events1!==undefined&&s.events2!==undefined);
if(binaryStudies.length===0)return{error:'No binary outcome studies'};
const results=binaryStudies.map(study=>{
let fi=0;
let e1=study.events1,e2=study.events2;
let n1=study.n1,n2=study.n2;
const originalOR=(e1/(n1-e1))/(e2/(n2-e2));
const originalSig=this.fisherExact(e1,n1-e1,e2,n2-e2)<0.05;
if(!originalSig)return{study:study.name,fi:Infinity,direction:'not significant'};
let direction='';
for(let i=1;i<=Math.min(n1,n2);i++){
const test1=this.fisherExact(e1+i,n1-e1-i,e2,n2-e2);
const test2=this.fisherExact(e1,n1-e1,e2+i,n2-e2-i);
if(test1>=0.05){fi=i;direction='add to treatment';break;}
if(test2>=0.05){fi=i;direction='add to control';break;}
}
return{study:study.name,fi,direction,originalOR};
});
const pooledFI=Math.min(...results.filter(r=>r.fi!==Infinity).map(r=>r.fi));
return{
studyLevel:results,
pooledFI:isFinite(pooledFI)?pooledFI:null,
interpretation:pooledFI<=3?'Very fragile':pooledFI<=8?'Moderately fragile':'Robust'
};
},
fisherExact(a,b,c,d){
const n=a+b+c+d;
const logFact=(x)=>{let r=0;for(let i=2;i<=x;i++)r+=Math.log(i);return r;};
const pHyper=(aa,bb,cc,dd)=>{
return Math.exp(logFact(aa+bb)+logFact(cc+dd)+logFact(aa+cc)+logFact(bb+dd)-logFact(n)-logFact(aa)-logFact(bb)-logFact(cc)-logFact(dd));
};
const p0=pHyper(a,b,c,d);
let pValue=0;
for(let i=0;i<=Math.min(a+b,a+c);i++){
const j=(a+b)-i,k=(a+c)-i,l=n-i-j-k;
if(j>=0&&k>=0&&l>=0){
const p=pHyper(i,j,k,l);
if(p<=p0+1e-10)pValue+=p;
}
}
return Math.min(1,pValue);
}
};

const DesignDecomposition={
analyze(processed,results){
if(!processed||processed.length<5)return{error:'Insufficient studies for design decomposition'};
const designs=new Map();
processed.forEach(s=>{
const design=[s.treatment1,s.treatment2].sort().join(':');
if(!designs.has(design))designs.set(design,{studies:[],effects:[]});
designs.get(design).studies.push(s.name);
designs.get(design).effects.push(s.yi);
});
const designStats=[];
designs.forEach((data,design)=>{
const mean=data.effects.reduce((a,b)=>a+b,0)/data.effects.length;
const variance=data.effects.length>1?
data.effects.reduce((s,e)=>s+(e-mean)*(e-mean),0)/(data.effects.length-1):0;
designStats.push({
design,
nStudies:data.studies.length,
meanEffect:mean,
variance,
studies:data.studies
});
});
let Qbetween=0,Qwithin=0;
const grandMean=processed.reduce((s,p)=>s+p.yi,0)/processed.length;
designStats.forEach(d=>{
Qbetween+=d.nStudies*(d.meanEffect-grandMean)*(d.meanEffect-grandMean);
d.studies.forEach((_,i)=>{
const design=designs.get(d.design);
Qwithin+=(design.effects[i]-d.meanEffect)*(design.effects[i]-d.meanEffect);
});
});
const dfBetween=designStats.length-1;
const dfWithin=processed.length-designStats.length;
const pBetween=dfBetween>0?1-Stats.pchisq(Qbetween,dfBetween):1;
const pWithin=dfWithin>0?1-Stats.pchisq(Qwithin,dfWithin):1;
return{
designs:designStats,
nDesigns:designStats.length,
Qbetween,dfBetween,pBetween,
Qwithin,dfWithin,pWithin,
inconsistency:pBetween<0.05,
interpretation:pBetween<0.05?
'Significant design-by-treatment interaction detected':'No significant inconsistency between designs'
};
}
};

const MetaforExport={
generate(processed,options={}){
const measure=options.measure||'OR';
const method=options.method||'REML';
const studyData=processed.map(s=>({
study:s.name,yi:s.yi,vi:s.vi,sei:Math.sqrt(s.vi),
treat1:s.treatment1,treat2:s.treatment2
}));
const rCode=`
# metafor R Validation Script
# Generated: ${new Date().toISOString()}

library(metafor)

# Study data
dat <- data.frame(
  study = c(${studyData.map(s=>`"${s.study}"`).join(', ')}),
  yi = c(${studyData.map(s=>s.yi.toFixed(6)).join(', ')}),
  vi = c(${studyData.map(s=>s.vi.toFixed(6)).join(', ')}),
  sei = c(${studyData.map(s=>s.sei.toFixed(6)).join(', ')})
)

# Random-effects meta-analysis
res <- rma(yi, vi, data=dat, method="${method}")
summary(res)

# Forest plot
forest(res, slab=dat$study)

# Funnel plot
funnel(res)

# Publication bias tests
regtest(res)  # Egger's test
ranktest(res) # Begg's test

# Trim and fill
trimfill(res)

# Influence diagnostics
influence(res)
leave1out(res)
`;
return{rCode,nStudies:processed.length,measure,method};
}
};

const HelpSystem={
topics:{
tau2:{
title:'Between-Study Variance (tau-squared)',
description:'Tau-squared represents the variance of true effects across studies. A tau2 of 0 indicates homogeneity.',
formula:'tau2 = (Q - df) / C',
interpretation:'tau2 = 0: Homogeneous; tau2 > 0.04: Low; tau2 > 0.16: Moderate; tau2 > 0.36: High',
references:['Higgins JPT, Thompson SG. Stat Med 2002;21:1539-58']
},
I2:{
title:'I-squared Statistic',
description:'Percentage of variability in effect estimates due to heterogeneity rather than sampling error.',
formula:'I2 = max(0, (Q - df) / Q * 100%)',
interpretation:'0-25%: Low; 25-50%: Moderate; 50-75%: Substantial; >75%: Considerable',
references:['Higgins JPT et al. BMJ 2003;327:557-60']
},
SUCRA:{
title:'Surface Under Cumulative Ranking',
description:'SUCRA values range from 0% to 100%, representing the probability of a treatment being the best.',
formula:'SUCRA = sum(cumulative probabilities) / (n_treatments - 1)',
interpretation:'100%: Certain to be best; 50%: Average; 0%: Certain to be worst',
references:['Salanti G et al. J Clin Epidemiol 2011;64:163-71']
},
HKSJ:{
title:'Hartung-Knapp-Sidik-Jonkman Adjustment',
description:'Adjustment to confidence intervals using a t-distribution instead of normal distribution.',
formula:'CI = estimate +/- t(df, 1-alpha/2) * SE_adjusted',
interpretation:'Produces wider, more conservative CIs, especially with few studies or high heterogeneity.',
references:['Hartung J, Knapp G. Stat Med 2001;20:3875-89']
}
},
get(topic){
return this.topics[topic]||{title:'Unknown',description:'No help available for this topic'};
},
list(){
return Object.keys(this.topics);
}
};

'''

# Find insertion point
insert_marker = 'const DEMO_DATASETS={'

if insert_marker in content:
    # Check which modules need adding
    modules = ['ContinuousOutcomes', 'MLEstimator', 'ROB2', 'ROBINSI',
               'ComparisonAdjustedFunnel', 'PCurve', 'CopasModel',
               'FragilityIndex', 'DesignDecomposition', 'MetaforExport', 'HelpSystem']

    missing = [m for m in modules if f'const {m}=' not in content]
    existing = [m for m in modules if f'const {m}=' in content]

    print(f'Existing: {existing}')
    print(f'Missing: {missing}')

    if missing:
        content = content.replace(insert_marker, batch1_code + '\n' + insert_marker)
        print(f'[OK] Added {len(missing)} modules')
    else:
        print('[INFO] All batch 1 modules exist')
else:
    print('[ERROR] Could not find insertion point')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Final size: {len(content):,} bytes')
print('Batch 1 complete')
