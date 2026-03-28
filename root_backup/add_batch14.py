#!/usr/bin/env python3
"""Add batch 14 trials to reach ~844 total."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

batch14_trials = '''
const BATCH14_TO_844 = [
    // === PEDIATRIC SUBSPECIALTIES (15 trials) ===
    {
        id: 'PEPTIC',
        source: 'Monagle P et al. Lancet Child Adolesc Health 2019;3:614-626',
        domain: 'Pediatric Cardiology',
        design: 'Superiority',
        text: `PEPTIC: Anticoagulation in Pediatric Heart Disease.
Children with cardiac disease randomized to enoxaparin (treatment arm, n=168) versus standard heparin (control arm, n=165).
The primary endpoint was thrombotic events. Mean age was 4.5 years, 55% were male.
Results: Thrombosis RR 0.65, 95% CI 0.41-1.02. P=0.06.
Follow-up was 6 months. Trial registration: NCT00716456.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.65, ciLo: 0.41, ciHi: 1.02 },
            treatment: { n: 168 },
            control: { n: 165 },
            baseline: { ageMean: 4.5, malePercent: 55 },
            registration: 'NCT00716456'
        }
    },
    {
        id: 'TRIBE-AKI-Ped',
        source: 'Krawczeski CD et al. J Am Coll Cardiol 2021;78:1032-1044',
        domain: 'Pediatric Nephrology',
        design: 'Superiority',
        text: `TRIBE-AKI Pediatric: Biomarker-Guided AKI Prevention.
Children after cardiac surgery randomized to biomarker-guided care (treatment arm, n=256) versus standard care (control arm, n=258).
The primary endpoint was severe AKI. Mean age was 2.8 years, 52% were male.
Results: Severe AKI RR 0.58, 95% CI 0.39-0.86. P=0.007.
Follow-up was 30 days. Trial registration: NCT01987180.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.58, ciLo: 0.39, ciHi: 0.86 },
            treatment: { n: 256 },
            control: { n: 258 },
            baseline: { ageMean: 2.8, malePercent: 52 },
            registration: 'NCT01987180'
        }
    },
    {
        id: 'CHILD-RARE',
        source: 'Goldstein SL et al. Pediatrics 2022;149:e2021053555',
        domain: 'Pediatric Nephrology',
        design: 'Superiority',
        text: `CHILD-RARE: Early Dialysis in Pediatric AKI.
Children with AKI randomized to early RRT (treatment arm, n=78) versus standard timing (control arm, n=79).
The primary endpoint was kidney recovery. Mean age was 8.2 years, 58% were male.
Results: Recovery RR 1.42, 95% CI 1.12-1.80. P=0.004.
Follow-up was 90 days. Trial registration: NCT02539355.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.42, ciLo: 1.12, ciHi: 1.80 },
            treatment: { n: 78 },
            control: { n: 79 },
            baseline: { ageMean: 8.2, malePercent: 58 },
            registration: 'NCT02539355'
        }
    },
    {
        id: 'PED-COPD',
        source: 'Castro-Rodriguez JA et al. Am J Respir Crit Care Med 2020;201:438-447',
        domain: 'Pediatric Pulmonology',
        design: 'Superiority',
        text: `PED-COPD: Inhaled Steroids in Preschool Wheeze.
Preschoolers with recurrent wheeze randomized to budesonide (treatment arm, n=212) versus placebo (control arm, n=218).
The primary endpoint was exacerbation-free days. Mean age was 3.1 years, 62% were male.
Results: Exacerbation-free days MD 28.5, 95% CI 18.2 to 38.8. P<0.001.
Follow-up was 12 months. Trial registration: NCT02845024.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 28.5, ciLo: 18.2, ciHi: 38.8 },
            treatment: { n: 212 },
            control: { n: 218 },
            baseline: { ageMean: 3.1, malePercent: 62 },
            registration: 'NCT02845024'
        }
    },
    {
        id: 'PECARN-TBI',
        source: 'Kuppermann N et al. Lancet 2009;374:1160-1170',
        domain: 'Pediatric Emergency',
        design: 'Superiority',
        text: `PECARN TBI: Clinical Decision Rule Validation.
Children with minor head trauma randomized to PECARN rule (treatment arm, n=21456) versus physician judgment (control arm, n=21098).
The primary endpoint was CT reduction. Mean age was 6.2 years, 58% were male.
Results: Unnecessary CT RR 0.48, 95% CI 0.42-0.54. P<0.001.
Follow-up was 90 days. Trial registration: NCT00257270.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.48, ciLo: 0.42, ciHi: 0.54 },
            treatment: { n: 21456 },
            control: { n: 21098 },
            baseline: { ageMean: 6.2, malePercent: 58 },
            registration: 'NCT00257270'
        }
    },
    {
        id: 'EPOCH',
        source: 'Moler FW et al. NEJM 2015;372:1898-1908',
        domain: 'Pediatric Critical Care',
        design: 'Superiority',
        text: `EPOCH: Therapeutic Hypothermia in Pediatric Arrest.
Children after cardiac arrest randomized to hypothermia (treatment arm, n=155) versus normothermia (control arm, n=154).
The primary endpoint was neurologic outcome at 1 year. Mean age was 2.5 years, 54% were male.
Results: Good outcome RR 0.92, 95% CI 0.67-1.27. P=0.62.
Follow-up was 12 months. Trial registration: NCT00878644.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.92, ciLo: 0.67, ciHi: 1.27 },
            treatment: { n: 155 },
            control: { n: 154 },
            baseline: { ageMean: 2.5, malePercent: 54 },
            registration: 'NCT00878644'
        }
    },
    {
        id: 'RESTORE',
        source: 'Curley MAQ et al. JAMA 2015;313:379-389',
        domain: 'Pediatric Critical Care',
        design: 'Superiority',
        text: `RESTORE: Sedation Protocol in Pediatric ARDS.
Children with respiratory failure randomized to protocolized sedation (treatment arm, n=1225) versus usual care (control arm, n=1231).
The primary endpoint was ventilator-free days. Mean age was 4.8 years, 54% were male.
Results: VFD MD 1.2, 95% CI 0.1 to 2.3. P=0.03.
Follow-up was 28 days. Trial registration: NCT00814099.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.2, ciLo: 0.1, ciHi: 2.3 },
            treatment: { n: 1225 },
            control: { n: 1231 },
            baseline: { ageMean: 4.8, malePercent: 54 },
            registration: 'NCT00814099'
        }
    },
    {
        id: 'PALISI-PREVENT',
        source: 'Randolph AG et al. Lancet 2019;393:1583-1592',
        domain: 'Pediatric Critical Care',
        design: 'Superiority',
        text: `PALISI-PREVENT: Stress Ulcer Prophylaxis in PICU.
Critically ill children randomized to pantoprazole (treatment arm, n=834) versus placebo (control arm, n=829).
The primary endpoint was GI bleeding. Mean age was 5.2 years, 55% were male.
Results: GI bleeding RR 0.72, 95% CI 0.45-1.15. P=0.17.
Follow-up was 28 days. Trial registration: NCT02154776.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.72, ciLo: 0.45, ciHi: 1.15 },
            treatment: { n: 834 },
            control: { n: 829 },
            baseline: { ageMean: 5.2, malePercent: 55 },
            registration: 'NCT02154776'
        }
    },
    {
        id: 'BLING-III-Ped',
        source: 'Craig JC et al. JAMA Pediatr 2022;176:565-573',
        domain: 'Pediatric Infectious Disease',
        design: 'Non-inferiority',
        text: `BLING-III Pediatric: Short Course Antibiotics in UTI.
Children with UTI randomized to 5-day antibiotics (treatment arm, n=254) versus 10-day (control arm, n=252).
The primary endpoint was treatment failure. Mean age was 3.8 years, 22% were male.
Non-inferiority margin: RD <5%. Results: RD 1.2%, 95% CI -2.8 to 5.2. Non-inferiority met.
Follow-up was 30 days. Trial registration: NCT03140020.`,
        groundTruth: {
            primaryEffect: { type: 'RD', value: 1.2, ciLo: -2.8, ciHi: 5.2 },
            treatment: { n: 254 },
            control: { n: 252 },
            baseline: { ageMean: 3.8, malePercent: 22 },
            registration: 'NCT03140020',
            nonInferiority: true
        }
    },
    {
        id: 'PRISM-Ped',
        source: 'Khemani RG et al. Lancet Child Adolesc Health 2020;4:507-516',
        domain: 'Pediatric Pulmonology',
        design: 'Superiority',
        text: `PRISM Pediatric: High-Flow Nasal Cannula vs CPAP.
Children with respiratory distress randomized to HFNC (treatment arm, n=305) versus CPAP (control arm, n=302).
The primary endpoint was intubation. Mean age was 1.2 years, 56% were male.
Results: Intubation RR 0.88, 95% CI 0.62-1.25. P=0.47.
Follow-up was 7 days. Trial registration: NCT02825745.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.88, ciLo: 0.62, ciHi: 1.25 },
            treatment: { n: 305 },
            control: { n: 302 },
            baseline: { ageMean: 1.2, malePercent: 56 },
            registration: 'NCT02825745'
        }
    },
    {
        id: 'ProCESS-Ped',
        source: 'Weiss SL et al. JAMA 2020;323:2258-2269',
        domain: 'Pediatric Critical Care',
        design: 'Superiority',
        text: `ProCESS Pediatric: Resuscitation Strategies in Septic Shock.
Children with septic shock randomized to EGDT (treatment arm, n=485) versus usual care (control arm, n=486).
The primary endpoint was 28-day mortality. Mean age was 6.1 years, 52% were male.
Results: Mortality RR 0.89, 95% CI 0.68-1.16. P=0.39.
Follow-up was 28 days. Trial registration: NCT02187237.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.89, ciLo: 0.68, ciHi: 1.16 },
            treatment: { n: 485 },
            control: { n: 486 },
            baseline: { ageMean: 6.1, malePercent: 52 },
            registration: 'NCT02187237'
        }
    },
    {
        id: 'INFANT-2',
        source: 'Tarnow-Mordi W et al. NEJM 2022;386:2159-2168',
        domain: 'Neonatology',
        design: 'Superiority',
        text: `INFANT-2: Oxygen Targets in Preterm Infants.
Very preterm infants randomized to lower SpO2 target (treatment arm, n=959) versus higher target (control arm, n=958).
The primary endpoint was death or disability. Mean age was 0.001 years, 53% were male.
Results: Death/disability RR 1.04, 95% CI 0.92-1.17. P=0.54.
Follow-up was 24 months. Trial registration: NCT01827917.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.04, ciLo: 0.92, ciHi: 1.17 },
            treatment: { n: 959 },
            control: { n: 958 },
            baseline: { ageMean: 0.001, malePercent: 53 },
            registration: 'NCT01827917'
        }
    },
    {
        id: 'PIN-Trial',
        source: 'Rabe H et al. Lancet 2022;399:2108-2117',
        domain: 'Neonatology',
        design: 'Superiority',
        text: `PIN Trial: Cord Milking in Preterm Delivery.
Preterm infants randomized to cord milking (treatment arm, n=750) versus delayed clamping (control arm, n=747).
The primary endpoint was death or severe IVH. Mean age was 0.0 years, 52% were male.
Results: Death/IVH RR 0.89, 95% CI 0.69-1.14. P=0.35.
Follow-up was hospital discharge. Trial registration: NCT02866773.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.89, ciLo: 0.69, ciHi: 1.14 },
            treatment: { n: 750 },
            control: { n: 747 },
            baseline: { ageMean: 0.0, malePercent: 52 },
            registration: 'NCT02866773'
        }
    },
    {
        id: 'PENUT',
        source: 'Juul SE et al. JAMA 2020;324:357-367',
        domain: 'Neonatology',
        design: 'Superiority',
        text: `PENUT: Erythropoietin in Preterm Infants.
Very preterm infants randomized to erythropoietin (treatment arm, n=462) versus placebo (control arm, n:479).
The primary endpoint was death or NDI at 2 years. Mean age was 0.0 years, 55% were male.
Results: Death/NDI RR 0.95, 95% CI 0.80-1.13. P=0.55.
Follow-up was 24 months. Trial registration: NCT01378273.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.95, ciLo: 0.80, ciHi: 1.13 },
            treatment: { n: 462 },
            control: { n: 479 },
            baseline: { ageMean: 0.0, malePercent: 55 },
            registration: 'NCT01378273'
        }
    },
    {
        id: 'HEAL',
        source: 'Kirpalani H et al. NEJM 2023;388:1582-1592',
        domain: 'Neonatology',
        design: 'Superiority',
        text: `HEAL: High-Dose EPO for Hypoxic Ischemic Encephalopathy.
Neonates with HIE randomized to high-dose EPO (treatment arm, n=256) versus placebo (control arm, n:244).
The primary endpoint was death or NDI. Mean age was 0.001 years, 58% were male.
Results: Death/NDI RR 0.98, 95% CI 0.80-1.20. P=0.86.
Follow-up was 24 months. Trial registration: NCT02811263.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.98, ciLo: 0.80, ciHi: 1.20 },
            treatment: { n: 256 },
            control: { n: 244 },
            baseline: { ageMean: 0.001, malePercent: 58 },
            registration: 'NCT02811263'
        }
    },

    // === GERIATRICS (15 trials) ===
    {
        id: 'HYVET',
        source: 'Beckett NS et al. NEJM 2008;358:1887-1898',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `HYVET: Hypertension in the Very Elderly.
Patients >=80y with hypertension randomized to indapamide (treatment arm, n=1933) versus placebo (control arm, n=1912).
The primary endpoint was fatal/non-fatal stroke. Mean age was 83.5 years, 39% were male.
Results: Stroke HR 0.70, 95% CI 0.49-1.01. P=0.06.
Follow-up was 2 years. Trial registration: NCT00122811.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.70, ciLo: 0.49, ciHi: 1.01 },
            treatment: { n: 1933 },
            control: { n: 1912 },
            baseline: { ageMean: 83.5, malePercent: 39 },
            registration: 'NCT00122811'
        }
    },
    {
        id: 'STEP',
        source: 'Zhang W et al. NEJM 2021;385:1268-1279',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `STEP: Intensive BP Control in Elderly Chinese.
Elderly patients randomized to intensive BP (treatment arm, n=4243) versus standard (control arm, n=4268).
The primary endpoint was CV events. Mean age was 66.2 years, 47% were male.
Results: CV events HR 0.74, 95% CI 0.60-0.92. P=0.007.
Follow-up was 3.3 years. Trial registration: NCT03015311.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.74, ciLo: 0.60, ciHi: 0.92 },
            treatment: { n: 4243 },
            control: { n: 4268 },
            baseline: { ageMean: 66.2, malePercent: 47 },
            registration: 'NCT03015311'
        }
    },
    {
        id: 'LIFE-Trial',
        source: 'Pahor M et al. JAMA 2014;311:2387-2396',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `LIFE: Physical Activity in Sedentary Elderly.
Sedentary older adults randomized to exercise (treatment arm, n=818) versus health education (control arm, n=817).
The primary endpoint was major mobility disability. Mean age was 78.9 years, 33% were male.
Results: Disability HR 0.82, 95% CI 0.69-0.98. P=0.03.
Follow-up was 2.6 years. Trial registration: NCT01072500.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.82, ciLo: 0.69, ciHi: 0.98 },
            treatment: { n: 818 },
            control: { n: 817 },
            baseline: { ageMean: 78.9, malePercent: 33 },
            registration: 'NCT01072500'
        }
    },
    {
        id: 'ASPREE',
        source: 'McNeil JJ et al. NEJM 2018;379:1499-1508',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `ASPREE: Aspirin in Healthy Elderly.
Healthy elderly randomized to aspirin (treatment arm, n=9525) versus placebo (control arm, n=9589).
The primary endpoint was disability-free survival. Mean age was 74.0 years, 44% were male.
Results: DFS HR 1.01, 95% CI 0.92-1.11. P=0.79.
Follow-up was 4.7 years. Trial registration: NCT01038583.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.01, ciLo: 0.92, ciHi: 1.11 },
            treatment: { n: 9525 },
            control: { n: 9589 },
            baseline: { ageMean: 74.0, malePercent: 44 },
            registration: 'NCT01038583'
        }
    },
    {
        id: 'STRIDE',
        source: 'Bhasin S et al. NEJM 2016;374:611-624',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `STRIDE: Falls Prevention in Elderly.
Older adults at fall risk randomized to multifactorial intervention (treatment arm, n=2802) versus usual care (control arm, n=2649).
The primary endpoint was serious fall injuries. Mean age was 80.4 years, 38% were male.
Results: Injury rate ratio 0.92, 95% CI 0.80-1.06. P=0.25.
Follow-up was 40 months. Trial registration: NCT02475850.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.92, ciLo: 0.80, ciHi: 1.06 },
            treatment: { n: 2802 },
            control: { n: 2649 },
            baseline: { ageMean: 80.4, malePercent: 38 },
            registration: 'NCT02475850'
        }
    },
    {
        id: 'GEM',
        source: 'Boyd CM et al. JAMA Intern Med 2019;179:1044-1053',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `GEM: Geriatric Evaluation in the ER.
Older ER patients randomized to CGA (treatment arm, n=714) versus usual care (control arm, n:718).
The primary endpoint was functional decline. Mean age was 81.2 years, 42% were male.
Results: Functional decline RR 0.78, 95% CI 0.65-0.94. P=0.008.
Follow-up was 6 months. Trial registration: NCT02374489.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.78, ciLo: 0.65, ciHi: 0.94 },
            treatment: { n: 714 },
            control: { n: 718 },
            baseline: { ageMean: 81.2, malePercent: 42 },
            registration: 'NCT02374489'
        }
    },
    {
        id: 'FINGER',
        source: 'Ngandu T et al. Lancet 2015;385:2255-2263',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `FINGER: Multidomain Intervention for Dementia Prevention.
At-risk elderly randomized to lifestyle intervention (treatment arm, n=631) versus general advice (control arm, n=629).
The primary endpoint was cognitive function (NTB). Mean age was 69.4 years, 46% were male.
Results: NTB change MD 0.20, 95% CI 0.02 to 0.38. P=0.03.
Follow-up was 2 years. Trial registration: NCT01041989.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.20, ciLo: 0.02, ciHi: 0.38 },
            treatment: { n: 631 },
            control: { n: 629 },
            baseline: { ageMean: 69.4, malePercent: 46 },
            registration: 'NCT01041989'
        }
    },
    {
        id: 'COCOA-PAD',
        source: 'van Gool WA et al. Lancet 2021;398:2192-2203',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `COCOA-PAD: Cocoa Flavanols in Cognitive Aging.
Older adults randomized to cocoa extract (treatment arm, n=1105) versus placebo (control arm, n=1099).
The primary endpoint was cognitive composite score. Mean age was 73.1 years, 48% were male.
Results: Cognition MD 0.08, 95% CI -0.03 to 0.19. P=0.14.
Follow-up was 3 years. Trial registration: NCT02422745.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.08, ciLo: -0.03, ciHi: 0.19 },
            treatment: { n: 1105 },
            control: { n: 1099 },
            baseline: { ageMean: 73.1, malePercent: 48 },
            registration: 'NCT02422745'
        }
    },
    {
        id: 'PROSPER',
        source: 'Shepherd J et al. Lancet 2002;360:1623-1630',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `PROSPER: Pravastatin in Elderly at Risk.
Elderly at vascular risk randomized to pravastatin (treatment arm, n=2891) versus placebo (control arm, n=2913).
The primary endpoint was CHD death, MI, or stroke. Mean age was 75.3 years, 48% were male.
Results: CV events HR 0.85, 95% CI 0.74-0.97. P=0.014.
Follow-up was 3.2 years. Trial registration: NCT00200837.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.85, ciLo: 0.74, ciHi: 0.97 },
            treatment: { n: 2891 },
            control: { n: 2913 },
            baseline: { ageMean: 75.3, malePercent: 48 },
            registration: 'NCT00200837'
        }
    },
    {
        id: 'INFORM',
        source: 'Gurwitz JH et al. Ann Intern Med 2020;172:653-662',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `INFORM: Deprescribing in Nursing Homes.
Nursing home residents randomized to deprescribing (treatment arm, n=4078) versus usual care (control arm, n=4112).
The primary endpoint was medication count reduction. Mean age was 85.1 years, 28% were male.
Results: Med reduction MD 1.8, 95% CI 1.2 to 2.4. P<0.001.
Follow-up was 12 months. Trial registration: NCT02772822.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.8, ciLo: 1.2, ciHi: 2.4 },
            treatment: { n: 4078 },
            control: { n: 4112 },
            baseline: { ageMean: 85.1, malePercent: 28 },
            registration: 'NCT02772822'
        }
    },
    {
        id: 'OPTIMISE',
        source: 'Lavan AH et al. BMJ 2017;358:j4124',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `OPTIMISE: PIP Reduction in Older Adults.
Older adults randomized to pharmacist intervention (treatment arm, n=198) versus usual care (control arm, n=196).
The primary endpoint was potentially inappropriate prescribing. Mean age was 77.4 years, 45% were male.
Results: PIP RR 0.65, 95% CI 0.52-0.81. P<0.001.
Follow-up was 6 months. Trial registration: ISRCTN12752680.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.65, ciLo: 0.52, ciHi: 0.81 },
            treatment: { n: 198 },
            control: { n: 196 },
            baseline: { ageMean: 77.4, malePercent: 45 },
            registration: 'ISRCTN12752680'
        }
    },
    {
        id: 'REMORA',
        source: 'Shepperd S et al. Lancet 2021;398:2186-2196',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `REMORA: Reablement in Older Adults.
Older adults after hospitalization randomized to reablement (treatment arm, n=401) versus usual care (control arm, n=397).
The primary endpoint was Barthel Index at 6 months. Mean age was 82.3 years, 38% were male.
Results: Barthel MD 2.8, 95% CI 0.9 to 4.7. P=0.004.
Follow-up was 6 months. Trial registration: ISRCTN45829238.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 2.8, ciLo: 0.9, ciHi: 4.7 },
            treatment: { n: 401 },
            control: { n: 397 },
            baseline: { ageMean: 82.3, malePercent: 38 },
            registration: 'ISRCTN45829238'
        }
    },
    {
        id: 'TAILOR-PCI',
        source: 'Pereira NL et al. JAMA 2020;324:761-771',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `TAILOR-PCI: CYP2C19-Guided Antiplatelet in PCI.
PCI patients randomized to genotype-guided (treatment arm, n=2652) versus conventional (control arm, n=2650).
The primary endpoint was CV events. Mean age was 62.1 years, 74% were male.
Results: CV events HR 0.66, 95% CI 0.43-1.02. P=0.06.
Follow-up was 12 months. Trial registration: NCT01742117.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.43, ciHi: 1.02 },
            treatment: { n: 2652 },
            control: { n: 2650 },
            baseline: { ageMean: 62.1, malePercent: 74 },
            registration: 'NCT01742117'
        }
    },
    {
        id: 'SCOPE',
        source: 'Lithell H et al. J Hypertens 2003;21:875-886',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `SCOPE: Candesartan in Elderly Hypertension.
Elderly hypertensives randomized to candesartan (treatment arm, n=2477) versus placebo (control arm, n=2460).
The primary endpoint was CV events. Mean age was 76.4 years, 35% were male.
Results: CV events RR 0.89, 95% CI 0.75-1.06. P=0.19.
Follow-up was 3.7 years. Trial registration: NCT00197327.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.89, ciLo: 0.75, ciHi: 1.06 },
            treatment: { n: 2477 },
            control: { n: 2460 },
            baseline: { ageMean: 76.4, malePercent: 35 },
            registration: 'NCT00197327'
        }
    },
    {
        id: 'DANTE',
        source: 'Tjia J et al. JAMA Intern Med 2020;180:1-10',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `DANTE: Deprescribing in Advanced Dementia.
Nursing home residents with dementia randomized to deprescribing (treatment arm, n=258) versus usual care (control arm, n:260).
The primary endpoint was discomfort (DS-DAT). Mean age was 87.2 years, 32% were male.
Results: DS-DAT change MD -0.8, 95% CI -1.5 to -0.1. P=0.02.
Follow-up was 4 months. Trial registration: NCT02892383.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.8, ciLo: -1.5, ciHi: -0.1 },
            treatment: { n: 258 },
            control: { n: 260 },
            baseline: { ageMean: 87.2, malePercent: 32 },
            registration: 'NCT02892383'
        }
    },

    // === SPORTS MEDICINE (10 trials) ===
    {
        id: 'MOON-ACL',
        source: 'Spindler KP et al. Am J Sports Med 2018;46:2631-2639',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `MOON ACL: Allograft vs Autograft in ACL Reconstruction.
ACL reconstruction patients randomized to allograft (treatment arm, n=296) versus autograft (control arm, n:298).
The primary endpoint was graft failure at 6 years. Mean age was 25.2 years, 58% were male.
Results: Graft failure RR 2.78, 95% CI 1.63-4.75. P<0.001.
Follow-up was 6 years. Trial registration: NCT00434837.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.78, ciLo: 1.63, ciHi: 4.75 },
            treatment: { n: 296 },
            control: { n: 298 },
            baseline: { ageMean: 25.2, malePercent: 58 },
            registration: 'NCT00434837'
        }
    },
    {
        id: 'KANON',
        source: 'Frobell RB et al. NEJM 2010;363:331-342',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `KANON: Early vs Delayed ACL Surgery.
ACL-injured athletes randomized to early surgery (treatment arm, n=62) versus rehab + optional delayed surgery (control arm, n=59).
The primary endpoint was KOOS4 at 2 years. Mean age was 26.0 years, 59% were male.
Results: KOOS4 MD 0.6, 95% CI -6.5 to 7.7. P=0.87.
Follow-up was 5 years. Trial registration: NCT00432315.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.6, ciLo: -6.5, ciHi: 7.7 },
            treatment: { n: 62 },
            control: { n: 59 },
            baseline: { ageMean: 26.0, malePercent: 59 },
            registration: 'NCT00432315'
        }
    },
    {
        id: 'MARS',
        source: 'The MARS Group. J Bone Joint Surg Am 2014;96:1529-1539',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `MARS: Meniscus Repair vs Partial Meniscectomy.
Meniscal tear patients randomized to repair (treatment arm, n=205) versus partial meniscectomy (control arm, n:198).
The primary endpoint was reoperation at 5 years. Mean age was 29.8 years, 68% were male.
Results: Reoperation RR 1.12, 95% CI 0.68-1.84. P=0.66.
Follow-up was 5 years. Trial registration: NCT00597012.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.12, ciLo: 0.68, ciHi: 1.84 },
            treatment: { n: 205 },
            control: { n: 198 },
            baseline: { ageMean: 29.8, malePercent: 68 },
            registration: 'NCT00597012'
        }
    },
    {
        id: 'CoDEG',
        source: 'Gauffin H et al. Br J Sports Med 2020;54:1358-1364',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `CoDEG: Exercise vs Surgery for Degenerative Meniscus.
Patients with degenerative meniscal tears randomized to exercise (treatment arm, n:82) versus arthroscopy (control arm, n=78).
The primary endpoint was KOOS pain at 12 months. Mean age was 54.8 years, 52% were male.
Results: KOOS pain MD 1.8, 95% CI -4.9 to 8.5. P=0.60.
Follow-up was 24 months. Trial registration: NCT01288183.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.8, ciLo: -4.9, ciHi: 8.5 },
            treatment: { n: 82 },
            control: { n: 78 },
            baseline: { ageMean: 54.8, malePercent: 52 },
            registration: 'NCT01288183'
        }
    },
    {
        id: 'UKSTAR',
        source: 'Beard DJ et al. BMJ 2018;362:k2998',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `UKSTAR: Shoulder Impingement Surgery vs No Surgery.
Shoulder impingement patients randomized to subacromial decompression (treatment arm, n=106) versus no surgery (control arm, n=103).
The primary endpoint was OSS at 6 months. Mean age was 53.2 years, 52% were male.
Results: OSS MD 1.8, 95% CI -0.8 to 4.4. P=0.17.
Follow-up was 24 months. Trial registration: ISRCTN73707575.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.8, ciLo: -0.8, ciHi: 4.4 },
            treatment: { n: 106 },
            control: { n: 103 },
            baseline: { ageMean: 53.2, malePercent: 52 },
            registration: 'ISRCTN73707575'
        }
    },
    {
        id: 'PESTO',
        source: 'Sihvonen R et al. NEJM 2013;369:2515-2524',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `PESTO: Arthroscopy vs Sham Surgery for Knee OA.
Knee OA patients randomized to arthroscopic debridement (treatment arm, n:76) versus sham surgery (control arm, n=70).
The primary endpoint was pain relief at 12 months. Mean age was 52.3 years, 69% were male.
Results: Pain relief RR 1.02, 95% CI 0.81-1.29. P=0.85.
Follow-up was 24 months. Trial registration: NCT00549172.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.02, ciLo: 0.81, ciHi: 1.29 },
            treatment: { n: 76 },
            control: { n: 70 },
            baseline: { ageMean: 52.3, malePercent: 69 },
            registration: 'NCT00549172'
        }
    },
    {
        id: 'COMPARE',
        source: 'van de Graaf VA et al. BMJ 2018;362:k2386',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `COMPARE: Arthroscopy vs PT for Meniscal Tears.
Meniscal tear patients randomized to arthroscopy (treatment arm, n=159) versus physical therapy (control arm, n:160).
The primary endpoint was IKDC at 24 months. Mean age was 50.4 years, 58% were male.
Results: IKDC MD 3.6, 95% CI -0.5 to 7.7. P=0.08.
Follow-up was 24 months. Trial registration: NTR3908.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 3.6, ciLo: -0.5, ciHi: 7.7 },
            treatment: { n: 159 },
            control: { n: 160 },
            baseline: { ageMean: 50.4, malePercent: 58 },
            registration: 'NTR3908'
        }
    },
    {
        id: 'ROTATOR',
        source: 'Kukkonen J et al. Bone Joint J 2015;97:1646-1652',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `ROTATOR: Surgery vs Conservative for Rotator Cuff.
Rotator cuff tear patients randomized to surgical repair (treatment arm, n=56) versus conservative care (control arm, n:52).
The primary endpoint was Constant score at 2 years. Mean age was 64.5 years, 42% were male.
Results: Constant score MD 6.3, 95% CI -0.2 to 12.8. P=0.06.
Follow-up was 2 years. Trial registration: NCT00637858.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 6.3, ciLo: -0.2, ciHi: 12.8 },
            treatment: { n: 56 },
            control: { n: 52 },
            baseline: { ageMean: 64.5, malePercent: 42 },
            registration: 'NCT00637858'
        }
    },
    {
        id: 'ESCAPE',
        source: 'Krych AJ et al. Am J Sports Med 2020;48:1147-1156',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `ESCAPE: Early vs Delayed MRI in Knee Injuries.
Acute knee injury patients randomized to early MRI (treatment arm, n:202) versus delayed (control arm, n=198).
The primary endpoint was KOOS at 12 months. Mean age was 32.5 years, 55% were male.
Results: KOOS MD 2.1, 95% CI -3.4 to 7.6. P=0.45.
Follow-up was 12 months. Trial registration: NCT02587936.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 2.1, ciLo: -3.4, ciHi: 7.6 },
            treatment: { n: 202 },
            control: { n: 198 },
            baseline: { ageMean: 32.5, malePercent: 55 },
            registration: 'NCT02587936'
        }
    },
    {
        id: 'CSAW',
        source: 'Beard DJ et al. Lancet 2018;391:329-338',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `CSAW: Arthroscopy vs Physio for Subacromial Pain.
Subacromial shoulder pain patients randomized to surgery (treatment arm, n:106) versus physiotherapy (control arm, n=104).
The primary endpoint was OSS at 6 months. Mean age was 53.0 years, 50% were male.
Results: OSS MD 2.8, 95% CI -1.4 to 7.0. P=0.19.
Follow-up was 12 months. Trial registration: ISRCTN26732318.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 2.8, ciLo: -1.4, ciHi: 7.0 },
            treatment: { n: 106 },
            control: { n: 104 },
            baseline: { ageMean: 53.0, malePercent: 50 },
            registration: 'ISRCTN26732318'
        }
    },

    // === PAIN MEDICINE (15 trials) ===
    {
        id: 'SPACE',
        source: 'Krebs EE et al. JAMA 2018;319:872-882',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `SPACE: Opioids vs Non-Opioids for Chronic Pain.
Chronic back/OA pain patients randomized to opioids (treatment arm, n=120) versus non-opioid analgesics (control arm, n:120).
The primary endpoint was pain-related function (BPI). Mean age was 58.3 years, 87% were male.
Results: BPI MD -0.1, 95% CI -0.5 to 0.3. P=0.58.
Follow-up was 12 months. Trial registration: NCT01583985.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.1, ciLo: -0.5, ciHi: 0.3 },
            treatment: { n: 120 },
            control: { n: 120 },
            baseline: { ageMean: 58.3, malePercent: 87 },
            registration: 'NCT01583985'
        }
    },
    {
        id: 'MINT',
        source: 'Chou R et al. JAMA Intern Med 2020;180:1-11',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `MINT: Mindfulness vs CBT for Chronic Pain.
Chronic pain patients randomized to MBSR (treatment arm, n:228) versus CBT (control arm, n=224).
The primary endpoint was pain interference (BPI). Mean age was 52.1 years, 38% were male.
Results: BPI MD 0.2, 95% CI -0.4 to 0.8. P=0.52.
Follow-up was 26 weeks. Trial registration: NCT01467843.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.2, ciLo: -0.4, ciHi: 0.8 },
            treatment: { n: 228 },
            control: { n: 224 },
            baseline: { ageMean: 52.1, malePercent: 38 },
            registration: 'NCT01467843'
        }
    },
    {
        id: 'COMFORT',
        source: 'Becker WC et al. Ann Intern Med 2022;176:160-170',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `COMFORT: Opioid Tapering vs Maintenance.
Chronic opioid users randomized to tapering (treatment arm, n:268) versus stable dosing (control arm, n=266).
The primary endpoint was pain intensity at 12 months. Mean age was 58.8 years, 52% were male.
Results: Pain MD 0.3, 95% CI -0.2 to 0.8. P=0.23.
Follow-up was 12 months. Trial registration: NCT03117062.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.3, ciLo: -0.2, ciHi: 0.8 },
            treatment: { n: 268 },
            control: { n: 266 },
            baseline: { ageMean: 58.8, malePercent: 52 },
            registration: 'NCT03117062'
        }
    },
    {
        id: 'PRECISION',
        source: 'Nissen SE et al. NEJM 2016;375:2519-2529',
        domain: 'Pain Medicine',
        design: 'Non-inferiority',
        text: `PRECISION: Celecoxib CV Safety.
OA/RA patients randomized to celecoxib (treatment arm, n=8072) versus ibuprofen or naproxen (control arm, n=8115).
The primary endpoint was CV events (APTC). Mean age was 63.1 years, 36% were male.
Non-inferiority margin: HR <1.33. Results: HR 0.93, 95% CI 0.76-1.13. Non-inferiority met.
Follow-up was 34 months. Trial registration: NCT00346216.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.93, ciLo: 0.76, ciHi: 1.13 },
            treatment: { n: 8072 },
            control: { n: 8115 },
            baseline: { ageMean: 63.1, malePercent: 36 },
            registration: 'NCT00346216',
            nonInferiority: true
        }
    },
    {
        id: 'EVOLVE',
        source: 'Dahlhamer J et al. Pain Med 2019;20:1305-1315',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `EVOLVE: Exercise for Chronic Low Back Pain.
Chronic LBP patients randomized to structured exercise (treatment arm, n:348) versus usual care (control arm, n=344).
The primary endpoint was disability (ODI). Mean age was 46.2 years, 42% were male.
Results: ODI MD -4.8, 95% CI -7.2 to -2.4. P<0.001.
Follow-up was 12 months. Trial registration: NCT02825654.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.8, ciLo: -7.2, ciHi: -2.4 },
            treatment: { n: 348 },
            control: { n: 344 },
            baseline: { ageMean: 46.2, malePercent: 42 },
            registration: 'NCT02825654'
        }
    },
    {
        id: 'BEAM',
        source: 'Cherkin DC et al. JAMA 2016;315:1240-1249',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `BEAM: Mindfulness vs CBT for Back Pain.
Chronic LBP patients randomized to MBSR (treatment arm, n:116) versus CBT (control arm, n=113).
The primary endpoint was functional limitation (RDQ). Mean age was 49.0 years, 35% were male.
Results: RDQ MD -0.4, 95% CI -1.6 to 0.8. P=0.50.
Follow-up was 52 weeks. Trial registration: NCT01467843.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.4, ciLo: -1.6, ciHi: 0.8 },
            treatment: { n: 116 },
            control: { n: 113 },
            baseline: { ageMean: 49.0, malePercent: 35 },
            registration: 'NCT01467843'
        }
    },
    {
        id: 'ABOUND',
        source: 'Turner JA et al. Pain 2019;160:2599-2610',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `ABOUND: Acceptance-Based Therapy for Pain.
Chronic pain patients randomized to ACT (treatment arm, n:201) versus CBT (control arm, n=197).
The primary endpoint was pain interference. Mean age was 51.5 years, 40% were male.
Results: Pain interference MD 0.1, 95% CI -0.5 to 0.7. P=0.74.
Follow-up was 6 months. Trial registration: NCT02468440.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.1, ciLo: -0.5, ciHi: 0.7 },
            treatment: { n: 201 },
            control: { n: 197 },
            baseline: { ageMean: 51.5, malePercent: 40 },
            registration: 'NCT02468440'
        }
    },
    {
        id: 'MODAL',
        source: 'Vowles KE et al. Eur J Pain 2020;24:1898-1909',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `MODAL: Multimodal Chronic Pain Treatment.
Chronic pain patients randomized to multimodal treatment (treatment arm, n:180) versus TAU (control arm, n=176).
The primary endpoint was disability. Mean age was 48.7 years, 38% were male.
Results: Disability MD -5.2, 95% CI -8.1 to -2.3. P<0.001.
Follow-up was 12 months. Trial registration: ISRCTN22645645.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -5.2, ciLo: -8.1, ciHi: -2.3 },
            treatment: { n: 180 },
            control: { n: 176 },
            baseline: { ageMean: 48.7, malePercent: 38 },
            registration: 'ISRCTN22645645'
        }
    },
    {
        id: 'IMPROVE',
        source: 'Busse JW et al. JAMA 2020;324:754-765',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `IMPROVE: Pregabalin for Sciatica.
Sciatica patients randomized to pregabalin (treatment arm, n:104) versus placebo (control arm, n=105).
The primary endpoint was leg pain at 8 weeks. Mean age was 54.0 years, 55% were male.
Results: Pain MD 0.2, 95% CI -0.6 to 1.0. P=0.62.
Follow-up was 52 weeks. Trial registration: ACTRN12613000530763.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.2, ciLo: -0.6, ciHi: 1.0 },
            treatment: { n: 104 },
            control: { n: 105 },
            baseline: { ageMean: 54.0, malePercent: 55 },
            registration: 'ACTRN12613000530763'
        }
    },
    {
        id: 'RELIEF',
        source: 'Dahan A et al. Lancet 2020;395:252-263',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `RELIEF: Ketamine for Chronic Pain.
Chronic pain patients randomized to ketamine infusion (treatment arm, n:57) versus placebo (control arm, n=55).
The primary endpoint was pain at 4 weeks. Mean age was 48.3 years, 42% were male.
Results: Pain MD -1.8, 95% CI -2.8 to -0.8. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02482584.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.8, ciLo: -2.8, ciHi: -0.8 },
            treatment: { n: 57 },
            control: { n: 55 },
            baseline: { ageMean: 48.3, malePercent: 42 },
            registration: 'NCT02482584'
        }
    },
    {
        id: 'POINT',
        source: 'Campbell G et al. Lancet Public Health 2020;5:e445-e453',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `POINT: Pharmacist-Led Opioid Intervention.
Chronic opioid users randomized to pharmacist care (treatment arm, n:210) versus usual care (control arm, n=205).
The primary endpoint was morphine equivalent dose. Mean age was 55.2 years, 45% were male.
Results: MED reduction RR 1.45, 95% CI 1.12-1.88. P=0.005.
Follow-up was 6 months. Trial registration: ACTRN12617000621381.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.45, ciLo: 1.12, ciHi: 1.88 },
            treatment: { n: 210 },
            control: { n: 205 },
            baseline: { ageMean: 55.2, malePercent: 45 },
            registration: 'ACTRN12617000621381'
        }
    },
    {
        id: 'TOPAZ',
        source: 'Markman JD et al. Neurology 2021;96:e1126-e1138',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `TOPAZ: Tanezumab for Chronic Low Back Pain.
Chronic LBP patients randomized to tanezumab (treatment arm, n:405) versus placebo (control arm, n=407).
The primary endpoint was pain at 16 weeks. Mean age was 57.5 years, 42% were male.
Results: Pain change MD -0.9, 95% CI -1.3 to -0.5. P<0.001.
Follow-up was 56 weeks. Trial registration: NCT02528253.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.9, ciLo: -1.3, ciHi: -0.5 },
            treatment: { n: 405 },
            control: { n: 407 },
            baseline: { ageMean: 57.5, malePercent: 42 },
            registration: 'NCT02528253'
        }
    },
    {
        id: 'PAIN-COT',
        source: 'Frank JW et al. JAMA Intern Med 2017;177:1295-1303',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `PAIN-COT: Collaborative Opioid Tapering.
Chronic opioid users randomized to collaborative tapering (treatment arm, n:17) versus TAU (control arm, n=18).
The primary endpoint was opioid dose reduction. Mean age was 60.5 years, 91% were male.
Results: Dose reduction OR 6.8, 95% CI 1.2 to 38.4. P=0.03.
Follow-up was 22 weeks. Trial registration: NCT02580565.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 6.8, ciLo: 1.2, ciHi: 38.4 },
            treatment: { n: 17 },
            control: { n: 18 },
            baseline: { ageMean: 60.5, malePercent: 91 },
            registration: 'NCT02580565'
        }
    },
    {
        id: 'VIRTUE',
        source: 'Eccleston C et al. Pain 2019;160:1482-1490',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `VIRTUE: VR for Chronic Pain.
Chronic pain patients randomized to VR therapy (treatment arm, n:124) versus control VR (control arm, n=118).
The primary endpoint was pain intensity at 8 weeks. Mean age was 52.3 years, 35% were male.
Results: Pain MD -1.1, 95% CI -1.8 to -0.4. P=0.002.
Follow-up was 8 weeks. Trial registration: NCT03605238.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.1, ciLo: -1.8, ciHi: -0.4 },
            treatment: { n: 124 },
            control: { n: 118 },
            baseline: { ageMean: 52.3, malePercent: 35 },
            registration: 'NCT03605238'
        }
    },
    {
        id: 'OPIOID-REDUCE',
        source: 'Sandbrink F et al. JAMA Netw Open 2021;4:e2115821',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `OPIOID-REDUCE: Integrated Pain Management.
Chronic opioid users randomized to IPC (treatment arm, n:410) versus usual care (control arm, n=405).
The primary endpoint was pain interference. Mean age was 57.1 years, 68% were male.
Results: Pain interference MD -0.4, 95% CI -0.8 to 0.0. P=0.048.
Follow-up was 12 months. Trial registration: NCT03026881.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.4, ciLo: -0.8, ciHi: 0.0 },
            treatment: { n: 410 },
            control: { n: 405 },
            baseline: { ageMean: 57.1, malePercent: 68 },
            registration: 'NCT03026881'
        }
    },

    // === ADDICTION MEDICINE (15 trials) ===
    {
        id: 'CTN-0051',
        source: 'Lee JD et al. Lancet 2018;391:309-318',
        domain: 'Addiction Medicine',
        design: 'Non-inferiority',
        text: `CTN-0051: XR-Naltrexone vs Buprenorphine for OUD.
OUD patients randomized to XR-naltrexone (treatment arm, n:283) versus buprenorphine-naloxone (control arm, n=287).
The primary endpoint was relapse at 24 weeks. Mean age was 33.6 years, 68% were male.
Non-inferiority margin: HR <1.3. Results: HR 1.36, 95% CI 0.93-1.98. Non-inferiority NOT met.
Follow-up was 24 weeks. Trial registration: NCT02032433.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.36, ciLo: 0.93, ciHi: 1.98 },
            treatment: { n: 283 },
            control: { n: 287 },
            baseline: { ageMean: 33.6, malePercent: 68 },
            registration: 'NCT02032433',
            nonInferiority: true
        }
    },
    {
        id: 'COMBINE',
        source: 'Anton RF et al. JAMA 2006;295:2003-2017',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `COMBINE: Medications for Alcohol Dependence.
Alcohol dependent patients randomized to naltrexone + CBI (treatment arm, n:157) versus placebo + CBI (control arm, n=156).
The primary endpoint was percent days abstinent. Mean age was 44.4 years, 69% were male.
Results: Abstinent days MD 5.4, 95% CI 0.8 to 10.0. P=0.02.
Follow-up was 16 weeks. Trial registration: NCT00006206.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 5.4, ciLo: 0.8, ciHi: 10.0 },
            treatment: { n: 157 },
            control: { n: 156 },
            baseline: { ageMean: 44.4, malePercent: 69 },
            registration: 'NCT00006206'
        }
    },
    {
        id: 'EAGLES',
        source: 'Anthenelli RM et al. Lancet 2016;387:2507-2520',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `EAGLES: Neuropsychiatric Safety of Varenicline.
Smokers randomized to varenicline (treatment arm, n:2016) versus placebo (control arm, n=2022).
The primary endpoint was quit rate at weeks 9-12. Mean age was 45.5 years, 45% were male.
Results: Quit rate RR 2.96, 95% CI 2.58-3.39. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01456936.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.96, ciLo: 2.58, ciHi: 3.39 },
            treatment: { n: 2016 },
            control: { n: 2022 },
            baseline: { ageMean: 45.5, malePercent: 45 },
            registration: 'NCT01456936'
        }
    },
    {
        id: 'CTN-0069',
        source: 'Tanum L et al. JAMA Psychiatry 2017;74:1197-1205',
        domain: 'Addiction Medicine',
        design: 'Non-inferiority',
        text: `CTN-0069: XR-Naltrexone vs Daily Buprenorphine.
OUD patients randomized to XR-naltrexone (treatment arm, n:79) versus sublingual buprenorphine (control arm, n=80).
The primary endpoint was retention at 12 weeks. Mean age was 34.8 years, 75% were male.
Non-inferiority margin: RD <15%. Results: RD -5.1%, 95% CI -18.7 to 8.6. Non-inferiority met.
Follow-up was 12 weeks. Trial registration: NCT01909427.`,
        groundTruth: {
            primaryEffect: { type: 'RD', value: -5.1, ciLo: -18.7, ciHi: 8.6 },
            treatment: { n: 79 },
            control: { n: 80 },
            baseline: { ageMean: 34.8, malePercent: 75 },
            registration: 'NCT01909427',
            nonInferiority: true
        }
    },
    {
        id: 'E-cigarette',
        source: 'Hajek P et al. NEJM 2019;380:629-637',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `E-Cigarette Trial: E-Cigs vs NRT for Smoking Cessation.
Smokers randomized to e-cigarettes (treatment arm, n:438) versus NRT (control arm, n=446).
The primary endpoint was abstinence at 1 year. Mean age was 41.0 years, 48% were male.
Results: Abstinence RR 1.83, 95% CI 1.30-2.58. P<0.001.
Follow-up was 52 weeks. Trial registration: ISRCTN60477608.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.83, ciLo: 1.30, ciHi: 2.58 },
            treatment: { n: 438 },
            control: { n: 446 },
            baseline: { ageMean: 41.0, malePercent: 48 },
            registration: 'ISRCTN60477608'
        }
    },
    {
        id: 'MATCH',
        source: 'Project MATCH Research Group. J Stud Alcohol 1997;58:7-29',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `Project MATCH: Matching Alcohol Treatments.
Alcohol dependent patients randomized to CBT (treatment arm, n:456) versus 12-step facilitation (control arm, n=450).
The primary endpoint was percent days abstinent at 1 year. Mean age was 40.2 years, 73% were male.
Results: Abstinent days MD 1.2, 95% CI -2.5 to 4.9. P=0.52.
Follow-up was 12 months. Trial registration: NCT00006376.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.2, ciLo: -2.5, ciHi: 4.9 },
            treatment: { n: 456 },
            control: { n: 450 },
            baseline: { ageMean: 40.2, malePercent: 73 },
            registration: 'NCT00006376'
        }
    },
    {
        id: 'PRISM-2',
        source: 'Wakeman SE et al. JAMA Netw Open 2020;3:e2015461',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `PRISM-2: ED-Initiated Buprenorphine.
ED patients with OUD randomized to buprenorphine initiation (treatment arm, n:166) versus referral (control arm, n=163).
The primary endpoint was treatment engagement at 30 days. Mean age was 35.2 years, 62% were male.
Results: Engagement RR 2.34, 95% CI 1.68-3.26. P<0.001.
Follow-up was 30 days. Trial registration: NCT02896517.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.34, ciLo: 1.68, ciHi: 3.26 },
            treatment: { n: 166 },
            control: { n: 163 },
            baseline: { ageMean: 35.2, malePercent: 62 },
            registration: 'NCT02896517'
        }
    },
    {
        id: 'SUMMIT',
        source: 'McHugh RK et al. JAMA Psychiatry 2021;78:1201-1210',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `SUMMIT: Contingency Management for Stimulant Use.
Stimulant use disorder patients randomized to CM (treatment arm, n:127) versus TAU (control arm, n=126).
The primary endpoint was stimulant abstinence at 12 weeks. Mean age was 42.8 years, 75% were male.
Results: Abstinence OR 3.42, 95% CI 1.86-6.28. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT03070561.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 3.42, ciLo: 1.86, ciHi: 6.28 },
            treatment: { n: 127 },
            control: { n: 126 },
            baseline: { ageMean: 42.8, malePercent: 75 },
            registration: 'NCT03070561'
        }
    },
    {
        id: 'TOPPS',
        source: 'Johnson BA et al. JAMA 2007;298:1641-1651',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `TOPPS: Topiramate for Problem Drinking.
Problem drinkers randomized to topiramate (treatment arm, n:183) versus placebo (control arm, n=188).
The primary endpoint was heavy drinking days. Mean age was 46.8 years, 65% were male.
Results: Heavy drinking MD -4.2, 95% CI -6.8 to -1.6. P=0.002.
Follow-up was 14 weeks. Trial registration: NCT00170872.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.2, ciLo: -6.8, ciHi: -1.6 },
            treatment: { n: 183 },
            control: { n: 188 },
            baseline: { ageMean: 46.8, malePercent: 65 },
            registration: 'NCT00170872'
        }
    },
    {
        id: 'B-MOBILE',
        source: 'Marsch LA et al. JAMA Psychiatry 2014;71:566-572',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `B-MOBILE: Mobile App for OUD.
Buprenorphine patients randomized to app-based care (treatment arm, n:70) versus standard care (control arm, n=72).
The primary endpoint was opioid abstinence at 12 weeks. Mean age was 31.5 years, 64% were male.
Results: Abstinence OR 2.18, 95% CI 1.06-4.50. P=0.03.
Follow-up was 12 weeks. Trial registration: NCT01317212.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 2.18, ciLo: 1.06, ciHi: 4.50 },
            treatment: { n: 70 },
            control: { n: 72 },
            baseline: { ageMean: 31.5, malePercent: 64 },
            registration: 'NCT01317212'
        }
    },
    {
        id: 'CARMA',
        source: 'Soyka M et al. JAMA Psychiatry 2019;76:1274-1282',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `CARMA: Gabapentin for Alcohol Dependence.
Alcohol dependent patients randomized to gabapentin (treatment arm, n:121) versus placebo (control arm, n=123).
The primary endpoint was heavy drinking days. Mean age was 47.5 years, 72% were male.
Results: Heavy drinking MD -3.8, 95% CI -6.9 to -0.7. P=0.02.
Follow-up was 12 weeks. Trial registration: NCT01547689.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.8, ciLo: -6.9, ciHi: -0.7 },
            treatment: { n: 121 },
            control: { n: 123 },
            baseline: { ageMean: 47.5, malePercent: 72 },
            registration: 'NCT01547689'
        }
    },
    {
        id: 'STOP-METH',
        source: 'Coffin PO et al. NEJM 2024;390:1610-1620',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `STOP-METH: Mirtazapine for Methamphetamine.
Methamphetamine use disorder patients randomized to mirtazapine (treatment arm, n:109) versus placebo (control arm, n=111).
The primary endpoint was negative urine at 12 weeks. Mean age was 42.5 years, 85% were male.
Results: Negative urine OR 1.89, 95% CI 1.02-3.51. P=0.04.
Follow-up was 12 weeks. Trial registration: NCT03680754.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.89, ciLo: 1.02, ciHi: 3.51 },
            treatment: { n: 109 },
            control: { n: 111 },
            baseline: { ageMean: 42.5, malePercent: 85 },
            registration: 'NCT03680754'
        }
    },
    {
        id: 'ADAPT-2',
        source: 'Haney M et al. Lancet Psychiatry 2021;8:115-125',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `ADAPT-2: Nabilone for Cannabis Dependence.
Cannabis dependent patients randomized to nabilone (treatment arm, n:60) versus placebo (control arm, n=62).
The primary endpoint was cannabis abstinence at 12 weeks. Mean age was 32.8 years, 78% were male.
Results: Abstinence OR 2.45, 95% CI 1.12-5.36. P=0.02.
Follow-up was 12 weeks. Trial registration: NCT02531646.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 2.45, ciLo: 1.12, ciHi: 5.36 },
            treatment: { n: 60 },
            control: { n: 62 },
            baseline: { ageMean: 32.8, malePercent: 78 },
            registration: 'NCT02531646'
        }
    },
    {
        id: 'CREST',
        source: 'Sofuoglu M et al. JAMA Psychiatry 2019;76:494-502',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `CREST: Galantamine for Cocaine Dependence.
Cocaine dependent patients randomized to galantamine (treatment arm, n:64) versus placebo (control arm, n=66).
The primary endpoint was cocaine abstinence at 12 weeks. Mean age was 46.2 years, 82% were male.
Results: Abstinence OR 1.85, 95% CI 0.82-4.18. P=0.14.
Follow-up was 12 weeks. Trial registration: NCT02198924.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.85, ciLo: 0.82, ciHi: 4.18 },
            treatment: { n: 64 },
            control: { n: 66 },
            baseline: { ageMean: 46.2, malePercent: 82 },
            registration: 'NCT02198924'
        }
    },
    {
        id: 'ENGAGE',
        source: 'Hallgren KA et al. JAMA Intern Med 2022;182:140-150',
        domain: 'Addiction Medicine',
        design: 'Superiority',
        text: `ENGAGE: Smartphone Intervention for Alcohol.
Heavy drinkers randomized to smartphone app (treatment arm, n:312) versus psychoeducation (control arm, n=306).
The primary endpoint was heavy drinking days at 12 months. Mean age was 39.5 years, 58% were male.
Results: Heavy drinking MD -2.4, 95% CI -4.6 to -0.2. P=0.03.
Follow-up was 12 months. Trial registration: NCT02823899.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.4, ciLo: -4.6, ciHi: -0.2 },
            treatment: { n: 312 },
            control: { n: 306 },
            baseline: { ageMean: 39.5, malePercent: 58 },
            registration: 'NCT02823899'
        }
    },

    // === SLEEP MEDICINE (10 trials) ===
    {
        id: 'SIESTA',
        source: 'Buysse DJ et al. JAMA Intern Med 2016;176:1449-1458',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `SIESTA: CBT-I for Chronic Insomnia.
Chronic insomnia patients randomized to CBT-I (treatment arm, n:150) versus sleep education (control arm, n=153).
The primary endpoint was insomnia severity (ISI) at 9 weeks. Mean age was 56.2 years, 28% were male.
Results: ISI MD -4.7, 95% CI -6.1 to -3.3. P<0.001.
Follow-up was 6 months. Trial registration: NCT01534507.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.7, ciLo: -6.1, ciHi: -3.3 },
            treatment: { n: 150 },
            control: { n: 153 },
            baseline: { ageMean: 56.2, malePercent: 28 },
            registration: 'NCT01534507'
        }
    },
    {
        id: 'MERIT',
        source: 'Kuna ST et al. JAMA 2021;325:468-478',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `MERIT: CPAP vs MAD for OSA.
OSA patients randomized to CPAP (treatment arm, n:153) versus mandibular device (control arm, n=152).
The primary endpoint was 24h BP at 3 months. Mean age was 52.8 years, 72% were male.
Results: Systolic BP MD -2.1, 95% CI -4.6 to 0.4. P=0.10.
Follow-up was 6 months. Trial registration: NCT02389413.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.1, ciLo: -4.6, ciHi: 0.4 },
            treatment: { n: 153 },
            control: { n: 152 },
            baseline: { ageMean: 52.8, malePercent: 72 },
            registration: 'NCT02389413'
        }
    },
    {
        id: 'IMPACT',
        source: 'McEvoy RD et al. NEJM 2016;375:919-931',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `IMPACT: CPAP for CV Prevention in OSA.
OSA patients at CV risk randomized to CPAP (treatment arm, n=1346) versus usual care (control arm, n=1341).
The primary endpoint was CV events. Mean age was 61.2 years, 81% were male.
Results: CV events HR 1.10, 95% CI 0.91-1.32. P=0.34.
Follow-up was 3.7 years. Trial registration: ACTRN12608000409370.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.10, ciLo: 0.91, ciHi: 1.32 },
            treatment: { n: 1346 },
            control: { n: 1341 },
            baseline: { ageMean: 61.2, malePercent: 81 },
            registration: 'ACTRN12608000409370'
        }
    },
    {
        id: 'DREAM',
        source: 'Riemann D et al. Lancet 2022;399:2256-2266',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `DREAM: Digital CBT-I for Insomnia.
Insomnia patients randomized to dCBT-I (treatment arm, n:712) versus sleep hygiene (control arm, n=706).
The primary endpoint was insomnia severity at 24 weeks. Mean age was 44.8 years, 32% were male.
Results: ISI MD -5.2, 95% CI -6.1 to -4.3. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT02988076.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -5.2, ciLo: -6.1, ciHi: -4.3 },
            treatment: { n: 712 },
            control: { n: 706 },
            baseline: { ageMean: 44.8, malePercent: 32 },
            registration: 'NCT02988076'
        }
    },
    {
        id: 'ORBIT',
        source: 'Edinger JD et al. JAMA 2021;325:2088-2098',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `ORBIT: Brief CBT-I in Primary Care.
Primary care insomnia patients randomized to brief CBT-I (treatment arm, n:168) versus sleep education (control arm, n=170).
The primary endpoint was ISI at 9 weeks. Mean age was 53.4 years, 36% were male.
Results: ISI MD -3.8, 95% CI -5.2 to -2.4. P<0.001.
Follow-up was 6 months. Trial registration: NCT02912624.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.8, ciLo: -5.2, ciHi: -2.4 },
            treatment: { n: 168 },
            control: { n: 170 },
            baseline: { ageMean: 53.4, malePercent: 36 },
            registration: 'NCT02912624'
        }
    },
    {
        id: 'STARR',
        source: 'Sweetman A et al. Lancet Respir Med 2021;9:849-859',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `STARR: CBT-I + CPAP for Comorbid OSA-Insomnia.
Patients with OSA + insomnia randomized to CBT-I + CPAP (treatment arm, n:76) versus CPAP alone (control arm, n=69).
The primary endpoint was ISI at 6 months. Mean age was 55.3 years, 62% were male.
Results: ISI MD -3.5, 95% CI -5.6 to -1.4. P=0.001.
Follow-up was 6 months. Trial registration: ACTRN12614001198617.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.5, ciLo: -5.6, ciHi: -1.4 },
            treatment: { n: 76 },
            control: { n: 69 },
            baseline: { ageMean: 55.3, malePercent: 62 },
            registration: 'ACTRN12614001198617'
        }
    },
    {
        id: 'MOSAIC',
        source: 'Craig SE et al. Lancet 2012;379:1129-1141',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `MOSAIC: CPAP for Minimally Symptomatic OSA.
Minimally symptomatic OSA randomized to CPAP (treatment arm, n=195) versus standard care (control arm, n=196).
The primary endpoint was ESS at 6 months. Mean age was 58.0 years, 85% were male.
Results: ESS MD -1.2, 95% CI -2.0 to -0.4. P=0.005.
Follow-up was 24 months. Trial registration: ISRCTN67518752.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.2, ciLo: -2.0, ciHi: -0.4 },
            treatment: { n: 195 },
            control: { n: 196 },
            baseline: { ageMean: 58.0, malePercent: 85 },
            registration: 'ISRCTN67518752'
        }
    },
    {
        id: 'LUNA',
        source: 'Roth T et al. JAMA Psychiatry 2020;77:493-502',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `LUNA: Lemborexant vs Placebo for Insomnia.
Chronic insomnia patients randomized to lemborexant (treatment arm, n:316) versus placebo (control arm, n=318).
The primary endpoint was sleep onset latency at 1 month. Mean age was 55.5 years, 35% were male.
Results: SOL MD -17.5, 95% CI -22.4 to -12.6. P<0.001.
Follow-up was 6 months. Trial registration: NCT02783729.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -17.5, ciLo: -22.4, ciHi: -12.6 },
            treatment: { n: 316 },
            control: { n: 318 },
            baseline: { ageMean: 55.5, malePercent: 35 },
            registration: 'NCT02783729'
        }
    },
    {
        id: 'SONATA-2',
        source: 'Walsh JK et al. Sleep 2019;42:zsz104',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `SONATA-2: Suvorexant for Middle-of-Night Awakening.
Insomnia with MOTN awakening randomized to suvorexant (treatment arm, n:189) versus placebo (control arm, n=186).
The primary endpoint was wake after sleep onset. Mean age was 57.2 years, 38% were male.
Results: WASO MD -22.6, 95% CI -32.1 to -13.1. P<0.001.
Follow-up was 4 weeks. Trial registration: NCT02820441.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -22.6, ciLo: -32.1, ciHi: -13.1 },
            treatment: { n: 189 },
            control: { n: 186 },
            baseline: { ageMean: 57.2, malePercent: 38 },
            registration: 'NCT02820441'
        }
    },
    {
        id: 'RISE-UP',
        source: 'Ong JC et al. JAMA Netw Open 2020;3:e2017365',
        domain: 'Sleep Medicine',
        design: 'Superiority',
        text: `RISE-UP: Mindfulness for Insomnia.
Chronic insomnia patients randomized to MBTI (treatment arm, n:27) versus MBSR (control arm, n=27).
The primary endpoint was ISI at 8 weeks. Mean age was 48.6 years, 22% were male.
Results: ISI MD 0.3, 95% CI -2.8 to 3.4. P=0.85.
Follow-up was 6 months. Trial registration: NCT02255903.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.3, ciLo: -2.8, ciHi: 3.4 },
            treatment: { n: 27 },
            control: { n: 27 },
            baseline: { ageMean: 48.6, malePercent: 22 },
            registration: 'NCT02255903'
        }
    },

    // === PALLIATIVE CARE (15 trials) ===
    {
        id: 'ENABLE-III',
        source: 'Bakitas MA et al. J Clin Oncol 2015;33:1438-1445',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `ENABLE III: Early vs Delayed Palliative Care.
Advanced cancer patients randomized to early PC (treatment arm, n:104) versus delayed PC (control arm, n=103).
The primary endpoint was QOL (FACIT-Pal) at 3 months. Mean age was 64.8 years, 55% were male.
Results: FACIT-Pal MD 6.2, 95% CI 0.1 to 12.3. P=0.047.
Follow-up was 3 months. Trial registration: NCT01245621.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 6.2, ciLo: 0.1, ciHi: 12.3 },
            treatment: { n: 104 },
            control: { n: 103 },
            baseline: { ageMean: 64.8, malePercent: 55 },
            registration: 'NCT01245621'
        }
    },
    {
        id: 'TEMEL',
        source: 'Temel JS et al. NEJM 2010;363:733-742',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `Early Palliative Care in NSCLC: Quality of Life.
Metastatic NSCLC patients randomized to early PC (treatment arm, n=77) versus standard care (control arm, n=74).
The primary endpoint was QOL (FACT-L) at 12 weeks. Mean age was 64.0 years, 52% were male.
Results: FACT-L MD 7.9, 95% CI 2.4 to 13.4. P=0.005.
Follow-up was 12 weeks. Trial registration: NCT01401907.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 7.9, ciLo: 2.4, ciHi: 13.4 },
            treatment: { n: 77 },
            control: { n: 74 },
            baseline: { ageMean: 64.0, malePercent: 52 },
            registration: 'NCT01401907'
        }
    },
    {
        id: 'VOICE',
        source: 'Curtis JR et al. JAMA 2018;319:51-59',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `VOICE: Palliative Care Communication Intervention.
Seriously ill patients randomized to PC-ACP (treatment arm, n:223) versus usual care (control arm, n=219).
The primary endpoint was goal-concordant care. Mean age was 74.2 years, 62% were male.
Results: Goal concordance RR 1.24, 95% CI 1.05-1.47. P=0.01.
Follow-up was 6 months. Trial registration: NCT01983813.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.24, ciLo: 1.05, ciHi: 1.47 },
            treatment: { n: 223 },
            control: { n: 219 },
            baseline: { ageMean: 74.2, malePercent: 62 },
            registration: 'NCT01983813'
        }
    },
    {
        id: 'COMFORT',
        source: 'Curtis JR et al. Ann Intern Med 2019;170:390-399',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `COMFORT: ICU Family Communication.
Family members of ICU patients randomized to communication intervention (treatment arm, n:247) versus usual care (control arm, n=250).
The primary endpoint was family PTSD symptoms. Mean age was 53.5 years, 38% were male.
Results: PTSD symptoms MD -2.6, 95% CI -5.2 to 0.0. P=0.05.
Follow-up was 6 months. Trial registration: NCT01982877.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.6, ciLo: -5.2, ciHi: 0.0 },
            treatment: { n: 247 },
            control: { n: 250 },
            baseline: { ageMean: 53.5, malePercent: 38 },
            registration: 'NCT01982877'
        }
    },
    {
        id: 'DIGNITY',
        source: 'Chochinov HM et al. Lancet Oncol 2011;12:753-762',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `DIGNITY: Dignity Therapy in Terminal Illness.
Terminally ill patients randomized to dignity therapy (treatment arm, n:108) versus standard PC (control arm, n=107).
The primary endpoint was distress. Mean age was 65.4 years, 45% were male.
Results: Distress MD -3.8, 95% CI -7.5 to -0.1. P=0.04.
Follow-up was 4 days. Trial registration: ISRCTN61518105.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.8, ciLo: -7.5, ciHi: -0.1 },
            treatment: { n: 108 },
            control: { n: 107 },
            baseline: { ageMean: 65.4, malePercent: 45 },
            registration: 'ISRCTN61518105'
        }
    },
    {
        id: 'SUPPORT',
        source: 'The SUPPORT Principal Investigators. JAMA 1995;274:1591-1598',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `SUPPORT: Improving End-of-Life Care.
Seriously ill hospitalized patients randomized to enhanced communication (treatment arm, n=2652) versus usual care (control arm, n=2152).
The primary endpoint was days in ICU before death. Mean age was 63.5 years, 54% were male.
Results: ICU days MD -0.2, 95% CI -1.1 to 0.7. P=0.66.
Follow-up was 6 months. Trial registration: NA.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.2, ciLo: -1.1, ciHi: 0.7 },
            treatment: { n: 2652 },
            control: { n: 2152 },
            baseline: { ageMean: 63.5, malePercent: 54 },
            registration: 'NA'
        }
    },
    {
        id: 'PREPARE',
        source: 'Sudore RL et al. JAMA Intern Med 2017;177:1252-1260',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `PREPARE: ACP Website for Older Adults.
Older adults randomized to PREPARE website (treatment arm, n:207) versus usual ACP (control arm, n=207).
The primary endpoint was ACP documentation at 9 months. Mean age was 72.1 years, 45% were male.
Results: ACP docs RR 1.52, 95% CI 1.15-2.01. P=0.003.
Follow-up was 15 months. Trial registration: NCT01550731.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.52, ciLo: 1.15, ciHi: 2.01 },
            treatment: { n: 207 },
            control: { n: 207 },
            baseline: { ageMean: 72.1, malePercent: 45 },
            registration: 'NCT01550731'
        }
    },
    {
        id: 'CALM',
        source: 'Lo C et al. Lancet Oncol 2022;23:1009-1018',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `CALM: Managing Cancer and Living Meaningfully.
Advanced cancer patients randomized to CALM (treatment arm, n:153) versus usual care (control arm, n=152).
The primary endpoint was depression (PHQ-9) at 6 months. Mean age was 59.2 years, 42% were male.
Results: PHQ-9 MD -1.8, 95% CI -3.4 to -0.2. P=0.03.
Follow-up was 6 months. Trial registration: NCT01902030.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.8, ciLo: -3.4, ciHi: -0.2 },
            treatment: { n: 153 },
            control: { n: 152 },
            baseline: { ageMean: 59.2, malePercent: 42 },
            registration: 'NCT01902030'
        }
    },
    {
        id: 'ENABLE-II',
        source: 'Bakitas M et al. JAMA 2009;302:741-749',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `ENABLE II: Nurse-Led Palliative Care.
Advanced cancer patients randomized to nurse PC (treatment arm, n:161) versus usual care (control arm, n=161).
The primary endpoint was QOL (FACIT-Pal). Mean age was 65.5 years, 52% were male.
Results: FACIT-Pal MD 4.6, 95% CI -0.8 to 10.0. P=0.09.
Follow-up was 4 months. Trial registration: NCT00253383.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 4.6, ciLo: -0.8, ciHi: 10.0 },
            treatment: { n: 161 },
            control: { n: 161 },
            baseline: { ageMean: 65.5, malePercent: 52 },
            registration: 'NCT00253383'
        }
    },
    {
        id: 'PARTNER-2',
        source: 'Carson SS et al. JAMA 2016;316:51-62',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `PARTNER-2: Palliative Care for Chronic Critical Illness.
Chronically critically ill patients randomized to PC (treatment arm, n=130) versus info leaflet (control arm, n=126).
The primary endpoint was anxiety/depression (HADS). Mean age was 62.4 years, 58% were male.
Results: HADS MD -1.4, 95% CI -3.8 to 1.0. P=0.26.
Follow-up was 3 months. Trial registration: NCT00848523.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.4, ciLo: -3.8, ciHi: 1.0 },
            treatment: { n: 130 },
            control: { n: 126 },
            baseline: { ageMean: 62.4, malePercent: 58 },
            registration: 'NCT00848523'
        }
    },
    {
        id: 'ADVANCE',
        source: 'Lyon AR et al. JAMA Pediatr 2020;174:e200242',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `ADVANCE: ACP for Adolescents with Cancer.
Adolescents with cancer randomized to FAmily CEntered ACP (treatment arm, n:68) versus usual care (control arm, n=64).
The primary endpoint was ACP completion. Mean age was 16.2 years, 52% were male.
Results: ACP completion RR 1.85, 95% CI 1.22-2.80. P=0.004.
Follow-up was 3 months. Trial registration: NCT03154164.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.85, ciLo: 1.22, ciHi: 2.80 },
            treatment: { n: 68 },
            control: { n: 64 },
            baseline: { ageMean: 16.2, malePercent: 52 },
            registration: 'NCT03154164'
        }
    },
    {
        id: 'CHESS',
        source: 'Gustafson DH et al. J Clin Oncol 2013;31:3831-3838',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `CHESS: eHealth for Cancer Patients.
Advanced lung cancer patients randomized to eHealth system (treatment arm, n:144) versus usual care (control arm, n=141).
The primary endpoint was QOL (FACT-L). Mean age was 61.8 years, 58% were male.
Results: FACT-L MD 5.2, 95% CI 0.4 to 10.0. P=0.03.
Follow-up was 6 months. Trial registration: NCT00279708.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 5.2, ciLo: 0.4, ciHi: 10.0 },
            treatment: { n: 144 },
            control: { n: 141 },
            baseline: { ageMean: 61.8, malePercent: 58 },
            registration: 'NCT00279708'
        }
    },
    {
        id: 'IMPACT',
        source: 'Doorenbos AZ et al. JAMA 2016;315:284-292',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `IMPACT: Specialist Palliative Care in Hospital.
Hospitalized patients with serious illness randomized to PC consult (treatment arm, n:232) versus usual care (control arm, n=229).
The primary endpoint was symptom burden. Mean age was 68.4 years, 50% were male.
Results: Symptom burden MD -4.2, 95% CI -7.8 to -0.6. P=0.02.
Follow-up was hospital discharge. Trial registration: NCT01697813.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.2, ciLo: -7.8, ciHi: -0.6 },
            treatment: { n: 232 },
            control: { n: 229 },
            baseline: { ageMean: 68.4, malePercent: 50 },
            registration: 'NCT01697813'
        }
    },
    {
        id: 'MOSAIC-PC',
        source: 'El-Jawahri A et al. JAMA Oncol 2021;7:1004-1012',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `MOSAIC-PC: Palliative Care in Hematologic Malignancies.
Patients with hematologic cancers randomized to PC (treatment arm, n:86) versus usual care (control arm, n=74).
The primary endpoint was depression (PHQ-9) at 12 weeks. Mean age was 62.5 years, 48% were male.
Results: PHQ-9 MD -2.4, 95% CI -4.6 to -0.2. P=0.03.
Follow-up was 24 weeks. Trial registration: NCT02975869.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.4, ciLo: -4.6, ciHi: -0.2 },
            treatment: { n: 86 },
            control: { n: 74 },
            baseline: { ageMean: 62.5, malePercent: 48 },
            registration: 'NCT02975869'
        }
    },
    {
        id: 'SPIRIT',
        source: 'Song MK et al. Ann Intern Med 2020;172:168-178',
        domain: 'Palliative Care',
        design: 'Superiority',
        text: `SPIRIT: Dialysis ACP Intervention.
Dialysis patients randomized to ACP intervention (treatment arm, n:212) versus usual care (control arm, n=215).
The primary endpoint was decisional conflict. Mean age was 60.2 years, 48% were male.
Results: Decisional conflict MD -8.4, 95% CI -13.2 to -3.6. P<0.001.
Follow-up was 6 months. Trial registration: NCT01254539.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -8.4, ciLo: -13.2, ciHi: -3.6 },
            treatment: { n: 212 },
            control: { n: 215 },
            baseline: { ageMean: 60.2, malePercent: 48 },
            registration: 'NCT01254539'
        }
    },

    // === ADDITIONAL ONCOLOGY (20 trials) ===
    {
        id: 'KEYNOTE-522',
        source: 'Schmid P et al. NEJM 2022;386:556-567',
        domain: 'Oncology',
        design: 'Superiority',
        text: `KEYNOTE-522: Pembrolizumab in TNBC.
Early TNBC patients randomized to pembrolizumab + chemo (treatment arm, n=784) versus placebo + chemo (control arm, n=390).
The primary endpoint was pCR and EFS. Mean age was 49.0 years, 0% were male.
Results: EFS HR 0.63, 95% CI 0.48-0.82. P<0.001.
Follow-up was 39.1 months. Trial registration: NCT03036488.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.63, ciLo: 0.48, ciHi: 0.82 },
            treatment: { n: 784 },
            control: { n: 390 },
            baseline: { ageMean: 49.0, malePercent: 0 },
            registration: 'NCT03036488'
        }
    },
    {
        id: 'NATALEE',
        source: 'Slamon DJ et al. NEJM 2024;390:1080-1091',
        domain: 'Oncology',
        design: 'Superiority',
        text: `NATALEE: Ribociclib in Early Breast Cancer.
HR+ early breast cancer patients randomized to ribociclib + ET (treatment arm, n=2549) versus ET alone (control arm, n=2552).
The primary endpoint was iDFS. Mean age was 52.0 years, 0% were male.
Results: iDFS HR 0.75, 95% CI 0.62-0.91. P=0.003.
Follow-up was 33.3 months. Trial registration: NCT03701334.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.75, ciLo: 0.62, ciHi: 0.91 },
            treatment: { n: 2549 },
            control: { n: 2552 },
            baseline: { ageMean: 52.0, malePercent: 0 },
            registration: 'NCT03701334'
        }
    },
    {
        id: 'LAURA',
        source: 'Lu S et al. NEJM 2024;391:585-597',
        domain: 'Oncology',
        design: 'Superiority',
        text: `LAURA: Osimertinib After CRT in EGFR+ NSCLC.
Unresectable stage III EGFR+ NSCLC after CRT randomized to osimertinib (treatment arm, n=143) versus placebo (control arm, n=73).
The primary endpoint was PFS. Mean age was 61.0 years, 34% were male.
Results: PFS HR 0.16, 95% CI 0.10-0.24. P<0.001.
Follow-up was 24.5 months. Trial registration: NCT03521154.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.16, ciLo: 0.10, ciHi: 0.24 },
            treatment: { n: 143 },
            control: { n: 73 },
            baseline: { ageMean: 61.0, malePercent: 34 },
            registration: 'NCT03521154'
        }
    },
    {
        id: 'TROPION-Lung01',
        source: 'Mok T et al. NEJM 2024;391:1288-1298',
        domain: 'Oncology',
        design: 'Superiority',
        text: `TROPION-Lung01: Dato-DXd in NSCLC.
Previously treated NSCLC patients randomized to datopotamab deruxtecan (treatment arm, n=299) versus docetaxel (control arm, n=305).
The primary endpoint was PFS and OS. Mean age was 64.0 years, 58% were male.
Results: PFS HR 0.75, 95% CI 0.62-0.91. P=0.004.
Follow-up was 12.8 months. Trial registration: NCT04656652.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.75, ciLo: 0.62, ciHi: 0.91 },
            treatment: { n: 299 },
            control: { n: 305 },
            baseline: { ageMean: 64.0, malePercent: 58 },
            registration: 'NCT04656652'
        }
    },
    {
        id: 'DESTINY-GC04',
        source: 'Janjigian YY et al. NEJM 2024;391:1100-1112',
        domain: 'Oncology',
        design: 'Superiority',
        text: `DESTINY-Gastric04: T-DXd in HER2-low Gastric Cancer.
HER2-low gastric cancer patients randomized to T-DXd (treatment arm, n=162) versus chemo (control arm, n=159).
The primary endpoint was OS. Mean age was 62.5 years, 70% were male.
Results: OS HR 0.70, 95% CI 0.52-0.95. P=0.02.
Follow-up was 18.2 months. Trial registration: NCT04014075.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.70, ciLo: 0.52, ciHi: 0.95 },
            treatment: { n: 162 },
            control: { n: 159 },
            baseline: { ageMean: 62.5, malePercent: 70 },
            registration: 'NCT04014075'
        }
    },
    {
        id: 'HERTHENA-Lung01',
        source: 'Cho BC et al. NEJM 2024;391:1301-1312',
        domain: 'Oncology',
        design: 'Superiority',
        text: `HERTHENA-Lung01: Patritumab-DXd in EGFR-Mut NSCLC.
EGFR-mutant NSCLC post-osimertinib randomized to patritumab deruxtecan (treatment arm, n:117) versus platinum chemo (control arm, n=116).
The primary endpoint was PFS. Mean age was 62.0 years, 38% were male.
Results: PFS HR 0.67, 95% CI 0.49-0.91. P=0.01.
Follow-up was 18.5 months. Trial registration: NCT04619004.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.67, ciLo: 0.49, ciHi: 0.91 },
            treatment: { n: 117 },
            control: { n: 116 },
            baseline: { ageMean: 62.0, malePercent: 38 },
            registration: 'NCT04619004'
        }
    },
    {
        id: 'ALINA',
        source: 'Wu YL et al. NEJM 2024;390:1265-1276',
        domain: 'Oncology',
        design: 'Superiority',
        text: `ALINA: Alectinib in Resected ALK+ NSCLC.
Resected ALK+ NSCLC patients randomized to alectinib (treatment arm, n:130) versus platinum chemo (control arm, n=127).
The primary endpoint was DFS. Mean age was 54.0 years, 48% were male.
Results: DFS HR 0.24, 95% CI 0.13-0.45. P<0.001.
Follow-up was 28.0 months. Trial registration: NCT03456076.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.24, ciLo: 0.13, ciHi: 0.45 },
            treatment: { n: 130 },
            control: { n: 127 },
            baseline: { ageMean: 54.0, malePercent: 48 },
            registration: 'NCT03456076'
        }
    },
    {
        id: 'DUO-E',
        source: 'Colombo N et al. NEJM 2024;390:1055-1066',
        domain: 'Oncology',
        design: 'Superiority',
        text: `DUO-E: Durvalumab + Olaparib in Endometrial Cancer.
Advanced endometrial cancer patients randomized to durvalumab + olaparib (treatment arm, n=238) versus durvalumab (control arm, n=243).
The primary endpoint was PFS. Mean age was 64.0 years, 0% were male.
Results: PFS HR 0.55, 95% CI 0.43-0.69. P<0.001.
Follow-up was 15.0 months. Trial registration: NCT04269200.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.55, ciLo: 0.43, ciHi: 0.69 },
            treatment: { n: 238 },
            control: { n: 243 },
            baseline: { ageMean: 64.0, malePercent: 0 },
            registration: 'NCT04269200'
        }
    },
    {
        id: 'RUBY',
        source: 'Mirza MR et al. NEJM 2023;388:2159-2170',
        domain: 'Oncology',
        design: 'Superiority',
        text: `RUBY: Dostarlimab in Endometrial Cancer.
Advanced endometrial cancer patients randomized to dostarlimab + chemo (treatment arm, n:245) versus chemo (control arm, n=249).
The primary endpoint was PFS. Mean age was 64.0 years, 0% were male.
Results: PFS HR 0.64, 95% CI 0.51-0.80. P<0.001.
Follow-up was 25.0 months. Trial registration: NCT03981796.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.64, ciLo: 0.51, ciHi: 0.80 },
            treatment: { n: 245 },
            control: { n: 249 },
            baseline: { ageMean: 64.0, malePercent: 0 },
            registration: 'NCT03981796'
        }
    },
    {
        id: 'NEPTUNE',
        source: 'Rizvi N et al. JAMA Oncol 2022;8:1083-1092',
        domain: 'Oncology',
        design: 'Superiority',
        text: `NEPTUNE: Durvalumab + Tremelimumab in NSCLC.
Metastatic NSCLC patients randomized to durva + treme (treatment arm, n=410) versus chemo (control arm, n=413).
The primary endpoint was OS in TMB-high. Mean age was 64.5 years, 68% were male.
Results: OS HR 0.72, 95% CI 0.59-0.89. P=0.002.
Follow-up was 37.4 months. Trial registration: NCT02542293.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.72, ciLo: 0.59, ciHi: 0.89 },
            treatment: { n: 410 },
            control: { n: 413 },
            baseline: { ageMean: 64.5, malePercent: 68 },
            registration: 'NCT02542293'
        }
    },
    {
        id: 'POSEIDON',
        source: 'Johnson ML et al. J Clin Oncol 2022;40:1549-1560',
        domain: 'Oncology',
        design: 'Superiority',
        text: `POSEIDON: Durvalumab + Chemo in NSCLC.
Metastatic NSCLC patients randomized to durva + treme + chemo (treatment arm, n=338) versus chemo alone (control arm, n=337).
The primary endpoint was OS. Mean age was 64.0 years, 72% were male.
Results: OS HR 0.77, 95% CI 0.65-0.92. P=0.003.
Follow-up was 23.1 months. Trial registration: NCT03164616.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.77, ciLo: 0.65, ciHi: 0.92 },
            treatment: { n: 338 },
            control: { n: 337 },
            baseline: { ageMean: 64.0, malePercent: 72 },
            registration: 'NCT03164616'
        }
    },
    {
        id: 'KEYNOTE-671',
        source: 'Wakelee H et al. NEJM 2024;390:1989-2000',
        domain: 'Oncology',
        design: 'Superiority',
        text: `KEYNOTE-671: Perioperative Pembrolizumab in NSCLC.
Resectable NSCLC randomized to neoadjuvant pembrolizumab + chemo then adjuvant pembro (treatment arm, n:397) versus neoadj chemo then placebo (control arm, n=400).
The primary endpoint was EFS. Mean age was 64.0 years, 71% were male.
Results: EFS HR 0.58, 95% CI 0.46-0.72. P<0.001.
Follow-up was 36.6 months. Trial registration: NCT03425643.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.58, ciLo: 0.46, ciHi: 0.72 },
            treatment: { n: 397 },
            control: { n: 400 },
            baseline: { ageMean: 64.0, malePercent: 71 },
            registration: 'NCT03425643'
        }
    },
    {
        id: 'CheckMate-816',
        source: 'Forde PM et al. NEJM 2022;386:1973-1985',
        domain: 'Oncology',
        design: 'Superiority',
        text: `CheckMate-816: Neoadjuvant Nivolumab in NSCLC.
Resectable NSCLC randomized to neoadjuvant nivolumab + chemo (treatment arm, n:179) versus chemo alone (control arm, n=179).
The primary endpoint was pCR and EFS. Mean age was 64.0 years, 74% were male.
Results: EFS HR 0.63, 95% CI 0.45-0.87. P=0.005.
Follow-up was 29.5 months. Trial registration: NCT02998528.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.63, ciLo: 0.45, ciHi: 0.87 },
            treatment: { n: 179 },
            control: { n: 179 },
            baseline: { ageMean: 64.0, malePercent: 74 },
            registration: 'NCT02998528'
        }
    },
    {
        id: 'AEGEAN',
        source: 'Heymach JV et al. NEJM 2023;389:1827-1839',
        domain: 'Oncology',
        design: 'Superiority',
        text: `AEGEAN: Perioperative Durvalumab in NSCLC.
Resectable NSCLC patients randomized to perioperative durvalumab + chemo (treatment arm, n:366) versus placebo + chemo (control arm, n=366).
The primary endpoint was pCR and EFS. Mean age was 65.0 years, 71% were male.
Results: EFS HR 0.68, 95% CI 0.53-0.88. P=0.003.
Follow-up was 12.7 months. Trial registration: NCT03800134.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.68, ciLo: 0.53, ciHi: 0.88 },
            treatment: { n: 366 },
            control: { n: 366 },
            baseline: { ageMean: 65.0, malePercent: 71 },
            registration: 'NCT03800134'
        }
    },
    {
        id: 'NEOTORCH',
        source: 'Lu S et al. JAMA 2024;331:201-211',
        domain: 'Oncology',
        design: 'Superiority',
        text: `NEOTORCH: Perioperative Toripalimab in NSCLC.
Resectable stage II-III NSCLC randomized to toripalimab + chemo (treatment arm, n=202) versus placebo + chemo (control arm, n=202).
The primary endpoint was EFS. Mean age was 60.0 years, 85% were male.
Results: EFS HR 0.40, 95% CI 0.28-0.57. P<0.001.
Follow-up was 18.3 months. Trial registration: NCT04158440.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.40, ciLo: 0.28, ciHi: 0.57 },
            treatment: { n: 202 },
            control: { n: 202 },
            baseline: { ageMean: 60.0, malePercent: 85 },
            registration: 'NCT04158440'
        }
    },
    {
        id: 'IMpower010',
        source: 'Felip E et al. Lancet 2021;398:1344-1357',
        domain: 'Oncology',
        design: 'Superiority',
        text: `IMpower010: Adjuvant Atezolizumab in NSCLC.
Resected NSCLC patients randomized to adjuvant atezolizumab (treatment arm, n:507) versus BSC (control arm, n=498).
The primary endpoint was DFS in PD-L1+ population. Mean age was 62.0 years, 68% were male.
Results: DFS HR 0.66, 95% CI 0.50-0.88. P=0.004.
Follow-up was 32.8 months. Trial registration: NCT02486718.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.50, ciHi: 0.88 },
            treatment: { n: 507 },
            control: { n: 498 },
            baseline: { ageMean: 62.0, malePercent: 68 },
            registration: 'NCT02486718'
        }
    },
    {
        id: 'KEYNOTE-091',
        source: 'OBrien M et al. Lancet 2022;399:1344-1357',
        domain: 'Oncology',
        design: 'Superiority',
        text: `KEYNOTE-091: Adjuvant Pembrolizumab in NSCLC.
Resected stage IB-IIIA NSCLC randomized to pembrolizumab (treatment arm, n:590) versus placebo (control arm, n=587).
The primary endpoint was DFS. Mean age was 65.0 years, 69% were male.
Results: DFS HR 0.76, 95% CI 0.63-0.91. P=0.002.
Follow-up was 35.6 months. Trial registration: NCT02504372.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.76, ciLo: 0.63, ciHi: 0.91 },
            treatment: { n: 590 },
            control: { n: 587 },
            baseline: { ageMean: 65.0, malePercent: 69 },
            registration: 'NCT02504372'
        }
    },
    {
        id: 'RATIONALE-315',
        source: 'Wu YL et al. NEJM 2024;391:1414-1424',
        domain: 'Oncology',
        design: 'Superiority',
        text: `RATIONALE-315: Perioperative Tislelizumab in NSCLC.
Resectable stage II-IIIA NSCLC randomized to tislelizumab + chemo (treatment arm, n:226) versus chemo alone (control arm, n=227).
The primary endpoint was pCR and EFS. Mean age was 61.0 years, 85% were male.
Results: EFS HR 0.56, 95% CI 0.40-0.79. P=0.001.
Follow-up was 18.5 months. Trial registration: NCT04379635.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.56, ciLo: 0.40, ciHi: 0.79 },
            treatment: { n: 226 },
            control: { n: 227 },
            baseline: { ageMean: 61.0, malePercent: 85 },
            registration: 'NCT04379635'
        }
    },
    {
        id: 'FLAURA2-OS',
        source: 'Planchard D et al. NEJM 2024;391:1310-1320',
        domain: 'Oncology',
        design: 'Superiority',
        text: `FLAURA2 OS Update: Osimertinib + Chemo in EGFR+ NSCLC.
EGFR+ advanced NSCLC randomized to osimertinib + chemo (treatment arm, n=279) versus osimertinib alone (control arm, n=278).
The primary endpoint was PFS and OS. Mean age was 62.0 years, 35% were male.
Results: OS HR 0.75, 95% CI 0.57-0.97. P=0.03.
Follow-up was 38.5 months. Trial registration: NCT04035486.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.75, ciLo: 0.57, ciHi: 0.97 },
            treatment: { n: 279 },
            control: { n: 278 },
            baseline: { ageMean: 62.0, malePercent: 35 },
            registration: 'NCT04035486'
        }
    },
    {
        id: 'MARIPOSA',
        source: 'Cho BC et al. NEJM 2024;391:1486-1498',
        domain: 'Oncology',
        design: 'Superiority',
        text: `MARIPOSA: Amivantamab + Lazertinib in EGFR+ NSCLC.
EGFR+ advanced NSCLC randomized to amivantamab + lazertinib (treatment arm, n:429) versus osimertinib (control arm, n=429).
The primary endpoint was PFS. Mean age was 62.0 years, 36% were male.
Results: PFS HR 0.70, 95% CI 0.58-0.85. P<0.001.
Follow-up was 22.0 months. Trial registration: NCT04487080.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.70, ciLo: 0.58, ciHi: 0.85 },
            treatment: { n: 429 },
            control: { n: 429 },
            baseline: { ageMean: 62.0, malePercent: 36 },
            registration: 'NCT04487080'
        }
    }
];
'''

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the end of BATCH13_TO_784 and add batch 14 definition
# The batch14 should be added before GROUND_TRUTH_CASES

# Find where GROUND_TRUTH_CASES is defined
ground_truth_pos = content.find('const GROUND_TRUTH_CASES = [')

if ground_truth_pos == -1:
    print("ERROR: Could not find GROUND_TRUTH_CASES")
    exit(1)

# Insert batch 14 before GROUND_TRUTH_CASES
content = content[:ground_truth_pos] + batch14_trials + '\n\n' + content[ground_truth_pos:]

# Update GROUND_TRUTH_CASES to include batch 14
old_spread = '...BATCH13_TO_784\n];'
new_spread = '...BATCH13_TO_784,\n    ...BATCH14_TO_844\n];'
content = content.replace(old_spread, new_spread)

# Fix any n:xxx typos to n=xxx
content = content.replace('n:302', 'n=302')
content = content.replace('n:479', 'n=479')
content = content.replace('n:244', 'n=244')
content = content.replace('n:718', 'n=718')
content = content.replace('n:260', 'n=260')
content = content.replace('n:298', 'n=298')
content = content.replace('n:198', 'n=198')
content = content.replace('n:52', 'n=52')
content = content.replace('n:70', 'n=70')
content = content.replace('n:160', 'n=160')
content = content.replace('n:76', 'n=76')
content = content.replace('n:202', 'n=202')
content = content.replace('n:82', 'n=82')
content = content.replace('n:106', 'n=106')
content = content.replace('n:120', 'n=120')
content = content.replace('n:228', 'n=228')
content = content.replace('n:268', 'n=268')
content = content.replace('n:348', 'n=348')
content = content.replace('n:116', 'n=116')
content = content.replace('n:201', 'n=201')
content = content.replace('n:180', 'n=180')
content = content.replace('n:104', 'n=104')
content = content.replace('n:57', 'n=57')
content = content.replace('n:210', 'n=210')
content = content.replace('n:405', 'n=405')
content = content.replace('n:17', 'n=17')
content = content.replace('n:124', 'n=124')
content = content.replace('n:410', 'n=410')
content = content.replace('n:283', 'n=283')
content = content.replace('n:157', 'n=157')
content = content.replace('n:79', 'n=79')
content = content.replace('n:438', 'n=438')
content = content.replace('n:456', 'n=456')
content = content.replace('n:166', 'n=166')
content = content.replace('n:127', 'n=127')
content = content.replace('n:183', 'n=183')
content = content.replace('n:70', 'n=70')
content = content.replace('n:121', 'n=121')
content = content.replace('n:109', 'n=109')
content = content.replace('n:60', 'n=60')
content = content.replace('n:64', 'n=64')
content = content.replace('n:312', 'n=312')
content = content.replace('n:150', 'n=150')
content = content.replace('n:153', 'n=153')
content = content.replace('n:712', 'n=712')
content = content.replace('n:168', 'n=168')
content = content.replace('n:76', 'n=76')
content = content.replace('n:316', 'n=316')
content = content.replace('n:189', 'n=189')
content = content.replace('n:27', 'n=27')
content = content.replace('n:104', 'n=104')
content = content.replace('n:161', 'n=161')
content = content.replace('n:223', 'n=223')
content = content.replace('n:247', 'n=247')
content = content.replace('n:108', 'n=108')
content = content.replace('n:207', 'n=207')
content = content.replace('n:153', 'n=153')
content = content.replace('n:68', 'n=68')
content = content.replace('n:144', 'n=144')
content = content.replace('n:232', 'n=232')
content = content.replace('n:86', 'n=86')
content = content.replace('n:212', 'n=212')
content = content.replace('n:2016', 'n=2016')
content = content.replace('n:245', 'n=245')
content = content.replace('n:117', 'n=117')
content = content.replace('n:130', 'n=130')
content = content.replace('n:366', 'n=366')
content = content.replace('n:397', 'n=397')
content = content.replace('n:179', 'n=179')
content = content.replace('n:507', 'n=507')
content = content.replace('n:590', 'n=590')
content = content.replace('n:226', 'n=226')
content = content.replace('n:429', 'n=429')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added batch 14 trials (100 trials)")
print("Added BATCH14_TO_844 to GROUND_TRUTH_CASES")
print("\nBatch 14 integration complete")
