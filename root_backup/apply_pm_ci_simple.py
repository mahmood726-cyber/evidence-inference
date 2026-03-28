# Insert pauleMandel_CI - simple version (no display update)

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The method to insert
pm_ci = '''pauleMandel_CI(matrices,tau2Est,alpha=0.05){const{X,y,v,n,p}=matrices;const df=n-p;if(df<=0)return null;const calcQ=t2=>{const W=v.map(vi=>1/(vi+t2));const XtWX=Matrix.zeros(p,p),XtWy=Array(p).fill(0);for(let i=0;i<n;i++)for(let j=0;j<p;j++){XtWy[j]+=X[i][j]*W[i]*y[i];for(let k=0;k<p;k++)XtWX[j][k]+=X[i][j]*W[i]*X[i][k]}try{const beta=Matrix.solve(XtWX,XtWy);let Q=0;for(let i=0;i<n;i++){let f=0;for(let j=0;j<p;j++)f+=X[i][j]*beta[j];Q+=W[i]*(y[i]-f)**2}return Q}catch{return Infinity}};const chi2L=jStat.chisquare.inv(1-alpha/2,df),chi2U=jStat.chisquare.inv(alpha/2,df);const find=(tgt,lo,hi)=>{for(let i=0;i<100;i++){const m=(lo+hi)/2,Q=calcQ(m);if(Math.abs(Q-tgt)<0.0001)return m;if(Q>tgt)lo=m;else hi=m}return(lo+hi)/2};return{lower:Math.max(0,find(chi2L,0,tau2Est*10+1)),upper:find(chi2U,tau2Est,tau2Est*20+5),method:'Q-profile'}},'''

# Insert after profileLikelihoodCI
old_pattern = 'return{lower:Math.max(0,lower),upper}},\ncalcTreatmentEffects'
new_pattern = 'return{lower:Math.max(0,lower),upper}},\n' + pm_ci + '\ncalcTreatmentEffects'

if old_pattern in content and 'pauleMandel_CI' not in content:
    content = content.replace(old_pattern, new_pattern)
    print("[OK] Inserted pauleMandel_CI method")

# Add pmCI to return statement (simpler pattern)
old_return = 'tau2CI,treatments:'
new_return = 'tau2CI,pmCI:this.pauleMandel_CI(matrices,tau2Result.tau2),treatments:'
if old_return in content and 'pmCI:this' not in content:
    content = content.replace(old_return, new_return)
    print("[OK] Added pmCI to results")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
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
    print(result.stderr[:400])
