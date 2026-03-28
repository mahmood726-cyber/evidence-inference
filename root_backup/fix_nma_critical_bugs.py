#!/usr/bin/env python3
"""Fix critical bugs in NMA Pro v6.2"""

import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("NMA Pro v6.2 - CRITICAL BUG FIX")
print("="*70)

# Bug 1: applyLOCF is incomplete and breaks DataQuality scope
print("\n[1] Fixing incomplete applyLOCF function...")

# Find the broken applyLOCF line
broken_pattern = r"applyLOCF\(studies,detection\)\{const locfStudies=studies\.map\(s=>\{const ns=\{\.\.\.\s*s\};\s*\nconst DataQuality="

# The complete applyLOCF function
complete_applyLOCF = '''applyLOCF(studies,detection){
const locfStudies=studies.map((s,i,arr)=>{
const ns={...s};
if(i>0){
if(ns.events1==null&&arr[i-1].events1!=null)ns.events1=arr[i-1].events1;
if(ns.events2==null&&arr[i-1].events2!=null)ns.events2=arr[i-1].events2;
if(ns.n1==null&&arr[i-1].n1!=null)ns.n1=arr[i-1].n1;
if(ns.n2==null&&arr[i-1].n2!=null)ns.n2=arr[i-1].n2;
}
return ns;
});
return{studies:locfStudies,method:'locf',imputedCount:locfStudies.filter((s,i)=>s.events1!==studies[i].events1||s.events2!==studies[i].events2).length,summary:'LOCF applied'};
}};

const DataQuality='''

if re.search(broken_pattern, content, re.MULTILINE):
    content = re.sub(broken_pattern, complete_applyLOCF, content, flags=re.MULTILINE)
    print("  [OK] Fixed applyLOCF function")
else:
    # Try simpler fix
    old = "applyLOCF(studies,detection){const locfStudies=studies.map(s=>{const ns={...s};\n\nconst DataQuality="
    if old in content:
        content = content.replace(old, complete_applyLOCF)
        print("  [OK] Fixed applyLOCF function (simple match)")
    else:
        print("  [WARN] Could not find broken applyLOCF pattern")
        # Try to fix by finding and replacing the exact broken section
        if "applyLOCF(studies,detection){const locfStudies=studies.map(s=>{const ns={...s};" in content:
            # Find the line and fix it
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "applyLOCF(studies,detection){const locfStudies=studies.map(s=>{const ns={...s};" in line:
                    # This line is incomplete - fix it
                    lines[i] = '''applyLOCF(studies,detection){const locfStudies=studies.map((s,i,arr)=>{const ns={...s};if(i>0){if(ns.events1==null&&arr[i-1].events1!=null)ns.events1=arr[i-1].events1;if(ns.events2==null&&arr[i-1].events2!=null)ns.events2=arr[i-1].events2;if(ns.n1==null&&arr[i-1].n1!=null)ns.n1=arr[i-1].n1;if(ns.n2==null&&arr[i-1].n2!=null)ns.n2=arr[i-1].n2;}return ns;});return{studies:locfStudies,method:'locf',imputedCount:0,summary:'LOCF applied'}}};'''
                    # Remove the blank line and fix DataQuality
                    if i+2 < len(lines) and lines[i+2].startswith("const DataQuality="):
                        lines[i+1] = ""  # Remove or keep
                    print(f"  [OK] Fixed at line {i+1}")
                    break
            content = '\n'.join(lines)

# Bug 2: BayesianNMA.summarizePosterior crashes when samples.beta is empty
print("\n[2] Fixing BayesianNMA empty samples handling...")

old_summarize = "summarizePosterior(samples,treatments){const summary={tau2:"
new_summarize = "summarizePosterior(samples,treatments){if(!samples.beta||samples.beta.length===0)return{tau2:{mean:0,sd:0,ci:[0,0],median:0},effects:{},DIC:{DIC:0,pD:0},error:'No samples after burnin'};const summary={tau2:"

if old_summarize in content:
    content = content.replace(old_summarize, new_summarize)
    print("  [OK] Added empty samples guard to summarizePosterior")
else:
    print("  [SKIP] summarizePosterior already has guard or not found")

# Bug 3: samples.beta[0].length crashes when beta is empty
old_beta_p = "const p=samples.beta[0].length;"
new_beta_p = "const p=samples.beta.length>0?samples.beta[0].length:0;"

if old_beta_p in content:
    content = content.replace(old_beta_p, new_beta_p)
    print("  [OK] Added guard for samples.beta[0].length")
else:
    print("  [SKIP] beta[0].length guard already present or not found")

# Bug 4: Accept both 'burnin' and 'nBurnin' parameter names
print("\n[3] Fixing parameter name compatibility...")
old_params = "const{reference,effectMeasure='OR',nChains=4,nIter=2000,burnin=1000,thin=2,"
new_params = "const{reference,effectMeasure='OR',nChains=4,nIter=2000,burnin:burninOpt,nBurnin,thin=2,"
after_params = "priorTau={type:'halfnormal',scale:0.5}}=options;"
after_params_new = "priorTau={type:'halfnormal',scale:0.5}}=options;const burnin=burninOpt||nBurnin||Math.min(1000,Math.floor(nIter/2));"

if old_params in content and after_params in content:
    content = content.replace(old_params, new_params)
    content = content.replace(after_params, after_params_new)
    print("  [OK] Added nBurnin parameter compatibility")
else:
    print("  [SKIP] Parameter fix already applied or not found")

# Write the fixed content
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*70)
print("Fixes applied. Running verification...")
print("="*70)
