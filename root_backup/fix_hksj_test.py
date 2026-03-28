#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the HKSJ test - needs theta and tau2 arguments"""

print("=" * 70)
print("FIXING HKSJ TEST")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# The test needs to pass: calculateHKSJ(yi, vi, theta, tau2)
# Current: calculateHKSJ(BCG.yi, BCG.vi, reml.tau2) - wrong!
# Should be: calculateHKSJ(BCG.yi, BCG.vi, pooled.theta, reml.tau2)

old_hksj = "const hksj = calculateHKSJ(BCG.yi, BCG.vi, reml.tau2);"
new_hksj = """// Need to calculate pooled estimate first
      const pooled_for_hksj = calculatePooledEstimate(BCG.yi, BCG.vi, reml.tau2);
      const hksj = calculateHKSJ(BCG.yi, BCG.vi, pooled_for_hksj.theta, reml.tau2);"""

if old_hksj in content:
    content = content.replace(old_hksj, new_hksj)
    fixes += 1
    print("[1] Fixed: HKSJ test (add theta argument)")
else:
    print("[1] SKIP: HKSJ pattern not found")

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nApplied {fixes} fixes")
print("=" * 70)
