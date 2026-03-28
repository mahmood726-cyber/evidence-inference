# Carefully apply editorial features to NMA Pro v6.2
# Features:
# 1. Paule-Mandel tau2 CI
# 2. Edge weights in network plots
# 3. Bayesian gemtc R export

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# ============================================================================
# 1. ADD PAULE-MANDEL TAU2 CI FUNCTION
# ============================================================================
# Find profileLikelihoodCI method and add pauleMandel_CI after it

pm_ci_function = '''
pauleMandel_CI(matrices, tau2, alpha=0.05) {
  /* Paule-Mandel CI via Q-profile method (Veroniki 2016) */
  const {V, y, X, n} = matrices;
  const df = n - X[0].length;
  if (df <= 0) return null;
  const calcQ = (t2) => {
    const W = Matrix.zeros(n, n);
    for (let i = 0; i < n; i++) W[i][i] = 1 / (V[i][i] + t2);
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

# Find a good insertion point - after profileLikelihoodCI method
if 'pauleMandel_CI' not in content:
    # Find end of profileLikelihoodCI
    idx = content.find('profileLikelihoodCI')
    if idx > 0:
        # Find the method's closing }, - track braces
        depth = 0
        found_start = False
        end_idx = idx
        for i in range(idx, min(idx + 5000, len(content))):
            if content[i] == '{':
                depth += 1
                found_start = True
            elif content[i] == '}':
                depth -= 1
                if found_start and depth == 0:
                    # Found the closing }
                    # Look for the comma after
                    j = i + 1
                    while j < len(content) and content[j] in ' \t':
                        j += 1
                    if content[j] == ',':
                        end_idx = j + 1
                    else:
                        end_idx = i + 1
                    break

        # Insert after the comma
        content = content[:end_idx] + pm_ci_function + content[end_idx:]
        changes.append("Added pauleMandel_CI function after profileLikelihoodCI")

# ============================================================================
# 2. ADD PM CI TO RESULTS
# ============================================================================
# Find where tau2CI is returned and add pmCI

if 'pmCI' not in content and 'pauleMandel_CI' in content:
    # Find the return statement that includes tau2CI
    old_return = 'tau2CI,treatments'
    new_return = 'tau2CI,pmCI:this.pauleMandel_CI(matrices,tau2Result.tau2),treatments'
    if old_return in content:
        content = content.replace(old_return, new_return)
        changes.append("Added PM CI to analysis results")

# ============================================================================
# 3. DISPLAY PM CI IN UI
# ============================================================================
# Find heterogeneity CI display and add PM CI

if 'pmCI' in content:
    old_ci_display = "document.getElementById('hetTau2CI').textContent=ciText"
    new_ci_display = '''const pmCI=AppState.results?.pmCI;if(pmCI)ciText+=' | PM: ['+pmCI.lower.toFixed(4)+', '+pmCI.upper.toFixed(4)+']';document.getElementById('hetTau2CI').textContent=ciText'''
    if old_ci_display in content and 'pmCI' not in content[content.find(old_ci_display):content.find(old_ci_display)+200]:
        content = content.replace(old_ci_display, new_ci_display)
        changes.append("Added PM CI to heterogeneity display")

# ============================================================================
# 4. EDGE WEIGHTS IN NETWORK PLOTS
# ============================================================================
# Modify network graph rendering to show edge weights

if 'edgeAnnotations' not in content:
    # Find the edge trace definition
    old_edge = "const edgeTrace={type:'scatter',mode:'lines',x:edgeX,y:edgeY,line:{color:colors.edge,width:2},hoverinfo:'skip'}"

    new_edge = '''/* Edge weights */
const edgeAnnotations=[];
edgeMap.forEach((cnt,k)=>{
  const[t1,t2]=k.split('|'),i1=treatments.indexOf(t1),i2=treatments.indexOf(t2);
  if(i1>=0&&i2>=0){
    const midX=(nodeX[i1]+nodeX[i2])/2,midY=(nodeY[i1]+nodeY[i2])/2;
    edgeAnnotations.push({x:midX,y:midY,text:String(cnt),showarrow:false,font:{size:10,color:colors.textSecondary},bgcolor:colors.background,borderpad:2});
  }
});
const edgeTrace={type:'scatter',mode:'lines',x:edgeX,y:edgeY,line:{color:colors.edge,width:2},hoverinfo:'skip'}'''

    if old_edge in content:
        content = content.replace(old_edge, new_edge)
        changes.append("Added edge weight calculations")

    # Add annotations to layout
    old_margin = "margin:{l:20,r:20,t:20,b:20},showlegend:false"
    new_margin = "margin:{l:20,r:20,t:20,b:20},showlegend:false,annotations:edgeAnnotations||[]"
    if old_margin in content:
        content = content.replace(old_margin, new_margin)
        changes.append("Added edge annotations to network plot")

# Save
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''
with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)

print("=" * 60)
print("EDITORIAL FEATURES IMPLEMENTATION")
print("=" * 60)
for c in changes:
    print(f"  [OK] {c}")

if result.returncode == 0:
    print("\n[SUCCESS] JavaScript syntax is valid")
else:
    print("\n[ERROR] Syntax error introduced:")
    print(result.stderr[:400])
print("=" * 60)
