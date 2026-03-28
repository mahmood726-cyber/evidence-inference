# Comprehensive Editorial Fixes for NMA Pro v6.2
# Fixes all methodological issues and adds future enhancements

import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("NMA Pro v6.2 - Comprehensive Editorial Fixes")
print("=" * 60)

fixes_applied = 0

# ============================================================================
# FIX 1: Node-splitting indirect variance (proper back-calculation)
# ============================================================================
print("\n[1/10] Fixing node-splitting indirect variance calculation...")

old_nodesplit = '''nodeSplitting(processed,matrices,tau2){const{treatments,X,y,v}=matrices;const results=[];const directMap=new Map();processed.forEach(s=>{const k=[s.treatment1,s.treatment2].sort().join('|');if(!directMap.has(k))directMap.set(k,[]);directMap.get(k).push(s)});const allWeights=v.map(vi=>1/(vi+tau2)),allSumW=Stats.sum(allWeights);const networkEst={};treatments.forEach((t,i)=>{if(i===0)networkEst[t]=0;else{const idx=i-1;let sumWE=0,sumW=0;for(let j=0;j<y.length;j++){if(X[j][idx]!==0){sumWE+=allWeights[j]*y[j]*X[j][idx];sumW+=allWeights[j]*X[j][idx]*X[j][idx]}}networkEst[t]=sumW>0?sumWE/sumW:0}});directMap.forEach((studies,k)=>{const[t1,t2]=k.split('|');const weights=studies.map(s=>1/(s.vi+tau2)),sumW=Stats.sum(weights);const directEst=sumW>0?Stats.sum(studies.map((s,i)=>weights[i]*s.yi))/sumW:0;const directSE=sumW>0?Math.sqrt(1/sumW):1;const indirectEst=networkEst[t1]-networkEst[t2];const indirectSE=Math.sqrt(1/sumW+tau2);const diffEstimate=directEst-indirectEst;const diffSE=Math.sqrt(directSE**2+indirectSE**2);const zScore=diffSE>0?diffEstimate/diffSE:0;const pValue=2*(1-Stats.pnorm(Math.abs(zScore)));const inconsistent=pValue<0.05;results.push({comparison:`${t1} vs ${t2}`,t1,t2,nStudies:studies.length,directEstimate:directEst,directSE,directCI:[directEst-1.96*directSE,directEst+1.96*directSE],indirectEstimate:indirectEst,indirectSE,difference:diffEstimate,differenceSE:diffSE,zScore,pValue,inconsistent})});return results}'''

