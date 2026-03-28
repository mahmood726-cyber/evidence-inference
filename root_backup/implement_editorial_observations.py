# Implement Editorial Observations for NMA Pro v6.2
# 1. Paule-Mandel tau2 CI
# 2. Edge weights in network plots
# 3. Bayesian R export integration

import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# ============================================================================
# 1. ADD PAULE-MANDEL TAU2 CONFIDENCE INTERVAL
# ============================================================================
# Add PM CI calculation method after profileLikelihoodCI

pm_ci_function = '''
pauleMandel_CI(matrices, tau2, alpha=0.05) {
  /* Paule-Mandel CI via Q-profile method (Veroniki 2016) */
  const {V, y, X, n} = matrices;
  const df = n - X[0].length;
  if (df <= 0) return null;

  const calcQ = (t2) => {
    const W = Matrix.zeros(n, n);
    for (let i = 0; i < n; i++) W[i][i] = 1 / (V[i][i] + t2);
    const XtW = this.transpose(X).map((row, i) => row.map((_, j) => {
      let s = 0; for (let k = 0; k < n; k++) s += X[k][i] * W[k][k]; return s;
    }));
    let XtWX = Matrix.zeros(X[0].length, X[0].length);
    for (let i = 0; i < X[0].length; i++) {
      for (let j = 0; j < X[0].length; j++) {
        let s = 0;
        for (let k = 0; k < n; k++) s += X[k][i] * W[k][k] * X[k][j];
        XtWX[i][j] = s;
      }
    }
    const XtWy = X[0].map((_, i) => {
      let s = 0; for (let k = 0; k < n; k++) s += X[k][i] * W[k][k] * y[k]; return s;
    });
    try {
      const beta = Matrix.solve(XtWX, XtWy);
      let Q = 0;
      for (let i = 0; i < n; i++) {
        let fitted = 0;
        for (let j = 0; j < beta.length; j++) fitted += X[i][j] * beta[j];
        Q += W[i][i] * (y[i] - fitted) ** 2;
      }
      return Q;
    } catch { return Infinity; }
  };

  const chi2Lower = jStat.chisquare.inv(1 - alpha/2, df);
  const chi2Upper = jStat.chisquare.inv(alpha/2, df);

  /* Find tau2 where Q = chi2 quantiles using bisection */
  const findTau2 = (targetQ, lower, upper) => {
    for (let i = 0; i < 100; i++) {
      const mid = (lower + upper) / 2;
      const Q = calcQ(mid);
      if (Math.abs(Q - targetQ) < 0.0001) return mid;
      if (Q > targetQ) lower = mid; else upper = mid;
    }
    return (lower + upper) / 2;
  };

  const tau2Lower = Math.max(0, findTau2(chi2Lower, 0, tau2 * 10 + 1));
  const tau2Upper = findTau2(chi2Upper, tau2, tau2 * 20 + 5);

  return { lower: tau2Lower, upper: tau2Upper, method: 'Q-profile (PM)' };
},'''

# Find profileLikelihoodCI and add PM CI after it
if 'profileLikelihoodCI' in content and 'pauleMandel_CI' not in content:
    # Find end of profileLikelihoodCI function
    idx = content.find('profileLikelihoodCI')
    depth = 0
    end_idx = idx
    found_start = False
    for i in range(idx, min(idx + 3000, len(content))):
        if content[i] == '{':
            depth += 1
            found_start = True
        elif content[i] == '}':
            depth -= 1
            if found_start and depth == 0:
                end_idx = i + 1
                break

    # Insert after profileLikelihoodCI
    content = content[:end_idx] + '\n' + pm_ci_function + content[end_idx:]
    changes.append("Added Paule-Mandel tau2 CI (Q-profile method)")

# Add PM CI to heterogeneity panel display
old_het_ci = "document.getElementById('hetTau2CI').textContent=ciText"
new_het_ci = """const pmCI=AppState.results?.pmCI;if(pmCI)ciText+=` | PM: [${pmCI.lower.toFixed(4)}, ${pmCI.upper.toFixed(4)}]`;document.getElementById('hetTau2CI').textContent=ciText"""

if old_het_ci in content and 'pmCI' not in content:
    content = content.replace(old_het_ci, new_het_ci)
    changes.append("Added PM CI to heterogeneity panel display")

# Add PM CI calculation in analyze function
old_analyze_return = "return{effects,heterogeneity,leagueTable,consistency,tau2:tau2Result.tau2,tau:Math.sqrt(tau2Result.tau2),tau2CI"
new_analyze_return = "const pmCI=this.pauleMandel_CI(matrices,tau2Result.tau2);return{effects,heterogeneity,leagueTable,consistency,tau2:tau2Result.tau2,tau:Math.sqrt(tau2Result.tau2),tau2CI,pmCI"

if old_analyze_return in content and 'pmCI=this.pauleMandel_CI' not in content:
    content = content.replace(old_analyze_return, new_analyze_return)
    changes.append("Added PM CI calculation to analyze function")

