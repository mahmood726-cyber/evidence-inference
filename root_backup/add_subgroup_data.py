"""Add subgroup and year data to demo datasets"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add subgroup to each study in thrombolytics
replacements = [
    # Thrombolytics
    ("{name:'Coll1988',treatment1:'SK',treatment2:'tPA',events1:8,n1:54,events2:4,n2:56}",
     "{name:'Coll1988',treatment1:'SK',treatment2:'tPA',events1:8,n1:54,events2:4,n2:56,subgroup:'Europe',year:1988}"),
    ("{name:'DeWood1990',treatment1:'SK',treatment2:'tPA',events1:6,n1:63,events2:4,n2:62}",
     "{name:'DeWood1990',treatment1:'SK',treatment2:'tPA',events1:6,n1:63,events2:4,n2:62,subgroup:'Americas',year:1990}"),
    ("{name:'GISSI-2',treatment1:'SK',treatment2:'tPA',events1:887,n1:10396,events2:1017,n2:10372}",
     "{name:'GISSI-2',treatment1:'SK',treatment2:'tPA',events1:887,n1:10396,events2:1017,n2:10372,subgroup:'Europe',year:1990}"),
    ("{name:'Guerci1987',treatment1:'SK',treatment2:'tPA',events1:2,n1:61,events2:3,n2:77}",
     "{name:'Guerci1987',treatment1:'SK',treatment2:'tPA',events1:2,n1:61,events2:3,n2:77,subgroup:'Americas',year:1987}"),
    ("{name:'ISIS-3',treatment1:'SK',treatment2:'tPA',events1:1455,n1:13780,events2:1418,n2:13773}",
     "{name:'ISIS-3',treatment1:'SK',treatment2:'tPA',events1:1455,n1:13780,events2:1418,n2:13773,subgroup:'International',year:1992}"),
    ("{name:'TIMI-I',treatment1:'SK',treatment2:'tPA',events1:3,n1:143,events2:2,n2:147}",
     "{name:'TIMI-I',treatment1:'SK',treatment2:'tPA',events1:3,n1:143,events2:2,n2:147,subgroup:'Americas',year:1985}"),
    ("{name:'ASSET',treatment1:'Placebo',treatment2:'tPA',events1:182,n1:2495,events2:118,n2:2516}",
     "{name:'ASSET',treatment1:'Placebo',treatment2:'tPA',events1:182,n1:2495,events2:118,n2:2516,subgroup:'Europe',year:1988}"),
    ("{name:'LATE',treatment1:'Placebo',treatment2:'tPA',events1:284,n1:2682,events2:256,n2:2686}",
     "{name:'LATE',treatment1:'Placebo',treatment2:'tPA',events1:284,n1:2682,events2:256,n2:2686,subgroup:'International',year:1993}"),
    ("{name:'EMERAS',treatment1:'Placebo',treatment2:'SK',events1:144,n1:2257,events2:149,n2:2253}",
     "{name:'EMERAS',treatment1:'Placebo',treatment2:'SK',events1:144,n1:2257,events2:149,n2:2253,subgroup:'Americas',year:1993}"),
    ("{name:'GISSI-1',treatment1:'Placebo',treatment2:'SK',events1:758,n1:5860,events2:628,n2:5852}",
     "{name:'GISSI-1',treatment1:'Placebo',treatment2:'SK',events1:758,n1:5860,events2:628,n2:5852,subgroup:'Europe',year:1986}"),
    ("{name:'ISAM',treatment1:'Placebo',treatment2:'SK',events1:63,n1:882,events2:46,n2:859}",
     "{name:'ISAM',treatment1:'Placebo',treatment2:'SK',events1:63,n1:882,events2:46,n2:859,subgroup:'Europe',year:1986}"),
    ("{name:'ISIS-2',treatment1:'Placebo',treatment2:'SK',events1:568,n1:4300,events2:461,n2:4292}",
     "{name:'ISIS-2',treatment1:'Placebo',treatment2:'SK',events1:568,n1:4300,events2:461,n2:4292,subgroup:'International',year:1988}"),
    # Vaccines
    ("{name:'Study1',treatment1:'Placebo',treatment2:'VaccineA',events1:50,n1:500,events2:20,n2:500}",
     "{name:'Study1',treatment1:'Placebo',treatment2:'VaccineA',events1:50,n1:500,events2:20,n2:500,subgroup:'Developed',year:2015}"),
    ("{name:'Study2',treatment1:'Placebo',treatment2:'VaccineB',events1:45,n1:450,events2:25,n2:460}",
     "{name:'Study2',treatment1:'Placebo',treatment2:'VaccineB',events1:45,n1:450,events2:25,n2:460,subgroup:'Developing',year:2016}"),
    ("{name:'Study3',treatment1:'VaccineA',treatment2:'VaccineB',events1:22,n1:400,events2:18,n2:420}",
     "{name:'Study3',treatment1:'VaccineA',treatment2:'VaccineB',events1:22,n1:400,events2:18,n2:420,subgroup:'Developed',year:2017}"),
    ("{name:'Study4',treatment1:'Placebo',treatment2:'VaccineA',events1:60,n1:600,events2:30,n2:590}",
     "{name:'Study4',treatment1:'Placebo',treatment2:'VaccineA',events1:60,n1:600,events2:30,n2:590,subgroup:'Developing',year:2018}"),
    ("{name:'Study5',treatment1:'VaccineA',treatment2:'VaccineB',events1:28,n1:380,events2:24,n2:390}",
     "{name:'Study5',treatment1:'VaccineA',treatment2:'VaccineB',events1:28,n1:380,events2:24,n2:390,subgroup:'Developed',year:2019}"),
    # Antihypertensives
    ("{name:'Trial1',treatment1:'Placebo',treatment2:'ACEi',events1:120,n1:1000,events2:85,n2:1020}",
     "{name:'Trial1',treatment1:'Placebo',treatment2:'ACEi',events1:120,n1:1000,events2:85,n2:1020,subgroup:'HighRisk',year:2010}"),
    ("{name:'Trial2',treatment1:'Placebo',treatment2:'ARB',events1:115,n1:980,events2:90,n2:990}",
     "{name:'Trial2',treatment1:'Placebo',treatment2:'ARB',events1:115,n1:980,events2:90,n2:990,subgroup:'LowRisk',year:2011}"),
    ("{name:'Trial3',treatment1:'ACEi',treatment2:'ARB',events1:88,n1:850,events2:82,n2:860}",
     "{name:'Trial3',treatment1:'ACEi',treatment2:'ARB',events1:88,n1:850,events2:82,n2:860,subgroup:'HighRisk',year:2012}"),
    ("{name:'Trial4',treatment1:'Placebo',treatment2:'CCB',events1:130,n1:1100,events2:100,n2:1080}",
     "{name:'Trial4',treatment1:'Placebo',treatment2:'CCB',events1:130,n1:1100,events2:100,n2:1080,subgroup:'LowRisk',year:2013}"),
    ("{name:'Trial5',treatment1:'ACEi',treatment2:'CCB',events1:78,n1:920,events2:72,n2:910}",
     "{name:'Trial5',treatment1:'ACEi',treatment2:'CCB',events1:78,n1:920,events2:72,n2:910,subgroup:'HighRisk',year:2014}"),
    ("{name:'Trial6',treatment1:'ARB',treatment2:'CCB',events1:75,n1:880,events2:70,n2:870}",
     "{name:'Trial6',treatment1:'ARB',treatment2:'CCB',events1:75,n1:880,events2:70,n2:870,subgroup:'LowRisk',year:2015}"),
    # Painkillers
    ("{name:'Pain1',treatment1:'Placebo',treatment2:'NSAID1',events1:80,n1:200,events2:40,n2:210}",
     "{name:'Pain1',treatment1:'Placebo',treatment2:'NSAID1',events1:80,n1:200,events2:40,n2:210,subgroup:'Acute',year:2018}"),
    ("{name:'Pain2',treatment1:'Placebo',treatment2:'NSAID2',events1:75,n1:190,events2:35,n2:200}",
     "{name:'Pain2',treatment1:'Placebo',treatment2:'NSAID2',events1:75,n1:190,events2:35,n2:200,subgroup:'Chronic',year:2019}"),
    ("{name:'Pain3',treatment1:'NSAID1',treatment2:'NSAID2',events1:45,n1:180,events2:42,n2:185}",
     "{name:'Pain3',treatment1:'NSAID1',treatment2:'NSAID2',events1:45,n1:180,events2:42,n2:185,subgroup:'Acute',year:2020}"),
    ("{name:'Pain4',treatment1:'Placebo',treatment2:'Opioid',events1:90,n1:220,events2:30,n2:215}",
     "{name:'Pain4',treatment1:'Placebo',treatment2:'Opioid',events1:90,n1:220,events2:30,n2:215,subgroup:'Chronic',year:2021}"),
    ("{name:'Pain5',treatment1:'NSAID1',treatment2:'Opioid',events1:38,n1:175,events2:28,n2:180}",
     "{name:'Pain5',treatment1:'NSAID1',treatment2:'Opioid',events1:38,n1:175,events2:28,n2:180,subgroup:'Acute',year:2022}"),
    # CBT Depression
    ("{name:'CBT1',treatment1:'TAU',treatment2:'CBT',events1:60,n1:150,events2:40,n2:155}",
     "{name:'CBT1',treatment1:'TAU',treatment2:'CBT',events1:60,n1:150,events2:40,n2:155,subgroup:'Mild',year:2015}"),
    ("{name:'CBT2',treatment1:'TAU',treatment2:'IPT',events1:58,n1:145,events2:38,n2:150}",
     "{name:'CBT2',treatment1:'TAU',treatment2:'IPT',events1:58,n1:145,events2:38,n2:150,subgroup:'Moderate',year:2016}"),
    ("{name:'CBT3',treatment1:'CBT',treatment2:'IPT',events1:42,n1:140,events2:40,n2:145}",
     "{name:'CBT3',treatment1:'CBT',treatment2:'IPT',events1:42,n1:140,events2:40,n2:145,subgroup:'Mild',year:2017}"),
    ("{name:'CBT4',treatment1:'TAU',treatment2:'MBCT',events1:55,n1:160,events2:35,n2:158}",
     "{name:'CBT4',treatment1:'TAU',treatment2:'MBCT',events1:55,n1:160,events2:35,n2:158,subgroup:'Severe',year:2018}"),
    ("{name:'CBT5',treatment1:'CBT',treatment2:'MBCT',events1:39,n1:135,events2:36,n2:140}",
     "{name:'CBT5',treatment1:'CBT',treatment2:'MBCT',events1:39,n1:135,events2:36,n2:140,subgroup:'Moderate',year:2019}"),
]

count = 0
for old, new in replacements:
    if old in content and 'subgroup' not in content[content.find(old):content.find(old)+len(old)+50]:
        content = content.replace(old, new)
        count += 1

print(f'[OK] Added subgroup/year to {count} studies')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
