#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix scope issues - winnersCurseCorrection and export ordering"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file: {len(content.split(chr(10)))} lines")
fixes_made = []

# Issue 1: window.winnersCurseCorrection is exported before the function is defined
# Solution: Add the function definition BEFORE the first export that references it

# First, find if winnersCurseCorrection function exists
if 'function winnersCurseCorrection' in content:
    print("winnersCurseCorrection function exists")
else:
    print("winnersCurseCorrection function NOT FOUND - need to add before line 34264")

# The export at line 34264 references winnersCurseCorrection but the function
# is defined later. We need to add a stub or move the function.

# Check where winnersCurseCorrection function is defined
wc_idx = content.find('function winnersCurseCorrection')
export_idx = content.find('window.winnersCurseCorrection = winnersCurseCorrection;')

print(f"winnersCurseCorrection function at char: {wc_idx}")
print(f"winnersCurseCorrection export at char: {export_idx}")

if wc_idx > export_idx and export_idx > 0:
    print("Function is defined AFTER export - need to fix")

    # Option 1: Remove the early export since function is exported later
    content = content.replace(
        "window.winnersCurseCorrection = winnersCurseCorrection;\n",
        "// window.winnersCurseCorrection exported later\n",
        1  # Only first occurrence
    )
    fixes_made.append("Commented out early winnersCurseCorrection export")

# Issue 2: METHODS_APPENDIX and EXTENDED_VALIDATION_DATA may be in wrong scope
# Check if they're inside an IIFE

# Find the main IIFE structure
# The exports at line 34264 are inside an IIFE that closes around that point
# The later exports (line 39600+) are outside

# Let's check the structure around line 34266
check_line = content.find("// log.info('TruthCert-PairwisePro v1.0")
if check_line > 0:
    # Check if there's a closing brace of the IIFE nearby
    next_100_chars = content[check_line:check_line+200]
    print(f"Context around line 34266: {next_100_chars[:100]}")

# The METHODS_APPENDIX and EXTENDED_VALIDATION_DATA are defined later in the file
# and should be accessible. Let's ensure they're properly exported.

# Check existing exports for these
if 'window.METHODS_APPENDIX = METHODS_APPENDIX;' in content:
    print("METHODS_APPENDIX is exported")
else:
    print("METHODS_APPENDIX NOT exported - adding")

if 'window.EXTENDED_VALIDATION_DATA = EXTENDED_VALIDATION_DATA;' in content:
    print("EXTENDED_VALIDATION_DATA is exported")
else:
    print("EXTENDED_VALIDATION_DATA NOT exported - adding")

# The issue might be that these are defined inside a block that's not the global scope
# Let's check if there's an IIFE closing before the definitions

# Find where METHODS_APPENDIX is defined
ma_def = content.find('const METHODS_APPENDIX = {')
evd_def = content.find('const EXTENDED_VALIDATION_DATA = {')

print(f"METHODS_APPENDIX defined at char: {ma_def}")
print(f"EXTENDED_VALIDATION_DATA defined at char: {evd_def}")

# Check if they're inside the IIFE by looking for })(); before their definition
# The IIFE likely ends around line 34266

# Let's find the end of the main IIFE
iife_patterns = [
    "})();\n",
    "}\n})();\n",
]

# Actually, let me just ensure these are in global scope by checking
# if they're outside the main IIFE

# A better approach: Move the definitions to be at the top level
# Or ensure the export block at the end works properly

# The real issue is that the test is running inside the browser where
# only window.* properties are accessible. The exports at line 39600+ should work
# but maybe there's a syntax issue.

# Let's verify the export block at the end is correct
last_export_block = content.rfind("if (typeof window !== 'undefined')")
if last_export_block > 0:
    export_sample = content[last_export_block:last_export_block+500]
    print(f"\nLast export block (first 500 chars):\n{export_sample[:300]}")

# Write back
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

final_lines = len(content.split('\n'))
print(f"\nFinal file: {final_lines} lines")
print(f"Fixes made: {len(fixes_made)}")
for fix in fixes_made:
    print(f"  - {fix}")
