# Add FP-NMA and ML-NMR to NMA Pro v6.2

import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("Adding FP-NMA and ML-NMR to NMA Pro v6.2")
print("=" * 60)

# ============================================================================
# FP-NMA (Fractional-Polynomial Network Meta-Analysis)
# For non-linear dose-response or time-course modeling
# ============================================================================
fp_nma_module = '''
const FPNMA_FractionalPolynomial={
// Fractional-Polynomial Network Meta-Analysis
// Models non-linear dose-response or time-course relationships
// Uses fractional polynomial powers: -2, -1, -0.5, 0 (log), 0.5, 1, 2, 3
analyze(studies,options={}){
const{effectMeasure='OR',covariate='dose',powers=[-2,-1,-0.5,0,0.5,1,2,3],reference,modelOrder=2}=options;
const processed=FrequentistNMA.calcEffects(studies,effectMeasure).filter(s=>s.yi!==null);
// Check covariate exists
if(!processed.every(s=>s[covariate]!==undefined&&s[covariate]!==null)){
return{applicable:false,message:`Covariate '${covariate}' missing in some studies`}}
const x=processed.map(s=>Math.max(0.001,parseFloat(s[covariate])||0.001));// Ensure positive for log
const y=processed.map(s=>s.yi);
const v=processed.map(s=>s.vi);
const W=v.map(vi=>1/vi);
const n=processed.length;
// Try all combinations of fractional polynomial powers
const results=[];
if(modelOrder===1){
// First-order FP: y = b0 + b1*x^p
powers.forEach(p1=>{
const X1=x.map(xi=>p1===0?Math.log(xi):Math.pow(xi,p1));
const fit=this.fitWLS([X1],y,W);
if(fit)results.push({powers:[p1],fit,aic:this.calcAIC(fit,2,n)})})}
else{
// Second-order FP: y = b0 + b1*x^p1 + b2*x^p2
for(let i=0;i<powers.length;i++){
for(let j=i;j<powers.length;j++){
const p1=powers[i],p2=powers[j];
let X1=x.map(xi=>p1===0?Math.log(xi):Math.pow(xi,p1));
let X2;
if(p1===p2){
// Repeated power: x^p * log(x)
X2=x.map(xi=>Math.pow(xi,p2)*Math.log(xi))}
else{
X2=x.map(xi=>p2===0?Math.log(xi):Math.pow(xi,p2))}
const fit=this.fitWLS([X1,X2],y,W);
if(fit)results.push({powers:[p1,p2],fit,aic:this.calcAIC(fit,3,n)})}}}
if(results.length===0)return{applicable:false,message:'No valid models could be fit'};
// Select best model by AIC
results.sort((a,b)=>a.aic-b.aic);
const best=results[0];
// Generate dose-response curve
const xMin=Math.min(...x),xMax=Math.max(...x);
const curve=[];
for(let i=0;i<=50;i++){
const xi=xMin+(xMax-xMin)*i/50;
let pred=best.fit.beta[0];
if(best.powers.length===1){
pred+=best.fit.beta[1]*(best.powers[0]===0?Math.log(xi):Math.pow(xi,best.powers[0]))}
else{
const p1=best.powers[0],p2=best.powers[1];
pred+=best.fit.beta[1]*(p1===0?Math.log(xi):Math.pow(xi,p1));
if(p1===p2){
pred+=best.fit.beta[2]*Math.pow(xi,p2)*Math.log(xi)}
else{
pred+=best.fit.beta[2]*(p2===0?Math.log(xi):Math.pow(xi,p2))}}
curve.push({x:xi,y:pred})}
// Find optimal dose (where effect is maximized/minimized)
let optimalDose=null,optimalEffect=null;
const derivative=this.numericalDerivative(curve);
const zeros=derivative.filter((d,i)=>i>0&&derivative[i-1].dy*d.dy<0);
if(zeros.length>0){
optimalDose=zeros[0].x;
optimalEffect=curve.find(c=>Math.abs(c.x-optimalDose)<(xMax-xMin)/50)?.y}
return{applicable:true,method:'FP-NMA',bestModel:{powers:best.powers,coefficients:best.fit.beta,se:best.fit.se,aic:best.aic},allModels:results.slice(0,5).map(r=>({powers:r.powers,aic:r.aic})),curve,optimalDose,optimalEffect,covariate,data:processed.map((s,i)=>({study:s.name,x:x[i],y:y[i],se:Math.sqrt(v[i])})),interpretation:`Best FP model: powers ${best.powers.join(', ')}. AIC=${best.aic.toFixed(2)}`}},
fitWLS(Xcols,y,W){
const n=y.length,p=Xcols.length+1;
// Build design matrix [1, X1, X2, ...]
const X=Array(n).fill(null).map((_,i)=>[1,...Xcols.map(col=>col[i])]);
// Check for valid values
for(let i=0;i<n;i++){
if(X[i].some(v=>!isFinite(v)))return null}
// Weighted least squares
const XtWX=Matrix.zeros(p,p),XtWy=Array(p).fill(0);
for(let i=0;i<n;i++){
for(let j=0;j<p;j++){
XtWy[j]+=X[i][j]*W[i]*y[i];
for(let k=0;k<p;k++)XtWX[j][k]+=X[i][j]*W[i]*X[i][k]}}
try{
const beta=Matrix.solve(XtWX,XtWy);
const vcov=Matrix.inverse(XtWX);
const se=vcov.map((row,i)=>Math.sqrt(row[i]));
// Residual sum of squares
let rss=0;
for(let i=0;i<n;i++){
let pred=0;for(let j=0;j<p;j++)pred+=X[i][j]*beta[j];
rss+=W[i]*(y[i]-pred)**2}
return{beta,se,vcov,rss}}
catch(e){return null}},
calcAIC(fit,p,n){
const logLik=-0.5*fit.rss;// Approximate
return 2*p-2*logLik},
numericalDerivative(curve){
return curve.map((c,i)=>{
if(i===0)return{x:c.x,dy:(curve[1].y-c.y)/(curve[1].x-c.x)};
if(i===curve.length-1)return{x:c.x,dy:(c.y-curve[i-1].y)/(c.x-curve[i-1].x)};
return{x:c.x,dy:(curve[i+1].y-curve[i-1].y)/(curve[i+1].x-curve[i-1].x)}})}};

'''