# ============================================================================
# 2. ADD EDGE WEIGHTS TO NETWORK PLOTS
# ============================================================================
# Modify renderNetworkGraph to show edge weights (study counts) and line thickness

old_network_edge = "const edgeTrace={type:'scatter',mode:'lines',x:edgeX,y:edgeY,line:{color:colors.edge,width:2},hoverinfo:'skip'}"

new_network_edge = """/* Calculate edge midpoints and annotations for weights */
const edgeAnnotations=[];
const edgePairs=[];
edgeMap.forEach((cnt,k)=>{
  const[t1,t2]=k.split('|'),i1=treatments.indexOf(t1),i2=treatments.indexOf(t2);
  if(i1>=0&&i2>=0){
    const midX=(nodeX[i1]+nodeX[i2])/2;
    const midY=(nodeY[i1]+nodeY[i2])/2;
    edgePairs.push({x1:nodeX[i1],y1:nodeY[i1],x2:nodeX[i2],y2:nodeY[i2],cnt,midX,midY});
    edgeAnnotations.push({x:midX,y:midY,text:String(cnt),showarrow:false,font:{size:10,color:colors.textSecondary},bgcolor:colors.background,borderpad:2});
  }
});
/* Create edge traces with width proportional to study count */
const edgeTraces=edgePairs.map(e=>({type:'scatter',mode:'lines',x:[e.x1,e.x2],y:[e.y1,e.y2],line:{color:colors.edge,width:Math.max(1,Math.min(8,e.cnt*1.5))},hoverinfo:'text',hovertext:`${e.cnt} ${e.cnt===1?'study':'studies'}`,showlegend:false}));
const edgeTrace={type:'scatter',mode:'lines',x:edgeX,y:edgeY,line:{color:colors.edge,width:2},hoverinfo:'skip',showlegend:false}"""

if old_network_edge in content and 'edgeAnnotations' not in content:
    content = content.replace(old_network_edge, new_network_edge)
    changes.append("Added edge weight calculations for network plot")

# Update Plotly layout to include annotations
old_network_layout = "schedulePlot('networkPlot',[edgeTrace,nodeTrace]"
new_network_layout = "schedulePlot('networkPlot',[...edgeTraces,nodeTrace]"

if old_network_layout in content and 'edgeTraces' not in content:
    content = content.replace(old_network_layout, new_network_layout)
    changes.append("Updated network plot to use weighted edge traces")

# Add annotations to layout
old_network_margin = "margin:{l:20,r:20,t:20,b:20},showlegend:false"
new_network_margin = "margin:{l:20,r:20,t:20,b:20},showlegend:false,annotations:edgeAnnotations"

if old_network_margin in content and 'annotations:edgeAnnotations' not in content:
    content = content.replace(old_network_margin, new_network_margin)
    changes.append("Added edge weight annotations to network plot")

# ============================================================================
# 3. INTEGRATE BAYESIAN MODULE WITH R EXPORT
# ============================================================================
# Add generateBayesianRScript function

