# Comprehensive fix for all missing }, separators between object methods

import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# Pattern: } followed by newline(s) then a method definition without comma
# Look for: }\n\nmethodName(  or  }\nmethodName(

# Fix 1: Line 2791-2792 - missing }, before generateRValidationScript
old1 = "URL.revokeObjectURL(url)}\n\ngenerateRValidationScript(){"
new1 = "URL.revokeObjectURL(url)}\n},\ngenerateRValidationScript(){"
if old1 in content:
    content = content.replace(old1, new1)
    changes.append("Fixed missing }, before generateRValidationScript")

# Fix 2: Check for generateBayesianRScript - same issue likely
old2 = "return script\n},\n\ngenerateBayesianRScript(){"
new2_check = "return script\n},\ngenerateBayesianRScript(){"  # Already has },
if old2 in content:
    content = content.replace(old2, new2_check)
    changes.append("Fixed generateBayesianRScript separator")

# Check for pattern: }\n\nfunctionName() without comma
patterns_to_fix = [
    (r'\}\n\n(generateRValidationScript\(\)\{)', r'},\n\1'),
    (r'\}\n\n(generateBayesianRScript\(\)\{)', r'},\n\1'),
    (r'\}\n(generateRValidationScript\(\)\{)', r'},\n\1'),
    (r'\}\n(generateBayesianRScript\(\)\{)', r'},\n\1'),
]

for pattern, replacement in patterns_to_fix:
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        changes.append(f"Applied regex fix for pattern: {pattern[:30]}...")

# Also check that all places have proper }, separators
# Find all occurrences of }followed by newline and then a function/method name
import_pattern = re.compile(r'\}\n+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
matches = import_pattern.finditer(content)
potential_issues = []
for m in matches:
    # Check if the previous character before } is not a comma
    start = m.start()
    # Check 10 chars before
    before = content[max(0, start-5):start+1]
    if not before.strip().endswith('},'):
        func_name = m.group(1)
        # Get line number
        line_num = content[:start].count('\n') + 1
        potential_issues.append(f"Line {line_num}: {func_name}")

if potential_issues:
    print("Potential remaining issues (functions without preceding ,}):")
    for issue in potential_issues[:10]:  # Show first 10
        print(f"  {issue}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 60)
print("COMPREHENSIVE SYNTAX FIX")
print("=" * 60)
for c in changes:
    print(f"  [FIXED] {c}")
if not changes:
    print("  [INFO] No changes needed or patterns not found")
print("=" * 60)
