# Fix JavaScript syntax error in NMA Pro v6.2
# Line 317 has },}, which should be },

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the double },},
old_pattern = "return { lower: tau2Lower, upper: tau2Upper, method: 'Q-profile (PM)' };\n},},"
new_pattern = "return { lower: tau2Lower, upper: tau2Upper, method: 'Q-profile (PM)' };\n},"

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print("[FIXED] Removed extra }, after pauleMandel_CI function")
else:
    # Try alternate pattern matching
    if '},},' in content:
        # Find and fix all occurrences of },},
        count = content.count('},},')
        content = content.replace('},},', '},')
        print(f"[FIXED] Replaced {count} occurrences of '}},}},' with '}},'")
    else:
        print("[INFO] Pattern not found - may already be fixed")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nVerifying fix...")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check around line 317
for i in range(max(0, 314), min(len(lines), 322)):
    print(f"  Line {i+1}: {lines[i].rstrip()[:80]}")

print("\n[DONE] Syntax error fix complete")
