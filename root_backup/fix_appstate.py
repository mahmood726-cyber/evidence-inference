# Fix AppState - missing closing brace
# The wasm object closes, then AppState needs to close

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern: new Map(),_nextId:0}; should be new Map(),_nextId:0}};
old = "_pending:new Map(),_nextId:0};"
new = "_pending:new Map(),_nextId:0}};"

if old in content:
    content = content.replace(old, new)
    print("[FIXED] Added missing } to close AppState")
else:
    # Check what's there
    idx = content.find("_nextId:0")
    if idx > 0:
        around = content[idx:idx+30]
        print(f"Current pattern: {repr(around)}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
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
    # Show first error
    lines = result.stderr.split('\n')
    print(f"\n[ERROR] Next syntax error:")
    for line in lines[:10]:
        print(line[:150])
