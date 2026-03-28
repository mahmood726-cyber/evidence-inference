# Add edge weights to network plots

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add edge weight annotations to network plot
# Find the edgeTrace definition
old_edge = "const edgeTrace={type:'scatter',mode:'lines',x:edgeX,y:edgeY,line:{color:colors.edge,width:2},hoverinfo:'skip'}"

new_edge = '''/* Edge annotations */
const edgeAnno=[];
edgeMap.forEach((cnt,k)=>{const[t1,t2]=k.split('|'),i1=treatments.indexOf(t1),i2=treatments.indexOf(t2);if(i1>=0&&i2>=0){const mx=(nodeX[i1]+nodeX[i2])/2,my=(nodeY[i1]+nodeY[i2])/2;edgeAnno.push({x:mx,y:my,text:String(cnt),showarrow:false,font:{size:10,color:colors.textSecondary},bgcolor:colors.background})}});
const edgeTrace={type:'scatter',mode:'lines',x:edgeX,y:edgeY,line:{color:colors.edge,width:2},hoverinfo:'skip'}'''

if old_edge in content and 'edgeAnno' not in content:
    content = content.replace(old_edge, new_edge)
    print("[OK] Added edge annotation calculations")

# Add annotations to layout
old_margin = "margin:{l:20,r:20,t:20,b:20},showlegend:false"
new_margin = "margin:{l:20,r:20,t:20,b:20},showlegend:false,annotations:edgeAnno||[]"
if old_margin in content and 'edgeAnno' in content:
    content = content.replace(old_margin, new_margin)
    print("[OK] Added edge annotations to plot layout")

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
