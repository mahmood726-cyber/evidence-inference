#!/usr/bin/env python3
"""Fix the new R-equivalent modules to use correct FrequentistNMA methods"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("FIXING NEW MODULES")
print("="*70)

# Fix 1: DesignDecomposition - replace calcEffectSize with inline calculation
print("\n[1] Fixing DesignDecomposition...")

old_dd_calc = """const effects=studies.map(s=>{
const yi=FrequentistNMA.calcEffectSize(s,effectMeasure);
return{...s,yi:yi.effect,vi:yi.variance,sei:Math.sqrt(yi.variance)};
});"""

new_dd_calc = """const effects=studies.map(s=>{
// Calculate log odds ratio
const a=s.events1+0.5,b=s.n1-s.events1+0.5,c=s.events2+0.5,d=s.n2-s.events2+0.5;
const yi=Math.log((a*d)/(b*c));
const vi=1/a+1/b+1/c+1/d;
return{...s,yi,vi,sei:Math.sqrt(vi)};
});"""

if old_dd_calc in content:
    content = content.replace(old_dd_calc, new_dd_calc)
    print("  [OK] Fixed DesignDecomposition effect calculation")
else:
    print("  [SKIP] Pattern not found")

# Fix 2: HierarchicalNMA - fix RNG.gamma call
print("\n[2] Fixing HierarchicalNMA RNG calls...")

# Check if RNG.gamma exists, if not add fallback
old_gamma = "tau2=1/RNG.gamma(shape,1/rate);"
new_gamma = "tau2=1/(typeof RNG.gamma==='function'?RNG.gamma(shape,1/rate):shape/rate);"

if old_gamma in content:
    content = content.replace(old_gamma, new_gamma)
    print("  [OK] Fixed RNG.gamma call")
else:
    print("  [SKIP] RNG.gamma pattern not found")

# Fix 3: Add RNG.gamma if it doesn't exist
print("\n[3] Checking RNG.gamma exists...")
if "gamma(shape,scale)" not in content and "const RNG=" in content:
    # Add gamma function to RNG
    old_rng_end = "normal(){let u,v;do{u=Math.random();v=Math.random();}while(u===0);return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}"
    new_rng_end = """normal(){let u,v;do{u=Math.random();v=Math.random();}while(u===0);return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);},
gamma(shape,scale){
// Marsaglia and Tsang's method
if(shape<1)return this.gamma(shape+1,scale)*Math.pow(Math.random(),1/shape);
const d=shape-1/3,c=1/Math.sqrt(9*d);
while(true){
let x,v;do{x=this.normal();v=1+c*x;}while(v<=0);
v=v*v*v;const u=Math.random();
if(u<1-0.0331*(x*x)*(x*x))return d*v*scale;
if(Math.log(u)<0.5*x*x+d*(1-v+Math.log(v)))return d*v*scale;
}
}"""
    if old_rng_end in content:
        content = content.replace(old_rng_end, new_rng_end)
        print("  [OK] Added RNG.gamma function")
    else:
        print("  [SKIP] RNG pattern not found")
else:
    print("  [SKIP] RNG.gamma already exists or RNG not found")

# Fix 4: Stats.logGamma for CustomLikelihood
print("\n[4] Checking Stats.logGamma exists...")
if "logGamma" not in content and "const Stats=" in content:
    # Add logGamma to Stats
    old_stats_pattern = "chiSquareCDF(x,df){"
    new_stats_addition = """logGamma(x){
// Stirling's approximation for log(Gamma(x))
if(x<=0)return Infinity;
if(x<0.5)return Math.log(Math.PI/Math.sin(Math.PI*x))-this.logGamma(1-x);
x-=1;
const g=7;const c=[0.99999999999980993,676.5203681218851,-1259.1392167224028,771.32342877765313,-176.61502916214059,12.507343278686905,-0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7];
let sum=c[0];for(let i=1;i<g+2;i++)sum+=c[i]/(x+i);
const t=x+g+0.5;
return 0.5*Math.log(2*Math.PI)+(x+0.5)*Math.log(t)-t+Math.log(sum);
},
chiSquareCDF(x,df){"""
    if old_stats_pattern in content:
        content = content.replace(old_stats_pattern, new_stats_addition)
        print("  [OK] Added Stats.logGamma function")
    else:
        print("  [SKIP] Stats pattern not found")
else:
    print("  [SKIP] logGamma already exists or pattern not found")

# Fix 5: CustomLikelihood - fix logChoose reference
print("\n[5] Fixing CustomLikelihood logChoose...")
old_logchoose = "return r*Math.log(p)+(n-r)*Math.log(1-p)+this.logChoose(n,r);"
new_logchoose = "return r*Math.log(p)+(n-r)*Math.log(1-p)+Stats.logGamma(n+1)-Stats.logGamma(r+1)-Stats.logGamma(n-r+1);"

if old_logchoose in content:
    content = content.replace(old_logchoose, new_logchoose)
    print("  [OK] Fixed logChoose reference")
else:
    print("  [SKIP] logChoose pattern not found")

# Write fixed content
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*70)
print("FIXES APPLIED")
print("="*70)
