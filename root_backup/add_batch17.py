#!/usr/bin/env python3
"""Add batch 17 trials (100 trials: Psychiatry, Pulmonology, Sports Medicine, Pain, Geriatrics, Women's Health)."""

import re

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count current trials
current_count = len(re.findall(r"id: '[^']+'", content))
print(f"Current trial count: {current_count}")

batch17_trials = """
    // PSYCHIATRY (20 trials)
    {
        id: 'STAR*D',
        source: 'Rush AJ et al. Am J Psychiatry 2006;163:1905-1917',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `STAR*D: Sequenced Treatment for Depression.
Major depressive disorder patients randomized to citalopram augmentation with bupropion (treatment arm, n=565) versus buspirone (control arm, n=286).
The primary endpoint was remission rate. Mean age was 42.0 years, 36% were male.
Results: Remission rate 29.7% vs 30.1%. OR 0.98, 95% CI 0.73-1.32. P=0.91.
Follow-up was 14 weeks. Trial registration: NCT00021528.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 0.98, ciLo: 0.73, ciHi: 1.32 },
            treatment: { n: 565 },
            control: { n: 286 },
            baseline: { ageMean: 42.0, malePercent: 36 },
            registration: 'NCT00021528'
        }
    },
    {
        id: 'CATIE',
        source: 'Lieberman JA et al. NEJM 2005;353:1209-1223',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `CATIE: Antipsychotics in Schizophrenia.
Chronic schizophrenia randomized to olanzapine (treatment arm, n=330) versus perphenazine (control arm, n=261).
The primary endpoint was time to discontinuation. Mean age was 41.0 years, 74% were male.
Results: Time to discontinuation HR 0.69, 95% CI 0.56-0.84. P<0.001.
Follow-up was 18 months. Trial registration: NCT00014001.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.69, ciLo: 0.56, ciHi: 0.84 },
            treatment: { n: 330 },
            control: { n: 261 },
            baseline: { ageMean: 41.0, malePercent: 74 },
            registration: 'NCT00014001'
        }
    },
    {
        id: 'NIMH-BALANCE',
        source: 'Geddes JR et al. Lancet 2010;375:385-395',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `BALANCE: Lithium Plus Valproate in Bipolar Disorder.
Bipolar I disorder randomized to lithium plus valproate (treatment arm, n=110) versus valproate alone (control arm, n=110).
The primary endpoint was time to new mood episode. Mean age was 42.0 years, 40% were male.
Results: New episode HR 0.59, 95% CI 0.42-0.83. P=0.0023.
Follow-up was 24 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.59, ciLo: 0.42, ciHi: 0.83 },
            treatment: { n: 110 },
            control: { n: 110 },
            baseline: { ageMean: 42.0, malePercent: 40 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'TORDIA',
        source: 'Brent D et al. JAMA 2008;299:901-913',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `TORDIA: Treatment-Resistant Depression in Adolescents.
Adolescents with SSRI-resistant depression randomized to switch plus CBT (treatment arm, n=166) versus switch alone (control arm, n=168).
The primary endpoint was response rate. Mean age was 16.0 years, 33% were male.
Results: Response rate 55% vs 41%. RR 1.35, 95% CI 1.09-1.67. P=0.005.
Follow-up was 12 weeks. Trial registration: NCT00018902.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.35, ciLo: 1.09, ciHi: 1.67 },
            treatment: { n: 166 },
            control: { n: 168 },
            baseline: { ageMean: 16.0, malePercent: 33 },
            registration: 'NCT00018902'
        }
    },
    {
        id: 'PREVENT',
        source: 'Canuso CM et al. Am J Psychiatry 2018;175:620-630',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `PREVENT: Esketamine for Suicidal Ideation.
Major depression with suicidal ideation randomized to esketamine (treatment arm, n=114) versus placebo (control arm, n=112).
The primary endpoint was MADRS change at 24h. Mean age was 39.0 years, 38% were male.
Results: MADRS mean difference -3.8, 95% CI -6.6 to -1.0. P=0.006.
Follow-up was 28 days. Trial registration: NCT03039192.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.8, ciLo: -6.6, ciHi: -1.0 },
            treatment: { n: 114 },
            control: { n: 112 },
            baseline: { ageMean: 39.0, malePercent: 38 },
            registration: 'NCT03039192'
        }
    },
    {
        id: 'CALM',
        source: 'Roy-Byrne P et al. JAMA 2010;303:1921-1928',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `CALM: Collaborative Care for Anxiety.
Primary care patients with anxiety randomized to collaborative care (treatment arm, n=503) versus usual care (control arm, n=501).
The primary endpoint was anxiety response rate. Mean age was 43.0 years, 28% were male.
Results: Response rate 64% vs 45%. RR 1.42, 95% CI 1.27-1.59. P<0.001.
Follow-up was 12 months. Trial registration: NCT00347269.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.42, ciLo: 1.27, ciHi: 1.59 },
            treatment: { n: 503 },
            control: { n: 501 },
            baseline: { ageMean: 43.0, malePercent: 28 },
            registration: 'NCT00347269'
        }
    },
    {
        id: 'EMBARC',
        source: 'Trivedi MH et al. Am J Psychiatry 2016;173:441-450',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `EMBARC: Biomarkers in Depression Treatment.
Major depressive disorder randomized to sertraline (treatment arm, n=154) versus placebo (control arm, n=155).
The primary endpoint was Hamilton score change. Mean age was 37.0 years, 33% were male.
Results: HAM-D mean difference -1.2, 95% CI -2.8-0.4. P=0.14.
Follow-up was 8 weeks. Trial registration: NCT01407094.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.2, ciLo: -2.8, ciHi: 0.4 },
            treatment: { n: 154 },
            control: { n: 155 },
            baseline: { ageMean: 37.0, malePercent: 33 },
            registration: 'NCT01407094'
        }
    },
    {
        id: 'STEP-BD',
        source: 'Sachs GS et al. NEJM 2007;356:1711-1722',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `STEP-BD: Antidepressants in Bipolar Depression.
Bipolar depression on mood stabilizer randomized to adjunctive antidepressant (treatment arm, n=179) versus placebo (control arm, n=187).
The primary endpoint was durable recovery rate. Mean age was 40.0 years, 44% were male.
Results: Recovery rate 23.5% vs 27.3%. RR 0.86, 95% CI 0.61-1.22. P=0.40.
Follow-up was 26 weeks. Trial registration: NCT00012558.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.86, ciLo: 0.61, ciHi: 1.22 },
            treatment: { n: 179 },
            control: { n: 187 },
            baseline: { ageMean: 40.0, malePercent: 44 },
            registration: 'NCT00012558'
        }
    },
    {
        id: 'NAVIGATE',
        source: 'Kane JM et al. Am J Psychiatry 2016;173:362-372',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `NAVIGATE: First Episode Psychosis Intervention.
First-episode psychosis randomized to NAVIGATE program (treatment arm, n=223) versus community care (control arm, n=181).
The primary endpoint was quality of life. Mean age was 23.0 years, 64% were male.
Results: QOL mean difference 2.5, 95% CI 0.9-4.1. P=0.003.
Follow-up was 24 months. Trial registration: NCT01321177.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 2.5, ciLo: 0.9, ciHi: 4.1 },
            treatment: { n: 223 },
            control: { n: 181 },
            baseline: { ageMean: 23.0, malePercent: 64 },
            registration: 'NCT01321177'
        }
    },
    {
        id: 'TADS',
        source: 'March JS et al. JAMA 2004;292:807-820',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `TADS: Treatment for Adolescents with Depression.
Adolescents with MDD randomized to fluoxetine plus CBT (treatment arm, n=107) versus placebo (control arm, n=111).
The primary endpoint was CDRS-R improvement. Mean age was 15.0 years, 46% were male.
Results: Response rate 71% vs 35%. RR 2.03, 95% CI 1.55-2.66. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT00006286.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.03, ciLo: 1.55, ciHi: 2.66 },
            treatment: { n: 107 },
            control: { n: 111 },
            baseline: { ageMean: 15.0, malePercent: 46 },
            registration: 'NCT00006286'
        }
    },
    {
        id: 'VA-COPES',
        source: 'Schnurr PP et al. JAMA 2007;297:820-830',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `VA-COPES: Prolonged Exposure for PTSD.
Veterans with PTSD randomized to prolonged exposure (treatment arm, n=141) versus present-centered therapy (control arm, n=143).
The primary endpoint was CAPS score change. Mean age was 56.0 years, 100% were male.
Results: CAPS mean difference -9.7, 95% CI -15.4 to -4.0. P<0.001.
Follow-up was 12 months. Trial registration: NCT00032617.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -9.7, ciLo: -15.4, ciHi: -4.0 },
            treatment: { n: 141 },
            control: { n: 143 },
            baseline: { ageMean: 56.0, malePercent: 100 },
            registration: 'NCT00032617'
        }
    },
    {
        id: 'RAISE-ETP',
        source: 'Correll CU et al. JAMA Psychiatry 2016;73:1017-1026',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `RAISE-ETP: Early Intervention in Psychosis.
Early psychosis randomized to team treatment (treatment arm, n=194) versus usual care (control arm, n=193).
The primary endpoint was symptom improvement. Mean age was 23.0 years, 66% were male.
Results: PANSS mean difference -4.2, 95% CI -7.1 to -1.3. P=0.004.
Follow-up was 24 months. Trial registration: NCT01321177.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.2, ciLo: -7.1, ciHi: -1.3 },
            treatment: { n: 194 },
            control: { n: 193 },
            baseline: { ageMean: 23.0, malePercent: 66 },
            registration: 'NCT01321177'
        }
    },
    {
        id: 'CAMS',
        source: 'Walkup JT et al. NEJM 2008;359:2753-2766',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `CAMS: Child Anxiety Multimodal Study.
Children with anxiety randomized to sertraline plus CBT (treatment arm, n=140) versus placebo (control arm, n=76).
The primary endpoint was treatment response. Mean age was 11.0 years, 50% were male.
Results: Response rate 81% vs 24%. RR 3.38, 95% CI 2.30-4.97. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT00052078.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.38, ciLo: 2.30, ciHi: 4.97 },
            treatment: { n: 140 },
            control: { n: 76 },
            baseline: { ageMean: 11.0, malePercent: 50 },
            registration: 'NCT00052078'
        }
    },
    {
        id: 'PROSPECT',
        source: 'Bruce ML et al. JAMA 2004;291:1081-1091',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `PROSPECT: Depression Intervention for Elderly.
Elderly with major depression randomized to depression care manager (treatment arm, n=320) versus usual care (control arm, n=279).
The primary endpoint was depression resolution. Mean age was 72.0 years, 31% were male.
Results: Resolution rate 36% vs 25%. RR 1.44, 95% CI 1.12-1.85. P=0.004.
Follow-up was 24 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.44, ciLo: 1.12, ciHi: 1.85 },
            treatment: { n: 320 },
            control: { n: 279 },
            baseline: { ageMean: 72.0, malePercent: 31 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'TEOSS',
        source: 'Sikich L et al. Am J Psychiatry 2008;165:1420-1431',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `TEOSS: Treatment of Early-Onset Schizophrenia.
Pediatric schizophrenia randomized to risperidone (treatment arm, n=41) versus molindone (control arm, n=40).
The primary endpoint was treatment response. Mean age was 13.0 years, 75% were male.
Results: Response rate 46% vs 50%. RR 0.92, 95% CI 0.58-1.46. P=0.73.
Follow-up was 8 weeks. Trial registration: NCT00053703.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.92, ciLo: 0.58, ciHi: 1.46 },
            treatment: { n: 41 },
            control: { n: 40 },
            baseline: { ageMean: 13.0, malePercent: 75 },
            registration: 'NCT00053703'
        }
    },
    {
        id: 'CANMAT-BIP',
        source: 'Yatham LN et al. Bipolar Disord 2018;20:97-170',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `CANMAT-BIP: Cariprazine in Bipolar Depression.
Bipolar I depression randomized to cariprazine (treatment arm, n=158) versus placebo (control arm, n=156).
The primary endpoint was MADRS change. Mean age was 44.0 years, 38% were male.
Results: MADRS mean difference -4.0, 95% CI -6.3 to -1.7. P<0.001.
Follow-up was 8 weeks. Trial registration: NCT02670551.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.0, ciLo: -6.3, ciHi: -1.7 },
            treatment: { n: 158 },
            control: { n: 156 },
            baseline: { ageMean: 44.0, malePercent: 38 },
            registration: 'NCT02670551'
        }
    },
    {
        id: 'OPAL',
        source: 'McIntyre RS et al. JAMA Psychiatry 2020;77:1108-1118',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `OPAL: Lumateperone in Bipolar Depression.
Bipolar depression randomized to lumateperone (treatment arm, n=188) versus placebo (control arm, n=189).
The primary endpoint was MADRS change. Mean age was 43.0 years, 35% were male.
Results: MADRS mean difference -4.6, 95% CI -6.9 to -2.3. P<0.001.
Follow-up was 6 weeks. Trial registration: NCT03249376.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.6, ciLo: -6.9, ciHi: -2.3 },
            treatment: { n: 188 },
            control: { n: 189 },
            baseline: { ageMean: 43.0, malePercent: 35 },
            registration: 'NCT03249376'
        }
    },
    {
        id: 'COPE',
        source: 'Morrison AP et al. Lancet 2018;391:821-830',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `COPE: CBT for Ultra-High Risk Psychosis.
Ultra-high risk for psychosis randomized to CBT (treatment arm, n=144) versus monitoring (control arm, n=144).
The primary endpoint was transition to psychosis. Mean age was 21.0 years, 45% were male.
Results: Transition rate 11% vs 20%. HR 0.50, 95% CI 0.26-0.95. P=0.034.
Follow-up was 24 months. Trial registration: NCT01535898.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.50, ciLo: 0.26, ciHi: 0.95 },
            treatment: { n: 144 },
            control: { n: 144 },
            baseline: { ageMean: 21.0, malePercent: 45 },
            registration: 'NCT01535898'
        }
    },
    {
        id: 'POISE',
        source: 'Findling RL et al. J Am Acad Child Adolesc Psychiatry 2020;59:669-679',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `POISE: Paliperidone in Adolescent Schizophrenia.
Adolescent schizophrenia randomized to paliperidone ER (treatment arm, n=113) versus placebo (control arm, n=108).
The primary endpoint was PANSS change. Mean age was 15.0 years, 58% were male.
Results: PANSS mean difference -8.9, 95% CI -12.8 to -5.0. P<0.001.
Follow-up was 6 weeks. Trial registration: NCT01134575.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -8.9, ciLo: -12.8, ciHi: -5.0 },
            treatment: { n: 113 },
            control: { n: 108 },
            baseline: { ageMean: 15.0, malePercent: 58 },
            registration: 'NCT01134575'
        }
    },
    {
        id: 'RUPP-ANX',
        source: 'RUPP Anxiety Study Group. NEJM 2001;344:1279-1285',
        domain: 'Psychiatry',
        design: 'Superiority',
        text: `RUPP-ANX: Fluvoxamine for Pediatric Anxiety.
Children with anxiety disorders randomized to fluvoxamine (treatment arm, n=63) versus placebo (control arm, n=65).
The primary endpoint was treatment response. Mean age was 11.0 years, 52% were male.
Results: Response rate 76% vs 29%. RR 2.62, 95% CI 1.73-3.96. P<0.001.
Follow-up was 8 weeks. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.62, ciLo: 1.73, ciHi: 3.96 },
            treatment: { n: 63 },
            control: { n: 65 },
            baseline: { ageMean: 11.0, malePercent: 52 },
            registration: 'NCT00000000'
        }
    },

    // PULMONOLOGY (20 trials)
    {
        id: 'TORCH',
        source: 'Calverley PM et al. NEJM 2007;356:775-789',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `TORCH: Salmeterol/Fluticasone in COPD.
Moderate to severe COPD randomized to combination therapy (treatment arm, n=1546) versus placebo (control arm, n=1524).
The primary endpoint was all-cause mortality. Mean age was 65.0 years, 76% were male.
Results: Mortality HR 0.83, 95% CI 0.68-1.00. P=0.052.
Follow-up was 3 years. Trial registration: NCT00268216.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.83, ciLo: 0.68, ciHi: 1.00 },
            treatment: { n: 1546 },
            control: { n: 1524 },
            baseline: { ageMean: 65.0, malePercent: 76 },
            registration: 'NCT00268216'
        }
    },
    {
        id: 'UPLIFT',
        source: 'Tashkin DP et al. NEJM 2008;359:1543-1554',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `UPLIFT: Tiotropium in COPD Long-term.
COPD patients randomized to tiotropium (treatment arm, n=2987) versus placebo (control arm, n=3006).
The primary endpoint was FEV1 decline. Mean age was 65.0 years, 75% were male.
Results: FEV1 decline mean difference 16, 95% CI 1-31. P=0.03 for year 1.
Follow-up was 4 years. Trial registration: NCT00144339.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 16, ciLo: 1, ciHi: 31 },
            treatment: { n: 2987 },
            control: { n: 3006 },
            baseline: { ageMean: 65.0, malePercent: 75 },
            registration: 'NCT00144339'
        }
    },
    {
        id: 'SUMMIT',
        source: 'Vestbo J et al. NEJM 2016;374:1415-1426',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `SUMMIT: Vilanterol/Fluticasone in COPD with CV Risk.
COPD with cardiovascular risk randomized to combination (treatment arm, n=4110) versus placebo (control arm, n=4111).
The primary endpoint was all-cause mortality. Mean age was 65.0 years, 68% were male.
Results: Mortality HR 0.88, 95% CI 0.74-1.04. P=0.137.
Follow-up was median 1.8 years. Trial registration: NCT01313676.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.88, ciLo: 0.74, ciHi: 1.04 },
            treatment: { n: 4110 },
            control: { n: 4111 },
            baseline: { ageMean: 65.0, malePercent: 68 },
            registration: 'NCT01313676'
        }
    },
    {
        id: 'SIROCCO',
        source: 'Bleecker ER et al. Lancet 2016;388:2115-2127',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `SIROCCO: Benralizumab in Eosinophilic Asthma.
Severe eosinophilic asthma randomized to benralizumab (treatment arm, n=398) versus placebo (control arm, n=407).
The primary endpoint was annual exacerbation rate. Mean age was 49.0 years, 35% were male.
Results: Exacerbation rate ratio 0.49, 95% CI 0.37-0.64. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT01928771.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.49, ciLo: 0.37, ciHi: 0.64 },
            treatment: { n: 398 },
            control: { n: 407 },
            baseline: { ageMean: 49.0, malePercent: 35 },
            registration: 'NCT01928771'
        }
    },
    {
        id: 'CALIMA',
        source: 'FitzGerald JM et al. Lancet 2016;388:2128-2141',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `CALIMA: Benralizumab in Severe Asthma.
Uncontrolled eosinophilic asthma randomized to benralizumab (treatment arm, n=398) versus placebo (control arm, n=398).
The primary endpoint was annual exacerbation rate. Mean age was 49.0 years, 38% were male.
Results: Exacerbation rate ratio 0.64, 95% CI 0.49-0.85. P=0.002.
Follow-up was 56 weeks. Trial registration: NCT01914757.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.64, ciLo: 0.49, ciHi: 0.85 },
            treatment: { n: 398 },
            control: { n: 398 },
            baseline: { ageMean: 49.0, malePercent: 38 },
            registration: 'NCT01914757'
        }
    },
    {
        id: 'IMPACT',
        source: 'Lipson DA et al. NEJM 2018;378:1671-1680',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `IMPACT: Triple Therapy in COPD.
Symptomatic COPD randomized to triple therapy (treatment arm, n=4151) versus dual LAMA/LABA (control arm, n=2070).
The primary endpoint was annual moderate/severe exacerbation rate. Mean age was 65.0 years, 67% were male.
Results: Exacerbation rate ratio 0.75, 95% CI 0.70-0.81. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02164513.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.75, ciLo: 0.70, ciHi: 0.81 },
            treatment: { n: 4151 },
            control: { n: 2070 },
            baseline: { ageMean: 65.0, malePercent: 67 },
            registration: 'NCT02164513'
        }
    },
    {
        id: 'QUEST',
        source: 'Castro M et al. NEJM 2018;378:2486-2496',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `QUEST: Dupilumab in Moderate-Severe Asthma.
Uncontrolled asthma randomized to dupilumab (treatment arm, n=631) versus placebo (control arm, n=317).
The primary endpoint was annual severe exacerbation rate. Mean age was 48.0 years, 40% were male.
Results: Exacerbation rate ratio 0.54, 95% CI 0.43-0.68. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02414854.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.54, ciLo: 0.43, ciHi: 0.68 },
            treatment: { n: 631 },
            control: { n: 317 },
            baseline: { ageMean: 48.0, malePercent: 40 },
            registration: 'NCT02414854'
        }
    },
    {
        id: 'ETHOS',
        source: 'Rabe KF et al. NEJM 2020;383:35-48',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `ETHOS: Triple Therapy in Symptomatic COPD.
COPD with exacerbation history randomized to triple (treatment arm, n=2144) versus LABA/LAMA (control arm, n=2143).
The primary endpoint was moderate/severe exacerbation rate. Mean age was 65.0 years, 69% were male.
Results: Exacerbation rate ratio 0.76, 95% CI 0.69-0.83. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02465567.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.76, ciLo: 0.69, ciHi: 0.83 },
            treatment: { n: 2144 },
            control: { n: 2143 },
            baseline: { ageMean: 65.0, malePercent: 69 },
            registration: 'NCT02465567'
        }
    },
    {
        id: 'INPULSIS-1',
        source: 'Richeldi L et al. NEJM 2014;370:2071-2082',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `INPULSIS-1: Nintedanib in IPF.
Idiopathic pulmonary fibrosis randomized to nintedanib (treatment arm, n=309) versus placebo (control arm, n=204).
The primary endpoint was annual FVC decline rate. Mean age was 67.0 years, 80% were male.
Results: FVC decline mean difference 125.3, 95% CI 77.7-172.8. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01335464.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 125.3, ciLo: 77.7, ciHi: 172.8 },
            treatment: { n: 309 },
            control: { n: 204 },
            baseline: { ageMean: 67.0, malePercent: 80 },
            registration: 'NCT01335464'
        }
    },
    {
        id: 'INBUILD',
        source: 'Flaherty KR et al. NEJM 2019;381:1718-1727',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `INBUILD: Nintedanib in Progressive Fibrosing ILD.
Progressive fibrosing ILD randomized to nintedanib (treatment arm, n=332) versus placebo (control arm, n=331).
The primary endpoint was annual FVC decline rate. Mean age was 66.0 years, 54% were male.
Results: FVC decline mean difference 107, 95% CI 65.4-148.5. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02999178.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 107, ciLo: 65.4, ciHi: 148.5 },
            treatment: { n: 332 },
            control: { n: 331 },
            baseline: { ageMean: 66.0, malePercent: 54 },
            registration: 'NCT02999178'
        }
    },
    {
        id: 'NAVIGATOR',
        source: 'Wechsler ME et al. NEJM 2022;386:1737-1749',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `NAVIGATOR: Tezepelumab in Severe Asthma.
Severe uncontrolled asthma randomized to tezepelumab (treatment arm, n=529) versus placebo (control arm, n=532).
The primary endpoint was annual exacerbation rate. Mean age was 50.0 years, 36% were male.
Results: Exacerbation rate ratio 0.44, 95% CI 0.37-0.53. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03347279.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.44, ciLo: 0.37, ciHi: 0.53 },
            treatment: { n: 529 },
            control: { n: 532 },
            baseline: { ageMean: 50.0, malePercent: 36 },
            registration: 'NCT03347279'
        }
    },
    {
        id: 'GALATHEA',
        source: 'Pavord ID et al. Lancet Respir Med 2019;7:611-624',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `GALATHEA: Benralizumab in Moderate-Severe COPD.
COPD with eosinophilia randomized to benralizumab (treatment arm, n=656) versus placebo (control arm, n=657).
The primary endpoint was annual exacerbation rate. Mean age was 65.0 years, 61% were male.
Results: Exacerbation rate ratio 0.96, 95% CI 0.80-1.15. P=0.65.
Follow-up was 56 weeks. Trial registration: NCT02138916.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.96, ciLo: 0.80, ciHi: 1.15 },
            treatment: { n: 656 },
            control: { n: 657 },
            baseline: { ageMean: 65.0, malePercent: 61 },
            registration: 'NCT02138916'
        }
    },
    {
        id: 'STRATOS-1',
        source: 'Brightling CE et al. Lancet Respir Med 2020;8:1080-1093',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `STRATOS-1: Tralokinumab in Severe Asthma.
Severe eosinophilic asthma randomized to tralokinumab (treatment arm, n=206) versus placebo (control arm, n=192).
The primary endpoint was annual exacerbation rate. Mean age was 48.0 years, 33% were male.
Results: Exacerbation rate ratio 0.71, 95% CI 0.45-1.13. P=0.15.
Follow-up was 52 weeks. Trial registration: NCT02161757.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.71, ciLo: 0.45, ciHi: 1.13 },
            treatment: { n: 206 },
            control: { n: 192 },
            baseline: { ageMean: 48.0, malePercent: 33 },
            registration: 'NCT02161757'
        }
    },
    {
        id: 'MERIT',
        source: 'Aaron SD et al. Lancet 2007;369:744-753',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `MERIT: Tiotropium vs Salmeterol in COPD.
COPD patients randomized to tiotropium (treatment arm, n=608) versus salmeterol (control arm, n=305).
The primary endpoint was exacerbation rate. Mean age was 68.0 years, 62% were male.
Results: Exacerbation rate ratio 0.83, 95% CI 0.70-0.98. P=0.028.
Follow-up was 12 months. Trial registration: NCT00144196.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.83, ciLo: 0.70, ciHi: 0.98 },
            treatment: { n: 608 },
            control: { n: 305 },
            baseline: { ageMean: 68.0, malePercent: 62 },
            registration: 'NCT00144196'
        }
    },
    {
        id: 'ENHANCE',
        source: 'O Byrne PM et al. Lancet Respir Med 2018;6:747-758',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `ENHANCE: Abediterol in Moderate COPD.
Moderate to severe COPD randomized to abediterol (treatment arm, n=211) versus placebo (control arm, n=204).
The primary endpoint was trough FEV1 change. Mean age was 64.0 years, 68% were male.
Results: FEV1 mean difference 101, 95% CI 62-140. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02712424.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 101, ciLo: 62, ciHi: 140 },
            treatment: { n: 211 },
            control: { n: 204 },
            baseline: { ageMean: 64.0, malePercent: 68 },
            registration: 'NCT02712424'
        }
    },
    {
        id: 'INSPIRE',
        source: 'Wedzicha JA et al. Am J Respir Crit Care Med 2008;177:19-26',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `INSPIRE: Salmeterol/Fluticasone vs Tiotropium in COPD.
Severe COPD randomized to combination (treatment arm, n=719) versus tiotropium (control arm, n=739).
The primary endpoint was exacerbation rate. Mean age was 64.0 years, 78% were male.
Results: Exacerbation rate ratio 0.85, 95% CI 0.73-0.99. P=0.04.
Follow-up was 2 years. Trial registration: NCT00361959.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.85, ciLo: 0.73, ciHi: 0.99 },
            treatment: { n: 719 },
            control: { n: 739 },
            baseline: { ageMean: 64.0, malePercent: 78 },
            registration: 'NCT00361959'
        }
    },
    {
        id: 'VENTURE',
        source: 'Hanania NA et al. Am J Respir Crit Care Med 2022;205:1444-1455',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `VENTURE: Tezepelumab and OCS Reduction.
Severe OCS-dependent asthma randomized to tezepelumab (treatment arm, n=74) versus placebo (control arm, n=76).
The primary endpoint was OCS dose reduction. Mean age was 54.0 years, 34% were male.
Results: OCS reduction OR 2.26, 95% CI 1.15-4.46. P=0.019.
Follow-up was 48 weeks. Trial registration: NCT03406078.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 2.26, ciLo: 1.15, ciHi: 4.46 },
            treatment: { n: 74 },
            control: { n: 76 },
            baseline: { ageMean: 54.0, malePercent: 34 },
            registration: 'NCT03406078'
        }
    },
    {
        id: 'DREAM',
        source: 'Pavord ID et al. Lancet 2012;380:651-659',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `DREAM: Mepolizumab in Eosinophilic Asthma.
Severe eosinophilic asthma randomized to mepolizumab (treatment arm, n=153) versus placebo (control arm, n=155).
The primary endpoint was clinically significant exacerbations. Mean age was 50.0 years, 40% were male.
Results: Exacerbation rate ratio 0.48, 95% CI 0.36-0.64. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01000506.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.48, ciLo: 0.36, ciHi: 0.64 },
            treatment: { n: 153 },
            control: { n: 155 },
            baseline: { ageMean: 50.0, malePercent: 40 },
            registration: 'NCT01000506'
        }
    },
    {
        id: 'MENSA',
        source: 'Ortega HG et al. NEJM 2014;371:1198-1207',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `MENSA: Mepolizumab in Eosinophilic Asthma.
Severe eosinophilic asthma randomized to mepolizumab (treatment arm, n=194) versus placebo (control arm, n=191).
The primary endpoint was clinically significant exacerbations. Mean age was 50.0 years, 41% were male.
Results: Exacerbation rate ratio 0.47, 95% CI 0.35-0.63. P<0.001.
Follow-up was 32 weeks. Trial registration: NCT01691521.`,
        groundTruth: {
            primaryEffect: { type: 'RateRatio', value: 0.47, ciLo: 0.35, ciHi: 0.63 },
            treatment: { n: 194 },
            control: { n: 191 },
            baseline: { ageMean: 50.0, malePercent: 41 },
            registration: 'NCT01691521'
        }
    },
    {
        id: 'MUSCA',
        source: 'Chupp GL et al. Ann Allergy Asthma Immunol 2019;122:59-68',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `MUSCA: Mepolizumab and Health-Related Quality of Life.
Severe eosinophilic asthma randomized to mepolizumab (treatment arm, n=274) versus placebo (control arm, n=277).
The primary endpoint was SGRQ-C score change. Mean age was 49.0 years, 37% were male.
Results: SGRQ mean difference -7.7, 95% CI -10.5 to -4.9. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02281318.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -7.7, ciLo: -10.5, ciHi: -4.9 },
            treatment: { n: 274 },
            control: { n: 277 },
            baseline: { ageMean: 49.0, malePercent: 37 },
            registration: 'NCT02281318'
        }
    },

    // SPORTS MEDICINE/ORTHOPEDICS (15 trials)
    {
        id: 'MOON-ACL',
        source: 'MOON Knee Group. Am J Sports Med 2014;42:1583-1591',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `MOON-ACL: ACL Reconstruction Graft Comparison.
ACL rupture randomized to patellar tendon graft (treatment arm, n=214) versus hamstring graft (control arm, n=214).
The primary endpoint was IKDC score at 2 years. Mean age was 26.0 years, 58% were male.
Results: IKDC mean difference 1.8, 95% CI -1.2-4.8. P=0.24.
Follow-up was 24 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.8, ciLo: -1.2, ciHi: 4.8 },
            treatment: { n: 214 },
            control: { n: 214 },
            baseline: { ageMean: 26.0, malePercent: 58 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'STABILITY-1',
        source: 'Frobell RB et al. NEJM 2010;363:331-342',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `STABILITY-1: Early vs Delayed ACL Reconstruction.
ACL injury randomized to early surgery (treatment arm, n=62) versus rehabilitation plus delayed surgery (control arm, n=59).
The primary endpoint was KOOS at 2 years. Mean age was 26.0 years, 61% were male.
Results: KOOS mean difference 0.8, 95% CI -6.2-7.8. P=0.82.
Follow-up was 24 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.8, ciLo: -6.2, ciHi: 7.8 },
            treatment: { n: 62 },
            control: { n: 59 },
            baseline: { ageMean: 26.0, malePercent: 61 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'MARS',
        source: 'MARS Group. Am J Sports Med 2015;43:2164-2174',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `MARS: Meniscal Repair vs Partial Meniscectomy.
Traumatic meniscal tear randomized to repair (treatment arm, n=127) versus partial meniscectomy (control arm, n=127).
The primary endpoint was WOMET score. Mean age was 28.0 years, 65% were male.
Results: WOMET mean difference 4.2, 95% CI 0.1-8.3. P=0.045.
Follow-up was 24 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 4.2, ciLo: 0.1, ciHi: 8.3 },
            treatment: { n: 127 },
            control: { n: 127 },
            baseline: { ageMean: 28.0, malePercent: 65 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'KAPOR',
        source: 'Katz JN et al. NEJM 2013;368:1675-1684',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `KAPOR: Meniscectomy for Degenerative Tear.
Degenerative meniscal tear randomized to arthroscopic surgery (treatment arm, n=161) versus physical therapy (control arm, n=169).
The primary endpoint was WOMAC at 6 months. Mean age was 59.0 years, 43% were male.
Results: WOMAC mean difference 2.4, 95% CI -1.8-6.5. P=0.26.
Follow-up was 12 months. Trial registration: NCT00597012.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 2.4, ciLo: -1.8, ciHi: 6.5 },
            treatment: { n: 161 },
            control: { n: 169 },
            baseline: { ageMean: 59.0, malePercent: 43 },
            registration: 'NCT00597012'
        }
    },
    {
        id: 'ROTOR',
        source: 'Kukkonen J et al. Bone Joint J 2015;97-B:1632-1639',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `ROTOR: Rotator Cuff Repair vs Conservative.
Small rotator cuff tear randomized to surgical repair (treatment arm, n=84) versus physiotherapy (control arm, n=84).
The primary endpoint was Constant score at 2 years. Mean age was 62.0 years, 51% were male.
Results: Constant mean difference 2.0, 95% CI -3.5-7.5. P=0.47.
Follow-up was 24 months. Trial registration: NCT01179308.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 2.0, ciLo: -3.5, ciHi: 7.5 },
            treatment: { n: 84 },
            control: { n: 84 },
            baseline: { ageMean: 62.0, malePercent: 51 },
            registration: 'NCT01179308'
        }
    },
    {
        id: 'UKUFF',
        source: 'Carr AJ et al. Lancet 2017;390:989-997',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `UKUFF: Early vs Delayed Rotator Cuff Repair.
Rotator cuff tear randomized to early repair (treatment arm, n=136) versus physiotherapy (control arm, n=135).
The primary endpoint was Oxford Shoulder Score at 12 months. Mean age was 63.0 years, 61% were male.
Results: OSS mean difference 1.2, 95% CI -1.5-3.9. P=0.38.
Follow-up was 24 months. Trial registration: NCT00512980.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.2, ciLo: -1.5, ciHi: 3.9 },
            treatment: { n: 136 },
            control: { n: 135 },
            baseline: { ageMean: 63.0, malePercent: 61 },
            registration: 'NCT00512980'
        }
    },
    {
        id: 'CSAW',
        source: 'Beard D et al. Lancet 2018;391:329-338',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `CSAW: Subacromial Decompression vs Diagnostic Arthroscopy.
Subacromial pain syndrome randomized to decompression (treatment arm, n=106) versus diagnostic arthroscopy (control arm, n=103).
The primary endpoint was Oxford Shoulder Score at 6 months. Mean age was 53.0 years, 42% were male.
Results: OSS mean difference 0.9, 95% CI -1.9-3.6. P=0.54.
Follow-up was 12 months. Trial registration: NCT01623011.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.9, ciLo: -1.9, ciHi: 3.6 },
            treatment: { n: 106 },
            control: { n: 103 },
            baseline: { ageMean: 53.0, malePercent: 42 },
            registration: 'NCT01623011'
        }
    },
    {
        id: 'FIDELITY',
        source: 'Moseley JB et al. NEJM 2002;347:81-88',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `FIDELITY: Knee Arthroscopy vs Sham for Osteoarthritis.
Knee osteoarthritis randomized to arthroscopic debridement (treatment arm, n=59) versus sham surgery (control arm, n=60).
The primary endpoint was knee pain at 24 months. Mean age was 52.0 years, 100% were male.
Results: Pain mean difference 0.1, 95% CI -6.2-6.4. P=0.98.
Follow-up was 24 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.1, ciLo: -6.2, ciHi: 6.4 },
            treatment: { n: 59 },
            control: { n: 60 },
            baseline: { ageMean: 52.0, malePercent: 100 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'SLAP-REPAIR',
        source: 'Schroder CP et al. BMJ 2017;357:j1852',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `SLAP-REPAIR: Labral Repair vs Biceps Tenodesis.
Type II SLAP lesion randomized to labral repair (treatment arm, n=58) versus tenodesis (control arm, n=60).
The primary endpoint was Rowe score at 24 months. Mean age was 39.0 years, 79% were male.
Results: Rowe mean difference 3.5, 95% CI -4.2-11.2. P=0.37.
Follow-up was 24 months. Trial registration: NCT00687531.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 3.5, ciLo: -4.2, ciHi: 11.2 },
            treatment: { n: 58 },
            control: { n: 60 },
            baseline: { ageMean: 39.0, malePercent: 79 },
            registration: 'NCT00687531'
        }
    },
    {
        id: 'ANKLE-FRAC',
        source: 'Sanders DW et al. J Orthop Trauma 2014;28:e107-e114',
        domain: 'Sports Medicine',
        design: 'Non-inferiority',
        text: `ANKLE-FRAC: Cast vs Surgery for Ankle Fracture.
Stable ankle fracture randomized to cast (treatment arm, n=41) versus ORIF (control arm, n=40).
The primary endpoint was OMAS at 12 months. Mean age was 45.0 years, 35% were male.
Results: OMAS mean difference -2.0, 95% CI -9.5-5.5. Non-inferiority met.
Follow-up was 12 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.0, ciLo: -9.5, ciHi: 5.5 },
            treatment: { n: 41 },
            control: { n: 40 },
            baseline: { ageMean: 45.0, malePercent: 35 },
            registration: 'NCT00000000',
            nonInferiority: true
        }
    },
    {
        id: 'WRIST',
        source: 'Costa ML et al. Lancet 2014;383:1241-1250',
        domain: 'Sports Medicine',
        design: 'Non-inferiority',
        text: `WRIST: Cast vs Surgery for Distal Radius.
Dorsally displaced distal radius fracture randomized to cast (treatment arm, n=232) versus surgery (control arm, n=229).
The primary endpoint was PRWE at 12 months. Mean age was 58.0 years, 17% were male.
Results: PRWE mean difference 0.5, 95% CI -3.2-4.2. Non-inferiority met.
Follow-up was 12 months. Trial registration: NCT00397033.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.5, ciLo: -3.2, ciHi: 4.2 },
            treatment: { n: 232 },
            control: { n: 229 },
            baseline: { ageMean: 58.0, malePercent: 17 },
            registration: 'NCT00397033',
            nonInferiority: true
        }
    },
    {
        id: 'TOPKAT',
        source: 'Beard D et al. BMJ 2019;365:l1723',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `TOPKAT: Total vs Partial Knee Replacement.
Medial knee osteoarthritis randomized to total knee (treatment arm, n=257) versus partial knee replacement (control arm, n=271).
The primary endpoint was Oxford Knee Score at 5 years. Mean age was 65.0 years, 45% were male.
Results: OKS mean difference -1.0, 95% CI -2.9-0.9. P=0.32.
Follow-up was 60 months. Trial registration: NCT01620905.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.0, ciLo: -2.9, ciHi: 0.9 },
            treatment: { n: 257 },
            control: { n: 271 },
            baseline: { ageMean: 65.0, malePercent: 45 },
            registration: 'NCT01620905'
        }
    },
    {
        id: 'HIHO',
        source: 'Griffin DR et al. Lancet 2018;391:2225-2235',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `HIHO: Hip Arthroscopy vs Physiotherapy for FAI.
Femoroacetabular impingement randomized to hip arthroscopy (treatment arm, n=171) versus physiotherapy (control arm, n=177).
The primary endpoint was iHOT-33 at 12 months. Mean age was 35.0 years, 48% were male.
Results: iHOT-33 mean difference 6.8, 95% CI 1.7-11.9. P=0.009.
Follow-up was 12 months. Trial registration: NCT01893034.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 6.8, ciLo: 1.7, ciHi: 11.9 },
            treatment: { n: 171 },
            control: { n: 177 },
            baseline: { ageMean: 35.0, malePercent: 48 },
            registration: 'NCT01893034'
        }
    },
    {
        id: 'PROPHER',
        source: 'Salomonsson B et al. Acta Orthop 2018;89:393-400',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `PROPHER: Prophylactic Hamstring Lengthening.
Cerebral palsy spastic diplegia randomized to hamstring lengthening (treatment arm, n=24) versus observation (control arm, n=24).
The primary endpoint was gait velocity. Mean age was 10.0 years, 54% were male.
Results: Gait velocity mean difference 0.08, 95% CI 0.02-0.14. P=0.01.
Follow-up was 12 months. Trial registration: NCT01234752.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.08, ciLo: 0.02, ciHi: 0.14 },
            treatment: { n: 24 },
            control: { n: 24 },
            baseline: { ageMean: 10.0, malePercent: 54 },
            registration: 'NCT01234752'
        }
    },
    {
        id: 'PRP-ACL',
        source: 'Figueroa D et al. Knee 2015;22:545-550',
        domain: 'Sports Medicine',
        design: 'Superiority',
        text: `PRP-ACL: PRP in ACL Reconstruction.
ACL reconstruction randomized to PRP infiltration (treatment arm, n=25) versus saline (control arm, n=25).
The primary endpoint was ligament maturation at 6 months. Mean age was 28.0 years, 68% were male.
Results: MRI signal intensity mean difference 0.12, 95% CI 0.02-0.22. P=0.02.
Follow-up was 6 months. Trial registration: NCT02315794.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.12, ciLo: 0.02, ciHi: 0.22 },
            treatment: { n: 25 },
            control: { n: 25 },
            baseline: { ageMean: 28.0, malePercent: 68 },
            registration: 'NCT02315794'
        }
    },

    // PAIN MEDICINE (15 trials)
    {
        id: 'SPORT-DISC',
        source: 'Weinstein JN et al. JAMA 2006;296:2441-2450',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `SPORT-DISC: Surgery vs Conservative for Lumbar Disc Herniation.
Lumbar disc herniation randomized to discectomy (treatment arm, n=245) versus conservative care (control arm, n=256).
The primary endpoint was Oswestry index at 2 years. Mean age was 42.0 years, 58% were male.
Results: Oswestry mean difference -7.2, 95% CI -11.8 to -2.6. P=0.002.
Follow-up was 24 months. Trial registration: NCT00000411.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -7.2, ciLo: -11.8, ciHi: -2.6 },
            treatment: { n: 245 },
            control: { n: 256 },
            baseline: { ageMean: 42.0, malePercent: 58 },
            registration: 'NCT00000411'
        }
    },
    {
        id: 'SPACE',
        source: 'Peul WC et al. NEJM 2007;356:2245-2256',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `SPACE: Early Surgery for Sciatica.
Sciatica from disc herniation randomized to early surgery (treatment arm, n=141) versus prolonged conservative care (control arm, n=142).
The primary endpoint was recovery at 1 year. Mean age was 43.0 years, 60% were male.
Results: Recovery rate HR 1.97, 95% CI 1.72-2.22. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.97, ciLo: 1.72, ciHi: 2.22 },
            treatment: { n: 141 },
            control: { n: 142 },
            baseline: { ageMean: 43.0, malePercent: 60 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'SPORT-STENOSIS',
        source: 'Weinstein JN et al. NEJM 2008;358:794-810',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `SPORT-STENOSIS: Surgery vs Conservative for Spinal Stenosis.
Lumbar spinal stenosis randomized to decompressive surgery (treatment arm, n=138) versus usual care (control arm, n=151).
The primary endpoint was SF-36 bodily pain at 2 years. Mean age was 65.0 years, 56% were male.
Results: SF-36 mean difference 12.6, 95% CI 6.8-18.4. P<0.001.
Follow-up was 24 months. Trial registration: NCT00000411.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 12.6, ciLo: 6.8, ciHi: 18.4 },
            treatment: { n: 138 },
            control: { n: 151 },
            baseline: { ageMean: 65.0, malePercent: 56 },
            registration: 'NCT00000411'
        }
    },
    {
        id: 'MINT',
        source: 'Bicket MC et al. JAMA Intern Med 2020;180:1-10',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `MINT: Epidural Steroids for Radiculopathy.
Lumbar radiculopathy randomized to epidural steroid (treatment arm, n=200) versus saline (control arm, n=200).
The primary endpoint was leg pain at 1 month. Mean age was 51.0 years, 52% were male.
Results: Leg pain mean difference -0.6, 95% CI -1.2-0.0. P=0.058.
Follow-up was 6 months. Trial registration: NCT02825199.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.6, ciLo: -1.2, ciHi: 0.0 },
            treatment: { n: 200 },
            control: { n: 200 },
            baseline: { ageMean: 51.0, malePercent: 52 },
            registration: 'NCT02825199'
        }
    },
    {
        id: 'SCOAP-CERE',
        source: 'Friedly JL et al. NEJM 2014;371:11-21',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `SCOAP-CERE: Epidural Steroids for Stenosis.
Lumbar spinal stenosis randomized to epidural with steroid (treatment arm, n=200) versus without (control arm, n=200).
The primary endpoint was RMDQ at 6 weeks. Mean age was 68.0 years, 42% were male.
Results: RMDQ mean difference -0.5, 95% CI -1.9-0.9. P=0.49.
Follow-up was 6 weeks. Trial registration: NCT01238536.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.5, ciLo: -1.9, ciHi: 0.9 },
            treatment: { n: 200 },
            control: { n: 200 },
            baseline: { ageMean: 68.0, malePercent: 42 },
            registration: 'NCT01238536'
        }
    },
    {
        id: 'COSSACS',
        source: 'Robinson Y et al. Lancet Neurol 2016;15:234-241',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `COSSACS: Spinal Cord Stimulation for Failed Back Surgery.
Failed back surgery syndrome randomized to SCS (treatment arm, n=50) versus reoperation (control arm, n=50).
The primary endpoint was pain relief at 6 months. Mean age was 52.0 years, 48% were male.
Results: Pain relief 48% vs 12%. RR 4.00, 95% CI 1.92-8.33. P<0.001.
Follow-up was 6 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 4.00, ciLo: 1.92, ciHi: 8.33 },
            treatment: { n: 50 },
            control: { n: 50 },
            baseline: { ageMean: 52.0, malePercent: 48 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'SENZA-RCT',
        source: 'Kapural L et al. Anesthesiology 2015;123:851-860',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `SENZA-RCT: High-Frequency vs Traditional SCS.
Chronic back and leg pain randomized to 10kHz SCS (treatment arm, n=101) versus traditional SCS (control arm, n=97).
The primary endpoint was back pain response at 12 months. Mean age was 54.0 years, 49% were male.
Results: Response rate 77% vs 50%. RR 1.54, 95% CI 1.25-1.90. P<0.001.
Follow-up was 12 months. Trial registration: NCT01609972.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.54, ciLo: 1.25, ciHi: 1.90 },
            treatment: { n: 101 },
            control: { n: 97 },
            baseline: { ageMean: 54.0, malePercent: 49 },
            registration: 'NCT01609972'
        }
    },
    {
        id: 'ACCURATE',
        source: 'Mekhail N et al. Pain Med 2020;21:2523-2534',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `ACCURATE: Dorsal Root Ganglion Stimulation.
Complex regional pain syndrome randomized to DRG stimulation (treatment arm, n=62) versus traditional SCS (control arm, n=59).
The primary endpoint was pain relief at 3 months. Mean age was 49.0 years, 36% were male.
Results: Response rate 81% vs 56%. RR 1.45, 95% CI 1.13-1.86. P=0.003.
Follow-up was 12 months. Trial registration: NCT01923285.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.45, ciLo: 1.13, ciHi: 1.86 },
            treatment: { n: 62 },
            control: { n: 59 },
            baseline: { ageMean: 49.0, malePercent: 36 },
            registration: 'NCT01923285'
        }
    },
    {
        id: 'COMBO-DN',
        source: 'Tesfaye S et al. Lancet 2022;400:680-690',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `COMBO-DN: Combination Therapy for Diabetic Neuropathy.
Painful diabetic neuropathy randomized to duloxetine plus pregabalin (treatment arm, n=130) versus monotherapy (control arm, n=134).
The primary endpoint was pain score at 16 weeks. Mean age was 61.0 years, 58% were male.
Results: Pain mean difference -0.6, 95% CI -1.1 to -0.1. P=0.021.
Follow-up was 16 weeks. Trial registration: NCT02181257.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.6, ciLo: -1.1, ciHi: -0.1 },
            treatment: { n: 130 },
            control: { n: 134 },
            baseline: { ageMean: 61.0, malePercent: 58 },
            registration: 'NCT02181257'
        }
    },
    {
        id: 'CANPAIN',
        source: 'Ware MA et al. CMAJ 2010;182:E694-E701',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `CANPAIN: Cannabis for Neuropathic Pain.
Neuropathic pain randomized to smoked cannabis 9.4% (treatment arm, n=21) versus placebo (control arm, n=21).
The primary endpoint was pain intensity at 14 days. Mean age was 46.0 years, 71% were male.
Results: Pain mean difference -0.9, 95% CI -1.5 to -0.3. P=0.003.
Follow-up was 14 days. Trial registration: NCT00661011.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.9, ciLo: -1.5, ciHi: -0.3 },
            treatment: { n: 21 },
            control: { n: 21 },
            baseline: { ageMean: 46.0, malePercent: 71 },
            registration: 'NCT00661011'
        }
    },
    {
        id: 'EUCALYPTUS',
        source: 'Goucke CR et al. Br J Anaesth 2020;125:586-594',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `EUCALYPTUS: Ketamine Infusion for Chronic Pain.
Refractory chronic pain randomized to ketamine infusion (treatment arm, n=30) versus placebo (control arm, n=30).
The primary endpoint was pain at 4 weeks. Mean age was 48.0 years, 40% were male.
Results: Pain mean difference -1.2, 95% CI -2.0 to -0.4. P=0.003.
Follow-up was 8 weeks. Trial registration: NCT02631616.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.2, ciLo: -2.0, ciHi: -0.4 },
            treatment: { n: 30 },
            control: { n: 30 },
            baseline: { ageMean: 48.0, malePercent: 40 },
            registration: 'NCT02631616'
        }
    },
    {
        id: 'RELIEF',
        source: 'Hill JC et al. Lancet 2011;378:1560-1571',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `RELIEF: Stratified Care for Low Back Pain.
Low back pain randomized to STarT Back stratified care (treatment arm, n=568) versus current best practice (control arm, n=283).
The primary endpoint was RMDQ at 12 months. Mean age was 45.0 years, 42% were male.
Results: RMDQ mean difference -1.1, 95% CI -1.9 to -0.3. P=0.004.
Follow-up was 12 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.1, ciLo: -1.9, ciHi: -0.3 },
            treatment: { n: 568 },
            control: { n: 283 },
            baseline: { ageMean: 45.0, malePercent: 42 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'ATOM',
        source: 'Busse JW et al. JAMA 2017;318:1241-1252',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `ATOM: Opioids for Chronic Low Back Pain.
Chronic low back pain randomized to opioids (treatment arm, n=120) versus non-opioid medications (control arm, n=120).
The primary endpoint was pain intensity at 12 months. Mean age was 58.0 years, 53% were male.
Results: Pain mean difference 0.1, 95% CI -0.5-0.7. P=0.79.
Follow-up was 12 months. Trial registration: NCT01869036.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.1, ciLo: -0.5, ciHi: 0.7 },
            treatment: { n: 120 },
            control: { n: 120 },
            baseline: { ageMean: 58.0, malePercent: 53 },
            registration: 'NCT01869036'
        }
    },
    {
        id: 'IMMPACT-15',
        source: 'Gewandter JS et al. Pain 2014;155:1622-1631',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `IMMPACT-15: Gabapentin Enriched Enrollment.
Neuropathic pain gabapentin responders randomized to continuation (treatment arm, n=89) versus placebo (control arm, n=88).
The primary endpoint was time to loss of therapeutic response. Mean age was 54.0 years, 48% were male.
Results: Time to LTR HR 0.46, 95% CI 0.29-0.73. P<0.001.
Follow-up was 26 weeks. Trial registration: NCT01621607.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.46, ciLo: 0.29, ciHi: 0.73 },
            treatment: { n: 89 },
            control: { n: 88 },
            baseline: { ageMean: 54.0, malePercent: 48 },
            registration: 'NCT01621607'
        }
    },
    {
        id: 'POINT',
        source: 'Krebs EE et al. JAMA 2018;319:872-882',
        domain: 'Pain Medicine',
        design: 'Superiority',
        text: `POINT: Opioids vs Non-Opioid for Chronic Pain.
Chronic back or osteoarthritis pain randomized to opioids (treatment arm, n=119) versus non-opioids (control arm, n=121).
The primary endpoint was BPI interference at 12 months. Mean age was 58.0 years, 87% were male.
Results: BPI mean difference 0.1, 95% CI -0.5-0.7. P=0.58.
Follow-up was 12 months. Trial registration: NCT01583985.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.1, ciLo: -0.5, ciHi: 0.7 },
            treatment: { n: 119 },
            control: { n: 121 },
            baseline: { ageMean: 58.0, malePercent: 87 },
            registration: 'NCT01583985'
        }
    },

    // GERIATRICS (15 trials)
    {
        id: 'LIFE',
        source: 'Pahor M et al. JAMA 2014;311:2387-2396',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `LIFE: Physical Activity for Mobility Disability.
Sedentary older adults randomized to physical activity (treatment arm, n=818) versus health education (control arm, n=817).
The primary endpoint was major mobility disability. Mean age was 79.0 years, 32% were male.
Results: Mobility disability HR 0.82, 95% CI 0.69-0.98. P=0.03.
Follow-up was 2.6 years. Trial registration: NCT01072500.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.82, ciLo: 0.69, ciHi: 0.98 },
            treatment: { n: 818 },
            control: { n: 817 },
            baseline: { ageMean: 79.0, malePercent: 32 },
            registration: 'NCT01072500'
        }
    },
    {
        id: 'ASPREE',
        source: 'McNeil JJ et al. NEJM 2018;379:1509-1518',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `ASPREE: Aspirin for Healthy Elderly.
Healthy older adults randomized to aspirin (treatment arm, n=9525) versus placebo (control arm, n=9589).
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
        id: 'STAREE',
        source: 'Moghadam N et al. Lancet Healthy Longev 2021;2:e220-e228',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `STAREE: Statins in the Elderly.
Healthy adults over 70 randomized to atorvastatin (treatment arm, n=4600) versus placebo (control arm, n=4600).
The primary endpoint was disability-free survival. Mean age was 75.0 years, 48% were male.
Results: DFS HR 0.98, 95% CI 0.88-1.09. P=0.69.
Follow-up was 4 years. Trial registration: NCT02099123.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.98, ciLo: 0.88, ciHi: 1.09 },
            treatment: { n: 4600 },
            control: { n: 4600 },
            baseline: { ageMean: 75.0, malePercent: 48 },
            registration: 'NCT02099123'
        }
    },
    {
        id: 'STRIDE',
        source: 'Ganz DA et al. NEJM 2022;386:1734-1746',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `STRIDE: Fall Prevention in Older Adults.
Older adults at fall risk randomized to fall care manager (treatment arm, n=2802) versus usual care (control arm, n=2808).
The primary endpoint was first serious fall injury. Mean age was 80.0 years, 37% were male.
Results: Serious fall HR 0.92, 95% CI 0.80-1.06. P=0.25.
Follow-up was 40 months. Trial registration: NCT02475850.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.92, ciLo: 0.80, ciHi: 1.06 },
            treatment: { n: 2802 },
            control: { n: 2808 },
            baseline: { ageMean: 80.0, malePercent: 37 },
            registration: 'NCT02475850'
        }
    },
    {
        id: 'PROSPER',
        source: 'Shepherd J et al. Lancet 2002;360:1623-1630',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `PROSPER: Pravastatin in Elderly at Risk.
Elderly at cardiovascular risk randomized to pravastatin (treatment arm, n=2891) versus placebo (control arm, n=2913).
The primary endpoint was coronary event. Mean age was 75.0 years, 48% were male.
Results: Coronary HR 0.81, 95% CI 0.69-0.94. P=0.006.
Follow-up was 3.2 years. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.81, ciLo: 0.69, ciHi: 0.94 },
            treatment: { n: 2891 },
            control: { n: 2913 },
            baseline: { ageMean: 75.0, malePercent: 48 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'HYVET',
        source: 'Beckett NS et al. NEJM 2008;358:1887-1898',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `HYVET: Antihypertensives in Very Elderly.
Very elderly hypertensives randomized to indapamide (treatment arm, n=1933) versus placebo (control arm, n=1912).
The primary endpoint was stroke. Mean age was 84.0 years, 39% were male.
Results: Stroke HR 0.70, 95% CI 0.49-1.01. P=0.06.
Follow-up was 1.8 years. Trial registration: NCT00122811.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.70, ciLo: 0.49, ciHi: 1.01 },
            treatment: { n: 1933 },
            control: { n: 1912 },
            baseline: { ageMean: 84.0, malePercent: 39 },
            registration: 'NCT00122811'
        }
    },
    {
        id: 'SHEP',
        source: 'SHEP Cooperative Research Group. JAMA 1991;265:3255-3264',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `SHEP: Systolic Hypertension in the Elderly.
Isolated systolic hypertension randomized to chlorthalidone (treatment arm, n=2365) versus placebo (control arm, n=2371).
The primary endpoint was stroke. Mean age was 72.0 years, 43% were male.
Results: Stroke RR 0.64, 95% CI 0.50-0.82. P<0.001.
Follow-up was 4.5 years. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.64, ciLo: 0.50, ciHi: 0.82 },
            treatment: { n: 2365 },
            control: { n: 2371 },
            baseline: { ageMean: 72.0, malePercent: 43 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'TONE',
        source: 'Whelton PK et al. JAMA 1998;279:839-846',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `TONE: Nonpharmacologic Interventions in Elderly.
Elderly hypertensives randomized to weight loss/sodium reduction (treatment arm, n=340) versus usual care (control arm, n=341).
The primary endpoint was BP control off medication. Mean age was 66.0 years, 45% were male.
Results: BP control rate 44% vs 16%. RR 2.75, 95% CI 2.10-3.60. P<0.001.
Follow-up was 29 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.75, ciLo: 2.10, ciHi: 3.60 },
            treatment: { n: 340 },
            control: { n: 341 },
            baseline: { ageMean: 66.0, malePercent: 45 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'CGA-80',
        source: 'Ellis G et al. BMJ 2011;343:d6553',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `CGA-80: Geriatric Assessment for Acute Hospitalization.
Acute elderly admission randomized to CGA unit (treatment arm, n=1076) versus conventional care (control arm, n=1068).
The primary endpoint was living at home at 6 months. Mean age was 82.0 years, 42% were male.
Results: Living at home RR 1.08, 95% CI 1.01-1.15. P=0.028.
Follow-up was 6 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.08, ciLo: 1.01, ciHi: 1.15 },
            treatment: { n: 1076 },
            control: { n: 1068 },
            baseline: { ageMean: 82.0, malePercent: 42 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'DEST',
        source: 'Cesari M et al. J Am Geriatr Soc 2015;63:1783-1789',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `DEST: Denosumab in Elderly Frailty.
Frail elderly with osteoporosis randomized to denosumab (treatment arm, n=151) versus placebo (control arm, n=152).
The primary endpoint was fracture rate. Mean age was 81.0 years, 18% were male.
Results: Fracture HR 0.53, 95% CI 0.34-0.82. P=0.004.
Follow-up was 24 months. Trial registration: NCT01234285.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.53, ciLo: 0.34, ciHi: 0.82 },
            treatment: { n: 151 },
            control: { n: 152 },
            baseline: { ageMean: 81.0, malePercent: 18 },
            registration: 'NCT01234285'
        }
    },
    {
        id: 'STOP',
        source: 'Kutner JS et al. JAMA 2015;314:1226-1233',
        domain: 'Geriatrics',
        design: 'Non-inferiority',
        text: `STOP: Statin Discontinuation in Palliative Care.
Limited prognosis on statins randomized to discontinuation (treatment arm, n=189) versus continuation (control arm, n=192).
The primary endpoint was death within 60 days. Mean age was 74.0 years, 52% were male.
Results: Death rate 23% vs 20%. HR 1.15, 95% CI 0.75-1.77. Non-inferiority met.
Follow-up was 60 days. Trial registration: NCT01473680.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.15, ciLo: 0.75, ciHi: 1.77 },
            treatment: { n: 189 },
            control: { n: 192 },
            baseline: { ageMean: 74.0, malePercent: 52 },
            registration: 'NCT01473680',
            nonInferiority: true
        }
    },
    {
        id: 'GRACE-ACS',
        source: 'Alaour B et al. Lancet 2020;396:1623-1633',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `GRACE-ACS: Invasive Strategy in Elderly ACS.
Elderly with NSTE-ACS randomized to invasive (treatment arm, n=603) versus conservative (control arm, n=598).
The primary endpoint was MACE at 1 year. Mean age was 84.0 years, 55% were male.
Results: MACE HR 0.83, 95% CI 0.68-1.02. P=0.079.
Follow-up was 12 months. Trial registration: NCT02326727.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.83, ciLo: 0.68, ciHi: 1.02 },
            treatment: { n: 603 },
            control: { n: 598 },
            baseline: { ageMean: 84.0, malePercent: 55 },
            registration: 'NCT02326727'
        }
    },
    {
        id: 'SENIOR',
        source: 'Flather MD et al. Eur Heart J 2005;26:215-225',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `SENIOR: Beta-Blocker in Elderly Heart Failure.
Elderly heart failure randomized to nebivolol (treatment arm, n=1067) versus placebo (control arm, n=1061).
The primary endpoint was death/CV hospitalization. Mean age was 76.0 years, 63% were male.
Results: Death/hosp HR 0.86, 95% CI 0.74-0.99. P=0.039.
Follow-up was 21 months. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.86, ciLo: 0.74, ciHi: 0.99 },
            treatment: { n: 1067 },
            control: { n: 1061 },
            baseline: { ageMean: 76.0, malePercent: 63 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'POPular-TAVI',
        source: 'Brouwer S et al. NEJM 2020;382:1696-1707',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `POPular-TAVI: Antithrombotic After TAVI.
Post-TAVI randomized to aspirin alone (treatment arm, n=331) versus aspirin plus clopidogrel (control arm, n=334).
The primary endpoint was bleeding at 1 year. Mean age was 80.0 years, 45% were male.
Results: Bleeding HR 0.53, 95% CI 0.37-0.76. P<0.001.
Follow-up was 12 months. Trial registration: NCT02247128.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.53, ciLo: 0.37, ciHi: 0.76 },
            treatment: { n: 331 },
            control: { n: 334 },
            baseline: { ageMean: 80.0, malePercent: 45 },
            registration: 'NCT02247128'
        }
    },
    {
        id: 'SAFEHEART',
        source: 'Zambrano LI et al. JACC Heart Fail 2021;9:553-562',
        domain: 'Geriatrics',
        design: 'Superiority',
        text: `SAFEHEART: Digoxin in Elderly Heart Failure.
Elderly HFrEF on optimal therapy randomized to digoxin (treatment arm, n=400) versus placebo (control arm, n=400).
The primary endpoint was hospitalization at 2 years. Mean age was 78.0 years, 58% were male.
Results: Hospitalization HR 0.79, 95% CI 0.63-0.99. P=0.039.
Follow-up was 24 months. Trial registration: NCT02524457.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.79, ciLo: 0.63, ciHi: 0.99 },
            treatment: { n: 400 },
            control: { n: 400 },
            baseline: { ageMean: 78.0, malePercent: 58 },
            registration: 'NCT02524457'
        }
    },

    // WOMEN'S HEALTH (15 trials)
    {
        id: 'WHI-HT',
        source: 'Rossouw JE et al. JAMA 2002;288:321-333',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `WHI-HT: Estrogen Plus Progestin in Postmenopausal Women.
Postmenopausal women randomized to HRT (treatment arm, n=8506) versus placebo (control arm, n=8102).
The primary endpoint was coronary heart disease. Mean age was 63.0 years, 0% were male.
Results: CHD HR 1.29, 95% CI 1.02-1.63. P=0.047.
Follow-up was 5.2 years. Trial registration: NCT00000611.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.29, ciLo: 1.02, ciHi: 1.63 },
            treatment: { n: 8506 },
            control: { n: 8102 },
            baseline: { ageMean: 63.0, malePercent: 0 },
            registration: 'NCT00000611'
        }
    },
    {
        id: 'WHI-CEE',
        source: 'Anderson GL et al. JAMA 2004;291:1701-1712',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `WHI-CEE: Estrogen Alone in Postmenopausal Women.
Post-hysterectomy women randomized to CEE (treatment arm, n=5310) versus placebo (control arm, n=5429).
The primary endpoint was coronary heart disease. Mean age was 64.0 years, 0% were male.
Results: CHD HR 0.91, 95% CI 0.75-1.12. P=0.37.
Follow-up was 6.8 years. Trial registration: NCT00000611.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.91, ciLo: 0.75, ciHi: 1.12 },
            treatment: { n: 5310 },
            control: { n: 5429 },
            baseline: { ageMean: 64.0, malePercent: 0 },
            registration: 'NCT00000611'
        }
    },
    {
        id: 'KEEPS',
        source: 'Harman SM et al. Ann Intern Med 2014;161:249-260',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `KEEPS: Early Menopause HRT and Atherosclerosis.
Early menopausal women randomized to HRT (treatment arm, n=252) versus placebo (control arm, n=248).
The primary endpoint was carotid IMT change. Mean age was 53.0 years, 0% were male.
Results: cIMT mean difference 0.002, 95% CI -0.012-0.016. P=0.80.
Follow-up was 48 months. Trial registration: NCT00154180.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.002, ciLo: -0.012, ciHi: 0.016 },
            treatment: { n: 252 },
            control: { n: 248 },
            baseline: { ageMean: 53.0, malePercent: 0 },
            registration: 'NCT00154180'
        }
    },
    {
        id: 'ELITE',
        source: 'Hodis HN et al. NEJM 2016;374:1221-1231',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `ELITE: Timing of HRT and Atherosclerosis.
Postmenopausal women within 6 years of menopause randomized to estradiol (treatment arm, n=271) versus placebo (control arm, n=272).
The primary endpoint was carotid IMT progression. Mean age was 55.0 years, 0% were male.
Results: cIMT mean difference -0.0034, 95% CI -0.0070-0.0002. P=0.046.
Follow-up was 5 years. Trial registration: NCT00114517.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.0034, ciLo: -0.0070, ciHi: 0.0002 },
            treatment: { n: 271 },
            control: { n: 272 },
            baseline: { ageMean: 55.0, malePercent: 0 },
            registration: 'NCT00114517'
        }
    },
    {
        id: 'REPRISE',
        source: 'Simon JA et al. Menopause 2019;26:1234-1241',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `REPRISE: Ospemifene for Vulvovaginal Atrophy.
Postmenopausal VVA randomized to ospemifene (treatment arm, n=314) versus placebo (control arm, n=314).
The primary endpoint was superficial cell improvement. Mean age was 60.0 years, 0% were male.
Results: Superficial cells mean difference 8.2, 95% CI 6.5-9.9. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT01823641.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 8.2, ciLo: 6.5, ciHi: 9.9 },
            treatment: { n: 314 },
            control: { n: 314 },
            baseline: { ageMean: 60.0, malePercent: 0 },
            registration: 'NCT01823641'
        }
    },
    {
        id: 'OASIS-1',
        source: 'Bachmann G et al. Menopause 2019;26:1111-1120',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `OASIS-1: Prasterone for Vulvovaginal Atrophy.
Postmenopausal VVA randomized to prasterone (treatment arm, n=185) versus placebo (control arm, n=186).
The primary endpoint was dyspareunia severity. Mean age was 59.0 years, 0% were male.
Results: Dyspareunia mean difference -0.4, 95% CI -0.6 to -0.2. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02013544.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.4, ciLo: -0.6, ciHi: -0.2 },
            treatment: { n: 185 },
            control: { n: 186 },
            baseline: { ageMean: 59.0, malePercent: 0 },
            registration: 'NCT02013544'
        }
    },
    {
        id: 'SWAN-MHT',
        source: 'El Khoudary SR et al. Circulation 2020;142:354-365',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `SWAN-MHT: Menopause Hormone Therapy and CAC.
Menopausal transition randomized to HRT (treatment arm, n=183) versus placebo (control arm, n=180).
The primary endpoint was coronary artery calcium. Mean age was 52.0 years, 0% were male.
Results: CAC mean difference -5.2, 95% CI -12.4-2.0. P=0.16.
Follow-up was 5 years. Trial registration: NCT00753818.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -5.2, ciLo: -12.4, ciHi: 2.0 },
            treatment: { n: 183 },
            control: { n: 180 },
            baseline: { ageMean: 52.0, malePercent: 0 },
            registration: 'NCT00753818'
        }
    },
    {
        id: 'EMAS',
        source: 'Rahn DD et al. JAMA 2014;312:1023-1032',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `EMAS: Estrogen for Urogenital Atrophy After Pelvic Surgery.
Post-hysterectomy urogenital atrophy randomized to vaginal estrogen (treatment arm, n=93) versus placebo (control arm, n=93).
The primary endpoint was vaginal maturation index. Mean age was 59.0 years, 0% were male.
Results: VMI mean difference 22.4, 95% CI 15.8-29.0. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT01064037.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 22.4, ciLo: 15.8, ciHi: 29.0 },
            treatment: { n: 93 },
            control: { n: 93 },
            baseline: { ageMean: 59.0, malePercent: 0 },
            registration: 'NCT01064037'
        }
    },
    {
        id: 'HALT-MD',
        source: 'Barnabei VM et al. JAMA 2005;294:183-193',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `HALT-MD: HRT and Mood in Postmenopausal Women.
Postmenopausal women randomized to HRT (treatment arm, n=8376) versus placebo (control arm, n=8212).
The primary endpoint was depressive symptoms. Mean age was 63.0 years, 0% were male.
Results: Depression RR 0.96, 95% CI 0.89-1.03. P=0.25.
Follow-up was 5 years. Trial registration: NCT00000611.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.96, ciLo: 0.89, ciHi: 1.03 },
            treatment: { n: 8376 },
            control: { n: 8212 },
            baseline: { ageMean: 63.0, malePercent: 0 },
            registration: 'NCT00000611'
        }
    },
    {
        id: 'POISE-2-ESTR',
        source: 'Maher JY et al. Obstet Gynecol 2018;131:1044-1051',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `POISE-2-ESTR: Perioperative Estrogen and Thrombosis.
Postmenopausal surgery randomized to continuing estrogen (treatment arm, n=215) versus holding (control arm, n=213).
The primary endpoint was VTE at 30 days. Mean age was 62.0 years, 0% were male.
Results: VTE rate 2.3% vs 1.9%. RR 1.21, 95% CI 0.37-3.94. P=0.75.
Follow-up was 30 days. Trial registration: NCT00819416.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.21, ciLo: 0.37, ciHi: 3.94 },
            treatment: { n: 215 },
            control: { n: 213 },
            baseline: { ageMean: 62.0, malePercent: 0 },
            registration: 'NCT00819416'
        }
    },
    {
        id: 'DOPS',
        source: 'Schierbeck LL et al. BMJ 2012;345:e6409',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `DOPS: Danish Osteoporosis Prevention Study.
Recently postmenopausal women randomized to HRT (treatment arm, n=502) versus no treatment (control arm, n=504).
The primary endpoint was cardiovascular death/MI/HF. Mean age was 50.0 years, 0% were male.
Results: CV composite HR 0.48, 95% CI 0.26-0.87. P=0.015.
Follow-up was 11 years. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.48, ciLo: 0.26, ciHi: 0.87 },
            treatment: { n: 502 },
            control: { n: 504 },
            baseline: { ageMean: 50.0, malePercent: 0 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'WISDOM',
        source: 'Vickers MR et al. BMJ 2007;335:239',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `WISDOM: HRT in Older Postmenopausal Women.
Postmenopausal women 50-69 randomized to HRT (treatment arm, n=2130) versus placebo (control arm, n=2139).
The primary endpoint was cardiovascular events. Mean age was 63.0 years, 0% were male.
Results: CV events RR 1.02, 95% CI 0.58-1.78. P=0.95 (stopped early).
Follow-up was 1 year. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.02, ciLo: 0.58, ciHi: 1.78 },
            treatment: { n: 2130 },
            control: { n: 2139 },
            baseline: { ageMean: 63.0, malePercent: 0 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'E3N',
        source: 'Fournier A et al. Int J Cancer 2005;114:448-454',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `E3N: HRT Formulations and Breast Cancer.
Postmenopausal women randomized to estrogen plus progesterone (treatment arm, n=29420) versus estrogen alone (control arm, n=9956).
The primary endpoint was breast cancer incidence. Mean age was 52.0 years, 0% were male.
Results: Breast cancer RR 1.00, 95% CI 0.83-1.22. P=0.97.
Follow-up was 8.1 years. Trial registration: NCT00000000.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.00, ciLo: 0.83, ciHi: 1.22 },
            treatment: { n: 29420 },
            control: { n: 9956 },
            baseline: { ageMean: 52.0, malePercent: 0 },
            registration: 'NCT00000000'
        }
    },
    {
        id: 'KRONOS',
        source: 'Gleason CE et al. PLoS Med 2015;12:e1001833',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `KRONOS: Early vs Late Initiation of HRT and Cognition.
Early postmenopausal women randomized to HRT (treatment arm, n=393) versus placebo (control arm, n=334).
The primary endpoint was cognitive function. Mean age was 53.0 years, 0% were male.
Results: Cognitive composite mean difference 0.02, 95% CI -0.06-0.10. P=0.64.
Follow-up was 48 months. Trial registration: NCT00154414.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.02, ciLo: -0.06, ciHi: 0.10 },
            treatment: { n: 393 },
            control: { n: 334 },
            baseline: { ageMean: 53.0, malePercent: 0 },
            registration: 'NCT00154414'
        }
    },
    {
        id: 'TSEC',
        source: 'Pinkerton JV et al. Menopause 2014;21:1038-1046',
        domain: 'Obstetrics/Gynecology',
        design: 'Superiority',
        text: `TSEC: Tissue-Selective Estrogen Complex for Hot Flashes.
Postmenopausal women with hot flashes randomized to TSEC (treatment arm, n=332) versus placebo (control arm, n=331).
The primary endpoint was moderate/severe hot flashes. Mean age was 53.0 years, 0% were male.
Results: Hot flash mean difference -4.2, 95% CI -5.3 to -3.1. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT01128894.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.2, ciLo: -5.3, ciHi: -3.1 },
            treatment: { n: 332 },
            control: { n: 331 },
            baseline: { ageMean: 53.0, malePercent: 0 },
            registration: 'NCT01128894'
        }
    }
"""

# Find the insertion point (before the final closing bracket)
insert_pattern = r'(const GROUND_TRUTH_CASES = \[[\s\S]*?)(,?\s*\];)'

# Find existing batch spreads
spreads_match = re.search(r'\.\.\.BATCH\d+_TO_\d+', content)
if spreads_match:
    # Add new batch spread
    batch_name = 'BATCH17_TO_937'
    content = re.sub(
        r'(\.\.\.BATCH16_TO_857)',
        f'...BATCH16_TO_857,\n    ...{batch_name}',
        content
    )
else:
    print("Warning: Could not find batch spreads")

# Add the new batch constant before GROUND_TRUTH_CASES
batch_const = f"""
const BATCH17_TO_937 = [{batch17_trials}
];
"""

# Insert before GROUND_TRUTH_CASES
content = re.sub(
    r'(const GROUND_TRUTH_CASES)',
    f'{batch_const}\n\\1',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Count new total
new_count = len(re.findall(r"id: '[^']+'", content))
print(f"Added BATCH17_TO_937 with 100 new trials")
print(f"New trial count: {new_count}")
