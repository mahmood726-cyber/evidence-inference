#!/usr/bin/env python3
"""Debug RR extraction failures."""

import re
import json

# Load Cochrane trials
with open('C:/Users/user/cochrane_trials.json', 'r', encoding='utf-8') as f:
    trials = json.load(f)

# Filter RR trials
rr_trials = [t for t in trials if t.get('effect_type') == 'RR']
print(f"Total RR trials: {len(rr_trials)}")

# Simulate extraction and find failures
def extract_rr(text):
    patterns = [
        r'RR\s*([\d.]+),?\s*95%\s*CI\s*([\d.-]+)-([\d.-]+)',
    ]
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return float(match.group(1)), float(match.group(2)), float(match.group(3))
    return None, None, None

# Generate sample text and check extraction
failures = []
successes = 0

for t in rr_trials[:100]:  # Sample first 100
    effect_val = t.get('effect_value', 1.0)
    ci_lo = t.get('ci_lo', 0.5)
    ci_hi = t.get('ci_hi', 2.0)

    # Generate text in same format as validation file
    text = f"Results: Primary outcome RR {effect_val}, 95% CI {ci_lo}-{ci_hi}. P<0.05."

    ext_val, ext_lo, ext_hi = extract_rr(text)

    if ext_val is not None:
        val_match = abs(ext_val - effect_val) < 0.01
        lo_match = abs(ext_lo - ci_lo) < 0.01
        hi_match = abs(ext_hi - ci_hi) < 0.01

        if val_match and lo_match and hi_match:
            successes += 1
        else:
            failures.append({
                'text': text,
                'expected': (effect_val, ci_lo, ci_hi),
                'extracted': (ext_val, ext_lo, ext_hi)
            })
    else:
        failures.append({
            'text': text,
            'expected': (effect_val, ci_lo, ci_hi),
            'extracted': (None, None, None)
        })

print(f"Successes: {successes}, Failures: {len(failures)}")

if failures:
    print("\nSample failures:")
    for f in failures[:5]:
        print(f"  Text: {f['text'][:80]}")
        print(f"  Expected: {f['expected']}")
        print(f"  Extracted: {f['extracted']}")
        print()
