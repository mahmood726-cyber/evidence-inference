#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final fix for BCG test data"""

import re

print("=" * 70)
print("FINAL FIX FOR BCG TEST DATA")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix yi values - handle any whitespace pattern
old_yi_pattern = r"yi: \[-0\.8893.*?-0\.1742\]"
new_yi = "yi: [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547, -0.786116, -1.620898, 0.011952, -0.469418, -1.371345, -0.339359, 0.445913, -0.017314]"

if re.search(old_yi_pattern, content, re.DOTALL):
    content = re.sub(old_yi_pattern, new_yi, content, flags=re.DOTALL)
    fixes += 1
    print("[1] Fixed: yi values")
else:
    print("[1] SKIP: yi pattern not found")

# Fix vi values
old_vi_pattern = r"vi: \[0\.0351.*?0\.0069\]"
new_vi = "vi: [0.325585, 0.194581, 0.415368, 0.020010, 0.051210, 0.006906, 0.223017, 0.003962, 0.056434, 0.073025, 0.012412, 0.532506, 0.071405]"

if re.search(old_vi_pattern, content, re.DOTALL):
    content = re.sub(old_vi_pattern, new_vi, content, flags=re.DOTALL)
    fixes += 1
    print("[2] Fixed: vi values")
else:
    print("[2] SKIP: vi pattern not found")

# Fix individual reference values that may have been partially fixed
replacements = [
    ("theta_DL: -0.714509", "theta_DL: -0.714117"),
    ("HKSJ_lower: -1.193", "HKSJ_lower: -1.108"),
    ("HKSJ_upper: -0.236", "HKSJ_upper: -0.321"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        fixes += 1
        print(f"[+] Fixed: {old[:20]}...")

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nApplied {fixes} fixes")
print("=" * 70)
