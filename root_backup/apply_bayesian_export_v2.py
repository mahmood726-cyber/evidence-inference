# Add Bayesian gemtc R export functionality - v2 with correct patterns

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add generateBayesianRScript function after BayesianNMA object
# Find the end of BayesianNMA object - it ends with buildLeagueTable

bayesian_r_function = '''
function generateBayesianRScript(){
if(!AppState.bayesianResults)return null;
const ref=AppState.reference||'A';
const em=AppState.effectMeasure||'OR';
const bayes=AppState.bayesianResults;
const rows=[];AppState.studies.forEach(s=>{rows.push({study:s.name,t1:s.treatment1,t2:s.treatment2,e1:s.events1,n1:s.n1,e2:s.events2,n2:s.n2})});
const esc=v=>`"${String(v||'').replace(/"/g,'\\\\"')}"`;
const num=v=>{const n=parseFloat(v);return Number.isFinite(n)?n:'NA'};
let code=`# NMA Pro v6.2 - Bayesian R Validation with gemtc\\n`;
code+=`# Generated: ${new Date().toISOString().split('T')[0]}\\n`;
code+=`# NMA Pro Bayesian Results: tau2=${bayes.summary?.tau2?.mean?.toFixed(6)||'NA'}\\n\\n`;
code+=`# Install packages if needed\\nif(!require(gemtc))install.packages('gemtc',repos='https://cloud.r-project.org')\\n`;
code+=`if(!require(coda))install.packages('coda',repos='https://cloud.r-project.org')\\n\\n`;
code+=`library(gemtc)\\nlibrary(coda)\\n\\n`;
code+=`# Convert to arm-level data\\narm_data <- data.frame(\\n`;
code+=`  study = c(${rows.map(r=>esc(r.study)).join(', ')}, ${rows.map(r=>esc(r.study)).join(', ')}),\\n`;
code+=`  treatment = c(${rows.map(r=>esc(r.t1)).join(', ')}, ${rows.map(r=>esc(r.t2)).join(', ')}),\\n`;
code+=`  responders = c(${rows.map(r=>num(r.e1)).join(', ')}, ${rows.map(r=>num(r.e2)).join(', ')}),\\n`;
code+=`  sampleSize = c(${rows.map(r=>num(r.n1)).join(', ')}, ${rows.map(r=>num(r.n2)).join(', ')})\\n`;
code+=`)\\n\\n`;
code+=`# Build network and run model\\nnetwork <- mtc.network(arm_data)\\n`;
code+=`model <- mtc.model(network, likelihood="binom", link="logit", linearModel="random")\\n`;
code+=`results <- mtc.run(model, n.adapt=500, n.iter=5000)\\n\\n`;
code+=`# Extract results\\ncat("\\\\n=== gemtc Results ===\\\\n")\\n`;
code+=`cat("tau (sd.d):", mean(as.matrix(results$samples[,"sd.d"])), "\\\\n")\\n`;
code+=`cat("tau2:", mean(as.matrix(results$samples[,"sd.d"])^2), "\\\\n")\\n`;
code+=`cat("\\\\n=== NMA Pro Results ===\\\\n")\\n`;
code+=`cat("tau2:", ${bayes.summary?.tau2?.mean?.toFixed(6)||'NA'}, "\\\\n")\\n`;
code+=`cat("\\\\n=== Comparison ===\\\\n")\\n`;
code+=`summary(results)\\n`;
return code;
}

'''

# Insert after the closing of BayesianNMA object - look for const BayesianNMA= ... buildLeagueTable
if 'generateBayesianRScript' not in content:
    # Find position after the first standalone function after BayesianNMA
    # Looking for "function render" after BayesianNMA
    bayesian_end = content.find('function renderMissingDataSummary')
    if bayesian_end > 0:
        content = content[:bayesian_end] + bayesian_r_function + content[bayesian_end:]
        print("[OK] Added generateBayesianRScript function")
    else:
        print("[WARN] Could not find insertion point for function")

# 2. Add export button to Bayesian panel header
old_btn = '<button class="btn btn--sm btn--secondary" id="runBayesianBtn">Run Bayesian</button>'
new_btn = '''<button class="btn btn--sm btn--secondary" id="runBayesianBtn">Run Bayesian</button><button class="btn btn--sm btn--ghost" onclick="const s=generateBayesianRScript();if(!s){alert('Run Bayesian analysis first');return}const b=new Blob([s],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='nma_bayesian_gemtc.R';a.click()" title="Export gemtc R validation script">gemtc R</button>'''

if old_btn in content and 'gemtc R' not in content:
    content = content.replace(old_btn, new_btn)
    print("[OK] Added gemtc R export button")
else:
    if 'gemtc R' in content:
        print("[INFO] gemtc R button already exists")
    else:
        print("[WARN] Could not find button pattern")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''
with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("\n[SUCCESS] JavaScript syntax valid")
else:
    print("\n[ERROR]:")
    print(result.stderr[:500])
