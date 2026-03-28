"""
Extract validation trials from llm-meta-analysis GitHub repository
Source: https://github.com/resubmission2024/llm-meta-analysis
Contains 699 annotated RCTs with binary and continuous outcome data
"""

import csv
import math
import json

INPUT_PATH = r"C:\Users\user\llm-meta-analysis\evaluation\data\annotated_rct_dataset.csv"
OUTPUT_PATH = r"C:\Users\user\Downloads\Dataextractor\validation_llm_meta.js"

def clean_text(text):
    if not text:
        return ''
    text = str(text).replace('\\', '\\\\')
    text = text.replace("'", "\\'")
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = text.replace('`', "'")
    return text.strip()

def calculate_or(a, b, c, d):
    """Calculate odds ratio and 95% CI from 2x2 table"""
    # a = intervention events, b = intervention non-events
    # c = comparator events, d = comparator non-events
    try:
        # Add 0.5 continuity correction if any zero
        if a == 0 or b == 0 or c == 0 or d == 0:
            a += 0.5
            b += 0.5
            c += 0.5
            d += 0.5

        or_val = (a * d) / (b * c)
        log_or = math.log(or_val)
        se_log_or = math.sqrt(1/a + 1/b + 1/c + 1/d)

        ci_lo = math.exp(log_or - 1.96 * se_log_or)
        ci_hi = math.exp(log_or + 1.96 * se_log_or)

        return round(or_val, 2), round(ci_lo, 2), round(ci_hi, 2)
    except:
        return None, None, None

def calculate_rr(e1, n1, e2, n2):
    """Calculate risk ratio and 95% CI"""
    try:
        # Add 0.5 continuity correction if any zero events
        if e1 == 0 or e2 == 0:
            e1 += 0.5
            n1 += 1
            e2 += 0.5
            n2 += 1

        p1 = e1 / n1
        p2 = e2 / n2
        rr = p1 / p2

        log_rr = math.log(rr)
        se_log_rr = math.sqrt((1/e1 - 1/n1) + (1/e2 - 1/n2))

        ci_lo = math.exp(log_rr - 1.96 * se_log_rr)
        ci_hi = math.exp(log_rr + 1.96 * se_log_rr)

        return round(rr, 2), round(ci_lo, 2), round(ci_hi, 2)
    except:
        return None, None, None

def calculate_md(m1, sd1, n1, m2, sd2, n2):
    """Calculate mean difference and 95% CI"""
    try:
        md = m1 - m2

        # Pooled standard error
        se = math.sqrt((sd1**2 / n1) + (sd2**2 / n2))

        ci_lo = md - 1.96 * se
        ci_hi = md + 1.96 * se

        return round(md, 2), round(ci_lo, 2), round(ci_hi, 2)
    except:
        return None, None, None

def format_ci(effect_type, val, lo, hi):
    if effect_type in ['OR', 'RR']:
        return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"
    elif effect_type == 'MD':
        if lo < 0:
            return f"MD {val:.2f}, 95% CI {lo:.2f} to {hi:.2f}"
        else:
            return f"MD {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"
    return f"{effect_type} {val:.2f}, 95% CI {lo:.2f}-{hi:.2f}"

def main():
    print("Processing llm-meta-analysis annotated RCT dataset...")

    trials = []
    type_counts = {}
    skipped = {'incomplete': 0, 'calculation_error': 0}

    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            outcome = row.get('outcome', '')
            intervention = row.get('intervention', '')
            comparator = row.get('comparator', '')
            outcome_type = row.get('outcome_type', '')
            is_complete = row.get('is_data_complete', '').upper() == 'TRUE'
            pmcid = row.get('pmcid', '')

            if not is_complete:
                skipped['incomplete'] += 1
                continue

            effect_type = None
            val, lo, hi = None, None, None

            if outcome_type == 'binary':
                # Binary outcome - calculate OR and RR
                try:
                    ie = float(row.get('intervention_events', ''))
                    igs = float(row.get('intervention_group_size', ''))
                    ce = float(row.get('comparator_events', ''))
                    cgs = float(row.get('comparator_group_size', ''))

                    if all([ie >= 0, igs > 0, ce >= 0, cgs > 0]):
                        # Calculate OR (primary)
                        a = ie  # intervention events
                        b = igs - ie  # intervention non-events
                        c = ce  # comparator events
                        d = cgs - ce  # comparator non-events

                        val, lo, hi = calculate_or(a, b, c, d)
                        if val is not None:
                            effect_type = 'OR'
                except:
                    pass

            elif outcome_type == 'continuous':
                # Continuous outcome - calculate MD
                try:
                    im = float(row.get('intervention_mean', ''))
                    isd = float(row.get('intervention_standard_deviation', ''))
                    igs = float(row.get('intervention_group_size', ''))
                    cm = float(row.get('comparator_mean', ''))
                    csd = float(row.get('comparator_standard_deviation', ''))
                    cgs = float(row.get('comparator_group_size', ''))

                    if all([igs > 0, cgs > 0, isd >= 0, csd >= 0]):
                        val, lo, hi = calculate_md(im, isd, igs, cm, csd, cgs)
                        if val is not None:
                            effect_type = 'MD'
                except:
                    pass

            if effect_type is None:
                skipped['calculation_error'] += 1
                continue

            # Build text
            text_parts = [f"PMC{pmcid}:"]
            if outcome:
                out = clean_text(outcome)[:150]
                text_parts.append(f"Outcome: {out}.")
            if intervention and comparator:
                interv = clean_text(intervention)[:100]
                comp = clean_text(comparator)[:100]
                text_parts.append(f"{interv} vs {comp}.")

            effect_str = format_ci(effect_type, val, lo, hi)
            text_parts.append(f"Results: {effect_str}.")

            text = ' '.join(text_parts)

            type_counts[effect_type] = type_counts.get(effect_type, 0) + 1

            trial_id = f"LLMMA_{len(trials)+1}"
            trials.append({
                'id': trial_id,
                'text': text,
                'groundTruth': {
                    'primaryEffect': {
                        'type': effect_type,
                        'value': val,
                        'ciLo': lo,
                        'ciHi': hi
                    }
                }
            })

    print(f"\nValid trials extracted: {len(trials)}")
    print(f"\nSkipped:")
    for reason, count in skipped.items():
        print(f"  {reason}: {count}")

    print(f"\nBy effect type:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    # Write JavaScript
    js_content = f"""// LLM-Meta-Analysis Annotated RCT Dataset
// Source: https://github.com/resubmission2024/llm-meta-analysis
// {len(trials)} real trials with calculated effect sizes

const LLM_META_ANALYSIS_TRIALS = [
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
    module.exports = { LLM_META_ANALYSIS_TRIALS };
}
"""

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"\nSaved to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
