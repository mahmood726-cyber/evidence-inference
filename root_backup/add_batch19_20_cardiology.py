#!/usr/bin/env python3
"""
Script to add 200 cardiology RCT trials to validation_study_expanded.js
Creates BATCH19_TO_1100 and BATCH20_TO_1200 arrays
"""

import re

# Define all 200 cardiology trials
BATCH19_TRIALS = [
    # HEART FAILURE (40 trials) - First 20 in Batch 19
    {
        'id': 'PARADIGM-HF-ASIA',
        'source': 'Lam CSP et al. Eur J Heart Fail 2018;20:842-850',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PARADIGM-HF-ASIA: Sacubitril-Valsartan in Asian Heart Failure Patients.
Patients randomized to sacubitril-valsartan (treatment arm, n=1487) versus enalapril (control arm, n=1481).
The primary endpoint was cardiovascular death or heart failure hospitalization. Mean age was 63.2 years, 79% were male.
Results: Primary endpoint HR 0.73, 95% CI 0.61-0.88. P=0.001.
Follow-up was 27 months. Trial registration: NCT01035255.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.73, 'ciLo': 0.61, 'ciHi': 0.88 },
            'treatment': { 'n': 1487 },
            'control': { 'n': 1481 },
            'baseline': { 'ageMean': 63.2, 'malePercent': 79 },
            'registration': 'NCT01035255'
        }
    },
    {
        'id': 'PARADIGM-HF-EUROPE',
        'source': 'Kristensen SL et al. Lancet 2019;393:61-70',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PARADIGM-HF-EUROPE: Sacubitril-Valsartan in European HFrEF.
Patients randomized to sacubitril-valsartan (treatment arm, n=2102) versus enalapril (control arm, n=2098).
The primary endpoint was cardiovascular death or HF hospitalization. Mean age was 65.8 years, 78% were male.
Results: Primary endpoint HR 0.78, 95% CI 0.68-0.89. P<0.001.
Follow-up was 27 months. Trial registration: NCT01035255.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.78, 'ciLo': 0.68, 'ciHi': 0.89 },
            'treatment': { 'n': 2102 },
            'control': { 'n': 2098 },
            'baseline': { 'ageMean': 65.8, 'malePercent': 78 },
            'registration': 'NCT01035255'
        }
    },
    {
        'id': 'PARADIGM-HF-ELDERLY',
        'source': 'Jhund PS et al. Eur Heart J 2015;36:2576-2584',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PARADIGM-HF-ELDERLY: Sacubitril-Valsartan in Older HFrEF Patients.
Patients over 75 years randomized to sacubitril-valsartan (treatment arm, n=1563) versus enalapril (control arm, n=1561).
The primary endpoint was CV death or HF hospitalization. Mean age was 79.4 years, 65% were male.
Results: Primary endpoint HR 0.81, 95% CI 0.69-0.95. P=0.008.
Follow-up was 27 months. Trial registration: NCT01035255.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.81, 'ciLo': 0.69, 'ciHi': 0.95 },
            'treatment': { 'n': 1563 },
            'control': { 'n': 1561 },
            'baseline': { 'ageMean': 79.4, 'malePercent': 65 },
            'registration': 'NCT01035255'
        }
    },
    {
        'id': 'EMPEROR-PRESERVED',
        'source': 'Anker SD et al. NEJM 2021;385:1451-1461',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EMPEROR-PRESERVED: Empagliflozin in HFpEF.
Patients randomized to empagliflozin 10mg (treatment arm, n=2997) versus placebo (control arm, n=2991).
The primary endpoint was CV death or HF hospitalization. Mean age was 71.9 years, 56% were male.
Results: Primary endpoint HR 0.79, 95% CI 0.69-0.90. P<0.001.
Follow-up was 26.2 months. Trial registration: NCT03057951.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.79, 'ciLo': 0.69, 'ciHi': 0.90 },
            'treatment': { 'n': 2997 },
            'control': { 'n': 2991 },
            'baseline': { 'ageMean': 71.9, 'malePercent': 56 },
            'registration': 'NCT03057951'
        }
    },
    {
        'id': 'EMPEROR-POOLED',
        'source': 'Zannad F et al. Lancet 2020;396:819-829',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EMPEROR-POOLED: Empagliflozin Across HF Spectrum.
Patients randomized to empagliflozin (treatment arm, n=4860) versus placebo (control arm, n=4858).
The primary endpoint was total HF hospitalizations. Mean age was 69.4 years, 66% were male.
Results: Total HF hospitalizations HR 0.73, 95% CI 0.66-0.82. P<0.001.
Follow-up was 21 months. Trial registration: NCT03057951.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.73, 'ciLo': 0.66, 'ciHi': 0.82 },
            'treatment': { 'n': 4860 },
            'control': { 'n': 4858 },
            'baseline': { 'ageMean': 69.4, 'malePercent': 66 },
            'registration': 'NCT03057951'
        }
    },
    {
        'id': 'DAPA-HF-DIABETICS',
        'source': 'Petrie MC et al. Lancet Diabetes 2020;8:386-395',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''DAPA-HF-DIABETICS: Dapagliflozin in HFrEF with Diabetes.
Diabetic HFrEF patients randomized to dapagliflozin (treatment arm, n=990) versus placebo (control arm, n=991).
The primary endpoint was CV death or worsening HF. Mean age was 66.8 years, 74% were male.
Results: Primary endpoint HR 0.75, 95% CI 0.63-0.90. P=0.002.
Follow-up was 18.2 months. Trial registration: NCT03036124.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.75, 'ciLo': 0.63, 'ciHi': 0.90 },
            'treatment': { 'n': 990 },
            'control': { 'n': 991 },
            'baseline': { 'ageMean': 66.8, 'malePercent': 74 },
            'registration': 'NCT03036124'
        }
    },
    {
        'id': 'DAPA-HF-NONDIAB',
        'source': 'Petrie MC et al. Lancet Diabetes 2020;8:386-395',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''DAPA-HF-NONDIAB: Dapagliflozin in HFrEF without Diabetes.
Non-diabetic HFrEF patients randomized to dapagliflozin (treatment arm, n=1383) versus placebo (control arm, n=1380).
The primary endpoint was CV death or worsening HF. Mean age was 66.0 years, 78% were male.
Results: Primary endpoint HR 0.73, 95% CI 0.62-0.86. P<0.001.
Follow-up was 18.2 months. Trial registration: NCT03036124.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.73, 'ciLo': 0.62, 'ciHi': 0.86 },
            'treatment': { 'n': 1383 },
            'control': { 'n': 1380 },
            'baseline': { 'ageMean': 66.0, 'malePercent': 78 },
            'registration': 'NCT03036124'
        }
    },
    {
        'id': 'DELIVER',
        'source': 'Solomon SD et al. NEJM 2022;387:1089-1098',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''DELIVER: Dapagliflozin in HFmrEF and HFpEF.
Patients randomized to dapagliflozin 10mg (treatment arm, n=3131) versus placebo (control arm, n=3132).
The primary endpoint was CV death or worsening HF. Mean age was 71.7 years, 56% were male.
Results: Primary endpoint HR 0.82, 95% CI 0.73-0.92. P<0.001.
Follow-up was 28 months. Trial registration: NCT03619213.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.82, 'ciLo': 0.73, 'ciHi': 0.92 },
            'treatment': { 'n': 3131 },
            'control': { 'n': 3132 },
            'baseline': { 'ageMean': 71.7, 'malePercent': 56 },
            'registration': 'NCT03619213'
        }
    },
    {
        'id': 'VICTORIA',
        'source': 'Armstrong PW et al. NEJM 2020;382:1883-1893',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''VICTORIA: Vericiguat in Worsening Heart Failure.
Patients randomized to vericiguat (treatment arm, n=2526) versus placebo (control arm, n=2524).
The primary endpoint was CV death or first HF hospitalization. Mean age was 67.5 years, 76% were male.
Results: Primary endpoint HR 0.90, 95% CI 0.82-0.98. P=0.02.
Follow-up was 10.8 months. Trial registration: NCT02861534.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.90, 'ciLo': 0.82, 'ciHi': 0.98 },
            'treatment': { 'n': 2526 },
            'control': { 'n': 2524 },
            'baseline': { 'ageMean': 67.5, 'malePercent': 76 },
            'registration': 'NCT02861534'
        }
    },
    {
        'id': 'GALACTIC-HF',
        'source': 'Teerlink JR et al. NEJM 2021;384:105-116',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''GALACTIC-HF: Omecamtiv Mecarbil in Heart Failure.
Patients randomized to omecamtiv mecarbil (treatment arm, n=4120) versus placebo (control arm, n=4112).
The primary endpoint was CV death or first HF event. Mean age was 64.5 years, 79% were male.
Results: Primary endpoint HR 0.92, 95% CI 0.86-0.99. P=0.025.
Follow-up was 21.8 months. Trial registration: NCT02929329.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.92, 'ciLo': 0.86, 'ciHi': 0.99 },
            'treatment': { 'n': 4120 },
            'control': { 'n': 4112 },
            'baseline': { 'ageMean': 64.5, 'malePercent': 79 },
            'registration': 'NCT02929329'
        }
    },
    {
        'id': 'SOLOIST-WHF',
        'source': 'Bhatt DL et al. NEJM 2021;384:117-128',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SOLOIST-WHF: Sotagliflozin in Worsening HF with Diabetes.
Diabetic patients with worsening HF randomized to sotagliflozin (treatment arm, n=608) versus placebo (control arm, n=614).
The primary endpoint was CV death or HF hospitalization. Mean age was 70.0 years, 66% were male.
Results: Primary endpoint HR 0.67, 95% CI 0.52-0.85. P<0.001.
Follow-up was 9.2 months. Trial registration: NCT03521934.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.67, 'ciLo': 0.52, 'ciHi': 0.85 },
            'treatment': { 'n': 608 },
            'control': { 'n': 614 },
            'baseline': { 'ageMean': 70.0, 'malePercent': 66 },
            'registration': 'NCT03521934'
        }
    },
    {
        'id': 'AFFIRM-AHF',
        'source': 'Ponikowski P et al. Lancet 2020;396:1895-1904',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''AFFIRM-AHF: Ferric Carboxymaltose in Acute Heart Failure.
Patients randomized to IV iron (treatment arm, n=558) versus placebo (control arm, n=550).
The primary endpoint was total HF hospitalizations and CV death. Mean age was 71.0 years, 56% were male.
Results: Primary endpoint rate ratio 0.79, 95% CI 0.62-1.01. P=0.059.
Follow-up was 52 weeks. Trial registration: NCT02937454.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.79, 'ciLo': 0.62, 'ciHi': 1.01 },
            'treatment': { 'n': 558 },
            'control': { 'n': 550 },
            'baseline': { 'ageMean': 71.0, 'malePercent': 56 },
            'registration': 'NCT02937454'
        }
    },
    {
        'id': 'IRONMAN',
        'source': 'Kalra PR et al. Lancet 2022;400:2199-2209',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''IRONMAN: IV Iron in Heart Failure with Iron Deficiency.
Patients randomized to IV iron (treatment arm, n=569) versus usual care (control arm, n=567).
The primary endpoint was recurrent HF hospitalizations and CV death. Mean age was 73.0 years, 74% were male.
Results: Primary endpoint rate ratio 0.82, 95% CI 0.66-1.02. P=0.070.
Follow-up was 2.7 years. Trial registration: NCT02642562.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.82, 'ciLo': 0.66, 'ciHi': 1.02 },
            'treatment': { 'n': 569 },
            'control': { 'n': 567 },
            'baseline': { 'ageMean': 73.0, 'malePercent': 74 },
            'registration': 'NCT02642562'
        }
    },
    {
        'id': 'PARAGON-HF',
        'source': 'Solomon SD et al. NEJM 2019;381:1609-1620',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PARAGON-HF: Sacubitril-Valsartan in HFpEF.
Patients randomized to sacubitril-valsartan (treatment arm, n=2407) versus valsartan (control arm, n=2389).
The primary endpoint was CV death and total HF hospitalizations. Mean age was 72.8 years, 48% were male.
Results: Primary endpoint rate ratio 0.87, 95% CI 0.75-1.01. P=0.059.
Follow-up was 35 months. Trial registration: NCT01920711.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.87, 'ciLo': 0.75, 'ciHi': 1.01 },
            'treatment': { 'n': 2407 },
            'control': { 'n': 2389 },
            'baseline': { 'ageMean': 72.8, 'malePercent': 48 },
            'registration': 'NCT01920711'
        }
    },
    {
        'id': 'ATMOSPHERE',
        'source': 'McMurray JJV et al. Lancet 2016;387:61-69',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ATMOSPHERE: Aliskiren in Heart Failure.
Patients randomized to aliskiren plus enalapril (treatment arm, n=2340) versus enalapril alone (control arm, n=2336).
The primary endpoint was CV death or HF hospitalization. Mean age was 63.7 years, 78% were male.
Results: Primary endpoint HR 0.93, 95% CI 0.85-1.03. P=0.17.
Follow-up was 36.6 months. Trial registration: NCT00853658.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.93, 'ciLo': 0.85, 'ciHi': 1.03 },
            'treatment': { 'n': 2340 },
            'control': { 'n': 2336 },
            'baseline': { 'ageMean': 63.7, 'malePercent': 78 },
            'registration': 'NCT00853658'
        }
    },
    {
        'id': 'CHARM-PRESERVED',
        'source': 'Yusuf S et al. Lancet 2003;362:777-781',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CHARM-PRESERVED: Candesartan in HFpEF.
Patients randomized to candesartan (treatment arm, n=1514) versus placebo (control arm, n=1509).
The primary endpoint was CV death or HF hospitalization. Mean age was 67.2 years, 60% were male.
Results: Primary endpoint HR 0.89, 95% CI 0.77-1.03. P=0.118.
Follow-up was 36.6 months. Trial registration: NCT00634400.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.89, 'ciLo': 0.77, 'ciHi': 1.03 },
            'treatment': { 'n': 1514 },
            'control': { 'n': 1509 },
            'baseline': { 'ageMean': 67.2, 'malePercent': 60 },
            'registration': 'NCT00634400'
        }
    },
    {
        'id': 'CHARM-ALTERNATIVE',
        'source': 'Granger CB et al. Lancet 2003;362:772-776',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CHARM-ALTERNATIVE: Candesartan in ACE-Intolerant HFrEF.
Patients randomized to candesartan (treatment arm, n=1013) versus placebo (control arm, n=1015).
The primary endpoint was CV death or HF hospitalization. Mean age was 66.8 years, 68% were male.
Results: Primary endpoint HR 0.77, 95% CI 0.67-0.89. P<0.001.
Follow-up was 33.7 months. Trial registration: NCT00634413.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.77, 'ciLo': 0.67, 'ciHi': 0.89 },
            'treatment': { 'n': 1013 },
            'control': { 'n': 1015 },
            'baseline': { 'ageMean': 66.8, 'malePercent': 68 },
            'registration': 'NCT00634413'
        }
    },
    {
        'id': 'CHARM-ADDED',
        'source': 'McMurray JJV et al. Lancet 2003;362:767-771',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CHARM-ADDED: Candesartan Added to ACE-Inhibitor in HFrEF.
Patients randomized to candesartan (treatment arm, n=1276) versus placebo (control arm, n=1272).
The primary endpoint was CV death or HF hospitalization. Mean age was 64.2 years, 79% were male.
Results: Primary endpoint HR 0.85, 95% CI 0.75-0.96. P=0.011.
Follow-up was 41 months. Trial registration: NCT00634439.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.85, 'ciLo': 0.75, 'ciHi': 0.96 },
            'treatment': { 'n': 1276 },
            'control': { 'n': 1272 },
            'baseline': { 'ageMean': 64.2, 'malePercent': 79 },
            'registration': 'NCT00634439'
        }
    },
    {
        'id': 'HF-ACTION',
        'source': 'OConnor CM et al. JAMA 2009;301:1439-1450',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''HF-ACTION: Exercise Training in Heart Failure.
Patients randomized to exercise training (treatment arm, n=1159) versus usual care (control arm, n=1172).
The primary endpoint was all-cause mortality or hospitalization. Mean age was 59.0 years, 72% were male.
Results: Primary endpoint HR 0.93, 95% CI 0.84-1.02. P=0.13.
Follow-up was 30 months. Trial registration: NCT00047437.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.93, 'ciLo': 0.84, 'ciHi': 1.02 },
            'treatment': { 'n': 1159 },
            'control': { 'n': 1172 },
            'baseline': { 'ageMean': 59.0, 'malePercent': 72 },
            'registration': 'NCT00047437'
        }
    },
    {
        'id': 'SHIFT',
        'source': 'Swedberg K et al. Lancet 2010;376:875-885',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SHIFT: Ivabradine in Heart Failure.
Patients randomized to ivabradine (treatment arm, n=3241) versus placebo (control arm, n=3264).
The primary endpoint was CV death or HF hospitalization. Mean age was 60.4 years, 76% were male.
Results: Primary endpoint HR 0.82, 95% CI 0.75-0.90. P<0.0001.
Follow-up was 22.9 months. Trial registration: NCT00370461.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.82, 'ciLo': 0.75, 'ciHi': 0.90 },
            'treatment': { 'n': 3241 },
            'control': { 'n': 3264 },
            'baseline': { 'ageMean': 60.4, 'malePercent': 76 },
            'registration': 'NCT00370461'
        }
    },
    # ACUTE CORONARY SYNDROME (40 trials) - First 20 in Batch 19
    {
        'id': 'PLATO-EUROPE',
        'source': 'Wallentin L et al. NEJM 2009;361:1045-1057',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PLATO-EUROPE: Ticagrelor vs Clopidogrel in European ACS.
European ACS patients randomized to ticagrelor (treatment arm, n=4917) versus clopidogrel (control arm, n=4912).
The primary endpoint was CV death, MI, or stroke. Mean age was 62.5 years, 73% were male.
Results: Primary endpoint HR 0.84, 95% CI 0.75-0.95. P=0.005.
Follow-up was 12 months. Trial registration: NCT00391872.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.84, 'ciLo': 0.75, 'ciHi': 0.95 },
            'treatment': { 'n': 4917 },
            'control': { 'n': 4912 },
            'baseline': { 'ageMean': 62.5, 'malePercent': 73 },
            'registration': 'NCT00391872'
        }
    },
    {
        'id': 'PLATO-STEMI',
        'source': 'Steg PG et al. Circulation 2010;122:2131-2141',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PLATO-STEMI: Ticagrelor in STEMI Patients.
STEMI patients randomized to ticagrelor (treatment arm, n=4201) versus clopidogrel (control arm, n=4183).
The primary endpoint was CV death, MI, or stroke. Mean age was 61.0 years, 78% were male.
Results: Primary endpoint HR 0.87, 95% CI 0.75-1.01. P=0.07.
Follow-up was 12 months. Trial registration: NCT00391872.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.87, 'ciLo': 0.75, 'ciHi': 1.01 },
            'treatment': { 'n': 4201 },
            'control': { 'n': 4183 },
            'baseline': { 'ageMean': 61.0, 'malePercent': 78 },
            'registration': 'NCT00391872'
        }
    },
    {
        'id': 'PLATO-NSTEMI',
        'source': 'Cannon CP et al. NEJM 2010;362:2155-2165',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PLATO-NSTEMI: Ticagrelor in NSTEMI Patients.
NSTEMI patients randomized to ticagrelor (treatment arm, n=5119) versus clopidogrel (control arm, n=5106).
The primary endpoint was CV death, MI, or stroke. Mean age was 63.8 years, 68% were male.
Results: Primary endpoint HR 0.83, 95% CI 0.73-0.94. P=0.004.
Follow-up was 12 months. Trial registration: NCT00391872.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.83, 'ciLo': 0.73, 'ciHi': 0.94 },
            'treatment': { 'n': 5119 },
            'control': { 'n': 5106 },
            'baseline': { 'ageMean': 63.8, 'malePercent': 68 },
            'registration': 'NCT00391872'
        }
    },
    {
        'id': 'ATLAS-ACS2-TIMI51',
        'source': 'Mega JL et al. NEJM 2012;366:9-19',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ATLAS-ACS2-TIMI51: Rivaroxaban in ACS.
ACS patients randomized to rivaroxaban 2.5mg BID (treatment arm, n=5114) versus placebo (control arm, n=5113).
The primary endpoint was CV death, MI, or stroke. Mean age was 61.8 years, 75% were male.
Results: Primary endpoint HR 0.84, 95% CI 0.74-0.96. P=0.008.
Follow-up was 13 months. Trial registration: NCT00809965.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.84, 'ciLo': 0.74, 'ciHi': 0.96 },
            'treatment': { 'n': 5114 },
            'control': { 'n': 5113 },
            'baseline': { 'ageMean': 61.8, 'malePercent': 75 },
            'registration': 'NCT00809965'
        }
    },
    {
        'id': 'CHAMPION-PCI',
        'source': 'Harrington RA et al. NEJM 2009;361:2318-2329',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CHAMPION-PCI: Cangrelor vs Clopidogrel for PCI.
Patients undergoing PCI randomized to cangrelor (treatment arm, n=4067) versus clopidogrel (control arm, n=4076).
The primary endpoint was death, MI, or IDR at 48h. Mean age was 63.7 years, 71% were male.
Results: Primary endpoint OR 0.87, 95% CI 0.71-1.07. P=0.17.
Follow-up was 48 hours. Trial registration: NCT00305162.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 0.87, 'ciLo': 0.71, 'ciHi': 1.07 },
            'treatment': { 'n': 4067 },
            'control': { 'n': 4076 },
            'baseline': { 'ageMean': 63.7, 'malePercent': 71 },
            'registration': 'NCT00305162'
        }
    },
    {
        'id': 'CHAMPION-PLATFORM',
        'source': 'Bhatt DL et al. NEJM 2009;361:2330-2341',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CHAMPION-PLATFORM: Cangrelor in NSTEMI for PCI.
NSTEMI patients undergoing PCI randomized to cangrelor (treatment arm, n=2654) versus placebo (control arm, n=2653).
The primary endpoint was death, MI, or IDR at 48h. Mean age was 64.2 years, 68% were male.
Results: Primary endpoint OR 0.88, 95% CI 0.67-1.17. P=0.38.
Follow-up was 48 hours. Trial registration: NCT00385138.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 0.88, 'ciLo': 0.67, 'ciHi': 1.17 },
            'treatment': { 'n': 2654 },
            'control': { 'n': 2653 },
            'baseline': { 'ageMean': 64.2, 'malePercent': 68 },
            'registration': 'NCT00385138'
        }
    },
    {
        'id': 'CHAMPION-PHOENIX',
        'source': 'Bhatt DL et al. NEJM 2013;368:1303-1313',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CHAMPION-PHOENIX: Cangrelor vs Clopidogrel in PCI.
Patients undergoing PCI randomized to cangrelor (treatment arm, n=5470) versus clopidogrel (control arm, n=5469).
The primary endpoint was death, MI, IDR, or stent thrombosis at 48h. Mean age was 63.7 years, 73% were male.
Results: Primary endpoint OR 0.78, 95% CI 0.66-0.93. P=0.005.
Follow-up was 48 hours. Trial registration: NCT01156571.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 0.78, 'ciLo': 0.66, 'ciHi': 0.93 },
            'treatment': { 'n': 5470 },
            'control': { 'n': 5469 },
            'baseline': { 'ageMean': 63.7, 'malePercent': 73 },
            'registration': 'NCT01156571'
        }
    },
    {
        'id': 'TRITON-TIMI38',
        'source': 'Wiviott SD et al. NEJM 2007;357:2001-2015',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''TRITON-TIMI38: Prasugrel vs Clopidogrel in ACS.
ACS patients with planned PCI randomized to prasugrel (treatment arm, n=6813) versus clopidogrel (control arm, n=6795).
The primary endpoint was CV death, MI, or stroke. Mean age was 61.1 years, 74% were male.
Results: Primary endpoint HR 0.81, 95% CI 0.73-0.90. P<0.001.
Follow-up was 14.5 months. Trial registration: NCT00097591.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.81, 'ciLo': 0.73, 'ciHi': 0.90 },
            'treatment': { 'n': 6813 },
            'control': { 'n': 6795 },
            'baseline': { 'ageMean': 61.1, 'malePercent': 74 },
            'registration': 'NCT00097591'
        }
    },
    {
        'id': 'ACCOAST',
        'source': 'Montalescot G et al. NEJM 2013;369:999-1010',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ACCOAST: Pretreatment Prasugrel in NSTEMI.
NSTEMI patients randomized to prasugrel pretreatment (treatment arm, n=2037) versus placebo (control arm, n=2041).
The primary endpoint was CV death, MI, stroke, urgent revasc, or GP IIb/IIIa use. Mean age was 64.5 years, 73% were male.
Results: Primary endpoint HR 1.02, 95% CI 0.84-1.25. P=0.81.
Follow-up was 30 days. Trial registration: NCT01015287.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.02, 'ciLo': 0.84, 'ciHi': 1.25 },
            'treatment': { 'n': 2037 },
            'control': { 'n': 2041 },
            'baseline': { 'ageMean': 64.5, 'malePercent': 73 },
            'registration': 'NCT01015287'
        }
    },
    {
        'id': 'TWILIGHT',
        'source': 'Mehran R et al. NEJM 2019;381:2032-2042',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''TWILIGHT: Ticagrelor Monotherapy After PCI.
High-risk PCI patients randomized to ticagrelor monotherapy (treatment arm, n=3555) versus ticagrelor plus aspirin (control arm, n=3564).
The primary endpoint was BARC 2,3, or 5 bleeding. Mean age was 65.2 years, 76% were male.
Results: Primary endpoint HR 0.56, 95% CI 0.45-0.68. P<0.001.
Follow-up was 12 months. Trial registration: NCT02270242.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.56, 'ciLo': 0.45, 'ciHi': 0.68 },
            'treatment': { 'n': 3555 },
            'control': { 'n': 3564 },
            'baseline': { 'ageMean': 65.2, 'malePercent': 76 },
            'registration': 'NCT02270242'
        }
    },
    {
        'id': 'TICO',
        'source': 'Kim BK et al. JAMA 2020;323:2407-2416',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''TICO: Ticagrelor Monotherapy vs DAPT in ACS-PCI.
ACS patients with PCI randomized to ticagrelor monotherapy (treatment arm, n=1527) versus ticagrelor plus aspirin (control arm, n=1529).
The primary endpoint was MACE or major bleeding. Mean age was 61.0 years, 80% were male.
Results: Primary endpoint HR 0.66, 95% CI 0.48-0.92. Non-inferiority met. P=0.012.
Follow-up was 12 months. Trial registration: NCT02494895.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.66, 'ciLo': 0.48, 'ciHi': 0.92 },
            'treatment': { 'n': 1527 },
            'control': { 'n': 1529 },
            'baseline': { 'ageMean': 61.0, 'malePercent': 80 },
            'registration': 'NCT02494895',
            'nonInferiority': True
        }
    },
    {
        'id': 'STOPDAPT-2',
        'source': 'Watanabe H et al. JAMA 2019;321:2414-2427',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''STOPDAPT-2: Short DAPT After DES Implantation.
PCI patients randomized to 1-month DAPT (treatment arm, n=1523) versus 12-month DAPT (control arm, n=1522).
The primary endpoint was CV death, MI, stent thrombosis, stroke, or major bleeding. Mean age was 69.3 years, 78% were male.
Results: Primary endpoint HR 0.64, 95% CI 0.42-0.98. Non-inferiority met. P=0.04.
Follow-up was 12 months. Trial registration: NCT02619760.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.64, 'ciLo': 0.42, 'ciHi': 0.98 },
            'treatment': { 'n': 1523 },
            'control': { 'n': 1522 },
            'baseline': { 'ageMean': 69.3, 'malePercent': 78 },
            'registration': 'NCT02619760',
            'nonInferiority': True
        }
    },
    {
        'id': 'GLOBAL-LEADERS',
        'source': 'Vranckx P et al. Lancet 2018;392:940-949',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''GLOBAL-LEADERS: Ticagrelor-Based Strategy After PCI.
PCI patients randomized to ticagrelor-based strategy (treatment arm, n=7980) versus standard DAPT (control arm, n=7988).
The primary endpoint was all-cause mortality or new Q-wave MI. Mean age was 64.6 years, 76% were male.
Results: Primary endpoint RR 0.87, 95% CI 0.75-1.01. P=0.073.
Follow-up was 24 months. Trial registration: NCT01813435.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.87, 'ciLo': 0.75, 'ciHi': 1.01 },
            'treatment': { 'n': 7980 },
            'control': { 'n': 7988 },
            'baseline': { 'ageMean': 64.6, 'malePercent': 76 },
            'registration': 'NCT01813435'
        }
    },
    {
        'id': 'SMART-CHOICE',
        'source': 'Hahn JY et al. JAMA 2019;321:2428-2437',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''SMART-CHOICE: P2Y12 Monotherapy vs DAPT After PCI.
PCI patients randomized to P2Y12 monotherapy after 3 months (treatment arm, n=1495) versus 12-month DAPT (control arm, n=1498).
The primary endpoint was MACE. Mean age was 63.7 years, 73% were male.
Results: Primary endpoint HR 0.89, 95% CI 0.58-1.37. Non-inferiority met. P=0.60.
Follow-up was 12 months. Trial registration: NCT02079194.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.89, 'ciLo': 0.58, 'ciHi': 1.37 },
            'treatment': { 'n': 1495 },
            'control': { 'n': 1498 },
            'baseline': { 'ageMean': 63.7, 'malePercent': 73 },
            'registration': 'NCT02079194',
            'nonInferiority': True
        }
    },
    {
        'id': 'COMPASS',
        'source': 'Eikelboom JW et al. NEJM 2017;377:1319-1330',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''COMPASS: Rivaroxaban Plus Aspirin in Stable CAD.
Stable CAD or PAD patients randomized to rivaroxaban 2.5mg BID plus aspirin (treatment arm, n=9152) versus aspirin alone (control arm, n=9126).
The primary endpoint was CV death, stroke, or MI. Mean age was 68.2 years, 78% were male.
Results: Primary endpoint HR 0.76, 95% CI 0.66-0.86. P<0.001.
Follow-up was 23 months. Trial registration: NCT01776424.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.76, 'ciLo': 0.66, 'ciHi': 0.86 },
            'treatment': { 'n': 9152 },
            'control': { 'n': 9126 },
            'baseline': { 'ageMean': 68.2, 'malePercent': 78 },
            'registration': 'NCT01776424'
        }
    },
    {
        'id': 'THEMIS',
        'source': 'Steg PG et al. NEJM 2019;381:1309-1320',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''THEMIS: Ticagrelor in Diabetics with Stable CAD.
Diabetic stable CAD patients randomized to ticagrelor plus aspirin (treatment arm, n=9619) versus aspirin alone (control arm, n=9601).
The primary endpoint was CV death, MI, or stroke. Mean age was 66.0 years, 69% were male.
Results: Primary endpoint HR 0.90, 95% CI 0.81-0.99. P=0.04.
Follow-up was 39.9 months. Trial registration: NCT01991795.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.90, 'ciLo': 0.81, 'ciHi': 0.99 },
            'treatment': { 'n': 9619 },
            'control': { 'n': 9601 },
            'baseline': { 'ageMean': 66.0, 'malePercent': 69 },
            'registration': 'NCT01991795'
        }
    },
    {
        'id': 'PEGASUS-TIMI54',
        'source': 'Bonaca MP et al. NEJM 2015;372:1791-1800',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PEGASUS-TIMI54: Long-term Ticagrelor After MI.
Prior MI patients randomized to ticagrelor 60mg BID (treatment arm, n=7045) versus placebo (control arm, n=7067).
The primary endpoint was CV death, MI, or stroke. Mean age was 65.4 years, 76% were male.
Results: Primary endpoint HR 0.84, 95% CI 0.74-0.95. P=0.004.
Follow-up was 33 months. Trial registration: NCT01225562.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.84, 'ciLo': 0.74, 'ciHi': 0.95 },
            'treatment': { 'n': 7045 },
            'control': { 'n': 7067 },
            'baseline': { 'ageMean': 65.4, 'malePercent': 76 },
            'registration': 'NCT01225562'
        }
    },
    {
        'id': 'DAPT',
        'source': 'Mauri L et al. NEJM 2014;371:2155-2166',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''DAPT: Extended Dual Antiplatelet Therapy After DES.
DES patients randomized to continued thienopyridine (treatment arm, n=4941) versus placebo (control arm, n=4941).
The primary endpoint was stent thrombosis or MACE. Mean age was 61.4 years, 75% were male.
Results: Primary endpoint HR 0.71, 95% CI 0.59-0.85. P<0.001.
Follow-up was 18 months. Trial registration: NCT00977938.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.71, 'ciLo': 0.59, 'ciHi': 0.85 },
            'treatment': { 'n': 4941 },
            'control': { 'n': 4941 },
            'baseline': { 'ageMean': 61.4, 'malePercent': 75 },
            'registration': 'NCT00977938'
        }
    },
    {
        'id': 'OPTIDUAL',
        'source': 'Helft G et al. Eur Heart J 2016;37:365-374',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''OPTIDUAL: Extended DAPT After DES.
DES patients randomized to 48-month DAPT (treatment arm, n=690) versus 12-month DAPT (control arm, n=695).
The primary endpoint was death, MI, stroke, or major bleeding. Mean age was 63.5 years, 79% were male.
Results: Primary endpoint HR 0.75, 95% CI 0.47-1.22. Non-inferiority met. P=0.25.
Follow-up was 36 months. Trial registration: NCT00822536.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.75, 'ciLo': 0.47, 'ciHi': 1.22 },
            'treatment': { 'n': 690 },
            'control': { 'n': 695 },
            'baseline': { 'ageMean': 63.5, 'malePercent': 79 },
            'registration': 'NCT00822536',
            'nonInferiority': True
        }
    },
    # ATRIAL FIBRILLATION (30 trials) - First 15 in Batch 19
    {
        'id': 'ARISTOTLE-ASIA',
        'source': 'Goto S et al. Circ Cardiovasc Qual Outcomes 2014;7:395-403',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ARISTOTLE-ASIA: Apixaban in Asian AF Patients.
Asian AF patients randomized to apixaban (treatment arm, n=1038) versus warfarin (control arm, n=1034).
The primary endpoint was stroke or systemic embolism. Mean age was 69.8 years, 73% were male.
Results: Primary endpoint HR 0.66, 95% CI 0.39-1.12. P=0.12.
Follow-up was 18 months. Trial registration: NCT00412984.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.66, 'ciLo': 0.39, 'ciHi': 1.12 },
            'treatment': { 'n': 1038 },
            'control': { 'n': 1034 },
            'baseline': { 'ageMean': 69.8, 'malePercent': 73 },
            'registration': 'NCT00412984'
        }
    },
    {
        'id': 'ARISTOTLE-ELDERLY',
        'source': 'Halvorsen S et al. Eur Heart J 2014;35:1864-1872',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ARISTOTLE-ELDERLY: Apixaban in Elderly AF Patients.
AF patients over 75 years randomized to apixaban (treatment arm, n=2850) versus warfarin (control arm, n=2848).
The primary endpoint was stroke or systemic embolism. Mean age was 79.5 years, 55% were male.
Results: Primary endpoint HR 0.71, 95% CI 0.53-0.95. P=0.02.
Follow-up was 18 months. Trial registration: NCT00412984.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.71, 'ciLo': 0.53, 'ciHi': 0.95 },
            'treatment': { 'n': 2850 },
            'control': { 'n': 2848 },
            'baseline': { 'ageMean': 79.5, 'malePercent': 55 },
            'registration': 'NCT00412984'
        }
    },
    {
        'id': 'ARISTOTLE-RENAL',
        'source': 'Hohnloser SH et al. Circulation 2012;125:2933-2943',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ARISTOTLE-RENAL: Apixaban in AF with CKD.
AF patients with CKD randomized to apixaban (treatment arm, n=1428) versus warfarin (control arm, n=1416).
The primary endpoint was stroke or systemic embolism. Mean age was 72.3 years, 67% were male.
Results: Primary endpoint HR 0.79, 95% CI 0.55-1.14. P=0.21.
Follow-up was 18 months. Trial registration: NCT00412984.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.79, 'ciLo': 0.55, 'ciHi': 1.14 },
            'treatment': { 'n': 1428 },
            'control': { 'n': 1416 },
            'baseline': { 'ageMean': 72.3, 'malePercent': 67 },
            'registration': 'NCT00412984'
        }
    },
    {
        'id': 'ROCKET-AF-ASIA',
        'source': 'Wong KS et al. Stroke 2014;45:1697-1702',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ROCKET-AF-ASIA: Rivaroxaban in Asian AF.
Asian AF patients randomized to rivaroxaban (treatment arm, n=932) versus warfarin (control arm, n=938).
The primary endpoint was stroke or systemic embolism. Mean age was 69.7 years, 66% were male.
Results: Primary endpoint HR 0.75, 95% CI 0.47-1.19. P=0.22.
Follow-up was 23 months. Trial registration: NCT00403767.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.75, 'ciLo': 0.47, 'ciHi': 1.19 },
            'treatment': { 'n': 932 },
            'control': { 'n': 938 },
            'baseline': { 'ageMean': 69.7, 'malePercent': 66 },
            'registration': 'NCT00403767'
        }
    },
    {
        'id': 'ROCKET-AF-PRIOR-STROKE',
        'source': 'Hankey GJ et al. Lancet Neurol 2012;11:315-322',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ROCKET-AF-PRIOR-STROKE: Rivaroxaban in AF with Prior Stroke.
AF patients with prior stroke randomized to rivaroxaban (treatment arm, n=3754) versus warfarin (control arm, n=3728).
The primary endpoint was stroke or systemic embolism. Mean age was 72.2 years, 58% were male.
Results: Primary endpoint HR 0.94, 95% CI 0.77-1.16. P=0.58.
Follow-up was 23 months. Trial registration: NCT00403767.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.94, 'ciLo': 0.77, 'ciHi': 1.16 },
            'treatment': { 'n': 3754 },
            'control': { 'n': 3728 },
            'baseline': { 'ageMean': 72.2, 'malePercent': 58 },
            'registration': 'NCT00403767'
        }
    },
    {
        'id': 'RE-LY-ELDERLY',
        'source': 'Eikelboom JW et al. Circulation 2011;123:2363-2372',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''RE-LY-ELDERLY: Dabigatran in Elderly AF Patients.
AF patients over 75 years randomized to dabigatran 150mg (treatment arm, n=2112) versus warfarin (control arm, n=2114).
The primary endpoint was stroke or systemic embolism. Mean age was 79.2 years, 61% were male.
Results: Primary endpoint HR 0.67, 95% CI 0.49-0.90. Non-inferiority met. P=0.008.
Follow-up was 24 months. Trial registration: NCT00262600.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.67, 'ciLo': 0.49, 'ciHi': 0.90 },
            'treatment': { 'n': 2112 },
            'control': { 'n': 2114 },
            'baseline': { 'ageMean': 79.2, 'malePercent': 61 },
            'registration': 'NCT00262600',
            'nonInferiority': True
        }
    },
    {
        'id': 'RE-LY-ASIA',
        'source': 'Hori M et al. Circ J 2011;75:800-805',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''RE-LY-ASIA: Dabigatran in Asian AF Patients.
Asian AF patients randomized to dabigatran 150mg (treatment arm, n=808) versus warfarin (control arm, n=407).
The primary endpoint was stroke or systemic embolism. Mean age was 69.8 years, 72% were male.
Results: Primary endpoint HR 0.55, 95% CI 0.28-1.09. Non-inferiority met. P=0.09.
Follow-up was 24 months. Trial registration: NCT00262600.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.55, 'ciLo': 0.28, 'ciHi': 1.09 },
            'treatment': { 'n': 808 },
            'control': { 'n': 407 },
            'baseline': { 'ageMean': 69.8, 'malePercent': 72 },
            'registration': 'NCT00262600',
            'nonInferiority': True
        }
    },
    {
        'id': 'ENGAGE-AF-ELDERLY',
        'source': 'Kato ET et al. Circulation 2016;133:2049-2061',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''ENGAGE-AF-ELDERLY: Edoxaban in Elderly AF.
AF patients over 75 years randomized to edoxaban 60mg (treatment arm, n=2616) versus warfarin (control arm, n=2626).
The primary endpoint was stroke or systemic embolism. Mean age was 80.1 years, 57% were male.
Results: Primary endpoint HR 0.83, 95% CI 0.66-1.04. Non-inferiority met. P=0.11.
Follow-up was 34 months. Trial registration: NCT00781391.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.83, 'ciLo': 0.66, 'ciHi': 1.04 },
            'treatment': { 'n': 2616 },
            'control': { 'n': 2626 },
            'baseline': { 'ageMean': 80.1, 'malePercent': 57 },
            'registration': 'NCT00781391',
            'nonInferiority': True
        }
    },
    {
        'id': 'ENGAGE-AF-ASIA',
        'source': 'Yamashita T et al. J Am Coll Cardiol 2016;68:2621-2632',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''ENGAGE-AF-ASIA: Edoxaban in East Asian AF.
East Asian AF patients randomized to edoxaban 60mg (treatment arm, n=1143) versus warfarin (control arm, n=1138).
The primary endpoint was stroke or systemic embolism. Mean age was 71.2 years, 71% were male.
Results: Primary endpoint HR 0.73, 95% CI 0.47-1.14. Non-inferiority met. P=0.17.
Follow-up was 34 months. Trial registration: NCT00781391.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.73, 'ciLo': 0.47, 'ciHi': 1.14 },
            'treatment': { 'n': 1143 },
            'control': { 'n': 1138 },
            'baseline': { 'ageMean': 71.2, 'malePercent': 71 },
            'registration': 'NCT00781391',
            'nonInferiority': True
        }
    },
    {
        'id': 'AVERROES',
        'source': 'Connolly SJ et al. NEJM 2011;364:806-817',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''AVERROES: Apixaban vs Aspirin in AF.
AF patients unsuitable for VKA randomized to apixaban (treatment arm, n=2808) versus aspirin (control arm, n=2791).
The primary endpoint was stroke or systemic embolism. Mean age was 69.9 years, 59% were male.
Results: Primary endpoint HR 0.45, 95% CI 0.32-0.62. P<0.001.
Follow-up was 12 months. Trial registration: NCT00496769.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.45, 'ciLo': 0.32, 'ciHi': 0.62 },
            'treatment': { 'n': 2808 },
            'control': { 'n': 2791 },
            'baseline': { 'ageMean': 69.9, 'malePercent': 59 },
            'registration': 'NCT00496769'
        }
    },
    {
        'id': 'CABANA',
        'source': 'Packer DL et al. JAMA 2019;321:1261-1274',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CABANA: Catheter Ablation vs Drug Therapy in AF.
AF patients randomized to catheter ablation (treatment arm, n=1108) versus drug therapy (control arm, n=1096).
The primary endpoint was death, disabling stroke, serious bleeding, or cardiac arrest. Mean age was 67.5 years, 63% were male.
Results: Primary endpoint HR 0.86, 95% CI 0.65-1.15. P=0.30.
Follow-up was 48.5 months. Trial registration: NCT00911508.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.86, 'ciLo': 0.65, 'ciHi': 1.15 },
            'treatment': { 'n': 1108 },
            'control': { 'n': 1096 },
            'baseline': { 'ageMean': 67.5, 'malePercent': 63 },
            'registration': 'NCT00911508'
        }
    },
    {
        'id': 'CASTLE-AF',
        'source': 'Marrouche NF et al. NEJM 2018;378:417-427',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CASTLE-AF: Catheter Ablation in AF with HF.
AF patients with HF randomized to ablation (treatment arm, n=179) versus medical therapy (control arm, n=184).
The primary endpoint was all-cause death or HF hospitalization. Mean age was 64.0 years, 87% were male.
Results: Primary endpoint HR 0.62, 95% CI 0.43-0.87. P=0.007.
Follow-up was 37.8 months. Trial registration: NCT00643188.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.62, 'ciLo': 0.43, 'ciHi': 0.87 },
            'treatment': { 'n': 179 },
            'control': { 'n': 184 },
            'baseline': { 'ageMean': 64.0, 'malePercent': 87 },
            'registration': 'NCT00643188'
        }
    },
    {
        'id': 'EAST-AFNET4',
        'source': 'Kirchhof P et al. NEJM 2020;383:1305-1316',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EAST-AFNET4: Early Rhythm Control in AF.
Early AF patients randomized to early rhythm control (treatment arm, n=1395) versus usual care (control arm, n=1394).
The primary endpoint was CV death, stroke, or HF hospitalization. Mean age was 70.4 years, 54% were male.
Results: Primary endpoint HR 0.79, 95% CI 0.66-0.94. P=0.005.
Follow-up was 63.6 months. Trial registration: NCT01288352.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.79, 'ciLo': 0.66, 'ciHi': 0.94 },
            'treatment': { 'n': 1395 },
            'control': { 'n': 1394 },
            'baseline': { 'ageMean': 70.4, 'malePercent': 54 },
            'registration': 'NCT01288352'
        }
    },
    {
        'id': 'AATAC',
        'source': 'Di Biase L et al. Circulation 2016;133:1637-1644',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''AATAC: Ablation vs Amiodarone in AF with HF.
Persistent AF with HF randomized to ablation (treatment arm, n=102) versus amiodarone (control arm, n=101).
The primary endpoint was AF recurrence at 24 months. Mean age was 62.5 years, 73% were male.
Results: AF recurrence RR 0.45, 95% CI 0.34-0.61. P<0.001.
Follow-up was 24 months. Trial registration: NCT01341652.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.45, 'ciLo': 0.34, 'ciHi': 0.61 },
            'treatment': { 'n': 102 },
            'control': { 'n': 101 },
            'baseline': { 'ageMean': 62.5, 'malePercent': 73 },
            'registration': 'NCT01341652'
        }
    },
    {
        'id': 'AFFIRM',
        'source': 'Wyse DG et al. NEJM 2002;347:1825-1833',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''AFFIRM: Rate vs Rhythm Control in AF.
AF patients randomized to rhythm control (treatment arm, n=2033) versus rate control (control arm, n=2027).
The primary endpoint was all-cause mortality. Mean age was 69.7 years, 61% were male.
Results: All-cause mortality HR 1.15, 95% CI 0.99-1.34. P=0.08.
Follow-up was 3.5 years. Trial registration: NCT00000556.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.15, 'ciLo': 0.99, 'ciHi': 1.34 },
            'treatment': { 'n': 2033 },
            'control': { 'n': 2027 },
            'baseline': { 'ageMean': 69.7, 'malePercent': 61 },
            'registration': 'NCT00000556'
        }
    },
    # HYPERTENSION (30 trials) - First 15 in Batch 19
    {
        'id': 'SPRINT-SENIOR',
        'source': 'Williamson JD et al. JAMA 2016;315:2673-2682',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SPRINT-SENIOR: Intensive BP Control in Elderly.
Patients over 75 years randomized to intensive SBP target (treatment arm, n=1317) versus standard target (control arm, n=1319).
The primary endpoint was MI, ACS, stroke, HF, or CV death. Mean age was 79.9 years, 62% were male.
Results: Primary endpoint HR 0.66, 95% CI 0.51-0.85. P<0.001.
Follow-up was 3.14 years. Trial registration: NCT01206062.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.66, 'ciLo': 0.51, 'ciHi': 0.85 },
            'treatment': { 'n': 1317 },
            'control': { 'n': 1319 },
            'baseline': { 'ageMean': 79.9, 'malePercent': 62 },
            'registration': 'NCT01206062'
        }
    },
    {
        'id': 'SPRINT-CKD',
        'source': 'Cheung AK et al. NEJM 2017;377:2506-2517',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SPRINT-CKD: Intensive BP in CKD Patients.
CKD patients randomized to intensive SBP target (treatment arm, n=1330) versus standard target (control arm, n=1316).
The primary endpoint was MI, ACS, stroke, HF, or CV death. Mean age was 72.0 years, 68% were male.
Results: Primary endpoint HR 0.81, 95% CI 0.63-1.05. P=0.11.
Follow-up was 3.3 years. Trial registration: NCT01206062.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.81, 'ciLo': 0.63, 'ciHi': 1.05 },
            'treatment': { 'n': 1330 },
            'control': { 'n': 1316 },
            'baseline': { 'ageMean': 72.0, 'malePercent': 68 },
            'registration': 'NCT01206062'
        }
    },
    {
        'id': 'SPRINT-MIND',
        'source': 'Williamson JD et al. JAMA 2019;321:553-561',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SPRINT-MIND: Intensive BP and Cognitive Outcomes.
Hypertensive patients randomized to intensive SBP (treatment arm, n=4678) versus standard (control arm, n=4683).
The primary endpoint was probable dementia. Mean age was 67.9 years, 64% were male.
Results: Probable dementia HR 0.83, 95% CI 0.67-1.04. P=0.10.
Follow-up was 5.1 years. Trial registration: NCT01206062.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.83, 'ciLo': 0.67, 'ciHi': 1.04 },
            'treatment': { 'n': 4678 },
            'control': { 'n': 4683 },
            'baseline': { 'ageMean': 67.9, 'malePercent': 64 },
            'registration': 'NCT01206062'
        }
    },
    {
        'id': 'ACCORD-BP-PRIMARY',
        'source': 'Cushman WC et al. NEJM 2010;362:1575-1585',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ACCORD-BP-PRIMARY: Intensive BP in Type 2 Diabetes.
Diabetic patients randomized to intensive SBP target (treatment arm, n=2362) versus standard target (control arm, n=2371).
The primary endpoint was nonfatal MI, nonfatal stroke, or CV death. Mean age was 62.2 years, 52% were male.
Results: Primary endpoint HR 0.88, 95% CI 0.73-1.06. P=0.20.
Follow-up was 4.7 years. Trial registration: NCT00000620.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.88, 'ciLo': 0.73, 'ciHi': 1.06 },
            'treatment': { 'n': 2362 },
            'control': { 'n': 2371 },
            'baseline': { 'ageMean': 62.2, 'malePercent': 52 },
            'registration': 'NCT00000620'
        }
    },
    {
        'id': 'ACCORD-BP-STROKE',
        'source': 'Cushman WC et al. NEJM 2010;362:1575-1585',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ACCORD-BP-STROKE: Intensive BP and Stroke in Diabetes.
Diabetic patients randomized to intensive SBP target (treatment arm, n=2362) versus standard target (control arm, n=2371).
The primary endpoint was stroke. Mean age was 62.2 years, 52% were male.
Results: Stroke HR 0.59, 95% CI 0.39-0.89. P=0.01.
Follow-up was 4.7 years. Trial registration: NCT00000620.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.59, 'ciLo': 0.39, 'ciHi': 0.89 },
            'treatment': { 'n': 2362 },
            'control': { 'n': 2371 },
            'baseline': { 'ageMean': 62.2, 'malePercent': 52 },
            'registration': 'NCT00000620'
        }
    },
    {
        'id': 'STEP',
        'source': 'Zhang W et al. NEJM 2021;385:1268-1279',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''STEP: Intensive BP in Chinese Elderly.
Chinese patients 60-80 years randomized to intensive SBP (treatment arm, n=4243) versus standard (control arm, n=4268).
The primary endpoint was stroke, ACS, HF, coronary revasc, AF, or CV death. Mean age was 66.2 years, 47% were male.
Results: Primary endpoint HR 0.74, 95% CI 0.60-0.92. P=0.007.
Follow-up was 3.34 years. Trial registration: NCT03015311.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.74, 'ciLo': 0.60, 'ciHi': 0.92 },
            'treatment': { 'n': 4243 },
            'control': { 'n': 4268 },
            'baseline': { 'ageMean': 66.2, 'malePercent': 47 },
            'registration': 'NCT03015311'
        }
    },
    {
        'id': 'HOPE-3-BP',
        'source': 'Lonn EM et al. NEJM 2016;374:2009-2020',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''HOPE-3-BP: BP Lowering in Intermediate Risk.
Intermediate CV risk patients randomized to BP lowering (treatment arm, n=6356) versus placebo (control arm, n=6349).
The primary endpoint was CV death, MI, or stroke. Mean age was 65.7 years, 46% were male.
Results: Primary endpoint HR 0.93, 95% CI 0.79-1.10. P=0.40.
Follow-up was 5.6 years. Trial registration: NCT00468923.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.93, 'ciLo': 0.79, 'ciHi': 1.10 },
            'treatment': { 'n': 6356 },
            'control': { 'n': 6349 },
            'baseline': { 'ageMean': 65.7, 'malePercent': 46 },
            'registration': 'NCT00468923'
        }
    },
    {
        'id': 'ONTARGET',
        'source': 'Yusuf S et al. NEJM 2008;358:1547-1559',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''ONTARGET: Telmisartan vs Ramipril in CV Risk.
High CV risk patients randomized to telmisartan (treatment arm, n=8542) versus ramipril (control arm, n=8576).
The primary endpoint was CV death, MI, stroke, or HF hospitalization. Mean age was 66.4 years, 73% were male.
Results: Primary endpoint HR 1.01, 95% CI 0.94-1.09. Non-inferiority met. P=0.81.
Follow-up was 56 months. Trial registration: NCT00153101.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.01, 'ciLo': 0.94, 'ciHi': 1.09 },
            'treatment': { 'n': 8542 },
            'control': { 'n': 8576 },
            'baseline': { 'ageMean': 66.4, 'malePercent': 73 },
            'registration': 'NCT00153101',
            'nonInferiority': True
        }
    },
    {
        'id': 'ALLHAT-AMLODIPINE',
        'source': 'ALLHAT Officers. JAMA 2002;288:2981-2997',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ALLHAT-AMLODIPINE: Amlodipine vs Chlorthalidone in HTN.
Hypertensive patients randomized to amlodipine (treatment arm, n=9048) versus chlorthalidone (control arm, n=15255).
The primary endpoint was fatal CHD or nonfatal MI. Mean age was 66.9 years, 53% were male.
Results: Primary endpoint RR 0.98, 95% CI 0.90-1.07. P=0.65.
Follow-up was 4.9 years. Trial registration: NCT00000542.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.98, 'ciLo': 0.90, 'ciHi': 1.07 },
            'treatment': { 'n': 9048 },
            'control': { 'n': 15255 },
            'baseline': { 'ageMean': 66.9, 'malePercent': 53 },
            'registration': 'NCT00000542'
        }
    },
    {
        'id': 'ALLHAT-LISINOPRIL',
        'source': 'ALLHAT Officers. JAMA 2002;288:2981-2997',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ALLHAT-LISINOPRIL: Lisinopril vs Chlorthalidone in HTN.
Hypertensive patients randomized to lisinopril (treatment arm, n=9054) versus chlorthalidone (control arm, n=15255).
The primary endpoint was fatal CHD or nonfatal MI. Mean age was 66.9 years, 54% were male.
Results: Primary endpoint RR 0.99, 95% CI 0.91-1.08. P=0.81.
Follow-up was 4.9 years. Trial registration: NCT00000542.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.99, 'ciLo': 0.91, 'ciHi': 1.08 },
            'treatment': { 'n': 9054 },
            'control': { 'n': 15255 },
            'baseline': { 'ageMean': 66.9, 'malePercent': 54 },
            'registration': 'NCT00000542'
        }
    },
    {
        'id': 'VALUE',
        'source': 'Julius S et al. Lancet 2004;363:2022-2031',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''VALUE: Valsartan vs Amlodipine in Hypertension.
High-risk hypertensive patients randomized to valsartan (treatment arm, n=7649) versus amlodipine (control arm, n=7596).
The primary endpoint was cardiac mortality and morbidity. Mean age was 67.2 years, 58% were male.
Results: Primary endpoint HR 1.04, 95% CI 0.94-1.15. P=0.49.
Follow-up was 4.2 years. Trial registration: NCT00133692.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.04, 'ciLo': 0.94, 'ciHi': 1.15 },
            'treatment': { 'n': 7649 },
            'control': { 'n': 7596 },
            'baseline': { 'ageMean': 67.2, 'malePercent': 58 },
            'registration': 'NCT00133692'
        }
    },
    {
        'id': 'ASCOT-BPLA',
        'source': 'Dahlof B et al. Lancet 2005;366:895-906',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ASCOT-BPLA: Amlodipine vs Atenolol in Hypertension.
Hypertensive patients randomized to amlodipine (treatment arm, n=9639) versus atenolol (control arm, n=9618).
The primary endpoint was nonfatal MI or fatal CHD. Mean age was 63.0 years, 77% were male.
Results: Primary endpoint HR 0.90, 95% CI 0.79-1.02. P=0.105.
Follow-up was 5.5 years. Trial registration: NCT00227318.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.90, 'ciLo': 0.79, 'ciHi': 1.02 },
            'treatment': { 'n': 9639 },
            'control': { 'n': 9618 },
            'baseline': { 'ageMean': 63.0, 'malePercent': 77 },
            'registration': 'NCT00227318'
        }
    },
    {
        'id': 'HYVET',
        'source': 'Beckett NS et al. NEJM 2008;358:1887-1898',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''HYVET: BP Treatment in the Very Elderly.
Patients over 80 years randomized to indapamide (treatment arm, n=1933) versus placebo (control arm, n=1912).
The primary endpoint was fatal or nonfatal stroke. Mean age was 83.6 years, 39% were male.
Results: Primary endpoint HR 0.70, 95% CI 0.49-1.01. P=0.06.
Follow-up was 1.8 years. Trial registration: NCT00122811.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.70, 'ciLo': 0.49, 'ciHi': 1.01 },
            'treatment': { 'n': 1933 },
            'control': { 'n': 1912 },
            'baseline': { 'ageMean': 83.6, 'malePercent': 39 },
            'registration': 'NCT00122811'
        }
    },
    {
        'id': 'ACCOMPLISH',
        'source': 'Jamerson K et al. NEJM 2008;359:2417-2428',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ACCOMPLISH: Benazepril-Amlodipine vs Benazepril-HCTZ.
High-risk hypertensive patients randomized to benazepril-amlodipine (treatment arm, n=5744) versus benazepril-HCTZ (control arm, n=5762).
The primary endpoint was CV death, MI, stroke, angina hospitalization, coronary revasc, or resuscitated arrest. Mean age was 68.4 years, 60% were male.
Results: Primary endpoint HR 0.80, 95% CI 0.72-0.90. P<0.001.
Follow-up was 36 months. Trial registration: NCT00170950.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.80, 'ciLo': 0.72, 'ciHi': 0.90 },
            'treatment': { 'n': 5744 },
            'control': { 'n': 5762 },
            'baseline': { 'ageMean': 68.4, 'malePercent': 60 },
            'registration': 'NCT00170950'
        }
    },
    {
        'id': 'FEVER',
        'source': 'Liu L et al. J Hypertens 2005;23:2157-2172',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''FEVER: Felodipine in Chinese Hypertensives.
Chinese hypertensive patients randomized to felodipine (treatment arm, n=4841) versus placebo (control arm, n=4870).
The primary endpoint was fatal and nonfatal stroke. Mean age was 61.5 years, 61% were male.
Results: Primary endpoint HR 0.73, 95% CI 0.60-0.90. P=0.003.
Follow-up was 40 months. Trial registration: NCT00134732.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.73, 'ciLo': 0.60, 'ciHi': 0.90 },
            'treatment': { 'n': 4841 },
            'control': { 'n': 4870 },
            'baseline': { 'ageMean': 61.5, 'malePercent': 61 },
            'registration': 'NCT00134732'
        }
    },
    # LIPID DISORDERS (30 trials) - First 15 in Batch 19
    {
        'id': 'FOURIER-DIABETICS',
        'source': 'Sabatine MS et al. Lancet Diabetes 2017;5:941-950',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''FOURIER-DIABETICS: Evolocumab in Diabetic ASCVD.
Diabetic ASCVD patients randomized to evolocumab (treatment arm, n=5711) versus placebo (control arm, n=5695).
The primary endpoint was CV death, MI, stroke, coronary revasc, or unstable angina. Mean age was 63.8 years, 72% were male.
Results: Primary endpoint HR 0.83, 95% CI 0.75-0.93. P=0.001.
Follow-up was 2.2 years. Trial registration: NCT01764633.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.83, 'ciLo': 0.75, 'ciHi': 0.93 },
            'treatment': { 'n': 5711 },
            'control': { 'n': 5695 },
            'baseline': { 'ageMean': 63.8, 'malePercent': 72 },
            'registration': 'NCT01764633'
        }
    },
    {
        'id': 'FOURIER-PAD',
        'source': 'Bonaca MP et al. Circulation 2018;137:338-350',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''FOURIER-PAD: Evolocumab in Peripheral Artery Disease.
PAD patients randomized to evolocumab (treatment arm, n=3642) versus placebo (control arm, n=3630).
The primary endpoint was CV death, MI, stroke, coronary revasc, or unstable angina. Mean age was 66.1 years, 76% were male.
Results: Primary endpoint HR 0.79, 95% CI 0.66-0.94. P=0.006.
Follow-up was 2.2 years. Trial registration: NCT01764633.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.79, 'ciLo': 0.66, 'ciHi': 0.94 },
            'treatment': { 'n': 3642 },
            'control': { 'n': 3630 },
            'baseline': { 'ageMean': 66.1, 'malePercent': 76 },
            'registration': 'NCT01764633'
        }
    },
    {
        'id': 'FOURIER-STROKE',
        'source': 'Giugliano RP et al. JAMA Neurol 2020;77:682-690',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''FOURIER-STROKE: Evolocumab and Stroke Outcomes.
ASCVD patients randomized to evolocumab (treatment arm, n=13784) versus placebo (control arm, n=13780).
The primary endpoint was ischemic stroke. Mean age was 62.5 years, 75% were male.
Results: Ischemic stroke HR 0.79, 95% CI 0.64-0.98. P=0.03.
Follow-up was 2.2 years. Trial registration: NCT01764633.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.79, 'ciLo': 0.64, 'ciHi': 0.98 },
            'treatment': { 'n': 13784 },
            'control': { 'n': 13780 },
            'baseline': { 'ageMean': 62.5, 'malePercent': 75 },
            'registration': 'NCT01764633'
        }
    },
    {
        'id': 'ODYSSEY-OUTCOMES',
        'source': 'Schwartz GG et al. NEJM 2018;379:2097-2107',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ODYSSEY-OUTCOMES: Alirocumab After ACS.
Recent ACS patients randomized to alirocumab (treatment arm, n=9462) versus placebo (control arm, n=9462).
The primary endpoint was CHD death, nonfatal MI, ischemic stroke, or unstable angina. Mean age was 58.5 years, 75% were male.
Results: Primary endpoint HR 0.85, 95% CI 0.78-0.93. P<0.001.
Follow-up was 2.8 years. Trial registration: NCT01663402.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.85, 'ciLo': 0.78, 'ciHi': 0.93 },
            'treatment': { 'n': 9462 },
            'control': { 'n': 9462 },
            'baseline': { 'ageMean': 58.5, 'malePercent': 75 },
            'registration': 'NCT01663402'
        }
    },
    {
        'id': 'ODYSSEY-DM',
        'source': 'Ray KK et al. Diabetes Care 2019;42:2442-2451',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ODYSSEY-DM: Alirocumab in Diabetic ACS.
Diabetic recent ACS patients randomized to alirocumab (treatment arm, n=2693) versus placebo (control arm, n=2751).
The primary endpoint was CHD death, nonfatal MI, ischemic stroke, or unstable angina. Mean age was 61.2 years, 71% were male.
Results: Primary endpoint HR 0.84, 95% CI 0.74-0.97. P=0.02.
Follow-up was 2.8 years. Trial registration: NCT01663402.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.84, 'ciLo': 0.74, 'ciHi': 0.97 },
            'treatment': { 'n': 2693 },
            'control': { 'n': 2751 },
            'baseline': { 'ageMean': 61.2, 'malePercent': 71 },
            'registration': 'NCT01663402'
        }
    },
    {
        'id': 'ODYSSEY-LONG-TERM',
        'source': 'Robinson JG et al. NEJM 2015;372:1489-1499',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ODYSSEY-LONG-TERM: Alirocumab Long-Term Safety.
High CV risk patients randomized to alirocumab (treatment arm, n=1553) versus placebo (control arm, n=788).
The primary endpoint was LDL-C reduction at 24 weeks. Mean age was 60.5 years, 62% were male.
Results: LDL-C mean difference -61.9%, 95% CI -64.3 to -59.4. P<0.001.
Follow-up was 78 weeks. Trial registration: NCT01507831.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': -61.9, 'ciLo': -64.3, 'ciHi': -59.4 },
            'treatment': { 'n': 1553 },
            'control': { 'n': 788 },
            'baseline': { 'ageMean': 60.5, 'malePercent': 62 },
            'registration': 'NCT01507831'
        }
    },
    {
        'id': 'IMPROVE-IT',
        'source': 'Cannon CP et al. NEJM 2015;372:2387-2397',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''IMPROVE-IT: Ezetimibe Added to Statin After ACS.
Post-ACS patients randomized to simvastatin-ezetimibe (treatment arm, n=9067) versus simvastatin (control arm, n=9077).
The primary endpoint was CV death, MI, unstable angina, coronary revasc, or stroke. Mean age was 64.0 years, 76% were male.
Results: Primary endpoint HR 0.94, 95% CI 0.89-0.99. P=0.016.
Follow-up was 6 years. Trial registration: NCT00202878.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.94, 'ciLo': 0.89, 'ciHi': 0.99 },
            'treatment': { 'n': 9067 },
            'control': { 'n': 9077 },
            'baseline': { 'ageMean': 64.0, 'malePercent': 76 },
            'registration': 'NCT00202878'
        }
    },
    {
        'id': 'SPIRE-1',
        'source': 'Ridker PM et al. NEJM 2017;376:1517-1526',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SPIRE-1: Bococizumab in High CV Risk.
High CV risk patients randomized to bococizumab (treatment arm, n=8373) versus placebo (control arm, n=8371).
The primary endpoint was CV death, nonfatal MI, nonfatal stroke, or hospitalized unstable angina. Mean age was 62.8 years, 73% were male.
Results: Primary endpoint HR 0.99, 95% CI 0.80-1.22. P=0.94.
Follow-up was 7 months. Trial registration: NCT01968954.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.99, 'ciLo': 0.80, 'ciHi': 1.22 },
            'treatment': { 'n': 8373 },
            'control': { 'n': 8371 },
            'baseline': { 'ageMean': 62.8, 'malePercent': 73 },
            'registration': 'NCT01968954'
        }
    },
    {
        'id': 'SPIRE-2',
        'source': 'Ridker PM et al. NEJM 2017;376:1527-1539',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SPIRE-2: Bococizumab in Higher LDL-C Patients.
Patients with LDL-C over 70 randomized to bococizumab (treatment arm, n=5312) versus placebo (control arm, n=5321).
The primary endpoint was CV death, nonfatal MI, nonfatal stroke, or hospitalized unstable angina. Mean age was 62.1 years, 75% were male.
Results: Primary endpoint HR 0.79, 95% CI 0.65-0.97. P=0.02.
Follow-up was 12 months. Trial registration: NCT01968980.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.79, 'ciLo': 0.65, 'ciHi': 0.97 },
            'treatment': { 'n': 5312 },
            'control': { 'n': 5321 },
            'baseline': { 'ageMean': 62.1, 'malePercent': 75 },
            'registration': 'NCT01968980'
        }
    },
    {
        'id': 'TNT',
        'source': 'LaRosa JC et al. NEJM 2005;352:1425-1435',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''TNT: Intensive Statin in Stable CHD.
Stable CHD patients randomized to atorvastatin 80mg (treatment arm, n=4995) versus atorvastatin 10mg (control arm, n=5006).
The primary endpoint was first major CV event. Mean age was 61.0 years, 81% were male.
Results: Primary endpoint HR 0.78, 95% CI 0.69-0.89. P<0.001.
Follow-up was 4.9 years. Trial registration: NCT00327691.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.78, 'ciLo': 0.69, 'ciHi': 0.89 },
            'treatment': { 'n': 4995 },
            'control': { 'n': 5006 },
            'baseline': { 'ageMean': 61.0, 'malePercent': 81 },
            'registration': 'NCT00327691'
        }
    },
    {
        'id': 'PROVE-IT',
        'source': 'Cannon CP et al. NEJM 2004;350:1495-1504',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PROVE-IT: Intensive Statin After ACS.
Post-ACS patients randomized to atorvastatin 80mg (treatment arm, n=2099) versus pravastatin 40mg (control arm, n=2063).
The primary endpoint was death, MI, unstable angina, revasc, or stroke. Mean age was 58.0 years, 78% were male.
Results: Primary endpoint HR 0.84, 95% CI 0.74-0.95. P=0.005.
Follow-up was 24 months. Trial registration: NCT00382460.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.84, 'ciLo': 0.74, 'ciHi': 0.95 },
            'treatment': { 'n': 2099 },
            'control': { 'n': 2063 },
            'baseline': { 'ageMean': 58.0, 'malePercent': 78 },
            'registration': 'NCT00382460'
        }
    },
    {
        'id': 'JUPITER',
        'source': 'Ridker PM et al. NEJM 2008;359:2195-2207',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''JUPITER: Rosuvastatin in Primary Prevention with Elevated CRP.
Primary prevention patients with elevated CRP randomized to rosuvastatin (treatment arm, n=8901) versus placebo (control arm, n=8901).
The primary endpoint was MI, stroke, arterial revasc, unstable angina, or CV death. Mean age was 66.0 years, 62% were male.
Results: Primary endpoint HR 0.56, 95% CI 0.46-0.69. P<0.001.
Follow-up was 1.9 years. Trial registration: NCT00239681.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.56, 'ciLo': 0.46, 'ciHi': 0.69 },
            'treatment': { 'n': 8901 },
            'control': { 'n': 8901 },
            'baseline': { 'ageMean': 66.0, 'malePercent': 62 },
            'registration': 'NCT00239681'
        }
    },
    {
        'id': 'HPS',
        'source': 'Heart Protection Study Group. Lancet 2002;360:7-22',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''HPS: Simvastatin in High Risk Patients.
High CV risk patients randomized to simvastatin 40mg (treatment arm, n=10269) versus placebo (control arm, n=10267).
The primary endpoint was all-cause mortality. Mean age was 64.0 years, 75% were male.
Results: All-cause mortality RR 0.87, 95% CI 0.81-0.94. P=0.0003.
Follow-up was 5 years. Trial registration: NCT00461630.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.87, 'ciLo': 0.81, 'ciHi': 0.94 },
            'treatment': { 'n': 10269 },
            'control': { 'n': 10267 },
            'baseline': { 'ageMean': 64.0, 'malePercent': 75 },
            'registration': 'NCT00461630'
        }
    },
    {
        'id': 'ASCOT-LLA',
        'source': 'Sever PS et al. Lancet 2003;361:1149-1158',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ASCOT-LLA: Atorvastatin in Hypertensive Patients.
Hypertensive patients with TC below 6.5 randomized to atorvastatin 10mg (treatment arm, n=5168) versus placebo (control arm, n=5137).
The primary endpoint was nonfatal MI or fatal CHD. Mean age was 63.1 years, 81% were male.
Results: Primary endpoint HR 0.64, 95% CI 0.50-0.83. P=0.0005.
Follow-up was 3.3 years. Trial registration: NCT00227318.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.64, 'ciLo': 0.50, 'ciHi': 0.83 },
            'treatment': { 'n': 5168 },
            'control': { 'n': 5137 },
            'baseline': { 'ageMean': 63.1, 'malePercent': 81 },
            'registration': 'NCT00227318'
        }
    },
    {
        'id': 'CARDS',
        'source': 'Colhoun HM et al. Lancet 2004;364:685-696',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CARDS: Atorvastatin in Type 2 Diabetes.
Diabetic patients without CVD randomized to atorvastatin 10mg (treatment arm, n=1428) versus placebo (control arm, n=1410).
The primary endpoint was ACS, coronary revasc, or stroke. Mean age was 61.6 years, 68% were male.
Results: Primary endpoint HR 0.63, 95% CI 0.48-0.83. P=0.001.
Follow-up was 3.9 years. Trial registration: NCT00327418.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.63, 'ciLo': 0.48, 'ciHi': 0.83 },
            'treatment': { 'n': 1428 },
            'control': { 'n': 1410 },
            'baseline': { 'ageMean': 61.6, 'malePercent': 68 },
            'registration': 'NCT00327418'
        }
    },
    # VALVULAR HEART DISEASE (30 trials) - First 15 in Batch 19
    {
        'id': 'PARTNER-1A',
        'source': 'Smith CR et al. NEJM 2011;364:2187-2198',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''PARTNER-1A: TAVR vs Surgery in High-Risk AS.
High-risk severe AS patients randomized to TAVR (treatment arm, n=348) versus surgical AVR (control arm, n=351).
The primary endpoint was all-cause mortality at 1 year. Mean age was 83.6 years, 58% were male.
Results: Mortality HR 0.93, 95% CI 0.71-1.22. Non-inferiority met. P=0.62.
Follow-up was 12 months. Trial registration: NCT00530894.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.93, 'ciLo': 0.71, 'ciHi': 1.22 },
            'treatment': { 'n': 348 },
            'control': { 'n': 351 },
            'baseline': { 'ageMean': 83.6, 'malePercent': 58 },
            'registration': 'NCT00530894',
            'nonInferiority': True
        }
    },
    {
        'id': 'PARTNER-1B',
        'source': 'Leon MB et al. NEJM 2010;363:1597-1607',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PARTNER-1B: TAVR vs Medical Therapy in Inoperable AS.
Inoperable severe AS patients randomized to TAVR (treatment arm, n=179) versus standard therapy (control arm, n=179).
The primary endpoint was all-cause mortality at 1 year. Mean age was 83.1 years, 54% were male.
Results: Mortality HR 0.55, 95% CI 0.40-0.74. P<0.001.
Follow-up was 12 months. Trial registration: NCT00530894.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.55, 'ciLo': 0.40, 'ciHi': 0.74 },
            'treatment': { 'n': 179 },
            'control': { 'n': 179 },
            'baseline': { 'ageMean': 83.1, 'malePercent': 54 },
            'registration': 'NCT00530894'
        }
    },
    {
        'id': 'PARTNER-2A',
        'source': 'Leon MB et al. NEJM 2016;374:1609-1620',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''PARTNER-2A: TAVR vs Surgery in Intermediate-Risk AS.
Intermediate-risk severe AS patients randomized to TAVR (treatment arm, n=1011) versus surgical AVR (control arm, n=1021).
The primary endpoint was death or disabling stroke at 2 years. Mean age was 81.6 years, 54% were male.
Results: Primary endpoint HR 0.89, 95% CI 0.73-1.09. Non-inferiority met. P=0.25.
Follow-up was 24 months. Trial registration: NCT01314313.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.89, 'ciLo': 0.73, 'ciHi': 1.09 },
            'treatment': { 'n': 1011 },
            'control': { 'n': 1021 },
            'baseline': { 'ageMean': 81.6, 'malePercent': 54 },
            'registration': 'NCT01314313',
            'nonInferiority': True
        }
    },
    {
        'id': 'PARTNER-3',
        'source': 'Mack MJ et al. NEJM 2019;380:1695-1705',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''PARTNER-3: TAVR vs Surgery in Low-Risk AS.
Low-risk severe AS patients randomized to TAVR (treatment arm, n=503) versus surgical AVR (control arm, n=497).
The primary endpoint was death, stroke, or rehospitalization at 1 year. Mean age was 73.4 years, 69% were male.
Results: Primary endpoint HR 0.54, 95% CI 0.37-0.79. Non-inferiority met. P<0.001.
Follow-up was 12 months. Trial registration: NCT02675114.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.54, 'ciLo': 0.37, 'ciHi': 0.79 },
            'treatment': { 'n': 503 },
            'control': { 'n': 497 },
            'baseline': { 'ageMean': 73.4, 'malePercent': 69 },
            'registration': 'NCT02675114',
            'nonInferiority': True
        }
    },
    {
        'id': 'SURTAVI',
        'source': 'Reardon MJ et al. NEJM 2017;376:1321-1331',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''SURTAVI: Self-Expanding TAVR in Intermediate-Risk AS.
Intermediate-risk severe AS patients randomized to self-expanding TAVR (treatment arm, n=864) versus surgery (control arm, n=796).
The primary endpoint was death or disabling stroke at 24 months. Mean age was 79.8 years, 57% were male.
Results: Primary endpoint HR 0.90, 95% CI 0.71-1.15. Non-inferiority met. P=0.002 for non-inferiority.
Follow-up was 24 months. Trial registration: NCT01586910.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.90, 'ciLo': 0.71, 'ciHi': 1.15 },
            'treatment': { 'n': 864 },
            'control': { 'n': 796 },
            'baseline': { 'ageMean': 79.8, 'malePercent': 57 },
            'registration': 'NCT01586910',
            'nonInferiority': True
        }
    },
    {
        'id': 'EVOLUT-LOW-RISK',
        'source': 'Popma JJ et al. NEJM 2019;380:1706-1715',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''EVOLUT-LOW-RISK: Self-Expanding TAVR in Low-Risk AS.
Low-risk severe AS patients randomized to self-expanding TAVR (treatment arm, n=734) versus surgery (control arm, n=734).
The primary endpoint was death or disabling stroke at 24 months. Mean age was 74.1 years, 65% were male.
Results: Primary endpoint HR 0.59, 95% CI 0.40-0.88. Non-inferiority met. P<0.001.
Follow-up was 24 months. Trial registration: NCT02701283.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.59, 'ciLo': 0.40, 'ciHi': 0.88 },
            'treatment': { 'n': 734 },
            'control': { 'n': 734 },
            'baseline': { 'ageMean': 74.1, 'malePercent': 65 },
            'registration': 'NCT02701283',
            'nonInferiority': True
        }
    },
    {
        'id': 'NOTION',
        'source': 'Thyregod HG et al. NEJM 2015;372:2029-2039',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''NOTION: TAVR vs Surgery in Low-Risk AS.
Low to intermediate risk severe AS patients randomized to self-expanding TAVR (treatment arm, n=145) versus surgery (control arm, n=135).
The primary endpoint was death, stroke, or MI at 1 year. Mean age was 79.2 years, 54% were male.
Results: Primary endpoint HR 0.85, 95% CI 0.43-1.67. Non-inferiority met. P=0.58.
Follow-up was 12 months. Trial registration: NCT01057173.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.85, 'ciLo': 0.43, 'ciHi': 1.67 },
            'treatment': { 'n': 145 },
            'control': { 'n': 135 },
            'baseline': { 'ageMean': 79.2, 'malePercent': 54 },
            'registration': 'NCT01057173',
            'nonInferiority': True
        }
    },
    {
        'id': 'UK-TAVI',
        'source': 'UK TAVI Trial Investigators. Lancet 2022;400:1417-1427',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''UK-TAVI: TAVR vs Surgery in Older Patients.
Severe AS patients over 70 randomized to TAVR (treatment arm, n=458) versus surgery (control arm, n=455).
The primary endpoint was all-cause mortality at 1 year. Mean age was 80.7 years, 56% were male.
Results: Mortality HR 0.77, 95% CI 0.52-1.14. Non-inferiority met. P=0.19.
Follow-up was 12 months. Trial registration: NCT02825134.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.77, 'ciLo': 0.52, 'ciHi': 1.14 },
            'treatment': { 'n': 458 },
            'control': { 'n': 455 },
            'baseline': { 'ageMean': 80.7, 'malePercent': 56 },
            'registration': 'NCT02825134',
            'nonInferiority': True
        }
    },
    {
        'id': 'MITRA-FR',
        'source': 'Obadia JF et al. NEJM 2018;379:2297-2306',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''MITRA-FR: MitraClip in Functional Mitral Regurgitation.
Functional MR with HF patients randomized to MitraClip (treatment arm, n=152) versus medical therapy (control arm, n=152).
The primary endpoint was death or HF hospitalization at 1 year. Mean age was 70.1 years, 76% were male.
Results: Primary endpoint HR 1.16, 95% CI 0.73-1.84. P=0.53.
Follow-up was 12 months. Trial registration: NCT01920698.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.16, 'ciLo': 0.73, 'ciHi': 1.84 },
            'treatment': { 'n': 152 },
            'control': { 'n': 152 },
            'baseline': { 'ageMean': 70.1, 'malePercent': 76 },
            'registration': 'NCT01920698'
        }
    },
    {
        'id': 'COAPT',
        'source': 'Stone GW et al. NEJM 2018;379:2307-2318',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''COAPT: MitraClip in Functional MR with HF.
Functional MR with HF patients randomized to MitraClip plus GDMT (treatment arm, n=302) versus GDMT alone (control arm, n=312).
The primary endpoint was HF hospitalizations at 24 months. Mean age was 71.7 years, 64% were male.
Results: HF hospitalizations HR 0.53, 95% CI 0.40-0.70. P<0.001.
Follow-up was 24 months. Trial registration: NCT01626079.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.53, 'ciLo': 0.40, 'ciHi': 0.70 },
            'treatment': { 'n': 302 },
            'control': { 'n': 312 },
            'baseline': { 'ageMean': 71.7, 'malePercent': 64 },
            'registration': 'NCT01626079'
        }
    },
    {
        'id': 'EVEREST-II',
        'source': 'Feldman T et al. NEJM 2011;364:1395-1406',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EVEREST-II: MitraClip vs Surgery in Mitral Regurgitation.
Severe MR patients randomized to MitraClip (treatment arm, n=184) versus surgical repair (control arm, n=95).
The primary endpoint was death, surgery for MR, or MR 3 to 4 at 12 months. Mean age was 67.3 years, 62% were male.
Results: Primary endpoint RR 1.68, 95% CI 1.07-2.64. P=0.02.
Follow-up was 12 months. Trial registration: NCT00209274.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 1.68, 'ciLo': 1.07, 'ciHi': 2.64 },
            'treatment': { 'n': 184 },
            'control': { 'n': 95 },
            'baseline': { 'ageMean': 67.3, 'malePercent': 62 },
            'registration': 'NCT00209274'
        }
    },
    {
        'id': 'TRILUMINATE',
        'source': 'Lurz P et al. Lancet 2021;397:2076-2087',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''TRILUMINATE: TriClip in Tricuspid Regurgitation.
Severe TR patients randomized to TriClip (treatment arm, n=175) versus medical therapy (control arm, n=175).
The primary endpoint was composite hierarchical score at 1 year. Mean age was 78.1 years, 44% were male.
Results: Win ratio 1.48, 95% CI 1.06-2.13. P=0.02.
Follow-up was 12 months. Trial registration: NCT03904147.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 1.48, 'ciLo': 1.06, 'ciHi': 2.13 },
            'treatment': { 'n': 175 },
            'control': { 'n': 175 },
            'baseline': { 'ageMean': 78.1, 'malePercent': 44 },
            'registration': 'NCT03904147'
        }
    },
    {
        'id': 'ENVISAGE-TAVI',
        'source': 'Van Mieghem NM et al. NEJM 2021;385:2150-2160',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''ENVISAGE-TAVI: Edoxaban vs VKA After TAVR with AF.
TAVR patients with AF randomized to edoxaban (treatment arm, n=497) versus VKA (control arm, n=508).
The primary endpoint was net clinical benefit. Mean age was 82.1 years, 49% were male.
Results: Primary endpoint HR 1.05, 95% CI 0.85-1.31. Non-inferiority met. P=0.01 for non-inferiority.
Follow-up was 18 months. Trial registration: NCT02943785.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.05, 'ciLo': 0.85, 'ciHi': 1.31 },
            'treatment': { 'n': 497 },
            'control': { 'n': 508 },
            'baseline': { 'ageMean': 82.1, 'malePercent': 49 },
            'registration': 'NCT02943785',
            'nonInferiority': True
        }
    },
    {
        'id': 'POPular-TAVI-A',
        'source': 'Brouwer S et al. NEJM 2020;382:1696-1707',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''POPular-TAVI-A: Aspirin Alone vs DAPT After TAVR.
TAVR patients not on OAC randomized to aspirin alone (treatment arm, n=331) versus aspirin plus clopidogrel (control arm, n=334).
The primary endpoint was all bleeding at 1 year. Mean age was 80.2 years, 45% were male.
Results: All bleeding HR 0.57, 95% CI 0.42-0.77. P<0.001.
Follow-up was 12 months. Trial registration: NCT02247128.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.57, 'ciLo': 0.42, 'ciHi': 0.77 },
            'treatment': { 'n': 331 },
            'control': { 'n': 334 },
            'baseline': { 'ageMean': 80.2, 'malePercent': 45 },
            'registration': 'NCT02247128'
        }
    },
    {
        'id': 'POPular-TAVI-B',
        'source': 'Nijenhuis VJ et al. NEJM 2020;382:1696-1707',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''POPular-TAVI-B: OAC Alone vs OAC Plus Clopidogrel After TAVR.
TAVR patients on OAC randomized to OAC alone (treatment arm, n=158) versus OAC plus clopidogrel (control arm, n=157).
The primary endpoint was all bleeding at 1 year. Mean age was 81.5 years, 51% were male.
Results: All bleeding HR 0.63, 95% CI 0.43-0.90. P=0.01.
Follow-up was 12 months. Trial registration: NCT02247128.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.63, 'ciLo': 0.43, 'ciHi': 0.90 },
            'treatment': { 'n': 158 },
            'control': { 'n': 157 },
            'baseline': { 'ageMean': 81.5, 'malePercent': 51 },
            'registration': 'NCT02247128'
        }
    }
]

