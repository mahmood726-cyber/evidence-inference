#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix remaining JavaScript errors"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file: {len(content.split(chr(10)))} lines")
fixes = 0

# Fix 1: Add null check at start of generateGRADESummary
old_grade = """    function generateGRADESummary(r) {
      // Determine GRADE factors
      const riskOfBias = 'Not assessed';  // Would need RoB data"""

new_grade = """    function generateGRADESummary(r) {
      // Early return if no results
      if (!r) {
        return '<div class="alert alert--warning">Run analysis first to generate GRADE summary.</div>';
      }
      // Determine GRADE factors
      const riskOfBias = 'Not assessed';  // Would need RoB data"""

if old_grade in content:
    content = content.replace(old_grade, new_grade)
    print("1. Added null check to generateGRADESummary")
    fixes += 1

# Write back
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal fixes applied: {fixes}")
print("Done!")