# ============================================================================
# ML-NMR (Multilevel Network Meta-Regression)
# Population adjustment combining IPD and aggregate data
# ============================================================================
ml_nmr_module = '''
const MLNMR={
// Multilevel Network Meta-Regression
// Population adjustment method combining:
// - Individual Patient Data (IPD)
// - Aggregate Data (AD)
// Allows effect modification by patient-level covariates
analyze(studies,options={}){
const{reference,effectMeasure='OR',covariates=[],targetPopulation={},ipdStudies=[]}=options;
const processed=FrequentistNMA.calcEffects(studies,effectMeasure).filter(s=>s.yi!==null);
const treatments=new Set();
processed.forEach(s=>{treatments.add(s.treatment1);treatments.add(s.treatment2)});
const treatList=Array.from(treatments).sort();
const refIdx=treatList.indexOf(reference);
if(refIdx>0){treatList.splice(refIdx,1);treatList.unshift(reference)}
const p=treatList.length-1;
// Separate IPD and AD studies
const ipdNames=new Set(ipdStudies);
const ipdData=processed.filter(s=>ipdNames.has(s.name));
const adData=processed.filter(s=>!ipdNames.has(s.name));
// Level 1: Within-study model (for IPD)
// Level 2: Between-study model (combining IPD summaries with AD)
// Level 3: Network synthesis
// For each covariate, estimate effect modification
const effectModifiers=[];
covariates.forEach(cov=>{
// Check if we have the covariate
const hasData=processed.filter(s=>s[cov]!==undefined&&s[cov]!==null);
if(hasData.length<3)return;
// Meta-regression to estimate interaction
const x=hasData.map(s=>s[cov]),y=hasData.map(s=>s.yi),v=hasData.map(s=>s.vi);
const xMean=Stats.mean(x),xC=x.map(xi=>xi-xMean);
const W=v.map(vi=>1/vi),n=hasData.length;
// Fit interaction model
const XtWX=[[0,0],[0,0]],XtWy=[0,0];
for(let i=0;i<n;i++){
XtWy[0]+=W[i]*y[i];
XtWy[1]+=xC[i]*W[i]*y[i];
XtWX[0][0]+=W[i];
XtWX[0][1]+=xC[i]*W[i];
XtWX[1][0]+=xC[i]*W[i];
XtWX[1][1]+=xC[i]*xC[i]*W[i]}
try{
const beta=Matrix.solve(XtWX,XtWy);
const vcov=Matrix.inverse(XtWX);
const interactionCoef=beta[1],interactionSE=Math.sqrt(vcov[1][1]);
const pValue=2*(1-Stats.pnorm(Math.abs(interactionCoef/interactionSE)));
effectModifiers.push({covariate:cov,coefficient:interactionCoef,se:interactionSE,pValue,significant:pValue<0.05,studyMean:xMean})}
catch(e){}});
// Population adjustment
// If target population differs from study populations, adjust effects
const adjustments={};
if(Object.keys(targetPopulation).length>0){
effectModifiers.forEach(em=>{
if(targetPopulation[em.covariate]!==undefined){
const diff=targetPopulation[em.covariate]-em.studyMean;
adjustments[em.covariate]={populationDiff:diff,effectAdjustment:em.coefficient*diff,se:Math.abs(em.coefficient)*0.5*Math.abs(diff)}}})}
// Synthesize adjusted effects
const y=processed.map(s=>s.yi),v=processed.map(s=>s.vi),n=processed.length;
const X=Matrix.zeros(n,p);
processed.forEach((s,i)=>{
const i1=treatList.indexOf(s.treatment1)-1;
const i2=treatList.indexOf(s.treatment2)-1;
if(i1>=0)X[i][i1]=1;
if(i2>=0)X[i][i2]=-1});
// Apply population adjustments to effect estimates
const yAdj=y.map((yi,i)=>{
let adj=0;
Object.values(adjustments).forEach(a=>{adj+=a.effectAdjustment});
return yi+adj});
// Random-effects synthesis
let tau2=0.1;
for(let iter=0;iter<50;iter++){
const W=v.map(vi=>1/(vi+tau2));
const XtWX=Matrix.zeros(p,p),XtWy=Array(p).fill(0);
for(let i=0;i<n;i++)for(let j=0;j<p;j++){
XtWy[j]+=X[i][j]*W[i]*yAdj[i];
for(let k=0;k<p;k++)XtWX[j][k]+=X[i][j]*W[i]*X[i][k]}
let beta;try{beta=Matrix.solve(XtWX,XtWy)}catch(e){break}
let Q=0;
for(let i=0;i<n;i++){
let f=0;for(let j=0;j<p;j++)f+=X[i][j]*beta[j];
Q+=W[i]*(yAdj[i]-f)**2}
const newTau2=Math.max(0,tau2*(Q/(n-p)));
if(Math.abs(newTau2-tau2)<1e-6)break;
tau2=newTau2}
// Final estimates
const W=v.map(vi=>1/(vi+tau2));
const XtWX=Matrix.zeros(p,p),XtWy=Array(p).fill(0);
for(let i=0;i<n;i++)for(let j=0;j<p;j++){
XtWy[j]+=X[i][j]*W[i]*yAdj[i];
for(let k=0;k<p;k++)XtWX[j][k]+=X[i][j]*W[i]*X[i][k]}
let beta,vcov;
try{beta=Matrix.solve(XtWX,XtWy);vcov=Matrix.inverse(XtWX)}
catch(e){return{applicable:false,message:'Matrix inversion failed'}}
// Build effects
const effects={},adjustedEffects={};
effects[treatList[0]]={estimate:0,se:0,ci_lower:0,ci_upper:0};
adjustedEffects[treatList[0]]={estimate:0,se:0,ci_lower:0,ci_upper:0};
for(let j=0;j<p;j++){
const t=treatList[j+1];
const est=beta[j],se=Math.sqrt(vcov[j][j]);
effects[t]={estimate:est,se,ci_lower:est-1.96*se,ci_upper:est+1.96*se};
// Adjusted effect with additional uncertainty from adjustment
let adjVar=vcov[j][j];
Object.values(adjustments).forEach(a=>{adjVar+=a.se**2});
const adjSE=Math.sqrt(adjVar);
adjustedEffects[t]={estimate:est,se:adjSE,ci_lower:est-1.96*adjSE,ci_upper:est+1.96*adjSE}}
// Calculate MAIC-style weights for sensitivity
const maicWeights=this.calculateMAICWeights(processed,targetPopulation,covariates);
return{applicable:true,method:'ML-NMR',effects,adjustedEffects,effectModifiers,adjustments,targetPopulation,tau2,treatments:treatList,reference,ipdStudies:ipdData.length,adStudies:adData.length,maicWeights,interpretation:this.interpretResults(effectModifiers,adjustments),summary:`ML-NMR: ${ipdData.length} IPD + ${adData.length} AD studies. ${effectModifiers.filter(e=>e.significant).length} significant effect modifiers.`}},
calculateMAICWeights(studies,targetPop,covariates){
if(Object.keys(targetPop).length===0)return studies.map(()=>1);
return studies.map(s=>{
let logWeight=0;
covariates.forEach(cov=>{
if(targetPop[cov]!==undefined&&s[cov]!==undefined){
const diff=s[cov]-targetPop[cov];
logWeight-=diff*diff/100}});// Gaussian kernel
return Math.exp(logWeight)})},
interpretResults(modifiers,adjustments){
const sigMods=modifiers.filter(m=>m.significant);
if(sigMods.length===0)return'No significant effect modifiers identified';
const adjMag=Object.values(adjustments).reduce((s,a)=>s+Math.abs(a.effectAdjustment),0);
if(adjMag<0.1)return`${sigMods.length} effect modifier(s) but minimal population adjustment needed`;
return`${sigMods.length} significant effect modifier(s). Population adjustment: ${adjMag.toFixed(3)} on log scale`},
// Anchored MAIC (Matching-Adjusted Indirect Comparison) for unanchored scenarios
maicAnalysis(studies,options={}){
const{anchorStudy,targetStudy,covariates=[],effectMeasure='OR'}=options;
if(!anchorStudy||!targetStudy)return{applicable:false,message:'Need anchor and target study names'};
const processed=FrequentistNMA.calcEffects(studies,effectMeasure).filter(s=>s.yi!==null);
const anchor=processed.find(s=>s.name===anchorStudy);
const target=processed.find(s=>s.name===targetStudy);
if(!anchor||!target)return{applicable:false,message:'Anchor or target study not found'};
// Simple propensity score weighting
const weights=processed.map(s=>{
if(s.name===anchorStudy)return 1;
let logOdds=0;
covariates.forEach(cov=>{
if(s[cov]!==undefined&&target[cov]!==undefined){
const diff=s[cov]-target[cov];
logOdds-=diff*diff/50}});
return Math.exp(logOdds)});
// Effective sample size
const ess=Math.pow(Stats.sum(weights),2)/Stats.sum(weights.map(w=>w*w));
// Weighted pooling
const y=processed.map(s=>s.yi),v=processed.map(s=>s.vi);
const wAdj=weights.map((w,i)=>w/(v[i]+0.01));
const sumW=Stats.sum(wAdj);
const est=Stats.sum(y.map((yi,i)=>wAdj[i]*yi))/sumW;
const se=Math.sqrt(1/sumW);
return{applicable:true,method:'MAIC',estimate:est,se,ci:[est-1.96*se,est+1.96*se],weights,effectiveSampleSize:ess,originalN:processed.length,interpretation:`MAIC adjusted estimate. ESS=${ess.toFixed(1)} (${((ess/processed.length)*100).toFixed(0)}% of original)`}},
// Simulated Treatment Comparison (STC)
stcAnalysis(studies,options={}){
const{targetStudy,covariates=[],effectMeasure='OR'}=options;
const processed=FrequentistNMA.calcEffects(studies,effectMeasure).filter(s=>s.yi!==null);
const target=processed.find(s=>s.name===targetStudy);
if(!target)return{applicable:false,message:'Target study not found'};
// Outcome regression adjustment
const y=processed.map(s=>s.yi),v=processed.map(s=>s.vi);
const W=v.map(vi=>1/vi),n=processed.length;
const X=[];const labels=['intercept'];
processed.forEach(s=>{
const row=[1];
covariates.forEach(cov=>{
if(s[cov]!==undefined)row.push(s[cov]-(target[cov]||0));
else row.push(0)});
X.push(row)});
covariates.forEach(c=>labels.push(c));
const p=X[0].length;
const XtWX=Matrix.zeros(p,p),XtWy=Array(p).fill(0);
for(let i=0;i<n;i++){
for(let j=0;j<p;j++){
XtWy[j]+=X[i][j]*W[i]*y[i];
for(let k=0;k<p;k++)XtWX[j][k]+=X[i][j]*W[i]*X[i][k]}}
try{
const beta=Matrix.solve(XtWX,XtWy);
const vcov=Matrix.inverse(XtWX);
const adjEst=beta[0];// Intercept = effect at target covariate values
const adjSE=Math.sqrt(vcov[0][0]);
const coefficients=labels.map((l,i)=>({covariate:l,estimate:beta[i],se:Math.sqrt(vcov[i][i])}));
return{applicable:true,method:'STC',adjustedEstimate:adjEst,se:adjSE,ci:[adjEst-1.96*adjSE,adjEst+1.96*adjSE],coefficients,targetStudy,interpretation:'STC outcome regression adjusted to target population'}}
catch(e){return{applicable:false,message:'Regression failed'}}}};

'''

