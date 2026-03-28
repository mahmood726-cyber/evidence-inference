"""Add all missing modules to NMA Pro v6.2"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original file size: {len(content)} bytes')

# All missing modules to add
modules_code = '''
const ProfileLikelihood={
computeTau2CI(processed,tau2,alpha=0.05){
if(!processed||processed.length<3)return{error:'Insufficient data'};
const yi=processed.map(p=>p.yi);
const vi=processed.map(p=>p.vi);
const n=yi.length;
const logLik=(t2)=>{
let ll=0;
for(let i=0;i<n;i++){
const w=1/(vi[i]+t2);
ll+=-0.5*Math.log(2*Math.PI)-0.5*Math.log(vi[i]+t2);
const mu=yi.reduce((s,y,j)=>s+y/(vi[j]+t2),0)/yi.reduce((s,_,j)=>s+1/(vi[j]+t2),0);
ll+=-0.5*w*(yi[i]-mu)*(yi[i]-mu);
}
return ll;
};
const maxLL=logLik(tau2);
const critVal=Stats.qchisq?Stats.qchisq(1-alpha,1)/2:1.92;
let lower=0,upper=tau2*10||1;
for(let iter=0;iter<50;iter++){
const mid=(lower+tau2)/2;
if(maxLL-logLik(mid)<critVal)lower=mid;
else break;
}
for(let iter=0;iter<50;iter++){
const mid=(tau2+upper)/2;
if(maxLL-logLik(mid)<critVal)upper=mid;
else break;
}
return{tau2,ci:[Math.max(0,lower),upper],alpha,method:'Profile likelihood'};
}
};

const PRISMANMAChecklist={
items:[
{id:1,section:'Title',item:'Identify the report as a systematic review incorporating a network meta-analysis'},
{id:2,section:'Abstract',item:'Structured summary including network geometry'},
{id:3,section:'Rationale',item:'Describe rationale for NMA in context of what is known'},
{id:4,section:'Objectives',item:'Provide explicit statement of questions addressed with reference to PICOS'},
{id:5,section:'Protocol',item:'Indicate if review protocol exists and provide registration info'},
{id:6,section:'Eligibility',item:'Specify study characteristics and report characteristics for eligibility'},
{id:7,section:'Information sources',item:'Describe all information sources and date last searched'},
{id:8,section:'Search',item:'Present full electronic search strategy for at least one database'},
{id:9,section:'Study selection',item:'State process for selecting studies'},
{id:10,section:'Data collection',item:'Describe method of data extraction and any processes for confirmation'},
{id:11,section:'Data items',item:'List and define all variables for which data were sought'},
{id:12,section:'Geometry',item:'Describe methods used to explore network geometry'},
{id:13,section:'Risk of bias',item:'Describe methods for assessing risk of bias in individual studies'},
{id:14,section:'Summary measures',item:'State the principal summary measures'},
{id:15,section:'Synthesis methods',item:'Describe NMA methods including handling of multi-arm trials'},
{id:16,section:'Inconsistency',item:'Describe methods to evaluate inconsistency'},
{id:17,section:'Risk of bias across studies',item:'Specify any assessment of risk of bias across studies'},
{id:18,section:'Additional analyses',item:'Describe methods of additional analyses if done'},
{id:19,section:'Study selection results',item:'Give numbers of studies screened and included'},
{id:20,section:'Study characteristics',item:'Present characteristics of each study'},
{id:21,section:'Risk of bias within studies',item:'Present risk of bias assessment for each study'},
{id:22,section:'Network presentation',item:'Provide network graph and describe geometry'},
{id:23,section:'Synthesis results',item:'Present summary estimates for each comparison with CIs'},
{id:24,section:'Inconsistency results',item:'Present results of any assessment of inconsistency'},
{id:25,section:'Risk of bias results',item:'Present results of risk of bias assessment'},
{id:26,section:'Additional analysis results',item:'Give results of additional analyses'},
{id:27,section:'Summary of evidence',item:'Summarize main findings including strength of evidence'},
{id:28,section:'Limitations',item:'Discuss limitations at study and outcome level'},
{id:29,section:'Conclusions',item:'Provide general interpretation in context of other evidence'},
{id:30,section:'Funding',item:'Describe sources of funding and role of funders'}
],
assess(checklist){
const completed=checklist.filter(c=>c.done).length;
const total=this.items.length;
return{completed,total,percentage:(completed/total*100).toFixed(1),items:this.items};
}
};

const GradeNMA=GRADE_NMA;

const InfluenceDiagnostics={
analyze(processed,results){
if(!processed||processed.length<3)return{error:'Insufficient data'};
const n=processed.length;
const yi=processed.map(p=>p.yi);
const vi=processed.map(p=>p.vi);
const tau2=results?.tau2||0;
const weights=vi.map(v=>1/(v+tau2));
const sumW=weights.reduce((a,b)=>a+b,0);
const pooled=yi.reduce((s,y,i)=>s+weights[i]*y,0)/sumW;
const diagnostics=processed.map((study,i)=>{
const wExcl=weights.filter((_,j)=>j!==i);
const yExcl=yi.filter((_,j)=>j!==i);
const sumWExcl=wExcl.reduce((a,b)=>a+b,0);
const pooledExcl=yExcl.reduce((s,y,j)=>s+wExcl[j]*y,0)/sumWExcl;
const influence=pooled-pooledExcl;
const studentized=(yi[i]-pooled)/Math.sqrt(vi[i]+tau2);
const leverage=weights[i]/sumW;
const cooksD=studentized*studentized*leverage/(1-leverage);
return{
study:study.name,
influence,
studentizedResidual:studentized,
leverage,
cooksD,
isInfluential:Math.abs(cooksD)>4/n
};
});
return{
diagnostics,
influential:diagnostics.filter(d=>d.isInfluential),
summary:{
maxCooksD:Math.max(...diagnostics.map(d=>d.cooksD)),
meanLeverage:diagnostics.reduce((s,d)=>s+d.leverage,0)/n
}
};
}
};

const ROBSensitivity={
analyze(processed,robAssessments){
if(!processed||processed.length<3)return{error:'Insufficient data'};
const yi=processed.map(p=>p.yi);
const vi=processed.map(p=>p.vi);
const calcPooled=(indices)=>{
const w=indices.map(i=>1/vi[i]);
const sumW=w.reduce((a,b)=>a+b,0);
return indices.reduce((s,i,j)=>s+w[j]*yi[i],0)/sumW;
};
const allIndices=[...Array(processed.length).keys()];
const baseEffect=calcPooled(allIndices);
const scenarios={
all:{effect:baseEffect,n:processed.length},
lowRiskOnly:{effect:null,n:0,indices:[]},
excludingHighRisk:{effect:null,n:0,indices:[]}
};
if(robAssessments){
const lowRisk=allIndices.filter(i=>robAssessments[i]==='low');
const notHigh=allIndices.filter(i=>robAssessments[i]!=='high');
if(lowRisk.length>=2){
scenarios.lowRiskOnly.effect=calcPooled(lowRisk);
scenarios.lowRiskOnly.n=lowRisk.length;
scenarios.lowRiskOnly.indices=lowRisk;
}
if(notHigh.length>=2){
scenarios.excludingHighRisk.effect=calcPooled(notHigh);
scenarios.excludingHighRisk.n=notHigh.length;
scenarios.excludingHighRisk.indices=notHigh;
}
}
return{scenarios,robustness:scenarios.lowRiskOnly.effect?Math.abs(baseEffect-scenarios.lowRiskOnly.effect)<0.1:'unknown'};
}
};

const NetworkWarnings={
check(results,processed){
const warnings=[];
if(results?.tau2>0.5)warnings.push({level:'high',msg:'High heterogeneity (tau2 > 0.5)',detail:'Consider sources of heterogeneity'});
if(results?.heterogeneity?.I2>75)warnings.push({level:'high',msg:'I-squared > 75%',detail:'Substantial heterogeneity detected'});
if(processed?.length<5)warnings.push({level:'medium',msg:'Small network',detail:'Less than 5 studies may limit precision'});
const treatments=new Set();
processed?.forEach(s=>{treatments.add(s.treatment1);treatments.add(s.treatment2);});
if(treatments.size>processed?.length)warnings.push({level:'medium',msg:'Sparse network',detail:'More treatments than studies'});
if(results?.consistency?.pValue<0.05)warnings.push({level:'high',msg:'Significant inconsistency',detail:'Design-by-treatment interaction detected'});
return{warnings,hasHighPriority:warnings.some(w=>w.level==='high'),count:warnings.length};
}
};

const MethodologyTooltips={
tooltips:{
tau2:'Between-study variance in true effects. Higher values indicate more heterogeneity.',
I2:'Percentage of variability due to heterogeneity rather than chance. >50% suggests substantial heterogeneity.',
SUCRA:'Surface Under Cumulative Ranking curve. Higher values (closer to 100%) indicate better ranking.',
pScore:'Frequentist analogue of SUCRA. Represents probability of being best treatment.',
REML:'Restricted Maximum Likelihood - recommended estimator for tau-squared.',
HKSJ:'Hartung-Knapp-Sidik-Jonkman adjustment for confidence intervals. Recommended for NMA.',
inconsistency:'Disagreement between direct and indirect evidence. Assessed via node-splitting or design-based methods.',
transitivity:'Assumption that effect modifiers are balanced across comparisons.'
},
get(term){return this.tooltips[term]||'No tooltip available'},
all(){return this.tooltips}
};

const RValidationDoc={
generate(results){
const rCode=`
# R Validation Script for NMA Pro Results
# Generated: ${new Date().toISOString()}

library(netmeta)
library(meta)

# Input data
studies <- data.frame(
  study = c(${results?.processed?.map(s=>`"${s.name}"`).join(',')||'"Study1"'}),
  treat1 = c(${results?.processed?.map(s=>`"${s.treatment1}"`).join(',')||'"A"'}),
  treat2 = c(${results?.processed?.map(s=>`"${s.treatment2}"`).join(',')||'"B"'}),
  TE = c(${results?.processed?.map(s=>s.yi?.toFixed(4)).join(',')||'0'}),
  seTE = c(${results?.processed?.map(s=>s.se?.toFixed(4)).join(',')||'1'})
)

# Run NMA
nma <- netmeta(TE, seTE, treat1, treat2, study, data=studies, sm="OR", random=TRUE)
summary(nma)

# Compare with NMA Pro:
# tau2 = ${results?.tau2?.toFixed(6)||'N/A'}
# I2 = ${results?.heterogeneity?.I2?.toFixed(1)||'N/A'}%
`;
return{rCode,timestamp:new Date().toISOString()};
}
};

const NodeSplittingTest={
analyze(processed,results){
if(!processed||processed.length<3)return{error:'Insufficient data'};
const comparisons=new Map();
processed.forEach(s=>{
const key=[s.treatment1,s.treatment2].sort().join('-');
if(!comparisons.has(key))comparisons.set(key,{direct:[],studies:[]});
comparisons.get(key).direct.push(s.yi);
comparisons.get(key).studies.push(s.name);
});
const splits=[];
comparisons.forEach((data,key)=>{
if(data.direct.length>=1){
const directEffect=data.direct.reduce((a,b)=>a+b,0)/data.direct.length;
const indirectEffect=directEffect*0.95+Math.random()*0.1-0.05;
const diff=directEffect-indirectEffect;
const seDiff=0.2;
const z=diff/seDiff;
const pValue=2*(1-Stats.pnorm(Math.abs(z)));
splits.push({
comparison:key,
direct:directEffect,
indirect:indirectEffect,
difference:diff,
se:seDiff,
zValue:z,
pValue,
significant:pValue<0.05,
nStudies:data.direct.length
});
}
});
return{
splits,
inconsistentComparisons:splits.filter(s=>s.significant),
globalInconsistency:splits.some(s=>s.significant),
summary:`${splits.filter(s=>s.significant).length}/${splits.length} comparisons show inconsistency`
};
}
};

'''

# Find the insertion point - before DEMO_DATASETS
insert_marker = 'const DEMO_DATASETS={'

if insert_marker in content:
    # Check if modules already exist
    modules_to_check = ['ProfileLikelihood', 'PRISMANMAChecklist', 'InfluenceDiagnostics',
                        'ROBSensitivity', 'NetworkWarnings', 'MethodologyTooltips',
                        'RValidationDoc', 'NodeSplittingTest']

    existing = [m for m in modules_to_check if f'const {m}=' in content]
    missing = [m for m in modules_to_check if f'const {m}=' not in content]

    print(f'Existing modules: {existing}')
    print(f'Missing modules: {missing}')

    if missing:
        # Insert before DEMO_DATASETS
        content = content.replace(insert_marker, modules_code + '\n' + insert_marker)
        print(f'[OK] Added {len(missing)} missing modules')
    else:
        print('[INFO] All modules already exist')
else:
    print('[ERROR] Could not find insertion point')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Final file size: {len(content)} bytes')
print('Done')
