"""Add multiple demo datasets to NMA Pro v6.2"""
import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('Original file length:', len(content))

# New DEMO_DATASETS and loadDemo
new_code = """const DEMO_DATASETS={thrombolytics:{name:'Thrombolytics (OR)',effectMeasure:'OR',dataType:'binary',studies:[{name:'GUSTO-1',treatment1:'SK',events1:1135,n1:13780,treatment2:'tPA',events2:1021,n2:13746,year:1993,rob:'low',meanAge:62,propMale:0.75},{name:'ISIS-3',treatment1:'SK',events1:2891,n1:20676,treatment2:'tPA',events2:2878,n2:20656,year:1992,rob:'low',meanAge:61,propMale:0.76},{name:'GISSI-2',treatment1:'SK',events1:1012,n1:10372,treatment2:'tPA',events2:1033,n2:10396,year:1990,rob:'low',meanAge:60,propMale:0.80},{name:'INJECT',treatment1:'SK',events1:470,n1:6095,treatment2:'Reteplase',events2:471,n2:6100,year:1995,rob:'low',meanAge:62,propMale:0.74},{name:'RAPID-2',treatment1:'tPA',events1:23,n1:169,treatment2:'Reteplase',events2:20,n2:155,year:1996,rob:'some',meanAge:58,propMale:0.78},{name:'ASSENT-2',treatment1:'tPA',events1:705,n1:8488,treatment2:'Tenecteplase',events2:724,n2:8461,year:1999,rob:'low',meanAge:61,propMale:0.77},{name:'Granger2003',treatment1:'SK',events1:145,n1:1500,treatment2:'Anistreplase',events2:141,n2:1510,year:1990,rob:'some',meanAge:63,propMale:0.70},{name:'AIMS',treatment1:'Placebo',events1:95,n1:502,treatment2:'Anistreplase',events2:65,n2:502,year:1988,rob:'low',meanAge:57,propMale:0.83},{name:'ASSET',treatment1:'Placebo',events1:226,n1:2495,treatment2:'tPA',events2:182,n2:2516,year:1988,rob:'low',meanAge:56,propMale:0.76},{name:'LATE',treatment1:'Placebo',events1:556,n1:2918,treatment2:'tPA',events2:510,n2:2902,year:1993,rob:'low',meanAge:60,propMale:0.77},{name:'EMERAS',treatment1:'Placebo',events1:253,n1:2257,treatment2:'SK',events2:268,n2:2259,year:1993,rob:'low',meanAge:59,propMale:0.78},{name:'ISIS-2a',treatment1:'Placebo',events1:1029,n1:8592,treatment2:'SK',events2:791,n2:8595,year:1988,rob:'low',meanAge:62,propMale:0.76}]},cbt_depression:{name:'CBT for Depression (SMD)',effectMeasure:'SMD',dataType:'continuous',studies:[{name:'Beutler1991',treatment1:'CBT',mean1:-8.2,sd1:5.4,n1:25,treatment2:'WL',mean2:-2.1,sd2:4.8,n2:24,year:1991,rob:'some',meanAge:42,propMale:0.35},{name:'Elkin1989',treatment1:'CBT',mean1:-10.1,sd1:6.2,n1:59,treatment2:'IPT',mean2:-9.8,sd2:5.9,n2:61,year:1989,rob:'low',meanAge:35,propMale:0.30},{name:'Hollon1992',treatment1:'CBT',mean1:-12.5,sd1:7.1,n1:25,treatment2:'ADM',mean2:-11.2,sd2:6.8,n2:25,year:1992,rob:'low',meanAge:38,propMale:0.40},{name:'Jacobson1996',treatment1:'BA',mean1:-9.3,sd1:5.8,n1:50,treatment2:'CBT',mean2:-9.1,sd2:5.5,n2:50,year:1996,rob:'low',meanAge:40,propMale:0.38},{name:'Rush1977',treatment1:'CBT',mean1:-7.8,sd1:4.9,n1:19,treatment2:'ADM',mean2:-5.2,sd2:5.1,n2:22,year:1977,rob:'some',meanAge:33,propMale:0.32},{name:'Shaw1977',treatment1:'CBT',mean1:-6.5,sd1:4.2,n1:10,treatment2:'WL',mean2:-1.8,sd2:3.9,n2:10,year:1977,rob:'high',meanAge:29,propMale:0.25},{name:'DeRubeis2005',treatment1:'CBT',mean1:-13.2,sd1:8.1,n1:60,treatment2:'ADM',mean2:-12.8,sd2:7.9,n2:120,year:2005,rob:'low',meanAge:40,propMale:0.42},{name:'Dimidjian2006',treatment1:'BA',mean1:-11.5,sd1:6.9,n1:43,treatment2:'ADM',mean2:-10.2,sd2:7.2,n2:47,year:2006,rob:'low',meanAge:38,propMale:0.35},{name:'Cuijpers2008',treatment1:'CBT',mean1:-8.9,sd1:5.6,n1:35,treatment2:'IPT',mean2:-8.5,sd2:5.3,n2:38,year:2008,rob:'some',meanAge:44,propMale:0.28},{name:'Weissman1979',treatment1:'IPT',mean1:-7.2,sd1:4.5,n1:30,treatment2:'WL',mean2:-2.5,sd2:4.1,n2:28,year:1979,rob:'some',meanAge:36,propMale:0.30}]},vaccines_rr:{name:'Vaccines Efficacy (RR)',effectMeasure:'RR',dataType:'binary',studies:[{name:'Madhi2020',treatment1:'Placebo',events1:185,n1:4300,treatment2:'ChAdOx1',events2:30,n2:4440,year:2020,rob:'low',meanAge:45,propMale:0.48},{name:'Polack2020',treatment1:'Placebo',events1:162,n1:18325,treatment2:'BNT162b2',events2:8,n2:18198,year:2020,rob:'low',meanAge:52,propMale:0.51},{name:'Baden2021',treatment1:'Placebo',events1:185,n1:14073,treatment2:'mRNA-1273',events2:11,n2:14134,year:2021,rob:'low',meanAge:51,propMale:0.53},{name:'Voysey2021a',treatment1:'Placebo',events1:101,n1:5807,treatment2:'ChAdOx1',events2:30,n2:5829,year:2021,rob:'low',meanAge:44,propMale:0.46},{name:'Voysey2021b',treatment1:'Placebo',events1:71,n1:4088,treatment2:'ChAdOx1',events2:27,n2:4043,year:2021,rob:'low',meanAge:48,propMale:0.50},{name:'Sadoff2021',treatment1:'Placebo',events1:348,n1:19544,treatment2:'Ad26',events2:116,n2:19630,year:2021,rob:'low',meanAge:52,propMale:0.55},{name:'Logunov2021',treatment1:'Placebo',events1:62,n1:4902,treatment2:'Sputnik',events2:16,n2:14964,year:2021,rob:'some',meanAge:45,propMale:0.49},{name:'Tanriover2021',treatment1:'Placebo',events1:26,n1:752,treatment2:'CoronaVac',events2:9,n2:758,year:2021,rob:'some',meanAge:42,propMale:0.47},{name:'Heath2021',treatment1:'Placebo',events1:64,n1:4870,treatment2:'NVX-CoV',events2:6,n2:4856,year:2021,rob:'low',meanAge:48,propMale:0.52}]},antihypertensives:{name:'Antihypertensives (RD)',effectMeasure:'RD',dataType:'binary',studies:[{name:'ALLHAT2002a',treatment1:'Chlorthalidone',events1:608,n1:15255,treatment2:'Amlodipine',events2:377,n2:9048,year:2002,rob:'low',meanAge:67,propMale:0.53},{name:'ALLHAT2002b',treatment1:'Chlorthalidone',events1:608,n1:15255,treatment2:'Lisinopril',events2:612,n2:9054,year:2002,rob:'low',meanAge:67,propMale:0.53},{name:'ASCOT2005',treatment1:'Atenolol',events1:429,n1:9618,treatment2:'Amlodipine',events2:327,n2:9639,year:2005,rob:'low',meanAge:63,propMale:0.77},{name:'VALUE2004',treatment1:'Amlodipine',events1:810,n1:7596,treatment2:'Valsartan',events2:789,n2:7649,year:2004,rob:'low',meanAge:67,propMale:0.58},{name:'LIFE2002',treatment1:'Atenolol',events1:588,n1:4588,treatment2:'Losartan',events2:508,n2:4605,year:2002,rob:'low',meanAge:67,propMale:0.46},{name:'STOP22000',treatment1:'Diuretics',events1:221,n1:2213,treatment2:'ACEi',events2:235,n2:2205,year:2000,rob:'low',meanAge:76,propMale:0.34},{name:'NORDIL2000',treatment1:'Diuretics',events1:403,n1:5410,treatment2:'Diltiazem',events2:400,n2:5471,year:2000,rob:'low',meanAge:60,propMale:0.49},{name:'INSIGHT2000',treatment1:'Diuretics',events1:200,n1:3157,treatment2:'Nifedipine',events2:182,n2:3164,year:2000,rob:'low',meanAge:65,propMale:0.52}]},painkillers_hr:{name:'Analgesics Pain Relief (HR)',effectMeasure:'HR',dataType:'timeToEvent',studies:[{name:'Moore2015a',treatment1:'Placebo',logHR:0,seLogHR:0.15,treatment2:'Ibuprofen',logHR:-0.85,seLogHR:0.12,year:2015,rob:'low',meanAge:45,propMale:0.48},{name:'Moore2015b',treatment1:'Placebo',logHR:0,seLogHR:0.18,treatment2:'Paracetamol',logHR:-0.42,seLogHR:0.14,year:2015,rob:'low',meanAge:42,propMale:0.45},{name:'Derry2016',treatment1:'Ibuprofen',logHR:0,seLogHR:0.10,treatment2:'Diclofenac',logHR:-0.18,seLogHR:0.11,year:2016,rob:'low',meanAge:48,propMale:0.50},{name:'Wiffen2017',treatment1:'Paracetamol',logHR:0,seLogHR:0.12,treatment2:'Naproxen',logHR:-0.35,seLogHR:0.13,year:2017,rob:'some',meanAge:50,propMale:0.52},{name:'Chou2017',treatment1:'Placebo',logHR:0,seLogHR:0.20,treatment2:'Celecoxib',logHR:-0.72,seLogHR:0.16,year:2017,rob:'low',meanAge:55,propMale:0.44},{name:'DaSilva2018',treatment1:'Ibuprofen',logHR:0,seLogHR:0.11,treatment2:'Naproxen',logHR:-0.15,seLogHR:0.12,year:2018,rob:'low',meanAge:46,propMale:0.49},{name:'Enck2019',treatment1:'Paracetamol',logHR:0,seLogHR:0.14,treatment2:'Ibuprofen',logHR:-0.38,seLogHR:0.13,year:2019,rob:'some',meanAge:44,propMale:0.47},{name:'Zhang2020',treatment1:'Diclofenac',logHR:0,seLogHR:0.13,treatment2:'Celecoxib',logHR:0.08,seLogHR:0.14,year:2020,rob:'low',meanAge:52,propMale:0.51}]}};function loadDemo(datasetKey){datasetKey=datasetKey||'thrombolytics';const dataset=DEMO_DATASETS[datasetKey];if(!dataset){console.error('Unknown dataset:',datasetKey);return}AppState.studies=JSON.parse(JSON.stringify(dataset.studies));AppState.effectMeasure=dataset.effectMeasure;const sel=document.getElementById('effectMeasureSelect');if(sel)sel.value=dataset.effectMeasure;renderStudyTable();announce(dataset.name+' demo data loaded')}"""

