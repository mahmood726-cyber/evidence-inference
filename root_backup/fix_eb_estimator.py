#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix EB estimator to match metafor 4.8-0"""

print("=" * 70)
print("FIXING EB ESTIMATOR")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# The current EB implementation uses:
#   num = sum((y - theta)^2 - vi)
#   tau2_new = num / k
#
# The correct Morris-style formula is:
#   num = sum(wi * (yi - theta)^2) - (k - 1)
#   denom = sum(wi) - sum(wi^2) / sum(wi)
#   tau2_new = tau2 + num / denom

# Find and replace the EB estimator function
old_eb = '''    function estimateTau2_EB(yi, vi, maxIter = 100, tol = 1e-8) {'''

# Search for the complete EB function to understand its structure
import re

# Find the EB function
eb_match = re.search(r'function estimateTau2_EB\(yi, vi, maxIter = 100, tol = 1e-8\) \{.*?return \{[^}]+\};[\s\n]*\}', content, re.DOTALL)

if eb_match:
    old_eb_func = eb_match.group(0)
    print(f"Found EB function at position {eb_match.start()}")
    print(f"Function length: {len(old_eb_func)} chars")

    # Create the corrected EB estimator
    new_eb_func = '''function estimateTau2_EB(yi, vi, maxIter = 100, tol = 1e-8) {
      // Empirical Bayes estimator (Morris 1983)
      // Uses iterative approach similar to PM
      const k = yi.length;

      // Initialize with DL estimate
      let tau2 = estimateTau2_DL(yi, vi).tau2;

      for (let iter = 0; iter < maxIter; iter++) {
        const wi = vi.map(v => 1 / (v + tau2));
        const sumW = sum(wi);
        const theta = sum(yi.map((y, i) => wi[i] * y)) / sumW;

        // Morris-style update: find tau2 where weighted RSS = k-1
        const RSS = sum(yi.map((y, i) => wi[i] * Math.pow(y - theta, 2)));
        const num = RSS - (k - 1);
        const denom = sumW - sum(wi.map(w => w * w)) / sumW;

        const tau2New = Math.max(0, tau2 + num / denom);

        if (Math.abs(tau2New - tau2) < tol) {
          return {
            tau2: tau2New,
            iterations: iter + 1,
            method: 'EB',
            converged: true
          };
        }
        tau2 = tau2New;
      }

      return {
        tau2: tau2,
        iterations: maxIter,
        method: 'EB',
        converged: false
      };
    }'''

    content = content.replace(old_eb_func, new_eb_func)
    print("Replaced EB function with Morris-style iteration")

    with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
        f.write(content)

    print("\nEB estimator fixed!")
else:
    print("ERROR: Could not find EB function")

print("=" * 70)