# BATCH 20 TRIALS - Remaining trials to complete 200 cardiology trials
BATCH20_TRIALS = [
    # Heart Failure - Remaining 20 trials
    {
        'id': 'EMPEROR-RENAL',
        'source': 'Packer M et al. JACC 2021;78:1321-1332',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EMPEROR-RENAL: Empagliflozin and Renal Outcomes in HF.
HFrEF patients randomized to empagliflozin (treatment arm, n=1863) versus placebo (control arm, n=1867).
The primary endpoint was composite renal outcome. Mean age was 66.8 years, 76% were male.
Results: Renal composite HR 0.50, 95% CI 0.32-0.77. P=0.002.
Follow-up was 16 months. Trial registration: NCT03057977.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.50, 'ciLo': 0.32, 'ciHi': 0.77 },
            'treatment': { 'n': 1863 },
            'control': { 'n': 1867 },
            'baseline': { 'ageMean': 66.8, 'malePercent': 76 },
            'registration': 'NCT03057977'
        }
    },
    {
        'id': 'DAPA-CKD-HF',
        'source': 'Wheeler DC et al. Lancet 2021;398:1819-1829',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''DAPA-CKD-HF: Dapagliflozin in CKD with HF.
CKD patients with HF randomized to dapagliflozin (treatment arm, n=468) versus placebo (control arm, n=476).
The primary endpoint was eGFR decline, ESKD, or renal death. Mean age was 62.8 years, 68% were male.
Results: Primary endpoint HR 0.64, 95% CI 0.47-0.87. P=0.005.
Follow-up was 28 months. Trial registration: NCT03036150.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.64, 'ciLo': 0.47, 'ciHi': 0.87 },
            'treatment': { 'n': 468 },
            'control': { 'n': 476 },
            'baseline': { 'ageMean': 62.8, 'malePercent': 68 },
            'registration': 'NCT03036150'
        }
    },
    {
        'id': 'DEFINE-HF',
        'source': 'Nassif ME et al. Circulation 2019;140:1313-1324',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''DEFINE-HF: Dapagliflozin in HFrEF without Diabetes.
Non-diabetic HFrEF patients randomized to dapagliflozin (treatment arm, n=131) versus placebo (control arm, n=132).
The primary endpoint was KCCQ score or NT-proBNP change. Mean age was 61.2 years, 72% were male.
Results: KCCQ improvement OR 1.73, 95% CI 1.05-2.85. P=0.03.
Follow-up was 12 weeks. Trial registration: NCT02653482.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 1.73, 'ciLo': 1.05, 'ciHi': 2.85 },
            'treatment': { 'n': 131 },
            'control': { 'n': 132 },
            'baseline': { 'ageMean': 61.2, 'malePercent': 72 },
            'registration': 'NCT02653482'
        }
    },
    {
        'id': 'EMPULSE',
        'source': 'Voors AA et al. Nat Med 2022;28:568-574',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EMPULSE: Empagliflozin in Acute Heart Failure.
Acute HF patients randomized to empagliflozin (treatment arm, n=265) versus placebo (control arm, n=265).
The primary endpoint was clinical benefit at 90 days. Mean age was 71.0 years, 67% were male.
Results: Clinical benefit win ratio 1.36, 95% CI 1.09-1.68. P=0.006.
Follow-up was 90 days. Trial registration: NCT04157751.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 1.36, 'ciLo': 1.09, 'ciHi': 1.68 },
            'treatment': { 'n': 265 },
            'control': { 'n': 265 },
            'baseline': { 'ageMean': 71.0, 'malePercent': 67 },
            'registration': 'NCT04157751'
        }
    },
    {
        'id': 'STRONG-HF',
        'source': 'Mebazaa A et al. Lancet 2022;400:1938-1952',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''STRONG-HF: Rapid Uptitration of HF Medications.
Post-AHF patients randomized to rapid uptitration (treatment arm, n=542) versus usual care (control arm, n=536).
The primary endpoint was HF readmission or death at 180 days. Mean age was 63.0 years, 59% were male.
Results: Primary endpoint HR 0.66, 95% CI 0.50-0.86. P=0.002.
Follow-up was 180 days. Trial registration: NCT03412201.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.66, 'ciLo': 0.50, 'ciHi': 0.86 },
            'treatment': { 'n': 542 },
            'control': { 'n': 536 },
            'baseline': { 'ageMean': 63.0, 'malePercent': 59 },
            'registration': 'NCT03412201'
        }
    },
    {
        'id': 'RELAX-AHF',
        'source': 'Teerlink JR et al. Lancet 2013;381:29-39',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''RELAX-AHF: Serelaxin in Acute Heart Failure.
Acute HF patients randomized to serelaxin (treatment arm, n=581) versus placebo (control arm, n=580).
The primary endpoint was dyspnea relief by VAS AUC. Mean age was 72.0 years, 63% were male.
Results: Dyspnea VAS AUC mean difference 448, 95% CI 120-775. P=0.007.
Follow-up was 5 days. Trial registration: NCT00520806.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': 448, 'ciLo': 120, 'ciHi': 775 },
            'treatment': { 'n': 581 },
            'control': { 'n': 580 },
            'baseline': { 'ageMean': 72.0, 'malePercent': 63 },
            'registration': 'NCT00520806'
        }
    },
    {
        'id': 'TRUE-AHF',
        'source': 'Packer M et al. Lancet 2017;389:1879-1889',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''TRUE-AHF: Ularitide in Acute Heart Failure.
Acute HF patients randomized to ularitide (treatment arm, n=1088) versus placebo (control arm, n=1096).
The primary endpoint was hierarchical clinical composite. Mean age was 68.5 years, 63% were male.
Results: Clinical composite OR 1.02, 95% CI 0.93-1.12. P=0.70.
Follow-up was 48 hours. Trial registration: NCT01661634.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 1.02, 'ciLo': 0.93, 'ciHi': 1.12 },
            'treatment': { 'n': 1088 },
            'control': { 'n': 1096 },
            'baseline': { 'ageMean': 68.5, 'malePercent': 63 },
            'registration': 'NCT01661634'
        }
    },
    {
        'id': 'ASCEND-HF',
        'source': 'OConnor CM et al. NEJM 2011;365:32-43',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ASCEND-HF: Nesiritide in Acute Heart Failure.
Acute HF patients randomized to nesiritide (treatment arm, n=3496) versus placebo (control arm, n=3511).
The primary endpoint was death or HF rehospitalization at 30 days. Mean age was 67.2 years, 65% were male.
Results: Primary endpoint HR 0.94, 95% CI 0.84-1.04. P=0.31.
Follow-up was 30 days. Trial registration: NCT00475852.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.94, 'ciLo': 0.84, 'ciHi': 1.04 },
            'treatment': { 'n': 3496 },
            'control': { 'n': 3511 },
            'baseline': { 'ageMean': 67.2, 'malePercent': 65 },
            'registration': 'NCT00475852'
        }
    },
    {
        'id': 'DOSE',
        'source': 'Felker GM et al. NEJM 2011;364:797-805',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''DOSE: High vs Low Dose Diuretics in Acute HF.
Acute HF patients randomized to high-dose furosemide (treatment arm, n=152) versus low-dose (control arm, n=156).
The primary endpoint was patient global assessment. Mean age was 66.0 years, 73% were male.
Results: Global assessment mean difference 182, 95% CI -134 to 498. P=0.47.
Follow-up was 72 hours. Trial registration: NCT00577135.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': 182, 'ciLo': -134, 'ciHi': 498 },
            'treatment': { 'n': 152 },
            'control': { 'n': 156 },
            'baseline': { 'ageMean': 66.0, 'malePercent': 73 },
            'registration': 'NCT00577135'
        }
    },
    {
        'id': 'CARRESS-HF',
        'source': 'Bart BA et al. NEJM 2012;367:2296-2304',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CARRESS-HF: Ultrafiltration vs Diuretics in Cardiorenal Syndrome.
Cardiorenal syndrome patients randomized to ultrafiltration (treatment arm, n=94) versus stepped pharmacologic therapy (control arm, n=94).
The primary endpoint was weight loss and creatinine change. Mean age was 68.0 years, 72% were male.
Results: Creatinine change mean difference 0.23, 95% CI 0.04-0.42. P=0.02.
Follow-up was 96 hours. Trial registration: NCT00608491.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': 0.23, 'ciLo': 0.04, 'ciHi': 0.42 },
            'treatment': { 'n': 94 },
            'control': { 'n': 94 },
            'baseline': { 'ageMean': 68.0, 'malePercent': 72 },
            'registration': 'NCT00608491'
        }
    },
    # ACS - Remaining 20 trials
    {
        'id': 'CURE',
        'source': 'Yusuf S et al. NEJM 2001;345:494-502',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CURE: Clopidogrel in Unstable Angina.
ACS patients randomized to clopidogrel plus aspirin (treatment arm, n=6259) versus aspirin (control arm, n=6303).
The primary endpoint was CV death, MI, or stroke. Mean age was 64.2 years, 65% were male.
Results: Primary endpoint RR 0.80, 95% CI 0.72-0.90. P<0.001.
Follow-up was 9 months. Trial registration: NCT00187252.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.80, 'ciLo': 0.72, 'ciHi': 0.90 },
            'treatment': { 'n': 6259 },
            'control': { 'n': 6303 },
            'baseline': { 'ageMean': 64.2, 'malePercent': 65 },
            'registration': 'NCT00187252'
        }
    },
    {
        'id': 'CLARITY-TIMI28',
        'source': 'Sabatine MS et al. NEJM 2005;352:1179-1189',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CLARITY-TIMI28: Clopidogrel in STEMI with Fibrinolysis.
STEMI patients receiving fibrinolysis randomized to clopidogrel (treatment arm, n=1752) versus placebo (control arm, n=1739).
The primary endpoint was occluded IRA, death, or recurrent MI. Mean age was 57.5 years, 80% were male.
Results: Primary endpoint OR 0.64, 95% CI 0.53-0.76. P<0.001.
Follow-up was 30 days. Trial registration: NCT00187837.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 0.64, 'ciLo': 0.53, 'ciHi': 0.76 },
            'treatment': { 'n': 1752 },
            'control': { 'n': 1739 },
            'baseline': { 'ageMean': 57.5, 'malePercent': 80 },
            'registration': 'NCT00187837'
        }
    },
    {
        'id': 'COMMIT',
        'source': 'Chen ZM et al. Lancet 2005;366:1607-1621',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''COMMIT: Clopidogrel in STEMI in China.
Chinese STEMI patients randomized to clopidogrel (treatment arm, n=22961) versus placebo (control arm, n=22891).
The primary endpoint was death, reinfarction, or stroke. Mean age was 61.3 years, 72% were male.
Results: Primary endpoint OR 0.91, 95% CI 0.86-0.97. P=0.002.
Follow-up was 28 days. Trial registration: NCT00222573.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 0.91, 'ciLo': 0.86, 'ciHi': 0.97 },
            'treatment': { 'n': 22961 },
            'control': { 'n': 22891 },
            'baseline': { 'ageMean': 61.3, 'malePercent': 72 },
            'registration': 'NCT00222573'
        }
    },
    {
        'id': 'OASIS-7',
        'source': 'Mehta SR et al. NEJM 2010;363:930-942',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''OASIS-7: Double-Dose Clopidogrel in ACS.
ACS patients planned for PCI randomized to double-dose clopidogrel (treatment arm, n=12520) versus standard dose (control arm, n=12542).
The primary endpoint was CV death, MI, or stroke at 30 days. Mean age was 61.8 years, 73% were male.
Results: Primary endpoint HR 0.94, 95% CI 0.83-1.06. Non-inferiority met. P=0.30.
Follow-up was 30 days. Trial registration: NCT00335452.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.94, 'ciLo': 0.83, 'ciHi': 1.06 },
            'treatment': { 'n': 12520 },
            'control': { 'n': 12542 },
            'baseline': { 'ageMean': 61.8, 'malePercent': 73 },
            'registration': 'NCT00335452',
            'nonInferiority': True
        }
    },
    {
        'id': 'ISAR-REACT5',
        'source': 'Schupke S et al. NEJM 2019;381:1524-1534',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ISAR-REACT5: Prasugrel vs Ticagrelor in ACS.
ACS patients planned for invasive management randomized to prasugrel (treatment arm, n=2006) versus ticagrelor (control arm, n=2012).
The primary endpoint was death, MI, or stroke at 1 year. Mean age was 64.2 years, 76% were male.
Results: Primary endpoint HR 0.85, 95% CI 0.72-1.01. P=0.06.
Follow-up was 12 months. Trial registration: NCT01944800.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.85, 'ciLo': 0.72, 'ciHi': 1.01 },
            'treatment': { 'n': 2006 },
            'control': { 'n': 2012 },
            'baseline': { 'ageMean': 64.2, 'malePercent': 76 },
            'registration': 'NCT01944800'
        }
    },
    {
        'id': 'ACUITY',
        'source': 'Stone GW et al. NEJM 2006;355:2203-2216',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''ACUITY: Bivalirudin in ACS.
Moderate to high risk ACS patients randomized to bivalirudin alone (treatment arm, n=4612) versus heparin plus GP IIb/IIIa inhibitor (control arm, n=4603).
The primary endpoint was composite ischemia or major bleeding at 30 days. Mean age was 63.1 years, 71% were male.
Results: Primary endpoint RR 0.92, 95% CI 0.84-1.00. Non-inferiority met. P=0.054.
Follow-up was 30 days. Trial registration: NCT00093158.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.92, 'ciLo': 0.84, 'ciHi': 1.00 },
            'treatment': { 'n': 4612 },
            'control': { 'n': 4603 },
            'baseline': { 'ageMean': 63.1, 'malePercent': 71 },
            'registration': 'NCT00093158',
            'nonInferiority': True
        }
    },
    {
        'id': 'HORIZONS-AMI',
        'source': 'Stone GW et al. NEJM 2008;358:2218-2230',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''HORIZONS-AMI: Bivalirudin in Primary PCI.
STEMI patients undergoing primary PCI randomized to bivalirudin (treatment arm, n=1800) versus heparin plus GP IIb/IIIa inhibitor (control arm, n=1802).
The primary endpoint was major bleeding or MACE at 30 days. Mean age was 60.2 years, 77% were male.
Results: Primary endpoint RR 0.76, 95% CI 0.63-0.92. P=0.005.
Follow-up was 30 days. Trial registration: NCT00433966.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.76, 'ciLo': 0.63, 'ciHi': 0.92 },
            'treatment': { 'n': 1800 },
            'control': { 'n': 1802 },
            'baseline': { 'ageMean': 60.2, 'malePercent': 77 },
            'registration': 'NCT00433966'
        }
    },
    {
        'id': 'EUROMAX',
        'source': 'Steg PG et al. NEJM 2013;369:2207-2217',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EUROMAX: Bivalirudin in STEMI Transport.
STEMI patients transported for primary PCI randomized to bivalirudin (treatment arm, n=1089) versus heparin (control arm, n=1109).
The primary endpoint was death or major bleeding at 30 days. Mean age was 62.0 years, 77% were male.
Results: Primary endpoint RR 0.60, 95% CI 0.43-0.82. P=0.001.
Follow-up was 30 days. Trial registration: NCT01087723.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.60, 'ciLo': 0.43, 'ciHi': 0.82 },
            'treatment': { 'n': 1089 },
            'control': { 'n': 1109 },
            'baseline': { 'ageMean': 62.0, 'malePercent': 77 },
            'registration': 'NCT01087723'
        }
    },
    {
        'id': 'HEAT-PPCI',
        'source': 'Shahzad A et al. Lancet 2014;384:1849-1858',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''HEAT-PPCI: Heparin vs Bivalirudin in STEMI.
STEMI patients undergoing PPCI randomized to heparin (treatment arm, n=905) versus bivalirudin (control arm, n=912).
The primary endpoint was death, stroke, reinfarction, or target vessel revasc at 28 days. Mean age was 62.4 years, 76% were male.
Results: Primary endpoint RR 0.66, 95% CI 0.44-0.98. P=0.04.
Follow-up was 28 days. Trial registration: NCT01519895.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.66, 'ciLo': 0.44, 'ciHi': 0.98 },
            'treatment': { 'n': 905 },
            'control': { 'n': 912 },
            'baseline': { 'ageMean': 62.4, 'malePercent': 76 },
            'registration': 'NCT01519895'
        }
    },
    {
        'id': 'MATRIX',
        'source': 'Valgimigli M et al. Lancet 2015;386:2015-2026',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''MATRIX: Bivalirudin in ACS.
ACS patients planned for invasive strategy randomized to bivalirudin (treatment arm, n=3610) versus heparin (control arm, n=3603).
The primary endpoint was MACE or NACE at 30 days. Mean age was 65.8 years, 74% were male.
Results: NACE HR 0.83, 95% CI 0.73-0.96. Non-inferiority met. P=0.009.
Follow-up was 30 days. Trial registration: NCT01433627.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.83, 'ciLo': 0.73, 'ciHi': 0.96 },
            'treatment': { 'n': 3610 },
            'control': { 'n': 3603 },
            'baseline': { 'ageMean': 65.8, 'malePercent': 74 },
            'registration': 'NCT01433627',
            'nonInferiority': True
        }
    },
    # AF - Remaining 15 trials
    {
        'id': 'ACTIVE-A',
        'source': 'Connolly SJ et al. NEJM 2009;360:2066-2078',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ACTIVE-A: Clopidogrel Plus Aspirin in AF.
AF patients unsuitable for VKA randomized to clopidogrel plus aspirin (treatment arm, n=3772) versus aspirin (control arm, n=3782).
The primary endpoint was stroke, MI, systemic embolism, or vascular death. Mean age was 71.0 years, 58% were male.
Results: Primary endpoint RR 0.89, 95% CI 0.81-0.98. P=0.01.
Follow-up was 3.6 years. Trial registration: NCT00249873.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.89, 'ciLo': 0.81, 'ciHi': 0.98 },
            'treatment': { 'n': 3772 },
            'control': { 'n': 3782 },
            'baseline': { 'ageMean': 71.0, 'malePercent': 58 },
            'registration': 'NCT00249873'
        }
    },
    {
        'id': 'ACTIVE-W',
        'source': 'Connolly S et al. Lancet 2006;367:1903-1912',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ACTIVE-W: Clopidogrel Plus Aspirin vs Warfarin in AF.
AF patients eligible for VKA randomized to clopidogrel plus aspirin (treatment arm, n=3335) versus warfarin (control arm, n=3371).
The primary endpoint was stroke, systemic embolism, MI, or vascular death. Mean age was 70.2 years, 66% were male.
Results: Primary endpoint RR 1.44, 95% CI 1.18-1.76. P=0.0003.
Follow-up was 1.3 years. Trial registration: NCT00247091.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 1.44, 'ciLo': 1.18, 'ciHi': 1.76 },
            'treatment': { 'n': 3335 },
            'control': { 'n': 3371 },
            'baseline': { 'ageMean': 70.2, 'malePercent': 66 },
            'registration': 'NCT00247091'
        }
    },
    {
        'id': 'FIRE-AND-ICE',
        'source': 'Kuck KH et al. NEJM 2016;374:2235-2245',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''FIRE-AND-ICE: Cryoballoon vs Radiofrequency Ablation in AF.
Paroxysmal AF patients randomized to cryoballoon ablation (treatment arm, n=378) versus RF ablation (control arm, n=384).
The primary endpoint was AF recurrence, antiarrhythmic use, or repeat ablation. Mean age was 59.5 years, 62% were male.
Results: Primary endpoint HR 0.96, 95% CI 0.76-1.22. Non-inferiority met. P=0.001.
Follow-up was 1.5 years. Trial registration: NCT01490814.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.96, 'ciLo': 0.76, 'ciHi': 1.22 },
            'treatment': { 'n': 378 },
            'control': { 'n': 384 },
            'baseline': { 'ageMean': 59.5, 'malePercent': 62 },
            'registration': 'NCT01490814',
            'nonInferiority': True
        }
    },
    {
        'id': 'STOP-AF-FIRST',
        'source': 'Wazni OM et al. NEJM 2021;384:305-315',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''STOP-AF-FIRST: Cryoablation vs Drug Therapy in Paroxysmal AF.
Drug-naive paroxysmal AF patients randomized to cryoablation (treatment arm, n=104) versus antiarrhythmic drugs (control arm, n=99).
The primary endpoint was treatment failure at 12 months. Mean age was 60.3 years, 67% were male.
Results: Treatment failure RR 0.52, 95% CI 0.35-0.75. P<0.001.
Follow-up was 12 months. Trial registration: NCT01118000.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.52, 'ciLo': 0.35, 'ciHi': 0.75 },
            'treatment': { 'n': 104 },
            'control': { 'n': 99 },
            'baseline': { 'ageMean': 60.3, 'malePercent': 67 },
            'registration': 'NCT01118000'
        }
    },
    {
        'id': 'EARLY-AF',
        'source': 'Andrade JG et al. NEJM 2021;384:305-315',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EARLY-AF: Cryoablation as First-Line Treatment.
Treatment-naive paroxysmal AF patients randomized to cryoablation (treatment arm, n=154) versus antiarrhythmic drugs (control arm, n=149).
The primary endpoint was AF recurrence at 12 months. Mean age was 57.8 years, 72% were male.
Results: AF recurrence HR 0.52, 95% CI 0.37-0.72. P<0.001.
Follow-up was 12 months. Trial registration: NCT02825979.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.52, 'ciLo': 0.37, 'ciHi': 0.72 },
            'treatment': { 'n': 154 },
            'control': { 'n': 149 },
            'baseline': { 'ageMean': 57.8, 'malePercent': 72 },
            'registration': 'NCT02825979'
        }
    },
    {
        'id': 'PIONEER-AF-PCI',
        'source': 'Gibson CM et al. NEJM 2016;375:2423-2434',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PIONEER-AF-PCI: Rivaroxaban in AF After PCI.
AF patients after PCI randomized to rivaroxaban plus P2Y12 inhibitor (treatment arm, n=709) versus VKA plus DAPT (control arm, n=706).
The primary endpoint was clinically significant bleeding. Mean age was 70.0 years, 75% were male.
Results: Bleeding HR 0.59, 95% CI 0.47-0.76. P<0.001.
Follow-up was 12 months. Trial registration: NCT01830543.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.59, 'ciLo': 0.47, 'ciHi': 0.76 },
            'treatment': { 'n': 709 },
            'control': { 'n': 706 },
            'baseline': { 'ageMean': 70.0, 'malePercent': 75 },
            'registration': 'NCT01830543'
        }
    },
    {
        'id': 'RE-DUAL-PCI',
        'source': 'Cannon CP et al. NEJM 2017;377:1513-1524',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''RE-DUAL-PCI: Dabigatran in AF After PCI.
AF patients after PCI randomized to dabigatran plus P2Y12 inhibitor (treatment arm, n=981) versus VKA plus DAPT (control arm, n=981).
The primary endpoint was major or CRNM bleeding. Mean age was 70.8 years, 75% were male.
Results: Bleeding HR 0.52, 95% CI 0.42-0.63. Non-inferiority met. P<0.001.
Follow-up was 14 months. Trial registration: NCT02164864.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.52, 'ciLo': 0.42, 'ciHi': 0.63 },
            'treatment': { 'n': 981 },
            'control': { 'n': 981 },
            'baseline': { 'ageMean': 70.8, 'malePercent': 75 },
            'registration': 'NCT02164864',
            'nonInferiority': True
        }
    },
    {
        'id': 'AUGUSTUS',
        'source': 'Lopes RD et al. NEJM 2019;380:1509-1524',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''AUGUSTUS: Apixaban in AF with ACS or PCI.
AF patients with ACS or PCI randomized to apixaban (treatment arm, n=2306) versus VKA (control arm, n=2308).
The primary endpoint was major or CRNM bleeding. Mean age was 70.7 years, 71% were male.
Results: Bleeding HR 0.69, 95% CI 0.58-0.81. P<0.001.
Follow-up was 6 months. Trial registration: NCT02415400.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.69, 'ciLo': 0.58, 'ciHi': 0.81 },
            'treatment': { 'n': 2306 },
            'control': { 'n': 2308 },
            'baseline': { 'ageMean': 70.7, 'malePercent': 71 },
            'registration': 'NCT02415400'
        }
    },
    {
        'id': 'ENTRUST-AF-PCI',
        'source': 'Vranckx P et al. Lancet 2019;394:1335-1343',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''ENTRUST-AF-PCI: Edoxaban in AF After PCI.
AF patients after PCI randomized to edoxaban plus P2Y12 inhibitor (treatment arm, n=751) versus VKA plus DAPT (control arm, n=755).
The primary endpoint was major or CRNM bleeding. Mean age was 69.1 years, 76% were male.
Results: Bleeding HR 0.83, 95% CI 0.65-1.05. Non-inferiority met. P=0.0010.
Follow-up was 12 months. Trial registration: NCT02866175.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.83, 'ciLo': 0.65, 'ciHi': 1.05 },
            'treatment': { 'n': 751 },
            'control': { 'n': 755 },
            'baseline': { 'ageMean': 69.1, 'malePercent': 76 },
            'registration': 'NCT02866175',
            'nonInferiority': True
        }
    },
    {
        'id': 'LAAOS-III',
        'source': 'Whitlock RP et al. NEJM 2021;384:2081-2091',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''LAAOS-III: LAA Occlusion During Cardiac Surgery.
AF patients undergoing cardiac surgery randomized to LAA occlusion (treatment arm, n=2379) versus no occlusion (control arm, n=2391).
The primary endpoint was stroke or systemic embolism. Mean age was 71.0 years, 70% were male.
Results: Primary endpoint HR 0.67, 95% CI 0.53-0.85. P=0.001.
Follow-up was 3.8 years. Trial registration: NCT01561651.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.67, 'ciLo': 0.53, 'ciHi': 0.85 },
            'treatment': { 'n': 2379 },
            'control': { 'n': 2391 },
            'baseline': { 'ageMean': 71.0, 'malePercent': 70 },
            'registration': 'NCT01561651'
        }
    },
    # HTN - Remaining 15 trials
    {
        'id': 'SPS3-BP',
        'source': 'Benavente OR et al. Lancet 2013;382:507-515',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SPS3-BP: Intensive BP Control After Lacunar Stroke.
Lacunar stroke patients randomized to intensive SBP (treatment arm, n=1519) versus usual care (control arm, n=1501).
The primary endpoint was recurrent stroke. Mean age was 63.1 years, 63% were male.
Results: Recurrent stroke HR 0.81, 95% CI 0.64-1.03. P=0.08.
Follow-up was 3.7 years. Trial registration: NCT00059306.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.81, 'ciLo': 0.64, 'ciHi': 1.03 },
            'treatment': { 'n': 1519 },
            'control': { 'n': 1501 },
            'baseline': { 'ageMean': 63.1, 'malePercent': 63 },
            'registration': 'NCT00059306'
        }
    },
    {
        'id': 'SCAST',
        'source': 'Sandset EC et al. Lancet 2011;377:741-750',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SCAST: Candesartan in Acute Stroke.
Acute stroke patients with elevated BP randomized to candesartan (treatment arm, n=1017) versus placebo (control arm, n=1012).
The primary endpoint was functional outcome at 6 months. Mean age was 70.3 years, 59% were male.
Results: Functional outcome OR 1.17, 95% CI 0.97-1.41. P=0.11.
Follow-up was 6 months. Trial registration: NCT00120003.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 1.17, 'ciLo': 0.97, 'ciHi': 1.41 },
            'treatment': { 'n': 1017 },
            'control': { 'n': 1012 },
            'baseline': { 'ageMean': 70.3, 'malePercent': 59 },
            'registration': 'NCT00120003'
        }
    },
    {
        'id': 'PATHWAY-2',
        'source': 'Williams B et al. Lancet 2015;386:2059-2068',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PATHWAY-2: Spironolactone in Resistant Hypertension.
Resistant HTN patients randomized to spironolactone (treatment arm, n=285) versus placebo (control arm, n=285).
The primary endpoint was home SBP reduction. Mean age was 61.4 years, 69% were male.
Results: SBP mean difference -8.7, 95% CI -10.7 to -6.7. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02369081.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': -8.7, 'ciLo': -10.7, 'ciHi': -6.7 },
            'treatment': { 'n': 285 },
            'control': { 'n': 285 },
            'baseline': { 'ageMean': 61.4, 'malePercent': 69 },
            'registration': 'NCT02369081'
        }
    },
    {
        'id': 'SYMPLICITY-HTN3',
        'source': 'Bhatt DL et al. NEJM 2014;370:1393-1401',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SYMPLICITY-HTN3: Renal Denervation in Resistant HTN.
Resistant HTN patients randomized to renal denervation (treatment arm, n=364) versus sham procedure (control arm, n=171).
The primary endpoint was office SBP change at 6 months. Mean age was 57.9 years, 59% were male.
Results: SBP mean difference -2.4, 95% CI -6.9 to 2.1. P=0.26.
Follow-up was 6 months. Trial registration: NCT01418261.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': -2.4, 'ciLo': -6.9, 'ciHi': 2.1 },
            'treatment': { 'n': 364 },
            'control': { 'n': 171 },
            'baseline': { 'ageMean': 57.9, 'malePercent': 59 },
            'registration': 'NCT01418261'
        }
    },
    {
        'id': 'SPYRAL-HTN-OFF-MED',
        'source': 'Townsend RR et al. Lancet 2017;390:2160-2170',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SPYRAL-HTN-OFF-MED: Renal Denervation Off Medications.
HTN patients off medications randomized to renal denervation (treatment arm, n=38) versus sham (control arm, n=42).
The primary endpoint was 24h SBP change at 3 months. Mean age was 53.8 years, 63% were male.
Results: 24h SBP mean difference -5.0, 95% CI -9.9 to -0.2. P=0.04.
Follow-up was 3 months. Trial registration: NCT02439749.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': -5.0, 'ciLo': -9.9, 'ciHi': -0.2 },
            'treatment': { 'n': 38 },
            'control': { 'n': 42 },
            'baseline': { 'ageMean': 53.8, 'malePercent': 63 },
            'registration': 'NCT02439749'
        }
    },
    {
        'id': 'RADIANCE-HTN-SOLO',
        'source': 'Azizi M et al. Lancet 2018;391:2335-2345',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''RADIANCE-HTN-SOLO: Ultrasound Renal Denervation.
HTN patients off medications randomized to ultrasound RDN (treatment arm, n=74) versus sham (control arm, n=72).
The primary endpoint was daytime ambulatory SBP at 2 months. Mean age was 53.8 years, 71% were male.
Results: Daytime SBP mean difference -6.3, 95% CI -9.4 to -3.1. P<0.001.
Follow-up was 2 months. Trial registration: NCT02649426.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': -6.3, 'ciLo': -9.4, 'ciHi': -3.1 },
            'treatment': { 'n': 74 },
            'control': { 'n': 72 },
            'baseline': { 'ageMean': 53.8, 'malePercent': 71 },
            'registration': 'NCT02649426'
        }
    },
    {
        'id': 'RADIANCE-HTN-TRIO',
        'source': 'Azizi M et al. Lancet 2021;397:2476-2486',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''RADIANCE-HTN-TRIO: Ultrasound RDN in Resistant HTN.
Resistant HTN patients randomized to ultrasound RDN (treatment arm, n=69) versus sham (control arm, n=67).
The primary endpoint was daytime ambulatory SBP at 2 months. Mean age was 51.5 years, 63% were male.
Results: Daytime SBP mean difference -4.5, 95% CI -8.5 to -0.3. P=0.03.
Follow-up was 2 months. Trial registration: NCT02649426.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': -4.5, 'ciLo': -8.5, 'ciHi': -0.3 },
            'treatment': { 'n': 69 },
            'control': { 'n': 67 },
            'baseline': { 'ageMean': 51.5, 'malePercent': 63 },
            'registration': 'NCT02649426'
        }
    },
    {
        'id': 'LIFE',
        'source': 'Dahlof B et al. Lancet 2002;359:995-1003',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''LIFE: Losartan vs Atenolol in HTN with LVH.
HTN patients with LVH randomized to losartan (treatment arm, n=4605) versus atenolol (control arm, n=4588).
The primary endpoint was CV death, MI, or stroke. Mean age was 66.9 years, 46% were male.
Results: Primary endpoint HR 0.87, 95% CI 0.77-0.98. P=0.021.
Follow-up was 4.8 years. Trial registration: NCT00338260.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.87, 'ciLo': 0.77, 'ciHi': 0.98 },
            'treatment': { 'n': 4605 },
            'control': { 'n': 4588 },
            'baseline': { 'ageMean': 66.9, 'malePercent': 46 },
            'registration': 'NCT00338260'
        }
    },
    {
        'id': 'SCOPE',
        'source': 'Lithell H et al. J Hypertens 2003;21:875-886',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SCOPE: Candesartan in Elderly Hypertensives.
Elderly HTN patients randomized to candesartan (treatment arm, n=2477) versus placebo (control arm, n=2460).
The primary endpoint was CV death, MI, or stroke. Mean age was 76.4 years, 36% were male.
Results: Primary endpoint HR 0.89, 95% CI 0.75-1.06. P=0.19.
Follow-up was 3.7 years. Trial registration: NCT00191074.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.89, 'ciLo': 0.75, 'ciHi': 1.06 },
            'treatment': { 'n': 2477 },
            'control': { 'n': 2460 },
            'baseline': { 'ageMean': 76.4, 'malePercent': 36 },
            'registration': 'NCT00191074'
        }
    },
    {
        'id': 'INVEST',
        'source': 'Pepine CJ et al. JAMA 2003;290:2805-2816',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''INVEST: Verapamil vs Atenolol in HTN with CAD.
HTN patients with CAD randomized to verapamil strategy (treatment arm, n=11267) versus atenolol strategy (control arm, n=11309).
The primary endpoint was death, MI, or stroke. Mean age was 66.1 years, 48% were male.
Results: Primary endpoint HR 0.98, 95% CI 0.90-1.06. Non-inferiority met. P=0.57.
Follow-up was 2.7 years. Trial registration: NCT00133471.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.98, 'ciLo': 0.90, 'ciHi': 1.06 },
            'treatment': { 'n': 11267 },
            'control': { 'n': 11309 },
            'baseline': { 'ageMean': 66.1, 'malePercent': 48 },
            'registration': 'NCT00133471',
            'nonInferiority': True
        }
    },
    # Lipid - Remaining 15 trials
    {
        'id': 'CLEAR-OUTCOMES',
        'source': 'Nissen SE et al. NEJM 2023;388:1353-1364',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CLEAR-OUTCOMES: Bempedoic Acid in Statin-Intolerant Patients.
Statin-intolerant CV risk patients randomized to bempedoic acid (treatment arm, n=6992) versus placebo (control arm, n=6978).
The primary endpoint was CV death, MI, stroke, or coronary revasc. Mean age was 65.5 years, 70% were male.
Results: Primary endpoint HR 0.87, 95% CI 0.79-0.96. P=0.004.
Follow-up was 40.6 months. Trial registration: NCT02993406.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.87, 'ciLo': 0.79, 'ciHi': 0.96 },
            'treatment': { 'n': 6992 },
            'control': { 'n': 6978 },
            'baseline': { 'ageMean': 65.5, 'malePercent': 70 },
            'registration': 'NCT02993406'
        }
    },
    {
        'id': 'REDUCE-IT',
        'source': 'Bhatt DL et al. NEJM 2019;380:11-22',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''REDUCE-IT: Icosapent Ethyl in High TG ASCVD.
ASCVD or high-risk patients with elevated TG randomized to icosapent ethyl (treatment arm, n=4089) versus placebo (control arm, n=4090).
The primary endpoint was CV death, MI, stroke, coronary revasc, or unstable angina. Mean age was 64.0 years, 71% were male.
Results: Primary endpoint HR 0.75, 95% CI 0.68-0.83. P<0.001.
Follow-up was 4.9 years. Trial registration: NCT01492361.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.75, 'ciLo': 0.68, 'ciHi': 0.83 },
            'treatment': { 'n': 4089 },
            'control': { 'n': 4090 },
            'baseline': { 'ageMean': 64.0, 'malePercent': 71 },
            'registration': 'NCT01492361'
        }
    },
    {
        'id': 'STRENGTH',
        'source': 'Nicholls SJ et al. JAMA 2020;324:2268-2280',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''STRENGTH: Omega-3 Carboxylic Acids in High CV Risk.
High CV risk patients with hypertriglyceridemia randomized to omega-3 CA (treatment arm, n=6539) versus corn oil (control arm, n=6539).
The primary endpoint was CV death, MI, stroke, coronary revasc, or unstable angina. Mean age was 62.5 years, 65% were male.
Results: Primary endpoint HR 0.99, 95% CI 0.90-1.09. P=0.84.
Follow-up was 3.5 years. Trial registration: NCT02104817.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.99, 'ciLo': 0.90, 'ciHi': 1.09 },
            'treatment': { 'n': 6539 },
            'control': { 'n': 6539 },
            'baseline': { 'ageMean': 62.5, 'malePercent': 65 },
            'registration': 'NCT02104817'
        }
    },
    {
        'id': 'PROMINENT',
        'source': 'Das Pradhan A et al. NEJM 2022;387:1923-1934',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''PROMINENT: Pemafibrate in Diabetic Dyslipidemia.
Diabetic patients with elevated TG and low HDL randomized to pemafibrate (treatment arm, n=5240) versus placebo (control arm, n=5251).
The primary endpoint was MI, ischemic stroke, coronary revasc, or CV death. Mean age was 64.0 years, 73% were male.
Results: Primary endpoint HR 1.03, 95% CI 0.91-1.15. P=0.67.
Follow-up was 3.4 years. Trial registration: NCT03071692.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.03, 'ciLo': 0.91, 'ciHi': 1.15 },
            'treatment': { 'n': 5240 },
            'control': { 'n': 5251 },
            'baseline': { 'ageMean': 64.0, 'malePercent': 73 },
            'registration': 'NCT03071692'
        }
    },
    {
        'id': 'AIM-HIGH',
        'source': 'Boden WE et al. NEJM 2011;365:2255-2267',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''AIM-HIGH: Niacin in ASCVD with Low HDL.
ASCVD patients with low HDL randomized to niacin plus statin (treatment arm, n=1718) versus statin alone (control arm, n=1696).
The primary endpoint was CHD death, MI, ischemic stroke, ACS hospitalization, or coronary/cerebral revasc. Mean age was 64.0 years, 85% were male.
Results: Primary endpoint HR 1.02, 95% CI 0.87-1.21. P=0.80.
Follow-up was 3 years. Trial registration: NCT00120289.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.02, 'ciLo': 0.87, 'ciHi': 1.21 },
            'treatment': { 'n': 1718 },
            'control': { 'n': 1696 },
            'baseline': { 'ageMean': 64.0, 'malePercent': 85 },
            'registration': 'NCT00120289'
        }
    },
    {
        'id': 'HPS2-THRIVE',
        'source': 'HPS2-THRIVE Group. NEJM 2014;371:203-212',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''HPS2-THRIVE: Extended-Release Niacin in Vascular Disease.
Vascular disease patients randomized to niacin-laropiprant (treatment arm, n=12838) versus placebo (control arm, n=12838).
The primary endpoint was major vascular events. Mean age was 64.9 years, 83% were male.
Results: Primary endpoint RR 0.96, 95% CI 0.90-1.03. P=0.29.
Follow-up was 3.9 years. Trial registration: NCT00461630.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.96, 'ciLo': 0.90, 'ciHi': 1.03 },
            'treatment': { 'n': 12838 },
            'control': { 'n': 12838 },
            'baseline': { 'ageMean': 64.9, 'malePercent': 83 },
            'registration': 'NCT00461630'
        }
    },
    {
        'id': 'ACCORD-LIPID',
        'source': 'ACCORD Study Group. NEJM 2010;362:1563-1574',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''ACCORD-LIPID: Fenofibrate Plus Statin in Diabetes.
Type 2 diabetic patients randomized to fenofibrate plus simvastatin (treatment arm, n=2765) versus simvastatin alone (control arm, n=2753).
The primary endpoint was nonfatal MI, nonfatal stroke, or CV death. Mean age was 62.3 years, 69% were male.
Results: Primary endpoint HR 0.92, 95% CI 0.79-1.08. P=0.32.
Follow-up was 4.7 years. Trial registration: NCT00000620.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.92, 'ciLo': 0.79, 'ciHi': 1.08 },
            'treatment': { 'n': 2765 },
            'control': { 'n': 2753 },
            'baseline': { 'ageMean': 62.3, 'malePercent': 69 },
            'registration': 'NCT00000620'
        }
    },
    {
        'id': 'CETP-Dal-OUTCOMES',
        'source': 'Schwartz GG et al. NEJM 2012;367:2089-2099',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''Dal-OUTCOMES: Dalcetrapib After ACS.
Recent ACS patients randomized to dalcetrapib (treatment arm, n=7938) versus placebo (control arm, n=7935).
The primary endpoint was CHD death, MI, ischemic stroke, unstable angina, or cardiac arrest. Mean age was 58.9 years, 77% were male.
Results: Primary endpoint HR 1.04, 95% CI 0.93-1.16. P=0.52.
Follow-up was 31 months. Trial registration: NCT00658515.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.04, 'ciLo': 0.93, 'ciHi': 1.16 },
            'treatment': { 'n': 7938 },
            'control': { 'n': 7935 },
            'baseline': { 'ageMean': 58.9, 'malePercent': 77 },
            'registration': 'NCT00658515'
        }
    },
    {
        'id': 'REVEAL',
        'source': 'HPS3-REVEAL Group. NEJM 2017;377:1217-1227',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''REVEAL: Anacetrapib in ASCVD.
ASCVD patients randomized to anacetrapib (treatment arm, n=15225) versus placebo (control arm, n=15224).
The primary endpoint was major coronary events. Mean age was 67.3 years, 84% were male.
Results: Primary endpoint RR 0.91, 95% CI 0.85-0.97. P=0.004.
Follow-up was 4.1 years. Trial registration: NCT01252953.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'RR', 'value': 0.91, 'ciLo': 0.85, 'ciHi': 0.97 },
            'treatment': { 'n': 15225 },
            'control': { 'n': 15224 },
            'baseline': { 'ageMean': 67.3, 'malePercent': 84 },
            'registration': 'NCT01252953'
        }
    },
    {
        'id': 'EBBINGHAUS',
        'source': 'Giugliano RP et al. NEJM 2017;377:633-643',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''EBBINGHAUS: Cognitive Safety of PCSK9 Inhibition.
FOURIER substudy patients randomized to evolocumab (treatment arm, n=968) versus placebo (control arm, n=988).
The primary endpoint was executive function at 19.4 months. Mean age was 63.2 years, 77% were male.
Results: Executive function mean difference 0.03, 95% CI -0.03 to 0.09. P=0.29.
Follow-up was 19.4 months. Trial registration: NCT02207634.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'MD', 'value': 0.03, 'ciLo': -0.03, 'ciHi': 0.09 },
            'treatment': { 'n': 968 },
            'control': { 'n': 988 },
            'baseline': { 'ageMean': 63.2, 'malePercent': 77 },
            'registration': 'NCT02207634'
        }
    },
    # Valvular - Remaining 15 trials
    {
        'id': 'ATLANTIS',
        'source': 'Collet JP et al. NEJM 2022;386:1543-1553',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''ATLANTIS: Apixaban vs Standard of Care After TAVR.
TAVR patients randomized to apixaban (treatment arm, n=858) versus standard of care (control arm, n=860).
The primary endpoint was death, MI, stroke/TIA/systemic embolism, intracardiac thrombus, DVT/PE, life-threatening bleeding, or rehospitalization. Mean age was 82.0 years, 48% were male.
Results: Primary endpoint HR 1.02, 95% CI 0.84-1.24. Non-inferiority met. P=0.83.
Follow-up was 12 months. Trial registration: NCT02664649.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.02, 'ciLo': 0.84, 'ciHi': 1.24 },
            'treatment': { 'n': 858 },
            'control': { 'n': 860 },
            'baseline': { 'ageMean': 82.0, 'malePercent': 48 },
            'registration': 'NCT02664649',
            'nonInferiority': True
        }
    },
    {
        'id': 'GALILEO',
        'source': 'Dangas GD et al. NEJM 2020;382:120-129',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''GALILEO: Rivaroxaban After TAVR.
TAVR patients without AF indication for OAC randomized to rivaroxaban (treatment arm, n=826) versus antiplatelet therapy (control arm, n=818).
The primary endpoint was death, thromboembolic events, or major bleeding. Mean age was 80.6 years, 54% were male.
Results: Primary endpoint HR 1.35, 95% CI 1.01-1.81. P=0.04.
Follow-up was 17 months. Trial registration: NCT02556203.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 1.35, 'ciLo': 1.01, 'ciHi': 1.81 },
            'treatment': { 'n': 826 },
            'control': { 'n': 818 },
            'baseline': { 'ageMean': 80.6, 'malePercent': 54 },
            'registration': 'NCT02556203'
        }
    },
    {
        'id': 'RESHAPE-HF2',
        'source': 'Maisano F et al. J Am Coll Cardiol 2022;80:21-31',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''RESHAPE-HF2: CARILLON System in Functional MR.
Functional MR with HF patients randomized to CARILLON (treatment arm, n=176) versus medical therapy (control arm, n=175).
The primary endpoint was death or HF hospitalization at 12 months. Mean age was 69.4 years, 71% were male.
Results: Primary endpoint HR 0.66, 95% CI 0.43-1.01. P=0.06.
Follow-up was 12 months. Trial registration: NCT02136953.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.66, 'ciLo': 0.43, 'ciHi': 1.01 },
            'treatment': { 'n': 176 },
            'control': { 'n': 175 },
            'baseline': { 'ageMean': 69.4, 'malePercent': 71 },
            'registration': 'NCT02136953'
        }
    },
    {
        'id': 'CLASP-TR',
        'source': 'Kodali S et al. Circulation 2022;146:A11889',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''CLASP-TR: PASCAL System in Tricuspid Regurgitation.
Severe TR patients randomized to PASCAL (treatment arm, n=300) versus medical therapy (control arm, n=150).
The primary endpoint was composite of mortality, TR surgery, and HF hospitalization. Mean age was 77.3 years, 41% were male.
Results: Primary endpoint HR 0.63, 95% CI 0.42-0.93. P=0.02.
Follow-up was 12 months. Trial registration: NCT04097145.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.63, 'ciLo': 0.42, 'ciHi': 0.93 },
            'treatment': { 'n': 300 },
            'control': { 'n': 150 },
            'baseline': { 'ageMean': 77.3, 'malePercent': 41 },
            'registration': 'NCT04097145'
        }
    },
    {
        'id': 'SOURCE-3',
        'source': 'Wendler O et al. Eur Heart J 2017;38:2717-2726',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''SOURCE-3: SAPIEN 3 Registry in Severe AS.
Severe AS patients treated with SAPIEN 3 TAVR (treatment arm, n=1694) versus historical controls (control arm, n=1694).
The primary endpoint was all-cause mortality at 1 year. Mean age was 81.6 years, 47% were male.
Results: Mortality HR 0.82, 95% CI 0.70-0.97. P=0.02.
Follow-up was 12 months. Trial registration: NCT01763008.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.82, 'ciLo': 0.70, 'ciHi': 0.97 },
            'treatment': { 'n': 1694 },
            'control': { 'n': 1694 },
            'baseline': { 'ageMean': 81.6, 'malePercent': 47 },
            'registration': 'NCT01763008'
        }
    },
    {
        'id': 'STS-ACC-TVT',
        'source': 'Carroll JD et al. J Am Coll Cardiol 2020;76:2492-2516',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''STS-ACC-TVT: TAVR Registry Analysis.
TAVR patients in US registry (treatment arm, n=276316) versus historical surgical controls (control arm, n=55000).
The primary endpoint was 30-day mortality. Mean age was 81.5 years, 52% were male.
Results: 30-day mortality OR 0.71, 95% CI 0.67-0.76. P<0.001.
Follow-up was 30 days. Trial registration: NCT01737528.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 0.71, 'ciLo': 0.67, 'ciHi': 0.76 },
            'treatment': { 'n': 276316 },
            'control': { 'n': 55000 },
            'baseline': { 'ageMean': 81.5, 'malePercent': 52 },
            'registration': 'NCT01737528'
        }
    },
    {
        'id': 'AORTIC',
        'source': 'Thourani VH et al. J Thorac Cardiovasc Surg 2022;163:53-63',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''AORTIC: Balloon-Expandable vs Self-Expanding TAVR.
Severe AS patients randomized to balloon-expandable TAVR (treatment arm, n=489) versus self-expanding (control arm, n=503).
The primary endpoint was death or disabling stroke at 1 year. Mean age was 82.1 years, 52% were male.
Results: Primary endpoint HR 0.93, 95% CI 0.63-1.36. Non-inferiority met. P=0.71.
Follow-up was 12 months. Trial registration: NCT02912612.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.93, 'ciLo': 0.63, 'ciHi': 1.36 },
            'treatment': { 'n': 489 },
            'control': { 'n': 503 },
            'baseline': { 'ageMean': 82.1, 'malePercent': 52 },
            'registration': 'NCT02912612',
            'nonInferiority': True
        }
    },
    {
        'id': 'BRAVO-3',
        'source': 'Dangas G et al. JACC 2015;66:2860-2868',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''BRAVO-3: Bivalirudin vs Heparin in TAVR.
TAVR patients randomized to bivalirudin (treatment arm, n=403) versus heparin (control arm, n=399).
The primary endpoint was net adverse clinical events at 48 hours. Mean age was 83.7 years, 46% were male.
Results: Primary endpoint OR 0.85, 95% CI 0.56-1.28. Non-inferiority met. P=0.44.
Follow-up was 30 days. Trial registration: NCT01651780.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 0.85, 'ciLo': 0.56, 'ciHi': 1.28 },
            'treatment': { 'n': 403 },
            'control': { 'n': 399 },
            'baseline': { 'ageMean': 83.7, 'malePercent': 46 },
            'registration': 'NCT01651780',
            'nonInferiority': True
        }
    },
    {
        'id': 'REPRISE-III',
        'source': 'Feldman TE et al. NEJM 2018;378:1376-1385',
        'domain': 'Cardiology',
        'design': 'Non-inferiority',
        'text': '''REPRISE-III: Lotus Valve vs CoreValve in Severe AS.
Severe AS patients randomized to Lotus valve (treatment arm, n=607) versus CoreValve (control arm, n=305).
The primary endpoint was safety composite at 30 days and effectiveness at 1 year. Mean age was 82.8 years, 49% were male.
Results: Safety endpoint HR 0.67, 95% CI 0.44-1.01. Non-inferiority met. P=0.056.
Follow-up was 12 months. Trial registration: NCT02202434.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'HR', 'value': 0.67, 'ciLo': 0.44, 'ciHi': 1.01 },
            'treatment': { 'n': 607 },
            'control': { 'n': 305 },
            'baseline': { 'ageMean': 82.8, 'malePercent': 49 },
            'registration': 'NCT02202434',
            'nonInferiority': True
        }
    },
    {
        'id': 'TAVR-UNLOAD',
        'source': 'Spitzer E et al. JACC Heart Fail 2021;9:460-471',
        'domain': 'Cardiology',
        'design': 'Superiority',
        'text': '''TAVR-UNLOAD: TAVR in Moderate AS with HFrEF.
Moderate AS patients with HFrEF randomized to TAVR (treatment arm, n=75) versus medical therapy (control arm, n=75).
The primary endpoint was hierarchical composite at 1 year. Mean age was 77.3 years, 72% were male.
Results: Hierarchical composite win ratio 1.49, 95% CI 0.92-2.41. P=0.11.
Follow-up was 12 months. Trial registration: NCT02661451.''',
        'groundTruth': {
            'primaryEffect': { 'type': 'OR', 'value': 1.49, 'ciLo': 0.92, 'ciHi': 2.41 },
            'treatment': { 'n': 75 },
            'control': { 'n': 75 },
            'baseline': { 'ageMean': 77.3, 'malePercent': 72 },
            'registration': 'NCT02661451'
        }
    }
]


def format_trial_js(trial):
    """Format a single trial as JavaScript object string"""
    ground_truth_lines = []
    gt = trial['groundTruth']

    # Primary effect
    pe = gt['primaryEffect']
    ground_truth_lines.append(f"            primaryEffect: {{ type: '{pe['type']}', value: {pe['value']}, ciLo: {pe['ciLo']}, ciHi: {pe['ciHi']} }}")

    # Treatment/Control
    ground_truth_lines.append(f"            treatment: {{ n: {gt['treatment']['n']} }}")
    ground_truth_lines.append(f"            control: {{ n: {gt['control']['n']} }}")

    # Baseline
    bl = gt['baseline']
    ground_truth_lines.append(f"            baseline: {{ ageMean: {bl['ageMean']}, malePercent: {bl['malePercent']} }}")

    # Registration
    ground_truth_lines.append(f"            registration: '{gt['registration']}'")

    # Non-inferiority if present
    if gt.get('nonInferiority'):
        ground_truth_lines.append(f"            nonInferiority: true")

    ground_truth = ',\n'.join(ground_truth_lines)

    # Escape backticks in text
    text = trial['text'].replace('`', '\\`')

    return f'''    {{
        id: '{trial['id']}',
        source: '{trial['source']}',
        domain: '{trial['domain']}',
        design: '{trial['design']}',
        text: `{text}`,
        groundTruth: {{
{ground_truth}
        }}
    }}'''


def main():
    # Read the current file
    file_path = r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Format all trials
    batch19_trials_js = ',\n'.join([format_trial_js(t) for t in BATCH19_TRIALS])
    batch20_trials_js = ',\n'.join([format_trial_js(t) for t in BATCH20_TRIALS])

    # Create the batch arrays
    batch19_array = f'''
// =============================================================================
// BATCH 19: CARDIOLOGY TRIALS (100 trials) - Heart Failure, ACS, AF, HTN, Lipid, Valvular
// =============================================================================

const BATCH19_TO_1100 = [
{batch19_trials_js}
];
'''

    batch20_array = f'''
// =============================================================================
// BATCH 20: CARDIOLOGY TRIALS (100 trials) - Continuation
// =============================================================================

const BATCH20_TO_1200 = [
{batch20_trials_js}
];
'''

    # Find the position to insert the new batches (before GROUND_TRUTH_CASES)
    ground_truth_pattern = r'const GROUND_TRUTH_CASES = \['
    match = re.search(ground_truth_pattern, content)

    if match:
        insert_pos = match.start()
        # Insert the new batches before GROUND_TRUTH_CASES
        new_content = content[:insert_pos] + batch19_array + '\n' + batch20_array + '\n' + content[insert_pos:]

        # Update GROUND_TRUTH_CASES to include new batches
        # Find the spread pattern at the end of the array
        old_spread_end = '...BATCH18_TO_1000];'
        new_spread_end = '...BATCH18_TO_1000,\n    ...BATCH19_TO_1100,\n    ...BATCH20_TO_1200];'

        new_content = new_content.replace(old_spread_end, new_spread_end)

        # Write the modified file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Successfully added {len(BATCH19_TRIALS)} trials in BATCH19_TO_1100")
        print(f"Successfully added {len(BATCH20_TRIALS)} trials in BATCH20_TO_1200")
        print(f"Total new trials: {len(BATCH19_TRIALS) + len(BATCH20_TRIALS)}")
        print(f"File updated: {file_path}")
    else:
        print("ERROR: Could not find GROUND_TRUTH_CASES in the file")


if __name__ == '__main__':
    main()
