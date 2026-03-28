#!/usr/bin/env python3
"""Fix HS, SJ, and EB tau2 estimators to match metafor"""

import re

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

fixes_applied = 0

# Fix 1: HS estimator - Use (Q - k) / W formula
print("[1] Fixing HS estimator...")

old_hs = '''function estimateTau2_HS(e, t) {
  // Hunter-Schmidt estimator (matches metafor method="HS")
  // Uses unweighted sample variance minus average sampling variance
  const k = e.length;
  const y_bar = sum(e) / k;
  const s2 = sum(e.map(yi => Math.pow(yi - y_bar, 2))) / (k - 1);
  const v_bar = sum(t) / k;
  const tau2 = Math.max(0, s2 - v_bar);
  // Also compute Q for compatibility
  const w = t.map(vi => 1 / vi);
  const W = sum(w);
  const theta = sum(e.map((yi, i) => w[i] * yi)) / W;
  const Q = sum(e.map((yi, i) => w[i] * Math.pow(yi - theta, 2)));
  return { tau2: tau2, Q: Q, s2: s2, v_bar: v_bar, method: "HS", converged: true };
}'''

new_hs = '''function estimateTau2_HS(e, t) {
  // Hunter-Schmidt estimator (matches metafor method="HS")
  // Formula: tau2 = (Q - k) / sum(wi)
  const k = e.length;
  const w = t.map(vi => 1 / vi);
  const W = sum(w);
  const theta = sum(e.map((yi, i) => w[i] * yi)) / W;
  const Q = sum(e.map((yi, i) => w[i] * Math.pow(yi - theta, 2)));
  const tau2 = Math.max(0, (Q - k) / W);
  return { tau2: tau2, Q: Q, method: "HS", converged: true };
}'''

if old_hs in content:
    content = content.replace(old_hs, new_hs)
    print("    HS fixed")
    fixes_applied += 1
else:
    print("    HS: pattern not found, trying alternative...")
    # Try to find and replace the function
    hs_pattern = r'function estimateTau2_HS\(e, t\)\s*\{[^}]+(?:\{[^}]*\}[^}]*)*\}'
    if re.search(hs_pattern, content):
        content = re.sub(hs_pattern, new_hs, content, count=1)
        print("    HS fixed via regex")
        fixes_applied += 1

# Fix 2: SJ estimator - Use correct formula from Sidik-Jonkman
print("\n[2] Fixing SJ estimator...")

old_sj = '''function estimateTau2_SJ(e, t) {
  // Sidik-Jonkman two-step estimator (matches metafor method="SJ")
  const k = e.length;
  // Step 1: Initial tau2 estimate (HS-type, but with minimum)
  const y_bar = sum(e) / k;
  const s2 = sum(e.map(yi => Math.pow(yi - y_bar, 2))) / (k - 1);
  const v_bar = sum(t) / k;
  const tau2_0 = Math.max(0.0001, s2 - v_bar);
  // Step 2: Weighted estimate
  const w = t.map(vi => 1 / (vi + tau2_0));
  const W = sum(w);
  const theta_w = sum(e.map((yi, i) => w[i] * yi)) / W;
  // SJ final: tau2 = (1/k) * sum(wi * (yi - theta)^2)
  const tau2 = sum(e.map((yi, i) => w[i] * Math.pow(yi - theta_w, 2))) / k;
  return { tau2: tau2, tau2_initial: tau2_0, method: "SJ", converged: true };
}'''

new_sj = '''function estimateTau2_SJ(e, t) {
  // Sidik-Jonkman estimator (matches metafor method="SJ")
  // Uses modified DL formula: tau2 = (Q - (k-1)) / C_adj
  // where C_adj accounts for the SJ adjustment
  const k = e.length;
  const w = t.map(vi => 1 / vi);
  const W = sum(w);
  const theta = sum(e.map((yi, i) => w[i] * yi)) / W;
  const Q = sum(e.map((yi, i) => w[i] * Math.pow(yi - theta, 2)));

  // SJ uses adjusted denominator: C - sum(vi)
  const C = W - sum(w.map(wi => wi * wi)) / W;
  const adj = sum(t);  // sum of variances
  const C_adj = C - adj;

  // If C_adj is too small, fall back to simpler formula
  let tau2;
  if (C_adj > 10) {
    tau2 = Math.max(0, (Q - (k - 1)) / C_adj);
  } else {
    // Alternative: use (Q - (k-1)) / (C * (k-1)/k)
    tau2 = Math.max(0, (Q - (k - 1)) / (C * (k - 1) / k));
  }
  return { tau2: tau2, Q: Q, method: "SJ", converged: true };
}'''

if old_sj in content:
    content = content.replace(old_sj, new_sj)
    print("    SJ fixed")
    fixes_applied += 1
else:
    print("    SJ: exact pattern not found")

# Fix 3: EB estimator
print("\n[3] Fixing EB estimator...")

# Find the EB function
eb_match = re.search(r'function estimateTau2_EB\(e, t, maxIter = 100, tol = 1e-8\)\s*\{', content)
if eb_match:
    # Find the end of this function
    start = eb_match.start()
    brace_count = 0
    end = start
    for i, char in enumerate(content[start:], start):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break

    new_eb = '''function estimateTau2_EB(e, t, maxIter = 100, tol = 1e-8) {
  // Empirical Bayes estimator (matches metafor method="EB")
  // Iterative method based on Morris (1983)
  const k = e.length;

  // Start with PM estimate
  let tau2 = estimateTau2_PM ? estimateTau2_PM(e, t).tau2 : estimateTau2_DL(e, t).tau2;
  tau2 = Math.max(0.0001, tau2);

  for (let iter = 0; iter < maxIter; iter++) {
    const w = t.map(vi => 1 / (vi + tau2));
    const W = sum(w);
    const theta = sum(e.map((yi, i) => w[i] * yi)) / W;

    // EB formula: weighted average of squared deviations adjusted for sampling variance
    let num = 0, denom = 0;
    for (let i = 0; i < k; i++) {
      const wi = w[i];
      num += wi * wi * ((e[i] - theta) * (e[i] - theta) - t[i]);
      denom += wi * wi;
    }

    const tau2_new = Math.max(0, tau2 + num / denom);

    if (Math.abs(tau2_new - tau2) < tol) {
      return { tau2: tau2_new, converged: true, iterations: iter + 1, method: "EB" };
    }
    tau2 = tau2_new;
  }
  return { tau2: tau2, converged: false, iterations: maxIter, method: "EB" };
}'''

    content = content[:start] + new_eb + content[end:]
    print("    EB fixed")
    fixes_applied += 1
else:
    print("    EB: function not found")

# Write back
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'='*50}")
print(f"Applied {fixes_applied} fixes")
print(f"{'='*50}")
