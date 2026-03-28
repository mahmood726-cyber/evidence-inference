#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add missing wrapper functions for UI buttons"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file: {len(content.split(chr(10)))} lines")
fixes = 0

# Find the window exports section to add new wrapper function
# Add runMLOutlierDetection wrapper

wrapper_function = '''
    // Wrapper for ML Outlier Detection button
    function runMLOutlierDetection() {
      const r = AppState.results;
      if (!r || !r.studies) {
        showToast('Run analysis first', 'error');
        return;
      }

      try {
        const yi = r.studies.map(s => s.yi);
        const vi = r.studies.map(s => s.vi);
        const names = r.studies.map(s => s.study || s.name || 'Study');

        const outliers = mlOutlierDetection(yi, vi, names);
        renderOutlierDetection(outliers);
        showToast('Outlier detection complete', 'success');
      } catch (e) {
        showToast('Outlier detection failed: ' + e.message, 'error');
        console.error(e);
      }
    }
'''

# Find location to insert (before window exports)
insert_marker = "    window.mlOutlierDetection = mlOutlierDetection;"
if insert_marker in content and "function runMLOutlierDetection()" not in content:
    content = content.replace(insert_marker, wrapper_function + "\n" + insert_marker)
    print("1. Added runMLOutlierDetection wrapper function")
    fixes += 1

# Add to window exports
old_export = "window.mlOutlierDetection = mlOutlierDetection;"
new_export = "window.mlOutlierDetection = mlOutlierDetection;\n    window.runMLOutlierDetection = runMLOutlierDetection;"
if old_export in content and "window.runMLOutlierDetection" not in content:
    content = content.replace(old_export, new_export)
    print("2. Added runMLOutlierDetection to window exports")
    fixes += 1

# Write back
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal fixes applied: {fixes}")
print("Done!")
