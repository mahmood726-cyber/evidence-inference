#!/usr/bin/env python3
"""
Add BATCH23_TO_1500 and BATCH24_TO_1600 to GROUND_TRUTH_CASES
"""

import re

input_file = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the last batch in GROUND_TRUTH_CASES and add the new ones
# Look for pattern like "...BATCHXX_TO_XXXX];"
pattern = r'(const GROUND_TRUTH_CASES = \[[\s\S]*?)(\.\.\.BATCH\d+_(?:TO_\d+|\w+))\];'

def add_batches(match):
    prefix = match.group(1)
    last_batch = match.group(2)
    return f'{prefix}{last_batch},\n    ...BATCH23_TO_1500,\n    ...BATCH24_TO_1600];'

# Check if already added
if '...BATCH23_TO_1500' in content:
    print("BATCH23_TO_1500 already in GROUND_TRUTH_CASES spread")
else:
    content = re.sub(pattern, add_batches, content)

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added BATCH23_TO_1500 and BATCH24_TO_1600 to GROUND_TRUTH_CASES")

# Verify
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all spreads in GROUND_TRUTH_CASES
gt_match = re.search(r'const GROUND_TRUTH_CASES = \[([\s\S]*?)\];', content)
if gt_match:
    gt_content = gt_match.group(1)
    spreads = re.findall(r'\.\.\.([\w_]+)', gt_content)
    print(f"\nTotal spreads in GROUND_TRUTH_CASES: {len(spreads)}")
    print(f"Last 5: {spreads[-5:]}")

    if 'BATCH23_TO_1500' in spreads and 'BATCH24_TO_1600' in spreads:
        print("\nSUCCESS: Both BATCH23_TO_1500 and BATCH24_TO_1600 are included!")
    else:
        print("\nWARNING: Missing batches!")