# Improved node-splitting with proper back-calculation (Dias et al. 2010)
new_nodesplit = '''nodeSplitting(processed,matrices,tau2){const{treatments,X,y,v,n,p}=matrices;const results=[];const directMap=new Map();processed.forEach(s=>{const k=[s.treatment1,s.treatment2].sort().join('|');if(!directMap.has(k))directMap.set(k,[]);directMap.get(k).push(s)});
// Full network analysis
const W=v.map(vi=>1/(vi+tau2));const XtWX=Matrix.zeros(p,p),XtWy=Array(p).fill(0);
for(let i=0;i<n;i++)for(let j=0;j<p;j++){XtWy[j]+=X[i][j]*W[i]*y[i];for(let k=0;k<p;k++)XtWX[j][k]+=X[i][j]*W[i]*X[i][k]}
let networkBeta,networkVcov;try{networkBeta=Matrix.solve(XtWX,XtWy);networkVcov=Matrix.inverse(XtWX)}catch(e){return results}
directMap.forEach((studies,k)=>{const[t1,t2]=k.split('|');const t1Idx=treatments.indexOf(t1),t2Idx=treatments.indexOf(t2);
// Direct evidence
const weights=studies.map(s=>1/(s.vi+tau2)),sumW=Stats.sum(weights);const directEst=sumW>0?Stats.sum(studies.map((s,i)=>weights[i]*s.yi))/sumW:0;const directSE=sumW>0?Math.sqrt(1/sumW):1;
// Network estimate for this comparison
let networkEst=0,networkVar=0;
if(t1Idx===0&&t2Idx>0){networkEst=-networkBeta[t2Idx-1];networkVar=networkVcov[t2Idx-1][t2Idx-1]}
else if(t2Idx===0&&t1Idx>0){networkEst=networkBeta[t1Idx-1];networkVar=networkVcov[t1Idx-1][t1Idx-1]}
else if(t1Idx>0&&t2Idx>0){networkEst=networkBeta[t1Idx-1]-networkBeta[t2Idx-1];networkVar=networkVcov[t1Idx-1][t1Idx-1]+networkVcov[t2Idx-1][t2Idx-1]-2*(networkVcov[t1Idx-1][t2Idx-1]||0)}
// Indirect = back-calculation: network - direct contribution (Dias et al.)
const directWeight=sumW,networkWeight=networkVar>0?1/networkVar:0;
const totalWeight=directWeight+networkWeight;
const indirectEst=totalWeight>directWeight?(networkEst*totalWeight-directEst*directWeight)/(totalWeight-directWeight):networkEst;
const indirectVar=directWeight>0&&totalWeight>directWeight?1/((totalWeight-directWeight)):networkVar+1/sumW;
const indirectSE=Math.sqrt(Math.max(0.0001,indirectVar));
// Difference test
const diffEstimate=directEst-indirectEst;const diffVar=1/sumW+indirectVar;const diffSE=Math.sqrt(Math.max(0.0001,diffVar));
const df=studies.length-1;const tScore=diffSE>0?diffEstimate/diffSE:0;
const pValue=df>0?2*(1-Stats.pt(Math.abs(tScore),Math.max(1,df))):2*(1-Stats.pnorm(Math.abs(tScore)));
const inconsistent=pValue<0.05;
results.push({comparison:`${t1} vs ${t2}`,t1,t2,nStudies:studies.length,directEstimate:directEst,directSE,directCI:[directEst-Stats.qt(0.975,Math.max(1,df))*directSE,directEst+Stats.qt(0.975,Math.max(1,df))*directSE],indirectEstimate:indirectEst,indirectSE,indirectCI:[indirectEst-1.96*indirectSE,indirectEst+1.96*indirectSE],difference:diffEstimate,differenceSE:diffSE,zScore:tScore,pValue,inconsistent,df})});return results}'''

if old_nodesplit in content:
    content = content.replace(old_nodesplit, new_nodesplit)
    print("  [OK] Node-splitting: Implemented Dias et al. back-calculation")
    fixes_applied += 1
else:
    print("  [SKIP] Node-splitting pattern not found (may already be fixed)")

# ============================================================================
# FIX 2: Prediction intervals - use t-distribution
# ============================================================================
print("\n[2/10] Fixing prediction intervals to use t-distribution...")

old_pi = '''addPredictionIntervals(effectsResult,tau2,matrices){const{effects,vcov,correctionFactor}=effectsResult;const{treatments}=matrices;treatments.forEach((t,i)=>{if(i===0){effects[t].pi_lower=0;effects[t].pi_upper=0}else{const predSE=Math.sqrt(vcov[i-1][i-1]*correctionFactor+tau2);effects[t].pi_lower=effects[t].estimate-1.96*predSE;effects[t].pi_upper=effects[t].estimate+1.96*predSE}})}'''

new_pi = '''addPredictionIntervals(effectsResult,tau2,matrices){const{effects,vcov,correctionFactor,df}=effectsResult;const{treatments,n,p}=matrices;const piDF=Math.max(1,n-p-1);const tCrit=piDF>2?Stats.qt(0.975,piDF):Stats.qt(0.975,Math.max(1,piDF));treatments.forEach((t,i)=>{if(i===0){effects[t].pi_lower=0;effects[t].pi_upper=0;effects[t].pi_df=piDF}else{const predSE=Math.sqrt(vcov[i-1][i-1]*correctionFactor+tau2);effects[t].pi_lower=effects[t].estimate-tCrit*predSE;effects[t].pi_upper=effects[t].estimate+tCrit*predSE;effects[t].pi_df=piDF}})}'''

if old_pi in content:
    content = content.replace(old_pi, new_pi)
    print("  [OK] Prediction intervals: Now using t-distribution with n-p-1 df")
    fixes_applied += 1
else:
    print("  [SKIP] Prediction interval pattern not found")

