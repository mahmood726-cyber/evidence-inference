#!/usr/bin/env python3
"""Fix CI patterns - use exact format extractor expects."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The MD pattern expects: "difference X, 95% CI Y to Z" format
# Let me revert my previous changes and use proper format

replacements = [
    # ULTRA - RD pattern (need "risk difference" keyword)
    ("RD -1.8%, 95% CI -5.5 to 1.9",
     "risk difference -1.8, 95% CI -5.5 to 1.9"),
    ("The difference was RD -1.8, 95% CI -5.5 to 1.9",  # revert my previous change
     "risk difference -1.8, 95% CI -5.5 to 1.9"),

    # ACORN - should be fine, check text

    # VITAMINS - MD pattern
    ("Mean difference MD -2.5, lower CI -18.1, upper CI 13.1",
     "mean difference -2.5, 95% CI -18.1 to 13.1"),
    ("MD -2.5, 95% CI -18.1 to 13.1",
     "mean difference -2.5, 95% CI -18.1 to 13.1"),

    # ESCAPE - MD pattern
    ("Difference MD 0.0, lower CI -4.3, upper CI 4.3",
     "mean difference 0.0, 95% CI -4.3 to 4.3"),

    # FOCUS - MD pattern
    ("Difference MD -2.7, lower CI -9.2, upper CI 3.8",
     "mean difference -2.7, 95% CI -9.2 to 3.8"),

    # TRANSFORM - RD pattern
    ("Difference RD -1.4, lower CI -5.8, upper CI 3.0",
     "risk difference -1.4, 95% CI -5.8 to 3.0"),
    ("RD -1.4%, 95% CI -5.8 to 3.0",
     "risk difference -1.4, 95% CI -5.8 to 3.0"),

    # SPACE - MD pattern
    ("Difference MD 0.1, lower CI -0.5, upper CI 0.7",
     "mean difference 0.1, 95% CI -0.5 to 0.7"),

    # POINT - MD pattern
    ("Difference MD 0.2, lower CI -0.4, upper CI 0.8",
     "mean difference 0.2, 95% CI -0.4 to 0.8"),

    # X-BOT - RD pattern
    ("Difference RD 8.0, lower CI 0.1, upper CI 15.9",
     "risk difference 8.0, 95% CI 0.1 to 15.9"),
    ("RD 8%, 95% CI 0.1 to 15.9",
     "risk difference 8.0, 95% CI 0.1 to 15.9"),

    # SIESTA - MD pattern
    ("Difference MD -2.7, lower CI -5.4, upper CI -0.1",
     "mean difference -2.7, 95% CI -5.4 to -0.1"),

    # HELIOS-A - MD pattern
    ("Difference MD -17.0, lower CI -22.3, upper CI -11.6",
     "mean difference -17.0, 95% CI -22.3 to -11.6"),

    # ESCAPE-TRD - MD pattern
    ("Difference MD -4.0, lower CI -7.3, upper CI -0.6",
     "mean difference -4.0, 95% CI -7.3 to -0.6"),

    # DELPHI - MD pattern
    ("Difference MD -3.9, lower CI -5.9, upper CI -1.9",
     "mean difference -3.9, 95% CI -5.9 to -1.9"),

    # REDS-III - RD pattern
    ("Difference RD 0.4, lower CI -0.7, upper CI 1.5",
     "risk difference 0.4, 95% CI -0.7 to 1.5"),
    ("RD 0.4%, 95% CI -0.7 to 1.5",
     "risk difference 0.4, 95% CI -0.7 to 1.5"),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"Fixed: {old[:40]}... -> {new[:40]}...")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nApplied {count} fixes to batch 9 trials")
