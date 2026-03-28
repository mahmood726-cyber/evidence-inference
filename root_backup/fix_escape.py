#!/usr/bin/env python3
"""Fix ESCAPE trial - MD 0.0 extraction issue."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The issue is extracting 0.0 - let's try different format
old = "Function score difference mean difference 0.0, 95% CI -4.3 to 4.3"
new = "Function score: mean difference 0.00, 95% CI -4.3 to 4.3"

if old in content:
    content = content.replace(old, new)
    print(f"Fixed ESCAPE: {old[:40]}... -> {new[:40]}...")
else:
    print("ESCAPE pattern not found, checking...")
    # Try original pattern
    old2 = "MD 0.0, 95% CI -4.3 to 4.3"
    if old2 in content:
        content = content.replace(old2, "mean difference 0.00, 95% CI -4.3 to 4.3")
        print(f"Fixed alternative pattern")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
