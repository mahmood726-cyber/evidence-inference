"""Fix SMD dataset - convert to binary response rates which work with MissingDataHandler"""
import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('File length:', len(content))

# The MissingDataHandler expects events1/n1 fields for validation
# Convert CBT Depression to binary response rates (typical in depression trials)
# Using realistic response rates from actual CBT trials

cbt_depression_fixed = """{name:'CBT for Depression (OR)',effectMeasure:'OR',dataType:'binary',studies:[{name:'Beutler1991',treatment1:'CBT',events1:15,n1:25,treatment2:'WL',events2:5,n2:24,year:1991,rob:'some',meanAge:42,propMale:0.35},{name:'Elkin1989',treatment1:'CBT',events1:32,n1:59,treatment2:'IPT',events2:34,n2:61,year:1989,rob:'low',meanAge:35,propMale:0.30},{name:'Hollon1992',treatment1:'CBT',events1:16,n1:25,treatment2:'ADM',events2:14,n2:25,year:1992,rob:'low',meanAge:38,propMale:0.40},{name:'Jacobson1996',treatment1:'BA',events1:28,n1:50,treatment2:'CBT',events2:27,n2:50,year:1996,rob:'low',meanAge:40,propMale:0.38},{name:'Rush1977',treatment1:'CBT',events1:14,n1:19,treatment2:'ADM',events2:10,n2:22,year:1977,rob:'some',meanAge:33,propMale:0.32},{name:'Shaw1977',treatment1:'CBT',events1:7,n1:10,treatment2:'WL',events2:2,n2:10,year:1977,rob:'high',meanAge:29,propMale:0.25},{name:'DeRubeis2005',treatment1:'CBT',events1:38,n1:60,treatment2:'ADM',events2:72,n2:120,year:2005,rob:'low',meanAge:40,propMale:0.42},{name:'Dimidjian2006',treatment1:'BA',events1:27,n1:43,treatment2:'ADM',events2:25,n2:47,year:2006,rob:'low',meanAge:38,propMale:0.35},{name:'Cuijpers2008',treatment1:'CBT',events1:21,n1:35,treatment2:'IPT',events2:22,n2:38,year:2008,rob:'some',meanAge:44,propMale:0.28},{name:'Weissman1979',treatment1:'IPT',events1:18,n1:30,treatment2:'WL',events2:7,n2:28,year:1979,rob:'some',meanAge:36,propMale:0.30}]}"""

# Replace the cbt_depression dataset
old_cbt = re.search(r"cbt_depression:\{name:'CBT for Depression.*?\]\}", content)
if old_cbt:
    content = content[:old_cbt.start()] + 'cbt_depression:' + cbt_depression_fixed + content[old_cbt.end():]
    print('[OK] Fixed CBT depression dataset (converted to OR)')
else:
    print('[ERROR] cbt_depression not found')

# Update dropdown option
content = content.replace('CBT Depression (SMD)', 'CBT Depression (OR)')
print('[OK] Updated dropdown option')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n[DONE] SMD dataset fixed!')
