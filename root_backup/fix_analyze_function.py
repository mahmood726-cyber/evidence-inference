# Fix analyze function - missing closing brace before checkConnectivity
# Pattern: return{...validCount},checkConnectivity
# Should be: return{...validCount}},checkConnectivity

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern is: validCount},\ncheckConnectivity
# Should be: validCount}},\ncheckConnectivity

old = "geometryMetrics,validCount},\ncheckConnectivity"
new = "geometryMetrics,validCount}},\ncheckConnectivity"

if old in content:
    content = content.replace(old, new)
    print("[FIXED] Added closing } for analyze function")
else:
    # Try to find the pattern
    idx = content.find("checkConnectivity")
    if idx > 0:
        before = content[max(0,idx-50):idx]
        print(f"Before checkConnectivity: ...{before}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Test
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''
with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("\n[OK] JavaScript syntax is now valid!")
else:
    print(f"\n[NEXT ERROR]:")
    print(result.stderr[:500])