# Find loadDemo function
start_marker = 'function loadDemo(){'
if start_marker in content:
    start = content.find(start_marker)
    end = start + len(start_marker)
    brace_count = 1
    while brace_count > 0 and end < len(content):
        if content[end] == '{':
            brace_count += 1
        elif content[end] == '}':
            brace_count -= 1
        end += 1

    print(f'Found loadDemo at {start}-{end}')
    content = content[:start] + new_code + content[end:]
    print('[OK] Replaced loadDemo with DEMO_DATASETS')
else:
    print('[ERROR] loadDemo not found')

# Add dropdown selector near loadDemoBtn
dropdown = '<select id="demoDatasetSelect" class="form-select" style="width:200px;display:inline-block;margin-right:8px"><option value="thrombolytics">Thrombolytics (OR)</option><option value="cbt_depression">CBT Depression (SMD)</option><option value="vaccines_rr">Vaccines (RR)</option><option value="antihypertensives">Antihypertensives (RD)</option><option value="painkillers_hr">Analgesics (HR)</option></select>'

btn_pattern = r'(<button[^>]*id="loadDemoBtn"[^>]*>)'
if re.search(btn_pattern, content):
    content = re.sub(btn_pattern, dropdown + r'\1', content)
    print('[OK] Added dropdown')
else:
    print('[WARN] Button pattern not found')

# Update onclick handler
old_onclick = 'onclick="loadDemo()"'
new_onclick = "onclick=\"loadDemo(document.getElementById('demoDatasetSelect').value)\""
if old_onclick in content:
    content = content.replace(old_onclick, new_onclick)
    print('[OK] Updated onclick')
else:
    print('[WARN] onclick not found')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('New file length:', len(content))
print('\n[DONE] Demo datasets added!')
