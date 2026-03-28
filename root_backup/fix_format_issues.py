#!/usr/bin/env python3
"""Fix format issues in 3000 trials."""

import re

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

fixes_made = 0

# Fix 1: Convert "CI X.XX to X.XX" to "CI X.XX-X.XX"
old_ci_pattern = r'(95% CI )([\d.-]+) to ([\d.-]+)'
content, count = re.subn(old_ci_pattern, r'\1\2-\3', content)
if count > 0:
    print(f"Fixed {count} 'CI X to Y' patterns")
    fixes_made += count

# Fix 2: Convert "CI: X.XX-X.XX" to "CI X.XX-X.XX"
old_ci_pattern2 = r'95% CI:\s*([\d.-]+)-([\d.-]+)'
content, count = re.subn(old_ci_pattern2, r'95% CI \1-\2', content)
if count > 0:
    print(f"Fixed {count} 'CI: X-Y' patterns")
    fixes_made += count

# Fix 3: Fix missing 95% CI prefix
no_ci_pattern = r'(\bHR|\bRR|\bOR|\bMD) ([\d.]+), ([\d.-]+)-([\d.-]+)'
def add_ci_prefix(m):
    return f"{m.group(1)} {m.group(2)}, 95% CI {m.group(3)}-{m.group(4)}"
content, count = re.subn(no_ci_pattern, add_ci_prefix, content)
if count > 0:
    print(f"Fixed {count} missing CI prefix patterns")
    fixes_made += count

# Fix 4: Fix "mean difference X.X, CI X.X-X.X" to "mean difference X.X, 95% CI X.X-X.X"
md_pattern = r'(mean difference [\d.-]+), CI ([\d.-]+)-([\d.-]+)'
content, count = re.subn(md_pattern, r'\1, 95% CI \2-\3', content)
if count > 0:
    print(f"Fixed {count} 'mean difference, CI' patterns")
    fixes_made += count

# Fix 5: Ensure proper arm notation "(treatment arm, n=X)"
# Some trials may have "treatment arm (n=X)" - fix this
arm_pattern1 = r'treatment arm \(n=(\d+)\)'
content, count = re.subn(arm_pattern1, r'(treatment arm, n=\1)', content)
if count > 0:
    print(f"Fixed {count} 'treatment arm (n=X)' patterns")
    fixes_made += count

arm_pattern2 = r'control arm \(n=(\d+)\)'
content, count = re.subn(arm_pattern2, r'(control arm, n=\1)', content)
if count > 0:
    print(f"Fixed {count} 'control arm (n=X)' patterns")
    fixes_made += count

# Fix 6: Add NCT prefix where missing
nct_pattern = r"registration:\s*'(\d{8})'"
def add_nct(m):
    return f"registration: 'NCT{m.group(1)}'"
content, count = re.subn(nct_pattern, add_nct, content)
if count > 0:
    print(f"Fixed {count} missing NCT prefix patterns")
    fixes_made += count

# Fix 7: Fix trials with treatment (n=X) instead of (treatment arm, n=X)
text_arm_pattern1 = r'randomized to ([a-zA-Z-]+) \(n=(\d+)\) versus'
def fix_arm_format(m):
    return f"randomized to {m.group(1)} (treatment arm, n={m.group(2)}) versus"
content, count = re.subn(text_arm_pattern1, fix_arm_format, content)
if count > 0:
    print(f"Fixed {count} 'drug (n=X) versus' patterns")
    fixes_made += count

text_arm_pattern2 = r'versus ([a-zA-Z ]+) \(n=(\d+)\)\.'
def fix_control_format(m):
    ctrl = m.group(1).strip()
    return f"versus {ctrl} (control arm, n={m.group(2)})."
content, count = re.subn(text_arm_pattern2, fix_control_format, content)
if count > 0:
    print(f"Fixed {count} 'versus X (n=X)' patterns")
    fixes_made += count

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal fixes made: {fixes_made}")

# Re-validate
matches = re.findall(r"id:\s*'[^']+'", content)
print(f"Trial count: {len(matches)}")
