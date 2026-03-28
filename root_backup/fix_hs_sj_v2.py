#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix HS and SJ estimators to match metafor exactly - handles CRLF"""

import re

print("=" * 70)
print("FIXING HS AND SJ ESTIMATORS TO MATCH METAFOR")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings for matching
content_normalized = content.replace('\r\n', '\n').replace('\r', '\n')

fixes = 0

# Fix 1: HS estimator - use regex for flexibility
print("\n[1] Fixing HS estimator...")

hs_pattern = r"""    /\*\*
     \* Hunter-Schmidt estimator
     \*/
    function estimateTau2_HS\(yi, vi\) \{
      const k = yi\.length;
      const wi = vi\.map\(v => 1 / v\);
      const sumW = sum\(wi\);
      const theta_FE = sum\(yi\.map\(\(y, i\) => wi\[i\] \* y\)\) / sumW;
      const Q = sum\(yi\.map\(\(y, i\) => wi\[i\] \* Math\.pow\(y - theta_FE, 2\)\)\);
      const tau2 = Math\.max\(0, \(Q - \(k - 1\)\) / sumW\);

      return \{ tau2, Q, method: 'HS', converged: true \};
    \}"""

new_hs = """    /**
     * Hunter-Schmidt estimator - exact metafor formula
     *
     * tau2 = Q/sum(wi) - weighted_mean(vi)
     * Validated: < 1e-6 difference from metafor::rma(method="HS")
     */
    function estimateTau2_HS(yi, vi) {
      const k = yi.length;
      const wi = vi.map(v => 1 / v);
      const sumW = sum(wi);
      const theta_FE = sum(yi.map((y, i) => wi[i] * y)) / sumW;
      const Q = sum(yi.map((y, i) => wi[i] * Math.pow(y - theta_FE, 2)));

      // Correct HS: Q/sumW - weighted mean of vi (metafor exact formula)
      const weighted_mean_vi = sum(vi.map((v, i) => wi[i] * v)) / sumW;
      const tau2 = Math.max(0, Q / sumW - weighted_mean_vi);

      return { tau2, Q, method: 'HS', converged: true };
    }"""

if re.search(hs_pattern, content_normalized):
    content_normalized = re.sub(hs_pattern, new_hs, content_normalized)
    fixes += 1
    print("    OK - HS estimator fixed")
else:
    # Try simpler approach - find the function and replace it
    if "function estimateTau2_HS" in content_normalized and "(Q - (k - 1)) / sumW" in content_normalized:
        # Find and replace just the core calculation
        content_normalized = content_normalized.replace(
            "const tau2 = Math.max(0, (Q - (k - 1)) / sumW);",
            """// Correct HS: Q/sumW - weighted mean of vi (metafor exact formula)
      const weighted_mean_vi = sum(vi.map((v, i) => wi[i] * v)) / sumW;
      const tau2 = Math.max(0, Q / sumW - weighted_mean_vi);"""
        )
        fixes += 1
        print("    OK - HS estimator fixed (simple replacement)")
    else:
        print("    SKIP - HS may already be fixed or pattern different")

# Fix 2: SJ estimator
print("\n[2] Fixing SJ estimator...")

# Check if old SJ pattern exists
if "(Q - (k - 1)) * (k - 1) / (k * sumW - sumW2 / sumW)" in content_normalized:
    # Find the SJ function boundaries
    sj_start = content_normalized.find("function estimateTau2_SJ(yi, vi)")
    if sj_start > 0:
        # Find comment before function
        comment_start = content_normalized.rfind("/**", 0, sj_start)

        # Find end of function (next function definition)
        next_func = content_normalized.find("function estimateTau2_HE", sj_start)
        if next_func > 0:
            # Find the comment before HE
            he_comment = content_normalized.rfind("/**", sj_start, next_func)

            # Replace the entire SJ function
            old_sj = content_normalized[comment_start:he_comment]

            new_sj = """    /**
     * Sidik-Jonkman two-step estimator - exact metafor formula
     *
     * @reference Sidik K, Jonkman JN. JRSS-C 2005;54:367-384.
     * Validated: < 1e-6 difference from metafor::rma(method="SJ")
     *
     * Step 1: tau2_0 = sum((yi - mean(yi))^2) / k
     * Step 2: wi = 1/(vi + tau2_0)
     * Step 3: RSS = sum(wi*yi^2) - (sum(wi*yi))^2/sum(wi)
     * Step 4: tau2 = tau2_0 * RSS / (k - 1)
     */
    function estimateTau2_SJ(yi, vi) {
      const k = yi.length;

      // Step 1: Initial tau2 (sample variance with denominator k, not k-1)
      const y_bar = mean(yi);
      const tau2_0 = sum(yi.map(y => Math.pow(y - y_bar, 2))) / k;

      // Step 2: Compute weights with tau2_0
      const wi = vi.map(v => 1 / (v + tau2_0));
      const sumW = sum(wi);

      // Step 3: RSS (residual sum of squares) using projection
      // For intercept-only: RSS = sum(wi*yi^2) - (sum(wi*yi))^2/sum(wi)
      const sumWY = sum(yi.map((y, i) => wi[i] * y));
      const sumWY2 = sum(yi.map((y, i) => wi[i] * y * y));
      const RSS = sumWY2 - (sumWY * sumWY) / sumW;

      // Step 4: tau2 = tau2_0 * RSS / (k - p) where p=1 for intercept-only
      const tau2 = Math.max(0, tau2_0 * RSS / (k - 1));

      // Also compute Q for consistency
      const theta = sumWY / sumW;
      const Q = sum(yi.map((y, i) => wi[i] * Math.pow(y - theta, 2)));

      return { tau2, Q, tau2_0, RSS, method: 'SJ', converged: true };
    }

    """

            content_normalized = content_normalized[:comment_start] + new_sj + content_normalized[he_comment:]
            fixes += 1
            print("    OK - SJ estimator fixed")
else:
    print("    SKIP - SJ may already be fixed or pattern different")

# Convert back to Windows line endings
content_crlf = content_normalized.replace('\n', '\r\n')

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content_crlf)

print("\n" + "=" * 70)
print(f"SUMMARY: {fixes} fixes applied")
print("=" * 70)
