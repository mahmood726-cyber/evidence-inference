#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add EB and PM estimators to automated test suite"""

print("=" * 70)
print("ADDING EB AND PM TO TEST SUITE")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix 1: Add EB and PM reference values after HE
print("\n[1] Adding EB and PM reference values...")
old_ref = "          HE: 0.328564,\n"
new_ref = """          HE: 0.328564,
          EB: 0.318069,  // metafor 4.8-0
          PM: 0.318094,  // metafor 4.8-0
"""

if old_ref in content:
    content = content.replace(old_ref, new_ref)
    fixes += 1
    print("    OK - Added EB: 0.318069, PM: 0.318094")
else:
    print("    SKIP - Reference pattern not found")

# Fix 2: Add EB test after HE test
print("\n[2] Adding EB test...")
old_he_test = "      assertClose(he.tau2, BCG.ref.HE, 0.001, 'tau2_HE');\n"
new_he_test = """      assertClose(he.tau2, BCG.ref.HE, 0.001, 'tau2_HE');

      // Test 7: EB estimator
      const eb = estimateTau2_EB(BCG.yi, BCG.vi);
      assertClose(eb.tau2, BCG.ref.EB, 0.001, 'tau2_EB');

      // Test 8: PM estimator
      const pm = estimateTau2_PM(BCG.yi, BCG.vi);
      assertClose(pm.tau2, BCG.ref.PM, 0.001, 'tau2_PM');
"""

if old_he_test in content:
    content = content.replace(old_he_test, new_he_test)
    fixes += 1
    print("    OK - Added EB and PM tests")
else:
    print("    SKIP - HE test pattern not found")

# Fix 3: Renumber subsequent tests (7 -> 9, 8 -> 10, etc.)
print("\n[3] Renumbering subsequent tests...")
renumber_map = [
    ("// Test 7: Pooled estimate", "// Test 9: Pooled estimate"),
    ("// Test 8: Cochran's Q", "// Test 10: Cochran's Q"),
    ("// Test 9: I-squared", "// Test 11: I-squared"),
    ("// Test 10: HKSJ confidence interval", "// Test 12: HKSJ confidence interval"),
    ("// Test 11: MCMC reproducibility", "// Test 13: MCMC reproducibility"),
    ("// Test 12: Bayesian posterior", "// Test 14: Bayesian posterior"),
]

for old, new in renumber_map:
    if old in content:
        content = content.replace(old, new)
        print(f"    {old[:25]}... -> {new[:25]}...")

fixes += 1

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nApplied {fixes} fixes")
print("=" * 70)
print("Test suite now has 14 tests (was 12)")
print("=" * 70)
