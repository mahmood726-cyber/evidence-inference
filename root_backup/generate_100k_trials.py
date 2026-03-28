"""
Generate 70,000 additional RCT trials to expand validation dataset to 100,000
"""

import random
import json

# Configuration for 70,000 new trials (to add to existing 30,000)
TRIAL_DISTRIBUTION = {
    'MD': 19000,      # Total will be ~27,000
    'OR': 19000,      # Total will be ~27,000
    'HR': 9000,       # Total will be ~13,000
    'RR': 9000,       # Total will be ~13,000
    'SMD': 7000,      # Total will be ~10,000
    'RD': 5000,       # Total will be ~7,000
    'RateRatio': 2000 # Total will be ~3,000
}

# Medical domains with realistic outcomes
DOMAINS = {
    'Cardiology': [
        'cardiovascular mortality', 'major adverse cardiac events', 'myocardial infarction',
        'stroke', 'heart failure hospitalization', 'blood pressure reduction', 'LDL cholesterol',
        'ejection fraction improvement', 'arrhythmia recurrence', 'coronary revascularization'
    ],
    'Oncology': [
        'overall survival', 'progression-free survival', 'tumor response rate',
        'disease control rate', 'time to progression', 'quality of life score',
        'adverse events grade 3+', 'treatment discontinuation', 'biomarker response'
    ],
    'Neurology': [
        'cognitive function score', 'disability progression', 'relapse rate',
        'seizure frequency', 'pain intensity score', 'functional independence',
        'motor function assessment', 'quality of life', 'neurological improvement'
    ],
    'Infectious Disease': [
        'viral clearance', 'clinical cure rate', 'mortality', 'hospital admission',
        'time to symptom resolution', 'bacterial eradication', 'infection recurrence',
        'treatment failure', 'adverse drug reaction'
    ],
    'Psychiatry': [
        'depression severity score', 'anxiety symptom reduction', 'remission rate',
        'response rate', 'quality of life', 'functional improvement', 'relapse prevention',
        'sleep quality score', 'cognitive function'
    ],
    'Rheumatology': [
        'disease activity score', 'ACR response rate', 'joint damage progression',
        'pain reduction', 'physical function', 'quality of life', 'flare rate',
        'steroid sparing effect', 'radiographic progression'
    ],
    'Gastroenterology': [
        'clinical remission', 'endoscopic healing', 'symptom improvement',
        'quality of life', 'hospitalization rate', 'surgery rate', 'adverse events',
        'mucosal healing', 'disease recurrence'
    ],
    'Respiratory': [
        'FEV1 improvement', 'exacerbation rate', 'symptom score', 'exercise capacity',
        'quality of life', 'hospitalization rate', 'mortality', 'lung function decline',
        'dyspnea score'
    ],
    'Endocrinology': [
        'HbA1c reduction', 'fasting glucose', 'weight change', 'hypoglycemia events',
        'blood pressure', 'lipid profile', 'cardiovascular events', 'renal function',
        'quality of life'
    ],
    'Nephrology': [
        'eGFR decline', 'proteinuria reduction', 'kidney failure', 'cardiovascular events',
        'mortality', 'dialysis initiation', 'transplant outcomes', 'quality of life',
        'hospitalization'
    ],
    'Hematology': [
        'overall survival', 'event-free survival', 'complete response rate',
        'transfusion independence', 'hemoglobin improvement', 'platelet response',
        'bleeding events', 'thrombotic events', 'quality of life'
    ],
    'Dermatology': [
        'disease severity score', 'clear skin response', 'itch reduction',
        'quality of life', 'treatment satisfaction', 'flare rate', 'adverse events',
        'sustained response', 'patient-reported outcomes'
    ],
    'Ophthalmology': [
        'visual acuity change', 'intraocular pressure', 'disease progression',
        'anatomic outcomes', 'quality of life', 'treatment burden', 'adverse events',
        'vision-related function', 'central retinal thickness'
    ],
    'Orthopedics': [
        'pain reduction', 'functional improvement', 'range of motion', 'quality of life',
        'revision surgery rate', 'union rate', 'complication rate', 'return to activity',
        'patient satisfaction'
    ],
    'Pediatrics': [
        'growth parameters', 'developmental milestones', 'symptom improvement',
        'quality of life', 'hospitalization', 'adverse events', 'treatment adherence',
        'disease control', 'functional outcomes'
    ]
}

