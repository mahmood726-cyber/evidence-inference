#!/usr/bin/env python3
"""Add standalone RNG for new modules"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("ADDING STANDALONE RNG FOR NEW MODULES")
print("="*70)

# Add standalone RNG before DesignDecomposition
standalone_rng = '''
// Standalone RNG for new advanced modules
const StandaloneRNG={
normal(){let u,v;do{u=Math.random();v=Math.random();}while(u===0);return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);},
gamma(shape,scale=1){if(shape<1)return this.gamma(shape+1,scale)*Math.pow(Math.random(),1/shape);const d=shape-1/3,c=1/Math.sqrt(9*d);while(true){let x,v;do{x=this.normal();v=1+c*x;}while(v<=0);v=v*v*v;const u=Math.random();if(u<1-0.0331*(x*x)*(x*x))return d*v*scale;if(Math.log(u)<0.5*x*x+d*(1-v+Math.log(v)))return d*v*scale;}}
};

'''

# Insert before DesignDecomposition if not already present
if "StandaloneRNG" not in content:
    marker = "const DesignDecomposition="
    if marker in content:
        content = content.replace(marker, standalone_rng + marker)
        print("[1] Added StandaloneRNG module")
    else:
        print("[1] WARN: DesignDecomposition not found")
else:
    print("[1] StandaloneRNG already exists")

# Now replace RNG.normal() and RNG.gamma() with StandaloneRNG versions in new modules
# But only in the HierarchicalNMA section

# Find HierarchicalNMA and replace RNG calls
print("\n[2] Fixing RNG calls in HierarchicalNMA...")

# Replace RNG.normal with StandaloneRNG.normal
old_rng_normal = "RNG.normal()"
new_rng_normal = "StandaloneRNG.normal()"

# Only replace in the HierarchicalNMA section
hier_start = content.find("const HierarchicalNMA=")
if hier_start > 0:
    hier_end = content.find("}};", hier_start) + 3
    hier_section = content[hier_start:hier_end]
    hier_section_fixed = hier_section.replace("RNG.normal()", "StandaloneRNG.normal()")
    hier_section_fixed = hier_section_fixed.replace("RNG.gamma(", "StandaloneRNG.gamma(")
    content = content[:hier_start] + hier_section_fixed + content[hier_end:]
    print("  [OK] Fixed RNG calls in HierarchicalNMA")
else:
    print("  [SKIP] HierarchicalNMA not found")

# Add logGamma to main Stats if needed
print("\n[3] Adding logGamma to Stats if needed...")
if "logGamma" not in content:
    # Find Stats definition and add logGamma
    stats_marker = "const Stats={"
    if stats_marker in content:
        logGamma_func = """const Stats={
logGamma(x){if(x<=0)return Infinity;if(x<0.5)return Math.log(Math.PI/Math.sin(Math.PI*x))-this.logGamma(1-x);x-=1;const g=7,c=[0.99999999999980993,676.5203681218851,-1259.1392167224028,771.32342877765313,-176.61502916214059,12.507343278686905,-0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7];let sum=c[0];for(let i=1;i<g+2;i++)sum+=c[i]/(x+i);const t=x+g+0.5;return 0.5*Math.log(2*Math.PI)+(x+0.5)*Math.log(t)-t+Math.log(sum);},"""
        content = content.replace("const Stats={", logGamma_func)
        print("  [OK] Added logGamma to Stats")
    else:
        print("  [SKIP] Stats not found")
else:
    print("  [SKIP] logGamma already exists")

# Write
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*70)
print("FIXES APPLIED")
print("="*70)
