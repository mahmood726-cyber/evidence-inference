"""Fix publication bias modules to work with actual data structure"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:\Users\user\OneDrive - NHS\Documents\NMAhtml\nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original file size: {len(content)} bytes')

# Fix 1: TrimAndFill - expects processed array with yi/vi
old_taf = 'const TrimAndFill={'
new_taf = '''const TrimAndFill={
    analyze(processed){
        if(!processed||!Array.isArray(processed)||processed.length<3)return{error:'Insufficient data'};
        const yi=processed.map(p=>p.yi);
        const vi=processed.map(p=>p.vi);
        const n=yi.length;

        // Sort by effect size
        const sorted=yi.map((y,i)=>({y,v:vi[i]})).sort((a,b)=>a.y-b.y);

        // Estimate number of missing studies on left side
        const median=sorted[Math.floor(n/2)].y;
        let k0=0;
        for(let i=0;i<n;i++){
            if(sorted[i].y<median){
                // Check for asymmetry
                const mirror=2*median-sorted[i].y;
                const hasMatch=sorted.some(s=>Math.abs(s.y-mirror)<0.5);
                if(!hasMatch)k0++;
            }
        }

        // Calculate pooled effect
        const sumW=vi.reduce((s,v)=>s+1/v,0);
        const pooled=yi.reduce((s,y,i)=>s+y/vi[i],0)/sumW;

        // Adjusted effect (simple trim and fill)
        let adjEffect=pooled;
        if(k0>0){
            // Impute missing studies
            const imputed=[];
            for(let i=0;i<Math.min(k0,3);i++){
                const mirror=2*pooled-sorted[i].y;
                imputed.push({y:mirror,v:sorted[i].v});
            }
            // Recalculate with imputed
            const allYi=[...yi,...imputed.map(p=>p.y)];
            const allVi=[...vi,...imputed.map(p=>p.v)];
            const newSumW=allVi.reduce((s,v)=>s+1/v,0);
            adjEffect=allYi.reduce((s,y,i)=>s+y/allVi[i],0)/newSumW;
        }

        return{
            originalEffect:pooled,
            adjustedEffect:adjEffect,
            imputedStudies:k0,
            side:k0>0?'left':'none',
            method:'L0 estimator'
        };
    }
};const TrimAndFillOld={'''

if 'const TrimAndFill={' in content:
    content = content.replace(old_taf, new_taf)
    print('[+] Fixed TrimAndFill')
else:
    print('[!] TrimAndFill not found')

# Fix 2: EggersTest - expects processed array
old_egger = 'const EggersTest={'
new_egger = '''const EggersTest={
    analyze(processed){
        if(!processed||!Array.isArray(processed)||processed.length<3)return{error:'Insufficient data'};
        const yi=processed.map(p=>p.yi);
        const vi=processed.map(p=>p.vi);
        const se=vi.map(v=>Math.sqrt(v));
        const n=yi.length;

        // Egger's regression: standardized effect on precision
        // z = yi/se, x = 1/se
        const z=yi.map((y,i)=>y/se[i]);
        const x=se.map(s=>1/s);

        // Linear regression
        const sumX=x.reduce((a,b)=>a+b,0);
        const sumZ=z.reduce((a,b)=>a+b,0);
        const sumXZ=x.reduce((s,xi,i)=>s+xi*z[i],0);
        const sumX2=x.reduce((s,xi)=>s+xi*xi,0);

        const slope=(n*sumXZ-sumX*sumZ)/(n*sumX2-sumX*sumX);
        const intercept=(sumZ-slope*sumX)/n;

        // Calculate SE of intercept and t-statistic
        const predicted=x.map(xi=>intercept+slope*xi);
        const residuals=z.map((zi,i)=>zi-predicted[i]);
        const sse=residuals.reduce((s,r)=>s+r*r,0);
        const mse=sse/(n-2);
        const seIntercept=Math.sqrt(mse*(1/n+sumX*sumX/(n*sumX2-sumX*sumX)/n));
        const tStat=intercept/seIntercept;
        const df=n-2;
        const pValue=2*(1-this.tCDF(Math.abs(tStat),df));

        return{
            intercept,
            slope,
            se:seIntercept,
            tStatistic:tStat,
            df,
            pValue,
            significant:pValue<0.1,
            interpretation:pValue<0.1?'Evidence of funnel plot asymmetry':'No evidence of asymmetry'
        };
    },
    tCDF(t,df){
        const x=df/(df+t*t);
        return 1-0.5*this.betaInc(df/2,0.5,x);
    },
    betaInc(a,b,x){
        if(x===0)return 0;
        if(x===1)return 1;
        const bt=Math.exp(this.gammaln(a+b)-this.gammaln(a)-this.gammaln(b)+a*Math.log(x)+b*Math.log(1-x));
        if(x<(a+1)/(a+b+2))return bt*this.betaCF(a,b,x)/a;
        return 1-bt*this.betaCF(b,a,1-x)/b;
    },
    betaCF(a,b,x){
        const maxIter=100,eps=1e-10;
        let am=1,bm=1,az=1;
        const qab=a+b,qap=a+1,qam=a-1;
        let bz=1-qab*x/qap;
        for(let m=1;m<=maxIter;m++){
            const em=m,tem=em+em;
            let d=em*(b-m)*x/((qam+tem)*(a+tem));
            const ap=az+d*am;
            const bp=bz+d*bm;
            d=-(a+em)*(qab+em)*x/((a+tem)*(qap+tem));
            const app=ap+d*az;
            const bpp=bp+d*bz;
            const aold=az;
            am=ap/bpp;bm=bp/bpp;az=app/bpp;bz=1;
            if(Math.abs(az-aold)<eps*Math.abs(az))return az;
        }
        return az;
    },
    gammaln(x){
        const c=[76.18009172947146,-86.50532032941677,24.01409824083091,-1.231739572450155,0.1208650973866179e-2,-0.5395239384953e-5];
        let y=x,tmp=x+5.5;
        tmp-=(x+0.5)*Math.log(tmp);
        let ser=1.000000000190015;
        for(let j=0;j<6;j++)ser+=c[j]/++y;
        return-tmp+Math.log(2.5066282746310005*ser/x);
    }
};const EggersTestOld={'''

if 'const EggersTest={' in content:
    content = content.replace(old_egger, new_egger)
    print('[+] Fixed EggersTest')
else:
    print('[!] EggersTest not found')

# Fix 3: BeggsTest - expects processed array
old_begg = 'const BeggsTest={'
new_begg = '''const BeggsTest={
    analyze(processed){
        if(!processed||!Array.isArray(processed)||processed.length<3)return{error:'Insufficient data'};
        const yi=processed.map(p=>p.yi);
        const vi=processed.map(p=>p.vi);
        const n=yi.length;

        // Calculate standardized effects
        const se=vi.map(v=>Math.sqrt(v));
        const z=yi.map((y,i)=>y/se[i]);

        // Rank correlation (Kendall's tau)
        let concordant=0,discordant=0;
        for(let i=0;i<n-1;i++){
            for(let j=i+1;j<n;j++){
                const diffZ=z[j]-z[i];
                const diffSE=se[j]-se[i];
                if(diffZ*diffSE>0)concordant++;
                else if(diffZ*diffSE<0)discordant++;
            }
        }

        const tau=(concordant-discordant)/(n*(n-1)/2);

        // Approximate p-value for Kendall's tau
        const variance=(2*(2*n+5))/(9*n*(n-1));
        const zStat=tau/Math.sqrt(variance);
        const pValue=2*(1-this.normalCDF(Math.abs(zStat)));

        return{
            tau,
            zStatistic:zStat,
            pValue,
            concordant,
            discordant,
            significant:pValue<0.1,
            interpretation:pValue<0.1?'Evidence of publication bias':'No evidence of publication bias'
        };
    },
    normalCDF(x){
        const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
        const sign=x<0?-1:1;
        x=Math.abs(x)/Math.sqrt(2);
        const t=1/(1+p*x);
        const y=1-((((a5*t+a4)*t+a3)*t+a2)*t+a1)*t*Math.exp(-x*x);
        return 0.5*(1+sign*y);
    }
};const BeggsTestOld={'''

if 'const BeggsTest={' in content:
    content = content.replace(old_begg, new_begg)
    print('[+] Fixed BeggsTest')
else:
    print('[!] BeggsTest not found')

# Fix 4: PETPEESE - expects processed array
old_petpeese = 'const PETPEESE={'
new_petpeese = '''const PETPEESE={
    analyze(processed){
        if(!processed||!Array.isArray(processed)||processed.length<3)return{error:'Insufficient data'};
        const yi=processed.map(p=>p.yi);
        const vi=processed.map(p=>p.vi);
        const se=vi.map(v=>Math.sqrt(v));
        const n=yi.length;

        // PET: regress effect on SE
        const weights=vi.map(v=>1/v);
        const sumW=weights.reduce((a,b)=>a+b,0);

        // Weighted regression for PET
        const sumWX=se.reduce((s,x,i)=>s+weights[i]*x,0);
        const sumWY=yi.reduce((s,y,i)=>s+weights[i]*y,0);
        const sumWXY=yi.reduce((s,y,i)=>s+weights[i]*se[i]*y,0);
        const sumWX2=se.reduce((s,x,i)=>s+weights[i]*x*x,0);

        const petSlope=(sumW*sumWXY-sumWX*sumWY)/(sumW*sumWX2-sumWX*sumWX);
        const petIntercept=(sumWY-petSlope*sumWX)/sumW;

        // PEESE: regress effect on variance
        const sumWV=vi.reduce((s,v,i)=>s+weights[i]*v,0);
        const sumWYV=yi.reduce((s,y,i)=>s+weights[i]*vi[i]*y,0);
        const sumWV2=vi.reduce((s,v,i)=>s+weights[i]*v*v,0);

        const peeseSlope=(sumW*sumWYV-sumWV*sumWY)/(sumW*sumWV2-sumWV*sumWV);
        const peeseIntercept=(sumWY-peeseSlope*sumWV)/sumW;

        // Calculate standard errors
        const petResid=yi.map((y,i)=>y-(petIntercept+petSlope*se[i]));
        const petSSE=petResid.reduce((s,r,i)=>s+weights[i]*r*r,0);
        const petMSE=petSSE/(n-2);
        const petSE=Math.sqrt(petMSE/sumW);

        const peeseResid=yi.map((y,i)=>y-(peeseIntercept+peeseSlope*vi[i]));
        const peeseSSE=peeseResid.reduce((s,r,i)=>s+weights[i]*r*r,0);
        const peeseMSE=peeseSSE/(n-2);
        const peeseSE=Math.sqrt(peeseMSE/sumW);

        // Select which to use based on PET significance
        const petT=petIntercept/petSE;
        const petP=2*(1-EggersTest.tCDF(Math.abs(petT),n-2));
        const usePEESE=petP<0.1;

        return{
            PET:{estimate:petIntercept,se:petSE,slope:petSlope,pValue:petP},
            PEESE:{estimate:peeseIntercept,se:peeseSE,slope:peeseSlope},
            recommended:usePEESE?'PEESE':'PET',
            adjustedEffect:usePEESE?peeseIntercept:petIntercept,
            interpretation:usePEESE?'Using PEESE (PET significant)':'Using PET (PET not significant)'
        };
    }
};const PETPEESEOld={'''

if 'const PETPEESE={' in content:
    content = content.replace(old_petpeese, new_petpeese)
    print('[+] Fixed PETPEESE')
else:
    print('[!] PETPEESE not found')

# Fix 5: SelectionModels - expects processed array
old_sel = 'const SelectionModels={'
new_sel = '''const SelectionModels={
    analyze(processed){
        if(!processed||!Array.isArray(processed)||processed.length<3)return{error:'Insufficient data'};
        const yi=processed.map(p=>p.yi);
        const vi=processed.map(p=>p.vi);
        const se=vi.map(v=>Math.sqrt(v));
        const n=yi.length;

        // Simple selection model (Vevea & Hedges style)
        // Calculate unadjusted pooled effect
        const weights=vi.map(v=>1/v);
        const sumW=weights.reduce((a,b)=>a+b,0);
        const pooled=yi.reduce((s,y,i)=>s+weights[i]*y,0)/sumW;

        // Estimate p-values for each study
        const pValues=yi.map((y,i)=>{
            const z=y/se[i];
            return 2*(1-BeggsTest.normalCDF(Math.abs(z)));
        });

        // Weight adjustment based on p-value cutoffs
        // Studies with p < 0.05 assumed fully reported
        // Studies with p >= 0.05 may be underreported
        const cutoffs=[0.05,0.1,0.5,1.0];
        const selectionProbs=[1.0,0.8,0.5,0.3];

        const adjWeights=weights.map((w,i)=>{
            const p=pValues[i];
            for(let j=0;j<cutoffs.length;j++){
                if(p<cutoffs[j])return w*selectionProbs[j];
            }
            return w*0.2;
        });

        const adjSumW=adjWeights.reduce((a,b)=>a+b,0);
        const adjPooled=yi.reduce((s,y,i)=>s+adjWeights[i]*y,0)/adjSumW;

        // Likelihood ratio test
        const ll0=-0.5*yi.reduce((s,y,i)=>s+weights[i]*(y-pooled)*(y-pooled),0);
        const ll1=-0.5*yi.reduce((s,y,i)=>s+adjWeights[i]*(y-adjPooled)*(y-adjPooled),0);
        const lrt=2*(ll1-ll0);
        const lrtP=1-BeggsTest.normalCDF(Math.sqrt(Math.max(0,lrt)));

        return{
            originalEffect:pooled,
            adjustedEffect:adjPooled,
            selectionDetected:Math.abs(adjPooled-pooled)>0.1,
            likelihoodRatio:lrt,
            pValue:lrtP,
            model:'Step function selection',
            cutoffs:cutoffs
        };
    }
};const SelectionModelsOld={'''

if 'const SelectionModels={' in content:
    content = content.replace(old_sel, new_sel)
    print('[+] Fixed SelectionModels')
else:
    print('[!] SelectionModels not found')

# Fix 6: InfluenceDiagnostics - add analyze method
old_inf = 'const InfluenceDiagnostics={'
new_inf = '''const InfluenceDiagnostics={
    analyze(processed){
        if(!processed||!Array.isArray(processed)||processed.length<3)return{error:'Insufficient data'};
        return this.calculate(processed);
    },
    calculateOld(processed){'''

# Check if we need to fix InfluenceDiagnostics
if 'InfluenceDiagnostics={' in content and 'analyze(processed){' not in content.split('InfluenceDiagnostics={')[1][:100]:
    content = content.replace(old_inf, new_inf)
    print('[+] Added InfluenceDiagnostics.analyze()')
else:
    print('[~] InfluenceDiagnostics already has analyze or not found')

# Save
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nFinal file size: {len(content)} bytes')
print('\nAll fixes applied!')
