#!/usr/bin/env python3
"""
Extract trials from CochraneDataExtractor CSV files.
This will add ~8,000+ additional trials with OR, RR, MD, HR effect types.
"""

import os
import csv
import json
import re
from collections import defaultdict

print("=" * 80)
print("  EXTRACTING TRIALS FROM COCHRANE CSV FILES")
print("=" * 80)

csv_dir = "C:/Users/user/OneDrive - NHS/Documents/CochraneDataExtractor/data/pairwise"
data_rows_files = [f for f in os.listdir(csv_dir) if '-data-rows.csv' in f]

print(f"\nFound {len(data_rows_files)} data-rows CSV files")

all_trials = []
effect_type_counts = defaultdict(int)
domain_counts = defaultdict(int)

def determine_effect_type(row):
    """Determine effect type from row data."""
    # Check if binary outcome (has cases)
    exp_cases = row.get('Experimental cases', '')
    ctrl_cases = row.get('Control cases', '')

    # Check if continuous outcome (has mean/SD)
    exp_mean = row.get('Experimental mean', '')
    exp_sd = row.get('Experimental SD', '')

    # Check analysis name for hints
    analysis = row.get('Analysis name', '').lower()

    if 'hazard' in analysis or 'survival' in analysis or 'time to' in analysis:
        return 'HR'
    elif 'odds' in analysis:
        return 'OR'
    elif 'risk ratio' in analysis or 'relative risk' in analysis:
        return 'RR'
    elif 'risk difference' in analysis:
        return 'RD'
    elif 'mean difference' in analysis or 'standardised mean' in analysis or 'standardized mean' in analysis:
        if 'standardised' in analysis or 'standardized' in analysis:
            return 'SMD'
        return 'MD'
    elif exp_cases and ctrl_cases:
        # Binary data - default to OR
        return 'OR'
    elif exp_mean and exp_sd:
        # Continuous data
        return 'MD'
    else:
        # Generic - check Mean value range
        mean_val = row.get('Mean', '')
        try:
            m = float(mean_val)
            if 0 < m < 10:  # Ratio measure range
                return 'RR'
            else:
                return 'MD'
        except:
            return 'MD'

def determine_domain(analysis_name, review_id):
    """Determine medical domain from analysis name."""
    analysis_lower = analysis_name.lower() if analysis_name else ''

    domain_keywords = {
        'Cardiology': ['mortality', 'cardiovascular', 'heart', 'myocardial', 'stroke', 'blood pressure', 'hypertension', 'coronary'],
        'Oncology': ['cancer', 'tumor', 'tumour', 'survival', 'progression', 'chemotherapy', 'radiation', 'carcinoma'],
        'Infectious Disease': ['infection', 'antibiotic', 'viral', 'bacterial', 'HIV', 'hepatitis', 'pneumonia', 'sepsis'],
        'Neurology': ['neurological', 'seizure', 'epilepsy', 'parkinson', 'alzheimer', 'dementia', 'migraine', 'stroke'],
        'Psychiatry': ['depression', 'anxiety', 'schizophrenia', 'bipolar', 'psychiatric', 'mental', 'psychosis'],
        'Respiratory': ['asthma', 'COPD', 'pulmonary', 'respiratory', 'bronchitis', 'lung', 'breathing'],
        'Gastroenterology': ['gastrointestinal', 'ulcer', 'crohn', 'colitis', 'liver', 'hepatic', 'bowel'],
        'Rheumatology': ['arthritis', 'rheumatoid', 'lupus', 'joint', 'inflammatory', 'autoimmune'],
        'Endocrinology': ['diabetes', 'thyroid', 'hormone', 'metabolic', 'insulin', 'glucose'],
        'Nephrology': ['kidney', 'renal', 'dialysis', 'nephropathy', 'creatinine'],
        'Dermatology': ['skin', 'dermatitis', 'psoriasis', 'eczema', 'wound'],
        'Pediatrics': ['child', 'pediatric', 'infant', 'neonatal', 'newborn'],
        'Ophthalmology': ['eye', 'vision', 'retina', 'glaucoma', 'cataract'],
        'Hematology': ['blood', 'anemia', 'transfusion', 'coagulation', 'bleeding'],
    }

    for domain, keywords in domain_keywords.items():
        for kw in keywords:
            if kw in analysis_lower:
                return domain
    return 'General Medicine'

# Process each CSV file
file_count = 0
for csv_file in data_rows_files:
    file_path = os.path.join(csv_dir, csv_file)

    # Extract review ID from filename
    match = re.search(r'CD(\d+)', csv_file)
    review_id = f"CD{match.group(1)}" if match else "CDXXXXXX"

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Skip rows without essential data
                study = row.get('Study', '')
                mean_val = row.get('Mean', '')
                ci_start = row.get('CI start', '')
                ci_end = row.get('CI end', '')

                if not study or not mean_val:
                    continue

                try:
                    effect_val = float(mean_val)
                    ci_lo = float(ci_start) if ci_start else None
                    ci_hi = float(ci_end) if ci_end else None
                except ValueError:
                    continue

                # Skip invalid CIs
                if ci_lo is None or ci_hi is None:
                    continue
                if ci_lo >= ci_hi:
                    continue

                # Get sample sizes
                exp_n = row.get('Experimental N', '')
                ctrl_n = row.get('Control N', '')

                try:
                    n_treatment = int(float(exp_n)) if exp_n else 100
                    n_control = int(float(ctrl_n)) if ctrl_n else 100
                except:
                    n_treatment = 100
                    n_control = 100

                # Skip very small studies
                if n_treatment < 5 or n_control < 5:
                    continue

                # Determine effect type
                effect_type = determine_effect_type(row)

                # Get analysis info
                analysis_name = row.get('Analysis name', 'Primary outcome')
                study_year = row.get('Study year', '')

                # Determine domain
                domain = determine_domain(analysis_name, review_id)

                # Create trial record
                trial_id = f"CSV-{review_id}-{len(all_trials):05d}"

                trial = {
                    'id': trial_id,
                    'study': study,
                    'year': study_year,
                    'review': review_id,
                    'effect_type': effect_type,
                    'effect_value': round(effect_val, 4),
                    'ci_lo': round(ci_lo, 4),
                    'ci_hi': round(ci_hi, 4),
                    'n_treatment': n_treatment,
                    'n_control': n_control,
                    'outcome': analysis_name,
                    'domain': domain,
                    'source': 'CochraneCSV'
                }

                all_trials.append(trial)
                effect_type_counts[effect_type] += 1
                domain_counts[domain] += 1

    except Exception as e:
        print(f"Error processing {csv_file}: {e}")
        continue

    file_count += 1
    if file_count % 100 == 0:
        print(f"Processed {file_count}/{len(data_rows_files)} files, {len(all_trials):,} trials")

print(f"\n--- EXTRACTION COMPLETE ---")
print(f"Total trials extracted: {len(all_trials):,}")

print("\nEffect type distribution:")
for et, count in sorted(effect_type_counts.items(), key=lambda x: -x[1]):
    print(f"  {et}: {count:,}")

print("\nDomain distribution:")
for d, count in sorted(domain_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"  {d}: {count:,}")

# Save extracted trials
output_path = 'C:/Users/user/cochrane_csv_trials.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_trials, f, indent=2)

print(f"\nSaved {len(all_trials):,} trials to {output_path}")

print("\n" + "=" * 80)
print("  CSV EXTRACTION COMPLETE")
print("=" * 80)
