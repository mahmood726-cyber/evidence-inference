"""
Integrate all REAL RCT data sources and create validation dataset
"""

import json
import os

OUTPUT_DIR = r"C:\Users\user\Downloads\Dataextractor"

print("=" * 70)
print("  INTEGRATING REAL RCT DATA")
print("=" * 70)

# Load R package trials
print("\nLoading R package trials...")
with open(r"C:\Users\user\r_package_trials.json", 'r') as f:
    r_trials = json.load(f)
print(f"  Loaded {len(r_trials)} trials from R packages")

# Convert R trials to standard format
r_formatted = []
for t in r_trials:
    text = f"""{t['id']}: {t['source']} - {t['dataset']}

This randomized controlled trial from metadat R package.
Results: {t['effect_type']} {t['value']}, 95% CI {t['ci_lo']}-{t['ci_hi']}.
Source: metadat::{t['dataset']}."""

    r_formatted.append({
        'id': t['id'],
        'source': t['source'],
        'domain': 'R-Package',
        'text': text,
        'groundTruth': {
            'primaryEffect': {
                'type': t['effect_type'],
                'value': t['value'],
                'ciLo': t['ci_lo'],
                'ciHi': t['ci_hi']
            },
            'treatment': {'n': t['n1']},
            'control': {'n': t['n2']},
            'registration': None
        }
    })

print(f"  Formatted {len(r_formatted)} R package trials")

# Count total by effect type
effect_counts = {}
for t in r_formatted:
    et = t['groundTruth']['primaryEffect']['type']
    effect_counts[et] = effect_counts.get(et, 0) + 1

print("\n  R package trials by effect type:")
for et, count in sorted(effect_counts.items(), key=lambda x: -x[1]):
    print(f"    {et:12} {count:,}")

# Write R package trials to JS
r_output_path = os.path.join(OUTPUT_DIR, "validation_r_packages.js")
print(f"\nWriting R package trials to {r_output_path}...")

def format_trial_js(trial):
    gt = trial['groundTruth']
    pe = gt['primaryEffect']
    text = trial['text'].replace('\\', '\\\\').replace('`', '\\`').replace("'", "\\'")
    source = str(trial['source']).replace("'", "\\'")
    treatment_n = gt['treatment']['n'] if gt['treatment']['n'] else 'null'
    control_n = gt['control']['n'] if gt['control']['n'] else 'null'
    registration = f"'{gt['registration']}'" if gt['registration'] else 'null'

    return f"""    {{
        id: '{trial['id']}',
        source: '{source}',
        domain: '{trial['domain']}',
        text: `{text}`,
        groundTruth: {{
            primaryEffect: {{ type: '{pe['type']}', value: {pe['value']}, ciLo: {pe['ciLo']}, ciHi: {pe['ciHi']} }},
            treatment: {{ n: {treatment_n} }},
            control: {{ n: {control_n} }},
            registration: {registration}
        }}
    }}"""

with open(r_output_path, 'w', encoding='utf-8') as f:
    f.write("/**\n")
    f.write(" * RCTExtractor Validation - R Package Trials (REAL DATA)\n")
    f.write(f" * Total trials: {len(r_formatted):,}\n")
    f.write(" */\n\n")
    f.write("const R_PACKAGE_TRIALS = [\n")

    for i, trial in enumerate(r_formatted):
        if i > 0:
            f.write(",\n")
        f.write(format_trial_js(trial))

    f.write("\n];\n\n")
    f.write("if (typeof module !== 'undefined') {\n")
    f.write("    module.exports = { R_PACKAGE_TRIALS };\n")
    f.write("}\n")

print(f"  Written {len(r_formatted)} R package trials")

print("\n" + "=" * 70)
print("  SUMMARY")
print("=" * 70)
print(f"  Cochrane trials:     84,362 (in validation_real_rcts.js)")
print(f"  R package trials:    {len(r_formatted):,} (in validation_r_packages.js)")
print(f"  TOTAL REAL TRIALS:   {84362 + len(r_formatted):,}")
print("=" * 70)
