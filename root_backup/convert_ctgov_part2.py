"""
Convert ClinicalTrials.gov Part 2 results to validation format and combine with Part 1
"""

import json

INPUT_PATH1 = r"C:\Users\user\Downloads\Dataextractor\ctgov_rct_results.json"
INPUT_PATH2 = r"C:\Users\user\Downloads\Dataextractor\ctgov_rct_results_part2.json"
OUTPUT_PATH = r"C:\Users\user\Downloads\Dataextractor\validation_ctgov_combined.js"

def clean_text(text):
    if not text:
        return ''
    text = text.replace('\\', '\\\\')
    text = text.replace("'", "\\'")
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('`', "'")
    return text.strip()

def format_ci(effect_type, val, lo, hi):
    if effect_type in ['OR', 'HR', 'RR']:
        return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"
    elif effect_type in ['MD', 'SMD', 'RD']:
        if lo < 0:
            return f"{effect_type} {val:.2f}, 95% CI {lo:.2f} to {hi:.2f}"
        else:
            return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"
    return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"

def main():
    print("Combining CTGov Part 1 and Part 2...")

    # Load both parts
    with open(INPUT_PATH1, 'r', encoding='utf-8') as f:
        results1 = json.load(f)
    print(f"Part 1: {len(results1):,} results")

    with open(INPUT_PATH2, 'r', encoding='utf-8') as f:
        results2 = json.load(f)
    print(f"Part 2: {len(results2):,} results")

    all_results = results1 + results2
    print(f"Total: {len(all_results):,} results")

    # Count by type
    type_counts = {}
    for r in all_results:
        t = r['effect_type']
        type_counts[t] = type_counts.get(t, 0) + 1

    print("\nBy effect type:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c:,}")

    # Group by NCT ID
    by_nct = {}
    for r in all_results:
        nct_id = r['nct_id']
        if nct_id not in by_nct:
            by_nct[nct_id] = []
        by_nct[nct_id].append(r)

    print(f"\nUnique studies: {len(by_nct):,}")

    # Generate trials (up to 3 per study)
    trials = []
    trial_id = 1

    for nct_id, study_results in by_nct.items():
        for r in study_results[:3]:
            title = clean_text(r['title'])
            condition = clean_text(r['condition'])
            outcome = clean_text(r['outcome'])

            effect_type = r['effect_type']
            val = r['value']
            lo = r['ci_lo']
            hi = r['ci_hi']
            p_val = r.get('p_value', '')
            enrollment = r.get('enrollment', 0)

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

            trials.append({
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
            })

            trial_id += 1

    print(f"\nGenerated {len(trials):,} validation trials")

    # Write JavaScript
    js_content = f"""// ClinicalTrials.gov COMBINED Real RCT Results
// Source: ClinicalTrials.gov API v2 (ALL studies with results)
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
