#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the automated unit test suite - correct Bayesian summary access"""

print("=" * 70)
print("FIXING UNIT TEST SUITE")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n').replace('\r', '\n')

# Fix the MCMC test - the summary uses 'theta' not 'mu'
old_test = "const mcmcMatch = Math.abs(mcmc1.summary.mu.mean - mcmc2.summary.mu.mean) < 0.0001;"
new_test = "const mcmcMatch = mcmc1.summary && mcmc2.summary && Math.abs(mcmc1.summary.theta.mean - mcmc2.summary.theta.mean) < 0.0001;"

if old_test in content:
    content = content.replace(old_test, new_test)
    print("Fixed: Changed summary.mu.mean to summary.theta.mean")
else:
    print("Pattern not found - may already be fixed")

# Convert back to CRLF
content = content.replace('\n', '\r\n')

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print("=" * 70)
