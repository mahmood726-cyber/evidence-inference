# Add gemtc R button to Bayesian panel

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if already added
if 'gemtc R</button>' in content:
    print("[INFO] gemtc R button already exists")
else:
    # Find the Run Bayesian button and add after it
    old = 'id="runBayesianBtn">Run Bayesian</button></div></div><div class="card__body" id="bayesianContainer">'
    gemtc_btn = '''<button class="btn btn--sm btn--ghost" onclick="const s=generateBayesianRScript();if(!s){alert('Run Bayesian analysis first');return}const b=new Blob([s],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='nma_bayesian_gemtc.R';a.click()" title="Export gemtc R validation script">gemtc R</button>'''

    new = f'id="runBayesianBtn">Run Bayesian</button>{gemtc_btn}</div></div><div class="card__body" id="bayesianContainer">'

    if old in content:
        content = content.replace(old, new)
        print("[OK] Added gemtc R export button")
    else:
        print("[WARN] Pattern not found")
        # Try alternative pattern
        old2 = 'id="runBayesianBtn">Run Bayesian</button>'
        new2 = f'id="runBayesianBtn">Run Bayesian</button>{gemtc_btn}'
        if old2 in content:
            content = content.replace(old2, new2, 1)
            print("[OK] Added gemtc R export button (alt pattern)")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''
with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("[SUCCESS] JavaScript syntax valid")
else:
    print("[ERROR]:", result.stderr[:300])
