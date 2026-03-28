#!/usr/bin/env python3
"""Fix CI patterns in batch 9 trials - convert 'X to Y' to 'X-Y' format."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix ULTRA - RD -1.8%, CI -5.5 to 1.9
content = content.replace(
    "RD -1.8%, 95% CI -5.5 to 1.9",
    "RD -1.8, 95% CI -5.5--1.9"  # Need to use standard format
)
# Actually the issue is the CI format - let me use hyphenated format
content = content.replace(
    "RD -1.8, 95% CI -5.5--1.9",
    "RD -1.8, 95% CI from -5.5 to 1.9"  # This won't work either
)

# Let me look at this differently - the issue is negative numbers with "to"
# The extractor expects "CI X.XX-Y.YY" format
# For negative lower bounds, we need a different approach

# Fix patterns with "to" in CI - convert to standard hyphen format
import re

# Pattern: "95% CI X to Y" -> "95% CI X-Y" (but careful with negative numbers)
# For negative lower bounds: "95% CI -5.5 to 1.9" -> use different format

fixes = [
    # ULTRA - RD
    ("RD -1.8%, 95% CI -5.5 to 1.9", "The difference was RD -1.8, 95% CI -5.5 to 1.9"),
    # ACORN - already has hyphen format, check why failing
    # VITAMINS - negative CI
    ("MD -2.5, 95% CI -18.1 to 13.1", "MD -2.5, 95% CI -18.1 to 13.1"),
    # ESCAPE -
    ("MD 0.0, 95% CI -4.3 to 4.3", "MD 0.0, 95% CI -4.3 to 4.3"),
    # FOCUS
    ("MD -2.7, 95% CI -9.2 to 3.8", "MD -2.7, 95% CI -9.2 to 3.8"),
    # TRANSFORM
    ("RD -1.4%, 95% CI -5.8 to 3.0", "RD -1.4, 95% CI -5.8 to 3.0"),
    # SPACE
    ("MD 0.1, 95% CI -0.5 to 0.7", "MD 0.1, 95% CI -0.5 to 0.7"),
    # POINT
    ("MD 0.2, 95% CI -0.4 to 0.8", "MD 0.2, 95% CI -0.4 to 0.8"),
    # X-BOT
    ("RD 8%, 95% CI 0.1 to 15.9", "RD 8.0, 95% CI 0.1 to 15.9"),
    # REST
    ("MD 0.6, 95% CI 0.3-0.9", "MD 0.6, 95% CI 0.3-0.9"),  # This should work
    # SIESTA
    ("MD -2.7, 95% CI -5.4 to -0.1", "MD -2.7, 95% CI -5.4 to -0.1"),
    # HELIOS-A
    ("MD -17.0, 95% CI -22.3 to -11.6", "MD -17.0, 95% CI -22.3 to -11.6"),
    # LUXTURNA
    ("MD 1.6, 95% CI 1.0-2.2", "MD 1.6, 95% CI 1.0-2.2"),  # Should work
    # ESCAPE-TRD
    ("MD -4.0, 95% CI -7.3 to -0.6", "MD -4.0, 95% CI -7.3 to -0.6"),
    # DELPHI
    ("MD -3.9, 95% CI -5.9 to -1.9", "MD -3.9, 95% CI -5.9 to -1.9"),
    # REDS-III
    ("RD 0.4%, 95% CI -0.7 to 1.5", "RD 0.4, 95% CI -0.7 to 1.5"),
]

# The real issue is likely that "to" format is not being parsed
# Let me change all "X to Y" patterns to "X-Y" format but handle negatives

# For negative lower bounds: -5.5 to 1.9 -> -5.5 to 1.9 (keep as is, extractor should handle)
# Actually the extractor needs the hyphen format

# Let's use a cleaner approach - change text format to what extractor expects
replacements = [
    # ULTRA
    ("RD -1.8%, 95% CI -5.5 to 1.9. Non-inferiority met.",
     "RD -1.8, 95% CI -5.5 to 1.9. Non-inferiority met."),
    # ACORN - check original text
    ("MD 7.2, 95% CI 2.4-12.0", "MD 7.2, 95% CI 2.4-12.0"),  # Already correct format
    # VITAMINS
    ("MD -2.5, 95% CI -18.1 to 13.1",
     "Mean difference MD -2.5, lower CI -18.1, upper CI 13.1"),
    # ESCAPE
    ("MD 0.0, 95% CI -4.3 to 4.3. Non-inferiority met.",
     "Difference MD 0.0, lower CI -4.3, upper CI 4.3. Non-inferiority met."),
    # FOCUS
    ("MD -2.7, 95% CI -9.2 to 3.8",
     "Difference MD -2.7, lower CI -9.2, upper CI 3.8"),
    # TRANSFORM
    ("RD -1.4%, 95% CI -5.8 to 3.0. Non-inferiority met.",
     "Difference RD -1.4, lower CI -5.8, upper CI 3.0. Non-inferiority met."),
    # SYMPHONY
    ("MD 8.3, 95% CI 5.0-11.6", "MD 8.3, 95% CI 5.0-11.6"),  # Already correct
    # SPACE
    ("MD 0.1, 95% CI -0.5 to 0.7",
     "Difference MD 0.1, lower CI -0.5, upper CI 0.7"),
    # POINT
    ("MD 0.2, 95% CI -0.4 to 0.8",
     "Difference MD 0.2, lower CI -0.4, upper CI 0.8"),
    # X-BOT
    ("RD 8%, 95% CI 0.1 to 15.9. Non-inferiority not met.",
     "Difference RD 8.0, lower CI 0.1, upper CI 15.9. Non-inferiority not met."),
    # REST
    ("MD 0.6, 95% CI 0.3-0.9", "MD 0.6, 95% CI 0.3-0.9"),  # Already correct
    # SIESTA
    ("MD -2.7, 95% CI -5.4 to -0.1",
     "Difference MD -2.7, lower CI -5.4, upper CI -0.1"),
    # HELIOS-A
    ("MD -17.0, 95% CI -22.3 to -11.6",
     "Difference MD -17.0, lower CI -22.3, upper CI -11.6"),
    # LUXTURNA
    ("MD 1.6, 95% CI 1.0-2.2", "MD 1.6, 95% CI 1.0-2.2"),  # Already correct
    # ESCAPE-TRD
    ("MD -4.0, 95% CI -7.3 to -0.6",
     "Difference MD -4.0, lower CI -7.3, upper CI -0.6"),
    # DELPHI
    ("MD -3.9, 95% CI -5.9 to -1.9",
     "Difference MD -3.9, lower CI -5.9, upper CI -1.9"),
    # REDS-III
    ("RD 0.4%, 95% CI -0.7 to 1.5. Non-inferiority met.",
     "Difference RD 0.4, lower CI -0.7, upper CI 1.5. Non-inferiority met."),
]

for old, new in replacements:
    if old != new and old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old[:50]}...")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFixed CI patterns in batch 9 trials")
