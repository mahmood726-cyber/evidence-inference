#!/usr/bin/env python3
"""Add standalone Stats functions for new modules"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("ADDING STANDALONE STATS FUNCTIONS")
print("="*70)

# Add standalone Stats before StandaloneRNG
standalone_stats = '''
// Standalone Stats for new advanced modules
const Stats={
logGamma(x){if(x<=0)return Infinity;if(x<0.5)return Math.log(Math.PI/Math.sin(Math.PI*x))-this.logGamma(1-x);x-=1;const g=7,c=[0.99999999999980993,676.5203681218851,-1259.1392167224028,771.32342877765313,-176.61502916214059,12.507343278686905,-0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7];let sum=c[0];for(let i=1;i<g+2;i++)sum+=c[i]/(x+i);const t=x+g+0.5;return 0.5*Math.log(2*Math.PI)+(x+0.5)*Math.log(t)-t+Math.log(sum);},
pnorm(x){const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;const sign=x<0?-1:1;x=Math.abs(x)/Math.sqrt(2);const t=1/(1+p*x);const y=1-((((a5*t+a4)*t+a3)*t+a2)*t+a1)*t*Math.exp(-x*x);return 0.5*(1+sign*y);},
qnorm(p){if(p<=0)return-Infinity;if(p>=1)return Infinity;if(p===0.5)return 0;const a=[-3.969683028665376e1,2.209460984245205e2,-2.759285104469687e2,1.383577518672690e2,-3.066479806614716e1,2.506628277459239e0];const b=[-5.447609879822406e1,1.615858368580409e2,-1.556989798598866e2,6.680131188771972e1,-1.328068155288572e1];const c=[-7.784894002430293e-3,-3.223964580411365e-1,-2.400758277161838e0,-2.549732539343734e0,4.374664141464968e0,2.938163982698783e0];const d=[7.784695709041462e-3,3.224671290700398e-1,2.445134137142996e0,3.754408661907416e0];const pLow=0.02425,pHigh=1-pLow;let q,r;if(p<pLow){q=Math.sqrt(-2*Math.log(p));return(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);}if(p<=pHigh){q=p-0.5;r=q*q;return(((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);}q=Math.sqrt(-2*Math.log(1-p));return-(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);},
dnorm(x,mean=0,sd=1){const z=(x-mean)/sd;return Math.exp(-0.5*z*z)/(sd*Math.sqrt(2*Math.PI));},
chiSquareCDF(x,df){if(x<=0)return 0;if(df<=0)return 0;const a=df/2;const g=this.logGamma(a);let sum=0,term=1/a;for(let n=1;n<=200;n++){term*=x/(2*(a+n));sum+=term;if(Math.abs(term)<1e-10)break;}return Math.exp(a*Math.log(x/2)-x/2-g)*sum/a;}
};

'''

# Insert before StandaloneRNG if not already present with chiSquareCDF
if "Stats={" in content and "chiSquareCDF" not in content:
    # Find where to insert - before StandaloneRNG
    marker = "// Standalone RNG"
    if marker in content:
        content = content.replace(marker, standalone_stats + marker)
        print("[1] Added Stats with chiSquareCDF")
    else:
        print("[1] WARN: StandaloneRNG marker not found")
elif "chiSquareCDF" in content:
    print("[1] chiSquareCDF already exists")
else:
    # Add Stats before DesignDecomposition
    marker = "const DesignDecomposition="
    if marker in content:
        content = content.replace(marker, standalone_stats + marker)
        print("[1] Added Stats before DesignDecomposition")

# Write
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*70)
print("FIXES APPLIED")
print("="*70)
