"""
Extract validation trials from Figshare efficacy dataset
Source: https://figshare.com/articles/dataset/Clinical_trials_efficacy_results/25247488
Contains ~120,000 rows with effect sizes and confidence intervals
"""

import csv
import json
import re

INPUT_PATH = r"C:\Users\user\Downloads\figshare_efficacy.csv"
OUTPUT_PATH = r"C:\Users\user\Downloads\Dataextractor\validation_figshare.js"

def clean_text(text):
    if not text:
        return ''
    text = str(text).replace('\\', '\\\\')
    text = text.replace("'", "\\'")
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('`', "'")
    return text.strip()

def classify_param_type(param_type):
    """Map Figshare param_type to our effect types"""
    if not param_type:
        return None
    pt = param_type.lower()

    # Hazard Ratio
    if 'hazard' in pt:
        return 'HR'

    # Odds Ratio
    if 'odds' in pt:
        return 'OR'

    # Risk Ratio / Relative Risk
    if 'risk ratio' in pt or 'relative risk' in pt or 'rr' in pt:
        return 'RR'

    # Mean Difference
    if 'mean difference' in pt or 'difference in' in pt or 'least squares' in pt:
        return 'MD'

    # Standardized Mean Difference
    if 'standardized' in pt or 'cohen' in pt or 'hedge' in pt:
        return 'SMD'

    # Risk Difference
    if 'risk difference' in pt or 'absolute' in pt:
        return 'RD'

    # Rate Ratio
    if 'rate ratio' in pt or 'incidence' in pt:
        return 'RateRatio'

    return None

def is_valid_value(val):
    """Check if value is valid for extraction"""
    if val is None or val == '':
        return False
    try:
        f = float(val)
        if f != f:  # NaN check
            return False
        if abs(f) > 1e10:  # Unreasonable value
            return False
        return True
    except:
        return False

def format_ci(effect_type, val, lo, hi):
    """Format effect with CI in extractable format"""
    if effect_type in ['OR', 'HR', 'RR', 'RateRatio']:
        return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"
    elif effect_type in ['MD', 'SMD', 'RD']:
        if lo < 0:
            return f"{effect_type} {val:.2f}, 95% CI {lo:.2f} to {hi:.2f}"
        else:
            return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"
    return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"

def main():
    print("Processing Figshare efficacy data...")

    trials = []
    seen_keys = set()
    type_counts = {}
    skipped = {'no_type': 0, 'invalid_value': 0, 'duplicate': 0, 'missing_ci': 0}

    with open(INPUT_PATH, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        row_count = 0

        for row in reader:
            row_count += 1
            if row_count % 10000 == 0:
                print(f"  Processed {row_count:,} rows...")

            nct_id = row.get('NCT_ID', '')
            param_type = row.get('param_type', '')
            param_value = row.get('param_value', '')
            ci_lo = row.get('ci_lower_limit_clean', '') or row.get('ci_lower_limit', '')
            ci_hi = row.get('ci_upper_limit_clean', '') or row.get('ci_upper_limit', '')
            condition = row.get('condition', '')
            outcome = row.get('outcome_title', '')
            intervention = row.get('intervention', '')
            comparator = row.get('comparator', '')
            enrollment = row.get('enrollment_num', '')

            # Classify effect type
            effect_type = classify_param_type(param_type)
            if not effect_type:
                skipped['no_type'] += 1
                continue

            # Validate values
            if not all([is_valid_value(param_value), is_valid_value(ci_lo), is_valid_value(ci_hi)]):
                if not is_valid_value(ci_lo) or not is_valid_value(ci_hi):
                    skipped['missing_ci'] += 1
                else:
                    skipped['invalid_value'] += 1
                continue

            val = float(param_value)
            lo = float(ci_lo)
            hi = float(ci_hi)

            # Validate CI order
            if lo > hi:
                lo, hi = hi, lo

            # Skip if value outside CI (data quality issue)
            if not (lo <= val <= hi) and abs(val - (lo + hi)/2) > abs(hi - lo):
                skipped['invalid_value'] += 1
                continue

            # Deduplicate by NCT_ID + outcome + effect
            key = f"{nct_id}_{outcome[:50]}_{effect_type}_{val:.2f}"
            if key in seen_keys:
                skipped['duplicate'] += 1
                continue
            seen_keys.add(key)

            # Build text
            text_parts = [f"{nct_id}:"]
            if condition:
                cond = clean_text(condition)[:100]
                text_parts.append(f"Condition: {cond}.")
            if outcome:
                out = clean_text(outcome)[:150]
                text_parts.append(f"Outcome: {out}.")
            if intervention and comparator:
                interv = clean_text(intervention)[:80]
                comp = clean_text(comparator)[:80]
                text_parts.append(f"{interv} vs {comp}.")
            if enrollment:
                try:
                    n = int(float(enrollment))
                    if n > 0:
                        text_parts.append(f"N={n}.")
                except:
                    pass

            effect_str = format_ci(effect_type, val, lo, hi)
            text_parts.append(f"Results: {effect_str}.")

            text = ' '.join(text_parts)

            # Count types
            type_counts[effect_type] = type_counts.get(effect_type, 0) + 1

            trial_id = f"FIGSH_{len(trials)+1}"
            trials.append({
                'id': trial_id,
                'text': text,
                'groundTruth': {
                    'primaryEffect': {
                        'type': effect_type,
                        'value': round(val, 2),
                        'ciLo': round(lo, 2),
                        'ciHi': round(hi, 2)
                    }
                }
            })

    print(f"\nTotal rows processed: {row_count:,}")
    print(f"Valid trials extracted: {len(trials):,}")
    print(f"\nSkipped:")
    for reason, count in skipped.items():
        print(f"  {reason}: {count:,}")

    print(f"\nBy effect type:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c:,}")

    # Write JavaScript
    js_content = f"""// Figshare Clinical Trials Efficacy Results
// Source: https://figshare.com/articles/dataset/Clinical_trials_efficacy_results/25247488
// {len(trials):,} real trials with effect sizes and confidence intervals

const FIGSHARE_REAL_TRIALS = [
"""

    for trial in trials:
        gt = trial['groundTruth']['primaryEffect']
        js_content += f"""    {{
        id: '{trial['id']}',
        text: '{clean_text(trial['text'])}',
        groundTruth: {{
            primaryEffect: {{ type: '{gt['type']}', value: {gt['value']}, ciLo: {gt['ciLo']}, ciHi: {gt['ciHi']} }}
        }}
    }},
"""

    js_content += """];

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FIGSHARE_REAL_TRIALS };
}
"""

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"\nSaved to {OUTPUT_PATH}")
    print(f"File size: {len(js_content):,} bytes")

if __name__ == '__main__':
    main()
