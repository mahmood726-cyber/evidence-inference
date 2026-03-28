#!/usr/bin/env python3
"""
Phase 1: Fix RR extraction bugs and prepare for 30,000 trial expansion.
Analyzes current data and fixes CI formatting issues.
"""

import json
import re
import os

print("=" * 80)
print("  PHASE 1: FIX RR EXTRACTION AND ANALYZE DATA")
print("=" * 80)

# Load current Cochrane data
with open('C:/Users/user/cochrane_trials.json', 'r', encoding='utf-8') as f:
    trials = json.load(f)

print(f"\nLoaded {len(trials):,} trials from cochrane_trials.json")

# Analyze effect types
effect_types = {}
for t in trials:
    et = t.get('effect_type', 'Unknown')
    effect_types[et] = effect_types.get(et, 0) + 1

print("\nEffect type distribution:")
for et, count in sorted(effect_types.items(), key=lambda x: -x[1]):
    print(f"  {et}: {count:,}")

# Find RR trials with potential issues
rr_trials = [t for t in trials if t.get('effect_type') == 'RR']
print(f"\n--- Analyzing {len(rr_trials)} RR trials ---")

issues_found = 0
fixed_trials = []

for i, t in enumerate(trials):
    trial = t.copy()

    # Get CI values
    ci_lo = t.get('ci_lo', '')
    ci_hi = t.get('ci_hi', '')

    # Convert to string and check for issues
    ci_lo_str = str(ci_lo)
    ci_hi_str = str(ci_hi)

    # Fix trailing periods
    if ci_lo_str.endswith('.'):
        ci_lo_str = ci_lo_str.rstrip('.')
        issues_found += 1
    if ci_hi_str.endswith('.'):
        ci_hi_str = ci_hi_str.rstrip('.')
        issues_found += 1

    # Fix double decimals like "2.06."
    ci_lo_str = re.sub(r'\.(\d+)\.', r'.\1', ci_lo_str)
    ci_hi_str = re.sub(r'\.(\d+)\.', r'.\1', ci_hi_str)

    # Convert back to float
    try:
        trial['ci_lo'] = float(ci_lo_str) if ci_lo_str else 0.0
    except ValueError:
        print(f"  Warning: Could not parse ci_lo '{ci_lo_str}' for trial {i}")
        trial['ci_lo'] = 0.0

    try:
        trial['ci_hi'] = float(ci_hi_str) if ci_hi_str else 0.0
    except ValueError:
        print(f"  Warning: Could not parse ci_hi '{ci_hi_str}' for trial {i}")
        trial['ci_hi'] = 0.0

    fixed_trials.append(trial)

print(f"\nFixed {issues_found} CI formatting issues")

# Save fixed data
with open('C:/Users/user/cochrane_trials_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(fixed_trials, f)
print(f"Saved fixed data to cochrane_trials_fixed.json")

# Now check what's in the CochraneDataExtractor CSV directory
csv_dir = "C:/Users/user/OneDrive - NHS/Documents/CochraneDataExtractor/data/pairwise"
if os.path.exists(csv_dir):
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    print(f"\n--- CochraneDataExtractor CSV Analysis ---")
    print(f"Total CSV files: {len(csv_files):,}")

    # Categorize by file type
    data_rows = [f for f in csv_files if '-data-rows.csv' in f]
    overall = [f for f in csv_files if '-overall-estimates' in f]
    rob = [f for f in csv_files if '-risk-of-bias' in f]
    study_info = [f for f in csv_files if '-study-information' in f]

    print(f"  Data rows files: {len(data_rows)}")
    print(f"  Overall estimates: {len(overall)}")
    print(f"  Risk of bias: {len(rob)}")
    print(f"  Study information: {len(study_info)}")

    # Sample one data-rows file to understand structure
    if data_rows:
        sample_file = os.path.join(csv_dir, data_rows[0])
        print(f"\nSample CSV structure from: {data_rows[0]}")

        import csv
        with open(sample_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames
            print(f"Columns: {columns}")

            # Read first few rows
            for i, row in enumerate(reader):
                if i >= 3:
                    break
                print(f"\nRow {i+1}:")
                for k, v in list(row.items())[:10]:
                    if v:
                        print(f"  {k}: {v}")
else:
    print(f"\nWarning: CSV directory not found: {csv_dir}")

print("\n" + "=" * 80)
print("  PHASE 1 COMPLETE")
print("=" * 80)
