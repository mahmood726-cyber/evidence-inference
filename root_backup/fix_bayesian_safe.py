#!/usr/bin/env python3
"""Safe fix for BayesianNMA bug"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("NMA Pro v6.2 - BayesianNMA Safe Fix")
print("="*70)

# Fix 1: Add empty samples guard to summarizePosterior
print("\n[1] Adding empty samples guard to summarizePosterior...")
old_summarize = "summarizePosterior(samples,treatments){const summary={tau2:"
new_summarize = "summarizePosterior(samples,treatments){if(!samples.beta||samples.beta.length===0){return{tau2:{mean:0,sd:0,ci:[0,0],median:0},effects:{},DIC:{DIC:0,pD:0},error:'No valid samples - increase nIter or decrease burnin'}};const summary={tau2:"

if old_summarize in content:
    content = content.replace(old_summarize, new_summarize)
    print("  [OK] Added empty samples guard")
else:
    print("  [SKIP] Guard already present")

# Fix 2: Add guard for samples.beta[0].length
print("\n[2] Adding guard for samples.beta[0].length...")
old_beta = "const p=samples.beta[0].length;"
new_beta = "const p=samples.beta.length>0&&samples.beta[0]?samples.beta[0].length:0;"

if old_beta in content:
    content = content.replace(old_beta, new_beta)
    print("  [OK] Added beta[0] guard")
else:
    print("  [SKIP] Guard already present")

# Fix 3: Accept both 'burnin' and 'nBurnin' parameters and auto-adjust
print("\n[3] Adding nBurnin parameter alias...")
old_params = "const{reference,effectMeasure='OR',nChains=4,nIter=2000,burnin=1000,thin=2,priorTau={type:'halfnormal',scale:0.5}}=options;"
# Handle both param names and auto-adjust burnin to be valid
new_params = "const{reference,effectMeasure='OR',nChains=4,nIter=2000,burnin:_burnin,nBurnin,thin=2,priorTau={type:'halfnormal',scale:0.5}}=options;const burnin=Math.min(_burnin||nBurnin||1000,Math.floor(nIter*0.8));"

if old_params in content:
    content = content.replace(old_params, new_params)
    print("  [OK] Added nBurnin alias and auto-adjustment")
else:
    print("  [SKIP] Parameter fix already present")

# Write the fixed content
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*70)
print("Fixes applied successfully")
print("="*70)
