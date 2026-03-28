"""Editorial Review Fixes - Batch 2: Export & Additional Methods"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original size: {len(content):,} bytes')

# ============================================================================
# BATCH 2: Export Capabilities and Additional Methods
# ============================================================================

batch2_code = '''
const ExportPNG={
async export(canvasId,filename='chart.png'){
const canvas=document.getElementById(canvasId);
if(!canvas)return{error:'Canvas not found'};
const dataURL=canvas.toDataURL('image/png');
const link=document.createElement('a');
link.download=filename;
link.href=dataURL;
link.click();
return{success:true,filename};
},
async exportAll(prefix='nma_export'){
const canvases=['networkCanvas','forestCanvas','funnelCanvas','rankingCanvas'];
const results=[];
for(const id of canvases){
const canvas=document.getElementById(id);
if(canvas&&canvas.width>0){
const result=await this.export(id,`${prefix}_${id}.png`);
results.push({id,...result});
}
}
return results;
}
};

const ExportPDF={
async export(options={}){
const title=options.title||'NMA Pro Analysis Report';
const includeCharts=options.includeCharts!==false;
const results=AppState.results||{};
let html=`<!DOCTYPE html><html><head><title>${title}</title>
<style>
body{font-family:Arial,sans-serif;margin:40px;line-height:1.6;}
h1{color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:10px;}
h2{color:#34495e;margin-top:30px;}
table{border-collapse:collapse;width:100%;margin:20px 0;}
th,td{border:1px solid #ddd;padding:12px;text-align:left;}
th{background:#3498db;color:white;}
tr:nth-child(even){background:#f9f9f9;}
.stat{font-weight:bold;color:#2980b9;}
.ci{color:#7f8c8d;}
img{max-width:100%;margin:20px 0;}
@media print{.no-print{display:none;}}
</style></head><body>
<h1>${title}</h1>
<p>Generated: ${new Date().toLocaleString()}</p>`;
if(results.pooledEffect!==undefined){
html+=`<h2>Main Results</h2>
<table>
<tr><th>Statistic</th><th>Value</th></tr>
<tr><td>Pooled Effect</td><td class="stat">${results.pooledEffect?.toFixed(4)||'N/A'}</td></tr>
<tr><td>95% CI</td><td class="ci">[${results.ci?.[0]?.toFixed(4)||'N/A'}, ${results.ci?.[1]?.toFixed(4)||'N/A'}]</td></tr>
<tr><td>Tau-squared</td><td>${results.tau2?.toFixed(4)||'N/A'}</td></tr>
<tr><td>I-squared</td><td>${results.heterogeneity?.I2?.toFixed(1)||'N/A'}%</td></tr>
<tr><td>Number of Studies</td><td>${results.k||'N/A'}</td></tr>
</table>`;
}
if(results.rankings){
html+=`<h2>Treatment Rankings</h2>
<table><tr><th>Treatment</th><th>SUCRA</th><th>P-Score</th><th>Mean Rank</th></tr>`;
results.rankings.forEach(r=>{
html+=`<tr><td>${r.treatment}</td><td>${(r.sucra*100).toFixed(1)}%</td>
<td>${r.pScore?.toFixed(3)||'N/A'}</td><td>${r.meanRank?.toFixed(2)||'N/A'}</td></tr>`;
});
html+=`</table>`;
}
html+=`</body></html>`;
const blob=new Blob([html],{type:'text/html'});
const link=document.createElement('a');
link.download=`${title.replace(/\\s+/g,'_')}.html`;
link.href=URL.createObjectURL(blob);
link.click();
return{success:true,format:'HTML (print to PDF)'};
}
};

const PUniform={
analyze(yi,vi,alpha=0.05){
const n=yi.length;
const se=vi.map(v=>Math.sqrt(v));
const z=yi.map((y,i)=>y/se[i]);
const pValues=z.map(zv=>2*(1-Stats.pnorm(Math.abs(zv))));
const sigIdx=pValues.map((p,i)=>p<=alpha?i:-1).filter(i=>i>=0);
if(sigIdx.length<3)return{error:'Fewer than 3 significant studies'};
const pSig=sigIdx.map(i=>pValues[i]);
const condP=pSig.map(p=>p/alpha);
const meanCondP=condP.reduce((a,b)=>a+b,0)/condP.length;
const expectedUnderH0=0.5;
const se_mean=Math.sqrt((1/12)/condP.length);
const z_test=(meanCondP-expectedUnderH0)/se_mean;
const pTest=2*(1-Stats.pnorm(Math.abs(z_test)));
const w=sigIdx.map(i=>1/vi[i]);
const sumW=w.reduce((a,b)=>a+b,0);
const thetaFE=sigIdx.reduce((s,idx,j)=>s+w[j]*yi[idx],0)/sumW;
let thetaPU=thetaFE;
for(let iter=0;iter<50;iter++){
const expP=sigIdx.map(idx=>{
const delta=(thetaPU-yi[idx])/se[idx];
return Stats.pnorm(-1.96-delta)+Stats.pnorm(-1.96+delta);
});
const meanExpP=expP.reduce((a,b)=>a+b,0)/expP.length;
if(Math.abs(meanExpP-0.5)<0.001)break;
thetaPU+=meanExpP>0.5?0.01:-0.01;
}
return{
nSignificant:sigIdx.length,
nTotal:n,
meanConditionalP:meanCondP,
zTest:z_test,
pValue:pTest,
fixedEffectEstimate:thetaFE,
pUniformEstimate:thetaPU,
bias:thetaFE-thetaPU,
evidentialValue:meanCondP<0.5,
interpretation:meanCondP<0.4?'Evidence of true effect':
meanCondP>0.6?'Evidence of p-hacking or publication bias':'Inconclusive'
};
}
};

const MantelHaenszel={
analyze(studies){
if(!studies||studies.length===0)return{error:'No studies'};
const valid=studies.filter(s=>s.events1!==undefined&&s.n1>0&&s.n2>0);
if(valid.length<2)return{error:'Need at least 2 studies with binary data'};
let sumA=0,sumB=0,sumC=0,sumD=0,sumVar=0;
valid.forEach(s=>{
const a=s.events1,b=s.n1-s.events1;
const c=s.events2,d=s.n2-s.events2;
const n=a+b+c+d;
sumA+=a*d/n;
sumB+=b*c/n;
const varTerm=((a+d)*a*d+(b+c)*b*c)/(n*n);
sumVar+=varTerm;
sumC+=(a+d)/n;
sumD+=(b+c)/n;
});
const orMH=sumA/sumB;
const logOR=Math.log(orMH);
const seLogOR=Math.sqrt(
(sumC/(2*sumA*sumA))+(sumC+sumD)/(2*sumA*sumB)+(sumD/(2*sumB*sumB))
);
const ci=[Math.exp(logOR-1.96*seLogOR),Math.exp(logOR+1.96*seLogOR)];
const z=logOR/seLogOR;
const pValue=2*(1-Stats.pnorm(Math.abs(z)));
return{
OR:orMH,
logOR,
se:seLogOR,
ci,
z,
pValue,
k:valid.length,
method:'Mantel-Haenszel'
};
}
};

const PetoMethod={
analyze(studies){
if(!studies||studies.length===0)return{error:'No studies'};
const valid=studies.filter(s=>s.events1!==undefined);
if(valid.length<2)return{error:'Need at least 2 studies'};
let sumOE=0,sumV=0;
valid.forEach(s=>{
const a=s.events1,n1=s.n1;
const c=s.events2,n2=s.n2;
const n=n1+n2;
const E=n1*(a+c)/n;
const V=n1*n2*(a+c)*(n-a-c)/(n*n*(n-1));
sumOE+=a-E;
sumV+=V;
});
const logOR=sumOE/sumV;
const se=1/Math.sqrt(sumV);
const or=Math.exp(logOR);
const ci=[Math.exp(logOR-1.96*se),Math.exp(logOR+1.96*se)];
const z=logOR/se;
const pValue=2*(1-Stats.pnorm(Math.abs(z)));
return{
OR:or,
logOR,
se,
ci,
z,
pValue,
k:valid.length,
method:'Peto'
};
}
};

const EBEstimator={
estimate(yi,vi){
const n=yi.length;
const w=vi.map(v=>1/v);
const sumW=w.reduce((a,b)=>a+b,0);
const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;
let Q=0;
for(let i=0;i<n;i++){
Q+=w[i]*(yi[i]-mu)*(yi[i]-mu);
}
const C=sumW-w.reduce((s,wi)=>s+wi*wi,0)/sumW;
const tau2DL=Math.max(0,(Q-(n-1))/C);
const tau2EB=tau2DL*(n-1)/(n+1);
return{tau2:tau2EB,tau2DL,method:'Empirical Bayes',shrinkage:(n-1)/(n+1)};
}
};

const HedgesEstimator={
estimate(yi,vi){
const n=yi.length;
const w=vi.map(v=>1/v);
const sumW=w.reduce((a,b)=>a+b,0);
const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;
let Q=0;
for(let i=0;i<n;i++){
Q+=w[i]*(yi[i]-mu)*(yi[i]-mu);
}
const varY=yi.reduce((s,y)=>s+(y-mu)*(y-mu),0)/(n-1);
const meanVi=vi.reduce((a,b)=>a+b,0)/n;
const tau2=Math.max(0,varY-meanVi);
return{tau2,method:'Hedges',varianceOfEffects:varY,meanWithinVariance:meanVi};
}
};

const InverseVariance={
pool(yi,vi,method='random'){
const n=yi.length;
const w=vi.map(v=>1/v);
const sumW=w.reduce((a,b)=>a+b,0);
const muFE=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;
const seFE=Math.sqrt(1/sumW);
let Q=0;
for(let i=0;i<n;i++){
Q+=w[i]*(yi[i]-muFE)*(yi[i]-muFE);
}
const I2=Math.max(0,(Q-(n-1))/Q)*100;
if(method==='fixed'){
return{pooled:muFE,se:seFE,ci:[muFE-1.96*seFE,muFE+1.96*seFE],Q,I2,method:'Fixed-IV'};
}
const C=sumW-w.reduce((s,wi)=>s+wi*wi,0)/sumW;
const tau2=Math.max(0,(Q-(n-1))/C);
const wRE=vi.map(v=>1/(v+tau2));
const sumWRE=wRE.reduce((a,b)=>a+b,0);
const muRE=yi.reduce((s,y,i)=>s+wRE[i]*y,0)/sumWRE;
const seRE=Math.sqrt(1/sumWRE);
return{pooled:muRE,se:seRE,ci:[muRE-1.96*seRE,muRE+1.96*seRE],Q,I2,tau2,method:'Random-IV'};
}
};

const SJEstimator={
estimate(yi,vi,maxIter=100,tol=1e-6){
const n=yi.length;
let tau2=0.01;
for(let iter=0;iter<maxIter;iter++){
const w=vi.map(v=>1/(v+tau2));
const sumW=w.reduce((a,b)=>a+b,0);
const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;
let num=0;
for(let i=0;i<n;i++){
num+=w[i]*w[i]*((yi[i]-mu)*(yi[i]-mu)-vi[i]);
}
const sumW2=w.reduce((s,wi)=>s+wi*wi,0);
const tau2New=Math.max(0,tau2+num/sumW2);
if(Math.abs(tau2New-tau2)<tol){
tau2=tau2New;break;
}
tau2=tau2New;
}
return{tau2,method:'Sidik-Jonkman'};
}
};

'''

# Find insertion point
insert_marker = 'const DEMO_DATASETS={'

if insert_marker in content:
    modules = ['ExportPNG', 'ExportPDF', 'PUniform', 'MantelHaenszel',
               'PetoMethod', 'EBEstimator', 'HedgesEstimator', 'InverseVariance', 'SJEstimator']

    missing = [m for m in modules if f'const {m}=' not in content]
    existing = [m for m in modules if f'const {m}=' in content]

    print(f'Existing: {existing}')
    print(f'Missing: {missing}')

    if missing:
        content = content.replace(insert_marker, batch2_code + '\n' + insert_marker)
        print(f'[OK] Added {len(missing)} modules')
    else:
        print('[INFO] All batch 2 modules exist')
else:
    print('[ERROR] Could not find insertion point')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Final size: {len(content):,} bytes')
print('Batch 2 complete')
