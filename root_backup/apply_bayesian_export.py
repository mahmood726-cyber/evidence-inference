# Add Bayesian gemtc R export functionality

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add generateBayesianRScript function
# Find a good place - after generateRValidationScript if it exists, or in the FrequentistNMA object

bayesian_r_script = '''
function generateBayesianRScript(){
  if(!AppState.bayesianResults)return null;
  const ref=AppState.reference||'A';
  const em=AppState.effectMeasure||'OR';
  const bayes=AppState.bayesianResults;
  const rows=[];AppState.studies.forEach(s=>{rows.push({study:s.name,t1:s.treatment1,t2:s.treatment2,e1:s.events1,n1:s.n1,e2:s.events2,n2:s.n2})});
  const esc=v=>`"${String(v||'').replace(/"/g,'\\\\"')}"`;
  const num=v=>{const n=parseFloat(v);return Number.isFinite(n)?n:'NA'};
  let code=`# NMA Pro v6.2 - Bayesian R Validation\\n`;
  code+=`# Generated: ${new Date().toISOString().split('T')[0]}\\n`;
  code+=`# NMA Pro Bayesian Results: tau2=${bayes.tau2?.mean?.toFixed(6)||'NA'}\\n\\n`;
  code+=`library(gemtc)\\nlibrary(coda)\\n\\n`;
  code+=`arm_data <- data.frame(\\n`;
  code+=`  study = c(${rows.map(r=>esc(r.study)).join(', ')}, ${rows.map(r=>esc(r.study)).join(', ')}),\\n`;
  code+=`  treatment = c(${rows.map(r=>esc(r.t1)).join(', ')}, ${rows.map(r=>esc(r.t2)).join(', ')}),\\n`;
  code+=`  responders = c(${rows.map(r=>num(r.e1)).join(', ')}, ${rows.map(r=>num(r.e2)).join(', ')}),\\n`;
  code+=`  sampleSize = c(${rows.map(r=>num(r.n1)).join(', ')}, ${rows.map(r=>num(r.n2)).join(', ')})\\n`;
  code+=`)\\n\\n`;
  code+=`network <- mtc.network(arm_data)\\n`;
  code+=`model <- mtc.model(network, likelihood="binom", link="logit", linearModel="random")\\n`;
  code+=`results <- mtc.run(model, n.adapt=500, n.iter=5000)\\n\\n`;
  code+=`# Compare with NMA Pro results\\n`;
  code+=`cat("tau2 (gemtc):", mean(as.matrix(results$samples[,"sd.d"])^2), "\\\\n")\\n`;
  code+=`cat("tau2 (NMA Pro): ${bayes.tau2?.mean?.toFixed(6)||'NA'}\\\\n")\\n`;
  return code;
}
'''

# Find where to insert - before the first onclick handler or at end of script
if 'generateBayesianRScript' not in content:
    # Find a good insertion point - look for onClick patterns
    idx = content.find("onClick('analyzeBtn'")
    if idx > 0:
        content = content[:idx] + bayesian_r_script + '\n\n' + content[idx:]
        print("[OK] Added generateBayesianRScript function")

# Add export button to Bayesian panel
old_bayes_title = '<span class="card__title">Bayesian MCMC Analysis</span>'
new_bayes_title = '<span class="card__title">Bayesian MCMC Analysis</span><button class="btn btn--sm btn--ghost" onclick="const s=generateBayesianRScript();if(!s){alert(\'Run Bayesian analysis first\');return}const b=new Blob([s],{type:\'text/plain\'});const a=document.createElement(\'a\');a.href=URL.createObjectURL(b);a.download=\'nma_bayesian_gemtc.R\';a.click()" title="Export gemtc R validation script">gemtc R</button>'

if old_bayes_title in content and 'gemtc R' not in content:
    content = content.replace(old_bayes_title, new_bayes_title)
    print("[OK] Added gemtc R export button")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
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
    print(result.stderr[:400])