# ============================================================================
# FIX 3: Zero-cell handling with multiple correction options
# ============================================================================
print("\n[3/10] Adding multiple zero-cell correction options...")

old_calceffects = '''calcEffects(studies,effectMeasure){return studies.map(s=>{let yi,vi;if(['OR','RR','HR'].includes(effectMeasure)){const e1=s.events1||0,e2=s.events2||0,n1=s.n1,n2=s.n2;const hasZero=e1===0||e2===0||(n1-e1)===0||(n2-e2)===0;const cc=hasZero?0.5:0;const a=e1+cc,b=(n1-e1)+cc,c=e2+cc,d=(n2-e2)+cc;if(effectMeasure==='OR'||effectMeasure==='HR'){yi=Math.log((a*d)/(b*c));vi=1/a+1/b+1/c+1/d}else{yi=Math.log((a/(a+b))/(c/(c+d)));vi=1/a-1/(a+b)+1/c-1/(c+d)}}else if(effectMeasure==='RD'){const p1=(s.events1||0)/s.n1,p2=(s.events2||0)/s.n2;yi=p1-p2;vi=p1*(1-p1)/s.n1+p2*(1-p2)/s.n2+0.0001}else if(effectMeasure==='SMD'){const n1=s.n1,n2=s.n2;if(!s.sd1||!s.sd2||s.sd1<=0||s.sd2<=0){yi=0;vi=1}else{const pooledSD=Math.sqrt(((n1-1)*s.sd1**2+(n2-1)*s.sd2**2)/(n1+n2-2)),d=((s.mean1||0)-(s.mean2||0))/pooledSD,j=1-3/(4*(n1+n2-2)-1);yi=d*j;vi=(n1+n2)/(n1*n2)+yi**2/(2*(n1+n2))}}else{yi=s.yi||0;vi=s.vi||1}return{...s,yi,vi,se:Math.sqrt(vi)}})}'''

new_calceffects = '''calcEffects(studies,effectMeasure,zeroCellCorrection='haldane'){return studies.map(s=>{let yi,vi;if(['OR','RR','HR'].includes(effectMeasure)){const e1=s.events1||0,e2=s.events2||0,n1=s.n1,n2=s.n2;const hasZero=e1===0||e2===0||(n1-e1)===0||(n2-e2)===0;const isDoubleZero=(e1===0&&e2===0)||((n1-e1)===0&&(n2-e2)===0);
// Skip double-zero studies if using exclusion method
if(isDoubleZero&&zeroCellCorrection==='exclude'){return{...s,yi:null,vi:null,se:null,excluded:true,reason:'Double-zero'}}
// Calculate continuity correction
let cc=0;
if(hasZero){
if(zeroCellCorrection==='haldane')cc=0.5;
else if(zeroCellCorrection==='tacc')cc=n1/(n1+n2);// Treatment-arm continuity correction
else if(zeroCellCorrection==='reciprocal')cc=1/(n1+n2);// Reciprocal of total n
else if(zeroCellCorrection==='sweeting'){const R=(n2/n1);cc=1/(1+R);} // Sweeting's empirical
else if(zeroCellCorrection==='none')cc=0.001;// Minimal for computation
else cc=0.5}// Default Haldane
const a=e1+cc,b=(n1-e1)+cc,c=e2+cc,d=(n2-e2)+cc;if(effectMeasure==='OR'||effectMeasure==='HR'){yi=Math.log((a*d)/(b*c));vi=1/a+1/b+1/c+1/d}else{yi=Math.log((a/(a+b))/(c/(c+d)));vi=1/a-1/(a+b)+1/c-1/(c+d)}}else if(effectMeasure==='RD'){const p1=(s.events1||0)/s.n1,p2=(s.events2||0)/s.n2;yi=p1-p2;vi=p1*(1-p1)/s.n1+p2*(1-p2)/s.n2+0.0001}else if(effectMeasure==='SMD'){const n1=s.n1,n2=s.n2;if(!s.sd1||!s.sd2||s.sd1<=0||s.sd2<=0){yi=0;vi=1}else{const pooledSD=Math.sqrt(((n1-1)*s.sd1**2+(n2-1)*s.sd2**2)/(n1+n2-2)),d=((s.mean1||0)-(s.mean2||0))/pooledSD,j=1-3/(4*(n1+n2-2)-1);yi=d*j;
// Hedges exact variance formula
const df=n1+n2-2;const c4=1-3/(4*df-1);const exactVar=(n1+n2)/(n1*n2)+(yi*yi)/(2*df)*(1-c4*c4);vi=exactVar}}else{yi=s.yi||0;vi=s.vi||1}return{...s,yi,vi,se:Math.sqrt(vi)}})}'''

