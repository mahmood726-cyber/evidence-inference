#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the I2 test assertion - don't multiply by 100"""

print("=" * 70)
print("FIXING I2 ASSERTION")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# The test does: assertClose(i2 * 100, BCG.ref.I2, ...)
# But i2 is already 92.12 (percentage), so we shouldn't multiply by 100
old_i2_assert = "assertClose(i2 * 100, BCG.ref.I2, 0.1, 'I_squared');"
new_i2_assert = "assertClose(i2, BCG.ref.I2, 0.1, 'I_squared');  // i2 is already percentage"

if old_i2_assert in content:
    content = content.replace(old_i2_assert, new_i2_assert)
    fixes += 1
    print("[1] Fixed: I2 assertion (don't multiply by 100)")
else:
    print("[1] SKIP: I2 assertion pattern not found")

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nApplied {fixes} fixes")
print("=" * 70)
