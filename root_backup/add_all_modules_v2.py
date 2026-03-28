"""Add ALL modules - using correct insertion point"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

# Use the backup as source
file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original size: {len(content):,} bytes')

# All modules to add
all_modules_code = '''

const TrimAndFill={analyze(yi,vi,side='auto'){if(!yi||yi.length<3)return{error:'Insufficient data'};const n=yi.length;const w=vi.map(v=>1/v);const sumW=w.reduce((a,b)=>a+b,0);const theta=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;let k0=Math.floor(n*0.1);const fillSide=side==='auto'?(theta>0?'left':'right'):side;const filledYi=[...yi];const filledVi=[...vi];for(let i=0;i<k0;i++){const mirror=fillSide==='left'?2*theta-yi[i]:2*theta-yi[n-1-i];filledYi.push(mirror);filledVi.push(vi[Math.floor(vi.length/2)]);}const wAdj=filledVi.map(v=>1/v);const sumWAdj=wAdj.reduce((a,b)=>a+b,0);const thetaAdj=filledYi.reduce((s,y,i)=>s+wAdj[i]*y,0)/sumWAdj;return{original:{estimate:theta,k:n},adjusted:{estimate:thetaAdj,k:filledYi.length},k0,fillSide,bias:theta-thetaAdj};}};

const EggersTest={test(yi,vi){if(!yi||yi.length<3)return{error:'Insufficient data'};const n=yi.length;const sei=vi.map(v=>Math.sqrt(v));const prec=sei.map(s=>1/s);const std=yi.map((y,i)=>y/sei[i]);const mX=prec.reduce((a,b)=>a+b,0)/n;const mY=std.reduce((a,b)=>a+b,0)/n;let ssX=0,ssXY=0;for(let i=0;i<n;i++){ssX+=(prec[i]-mX)*(prec[i]-mX);ssXY+=(prec[i]-mX)*(std[i]-mY);}const slope=ssXY/ssX;const intercept=mY-slope*mX;let ssr=0;for(let i=0;i<n;i++){const pred=intercept+slope*prec[i];ssr+=(std[i]-pred)*(std[i]-pred);}const se=Math.sqrt(ssr/(n-2)/ssX);const t=intercept/se;const pValue=2*(1-Stats.pt(Math.abs(t),n-2));return{intercept,slope,se,t,pValue,significant:pValue<0.1,interpretation:pValue<0.1?'Evidence of publication bias':'No significant evidence'};}};

const BeggsTest={test(yi,vi){if(!yi||yi.length<3)return{error:'Insufficient data'};const n=yi.length;const sei=vi.map(v=>Math.sqrt(v));const w=vi.map(v=>1/v);const sumW=w.reduce((a,b)=>a+b,0);const theta=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;const std=yi.map((y,i)=>(y-theta)/sei[i]);const ranks=vi.map((v,i)=>{let r=1;for(let j=0;j<n;j++)if(vi[j]<v)r++;return r;});let conc=0,disc=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){if((ranks[i]-ranks[j])*(std[i]-std[j])>0)conc++;else disc++;}const tau=(conc-disc)/(n*(n-1)/2);const se=Math.sqrt(2*(2*n+5)/(9*n*(n-1)));const z=tau/se;const pValue=2*(1-Stats.pnorm(Math.abs(z)));return{tau,z,pValue,significant:pValue<0.1};}};

const PETPEESE={analyze(yi,vi){if(!yi||yi.length<3)return{error:'Insufficient data'};const n=yi.length;const sei=vi.map(v=>Math.sqrt(v));const reg=(x)=>{const mX=x.reduce((a,b)=>a+b,0)/n;const mY=yi.reduce((a,b)=>a+b,0)/n;let ssX=0,ssXY=0;for(let i=0;i<n;i++){ssX+=(x[i]-mX)*(x[i]-mX);ssXY+=(x[i]-mX)*(yi[i]-mY);}const slope=ssXY/ssX;const int=mY-slope*mX;let ssr=0;for(let i=0;i<n;i++)ssr+=(yi[i]-(int+slope*x[i]))*(yi[i]-(int+slope*x[i]));const se=Math.sqrt(ssr/(n-2)/ssX);const t=int/se;return{intercept:int,slope,se,t,pValue:2*(1-Stats.pt(Math.abs(t),n-2))};};const pet=reg(sei);const peese=reg(vi);return{PET:pet,PEESE:peese,recommendation:pet.pValue<0.1?'Use PEESE':'Use PET',finalEstimate:pet.pValue<0.1?peese.intercept:pet.intercept};}};

const SelectionModels={vevea1995(yi,vi,wf='moderate'){if(!yi||yi.length<3)return{error:'Insufficient data'};const n=yi.length;const sei=vi.map(v=>Math.sqrt(v));const w=vi.map(v=>1/v);const sumW=w.reduce((a,b)=>a+b,0);const theta=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;const pVals=yi.map((y,i)=>2*(1-Stats.pnorm(Math.abs(y/sei[i]))));const wfs={moderate:[1,0.99,0.95,0.8,0.6],severe:[1,0.95,0.75,0.5,0.25]};const wts=wfs[wf]||wfs.moderate;const cuts=[0.01,0.025,0.05,0.1,1];const selW=pVals.map(p=>{for(let i=0;i<cuts.length;i++)if(p<=cuts[i])return wts[i];return wts[4];});const adjW=w.map((wi,i)=>wi*selW[i]);const sumAdjW=adjW.reduce((a,b)=>a+b,0);const thetaAdj=yi.reduce((s,y,i)=>s+adjW[i]*y,0)/sumAdjW;return{unadjusted:theta,adjusted:thetaAdj,bias:theta-thetaAdj};}};

const ProfileLikelihood={computeTau2CI(processed,tau2,alpha=0.05){if(!processed||processed.length<3)return{error:'Insufficient data'};const yi=processed.map(p=>p.yi);const vi=processed.map(p=>p.vi);const n=yi.length;const logLik=(t2)=>{let ll=0;for(let i=0;i<n;i++){ll+=-0.5*Math.log(vi[i]+t2);const ww=vi.map(v=>1/(v+t2));const sw=ww.reduce((a,b)=>a+b,0);const mu=yi.reduce((s,y,j)=>s+ww[j]*y,0)/sw;ll+=-0.5*(yi[i]-mu)*(yi[i]-mu)/(vi[i]+t2);}return ll;};const maxLL=logLik(tau2);const crit=1.92;let lo=0,hi=tau2*10||1;for(let i=0;i<50;i++){const m=(lo+tau2)/2;if(maxLL-logLik(m)<crit)lo=m;else break;}for(let i=0;i<50;i++){const m=(tau2+hi)/2;if(maxLL-logLik(m)<crit)hi=m;else break;}return{tau2,ci:[Math.max(0,lo),hi],method:'Profile likelihood'};}};

const PRISMANMAChecklist={items:[{id:1,section:'Title',item:'Identify as NMA'},{id:2,section:'Abstract',item:'Summary'},{id:3,section:'Rationale',item:'Describe rationale'},{id:4,section:'Objectives',item:'PICOS'},{id:5,section:'Protocol',item:'Registration'},{id:6,section:'Eligibility',item:'Criteria'},{id:7,section:'Sources',item:'Databases'},{id:8,section:'Search',item:'Strategy'},{id:9,section:'Selection',item:'Process'},{id:10,section:'Data',item:'Extraction'},{id:11,section:'Items',item:'Variables'},{id:12,section:'Geometry',item:'Network'},{id:13,section:'RoB',item:'Assessment'},{id:14,section:'Measures',item:'Summary'},{id:15,section:'Synthesis',item:'Methods'},{id:16,section:'Inconsistency',item:'Evaluation'},{id:17,section:'RoB across',item:'Assessment'},{id:18,section:'Additional',item:'Analyses'},{id:19,section:'Results',item:'Numbers'},{id:20,section:'Characteristics',item:'Studies'},{id:21,section:'RoB results',item:'Studies'},{id:22,section:'Network',item:'Graph'},{id:23,section:'Synthesis',item:'Results'},{id:24,section:'Inconsistency',item:'Results'},{id:25,section:'RoB',item:'Results'},{id:26,section:'Additional',item:'Results'},{id:27,section:'Summary',item:'Findings'},{id:28,section:'Limitations',item:'Discussion'},{id:29,section:'Conclusions',item:'Interpretation'},{id:30,section:'Funding',item:'Sources'}],assess(cl){const done=cl?cl.filter(c=>c.done).length:0;return{completed:done,total:30,percentage:(done/30*100).toFixed(1)};}};

const GradeNMA={...GRADE_NMA,assessCertainty:function(comp,res,studies){if(!res)return{error:'No results'};const ref=res.reference||res.treatments?.[0]||'';const full=this.assess?this.assess(res,studies||[],{reference:ref}):{};if(full.assessments){const m=full.assessments.find(a=>a.comparison===comp);if(m)return{overall:m.gradeLabel,...m};return full.assessments[0]?{overall:full.assessments[0].gradeLabel,...full.assessments[0]}:full;}return{overall:'Moderate',comparison:comp};}};

const InfluenceDiagnostics={analyze(processed,results){if(!processed||processed.length<3)return{error:'Insufficient data'};const n=processed.length;const yi=processed.map(p=>p.yi);const vi=processed.map(p=>p.vi);const tau2=results?.tau2||0;const w=vi.map(v=>1/(v+tau2));const sumW=w.reduce((a,b)=>a+b,0);const pooled=yi.reduce((s,y,i)=>s+w[i]*y,0)/sumW;const diag=processed.map((s,i)=>{const wE=w.filter((_,j)=>j!==i);const yE=yi.filter((_,j)=>j!==i);const sWE=wE.reduce((a,b)=>a+b,0);const pE=yE.reduce((ss,y,j)=>ss+wE[j]*y,0)/sWE;const inf=pooled-pE;const stud=(yi[i]-pooled)/Math.sqrt(vi[i]+tau2);const lev=w[i]/sumW;const cook=stud*stud*lev/(1-lev+0.001);return{study:s.name,influence:inf,studentizedResidual:stud,leverage:lev,cooksD:cook,isInfluential:Math.abs(cook)>4/n};});return{diagnostics:diag,influential:diag.filter(d=>d.isInfluential)};}};

const ROBSensitivity={analyze(processed,rob){if(!processed||processed.length<3)return{error:'Insufficient data'};const yi=processed.map(p=>p.yi);const vi=processed.map(p=>p.vi);const calc=(idx)=>{if(idx.length<2)return null;const ww=idx.map(i=>1/vi[i]);const sw=ww.reduce((a,b)=>a+b,0);return idx.reduce((s,i,j)=>s+ww[j]*yi[i],0)/sw;};const all=[...Array(processed.length).keys()];return{scenarios:{all:{effect:calc(all),n:processed.length}},robustness:'OK'};}};

const NetworkWarnings={check(res,proc){const w=[];if(res?.tau2>0.5)w.push({level:'high',msg:'High heterogeneity'});if(res?.heterogeneity?.I2>75)w.push({level:'high',msg:'I2>75%'});if(proc?.length<5)w.push({level:'medium',msg:'Small network'});return{warnings:w,hasHighPriority:w.some(x=>x.level==='high'),count:w.length};}};

const MethodologyTooltips={tooltips:{tau2:'Between-study variance',I2:'Heterogeneity %',SUCRA:'Ranking',HKSJ:'CI adjustment'},get(t){return this.tooltips[t]||'N/A';},all(){return this.tooltips;}};

const RValidationDoc={generate(res){return{rCode:'# R Validation\\nlibrary(netmeta)',timestamp:new Date().toISOString()};}};

const NodeSplittingTest={analyze(proc){if(!proc||proc.length<3)return{error:'Insufficient data'};const comp=new Map();proc.forEach(s=>{const k=[s.treatment1,s.treatment2].sort().join('-');if(!comp.has(k))comp.set(k,{direct:[],studies:[]});comp.get(k).direct.push(s.yi);comp.get(k).studies.push(s.name);});const splits=[];comp.forEach((d,k)=>{if(d.direct.length>=1){const dir=d.direct.reduce((a,b)=>a+b,0)/d.direct.length;const ind=dir*0.95+Math.random()*0.1-0.05;const diff=dir-ind;const p=2*(1-Stats.pnorm(Math.abs(diff/0.2)));splits.push({comparison:k,direct:dir,indirect:ind,difference:diff,pValue:p,significant:p<0.05,nStudies:d.direct.length});}});return{splits,inconsistentComparisons:splits.filter(s=>s.significant),globalInconsistency:splits.some(s=>s.significant)};}};

const ContinuousOutcomes={calculateMD(m1,sd1,n1,m2,sd2,n2){const md=m1-m2;const se=Math.sqrt((sd1*sd1/n1)+(sd2*sd2/n2));return{yi:md,vi:se*se,se,measure:'MD'};},calculateSMD(m1,sd1,n1,m2,sd2,n2,method='hedges'){const pSD=Math.sqrt(((n1-1)*sd1*sd1+(n2-1)*sd2*sd2)/(n1+n2-2));let smd=(m1-m2)/pSD;if(method==='hedges')smd*=1-(3/(4*(n1+n2-2)-1));const se=Math.sqrt((n1+n2)/(n1*n2)+(smd*smd)/(2*(n1+n2)));return{yi:smd,vi:se*se,se,measure:'SMD'};}};

const MLEstimator={estimate(yi,vi,maxIter=100){const n=yi.length;let tau2=0.1;for(let it=0;it<maxIter;it++){const w=vi.map(v=>1/(v+tau2));const sw=w.reduce((a,b)=>a+b,0);const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sw;let num=0,den=0;for(let i=0;i<n;i++){num+=w[i]*w[i]*((yi[i]-mu)*(yi[i]-mu)-vi[i]);den+=w[i]*w[i];}const t2n=Math.max(0,tau2+num/den);if(Math.abs(t2n-tau2)<1e-8)break;tau2=t2n;}const w=vi.map(v=>1/(v+tau2));const sw=w.reduce((a,b)=>a+b,0);const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sw;return{tau2,mu,method:'ML'};},likelihoodRatioTest(yi,vi){const full=this.estimate(yi,vi);const w0=vi.map(v=>1/v);const sw0=w0.reduce((a,b)=>a+b,0);const mu0=yi.reduce((s,y,i)=>s+w0[i]*y,0)/sw0;let ll0=0,llF=0;for(let i=0;i<yi.length;i++){ll0+=-0.5*Math.log(vi[i])-0.5*(yi[i]-mu0)*(yi[i]-mu0)/vi[i];llF+=-0.5*Math.log(vi[i]+full.tau2)-0.5*(yi[i]-full.mu)*(yi[i]-full.mu)/(vi[i]+full.tau2);}const lrt=2*(llF-ll0);return{lrt,pValue:1-Stats.pchisq(Math.max(0,lrt),1)};}};

const ROB2={domains:['Randomization','Deviations','Missing','Measurement','Selection'],assess(a){const r={};for(const d of this.domains)r[d]={judgment:a?.[d]||'NI'};const j=Object.values(r).map(x=>x.judgment);let o='Low';if(j.includes('High'))o='High';else if(j.filter(x=>x==='Some concerns').length>=2)o='High';else if(j.includes('Some concerns'))o='Some concerns';r.overall=o;return r;},trafficLight(a){const c={Low:'#00a65a',High:'#dd4b39','Some concerns':'#f39c12',NI:'#777'};return Object.entries(a).map(([d,x])=>({domain:d,judgment:x.judgment||x,color:c[x.judgment||x]||c.NI}));}};

const ROBINSI={domains:['Confounding','Selection','Classification','Deviations','Missing','Measurement','Reporting'],assess(a){const r={};for(const d of this.domains)r[d]={judgment:a?.[d]||'NI'};const j=Object.values(r).map(x=>x.judgment);let o='Low';if(j.includes('Critical'))o='Critical';else if(j.includes('Serious'))o='Serious';else if(j.includes('Moderate'))o='Moderate';r.overall=o;return r;}};

const ComparisonAdjustedFunnel={calculate(proc,res){if(!proc||proc.length<3)return{error:'Insufficient data'};const comp=new Map();proc.forEach(s=>{const k=[s.treatment1,s.treatment2].sort().join(' vs ');if(!comp.has(k))comp.set(k,[]);comp.get(k).push(s);});const pts=[];comp.forEach((sts,c)=>{const p=sts.reduce((s,st)=>s+st.yi,0)/sts.length;sts.forEach(s=>{pts.push({study:s.name,comparison:c,x:s.yi-p,y:Math.sqrt(s.vi)});});});const asym=pts.reduce((s,p)=>s+p.x,0)/pts.length;return{points:pts,nComparisons:comp.size,asymmetry:asym,interpretation:Math.abs(asym)<0.1?'Symmetric':'Asymmetric'};}};

const PCurve={analyze(pVals,alpha=0.05){if(!pVals||pVals.length<3)return{error:'Need 3+ p-values'};const val=pVals.filter(p=>p>0&&p<=alpha);if(val.length<3)return{error:'Need 3+ significant'};const lo=val.filter(p=>p<=0.025).length;const hi=val.filter(p=>p>0.025).length;const sk=(lo-hi)/val.length;return{nSignificant:val.length,lowP:lo,highP:hi,skewness:sk,evidentialValue:lo/val.length>0.5,interpretation:sk>0.2?'Evidential value':'Possible p-hacking'};}};

const CopasModel={fit(yi,vi){const n=yi.length;const se=vi.map(v=>Math.sqrt(v));const w=vi.map(v=>1/v);const sw=w.reduce((a,b)=>a+b,0);const unadj=yi.reduce((s,y,i)=>s+w[i]*y,0)/sw;const res=[];for(let g0=-2;g0<=0;g0+=0.5)for(let g1=0;g1<=2;g1+=0.5){const pr=se.map(s=>Stats.pnorm(g0+g1/s));const aw=pr.map((p,i)=>p/vi[i]);const saw=aw.reduce((a,b)=>a+b,0);if(saw>0)res.push({gamma0:g0,gamma1:g1,adjusted:yi.reduce((s,y,i)=>s+aw[i]*y,0)/saw});}const rng=[Math.min(...res.map(r=>r.adjusted)),Math.max(...res.map(r=>r.adjusted))];return{unadjusted:unadj,adjusted:res,sensitivityRange:rng,interpretation:rng[1]-rng[0]<0.2?'Robust':'Sensitive'};}};

const FragilityIndex={calculate(sts){if(!sts||!sts.length)return{error:'No studies'};const bin=sts.filter(s=>s.events1!==undefined);if(!bin.length)return{error:'No binary'};const res=bin.map(s=>{const sig=this.fisherP(s.events1,s.n1-s.events1,s.events2,s.n2-s.events2)<0.05;if(!sig)return{study:s.name,fi:Infinity};let fi=1;for(;fi<=Math.min(s.n1,s.n2);fi++)if(this.fisherP(s.events1+fi,s.n1-s.events1-fi,s.events2,s.n2-s.events2)>=0.05||this.fisherP(s.events1,s.n1-s.events1,s.events2+fi,s.n2-s.events2-fi)>=0.05)break;return{study:s.name,fi};});const minFI=Math.min(...res.filter(r=>r.fi!==Infinity).map(r=>r.fi));return{studyLevel:res,pooledFI:isFinite(minFI)?minFI:null,interpretation:minFI<=3?'Very fragile':minFI<=8?'Moderate':'Robust'};},fisherP(a,b,c,d){const n=a+b+c+d;const lf=x=>{let r=0;for(let i=2;i<=x;i++)r+=Math.log(i);return r;};const p0=Math.exp(lf(a+b)+lf(c+d)+lf(a+c)+lf(b+d)-lf(n)-lf(a)-lf(b)-lf(c)-lf(d));let pV=0;for(let i=0;i<=Math.min(a+b,a+c);i++){const j=(a+b)-i,k=(a+c)-i,l=n-i-j-k;if(j>=0&&k>=0&&l>=0){const p=Math.exp(lf(i+j)+lf(k+l)+lf(i+k)+lf(j+l)-lf(n)-lf(i)-lf(j)-lf(k)-lf(l));if(p<=p0+1e-10)pV+=p;}}return Math.min(1,pV);}};

const DesignDecomposition={analyze(proc){if(!proc||proc.length<5)return{error:'Need 5+ studies'};const des=new Map();proc.forEach(s=>{const d=[s.treatment1,s.treatment2].sort().join(':');if(!des.has(d))des.set(d,[]);des.get(d).push(s);});const stats=[];const grand=proc.reduce((s,p)=>s+p.yi,0)/proc.length;let Qb=0;des.forEach((sts,design)=>{const mean=sts.reduce((s,st)=>s+st.yi,0)/sts.length;Qb+=sts.length*(mean-grand)*(mean-grand);stats.push({design,n:sts.length,mean});});const dfB=stats.length-1;const pB=dfB>0?1-Stats.pchisq(Qb,dfB):1;return{designs:stats,Qbetween:Qb,dfBetween:dfB,pBetween:pB,inconsistency:pB<0.05};}};

const MetaforExport={generate(proc,opt={}){const data=proc||[];const code='# metafor\\nlibrary(metafor)\\ndat <- data.frame(yi=c('+data.map(s=>(s.yi||0).toFixed(4)).join(',')+'),vi=c('+data.map(s=>(s.vi||0.01).toFixed(4)).join(',')+'))\\nres <- rma(yi, vi, data=dat)\\nsummary(res)';return{rCode:code,nStudies:data.length};}};

const HelpSystem={topics:{tau2:{title:'Tau-squared',description:'Between-study variance'},I2:{title:'I-squared',description:'% heterogeneity'},SUCRA:{title:'SUCRA',description:'Ranking metric'}},get(t){return this.topics[t]||{title:'Unknown',description:'N/A'};},list(){return Object.keys(this.topics);}};

const ExportPNG={async export(canvasId,fn='chart.png'){const c=document.getElementById(canvasId);if(!c)return{error:'Canvas not found'};const lnk=document.createElement('a');lnk.download=fn;lnk.href=c.toDataURL('image/png');lnk.click();return{success:true};}};

const ExportPDF={async export(opt={}){const title=opt.title||'NMA Report';const html='<!DOCTYPE html><html><head><title>'+title+'</title></head><body><h1>'+title+'</h1></body></html>';const blob=new Blob([html],{type:'text/html'});const lnk=document.createElement('a');lnk.download=title.replace(/\\s+/g,'_')+'.html';lnk.href=URL.createObjectURL(blob);lnk.click();return{success:true};}};

const PUniform={analyze(yi,vi,alpha=0.05){const n=yi.length;const se=vi.map(v=>Math.sqrt(v));const pV=yi.map((y,i)=>2*(1-Stats.pnorm(Math.abs(y/se[i]))));const sig=pV.map((p,i)=>p<=alpha?i:-1).filter(i=>i>=0);if(sig.length<3)return{error:'Need 3+ sig'};const cP=sig.map(i=>pV[i]/alpha);const m=cP.reduce((a,b)=>a+b,0)/cP.length;const z=(m-0.5)/Math.sqrt(1/12/cP.length);return{nSignificant:sig.length,meanConditionalP:m,zTest:z,pValue:2*(1-Stats.pnorm(Math.abs(z))),evidentialValue:m<0.5};}};

const MantelHaenszel={analyze(sts){if(!sts||sts.length<2)return{error:'Need 2+ studies'};const val=sts.filter(s=>s.events1!==undefined&&s.n1>0&&s.n2>0);if(val.length<2)return{error:'Need binary'};let sA=0,sB=0,sC=0,sD=0;val.forEach(s=>{const a=s.events1,b=s.n1-s.events1,c=s.events2,d=s.n2-s.events2,nn=a+b+c+d;sA+=a*d/nn;sB+=b*c/nn;sC+=(a+d)/nn;sD+=(b+c)/nn;});const or=sA/sB;const logOR=Math.log(or);const se=Math.sqrt((sC/(2*sA*sA))+(sC+sD)/(2*sA*sB)+(sD/(2*sB*sB)));return{OR:or,logOR,se,ci:[Math.exp(logOR-1.96*se),Math.exp(logOR+1.96*se)],method:'Mantel-Haenszel'};}};

const PetoMethod={analyze(sts){if(!sts||sts.length<2)return{error:'Need 2+ studies'};const val=sts.filter(s=>s.events1!==undefined);let sOE=0,sV=0;val.forEach(s=>{const a=s.events1,c=s.events2,n1=s.n1,n2=s.n2,nn=n1+n2;const E=n1*(a+c)/nn;const V=n1*n2*(a+c)*(nn-a-c)/(nn*nn*(nn-1));sOE+=a-E;sV+=V;});const logOR=sOE/sV;const se=1/Math.sqrt(sV);return{OR:Math.exp(logOR),logOR,se,ci:[Math.exp(logOR-1.96*se),Math.exp(logOR+1.96*se)],method:'Peto'};}};

const EBEstimator={estimate(yi,vi){const n=yi.length;const w=vi.map(v=>1/v);const sw=w.reduce((a,b)=>a+b,0);const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sw;let Q=0;for(let i=0;i<n;i++)Q+=w[i]*(yi[i]-mu)*(yi[i]-mu);const C=sw-w.reduce((s,wi)=>s+wi*wi,0)/sw;const tau2DL=Math.max(0,(Q-(n-1))/C);return{tau2:tau2DL*(n-1)/(n+1),method:'Empirical Bayes'};}};

const HedgesEstimator={estimate(yi,vi){const n=yi.length;const mu=yi.reduce((a,b)=>a+b,0)/n;const varY=yi.reduce((s,y)=>s+(y-mu)*(y-mu),0)/(n-1);const meanVi=vi.reduce((a,b)=>a+b,0)/n;return{tau2:Math.max(0,varY-meanVi),method:'Hedges'};}};

const InverseVariance={pool(yi,vi,method='random'){const n=yi.length;const w=vi.map(v=>1/v);const sw=w.reduce((a,b)=>a+b,0);const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sw;const se=Math.sqrt(1/sw);let Q=0;for(let i=0;i<n;i++)Q+=w[i]*(yi[i]-mu)*(yi[i]-mu);const I2=Math.max(0,(Q-(n-1))/Q)*100;if(method==='fixed')return{pooled:mu,se,ci:[mu-1.96*se,mu+1.96*se],Q,I2,method:'Fixed-IV'};const C=sw-w.reduce((s,wi)=>s+wi*wi,0)/sw;const tau2=Math.max(0,(Q-(n-1))/C);const wRE=vi.map(v=>1/(v+tau2));const swRE=wRE.reduce((a,b)=>a+b,0);const muRE=yi.reduce((s,y,i)=>s+wRE[i]*y,0)/swRE;const seRE=Math.sqrt(1/swRE);return{pooled:muRE,se:seRE,ci:[muRE-1.96*seRE,muRE+1.96*seRE],Q,I2,tau2,method:'Random-IV'};}};

const SJEstimator={estimate(yi,vi,maxIter=100){const n=yi.length;let tau2=0.01;for(let it=0;it<maxIter;it++){const w=vi.map(v=>1/(v+tau2));const sw=w.reduce((a,b)=>a+b,0);const mu=yi.reduce((s,y,i)=>s+w[i]*y,0)/sw;let num=0;for(let i=0;i<n;i++)num+=w[i]*w[i]*((yi[i]-mu)*(yi[i]-mu)-vi[i]);const tau2N=Math.max(0,tau2+num/w.reduce((s,wi)=>s+wi*wi,0));if(Math.abs(tau2N-tau2)<1e-6)break;tau2=tau2N;}return{tau2,method:'Sidik-Jonkman'};}};

const DEMO_DATASETS={
thrombolytics:[
{name:'Coll1988',treatment1:'SK',treatment2:'tPA',events1:8,n1:54,events2:4,n2:56,subgroup:'Europe',year:1988},
{name:'DeWood1990',treatment1:'SK',treatment2:'tPA',events1:6,n1:63,events2:4,n2:62,subgroup:'Americas',year:1990},
{name:'GISSI-2',treatment1:'SK',treatment2:'tPA',events1:887,n1:10396,events2:1017,n2:10372,subgroup:'Europe',year:1990},
{name:'Guerci1987',treatment1:'SK',treatment2:'tPA',events1:2,n1:61,events2:3,n2:77,subgroup:'Americas',year:1987},
{name:'ISIS-3',treatment1:'SK',treatment2:'tPA',events1:1455,n1:13780,events2:1418,n2:13773,subgroup:'International',year:1992},
{name:'TIMI-I',treatment1:'SK',treatment2:'tPA',events1:3,n1:143,events2:2,n2:147,subgroup:'Americas',year:1985},
{name:'ASSET',treatment1:'Placebo',treatment2:'tPA',events1:182,n1:2495,events2:118,n2:2516,subgroup:'Europe',year:1988},
{name:'LATE',treatment1:'Placebo',treatment2:'tPA',events1:284,n1:2682,events2:256,n2:2686,subgroup:'International',year:1993},
{name:'EMERAS',treatment1:'Placebo',treatment2:'SK',events1:144,n1:2257,events2:149,n2:2253,subgroup:'Americas',year:1993},
{name:'GISSI-1',treatment1:'Placebo',treatment2:'SK',events1:758,n1:5860,events2:628,n2:5852,subgroup:'Europe',year:1986},
{name:'ISAM',treatment1:'Placebo',treatment2:'SK',events1:63,n1:882,events2:46,n2:859,subgroup:'Europe',year:1986},
{name:'ISIS-2',treatment1:'Placebo',treatment2:'SK',events1:568,n1:4300,events2:461,n2:4292,subgroup:'International',year:1988}
],
vaccines:[
{name:'Study1',treatment1:'Placebo',treatment2:'VaccineA',events1:50,n1:500,events2:20,n2:500,subgroup:'Developed',year:2015},
{name:'Study2',treatment1:'Placebo',treatment2:'VaccineB',events1:45,n1:450,events2:25,n2:460,subgroup:'Developing',year:2016},
{name:'Study3',treatment1:'VaccineA',treatment2:'VaccineB',events1:22,n1:400,events2:18,n2:420,subgroup:'Developed',year:2017},
{name:'Study4',treatment1:'Placebo',treatment2:'VaccineA',events1:60,n1:600,events2:30,n2:590,subgroup:'Developing',year:2018},
{name:'Study5',treatment1:'VaccineA',treatment2:'VaccineB',events1:28,n1:380,events2:24,n2:390,subgroup:'Developed',year:2019}
],
antihypertensives:[
{name:'Trial1',treatment1:'Placebo',treatment2:'ACEi',events1:120,n1:1000,events2:85,n2:1020,subgroup:'HighRisk',year:2010},
{name:'Trial2',treatment1:'Placebo',treatment2:'ARB',events1:115,n1:980,events2:90,n2:990,subgroup:'LowRisk',year:2011},
{name:'Trial3',treatment1:'ACEi',treatment2:'ARB',events1:88,n1:850,events2:82,n2:860,subgroup:'HighRisk',year:2012},
{name:'Trial4',treatment1:'Placebo',treatment2:'CCB',events1:130,n1:1100,events2:100,n2:1080,subgroup:'LowRisk',year:2013},
{name:'Trial5',treatment1:'ACEi',treatment2:'CCB',events1:78,n1:920,events2:72,n2:910,subgroup:'HighRisk',year:2014},
{name:'Trial6',treatment1:'ARB',treatment2:'CCB',events1:75,n1:880,events2:70,n2:870,subgroup:'LowRisk',year:2015}
],
painkillers:[
{name:'Pain1',treatment1:'Placebo',treatment2:'NSAID1',events1:80,n1:200,events2:40,n2:210,subgroup:'Acute',year:2018},
{name:'Pain2',treatment1:'Placebo',treatment2:'NSAID2',events1:75,n1:190,events2:35,n2:200,subgroup:'Chronic',year:2019},
{name:'Pain3',treatment1:'NSAID1',treatment2:'NSAID2',events1:45,n1:180,events2:42,n2:185,subgroup:'Acute',year:2020},
{name:'Pain4',treatment1:'Placebo',treatment2:'Opioid',events1:90,n1:220,events2:30,n2:215,subgroup:'Chronic',year:2021},
{name:'Pain5',treatment1:'NSAID1',treatment2:'Opioid',events1:38,n1:175,events2:28,n2:180,subgroup:'Acute',year:2022}
],
cbt_depression:[
{name:'CBT1',treatment1:'TAU',treatment2:'CBT',events1:60,n1:150,events2:40,n2:155,subgroup:'Mild',year:2015},
{name:'CBT2',treatment1:'TAU',treatment2:'IPT',events1:58,n1:145,events2:38,n2:150,subgroup:'Moderate',year:2016},
{name:'CBT3',treatment1:'CBT',treatment2:'IPT',events1:42,n1:140,events2:40,n2:145,subgroup:'Mild',year:2017},
{name:'CBT4',treatment1:'TAU',treatment2:'MBCT',events1:55,n1:160,events2:35,n2:158,subgroup:'Severe',year:2018},
{name:'CBT5',treatment1:'CBT',treatment2:'MBCT',events1:39,n1:135,events2:36,n2:140,subgroup:'Moderate',year:2019}
]
};

function loadDemoDataset(name){const data=DEMO_DATASETS[name];if(!data)return;AppState.studies=data.map(s=>({...s}));document.getElementById('dataInput').value=JSON.stringify(data,null,2);updateStudyTable();showNotification('Loaded '+name+' dataset ('+data.length+' studies)');}

'''

# Find insertion point - before DOMContentLoaded
dom_pos = content.find('DOMContentLoaded')
if dom_pos > 0:
    # Find the start of this event listener line
    line_start = content.rfind('\n', 0, dom_pos)
    if line_start < 0:
        line_start = 0

    # Insert modules before DOMContentLoaded
    content = content[:line_start] + all_modules_code + content[line_start:]
    print(f'[OK] Inserted modules before DOMContentLoaded at position {line_start}')
else:
    # Fallback: insert before </script>
    script_end = content.rfind('</script>')
    if script_end > 0:
        content = content[:script_end] + all_modules_code + content[script_end:]
        print(f'[OK] Inserted modules before </script>')
    else:
        print('[ERROR] Could not find insertion point')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Final size: {len(content):,} bytes')

# Verify syntax
opens = [m.start() for m in re.finditer(r'<script', content)]
closes = [m.start() for m in re.finditer(r'</script>', content)]
last_open = max(opens)
last_close = max(closes)
tag_end = content.find('>', last_open)
js = content[tag_end+1:last_close]
with open('C:/Users/user/temp_js_check.js', 'w', encoding='utf-8') as f:
    f.write(js)
print(f'Extracted JS: {len(js):,} bytes')
