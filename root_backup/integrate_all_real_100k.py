"""
Integrate all real RCT data sources into one comprehensive validation file

Sources:
1. Cochrane CSV data: 84,362 trials (validation_real_rcts.js)
2. metadat R packages: 2,520 trials (validation_metadat_real.js)
3. ClinicalTrials.gov: 18,314 trials (validation_ctgov_real.js)
"""

import re
import os

OUTPUT_PATH = r"C:\Users\user\Downloads\Dataextractor\validation_all_real_100k.js"

SOURCES = [
    (r"C:\Users\user\Downloads\Dataextractor\validation_real_rcts.js", "REAL_RCT_TRIALS"),
    (r"C:\Users\user\Downloads\Dataextractor\validation_metadat_real.js", "METADAT_REAL_TRIALS"),
    (r"C:\Users\user\Downloads\Dataextractor\validation_ctgov_real.js", "CTGOV_REAL_TRIALS"),
]

def extract_trials_from_js(filepath, var_name):
    """Extract trial objects from JavaScript file"""
    print(f"Loading {filepath}...")

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Find the array content
    start_pattern = f"const {var_name} = ["
    start_idx = content.find(start_pattern)
    if start_idx == -1:
        print(f"  Warning: Could not find {var_name} array")
        return []

    # Find all trial objects
    trials = []
    trial_pattern = re.compile(
        r"\{\s*id:\s*['\"]([^'\"]+)['\"],\s*text:\s*['\"](.+?)['\"],\s*groundTruth:\s*\{[^}]*primaryEffect:\s*\{\s*type:\s*['\"](\w+)['\"],\s*value:\s*([-\d.]+),\s*ciLo:\s*([-\d.]+),\s*ciHi:\s*([-\d.]+)\s*\}",
        re.DOTALL
    )

    for match in trial_pattern.finditer(content):
        trial_id = match.group(1)
        text = match.group(2)
        effect_type = match.group(3)
        value = float(match.group(4))
        ci_lo = float(match.group(5))
        ci_hi = float(match.group(6))

        trials.append({
            'id': trial_id,
            'text': text,
            'effect_type': effect_type,
            'value': value,
            'ci_lo': ci_lo,
            'ci_hi': ci_hi
        })

    print(f"  Extracted {len(trials):,} trials")
    return trials


def main():
    print("=" * 70)
    print("  INTEGRATING ALL REAL RCT DATA SOURCES")
    print("=" * 70)
    print()

    all_trials = []

    # Load each source
    for filepath, var_name in SOURCES:
        if os.path.exists(filepath):
            trials = extract_trials_from_js(filepath, var_name)
            all_trials.extend(trials)
        else:
            print(f"  File not found: {filepath}")

    print(f"\nTotal trials loaded: {len(all_trials):,}")

    # Count by type before dedup
    type_counts = {}
    for t in all_trials:
        et = t['effect_type']
        type_counts[et] = type_counts.get(et, 0) + 1

    print("\nBy effect type (before dedup):")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c:,}")

    # Generate combined JavaScript
    print("\nWriting combined file...")

    js_content = f"""// ALL REAL RCT VALIDATION DATA - Combined from multiple sources
// Sources:
//   - Cochrane Systematic Reviews (validation_real_rcts.js)
//   - metadat R Package (validation_metadat_real.js)
//   - ClinicalTrials.gov API (validation_ctgov_real.js)
// Total: {len(all_trials):,} real RCT results

const ALL_REAL_TRIALS = [
"""

    for i, trial in enumerate(all_trials):
        # Clean text for JS
        text = trial['text'].replace('\\', '\\\\').replace("'", "\\'")

        js_content += f"""    {{
        id: '{trial['id']}',
        text: '{text}',
        groundTruth: {{
            primaryEffect: {{ type: '{trial['effect_type']}', value: {trial['value']}, ciLo: {trial['ci_lo']}, ciHi: {trial['ci_hi']} }}
        }}
    }},
"""

    js_content += """];

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ALL_REAL_TRIALS };
}
"""

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Saved to {OUTPUT_PATH}")

    # Final stats
    final_types = {}
    for t in all_trials:
        et = t['effect_type']
        final_types[et] = final_types.get(et, 0) + 1

    print(f"\nFinal dataset: {len(all_trials):,} trials")
    print("\nBy effect type:")
    for t, c in sorted(final_types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c:,}")

    # Source breakdown
    sources = {}
    for t in all_trials:
        tid = t['id']
        if tid.startswith('COCHRANE'):
            s = 'Cochrane'
        elif tid.startswith('METADAT'):
            s = 'metadat'
        elif tid.startswith('CTGOV'):
            s = 'CTGov'
        else:
            s = 'Other'
        sources[s] = sources.get(s, 0) + 1

    print("\nBy source:")
    for s, c in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {s}: {c:,}")


if __name__ == '__main__':
    main()
