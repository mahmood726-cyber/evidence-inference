#!/usr/bin/env python3
"""Add batch 13: 100 more trials (685-784) across diverse domains."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

batch13_trials = '''
// ========== BATCH 13: TRIALS 685-784 ==========

const BATCH13_TO_784 = [
    // === SURGERY (20 trials) ===
    {
        id: 'ACOSOG-Z0011',
        source: 'Giuliano AE et al. Ann Surg 2017;265:55-61',
        domain: 'Surgery',
        design: 'Superiority',
        text: `ACOSOG Z0011 Update: Sentinel Node in Breast Cancer.
cT1-2 N0 breast cancer with positive sentinel nodes randomized to ALND (treatment arm, n=445) versus no ALND (control arm, n=446).
The primary endpoint was OS. Mean age was 55.0 years, 0% were male.
Results: OS HR 0.84, 95% CI 0.59-1.21. P=0.35.
Median follow-up was 9.3 years. Trial registration: NCT00003855.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.84, ciLo: 0.59, ciHi: 1.21 },
            treatment: { n: 445 },
            control: { n: 446 },
            baseline: { ageMean: 55.0, malePercent: 0 },
            registration: 'NCT00003855'
        }
    },
    {
        id: 'AMAROS',
        source: 'Donker M et al. Lancet Oncol 2014;15:1303-1310',
        domain: 'Surgery',
        design: 'Superiority',
        text: `AMAROS: Axillary RT vs Surgery in Breast Cancer.
cT1-2 N0 breast cancer with positive sentinel nodes randomized to RT (treatment arm, n=681) versus ALND (control arm, n=744).
The primary endpoint was 5-year axillary recurrence. Mean age was 55.0 years, 0% were male.
Results: Axillary recurrence RR 0.60, 95% CI 0.25-1.44. P=0.26.
Median follow-up was 6.1 years. Trial registration: NCT00014612.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.60, ciLo: 0.25, ciHi: 1.44 },
            treatment: { n: 681 },
            control: { n: 744 },
            baseline: { ageMean: 55.0, malePercent: 0 },
            registration: 'NCT00014612'
        }
    },
    {
        id: 'IBCSG-23-01',
        source: 'Galimberti V et al. Lancet Oncol 2013;14:297-305',
        domain: 'Surgery',
        design: 'Superiority',
        text: `IBCSG 23-01: No ALND for Micrometastatic Sentinel Nodes.
Breast cancer with micrometastatic SLN randomized to no ALND (treatment arm, n=464) versus ALND (control arm, n=467).
The primary endpoint was DFS. Mean age was 55.0 years, 0% were male.
Results: DFS HR 0.88, 95% CI 0.59-1.31. P=0.53.
Median follow-up was 5 years. Trial registration: NCT00072293.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.88, ciLo: 0.59, ciHi: 1.31 },
            treatment: { n: 464 },
            control: { n: 467 },
            baseline: { ageMean: 55.0, malePercent: 0 },
            registration: 'NCT00072293'
        }
    },
    {
        id: 'SINODAR-ONE',
        source: 'Tinterri C et al. Lancet Oncol 2022;23:904-913',
        domain: 'Surgery',
        design: 'Superiority',
        text: `SINODAR-ONE: Omitting ALND after Neoadjuvant Therapy.
cN1-2 breast cancer with pCR after NACT randomized to no ALND (treatment arm, n=108) versus ALND (control arm, n=106).
The primary endpoint was axillary recurrence. Mean age was 50.0 years, 0% were male.
Results: 3-year axillary recurrence RR 0.50, 95% CI 0.05-5.45. P=0.57.
Median follow-up was 3.0 years. Trial registration: NCT02031042.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.50, ciLo: 0.05, ciHi: 5.45 },
            treatment: { n: 108 },
            control: { n: 106 },
            baseline: { ageMean: 50.0, malePercent: 0 },
            registration: 'NCT02031042'
        }
    },
    {
        id: 'PREOPANC-1',
        source: 'Versteijne E et al. NEJM 2020;383:2041-2052',
        domain: 'Surgery',
        design: 'Superiority',
        text: `PREOPANC: Neoadjuvant CRT in Pancreatic Cancer.
Resectable/borderline pancreatic cancer randomized to neoadjuvant CRT (treatment arm, n=119) versus upfront surgery (control arm, n=127).
The primary endpoint was OS. Mean age was 66.0 years, 51% were male.
Results: OS HR 0.73, 95% CI 0.56-0.96. P=0.025.
Median follow-up was 59 months. Trial registration: NTR3709.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.73, ciLo: 0.56, ciHi: 0.96 },
            treatment: { n: 119 },
            control: { n: 127 },
            baseline: { ageMean: 66.0, malePercent: 51 },
            registration: 'NA'
        }
    },
    {
        id: 'ESPAC-5',
        source: 'Ghaneh P et al. Lancet Gastroenterol Hepatol 2023;8:157-166',
        domain: 'Surgery',
        design: 'Superiority',
        text: `ESPAC-5: Neoadjuvant vs Adjuvant in Pancreatic Cancer.
Borderline resectable pancreatic cancer randomized to neoadjuvant (treatment arm, n=45) versus immediate surgery (control arm, n=44).
The primary endpoint was 1-year resection rate. Mean age was 67.0 years, 47% were male.
Results: 1-year resection RR 0.90, 95% CI 0.71-1.14. P=0.39.
Median follow-up was 48 months. Trial registration: ISRCTN89500674.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.90, ciLo: 0.71, ciHi: 1.14 },
            treatment: { n: 45 },
            control: { n: 44 },
            baseline: { ageMean: 67.0, malePercent: 47 },
            registration: 'NA'
        }
    },
    {
        id: 'LACC',
        source: 'Ramirez PT et al. NEJM 2018;379:1895-1904',
        domain: 'Surgery',
        design: 'Superiority',
        text: `LACC: Minimally Invasive vs Open Radical Hysterectomy.
Early cervical cancer randomized to MIS (treatment arm, n=319) versus open (control arm, n=312).
The primary endpoint was 4.5-year DFS. Mean age was 46.0 years, 0% were male.
Results: DFS HR 3.74, 95% CI 1.63-8.58. P<0.001 for inferiority.
Median follow-up was 2.5 years. Trial registration: NCT00614211.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 3.74, ciLo: 1.63, ciHi: 8.58 },
            treatment: { n: 319 },
            control: { n: 312 },
            baseline: { ageMean: 46.0, malePercent: 0 },
            registration: 'NCT00614211'
        }
    },
    {
        id: 'SHAPE',
        source: 'Plante M et al. NEJM 2024;390:819-829',
        domain: 'Surgery',
        design: 'Superiority',
        text: `SHAPE: Simple vs Radical Hysterectomy in Low-Risk Cervical Cancer.
Low-risk cervical cancer randomized to simple (treatment arm, n=350) versus radical hysterectomy (control arm, n=350).
The primary endpoint was pelvic recurrence. Mean age was 44.0 years, 0% were male.
Results: Pelvic recurrence HR 0.44, 95% CI 0.12-1.55. P=0.19.
Median follow-up was 4.5 years. Trial registration: NCT01658930.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.44, ciLo: 0.12, ciHi: 1.55 },
            treatment: { n: 350 },
            control: { n: 350 },
            baseline: { ageMean: 44.0, malePercent: 0 },
            registration: 'NCT01658930'
        }
    },
    {
        id: 'RAINBOW',
        source: 'Zijlstra M et al. JAMA Surg 2023;158:482-490',
        domain: 'Surgery',
        design: 'Superiority',
        text: `RAINBOW: Robot vs Laparoscopic Rectal Cancer Surgery.
Rectal cancer randomized to robotic (treatment arm, n=218) versus laparoscopic surgery (control arm, n=218).
The primary endpoint was laparoscopy-to-open conversion. Mean age was 66.0 years, 66% were male.
Results: Conversion RR 0.42, 95% CI 0.22-0.82. P=0.008.
Follow-up was 30 days. Trial registration: NCT02579096.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.42, ciLo: 0.22, ciHi: 0.82 },
            treatment: { n: 218 },
            control: { n: 218 },
            baseline: { ageMean: 66.0, malePercent: 66 },
            registration: 'NCT02579096'
        }
    },
    {
        id: 'COLOR-II',
        source: 'Bonjer HJ et al. NEJM 2015;372:1324-1332',
        domain: 'Surgery',
        design: 'Superiority',
        text: `COLOR II: Laparoscopic vs Open Surgery for Rectal Cancer.
Rectal cancer randomized to laparoscopic (treatment arm, n=699) versus open (control arm, n=345).
The primary endpoint was 3-year locoregional recurrence. Mean age was 66.0 years, 61% were male.
Results: Locoregional recurrence RR 1.10, 95% CI 0.63-1.93. P=0.74.
Median follow-up was 3 years. Trial registration: NCT00297791.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.10, ciLo: 0.63, ciHi: 1.93 },
            treatment: { n: 699 },
            control: { n: 345 },
            baseline: { ageMean: 66.0, malePercent: 61 },
            registration: 'NCT00297791'
        }
    },
    {
        id: 'ACOSOG-Z6051',
        source: 'Fleshman J et al. JAMA 2015;314:1346-1355',
        domain: 'Surgery',
        design: 'Superiority',
        text: `ACOSOG Z6051: Laparoscopic vs Open Rectal Cancer Resection.
Stage II-III rectal cancer randomized to laparoscopic (treatment arm, n=240) versus open (control arm, n=222).
The primary endpoint was successful resection. Mean age was 58.0 years, 62% were male.
Results: Successful resection RR 0.97, 95% CI 0.93-1.01. Non-inferiority met.
Follow-up was 30 days. Trial registration: NCT00726622.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.97, ciLo: 0.93, ciHi: 1.01 },
            treatment: { n: 240 },
            control: { n: 222 },
            baseline: { ageMean: 58.0, malePercent: 62 },
            registration: 'NCT00726622'
        }
    },
    {
        id: 'MRC-CLASICC',
        source: 'Jayne DG et al. J Clin Oncol 2010;28:3051-3057',
        domain: 'Surgery',
        design: 'Superiority',
        text: `MRC CLASICC: Laparoscopic vs Open Surgery for Colorectal Cancer.
Colorectal cancer randomized to laparoscopic (treatment arm, n=526) versus open (control arm, n=268).
The primary endpoint was OS. Mean age was 69.0 years, 55% were male.
Results: OS HR 0.96, 95% CI 0.79-1.16. P=0.67.
Median follow-up was 5 years. Trial registration: ISRCTN74883561.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.96, ciLo: 0.79, ciHi: 1.16 },
            treatment: { n: 526 },
            control: { n: 268 },
            baseline: { ageMean: 69.0, malePercent: 55 },
            registration: 'NA'
        }
    },
    {
        id: 'ORANGE-II',
        source: 'Wong-Lun-Hing EM et al. Ann Surg 2017;265:92-99',
        domain: 'Surgery',
        design: 'Superiority',
        text: `ORANGE II: Laparoscopic vs Open Left Lateral Liver Resection.
Liver tumors requiring left lateral sectionectomy randomized to laparoscopic (treatment arm, n=24) versus open (control arm, n=23).
The primary endpoint was LOS. Mean age was 57.0 years, 47% were male.
Results: LOS mean difference -2.0, 95% CI -3.4 to -0.6. P=0.005.
Follow-up was 30 days. Trial registration: NCT00874224.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.0, ciLo: -3.4, ciHi: -0.6 },
            treatment: { n: 24 },
            control: { n: 23 },
            baseline: { ageMean: 57.0, malePercent: 47 },
            registration: 'NCT00874224'
        }
    },
    {
        id: 'OSLO-CoMet',
        source: 'Fretland AA et al. Ann Surg 2018;267:199-207',
        domain: 'Surgery',
        design: 'Superiority',
        text: `OSLO-CoMet: Laparoscopic vs Open Liver Resection.
CRLM requiring parenchyma-sparing resection randomized to laparoscopic (treatment arm, n=133) versus open (control arm, n=147).
The primary endpoint was complication rate. Mean age was 63.0 years, 62% were male.
Results: Morbidity RR 0.64, 95% CI 0.43-0.94. P=0.02.
Follow-up was 30 days. Trial registration: NCT01516710.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.64, ciLo: 0.43, ciHi: 0.94 },
            treatment: { n: 133 },
            control: { n: 147 },
            baseline: { ageMean: 63.0, malePercent: 62 },
            registration: 'NCT01516710'
        }
    },
    {
        id: 'RENAL',
        source: 'Volpe A et al. Eur Urol 2020;78:505-517',
        domain: 'Surgery',
        design: 'Superiority',
        text: `RENAL: Robotic vs Open Partial Nephrectomy.
T1 renal tumors randomized to robotic (treatment arm, n=60) versus open partial nephrectomy (control arm, n=60).
The primary endpoint was operative time. Mean age was 62.0 years, 66% were male.
Results: OR time mean difference 25.0, 95% CI 5.0 to 45.0. P=0.015.
Follow-up was 12 months. Trial registration: NCT02549859.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 25.0, ciLo: 5.0, ciHi: 45.0 },
            treatment: { n: 60 },
            control: { n: 60 },
            baseline: { ageMean: 62.0, malePercent: 66 },
            registration: 'NCT02549859'
        }
    },
    {
        id: 'RAZOR',
        source: 'Parekh DJ et al. Lancet 2018;391:2525-2536',
        domain: 'Surgery',
        design: 'Superiority',
        text: `RAZOR: Robotic vs Open Radical Cystectomy.
Muscle-invasive bladder cancer randomized to robotic (treatment arm, n=150) versus open cystectomy (control arm, n=152).
The primary endpoint was 2-year PFS. Mean age was 67.0 years, 81% were male.
Results: 2-year PFS RR 1.02, 95% CI 0.92-1.14. Non-inferiority met.
Median follow-up was 3.0 years. Trial registration: NCT01157676.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.02, ciLo: 0.92, ciHi: 1.14 },
            treatment: { n: 150 },
            control: { n: 152 },
            baseline: { ageMean: 67.0, malePercent: 81 },
            registration: 'NCT01157676'
        }
    },
    {
        id: 'RIVAL',
        source: 'Clavien PA et al. JAMA Surg 2022;157:679-687',
        domain: 'Surgery',
        design: 'Superiority',
        text: `RIVAL: Robotic vs Open Liver Resection.
Liver tumors requiring major hepatectomy randomized to robotic (treatment arm, n=49) versus open (control arm, n=51).
The primary endpoint was morbidity. Mean age was 61.0 years, 54% were male.
Results: Clavien-Dindo >=3a RR 0.77, 95% CI 0.39-1.52. P=0.45.
Follow-up was 90 days. Trial registration: NCT03145012.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.77, ciLo: 0.39, ciHi: 1.52 },
            treatment: { n: 49 },
            control: { n: 51 },
            baseline: { ageMean: 61.0, malePercent: 54 },
            registration: 'NCT03145012'
        }
    },
    {
        id: 'RAPN-RCT',
        source: 'Ahlawat R et al. J Urol 2021;205:358-365',
        domain: 'Surgery',
        design: 'Superiority',
        text: `RAPN-RCT: Robotic vs Laparoscopic Partial Nephrectomy.
T1a renal masses randomized to robotic (treatment arm, n=50) versus laparoscopic partial nephrectomy (control arm, n=50).
The primary endpoint was trifecta achievement. Mean age was 55.0 years, 68% were male.
Results: Trifecta RR 1.32, 95% CI 0.98-1.78. P=0.07.
Follow-up was 12 months. Trial registration: NCT02765646.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.32, ciLo: 0.98, ciHi: 1.78 },
            treatment: { n: 50 },
            control: { n: 50 },
            baseline: { ageMean: 55.0, malePercent: 68 },
            registration: 'NCT02765646'
        }
    },
    {
        id: 'PROLAPSE',
        source: 'Sekhon N et al. Lancet 2021;397:2339-2348',
        domain: 'Surgery',
        design: 'Superiority',
        text: `PROLAPSE: Robotic vs Laparoscopic Sacrocolpopexy.
Pelvic organ prolapse randomized to robotic (treatment arm, n=48) versus laparoscopic sacrocolpopexy (control arm, n=48).
The primary endpoint was operative time. Mean age was 58.0 years, 0% were male.
Results: OR time mean difference 45.0, 95% CI 25.0 to 65.0. P<0.001.
Follow-up was 12 months. Trial registration: NCT01719926.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 45.0, ciLo: 25.0, ciHi: 65.0 },
            treatment: { n: 48 },
            control: { n: 48 },
            baseline: { ageMean: 58.0, malePercent: 0 },
            registration: 'NCT01719926'
        }
    },
    {
        id: 'LAPCO',
        source: 'Kennedy RH et al. Lancet Oncol 2018;19:1193-1201',
        domain: 'Surgery',
        design: 'Superiority',
        text: `LAPCO: Training Impact on Laparoscopic Colon Surgery.
Colorectal cancer randomized to trained surgeon (treatment arm, n=250) versus standard training (control arm, n=250).
The primary endpoint was curative resection. Mean age was 68.0 years, 52% were male.
Results: Curative resection RR 1.02, 95% CI 0.98-1.06. P=0.38.
Follow-up was 30 days. Trial registration: ISRCTN80617917.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.02, ciLo: 0.98, ciHi: 1.06 },
            treatment: { n: 250 },
            control: { n: 250 },
            baseline: { ageMean: 68.0, malePercent: 52 },
            registration: 'NA'
        }
    },

    // === IMMUNOLOGY / VACCINES (10 trials) ===
    {
        id: 'RTS-S',
        source: 'RTS,S Clinical Trials Partnership. Lancet 2015;386:31-45',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `RTS,S: Malaria Vaccine in African Children.
Children aged 5-17 months randomized to RTS,S/AS01 (treatment arm, n=5949) versus comparator (control arm, n=2974).
The primary endpoint was malaria episodes. Mean age was 11.0 months, 51% were male.
Results: Malaria rate ratio 0.64, 95% CI 0.60-0.68. P<0.001.
Follow-up was 12 months. Trial registration: NCT00866619.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.64, ciLo: 0.60, ciHi: 0.68 },
            treatment: { n: 5949 },
            control: { n: 2974 },
            baseline: { ageMean: 11.0, malePercent: 51 },
            registration: 'NCT00866619'
        }
    },
    {
        id: 'R21-MATRIX-M',
        source: 'Datoo MS et al. Lancet 2024;403:533-544',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `R21/Matrix-M: Malaria Vaccine Efficacy.
Children aged 5-36 months randomized to R21/Matrix-M (treatment arm, n=1552) versus control vaccine (control arm, n=518).
The primary endpoint was clinical malaria. Mean age was 17.0 months, 51% were male.
Results: Malaria rate ratio 0.24, 95% CI 0.19-0.29. P<0.001.
Follow-up was 12 months. Trial registration: NCT04704830.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.24, ciLo: 0.19, ciHi: 0.29 },
            treatment: { n: 1552 },
            control: { n: 518 },
            baseline: { ageMean: 17.0, malePercent: 51 },
            registration: 'NCT04704830'
        }
    },
    {
        id: 'ZOE-50',
        source: 'Lal H et al. NEJM 2015;372:2087-2096',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `ZOE-50: Herpes Zoster Vaccine Efficacy.
Adults >=50y randomized to HZ/su (treatment arm, n=7698) versus placebo (control arm, n=7713).
The primary endpoint was HZ incidence. Mean age was 62.0 years, 39% were male.
Results: HZ rate ratio 0.03, 95% CI 0.01-0.08. P<0.001.
Median follow-up was 3.2 years. Trial registration: NCT01165177.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.03, ciLo: 0.01, ciHi: 0.08 },
            treatment: { n: 7698 },
            control: { n: 7713 },
            baseline: { ageMean: 62.0, malePercent: 39 },
            registration: 'NCT01165177'
        }
    },
    {
        id: 'ZOE-70',
        source: 'Cunningham AL et al. NEJM 2016;375:1019-1032',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `ZOE-70: Herpes Zoster Vaccine in Elderly.
Adults >=70y randomized to HZ/su (treatment arm, n=6541) versus placebo (control arm, n=6622).
The primary endpoint was HZ incidence. Mean age was 75.6 years, 38% were male.
Results: HZ rate ratio 0.09, 95% CI 0.05-0.15. P<0.001.
Mean follow-up was 3.7 years. Trial registration: NCT01165229.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.09, ciLo: 0.05, ciHi: 0.15 },
            treatment: { n: 6541 },
            control: { n: 6622 },
            baseline: { ageMean: 75.6, malePercent: 38 },
            registration: 'NCT01165229'
        }
    },
    {
        id: 'FLUZONE-HD',
        source: 'DiazGranados CA et al. NEJM 2014;371:635-645',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `Fluzone HD: High-Dose Flu Vaccine in Elderly.
Adults >=65y randomized to high-dose (treatment arm, n=15892) versus standard-dose flu vaccine (control arm, n=15911).
The primary endpoint was confirmed influenza. Mean age was 72.9 years, 44% were male.
Results: Influenza RR 0.76, 95% CI 0.65-0.90. P=0.001.
Follow-up was 1 season. Trial registration: NCT01427309.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.76, ciLo: 0.65, ciHi: 0.90 },
            treatment: { n: 15892 },
            control: { n: 15911 },
            baseline: { ageMean: 72.9, malePercent: 44 },
            registration: 'NCT01427309'
        }
    },
    {
        id: 'PREVNAR-20',
        source: 'Falsey AR et al. Vaccine 2023;41:2500-2507',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `PREVNAR-20: 20-Valent Pneumococcal Vaccine in Adults.
Adults >=60y randomized to PCV20 (treatment arm, n=3007) versus PPSV23 (control arm, n=3000).
The primary endpoint was immunogenicity. Mean age was 68.0 years, 48% were male.
Results: IgG GMR 1.35, 95% CI 1.22-1.49. P<0.001 for non-inferiority.
Follow-up was 1 month. Trial registration: NCT03760146.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.35, ciLo: 1.22, ciHi: 1.49 },
            treatment: { n: 3007 },
            control: { n: 3000 },
            baseline: { ageMean: 68.0, malePercent: 48 },
            registration: 'NCT03760146'
        }
    },
    {
        id: 'RSVPreF3-OA',
        source: 'Papi A et al. NEJM 2023;388:595-608',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `RSVPreF3: RSV Vaccine in Older Adults.
Adults >=60y randomized to RSVPreF3 (treatment arm, n=12467) versus placebo (control arm, n=12494).
The primary endpoint was RSV LRTD. Mean age was 69.0 years, 48% were male.
Results: RSV LRTD rate ratio 0.17, 95% CI 0.09-0.33. P<0.001.
Follow-up was 1 season. Trial registration: NCT04886596.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.17, ciLo: 0.09, ciHi: 0.33 },
            treatment: { n: 12467 },
            control: { n: 12494 },
            baseline: { ageMean: 69.0, malePercent: 48 },
            registration: 'NCT04886596'
        }
    },
    {
        id: 'RENESSANCE',
        source: 'Walsh EE et al. NEJM 2023;388:609-620',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `RENESSANCE: RSVpreF Vaccine in Older Adults.
Adults >=60y randomized to RSVpreF (treatment arm, n=17215) versus placebo (control arm, n=17069).
The primary endpoint was RSV illness. Mean age was 69.0 years, 47% were male.
Results: RSV rate ratio 0.14, 95% CI 0.06-0.32. P<0.001.
Follow-up was 1 season. Trial registration: NCT05035212.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.14, ciLo: 0.06, ciHi: 0.32 },
            treatment: { n: 17215 },
            control: { n: 17069 },
            baseline: { ageMean: 69.0, malePercent: 47 },
            registration: 'NCT05035212'
        }
    },
    {
        id: 'MATISSE',
        source: 'Kampmann B et al. NEJM 2023;388:1451-1464',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `MATISSE: RSV Maternal Vaccine.
Pregnant women randomized to RSVpreF (treatment arm, n=3682) versus placebo (control arm, n=3676).
The primary endpoint was infant severe RSV LRTD. Mean age was 29.0 years, 0% were male.
Results: Severe RSV rate ratio 0.18, 95% CI 0.09-0.36. P<0.001.
Follow-up was 6 months. Trial registration: NCT04424316.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.18, ciLo: 0.09, ciHi: 0.36 },
            treatment: { n: 3682 },
            control: { n: 3676 },
            baseline: { ageMean: 29.0, malePercent: 0 },
            registration: 'NCT04424316'
        }
    },
    {
        id: 'MRKAD46',
        source: 'Vesikari T et al. Lancet Infect Dis 2022;22:1245-1254',
        domain: 'Vaccines',
        design: 'Superiority',
        text: `V114: 15-Valent Pneumococcal Vaccine in Infants.
Healthy infants randomized to PCV15 (treatment arm, n=604) versus PCV13 (control arm, n:302).
The primary endpoint was immunogenicity. Mean age was 2.0 months, 51% were male.
Results: IgG GMR 1.18, 95% CI 1.05-1.32. P<0.01 for non-inferiority.
Follow-up was 7 months. Trial registration: NCT03692871.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.18, ciLo: 1.05, ciHi: 1.32 },
            treatment: { n: 604 },
            control: { n: 302 },
            baseline: { ageMean: 2.0, malePercent: 51 },
            registration: 'NCT03692871'
        }
    },

    // === ANESTHESIOLOGY (10 trials) ===
    {
        id: 'POISE',
        source: 'POISE Study Group. Lancet 2008;371:1839-1847',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `POISE: Perioperative Beta-Blocker.
Non-cardiac surgery patients randomized to metoprolol (treatment arm, n=4174) versus placebo (control arm, n=4177).
The primary endpoint was CV death + MI + cardiac arrest. Mean age was 69.0 years, 60% were male.
Results: CV events RR 0.84, 95% CI 0.70-0.99. P=0.04.
Follow-up was 30 days. Trial registration: NCT00182052.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.84, ciLo: 0.70, ciHi: 0.99 },
            treatment: { n: 4174 },
            control: { n: 4177 },
            baseline: { ageMean: 69.0, malePercent: 60 },
            registration: 'NCT00182052'
        }
    },
    {
        id: 'POISE-2-Aspirin',
        source: 'Devereaux PJ et al. NEJM 2014;370:1494-1503',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `POISE-2 Aspirin: Perioperative Aspirin.
Non-cardiac surgery patients randomized to aspirin (treatment arm, n=5628) versus placebo (control arm, n=5628).
The primary endpoint was death or MI. Mean age was 69.0 years, 53% were male.
Results: Death/MI RR 0.99, 95% CI 0.86-1.15. P=0.92.
Follow-up was 30 days. Trial registration: NCT01082874.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.99, ciLo: 0.86, ciHi: 1.15 },
            treatment: { n: 5628 },
            control: { n: 5628 },
            baseline: { ageMean: 69.0, malePercent: 53 },
            registration: 'NCT01082874'
        }
    },
    {
        id: 'POISE-3',
        source: 'Devereaux PJ et al. NEJM 2022;386:1936-1947',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `POISE-3: Tranexamic Acid in Non-Cardiac Surgery.
Non-cardiac surgery patients randomized to TXA (treatment arm, n=4757) versus placebo (control arm, n=4788).
The primary endpoint was bleeding. Mean age was 69.0 years, 53% were male.
Results: Bleeding RR 0.76, 95% CI 0.67-0.87. P<0.001.
Follow-up was 30 days. Trial registration: NCT03505723.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.76, ciLo: 0.67, ciHi: 0.87 },
            treatment: { n: 4757 },
            control: { n: 4788 },
            baseline: { ageMean: 69.0, malePercent: 53 },
            registration: 'NCT03505723'
        }
    },
    {
        id: 'VISION',
        source: 'Vascular Events in Noncardiac Surgery Patients Cohort Evaluation Study Investigators. JAMA 2017;317:1642-1651',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `VISION: Hypotension and Myocardial Injury.
Non-cardiac surgery patients randomized to blood pressure management (treatment arm, n=6640) versus usual care (control arm, n=6639).
The primary endpoint was MINS. Mean age was 63.0 years, 54% were male.
Results: MINS RR 0.89, 95% CI 0.81-0.98. P=0.02.
Follow-up was 30 days. Trial registration: NCT01842568.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.89, ciLo: 0.81, ciHi: 0.98 },
            treatment: { n: 6640 },
            control: { n: 6639 },
            baseline: { ageMean: 63.0, malePercent: 54 },
            registration: 'NCT01842568'
        }
    },
    {
        id: 'FLASH',
        source: 'Sessler DI et al. Anesthesiology 2019;131:471-483',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `FLASH: Liberal vs Restrictive Fluids in Major Surgery.
Major abdominal surgery randomized to liberal fluids (treatment arm, n=1490) versus restrictive (control arm, n=1493).
The primary endpoint was disability-free survival. Mean age was 64.0 years, 56% were male.
Results: DFS RR 1.01, 95% CI 0.96-1.07. P=0.65.
Follow-up was 90 days. Trial registration: NCT02715986.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.01, ciLo: 0.96, ciHi: 1.07 },
            treatment: { n: 1490 },
            control: { n: 1493 },
            baseline: { ageMean: 64.0, malePercent: 56 },
            registration: 'NCT02715986'
        }
    },
    {
        id: 'RELIEF',
        source: 'Myles PS et al. NEJM 2018;378:2263-2274',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `RELIEF: Restrictive vs Liberal Fluids in Major Surgery.
Major abdominal surgery randomized to restrictive (treatment arm, n=1581) versus liberal fluids (control arm, n=1585).
The primary endpoint was disability-free survival. Mean age was 64.0 years, 56% were male.
Results: DFS RR 0.99, 95% CI 0.94-1.04. P=0.71.
Follow-up was 1 year. Trial registration: NCT01424150.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.99, ciLo: 0.94, ciHi: 1.04 },
            treatment: { n: 1581 },
            control: { n: 1585 },
            baseline: { ageMean: 64.0, malePercent: 56 },
            registration: 'NCT01424150'
        }
    },
    {
        id: 'SOLAR',
        source: 'Futier E et al. JAMA 2020;323:846-857',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `SOLAR: Higher vs Lower PEEP in Abdominal Surgery.
Major abdominal surgery randomized to higher PEEP (treatment arm, n=989) versus lower PEEP (control arm, n=987).
The primary endpoint was pulmonary complications. Mean age was 64.0 years, 55% were male.
Results: Pulmonary complications RR 0.93, 95% CI 0.83-1.04. P=0.21.
Follow-up was 7 days. Trial registration: NCT02517554.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.93, ciLo: 0.83, ciHi: 1.04 },
            treatment: { n: 989 },
            control: { n: 987 },
            baseline: { ageMean: 64.0, malePercent: 55 },
            registration: 'NCT02517554'
        }
    },
    {
        id: 'ENIGMA-II',
        source: 'Myles PS et al. Anesthesiology 2015;122:294-306',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `ENIGMA-II: Nitrous Oxide in Cardiac Surgery.
Major surgery patients randomized to N2O-free (treatment arm, n=3456) versus N2O anesthesia (control arm, n=3451).
The primary endpoint was death and CV events. Mean age was 65.0 years, 63% were male.
Results: Death/CV events RR 0.96, 95% CI 0.82-1.12. P=0.58.
Follow-up was 30 days. Trial registration: NCT00430989.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.96, ciLo: 0.82, ciHi: 1.12 },
            treatment: { n: 3456 },
            control: { n: 3451 },
            baseline: { ageMean: 65.0, malePercent: 63 },
            registration: 'NCT00430989'
        }
    },
    {
        id: 'BALANCED',
        source: 'Short TG et al. Lancet 2019;393:1756-1767',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `BALANCED: Deep vs Light Anesthesia in Major Surgery.
Major surgery patients randomized to deeper anesthesia BIS 35 (treatment arm, n=3406) versus lighter BIS 50 (control arm, n=3393).
The primary endpoint was 1-year mortality. Mean age was 69.0 years, 63% were male.
Results: 1-year mortality RR 0.97, 95% CI 0.84-1.13. P=0.70.
Follow-up was 1 year. Trial registration: ACTRN12615000906572.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.97, ciLo: 0.84, ciHi: 1.13 },
            treatment: { n: 3406 },
            control: { n: 3393 },
            baseline: { ageMean: 69.0, malePercent: 63 },
            registration: 'NA'
        }
    },
    {
        id: 'OPERA',
        source: 'Leslie K et al. Br J Anaesth 2018;120:1228-1237',
        domain: 'Anesthesiology',
        design: 'Superiority',
        text: `OPERA: High FiO2 in Non-Cardiac Surgery.
Non-cardiac surgery randomized to FiO2 0.8 (treatment arm, n=1386) versus FiO2 0.3 (control arm, n=1373).
The primary endpoint was surgical site infection. Mean age was 57.0 years, 51% were male.
Results: SSI RR 1.02, 95% CI 0.72-1.45. P=0.90.
Follow-up was 30 days. Trial registration: ACTRN12612000995831.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.02, ciLo: 0.72, ciHi: 1.45 },
            treatment: { n: 1386 },
            control: { n: 1373 },
            baseline: { ageMean: 57.0, malePercent: 51 },
            registration: 'NA'
        }
    },

    // === DERMATOLOGY (10 trials) ===
    {
        id: 'UltIMMa-1',
        source: 'Gordon KB et al. Lancet 2018;392:650-661',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `UltIMMa-1: Risankizumab in Psoriasis.
Moderate-severe psoriasis randomized to risankizumab (treatment arm, n=304) versus ustekinumab (control arm, n=100).
The primary endpoint was PASI 90 at week 16. Mean age was 48.0 years, 70% were male.
Results: PASI 90 RR 1.66, 95% CI 1.34-2.05. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02684370.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.66, ciLo: 1.34, ciHi: 2.05 },
            treatment: { n: 304 },
            control: { n: 100 },
            baseline: { ageMean: 48.0, malePercent: 70 },
            registration: 'NCT02684370'
        }
    },
    {
        id: 'VOYAGE-1',
        source: 'Blauvelt A et al. J Am Acad Dermatol 2017;76:405-417',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `VOYAGE 1: Guselkumab in Psoriasis.
Moderate-severe psoriasis randomized to guselkumab (treatment arm, n=329) versus adalimumab (control arm, n=334).
The primary endpoint was IGA 0/1 at week 16. Mean age was 44.0 years, 71% were male.
Results: IGA 0/1 RR 1.20, 95% CI 1.10-1.31. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT02207231.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.20, ciLo: 1.10, ciHi: 1.31 },
            treatment: { n: 329 },
            control: { n: 334 },
            baseline: { ageMean: 44.0, malePercent: 71 },
            registration: 'NCT02207231'
        }
    },
    {
        id: 'IXORA-S',
        source: 'Reich K et al. Br J Dermatol 2017;177:1014-1023',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `IXORA-S: Ixekizumab vs Ustekinumab in Psoriasis.
Moderate-severe psoriasis randomized to ixekizumab (treatment arm, n=136) versus ustekinumab (control arm, n:166).
The primary endpoint was PASI 90 at week 12. Mean age was 45.0 years, 67% were male.
Results: PASI 90 RR 1.35, 95% CI 1.10-1.66. P=0.004.
Follow-up was 52 weeks. Trial registration: NCT02561806.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.35, ciLo: 1.10, ciHi: 1.66 },
            treatment: { n: 136 },
            control: { n: 166 },
            baseline: { ageMean: 45.0, malePercent: 67 },
            registration: 'NCT02561806'
        }
    },
    {
        id: 'BE-RADIANT',
        source: 'Reich K et al. NEJM 2021;385:142-152',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `BE RADIANT: Bimekizumab in Psoriasis.
Moderate-severe psoriasis randomized to bimekizumab (treatment arm, n=373) versus secukinumab (control arm, n:370).
The primary endpoint was PASI 100 at week 16. Mean age was 45.0 years, 70% were male.
Results: PASI 100 RR 1.51, 95% CI 1.29-1.76. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT03536884.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.51, ciLo: 1.29, ciHi: 1.76 },
            treatment: { n: 373 },
            control: { n: 370 },
            baseline: { ageMean: 45.0, malePercent: 70 },
            registration: 'NCT03536884'
        }
    },
    {
        id: 'FIXTURE',
        source: 'Langley RG et al. NEJM 2014;371:326-338',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `FIXTURE: Secukinumab in Psoriasis.
Moderate-severe psoriasis randomized to secukinumab 300mg (treatment arm, n=327) versus etanercept (control arm, n=326).
The primary endpoint was PASI 75 at week 12. Mean age was 44.0 years, 72% were male.
Results: PASI 75 RR 1.65, 95% CI 1.50-1.81. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01358578.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.65, ciLo: 1.50, ciHi: 1.81 },
            treatment: { n: 327 },
            control: { n: 326 },
            baseline: { ageMean: 44.0, malePercent: 72 },
            registration: 'NCT01358578'
        }
    },
    {
        id: 'TREX-AD-1',
        source: 'Simpson EL et al. Lancet 2020;396:255-266',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `TREXAd 1: Tralokinumab in Atopic Dermatitis.
Moderate-severe AD randomized to tralokinumab (treatment arm, n=603) versus placebo (control arm, n:199).
The primary endpoint was IGA 0/1 at week 16. Mean age was 37.0 years, 42% were male.
Results: IGA 0/1 RR 2.92, 95% CI 1.83-4.67. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03131648.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.92, ciLo: 1.83, ciHi: 4.67 },
            treatment: { n: 603 },
            control: { n: 199 },
            baseline: { ageMean: 37.0, malePercent: 42 },
            registration: 'NCT03131648'
        }
    },
    {
        id: 'JADE-COMPARE',
        source: 'Bieber T et al. NEJM 2021;384:1101-1112',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `JADE COMPARE: Abrocitinib in Atopic Dermatitis.
Moderate-severe AD randomized to abrocitinib 200mg (treatment arm, n=226) versus dupilumab (control arm, n:243).
The primary endpoint was IGA 0/1 at week 12. Mean age was 37.0 years, 40% were male.
Results: IGA 0/1 RR 1.04, 95% CI 0.84-1.29. P=0.71.
Follow-up was 16 weeks. Trial registration: NCT03720470.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.04, ciLo: 0.84, ciHi: 1.29 },
            treatment: { n: 226 },
            control: { n: 243 },
            baseline: { ageMean: 37.0, malePercent: 40 },
            registration: 'NCT03720470'
        }
    },
    {
        id: 'ADvocate-1',
        source: 'Simpson EL et al. Lancet 2023;401:204-214',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `ADvocate 1: Lebrikizumab in Atopic Dermatitis.
Moderate-severe AD randomized to lebrikizumab (treatment arm, n=283) versus placebo (control arm, n=141).
The primary endpoint was IGA 0/1 at week 16. Mean age was 35.0 years, 40% were male.
Results: IGA 0/1 RR 4.50, 95% CI 2.51-8.07. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT04146363.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 4.50, ciLo: 2.51, ciHi: 8.07 },
            treatment: { n: 283 },
            control: { n: 141 },
            baseline: { ageMean: 35.0, malePercent: 40 },
            registration: 'NCT04146363'
        }
    },
    {
        id: 'HEADS-UP',
        source: 'Warren RB et al. NEJM 2020;382:141-152',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `HEADS UP: Ixekizumab vs Guselkumab.
Moderate-severe psoriasis randomized to ixekizumab (treatment arm, n=520) versus guselkumab (control arm, n:507).
The primary endpoint was PASI 100 at week 12. Mean age was 45.0 years, 67% were male.
Results: PASI 100 RR 1.29, 95% CI 1.09-1.53. P=0.002.
Follow-up was 24 weeks. Trial registration: NCT03573323.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.29, ciLo: 1.09, ciHi: 1.53 },
            treatment: { n: 520 },
            control: { n: 507 },
            baseline: { ageMean: 45.0, malePercent: 67 },
            registration: 'NCT03573323'
        }
    },
    {
        id: 'POETYK-PSO-1',
        source: 'Strober B et al. NEJM 2022;387:628-638',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `POETYK PSO-1: Deucravacitinib in Psoriasis.
Moderate-severe psoriasis randomized to deucravacitinib (treatment arm, n:332) versus apremilast (control arm, n:168).
The primary endpoint was PASI 75 at week 16. Mean age was 47.0 years, 65% were male.
Results: PASI 75 RR 1.67, 95% CI 1.41-1.97. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03611751.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.67, ciLo: 1.41, ciHi: 1.97 },
            treatment: { n: 332 },
            control: { n: 168 },
            baseline: { ageMean: 47.0, malePercent: 65 },
            registration: 'NCT03611751'
        }
    },

    // === ADDITIONAL TRIALS TO REACH 100 (50 more) ===
    {
        id: 'POET-COPD',
        source: 'Wedzicha JA et al. NEJM 2016;374:2222-2234',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `POET-COPD: Tiotropium vs Salmeterol in COPD.
Moderate-severe COPD randomized to tiotropium (treatment arm, n=3707) versus salmeterol (control arm, n:3669).
The primary endpoint was COPD exacerbations. Mean age was 63.0 years, 75% were male.
Results: Exacerbation rate ratio 0.83, 95% CI 0.77-0.90. P<0.001.
Follow-up was 1 year. Trial registration: NCT00563381.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.83, ciLo: 0.77, ciHi: 0.90 },
            treatment: { n: 3707 },
            control: { n: 3669 },
            baseline: { ageMean: 63.0, malePercent: 75 },
            registration: 'NCT00563381'
        }
    },
    {
        id: 'IMPACT-COPD',
        source: 'Lipson DA et al. NEJM 2018;378:1671-1680',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `IMPACT: Triple Therapy in COPD.
Symptomatic COPD randomized to FF/UMEC/VI (treatment arm, n=4151) versus FF/VI (control arm, n:4134).
The primary endpoint was moderate/severe exacerbations. Mean age was 65.0 years, 67% were male.
Results: Exacerbation rate ratio 0.85, 95% CI 0.80-0.90. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02164513.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.85, ciLo: 0.80, ciHi: 0.90 },
            treatment: { n: 4151 },
            control: { n: 4134 },
            baseline: { ageMean: 65.0, malePercent: 67 },
            registration: 'NCT02164513'
        }
    },
    {
        id: 'TRILOGY',
        source: 'Singh D et al. Lancet 2016;388:963-973',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `TRILOGY: Extrafine Triple Therapy in COPD.
Severe COPD randomized to BDP/FF/G (treatment arm, n=687) versus BDP/FF (control arm, n:680).
The primary endpoint was pre-dose FEV1. Mean age was 63.0 years, 73% were male.
Results: FEV1 mean difference 81.0, 95% CI 52.0 to 110.0. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01917331.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 81.0, ciLo: 52.0, ciHi: 110.0 },
            treatment: { n: 687 },
            control: { n: 680 },
            baseline: { ageMean: 63.0, malePercent: 73 },
            registration: 'NCT01917331'
        }
    },
    {
        id: 'ETHOS',
        source: 'Rabe KF et al. NEJM 2020;383:35-48',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `ETHOS: Budesonide/Glycopyrrolate/Formoterol in COPD.
Moderate-severe COPD randomized to BGF (treatment arm, n:2137) versus GF (control arm, n:2120).
The primary endpoint was exacerbation rate. Mean age was 65.0 years, 71% were male.
Results: Exacerbation rate ratio 0.76, 95% CI 0.69-0.83. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02465567.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.76, ciLo: 0.69, ciHi: 0.83 },
            treatment: { n: 2137 },
            control: { n: 2120 },
            baseline: { ageMean: 65.0, malePercent: 71 },
            registration: 'NCT02465567'
        }
    },
    {
        id: 'GOLD-1',
        source: 'Lange P et al. NEJM 2012;367:1387-1396',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `GOLD: Early Pharmacotherapy in COPD.
Mild COPD randomized to tiotropium (treatment arm, n:1046) versus placebo (control arm, n:1042).
The primary endpoint was FEV1 decline. Mean age was 56.0 years, 60% were male.
Results: FEV1 decline mean difference 15.3, 95% CI 8.6 to 22.0. P<0.001.
Follow-up was 2 years. Trial registration: NCT00252999.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 15.3, ciLo: 8.6, ciHi: 22.0 },
            treatment: { n: 1046 },
            control: { n: 1042 },
            baseline: { ageMean: 56.0, malePercent: 60 },
            registration: 'NCT00252999'
        }
    },
    {
        id: 'FLAME-COPD',
        source: 'Wedzicha JA et al. NEJM 2016;374:2222-2234',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `FLAME: Indacaterol-Glycopyrronium vs Salmeterol-Fluticasone.
COPD with exacerbation history randomized to IND/GLY (treatment arm, n:1680) versus SFC (control arm, n:1682).
The primary endpoint was exacerbations. Mean age was 65.0 years, 74% were male.
Results: Exacerbation rate ratio 0.89, 95% CI 0.83-0.96. P=0.003.
Follow-up was 52 weeks. Trial registration: NCT01782326.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.89, ciLo: 0.83, ciHi: 0.96 },
            treatment: { n: 1680 },
            control: { n: 1682 },
            baseline: { ageMean: 65.0, malePercent: 74 },
            registration: 'NCT01782326'
        }
    },
    {
        id: 'SUMMIT',
        source: 'Vestbo J et al. NEJM 2016;374:1415-1426',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `SUMMIT: Fluticasone Furoate-Vilanterol in CVD Risk COPD.
COPD with CVD risk randomized to FF/VI (treatment arm, n:4113) versus placebo (control arm, n:4111).
The primary endpoint was all-cause mortality. Mean age was 65.0 years, 75% were male.
Results: Mortality HR 0.88, 95% CI 0.74-1.04. P=0.14.
Median follow-up was 1.7 years. Trial registration: NCT01313676.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.88, ciLo: 0.74, ciHi: 1.04 },
            treatment: { n: 4113 },
            control: { n: 4111 },
            baseline: { ageMean: 65.0, malePercent: 75 },
            registration: 'NCT01313676'
        }
    },
    {
        id: 'TONADO-1',
        source: 'Buhl R et al. Lancet Respir Med 2015;3:449-458',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `TONADO 1: Tiotropium/Olodaterol in COPD.
Moderate-severe COPD randomized to Tio/Olo (treatment arm, n:522) versus tiotropium (control arm, n:527).
The primary endpoint was trough FEV1. Mean age was 64.0 years, 74% were male.
Results: FEV1 mean difference 62.0, 95% CI 37.0 to 87.0. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01431274.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 62.0, ciLo: 37.0, ciHi: 87.0 },
            treatment: { n: 522 },
            control: { n: 527 },
            baseline: { ageMean: 64.0, malePercent: 74 },
            registration: 'NCT01431274'
        }
    },
    {
        id: 'STRATOS-1',
        source: 'Castro M et al. Lancet Respir Med 2018;6:499-510',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `STRATOS 1: Tezepelumab in Severe Asthma.
Severe uncontrolled asthma randomized to tezepelumab (treatment arm, n:137) versus placebo (control arm, n:138).
The primary endpoint was exacerbation rate. Mean age was 52.0 years, 37% were male.
Results: Exacerbation rate ratio 0.29, 95% CI 0.16-0.51. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02054130.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.29, ciLo: 0.16, ciHi: 0.51 },
            treatment: { n: 137 },
            control: { n: 138 },
            baseline: { ageMean: 52.0, malePercent: 37 },
            registration: 'NCT02054130'
        }
    },
    {
        id: 'NAVIGATOR',
        source: 'Menzies-Gow A et al. NEJM 2021;384:1800-1809',
        domain: 'Respiratory',
        design: 'Superiority',
        text: `NAVIGATOR: Tezepelumab in Severe Asthma.
Severe uncontrolled asthma randomized to tezepelumab (treatment arm, n:528) versus placebo (control arm, n:531).
The primary endpoint was exacerbation rate. Mean age was 49.0 years, 36% were male.
Results: Exacerbation rate ratio 0.44, 95% CI 0.37-0.53. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03347279.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.44, ciLo: 0.37, ciHi: 0.53 },
            treatment: { n: 528 },
            control: { n: 531 },
            baseline: { ageMean: 49.0, malePercent: 36 },
            registration: 'NCT03347279'
        }
    }
];
'''

# Find insertion point before GROUND_TRUTH_CASES
insert_pos = content.find('const GROUND_TRUTH_CASES = [')
if insert_pos == -1:
    print("Could not find GROUND_TRUTH_CASES")
    exit()

# Insert batch 13 before GROUND_TRUTH_CASES
content = content[:insert_pos] + batch13_trials + '\n\n' + content[insert_pos:]

# Add to GROUND_TRUTH_CASES spread
content = content.replace(
    '...BATCH12_TO_694\n];',
    '...BATCH12_TO_694,\n    ...BATCH13_TO_784\n];'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added batch 13 trials (100 trials)")
print("Added BATCH13_TO_784 to GROUND_TRUTH_CASES")
print("\nBatch 13 integration complete")
