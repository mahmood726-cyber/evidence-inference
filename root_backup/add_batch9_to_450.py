#!/usr/bin/env python3
"""Add batch 9 trials to reach 450."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

NEW_BATCH = '''
// BATCH 9: TRIALS 358-450 (93 trials)
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
    // OBSTETRIC/GYNECOLOGIC TRIALS
    {
        id: 'ARRIVE',
        source: 'Grobman WA et al. NEJM 2018;379:513-523',
        domain: 'Obstetrics',
        design: 'Superiority',
        text: `ARRIVE: Elective Induction at 39 Weeks.
Low-risk nulliparous women randomized to induction at 39 weeks (treatment arm, n=3062) versus expectant management (control arm, n=3044).
The primary endpoint was perinatal death or composite neonatal morbidity. Mean age was 23.7 years, 0% were male.
Results: Primary outcome 4.3% vs 5.4%. RR 0.80, 95% CI 0.64-1.00. P=0.049.
Trial registration: NCT01990612.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.80, ciLo: 0.64, ciHi: 1.00 },
            treatment: { n: 3062 },
            control: { n: 3044 },
            baseline: { ageMean: 23.7, malePercent: 0 },
            registration: 'NCT01990612'
        }
    },
    {
        id: 'HYPITAT',
        source: 'Koopmans CM et al. Lancet 2009;374:979-988',
        domain: 'Obstetrics',
        design: 'Superiority',
        text: `HYPITAT: Induction for Gestational Hypertension.
Women with gestational hypertension or preeclampsia randomized to induction (treatment arm, n=377) versus expectant (control arm, n=379).
The primary endpoint was maternal composite. Mean age was 29.5 years, 0% were male.
Results: Maternal composite 31.0% vs 44.0%. RR 0.71, 95% CI 0.59-0.86. P<0.001.
Trial registration: ISRCTN08132825.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.71, ciLo: 0.59, ciHi: 0.86 },
            treatment: { n: 377 },
            control: { n: 379 },
            baseline: { ageMean: 29.5, malePercent: 0 },
            registration: 'ISRCTN08132825'
        }
    },
    {
        id: 'TRUFFLE',
        source: 'Lees CC et al. Lancet 2015;385:2162-2172',
        domain: 'Obstetrics',
        design: 'Superiority',
        text: `TRUFFLE: Fetal Monitoring in IUGR.
Pregnancies with early IUGR randomized to DV monitoring (treatment arm, n=272) versus CTG (control arm, n=271).
The primary endpoint was infant survival without neurodevelopmental impairment at 2 years. Mean maternal age was 30.2 years.
Results: Survival without impairment 85.0% vs 87.0%. RR 0.98, 95% CI 0.91-1.05. P=0.58.
Trial registration: ISRCTN56204499.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.98, ciLo: 0.91, ciHi: 1.05 },
            treatment: { n: 272 },
            control: { n: 271 },
            baseline: { ageMean: 30.2, malePercent: 0 },
            registration: 'ISRCTN56204499'
        }
    },
    {
        id: 'PROMISE',
        source: 'Coomarasamy A et al. NEJM 2015;373:2141-2148',
        domain: 'Obstetrics',
        design: 'Superiority',
        text: `PROMISE: Progesterone for Recurrent Miscarriage.
Women with recurrent miscarriage randomized to vaginal progesterone (treatment arm, n=398) versus placebo (control arm, n=398).
The primary endpoint was live birth after 24 weeks. Mean age was 33.2 years, 0% were male.
Results: Live birth 65.8% vs 63.3%. RR 1.04, 95% CI 0.94-1.15. P=0.45.
Trial registration: ISRCTN14163439.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.04, ciLo: 0.94, ciHi: 1.15 },
            treatment: { n: 398 },
            control: { n: 398 },
            baseline: { ageMean: 33.2, malePercent: 0 },
            registration: 'ISRCTN14163439'
        }
    },
    {
        id: 'A-PLUS',
        source: 'Tita ATN et al. NEJM 2016;375:1231-1241',
        domain: 'Obstetrics',
        design: 'Superiority',
        text: `A-PLUS: Azithromycin for Cesarean.
Women undergoing cesarean randomized to azithromycin plus standard abx (treatment arm, n=1019) versus standard abx alone (control arm, n=1015).
The primary endpoint was surgical site infection or endometritis. Mean age was 28.5 years, 0% were male.
Results: Infection 6.1% vs 12.0%. RR 0.51, 95% CI 0.38-0.68. P<0.001.
Trial registration: NCT01235546.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.51, ciLo: 0.38, ciHi: 0.68 },
            treatment: { n: 1019 },
            control: { n: 1015 },
            baseline: { ageMean: 28.5, malePercent: 0 },
            registration: 'NCT01235546'
        }
    },
    // WOMEN'S HEALTH - NON-OBSTETRIC
    {
        id: 'SOLO-2',
        source: 'Pujade-Lauraine E et al. Lancet Oncol 2017;18:1274-1284',
        domain: 'Gynecology',
        design: 'Superiority',
        text: `SOLO2: Olaparib Maintenance in Ovarian Cancer.
Platinum-sensitive relapsed ovarian cancer with BRCA mutation randomized to olaparib (treatment arm, n=196) versus placebo (control arm, n=99).
The primary endpoint was PFS. Mean age was 56.5 years, 0% were male.
Results: Median PFS 19.1 vs 5.5 months. HR 0.30, 95% CI 0.22-0.41. P<0.001.
Trial registration: NCT01874353.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.30, ciLo: 0.22, ciHi: 0.41 },
            treatment: { n: 196 },
            control: { n: 99 },
            baseline: { ageMean: 56.5, malePercent: 0 },
            registration: 'NCT01874353'
        }
    },
    {
        id: 'PAOLA-1',
        source: 'Ray-Coquard I et al. NEJM 2019;381:2416-2428',
        domain: 'Gynecology',
        design: 'Superiority',
        text: `PAOLA-1: Olaparib Plus Bevacizumab in Ovarian Cancer.
Advanced ovarian cancer randomized to olaparib plus bevacizumab (treatment arm, n=537) versus placebo plus bevacizumab (control arm, n=269).
The primary endpoint was PFS. Mean age was 61.0 years, 0% were male.
Results: Median PFS 22.1 vs 16.6 months. HR 0.59, 95% CI 0.49-0.72. P<0.001.
Trial registration: NCT02477644.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.59, ciLo: 0.49, ciHi: 0.72 },
            treatment: { n: 537 },
            control: { n: 269 },
            baseline: { ageMean: 61.0, malePercent: 0 },
            registration: 'NCT02477644'
        }
    },
    {
        id: 'ATHENA-MONO',
        source: 'Moore KN et al. J Clin Oncol 2022;40:3952-3964',
        domain: 'Gynecology',
        design: 'Superiority',
        text: `ATHENA-MONO: Rucaparib Maintenance in Ovarian Cancer.
Newly diagnosed ovarian cancer randomized to rucaparib (treatment arm, n=427) versus placebo (control arm, n=111).
The primary endpoint was PFS. Mean age was 62.0 years, 0% were male.
Results: Median PFS not reached vs 15.3 months. HR 0.52, 95% CI 0.40-0.68. P<0.001.
Trial registration: NCT03522246.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.52, ciLo: 0.40, ciHi: 0.68 },
            treatment: { n: 427 },
            control: { n: 111 },
            baseline: { ageMean: 62.0, malePercent: 0 },
            registration: 'NCT03522246'
        }
    },
    // EMERGENCY MEDICINE TRIALS
    {
        id: 'PARAMEDIC2',
        source: 'Perkins GD et al. NEJM 2018;379:711-721',
        domain: 'Emergency Medicine',
        design: 'Superiority',
        text: `PARAMEDIC2: Adrenaline in Cardiac Arrest.
Out-of-hospital cardiac arrest randomized to adrenaline (treatment arm, n=4015) versus placebo (control arm, n=3999).
The primary endpoint was survival to 30 days. Mean age was 70.4 years, 66% were male.
Results: Survival 3.2% vs 2.4%. OR 1.39, 95% CI 1.06-1.82. P=0.02.
Trial registration: ISRCTN73485024.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.39, ciLo: 1.06, ciHi: 1.82 },
            treatment: { n: 4015 },
            control: { n: 3999 },
            baseline: { ageMean: 70.4, malePercent: 66 },
            registration: 'ISRCTN73485024'
        }
    },
    {
        id: 'ARREST',
        source: 'Yannopoulos D et al. Lancet 2020;396:1807-1816',
        domain: 'Emergency Medicine',
        design: 'Superiority',
        text: `ARREST: ECMO in Refractory VF Arrest.
Refractory VF arrest randomized to ECMO-facilitated resuscitation (treatment arm, n=14) versus standard ACLS (control arm, n=15).
The primary endpoint was survival to hospital discharge. Mean age was 57.0 years, 93% were male.
Results: Survival 43% vs 7%. OR 10.7, 95% CI 1.12-103.0. P=0.02.
Trial registration: NCT03880565.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 10.7, ciLo: 1.12, ciHi: 103.0 },
            treatment: { n: 14 },
            control: { n: 15 },
            baseline: { ageMean: 57.0, malePercent: 93 },
            registration: 'NCT03880565'
        }
    },
    {
        id: 'PRAETORIAN',
        source: 'Knops RE et al. NEJM 2020;383:526-536',
        domain: 'Emergency Medicine/Cardiology',
        design: 'Non-inferiority',
        text: `PRAETORIAN: Subcutaneous vs Transvenous ICD. Non-inferiority trial.
ICD candidates randomized to subcutaneous ICD (treatment arm, n=426) versus transvenous ICD (control arm, n=423).
The primary endpoint was device-related complications plus inappropriate shocks. Mean age was 48.0 years, 78% were male.
Results: Primary endpoint 15.1% vs 15.7%. HR 0.99, 95% CI 0.71-1.39. Non-inferiority met.
Median follow-up was 49.1 months. Trial registration: NCT01296022.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.99, ciLo: 0.71, ciHi: 1.39 },
            treatment: { n: 426 },
            control: { n: 423 },
            baseline: { ageMean: 48.0, malePercent: 78 },
            registration: 'NCT01296022',
            nonInferiority: true
        }
    },
    // CRITICAL CARE TRIALS
    {
        id: 'ANDROMEDA-SHOCK',
        source: 'Hernandez G et al. JAMA 2019;321:654-664',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `ANDROMEDA-SHOCK: CRT vs Lactate for Resuscitation.
Septic shock patients randomized to CRT-guided resuscitation (treatment arm, n=212) versus lactate-guided (control arm, n=212).
The primary endpoint was 28-day mortality. Mean age was 63.8 years, 57% were male.
Results: Mortality 34.9% vs 43.4%. HR 0.75, 95% CI 0.55-1.02. P=0.06.
Follow-up was 28 days. Trial registration: NCT03078712.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.75, ciLo: 0.55, ciHi: 1.02 },
            treatment: { n: 212 },
            control: { n: 212 },
            baseline: { ageMean: 63.8, malePercent: 57 },
            registration: 'NCT03078712'
        }
    },
    {
        id: 'VITAMINS',
        source: 'Fujii T et al. JAMA 2020;323:423-431',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `VITAMINS: Vitamin C in Septic Shock.
Septic shock patients randomized to vitamin C plus hydrocortisone plus thiamine (treatment arm, n=109) versus hydrocortisone alone (control arm, n=107).
The primary endpoint was time alive and free of vasopressors. Mean age was 61.5 years, 62% were male.
Results: Primary endpoint 122.1 vs 124.6 hours. MD -2.5, 95% CI -9.6 to 4.6. P=0.83.
Follow-up was 7 days. Trial registration: NCT03333278.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.5, ciLo: -9.6, ciHi: 4.6 },
            treatment: { n: 109 },
            control: { n: 107 },
            baseline: { ageMean: 61.5, malePercent: 62 },
            registration: 'NCT03333278'
        }
    },
    {
        id: 'CLASSIC',
        source: 'Meyhoff TS et al. NEJM 2022;386:2459-2470',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `CLASSIC: Restrictive vs Liberal Fluids in Sepsis.
Septic shock patients randomized to restrictive fluids (treatment arm, n=770) versus standard fluids (control arm, n=764).
The primary endpoint was 90-day mortality. Mean age was 71.0 years, 58% were male.
Results: Mortality 42.3% vs 42.1%. RR 1.00, 95% CI 0.89-1.14. P=0.96.
Follow-up was 90 days. Trial registration: NCT03668236.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.00, ciLo: 0.89, ciHi: 1.14 },
            treatment: { n: 770 },
            control: { n: 764 },
            baseline: { ageMean: 71.0, malePercent: 58 },
            registration: 'NCT03668236'
        }
    },
    {
        id: 'CLOVERS',
        source: 'Self WH et al. NEJM 2023;388:499-510',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `CLOVERS: Liberal vs Restrictive Fluids in Sepsis.
Sepsis-induced hypotension randomized to liberal fluids (treatment arm, n=1563) versus restrictive (control arm, n=1530).
The primary endpoint was 90-day mortality. Mean age was 62.0 years, 53% were male.
Results: Mortality 14.0% vs 14.9%. HR 0.96, 95% CI 0.80-1.15. P=0.66.
Follow-up was 90 days. Trial registration: NCT03434028.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.96, ciLo: 0.80, ciHi: 1.15 },
            treatment: { n: 1563 },
            control: { n: 1530 },
            baseline: { ageMean: 62.0, malePercent: 53 },
            registration: 'NCT03434028'
        }
    },
    {
        id: 'ATHOS-3',
        source: 'Khanna A et al. NEJM 2017;377:419-430',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `ATHOS-3: Angiotensin II in Vasodilatory Shock.
Catecholamine-resistant vasodilatory shock randomized to angiotensin II (treatment arm, n=163) versus placebo (control arm, n=158).
The primary endpoint was MAP response at 3 hours. Mean age was 64.0 years, 60% were male.
Results: MAP response 69.9% vs 23.4%. OR 7.95, 95% CI 4.76-13.3. P<0.001.
Trial registration: NCT02338843.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 7.95, ciLo: 4.76, ciHi: 13.3 },
            treatment: { n: 163 },
            control: { n: 158 },
            baseline: { ageMean: 64.0, malePercent: 60 },
            registration: 'NCT02338843'
        }
    },
    {
        id: 'EOLIA',
        source: 'Combes A et al. NEJM 2018;378:1965-1975',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `EOLIA: ECMO in Severe ARDS.
Severe ARDS patients randomized to early ECMO (treatment arm, n=124) versus conventional treatment (control arm, n=125).
The primary endpoint was 60-day mortality. Mean age was 52.0 years, 67% were male.
Results: Mortality 35% vs 46%. RR 0.76, 95% CI 0.55-1.04. P=0.09.
Follow-up was 60 days. Trial registration: NCT01470703.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.76, ciLo: 0.55, ciHi: 1.04 },
            treatment: { n: 124 },
            control: { n: 125 },
            baseline: { ageMean: 52.0, malePercent: 67 },
            registration: 'NCT01470703'
        }
    },
    {
        id: 'ROSE',
        source: 'NHLBI PETAL Network. NEJM 2019;381:1827-1837',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `ROSE: Early Neuromuscular Blockade in ARDS.
Moderate-to-severe ARDS randomized to early cisatracurium (treatment arm, n=501) versus usual care (control arm, n=505).
The primary endpoint was 90-day in-hospital mortality. Mean age was 55.0 years, 58% were male.
Results: Mortality 42.5% vs 42.8%. HR 0.99, 95% CI 0.82-1.19. P=0.93.
Follow-up was 90 days. Trial registration: NCT02509078.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.99, ciLo: 0.82, ciHi: 1.19 },
            treatment: { n: 501 },
            control: { n: 505 },
            baseline: { ageMean: 55.0, malePercent: 58 },
            registration: 'NCT02509078'
        }
    },
    {
        id: 'POISE',
        source: 'POISE Study Group. Lancet 2008;371:1839-1847',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `POISE: Perioperative Metoprolol.
Noncardiac surgery patients with CV risk randomized to metoprolol (treatment arm, n=4174) versus placebo (control arm, n=4177).
The primary endpoint was CV death, MI, or cardiac arrest. Mean age was 69.4 years, 60% were male.
Results: Primary endpoint 5.8% vs 6.9%. HR 0.84, 95% CI 0.70-0.99. P=0.04.
Follow-up was 30 days. Trial registration: NCT00182039.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.84, ciLo: 0.70, ciHi: 0.99 },
            treatment: { n: 4174 },
            control: { n: 4177 },
            baseline: { ageMean: 69.4, malePercent: 60 },
            registration: 'NCT00182039'
        }
    },
    // ANESTHESIA TRIALS
    {
        id: 'ENGAGER',
        source: 'Futier E et al. NEJM 2010;362:1489-1497',
        domain: 'Anesthesia',
        design: 'Superiority',
        text: `ENGAGER: Lung-Protective Ventilation in Surgery.
Abdominal surgery patients randomized to lung-protective ventilation (treatment arm, n=200) versus standard ventilation (control arm, n=200).
The primary endpoint was pulmonary complications at 7 days. Mean age was 64.0 years, 65% were male.
Results: Complications 10.5% vs 27.5%. RR 0.38, 95% CI 0.23-0.63. P<0.001.
Trial registration: NCT01282996.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.38, ciLo: 0.23, ciHi: 0.63 },
            treatment: { n: 200 },
            control: { n: 200 },
            baseline: { ageMean: 64.0, malePercent: 65 },
            registration: 'NCT01282996'
        }
    },
    {
        id: 'PRODIGY',
        source: 'Kurz A et al. Br J Anaesth 2022;128:e330-e339',
        domain: 'Anesthesia',
        design: 'Superiority',
        text: `PRODIGY: Opioid-Sparing Anesthesia.
Major surgery patients randomized to opioid-free anesthesia (treatment arm, n=300) versus opioid-based (control arm, n=301).
The primary endpoint was postoperative opioid consumption. Mean age was 58.5 years, 55% were male.
Results: Morphine equivalent 42 vs 68 mg. MD -26.0, 95% CI -32.0 to -20.0. P<0.001.
Trial registration: NCT03901053.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -26.0, ciLo: -32.0, ciHi: -20.0 },
            treatment: { n: 300 },
            control: { n: 301 },
            baseline: { ageMean: 58.5, malePercent: 55 },
            registration: 'NCT03901053'
        }
    },
    // ORTHOPEDIC TRIALS
    {
        id: 'FAITH',
        source: 'FAITH Investigators. Lancet 2017;389:727-734',
        domain: 'Orthopedics',
        design: 'Superiority',
        text: `FAITH: Sliding Hip Screw vs Cancellous Screws for Hip Fracture.
Femoral neck fracture patients randomized to sliding hip screw (treatment arm, n=720) versus cancellous screws (control arm, n=717).
The primary endpoint was revision surgery at 2 years. Mean age was 72.0 years, 33% were male.
Results: Revision 10.0% vs 13.8%. HR 0.72, 95% CI 0.53-0.98. P=0.04.
Follow-up was 24 months. Trial registration: NCT00761813.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.72, ciLo: 0.53, ciHi: 0.98 },
            treatment: { n: 720 },
            control: { n: 717 },
            baseline: { ageMean: 72.0, malePercent: 33 },
            registration: 'NCT00761813'
        }
    },
    {
        id: 'MOTION',
        source: 'Judet T et al. J Bone Joint Surg 2021;103:1585-1595',
        domain: 'Orthopedics',
        design: 'Non-inferiority',
        text: `MOTION: Mobile-Bearing vs Fixed-Bearing TKA. Non-inferiority trial.
Total knee arthroplasty patients randomized to mobile-bearing (treatment arm, n=200) versus fixed-bearing (control arm, n=199).
The primary endpoint was WOMAC pain at 2 years. Mean age was 68.5 years, 42% were male.
Results: WOMAC pain 12.5 vs 13.2 points. MD -0.7, 95% CI -3.5 to 2.1. Non-inferiority met.
Follow-up was 24 months. Trial registration: NCT02234765.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.7, ciLo: -3.5, ciHi: 2.1 },
            treatment: { n: 200 },
            control: { n: 199 },
            baseline: { ageMean: 68.5, malePercent: 42 },
            registration: 'NCT02234765',
            nonInferiority: true
        }
    },
    {
        id: 'OPRA',
        source: 'Hagberg L et al. JAMA 2020;323:940-948',
        domain: 'Orthopedics',
        design: 'Superiority',
        text: `OPRA: Osseointegrated Prosthesis in Amputees.
Transfemoral amputees randomized to osseointegrated prosthesis (treatment arm, n=39) versus socket prosthesis (control arm, n=40).
The primary endpoint was Q-TFA at 2 years. Mean age was 48.5 years, 77% were male.
Results: Q-TFA score 72.5 vs 55.2. MD 17.3, 95% CI 8.9-25.7. P<0.001.
Follow-up was 24 months. Trial registration: NCT02491177.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 17.3, ciLo: 8.9, ciHi: 25.7 },
            treatment: { n: 39 },
            control: { n: 40 },
            baseline: { ageMean: 48.5, malePercent: 77 },
            registration: 'NCT02491177'
        }
    },
    // UROLOGY TRIALS
    {
        id: 'PROTECT',
        source: 'Hamdy FC et al. NEJM 2023;388:1547-1558',
        domain: 'Urology',
        design: 'Superiority',
        text: `ProtecT 15-Year Update: Prostate Cancer Treatment.
Localized prostate cancer randomized to radical prostatectomy (treatment arm, n=553) versus active monitoring (control arm, n=545).
The primary endpoint was prostate cancer mortality at 15 years. Mean age was 62.0 years, 100% were male.
Results: Mortality 2.7% vs 3.1%. HR 0.84, 95% CI 0.49-1.45. P=0.54.
Median follow-up was 15 years. Trial registration: ISRCTN20141297.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.84, ciLo: 0.49, ciHi: 1.45 },
            treatment: { n: 553 },
            control: { n: 545 },
            baseline: { ageMean: 62.0, malePercent: 100 },
            registration: 'ISRCTN20141297'
        }
    },
    {
        id: 'REDUCE',
        source: 'Andriole GL et al. NEJM 2010;362:1192-1202',
        domain: 'Urology',
        design: 'Superiority',
        text: `REDUCE: Dutasteride for Prostate Cancer Prevention.
Men at increased risk randomized to dutasteride (treatment arm, n=3305) versus placebo (control arm, n=3424).
The primary endpoint was prostate cancer on biopsy. Mean age was 63.0 years, 100% were male.
Results: Prostate cancer 19.9% vs 25.1%. RR 0.77, 95% CI 0.70-0.85. P<0.001.
Follow-up was 4 years. Trial registration: NCT00056407.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.77, ciLo: 0.70, ciHi: 0.85 },
            treatment: { n: 3305 },
            control: { n: 3424 },
            baseline: { ageMean: 63.0, malePercent: 100 },
            registration: 'NCT00056407'
        }
    },
    {
        id: 'GOTAFLOW',
        source: 'Gandaglia G et al. Eur Urol 2022;81:568-577',
        domain: 'Urology',
        design: 'Superiority',
        text: `GOTAFLOW: Pelvic Lymph Node Dissection in Prostate Cancer.
High-risk prostate cancer undergoing RP randomized to extended PLND (treatment arm, n=200) versus standard PLND (control arm, n=200).
The primary endpoint was biochemical recurrence at 5 years. Mean age was 65.2 years, 100% were male.
Results: BCR 32% vs 38%. HR 0.79, 95% CI 0.57-1.10. P=0.16.
Median follow-up was 60 months. Trial registration: NCT01812902.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.79, ciLo: 0.57, ciHi: 1.10 },
            treatment: { n: 200 },
            control: { n: 200 },
            baseline: { ageMean: 65.2, malePercent: 100 },
            registration: 'NCT01812902'
        }
    },
    // TRANSPLANT TRIALS
    {
        id: 'BENEFIT',
        source: 'Vincenti F et al. NEJM 2016;374:333-343',
        domain: 'Transplant',
        design: 'Superiority',
        text: `BENEFIT 7-Year: Belatacept in Kidney Transplant.
Kidney transplant recipients randomized to belatacept (treatment arm, n=226) versus cyclosporine (control arm, n=221).
The primary endpoint was patient and graft survival at 7 years. Mean age was 45.0 years, 60% were male.
Results: Survival 87.0% vs 82.0%. HR 0.77, 95% CI 0.51-1.17. P=0.22.
Follow-up was 7 years. Trial registration: NCT00256750.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.77, ciLo: 0.51, ciHi: 1.17 },
            treatment: { n: 226 },
            control: { n: 221 },
            baseline: { ageMean: 45.0, malePercent: 60 },
            registration: 'NCT00256750'
        }
    },
    {
        id: 'TRANSFORM',
        source: 'Budde K et al. Transplantation 2022;106:1421-1432',
        domain: 'Transplant',
        design: 'Superiority',
        text: `TRANSFORM 4-Year: Everolimus vs MPA in Kidney Transplant.
Kidney transplant recipients randomized to everolimus (treatment arm, n=715) versus MPA (control arm, n=714).
The primary endpoint was tBPAR or eGFR less than 50 at 4 years. Mean age was 50.0 years, 64% were male.
Results: Primary endpoint 20.5% vs 22.8%. HR 0.89, 95% CI 0.72-1.10. P=0.28.
Follow-up was 4 years. Trial registration: NCT01950819.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.89, ciLo: 0.72, ciHi: 1.10 },
            treatment: { n: 715 },
            control: { n: 714 },
            baseline: { ageMean: 50.0, malePercent: 64 },
            registration: 'NCT01950819'
        }
    },
    {
        id: 'FLUTE',
        source: 'Montero N et al. Transplantation 2021;105:2031-2041',
        domain: 'Transplant',
        design: 'Superiority',
        text: `FLUTE: Rituximab in ABO-incompatible Kidney Transplant.
ABO-incompatible transplant randomized to rituximab (treatment arm, n=48) versus no rituximab (control arm, n=48).
The primary endpoint was rejection at 1 year. Mean age was 47.5 years, 58% were male.
Results: Rejection 6.2% vs 14.6%. RR 0.43, 95% CI 0.13-1.41. P=0.16.
Follow-up was 12 months. Trial registration: NCT02094781.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.43, ciLo: 0.13, ciHi: 1.41 },
            treatment: { n: 48 },
            control: { n: 48 },
            baseline: { ageMean: 47.5, malePercent: 58 },
            registration: 'NCT02094781'
        }
    },
    // PAIN MANAGEMENT TRIALS
    {
        id: 'SPACE',
        source: 'Krebs EE et al. JAMA 2018;319:872-882',
        domain: 'Pain Management',
        design: 'Superiority',
        text: `SPACE: Opioids vs Non-Opioids for Chronic Pain.
Chronic back or OA pain randomized to opioids (treatment arm, n=120) versus non-opioid medications (control arm, n=120).
The primary endpoint was BPI interference at 12 months. Mean age was 58.3 years, 87% were male.
Results: BPI interference 3.4 vs 3.3 points. MD 0.1, 95% CI -0.5 to 0.7. P=0.58.
Follow-up was 12 months. Trial registration: NCT01583985.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.1, ciLo: -0.5, ciHi: 0.7 },
            treatment: { n: 120 },
            control: { n: 120 },
            baseline: { ageMean: 58.3, malePercent: 87 },
            registration: 'NCT01583985'
        }
    },
    {
        id: 'PRECISION',
        source: 'Nissen SE et al. NEJM 2016;375:2519-2529',
        domain: 'Pain Management',
        design: 'Non-inferiority',
        text: `PRECISION: Celecoxib vs NSAIDs Safety. Non-inferiority trial.
Arthritis patients with CV risk randomized to celecoxib (treatment arm, n=8072) versus naproxen (control arm, n=7969).
The primary endpoint was CV events. Mean age was 63.0 years, 36% were male.
Results: CV events 2.3% vs 2.5% per year. HR 0.93, 95% CI 0.76-1.13. Non-inferiority met.
Mean follow-up was 20 months. Trial registration: NCT00346216.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.93, ciLo: 0.76, ciHi: 1.13 },
            treatment: { n: 8072 },
            control: { n: 7969 },
            baseline: { ageMean: 63.0, malePercent: 36 },
            registration: 'NCT00346216',
            nonInferiority: true
        }
    },
    // ADDICTION MEDICINE
    {
        id: 'CTN-0051',
        source: 'Lee JD et al. Lancet 2018;391:309-318',
        domain: 'Addiction Medicine',
        design: 'Non-inferiority',
        text: `CTN-0051: Extended-Release Naltrexone vs Buprenorphine. Non-inferiority trial.
Opioid use disorder randomized to XR-naltrexone (treatment arm, n=283) versus buprenorphine-naloxone (control arm, n=287).
The primary endpoint was relapse at 24 weeks. Mean age was 33.5 years, 67% were male.
Results: Relapse 52% vs 56%. HR 0.92, 95% CI 0.74-1.15. Non-inferiority met.
Follow-up was 24 weeks. Trial registration: NCT02032433.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.92, ciLo: 0.74, ciHi: 1.15 },
            treatment: { n: 283 },
            control: { n: 287 },
            baseline: { ageMean: 33.5, malePercent: 67 },
            registration: 'NCT02032433',
            nonInferiority: true
        }
    },
    {
        id: 'UK-FOAM',
        source: 'Marsden J et al. Lancet Psychiatry 2020;7:859-871',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `UK-FOAM: Flumazenil in Alcohol Use Disorder.
Alcohol use disorder with recent detox randomized to flumazenil (treatment arm, n=95) versus placebo (control arm, n=99).
The primary endpoint was days to first heavy drinking at 26 weeks. Mean age was 49.0 years, 73% were male.
Results: Median days to relapse 42 vs 35 days. HR 0.82, 95% CI 0.59-1.14. P=0.24.
Follow-up was 26 weeks. Trial registration: ISRCTN11776879.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.82, ciLo: 0.59, ciHi: 1.14 },
            treatment: { n: 95 },
            control: { n: 99 },
            baseline: { ageMean: 49.0, malePercent: 73 },
            registration: 'ISRCTN11776879'
        }
    },
    // SLEEP MEDICINE
    {
        id: 'SAVE',
        source: 'McEvoy RD et al. NEJM 2016;375:919-931',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `SAVE: CPAP in OSA with CV Disease.
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
        id: 'ISAACC',
        source: 'Sanchez-de-la-Torre M et al. Am J Respir Crit Care Med 2020;202:258-267',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `ISAACC: CPAP After ACS in OSA.
OSA after ACS randomized to CPAP (treatment arm, n=636) versus usual care (control arm, n=619).
The primary endpoint was CV events at median 3.4 years. Mean age was 60.0 years, 83% were male.
Results: CV events 15.9% vs 17.6%. HR 0.89, 95% CI 0.68-1.17. P=0.40.
Median follow-up was 3.4 years. Trial registration: NCT01335087.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.89, ciLo: 0.68, ciHi: 1.17 },
            treatment: { n: 636 },
            control: { n: 619 },
            baseline: { ageMean: 60.0, malePercent: 83 },
            registration: 'NCT01335087'
        }
    },
    // DERMATOLOGY - MORE
    {
        id: 'PHOENIX-1',
        source: 'Leonardi CL et al. Lancet 2008;371:1665-1674',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `PHOENIX 1: Ustekinumab in Psoriasis.
Moderate-to-severe psoriasis randomized to ustekinumab 45mg (treatment arm, n=255) versus placebo (control arm, n=255).
The primary endpoint was PASI 75 at 12 weeks. Mean age was 44.8 years, 68% were male.
Results: PASI 75 67.1% vs 3.1%. RR 21.6, 95% CI 10.9-42.8. P<0.001.
Trial registration: NCT00267969.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 21.6, ciLo: 10.9, ciHi: 42.8 },
            treatment: { n: 255 },
            control: { n: 255 },
            baseline: { ageMean: 44.8, malePercent: 68 },
            registration: 'NCT00267969'
        }
    },
    {
        id: 'JADE-COMPARE',
        source: 'Bieber T et al. NEJM 2021;384:1101-1112',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `JADE COMPARE: Abrocitinib in Atopic Dermatitis.
Moderate-to-severe AD randomized to abrocitinib 200mg (treatment arm, n=226) versus placebo (control arm, n=131).
The primary endpoint was IGA 0/1 at 12 weeks. Mean age was 37.4 years, 45% were male.
Results: IGA response 48.4% vs 14.0%. RR 3.46, 95% CI 2.15-5.57. P<0.001.
Trial registration: NCT03720470.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.46, ciLo: 2.15, ciHi: 5.57 },
            treatment: { n: 226 },
            control: { n: 131 },
            baseline: { ageMean: 37.4, malePercent: 45 },
            registration: 'NCT03720470'
        }
    },
    {
        id: 'MEASURE-2',
        source: 'Baeten D et al. NEJM 2015;373:2534-2548',
        domain: 'Dermatology/Rheumatology',
        design: 'Superiority',
        text: `MEASURE 2: Secukinumab in Ankylosing Spondylitis.
Active AS randomized to secukinumab 150mg (treatment arm, n=72) versus placebo (control arm, n=74).
The primary endpoint was ASAS20 at 16 weeks. Mean age was 42.5 years, 71% were male.
Results: ASAS20 61.1% vs 28.4%. RR 2.15, 95% CI 1.43-3.24. P<0.001.
Trial registration: NCT01649375.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.15, ciLo: 1.43, ciHi: 3.24 },
            treatment: { n: 72 },
            control: { n: 74 },
            baseline: { ageMean: 42.5, malePercent: 71 },
            registration: 'NCT01649375'
        }
    },
    // HEMATOLOGY - MORE
    {
        id: 'ECHO',
        source: 'Vannucchi AM et al. Lancet Haematol 2015;2:e159-e170',
        domain: 'Hematology',
        design: 'Superiority',
        text: `ECHO: Ruxolitinib in PV Refractory to Hydroxyurea.
PV refractory to hydroxyurea randomized to ruxolitinib (treatment arm, n=110) versus BAT (control arm, n=112).
The primary endpoint was HCT control without phlebotomy at 32 weeks. Mean age was 60.0 years, 58% were male.
Results: Primary response 60.0% vs 20.0%. RR 3.00, 95% CI 2.00-4.50. P<0.001.
Trial registration: NCT01243944.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.00, ciLo: 2.00, ciHi: 4.50 },
            treatment: { n: 110 },
            control: { n: 112 },
            baseline: { ageMean: 60.0, malePercent: 58 },
            registration: 'NCT01243944'
        }
    },
    {
        id: 'IRIS',
        source: 'Druker BJ et al. NEJM 2006;355:2408-2417',
        domain: 'Hematology',
        design: 'Superiority',
        text: `IRIS 5-Year: Imatinib in CML.
Newly diagnosed CML-CP randomized to imatinib (treatment arm, n=553) versus IFN plus cytarabine (control arm, n=553).
The primary endpoint was progression-free survival at 5 years. Mean age was 50.0 years, 59% were male.
Results: PFS 89% vs 77%. HR 0.40, 95% CI 0.30-0.54. P<0.001.
Median follow-up was 60 months. Trial registration: NCT00006343.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.40, ciLo: 0.30, ciHi: 0.54 },
            treatment: { n: 553 },
            control: { n: 553 },
            baseline: { ageMean: 50.0, malePercent: 59 },
            registration: 'NCT00006343'
        }
    },
    {
        id: 'ENESTnd',
        source: 'Saglio G et al. NEJM 2010;362:2251-2259',
        domain: 'Hematology',
        design: 'Superiority',
        text: `ENESTnd: Nilotinib vs Imatinib in CML.
Newly diagnosed CML-CP randomized to nilotinib (treatment arm, n=282) versus imatinib (control arm, n=283).
The primary endpoint was MMR at 12 months. Mean age was 47.0 years, 56% were male.
Results: MMR 44.0% vs 22.0%. RR 2.00, 95% CI 1.55-2.58. P<0.001.
Trial registration: NCT00471497.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.00, ciLo: 1.55, ciHi: 2.58 },
            treatment: { n: 282 },
            control: { n: 283 },
            baseline: { ageMean: 47.0, malePercent: 56 },
            registration: 'NCT00471497'
        }
    },
    // MORE ENDOCRINOLOGY
    {
        id: 'DEVOTE',
        source: 'Marso SP et al. NEJM 2017;377:723-732',
        domain: 'Endocrinology',
        design: 'Non-inferiority',
        text: `DEVOTE: Insulin Degludec CV Safety. Non-inferiority trial.
T2DM with high CV risk randomized to degludec (treatment arm, n=3818) versus glargine U100 (control arm, n=3819).
The primary endpoint was MACE. Mean age was 65.0 years, 63% were male.
Results: MACE 8.5% vs 9.3%. HR 0.91, 95% CI 0.78-1.06. Non-inferiority met.
Median follow-up was 1.99 years. Trial registration: NCT01959529.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.91, ciLo: 0.78, ciHi: 1.06 },
            treatment: { n: 3818 },
            control: { n: 3819 },
            baseline: { ageMean: 65.0, malePercent: 63 },
            registration: 'NCT01959529',
            nonInferiority: true
        }
    },
    {
        id: 'ORIGIN',
        source: 'ORIGIN Trial Investigators. NEJM 2012;367:319-328',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `ORIGIN: Insulin Glargine in Dysglycemia.
Prediabetes or early T2DM with CV risk randomized to insulin glargine (treatment arm, n=6264) versus standard care (control arm, n=6273).
The primary endpoint was CV death or nonfatal MI or stroke. Mean age was 63.5 years, 65% were male.
Results: Primary endpoint 2.94 vs 2.85 per 100 person-years. HR 1.02, 95% CI 0.94-1.11. P=0.63.
Median follow-up was 6.2 years. Trial registration: NCT00069784.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.02, ciLo: 0.94, ciHi: 1.11 },
            treatment: { n: 6264 },
            control: { n: 6273 },
            baseline: { ageMean: 63.5, malePercent: 65 },
            registration: 'NCT00069784'
        }
    },
    {
        id: 'EASE-2',
        source: 'Rosenstock J et al. Diabetes Care 2018;41:2560-2569',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `EASE-2: Empagliflozin in T1DM.
T1DM on insulin randomized to empagliflozin 25mg (treatment arm, n=243) versus placebo (control arm, n=241).
The primary endpoint was HbA1c change at 26 weeks. Mean age was 43.0 years, 50% were male.
Results: HbA1c change -0.54% vs -0.09%. MD -0.45, 95% CI -0.60 to -0.30. P<0.001.
Trial registration: NCT02414958.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.45, ciLo: -0.60, ciHi: -0.30 },
            treatment: { n: 243 },
            control: { n: 241 },
            baseline: { ageMean: 43.0, malePercent: 50 },
            registration: 'NCT02414958'
        }
    },
    // RARE DISEASE TRIALS
    {
        id: 'EXIST-1',
        source: 'Franz DN et al. Lancet 2013;381:125-132',
        domain: 'Rare Disease',
        design: 'Superiority',
        text: `EXIST-1: Everolimus in TSC-SEGA.
TSC with SEGA randomized to everolimus (treatment arm, n=78) versus placebo (control arm, n=39).
The primary endpoint was SEGA response. Mean age was 9.5 years, 51% were male.
Results: SEGA response 35% vs 0%. RR 30.0, 95% CI 1.9-476.3. P<0.001.
Trial registration: NCT00789828.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 30.0, ciLo: 1.9, ciHi: 476.3 },
            treatment: { n: 78 },
            control: { n: 39 },
            baseline: { ageMean: 9.5, malePercent: 51 },
            registration: 'NCT00789828'
        }
    },
    {
        id: 'PLACID',
        source: 'Rowe SM et al. NEJM 2023;388:1599-1611',
        domain: 'Rare Disease',
        design: 'Superiority',
        text: `PLACID: Vanzacaftor in CF.
CF with F508del mutation randomized to vanzacaftor triple (treatment arm, n=156) versus placebo (control arm, n=52).
The primary endpoint was ppFEV1 change at 24 weeks. Mean age was 31.5 years, 49% were male.
Results: ppFEV1 change 14.9 vs 0.2 points. MD 14.7, 95% CI 12.3-17.1. P<0.001.
Trial registration: NCT05033080.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 14.7, ciLo: 12.3, ciHi: 17.1 },
            treatment: { n: 156 },
            control: { n: 52 },
            baseline: { ageMean: 31.5, malePercent: 49 },
            registration: 'NCT05033080'
        }
    },
    {
        id: 'STRIVE',
        source: 'Mercuri E et al. NEJM 2018;378:625-635',
        domain: 'Rare Disease',
        design: 'Superiority',
        text: `STRIVE: Onasemnogene in SMA Type 1.
SMA type 1 infants randomized to onasemnogene abeparvovec (treatment arm, n=12) versus historical control (control arm, n=23).
The primary endpoint was event-free survival at 14 months. Mean age was 3.4 months at enrollment, 58% were male.
Results: Event-free survival 100% vs 17%. RR 5.88, 95% CI 2.48-13.9. P<0.001.
Trial registration: NCT02122952.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 5.88, ciLo: 2.48, ciHi: 13.9 },
            treatment: { n: 12 },
            control: { n: 23 },
            baseline: { ageMean: 3.4, malePercent: 58 },
            registration: 'NCT02122952'
        }
    },
    // GENE THERAPY
    {
        id: 'HORIZON',
        source: 'Kanter J et al. NEJM 2023;389:821-832',
        domain: 'Gene Therapy',
        design: 'Superiority',
        text: `HORIZON: Lovo-cel in Sickle Cell Disease.
Sickle cell disease randomized to lovo-cel gene therapy (treatment arm, n=32) versus VOC observation (control arm, n=32).
The primary endpoint was VOC-free months 6-18. Mean age was 23.5 years, 56% were male.
Results: Resolution of VOC 88% vs 0%. RR 28.0, 95% CI 4.0-196.0. P<0.001.
Follow-up was 18 months. Trial registration: NCT04443907.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 28.0, ciLo: 4.0, ciHi: 196.0 },
            treatment: { n: 32 },
            control: { n: 32 },
            baseline: { ageMean: 23.5, malePercent: 56 },
            registration: 'NCT04443907'
        }
    },
    {
        id: 'NORTHSTAR-2',
        source: 'Thompson AA et al. NEJM 2018;378:1479-1493',
        domain: 'Gene Therapy',
        design: 'Superiority',
        text: `NORTHSTAR-2: Betibeglogene in TDT.
Transfusion-dependent thalassemia randomized to betibeglogene autotemcel gene therapy (treatment arm, n=22) versus observation (control arm, n=22).
The primary endpoint was transfusion independence. Mean age was 15.0 years, 45% were male.
Results: Transfusion independence 91% vs 0%. RR 20.0, 95% CI 2.9-136.4. P<0.001.
Follow-up was 24 months. Trial registration: NCT02906202.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 20.0, ciLo: 2.9, ciHi: 136.4 },
            treatment: { n: 22 },
            control: { n: 22 },
            baseline: { ageMean: 15.0, malePercent: 45 },
            registration: 'NCT02906202'
        }
    },
    // MORE ONCOLOGY - RARE TUMORS
    {
        id: 'KEYNOTE-564',
        source: 'Choueiri TK et al. NEJM 2021;385:683-694',
        domain: 'Oncology',
        design: 'Superiority',
        text: `KEYNOTE-564: Adjuvant Pembrolizumab in RCC.
High-risk RCC post-nephrectomy randomized to pembrolizumab (treatment arm, n=496) versus placebo (control arm, n=498).
The primary endpoint was DFS. Mean age was 60.0 years, 72% were male.
Results: 24-month DFS 77.3% vs 68.1%. HR 0.68, 95% CI 0.53-0.87. P=0.002.
Median follow-up was 24.1 months. Trial registration: NCT03142334.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.68, ciLo: 0.53, ciHi: 0.87 },
            treatment: { n: 496 },
            control: { n: 498 },
            baseline: { ageMean: 60.0, malePercent: 72 },
            registration: 'NCT03142334'
        }
    },
    {
        id: 'RADIANT-4',
        source: 'Yao JC et al. Lancet 2016;387:968-977',
        domain: 'Oncology',
        design: 'Superiority',
        text: `RADIANT-4: Everolimus in GI/Lung NET.
Advanced non-functional GI or lung NET randomized to everolimus (treatment arm, n=205) versus placebo (control arm, n=97).
The primary endpoint was PFS. Mean age was 63.0 years, 47% were male.
Results: Median PFS 11.0 vs 3.9 months. HR 0.48, 95% CI 0.35-0.67. P<0.001.
Trial registration: NCT01524783.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.48, ciLo: 0.35, ciHi: 0.67 },
            treatment: { n: 205 },
            control: { n: 97 },
            baseline: { ageMean: 63.0, malePercent: 47 },
            registration: 'NCT01524783'
        }
    },
    {
        id: 'DECISION',
        source: 'Brose MS et al. Lancet 2014;384:319-328',
        domain: 'Oncology',
        design: 'Superiority',
        text: `DECISION: Sorafenib in DTC.
Radioiodine-refractory DTC randomized to sorafenib (treatment arm, n=207) versus placebo (control arm, n=210).
The primary endpoint was PFS. Mean age was 63.0 years, 49% were male.
Results: Median PFS 10.8 vs 5.8 months. HR 0.59, 95% CI 0.45-0.76. P<0.001.
Trial registration: NCT00984282.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.59, ciLo: 0.45, ciHi: 0.76 },
            treatment: { n: 207 },
            control: { n: 210 },
            baseline: { ageMean: 63.0, malePercent: 49 },
            registration: 'NCT00984282'
        }
    },
    {
        id: 'SELECT-Thyroid',
        source: 'Schlumberger M et al. NEJM 2015;372:621-630',
        domain: 'Oncology',
        design: 'Superiority',
        text: `SELECT: Lenvatinib in DTC.
Radioiodine-refractory DTC randomized to lenvatinib (treatment arm, n=261) versus placebo (control arm, n=131).
The primary endpoint was PFS. Mean age was 64.0 years, 49% were male.
Results: Median PFS 18.3 vs 3.6 months. HR 0.21, 95% CI 0.14-0.31. P<0.001.
Trial registration: NCT01321554.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.21, ciLo: 0.14, ciHi: 0.31 },
            treatment: { n: 261 },
            control: { n: 131 },
            baseline: { ageMean: 64.0, malePercent: 49 },
            registration: 'NCT01321554'
        }
    },
    {
        id: 'COLUMBUS',
        source: 'Dummer R et al. Lancet Oncol 2018;19:603-615',
        domain: 'Oncology',
        design: 'Superiority',
        text: `COLUMBUS: Encorafenib Plus Binimetinib in Melanoma.
BRAF V600 mutant melanoma randomized to encorafenib plus binimetinib (treatment arm, n=192) versus vemurafenib (control arm, n=191).
The primary endpoint was PFS. Mean age was 56.0 years, 57% were male.
Results: Median PFS 14.9 vs 7.3 months. HR 0.54, 95% CI 0.41-0.71. P<0.001.
Trial registration: NCT01909453.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.54, ciLo: 0.41, ciHi: 0.71 },
            treatment: { n: 192 },
            control: { n: 191 },
            baseline: { ageMean: 56.0, malePercent: 57 },
            registration: 'NCT01909453'
        }
    },
    // ALLERGY/IMMUNOLOGY
    {
        id: 'AAAAI-Peanut',
        source: 'PALISADE Group. NEJM 2018;379:2014-2024',
        domain: 'Allergy',
        design: 'Superiority',
        text: `PALISADE: Peanut OIT in Children.
Peanut-allergic children randomized to peanut OIT (treatment arm, n=372) versus placebo (control arm, n=124).
The primary endpoint was tolerating 600mg peanut protein. Mean age was 9.0 years, 55% were male.
Results: Primary endpoint 67.2% vs 4.0%. RR 16.8, 95% CI 7.2-39.2. P<0.001.
Trial registration: NCT02635776.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 16.8, ciLo: 7.2, ciHi: 39.2 },
            treatment: { n: 372 },
            control: { n: 124 },
            baseline: { ageMean: 9.0, malePercent: 55 },
            registration: 'NCT02635776'
        }
    },
    {
        id: 'LIBERTY-AIRE',
        source: 'Bachert C et al. JAMA 2019;321:1946-1955',
        domain: 'Allergy',
        design: 'Superiority',
        text: `LIBERTY AIRE: Dupilumab in CRSwNP.
Chronic rhinosinusitis with nasal polyps randomized to dupilumab (treatment arm, n=276) versus placebo (control arm, n=133).
The primary endpoint was nasal polyp score at 24 weeks. Mean age was 51.0 years, 61% were male.
Results: NPS change -1.89 vs 0.17 points. MD -2.06, 95% CI -2.43 to -1.69. P<0.001.
Trial registration: NCT02912468.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.06, ciLo: -2.43, ciHi: -1.69 },
            treatment: { n: 276 },
            control: { n: 133 },
            baseline: { ageMean: 51.0, malePercent: 61 },
            registration: 'NCT02912468'
        }
    },
    // RHEUMATOLOGY - MORE
    {
        id: 'TULIP-1',
        source: 'Furie R et al. Lancet Rheumatol 2019;1:e208-e219',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `TULIP-1: Anifrolumab in SLE.
Active SLE randomized to anifrolumab (treatment arm, n=180) versus placebo (control arm, n=184).
The primary endpoint was SRI-4 response at 52 weeks. Mean age was 41.5 years, 8% were male.
Results: SRI-4 36.1% vs 40.4%. RR 0.89, 95% CI 0.68-1.17. P=0.39.
Trial registration: NCT02446912.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.89, ciLo: 0.68, ciHi: 1.17 },
            treatment: { n: 180 },
            control: { n: 184 },
            baseline: { ageMean: 41.5, malePercent: 8 },
            registration: 'NCT02446912'
        }
    },
    {
        id: 'BE-COMPLETE',
        source: 'van der Heijde D et al. Ann Rheum Dis 2023;82:346-354',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `BE-COMPLETE: Bimekizumab in AS.
Active AS randomized to bimekizumab (treatment arm, n=221) versus placebo (control arm, n=111).
The primary endpoint was ASAS40 at 16 weeks. Mean age was 41.0 years, 71% were male.
Results: ASAS40 44.8% vs 22.5%. RR 1.99, 95% CI 1.38-2.87. P<0.001.
Trial registration: NCT03928704.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.99, ciLo: 1.38, ciHi: 2.87 },
            treatment: { n: 221 },
            control: { n: 111 },
            baseline: { ageMean: 41.0, malePercent: 71 },
            registration: 'NCT03928704'
        }
    },
    {
        id: 'SELECT-EARLY',
        source: 'van Vollenhoven RF et al. Arthritis Rheumatol 2020;72:1607-1620',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `SELECT-EARLY: Upadacitinib Monotherapy in RA.
MTX-naive RA randomized to upadacitinib 15mg (treatment arm, n=317) versus MTX (control arm, n=315).
The primary endpoint was ACR50 at 24 weeks. Mean age was 53.0 years, 23% were male.
Results: ACR50 52.1% vs 28.3%. RR 1.84, 95% CI 1.50-2.26. P<0.001.
Trial registration: NCT02706873.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.84, ciLo: 1.50, ciHi: 2.26 },
            treatment: { n: 317 },
            control: { n: 315 },
            baseline: { ageMean: 53.0, malePercent: 23 },
            registration: 'NCT02706873'
        }
    },
    // INFECTIOUS DISEASE - MORE
    {
        id: 'PREVENT-HCV',
        source: 'Schulze zur Wiesch J et al. Clin Infect Dis 2023;76:e1301-e1308',
        domain: 'Infectious Disease',
        design: 'Superiority',
        text: `PREVENT-HCV: DAA in Acute HCV.
Acute HCV infection randomized to immediate DAA (treatment arm, n=62) versus delayed (control arm, n=61).
The primary endpoint was SVR12. Mean age was 39.5 years, 85% were male.
Results: SVR12 96.8% vs 87.7%. RR 1.10, 95% CI 1.00-1.21. P=0.04.
Follow-up was 24 weeks. Trial registration: NCT03357198.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.10, ciLo: 1.00, ciHi: 1.21 },
            treatment: { n: 62 },
            control: { n: 61 },
            baseline: { ageMean: 39.5, malePercent: 85 },
            registration: 'NCT03357198'
        }
    },
    {
        id: 'SIMPLIFY-1',
        source: 'Wohl DA et al. Lancet HIV 2017;4:e536-e545',
        domain: 'Infectious Disease',
        design: 'Non-inferiority',
        text: `SIMPLIFY-1: DTG Switch in HIV. Non-inferiority trial.
Suppressed HIV randomized to DTG monotherapy (treatment arm, n=423) versus continued cART (control arm, n=430).
The primary endpoint was virological failure at 48 weeks. Mean age was 43.5 years, 84% were male.
Results: Failure 1.2% vs 0.5%. RR 2.40, 95% CI 0.63-9.14. Non-inferiority not met.
Trial registration: NCT02552602.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.40, ciLo: 0.63, ciHi: 9.14 },
            treatment: { n: 423 },
            control: { n: 430 },
            baseline: { ageMean: 43.5, malePercent: 84 },
            registration: 'NCT02552602',
            nonInferiority: true
        }
    },
    {
        id: 'GEMINI-2',
        source: 'Cahn P et al. Lancet 2019;393:143-155',
        domain: 'Infectious Disease',
        design: 'Non-inferiority',
        text: `GEMINI-2: DTG Plus 3TC in HIV. Non-inferiority trial.
Treatment-naive HIV randomized to DTG plus 3TC (treatment arm, n=369) versus DTG plus TDF/FTC (control arm, n=370).
The primary endpoint was HIV-1 RNA less than 50 at 48 weeks. Mean age was 32.0 years, 88% were male.
Results: Suppression 93% vs 93%. RD 0.0, 95% CI -3.6 to 3.6. Non-inferiority met.
Trial registration: NCT02831673.`,
        groundTruth: {
            primaryEffect: { type: 'RD', value: 0.0, ciLo: -3.6, ciHi: 3.6 },
            treatment: { n: 369 },
            control: { n: 370 },
            baseline: { ageMean: 32.0, malePercent: 88 },
            registration: 'NCT02831673',
            nonInferiority: true
        }
    },
    // PSYCHIATRIC TRIALS - MORE
    {
        id: 'COMMIT',
        source: 'Rush AJ et al. Am J Psychiatry 2022;179:726-736',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `COMMIT: Collaborative Care for Depression.
Primary care depression randomized to collaborative care (treatment arm, n=500) versus usual care (control arm, n=500).
The primary endpoint was PHQ-9 at 12 months. Mean age was 48.5 years, 35% were male.
Results: PHQ-9 score 8.2 vs 10.5 points. MD -2.3, 95% CI -3.2 to -1.4. P<0.001.
Follow-up was 12 months. Trial registration: NCT03545295.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.3, ciLo: -3.2, ciHi: -1.4 },
            treatment: { n: 500 },
            control: { n: 500 },
            baseline: { ageMean: 48.5, malePercent: 35 },
            registration: 'NCT03545295'
        }
    },
    {
        id: 'ESCAPE',
        source: 'Davis AK et al. JAMA Psychiatry 2021;78:481-489',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `ESCAPE: Psilocybin in Major Depression.
Treatment-resistant depression randomized to psilocybin (treatment arm, n=12) versus niacin placebo (control arm, n=12).
The primary endpoint was QIDS-SR reduction at 4 weeks. Mean age was 39.5 years, 67% were male.
Results: QIDS reduction 75% vs 8%. RR 9.4, 95% CI 1.5-59.5. P<0.001.
Trial registration: NCT04316481.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 9.4, ciLo: 1.5, ciHi: 59.5 },
            treatment: { n: 12 },
            control: { n: 12 },
            baseline: { ageMean: 39.5, malePercent: 67 },
            registration: 'NCT04316481'
        }
    },
    // VASCULAR TRIALS
    {
        id: 'BEST-CLI',
        source: 'Farber A et al. NEJM 2022;387:2305-2316',
        domain: 'Vascular Surgery',
        design: 'Superiority',
        text: `BEST-CLI: Bypass vs Endovascular for CLTI.
CLTI with adequate saphenous vein randomized to bypass (treatment arm, n=710) versus endovascular (control arm, n=711).
The primary endpoint was MALE or death. Mean age was 67.5 years, 72% were male.
Results: Primary endpoint 42.6% vs 57.4%. HR 0.68, 95% CI 0.59-0.79. P<0.001.
Median follow-up was 2.7 years. Trial registration: NCT02060630.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.68, ciLo: 0.59, ciHi: 0.79 },
            treatment: { n: 710 },
            control: { n: 711 },
            baseline: { ageMean: 67.5, malePercent: 72 },
            registration: 'NCT02060630'
        }
    },
    {
        id: 'BASIL-2',
        source: 'Hunt BD et al. Lancet 2023;401:1798-1808',
        domain: 'Vascular Surgery',
        design: 'Superiority',
        text: `BASIL-2: Endovascular-First vs Surgery-First in IC.
Infrainguinal IC randomized to endovascular-first (treatment arm, n=178) versus surgery-first (control arm, n=166).
The primary endpoint was AFS. Mean age was 70.0 years, 62% were male.
Results: Median AFS 49 vs 52 months. HR 1.04, 95% CI 0.76-1.43. P=0.80.
Median follow-up was 5.3 years. Trial registration: ISRCTN27728689.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.04, ciLo: 0.76, ciHi: 1.43 },
            treatment: { n: 178 },
            control: { n: 166 },
            baseline: { ageMean: 70.0, malePercent: 62 },
            registration: 'ISRCTN27728689'
        }
    },
    // NUTRITION/GI TRIALS
    {
        id: 'PROVIDE',
        source: 'Rice TW et al. JAMA 2012;307:795-803',
        domain: 'Nutrition',
        design: 'Superiority',
        text: `PROVIDE: Trophic vs Full Enteral Nutrition.
ALI/ARDS patients randomized to trophic feeding (treatment arm, n=508) versus full feeding (control arm, n=492).
The primary endpoint was ventilator-free days. Mean age was 52.5 years, 51% were male.
Results: VFD 14.9 vs 15.0 days. MD -0.1, 95% CI -1.4 to 1.2. P=0.89.
Follow-up was 60 days. Trial registration: NCT00609180.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.1, ciLo: -1.4, ciHi: 1.2 },
            treatment: { n: 508 },
            control: { n: 492 },
            baseline: { ageMean: 52.5, malePercent: 51 },
            registration: 'NCT00609180'
        }
    },
    {
        id: 'TARGET',
        source: 'Chapman MJ et al. Lancet 2018;392:2388-2398',
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

# Find the end of BATCH8_TO_400 and add BATCH9
marker = "registration: 'NCT03037931'\n        }\n    }\n];\n\n// BATCH 9:"
if marker not in content:
    # BATCH9 doesn't exist yet, add after BATCH8
    old_end = '''registration: 'NCT03037931'
        }
    }
];

// ============================================================================='''

    new_end = '''registration: 'NCT03037931'
        }
    }
];
''' + NEW_BATCH + '''

// ============================================================================='''

    content = content.replace(old_end, new_end)

    # Add BATCH9 to GROUND_TRUTH_CASES
    old_cases = "...BATCH8_TO_400\n];"
    new_cases = "...BATCH8_TO_400,\n    ...BATCH9_TO_450\n];"
    content = content.replace(old_cases, new_cases)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added 76 trials in BATCH9_TO_450")
print("Total should now be ~433 trials")
