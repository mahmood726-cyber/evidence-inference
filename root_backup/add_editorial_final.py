"""Add final editorial recommendations to NMA Pro v6.2"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original file size: {len(content)} bytes')

# 1. Profile-Likelihood CI for tau-squared
profile_likelihood = '''
const ProfileLikelihood={
  computeTau2CI(processed,tau2,alpha=0.05){
    if(!processed||processed.length<3||tau2===undefined)return null;
    const n=processed.length;
    const yi=processed.map(p=>p.yi||0);
    const vi=processed.map(p=>p.vi||0.1);
    const logLik=(t2)=>{
      let ll=0;
      for(let i=0;i<n;i++){
        const w=1/(vi[i]+t2);
        const mu=yi.reduce((s,y,j)=>s+y/(vi[j]+t2),0)/yi.reduce((s,_,j)=>s+1/(vi[j]+t2),0);
        ll+=-0.5*(Math.log(vi[i]+t2)+(yi[i]-mu)*(yi[i]-mu)*w);
      }
      return ll;
    };
    const ll0=logLik(tau2);
    const critVal=3.841/2;
    const findBound=(dir)=>{
      let bound=tau2;
      const step=dir>0?0.01:-0.01;
      let maxIter=1000;
      while(maxIter-->0){
        bound+=step;
        if(bound<0)return 0;
        if(bound>10)return 10;
        if(ll0-logLik(bound)>critVal)return bound;
      }
      return bound;
    };
    return{lower:Math.max(0,findBound(-1)),upper:findBound(1),method:'Profile Likelihood'};
  },
  computeQProfile(processed,tau2,alpha=0.05){
    if(!processed||processed.length<3)return null;
    const n=processed.length;
    const k=n-1;
    const yi=processed.map(p=>p.yi||0);
    const vi=processed.map(p=>p.vi||0.1);
    const calcQ=(t2)=>{
      const wi=vi.map(v=>1/(v+t2));
      const W=wi.reduce((a,b)=>a+b,0);
      const mu=yi.reduce((s,y,i)=>s+y*wi[i],0)/W;
      return yi.reduce((s,y,i)=>s+(y-mu)*(y-mu)*wi[i],0);
    };
    const qLower=this.chiSquareQuantile(1-alpha/2,k);
    const qUpper=this.chiSquareQuantile(alpha/2,k);
    const findTau2=(targetQ,start,dir)=>{
      let t2=start;
      const step=dir*0.001;
      let iter=10000;
      while(iter-->0){
        const q=calcQ(t2);
        if(dir>0&&q<targetQ)return t2;
        if(dir<0&&q>targetQ)return Math.max(0,t2);
        t2+=step;
        if(t2<0)return 0;
        if(t2>10)return 10;
      }
      return t2;
    };
    const lower=findTau2(qLower,tau2,-1);
    const upper=findTau2(qUpper,tau2,1);
    return{lower,upper,method:'Q-Profile'};
  },
  chiSquareQuantile(p,df){
    if(p<=0)return 0;
    if(p>=1)return Infinity;
    let x=df;
    for(let i=0;i<100;i++){
      const cdf=this.chiSquareCDF(x,df);
      const pdf=this.chiSquarePDF(x,df);
      if(Math.abs(cdf-p)<1e-10||pdf<1e-15)break;
      x=x-(cdf-p)/pdf;
      if(x<0)x=0.001;
    }
    return x;
  },
  chiSquareCDF(x,df){
    if(x<=0)return 0;
    return this.gammainc(df/2,x/2);
  },
  chiSquarePDF(x,df){
    if(x<=0)return 0;
    const k=df/2;
    return Math.pow(x,k-1)*Math.exp(-x/2)/(Math.pow(2,k)*this.gamma(k));
  },
  gammainc(a,x){
    if(x<0)return 0;
    if(x===0)return 0;
    if(x<a+1){
      let sum=1/a,term=1/a;
      for(let n=1;n<100;n++){
        term*=x/(a+n);
        sum+=term;
        if(Math.abs(term)<1e-10)break;
      }
      return sum*Math.exp(-x+a*Math.log(x)-this.gammaln(a));
    }else{
      let f=1,c=1,d=1/(x+1-a);
      for(let n=1;n<100;n++){
        const an=-n*(n-a);
        const bn=x+2*n+1-a;
        d=bn+an*d;if(Math.abs(d)<1e-30)d=1e-30;d=1/d;
        c=bn+an/c;if(Math.abs(c)<1e-30)c=1e-30;
        f*=d*c;
        if(Math.abs(d*c-1)<1e-10)break;
      }
      return 1-Math.exp(-x+a*Math.log(x)-this.gammaln(a))*f;
    }
  },
  gammaln(x){
    const c=[76.18009172947146,-86.50532032941677,24.01409824083091,-1.231739572450155,0.1208650973866179e-2,-0.5395239384953e-5];
    let y=x,tmp=x+5.5;
    tmp-=(x+0.5)*Math.log(tmp);
    let ser=1.000000000190015;
    for(let j=0;j<6;j++)ser+=c[j]/++y;
    return-tmp+Math.log(2.5066282746310005*ser/x);
  },
  gamma(x){return Math.exp(this.gammaln(x));}
};
'''

# 2. GRADE-NMA Certainty Assessment
grade_nma = '''
const GradeNMA={
  domains:['withinStudyBias','acrossStudyBias','indirectness','imprecision','heterogeneity','incoherence'],
  assessCertainty(comparison,results,studies){
    const assessment={comparison,domains:{},overall:'',explanation:[]};
    assessment.domains.withinStudyBias=this.assessWithinStudyBias(studies);
    assessment.domains.acrossStudyBias=this.assessAcrossStudyBias(results);
    assessment.domains.indirectness=this.assessIndirectness(comparison,results);
    assessment.domains.imprecision=this.assessImprecision(comparison,results);
    assessment.domains.heterogeneity=this.assessHeterogeneity(results);
    assessment.domains.incoherence=this.assessIncoherence(comparison,results);
    const domainLevels=Object.values(assessment.domains).map(d=>d.level);
    const concerns=domainLevels.filter(l=>l!=='No concerns').length;
    const majorConcerns=domainLevels.filter(l=>l==='Major concerns').length;
    if(majorConcerns>=2)assessment.overall='Very Low';
    else if(majorConcerns===1||concerns>=3)assessment.overall='Low';
    else if(concerns>=2)assessment.overall='Moderate';
    else if(concerns===1)assessment.overall='Moderate';
    else assessment.overall='High';
    return assessment;
  },
  assessWithinStudyBias(studies){
    if(!studies||studies.length===0)return{level:'No information',reason:'No studies'};
    const robCounts={low:0,unclear:0,high:0};
    studies.forEach(s=>{
      const rob=s.rob||'unclear';
      robCounts[rob]=(robCounts[rob]||0)+1;
    });
    const pctHigh=robCounts.high/studies.length;
    const pctLow=robCounts.low/studies.length;
    if(pctHigh>0.5)return{level:'Major concerns',reason:`${(pctHigh*100).toFixed(0)}% high ROB studies`};
    if(pctHigh>0.25||pctLow<0.5)return{level:'Some concerns',reason:'Mixed ROB across studies'};
    return{level:'No concerns',reason:'Majority low ROB'};
  },
  assessAcrossStudyBias(results){
    if(!results)return{level:'No information',reason:'No results'};
    return{level:'Some concerns',reason:'Small study effects not formally tested'};
  },
  assessIndirectness(comparison,results){
    if(!results||!results.processed)return{level:'No information',reason:'No data'};
    const isDirect=results.processed.some(p=>{
      const t1=p.treatment1||p.treat1;
      const t2=p.treatment2||p.treat2;
      const comp=comparison.split(' vs ');
      return(t1===comp[0]&&t2===comp[1])||(t1===comp[1]&&t2===comp[0]);
    });
    if(isDirect)return{level:'No concerns',reason:'Direct evidence available'};
    return{level:'Some concerns',reason:'Indirect evidence only'};
  },
  assessImprecision(comparison,results){
    if(!results||!results.effects)return{level:'No information',reason:'No effects'};
    return{level:'Some concerns',reason:'CI width not formally evaluated'};
  },
  assessHeterogeneity(results){
    if(!results||!results.heterogeneity)return{level:'No information',reason:'No heterogeneity data'};
    const I2=results.heterogeneity.I2||0;
    if(I2>75)return{level:'Major concerns',reason:`I²=${I2.toFixed(0)}% (high)`};
    if(I2>50)return{level:'Some concerns',reason:`I²=${I2.toFixed(0)}% (moderate)`};
    return{level:'No concerns',reason:`I²=${I2.toFixed(0)}% (low)`};
  },
  assessIncoherence(comparison,results){
    if(!results||!results.consistency)return{level:'No information',reason:'Consistency not assessed'};
    const pval=results.consistency.pValue;
    if(pval&&pval<0.05)return{level:'Major concerns',reason:`Inconsistency detected (p=${pval.toFixed(3)})`};
    if(pval&&pval<0.1)return{level:'Some concerns',reason:`Possible inconsistency (p=${pval.toFixed(3)})`};
    return{level:'No concerns',reason:'No evidence of inconsistency'};
  },
  generateSummaryTable(assessments){
    let html='<table class="grade-table"><thead><tr><th>Comparison</th>';
    this.domains.forEach(d=>html+=`<th>${d}</th>`);
    html+='<th>Overall</th></tr></thead><tbody>';
    assessments.forEach(a=>{
      html+=`<tr><td>${a.comparison}</td>`;
      this.domains.forEach(d=>{
        const level=a.domains[d]?.level||'?';
        const cls=level.includes('Major')?'major':level.includes('Some')?'some':'none';
        html+=`<td class="${cls}" title="${a.domains[d]?.reason||''}">${level}</td>`;
      });
      html+=`<td class="overall-${a.overall.toLowerCase().replace(' ','-')}">${a.overall}</td></tr>`;
    });
    html+='</tbody></table>';
    return html;
  }
};
'''

# 3. Node-Splitting for Inconsistency Testing
node_splitting = '''
const NodeSplittingTest={
  analyze(studies,effectMeasure,reference){
    if(!studies||studies.length<3)return null;
    const comparisons=new Map();
    studies.forEach(s=>{
      const t1=s.treatment1||s.treat1;
      const t2=s.treatment2||s.treat2;
      const key=[t1,t2].sort().join(' vs ');
      if(!comparisons.has(key))comparisons.set(key,[]);
      comparisons.get(key).push(s);
    });
    const results=[];
    comparisons.forEach((studyList,comparison)=>{
      if(studyList.length<1)return;
      const direct=this.computeDirectEstimate(studyList,effectMeasure);
      const indirect=this.computeIndirectEstimate(studies,studyList,comparison,effectMeasure,reference);
      if(direct&&indirect){
        const diff=direct.effect-indirect.effect;
        const seDiff=Math.sqrt(direct.se*direct.se+indirect.se*indirect.se);
        const z=Math.abs(diff/seDiff);
        const pval=2*(1-this.normalCDF(z));
        results.push({
          comparison,
          nDirect:studyList.length,
          direct:{effect:direct.effect,se:direct.se,ci:[direct.effect-1.96*direct.se,direct.effect+1.96*direct.se]},
          indirect:{effect:indirect.effect,se:indirect.se,ci:[indirect.effect-1.96*indirect.se,indirect.effect+1.96*indirect.se]},
          difference:diff,
          seDifference:seDiff,
          zScore:z,
          pValue:pval,
          inconsistent:pval<0.05
        });
      }
    });
    const globalP=this.computeGlobalInconsistency(results);
    return{comparisons:results,globalTest:{chi2:globalP.chi2,df:globalP.df,pValue:globalP.pval},hasInconsistency:results.some(r=>r.inconsistent)};
  },
  computeDirectEstimate(studies,effectMeasure){
    if(studies.length===0)return null;
    const effects=studies.map(s=>{
      const yi=s.yi!==undefined?s.yi:this.computeEffect(s,effectMeasure);
      const vi=s.vi!==undefined?s.vi:this.computeVariance(s,effectMeasure);
      return{yi,vi};
    }).filter(e=>e.yi!==null&&e.vi>0);
    if(effects.length===0)return null;
    const weights=effects.map(e=>1/e.vi);
    const W=weights.reduce((a,b)=>a+b,0);
    const effect=effects.reduce((s,e,i)=>s+e.yi*weights[i],0)/W;
    const se=Math.sqrt(1/W);
    return{effect,se};
  },
  computeIndirectEstimate(allStudies,directStudies,comparison,effectMeasure,reference){
    const indirectStudies=allStudies.filter(s=>!directStudies.includes(s));
    if(indirectStudies.length<2)return{effect:0,se:1};
    const est=this.computeDirectEstimate(indirectStudies,effectMeasure);
    return est||{effect:0,se:1};
  },
  computeEffect(s,effectMeasure){
    const a=(s.events1||0)+0.5,b=s.n1-(s.events1||0)+0.5;
    const c=(s.events2||0)+0.5,d=s.n2-(s.events2||0)+0.5;
    if(effectMeasure==='OR')return Math.log((a*d)/(b*c));
    if(effectMeasure==='RR')return Math.log((a/(a+b))/(c/(c+d)));
    return Math.log((a*d)/(b*c));
  },
  computeVariance(s,effectMeasure){
    const a=(s.events1||0)+0.5,b=s.n1-(s.events1||0)+0.5;
    const c=(s.events2||0)+0.5,d=s.n2-(s.events2||0)+0.5;
    return 1/a+1/b+1/c+1/d;
  },
  computeGlobalInconsistency(results){
    if(results.length===0)return{chi2:0,df:0,pval:1};
    const chi2=results.reduce((s,r)=>{
      const z=r.difference/r.seDifference;
      return s+z*z;
    },0);
    const df=results.length;
    const pval=1-this.chiSquareCDF(chi2,df);
    return{chi2,df,pval};
  },
  normalCDF(x){
    const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
    const sign=x<0?-1:1;
    x=Math.abs(x)/Math.sqrt(2);
    const t=1/(1+p*x);
    const y=1-((((a5*t+a4)*t+a3)*t+a2)*t+a1)*t*Math.exp(-x*x);
    return 0.5*(1+sign*y);
  },
  chiSquareCDF(x,df){
    if(x<=0)return 0;
    return ProfileLikelihood.gammainc(df/2,x/2);
  },
  generateReport(results){
    if(!results)return'<p>Insufficient data for node-splitting</p>';
    let html='<h3>Node-Splitting Inconsistency Test</h3>';
    html+='<table class="node-split-table"><thead><tr><th>Comparison</th><th>Direct</th><th>Indirect</th><th>Difference</th><th>P-value</th><th>Status</th></tr></thead><tbody>';
    results.comparisons.forEach(r=>{
      const status=r.inconsistent?'<span class="inconsistent">Inconsistent</span>':'<span class="consistent">Consistent</span>';
      html+=`<tr>
        <td>${r.comparison} (n=${r.nDirect})</td>
        <td>${r.direct.effect.toFixed(3)} [${r.direct.ci[0].toFixed(3)}, ${r.direct.ci[1].toFixed(3)}]</td>
        <td>${r.indirect.effect.toFixed(3)} [${r.indirect.ci[0].toFixed(3)}, ${r.indirect.ci[1].toFixed(3)}]</td>
        <td>${r.difference.toFixed(3)} (SE=${r.seDifference.toFixed(3)})</td>
        <td>${r.pValue.toFixed(4)}</td>
        <td>${status}</td>
      </tr>`;
    });
    html+='</tbody></table>';
    html+=`<p><strong>Global inconsistency test:</strong> Chi²=${results.globalTest.chi2.toFixed(2)}, df=${results.globalTest.df}, p=${results.globalTest.pValue.toFixed(4)}</p>`;
    if(results.hasInconsistency){
      html+='<p class="warning">⚠️ Evidence of inconsistency detected. Consider investigating sources of heterogeneity.</p>';
    }else{
      html+='<p class="success">✓ No significant inconsistency detected between direct and indirect evidence.</p>';
    }
    return html;
  }
};
'''

# Find insertion point (before closing </script>)
script_end = content.rfind('</script>')

# Check if modules already exist
modules_to_add = []
if 'const ProfileLikelihood=' not in content:
    modules_to_add.append(('ProfileLikelihood', profile_likelihood))
if 'const GradeNMA=' not in content:
    modules_to_add.append(('GradeNMA', grade_nma))
if 'const NodeSplittingTest=' not in content:
    modules_to_add.append(('NodeSplittingTest', node_splitting))

if modules_to_add and script_end >= 0:
    insertion = '\n'.join([code for name, code in modules_to_add])
    content = content[:script_end] + insertion + '\n' + content[script_end:]
    for name, _ in modules_to_add:
        print(f'Added {name} module')

# Save
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Final file size: {len(content)} bytes')
print('Done!')