# Intervention types
INTERVENTIONS = [
    'active treatment', 'experimental drug', 'novel therapy', 'combination therapy',
    'targeted treatment', 'immunotherapy', 'biological agent', 'small molecule inhibitor',
    'monoclonal antibody', 'gene therapy', 'cell therapy', 'device intervention',
    'surgical procedure', 'behavioral intervention', 'lifestyle modification'
]

COMPARATORS = [
    'placebo', 'standard care', 'active control', 'usual care', 'best supportive care',
    'sham procedure', 'waitlist control', 'no intervention', 'conventional therapy'
]

def generate_effect_value(effect_type):
    """Generate realistic effect values for each type"""
    if effect_type == 'HR':
        # Hazard ratios typically 0.3-1.5
        return round(random.uniform(0.35, 1.45), 2)
    elif effect_type == 'RR':
        # Risk ratios typically 0.2-2.0
        return round(random.uniform(0.25, 1.85), 2)
    elif effect_type == 'OR':
        # Odds ratios typically 0.2-3.0
        return round(random.uniform(0.25, 2.75), 2)
    elif effect_type == 'MD':
        # Mean differences vary widely, use -20 to 20
        return round(random.uniform(-18, 18), 2)
    elif effect_type == 'SMD':
        # Standardized mean differences typically -2 to 2
        return round(random.uniform(-1.8, 1.8), 2)
    elif effect_type == 'RD':
        # Risk differences typically -0.3 to 0.3
        return round(random.uniform(-0.28, 0.28), 2)
    elif effect_type == 'RateRatio':
        # Rate ratios typically 0.3-2.0
        return round(random.uniform(0.35, 1.85), 2)
    return 1.0

def generate_ci(value, effect_type):
    """Generate realistic confidence intervals"""
    if effect_type in ['HR', 'RR', 'OR', 'RateRatio']:
        # Multiplicative scale - CI width proportional to value
        width = abs(value) * random.uniform(0.15, 0.45)
        ci_lo = round(max(0.01, value - width), 2)
        ci_hi = round(value + width, 2)
    else:
        # Additive scale (MD, SMD, RD)
        width = random.uniform(0.5, 3.0) if effect_type == 'MD' else random.uniform(0.2, 0.8)
        ci_lo = round(value - width, 2)
        ci_hi = round(value + width, 2)
    return ci_lo, ci_hi

def generate_trial(trial_id, effect_type, batch_num):
    """Generate a single trial"""
    domain = random.choice(list(DOMAINS.keys()))
    outcome = random.choice(DOMAINS[domain])
    intervention = random.choice(INTERVENTIONS)
    comparator = random.choice(COMPARATORS)

    # Sample sizes
    n_treatment = random.randint(50, 800)
    n_control = random.randint(50, 800)

    # Demographics
    mean_age = round(random.uniform(35, 75), 1)
    pct_male = random.randint(35, 70)

    # Effect estimates
    value = generate_effect_value(effect_type)
    ci_lo, ci_hi = generate_ci(value, effect_type)

    # Follow-up
    follow_up_months = random.choice([3, 6, 12, 18, 24, 36, 48, 60])

    # P-value
    p_val = random.choice(['P<0.001', 'P<0.01', 'P<0.05', 'P=0.03', 'P=0.04', 'P=0.02'])

    # NCT number
    nct = f"NCT{30000000 + batch_num * 10000 + trial_id:08d}"

    # Generate text based on effect type
    if effect_type in ['HR', 'RR', 'OR', 'RateRatio']:
        effect_text = f"{effect_type} {value}, 95% CI {ci_lo}-{ci_hi}"
    else:
        # Handle negative CI bounds with proper formatting
        if ci_lo < 0 and ci_hi < 0:
            effect_text = f"{effect_type} {value}, 95% CI {ci_lo}-{ci_hi}"
        elif ci_lo < 0:
            effect_text = f"{effect_type} {value}, 95% CI {ci_lo} to {ci_hi}"
        else:
            effect_text = f"{effect_type} {value}, 95% CI {ci_lo}-{ci_hi}"

    text = f"""EXP-{effect_type}-{batch_num:02d}-{trial_id:05d}: TRIAL-{effect_type}-{batch_num}-{trial_id} - {domain} {outcome}

This randomized controlled trial evaluated {outcome} in {domain.lower()} patients.
Patients were randomized to {intervention} (treatment arm, n={n_treatment}) versus {comparator} (control arm, n={n_control}).
The primary endpoint was {outcome}. Mean age was {mean_age} years, {pct_male}% were male.
Results: Primary outcome {effect_text}. {p_val}.
Follow-up was {follow_up_months} months. Trial registration: {nct}."""

    return {
        'id': f"EXP-{effect_type}-{batch_num:02d}-{trial_id:05d}",
        'source': f"TRIAL-{effect_type}-{batch_num}-{trial_id}",
        'domain': domain,
        'design': 'Superiority',
        'text': text,
        'groundTruth': {
            'primaryEffect': {
                'type': effect_type,
                'value': value,
                'ciLo': ci_lo,
                'ciHi': ci_hi
            },
            'treatment': {'n': n_treatment},
            'control': {'n': n_control},
            'registration': nct
        }
    }

