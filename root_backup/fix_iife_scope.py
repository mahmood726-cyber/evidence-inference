#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix IIFE scope issue - add winnersCurseCorrection inside the IIFE"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file: {len(content.split(chr(10)))} lines")

# The issue: at line 34264, window.winnersCurseCorrection = winnersCurseCorrection
# references a function that doesn't exist in that scope.
# Solution: Add the function definition BEFORE the export

winners_curse_function = '''
    // Winners' Curse Correction
    // Adjusts effect sizes for publication bias due to significance filtering
    function winnersCurseCorrection(yi, vi, alpha = 0.05) {
      const k = yi.length;
      const sei = vi.map(v => Math.sqrt(v));
      const zi = yi.map((y, i) => y / sei[i]);
      const z_crit = 1.96; // qnorm(1 - alpha/2)

      // Identify significant studies
      const significant = zi.map(z => Math.abs(z) > z_crit);
      const n_sig = significant.filter(s => s).length;

      // Apply conditional mean correction (shrinkage)
      const corrected = yi.map((y, i) => {
        if (significant[i]) {
          // Shrink significant effects toward zero
          const shrinkage = 0.85;
          return y * shrinkage;
        }
        return y;
      });

      // Calculate correction magnitude
      const originalMean = yi.reduce((a, b) => a + b, 0) / k;
      const correctedMean = corrected.reduce((a, b) => a + b, 0) / k;

      return {
        original: yi,
        corrected: corrected,
        n_significant: n_sig,
        n_total: k,
        proportion_significant: n_sig / k,
        original_mean: originalMean,
        corrected_mean: correctedMean,
        correction_magnitude: originalMean - correctedMean,
        method: 'Simple shrinkage correction for significant results',
        reference: 'Ioannidis JPA. PLoS Med 2008;5:e201'
      };
    }

'''

# Find the line before the export and insert the function
target = "    window.VALIDATION_DATASETS_EXTENDED = VALIDATION_DATASETS_EXTENDED;\n    window.winnersCurseCorrection = winnersCurseCorrection;"

if target in content:
    # Insert function definition before the exports
    new_content = content.replace(
        target,
        winners_curse_function + "    window.VALIDATION_DATASETS_EXTENDED = VALIDATION_DATASETS_EXTENDED;\n    window.winnersCurseCorrection = winnersCurseCorrection;"
    )
    content = new_content
    print("Added winnersCurseCorrection function inside IIFE scope")
else:
    print("Target pattern not found, trying alternative...")
    # Alternative: just before the export line
    alt_target = "    window.winnersCurseCorrection = winnersCurseCorrection;"
    if alt_target in content:
        content = content.replace(alt_target, winners_curse_function + alt_target)
        print("Added function before export (alternative method)")
    else:
        print("ERROR: Could not find insertion point")

# Write back
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

final_lines = len(content.split('\n'))
print(f"Final file: {final_lines} lines")
print("Done!")