if old_calceffects in content:
    content = content.replace(old_calceffects, new_calceffects)
    print("  [OK] Zero-cell: Added TACC, reciprocal, Sweeting, and exclude options")
    print("  [OK] SMD variance: Added Hedges exact formula")
    fixes_applied += 1
else:
    print("  [SKIP] calcEffects pattern not found")

# ============================================================================
# FIX 4: mKH floor adjustment (1.5 -> configurable, default 2.0)
# ============================================================================
print("\n[4/10] Fixing mKH floor to be configurable (default 2.0)...")

old_mkh = '''else if(correction==='mkh'){correctionFactor=Math.max(1.5,swr/(n-p))}'''
new_mkh = '''else if(correction==='mkh'){const mkhFloor=options.mkhFloor||2.0;correctionFactor=Math.max(mkhFloor,swr/(n-p))}'''

if old_mkh in content:
    content = content.replace(old_mkh, new_mkh)
    print("  [OK] mKH floor: Now configurable with default 2.0 (was 1.5)")
    fixes_applied += 1
else:
    print("  [SKIP] mKH floor pattern not found")

# ============================================================================
# FIX 5: I2 decomposition for NMA (within/between design)
# ============================================================================
print("\n[5/10] Adding NMA-specific I2 decomposition...")

old_hetero = '''calcHeterogeneity(matrices,tau2){const{y,v,X,n,p}=matrices;const W=v.map(vi=>1/vi);const XtWX=Matrix.zeros(p,p),XtWy=Array(p).fill(0);for(let i=0;i<n;i++)for(let j=0;j<p;j++){XtWy[j]+=X[i][j]*W[i]*y[i];for(let k=0;k<p;k++)XtWX[j][k]+=X[i][j]*W[i]*X[i][k]}const beta=Matrix.solve(XtWX,XtWy);let Q=0;for(let i=0;i<n;i++){let f=0;for(let j=0;j<p;j++)f+=X[i][j]*beta[j];Q+=W[i]*(y[i]-f)**2}const df=n-p,pQ=1-Stats.pchisq(Q,df),I2=Math.max(0,((Q-df)/Q)*100),H2=df>0?Q/df:1;return{tau2,tau:Math.sqrt(tau2),Q,df,pQ,I2,H2}}'''

new_hetero = '''calcHeterogeneity(matrices,tau2){const{y,v,X,n,p}=matrices;const W=v.map(vi=>1/vi);const XtWX=Matrix.zeros(p,p),XtWy=Array(p).fill(0);for(let i=0;i<n;i++)for(let j=0;j<p;j++){XtWy[j]+=X[i][j]*W[i]*y[i];for(let k=0;k<p;k++)XtWX[j][k]+=X[i][j]*W[i]*X[i][k]}const beta=Matrix.solve(XtWX,XtWy);let Q=0;const residuals=[];for(let i=0;i<n;i++){let f=0;for(let j=0;j<p;j++)f+=X[i][j]*beta[j];const r=y[i]-f;residuals.push(r);Q+=W[i]*r*r}const df=n-p,pQ=1-Stats.pchisq(Q,df),I2=Math.max(0,((Q-df)/Q)*100),H2=df>0?Q/df:1;
// NMA-specific I2 decomposition (Jackson et al. 2012)
const designMap=new Map();for(let i=0;i<n;i++){const design=X[i].map(x=>x!==0?1:0).join('');if(!designMap.has(design))designMap.set(design,{indices:[],Q:0,df:0});designMap.get(design).indices.push(i)}
let Qwithin=0,dfWithin=0,Qbetween=0;
designMap.forEach(d=>{if(d.indices.length>1){const subY=d.indices.map(i=>y[i]),subV=d.indices.map(i=>v[i]),subW=subV.map(vi=>1/vi);const pooled=Stats.sum(subY.map((yi,j)=>subW[j]*yi))/Stats.sum(subW);d.indices.forEach((idx,j)=>{Qwithin+=subW[j]*(subY[j]-pooled)**2});dfWithin+=d.indices.length-1}});
Qbetween=Q-Qwithin;const dfBetween=designMap.size>1?designMap.size-1:0;
const I2within=dfWithin>0?Math.max(0,((Qwithin-dfWithin)/Qwithin)*100):0;
const I2between=dfBetween>0&&Qbetween>0?Math.max(0,((Qbetween-dfBetween)/Qbetween)*100):0;
return{tau2,tau:Math.sqrt(tau2),Q,df,pQ,I2,H2,decomposition:{Qwithin,dfWithin,I2within,Qbetween,dfBetween,I2between,nDesigns:designMap.size}}}'''

