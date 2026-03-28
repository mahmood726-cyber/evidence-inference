#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix JavaScript errors in HTML file"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original HTML file: {len(content.split(chr(10)))} lines")
fixes = 0

# Fix 1: runSimplifiedMA - fix property names
old_modelavg = '''  document.getElementById('modelavgResults').innerHTML = `
    <div style="background: var(--bg-secondary); padding: var(--space-3); border-radius: var(--radius-md);">
      <p><strong>Model-Averaged Effect:</strong> ${results.theta.toFixed(3)} (95% CI: ${results.ci_lower.toFixed(3)} to ${results.ci_upper.toFixed(3)})</p>
      <p><strong>P(Effect ≠ 0):</strong> ${(results.pip_effect * 100).toFixed(1)}%</p>
      <p><strong>P(Heterogeneity):</strong> ${(results.pip_heterogeneity * 100).toFixed(1)}%</p>
      <h5 style="margin-top: var(--space-2);">Model Weights:</h5>
      <ul style="font-size: 0.85em; margin: 0; padding-left: var(--space-4);">
        ${results.models.map(m => `<li>${m.name}: θ=${m.theta.toFixed(3)} (weight=${(m.weight*100).toFixed(0)}%)</li>`).join('')}
      </ul>
      <p style="color: ${results.pip_effect > 0.9 ? 'var(--color-success-500)' : 'var(--color-warning-500)'}; font-weight: bold; margin-top: var(--space-2);">
        ${results.interpretation}
      </p>
    </div>
  `;'''

new_modelavg = '''  if (!results || !results.ok) {
    document.getElementById('modelavgResults').innerHTML = '<p class="text-warning">Model averaging failed. Try running analysis first.</p>';
    showToast('ModelAvg failed', 'warning');
    return;
  }
  document.getElementById('modelavgResults').innerHTML = `
    <div style="background: var(--bg-secondary); padding: var(--space-3); border-radius: var(--radius-md);">
      <p><strong>Model-Averaged Effect:</strong> ${results.theta.toFixed(3)} (95% CI: ${results.ciLower.toFixed(3)} to ${results.ciUpper.toFixed(3)})</p>
      <p><strong>P(Effect ≠ 0):</strong> ${(results.pEffect * 100).toFixed(1)}%</p>
      <p><strong>P(Publication Bias):</strong> ${(results.pBias * 100).toFixed(1)}%</p>
      <h5 style="margin-top: var(--space-2);">Model Weights:</h5>
      <ul style="font-size: 0.85em; margin: 0; padding-left: var(--space-4);">
        ${results.models.map(m => `<li>${m.name}: θ=${m.theta.toFixed(3)} (weight=${(m.weight*100).toFixed(0)}%)</li>`).join('')}
      </ul>
      <p style="color: ${results.pEffect > 0.9 ? 'var(--color-success-500)' : 'var(--color-warning-500)'}; font-weight: bold; margin-top: var(--space-2);">
        ${results.interpretation}
      </p>
    </div>
  `;'''

if old_modelavg in content:
    content = content.replace(old_modelavg, new_modelavg)
    print("1. Fixed runSimplifiedMA property names")
    fixes += 1

# Write back
with open('C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Total HTML fixes applied: {fixes}")
print("Done!")
