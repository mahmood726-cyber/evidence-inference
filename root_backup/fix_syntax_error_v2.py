# Fix JavaScript syntax error - missing closing brace for analyze function

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The analyze function return statement needs a }, at the end before pauleMandel_CI starts
old_pattern = "processed,matrices}\n\npauleMandel_CI"
new_pattern = "processed,matrices}\n},\npauleMandel_CI"

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print("[FIXED] Added missing }, to close analyze function")
else:
    # Try alternate pattern
    old_pattern2 = "processed,matrices}\npauleMandel_CI"
    new_pattern2 = "processed,matrices}\n},\npauleMandel_CI"
    if old_pattern2 in content:
        content = content.replace(old_pattern2, new_pattern2)
        print("[FIXED] Added missing }, to close analyze function (alt)")
    else:
        print("[INFO] Pattern not found - checking current structure")
        # Check what's actually there
        idx = content.find("pauleMandel_CI")
        if idx > 0:
            before = content[max(0,idx-100):idx]
            print(f"Before pauleMandel_CI: ...{before[-50:]}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nVerifying fix...")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check around line 262-265
for i in range(max(0, 260), min(len(lines), 270)):
    print(f"  Line {i+1}: {lines[i].rstrip()[:100]}")

print("\n[DONE] Fix attempt complete")
