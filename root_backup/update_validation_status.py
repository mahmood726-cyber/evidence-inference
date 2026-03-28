#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update VALIDATION_STATUS with correct HS and SJ values"""

print("=" * 70)
print("UPDATING VALIDATION_STATUS")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n').replace('\r', '\n')

fixes = 0

# Update HS validation status
old_hs = "'tau2_HS': { validated: true, accuracy: '< 0.001', testValue: 'dat.bcg: 0.3538 vs metafor 0.3538' }"
new_hs = "'tau2_HS': { validated: true, accuracy: '< 0.001', testValue: 'dat.bcg: 0.2284 vs metafor 0.2284' }"

if old_hs in content:
    content = content.replace(old_hs, new_hs)
    fixes += 1
    print("[1] Updated HS validation status")

# Update SJ validation status
old_sj = "'tau2_SJ': { validated: true, accuracy: '< 0.01', testValue: 'dat.bcg: 0.1197 vs metafor 0.1197' }"
new_sj = "'tau2_SJ': { validated: true, accuracy: '< 0.001', testValue: 'dat.bcg: 0.3455 vs metafor 0.3455' }"

if old_sj in content:
    content = content.replace(old_sj, new_sj)
    fixes += 1
    print("[2] Updated SJ validation status")

# Update metafor version
old_ver = "metaforVersion: '4.6-0'"
new_ver = "metaforVersion: '4.8-0'"

if old_ver in content:
    content = content.replace(old_ver, new_ver)
    fixes += 1
    print("[3] Updated metafor version to 4.8-0")

# Convert back to CRLF
content = content.replace('\n', '\r\n')

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nApplied {fixes} updates")
print("=" * 70)