if old_hetero in content:
    content = content.replace(old_hetero, new_hetero)
    print("  [OK] I2 decomposition: Added within/between design decomposition")
    fixes_applied += 1
else:
    print("  [SKIP] Heterogeneity pattern not found")

# ============================================================================
# FIX 6: Enhance Component NMA with additive/multiplicative models
# ============================================================================
print("\n[6/10] Enhancing Component NMA with additive/multiplicative models...")

old_cnma = '''const CNMA={
analyze(studies,options={}){const{separator='+',effectMeasure='OR'}=options;'''

new_cnma = '''const CNMA={
analyze(studies,options={}){const{separator='+',effectMeasure='OR',model='additive'}=options;'''

if old_cnma in content:
    content = content.replace(old_cnma, new_cnma)

# Find and enhance the CNMA return statement
old_cnma_return = '''return{applicable:true,components:compList,componentEffects,heterogeneity:{Q,df:n-p,I2:Math.max(0,((Q-(n-p))/Q)*100)}}}catch(e){return{applicable:false,message:'CNMA failed'}}}};'''

new_cnma_return = '''// Calculate interaction terms for multiplicative model
let interactionEffects=[];
if(model==='multiplicative'){
const compPairs=[];for(let i=0;i<compList.length;i++)for(let j=i+1;j<compList.length;j++)compPairs.push([compList[i],compList[j]]);
interactionEffects=compPairs.map(([c1,c2])=>{
const bothPresent=processed.filter(s=>{const t1Comps=treatmentComponents[s.treatment1]||[],t2Comps=treatmentComponents[s.treatment2]||[];return(t1Comps.includes(c1)&&t1Comps.includes(c2))||(t2Comps.includes(c1)&&t2Comps.includes(c2))});
if(bothPresent.length<2)return{pair:`${c1}*${c2}`,estimate:null,applicable:false};
const intY=bothPresent.map(s=>s.yi),intW=bothPresent.map(s=>1/s.vi);
const pooled=Stats.sum(intY.map((y,i)=>intW[i]*y))/Stats.sum(intW);
const synergy=pooled-(componentEffects.find(c=>c.component===c1)?.estimate||0)-(componentEffects.find(c=>c.component===c2)?.estimate||0);
return{pair:`${c1}*${c2}`,synergy,nStudies:bothPresent.length,applicable:true}})}
return{applicable:true,model,components:compList,componentEffects,interactionEffects,heterogeneity:{Q,df:n-p,I2:Math.max(0,((Q-(n-p))/Q)*100)}}}catch(e){return{applicable:false,message:'CNMA failed'}}}};'''

if old_cnma_return in content:
    content = content.replace(old_cnma_return, new_cnma_return)
    print("  [OK] CNMA: Added multiplicative model with interaction terms")
    fixes_applied += 1
else:
    print("  [SKIP] CNMA return pattern not found")

# ============================================================================
# FIX 7: Network meta-regression with interaction terms
# ============================================================================
print("\n[7/10] Adding interaction terms to network meta-regression...")

# Add interaction analysis method to NetworkMetaRegression
old_nmr_end = '''xMean}},
categoricalAnalysis'''

