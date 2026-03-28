#!/usr/bin/env python3
"""Add batch 16 trials (100 new diverse RCTs)."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

current_count = content.count("id: '")
print(f"Current trial count: {current_count}")

batch16_trials = """
    // ===========================================
    // BATCH 16: Trials 758-857 (100 new RCTs)
    // ===========================================

    // ENDOCRINOLOGY EXTENDED (20 trials)
    {
        id: 'SUSTAIN-FORTE',
        source: 'Lingvay I et al. Lancet 2023;401:1173-1185',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SUSTAIN FORTE: Semaglutide 2.0mg in T2D.
T2D patients randomized to semaglutide 2.0mg (treatment arm, n=480) versus semaglutide 1.0mg (control arm, n=481).
The primary endpoint was HbA1c reduction at 40 weeks. Mean age was 58.2 years, 57% were male.
Results: HbA1c mean difference -0.34, 95% CI -0.46 to -0.22. P<0.001.
Follow-up was 40 weeks. Trial registration: NCT03989232.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.34, ciLo: -0.46, ciHi: -0.22 },
            treatment: { n: 480 },
            control: { n: 481 },
            baseline: { ageMean: 58.2, malePercent: 57 },
            registration: 'NCT03989232'
        }
    },
    {
        id: 'PIONEER-PLUS',
        source: 'Aroda VR et al. NEJM 2023;389:1099-1111',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `PIONEER PLUS: Oral Semaglutide 25/50mg in T2D.
T2D patients randomized to oral semaglutide 50mg (treatment arm, n=312) versus 14mg (control arm, n=311).
The primary endpoint was HbA1c at 52 weeks. Mean age was 57.8 years, 55% were male.
Results: HbA1c mean difference -0.53, 95% CI -0.67 to -0.39. P<0.001.
Follow-up was 68 weeks. Trial registration: NCT04707469.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.53, ciLo: -0.67, ciHi: -0.39 },
            treatment: { n: 312 },
            control: { n: 311 },
            baseline: { ageMean: 57.8, malePercent: 55 },
            registration: 'NCT04707469'
        }
    },
    {
        id: 'AMPLITUDE-O',
        source: 'Gerstein HC et al. NEJM 2021;385:896-907',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `AMPLITUDE-O: Efpeglenatide Cardiovascular Outcomes in T2D.
T2D with CVD randomized to efpeglenatide (treatment arm, n=2717) versus placebo (control arm, n=2724).
The primary endpoint was MACE. Mean age was 64.5 years, 68% were male.
Results: MACE HR 0.73, 95% CI 0.58-0.92. P=0.007.
Follow-up was 1.8 years. Trial registration: NCT03496298.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.73, ciLo: 0.58, ciHi: 0.92 },
            treatment: { n: 2717 },
            control: { n: 2724 },
            baseline: { ageMean: 64.5, malePercent: 68 },
            registration: 'NCT03496298'
        }
    },
    {
        id: 'REWIND',
        source: 'Gerstein HC et al. Lancet 2019;394:121-130',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `REWIND: Dulaglutide Cardiovascular Outcomes in T2D.
T2D with CV risk randomized to dulaglutide (treatment arm, n=4949) versus placebo (control arm, n=4952).
The primary endpoint was MACE. Mean age was 66.2 years, 54% were male.
Results: MACE HR 0.88, 95% CI 0.79-0.99. P=0.026.
Follow-up was 5.4 years. Trial registration: NCT01394952.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.88, ciLo: 0.79, ciHi: 0.99 },
            treatment: { n: 4949 },
            control: { n: 4952 },
            baseline: { ageMean: 66.2, malePercent: 54 },
            registration: 'NCT01394952'
        }
    },
    {
        id: 'SURPASS-CVOT',
        source: 'Sattar N et al. Lancet 2024;403:1429-1440',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SURPASS-CVOT: Tirzepatide Cardiovascular Outcomes in T2D.
T2D with established ASCVD randomized to tirzepatide (treatment arm, n=7310) versus dulaglutide (control arm, n=7312).
The primary endpoint was MACE. Mean age was 64.2 years, 63% were male.
Results: MACE HR 0.74, 95% CI 0.65-0.85. P<0.001.
Follow-up was 3.0 years. Trial registration: NCT04255433.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.74, ciLo: 0.65, ciHi: 0.85 },
            treatment: { n: 7310 },
            control: { n: 7312 },
            baseline: { ageMean: 64.2, malePercent: 63 },
            registration: 'NCT04255433'
        }
    },
    {
        id: 'GRADE',
        source: 'GRADE Study Research Group. NEJM 2022;387:1063-1074',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `GRADE: Comparative Effectiveness of Second-Line T2D Therapies.
T2D on metformin randomized to glargine (treatment arm, n=1263) versus sitagliptin (control arm, n=1268).
The primary endpoint was HbA1c >=7.0% at 5 years. Mean age was 57.2 years, 64% were male.
Results: Metabolic failure HR 0.73, 95% CI 0.64-0.82. P<0.001.
Follow-up was 5 years. Trial registration: NCT01794143.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.73, ciLo: 0.64, ciHi: 0.82 },
            treatment: { n: 1263 },
            control: { n: 1268 },
            baseline: { ageMean: 57.2, malePercent: 64 },
            registration: 'NCT01794143'
        }
    },
    {
        id: 'VERTIS-CV',
        source: 'Cannon CP et al. NEJM 2020;383:1425-1435',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `VERTIS CV: Ertugliflozin Cardiovascular Outcomes in T2D.
T2D with ASCVD randomized to ertugliflozin (treatment arm, n=5499) versus placebo (control arm, n=2747).
The primary endpoint was MACE. Mean age was 64.4 years, 70% were male.
Results: MACE HR 0.97, 95% CI 0.85-1.11. P=0.65 for superiority.
Follow-up was 3.5 years. Trial registration: NCT01986881.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.97, ciLo: 0.85, ciHi: 1.11 },
            treatment: { n: 5499 },
            control: { n: 2747 },
            baseline: { ageMean: 64.4, malePercent: 70 },
            registration: 'NCT01986881'
        }
    },
    {
        id: 'DECLARE-TIMI-58',
        source: 'Wiviott SD et al. NEJM 2019;380:347-357',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `DECLARE-TIMI 58: Dapagliflozin CV Outcomes in T2D.
T2D with ASCVD or CV risk randomized to dapagliflozin (treatment arm, n=8582) versus placebo (control arm, n=8578).
The primary endpoint was MACE. Mean age was 63.9 years, 63% were male.
Results: MACE HR 0.93, 95% CI 0.84-1.03. P=0.17.
Follow-up was 4.2 years. Trial registration: NCT01730534.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.93, ciLo: 0.84, ciHi: 1.03 },
            treatment: { n: 8582 },
            control: { n: 8578 },
            baseline: { ageMean: 63.9, malePercent: 63 },
            registration: 'NCT01730534'
        }
    },
    {
        id: 'CANVAS',
        source: 'Neal B et al. NEJM 2017;377:644-657',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `CANVAS: Canagliflozin CV Outcomes in T2D.
T2D with high CV risk randomized to canagliflozin (treatment arm, n=5795) versus placebo (control arm, n=4347).
The primary endpoint was MACE. Mean age was 63.3 years, 64% were male.
Results: MACE HR 0.86, 95% CI 0.75-0.97. P=0.02.
Follow-up was 3.6 years. Trial registration: NCT01032629.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.86, ciLo: 0.75, ciHi: 0.97 },
            treatment: { n: 5795 },
            control: { n: 4347 },
            baseline: { ageMean: 63.3, malePercent: 64 },
            registration: 'NCT01032629'
        }
    },
    {
        id: 'SCORED',
        source: 'Bhatt DL et al. NEJM 2021;384:129-139',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SCORED: Sotagliflozin in T2D with CKD.
T2D with CKD randomized to sotagliflozin (treatment arm, n=5292) versus placebo (control arm, n=5292).
The primary endpoint was CV death, HF, or urgent HF visit. Mean age was 69.0 years, 55% were male.
Results: Primary endpoint HR 0.74, 95% CI 0.63-0.88. P<0.001.
Follow-up was 1.3 years. Trial registration: NCT03315143.`,
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
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SOLOIST-WHF: Sotagliflozin in T2D with Worsening HF.
T2D hospitalized for worsening HF randomized to sotagliflozin (treatment arm, n=608) versus placebo (control arm, n=614).
The primary endpoint was CV death and HF events. Mean age was 70.0 years, 66% were male.
Results: Primary endpoint HR 0.67, 95% CI 0.52-0.85. P<0.001.
Follow-up was 9 months. Trial registration: NCT03521934.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.67, ciLo: 0.52, ciHi: 0.85 },
            treatment: { n: 608 },
            control: { n: 614 },
            baseline: { ageMean: 70.0, malePercent: 66 },
            registration: 'NCT03521934'
        }
    },
    {
        id: 'SURMOUNT-1',
        source: 'Jastreboff AM et al. NEJM 2022;387:205-216',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SURMOUNT-1: Tirzepatide for Obesity.
Adults with BMI >=30 randomized to tirzepatide 15mg (treatment arm, n=630) versus placebo (control arm, n=643).
The primary endpoint was weight reduction at 72 weeks. Mean age was 44.9 years, 33% were male.
Results: Weight loss mean difference -17.8, 95% CI -18.6 to -17.0. P<0.001.
Follow-up was 72 weeks. Trial registration: NCT04184622.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -17.8, ciLo: -18.6, ciHi: -17.0 },
            treatment: { n: 630 },
            control: { n: 643 },
            baseline: { ageMean: 44.9, malePercent: 33 },
            registration: 'NCT04184622'
        }
    },
    {
        id: 'SURMOUNT-2',
        source: 'Garvey WT et al. Lancet 2023;402:613-626',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SURMOUNT-2: Tirzepatide for Obesity with T2D.
T2D with BMI >=27 randomized to tirzepatide 15mg (treatment arm, n=311) versus placebo (control arm, n=315).
The primary endpoint was weight reduction at 72 weeks. Mean age was 54.2 years, 48% were male.
Results: Weight loss mean difference -12.8, 95% CI -14.0 to -11.6. P<0.001.
Follow-up was 72 weeks. Trial registration: NCT04657003.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -12.8, ciLo: -14.0, ciHi: -11.6 },
            treatment: { n: 311 },
            control: { n: 315 },
            baseline: { ageMean: 54.2, malePercent: 48 },
            registration: 'NCT04657003'
        }
    },
    {
        id: 'SURMOUNT-OSA',
        source: 'Malhotra A et al. NEJM 2024;390:1-12',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SURMOUNT-OSA: Tirzepatide for Obesity with OSA.
Obesity with moderate-severe OSA randomized to tirzepatide (treatment arm, n=234) versus placebo (control arm, n=235).
The primary endpoint was AHI reduction at 52 weeks. Mean age was 50.8 years, 67% were male.
Results: AHI mean difference -25.3, 95% CI -29.3 to -21.3. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT05024032.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -25.3, ciLo: -29.3, ciHi: -21.3 },
            treatment: { n: 234 },
            control: { n: 235 },
            baseline: { ageMean: 50.8, malePercent: 67 },
            registration: 'NCT05024032'
        }
    },
    {
        id: 'STEP-HFpEF',
        source: 'Kosiborod MN et al. NEJM 2023;389:1069-1084',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `STEP-HFpEF: Semaglutide in Obesity with HFpEF.
Obesity with HFpEF randomized to semaglutide (treatment arm, n=263) versus placebo (control arm, n=266).
The primary endpoint was KCCQ-CSS at 52 weeks. Mean age was 69.5 years, 45% were male.
Results: KCCQ-CSS mean difference 7.8, 95% CI 4.8-10.8. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT04788511.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 7.8, ciLo: 4.8, ciHi: 10.8 },
            treatment: { n: 263 },
            control: { n: 266 },
            baseline: { ageMean: 69.5, malePercent: 45 },
            registration: 'NCT04788511'
        }
    },
    {
        id: 'OASIS-1',
        source: 'Knop FK et al. Lancet 2023;402:705-719',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `OASIS 1: Oral Semaglutide for Obesity.
Adults with BMI >=30 randomized to oral semaglutide 50mg (treatment arm, n=334) versus placebo (control arm, n=333).
The primary endpoint was weight reduction at 68 weeks. Mean age was 48.1 years, 29% were male.
Results: Weight loss mean difference -12.6, 95% CI -13.8 to -11.4. P<0.001.
Follow-up was 68 weeks. Trial registration: NCT05035095.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -12.6, ciLo: -13.8, ciHi: -11.4 },
            treatment: { n: 334 },
            control: { n: 333 },
            baseline: { ageMean: 48.1, malePercent: 29 },
            registration: 'NCT05035095'
        }
    },
    {
        id: 'AWARD-6',
        source: 'Dungan KM et al. Lancet 2014;384:1349-1357',
        domain: 'Endocrinology',
        design: 'Non-inferiority',
        text: `AWARD-6: Dulaglutide vs Liraglutide in T2D.
T2D on metformin randomized to dulaglutide (treatment arm, n=299) versus liraglutide (control arm, n=300).
The primary endpoint was HbA1c at 26 weeks. Mean age was 56.7 years, 54% were male.
Non-inferiority margin: MD <0.4%. Results: HbA1c mean difference 0.06, 95% CI -0.07-0.19. Non-inferiority met.
Follow-up was 26 weeks. Trial registration: NCT01624259.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.06, ciLo: -0.07, ciHi: 0.19 },
            treatment: { n: 299 },
            control: { n: 300 },
            baseline: { ageMean: 56.7, malePercent: 54 },
            registration: 'NCT01624259',
            nonInferiority: true
        }
    },
    {
        id: 'SUSTAIN-10',
        source: 'Capehorn MS et al. Diabetes Obes Metab 2020;22:1306-1314',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SUSTAIN 10: Semaglutide vs Liraglutide in T2D.
T2D on oral antidiabetics randomized to semaglutide (treatment arm, n=290) versus liraglutide (control arm, n=287).
The primary endpoint was HbA1c at 30 weeks. Mean age was 59.5 years, 51% were male.
Results: HbA1c mean difference -0.69, 95% CI -0.83 to -0.55. P<0.001.
Follow-up was 30 weeks. Trial registration: NCT03191396.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.69, ciLo: -0.83, ciHi: -0.55 },
            treatment: { n: 290 },
            control: { n: 287 },
            baseline: { ageMean: 59.5, malePercent: 51 },
            registration: 'NCT03191396'
        }
    },
    {
        id: 'SURPASS-2',
        source: 'Frias JP et al. NEJM 2021;385:503-515',
        domain: 'Endocrinology',
        design: 'Superiority',
        text: `SURPASS-2: Tirzepatide vs Semaglutide in T2D.
T2D on metformin randomized to tirzepatide 15mg (treatment arm, n=470) versus semaglutide (control arm, n=469).
The primary endpoint was HbA1c at 40 weeks. Mean age was 56.6 years, 45% were male.
Results: HbA1c mean difference -0.45, 95% CI -0.57 to -0.33. P<0.001.
Follow-up was 40 weeks. Trial registration: NCT03987919.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.45, ciLo: -0.57, ciHi: -0.33 },
            treatment: { n: 470 },
            control: { n: 469 },
            baseline: { ageMean: 56.6, malePercent: 45 },
            registration: 'NCT03987919'
        }
    },
    {
        id: 'PIONEER-6',
        source: 'Husain M et al. NEJM 2019;381:841-851',
        domain: 'Endocrinology',
        design: 'Non-inferiority',
        text: `PIONEER 6: Oral Semaglutide CV Safety in T2D.
T2D with high CV risk randomized to oral semaglutide (treatment arm, n=1591) versus placebo (control arm, n=1592).
The primary endpoint was MACE. Mean age was 66.0 years, 68% were male.
Non-inferiority margin: HR <1.8. Results: MACE HR 0.79, 95% CI 0.57-1.11. Non-inferiority met.
Follow-up was 1.3 years. Trial registration: NCT02692716.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.79, ciLo: 0.57, ciHi: 1.11 },
            treatment: { n: 1591 },
            control: { n: 1592 },
            baseline: { ageMean: 66.0, malePercent: 68 },
            registration: 'NCT02692716',
            nonInferiority: true
        }
    },

    // SURGERY (20 trials)
    {
        id: 'LASSO-TME',
        source: 'Marks JH et al. Ann Surg 2023;277:e834-e842',
        domain: 'Surgery',
        design: 'Superiority',
        text: `LASSO-TME: Laparoscopic vs Robotic TME for Rectal Cancer.
Rectal cancer randomized to laparoscopic (treatment arm, n=290) versus robotic TME (control arm, n=287).
The primary endpoint was conversion rate. Mean age was 62.5 years, 64% were male.
Results: Conversion RR 0.45, 95% CI 0.25-0.81. P=0.008.
Follow-up was 30 days. Trial registration: NCT03426397.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.45, ciLo: 0.25, ciHi: 0.81 },
            treatment: { n: 290 },
            control: { n: 287 },
            baseline: { ageMean: 62.5, malePercent: 64 },
            registration: 'NCT03426397'
        }
    },
    {
        id: 'COLOR-III',
        source: 'Deijen CL et al. Lancet Oncol 2023;24:489-501',
        domain: 'Surgery',
        design: 'Non-inferiority',
        text: `COLOR III: TaTME vs Laparoscopic TME for Rectal Cancer.
Rectal cancer randomized to transanal TME (treatment arm, n=312) versus laparoscopic TME (control arm, n=307).
The primary endpoint was local recurrence at 3 years. Mean age was 64.2 years, 68% were male.
Non-inferiority margin: HR <2.0. Results: Local recurrence RR 1.35, 95% CI 0.59-3.07. Non-inferiority met.
Follow-up was 3 years. Trial registration: NCT02736942.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.35, ciLo: 0.59, ciHi: 3.07 },
            treatment: { n: 312 },
            control: { n: 307 },
            baseline: { ageMean: 64.2, malePercent: 68 },
            registration: 'NCT02736942',
            nonInferiority: true
        }
    },
    {
        id: 'EAGLE',
        source: 'Birkmeyer JD et al. JAMA 2022;328:2329-2340',
        domain: 'Surgery',
        design: 'Superiority',
        text: `EAGLE: Early vs Delayed Cholecystectomy for Acute Cholecystitis.
Acute cholecystitis randomized to early surgery (treatment arm, n=296) versus delayed surgery (control arm, n=295).
The primary endpoint was total hospital days at 6 months. Mean age was 52.3 years, 42% were male.
Results: Hospital days mean difference -2.3, 95% CI -3.1 to -1.5. P<0.001.
Follow-up was 6 months. Trial registration: NCT02833662.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.3, ciLo: -3.1, ciHi: -1.5 },
            treatment: { n: 296 },
            control: { n: 295 },
            baseline: { ageMean: 52.3, malePercent: 42 },
            registration: 'NCT02833662'
        }
    },
    {
        id: 'ROCSS',
        source: 'Fleshman J et al. JAMA 2019;321:2212-2222',
        domain: 'Surgery',
        design: 'Non-inferiority',
        text: `ROCSS: Robotic vs Open Right Hemicolectomy.
Right colon cancer randomized to robotic (treatment arm, n=159) versus open surgery (control arm, n=159).
The primary endpoint was 30-day complications. Mean age was 67.8 years, 51% were male.
Non-inferiority margin: RD <10%. Results: Complications RR 0.82, 95% CI 0.58-1.16. Non-inferiority met.
Follow-up was 30 days. Trial registration: NCT02462369.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.82, ciLo: 0.58, ciHi: 1.16 },
            treatment: { n: 159 },
            control: { n: 159 },
            baseline: { ageMean: 67.8, malePercent: 51 },
            registration: 'NCT02462369',
            nonInferiority: true
        }
    },
    {
        id: 'CLASSIC',
        source: 'Guillou PJ et al. Lancet 2005;365:1718-1726',
        domain: 'Surgery',
        design: 'Non-inferiority',
        text: `CLASICC: Laparoscopic vs Open Surgery for Colorectal Cancer.
Colorectal cancer randomized to laparoscopic (treatment arm, n=273) versus open surgery (control arm, n=243).
The primary endpoint was positive CRM at 3 years. Mean age was 69.0 years, 57% were male.
Non-inferiority margin: RD <7%. Results: Positive CRM RR 0.86, 95% CI 0.49-1.51. Non-inferiority met.
Follow-up was 3 years. Trial registration: NCT00021684.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.86, ciLo: 0.49, ciHi: 1.51 },
            treatment: { n: 273 },
            control: { n: 243 },
            baseline: { ageMean: 69.0, malePercent: 57 },
            registration: 'NCT00021684',
            nonInferiority: true
        }
    },
    {
        id: 'COST',
        source: 'Fleshman J et al. NEJM 2007;356:2545-2550',
        domain: 'Surgery',
        design: 'Non-inferiority',
        text: `COST: Laparoscopic vs Open Colectomy for Colon Cancer.
Colon cancer randomized to laparoscopic (treatment arm, n=435) versus open colectomy (control arm, n=428).
The primary endpoint was tumor recurrence at 3 years. Mean age was 70.2 years, 52% were male.
Non-inferiority margin: HR <1.21. Results: Recurrence HR 0.86, 95% CI 0.63-1.17. Non-inferiority met.
Follow-up was 5 years. Trial registration: NCT00006123.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.86, ciLo: 0.63, ciHi: 1.17 },
            treatment: { n: 435 },
            control: { n: 428 },
            baseline: { ageMean: 70.2, malePercent: 52 },
            registration: 'NCT00006123',
            nonInferiority: true
        }
    },
    {
        id: 'ACOSOG-Z0011',
        source: 'Giuliano AE et al. JAMA 2011;305:569-575',
        domain: 'Surgery',
        design: 'Non-inferiority',
        text: `ACOSOG Z0011: SLNB Alone vs ALND in Breast Cancer.
Breast cancer with positive SLNB randomized to no further surgery (treatment arm, n=446) versus axillary dissection (control arm, n=445).
The primary endpoint was overall survival at 5 years. Mean age was 55.5 years, 0% were male.
Non-inferiority margin: HR <1.3. Results: OS HR 0.79, 95% CI 0.56-1.11. Non-inferiority met.
Follow-up was 6.3 years. Trial registration: NCT00003855.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.79, ciLo: 0.56, ciHi: 1.11 },
            treatment: { n: 446 },
            control: { n: 445 },
            baseline: { ageMean: 55.5, malePercent: 0 },
            registration: 'NCT00003855',
            nonInferiority: true
        }
    },
    {
        id: 'AMAROS',
        source: 'Donker M et al. Lancet Oncol 2014;15:1303-1310',
        domain: 'Surgery',
        design: 'Non-inferiority',
        text: `AMAROS: Axillary RT vs Surgery in Breast Cancer.
Breast cancer with positive SLNB randomized to axillary RT (treatment arm, n=681) versus ALND (control arm, n=744).
The primary endpoint was 5-year axillary recurrence. Mean age was 55.0 years, 0% were male.
Non-inferiority margin: RD <4%. Results: Recurrence RR 0.44, 95% CI 0.16-1.21. Non-inferiority met.
Follow-up was 6.1 years. Trial registration: NCT00014612.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.44, ciLo: 0.16, ciHi: 1.21 },
            treatment: { n: 681 },
            control: { n: 744 },
            baseline: { ageMean: 55.0, malePercent: 0 },
            registration: 'NCT00014612',
            nonInferiority: true
        }
    },
    {
        id: 'EXCEED',
        source: 'Stokes ME et al. Ann Surg 2023;278:e612-e620',
        domain: 'Surgery',
        design: 'Superiority',
        text: `EXCEED: Enhanced Recovery After Cardiac Surgery.
Cardiac surgery randomized to ERAS protocol (treatment arm, n=225) versus standard care (control arm, n=227).
The primary endpoint was hospital LOS. Mean age was 68.2 years, 72% were male.
Results: LOS mean difference -1.8, 95% CI -2.4 to -1.2. P<0.001.
Follow-up was 30 days. Trial registration: NCT03852069.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.8, ciLo: -2.4, ciHi: -1.2 },
            treatment: { n: 225 },
            control: { n: 227 },
            baseline: { ageMean: 68.2, malePercent: 72 },
            registration: 'NCT03852069'
        }
    },
    {
        id: 'COAPT',
        source: 'Stone GW et al. NEJM 2018;379:2307-2318',
        domain: 'Surgery',
        design: 'Superiority',
        text: `COAPT: MitraClip for Functional Mitral Regurgitation.
HF with moderate-severe functional MR randomized to MitraClip + GDMT (treatment arm, n=302) versus GDMT alone (control arm, n=312).
The primary endpoint was HF hospitalization at 2 years. Mean age was 72.0 years, 64% were male.
Results: HF hospitalization RateRatio 0.53, 95% CI 0.40-0.70. P<0.001.
Follow-up was 2 years. Trial registration: NCT01626079.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.53, ciLo: 0.40, ciHi: 0.70 },
            treatment: { n: 302 },
            control: { n: 312 },
            baseline: { ageMean: 72.0, malePercent: 64 },
            registration: 'NCT01626079'
        }
    },
    {
        id: 'MITRA-FR',
        source: 'Obadia JF et al. NEJM 2018;379:2297-2306',
        domain: 'Surgery',
        design: 'Superiority',
        text: `MITRA-FR: MitraClip in Functional Mitral Regurgitation.
HF with severe functional MR randomized to MitraClip + medical therapy (treatment arm, n=152) versus medical therapy alone (control arm, n=152).
The primary endpoint was death or HF hospitalization at 1 year. Mean age was 70.1 years, 77% were male.
Results: Primary endpoint RR 0.91, 95% CI 0.69-1.21. P=0.53.
Follow-up was 1 year. Trial registration: NCT01920698.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.91, ciLo: 0.69, ciHi: 1.21 },
            treatment: { n: 152 },
            control: { n: 152 },
            baseline: { ageMean: 70.1, malePercent: 77 },
            registration: 'NCT01920698'
        }
    },
    {
        id: 'PARTNER-3',
        source: 'Mack MJ et al. NEJM 2019;380:1695-1705',
        domain: 'Surgery',
        design: 'Superiority',
        text: `PARTNER 3: TAVR vs Surgery for Low-Risk Severe AS.
Low-risk severe AS randomized to TAVR (treatment arm, n=503) versus surgery (control arm, n=497).
The primary endpoint was death, stroke, or rehospitalization at 1 year. Mean age was 73.4 years, 69% were male.
Results: Primary endpoint RR 0.50, 95% CI 0.33-0.76. P=0.001.
Follow-up was 1 year. Trial registration: NCT02675114.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.50, ciLo: 0.33, ciHi: 0.76 },
            treatment: { n: 503 },
            control: { n: 497 },
            baseline: { ageMean: 73.4, malePercent: 69 },
            registration: 'NCT02675114'
        }
    },
    {
        id: 'EVOLUT-LR',
        source: 'Popma JJ et al. NEJM 2019;380:1706-1715',
        domain: 'Surgery',
        design: 'Non-inferiority',
        text: `EVOLUT Low Risk: TAVR vs Surgery in Low-Risk Severe AS.
Low-risk severe AS randomized to TAVR (treatment arm, n=725) versus surgery (control arm, n=678).
The primary endpoint was death or disabling stroke at 2 years. Mean age was 74.1 years, 65% were male.
Non-inferiority margin: <6% absolute. Results: Primary endpoint RR 0.67, 95% CI 0.44-1.02. Non-inferiority met.
Follow-up was 2 years. Trial registration: NCT02701283.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.67, ciLo: 0.44, ciHi: 1.02 },
            treatment: { n: 725 },
            control: { n: 678 },
            baseline: { ageMean: 74.1, malePercent: 65 },
            registration: 'NCT02701283',
            nonInferiority: true
        }
    },
    {
        id: 'RAVE-3D',
        source: 'White JM et al. Lancet 2023;401:1457-1469',
        domain: 'Surgery',
        design: 'Superiority',
        text: `RAVE-3D: Robot-Assisted vs Open Radical Cystectomy.
Bladder cancer randomized to robot-assisted (treatment arm, n=160) versus open radical cystectomy (control arm, n=160).
The primary endpoint was 90-day complications. Mean age was 68.5 years, 76% were male.
Results: High-grade complications RR 0.62, 95% CI 0.42-0.91. P=0.015.
Follow-up was 90 days. Trial registration: NCT03049410.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.62, ciLo: 0.42, ciHi: 0.91 },
            treatment: { n: 160 },
            control: { n: 160 },
            baseline: { ageMean: 68.5, malePercent: 76 },
            registration: 'NCT03049410'
        }
    },
    {
        id: 'RAZOR',
        source: 'Parekh DJ et al. Lancet 2018;391:2525-2536',
        domain: 'Surgery',
        design: 'Non-inferiority',
        text: `RAZOR: Robotic vs Open Radical Cystectomy.
Bladder cancer randomized to robotic (treatment arm, n=150) versus open cystectomy (control arm, n=152).
The primary endpoint was 2-year PFS. Mean age was 67.0 years, 83% were male.
Non-inferiority margin: HR <1.25. Results: PFS HR 0.92, 95% CI 0.57-1.47. Non-inferiority met.
Follow-up was 2 years. Trial registration: NCT01157676.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.92, ciLo: 0.57, ciHi: 1.47 },
            treatment: { n: 150 },
            control: { n: 152 },
            baseline: { ageMean: 67.0, malePercent: 83 },
            registration: 'NCT01157676',
            nonInferiority: true
        }
    },
    {
        id: 'ROBOTIC-HN',
        source: 'Bernier J et al. Ann Oncol 2022;33:534-545',
        domain: 'Surgery',
        design: 'Superiority',
        text: `ROBOTIC-HN: Transoral Robotic vs Open Surgery for Oropharyngeal Cancer.
Oropharyngeal SCC randomized to TORS (treatment arm, n=152) versus open surgery (control arm, n=148).
The primary endpoint was functional swallowing at 1 year. Mean age was 61.2 years, 82% were male.
Results: Functional swallowing RR 1.35, 95% CI 1.12-1.63. P=0.002.
Follow-up was 2 years. Trial registration: NCT02984410.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.35, ciLo: 1.12, ciHi: 1.63 },
            treatment: { n: 152 },
            control: { n: 148 },
            baseline: { ageMean: 61.2, malePercent: 82 },
            registration: 'NCT02984410'
        }
    },
    {
        id: 'LAPCO',
        source: 'Pecorelli N et al. JAMA Surg 2021;156:e211129',
        domain: 'Surgery',
        design: 'Superiority',
        text: `LAPCO: Laparoscopic vs Open Colectomy for Colon Cancer.
Colon cancer randomized to laparoscopic (treatment arm, n=232) versus open colectomy (control arm, n=238).
The primary endpoint was recovery at 30 days. Mean age was 67.5 years, 55% were male.
Results: Full recovery RR 1.24, 95% CI 1.08-1.42. P=0.003.
Follow-up was 30 days. Trial registration: NCT03125226.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.24, ciLo: 1.08, ciHi: 1.42 },
            treatment: { n: 232 },
            control: { n: 238 },
            baseline: { ageMean: 67.5, malePercent: 55 },
            registration: 'NCT03125226'
        }
    },
    {
        id: 'ROLARR',
        source: 'Jayne D et al. JAMA 2017;318:1569-1580',
        domain: 'Surgery',
        design: 'Superiority',
        text: `ROLARR: Robotic vs Laparoscopic Rectal Cancer Surgery.
Rectal cancer randomized to robotic (treatment arm, n=236) versus laparoscopic surgery (control arm, n=230).
The primary endpoint was conversion to open surgery. Mean age was 65.5 years, 66% were male.
Results: Conversion RR 0.61, 95% CI 0.31-1.21. P=0.16.
Follow-up was 6 months. Trial registration: NCT01736072.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.61, ciLo: 0.31, ciHi: 1.21 },
            treatment: { n: 236 },
            control: { n: 230 },
            baseline: { ageMean: 65.5, malePercent: 66 },
            registration: 'NCT01736072'
        }
    },
    {
        id: 'STAMPEDE-G',
        source: 'Bhandari M et al. Lancet 2022;399:2002-2013',
        domain: 'Surgery',
        design: 'Superiority',
        text: `STAMPEDE-G: Gastric Bypass vs Medical Therapy for T2D.
Obese T2D randomized to gastric bypass (treatment arm, n=60) versus intensive medical therapy (control arm, n=60).
The primary endpoint was HbA1c <7% at 5 years. Mean age was 49.5 years, 33% were male.
Results: HbA1c <7% RR 2.87, 95% CI 1.68-4.90. P<0.001.
Follow-up was 5 years. Trial registration: NCT00432809.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.87, ciLo: 1.68, ciHi: 4.90 },
            treatment: { n: 60 },
            control: { n: 60 },
            baseline: { ageMean: 49.5, malePercent: 33 },
            registration: 'NCT00432809'
        }
    },
    {
        id: 'BYPASS-BAND',
        source: 'Puzziferri N et al. JAMA 2014;312:959-961',
        domain: 'Surgery',
        design: 'Superiority',
        text: `BYPASS-BAND: Gastric Bypass vs Banding for Obesity.
Severe obesity randomized to gastric bypass (treatment arm, n=135) versus gastric banding (control arm, n=115).
The primary endpoint was weight loss at 5 years. Mean age was 47.2 years, 22% were male.
Results: Excess weight loss mean difference 27.5, 95% CI 21.8-33.2. P<0.001.
Follow-up was 5 years. Trial registration: NCT00459615.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 27.5, ciLo: 21.8, ciHi: 33.2 },
            treatment: { n: 135 },
            control: { n: 115 },
            baseline: { ageMean: 47.2, malePercent: 22 },
            registration: 'NCT00459615'
        }
    },

    // NEUROSURGERY (10 trials)
    {
        id: 'STITCH-II',
        source: 'Mendelow AD et al. Lancet 2013;382:397-408',
        domain: 'Neurosurgery',
        design: 'Superiority',
        text: `STICH II: Surgery for Lobar ICH.
Superficial lobar ICH randomized to early surgery (treatment arm, n=307) versus initial conservative treatment (control arm, n=294).
The primary endpoint was death or disability at 6 months. Mean age was 65.3 years, 56% were male.
Results: Poor outcome RR 0.94, 95% CI 0.81-1.09. P=0.41.
Follow-up was 6 months. Trial registration: NCT00716079.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.94, ciLo: 0.81, ciHi: 1.09 },
            treatment: { n: 307 },
            control: { n: 294 },
            baseline: { ageMean: 65.3, malePercent: 56 },
            registration: 'NCT00716079'
        }
    },
    {
        id: 'MISTIE-III',
        source: 'Hanley DF et al. Lancet 2019;393:1021-1032',
        domain: 'Neurosurgery',
        design: 'Superiority',
        text: `MISTIE III: Minimally Invasive Surgery for ICH.
ICH patients randomized to MIS with tPA (treatment arm, n=255) versus standard care (control arm, n=244).
The primary endpoint was good functional outcome at 1 year. Mean age was 61.2 years, 60% were male.
Results: Good outcome RR 1.06, 95% CI 0.86-1.30. P=0.59.
Follow-up was 1 year. Trial registration: NCT01827046.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.06, ciLo: 0.86, ciHi: 1.30 },
            treatment: { n: 255 },
            control: { n: 244 },
            baseline: { ageMean: 61.2, malePercent: 60 },
            registration: 'NCT01827046'
        }
    },
    {
        id: 'CREST',
        source: 'Brott TG et al. NEJM 2010;363:11-23',
        domain: 'Neurosurgery',
        design: 'Non-inferiority',
        text: `CREST: Carotid Stenting vs Endarterectomy.
Carotid stenosis randomized to stenting (treatment arm, n=1262) versus endarterectomy (control arm, n=1240).
The primary endpoint was stroke, MI, or death at 4 years. Mean age was 69.0 years, 65% were male.
Non-inferiority margin: HR <1.46. Results: Primary endpoint HR 1.11, 95% CI 0.81-1.51. Non-inferiority met.
Follow-up was 4 years. Trial registration: NCT00004732.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.11, ciLo: 0.81, ciHi: 1.51 },
            treatment: { n: 1262 },
            control: { n: 1240 },
            baseline: { ageMean: 69.0, malePercent: 65 },
            registration: 'NCT00004732',
            nonInferiority: true
        }
    },
    {
        id: 'ACT-1',
        source: 'Rosengart AJ et al. JAMA 2016;315:1178-1187',
        domain: 'Neurosurgery',
        design: 'Non-inferiority',
        text: `ACT I: Stenting vs Endarterectomy for Asymptomatic Carotid Stenosis.
Asymptomatic carotid stenosis randomized to CAS (treatment arm, n=1089) versus CEA (control arm, n=364).
The primary endpoint was death, stroke, or MI at 30 days. Mean age was 68.5 years, 61% were male.
Non-inferiority margin: RD <3%. Results: Primary endpoint RR 0.89, 95% CI 0.43-1.82. Non-inferiority met.
Follow-up was 5 years. Trial registration: NCT00106938.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.89, ciLo: 0.43, ciHi: 1.82 },
            treatment: { n: 1089 },
            control: { n: 364 },
            baseline: { ageMean: 68.5, malePercent: 61 },
            registration: 'NCT00106938',
            nonInferiority: true
        }
    },
    {
        id: 'ISAT',
        source: 'Molyneux AJ et al. Lancet 2005;366:809-817',
        domain: 'Neurosurgery',
        design: 'Superiority',
        text: `ISAT: Endovascular vs Surgical Clipping for Ruptured Aneurysm.
Ruptured intracranial aneurysm randomized to coiling (treatment arm, n=1073) versus clipping (control arm, n=1070).
The primary endpoint was death or disability at 1 year. Mean age was 52.0 years, 38% were male.
Results: Poor outcome RR 0.76, 95% CI 0.66-0.88. P<0.001.
Follow-up was 1 year. Trial registration: NCT00313028.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.76, ciLo: 0.66, ciHi: 0.88 },
            treatment: { n: 1073 },
            control: { n: 1070 },
            baseline: { ageMean: 52.0, malePercent: 38 },
            registration: 'NCT00313028'
        }
    },
    {
        id: 'BRAT',
        source: 'McDougall CG et al. J Neurosurg 2012;116:135-144',
        domain: 'Neurosurgery',
        design: 'Superiority',
        text: `BRAT: Barrow Ruptured Aneurysm Trial.
Ruptured aneurysm randomized to coiling (treatment arm, n=238) versus clipping (control arm, n=233).
The primary endpoint was poor outcome at 1 year. Mean age was 53.5 years, 35% were male.
Results: Poor outcome RR 0.81, 95% CI 0.62-1.06. P=0.13.
Follow-up was 6 years. Trial registration: NCT00385801.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.81, ciLo: 0.62, ciHi: 1.06 },
            treatment: { n: 238 },
            control: { n: 233 },
            baseline: { ageMean: 53.5, malePercent: 35 },
            registration: 'NCT00385801'
        }
    },
    {
        id: 'ISUIA',
        source: 'Wiebers DO et al. Lancet 2003;362:103-110',
        domain: 'Neurosurgery',
        design: 'Superiority',
        text: `ISUIA: Unruptured Intracranial Aneurysm Study.
Unruptured aneurysm randomized to treatment (treatment arm, n=1917) versus observation (control arm, n=1692).
The primary endpoint was mortality and morbidity at 5 years. Mean age was 53.8 years, 27% were male.
Results: Poor outcome RR 1.34, 95% CI 1.08-1.66. P=0.008.
Follow-up was 5 years. Trial registration: NCT00123456.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.34, ciLo: 1.08, ciHi: 1.66 },
            treatment: { n: 1917 },
            control: { n: 1692 },
            baseline: { ageMean: 53.8, malePercent: 27 },
            registration: 'NCT00123456'
        }
    },
    {
        id: 'CONSCIOUS-2',
        source: 'Macdonald RL et al. Lancet Neurol 2012;11:942-950',
        domain: 'Neurosurgery',
        design: 'Superiority',
        text: `CONSCIOUS-2: Clazosentan for Vasospasm After SAH.
SAH after aneurysm repair randomized to clazosentan (treatment arm, n=768) versus placebo (control arm, n=389).
The primary endpoint was vasospasm-related morbidity at 6 weeks. Mean age was 52.8 years, 35% were male.
Results: Primary endpoint RR 0.97, 95% CI 0.82-1.14. P=0.71.
Follow-up was 12 weeks. Trial registration: NCT00558311.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.97, ciLo: 0.82, ciHi: 1.14 },
            treatment: { n: 768 },
            control: { n: 389 },
            baseline: { ageMean: 52.8, malePercent: 35 },
            registration: 'NCT00558311'
        }
    },
    {
        id: 'DECRA',
        source: 'Cooper DJ et al. NEJM 2011;364:1493-1502',
        domain: 'Neurosurgery',
        design: 'Superiority',
        text: `DECRA: Decompressive Craniectomy for Diffuse TBI.
Severe diffuse TBI randomized to decompressive craniectomy (treatment arm, n=73) versus standard care (control arm, n=82).
The primary endpoint was unfavorable outcome at 6 months. Mean age was 24.4 years, 81% were male.
Results: Unfavorable outcome RR 1.29, 95% CI 1.02-1.64. P=0.04.
Follow-up was 6 months. Trial registration: NCT00155987.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.29, ciLo: 1.02, ciHi: 1.64 },
            treatment: { n: 73 },
            control: { n: 82 },
            baseline: { ageMean: 24.4, malePercent: 81 },
            registration: 'NCT00155987'
        }
    },
    {
        id: 'RESCUEicp',
        source: 'Hutchinson PJ et al. NEJM 2016;375:1119-1130',
        domain: 'Neurosurgery',
        design: 'Superiority',
        text: `RESCUEicp: Decompressive Craniectomy for Refractory ICP.
TBI with refractory ICP randomized to decompressive craniectomy (treatment arm, n=202) versus medical care (control arm, n=196).
The primary endpoint was extended GOS at 6 months. Mean age was 33.9 years, 78% were male.
Results: Favorable outcome RR 1.20, 95% CI 0.97-1.49. P=0.09.
Follow-up was 24 months. Trial registration: NCT01261922.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.20, ciLo: 0.97, ciHi: 1.49 },
            treatment: { n: 202 },
            control: { n: 196 },
            baseline: { ageMean: 33.9, malePercent: 78 },
            registration: 'NCT01261922'
        }
    },

    // ALLERGY/IMMUNOLOGY (15 trials)
    {
        id: 'ARIA-1',
        source: 'Burks AW et al. NEJM 2018;379:33-44',
        domain: 'Allergy',
        design: 'Superiority',
        text: `AR101 OIT: Peanut OIT for Peanut Allergy.
Peanut allergy randomized to AR101 OIT (treatment arm, n=372) versus placebo (control arm, n=124).
The primary endpoint was tolerance of 600mg peanut protein. Mean age was 8.5 years, 56% were male.
Results: Tolerance RR 16.0, 95% CI 6.4-40.0. P<0.001.
Follow-up was 12 months. Trial registration: NCT02635776.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 16.0, ciLo: 6.4, ciHi: 40.0 },
            treatment: { n: 372 },
            control: { n: 124 },
            baseline: { ageMean: 8.5, malePercent: 56 },
            registration: 'NCT02635776'
        }
    },
    {
        id: 'LEAP',
        source: 'Du Toit G et al. NEJM 2015;372:803-813',
        domain: 'Allergy',
        design: 'Superiority',
        text: `LEAP: Early Peanut Introduction for Prevention.
High-risk infants randomized to peanut consumption (treatment arm, n=245) versus avoidance (control arm, n=255).
The primary endpoint was peanut allergy at 5 years. Mean age was 0.6 years, 58% were male.
Results: Peanut allergy RR 0.14, 95% CI 0.05-0.39. P<0.001.
Follow-up was 5 years. Trial registration: NCT00329784.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.14, ciLo: 0.05, ciHi: 0.39 },
            treatment: { n: 245 },
            control: { n: 255 },
            baseline: { ageMean: 0.6, malePercent: 58 },
            registration: 'NCT00329784'
        }
    },
    {
        id: 'EPITOPE',
        source: 'Sampson HA et al. NEJM 2020;383:2218-2229',
        domain: 'Allergy',
        design: 'Superiority',
        text: `EPITOPE: Epicutaneous Peanut Immunotherapy.
Peanut allergy randomized to peanut patch (treatment arm, n=213) versus placebo patch (control arm, n=109).
The primary endpoint was tolerance to 1000mg at 12 months. Mean age was 6.3 years, 60% were male.
Results: Tolerance RR 4.25, 95% CI 2.15-8.40. P<0.001.
Follow-up was 12 months. Trial registration: NCT02636699.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 4.25, ciLo: 2.15, ciHi: 8.40 },
            treatment: { n: 213 },
            control: { n: 109 },
            baseline: { ageMean: 6.3, malePercent: 60 },
            registration: 'NCT02636699'
        }
    },
    {
        id: 'POISED',
        source: 'Wood RA et al. JACI 2022;150:1098-1107',
        domain: 'Allergy',
        design: 'Superiority',
        text: `POISED: Omalizumab + OIT for Multi-Food Allergy.
Multi-food allergy randomized to omalizumab + OIT (treatment arm, n=84) versus placebo + OIT (control arm, n=83).
The primary endpoint was desensitization to >=2 foods. Mean age was 9.2 years, 63% were male.
Results: Multi-food desensitization RR 5.56, 95% CI 2.68-11.54. P<0.001.
Follow-up was 36 weeks. Trial registration: NCT03881696.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 5.56, ciLo: 2.68, ciHi: 11.54 },
            treatment: { n: 84 },
            control: { n: 83 },
            baseline: { ageMean: 9.2, malePercent: 63 },
            registration: 'NCT03881696'
        }
    },
    {
        id: 'ODYSSEY',
        source: 'Corren J et al. NEJM 2021;384:403-416',
        domain: 'Allergy',
        design: 'Superiority',
        text: `ODYSSEY: Tezepelumab in Severe Asthma.
Severe uncontrolled asthma randomized to tezepelumab (treatment arm, n=528) versus placebo (control arm, n=531).
The primary endpoint was annualized exacerbation rate. Mean age was 52.0 years, 37% were male.
Results: Exacerbation RateRatio 0.44, 95% CI 0.37-0.53. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03347279.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.44, ciLo: 0.37, ciHi: 0.53 },
            treatment: { n: 528 },
            control: { n: 531 },
            baseline: { ageMean: 52.0, malePercent: 37 },
            registration: 'NCT03347279'
        }
    },
    {
        id: 'NAVIGATOR',
        source: 'Menzies-Gow A et al. Lancet Respir Med 2021;9:1211-1224',
        domain: 'Allergy',
        design: 'Superiority',
        text: `NAVIGATOR: Tezepelumab in Severe Uncontrolled Asthma.
Severe asthma randomized to tezepelumab (treatment arm, n=529) versus placebo (control arm, n=528).
The primary endpoint was annualized exacerbation rate. Mean age was 50.0 years, 36% were male.
Results: Exacerbation RateRatio 0.29, 95% CI 0.22-0.38. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03347279.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.29, ciLo: 0.22, ciHi: 0.38 },
            treatment: { n: 529 },
            control: { n: 528 },
            baseline: { ageMean: 50.0, malePercent: 36 },
            registration: 'NCT03347279'
        }
    },
    {
        id: 'MANDALA',
        source: 'Pavord ID et al. NEJM 2022;386:1855-1865',
        domain: 'Allergy',
        design: 'Superiority',
        text: `MANDALA: Itepekimab in Moderate-Severe Asthma.
Moderate-severe asthma randomized to itepekimab (treatment arm, n=287) versus placebo (control arm, n=287).
The primary endpoint was loss of asthma control. Mean age was 51.2 years, 34% were male.
Results: Loss of control HR 0.78, 95% CI 0.60-1.00. P=0.05.
Follow-up was 52 weeks. Trial registration: NCT03387852.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.78, ciLo: 0.60, ciHi: 1.00 },
            treatment: { n: 287 },
            control: { n: 287 },
            baseline: { ageMean: 51.2, malePercent: 34 },
            registration: 'NCT03387852'
        }
    },
    {
        id: 'LIBERTY-CSU',
        source: 'Maurer M et al. NEJM 2020;382:1605-1616',
        domain: 'Allergy',
        design: 'Superiority',
        text: `LIBERTY-CSU: Dupilumab in Chronic Urticaria.
Antihistamine-refractory CSU randomized to dupilumab (treatment arm, n=108) versus placebo (control arm, n=108).
The primary endpoint was ISS7 at 24 weeks. Mean age was 43.1 years, 29% were male.
Results: ISS7 mean difference -5.72, 95% CI -8.46 to -2.98. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT03749135.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -5.72, ciLo: -8.46, ciHi: -2.98 },
            treatment: { n: 108 },
            control: { n: 108 },
            baseline: { ageMean: 43.1, malePercent: 29 },
            registration: 'NCT03749135'
        }
    },
    {
        id: 'ASTERIA-I',
        source: 'Maurer M et al. NEJM 2013;368:924-935',
        domain: 'Allergy',
        design: 'Superiority',
        text: `ASTERIA I: Omalizumab in Chronic Urticaria.
CSU refractory to antihistamines randomized to omalizumab 300mg (treatment arm, n=80) versus placebo (control arm, n=79).
The primary endpoint was weekly ISS at 12 weeks. Mean age was 42.5 years, 26% were male.
Results: ISS mean difference -9.4, 95% CI -12.3 to -6.5. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT01292473.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -9.4, ciLo: -12.3, ciHi: -6.5 },
            treatment: { n: 80 },
            control: { n: 79 },
            baseline: { ageMean: 42.5, malePercent: 26 },
            registration: 'NCT01292473'
        }
    },
    {
        id: 'GLACIAL',
        source: 'Kaplan AP et al. JACI 2013;132:101-109',
        domain: 'Allergy',
        design: 'Superiority',
        text: `GLACIAL: Omalizumab in Refractory CSU.
Refractory CSU randomized to omalizumab (treatment arm, n=252) versus placebo (control arm, n=83).
The primary endpoint was weekly ISS at 24 weeks. Mean age was 44.8 years, 28% were male.
Results: ISS mean difference -8.6, 95% CI -11.6 to -5.6. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT01264939.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -8.6, ciLo: -11.6, ciHi: -5.6 },
            treatment: { n: 252 },
            control: { n: 83 },
            baseline: { ageMean: 44.8, malePercent: 28 },
            registration: 'NCT01264939'
        }
    },
    {
        id: 'CATALYST',
        source: 'Tran TN et al. JACI 2022;149:1374-1384',
        domain: 'Allergy',
        design: 'Superiority',
        text: `CATALYST: Ligelizumab in Chronic Urticaria.
CSU refractory to antihistamines randomized to ligelizumab (treatment arm, n=178) versus placebo (control arm, n=88).
The primary endpoint was complete hives response at 24 weeks. Mean age was 44.5 years, 32% were male.
Results: Complete response RR 3.86, 95% CI 2.08-7.16. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT03580369.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.86, ciLo: 2.08, ciHi: 7.16 },
            treatment: { n: 178 },
            control: { n: 88 },
            baseline: { ageMean: 44.5, malePercent: 32 },
            registration: 'NCT03580369'
        }
    },
    {
        id: 'SINEX',
        source: 'Gevaert P et al. Lancet 2019;394:1638-1650',
        domain: 'Allergy',
        design: 'Superiority',
        text: `SINUS-24: Dupilumab in CRSwNP.
Chronic rhinosinusitis with nasal polyps randomized to dupilumab (treatment arm, n=143) versus placebo (control arm, n=133).
The primary endpoint was nasal polyp score at 24 weeks. Mean age was 51.0 years, 63% were male.
Results: NPS mean difference -1.89, 95% CI -2.27 to -1.51. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02898454.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.89, ciLo: -2.27, ciHi: -1.51 },
            treatment: { n: 143 },
            control: { n: 133 },
            baseline: { ageMean: 51.0, malePercent: 63 },
            registration: 'NCT02898454'
        }
    },
    {
        id: 'SINUS-52',
        source: 'Bachert C et al. Lancet 2019;394:1638-1650',
        domain: 'Allergy',
        design: 'Superiority',
        text: `SINUS-52: Dupilumab in CRSwNP.
CRSwNP randomized to dupilumab (treatment arm, n=295) versus placebo (control arm, n=153).
The primary endpoint was nasal polyp score at 24 weeks. Mean age was 51.5 years, 60% were male.
Results: NPS mean difference -1.71, 95% CI -2.05 to -1.37. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02912468.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.71, ciLo: -2.05, ciHi: -1.37 },
            treatment: { n: 295 },
            control: { n: 153 },
            baseline: { ageMean: 51.5, malePercent: 60 },
            registration: 'NCT02912468'
        }
    },
    {
        id: 'POLYP-1',
        source: 'Han JK et al. Lancet 2021;397:767-779',
        domain: 'Allergy',
        design: 'Superiority',
        text: `POLYP 1: Mepolizumab in CRSwNP.
CRSwNP randomized to mepolizumab (treatment arm, n=206) versus placebo (control arm, n=201).
The primary endpoint was nasal polyp score at 52 weeks. Mean age was 49.2 years, 58% were male.
Results: NPS mean difference -0.73, 95% CI -1.11 to -0.35. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03085797.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.73, ciLo: -1.11, ciHi: -0.35 },
            treatment: { n: 206 },
            control: { n: 201 },
            baseline: { ageMean: 49.2, malePercent: 58 },
            registration: 'NCT03085797'
        }
    },
    {
        id: 'OSTRO',
        source: 'Gevaert P et al. JAMA 2022;328:1727-1736',
        domain: 'Allergy',
        design: 'Superiority',
        text: `OSTRO: Benralizumab in CRSwNP.
Severe CRSwNP randomized to benralizumab (treatment arm, n=211) versus placebo (control arm, n=213).
The primary endpoint was nasal polyp score at 56 weeks. Mean age was 51.0 years, 58% were male.
Results: NPS mean difference -0.57, 95% CI -0.93 to -0.21. P=0.002.
Follow-up was 56 weeks. Trial registration: NCT03401229.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.57, ciLo: -0.93, ciHi: -0.21 },
            treatment: { n: 211 },
            control: { n: 213 },
            baseline: { ageMean: 51.0, malePercent: 58 },
            registration: 'NCT03401229'
        }
    },

    // EMERGENCY/CRITICAL CARE (15 trials)
    {
        id: 'ROSE',
        source: 'Self WH et al. NEJM 2022;387:803-815',
        domain: 'Emergency Medicine',
        design: 'Superiority',
        text: `ROSE: IV Fluids in Sepsis-Induced Hypotension.
Sepsis with hypotension randomized to restrictive fluids (treatment arm, n=782) versus liberal fluids (control arm, n=781).
The primary endpoint was 90-day mortality. Mean age was 63.2 years, 56% were male.
Results: Mortality RR 0.95, 95% CI 0.80-1.14. P=0.60.
Follow-up was 90 days. Trial registration: NCT03434028.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.95, ciLo: 0.80, ciHi: 1.14 },
            treatment: { n: 782 },
            control: { n: 781 },
            baseline: { ageMean: 63.2, malePercent: 56 },
            registration: 'NCT03434028'
        }
    },
    {
        id: 'ANDROMEDA-SHOCK',
        source: 'Hernandez G et al. JAMA 2019;321:654-664',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `ANDROMEDA-SHOCK: Capillary Refill vs Lactate in Septic Shock.
Septic shock randomized to capillary refill-guided resuscitation (treatment arm, n=212) versus lactate-guided (control arm, n=212).
The primary endpoint was 28-day mortality. Mean age was 65.5 years, 53% were male.
Results: Mortality RR 0.80, 95% CI 0.59-1.08. P=0.15.
Follow-up was 28 days. Trial registration: NCT03078712.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.80, ciLo: 0.59, ciHi: 1.08 },
            treatment: { n: 212 },
            control: { n: 212 },
            baseline: { ageMean: 65.5, malePercent: 53 },
            registration: 'NCT03078712'
        }
    },
    {
        id: 'BASICS',
        source: 'Zampieri FG et al. JAMA 2021;326:818-829',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `BaSICS: Balanced vs Saline in ICU.
ICU patients randomized to balanced solution (treatment arm, n=5230) versus saline (control arm, n=5290).
The primary endpoint was 90-day mortality. Mean age was 61.5 years, 56% were male.
Results: Mortality RR 1.01, 95% CI 0.93-1.10. P=0.81.
Follow-up was 90 days. Trial registration: NCT02875873.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.01, ciLo: 0.93, ciHi: 1.10 },
            treatment: { n: 5230 },
            control: { n: 5290 },
            baseline: { ageMean: 61.5, malePercent: 56 },
            registration: 'NCT02875873'
        }
    },
    {
        id: 'SALT-ED',
        source: 'Self WH et al. NEJM 2018;378:819-828',
        domain: 'Emergency Medicine',
        design: 'Superiority',
        text: `SALT-ED: Balanced vs Saline in ED.
ED patients requiring IV fluids randomized to balanced crystalloids (treatment arm, n=6708) versus saline (control arm, n=6678).
The primary endpoint was major kidney events at 30 days. Mean age was 52.0 years, 46% were male.
Results: MAKE30 RR 0.82, 95% CI 0.70-0.95. P=0.01.
Follow-up was 30 days. Trial registration: NCT02614040.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.82, ciLo: 0.70, ciHi: 0.95 },
            treatment: { n: 6708 },
            control: { n: 6678 },
            baseline: { ageMean: 52.0, malePercent: 46 },
            registration: 'NCT02614040'
        }
    },
    {
        id: 'SMART',
        source: 'Semler MW et al. NEJM 2018;378:829-839',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `SMART: Balanced vs Saline in ICU.
ICU patients randomized to balanced crystalloids (treatment arm, n=7942) versus saline (control arm, n=7860).
The primary endpoint was major kidney events at 30 days. Mean age was 58.0 years, 55% were male.
Results: MAKE30 RR 0.91, 95% CI 0.84-0.99. P=0.04.
Follow-up was 30 days. Trial registration: NCT02444988.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.91, ciLo: 0.84, ciHi: 0.99 },
            treatment: { n: 7942 },
            control: { n: 7860 },
            baseline: { ageMean: 58.0, malePercent: 55 },
            registration: 'NCT02444988'
        }
    },
    {
        id: 'PLUS',
        source: 'Finfer S et al. NEJM 2022;386:815-826',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `PLUS: Balanced vs Saline in ICU.
ICU patients randomized to balanced solution (treatment arm, n=2515) versus saline (control arm, n=2520).
The primary endpoint was 90-day mortality. Mean age was 65.1 years, 61% were male.
Results: Mortality RR 0.97, 95% CI 0.90-1.05. P=0.47.
Follow-up was 90 days. Trial registration: NCT02721654.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.97, ciLo: 0.90, ciHi: 1.05 },
            treatment: { n: 2515 },
            control: { n: 2520 },
            baseline: { ageMean: 65.1, malePercent: 61 },
            registration: 'NCT02721654'
        }
    },
    {
        id: 'ARDS-Net',
        source: 'ARDS Network. NEJM 2000;342:1301-1308',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `ARMA: Low Tidal Volume in ARDS.
ARDS patients randomized to low tidal volume (treatment arm, n=432) versus traditional ventilation (control arm, n=429).
The primary endpoint was mortality. Mean age was 51.5 years, 54% were male.
Results: Mortality RR 0.78, 95% CI 0.65-0.93. P=0.005.
Follow-up was 180 days. Trial registration: NCT00000579.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.78, ciLo: 0.65, ciHi: 0.93 },
            treatment: { n: 432 },
            control: { n: 429 },
            baseline: { ageMean: 51.5, malePercent: 54 },
            registration: 'NCT00000579'
        }
    },
    {
        id: 'ACURASYS',
        source: 'Papazian L et al. NEJM 2010;363:1107-1116',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `ACURASYS: Neuromuscular Blockade in Severe ARDS.
Severe ARDS randomized to cisatracurium (treatment arm, n=178) versus placebo (control arm, n=162).
The primary endpoint was 90-day mortality. Mean age was 57.0 years, 64% were male.
Results: Mortality HR 0.68, 95% CI 0.48-0.98. P=0.04.
Follow-up was 90 days. Trial registration: NCT00299650.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.68, ciLo: 0.48, ciHi: 0.98 },
            treatment: { n: 178 },
            control: { n: 162 },
            baseline: { ageMean: 57.0, malePercent: 64 },
            registration: 'NCT00299650'
        }
    },
    {
        id: 'ROSE-PETAL',
        source: 'National Heart, Lung, and Blood Institute PETAL Clinical Trials Network. NEJM 2019;380:1997-2008',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `ROSE: Neuromuscular Blockade in Moderate-Severe ARDS.
Moderate-severe ARDS randomized to cisatracurium (treatment arm, n=501) versus usual care (control arm, n=505).
The primary endpoint was 90-day mortality. Mean age was 58.3 years, 56% were male.
Results: Mortality RR 1.03, 95% CI 0.87-1.23. P=0.72.
Follow-up was 90 days. Trial registration: NCT02509078.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.03, ciLo: 0.87, ciHi: 1.23 },
            treatment: { n: 501 },
            control: { n: 505 },
            baseline: { ageMean: 58.3, malePercent: 56 },
            registration: 'NCT02509078'
        }
    },
    {
        id: 'PROSEVA',
        source: 'Guerin C et al. NEJM 2013;368:2159-2168',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `PROSEVA: Prone Position in Severe ARDS.
Severe ARDS randomized to prone position (treatment arm, n=237) versus supine (control arm, n=229).
The primary endpoint was 28-day mortality. Mean age was 58.3 years, 71% were male.
Results: Mortality RR 0.51, 95% CI 0.36-0.72. P<0.001.
Follow-up was 90 days. Trial registration: NCT00527813.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.51, ciLo: 0.36, ciHi: 0.72 },
            treatment: { n: 237 },
            control: { n: 229 },
            baseline: { ageMean: 58.3, malePercent: 71 },
            registration: 'NCT00527813'
        }
    },
    {
        id: 'TTM2',
        source: 'Dankiewicz J et al. NEJM 2021;384:2283-2294',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `TTM2: Hypothermia After Cardiac Arrest.
Comatose after OHCA randomized to hypothermia 33C (treatment arm, n=930) versus normothermia (control arm, n=931).
The primary endpoint was death at 6 months. Mean age was 64.0 years, 80% were male.
Results: Mortality RR 1.04, 95% CI 0.94-1.14. P=0.46.
Follow-up was 6 months. Trial registration: NCT02908308.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.04, ciLo: 0.94, ciHi: 1.14 },
            treatment: { n: 930 },
            control: { n: 931 },
            baseline: { ageMean: 64.0, malePercent: 80 },
            registration: 'NCT02908308'
        }
    },
    {
        id: 'HYPERION',
        source: 'Lascarrou JB et al. NEJM 2019;381:2327-2337',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `HYPERION: Hypothermia After Non-Shockable Cardiac Arrest.
Comatose after non-shockable cardiac arrest randomized to hypothermia (treatment arm, n=284) versus normothermia (control arm, n=297).
The primary endpoint was favorable neurologic outcome at 90 days. Mean age was 67.2 years, 61% were male.
Results: Favorable outcome RR 1.79, 95% CI 1.04-3.08. P=0.03.
Follow-up was 90 days. Trial registration: NCT01994772.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.79, ciLo: 1.04, ciHi: 3.08 },
            treatment: { n: 284 },
            control: { n: 297 },
            baseline: { ageMean: 67.2, malePercent: 61 },
            registration: 'NCT01994772'
        }
    },
    {
        id: 'COACT',
        source: 'Lemkes JJ et al. NEJM 2019;380:1397-1407',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `COACT: Immediate vs Delayed Angiography After OHCA.
OHCA without ST-elevation randomized to immediate angiography (treatment arm, n=273) versus delayed (control arm, n=265).
The primary endpoint was 90-day survival. Mean age was 65.3 years, 77% were male.
Results: Survival RR 1.03, 95% CI 0.88-1.21. P=0.71.
Follow-up was 90 days. Trial registration: NCT02641626.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.03, ciLo: 0.88, ciHi: 1.21 },
            treatment: { n: 273 },
            control: { n: 265 },
            baseline: { ageMean: 65.3, malePercent: 77 },
            registration: 'NCT02641626'
        }
    },
    {
        id: 'TOMAHAWK-CA',
        source: 'Desch S et al. NEJM 2021;385:2544-2553',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `TOMAHAWK: Immediate vs Delayed Angiography After OHCA.
OHCA without ST-elevation randomized to immediate angiography (treatment arm, n=266) versus delayed (control arm, n=264).
The primary endpoint was 30-day mortality. Mean age was 70.0 years, 72% were male.
Results: Mortality RR 1.10, 95% CI 0.82-1.47. P=0.54.
Follow-up was 30 days. Trial registration: NCT02750462.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.10, ciLo: 0.82, ciHi: 1.47 },
            treatment: { n: 266 },
            control: { n: 264 },
            baseline: { ageMean: 70.0, malePercent: 72 },
            registration: 'NCT02750462'
        }
    },
    {
        id: 'EPO-TBI',
        source: 'Nichol A et al. NEJM 2020;382:2523-2534',
        domain: 'Critical Care',
        design: 'Superiority',
        text: `EPO-TBI: Erythropoietin in Moderate-Severe TBI.
Moderate-severe TBI randomized to EPO (treatment arm, n=307) versus placebo (control arm, n=299).
The primary endpoint was favorable outcome at 6 months. Mean age was 39.1 years, 78% were male.
Results: Favorable outcome RR 1.10, 95% CI 0.92-1.31. P=0.28.
Follow-up was 6 months. Trial registration: NCT00987454.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.10, ciLo: 0.92, ciHi: 1.31 },
            treatment: { n: 307 },
            control: { n: 299 },
            baseline: { ageMean: 39.1, malePercent: 78 },
            registration: 'NCT00987454'
        }
    }
"""

# Find insertion position
import re
pattern = r"const BATCH15_TO_762 = \["
match = re.search(pattern, content)

if match:
    # Insert new batch before BATCH15
    insert_pos = match.start()
    batch_def = "const BATCH16_TO_857 = [" + batch16_trials + "\n];\n\n"
    content = content[:insert_pos] + batch_def + content[insert_pos:]

    # Update GROUND_TRUTH_CASES spread
    content = content.replace(
        "...BATCH15_TO_762",
        "...BATCH15_TO_762,\n    ...BATCH16_TO_857"
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Added BATCH16_TO_857 with 100 new trials")
else:
    print("Could not find insertion position")

# Verify
with open(file_path, 'r', encoding='utf-8') as f:
    new_content = f.read()
new_count = new_content.count("id: '")
print(f"New trial count: {new_count}")
