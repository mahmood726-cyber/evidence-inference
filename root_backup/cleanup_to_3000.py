#!/usr/bin/env python3
"""Cleanup validation file to exactly 3000 unique trials."""

import re

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all const BATCH definitions
batch_pattern = r'const\s+(BATCH\d+[A-Z_]*|GROUND_TRUTH_ORIGINAL|BATCH\d+_TO_\d+|BATCH\d+_[A-Z]+)\s*=\s*\['

# Find the GROUND_TRUTH_CASES definition
gt_match = re.search(r'const\s+GROUND_TRUTH_CASES\s*=\s*\[([\s\S]*?)\];', content)
if not gt_match:
    print("ERROR: Could not find GROUND_TRUTH_CASES")
    exit(1)

# Extract all trial objects from the file
trial_pattern = r'\{\s*id:\s*\'([^\']+)\'[\s\S]*?groundTruth:\s*\{[\s\S]*?\}\s*\}'

# Find all matches
all_matches = list(re.finditer(trial_pattern, content))
print(f"Found {len(all_matches)} total trial blocks")

# Track unique trials (first occurrence wins)
seen_ids = set()
unique_trials = []

for match in all_matches:
    trial_id = match.group(1)
    trial_block = match.group(0)

    if trial_id not in seen_ids:
        seen_ids.add(trial_id)
        unique_trials.append((trial_id, trial_block))

print(f"Unique trials: {len(unique_trials)}")

# Keep first 3000
target = 3000
if len(unique_trials) > target:
    unique_trials = unique_trials[:target]
    print(f"Trimmed to {target} trials")

# Rebuild the file with clean structure
trials_js = ",\n    ".join([t[1] for t in unique_trials])

new_content = f'''// RCTExtractor v4.9.1-AI Validation Study
// 3000 Clinical Trials - Comprehensive Validation Dataset
// Generated for RCTExtractor accuracy benchmarking

const GROUND_TRUTH_CASES = [
    {trials_js}
];

// Export for validation
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ GROUND_TRUTH_CASES }};
}}
'''

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify
with open(file_path, 'r', encoding='utf-8') as f:
    verify_content = f.read()

final_count = len(re.findall(r"id:\s*'[^']+'", verify_content))
print(f"Final trial count: {final_count}")
print(f"File size: {len(verify_content):,} bytes")