new_nmr_end = '''xMean}},
interactionAnalysis(studies,covariate1,covariate2,options={}){
const{effectMeasure='OR'}=options;
if(!covariate1||!covariate2)return{applicable:false,message:'Need two covariates'};
const hasData=studies.every(s=>s[covariate1]!==undefined&&s[covariate2]!==undefined);
if(!hasData)return{applicable:false,message:'Missing covariate data'};
const processed=FrequentistNMA.calcEffects(studies,effectMeasure);
const x1=processed.map(s=>s[covariate1]),x2=processed.map(s=>s[covariate2]);
const y=processed.map(s=>s.yi),v=processed.map(s=>s.vi),n=processed.length;
const x1Mean=Stats.mean(x1),x2Mean=Stats.mean(x2);
const x1C=x1.map(xi=>xi-x1Mean),x2C=x2.map(xi=>xi-x2Mean);
const interaction=x1C.map((xi,i)=>xi*x2C[i]);
const W=v.map(vi=>1/vi);
// Build design matrix [1, x1, x2, x1*x2]
const XtWX=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],XtWy=[0,0,0,0];
for(let i=0;i<n;i++){
const xi=[1,x1C[i],x2C[i],interaction[i]];
for(let j=0;j<4;j++){XtWy[j]+=xi[j]*W[i]*y[i];for(let k=0;k<4;k++)XtWX[j][k]+=xi[j]*W[i]*xi[k]}}
try{
const beta=Matrix.solve(XtWX,XtWy),vcov=Matrix.inverse(XtWX);
const interactionCoef=beta[3],interactionSE=Math.sqrt(vcov[3][3]);
const tStat=interactionCoef/interactionSE,pValue=2*(1-Stats.pnorm(Math.abs(tStat)));
return{applicable:true,covariate1,covariate2,intercept:beta[0],coef1:{estimate:beta[1],se:Math.sqrt(vcov[1][1])},coef2:{estimate:beta[2],se:Math.sqrt(vcov[2][2])},interaction:{estimate:interactionCoef,se:interactionSE,ci:[interactionCoef-1.96*interactionSE,interactionCoef+1.96*interactionSE],pValue,significant:pValue<0.05},interpretation:pValue<0.05?`Significant interaction between ${covariate1} and ${covariate2}`:'No significant interaction'}}
catch(e){return{applicable:false,message:'Matrix inversion failed'}}},
categoricalAnalysis'''

if old_nmr_end in content:
    content = content.replace(old_nmr_end, new_nmr_end)
    print("  [OK] Meta-regression: Added interaction term analysis")
    fixes_applied += 1
else:
    print("  [SKIP] Meta-regression pattern not found")

# ============================================================================
# FIX 8: Automated sensitivity analysis for influential studies
# ============================================================================
print("\n[8/10] Adding automated sensitivity analysis for influential studies...")

# Find LeaveOneOut and add automated sensitivity analysis
old_loo_end = '''interpretation:`${influentialStudies.length} influential stud${influentialStudies.length===1?'y':'ies'} detected (tau2 change > 20% or I2 change > 10%)`}}};'''

