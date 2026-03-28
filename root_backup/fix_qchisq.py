# Add qchisq function to Stats and fix pauleMandel_CI jStat reference

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add qchisq function to Stats object (after pchisq)
old_pchisq = 'pchisq(x,df){if(x<=0)return 0;if(df>100){const z=Math.pow(x/df,1/3)-(1-2/(9*df));return Stats.pnorm(z/Math.sqrt(2/(9*df)))}return Stats.gammainc(df/2,x/2)},'

# Add qchisq using bisection method (inverse of pchisq)
qchisq_func = '''qchisq(p,df){if(p<=0)return 0;if(p>=1)return Infinity;let lo=0,hi=df*4;while(Stats.pchisq(hi,df)<p)hi*=2;for(let i=0;i<100;i++){const mid=(lo+hi)/2;if(Stats.pchisq(mid,df)<p)lo=mid;else hi=mid;if(Math.abs(hi-lo)<1e-8)break}return(lo+hi)/2},'''

new_pchisq = old_pchisq + '\n' + qchisq_func

if 'qchisq' not in content:
    content = content.replace(old_pchisq, new_pchisq)
    print("[OK] Added qchisq function to Stats")

# 2. Replace jStat.chisquare.inv with Stats.qchisq
old_jstat = 'jStat.chisquare.inv(1-alpha/2,df)'
new_jstat = 'Stats.qchisq(1-alpha/2,df)'
if old_jstat in content:
    content = content.replace(old_jstat, new_jstat)
    print("[OK] Replaced jStat.chisquare.inv(1-alpha/2) with Stats.qchisq")

old_jstat2 = 'jStat.chisquare.inv(alpha/2,df)'
new_jstat2 = 'Stats.qchisq(alpha/2,df)'
if old_jstat2 in content:
    content = content.replace(old_jstat2, new_jstat2)
    print("[OK] Replaced jStat.chisquare.inv(alpha/2) with Stats.qchisq")

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
    print("\n[SUCCESS] JavaScript syntax valid")
else:
    print("\n[ERROR]:")
    print(result.stderr[:500])
