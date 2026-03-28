# Fix Matrix.lu - restore correct brace count

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Current (over-corrected): }}}return{L,U,P}},
# Correct should be: }}}return{L,U,P},

old = "U[i][j]-=L[i][k]*U[k][j]}}}return{L,U,P}},"
new = "U[i][j]-=L[i][k]*U[k][j]}}}return{L,U,P},"

if old in content:
    content = content.replace(old, new)
    print("[FIXED] Corrected Matrix.lu closing braces")
else:
    print("[INFO] Pattern not found")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

lu_line = lines[139]
opens = lu_line.count('{')
closes = lu_line.count('}')
print(f"\nAfter fix - Opening braces: {opens}, Closing braces: {closes}")
print(f"Balance: {opens - closes} (should be 0)")

if opens != closes:
    print(f"\nWARNING: Brace imbalance detected!")
