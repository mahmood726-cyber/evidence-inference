# Fix extra } on line 2792 - should be just , not },

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern is: URL.revokeObjectURL(url)}\n},\ngenerateRValidationScript
# Should be: URL.revokeObjectURL(url)},\ngenerateRValidationScript

old = "URL.revokeObjectURL(url)}\n},\ngenerateRValidationScript"
new = "URL.revokeObjectURL(url)},\ngenerateRValidationScript"

if old in content:
    content = content.replace(old, new)
    print("[FIXED] Removed extra } before generateRValidationScript")
else:
    print("[INFO] Pattern not found - checking current state")
    # Check what's there
    idx = content.find("generateRValidationScript")
    if idx > 0:
        print(f"Before: ...{content[idx-30:idx]}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2788, min(2798, len(lines))):
    print(f"  Line {i+1}: {lines[i].rstrip()[:100]}")
