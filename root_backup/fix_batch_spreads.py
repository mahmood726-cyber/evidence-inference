#!/usr/bin/env python3
"""
Fix the GROUND_TRUTH_CASES array to include BATCH19_TO_1100 and BATCH20_TO_1200
"""

file_path = r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the closing of GROUND_TRUTH_CASES
old_pattern = '...BATCH24_TO_1600];'
new_pattern = '''...BATCH24_TO_1600,
    ...BATCH19_TO_1100,
    ...BATCH20_TO_1200];'''

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully added BATCH19_TO_1100 and BATCH20_TO_1200 to GROUND_TRUTH_CASES")
else:
    print("Pattern not found - checking if already added")
    if '...BATCH19_TO_1100' in content and '...BATCH20_TO_1200' in content:
        print("Batches already included in GROUND_TRUTH_CASES")
    else:
        print("ERROR: Could not find the pattern to replace")