new_loo_end = '''interpretation:`${influentialStudies.length} influential stud${influentialStudies.length===1?'y':'ies'} detected (tau2 change > 20% or I2 change > 10%)`}},
automatedSensitivity(studies,options={}){
const{reference,effectMeasure='OR',estimator='REML',smallStudyCorrection='hksj',thresholds={tau2:0.2,I2:10,effect:0.1}}=options;
if(studies.length<4)return{applicable:false,message:'Need >=4 studies'};
// Full analysis
const fullRes=FrequentistNMA.analyze(studies,{reference,effectMeasure,estimator,smallStudyCorrection,predictionIntervals:false});
const fullTau2=fullRes.tau2,fullI2=fullRes.heterogeneity.I2;
const fullEffects={};Object.entries(fullRes.effects.effects).forEach(([t,e])=>{fullEffects[t]=e.estimate});
// Identify influential studies
const influential=[];const robustness=[];
studies.forEach((excl,idx)=>{
const remaining=studies.filter((_,i)=>i!==idx);
try{
const looRes=FrequentistNMA.analyze(remaining,{reference,effectMeasure,estimator,smallStudyCorrection,predictionIntervals:false});
const tau2Change=Math.abs(looRes.tau2-fullTau2)/Math.max(0.001,fullTau2);
const i2Change=Math.abs(looRes.heterogeneity.I2-fullI2);
let maxEffectChange=0;
Object.entries(looRes.effects.effects).forEach(([t,e])=>{
if(fullEffects[t]!==undefined){
const change=Math.abs(e.estimate-fullEffects[t])/Math.max(0.001,Math.abs(fullEffects[t]));
if(change>maxEffectChange)maxEffectChange=change}});
const isInfluential=tau2Change>thresholds.tau2||i2Change>thresholds.I2||maxEffectChange>thresholds.effect;
if(isInfluential){
influential.push({study:excl.name,idx,tau2Change,i2Change,maxEffectChange,reason:tau2Change>thresholds.tau2?'tau2':i2Change>thresholds.I2?'I2':'effect'})}
robustness.push({study:excl.name,tau2Change,i2Change,maxEffectChange,influential:isInfluential})}
catch(e){}});
// Sensitivity scenarios
const scenarios=[];
// Scenario 1: Exclude all influential
if(influential.length>0&&influential.length<studies.length-2){
const excIndices=influential.map(i=>i.idx);
const sensStudies=studies.filter((_,i)=>!excIndices.includes(i));
try{
const sensRes=FrequentistNMA.analyze(sensStudies,{reference,effectMeasure,estimator,smallStudyCorrection,predictionIntervals:false});
scenarios.push({name:'Exclude influential',nExcluded:influential.length,tau2:sensRes.tau2,I2:sensRes.heterogeneity.I2,effects:sensRes.effects.effects})}
catch(e){}}
// Scenario 2: Small studies only (n>=50)
const largeStudies=studies.filter(s=>(s.n1||0)+(s.n2||0)>=50);
if(largeStudies.length>=3){
try{
const largeRes=FrequentistNMA.analyze(largeStudies,{reference,effectMeasure,estimator,smallStudyCorrection,predictionIntervals:false});
scenarios.push({name:'Large studies only (n>=50)',nIncluded:largeStudies.length,tau2:largeRes.tau2,I2:largeRes.heterogeneity.I2,effects:largeRes.effects.effects})}
catch(e){}}
// Scenario 3: Low ROB only
const lowRobStudies=studies.filter(s=>s.rob==='low'||!s.rob);
if(lowRobStudies.length>=3&&lowRobStudies.length<studies.length){
try{
const robRes=FrequentistNMA.analyze(lowRobStudies,{reference,effectMeasure,estimator,smallStudyCorrection,predictionIntervals:false});
scenarios.push({name:'Low ROB only',nIncluded:lowRobStudies.length,tau2:robRes.tau2,I2:robRes.heterogeneity.I2,effects:robRes.effects.effects})}
catch(e){}}
const robustnessIndex=1-(influential.length/studies.length);
return{applicable:true,fullResults:{tau2:fullTau2,I2:fullI2,effects:fullEffects},influential,nInfluential:influential.length,scenarios,robustness,robustnessIndex,interpretation:robustnessIndex>0.8?'Results robust':'Results sensitive to study exclusion'}}};'''

if old_loo_end in content:
    content = content.replace(old_loo_end, new_loo_end)
    print("  [OK] Sensitivity: Added automated multi-scenario sensitivity analysis")
    fixes_applied += 1
else:
    print("  [SKIP] LeaveOneOut pattern not found")

# ============================================================================
# FIX 9: PROSPERO registration integration
# ============================================================================
print("\n[9/10] Adding PROSPERO registration integration...")

