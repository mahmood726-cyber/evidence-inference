#!/usr/bin/env python3
"""
Fix the GROUND_TRUTH_CASES to include BATCH23 and BATCH24
"""

import re

input_file = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if BATCH23 and BATCH24 are already in GROUND_TRUTH_CASES
if '...BATCH23_TO_1500' in content and '...BATCH24_TO_1600' in content:
    if content.count('...BATCH23_TO_1500') > 0:
        # Check if they're in the GROUND_TRUTH_CASES section
        gt_match = re.search(r'const GROUND_TRUTH_CASES = \[(.*?)\];', content, re.DOTALL)
        if gt_match and '...BATCH23_TO_1500' in gt_match.group(1):
            print("BATCH23_TO_1500 and BATCH24_TO_1600 already in GROUND_TRUTH_CASES")
        else:
            # Need to add them
            # Find the closing of GROUND_TRUTH_CASES and add before it
            pattern = r'(\.\.\.BATCH\d+_TO_\d+)\];(\s*\n\s*//\s*=+\s*\n\s*//\s*EXPANDED VALIDATION METRICS)'
            replacement = r'\1,\n    ...BATCH23_TO_1500,\n    ...BATCH24_TO_1600];\2'
            content = re.sub(pattern, replacement, content)

            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Added BATCH23_TO_1500 and BATCH24_TO_1600 to GROUND_TRUTH_CASES")
else:
    print("BATCH23_TO_1500 or BATCH24_TO_1600 not found in file!")
    print("Please run add_batch23_24_neurology.py first")

# Verify
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

gt_match = re.search(r'const GROUND_TRUTH_CASES = \[(.*?)\];', content, re.DOTALL)
if gt_match:
    gt_content = gt_match.group(1)
    batches = re.findall(r'\.\.\.(\w+)', gt_content)
    print(f"\nBatches in GROUND_TRUTH_CASES: {len(batches)}")
    print("Last 5 batches:", batches[-5:] if len(batches) >= 5 else batches)
