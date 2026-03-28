#!/usr/bin/env python3
"""Add 100 more trials (batch to reach 400)."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

NEW_BATCH = '''

// BATCH 8: TRIALS 301-400 (100 trials)
const BATCH8_TO_400 = [
    // MORE CARDIOVASCULAR TRIALS
    {
        id: 'DAPA-CKD',
        source: 'Heerspink HJL et al. NEJM 2020;383:1436-1446',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `DAPA-CKD: Dapagliflozin in CKD.
CKD patients with or without diabetes randomized to dapagliflozin (treatment arm, n=2152) versus placebo (control arm, n=2152).
The primary endpoint was sustained GFR decline, ESKD, or renal/CV death. Mean age was 61.8 years, 67% were male.
Results: Primary endpoint 9.2% vs 14.5%. HR 0.61, 95% CI 0.51-0.72. P<0.001.
Median follow-up was 2.4 years. Trial registration: NCT03036150.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.61, ciLo: 0.51, ciHi: 0.72 },
            treatment: { n: 2152 },
            control: { n: 2152 },
            baseline: { ageMean: 61.8, malePercent: 67 },
            registration: 'NCT03036150'
        }
    },
    {
        id: 'CREDENCE',
        source: 'Perkovic V et al. NEJM 2019;380:2295-2306',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `CREDENCE: Canagliflozin in Diabetic Kidney Disease.
T2DM with CKD randomized to canagliflozin (treatment arm, n=2202) versus placebo (control arm, n=2199).
The primary endpoint was ESKD, doubling creatinine, or renal/CV death. Mean age was 63.0 years, 66% were male.
Results: Primary endpoint 11.1% vs 15.5%. HR 0.70, 95% CI 0.59-0.82. P<0.001.
Median follow-up was 2.6 years. Trial registration: NCT02065791.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.70, ciLo: 0.59, ciHi: 0.82 },
            treatment: { n: 2202 },
            control: { n: 2199 },
            baseline: { ageMean: 63.0, malePercent: 66 },
            registration: 'NCT02065791'
        }
    },
    {
        id: 'FIDELIO-DKD',
        source: 'Bakris GL et al. NEJM 2020;383:2219-2229',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `FIDELIO-DKD: Finerenone in Diabetic Kidney Disease.
T2DM with CKD randomized to finerenone (treatment arm, n=2833) versus placebo (control arm, n=2841).
The primary endpoint was kidney failure, sustained GFR decline, or renal death. Mean age was 65.6 years, 70% were male.
Results: Primary endpoint 17.8% vs 21.1%. HR 0.82, 95% CI 0.73-0.93. P=0.001.
Median follow-up was 2.6 years. Trial registration: NCT02540993.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.82, ciLo: 0.73, ciHi: 0.93 },
            treatment: { n: 2833 },
            control: { n: 2841 },
            baseline: { ageMean: 65.6, malePercent: 70 },
            registration: 'NCT02540993'
        }
    },
    {
        id: 'FIGARO-DKD',
        source: 'Pitt B et al. NEJM 2021;385:2252-2263',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `FIGARO-DKD: Finerenone CV Outcomes in DKD.
T2DM with CKD randomized to finerenone (treatment arm, n=3686) versus placebo (control arm, n=3666).
The primary endpoint was CV death, MI, stroke, or HF hospitalization. Mean age was 64.1 years, 69% were male.
Results: Primary endpoint 12.4% vs 14.2%. HR 0.87, 95% CI 0.76-0.98. P=0.03.
Median follow-up was 3.4 years. Trial registration: NCT02545049.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.87, ciLo: 0.76, ciHi: 0.98 },
            treatment: { n: 3686 },
            control: { n: 3666 },
            baseline: { ageMean: 64.1, malePercent: 69 },
            registration: 'NCT02545049'
        }
    },
    {
        id: 'SCORED',
        source: 'Bhatt DL et al. NEJM 2021;384:129-139',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `SCORED: Sotagliflozin in T2DM with CKD.
T2DM with CKD and CV risk randomized to sotagliflozin (treatment arm, n=5292) versus placebo (control arm, n=5292).
The primary endpoint was CV death, HF hospitalization, or urgent HF visit. Mean age was 69.0 years, 55% were male.
Results: Primary endpoint 5.6% vs 7.5%. HR 0.74, 95% CI 0.63-0.88. P<0.001.
Median follow-up was 16 months. Trial registration: NCT03315143.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.74, ciLo: 0.63, ciHi: 0.88 },
            treatment: { n: 5292 },
            control: { n: 5292 },
            baseline: { ageMean: 69.0, malePercent: 55 },
            registration: 'NCT03315143'
        }
    },
    {
        id: 'SOLOIST-WHF',
        source: 'Bhatt DL et al. NEJM 2021;384:117-128',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `SOLOIST-WHF: Sotagliflozin in Worsening Heart Failure.
T2DM hospitalized for worsening HF randomized to sotagliflozin (treatment arm, n=608) versus placebo (control arm, n=614).
The primary endpoint was CV death, HF hospitalization, or urgent HF visit. Mean age was 70.0 years, 66% were male.
Results: Primary endpoint 51.0 vs 76.3 per 100 patient-years. HR 0.67, 95% CI 0.52-0.85. P<0.001.
Median follow-up was 9.2 months. Trial registration: NCT03521934.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.67, ciLo: 0.52, ciHi: 0.85 },
            treatment: { n: 608 },
            control: { n: 614 },
            baseline: { ageMean: 70.0, malePercent: 66 },
            registration: 'NCT03521934'
        }
    },
    {
        id: 'EMPULSE',
        source: 'Voors AA et al. Nat Med 2022;28:568-574',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `EMPULSE: Empagliflozin in Acute HF.
Hospitalized acute HF patients randomized to empagliflozin (treatment arm, n=265) versus placebo (control arm, n=265).
The primary endpoint was clinical benefit at 90 days. Mean age was 71.0 years, 66% were male.
Results: Clinical benefit win ratio 1.36, 95% CI 1.09-1.68. P=0.006.
Trial registration: NCT04157751.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.36, ciLo: 1.09, ciHi: 1.68 },
            treatment: { n: 265 },
            control: { n: 265 },
            baseline: { ageMean: 71.0, malePercent: 66 },
            registration: 'NCT04157751'
        }
    },
    {
        id: 'STRONG-HF',
        source: 'Mebazaa A et al. Lancet 2022;400:1938-1952',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `STRONG-HF: Rapid Up-titration After AHF.
Post-AHF discharge randomized to intensive up-titration (treatment arm, n=542) versus usual care (control arm, n=536).
The primary endpoint was 180-day HF readmission or death. Mean age was 63.0 years, 59% were male.
Results: Primary endpoint 15.2% vs 23.3%. HR 0.66, 95% CI 0.50-0.86. P=0.002.
Trial registration: NCT03412201.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.50, ciHi: 0.86 },
            treatment: { n: 542 },
            control: { n: 536 },
            baseline: { ageMean: 63.0, malePercent: 59 },
            registration: 'NCT03412201'
        }
    },
    {
        id: 'STEP-HFpEF',
        source: 'Kosiborod MN et al. NEJM 2023;389:1186-1198',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `STEP-HFpEF: Semaglutide in HFpEF with Obesity.
HFpEF with obesity randomized to semaglutide (treatment arm, n=259) versus placebo (control arm, n=270).
The primary endpoint was KCCQ-CSS change at 52 weeks. Mean age was 69.0 years, 44% were male.
Results: KCCQ-CSS improved 16.6 vs 8.7 points. Mean difference 7.8, 95% CI 4.8 to 10.9. P<0.001.
Trial registration: NCT04788511.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 7.8, ciLo: 4.8, ciHi: 10.9 },
            treatment: { n: 259 },
            control: { n: 270 },
            baseline: { ageMean: 69.0, malePercent: 44 },
            registration: 'NCT04788511'
        }
    },
    {
        id: 'DELIVER',
        source: 'Solomon SD et al. NEJM 2022;387:1089-1098',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `DELIVER: Dapagliflozin in HFpEF.
HFpEF patients randomized to dapagliflozin (treatment arm, n=3131) versus placebo (control arm, n=3132).
The primary endpoint was worsening HF or CV death. Mean age was 71.7 years, 56% were male.
Results: Primary endpoint 16.4% vs 19.5%. HR 0.82, 95% CI 0.73-0.92. P<0.001.
Median follow-up was 2.3 years. Trial registration: NCT03619213.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.82, ciLo: 0.73, ciHi: 0.92 },
            treatment: { n: 3131 },
            control: { n: 3132 },
            baseline: { ageMean: 71.7, malePercent: 56 },
            registration: 'NCT03619213'
        }
    },
    {
        id: 'EMPEROR-Preserved',
        source: 'Anker SD et al. NEJM 2021;385:1451-1461',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `EMPEROR-Preserved: Empagliflozin in HFpEF.
HFpEF patients randomized to empagliflozin (treatment arm, n=2997) versus placebo (control arm, n=2991).
The primary endpoint was CV death or HF hospitalization. Mean age was 71.9 years, 56% were male.
Results: Primary endpoint 13.8% vs 17.1%. HR 0.79, 95% CI 0.69-0.90. P<0.001.
Median follow-up was 26.2 months. Trial registration: NCT03057951.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.79, ciLo: 0.69, ciHi: 0.90 },
            treatment: { n: 2997 },
            control: { n: 2991 },
            baseline: { ageMean: 71.9, malePercent: 56 },
            registration: 'NCT03057951'
        }
    },
    // ATRIAL FIBRILLATION ABLATION
    {
        id: 'EAST-AFNET4',
        source: 'Kirchhof P et al. NEJM 2020;383:1305-1316',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `EAST-AFNET 4: Early Rhythm Control in AF.
Early AF patients randomized to early rhythm control (treatment arm, n=1395) versus usual care (control arm, n=1394).
The primary endpoint was CV death, stroke, or HF/ACS hospitalization. Mean age was 70.3 years, 55% were male.
Results: Primary endpoint 3.9% vs 5.0% per year. HR 0.79, 95% CI 0.66-0.94. P=0.005.
Median follow-up was 5.1 years. Trial registration: NCT01288352.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.79, ciLo: 0.66, ciHi: 0.94 },
            treatment: { n: 1395 },
            control: { n: 1394 },
            baseline: { ageMean: 70.3, malePercent: 55 },
            registration: 'NCT01288352'
        }
    },
    {
        id: 'EARLY-AF',
        source: 'Andrade JG et al. NEJM 2021;384:305-315',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `EARLY-AF: Cryoablation vs Drug Therapy in AF.
Treatment-naive paroxysmal AF randomized to cryoablation (treatment arm, n=154) versus drug therapy (control arm, n=149).
The primary endpoint was recurrent atrial tachyarrhythmia. Mean age was 58.0 years, 70% were male.
Results: Recurrence 42.9% vs 67.8%. HR 0.48, 95% CI 0.35-0.66. P<0.001.
Follow-up was 12 months. Trial registration: NCT02825979.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.48, ciLo: 0.35, ciHi: 0.66 },
            treatment: { n: 154 },
            control: { n: 149 },
            baseline: { ageMean: 58.0, malePercent: 70 },
            registration: 'NCT02825979'
        }
    },
    {
        id: 'STOP-AF-First',
        source: 'Wazni OM et al. NEJM 2021;384:316-324',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `STOP AF First: Cryoablation as First-Line.
Paroxysmal AF randomized to cryoablation (treatment arm, n=104) versus drug therapy (control arm, n=99).
The primary endpoint was treatment failure at 12 months. Mean age was 61.0 years, 69% were male.
Results: Treatment failure 24.0% vs 43.4%. HR 0.46, 95% CI 0.29-0.74. P<0.001.
Trial registration: NCT02617loosely.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.46, ciLo: 0.29, ciHi: 0.74 },
            treatment: { n: 104 },
            control: { n: 99 },
            baseline: { ageMean: 61.0, malePercent: 69 },
            registration: 'NCT02617loosely'
        }
    },
    // MORE ONCOLOGY - IMMUNOTHERAPY
    {
        id: 'CheckMate-9LA',
        source: 'Paz-Ares L et al. Lancet Oncol 2021;22:198-211',
        domain: 'Oncology',
        design: 'Superiority',
        text: `CheckMate 9LA: Nivo+Ipi+Chemo in NSCLC.
Advanced NSCLC randomized to nivolumab + ipilimumab + chemo (treatment arm, n=361) versus chemo (control arm, n=358).
The primary endpoint was OS. Mean age was 65.0 years, 70% were male.
Results: Median OS 15.6 vs 10.9 months. HR 0.66, 95% CI 0.55-0.80. P<0.001.
Trial registration: NCT03215706.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.55, ciHi: 0.80 },
            treatment: { n: 361 },
            control: { n: 358 },
            baseline: { ageMean: 65.0, malePercent: 70 },
            registration: 'NCT03215706'
        }
    },
    {
        id: 'KEYNOTE-604',
        source: 'Rudin CM et al. J Clin Oncol 2020;38:2369-2379',
        domain: 'Oncology',
        design: 'Superiority',
        text: `KEYNOTE-604: Pembrolizumab in ES-SCLC.
Extensive-stage SCLC randomized to pembrolizumab + chemo (treatment arm, n=228) versus chemo (control arm, n=225).
The primary endpoint was PFS and OS. Mean age was 65.0 years, 57% were male.
Results: Median PFS 4.5 vs 4.3 months. HR 0.75, 95% CI 0.61-0.91. P=0.0023.
Trial registration: NCT03066778.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.75, ciLo: 0.61, ciHi: 0.91 },
            treatment: { n: 228 },
            control: { n: 225 },
            baseline: { ageMean: 65.0, malePercent: 57 },
            registration: 'NCT03066778'
        }
    },
    {
        id: 'IMpower133',
        source: 'Horn L et al. NEJM 2018;379:2220-2229',
        domain: 'Oncology',
        design: 'Superiority',
        text: `IMpower133: Atezolizumab in ES-SCLC.
Extensive-stage SCLC randomized to atezolizumab + chemo (treatment arm, n=201) versus chemo (control arm, n=202).
The primary endpoint was OS. Mean age was 64.0 years, 65% were male.
Results: Median OS 12.3 vs 10.3 months. HR 0.70, 95% CI 0.54-0.91. P=0.007.
Trial registration: NCT02763579.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.70, ciLo: 0.54, ciHi: 0.91 },
            treatment: { n: 201 },
            control: { n: 202 },
            baseline: { ageMean: 64.0, malePercent: 65 },
            registration: 'NCT02763579'
        }
    },
    {
        id: 'CASPIAN',
        source: 'Paz-Ares L et al. Lancet 2019;394:1929-1939',
        domain: 'Oncology',
        design: 'Superiority',
        text: `CASPIAN: Durvalumab in ES-SCLC.
Extensive-stage SCLC randomized to durvalumab + chemo (treatment arm, n=268) versus chemo (control arm, n=269).
The primary endpoint was OS. Mean age was 63.0 years, 69% were male.
Results: Median OS 13.0 vs 10.3 months. HR 0.73, 95% CI 0.59-0.91. P=0.0047.
Trial registration: NCT03043872.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.73, ciLo: 0.59, ciHi: 0.91 },
            treatment: { n: 268 },
            control: { n: 269 },
            baseline: { ageMean: 63.0, malePercent: 69 },
            registration: 'NCT03043872'
        }
    },
    {
        id: 'PACIFIC',
        source: 'Antonia SJ et al. NEJM 2017;377:1919-1929',
        domain: 'Oncology',
        design: 'Superiority',
        text: `PACIFIC: Durvalumab After CRT in NSCLC.
Stage III NSCLC after chemoradiation randomized to durvalumab (treatment arm, n=476) versus placebo (control arm, n=237).
The primary endpoint was PFS. Mean age was 64.0 years, 70% were male.
Results: 12-month PFS 55.9% vs 35.3%. HR 0.52, 95% CI 0.42-0.65. P<0.001.
Trial registration: NCT02125461.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.52, ciLo: 0.42, ciHi: 0.65 },
            treatment: { n: 476 },
            control: { n: 237 },
            baseline: { ageMean: 64.0, malePercent: 70 },
            registration: 'NCT02125461'
        }
    },
    {
        id: 'FLAURA',
        source: 'Soria JC et al. NEJM 2018;378:113-125',
        domain: 'Oncology',
        design: 'Superiority',
        text: `FLAURA: Osimertinib in EGFR+ NSCLC.
EGFR-mutant advanced NSCLC randomized to osimertinib (treatment arm, n=279) versus erlotinib/gefitinib (control arm, n=277).
The primary endpoint was PFS. Mean age was 64.0 years, 37% were male.
Results: Median PFS 18.9 vs 10.2 months. HR 0.46, 95% CI 0.37-0.57. P<0.001.
Trial registration: NCT02296125.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.46, ciLo: 0.37, ciHi: 0.57 },
            treatment: { n: 279 },
            control: { n: 277 },
            baseline: { ageMean: 64.0, malePercent: 37 },
            registration: 'NCT02296125'
        }
    },
    {
        id: 'ALEX',
        source: 'Peters S et al. NEJM 2017;377:829-838',
        domain: 'Oncology',
        design: 'Superiority',
        text: `ALEX: Alectinib vs Crizotinib in ALK+ NSCLC.
ALK-positive advanced NSCLC randomized to alectinib (treatment arm, n=152) versus crizotinib (control arm, n=151).
The primary endpoint was investigator-assessed PFS. Mean age was 54.0 years, 45% were male.
Results: 12-month PFS 68.4% vs 48.7%. HR 0.47, 95% CI 0.34-0.65. P<0.001.
Trial registration: NCT02075840.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.47, ciLo: 0.34, ciHi: 0.65 },
            treatment: { n: 152 },
            control: { n: 151 },
            baseline: { ageMean: 54.0, malePercent: 45 },
            registration: 'NCT02075840'
        }
    },
    {
        id: 'CROWN',
        source: 'Shaw AT et al. NEJM 2020;383:2018-2029',
        domain: 'Oncology',
        design: 'Superiority',
        text: `CROWN: Lorlatinib vs Crizotinib in ALK+ NSCLC.
ALK-positive advanced NSCLC randomized to lorlatinib (treatment arm, n=149) versus crizotinib (control arm, n=147).
The primary endpoint was PFS. Mean age was 59.0 years, 43% were male.
Results: 12-month PFS 78% vs 39%. HR 0.28, 95% CI 0.19-0.41. P<0.001.
Trial registration: NCT03052608.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.28, ciLo: 0.19, ciHi: 0.41 },
            treatment: { n: 149 },
            control: { n: 147 },
            baseline: { ageMean: 59.0, malePercent: 43 },
            registration: 'NCT03052608'
        }
    },
    {
        id: 'CodeBreaK-200',
        source: 'Janne PA et al. NEJM 2022;387:2029-2040',
        domain: 'Oncology',
        design: 'Superiority',
        text: `CodeBreaK 200: Sotorasib vs Docetaxel in KRAS G12C+ NSCLC.
KRAS G12C-mutant NSCLC randomized to sotorasib (treatment arm, n=171) versus docetaxel (control arm, n=174).
The primary endpoint was PFS. Mean age was 64.0 years, 47% were male.
Results: Median PFS 5.6 vs 4.5 months. HR 0.66, 95% CI 0.51-0.86. P=0.002.
Trial registration: NCT04303780.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.51, ciHi: 0.86 },
            treatment: { n: 171 },
            control: { n: 174 },
            baseline: { ageMean: 64.0, malePercent: 47 },
            registration: 'NCT04303780'
        }
    },
    // BREAST CANCER
    {
        id: 'DESTINY-Breast04',
        source: 'Modi S et al. NEJM 2022;387:9-20',
        domain: 'Oncology',
        design: 'Superiority',
        text: `DESTINY-Breast04: T-DXd in HER2-low Breast Cancer.
HER2-low metastatic breast cancer randomized to T-DXd (treatment arm, n=373) versus chemo (control arm, n=184).
The primary endpoint was PFS in HR+ cohort. Mean age was 57.0 years, 0% were male.
Results: Median PFS 10.1 vs 5.4 months. HR 0.51, 95% CI 0.40-0.64. P<0.001.
Trial registration: NCT03734029.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.51, ciLo: 0.40, ciHi: 0.64 },
            treatment: { n: 373 },
            control: { n: 184 },
            baseline: { ageMean: 57.0, malePercent: 0 },
            registration: 'NCT03734029'
        }
    },
    {
        id: 'MONALEESA-2',
        source: 'Hortobagyi GN et al. NEJM 2016;375:1738-1748',
        domain: 'Oncology',
        design: 'Superiority',
        text: `MONALEESA-2: Ribociclib in HR+ Breast Cancer.
HR+/HER2- advanced breast cancer randomized to ribociclib + letrozole (treatment arm, n=334) versus letrozole (control arm, n=334).
The primary endpoint was PFS. Mean age was 62.0 years, 0% were male.
Results: 18-month PFS 63% vs 42.2%. HR 0.56, 95% CI 0.43-0.72. P<0.001.
Trial registration: NCT01958021.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.56, ciLo: 0.43, ciHi: 0.72 },
            treatment: { n: 334 },
            control: { n: 334 },
            baseline: { ageMean: 62.0, malePercent: 0 },
            registration: 'NCT01958021'
        }
    },
    {
        id: 'MONALEESA-7',
        source: 'Tripathy D et al. Lancet Oncol 2018;19:904-915',
        domain: 'Oncology',
        design: 'Superiority',
        text: `MONALEESA-7: Ribociclib in Premenopausal.
Premenopausal HR+ advanced breast cancer randomized to ribociclib + ET (treatment arm, n=335) versus ET (control arm, n=337).
The primary endpoint was PFS. Mean age was 43.0 years, 0% were male.
Results: Median PFS 23.8 vs 13.0 months. HR 0.55, 95% CI 0.44-0.69. P<0.001.
Trial registration: NCT02278120.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.55, ciLo: 0.44, ciHi: 0.69 },
            treatment: { n: 335 },
            control: { n: 337 },
            baseline: { ageMean: 43.0, malePercent: 0 },
            registration: 'NCT02278120'
        }
    },
    {
        id: 'PALOMA-2',
        source: 'Finn RS et al. NEJM 2016;375:1925-1936',
        domain: 'Oncology',
        design: 'Superiority',
        text: `PALOMA-2: Palbociclib in HR+ Breast Cancer.
HR+/HER2- metastatic breast cancer randomized to palbociclib + letrozole (treatment arm, n=444) versus letrozole (control arm, n=222).
The primary endpoint was PFS. Mean age was 62.0 years, 0% were male.
Results: Median PFS 24.8 vs 14.5 months. HR 0.58, 95% CI 0.46-0.72. P<0.001.
Trial registration: NCT01740427.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.58, ciLo: 0.46, ciHi: 0.72 },
            treatment: { n: 444 },
            control: { n: 222 },
            baseline: { ageMean: 62.0, malePercent: 0 },
            registration: 'NCT01740427'
        }
    },
    {
        id: 'MONARCH-3',
        source: 'Goetz MP et al. J Clin Oncol 2017;35:3638-3646',
        domain: 'Oncology',
        design: 'Superiority',
        text: `MONARCH 3: Abemaciclib in HR+ Breast Cancer.
HR+/HER2- advanced breast cancer randomized to abemaciclib + AI (treatment arm, n=328) versus AI (control arm, n=165).
The primary endpoint was PFS. Mean age was 63.0 years, 0% were male.
Results: Median PFS 28.2 vs 14.8 months. HR 0.54, 95% CI 0.41-0.72. P<0.001.
Trial registration: NCT02246621.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.54, ciLo: 0.41, ciHi: 0.72 },
            treatment: { n: 328 },
            control: { n: 165 },
            baseline: { ageMean: 63.0, malePercent: 0 },
            registration: 'NCT02246621'
        }
    },
    {
        id: 'monarchE',
        source: 'Johnston SRD et al. J Clin Oncol 2020;38:3987-3998',
        domain: 'Oncology',
        design: 'Superiority',
        text: `monarchE: Abemaciclib in Early Breast Cancer.
HR+/HER2- high-risk early breast cancer randomized to abemaciclib + ET (treatment arm, n=2808) versus ET (control arm, n=2829).
The primary endpoint was IDFS. Mean age was 51.0 years, 0% were male.
Results: 2-year IDFS 92.2% vs 88.7%. HR 0.75, 95% CI 0.60-0.93. P=0.01.
Trial registration: NCT03155997.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.75, ciLo: 0.60, ciHi: 0.93 },
            treatment: { n: 2808 },
            control: { n: 2829 },
            baseline: { ageMean: 51.0, malePercent: 0 },
            registration: 'NCT03155997'
        }
    },
    {
        id: 'OlympiA',
        source: 'Tutt ANJ et al. NEJM 2021;384:2394-2405',
        domain: 'Oncology',
        design: 'Superiority',
        text: `OlympiA: Olaparib in gBRCA+ Early Breast Cancer.
gBRCA+ HER2- early breast cancer randomized to olaparib (treatment arm, n=921) versus placebo (control arm, n=915).
The primary endpoint was IDFS. Mean age was 42.0 years, 0% were male.
Results: 3-year IDFS 85.9% vs 77.1%. HR 0.58, 95% CI 0.41-0.82. P<0.001.
Trial registration: NCT02032823.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.58, ciLo: 0.41, ciHi: 0.82 },
            treatment: { n: 921 },
            control: { n: 915 },
            baseline: { ageMean: 42.0, malePercent: 0 },
            registration: 'NCT02032823'
        }
    },
    {
        id: 'OlympiAD',
        source: 'Robson M et al. NEJM 2017;377:523-533',
        domain: 'Oncology',
        design: 'Superiority',
        text: `OlympiAD: Olaparib in gBRCA+ Metastatic Breast.
gBRCA+ HER2- metastatic breast cancer randomized to olaparib (treatment arm, n=205) versus chemo (control arm, n=97).
The primary endpoint was PFS. Mean age was 44.0 years, 0% were male.
Results: Median PFS 7.0 vs 4.2 months. HR 0.58, 95% CI 0.43-0.80. P<0.001.
Trial registration: NCT02000622.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.58, ciLo: 0.43, ciHi: 0.80 },
            treatment: { n: 205 },
            control: { n: 97 },
            baseline: { ageMean: 44.0, malePercent: 0 },
            registration: 'NCT02000622'
        }
    },
    {
        id: 'EMBRACA',
        source: 'Litton JK et al. NEJM 2018;379:753-763',
        domain: 'Oncology',
        design: 'Superiority',
        text: `EMBRACA: Talazoparib in gBRCA+ Breast Cancer.
gBRCA+ HER2- advanced breast cancer randomized to talazoparib (treatment arm, n=287) versus chemo (control arm, n=144).
The primary endpoint was PFS. Mean age was 45.0 years, 0% were male.
Results: Median PFS 8.6 vs 5.6 months. HR 0.54, 95% CI 0.41-0.71. P<0.001.
Trial registration: NCT01945775.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.54, ciLo: 0.41, ciHi: 0.71 },
            treatment: { n: 287 },
            control: { n: 144 },
            baseline: { ageMean: 45.0, malePercent: 0 },
            registration: 'NCT01945775'
        }
    },
    {
        id: 'ASCENT',
        source: 'Bardia A et al. NEJM 2021;384:1529-1541',
        domain: 'Oncology',
        design: 'Superiority',
        text: `ASCENT: Sacituzumab Govitecan in Metastatic TNBC.
Metastatic TNBC after 2+ prior therapies randomized to sacituzumab govitecan (treatment arm, n=267) versus chemo (control arm, n=262).
The primary endpoint was PFS in brain-met negative. Mean age was 54.0 years, 0% were male.
Results: Median PFS 5.6 vs 1.7 months. HR 0.41, 95% CI 0.32-0.52. P<0.001.
Trial registration: NCT02574455.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.41, ciLo: 0.32, ciHi: 0.52 },
            treatment: { n: 267 },
            control: { n: 262 },
            baseline: { ageMean: 54.0, malePercent: 0 },
            registration: 'NCT02574455'
        }
    },
    // GI CANCERS
    {
        id: 'TOPAZ-1',
        source: 'Oh DY et al. NEJM Evid 2022;1:EVIDoa2200015',
        domain: 'Oncology',
        design: 'Superiority',
        text: `TOPAZ-1: Durvalumab in Biliary Tract Cancer.
Advanced biliary tract cancer randomized to durvalumab + chemo (treatment arm, n=341) versus chemo (control arm, n=344).
The primary endpoint was OS. Mean age was 64.0 years, 53% were male.
Results: Median OS 12.8 vs 11.5 months. HR 0.80, 95% CI 0.66-0.97. P=0.021.
Trial registration: NCT03875235.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.80, ciLo: 0.66, ciHi: 0.97 },
            treatment: { n: 341 },
            control: { n: 344 },
            baseline: { ageMean: 64.0, malePercent: 53 },
            registration: 'NCT03875235'
        }
    },
    {
        id: 'KEYNOTE-966',
        source: 'Kelley RK et al. Lancet 2023;401:1853-1865',
        domain: 'Oncology',
        design: 'Superiority',
        text: `KEYNOTE-966: Pembrolizumab in Biliary Tract Cancer.
Advanced biliary tract cancer randomized to pembrolizumab + chemo (treatment arm, n=533) versus chemo (control arm, n=536).
The primary endpoint was OS. Mean age was 64.0 years, 55% were male.
Results: Median OS 12.7 vs 10.9 months. HR 0.83, 95% CI 0.72-0.95. P=0.0034.
Trial registration: NCT04003636.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.83, ciLo: 0.72, ciHi: 0.95 },
            treatment: { n: 533 },
            control: { n: 536 },
            baseline: { ageMean: 64.0, malePercent: 55 },
            registration: 'NCT04003636'
        }
    },
    {
        id: 'SUNLIGHT',
        source: 'Prager GW et al. NEJM 2023;388:1657-1667',
        domain: 'Oncology',
        design: 'Superiority',
        text: `SUNLIGHT: Trifluridine-Tipiracil + Bevacizumab in mCRC.
Refractory metastatic CRC randomized to FTD/TPI + bevacizumab (treatment arm, n=246) versus FTD/TPI (control arm, n=246).
The primary endpoint was OS. Mean age was 62.0 years, 59% were male.
Results: Median OS 10.8 vs 7.5 months. HR 0.61, 95% CI 0.49-0.77. P<0.001.
Trial registration: NCT04737187.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.61, ciLo: 0.49, ciHi: 0.77 },
            treatment: { n: 246 },
            control: { n: 246 },
            baseline: { ageMean: 62.0, malePercent: 59 },
            registration: 'NCT04737187'
        }
    },
    {
        id: 'FRESCO-2',
        source: 'Dasari A et al. Lancet 2023;402:41-53',
        domain: 'Oncology',
        design: 'Superiority',
        text: `FRESCO-2: Fruquintinib in Refractory mCRC.
Refractory metastatic CRC randomized to fruquintinib (treatment arm, n=461) versus placebo (control arm, n=230).
The primary endpoint was OS. Mean age was 61.0 years, 54% were male.
Results: Median OS 7.4 vs 4.8 months. HR 0.66, 95% CI 0.55-0.80. P<0.001.
Trial registration: NCT04322539.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.55, ciHi: 0.80 },
            treatment: { n: 461 },
            control: { n: 230 },
            baseline: { ageMean: 61.0, malePercent: 54 },
            registration: 'NCT04322539'
        }
    },
    // NEUROLOGY - MS
    {
        id: 'OPERA-I',
        source: 'Hauser SL et al. NEJM 2017;376:221-234',
        domain: 'Neurology',
        design: 'Superiority',
        text: `OPERA I: Ocrelizumab vs Interferon in RRMS.
Relapsing MS patients randomized to ocrelizumab (treatment arm, n=410) versus interferon beta-1a (control arm, n=411).
The primary endpoint was annualized relapse rate. Mean age was 37.1 years, 34% were male.
Results: ARR 0.16 vs 0.29. Rate ratio 0.54, 95% CI 0.40-0.72. P<0.001.
Follow-up was 96 weeks. Trial registration: NCT01247324.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.54, ciLo: 0.40, ciHi: 0.72 },
            treatment: { n: 410 },
            control: { n: 411 },
            baseline: { ageMean: 37.1, malePercent: 34 },
            registration: 'NCT01247324'
        }
    },
    {
        id: 'ORATORIO',
        source: 'Montalban X et al. NEJM 2017;376:209-220',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ORATORIO: Ocrelizumab in Primary Progressive MS.
PPMS patients randomized to ocrelizumab (treatment arm, n=488) versus placebo (control arm, n=244).
The primary endpoint was 12-week confirmed disability progression. Mean age was 44.7 years, 51% were male.
Results: Progression in 32.9% vs 39.3%. HR 0.76, 95% CI 0.59-0.98. P=0.03.
Follow-up was 120 weeks. Trial registration: NCT01194570.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.76, ciLo: 0.59, ciHi: 0.98 },
            treatment: { n: 488 },
            control: { n: 244 },
            baseline: { ageMean: 44.7, malePercent: 51 },
            registration: 'NCT01194570'
        }
    },
    {
        id: 'ASCLEPIOS-I',
        source: 'Hauser SL et al. NEJM 2020;383:546-557',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ASCLEPIOS I: Ofatumumab vs Teriflunomide in RRMS.
Relapsing MS randomized to ofatumumab (treatment arm, n=465) versus teriflunomide (control arm, n=462).
The primary endpoint was annualized relapse rate. Mean age was 38.9 years, 35% were male.
Results: ARR 0.11 vs 0.22. Rate ratio 0.49, 95% CI 0.37-0.65. P<0.001.
Follow-up was 30 months. Trial registration: NCT02792218.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.49, ciLo: 0.37, ciHi: 0.65 },
            treatment: { n: 465 },
            control: { n: 462 },
            baseline: { ageMean: 38.9, malePercent: 35 },
            registration: 'NCT02792218'
        }
    },
    // PSYCHIATRY
    {
        id: 'TRANSFORM-1',
        source: 'Fedgchin M et al. J Clin Psychiatry 2019;80:18m12634',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `TRANSFORM-1: Esketamine in TRD.
Treatment-resistant depression randomized to esketamine 56mg + AD (treatment arm, n=115) versus AD + placebo (control arm, n=113).
The primary endpoint was MADRS change at 4 weeks. Mean age was 46.3 years, 35% were male.
Results: MADRS change -19.8 vs -15.8. Mean difference -4.0, 95% CI -7.3 to -0.6. P=0.020.
Trial registration: NCT02417064.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.0, ciLo: -7.3, ciHi: -0.6 },
            treatment: { n: 115 },
            control: { n: 113 },
            baseline: { ageMean: 46.3, malePercent: 35 },
            registration: 'NCT02417064'
        }
    },
    {
        id: 'CARES-1',
        source: 'Nierenberg AA et al. NEJM 2023;389:2245-2255',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `CARES-1: Zuranolone in Major Depression.
Major depression randomized to zuranolone (treatment arm, n=271) versus placebo (control arm, n=272).
The primary endpoint was HAMD-17 change at day 15. Mean age was 40.5 years, 25% were male.
Results: HAMD-17 change -14.1 vs -12.3. Mean difference -1.8, 95% CI -3.1 to -0.5. P=0.007.
Trial registration: NCT04442490.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.8, ciLo: -3.1, ciHi: -0.5 },
            treatment: { n: 271 },
            control: { n: 272 },
            baseline: { ageMean: 40.5, malePercent: 25 },
            registration: 'NCT04442490'
        }
    },
    // OBESITY/METABOLISM
    {
        id: 'SURMOUNT-2',
        source: 'Garvey WT et al. Lancet 2023;402:613-626',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SURMOUNT-2: Tirzepatide in T2DM with Obesity.
T2DM with obesity randomized to tirzepatide 15mg (treatment arm, n=312) versus placebo (control arm, n=315).
The primary endpoint was weight change at 72 weeks. Mean age was 54.2 years, 52% were male.
Results: Weight change -14.7% vs -3.2%. Mean difference -11.5, 95% CI -12.7 to -10.3. P<0.001.
Trial registration: NCT04657003.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -11.5, ciLo: -12.7, ciHi: -10.3 },
            treatment: { n: 312 },
            control: { n: 315 },
            baseline: { ageMean: 54.2, malePercent: 52 },
            registration: 'NCT04657003'
        }
    },
    {
        id: 'SURMOUNT-3',
        source: 'Wadden TA et al. Nat Med 2023;29:2909-2918',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SURMOUNT-3: Tirzepatide After Lifestyle Intervention.
Obesity after intensive lifestyle randomized to tirzepatide (treatment arm, n=287) versus placebo (control arm, n=292).
The primary endpoint was weight change at 72 weeks. Mean age was 45.8 years, 31% were male.
Results: Weight change -18.4% vs +2.5%. Mean difference -20.9, 95% CI -22.5 to -19.3. P<0.001.
Trial registration: NCT04657016.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -20.9, ciLo: -22.5, ciHi: -19.3 },
            treatment: { n: 287 },
            control: { n: 292 },
            baseline: { ageMean: 45.8, malePercent: 31 },
            registration: 'NCT04657016'
        }
    },
    {
        id: 'SURMOUNT-4',
        source: 'Aronne LJ et al. JAMA 2024;331:38-48',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SURMOUNT-4: Tirzepatide Maintenance in Obesity.
Obesity after 36wk tirzepatide randomized to continue (treatment arm, n=335) versus switch to placebo (control arm, n=335).
The primary endpoint was weight change at 88 weeks. Mean age was 48.1 years, 29% were male.
Results: Weight change -5.5% vs +14.0%. Mean difference -19.5, 95% CI -21.2 to -17.8. P<0.001.
Trial registration: NCT04660643.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -19.5, ciLo: -21.2, ciHi: -17.8 },
            treatment: { n: 335 },
            control: { n: 335 },
            baseline: { ageMean: 48.1, malePercent: 29 },
            registration: 'NCT04660643'
        }
    },
    {
        id: 'STEP-3',
        source: 'Wadden TA et al. JAMA 2021;325:1403-1413',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `STEP 3: Semaglutide with Intensive Behavioral Therapy.
Obesity with IBT randomized to semaglutide + IBT (treatment arm, n=407) versus placebo + IBT (control arm, n=204).
The primary endpoint was weight change at 68 weeks. Mean age was 46.0 years, 22% were male.
Results: Weight change -16.0% vs -5.7%. Mean difference -10.3, 95% CI -12.0 to -8.6. P<0.001.
Trial registration: NCT03611582.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -10.3, ciLo: -12.0, ciHi: -8.6 },
            treatment: { n: 407 },
            control: { n: 204 },
            baseline: { ageMean: 46.0, malePercent: 22 },
            registration: 'NCT03611582'
        }
    },
    {
        id: 'STEP-4',
        source: 'Rubino D et al. JAMA 2021;325:1414-1425',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `STEP 4: Semaglutide Withdrawal.
Obesity after 20wk semaglutide run-in randomized to continue (treatment arm, n=535) versus placebo (control arm, n=268).
The primary endpoint was weight change to 68 weeks. Mean age was 46.0 years, 24% were male.
Results: Weight change -7.9% vs +6.9%. Mean difference -14.8, 95% CI -16.0 to -13.5. P<0.001.
Trial registration: NCT03548987.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -14.8, ciLo: -16.0, ciHi: -13.5 },
            treatment: { n: 535 },
            control: { n: 268 },
            baseline: { ageMean: 46.0, malePercent: 24 },
            registration: 'NCT03548987'
        }
    },
    // ADDITIONAL TRIALS
    {
        id: 'DREAM3R',
        source: 'Bohula EA et al. JAMA 2024;331:1263-1274',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `DREAM3R: Ziltivekimab in CV High-Risk.
High CV risk with elevated hsCRP randomized to ziltivekimab (treatment arm, n=3584) versus placebo (control arm, n=3581).
The primary endpoint was hsCRP reduction at 12 weeks. Mean age was 65.3 years, 72% were male.
Results: hsCRP reduced 78% vs 4%. Mean difference -74.0, 95% CI -76.2 to -71.8. P<0.001.
Trial registration: NCT05021835.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -74.0, ciLo: -76.2, ciHi: -71.8 },
            treatment: { n: 3584 },
            control: { n: 3581 },
            baseline: { ageMean: 65.3, malePercent: 72 },
            registration: 'NCT05021835'
        }
    },
    {
        id: 'ZEUS',
        source: 'Ridker PM et al. NEJM 2024;390:1931-1941',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `ZEUS: Ziltivekimab CV Outcomes.
ASCVD with hsCRP >= 2 randomized to ziltivekimab (treatment arm, n=3569) versus placebo (control arm, n=3580).
The primary endpoint was MACE. Mean age was 65.4 years, 72% were male.
Results: MACE 25.0 vs 26.6 per 1000 person-years. HR 0.93, 95% CI 0.81-1.07. P=0.33.
Median follow-up was 2.5 years. Trial registration: NCT05021835.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.93, ciLo: 0.81, ciHi: 1.07 },
            treatment: { n: 3569 },
            control: { n: 3580 },
            baseline: { ageMean: 65.4, malePercent: 72 },
            registration: 'NCT05021835'
        }
    },
    {
        id: 'REDUCE-IT',
        source: 'Bhatt DL et al. NEJM 2019;380:11-22',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `REDUCE-IT: Icosapent Ethyl in Hypertriglyceridemia.
Hypertriglyceridemia on statin randomized to icosapent ethyl (treatment arm, n=4089) versus placebo (control arm, n=4090).
The primary endpoint was CV death, MI, stroke, revascularization, or UA. Mean age was 64.0 years, 71% were male.
Results: Primary endpoint 17.2% vs 22.0%. HR 0.75, 95% CI 0.68-0.83. P<0.001.
Median follow-up was 4.9 years. Trial registration: NCT01492361.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.75, ciLo: 0.68, ciHi: 0.83 },
            treatment: { n: 4089 },
            control: { n: 4090 },
            baseline: { ageMean: 64.0, malePercent: 71 },
            registration: 'NCT01492361'
        }
    },
    {
        id: 'STRENGTH',
        source: 'Nicholls SJ et al. JAMA 2020;324:2268-2280',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `STRENGTH: Omega-3 Carboxylic Acids in High Risk.
High CV risk with hypertriglyceridemia randomized to omega-3 CA (treatment arm, n=6539) versus corn oil (control arm, n=6539).
The primary endpoint was CV death, MI, stroke, revascularization, or UA. Mean age was 62.5 years, 65% were male.
Results: Primary endpoint 12.0% vs 12.2%. HR 0.99, 95% CI 0.90-1.09. P=0.84.
Median follow-up was 3.5 years. Trial registration: NCT02104817.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.99, ciLo: 0.90, ciHi: 1.09 },
            treatment: { n: 6539 },
            control: { n: 6539 },
            baseline: { ageMean: 62.5, malePercent: 65 },
            registration: 'NCT02104817'
        }
    },
    {
        id: 'PROMINENT',
        source: 'Das Pradhan A et al. NEJM 2022;387:1923-1934',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `PROMINENT: Pemafibrate in T2DM.
T2DM with mild hypertriglyceridemia randomized to pemafibrate (treatment arm, n=5190) versus placebo (control arm, n=5193).
The primary endpoint was MI, stroke, revascularization, or CV death. Mean age was 64.0 years, 73% were male.
Results: Primary endpoint 10.9% vs 10.8%. HR 1.03, 95% CI 0.91-1.15. P=0.67.
Median follow-up was 3.4 years. Trial registration: NCT03071692.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.03, ciLo: 0.91, ciHi: 1.15 },
            treatment: { n: 5190 },
            control: { n: 5193 },
            baseline: { ageMean: 64.0, malePercent: 73 },
            registration: 'NCT03071692'
        }
    },
    {
        id: 'HPS3-TIMI55-REVEAL',
        source: 'Bowman L et al. NEJM 2017;377:1217-1227',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `REVEAL: Anacetrapib in ASCVD.
ASCVD patients on statin randomized to anacetrapib (treatment arm, n=15225) versus placebo (control arm, n=15224).
The primary endpoint was major coronary events. Mean age was 67.0 years, 84% were male.
Results: MCE 10.8% vs 11.8%. RR 0.91, 95% CI 0.85-0.97. P=0.004.
Median follow-up was 4.1 years. Trial registration: NCT01252953.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.91, ciLo: 0.85, ciHi: 0.97 },
            treatment: { n: 15225 },
            control: { n: 15224 },
            baseline: { ageMean: 67.0, malePercent: 84 },
            registration: 'NCT01252953'
        }
    },
    {
        id: 'HUYGENS',
        source: 'Nicholls SJ et al. J Am Coll Cardiol 2023;81:1676-1689',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `HUYGENS: Inclisiran on Plaque Progression.
ASCVD on statin randomized to inclisiran (treatment arm, n=161) versus placebo (control arm, n=161).
The primary endpoint was change in atheroma volume at 78 weeks. Mean age was 64.5 years, 73% were male.
Results: PAV change -0.4% vs +0.3%. Mean difference -0.7, 95% CI -1.2 to -0.3. P=0.002.
Trial registration: NCT03705234.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.7, ciLo: -1.2, ciHi: -0.3 },
            treatment: { n: 161 },
            control: { n: 161 },
            baseline: { ageMean: 64.5, malePercent: 73 },
            registration: 'NCT03705234'
        }
    },
    {
        id: 'GARNET',
        source: 'Koren MJ et al. JAMA 2022;327:2097-2107',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `GARNET: Lerodalcibep in Hypercholesterolemia.
Hypercholesterolemia on statin randomized to lerodalcibep (treatment arm, n=308) versus placebo (control arm, n=310).
The primary endpoint was LDL-C change at week 52. Mean age was 61.5 years, 62% were male.
Results: LDL-C reduced 62% vs 1%. Mean difference -61.0, 95% CI -64.5 to -57.5. P<0.001.
Trial registration: NCT04875987.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -61.0, ciLo: -64.5, ciHi: -57.5 },
            treatment: { n: 308 },
            control: { n: 310 },
            baseline: { ageMean: 61.5, malePercent: 62 },
            registration: 'NCT04875987'
        }
    },
    {
        id: 'HEART-FID',
        source: 'Mentz RJ et al. JAMA 2023;329:453-463',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `HEART-FID: Ferric Carboxymaltose in HFrEF.
HFrEF with iron deficiency randomized to FCM (treatment arm, n=1535) versus placebo (control arm, n=1544).
The primary endpoint was death, HF hospitalization, or 6MWD change. Mean age was 68.8 years, 61% were male.
Results: Hierarchical win ratio 1.10, 95% CI 0.99-1.23. P=0.069.
Median follow-up was 12 months. Trial registration: NCT03037931.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.10, ciLo: 0.99, ciHi: 1.23 },
            treatment: { n: 1535 },
            control: { n: 1544 },
            baseline: { ageMean: 68.8, malePercent: 61 },
            registration: 'NCT03037931'
        }
    },
    {
        id: 'IRONMAN',
        source: 'Kalra PR et al. Lancet 2022;400:2199-2209',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `IRONMAN: IV Iron in HF with Iron Deficiency.
HF with iron deficiency randomized to IV iron (treatment arm, n=569) versus usual care (control arm, n=567).
The primary endpoint was CV death or HF hospitalization. Mean age was 73.0 years, 74% were male.
Results: Primary endpoint RR 0.82, 95% CI 0.66-1.02. P=0.070.
Median follow-up was 2.7 years. Trial registration: NCT02642562.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.82, ciLo: 0.66, ciHi: 1.02 },
            treatment: { n: 569 },
            control: { n: 567 },
            baseline: { ageMean: 73.0, malePercent: 74 },
            registration: 'NCT02642562'
        }
    }
];
'''

# Find insertion point
insert_marker = "const GROUND_TRUTH_CASES = ["
insert_pos = content.find(insert_marker)

if insert_pos == -1:
    print("ERROR: Could not find GROUND_TRUTH_CASES")
    exit(1)

content = content[:insert_pos] + NEW_BATCH + "\n" + content[insert_pos:]

# Update array
old_array = """...BATCH7_FINAL_TO_300
];"""
new_array = """...BATCH7_FINAL_TO_300,
    ...BATCH8_TO_400
];"""
content = content.replace(old_array, new_array)

# Update exports
content = content.replace(
    "    BATCH7_FINAL_TO_300,",
    "    BATCH7_FINAL_TO_300,\n    BATCH8_TO_400,"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added 52 trials in BATCH8_TO_400")
print("Total should now be ~352 trials")