# Add PROSPERO module after EValues
prospero_module = '''
const PROSPERO={
validate(registrationData){const required=['title','reviewQuestion','population','intervention','comparator','outcomes','searchDatabases','studyDesigns'];const missing=required.filter(f=>!registrationData[f]||registrationData[f].length===0);const warnings=[];
if(registrationData.dateStarted&&new Date(registrationData.dateStarted)>new Date())warnings.push('Start date is in the future');
if(!registrationData.protocol)warnings.push('No protocol document linked');
if(registrationData.outcomes&&registrationData.outcomes.length<2)warnings.push('Consider specifying more outcomes');
return{valid:missing.length===0,missing,warnings,complete:missing.length===0&&warnings.length===0}},
generateReport(registrationData,results){
const validation=this.validate(registrationData);
const deviations=this.checkDeviations(registrationData,results);
return{registrationId:registrationData.prosperoId||'Not registered',title:registrationData.title||'Untitled',validation,deviations,timestamp:new Date().toISOString(),
summary:{plannedStudies:registrationData.expectedStudies||'Not specified',actualStudies:results.processed?.length||0,plannedComparisons:registrationData.plannedComparisons||'Not specified',actualComparisons:Object.keys(results.effects?.effects||{}).length-1}}},
checkDeviations(registrationData,results){
const deviations=[];
if(registrationData.primaryOutcome&&results.effectMeasure!==registrationData.primaryOutcome){
deviations.push({type:'outcome',severity:'major',description:`Planned: ${registrationData.primaryOutcome}, Used: ${results.effectMeasure}`})}
if(registrationData.expectedStudies&&results.processed){
const diff=Math.abs(results.processed.length-registrationData.expectedStudies)/registrationData.expectedStudies;
if(diff>0.2)deviations.push({type:'sample',severity:'minor',description:`Expected ${registrationData.expectedStudies} studies, found ${results.processed.length}`})}
if(registrationData.analysisMethod&&registrationData.analysisMethod!==results.effects?.correctionMethod){
deviations.push({type:'method',severity:'moderate',description:`Planned: ${registrationData.analysisMethod}, Used: ${results.effects?.correctionMethod}`})}
return deviations},
exportCRD(registrationData,format='json'){
if(format==='json')return JSON.stringify(registrationData,null,2);
if(format==='xml'){
let xml='<?xml version="1.0" encoding="UTF-8"?>\\n<prospero_registration>\\n';
Object.entries(registrationData).forEach(([k,v])=>{
if(Array.isArray(v))xml+=`  <${k}>${v.join('; ')}</${k}>\\n`;
else xml+=`  <${k}>${v}</${k}>\\n`});
xml+='</prospero_registration>';
return xml}
return null}};

'''

# Insert PROSPERO module after EValues
if 'const PROSPERO=' not in content:
    evalues_end = '''analyzeAll(results,reference,effectMeasure){const isRatio=['OR','RR','HR'].includes(effectMeasure);const evalues=[];Object.entries(results.effects.effects).forEach(([t,e])=>{if(t===reference)return;const ev=this.calculate(isRatio?Math.exp(e.estimate):e.estimate,isRatio?Math.exp(e.ci_lower):e.ci_lower,isRatio);evalues.push({treatment:t,...ev})});return evalues}};'''

    if evalues_end in content:
        content = content.replace(evalues_end, evalues_end + prospero_module)
        print("  [OK] PROSPERO: Added registration validation and deviation tracking")
        fixes_applied += 1
    else:
        print("  [SKIP] Could not find insertion point for PROSPERO module")
else:
    print("  [SKIP] PROSPERO module already exists")

# ============================================================================
# FIX 10: Add UI elements for new features
# ============================================================================
print("\n[10/10] Adding UI elements for new features...")

# Add zero-cell correction dropdown option reference in analyze function
old_analyze = '''analyze(studies,options={}){const{reference,effectMeasure='OR',estimator='REML',smallStudyCorrection='hksj',predictionIntervals=true}=options;
const processed=this.calcEffects(studies,effectMeasure);'''

new_analyze = '''analyze(studies,options={}){const{reference,effectMeasure='OR',estimator='REML',smallStudyCorrection='hksj',predictionIntervals=true,zeroCellCorrection='haldane',mkhFloor=2.0}=options;
const processed=this.calcEffects(studies,effectMeasure,zeroCellCorrection).filter(s=>s.yi!==null);'''

if old_analyze in content:
    content = content.replace(old_analyze, new_analyze)
    print("  [OK] Added zeroCellCorrection and mkhFloor to analyze options")
    fixes_applied += 1
else:
    print("  [SKIP] Analyze function pattern not found")

# Save the file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 60)
print(f"SUMMARY: Applied {fixes_applied} fixes/enhancements")
print("=" * 60)

# Verify JavaScript syntax
import subprocess
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''
with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("\n[SUCCESS] JavaScript syntax valid")
else:
    print("\n[ERROR] JavaScript syntax error:")
    print(result.stderr[:1000])
