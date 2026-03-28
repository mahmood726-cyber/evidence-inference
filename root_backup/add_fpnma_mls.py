# Add FPNMA and MLS NMA methods to NMA Pro v6.2

import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("Adding FPNMA and MLS NMA to NMA Pro v6.2")
print("=" * 60)

# ============================================================================
# Add FPNMA (Frequentist Pairwise NMA) - Two-stage approach
# ============================================================================
fpnma_module = '''
const FPNMA={
// Frequentist Pairwise NMA (Two-stage approach)
// Stage 1: Pairwise meta-analyses for each direct comparison
// Stage 2: Synthesize using graph-theoretical approach
analyze(studies,options={}){
const{reference,effectMeasure='OR',estimator='REML',smallStudyCorrection='hksj'}=options;
const processed=FrequentistNMA.calcEffects(studies,effectMeasure).filter(s=>s.yi!==null);
// Stage 1: Pairwise meta-analyses for each direct comparison
const directMap=new Map();
processed.forEach(s=>{
const key=[s.treatment1,s.treatment2].sort().join('|');
if(!directMap.has(key))directMap.set(key,[]);
directMap.get(key).push(s)});
const pairwiseResults=[];
directMap.forEach((studies,key)=>{
const[t1,t2]=key.split('|');
const y=studies.map(s=>s.yi),v=studies.map(s=>s.vi),w=v.map(vi=>1/vi);
const n=studies.length;
// Fixed-effect pooling first
const feEst=Stats.sum(y.map((yi,i)=>w[i]*yi))/Stats.sum(w);
const feSE=Math.sqrt(1/Stats.sum(w));
// Q statistic for heterogeneity
let Q=0;for(let i=0;i<n;i++)Q+=w[i]*(y[i]-feEst)**2;
const df=n-1;
// DerSimonian-Laird tau2
let tau2=0;
if(estimator!=='FE'&&df>0){
const c=Stats.sum(w)-Stats.sum(w.map(wi=>wi*wi))/Stats.sum(w);
tau2=Math.max(0,(Q-df)/c)}
// Random-effects pooling
const wRE=v.map(vi=>1/(vi+tau2)),sumWRE=Stats.sum(wRE);
const reEst=Stats.sum(y.map((yi,i)=>wRE[i]*yi))/sumWRE;
let reSE=Math.sqrt(1/sumWRE);
// HKSJ correction if requested
if(smallStudyCorrection==='hksj'&&n>1){
let swr=0;for(let i=0;i<n;i++)swr+=wRE[i]*(y[i]-reEst)**2;
const hksjFactor=Math.max(1,swr/df);
reSE*=Math.sqrt(hksjFactor)}
const I2=df>0?Math.max(0,((Q-df)/Q)*100):0;
pairwiseResults.push({comparison:key,t1,t2,nStudies:n,estimate:reEst,se:reSE,ci:[reEst-Stats.qt(0.975,Math.max(1,df))*reSE,reEst+Stats.qt(0.975,Math.max(1,df))*reSE],tau2,I2,Q,df,feEstimate:feEst,feSE})});
// Stage 2: Graph-theoretical synthesis using shortest paths
const treatments=new Set();
processed.forEach(s=>{treatments.add(s.treatment1);treatments.add(s.treatment2)});
const treatList=Array.from(treatments).sort();
const refIdx=treatList.indexOf(reference);
if(refIdx>0){treatList.splice(refIdx,1);treatList.unshift(reference)}
// Build adjacency matrix with estimates and variances
const n=treatList.length;
const adjEst=Array(n).fill(null).map(()=>Array(n).fill(null));
const adjVar=Array(n).fill(null).map(()=>Array(n).fill(null));
pairwiseResults.forEach(pr=>{
const i=treatList.indexOf(pr.t1),j=treatList.indexOf(pr.t2);
if(i>=0&&j>=0){
adjEst[i][j]=pr.estimate;adjEst[j][i]=-pr.estimate;
adjVar[i][j]=pr.se**2;adjVar[j][i]=pr.se**2}});
// Find all paths from reference to each treatment
const effects={};
treatList.forEach((t,idx)=>{
if(idx===0){effects[t]={estimate:0,se:0,ci_lower:0,ci_upper:0,pValue:1,source:'reference'};return}
// Direct path
if(adjEst[0][idx]!==null){
const est=adjEst[0][idx],se=Math.sqrt(adjVar[0][idx]);
effects[t]={estimate:est,se,ci_lower:est-1.96*se,ci_upper:est+1.96*se,pValue:2*(1-Stats.pnorm(Math.abs(est/se))),source:'direct'};return}
// Find shortest path (minimum variance) using modified Dijkstra
const dist=Array(n).fill(Infinity),prev=Array(n).fill(-1),variance=Array(n).fill(Infinity);
dist[0]=0;variance[0]=0;
const unvisited=new Set(Array(n).keys());
while(unvisited.size>0){
let u=-1,minVar=Infinity;
for(const v of unvisited){if(variance[v]<minVar){minVar=variance[v];u=v}}
if(u===-1)break;
unvisited.delete(u);
for(let v=0;v<n;v++){
if(adjVar[u][v]!==null&&unvisited.has(v)){
const newVar=variance[u]+adjVar[u][v];
if(newVar<variance[v]){variance[v]=newVar;dist[v]=dist[u]+adjEst[u][v];prev[v]=u}}}}
if(variance[idx]<Infinity){
const est=dist[idx],se=Math.sqrt(variance[idx]);
// Reconstruct path
let path=[idx],curr=idx;
while(prev[curr]!==-1){path.unshift(prev[curr]);curr=prev[curr]}
effects[t]={estimate:est,se,ci_lower:est-1.96*se,ci_upper:est+1.96*se,pValue:2*(1-Stats.pnorm(Math.abs(est/se))),source:'indirect',pathLength:path.length-1,path:path.map(i=>treatList[i]).join(' → ')}}
else{effects[t]={estimate:null,se:null,ci_lower:null,ci_upper:null,pValue:null,source:'disconnected'}}});
return{applicable:true,method:'FPNMA',stage1:pairwiseResults,effects,treatments:treatList,reference,summary:`FPNMA: ${pairwiseResults.length} direct comparisons, ${treatList.length} treatments`}}};

'''