def format_trial_js(trial):
    """Format trial as JavaScript object"""
    gt = trial['groundTruth']
    pe = gt['primaryEffect']

    # Escape backticks and special chars in text
    text = trial['text'].replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

    return f"""    {{
        id: '{trial['id']}',
        source: '{trial['source']}',
        domain: '{trial['domain']}',
        design: '{trial['design']}',
        text: `{text}`,
        groundTruth: {{
            primaryEffect: {{ type: '{pe['type']}', value: {pe['value']}, ciLo: {pe['ciLo']}, ciHi: {pe['ciHi']} }},
            treatment: {{ n: {gt['treatment']['n']} }},
            control: {{ n: {gt['control']['n']} }},
            registration: '{gt['registration']}'
        }}
    }}"""

def main():
    print("=" * 70)
    print("  GENERATING 70,000 ADDITIONAL RCT TRIALS")
    print("=" * 70)

    all_trials = []
    batch_num = 40  # Start after existing batches

    for effect_type, count in TRIAL_DISTRIBUTION.items():
        print(f"\nGenerating {count} {effect_type} trials...")

        trials_per_batch = 5000
        num_batches = (count + trials_per_batch - 1) // trials_per_batch

        for b in range(num_batches):
            batch_count = min(trials_per_batch, count - b * trials_per_batch)

            for i in range(batch_count):
                trial = generate_trial(b * trials_per_batch + i + 1, effect_type, batch_num)
                all_trials.append(trial)

            batch_num += 1
            print(f"  Batch {b+1}/{num_batches}: {batch_count} trials")

    print(f"\nTotal trials generated: {len(all_trials)}")

    # Write to JS file
    output_path = r"C:\Users\user\Downloads\Dataextractor\validation_expansion_70k.js"

    print(f"\nWriting to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("/**\n")
        f.write(" * RCTExtractor Validation Expansion - 70,000 Additional Trials\n")
        f.write(" * Generated for 100K validation dataset\n")
        f.write(" */\n\n")
        f.write("const EXPANSION_TRIALS_70K = [\n")

        for i, trial in enumerate(all_trials):
            if i > 0:
                f.write(",\n")
            f.write(format_trial_js(trial))

            if (i + 1) % 10000 == 0:
                print(f"  Written {i+1}/{len(all_trials)} trials...")

        f.write("\n];\n\n")
        f.write("// Export for Node.js\n")
        f.write("if (typeof module !== 'undefined') {\n")
        f.write("    module.exports = { EXPANSION_TRIALS_70K };\n")
        f.write("}\n")

    print(f"\nDone! Generated {len(all_trials)} trials")
    print(f"Output: {output_path}")

    # Summary
    print("\n" + "=" * 70)
    print("  DISTRIBUTION SUMMARY")
    print("=" * 70)
    for effect_type, count in TRIAL_DISTRIBUTION.items():
        print(f"  {effect_type:12} {count:,} trials")
    print(f"  {'TOTAL':12} {sum(TRIAL_DISTRIBUTION.values()):,} trials")

if __name__ == '__main__':
    main()
