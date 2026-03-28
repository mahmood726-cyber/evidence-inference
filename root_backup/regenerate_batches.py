#!/usr/bin/env python3
"""
Remove existing BATCH27 and BATCH28, then regenerate them properly with all 200 trials
"""

import re

# Read the file
with open(r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js', 'r', encoding='utf-8') as f:
    content = f.read()

print("Step 1: Removing existing BATCH27_TO_1900 and BATCH28_TO_2000...")

# Remove BATCH27_TO_1900 completely
batch27_pattern = r'\n// =+\n// BATCH27_TO_1900.*?const BATCH27_TO_1900 = \[.*?\];\n'
match = re.search(batch27_pattern, content, re.DOTALL)
if match:
    print(f"  Found BATCH27_TO_1900 at position {match.start()}, removing...")
    content = content[:match.start()] + '\n' + content[match.end():]
else:
    print("  BATCH27_TO_1900 not found with header, trying without header...")
    batch27_pattern2 = r'const BATCH27_TO_1900 = \[.*?\];\n'
    content = re.sub(batch27_pattern2, '', content, flags=re.DOTALL)

# Remove BATCH28_TO_2000 completely
batch28_pattern = r'\n// =+\n// BATCH28_TO_2000.*?const BATCH28_TO_2000 = \[.*?\];\n'
match = re.search(batch28_pattern, content, re.DOTALL)
if match:
    print(f"  Found BATCH28_TO_2000 at position {match.start()}, removing...")
    content = content[:match.start()] + '\n' + content[match.end():]
else:
    print("  BATCH28_TO_2000 not found with header, trying without header...")
    batch28_pattern2 = r'const BATCH28_TO_2000 = \[.*?\];\n'
    content = re.sub(batch28_pattern2, '', content, flags=re.DOTALL)

# Also remove the main batch header
header_pattern = r'\n// =+\n// BATCH 27-28: 200 RHEUMATOLOGY RCT TRIALS.*?// =+\n'
content = re.sub(header_pattern, '\n', content, flags=re.DOTALL)

# Check for ...BATCH27 and ...BATCH28 in GROUND_TRUTH_CASES and remove them
content = content.replace('    ...BATCH27_TO_1900,\n', '')
content = content.replace('    ...BATCH28_TO_2000,\n', '')
content = content.replace('    ...BATCH27_TO_1900,', '')
content = content.replace('    ...BATCH28_TO_2000,', '')
content = content.replace('...BATCH27_TO_1900,\n', '')
content = content.replace('...BATCH28_TO_2000,\n', '')
content = content.replace('...BATCH27_TO_1900,', '')
content = content.replace('...BATCH28_TO_2000,', '')

# Clean up any double newlines
content = re.sub(r'\n{4,}', '\n\n\n', content)

# Write the file
with open(r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Step 2: Verifying removal...")
# Check if they're gone
if 'const BATCH27_TO_1900' in content:
    print("  WARNING: BATCH27_TO_1900 still exists!")
else:
    print("  BATCH27_TO_1900 removed successfully")

if 'const BATCH28_TO_2000' in content:
    print("  WARNING: BATCH28_TO_2000 still exists!")
else:
    print("  BATCH28_TO_2000 removed successfully")

print("\nNow run add_batch27_28_rheumatology.py to add the complete 200 trials")
