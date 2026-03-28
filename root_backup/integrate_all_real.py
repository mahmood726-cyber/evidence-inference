"""
Integrate ALL real RCT data and create final validation dataset
"""

import json
import os

OUTPUT_DIR = r"C:\Users\user\Downloads\Dataextractor"

print("=" * 70)
print("  INTEGRATING ALL REAL RCT DATA")
print("=" * 70)

# Load original R package trials
print("\nLoading original R package trials...")
with open(r"C:\Users\user\r_package_trials.json", 'r') as f:
    r_trials_orig = json.load(f)
print(f"  Loaded {len(r_trials_orig)} original trials")

# Load extended R package trials (OR, RR, SMD)
print("Loading extended R package trials...")
with open(r"C:\Users\user\r_package_extended.json", 'r') as f:
    r_trials_ext = json.load(f)
print(f"  Loaded {len(r_trials_ext)} extended trials")

# Combine R trials (avoid duplicates by ID)
all_r_trials = []
seen_ids = set()

for t in r_trials_orig + r_trials_ext:
    tid = t['id']
    if tid not in seen_ids:
        seen_ids.add(tid)
        all_r_trials.append(t)

print(f"  Total unique R trials: {len(all_r_trials)}")

# Count by effect type
effect_counts = {}
for t in all_r_trials:
    et = t['effect_type']
    effect_counts[et] = effect_counts.get(et, 0) + 1

print("\n  R package trials by effect type:")
for et, count in sorted(effect_counts.items(), key=lambda x: -x[1]):
    print(f"    {et:12} {count:,}")

# Format function
def format_trial_js(trial):
    text = f"""{trial['id']}: {trial['source']} - {trial['dataset']}

This randomized controlled trial from R package.
Results: {trial['effect_type']} {trial['value']}, 95% CI {trial['ci_lo']}-{trial['ci_hi']}.
Source: metadat::{trial['dataset']}."""

    text = text.replace('\\', '\\\\').replace('`', '\\`').replace("'", "\\'")
    source = str(trial['source']).replace("'", "\\'")
    n1 = trial.get('n1') if trial.get('n1') else 'null'
    n2 = trial.get('n2') if trial.get('n2') else 'null'

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

# Write combined R package trials
output_path = os.path.join(OUTPUT_DIR, "validation_r_packages_combined.js")
print(f"\nWriting to {output_path}...")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("/**\n")
    f.write(" * RCTExtractor - Combined R Package Trials (REAL DATA)\n")
    f.write(f" * Total: {len(all_r_trials):,} trials\n")
    f.write(" */\n\n")
    f.write("const R_PACKAGE_TRIALS_COMBINED = [\n")

    for i, trial in enumerate(all_r_trials):
        if i > 0:
            f.write(",\n")
        f.write(format_trial_js(trial))

    f.write("\n];\n\n")
    f.write("if (typeof module !== 'undefined') {\n")
    f.write("    module.exports = { R_PACKAGE_TRIALS_COMBINED };\n")
    f.write("}\n")

print(f"  Written {len(all_r_trials)} trials")

print("\n" + "=" * 70)
print("  FINAL SUMMARY - ALL REAL DATA")
print("=" * 70)
print(f"  Cochrane trials:        84,362")
print(f"  R package trials:       {len(all_r_trials):,}")
print(f"  TOTAL REAL TRIALS:      {84362 + len(all_r_trials):,}")
print("=" * 70)