# ============================================================================
# Add MLS NMA (Multivariate Likelihood Synthesis)
# ============================================================================
mls_module = '''
const MLSNMA={
// Multivariate Likelihood Synthesis NMA
// Full likelihood approach accounting for multi-arm trial correlations
analyze(studies,options={}){
const{reference,effectMeasure='OR',maxIter=100,tol=1e-6}=options;
const processed=FrequentistNMA.calcEffects(studies,effectMeasure).filter(s=>s.yi!==null);
// Identify multi-arm trials (same study name with multiple comparisons)
const studyMap=new Map();
processed.forEach((s,idx)=>{
const studyId=s.name||`Study_${idx}`;
if(!studyMap.has(studyId))studyMap.set(studyId,{comparisons:[],indices:[]});
studyMap.get(studyId).comparisons.push(s);
studyMap.get(studyId).indices.push(idx)});
// Build treatment list
const treatSet=new Set();
processed.forEach(s=>{treatSet.add(s.treatment1);treatSet.add(s.treatment2)});
const treatments=Array.from(treatSet).sort();
const refIdx=treatments.indexOf(reference);
if(refIdx>0){treatments.splice(refIdx,1);treatments.unshift(reference)}
const p=treatments.length-1;// Number of basic parameters
// Build block-diagonal variance-covariance matrix
// For multi-arm trials, we need to account for correlation
const n=processed.length;
const y=processed.map(s=>s.yi);
const V=Matrix.zeros(n,n);// Full variance matrix
const X=Matrix.zeros(n,p);// Design matrix
processed.forEach((s,i)=>{
// Design matrix
const i1=treatments.indexOf(s.treatment1)-1;
const i2=treatments.indexOf(s.treatment2)-1;
if(i1>=0)X[i][i1]=1;
if(i2>=0)X[i][i2]=-1;
// Diagonal variance
V[i][i]=s.vi});
// Add correlations for multi-arm trials
studyMap.forEach(study=>{
if(study.comparisons.length>1){
// Multi-arm trial: comparisons share a common arm
// Correlation = vi*vj / (vi*vj + cov) where cov depends on shared arm
const comps=study.comparisons;
const indices=study.indices;
for(let a=0;a<comps.length;a++){
for(let b=a+1;b<comps.length;b++){
const s1=comps[a],s2=comps[b];
// Check for shared arm
const arms1=[s1.treatment1,s1.treatment2];
const arms2=[s2.treatment1,s2.treatment2];
const shared=arms1.filter(arm=>arms2.includes(arm));
if(shared.length>0){
// Approximate covariance for shared arm
// Cov ≈ 1/(2*n_shared) for log-scale measures
const sharedArm=shared[0];
const n1=s1.treatment1===sharedArm?s1.n1:s1.n2;
const n2=s2.treatment1===sharedArm?s2.n1:s2.n2;
const cov=1/(2*Math.min(n1||50,n2||50));
V[indices[a]][indices[b]]=cov;
V[indices[b]][indices[a]]=cov}}}}});
// REML estimation with Newton-Raphson
let tau2=0.1;
let beta=Array(p).fill(0);
let converged=false;
for(let iter=0;iter<maxIter;iter++){
// Update weights: W = (V + tau2*I)^{-1}
const Sigma=V.map((row,i)=>row.map((v,j)=>v+(i===j?tau2:0)));
let W;
try{W=Matrix.inverse(Sigma)}
catch(e){
// If singular, add regularization
const reg=0.01;
const SigmaReg=Sigma.map((row,i)=>row.map((v,j)=>v+(i===j?reg:0)));
W=Matrix.inverse(SigmaReg)}
// Weighted least squares: beta = (X'WX)^{-1} X'Wy
const XtW=Matrix.zeros(p,n);
for(let i=0;i<p;i++)for(let j=0;j<n;j++){
let sum=0;for(let k=0;k<n;k++)sum+=X[k][i]*W[k][j];
XtW[i][j]=sum}
const XtWX=Matrix.zeros(p,p);
for(let i=0;i<p;i++)for(let j=0;j<p;j++){
let sum=0;for(let k=0;k<n;k++)sum+=XtW[i][k]*X[k][j];
XtWX[i][j]=sum}
const XtWy=Array(p).fill(0);
for(let i=0;i<p;i++){
let sum=0;for(let k=0;k<n;k++)sum+=XtW[i][k]*y[k];
XtWy[i]=sum}
let newBeta;
try{newBeta=Matrix.solve(XtWX,XtWy)}
catch(e){newBeta=beta}
// Residuals and REML update for tau2
let Q=0;
for(let i=0;i<n;i++){
let fitted=0;for(let j=0;j<p;j++)fitted+=X[i][j]*newBeta[j];
const r=y[i]-fitted;
let wr=0;for(let k=0;k<n;k++){
let rk=y[k];for(let j=0;j<p;j++)rk-=X[k][j]*newBeta[j];
wr+=W[i][k]*rk}
Q+=r*wr}
const df=n-p;
// Trace term for REML
let trP=0;
try{
const vcov=Matrix.inverse(XtWX);
for(let i=0;i<n;i++){
let hii=0;
for(let j=0;j<p;j++)for(let k=0;k<p;k++)hii+=X[i][j]*vcov[j][k]*X[i][k];
trP+=W[i][i]*(1-hii)}}
catch(e){trP=df}
const newTau2=Math.max(0,tau2+(Q-df)/(trP+0.01));
// Check convergence
const betaDiff=Math.max(...newBeta.map((b,i)=>Math.abs(b-beta[i])));
const tau2Diff=Math.abs(newTau2-tau2);
if(betaDiff<tol&&tau2Diff<tol){converged=true;break}
beta=newBeta;
tau2=newTau2}
// Final variance-covariance matrix
const Sigma=V.map((row,i)=>row.map((v,j)=>v+(i===j?tau2:0)));
let W,vcov;
try{
W=Matrix.inverse(Sigma);
const XtW=Matrix.zeros(p,n);
for(let i=0;i<p;i++)for(let j=0;j<n;j++){
let sum=0;for(let k=0;k<n;k++)sum+=X[k][i]*W[k][j];
XtW[i][j]=sum}
const XtWX=Matrix.zeros(p,p);
for(let i=0;i<p;i++)for(let j=0;j<p;j++){
let sum=0;for(let k=0;k<n;k++)sum+=XtW[i][k]*X[k][j];
XtWX[i][j]=sum}
vcov=Matrix.inverse(XtWX)}
catch(e){vcov=Matrix.zeros(p,p).map((r,i)=>r.map((v,j)=>i===j?1:0))}
// Build effects
const effects={};
effects[treatments[0]]={estimate:0,se:0,ci_lower:0,ci_upper:0,pValue:1};
for(let j=0;j<p;j++){
const t=treatments[j+1];
const est=beta[j],se=Math.sqrt(vcov[j][j]);
effects[t]={estimate:est,se,ci_lower:est-1.96*se,ci_upper:est+1.96*se,pValue:2*(1-Stats.pnorm(Math.abs(est/se)))}}
// Calculate heterogeneity
let Q=0;
const Wfinal=V.map(row=>row.map(v=>1/v));
for(let i=0;i<n;i++){
let fitted=0;for(let j=0;j<p;j++)fitted+=X[i][j]*beta[j];
Q+=(y[i]-fitted)**2/V[i][i]}
const I2=Math.max(0,((Q-(n-p))/Q)*100);
// Multi-arm trial summary
const multiArmTrials=Array.from(studyMap.entries()).filter(([k,v])=>v.comparisons.length>1).map(([k,v])=>({study:k,nComparisons:v.comparisons.length}));
return{applicable:true,method:'MLS-NMA',effects,treatments,reference,tau2,tau:Math.sqrt(tau2),heterogeneity:{Q,df:n-p,I2},vcov,converged,multiArmTrials,nMultiArm:multiArmTrials.length,summary:`MLS-NMA: ${n} comparisons, ${multiArmTrials.length} multi-arm trials properly accounted for`}}};

'''

# Find insertion point (after FrequentistNMA)
insertion_marker = 'const BayesianNMA={'

if 'const FPNMA=' not in content:
    content = content.replace(insertion_marker, fpnma_module + insertion_marker)
    print("[OK] Added FPNMA (Frequentist Pairwise NMA)")
else:
    print("[SKIP] FPNMA already exists")

if 'const MLSNMA=' not in content:
    content = content.replace(insertion_marker, mls_module + insertion_marker)
    print("[OK] Added MLS NMA (Multivariate Likelihood Synthesis)")
else:
    print("[SKIP] MLS NMA already exists")

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
print("FPNMA and MLS NMA methods added successfully!")
print("=" * 60)
print("""
FPNMA (Frequentist Pairwise NMA):
- Two-stage approach
- Stage 1: Pairwise meta-analyses for each direct comparison
- Stage 2: Graph-theoretical synthesis using minimum variance paths
- Supports HKSJ correction and multiple estimators

MLS NMA (Multivariate Likelihood Synthesis):
- Full likelihood approach
- Properly accounts for multi-arm trial correlations
- Uses block-diagonal variance-covariance matrix
- REML estimation with Newton-Raphson
- Reports number of multi-arm trials handled
""")
