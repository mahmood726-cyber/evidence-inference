"""
Create Final Real RCT Dataset
Combine all real data sources for validation
"""

import json
import os

OUTPUT_DIR = r"C:\Users\user\Downloads\Dataextractor"

print("=" * 70)
print("  CREATING FINAL REAL RCT DATASET")
print("=" * 70)

# Load metadat comprehensive extraction
print("\nLoading metadat comprehensive data...")
try:
    with open(r"C:\Users\user\metadat_comprehensive.json", 'r') as f:
        metadat = json.load(f)
    print(f"  Loaded {len(metadat)} trials from metadat")
except:
    metadat = []
    print("  metadat file not found")

# Count by effect type
if metadat:
    types = {}
    for t in metadat:
        et = t['effect_type']
        types[et] = types.get(et, 0) + 1
    print("  By type:", types)

# Summary
total_r_package = len(metadat)

print("\n" + "=" * 70)
print("  REAL DATA SUMMARY")
print("=" * 70)
print(f"  Cochrane CSV trials:    84,362")
print(f"  R package trials:       {total_r_package:,}")
print(f"  TOTAL REAL TRIALS:      {84362 + total_r_package:,}")
print("=" * 70)

# Format metadat trials for JS
def format_trial_js(trial):
    """Format a trial for JavaScript"""
    # Build text description
    text = f"""{trial['id']}: {trial['source']} - {trial['dataset']}

This is real RCT data from the metadat R package.
Results: {trial['effect_type']} {trial['value']}, 95% CI {trial['ci_lo']} to {trial['ci_hi']}.
Source: metadat::{trial['dataset']}."""

    # Escape for JS
    text = text.replace('\\', '\\\\').replace('`', '\\`').replace("'", "\\'")
    source = str(trial['source']).replace("'", "\\'")

    n1 = trial.get('n1') if trial.get('n1') and trial.get('n1') != 'NA' else 'null'
    n2 = trial.get('n2') if trial.get('n2') and trial.get('n2') != 'NA' else 'null'

    return f"""    {{
        id: '{trial['id']}',
        source: '{source}',
        domain: 'R-Package',
        text: `{text}`,
        groundTruth: {{
            primaryEffect: {{ type: '{trial['effect_type']}', value: {trial['value']}, ciLo: {trial['ci_lo']}, ciHi: {trial['ci_hi']} }},
            treatment: {{ n: {n1} }},
            control: {{ n: {n2} }},
            registration: null
        }}
    }}"""

# Write metadat trials to JS
output_path = os.path.join(OUTPUT_DIR, "validation_metadat_real.js")
print(f"\nWriting metadat trials to {output_path}...")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("/**\n")
    f.write(" * RCTExtractor - Real Data from metadat R Package\n")
    f.write(f" * Total: {len(metadat):,} trials\n")
    f.write(" */\n\n")
    f.write("const METADAT_REAL_TRIALS = [\n")

    for i, trial in enumerate(metadat):
        if i > 0:
            f.write(",\n")
        f.write(format_trial_js(trial))

    f.write("\n];\n\n")
    f.write("if (typeof module !== 'undefined') {\n")
    f.write("    module.exports = { METADAT_REAL_TRIALS };\n")
    f.write("}\n")

print(f"  Written {len(metadat)} trials")
print("\nDone!")
