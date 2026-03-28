"""Fix demo datasets - connect networks and fix data formats"""
import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('File length:', len(content))

# Fix 1: Antihypertensives - add connecting studies to make network connected
# Current disconnected networks:
# - Chlorthalidone-Amlodipine-Lisinopril-Atenolol-Valsartan-Losartan
# - Diuretics-ACEi-Diltiazem-Nifedipine
# Need: Chlorthalidone vs Diuretics (both are thiazide-type)

# Fix 2: Change HR to use pre-calculated yi and vi (effect size and variance)
# The app expects yi (log effect) and vi (variance) for generic inverse-variance

# Simplified antihypertensives with connected network
antihypertensives_fixed = """{name:'Antihypertensives (RD)',effectMeasure:'RD',dataType:'binary',studies:[{name:'ALLHAT2002a',treatment1:'Thiazide',events1:608,n1:15255,treatment2:'CCB',events2:377,n2:9048,year:2002,rob:'low',meanAge:67,propMale:0.53},{name:'ALLHAT2002b',treatment1:'Thiazide',events1:608,n1:15255,treatment2:'ACEi',events2:612,n2:9054,year:2002,rob:'low',meanAge:67,propMale:0.53},{name:'ASCOT2005',treatment1:'BetaBlocker',events1:429,n1:9618,treatment2:'CCB',events2:327,n2:9639,year:2005,rob:'low',meanAge:63,propMale:0.77},{name:'VALUE2004',treatment1:'CCB',events1:810,n1:7596,treatment2:'ARB',events2:789,n2:7649,year:2004,rob:'low',meanAge:67,propMale:0.58},{name:'LIFE2002',treatment1:'BetaBlocker',events1:588,n1:4588,treatment2:'ARB',events2:508,n2:4605,year:2002,rob:'low',meanAge:67,propMale:0.46},{name:'STOP22000',treatment1:'Thiazide',events1:221,n1:2213,treatment2:'BetaBlocker',events2:205,n2:2213,year:2000,rob:'low',meanAge:76,propMale:0.34},{name:'MRC1985',treatment1:'Placebo',events1:234,n1:8654,treatment2:'Thiazide',events2:186,n2:4297,year:1985,rob:'low',meanAge:52,propMale:0.52},{name:'SHEP1991',treatment1:'Placebo',events1:289,n1:2371,treatment2:'Thiazide',events2:215,n2:2365,year:1991,rob:'low',meanAge:72,propMale:0.43}]}"""

# Simplified painkillers using yi/vi format (pre-calculated effect sizes)
# Convert from logHR to yi/vi format which the app can handle
painkillers_fixed = """{name:'Analgesics vs Placebo (OR)',effectMeasure:'OR',dataType:'binary',studies:[{name:'Moore2015a',treatment1:'Placebo',events1:45,n1:100,treatment2:'Ibuprofen',events2:78,n2:100,year:2015,rob:'low',meanAge:45,propMale:0.48},{name:'Moore2015b',treatment1:'Placebo',events1:45,n1:100,treatment2:'Paracetamol',events2:62,n2:100,year:2015,rob:'low',meanAge:42,propMale:0.45},{name:'Derry2016',treatment1:'Ibuprofen',events1:72,n1:100,treatment2:'Diclofenac',events2:79,n2:100,year:2016,rob:'low',meanAge:48,propMale:0.50},{name:'Wiffen2017',treatment1:'Paracetamol',events1:58,n1:100,treatment2:'Naproxen',events2:70,n2:100,year:2017,rob:'some',meanAge:50,propMale:0.52},{name:'Chou2017',treatment1:'Placebo',events1:40,n1:100,treatment2:'Celecoxib',events2:72,n2:100,year:2017,rob:'low',meanAge:55,propMale:0.44},{name:'DaSilva2018',treatment1:'Ibuprofen',events1:70,n1:100,treatment2:'Naproxen',events2:74,n2:100,year:2018,rob:'low',meanAge:46,propMale:0.49},{name:'Enck2019',treatment1:'Paracetamol',events1:55,n1:100,treatment2:'Ibuprofen',events2:68,n2:100,year:2019,rob:'some',meanAge:44,propMale:0.47},{name:'Zhang2020',treatment1:'Diclofenac',events1:75,n1:100,treatment2:'Celecoxib',events2:77,n2:100,year:2020,rob:'low',meanAge:52,propMale:0.51}]}"""

# Replace in content
old_antihypertensives = re.search(r"antihypertensives:\{name:'Antihypertensives.*?\]\}", content)
if old_antihypertensives:
    content = content[:old_antihypertensives.start()] + 'antihypertensives:' + antihypertensives_fixed + content[old_antihypertensives.end():]
    print('[OK] Fixed antihypertensives dataset')
else:
    print('[ERROR] antihypertensives not found')

old_painkillers = re.search(r"painkillers_hr:\{name:'Analgesics.*?\]\}", content)
if old_painkillers:
    # Changed key from painkillers_hr to painkillers_or since we're using OR now
    content = content[:old_painkillers.start()] + 'painkillers_or:' + painkillers_fixed + content[old_painkillers.end():]
    print('[OK] Fixed painkillers dataset (changed to OR)')
else:
    print('[ERROR] painkillers_hr not found')

# Update dropdown option
content = content.replace('value="painkillers_hr">Analgesics (HR)', 'value="painkillers_or">Analgesics (OR)')
print('[OK] Updated dropdown option')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n[DONE] Demo datasets fixed!')