bayesian_r_export = '''
generateBayesianRScript(){
if(!AppState.bayesianResults){return null}
const ref=AppState.reference||'A';
const em=AppState.effectMeasure||'OR';
const bayes=AppState.bayesianResults;

const rows=[];
AppState.studies.forEach(s=>{
  rows.push({study:s.name,t1:s.treatment1,t2:s.treatment2,
    e1:s.events1,n1:s.n1,e2:s.events2,n2:s.n2,
    logHR:s.logHR,se:s.se});
});

const esc=v=>`"${String(v||'').replace(/"/g,'\\\\"')}"`;
const num=v=>{const n=parseFloat(v);return Number.isFinite(n)?n:'NA'};

let script=`# NMA Pro v6.2 - Bayesian R Validation Script
# Generated: ${new Date().toISOString().split('T')[0]}
# Reference: ${ref}, Effect Measure: ${em}
# NMA Pro Bayesian Results:
#   tau2 posterior mean: ${bayes.tau2?.mean?.toFixed(6)||'NA'}
#   tau2 95% CI: [${bayes.tau2?.ci?.[0]?.toFixed(6)||'NA'}, ${bayes.tau2?.ci?.[1]?.toFixed(6)||'NA'}]
#   DIC: ${bayes.DIC?.toFixed(2)||'NA'}

library(gemtc)
library(rjags)
library(coda)

# ============================================================================
# STUDY DATA
# ============================================================================
data <- data.frame(
  study = c(${rows.map(r=>esc(r.study)).join(', ')}),
  treatment = c(${rows.map(r=>esc(r.t1)).join(', ')}, ${rows.map(r=>esc(r.t2)).join(', ')}),
  responders = c(${rows.map(r=>num(r.e1)).join(', ')}, ${rows.map(r=>num(r.e2)).join(', ')}),
  sampleSize = c(${rows.map(r=>num(r.n1)).join(', ')}, ${rows.map(r=>num(r.n2)).join(', ')})
)

# Reshape to arm-based format for gemtc
arm_data <- data.frame(
  study = rep(c(${rows.map(r=>esc(r.study)).join(', ')}), 2),
  treatment = c(${rows.map(r=>esc(r.t1)).join(', ')}, ${rows.map(r=>esc(r.t2)).join(', ')}),
  responders = c(${rows.map(r=>num(r.e1)).join(', ')}, ${rows.map(r=>num(r.e2)).join(', ')}),
  sampleSize = c(${rows.map(r=>num(r.n1)).join(', ')}, ${rows.map(r=>num(r.n2)).join(', ')})
)

# ============================================================================
# BAYESIAN NMA (gemtc)
# ============================================================================
network <- mtc.network(arm_data)

# Model with half-normal prior on tau (matching NMA Pro default)
model <- mtc.model(network,
  likelihood = "binom",
  link = "logit",
  linearModel = "random",
  hy.prior = mtc.hy.prior("std.dev", "dunif", 0, 2)  # Half-normal approx
)

# Run MCMC
results <- mtc.run(model, n.adapt = 500, n.iter = 5000, thin = 2)

# ============================================================================
# RESULTS COMPARISON
# ============================================================================
cat("======================================================================\\n")
cat("BAYESIAN NMA COMPARISON: NMA Pro vs gemtc\\n")
cat("======================================================================\\n\\n")

# Extract tau2 posterior
tau_samples <- as.matrix(results$samples[, "sd.d"])^2
tau2_mean <- mean(tau_samples)
tau2_ci <- quantile(tau_samples, c(0.025, 0.975))

cat("HETEROGENEITY (tau2):\\n")
cat(sprintf("  NMA Pro:  mean = ${bayes.tau2?.mean?.toFixed(6)||'NA'}, 95%% CI = [${bayes.tau2?.ci?.[0]?.toFixed(6)||'NA'}, ${bayes.tau2?.ci?.[1]?.toFixed(6)||'NA'}]\\n"))
cat(sprintf("  gemtc:    mean = %.6f, 95%% CI = [%.6f, %.6f]\\n", tau2_mean, tau2_ci[1], tau2_ci[2]))

# DIC comparison
dic <- summary(results)$DIC
cat(sprintf("\\nDIC:\\n  NMA Pro: ${bayes.DIC?.toFixed(2)||'NA'}\\n  gemtc:   %.2f\\n", dic))

# Treatment effects
cat("\\nTREATMENT EFFECTS vs ${ref}:\\n")
print(summary(relative.effect(results, "${ref}")))

cat("\\n======================================================================\\n")
`;

return script
},'''

# Find a good place to insert - after generateRValidationScript
if 'generateRValidationScript' in content and 'generateBayesianRScript' not in content:
    idx = content.find('generateRValidationScript')
    depth = 0
    end_idx = idx
    found_start = False
    for i in range(idx, min(idx + 8000, len(content))):
        if content[i] == '{':
            depth += 1
            found_start = True
        elif content[i] == '}':
            depth -= 1
            if found_start and depth == 0:
                end_idx = i + 1
                break

    content = content[:end_idx] + '\n' + bayesian_r_export + content[end_idx:]
    changes.append("Added generateBayesianRScript function for gemtc validation")

# Add export button for Bayesian R script
old_bayes_header = '<span class="card__title">Bayesian NMA</span>'
new_bayes_header = '<span class="card__title">Bayesian NMA</span><button class="btn btn--sm btn--ghost" id="exportBayesRBtn" title="Export R script for gemtc validation">Export gemtc R</button>'

if old_bayes_header in content and 'exportBayesRBtn' not in content:
    content = content.replace(old_bayes_header, new_bayes_header)
    changes.append("Added Export gemtc R button to Bayesian panel")

# Add click handler for Bayesian R export
old_bayes_handler = "onClick('runBayesianBtn',runBayesian)"
new_bayes_handler = """onClick('runBayesianBtn',runBayesian);onClick('exportBayesRBtn',()=>{const script=FrequentistNMA.generateBayesianRScript();if(!script){alert('Run Bayesian analysis first');return}const blob=new Blob([script],{type:'text/plain'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='nma_bayesian_gemtc.R';a.click();URL.revokeObjectURL(url)})"""

if old_bayes_handler in content and 'exportBayesRBtn' not in old_bayes_handler:
    content = content.replace(old_bayes_handler, new_bayes_handler)
    changes.append("Added click handler for Bayesian R export")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 70)
print("EDITORIAL OBSERVATIONS IMPLEMENTATION")
print("=" * 70)
print("\nChanges applied:")
for i, change in enumerate(changes, 1):
    print(f"  {i}. {change}")
print("\n" + "=" * 70)
print(f"Total: {len(changes)} changes")
print("=" * 70)
