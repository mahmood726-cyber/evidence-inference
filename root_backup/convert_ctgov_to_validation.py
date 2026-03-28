"""
Convert ClinicalTrials.gov JSON results to JavaScript validation format
"""

import json
import re

INPUT_PATH = r"C:\Users\user\Downloads\Dataextractor\ctgov_rct_results.json"
OUTPUT_PATH = r"C:\Users\user\Downloads\Dataextractor\validation_ctgov_real.js"

def clean_text(text):
    """Clean text for JavaScript string"""
    if not text:
        return ''
    # Remove problematic characters
    text = text.replace('\\', '\\\\')
    text = text.replace("'", "\\'")
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('`', "'")
    return text.strip()

def format_ci(effect_type, val, lo, hi):
    """Format CI appropriately for effect type"""
    # For ratios, use standard CI format
    if effect_type in ['OR', 'HR', 'RR']:
        return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"
    # For differences
    elif effect_type in ['MD', 'SMD', 'RD']:
        if lo < 0:
            return f"{effect_type} {val:.2f}, 95% CI {lo:.2f} to {hi:.2f}"
        else:
            return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"
    return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"

def main():
    print("Converting ClinicalTrials.gov results to validation format...")

    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        results = json.load(f)

    print(f"Loaded {len(results):,} results")

    # Count by type
    type_counts = {}
    for r in results:
        t = r['effect_type']
        type_counts[t] = type_counts.get(t, 0) + 1

    print("\nBy effect type:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c:,}")

    # Group by NCT ID to avoid duplicates
    by_nct = {}
    for r in results:
        nct_id = r['nct_id']
        if nct_id not in by_nct:
            by_nct[nct_id] = []
        by_nct[nct_id].append(r)

    print(f"\nUnique studies: {len(by_nct):,}")

    # Generate JavaScript trials
    trials = []
    trial_id = 1

    for nct_id, study_results in by_nct.items():
        # Take up to 3 results per study to avoid over-representation
        for r in study_results[:3]:
            # Build trial text
            title = clean_text(r['title'])
            condition = clean_text(r['condition'])
            outcome = clean_text(r['outcome'])

            effect_type = r['effect_type']
            val = r['value']
            lo = r['ci_lo']
            hi = r['ci_hi']
            p_val = r.get('p_value', '')
            enrollment = r.get('enrollment', 0)

            # Generate realistic trial text
            effect_str = format_ci(effect_type, val, lo, hi)

            text_parts = [
                f"{nct_id}: {title}.",
                f"Condition: {condition}.",
                f"Outcome: {outcome}."
            ]

            if enrollment and enrollment > 0:
                text_parts.append(f"N={enrollment}.")

            text_parts.append(f"Results: {effect_str}.")

            if p_val:
                try:
                    if '<' in str(p_val):
                        text_parts.append(f"P{p_val}.")
                    else:
                        pv = float(p_val)
                        if pv < 0.001:
                            text_parts.append("P<0.001.")
                        elif pv < 0.05:
                            text_parts.append(f"P={pv:.3f}.")
                except:
                    pass

            text = ' '.join(text_parts)

            trial = {
                'id': f'CTGOV_{trial_id}',
                'text': text,
                'groundTruth': {
                    'primaryEffect': {
                        'type': effect_type,
                        'value': round(val, 2),
                        'ciLo': round(lo, 2),
                        'ciHi': round(hi, 2)
                    }
                }
            }

            trials.append(trial)
            trial_id += 1

    print(f"\nGenerated {len(trials):,} validation trials")

    # Write JavaScript file
    js_content = f"""// ClinicalTrials.gov Real RCT Results - Auto-generated
// Source: ClinicalTrials.gov API v2
// {len(trials):,} real trials with complete statistical results

const CTGOV_REAL_TRIALS = [
"""

    for trial in trials:
        js_content += f"""    {{
        id: '{trial['id']}',
        text: '{clean_text(trial['text'])}',
        groundTruth: {{
            primaryEffect: {{ type: '{trial['groundTruth']['primaryEffect']['type']}', value: {trial['groundTruth']['primaryEffect']['value']}, ciLo: {trial['groundTruth']['primaryEffect']['ciLo']}, ciHi: {trial['groundTruth']['primaryEffect']['ciHi']} }}
        }}
    }},
"""

    js_content += """];

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CTGOV_REAL_TRIALS };
}
"""

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Saved to {OUTPUT_PATH}")

    # Final stats
    final_types = {}
    for trial in trials:
        t = trial['groundTruth']['primaryEffect']['type']
        final_types[t] = final_types.get(t, 0) + 1

    print("\nFinal distribution:")
    for t, c in sorted(final_types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c:,}")


if __name__ == '__main__':
    main()
