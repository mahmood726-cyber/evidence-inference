#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix multiple JavaScript errors in the app"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file: {len(content.split(chr(10)))} lines")
fixes = 0

# Fix 1: runZCurveAnalysis - check for null before accessing .ok
old_zcurve = '''      const zcurve = zCurveAnalysis(studies);

        if (!zcurve.ok) {'''
new_zcurve = '''      const zcurve = zCurveAnalysis(studies);

        if (!zcurve || zcurve.error) {
          document.getElementById('zCurveResults').innerHTML = '<p class="text-warning">' + (zcurve ? zcurve.error : 'Need at least 10 studies for Z-curve analysis') + '</p>';
          return;
        }

        if (false) {  // Original check disabled'''
if old_zcurve in content:
    content = content.replace(old_zcurve, new_zcurve)
    print("1. Fixed runZCurveAnalysis null check")
    fixes += 1

# Fix 2: generateGRADESummary - check for r.het before accessing I2
old_grade = "const inconsistency = r.het.I2 > 75 ? 'Serious (-1)' : r.het.I2 > 50 ? 'Moderate' : 'Not serious';"
new_grade = "const inconsistency = (r.het && r.het.I2 !== undefined) ? (r.het.I2 > 75 ? 'Serious (-1)' : r.het.I2 > 50 ? 'Moderate' : 'Not serious') : 'Not assessed';"
if old_grade in content:
    content = content.replace(old_grade, new_grade)
    print("2. Fixed generateGRADESummary I2 check")
    fixes += 1

# Fix 3: imprecision check
old_imprecision = "const imprecision = r.pooled.ci_upper / r.pooled.ci_lower > 2 ? 'Serious (-1)' : 'Not serious';"
new_imprecision = "const imprecision = (r.pooled && r.pooled.ci_upper && r.pooled.ci_lower && r.pooled.ci_lower !== 0) ? (Math.abs(r.pooled.ci_upper / r.pooled.ci_lower) > 2 ? 'Serious (-1)' : 'Not serious') : 'Not assessed';"
if old_imprecision in content:
    content = content.replace(old_imprecision, new_imprecision)
    print("3. Fixed imprecision check")
    fixes += 1

# Fix 4: publication bias check
old_pubbias = "const publicationBias = r.egger.p_value < 0.10 ? 'Suspected (-1)' : 'Undetected';"
new_pubbias = "const publicationBias = (r.egger && r.egger.p_value !== undefined) ? (r.egger.p_value < 0.10 ? 'Suspected (-1)' : 'Undetected') : 'Not assessed';"
if old_pubbias in content:
    content = content.replace(old_pubbias, new_pubbias)
    print("4. Fixed publication bias check")
    fixes += 1

# Fix 5: Add Q_of_tau2 inside estimateTau2_PM
if "if (Q_of_tau2(0) <= k - 1)" in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "if (Q_of_tau2(0) <= k - 1)" in line and i > 0:
            prev_100 = '\n'.join(lines[max(0,i-100):i])
            if 'function Q_of_tau2' not in prev_100:
                q_def = '''      // Local Q function for PM estimator
      function Q_of_tau2(t2) {
        const w = vi.map(v => 1 / (v + t2));
        const sumW = sum(w);
        const theta = sum(yi.map((y, j) => w[j] * y)) / sumW;
        return sum(yi.map((y, j) => w[j] * Math.pow(y - theta, 2)));
      }
'''
                lines.insert(i, q_def)
                content = '\n'.join(lines)
                print("5. Added Q_of_tau2 function")
                fixes += 1
            break

# Fix 6: runSmallSampleCI null checks
old_ss = '''const zej = zejnullahiCI(yi, vi, tau2);
        const pred = calculatePredictionInterval(yi, vi, tau2);
        const profLik = profileLikelihoodTau2CI(yi, vi, tau2);

        document.getElementById('smallSampleResults').innerHTML'''
new_ss = '''const zej = zejnullahiCI(yi, vi, tau2);
        const pred = calculatePredictionInterval(yi, vi, tau2);
        const profLik = profileLikelihoodTau2CI(yi, vi, tau2);

        if (!zej || !pred || !profLik) {
          document.getElementById('smallSampleResults').innerHTML = '<p class="text-warning">Could not compute intervals</p>';
          return;
        }

        document.getElementById('smallSampleResults').innerHTML'''
if old_ss in content:
    content = content.replace(old_ss, new_ss)
    print("6. Added null checks in runSmallSampleCI")
    fixes += 1

# Fix 7: copasSelectionModel null check  
if "if (!copas.success) {" in content:
    content = content.replace("if (!copas.success) {", "if (!copas || !copas.success) {")
    print("7. Fixed Copas null check")
    fixes += 1

# Write back
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal fixes applied: {fixes}")
print("Done!")
