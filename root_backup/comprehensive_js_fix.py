# Comprehensive fix for NMA Pro JavaScript structure
# The issue is malformed method definitions from previous edits

import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 70)
print("COMPREHENSIVE JAVASCRIPT FIX")
print("=" * 70)

# Find the problematic area - around generateRValidationScript
idx_val = content.find('generateRValidationScript')
idx_bayes = content.find('generateBayesianRScript')

print(f"generateRValidationScript at position: {idx_val}")
print(f"generateBayesianRScript at position: {idx_bayes}")

# Check context before generateRValidationScript
if idx_val > 0:
    before = content[max(0, idx_val-200):idx_val]
    print(f"\n50 chars before generateRValidationScript:")
    print(repr(before[-50:]))

# The pattern should be:
#   ...code...},
#   generateRValidationScript(){
#
# But we might have malformed patterns like:
#   ...code...},},  (extra brace)
#   ...code...}},   (extra brace)
#   ...code...}     (missing comma)

# Fix pattern 1: Ensure proper }, before generateRValidationScript
# Pattern: something}[whitespace]generateRValidationScript should be something},[newline]generateRValidationScript

patterns = [
    # Fix: }[newline]generateRValidationScript -> },[newline]generateRValidationScript
    (r'\}\n(generateRValidationScript\(\))', r'},\n\1'),
    (r'\}\n\n(generateRValidationScript\(\))', r'},\n\1'),

    # Fix: },[newline]generateRValidationScript - already correct, don't change

    # Fix: }[newline]generateBayesianRScript -> },[newline]generateBayesianRScript
    (r'\}\n(generateBayesianRScript\(\))', r'},\n\1'),
    (r'\}\n\n(generateBayesianRScript\(\))', r'},\n\1'),

    # Fix: },[newline]}, - extra closing brace
    (r'\},\n\},\n(generate[A-Za-z]+Script)', r'},\n\1'),

    # Fix: }},[\n] - consecutive closing
    (r'\}\},', r'},'),
]

changes = []
for pattern, replacement in patterns:
    if re.search(pattern, content):
        old_len = len(content)
        content = re.sub(pattern, replacement, content)
        if len(content) != old_len:
            changes.append(f"Applied: {pattern[:40]}...")

# Check and fix any remaining issues
# The key structure should be:
#   methodName() { ...body... },
#   nextMethodName() { ...body... },

# Make sure generateRValidationScript is properly formatted
# Check what's immediately before it
idx_val2 = content.find('generateRValidationScript(){')
if idx_val2 > 0:
    before_char = content[idx_val2-1:idx_val2]
    print(f"\nChar before generateRValidationScript: {repr(before_char)}")
    if before_char == '\n':
        # Check the line before
        line_before = content[:idx_val2].split('\n')[-2] if '\n' in content[:idx_val2] else ''
        print(f"Line before: {repr(line_before[-50:])}")

        if not line_before.rstrip().endswith(','):
            # Need to add comma
            idx_line_end = content[:idx_val2].rfind('\n')
            idx_prev_line_end = content[:idx_line_end].rfind('\n')
            line = content[idx_prev_line_end+1:idx_line_end]
            if line.rstrip().endswith('}'):
                # Add comma after the }
                fixed_line = line.rstrip() + ','
                content = content[:idx_prev_line_end+1] + fixed_line + content[idx_line_end:]
                changes.append("Added comma after } before generateRValidationScript")

# Same check for generateBayesianRScript
idx_bayes2 = content.find('generateBayesianRScript(){')
if idx_bayes2 > 0 and idx_bayes2 != -1:
    before_char = content[idx_bayes2-1:idx_bayes2]
    print(f"\nChar before generateBayesianRScript: {repr(before_char)}")
    if before_char == '\n':
        line_before = content[:idx_bayes2].split('\n')[-2] if '\n' in content[:idx_bayes2] else ''
        print(f"Line before: {repr(line_before[-50:])}")

        if not line_before.rstrip().endswith(','):
            idx_line_end = content[:idx_bayes2].rfind('\n')
            idx_prev_line_end = content[:idx_line_end].rfind('\n')
            line = content[idx_prev_line_end+1:idx_line_end]
            if line.rstrip().endswith('}'):
                fixed_line = line.rstrip() + ','
                content = content[:idx_prev_line_end+1] + fixed_line + content[idx_line_end:]
                changes.append("Added comma after } before generateBayesianRScript")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nChanges applied: {len(changes)}")
for c in changes:
    print(f"  - {c}")

# Verify structure
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("\nVerifying around generateRValidationScript:")
idx_line = None
for i, line in enumerate(lines):
    if 'generateRValidationScript' in line:
        idx_line = i
        break

if idx_line:
    for i in range(max(0, idx_line-3), min(len(lines), idx_line+3)):
        print(f"  {i+1}: {lines[i].rstrip()[:80]}")

print("\n" + "=" * 70)
