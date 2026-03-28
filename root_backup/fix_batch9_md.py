#!/usr/bin/env python3
"""Fix MD pattern trials - use 'mean difference' spelled out."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Convert "MD X.X, 95% CI X.X-Y.Y" to "mean difference X.X, 95% CI X.X to Y.Y"
replacements = [
    # ULTRA - also fix "from"
    ("RD -1.8, 95% CI from -5.5 to 1.9",
     "risk difference -1.8, 95% CI -5.5 to 1.9"),

    # ACORN
    ("MD 7.2, 95% CI 2.4-12.0",
     "mean difference 7.2, 95% CI 2.4 to 12.0"),

    # SYMPHONY
    ("MD 8.3, 95% CI 5.0-11.6",
     "mean difference 8.3, 95% CI 5.0 to 11.6"),

    # REST (Sleep Medicine)
    ("MD 0.6, 95% CI 0.3-0.9",
     "mean difference 0.6, 95% CI 0.3 to 0.9"),

    # LUXTURNA
    ("MD 1.6, 95% CI 1.0-2.2",
     "mean difference 1.6, 95% CI 1.0 to 2.2"),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"Fixed: {old} -> {new}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nApplied {count} MD fixes")