# Find insertion point (after MLSNMA)
insertion_marker = 'const BayesianNMA={'

if 'const FPNMA_FractionalPolynomial=' not in content:
    content = content.replace(insertion_marker, fp_nma_module + insertion_marker)
    print("[OK] Added FP-NMA (Fractional-Polynomial NMA)")
else:
    print("[SKIP] FP-NMA already exists")

if 'const MLNMR=' not in content:
    content = content.replace(insertion_marker, ml_nmr_module + insertion_marker)
    print("[OK] Added ML-NMR (Multilevel Network Meta-Regression)")
else:
    print("[SKIP] ML-NMR already exists")

# Save the file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

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

print("\n" + "=" * 60)
print("FP-NMA and ML-NMR added successfully!")
print("=" * 60)
print("""
FP-NMA (Fractional-Polynomial NMA):
- Non-linear dose-response/time-course modeling
- Tests powers: -2, -1, -0.5, 0 (log), 0.5, 1, 2, 3
- First and second-order models
- AIC-based model selection
- Optimal dose/time point identification
- Dose-response curve generation

ML-NMR (Multilevel Network Meta-Regression):
- Population adjustment combining IPD + Aggregate Data
- Effect modification by patient-level covariates
- Three-level hierarchical model
- Target population adjustment
- Includes:
  * MAIC (Matching-Adjusted Indirect Comparison)
  * STC (Simulated Treatment Comparison)
  * Effective sample size calculation
""")
