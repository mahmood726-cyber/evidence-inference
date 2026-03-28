# Fix Matrix.lu - return is outside function due to extra }
# Current: }}}return{L,U,P},  (return outside function)
# Should be: }}return{L,U,P}},  (return inside function)

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern: }}}return should be }}return
old = "U[i][j]-=L[i][k]*U[k][j]}}}return{L,U,P},"
new = "U[i][j]-=L[i][k]*U[k][j]}}return{L,U,P}},"

if old in content:
    content = content.replace(old, new)
    print("[FIXED] Moved return statement inside lu function")
else:
    # Check what's there
    idx = content.find("return{L,U,P}")
    if idx > 0:
        before = content[max(0,idx-30):idx+20]
        print(f"Current pattern: {repr(before)}")
    else:
        print("return{L,U,P} not found")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify with node
import subprocess
import re

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''

with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("\n[OK] JavaScript syntax is valid!")
else:
    print(f"\n[ERROR] Syntax still invalid:")
    print(result.stderr[:500])
