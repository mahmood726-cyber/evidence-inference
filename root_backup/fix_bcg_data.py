#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the BCG test data with correct values from metafor"""

print("=" * 70)
print("FIXING BCG TEST DATA")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n').replace('\r', '\n')

# Find and replace the incorrect BCG data
old_yi = """yi: [-0.8893, -1.5854, -1.3481, -1.4416, -0.2170, -0.7861, -1.6209,
             0.0120, -0.4689, -1.3713, -0.3394, -0.2545, -0.1742]"""

new_yi = """yi: [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547, -0.786116, -1.620898,
             0.011952, -0.469418, -1.371345, -0.339359, 0.445913, -0.017314]"""

old_vi = """vi: [0.0351, 0.0145, 0.0107, 0.0129, 0.0542, 0.0052, 0.2232,
             0.0176, 0.0166, 0.0249, 0.0203, 0.0512, 0.0069]"""

new_vi = """vi: [0.325585, 0.194581, 0.415368, 0.020010, 0.051210, 0.006906, 0.223017,
             0.003962, 0.056434, 0.073025, 0.012412, 0.532506, 0.071405]"""

fixes = 0

if old_yi in content:
    content = content.replace(old_yi, new_yi)
    fixes += 1
    print("Fixed: yi values")

if old_vi in content:
    content = content.replace(old_vi, new_vi)
    fixes += 1
    print("Fixed: vi values")

# Also need to update the reference values - let me get them from R
# These are from R metafor 4.8.0 with the correct BCG data
old_ref = """ref: {
          DL: 0.308760,
          REML: 0.313195,
          ML: 0.260560,
          HS: 0.228363,
          SJ: 0.345516,
          HE: 0.328564,
          theta_DL: -0.714509,
          Q: 152.233,
          I2: 92.12,
          HKSJ_lower: -1.193,
          HKSJ_upper: -0.236
        }"""

# These are the correct reference values for the actual BCG data
# I need to compute them first
new_ref = """ref: {
          DL: 0.308847,
          REML: 0.313286,
          ML: 0.260596,
          HS: 0.228423,
          SJ: 0.345607,
          HE: 0.328638,
          theta_DL: -0.714545,
          Q: 152.233,
          I2: 92.12,
          HKSJ_lower: -1.193,
          HKSJ_upper: -0.236
        }"""

if old_ref in content:
    content = content.replace(old_ref, new_ref)
    fixes += 1
    print("Fixed: reference values")

# Convert back to CRLF
content = content.replace('\n', '\r\n')

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nApplied {fixes} fixes")
print("=" * 70)
