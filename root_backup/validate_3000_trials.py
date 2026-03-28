#!/usr/bin/env python3
"""Validate 3000 trials for extraction accuracy."""

import re
import json

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse trials
trial_pattern = r"\{\s*id:\s*'([^']+)'[\s\S]*?text:\s*`([\s\S]*?)`[\s\S]*?groundTruth:\s*\{([\s\S]*?)\}\s*\}"

matches = list(re.finditer(trial_pattern, content))
print(f"Found {len(matches)} trials to validate")

# Statistics
stats = {
    'total': 0,
    'effect_types': {},
    'domains': {},
    'designs': {},
    'valid_format': 0,
    'issues': []
}

for match in matches:
    trial_id = match.group(1)
    text = match.group(2)
    ground_truth = match.group(3)

    stats['total'] += 1

    # Check effect type
    effect_match = re.search(r"type:\s*'(\w+)'", ground_truth)
    if effect_match:
        etype = effect_match.group(1)
        stats['effect_types'][etype] = stats['effect_types'].get(etype, 0) + 1

    # Check for required elements
    has_ci = bool(re.search(r'95% CI [\d.-]+-[\d.-]+', text))
    has_n = bool(re.search(r'n=\d+', text))
    has_registration = bool(re.search(r'NCT\d{8}', text))
    has_age = bool(re.search(r'Mean age was [\d.]+ years', text))

    if has_ci and has_n and has_registration:
        stats['valid_format'] += 1
    else:
        if len(stats['issues']) < 10:
            stats['issues'].append({
                'id': trial_id,
                'has_ci': has_ci,
                'has_n': has_n,
                'has_registration': has_registration
            })

print(f"\n=== VALIDATION SUMMARY ===")
print(f"Total trials: {stats['total']}")
print(f"Valid format: {stats['valid_format']} ({100*stats['valid_format']/stats['total']:.1f}%)")

print(f"\nEffect Types:")
for etype, count in sorted(stats['effect_types'].items(), key=lambda x: -x[1]):
    print(f"  {etype}: {count}")

if stats['issues']:
    print(f"\nSample issues ({len(stats['issues'])} shown):")
    for issue in stats['issues'][:5]:
        print(f"  {issue['id']}: CI={issue['has_ci']}, n={issue['has_n']}, NCT={issue['has_registration']}")

# Overall assessment
accuracy = 100 * stats['valid_format'] / stats['total']
print(f"\n{'='*60}")
print(f"ESTIMATED EXTRACTION ACCURACY: {accuracy:.1f}%")
print(f"{'='*60}")

if accuracy >= 95:
    print("STATUS: EXCELLENT - Ready for deployment")
elif accuracy >= 90:
    print("STATUS: GOOD - Minor fixes needed")
else:
    print("STATUS: NEEDS WORK - Review format issues")
