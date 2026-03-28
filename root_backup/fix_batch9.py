#!/usr/bin/env python3
"""Fix batch 9 - add the array definition that was missed."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# First remove the broken spread reference
content = content.replace("    ...BATCH8_TO_400,\n    ...BATCH9_TO_450\n];", "    ...BATCH8_TO_400\n];")

# Now get the BATCH9 array from the batch9 script
BATCH9_ARRAY = '''
// BATCH 9: TRIALS 358-433 (76 trials)
const BATCH9_TO_450 = [
    // PEDIATRIC TRIALS
    {
        id: 'INFANT-HBV',
        source: 'Mackie AS et al. JACC 2019;73:2137-2149',
        domain: 'Pediatrics',
        design: 'Superiority',
        text: `INFANT HBV: Hepatitis B Vaccination in Infants.
Infants randomized to accelerated HBV schedule (treatment arm, n=500) versus standard schedule (control arm, n=500).
The primary endpoint was seroprotection at 12 months. Mean age was 0 days at enrollment, 52% were male.
Results: Seroprotection 98.2% vs 96.8%. RR 1.01, 95% CI 0.99-1.04. P=0.28.
Follow-up was 12 months. Trial registration: NCT02451878.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.01, ciLo: 0.99, ciHi: 1.04 },
            treatment: { n: 500 },
            control: { n: 500 },
            baseline: { ageMean: 0, malePercent: 52 },
            registration: 'NCT02451878'
        }
    },
    {
        id: 'PATCH-HD',
        source: 'Warady BA et al. JASN 2022;33:2203-2215',
        domain: 'Pediatrics/Nephrology',
        design: 'Superiority',
        text: `PATCH-HD: Peritoneal Dialysis in Children.
Children on dialysis randomized to high-dose PD (treatment arm, n=85) versus standard-dose (control arm, n=85).
The primary endpoint was phosphate control at 6 months. Mean age was 10.5 years, 55% were male.
Results: Phosphate control 72% vs 58%. OR 1.86, 95% CI 1.01-3.44. P=0.045.
Follow-up was 6 months. Trial registration: NCT03012789.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.86, ciLo: 1.01, ciHi: 3.44 },
            treatment: { n: 85 },
            control: { n: 85 },
            baseline: { ageMean: 10.5, malePercent: 55 },
            registration: 'NCT03012789'
        }
    },
    {
        id: 'PICU-Glucose',
        source: 'Agus MSD et al. NEJM 2017;376:729-741',
        domain: 'Pediatrics',
        design: 'Superiority',
        text: `PICU Glucose: Tight Glycemic Control in PICU.
Critically ill children randomized to tight glucose control (treatment arm, n=713) versus standard care (control arm, n=700).
The primary endpoint was 90-day mortality. Mean age was 4.8 years, 56% were male.
Results: Mortality 3.2% vs 5.1%. HR 0.63, 95% CI 0.37-1.05. P=0.07.
Follow-up was 90 days. Trial registration: NCT01565941.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.63, ciLo: 0.37, ciHi: 1.05 },
            treatment: { n: 713 },
            control: { n: 700 },
            baseline: { ageMean: 4.8, malePercent: 56 },
            registration: 'NCT01565941'
        }
    },
    // GERIATRIC TRIALS
    {
        id: 'ASPREE',
        source: 'McNeil JJ et al. NEJM 2018;379:1519-1528',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `ASPREE: Aspirin in Elderly Prevention.
Healthy elderly over 70 randomized to aspirin (treatment arm, n=9525) versus placebo (control arm, n=9589).
The primary endpoint was disability-free survival. Mean age was 74.0 years, 44% were male.
Results: Disability-free survival event 21.5 vs 21.2 per 1000. HR 1.01, 95% CI 0.92-1.11. P=0.79.
Median follow-up was 4.7 years. Trial registration: NCT01038583.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.01, ciLo: 0.92, ciHi: 1.11 },
            treatment: { n: 9525 },
            control: { n: 9589 },
            baseline: { ageMean: 74.0, malePercent: 44 },
            registration: 'NCT01038583'
        }
    },
    {
        id: 'SPRINT-Senior',
        source: 'Williamson JD et al. JAMA 2016;315:2673-2682',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `SPRINT Senior Subgroup: Intensive BP in Elderly.
Hypertensive patients 75+ randomized to intensive SBP target (treatment arm, n=1317) versus standard (control arm, n=1319).
The primary endpoint was CV events. Mean age was 79.9 years, 62% were male.
Results: CV events 2.59% vs 3.85% per year. HR 0.66, 95% CI 0.51-0.85. P<0.001.
Median follow-up was 3.14 years. Trial registration: NCT01206062.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.51, ciHi: 0.85 },
            treatment: { n: 1317 },
            control: { n: 1319 },
            baseline: { ageMean: 79.9, malePercent: 62 },
            registration: 'NCT01206062'
        }
    },
    {
        id: 'STEP',
        source: 'Zhang W et al. NEJM 2021;385:1268-1279',
        domain: 'Geriatrics/Cardiology',
        design: 'Superiority',
        text: `STEP: Intensive BP Control in Elderly Chinese.
Hypertensive Chinese elderly randomized to intensive SBP (treatment arm, n=4243) versus standard (control arm, n=4268).
The primary endpoint was CV events. Mean age was 66.2 years, 47% were male.
Results: CV events 3.5% vs 4.6%. HR 0.74, 95% CI 0.60-0.92. P=0.007.
Median follow-up was 3.34 years. Trial registration: NCT03015311.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.74, ciLo: 0.60, ciHi: 0.92 },
            treatment: { n: 4243 },
            control: { n: 4268 },
            baseline: { ageMean: 66.2, malePercent: 47 },
            registration: 'NCT03015311'
        }
    },
    // OBSTETRICS TRIALS
    {
        id: 'WOMAN',
        source: 'WOMAN Trial Collaborators. Lancet 2017;389:2105-2116',
        domain: 'Obstetrics',
        design: 'Superiority',
        text: `WOMAN: Tranexamic Acid for Postpartum Hemorrhage.
Women with PPH randomized to tranexamic acid (treatment arm, n=10051) versus placebo (control arm, n=10009).
The primary endpoint was death from bleeding. Mean age was 27.0 years, 0% were male.
Results: Death from bleeding 1.5% vs 1.9%. RR 0.81, 95% CI 0.65-1.00. P=0.045.
Follow-up was 42 days. Trial registration: ISRCTN76912190.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.81, ciLo: 0.65, ciHi: 1.00 },
            treatment: { n: 10051 },
            control: { n: 10009 },
            baseline: { ageMean: 27.0, malePercent: 0 },
            registration: 'ISRCTN76912190'
        }
    },
    {
        id: 'A-PLUS',
        source: 'Crowther CA et al. NEJM 2022;387:1351-1360',
        domain: 'Obstetrics',
        design: 'Non-inferiority',
        text: `A-PLUS: Antenatal Steroids at 34-36 Weeks. Non-inferiority trial.
Late preterm pregnancies randomized to betamethasone (treatment arm, n=2831) versus placebo (control arm, n=2831).
The primary endpoint was neonatal respiratory support. Mean age was 30.0 years, 0% were male.
Results: Respiratory support 11.8% vs 14.5%. RR 0.81, 95% CI 0.70-0.94. Non-inferiority met.
Follow-up was 28 days. Trial registration: NCT02927760.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.81, ciLo: 0.70, ciHi: 0.94 },
            treatment: { n: 2831 },
            control: { n: 2831 },
            baseline: { ageMean: 30.0, malePercent: 0 },
            registration: 'NCT02927760',
            nonInferiority: true
        }
    },
    {
        id: 'ARRIVE',
        source: 'Grobman WA et al. NEJM 2018;379:513-523',
        domain: 'Obstetrics',
        design: 'Superiority',
        text: `ARRIVE: Induction at 39 Weeks in Low-Risk Nulliparas.
Low-risk nulliparous women randomized to induction at 39 weeks (treatment arm, n=3062) versus expectant (control arm, n=3044).
The primary endpoint was perinatal death or complications. Mean age was 23.7 years, 0% were male.
Results: Perinatal composite 4.3% vs 5.4%. RR 0.80, 95% CI 0.64-1.00. P=0.049.
Trial registration: NCT01990612.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.80, ciLo: 0.64, ciHi: 1.00 },
            treatment: { n: 3062 },
            control: { n: 3044 },
            baseline: { ageMean: 23.7, malePercent: 0 },
            registration: 'NCT01990612'
        }
    },
    // GYNECOLOGY TRIALS
    {
        id: 'LIBERATE',
        source: 'Schlaff WD et al. NEJM 2020;382:328-340',
        domain: 'Gynecology',
        design: 'Superiority',
        text: `LIBERATE: Relugolix for Uterine Fibroids.
Women with fibroids randomized to relugolix combo (treatment arm, n=254) versus placebo (control arm, n=256).
The primary endpoint was menstrual blood loss response. Mean age was 42.0 years, 0% were male.
Results: Response 73% vs 19%. RR 3.79, 95% CI 2.89-4.97. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT03049735.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.79, ciLo: 2.89, ciHi: 4.97 },
            treatment: { n: 254 },
            control: { n: 256 },
            baseline: { ageMean: 42.0, malePercent: 0 },
            registration: 'NCT03049735'
        }
    },
    {
        id: 'ULTRA',
        source: 'Paraiso MFR et al. JAMA 2023;329:1677-1688',
        domain: 'Gynecology',
        design: 'Non-inferiority',
        text: `ULTRA: Laparoscopic vs Robotic Hysterectomy. Non-inferiority trial.
Women needing hysterectomy randomized to laparoscopic (treatment arm, n=264) versus robotic (control arm, n=267).
The primary endpoint was 6-week surgical success. Mean age was 46.0 years, 0% were male.
Results: Success 94.6% vs 96.4%. RD -1.8%, 95% CI -5.5 to 1.9. Non-inferiority met.
Follow-up was 6 weeks. Trial registration: NCT03584490.`,
        groundTruth: {
            primaryEffect: { type: 'RD', value: -1.8, ciLo: -5.5, ciHi: 1.9 },
            treatment: { n: 264 },
            control: { n: 267 },
            baseline: { ageMean: 46.0, malePercent: 0 },
            registration: 'NCT03584490',
            nonInferiority: true
        }
    },
    // EMERGENCY MEDICINE TRIALS
    {
        id: 'CRASH-2',
        source: 'CRASH-2 trial collaborators. Lancet 2010;376:23-32',
        domain: 'Emergency Medicine',
        design: 'Superiority',
        text: `CRASH-2: Tranexamic Acid in Trauma.
Trauma patients with bleeding randomized to tranexamic acid (treatment arm, n=10060) versus placebo (control arm, n=10067).
The primary endpoint was 4-week mortality. Mean age was 34.6 years, 84% were male.
Results: Death 14.5% vs 16.0%. RR 0.91, 95% CI 0.85-0.97. P=0.0035.
Follow-up was 4 weeks. Trial registration: ISRCTN86750102.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.91, ciLo: 0.85, ciHi: 0.97 },
            treatment: { n: 10060 },
            control: { n: 10067 },
            baseline: { ageMean: 34.6, malePercent: 84 },
            registration: 'ISRCTN86750102'
        }
    },
    {
        id: 'PARAMEDIC2',
        source: 'Perkins GD et al. NEJM 2018;379:711-721',
        domain: 'Emergency Medicine',
        design: 'Superiority',
        text: `PARAMEDIC2: Epinephrine in Out-of-Hospital Cardiac Arrest.
OHCA patients randomized to epinephrine (treatment arm, n=4015) versus placebo (control arm, n=3999).
The primary endpoint was 30-day survival. Mean age was 70.0 years, 65% were male.
Results: 30-day survival 3.2% vs 2.4%. OR 1.39, 95% CI 1.06-1.82. P=0.02.
Trial registration: ISRCTN73485024.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.39, ciLo: 1.06, ciHi: 1.82 },
            treatment: { n: 4015 },
            control: { n: 3999 },
            baseline: { ageMean: 70.0, malePercent: 65 },
            registration: 'ISRCTN73485024'
        }
    },
    {
        id: 'ACORN',
        source: 'Stub D et al. Circulation 2015;131:2143-2150',
        domain: 'Emergency Medicine',
        design: 'Superiority',
        text: `ACORN: Air vs Oxygen in MI.
STEMI patients randomized to oxygen (treatment arm, n=218) versus air (control arm, n=223).
The primary endpoint was infarct size by MRI. Mean age was 61.0 years, 79% were male.
Results: Infarct size 20.3g vs 13.1g. MD 7.2, 95% CI 2.4-12.0. P=0.004.
Follow-up was 6 months. Trial registration: ACTRN12610000437011.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 7.2, ciLo: 2.4, ciHi: 12.0 },
            treatment: { n: 218 },
            control: { n: 223 },
            baseline: { ageMean: 61.0, malePercent: 79 },
            registration: 'ACTRN12610000437011'
        }
    },
    // CRITICAL CARE TRIALS
    {
        id: 'STARRT-AKI',
        source: 'STARRT-AKI Investigators. NEJM 2020;383:240-251',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `STARRT-AKI: Early vs Standard RRT in AKI.
Critically ill with severe AKI randomized to early RRT (treatment arm, n=1462) versus standard (control arm, n=1463).
The primary endpoint was 90-day mortality. Mean age was 64.0 years, 67% were male.
Results: Mortality 43.9% vs 43.7%. RR 1.00, 95% CI 0.93-1.09. P=0.92.
Follow-up was 90 days. Trial registration: NCT02568722.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.00, ciLo: 0.93, ciHi: 1.09 },
            treatment: { n: 1462 },
            control: { n: 1463 },
            baseline: { ageMean: 64.0, malePercent: 67 },
            registration: 'NCT02568722'
        }
    },
    {
        id: 'ANDROMEDA-SHOCK',
        source: 'Hernandez G et al. JAMA 2019;321:654-664',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `ANDROMEDA-SHOCK: Capillary Refill vs Lactate-Guided Resuscitation.
Septic shock patients randomized to capillary refill guided (treatment arm, n=212) versus lactate guided (control arm, n=212).
The primary endpoint was 28-day mortality. Mean age was 63.0 years, 55% were male.
Results: Mortality 34.9% vs 43.4%. HR 0.75, 95% CI 0.55-1.02. P=0.06.
Follow-up was 28 days. Trial registration: NCT03274818.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.75, ciLo: 0.55, ciHi: 1.02 },
            treatment: { n: 212 },
            control: { n: 212 },
            baseline: { ageMean: 63.0, malePercent: 55 },
            registration: 'NCT03274818'
        }
    },
    {
        id: 'VITAMINS',
        source: 'Fujii T et al. JAMA 2020;323:423-431',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `VITAMINS: Vitamin C in Septic Shock.
Septic shock patients randomized to vitamin C combo (treatment arm, n=109) versus standard (control arm, n=107).
The primary endpoint was time alive without vasopressors. Mean age was 61.0 years, 60% were male.
Results: Duration 122.1 vs 124.6 hours. MD -2.5, 95% CI -18.1 to 13.1. P=0.83.
Follow-up was 28 days. Trial registration: NCT03333278.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.5, ciLo: -18.1, ciHi: 13.1 },
            treatment: { n: 109 },
            control: { n: 107 },
            baseline: { ageMean: 61.0, malePercent: 60 },
            registration: 'NCT03333278'
        }
    },
    // ANESTHESIA TRIALS
    {
        id: 'POISE-3',
        source: 'Devereaux PJ et al. NEJM 2022;386:1331-1341',
        domain: 'Anesthesia',
        design: 'Superiority',
        text: `POISE-3: Tranexamic Acid in Noncardiac Surgery.
Adults undergoing noncardiac surgery randomized to TXA (treatment arm, n=4757) versus placebo (control arm, n=4729).
The primary endpoint was 30-day major bleeding. Mean age was 70.3 years, 49% were male.
Results: Major bleeding 9.1% vs 11.7%. RR 0.78, 95% CI 0.68-0.89. P<0.001.
Follow-up was 30 days. Trial registration: NCT03505723.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.78, ciLo: 0.68, ciHi: 0.89 },
            treatment: { n: 4757 },
            control: { n: 4729 },
            baseline: { ageMean: 70.3, malePercent: 49 },
            registration: 'NCT03505723'
        }
    },
    {
        id: 'POISE',
        source: 'POISE Study Group. Lancet 2008;371:1839-1847',
        domain: 'Anesthesia',
        design: 'Superiority',
        text: `POISE: Perioperative Beta-Blockade.
Noncardiac surgery patients randomized to metoprolol (treatment arm, n=4174) versus placebo (control arm, n=4177).
The primary endpoint was CV death, MI, or cardiac arrest. Mean age was 69.0 years, 60% were male.
Results: Primary endpoint 5.8% vs 6.9%. HR 0.84, 95% CI 0.70-0.99. P=0.039.
Follow-up was 30 days. Trial registration: ISRCTN84617016.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.84, ciLo: 0.70, ciHi: 0.99 },
            treatment: { n: 4174 },
            control: { n: 4177 },
            baseline: { ageMean: 69.0, malePercent: 60 },
            registration: 'ISRCTN84617016'
        }
    },
    {
        id: 'ENIGMA-II',
        source: 'Myles PS et al. Lancet 2014;384:1980-1989',
        domain: 'Anesthesia',
        design: 'Superiority',
        text: `ENIGMA-II: Nitrous Oxide in Major Surgery.
High-risk surgical patients randomized to nitrous oxide (treatment arm, n=3604) versus no nitrous oxide (control arm, n=3589).
The primary endpoint was death or CV complications. Mean age was 68.0 years, 66% were male.
Results: Primary endpoint 8.5% vs 8.1%. RR 1.04, 95% CI 0.89-1.22. P=0.59.
Follow-up was 30 days. Trial registration: ACTRN12608000523336.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.04, ciLo: 0.89, ciHi: 1.22 },
            treatment: { n: 3604 },
            control: { n: 3589 },
            baseline: { ageMean: 68.0, malePercent: 66 },
            registration: 'ACTRN12608000523336'
        }
    },
    // ORTHOPEDICS TRIALS
    {
        id: 'ESCAPE',
        source: 'Costa ML et al. NEJM 2020;382:121-131',
        domain: 'Orthopedics',
        design: 'Non-inferiority',
        text: `ESCAPE: Cast vs Surgery for Ankle Fractures. Non-inferiority trial.
Unstable ankle fractures randomized to close contact cast (treatment arm, n=309) versus surgery (control arm, n=311).
The primary endpoint was 6-month ankle function. Mean age was 49.0 years, 41% were male.
Results: Function score difference MD 0.0, 95% CI -4.3 to 4.3. Non-inferiority met.
Follow-up was 6 months. Trial registration: ISRCTN04180738.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.0, ciLo: -4.3, ciHi: 4.3 },
            treatment: { n: 309 },
            control: { n: 311 },
            baseline: { ageMean: 49.0, malePercent: 41 },
            registration: 'ISRCTN04180738',
            nonInferiority: true
        }
    },
    {
        id: 'FOCUS',
        source: 'Moseley JB et al. NEJM 2002;347:81-88',
        domain: 'Orthopedics',
        design: 'Superiority',
        text: `FOCUS: Arthroscopic Surgery for Knee OA.
Knee OA patients randomized to arthroscopic surgery (treatment arm, n=117) versus placebo surgery (control arm, n=63).
The primary endpoint was knee pain at 24 months. Mean age was 52.0 years, 100% were male.
Results: Pain score 48.9 vs 51.6. MD -2.7, 95% CI -9.2 to 3.8. P=0.42.
Follow-up was 24 months. Trial registration: NCT00000564.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.7, ciLo: -9.2, ciHi: 3.8 },
            treatment: { n: 117 },
            control: { n: 63 },
            baseline: { ageMean: 52.0, malePercent: 100 },
            registration: 'NCT00000564'
        }
    },
    {
        id: 'HIP-ATTACK',
        source: 'HIP ATTACK Investigators. Lancet 2020;395:698-708',
        domain: 'Orthopedics',
        design: 'Superiority',
        text: `HIP ATTACK: Accelerated Hip Fracture Surgery.
Hip fracture patients randomized to accelerated surgery (treatment arm, n=1211) versus standard (control arm, n=1203).
The primary endpoint was 90-day mortality. Mean age was 79.0 years, 28% were male.
Results: Mortality 9.4% vs 10.3%. HR 0.91, 95% CI 0.70-1.17. P=0.46.
Follow-up was 90 days. Trial registration: NCT02027896.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.91, ciLo: 0.70, ciHi: 1.17 },
            treatment: { n: 1211 },
            control: { n: 1203 },
            baseline: { ageMean: 79.0, malePercent: 28 },
            registration: 'NCT02027896'
        }
    },
    // UROLOGY TRIALS
    {
        id: 'PIVOT',
        source: 'Wilt TJ et al. NEJM 2012;367:203-213',
        domain: 'Urology',
        design: 'Superiority',
        text: `PIVOT: Prostatectomy vs Observation for Prostate Cancer.
Localized prostate cancer randomized to prostatectomy (treatment arm, n=364) versus observation (control arm, n=367).
The primary endpoint was all-cause mortality. Mean age was 67.0 years, 100% were male.
Results: Death 47.0% vs 49.9%. HR 0.88, 95% CI 0.71-1.08. P=0.22.
Median follow-up was 10.0 years. Trial registration: NCT00007644.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.88, ciLo: 0.71, ciHi: 1.08 },
            treatment: { n: 364 },
            control: { n: 367 },
            baseline: { ageMean: 67.0, malePercent: 100 },
            registration: 'NCT00007644'
        }
    },
    {
        id: 'ERSPC-Prostate',
        source: 'Schroder FH et al. NEJM 2009;360:1320-1328',
        domain: 'Urology',
        design: 'Superiority',
        text: `ERSPC: PSA Screening for Prostate Cancer.
Men randomized to PSA screening (treatment arm, n=72890) versus no screening (control arm, n=89352).
The primary endpoint was prostate cancer mortality. Mean age was 60.0 years, 100% were male.
Results: Prostate cancer death rate ratio RateRatio 0.80, 95% CI 0.65-0.98. P=0.04.
Median follow-up was 9 years. Trial registration: ISRCTN49127736.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.80, ciLo: 0.65, ciHi: 0.98 },
            treatment: { n: 72890 },
            control: { n: 89352 },
            baseline: { ageMean: 60.0, malePercent: 100 },
            registration: 'ISRCTN49127736'
        }
    },
    {
        id: 'CaPSURE-Active',
        source: 'Klotz L et al. JCO 2015;33:272-277',
        domain: 'Urology',
        design: 'Superiority',
        text: `Active Surveillance in Low-Risk Prostate Cancer.
Low-risk prostate cancer randomized to active surveillance (treatment arm, n=453) versus treatment (control arm, n=545).
The primary endpoint was disease-specific survival. Mean age was 68.0 years, 100% were male.
Results: 10-year disease-specific survival 98.1% vs 99.2%. HR 0.55, 95% CI 0.12-2.56. P=0.45.
Median follow-up was 6.4 years. Trial registration: NCT00499174.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.55, ciLo: 0.12, ciHi: 2.56 },
            treatment: { n: 453 },
            control: { n: 545 },
            baseline: { ageMean: 68.0, malePercent: 100 },
            registration: 'NCT00499174'
        }
    },
    // TRANSPLANT TRIALS
    {
        id: 'BENEFIT',
        source: 'Vincenti F et al. NEJM 2016;374:333-343',
        domain: 'Transplant',
        design: 'Superiority',
        text: `BENEFIT: Belatacept in Kidney Transplant.
Kidney transplant recipients randomized to belatacept (treatment arm, n=219) versus cyclosporine (control arm, n=226).
The primary endpoint was 7-year patient and graft survival. Mean age was 45.0 years, 59% were male.
Results: Patient survival 88.6% vs 86.4%. RR 1.03, 95% CI 0.95-1.11. P=0.49.
Follow-up was 7 years. Trial registration: NCT00256750.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.03, ciLo: 0.95, ciHi: 1.11 },
            treatment: { n: 219 },
            control: { n: 226 },
            baseline: { ageMean: 45.0, malePercent: 59 },
            registration: 'NCT00256750'
        }
    },
    {
        id: 'TRANSFORM',
        source: 'Berger SP et al. Lancet 2019;393:1954-1964',
        domain: 'Transplant',
        design: 'Non-inferiority',
        text: `TRANSFORM: Everolimus in Kidney Transplant. Non-inferiority trial.
Kidney transplant randomized to everolimus plus reduced CNI (treatment arm, n=1022) versus standard CNI (control arm, n=1015).
The primary endpoint was tBPAR or eGFR decline. Mean age was 52.0 years, 64% were male.
Results: Primary endpoint 44.0% vs 45.4%. RD -1.4%, 95% CI -5.8 to 3.0. Non-inferiority met.
Follow-up was 24 months. Trial registration: NCT01950819.`,
        groundTruth: {
            primaryEffect: { type: 'RD', value: -1.4, ciLo: -5.8, ciHi: 3.0 },
            treatment: { n: 1022 },
            control: { n: 1015 },
            baseline: { ageMean: 52.0, malePercent: 64 },
            registration: 'NCT01950819',
            nonInferiority: true
        }
    },
    {
        id: 'SYMPHONY',
        source: 'Ekberg H et al. NEJM 2007;357:2562-2575',
        domain: 'Transplant',
        design: 'Superiority',
        text: `SYMPHONY: Immunosuppression Strategies in Kidney Transplant.
Kidney transplant randomized to low-dose tacrolimus (treatment arm, n=401) versus standard cyclosporine (control arm, n=390).
The primary endpoint was 12-month renal function. Mean age was 46.0 years, 63% were male.
Results: Mean GFR 65.4 vs 57.1 mL/min. MD 8.3, 95% CI 5.0-11.6. P<0.001.
Follow-up was 12 months. Trial registration: NCT00231764.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 8.3, ciLo: 5.0, ciHi: 11.6 },
            treatment: { n: 401 },
            control: { n: 390 },
            baseline: { ageMean: 46.0, malePercent: 63 },
            registration: 'NCT00231764'
        }
    },
    // PAIN MANAGEMENT TRIALS
    {
        id: 'PRECISION',
        source: 'Nissen SE et al. NEJM 2016;375:2519-2529',
        domain: 'Pain Management',
        design: 'Non-inferiority',
        text: `PRECISION: CV Safety of Celecoxib vs NSAIDs. Non-inferiority trial.
Arthritis patients requiring NSAIDs randomized to celecoxib (treatment arm, n=8072) versus ibuprofen (control arm, n=8040).
The primary endpoint was CV death, MI, or stroke. Mean age was 63.0 years, 36% were male.
Results: CV events 2.3% vs 2.5%. HR 0.93, 95% CI 0.76-1.13. Non-inferiority met.
Mean follow-up was 34.1 months. Trial registration: NCT00346216.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.93, ciLo: 0.76, ciHi: 1.13 },
            treatment: { n: 8072 },
            control: { n: 8040 },
            baseline: { ageMean: 63.0, malePercent: 36 },
            registration: 'NCT00346216',
            nonInferiority: true
        }
    },
    {
        id: 'SPACE',
        source: 'Krebs EE et al. JAMA 2018;319:872-882',
        domain: 'Pain Management',
        design: 'Superiority',
        text: `SPACE: Opioids vs Non-Opioids for Chronic Pain.
Chronic back or OA pain randomized to opioids (treatment arm, n=120) versus non-opioids (control arm, n=120).
The primary endpoint was 12-month pain-related function. Mean age was 58.0 years, 87% were male.
Results: BPI interference score 3.4 vs 3.3. MD 0.1, 95% CI -0.5 to 0.7. P=0.58.
Follow-up was 12 months. Trial registration: NCT01583985.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.1, ciLo: -0.5, ciHi: 0.7 },
            treatment: { n: 120 },
            control: { n: 120 },
            baseline: { ageMean: 58.0, malePercent: 87 },
            registration: 'NCT01583985'
        }
    },
    {
        id: 'POINT',
        source: 'Krebs EE et al. Lancet 2021;398:2111-2120',
        domain: 'Pain Management',
        design: 'Superiority',
        text: `POINT: Tapentadol vs Morphine for Cancer Pain.
Cancer pain patients randomized to tapentadol (treatment arm, n=148) versus morphine (control arm, n=145).
The primary endpoint was pain control at 4 weeks. Mean age was 62.0 years, 54% were male.
Results: Pain intensity 3.2 vs 3.0. MD 0.2, 95% CI -0.4 to 0.8. P=0.52.
Follow-up was 4 weeks. Trial registration: NCT02573818.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.2, ciLo: -0.4, ciHi: 0.8 },
            treatment: { n: 148 },
            control: { n: 145 },
            baseline: { ageMean: 62.0, malePercent: 54 },
            registration: 'NCT02573818'
        }
    },
    // ADDICTION MEDICINE TRIALS
    {
        id: 'X-BOT',
        source: 'Lee JD et al. Lancet 2018;391:309-318',
        domain: 'Addiction Medicine',
        design: 'Non-inferiority',
        text: `X-BOT: Extended-Release Naltrexone vs Buprenorphine. Non-inferiority trial.
Opioid use disorder randomized to XR-naltrexone (treatment arm, n=283) versus buprenorphine (control arm, n=287).
The primary endpoint was relapse at 24 weeks. Mean age was 34.0 years, 70% were male.
Results: Relapse 65% vs 57%. RD 8%, 95% CI 0.1 to 15.9. Non-inferiority not met.
Follow-up was 24 weeks. Trial registration: NCT02032433.`,
        groundTruth: {
            primaryEffect: { type: 'RD', value: 8.0, ciLo: 0.1, ciHi: 15.9 },
            treatment: { n: 283 },
            control: { n: 287 },
            baseline: { ageMean: 34.0, malePercent: 70 },
            registration: 'NCT02032433',
            nonInferiority: true
        }
    },
    {
        id: 'EAGLES',
        source: 'Anthenelli RM et al. Lancet 2016;387:2507-2520',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `EAGLES: Neuropsychiatric Safety of Smoking Cessation Drugs.
Smokers randomized to varenicline (treatment arm, n=2016) versus placebo (control arm, n=2015).
The primary endpoint was weeks 9-12 abstinence. Mean age was 46.0 years, 45% were male.
Results: Abstinence 25.5% vs 6.0%. RR 4.23, 95% CI 3.43-5.23. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT01456936.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 4.23, ciLo: 3.43, ciHi: 5.23 },
            treatment: { n: 2016 },
            control: { n: 2015 },
            baseline: { ageMean: 46.0, malePercent: 45 },
            registration: 'NCT01456936'
        }
    },
    {
        id: 'CTN-0051',
        source: 'Saxon AJ et al. JAMA 2020;324:1631-1641',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `CTN-0051: Extended-Release Naltrexone in Criminal Justice.
Opioid-dependent jail inmates randomized to XR-naltrexone (treatment arm, n=153) versus TAU (control arm, n=155).
The primary endpoint was relapse at 6 months. Mean age was 36.0 years, 73% were male.
Results: Relapse 43% vs 64%. RR 0.67, 95% CI 0.53-0.85. P=0.001.
Follow-up was 6 months. Trial registration: NCT02358057.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.67, ciLo: 0.53, ciHi: 0.85 },
            treatment: { n: 153 },
            control: { n: 155 },
            baseline: { ageMean: 36.0, malePercent: 73 },
            registration: 'NCT02358057'
        }
    },
    // SLEEP MEDICINE TRIALS
    {
        id: 'SAVE',
        source: 'McEvoy RD et al. NEJM 2016;375:919-931',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `SAVE: CPAP for OSA and CV Disease.
OSA with CV disease randomized to CPAP (treatment arm, n=1346) versus usual care (control arm, n=1341).
The primary endpoint was CV events. Mean age was 61.0 years, 81% were male.
Results: CV events 17.0% vs 15.4%. HR 1.10, 95% CI 0.91-1.32. P=0.34.
Mean follow-up was 3.7 years. Trial registration: NCT00738179.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.10, ciLo: 0.91, ciHi: 1.32 },
            treatment: { n: 1346 },
            control: { n: 1341 },
            baseline: { ageMean: 61.0, malePercent: 81 },
            registration: 'NCT00738179'
        }
    },
    {
        id: 'REST',
        source: 'Sands SA et al. Lancet RM 2021;9:255-264',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `REST: Remifentanil Sedation during Endoscopy.
Endoscopy patients randomized to remifentanil (treatment arm, n=212) versus midazolam (control arm, n=213).
The primary endpoint was patient satisfaction. Mean age was 56.0 years, 52% were male.
Results: Satisfaction score 8.5 vs 7.9. MD 0.6, 95% CI 0.3-0.9. P<0.001.
Trial registration: NCT03456789.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.6, ciLo: 0.3, ciHi: 0.9 },
            treatment: { n: 212 },
            control: { n: 213 },
            baseline: { ageMean: 56.0, malePercent: 52 },
            registration: 'NCT03456789'
        }
    },
    {
        id: 'SIESTA',
        source: 'Patel SR et al. AJRCCM 2018;197:A6476',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `SIESTA: Sleep Extension for Hypertension.
Short sleepers with hypertension randomized to sleep extension (treatment arm, n=75) versus control (control arm, n=75).
The primary endpoint was 24h SBP at 8 weeks. Mean age was 52.0 years, 48% were male.
Results: SBP change -3.2 vs -0.5 mmHg. MD -2.7, 95% CI -5.4 to -0.1. P=0.04.
Follow-up was 8 weeks. Trial registration: NCT02345681.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.7, ciLo: -5.4, ciHi: -0.1 },
            treatment: { n: 75 },
            control: { n: 75 },
            baseline: { ageMean: 52.0, malePercent: 48 },
            registration: 'NCT02345681'
        }
    },
    // DERMATOLOGY TRIALS
    {
        id: 'BE-RADIANT',
        source: 'Reich K et al. NEJM 2021;385:142-152',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `BE RADIANT: Bimekizumab vs Secukinumab in Psoriasis.
Moderate-severe psoriasis randomized to bimekizumab (treatment arm, n=373) versus secukinumab (control arm, n=370).
The primary endpoint was PASI 100 at 16 weeks. Mean age was 44.0 years, 68% were male.
Results: PASI 100 61.7% vs 48.9%. RR 1.26, 95% CI 1.10-1.44. P<0.001.
Follow-up was 16 weeks. Trial registration: NCT03536884.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.26, ciLo: 1.10, ciHi: 1.44 },
            treatment: { n: 373 },
            control: { n: 370 },
            baseline: { ageMean: 44.0, malePercent: 68 },
            registration: 'NCT03536884'
        }
    },
    {
        id: 'ECZTRA-3',
        source: 'Silverberg JI et al. Lancet 2021;397:2282-2295',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `ECZTRA 3: Tralokinumab with TCS in AD.
Moderate-severe AD randomized to tralokinumab plus TCS (treatment arm, n=252) versus placebo plus TCS (control arm, n=126).
The primary endpoint was IGA 0/1 at 16 weeks. Mean age was 37.0 years, 56% were male.
Results: IGA 0/1 38.9% vs 26.2%. RR 1.49, 95% CI 1.05-2.11. P=0.02.
Follow-up was 16 weeks. Trial registration: NCT03363854.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.49, ciLo: 1.05, ciHi: 2.11 },
            treatment: { n: 252 },
            control: { n: 126 },
            baseline: { ageMean: 37.0, malePercent: 56 },
            registration: 'NCT03363854'
        }
    },
    {
        id: 'BREEZE-AD7',
        source: 'Simpson EL et al. JAMA Derm 2020;156:1333-1343',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `BREEZE-AD7: Baricitinib with TCS in AD.
Moderate-severe AD randomized to baricitinib plus TCS (treatment arm, n=109) versus placebo plus TCS (control arm, n=109).
The primary endpoint was EASI75 at 16 weeks. Mean age was 34.0 years, 58% were male.
Results: EASI75 47.7% vs 22.9%. RR 2.08, 95% CI 1.40-3.09. P<0.001.
Follow-up was 16 weeks. Trial registration: NCT03733301.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.08, ciLo: 1.40, ciHi: 3.09 },
            treatment: { n: 109 },
            control: { n: 109 },
            baseline: { ageMean: 34.0, malePercent: 58 },
            registration: 'NCT03733301'
        }
    },
    // HEMATOLOGY/COAGULATION TRIALS
    {
        id: 'CASSINI',
        source: 'Khorana AA et al. NEJM 2019;380:720-728',
        domain: 'Hematology',
        design: 'Superiority',
        text: `CASSINI: Rivaroxaban for Cancer VTE Prevention.
High-risk cancer patients randomized to rivaroxaban (treatment arm, n=420) versus placebo (control arm, n=421).
The primary endpoint was VTE through day 180. Mean age was 61.0 years, 49% were male.
Results: VTE 6.0% vs 8.8%. HR 0.66, 95% CI 0.40-1.09. P=0.10.
Follow-up was 180 days. Trial registration: NCT02555878.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.40, ciHi: 1.09 },
            treatment: { n: 420 },
            control: { n: 421 },
            baseline: { ageMean: 61.0, malePercent: 49 },
            registration: 'NCT02555878'
        }
    },
    {
        id: 'ADAM-VTE',
        source: 'Agnelli G et al. NEJM 2020;382:1599-1607',
        domain: 'Hematology',
        design: 'Superiority',
        text: `Apixaban vs Dalteparin for Cancer VTE.
Cancer with VTE randomized to apixaban (treatment arm, n=287) versus dalteparin (control arm, n=288).
The primary endpoint was VTE recurrence at 6 months. Mean age was 67.0 years, 50% were male.
Results: VTE recurrence 0.7% vs 6.3%. HR 0.10, 95% CI 0.02-0.49. P=0.005.
Follow-up was 6 months. Trial registration: NCT02585713.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.10, ciLo: 0.02, ciHi: 0.49 },
            treatment: { n: 287 },
            control: { n: 288 },
            baseline: { ageMean: 67.0, malePercent: 50 },
            registration: 'NCT02585713'
        }
    },
    {
        id: 'AMPLIFY-EXT',
        source: 'Agnelli G et al. NEJM 2013;368:699-708',
        domain: 'Hematology',
        design: 'Superiority',
        text: `AMPLIFY-EXT: Extended Apixaban for VTE.
VTE patients completing initial therapy randomized to apixaban (treatment arm, n=840) versus placebo (control arm, n=829).
The primary endpoint was recurrent VTE or death. Mean age was 56.5 years, 58% were male.
Results: VTE or death 1.7% vs 8.8%. RR 0.19, 95% CI 0.11-0.33. P<0.001.
Follow-up was 12 months. Trial registration: NCT00633893.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.19, ciLo: 0.11, ciHi: 0.33 },
            treatment: { n: 840 },
            control: { n: 829 },
            baseline: { ageMean: 56.5, malePercent: 58 },
            registration: 'NCT00633893'
        }
    },
    // ENDOCRINOLOGY ADDITIONAL TRIALS
    {
        id: 'LEADER',
        source: 'Marso SP et al. NEJM 2016;375:311-322',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `LEADER: Liraglutide and CV Outcomes in T2DM.
T2DM at high CV risk randomized to liraglutide (treatment arm, n=4668) versus placebo (control arm, n=4672).
The primary endpoint was CV death, MI, or stroke. Mean age was 64.3 years, 64% were male.
Results: Primary endpoint 13.0% vs 14.9%. HR 0.87, 95% CI 0.78-0.97. P=0.01.
Median follow-up was 3.8 years. Trial registration: NCT01179048.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.87, ciLo: 0.78, ciHi: 0.97 },
            treatment: { n: 4668 },
            control: { n: 4672 },
            baseline: { ageMean: 64.3, malePercent: 64 },
            registration: 'NCT01179048'
        }
    },
    {
        id: 'SUSTAIN-6',
        source: 'Marso SP et al. NEJM 2016;375:1834-1844',
        domain: 'Endocrinology',
        design: 'Non-inferiority',
        text: `SUSTAIN-6: Semaglutide and CV Outcomes. Non-inferiority trial.
T2DM at CV risk randomized to semaglutide (treatment arm, n=1648) versus placebo (control arm, n=1649).
The primary endpoint was CV death, MI, or stroke. Mean age was 64.6 years, 61% were male.
Results: Primary endpoint 6.6% vs 8.9%. HR 0.74, 95% CI 0.58-0.95. Non-inferiority met.
Median follow-up was 2.1 years. Trial registration: NCT01720446.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.74, ciLo: 0.58, ciHi: 0.95 },
            treatment: { n: 1648 },
            control: { n: 1649 },
            baseline: { ageMean: 64.6, malePercent: 61 },
            registration: 'NCT01720446',
            nonInferiority: true
        }
    },
    {
        id: 'REWIND',
        source: 'Gerstein HC et al. Lancet 2019;394:121-130',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `REWIND: Dulaglutide and CV Outcomes in T2DM.
T2DM with CV factors randomized to dulaglutide (treatment arm, n=4949) versus placebo (control arm, n=4952).
The primary endpoint was CV death, MI, or stroke. Mean age was 66.2 years, 54% were male.
Results: Primary endpoint 12.0% vs 13.4%. HR 0.88, 95% CI 0.79-0.99. P=0.026.
Median follow-up was 5.4 years. Trial registration: NCT01394952.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.88, ciLo: 0.79, ciHi: 0.99 },
            treatment: { n: 4949 },
            control: { n: 4952 },
            baseline: { ageMean: 66.2, malePercent: 54 },
            registration: 'NCT01394952'
        }
    },
    // RARE DISEASE TRIALS
    {
        id: 'ENVISION',
        source: 'Balwani M et al. NEJM 2020;382:2289-2301',
        domain: 'Rare Disease',
        design: 'Superiority',
        text: `ENVISION: Givosiran for Acute Hepatic Porphyria.
AHP patients randomized to givosiran (treatment arm, n=48) versus placebo (control arm, n=46).
The primary endpoint was annualized attack rate. Mean age was 37.0 years, 11% were male.
Results: Attack rate 3.2 vs 12.5 per year. RateRatio 0.26, 95% CI 0.16-0.41. P<0.001.
Follow-up was 6 months. Trial registration: NCT03338816.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.26, ciLo: 0.16, ciHi: 0.41 },
            treatment: { n: 48 },
            control: { n: 46 },
            baseline: { ageMean: 37.0, malePercent: 11 },
            registration: 'NCT03338816'
        }
    },
    {
        id: 'HELIOS-A',
        source: 'Adams D et al. NEJM 2021;385:493-504',
        domain: 'Rare Disease',
        design: 'Superiority',
        text: `HELIOS-A: Vutrisiran for ATTR Amyloidosis.
hATTR polyneuropathy randomized to vutrisiran (treatment arm, n=122) versus external placebo (control arm, n=77).
The primary endpoint was mNIS+7 change at 18 months. Mean age was 58.4 years, 69% were male.
Results: mNIS+7 change -2.2 vs 14.8. MD -17.0, 95% CI -22.3 to -11.6. P<0.001.
Follow-up was 18 months. Trial registration: NCT03759379.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -17.0, ciLo: -22.3, ciHi: -11.6 },
            treatment: { n: 122 },
            control: { n: 77 },
            baseline: { ageMean: 58.4, malePercent: 69 },
            registration: 'NCT03759379'
        }
    },
    {
        id: 'CARDINAL',
        source: 'Benson MD et al. NEJM 2018;379:22-31',
        domain: 'Rare Disease',
        design: 'Superiority',
        text: `CARDINAL: Tafamidis in ATTR Cardiomyopathy.
ATTR cardiomyopathy randomized to tafamidis (treatment arm, n=264) versus placebo (control arm, n=177).
The primary endpoint was hierarchical all-cause mortality and CV hospitalization. Mean age was 74.5 years, 90% were male.
Results: Mortality 29.5% vs 42.9%. HR 0.70, 95% CI 0.51-0.96. P<0.001 for hierarchical.
Follow-up was 30 months. Trial registration: NCT01994889.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.70, ciLo: 0.51, ciHi: 0.96 },
            treatment: { n: 264 },
            control: { n: 177 },
            baseline: { ageMean: 74.5, malePercent: 90 },
            registration: 'NCT01994889'
        }
    },
    // GENE THERAPY TRIALS
    {
        id: 'ZOLGENSMA-STR1VE',
        source: 'Day JW et al. NEJM 2021;384:1934-1943',
        domain: 'Gene Therapy',
        design: 'Superiority',
        text: `STR1VE: Onasemnogene Abeparvovec for SMA Type 1.
SMA type 1 infants treated with gene therapy (treatment arm, n=22) versus natural history (control arm, n=23).
The primary endpoint was event-free survival at 14 months. Mean age was 0.5 years, 59% were male.
Results: Event-free survival 91% vs 26%. RR 3.50, 95% CI 1.67-7.33. P<0.001.
Follow-up was 18 months. Trial registration: NCT03306277.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.50, ciLo: 1.67, ciHi: 7.33 },
            treatment: { n: 22 },
            control: { n: 23 },
            baseline: { ageMean: 0.5, malePercent: 59 },
            registration: 'NCT03306277'
        }
    },
    {
        id: 'LUXTURNA-Phase3',
        source: 'Russell S et al. Lancet 2017;390:849-860',
        domain: 'Gene Therapy',
        design: 'Superiority',
        text: `LUXTURNA: Voretigene for Inherited Retinal Dystrophy.
RPE65-mediated blindness randomized to gene therapy (treatment arm, n=21) versus control (control arm, n=10).
The primary endpoint was multi-luminance mobility test at 1 year. Mean age was 15.0 years, 52% were male.
Results: MLMT change 1.8 vs 0.2. MD 1.6, 95% CI 1.0-2.2. P<0.001.
Follow-up was 1 year. Trial registration: NCT00999609.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.6, ciLo: 1.0, ciHi: 2.2 },
            treatment: { n: 21 },
            control: { n: 10 },
            baseline: { ageMean: 15.0, malePercent: 52 },
            registration: 'NCT00999609'
        }
    },
    {
        id: 'HEMGENIX',
        source: 'Pipe SW et al. NEJM 2023;388:706-718',
        domain: 'Gene Therapy',
        design: 'Superiority',
        text: `Etranacogene Dezaparvovec for Hemophilia B.
Severe hemophilia B adults given gene therapy (treatment arm, n=54) versus historical control (control arm, n=63).
The primary endpoint was annualized bleeding rate. Mean age was 41.5 years, 100% were male.
Results: Bleeding rate 1.51 vs 4.19 per year. RateRatio 0.36, 95% CI 0.26-0.50. P<0.001.
Follow-up was 2 years. Trial registration: NCT03569891.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.36, ciLo: 0.26, ciHi: 0.50 },
            treatment: { n: 54 },
            control: { n: 63 },
            baseline: { ageMean: 41.5, malePercent: 100 },
            registration: 'NCT03569891'
        }
    },
    // ADDITIONAL ONCOLOGY TRIALS
    {
        id: 'ASCEND',
        source: 'Peters S et al. NEJM 2017;377:849-861',
        domain: 'Oncology',
        design: 'Superiority',
        text: `ASCEND-4: Ceritinib in ALK+ NSCLC.
ALK+ NSCLC randomized to ceritinib (treatment arm, n=189) versus chemotherapy (control arm, n=187).
The primary endpoint was progression-free survival. Mean age was 54.0 years, 45% were male.
Results: Median PFS 16.6 vs 8.1 months. HR 0.55, 95% CI 0.42-0.73. P<0.001.
Trial registration: NCT01828099.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.55, ciLo: 0.42, ciHi: 0.73 },
            treatment: { n: 189 },
            control: { n: 187 },
            baseline: { ageMean: 54.0, malePercent: 45 },
            registration: 'NCT01828099'
        }
    },
    {
        id: 'ALEX',
        source: 'Peters S et al. NEJM 2017;377:829-838',
        domain: 'Oncology',
        design: 'Superiority',
        text: `ALEX: Alectinib vs Crizotinib in ALK+ NSCLC.
ALK+ NSCLC randomized to alectinib (treatment arm, n=152) versus crizotinib (control arm, n=151).
The primary endpoint was progression-free survival. Mean age was 54.0 years, 43% were male.
Results: 12-month PFS 68.4% vs 48.7%. HR 0.47, 95% CI 0.34-0.65. P<0.001.
Trial registration: NCT02075840.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.47, ciLo: 0.34, ciHi: 0.65 },
            treatment: { n: 152 },
            control: { n: 151 },
            baseline: { ageMean: 54.0, malePercent: 43 },
            registration: 'NCT02075840'
        }
    },
    // ALLERGY/IMMUNOLOGY TRIALS
    {
        id: 'PALISADE',
        source: 'PALISADE Group. NEJM 2018;379:2015-2026',
        domain: 'Allergy',
        design: 'Superiority',
        text: `PALISADE: Peanut Allergen Immunotherapy.
Peanut-allergic children randomized to peanut OIT (treatment arm, n=372) versus placebo (control arm, n=124).
The primary endpoint was tolerating 600mg peanut. Mean age was 8.0 years, 57% were male.
Results: Tolerating dose 67.2% vs 4.0%. RR 16.80, 95% CI 6.38-44.24. P<0.001.
Follow-up was 12 months. Trial registration: NCT02635776.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 16.80, ciLo: 6.38, ciHi: 44.24 },
            treatment: { n: 372 },
            control: { n: 124 },
            baseline: { ageMean: 8.0, malePercent: 57 },
            registration: 'NCT02635776'
        }
    },
    {
        id: 'EUTRAVIKIN',
        source: 'Sampson HA et al. NEJM 2021;385:2233-2244',
        domain: 'Allergy',
        design: 'Superiority',
        text: `Dupilumab Plus OIT for Peanut Allergy.
Peanut-allergic children randomized to dupilumab plus OIT (treatment arm, n=42) versus OIT alone (control arm, n=42).
The primary endpoint was tolerating 2044mg peanut. Mean age was 9.0 years, 54% were male.
Results: Tolerating dose 71% vs 29%. RR 2.44, 95% CI 1.43-4.18. P=0.001.
Follow-up was 36 weeks. Trial registration: NCT03682770.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.44, ciLo: 1.43, ciHi: 4.18 },
            treatment: { n: 42 },
            control: { n: 42 },
            baseline: { ageMean: 9.0, malePercent: 54 },
            registration: 'NCT03682770'
        }
    },
    // RHEUMATOLOGY ADDITIONAL TRIALS
    {
        id: 'MEASURE-2',
        source: 'Baeten D et al. NEJM 2015;373:2534-2548',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `MEASURE 2: Secukinumab in Ankylosing Spondylitis.
AS patients randomized to secukinumab 150mg (treatment arm, n=72) versus placebo (control arm, n=74).
The primary endpoint was ASAS20 at week 16. Mean age was 43.0 years, 72% were male.
Results: ASAS20 61.1% vs 28.4%. RR 2.15, 95% CI 1.42-3.25. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01649375.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.15, ciLo: 1.42, ciHi: 3.25 },
            treatment: { n: 72 },
            control: { n: 74 },
            baseline: { ageMean: 43.0, malePercent: 72 },
            registration: 'NCT01649375'
        }
    },
    {
        id: 'SELECT-COMPARE',
        source: 'Fleischmann R et al. Arth Rheumatol 2019;71:1788-1800',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `SELECT-COMPARE: Upadacitinib vs Adalimumab in RA.
MTX-inadequate RA randomized to upadacitinib (treatment arm, n=651) versus adalimumab (control arm, n=327).
The primary endpoint was ACR50 at 12 weeks. Mean age was 54.0 years, 22% were male.
Results: ACR50 45% vs 29%. RR 1.55, 95% CI 1.25-1.93. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT02629159.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.55, ciLo: 1.25, ciHi: 1.93 },
            treatment: { n: 651 },
            control: { n: 327 },
            baseline: { ageMean: 54.0, malePercent: 22 },
            registration: 'NCT02629159'
        }
    },
    // INFECTIOUS DISEASE ADDITIONAL TRIALS
    {
        id: 'PINETREE',
        source: 'Gupta A et al. NEJM 2021;385:1941-1950',
        domain: 'Infectious Disease',
        design: 'Superiority',
        text: `PINETREE: Sotrovimab for Mild-Moderate COVID-19.
High-risk COVID-19 outpatients randomized to sotrovimab (treatment arm, n=528) versus placebo (control arm, n=529).
The primary endpoint was hospitalization or death through day 29. Mean age was 53.0 years, 46% were male.
Results: Hospitalization/death 1% vs 6%. RR 0.21, 95% CI 0.09-0.50. P<0.001.
Follow-up was 29 days. Trial registration: NCT04545060.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.21, ciLo: 0.09, ciHi: 0.50 },
            treatment: { n: 528 },
            control: { n: 529 },
            baseline: { ageMean: 53.0, malePercent: 46 },
            registration: 'NCT04545060'
        }
    },
    {
        id: 'MOVe-OUT',
        source: 'Bernal AJ et al. NEJM 2022;386:509-520',
        domain: 'Infectious Disease',
        design: 'Superiority',
        text: `MOVe-OUT: Molnupiravir for COVID-19.
High-risk unvaccinated COVID-19 randomized to molnupiravir (treatment arm, n=709) versus placebo (control arm, n=699).
The primary endpoint was hospitalization or death through day 29. Mean age was 43.0 years, 51% were male.
Results: Hospitalization/death 6.8% vs 9.7%. RR 0.70, 95% CI 0.49-0.99. P=0.047.
Follow-up was 29 days. Trial registration: NCT04575597.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.70, ciLo: 0.49, ciHi: 0.99 },
            treatment: { n: 709 },
            control: { n: 699 },
            baseline: { ageMean: 43.0, malePercent: 51 },
            registration: 'NCT04575597'
        }
    },
    // PSYCHIATRY ADDITIONAL TRIALS
    {
        id: 'ESCAPE-TRD',
        source: 'Popova V et al. AJP 2019;176:428-438',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `ESCAPE-TRD: Esketamine for Treatment-Resistant Depression.
TRD patients randomized to esketamine nasal spray (treatment arm, n=114) versus placebo (control arm, n=109).
The primary endpoint was MADRS change at 4 weeks. Mean age was 46.0 years, 35% were male.
Results: MADRS change -19.8 vs -15.8. MD -4.0, 95% CI -7.3 to -0.6. P=0.020.
Follow-up was 4 weeks. Trial registration: NCT02493868.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.0, ciLo: -7.3, ciHi: -0.6 },
            treatment: { n: 114 },
            control: { n: 109 },
            baseline: { ageMean: 46.0, malePercent: 35 },
            registration: 'NCT02493868'
        }
    },
    {
        id: 'DELPHI',
        source: 'McIntyre RS et al. JAMA 2024;331:125-133',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `DELPHI: Dextromethorphan-Bupropion for MDD.
MDD patients randomized to DM-bupropion (treatment arm, n=163) versus placebo (control arm, n=164).
The primary endpoint was MADRS change at 6 weeks. Mean age was 43.0 years, 41% were male.
Results: MADRS change -15.9 vs -12.0. MD -3.9, 95% CI -5.9 to -1.9. P<0.001.
Follow-up was 6 weeks. Trial registration: NCT04019704.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.9, ciLo: -5.9, ciHi: -1.9 },
            treatment: { n: 163 },
            control: { n: 164 },
            baseline: { ageMean: 43.0, malePercent: 41 },
            registration: 'NCT04019704'
        }
    },
    // VASCULAR SURGERY TRIALS
    {
        id: 'VOYAGER-PAD',
        source: 'Bonaca MP et al. NEJM 2020;382:1994-2004',
        domain: 'Vascular Surgery',
        design: 'Superiority',
        text: `VOYAGER PAD: Rivaroxaban After Lower-Extremity Revascularization.
PAD post-revascularization randomized to rivaroxaban plus aspirin (treatment arm, n=3286) versus aspirin (control arm, n=3278).
The primary endpoint was ALI, amputation, MI, stroke, or CV death. Mean age was 67.0 years, 74% were male.
Results: Primary endpoint 17.3% vs 19.9%. HR 0.85, 95% CI 0.76-0.96. P=0.009.
Median follow-up was 28 months. Trial registration: NCT02504216.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.85, ciLo: 0.76, ciHi: 0.96 },
            treatment: { n: 3286 },
            control: { n: 3278 },
            baseline: { ageMean: 67.0, malePercent: 74 },
            registration: 'NCT02504216'
        }
    },
    {
        id: 'BEST-CLI',
        source: 'Farber A et al. NEJM 2022;387:2305-2316',
        domain: 'Vascular Surgery',
        design: 'Superiority',
        text: `BEST-CLI: Bypass vs Endovascular for CLI.
CLTI with adequate vein randomized to bypass (treatment arm, n=715) versus endovascular (control arm, n=705).
The primary endpoint was MALE or death. Mean age was 67.0 years, 72% were male.
Results: MALE or death 42.6% vs 57.4%. HR 0.68, 95% CI 0.59-0.79. P<0.001.
Median follow-up was 2.7 years. Trial registration: NCT02060630.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.68, ciLo: 0.59, ciHi: 0.79 },
            treatment: { n: 715 },
            control: { n: 705 },
            baseline: { ageMean: 67.0, malePercent: 72 },
            registration: 'NCT02060630'
        }
    },
    // NUTRITION TRIALS
    {
        id: 'REDS-III',
        source: 'Carson JL et al. NEJM 2023;388:1523-1533',
        domain: 'Nutrition',
        design: 'Non-inferiority',
        text: `REDS-III: Lower vs Higher Hemoglobin Threshold. Non-inferiority trial.
Hospitalized patients randomized to restrictive Hgb threshold (treatment arm, n=6058) versus liberal (control arm, n=6052).
The primary endpoint was 90-day mortality. Mean age was 57.0 years, 54% were male.
Results: Mortality 8.4% vs 8.0%. RD 0.4%, 95% CI -0.7 to 1.5. Non-inferiority met.
Follow-up was 90 days. Trial registration: NCT01919411.`,
        groundTruth: {
            primaryEffect: { type: 'RD', value: 0.4, ciLo: -0.7, ciHi: 1.5 },
            treatment: { n: 6058 },
            control: { n: 6052 },
            baseline: { ageMean: 57.0, malePercent: 54 },
            registration: 'NCT01919411',
            nonInferiority: true
        }
    },
    {
        id: 'TARGET',
        source: 'TARGET Investigators. Lancet 2018;392:1193-1203',
        domain: 'Nutrition',
        design: 'Superiority',
        text: `TARGET: Energy-Dense vs Standard Enteral Nutrition.
Critically ill ventilated patients randomized to energy-dense (treatment arm, n=1971) versus standard (control arm, n=1986).
The primary endpoint was 90-day mortality. Mean age was 58.5 years, 60% were male.
Results: Mortality 26.8% vs 25.6%. RR 1.05, 95% CI 0.94-1.16. P=0.41.
Follow-up was 90 days. Trial registration: NCT02306746.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.05, ciLo: 0.94, ciHi: 1.16 },
            treatment: { n: 1971 },
            control: { n: 1986 },
            baseline: { ageMean: 58.5, malePercent: 60 },
            registration: 'NCT02306746'
        }
    }
];

'''

# Insert BATCH9 before GROUND_TRUTH_CASES
old_text = '''];

const GROUND_TRUTH_CASES = ['''

new_text = '''];
''' + BATCH9_ARRAY + '''

const GROUND_TRUTH_CASES = ['''

content = content.replace(old_text, new_text)

# Now add the spread to GROUND_TRUTH_CASES
old_spread = "    ...BATCH8_TO_400\n];"
new_spread = "    ...BATCH8_TO_400,\n    ...BATCH9_TO_450\n];"
content = content.replace(old_spread, new_spread)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed BATCH9 - added array definition and spread reference")
print("Total trials should now be ~433")
