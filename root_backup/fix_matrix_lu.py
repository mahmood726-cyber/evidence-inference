# Fix missing } in Matrix.lu method
# The pattern }}return{L,U,P}, should be }}}return{L,U,P}},

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The broken pattern (missing one } before return)
old = "U[i][j]-=L[i][k]*U[k][j]}}return{L,U,P},"
new = "U[i][j]-=L[i][k]*U[k][j]}}}return{L,U,P}},"

if old in content:
    content = content.replace(old, new)
    print("[FIXED] Restored missing } in Matrix.lu method")
else:
    print("[INFO] Pattern not found - checking variants")
    # Try to find what's there
    idx = content.find("return{L,U,P}")
    if idx > 0:
        around = content[max(0, idx-30):idx+30]
        print(f"Found around return: {repr(around)}")

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
