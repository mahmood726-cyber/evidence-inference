#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the I2 test - should pass k-1 (df) not k"""

print("=" * 70)
print("FIXING I2 TEST AND HKSJ/MCMC TESTS")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix 1: I2 test - pass k-1 instead of k
old_i2 = "const i2 = calculateI2(dl.Q, BCG.yi.length);"
new_i2 = "const i2 = calculateI2(dl.Q, BCG.yi.length - 1);  // df = k-1"

if old_i2 in content:
    content = content.replace(old_i2, new_i2)
    fixes += 1
    print("[1] Fixed: I2 test (pass k-1 instead of k)")
else:
    print("[1] SKIP: I2 pattern not found")

# Fix 2: The MCMC test needs to handle cases where summary might not have theta
# The issue is likely that the Bayesian function is not finding enough iterations
# Let's make the test more robust by using fewer iterations and checking structure
old_mcmc = "const mcmc1 = bayesianMetaAnalysis(BCG.yi, BCG.vi, { seed: 12345, iterations: 500 });"
new_mcmc = "const mcmc1 = bayesianMetaAnalysis(BCG.yi, BCG.vi, { seed: 12345, iterations: 1000, burnin: 200, thin: 1 });"

if old_mcmc in content:
    content = content.replace(old_mcmc, new_mcmc)
    # Also fix the second call
    content = content.replace(
        "const mcmc2 = bayesianMetaAnalysis(BCG.yi, BCG.vi, { seed: 12345, iterations: 500 });",
        "const mcmc2 = bayesianMetaAnalysis(BCG.yi, BCG.vi, { seed: 12345, iterations: 1000, burnin: 200, thin: 1 });"
    )
    fixes += 1
    print("[2] Fixed: MCMC test (use consistent settings)")
else:
    print("[2] SKIP: MCMC pattern not found")

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nApplied {fixes} fixes")
print("=" * 70)
