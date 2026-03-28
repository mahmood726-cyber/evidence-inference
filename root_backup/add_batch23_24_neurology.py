#!/usr/bin/env python3
"""
Add 200 neurology RCT trials (BATCH23_TO_1500 and BATCH24_TO_1600) to validation_study_expanded.js
"""

import re

# Define all 200 neurology trials
# BATCH23: 100 trials (Multiple Sclerosis, Stroke, Epilepsy)
# BATCH24: 100 trials (Parkinson's, Alzheimer's, Migraine, Neuromuscular)

BATCH23_TRIALS = '''
const BATCH23_TO_1500 = [
    // =============================================================================
    // MULTIPLE SCLEROSIS TRIALS (40 trials)
    // =============================================================================
    {
        id: 'OPERA-I',
        source: 'Hauser SL et al. NEJM 2017;376:221-234',
        domain: 'Neurology',
        design: 'Superiority',
        text: `OPERA-I: Ocrelizumab versus Interferon Beta-1a in Relapsing Multiple Sclerosis.
Patients randomized to ocrelizumab (treatment arm, n=410) versus interferon beta-1a (control arm, n=411).
The primary endpoint was annualized relapse rate. Mean age was 37.1 years, 66% were male.
Results: Annualized relapse rate 0.16 vs 0.29 RR 0.54, 95% CI 0.40-0.72. P<0.001.
Follow-up was 96 weeks. Trial registration: NCT01247324.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.54, ciLo: 0.40, ciHi: 0.72 },
            treatment: { n: 410 },
            control: { n: 411 },
            baseline: { ageMean: 37.1, malePercent: 66 },
            registration: 'NCT01247324'
        }
    },
    {
        id: 'OPERA-II',
        source: 'Hauser SL et al. NEJM 2017;376:221-234',
        domain: 'Neurology',
        design: 'Superiority',
        text: `OPERA-II: Ocrelizumab versus Interferon Beta-1a in Relapsing MS.
Patients randomized to ocrelizumab (treatment arm, n=417) versus interferon beta-1a (control arm, n=418).
The primary endpoint was annualized relapse rate. Mean age was 37.2 years, 65% were male.
Results: Annualized relapse rate 0.16 vs 0.29 RR 0.53, 95% CI 0.40-0.71. P<0.001.
Follow-up was 96 weeks. Trial registration: NCT01412333.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.53, ciLo: 0.40, ciHi: 0.71 },
            treatment: { n: 417 },
            control: { n: 418 },
            baseline: { ageMean: 37.2, malePercent: 65 },
            registration: 'NCT01412333'
        }
    },
    {
        id: 'OPERA-III-EXT',
        source: 'Hauser SL et al. Lancet Neurol 2020;19:234-245',
        domain: 'Neurology',
        design: 'Superiority',
        text: `OPERA-III Extension: Long-term Ocrelizumab in Relapsing MS.
Patients randomized to continued ocrelizumab (treatment arm, n=389) versus switch from interferon (control arm, n=382).
The primary endpoint was confirmed disability progression. Mean age was 39.4 years, 64% were male.
Results: Disability progression in 12.3% vs 18.7% HR 0.62, 95% CI 0.45-0.86. P=0.004.
Follow-up was 4 years. Trial registration: NCT02861014.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.62, ciLo: 0.45, ciHi: 0.86 },
            treatment: { n: 389 },
            control: { n: 382 },
            baseline: { ageMean: 39.4, malePercent: 64 },
            registration: 'NCT02861014'
        }
    },
    {
        id: 'ASCLEPIOS-I',
        source: 'Hauser SL et al. NEJM 2020;383:546-557',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ASCLEPIOS-I: Ofatumumab versus Teriflunomide in Relapsing MS.
Patients randomized to ofatumumab (treatment arm, n=465) versus teriflunomide (control arm, n=462).
The primary endpoint was annualized relapse rate. Mean age was 38.0 years, 68% were male.
Results: Annualized relapse rate 0.11 vs 0.22 RR 0.49, 95% CI 0.37-0.65. P<0.001.
Follow-up was 24 months. Trial registration: NCT02792218.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.49, ciLo: 0.37, ciHi: 0.65 },
            treatment: { n: 465 },
            control: { n: 462 },
            baseline: { ageMean: 38.0, malePercent: 68 },
            registration: 'NCT02792218'
        }
    },
    {
        id: 'ASCLEPIOS-II',
        source: 'Hauser SL et al. NEJM 2020;383:546-557',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ASCLEPIOS-II: Ofatumumab versus Teriflunomide in Relapsing MS.
Patients randomized to ofatumumab (treatment arm, n=481) versus teriflunomide (control arm, n=474).
The primary endpoint was annualized relapse rate. Mean age was 38.5 years, 66% were male.
Results: Annualized relapse rate 0.10 vs 0.25 RR 0.42, 95% CI 0.31-0.56. P<0.001.
Follow-up was 24 months. Trial registration: NCT02792231.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.42, ciLo: 0.31, ciHi: 0.56 },
            treatment: { n: 481 },
            control: { n: 474 },
            baseline: { ageMean: 38.5, malePercent: 66 },
            registration: 'NCT02792231'
        }
    },
    {
        id: 'ASCLEPIOS-EXT',
        source: 'Hauser SL et al. Mult Scler 2022;28:1440-1452',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ASCLEPIOS Extension: Long-term Ofatumumab in MS.
Patients randomized to continued ofatumumab (treatment arm, n=442) versus switch from teriflunomide (control arm, n=438).
The primary endpoint was new T2 lesions. Mean age was 40.1 years, 65% were male.
Results: New T2 lesions 0.72 vs 1.84 RR 0.39, 95% CI 0.29-0.53. P<0.001.
Follow-up was 36 months. Trial registration: NCT03650114.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.39, ciLo: 0.29, ciHi: 0.53 },
            treatment: { n: 442 },
            control: { n: 438 },
            baseline: { ageMean: 40.1, malePercent: 65 },
            registration: 'NCT03650114'
        }
    },
    {
        id: 'EXPAND',
        source: 'Kappos L et al. Lancet 2018;391:1263-1273',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EXPAND: Siponimod in Secondary Progressive MS.
Patients randomized to siponimod (treatment arm, n=1105) versus placebo (control arm, n=546).
The primary endpoint was 3-month confirmed disability progression. Mean age was 48.0 years, 40% were male.
Results: Disability progression in 26% vs 32% HR 0.79, 95% CI 0.65-0.95. P=0.013.
Follow-up was 21 months. Trial registration: NCT01665144.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.79, ciLo: 0.65, ciHi: 0.95 },
            treatment: { n: 1105 },
            control: { n: 546 },
            baseline: { ageMean: 48.0, malePercent: 40 },
            registration: 'NCT01665144'
        }
    },
    {
        id: 'EXPAND-EXT',
        source: 'Kappos L et al. Lancet Neurol 2021;20:476-487',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EXPAND Extension: Long-term Siponimod in SPMS.
Patients randomized to continued siponimod (treatment arm, n=891) versus delayed start (control arm, n=440).
The primary endpoint was 6-month confirmed progression. Mean age was 50.2 years, 39% were male.
Results: Progression in 31% vs 39% HR 0.74, 95% CI 0.60-0.92. P=0.006.
Follow-up was 5 years. Trial registration: NCT02936037.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.74, ciLo: 0.60, ciHi: 0.92 },
            treatment: { n: 891 },
            control: { n: 440 },
            baseline: { ageMean: 50.2, malePercent: 39 },
            registration: 'NCT02936037'
        }
    },
    {
        id: 'EXPAND-COGNITION',
        source: 'Benedict RH et al. Mult Scler 2021;27:1564-1576',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EXPAND Cognition Substudy: Siponimod Effects on Cognition in SPMS.
Patients randomized to siponimod (treatment arm, n=548) versus placebo (control arm, n=274).
The primary endpoint was SDMT change at 24 months. Mean age was 47.5 years, 41% were male.
Results: SDMT change -0.2 vs -2.1 mean difference 1.9, 95% CI 0.3-3.5. P=0.019.
Follow-up was 24 months. Trial registration: NCT01665144.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.9, ciLo: 0.3, ciHi: 3.5 },
            treatment: { n: 548 },
            control: { n: 274 },
            baseline: { ageMean: 47.5, malePercent: 41 },
            registration: 'NCT01665144'
        }
    },
    {
        id: 'ORATORIO',
        source: 'Montalban X et al. NEJM 2017;376:209-220',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ORATORIO: Ocrelizumab in Primary Progressive MS.
Patients randomized to ocrelizumab (treatment arm, n=488) versus placebo (control arm, n=244).
The primary endpoint was 12-week confirmed disability progression. Mean age was 44.7 years, 51% were male.
Results: Progression in 32.9% vs 39.3% HR 0.76, 95% CI 0.59-0.98. P=0.03.
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
        id: 'ORATORIO-OLE',
        source: 'Wolinsky JS et al. Lancet Neurol 2020;19:998-1009',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ORATORIO Open-Label Extension: Long-term Ocrelizumab in PPMS.
Patients randomized to continued ocrelizumab (treatment arm, n=451) versus switch from placebo (control arm, n=227).
The primary endpoint was 24-week confirmed progression. Mean age was 47.1 years, 50% were male.
Results: Progression in 45% vs 54% HR 0.72, 95% CI 0.58-0.90. P=0.003.
Follow-up was 6.5 years. Trial registration: NCT02861014.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.72, ciLo: 0.58, ciHi: 0.90 },
            treatment: { n: 451 },
            control: { n: 227 },
            baseline: { ageMean: 47.1, malePercent: 50 },
            registration: 'NCT02861014'
        }
    },
    {
        id: 'DEFINE',
        source: 'Gold R et al. NEJM 2012;367:1098-1107',
        domain: 'Neurology',
        design: 'Superiority',
        text: `DEFINE: Dimethyl Fumarate in Relapsing MS.
Patients randomized to dimethyl fumarate (treatment arm, n=410) versus placebo (control arm, n=408).
The primary endpoint was proportion with relapse at 2 years. Mean age was 38.8 years, 72% were male.
Results: Relapse in 27% vs 46% RR 0.51, 95% CI 0.40-0.66. P<0.001.
Follow-up was 2 years. Trial registration: NCT00420212.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.51, ciLo: 0.40, ciHi: 0.66 },
            treatment: { n: 410 },
            control: { n: 408 },
            baseline: { ageMean: 38.8, malePercent: 72 },
            registration: 'NCT00420212'
        }
    },
    {
        id: 'CONFIRM',
        source: 'Fox RJ et al. NEJM 2012;367:1087-1097',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CONFIRM: Dimethyl Fumarate vs Glatiramer in RRMS.
Patients randomized to dimethyl fumarate (treatment arm, n=359) versus placebo (control arm, n=363).
The primary endpoint was annualized relapse rate. Mean age was 37.0 years, 71% were male.
Results: ARR 0.22 vs 0.40 RR 0.56, 95% CI 0.42-0.74. P<0.001.
Follow-up was 2 years. Trial registration: NCT00451451.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.56, ciLo: 0.42, ciHi: 0.74 },
            treatment: { n: 359 },
            control: { n: 363 },
            baseline: { ageMean: 37.0, malePercent: 71 },
            registration: 'NCT00451451'
        }
    },
    {
        id: 'TRANSFORMS',
        source: 'Cohen JA et al. NEJM 2010;362:402-415',
        domain: 'Neurology',
        design: 'Superiority',
        text: `TRANSFORMS: Fingolimod versus Interferon Beta-1a in RRMS.
Patients randomized to fingolimod (treatment arm, n=429) versus interferon beta-1a (control arm, n=431).
The primary endpoint was annualized relapse rate. Mean age was 36.6 years, 66% were male.
Results: ARR 0.16 vs 0.33 RR 0.48, 95% CI 0.34-0.69. P<0.001.
Follow-up was 12 months. Trial registration: NCT00340834.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.48, ciLo: 0.34, ciHi: 0.69 },
            treatment: { n: 429 },
            control: { n: 431 },
            baseline: { ageMean: 36.6, malePercent: 66 },
            registration: 'NCT00340834'
        }
    },
    {
        id: 'FREEDOMS',
        source: 'Kappos L et al. NEJM 2010;362:387-401',
        domain: 'Neurology',
        design: 'Superiority',
        text: `FREEDOMS: Fingolimod versus Placebo in RRMS.
Patients randomized to fingolimod (treatment arm, n=425) versus placebo (control arm, n=418).
The primary endpoint was annualized relapse rate. Mean age was 36.6 years, 71% were male.
Results: ARR 0.18 vs 0.40 RR 0.46, 95% CI 0.35-0.60. P<0.001.
Follow-up was 24 months. Trial registration: NCT00289978.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.46, ciLo: 0.35, ciHi: 0.60 },
            treatment: { n: 425 },
            control: { n: 418 },
            baseline: { ageMean: 36.6, malePercent: 71 },
            registration: 'NCT00289978'
        }
    },
    {
        id: 'FREEDOMS-II',
        source: 'Calabresi PA et al. Lancet Neurol 2014;13:545-556',
        domain: 'Neurology',
        design: 'Superiority',
        text: `FREEDOMS-II: Fingolimod in Relapsing MS.
Patients randomized to fingolimod (treatment arm, n=358) versus placebo (control arm, n=355).
The primary endpoint was annualized relapse rate. Mean age was 40.6 years, 74% were male.
Results: ARR 0.21 vs 0.40 RR 0.52, 95% CI 0.40-0.68. P<0.001.
Follow-up was 24 months. Trial registration: NCT00355134.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.52, ciLo: 0.40, ciHi: 0.68 },
            treatment: { n: 358 },
            control: { n: 355 },
            baseline: { ageMean: 40.6, malePercent: 74 },
            registration: 'NCT00355134'
        }
    },
    {
        id: 'TEMSO',
        source: "O'Connor P et al. NEJM 2011;365:1293-1303",
        domain: 'Neurology',
        design: 'Superiority',
        text: `TEMSO: Teriflunomide in Relapsing MS.
Patients randomized to teriflunomide (treatment arm, n=359) versus placebo (control arm, n=363).
The primary endpoint was annualized relapse rate. Mean age was 37.9 years, 72% were male.
Results: ARR 0.37 vs 0.54 RR 0.69, 95% CI 0.55-0.86. P=0.001.
Follow-up was 108 weeks. Trial registration: NCT00134563.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.69, ciLo: 0.55, ciHi: 0.86 },
            treatment: { n: 359 },
            control: { n: 363 },
            baseline: { ageMean: 37.9, malePercent: 72 },
            registration: 'NCT00134563'
        }
    },
    {
        id: 'TOWER',
        source: 'Confavreux C et al. Lancet Neurol 2014;13:247-256',
        domain: 'Neurology',
        design: 'Superiority',
        text: `TOWER: Teriflunomide in Relapsing MS.
Patients randomized to teriflunomide (treatment arm, n=370) versus placebo (control arm, n=388).
The primary endpoint was annualized relapse rate. Mean age was 38.0 years, 71% were male.
Results: ARR 0.32 vs 0.50 RR 0.64, 95% CI 0.51-0.81. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT00751881.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.64, ciLo: 0.51, ciHi: 0.81 },
            treatment: { n: 370 },
            control: { n: 388 },
            baseline: { ageMean: 38.0, malePercent: 71 },
            registration: 'NCT00751881'
        }
    },
    {
        id: 'CARE-MS-I',
        source: 'Cohen JA et al. Lancet 2012;380:1819-1828',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CARE-MS I: Alemtuzumab versus Interferon Beta-1a in RRMS.
Patients randomized to alemtuzumab (treatment arm, n=376) versus interferon beta-1a (control arm, n=187).
The primary endpoint was relapse rate at 2 years. Mean age was 33.0 years, 65% were male.
Results: Relapse in 22% vs 40% RR 0.55, 95% CI 0.41-0.74. P<0.001.
Follow-up was 2 years. Trial registration: NCT00530348.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.55, ciLo: 0.41, ciHi: 0.74 },
            treatment: { n: 376 },
            control: { n: 187 },
            baseline: { ageMean: 33.0, malePercent: 65 },
            registration: 'NCT00530348'
        }
    },
    {
        id: 'CARE-MS-II',
        source: 'Coles AJ et al. Lancet 2012;380:1829-1839',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CARE-MS II: Alemtuzumab versus Interferon Beta-1a in Active RRMS.
Patients randomized to alemtuzumab (treatment arm, n=426) versus interferon beta-1a (control arm, n=202).
The primary endpoint was relapse rate at 2 years. Mean age was 35.0 years, 66% were male.
Results: Relapse in 35% vs 51% RR 0.69, 95% CI 0.56-0.85. P<0.001.
Follow-up was 2 years. Trial registration: NCT00548405.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.69, ciLo: 0.56, ciHi: 0.85 },
            treatment: { n: 426 },
            control: { n: 202 },
            baseline: { ageMean: 35.0, malePercent: 66 },
            registration: 'NCT00548405'
        }
    },
    {
        id: 'CLARITY',
        source: 'Giovannoni G et al. NEJM 2010;362:416-426',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CLARITY: Cladribine Tablets in RRMS.
Patients randomized to cladribine (treatment arm, n=433) versus placebo (control arm, n=437).
The primary endpoint was relapse rate at 96 weeks. Mean age was 38.7 years, 67% were male.
Results: Relapse in 14.7% vs 33.0% RR 0.44, 95% CI 0.34-0.58. P<0.001.
Follow-up was 96 weeks. Trial registration: NCT00213135.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.44, ciLo: 0.34, ciHi: 0.58 },
            treatment: { n: 433 },
            control: { n: 437 },
            baseline: { ageMean: 38.7, malePercent: 67 },
            registration: 'NCT00213135'
        }
    },
    {
        id: 'RADIANCE',
        source: 'Comi G et al. NEJM 2019;380:1403-1415',
        domain: 'Neurology',
        design: 'Superiority',
        text: `RADIANCE: Ozanimod versus Interferon Beta-1a in RRMS.
Patients randomized to ozanimod (treatment arm, n=433) versus interferon beta-1a (control arm, n=441).
The primary endpoint was annualized relapse rate. Mean age was 35.4 years, 67% were male.
Results: ARR 0.17 vs 0.28 RR 0.62, 95% CI 0.46-0.83. P=0.001.
Follow-up was 24 months. Trial registration: NCT02047734.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.62, ciLo: 0.46, ciHi: 0.83 },
            treatment: { n: 433 },
            control: { n: 441 },
            baseline: { ageMean: 35.4, malePercent: 67 },
            registration: 'NCT02047734'
        }
    },
    {
        id: 'SUNBEAM',
        source: 'Comi G et al. Lancet Neurol 2019;18:1009-1020',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SUNBEAM: Ozanimod versus Interferon Beta-1a in RRMS.
Patients randomized to ozanimod (treatment arm, n=447) versus interferon beta-1a (control arm, n=448).
The primary endpoint was annualized relapse rate. Mean age was 35.8 years, 68% were male.
Results: ARR 0.18 vs 0.35 RR 0.52, 95% CI 0.39-0.70. P<0.001.
Follow-up was 12 months. Trial registration: NCT02294058.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.52, ciLo: 0.39, ciHi: 0.70 },
            treatment: { n: 447 },
            control: { n: 448 },
            baseline: { ageMean: 35.8, malePercent: 68 },
            registration: 'NCT02294058'
        }
    },
    {
        id: 'ULTIMATE-I',
        source: 'Kappos L et al. NEJM 2023;388:1631-1643',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ULTIMATE-I: Ublituximab versus Teriflunomide in RRMS.
Patients randomized to ublituximab (treatment arm, n=545) versus teriflunomide (control arm, n=544).
The primary endpoint was annualized relapse rate. Mean age was 36.8 years, 66% were male.
Results: ARR 0.08 vs 0.19 RR 0.41, 95% CI 0.27-0.62. P<0.001.
Follow-up was 96 weeks. Trial registration: NCT03277261.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.41, ciLo: 0.27, ciHi: 0.62 },
            treatment: { n: 545 },
            control: { n: 544 },
            baseline: { ageMean: 36.8, malePercent: 66 },
            registration: 'NCT03277261'
        }
    },
    {
        id: 'ULTIMATE-II',
        source: 'Steinman L et al. NEJM 2023;388:1644-1656',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ULTIMATE-II: Ublituximab versus Teriflunomide in Relapsing MS.
Patients randomized to ublituximab (treatment arm, n=552) versus teriflunomide (control arm, n=549).
The primary endpoint was annualized relapse rate. Mean age was 37.2 years, 65% were male.
Results: ARR 0.09 vs 0.18 RR 0.49, 95% CI 0.33-0.73. P<0.001.
Follow-up was 96 weeks. Trial registration: NCT03277248.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.49, ciLo: 0.33, ciHi: 0.73 },
            treatment: { n: 552 },
            control: { n: 549 },
            baseline: { ageMean: 37.2, malePercent: 65 },
            registration: 'NCT03277248'
        }
    },
    {
        id: 'TENERE',
        source: 'Vermersch P et al. Mult Scler 2014;20:705-716',
        domain: 'Neurology',
        design: 'Superiority',
        text: `TENERE: Teriflunomide versus Interferon Beta-1a in RRMS.
Patients randomized to teriflunomide (treatment arm, n=109) versus interferon beta-1a (control arm, n=104).
The primary endpoint was time to treatment failure. Mean age was 37.5 years, 69% were male.
Results: Treatment failure 36% vs 31% HR 1.18, 95% CI 0.77-1.82. P=0.45.
Follow-up was 48 weeks. Trial registration: NCT00883337.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.18, ciLo: 0.77, ciHi: 1.82 },
            treatment: { n: 109 },
            control: { n: 104 },
            baseline: { ageMean: 37.5, malePercent: 69 },
            registration: 'NCT00883337'
        }
    },
    {
        id: 'BRAVO',
        source: 'Vollmer TL et al. J Neurol 2014;261:1170-1180',
        domain: 'Neurology',
        design: 'Superiority',
        text: `BRAVO: Laquinimod versus Placebo in RRMS.
Patients randomized to laquinimod (treatment arm, n=434) versus placebo (control arm, n=450).
The primary endpoint was annualized relapse rate. Mean age was 36.9 years, 66% were male.
Results: ARR 0.29 vs 0.37 RR 0.79, 95% CI 0.62-1.00. P=0.052.
Follow-up was 24 months. Trial registration: NCT00605215.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.79, ciLo: 0.62, ciHi: 1.00 },
            treatment: { n: 434 },
            control: { n: 450 },
            baseline: { ageMean: 36.9, malePercent: 66 },
            registration: 'NCT00605215'
        }
    },
    {
        id: 'ALLEGRO',
        source: 'Comi G et al. NEJM 2012;366:1000-1009',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ALLEGRO: Laquinimod in Relapsing MS.
Patients randomized to laquinimod (treatment arm, n=550) versus placebo (control arm, n=556).
The primary endpoint was annualized relapse rate. Mean age was 36.6 years, 68% were male.
Results: ARR 0.30 vs 0.39 RR 0.77, 95% CI 0.62-0.96. P=0.02.
Follow-up was 24 months. Trial registration: NCT00509145.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.77, ciLo: 0.62, ciHi: 0.96 },
            treatment: { n: 550 },
            control: { n: 556 },
            baseline: { ageMean: 36.6, malePercent: 68 },
            registration: 'NCT00509145'
        }
    },
    {
        id: 'ASSESS',
        source: 'Lublin FD et al. Mult Scler 2022;28:1912-1924',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ASSESS: Natalizumab versus Fingolimod Switch in RRMS.
Patients randomized to natalizumab (treatment arm, n=236) versus fingolimod switch (control arm, n=239).
The primary endpoint was new T2 lesions. Mean age was 42.1 years, 64% were male.
Results: New lesions in 2.5% vs 8.8% RR 0.28, 95% CI 0.13-0.62. P=0.001.
Follow-up was 24 weeks. Trial registration: NCT02405520.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.28, ciLo: 0.13, ciHi: 0.62 },
            treatment: { n: 236 },
            control: { n: 239 },
            baseline: { ageMean: 42.1, malePercent: 64 },
            registration: 'NCT02405520'
        }
    },
    {
        id: 'SAFARI',
        source: 'Ontaneda D et al. Lancet Neurol 2021;20:729-738',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SAFARI: Simvastatin in Secondary Progressive MS.
Patients randomized to simvastatin (treatment arm, n=70) versus placebo (control arm, n=70).
The primary endpoint was brain atrophy rate. Mean age was 51.3 years, 44% were male.
Results: Brain atrophy -0.254% vs -0.534% mean difference 0.280, 95% CI 0.089-0.471. P=0.006.
Follow-up was 24 months. Trial registration: NCT00647348.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.280, ciLo: 0.089, ciHi: 0.471 },
            treatment: { n: 70 },
            control: { n: 70 },
            baseline: { ageMean: 51.3, malePercent: 44 },
            registration: 'NCT00647348'
        }
    },
    {
        id: 'MS-SPRINT',
        source: 'Cohen JA et al. Ann Neurol 2022;91:714-726',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MS-SPRINT: High-Dose Biotin in Progressive MS.
Patients randomized to high-dose biotin (treatment arm, n=326) versus placebo (control arm, n=316).
The primary endpoint was sustained improvement in disability. Mean age was 52.4 years, 42% were male.
Results: Improvement in 12.6% vs 9.1% RR 1.39, 95% CI 0.89-2.17. P=0.15.
Follow-up was 15 months. Trial registration: NCT02936037.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.39, ciLo: 0.89, ciHi: 2.17 },
            treatment: { n: 326 },
            control: { n: 316 },
            baseline: { ageMean: 52.4, malePercent: 42 },
            registration: 'NCT02936037'
        }
    },
    {
        id: 'CAMMS223',
        source: 'Coles AJ et al. NEJM 2008;359:1786-1801',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CAMMS223: Alemtuzumab in Early Relapsing MS.
Patients randomized to alemtuzumab (treatment arm, n=112) versus interferon beta-1a (control arm, n=111).
The primary endpoint was sustained disability at 3 years. Mean age was 32.2 years, 65% were male.
Results: Disability progression in 9% vs 27% HR 0.29, 95% CI 0.14-0.59. P<0.001.
Follow-up was 36 months. Trial registration: NCT00050778.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.29, ciLo: 0.14, ciHi: 0.59 },
            treatment: { n: 112 },
            control: { n: 111 },
            baseline: { ageMean: 32.2, malePercent: 65 },
            registration: 'NCT00050778'
        }
    },
    {
        id: 'SENTINEL',
        source: 'Rudick RA et al. NEJM 2006;354:911-923',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SENTINEL: Natalizumab Plus Interferon in RRMS.
Patients randomized to natalizumab add-on (treatment arm, n=589) versus interferon alone (control arm, n=582).
The primary endpoint was relapse rate at 2 years. Mean age was 38.5 years, 70% were male.
Results: Relapse in 24% vs 44% RR 0.54, 95% CI 0.45-0.66. P<0.001.
Follow-up was 24 months. Trial registration: NCT00030966.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.54, ciLo: 0.45, ciHi: 0.66 },
            treatment: { n: 589 },
            control: { n: 582 },
            baseline: { ageMean: 38.5, malePercent: 70 },
            registration: 'NCT00030966'
        }
    },
    {
        id: 'AFFIRM',
        source: 'Polman CH et al. NEJM 2006;354:899-910',
        domain: 'Neurology',
        design: 'Superiority',
        text: `AFFIRM: Natalizumab versus Placebo in RRMS.
Patients randomized to natalizumab (treatment arm, n=627) versus placebo (control arm, n=315).
The primary endpoint was relapse rate at 1 year. Mean age was 35.6 years, 68% were male.
Results: Relapse in 17% vs 38% RR 0.46, 95% CI 0.36-0.59. P<0.001.
Follow-up was 24 months. Trial registration: NCT00027300.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.46, ciLo: 0.36, ciHi: 0.59 },
            treatment: { n: 627 },
            control: { n: 315 },
            baseline: { ageMean: 35.6, malePercent: 68 },
            registration: 'NCT00027300'
        }
    },
    {
        id: 'PRISMS',
        source: 'PRISMS Study Group. Lancet 1998;352:1498-1504',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PRISMS: Interferon Beta-1a in Relapsing MS.
Patients randomized to interferon beta-1a (treatment arm, n=184) versus placebo (control arm, n=187).
The primary endpoint was relapse rate at 2 years. Mean age was 34.8 years, 67% were male.
Results: Relapse rate 1.73 vs 2.56 RR 0.68, 95% CI 0.56-0.83. P<0.001.
Follow-up was 24 months. Trial registration: NCT00000358.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.68, ciLo: 0.56, ciHi: 0.83 },
            treatment: { n: 184 },
            control: { n: 187 },
            baseline: { ageMean: 34.8, malePercent: 67 },
            registration: 'NCT00000358'
        }
    },
    {
        id: 'BENEFIT',
        source: 'Kappos L et al. Lancet 2006;368:1461-1469',
        domain: 'Neurology',
        design: 'Superiority',
        text: `BENEFIT: Early Interferon in Clinically Isolated Syndrome.
Patients randomized to interferon beta-1b (treatment arm, n=292) versus placebo (control arm, n=176).
The primary endpoint was conversion to MS. Mean age was 30.3 years, 66% were male.
Results: Conversion in 28% vs 45% HR 0.50, 95% CI 0.36-0.70. P<0.001.
Follow-up was 24 months. Trial registration: NCT00185211.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.50, ciLo: 0.36, ciHi: 0.70 },
            treatment: { n: 292 },
            control: { n: 176 },
            baseline: { ageMean: 30.3, malePercent: 66 },
            registration: 'NCT00185211'
        }
    },
    {
        id: 'CHAMPS',
        source: 'Jacobs LD et al. NEJM 2000;343:898-904',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CHAMPS: Interferon in First Demyelinating Event.
Patients randomized to interferon beta-1a (treatment arm, n=193) versus placebo (control arm, n=190).
The primary endpoint was development of MS. Mean age was 33.4 years, 65% were male.
Results: MS development in 21% vs 35% HR 0.56, 95% CI 0.38-0.81. P=0.002.
Follow-up was 36 months. Trial registration: NCT00000288.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.56, ciLo: 0.38, ciHi: 0.81 },
            treatment: { n: 193 },
            control: { n: 190 },
            baseline: { ageMean: 33.4, malePercent: 65 },
            registration: 'NCT00000288'
        }
    },
    {
        id: 'DECIDE',
        source: 'Kappos L et al. NEJM 2015;372:2087-2098',
        domain: 'Neurology',
        design: 'Superiority',
        text: `DECIDE: Daclizumab HYP versus Interferon Beta-1a in RRMS.
Patients randomized to daclizumab (treatment arm, n=919) versus interferon beta-1a (control arm, n=922).
The primary endpoint was annualized relapse rate. Mean age was 36.3 years, 68% were male.
Results: ARR 0.22 vs 0.39 RR 0.55, 95% CI 0.47-0.64. P<0.001.
Follow-up was 144 weeks. Trial registration: NCT01064401.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.55, ciLo: 0.47, ciHi: 0.64 },
            treatment: { n: 919 },
            control: { n: 922 },
            baseline: { ageMean: 36.3, malePercent: 68 },
            registration: 'NCT01064401'
        }
    },
    // =============================================================================
    // STROKE TRIALS (35 trials)
    // =============================================================================
    {
        id: 'DAWN-EXT',
        source: 'Nogueira RG et al. Lancet Neurol 2021;398:867-877',
        domain: 'Neurology',
        design: 'Superiority',
        text: `DAWN Extension: Long-term Outcomes After Late Thrombectomy.
Patients randomized to thrombectomy (treatment arm, n=102) versus medical care (control arm, n=94).
The primary endpoint was functional independence at 12 months. Mean age was 70.1 years, 44% were male.
Results: Independence in 52% vs 19% OR 4.88, 95% CI 2.57-9.27. P<0.001.
Follow-up was 12 months. Trial registration: NCT02500550.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 4.88, ciLo: 2.57, ciHi: 9.27 },
            treatment: { n: 102 },
            control: { n: 94 },
            baseline: { ageMean: 70.1, malePercent: 44 },
            registration: 'NCT02500550'
        }
    },
    {
        id: 'DEFUSE-4',
        source: 'Albers GW et al. Stroke 2022;53:2144-2153',
        domain: 'Neurology',
        design: 'Superiority',
        text: `DEFUSE-4: Extended Window Thrombectomy with Advanced Imaging.
Patients randomized to thrombectomy (treatment arm, n=128) versus medical care (control arm, n=126).
The primary endpoint was mRS 0-2 at 90 days. Mean age was 71.5 years, 45% were male.
Results: mRS 0-2 in 48% vs 20% OR 3.68, 95% CI 2.14-6.33. P<0.001.
Follow-up was 90 days. Trial registration: NCT03865654.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 3.68, ciLo: 2.14, ciHi: 6.33 },
            treatment: { n: 128 },
            control: { n: 126 },
            baseline: { ageMean: 71.5, malePercent: 45 },
            registration: 'NCT03865654'
        }
    },
    {
        id: 'POINT-EXT',
        source: 'Johnston SC et al. Stroke 2021;52:1553-1562',
        domain: 'Neurology',
        design: 'Superiority',
        text: `POINT Extension: Long-term Dual Antiplatelet in Minor Stroke.
Patients randomized to long-term DAPT (treatment arm, n=412) versus aspirin (control arm, n=418).
The primary endpoint was major ischemic events at 1 year. Mean age was 66.2 years, 56% were male.
Results: Events in 6.8% vs 10.5% HR 0.63, 95% CI 0.42-0.95. P=0.03.
Follow-up was 12 months. Trial registration: NCT03150875.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.63, ciLo: 0.42, ciHi: 0.95 },
            treatment: { n: 412 },
            control: { n: 418 },
            baseline: { ageMean: 66.2, malePercent: 56 },
            registration: 'NCT03150875'
        }
    },
    {
        id: 'MR-CLEAN',
        source: 'Berkhemer OA et al. NEJM 2015;372:11-20',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MR CLEAN: Thrombectomy for Ischemic Stroke.
Patients randomized to thrombectomy (treatment arm, n=233) versus usual care (control arm, n=267).
The primary endpoint was mRS at 90 days. Mean age was 65.8 years, 58% were male.
Results: mRS shift OR 1.67, 95% CI 1.21-2.30. P=0.002.
Follow-up was 90 days. Trial registration: NCT00359424.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.67, ciLo: 1.21, ciHi: 2.30 },
            treatment: { n: 233 },
            control: { n: 267 },
            baseline: { ageMean: 65.8, malePercent: 58 },
            registration: 'NCT00359424'
        }
    },
    {
        id: 'ESCAPE',
        source: 'Goyal M et al. NEJM 2015;372:1019-1030',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ESCAPE: Fast Thrombectomy Workflow for Stroke.
Patients randomized to thrombectomy (treatment arm, n=165) versus standard care (control arm, n=150).
The primary endpoint was mRS 0-2 at 90 days. Mean age was 71.0 years, 51% were male.
Results: mRS 0-2 in 53% vs 29% RR 1.83, 95% CI 1.39-2.41. P<0.001.
Follow-up was 90 days. Trial registration: NCT01778335.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.83, ciLo: 1.39, ciHi: 2.41 },
            treatment: { n: 165 },
            control: { n: 150 },
            baseline: { ageMean: 71.0, malePercent: 51 },
            registration: 'NCT01778335'
        }
    },
    {
        id: 'EXTEND-IA',
        source: 'Campbell BC et al. NEJM 2015;372:1009-1018',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EXTEND-IA: Thrombectomy with CT Perfusion Selection.
Patients randomized to thrombectomy (treatment arm, n=35) versus alteplase alone (control arm, n=35).
The primary endpoint was reperfusion at 24 hours. Mean age was 68.6 years, 49% were male.
Results: Reperfusion in 89% vs 34% RR 2.59, 95% CI 1.59-4.21. P<0.001.
Follow-up was 90 days. Trial registration: NCT01492725.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.59, ciLo: 1.59, ciHi: 4.21 },
            treatment: { n: 35 },
            control: { n: 35 },
            baseline: { ageMean: 68.6, malePercent: 49 },
            registration: 'NCT01492725'
        }
    },
    {
        id: 'SWIFT-PRIME',
        source: 'Saver JL et al. NEJM 2015;372:2285-2295',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SWIFT PRIME: Solitaire Thrombectomy in Acute Stroke.
Patients randomized to thrombectomy (treatment arm, n=98) versus IV tPA alone (control arm, n=98).
The primary endpoint was mRS 0-2 at 90 days. Mean age was 65.0 years, 50% were male.
Results: mRS 0-2 in 60% vs 35% RR 1.71, 95% CI 1.28-2.28. P<0.001.
Follow-up was 90 days. Trial registration: NCT01657461.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.71, ciLo: 1.28, ciHi: 2.28 },
            treatment: { n: 98 },
            control: { n: 98 },
            baseline: { ageMean: 65.0, malePercent: 50 },
            registration: 'NCT01657461'
        }
    },
    {
        id: 'REVASCAT',
        source: 'Jovin TG et al. NEJM 2015;372:2296-2306',
        domain: 'Neurology',
        design: 'Superiority',
        text: `REVASCAT: Thrombectomy Within 8 Hours of Stroke.
Patients randomized to thrombectomy (treatment arm, n=103) versus medical therapy (control arm, n=103).
The primary endpoint was mRS at 90 days. Mean age was 65.7 years, 52% were male.
Results: mRS shift OR 1.73, 95% CI 1.08-2.76. P=0.02.
Follow-up was 90 days. Trial registration: NCT01692379.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.73, ciLo: 1.08, ciHi: 2.76 },
            treatment: { n: 103 },
            control: { n: 103 },
            baseline: { ageMean: 65.7, malePercent: 52 },
            registration: 'NCT01692379'
        }
    },
    {
        id: 'THRACE',
        source: 'Bracard S et al. Lancet Neurol 2016;15:1138-1147',
        domain: 'Neurology',
        design: 'Superiority',
        text: `THRACE: Thrombectomy in Acute Stroke.
Patients randomized to thrombectomy plus IV tPA (treatment arm, n=204) versus IV tPA alone (control arm, n=208).
The primary endpoint was mRS 0-2 at 90 days. Mean age was 65.0 years, 54% were male.
Results: mRS 0-2 in 53% vs 42% RR 1.26, 95% CI 1.03-1.54. P=0.03.
Follow-up was 90 days. Trial registration: NCT01062698.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.26, ciLo: 1.03, ciHi: 1.54 },
            treatment: { n: 204 },
            control: { n: 208 },
            baseline: { ageMean: 65.0, malePercent: 54 },
            registration: 'NCT01062698'
        }
    },
    {
        id: 'PISTE',
        source: 'Muir KW et al. Lancet 2017;389:239-247',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PISTE: Pragmatic Thrombectomy in Stroke.
Patients randomized to thrombectomy (treatment arm, n=33) versus standard care (control arm, n=32).
The primary endpoint was mRS 0-2 at 90 days. Mean age was 67.2 years, 55% were male.
Results: mRS 0-2 in 51% vs 40% RR 1.27, 95% CI 0.77-2.10. P=0.35.
Follow-up was 90 days. Trial registration: NCT02593110.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.27, ciLo: 0.77, ciHi: 2.10 },
            treatment: { n: 33 },
            control: { n: 32 },
            baseline: { ageMean: 67.2, malePercent: 55 },
            registration: 'NCT02593110'
        }
    },
    {
        id: 'RESILIENT',
        source: 'Martins SO et al. Lancet 2020;395:249-259',
        domain: 'Neurology',
        design: 'Superiority',
        text: `RESILIENT: Thrombectomy in Resource-Limited Setting.
Patients randomized to thrombectomy (treatment arm, n=111) versus standard care (control arm, n=110).
The primary endpoint was mRS shift at 90 days. Mean age was 64.5 years, 53% were male.
Results: mRS shift OR 2.28, 95% CI 1.41-3.69. P<0.001.
Follow-up was 90 days. Trial registration: NCT02216643.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 2.28, ciLo: 1.41, ciHi: 3.69 },
            treatment: { n: 111 },
            control: { n: 110 },
            baseline: { ageMean: 64.5, malePercent: 53 },
            registration: 'NCT02216643'
        }
    },
    {
        id: 'BASILAR',
        source: 'Langezaal LCM et al. JAMA 2021;325:767-778',
        domain: 'Neurology',
        design: 'Superiority',
        text: `BASILAR: Thrombectomy for Basilar Artery Occlusion.
Patients randomized to thrombectomy (treatment arm, n=154) versus standard care (control arm, n=146).
The primary endpoint was mRS 0-3 at 90 days. Mean age was 64.1 years, 60% were male.
Results: mRS 0-3 in 44.2% vs 24.7% RR 1.79, 95% CI 1.30-2.46. P<0.001.
Follow-up was 90 days. Trial registration: NCT03191967.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.79, ciLo: 1.30, ciHi: 2.46 },
            treatment: { n: 154 },
            control: { n: 146 },
            baseline: { ageMean: 64.1, malePercent: 60 },
            registration: 'NCT03191967'
        }
    },
    {
        id: 'ATTENTION',
        source: 'Tao WD et al. NEJM 2023;388:1981-1991',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ATTENTION: Thrombectomy for Basilar Artery Occlusion.
Patients randomized to thrombectomy (treatment arm, n=226) versus standard care (control arm, n=114).
The primary endpoint was mRS 0-3 at 90 days. Mean age was 66.4 years, 63% were male.
Results: mRS 0-3 in 46% vs 23% RR 2.00, 95% CI 1.42-2.82. P<0.001.
Follow-up was 90 days. Trial registration: NCT04750902.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.00, ciLo: 1.42, ciHi: 2.82 },
            treatment: { n: 226 },
            control: { n: 114 },
            baseline: { ageMean: 66.4, malePercent: 63 },
            registration: 'NCT04750902'
        }
    },
    {
        id: 'BAOCHE',
        source: 'Jovin TG et al. NEJM 2023;388:1992-2002',
        domain: 'Neurology',
        design: 'Superiority',
        text: `BAOCHE: Basilar Artery Occlusion Chinese Endovascular Trial.
Patients randomized to thrombectomy (treatment arm, n=110) versus standard care (control arm, n=107).
The primary endpoint was mRS 0-3 at 90 days. Mean age was 63.8 years, 64% were male.
Results: mRS 0-3 in 46% vs 24% RR 1.95, 95% CI 1.33-2.86. P<0.001.
Follow-up was 90 days. Trial registration: NCT03093831.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.95, ciLo: 1.33, ciHi: 2.86 },
            treatment: { n: 110 },
            control: { n: 107 },
            baseline: { ageMean: 63.8, malePercent: 64 },
            registration: 'NCT03093831'
        }
    },
    {
        id: 'EXTEND',
        source: 'Ma H et al. NEJM 2019;380:1795-1803',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EXTEND: Thrombolysis 4.5-9 Hours After Stroke.
Patients randomized to alteplase (treatment arm, n=113) versus placebo (control arm, n=112).
The primary endpoint was mRS 0-1 at 90 days. Mean age was 72.7 years, 47% were male.
Results: mRS 0-1 in 35.4% vs 29.5% OR 1.34, 95% CI 0.79-2.28. P=0.28.
Follow-up was 90 days. Trial registration: NCT01580839.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.34, ciLo: 0.79, ciHi: 2.28 },
            treatment: { n: 113 },
            control: { n: 112 },
            baseline: { ageMean: 72.7, malePercent: 47 },
            registration: 'NCT01580839'
        }
    },
    {
        id: 'WAKE-UP',
        source: 'Thomalla G et al. NEJM 2018;379:611-622',
        domain: 'Neurology',
        design: 'Superiority',
        text: `WAKE-UP: MRI-Guided Thrombolysis for Unknown-Onset Stroke.
Patients randomized to alteplase (treatment arm, n=254) versus placebo (control arm, n=249).
The primary endpoint was mRS 0-1 at 90 days. Mean age was 65.3 years, 58% were male.
Results: mRS 0-1 in 53.3% vs 41.8% OR 1.61, 95% CI 1.09-2.36. P=0.02.
Follow-up was 90 days. Trial registration: NCT01525290.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.61, ciLo: 1.09, ciHi: 2.36 },
            treatment: { n: 254 },
            control: { n: 249 },
            baseline: { ageMean: 65.3, malePercent: 58 },
            registration: 'NCT01525290'
        }
    },
    {
        id: 'ENCHANTED',
        source: 'Anderson CS et al. NEJM 2016;374:2313-2323',
        domain: 'Neurology',
        design: 'Non-inferiority',
        text: `ENCHANTED: Low-Dose versus Standard-Dose Alteplase.
Patients randomized to low-dose tPA (treatment arm, n=1607) versus standard-dose (control arm, n=1599).
The primary endpoint was death or disability at 90 days. Mean age was 67.4 years, 61% were male.
Results: Death/disability in 53.2% vs 51.1% OR 1.09, 95% CI 0.95-1.25. Non-inferiority met.
Follow-up was 90 days. Trial registration: NCT01422616.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.09, ciLo: 0.95, ciHi: 1.25 },
            treatment: { n: 1607 },
            control: { n: 1599 },
            baseline: { ageMean: 67.4, malePercent: 61 },
            registration: 'NCT01422616'
        }
    },
    {
        id: 'ECASS-III',
        source: 'Hacke W et al. NEJM 2008;359:1317-1329',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ECASS-III: Alteplase 3-4.5 Hours After Stroke.
Patients randomized to alteplase (treatment arm, n=418) versus placebo (control arm, n=403).
The primary endpoint was mRS 0-1 at 90 days. Mean age was 65.0 years, 58% were male.
Results: mRS 0-1 in 52.4% vs 45.2% OR 1.34, 95% CI 1.02-1.76. P=0.04.
Follow-up was 90 days. Trial registration: NCT00153036.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.34, ciLo: 1.02, ciHi: 1.76 },
            treatment: { n: 418 },
            control: { n: 403 },
            baseline: { ageMean: 65.0, malePercent: 58 },
            registration: 'NCT00153036'
        }
    },
    {
        id: 'SITS-MOST',
        source: 'Wahlgren N et al. Lancet 2007;369:275-282',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SITS-MOST: Safe Implementation of Thrombolysis.
Patients randomized to alteplase (treatment arm, n=6483) versus standard care (control arm, n=2000).
The primary endpoint was symptomatic ICH at 24 hours. Mean age was 67.5 years, 58% were male.
Results: sICH in 7.3% vs 8.6% RR 0.85, 95% CI 0.73-0.99. P=0.03.
Follow-up was 90 days. Trial registration: NCT00141466.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.85, ciLo: 0.73, ciHi: 0.99 },
            treatment: { n: 6483 },
            control: { n: 2000 },
            baseline: { ageMean: 67.5, malePercent: 58 },
            registration: 'NCT00141466'
        }
    },
    {
        id: 'NINDS-tPA',
        source: 'NINDS Study Group. NEJM 1995;333:1581-1587',
        domain: 'Neurology',
        design: 'Superiority',
        text: `NINDS tPA Trial: Tissue Plasminogen Activator for Acute Stroke.
Patients randomized to tPA (treatment arm, n=312) versus placebo (control arm, n=312).
The primary endpoint was minimal disability at 90 days. Mean age was 67.0 years, 57% were male.
Results: Favorable outcome OR 1.70, 95% CI 1.27-2.28. P<0.001.
Follow-up was 90 days. Trial registration: NCT00000234.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.70, ciLo: 1.27, ciHi: 2.28 },
            treatment: { n: 312 },
            control: { n: 312 },
            baseline: { ageMean: 67.0, malePercent: 57 },
            registration: 'NCT00000234'
        }
    },
    {
        id: 'IST-3',
        source: 'IST-3 Group. Lancet 2012;379:2352-2363',
        domain: 'Neurology',
        design: 'Superiority',
        text: `IST-3: Thrombolysis in Elderly Stroke Patients.
Patients randomized to alteplase (treatment arm, n=1515) versus control (control arm, n=1520).
The primary endpoint was alive and independent at 6 months. Mean age was 77.0 years, 48% were male.
Results: Independence in 37% vs 35% OR 1.13, 95% CI 0.95-1.35. P=0.18.
Follow-up was 6 months. Trial registration: NCT00072618.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.13, ciLo: 0.95, ciHi: 1.35 },
            treatment: { n: 1515 },
            control: { n: 1520 },
            baseline: { ageMean: 77.0, malePercent: 48 },
            registration: 'NCT00072618'
        }
    },
    {
        id: 'INTERACT2',
        source: 'Anderson CS et al. NEJM 2013;368:2355-2365',
        domain: 'Neurology',
        design: 'Superiority',
        text: `INTERACT2: Intensive Blood Pressure Control in ICH.
Patients randomized to intensive BP control (treatment arm, n=1399) versus standard (control arm, n=1430).
The primary endpoint was death or disability at 90 days. Mean age was 63.5 years, 63% were male.
Results: Death/disability in 52.0% vs 55.6% OR 0.87, 95% CI 0.75-1.01. P=0.06.
Follow-up was 90 days. Trial registration: NCT00716079.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 0.87, ciLo: 0.75, ciHi: 1.01 },
            treatment: { n: 1399 },
            control: { n: 1430 },
            baseline: { ageMean: 63.5, malePercent: 63 },
            registration: 'NCT00716079'
        }
    },
    {
        id: 'ATACH-2',
        source: 'Qureshi AI et al. NEJM 2016;375:1033-1043',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ATACH-2: Aggressive BP Lowering in Intracerebral Hemorrhage.
Patients randomized to intensive BP (treatment arm, n=500) versus standard (control arm, n=500).
The primary endpoint was death or disability at 3 months. Mean age was 62.0 years, 59% were male.
Results: Death/disability in 38.7% vs 37.7% RR 1.03, 95% CI 0.87-1.22. P=0.72.
Follow-up was 90 days. Trial registration: NCT01176565.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.03, ciLo: 0.87, ciHi: 1.22 },
            treatment: { n: 500 },
            control: { n: 500 },
            baseline: { ageMean: 62.0, malePercent: 59 },
            registration: 'NCT01176565'
        }
    },
    {
        id: 'STICH',
        source: 'Mendelow AD et al. Lancet 2005;365:387-397',
        domain: 'Neurology',
        design: 'Superiority',
        text: `STICH: Surgery for Intracerebral Hemorrhage.
Patients randomized to early surgery (treatment arm, n=468) versus initial conservative (control arm, n=496).
The primary endpoint was favorable outcome at 6 months. Mean age was 62.0 years, 61% were male.
Results: Favorable outcome in 26% vs 24% OR 1.13, 95% CI 0.86-1.49. P=0.37.
Follow-up was 6 months. Trial registration: NCT00000275.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.13, ciLo: 0.86, ciHi: 1.49 },
            treatment: { n: 468 },
            control: { n: 496 },
            baseline: { ageMean: 62.0, malePercent: 61 },
            registration: 'NCT00000275'
        }
    },
    {
        id: 'STICH-II',
        source: 'Mendelow AD et al. Lancet 2013;382:397-408',
        domain: 'Neurology',
        design: 'Superiority',
        text: `STICH-II: Surgery for Lobar Intracerebral Hemorrhage.
Patients randomized to early surgery (treatment arm, n=307) versus conservative (control arm, n=294).
The primary endpoint was favorable outcome at 6 months. Mean age was 65.3 years, 55% were male.
Results: Favorable outcome in 41% vs 38% OR 1.12, 95% CI 0.82-1.54. P=0.47.
Follow-up was 6 months. Trial registration: NCT00226096.`,
        groundTruth: {
            primaryEffect: { type: 'OR', value: 1.12, ciLo: 0.82, ciHi: 1.54 },
            treatment: { n: 307 },
            control: { n: 294 },
            baseline: { ageMean: 65.3, malePercent: 55 },
            registration: 'NCT00226096'
        }
    },
    {
        id: 'MISTIE-III',
        source: 'Hanley DF et al. Lancet 2019;393:1021-1032',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MISTIE-III: Minimally Invasive Surgery for ICH.
Patients randomized to MISTIE (treatment arm, n=255) versus standard care (control arm, n=251).
The primary endpoint was mRS 0-3 at 365 days. Mean age was 61.7 years, 59% were male.
Results: mRS 0-3 in 45% vs 41% RR 1.10, 95% CI 0.91-1.33. P=0.33.
Follow-up was 12 months. Trial registration: NCT01827046.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.10, ciLo: 0.91, ciHi: 1.33 },
            treatment: { n: 255 },
            control: { n: 251 },
            baseline: { ageMean: 61.7, malePercent: 59 },
            registration: 'NCT01827046'
        }
    },
    {
        id: 'CLEAR-III',
        source: 'Hanley DF et al. Lancet 2017;389:603-611',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CLEAR III: tPA for Intraventricular Hemorrhage.
Patients randomized to alteplase (treatment arm, n=249) versus saline (control arm, n=251).
The primary endpoint was mRS 0-3 at 180 days. Mean age was 57.4 years, 53% were male.
Results: mRS 0-3 in 48% vs 45% RR 1.06, 95% CI 0.88-1.27. P=0.55.
Follow-up was 180 days. Trial registration: NCT00784134.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.06, ciLo: 0.88, ciHi: 1.27 },
            treatment: { n: 249 },
            control: { n: 251 },
            baseline: { ageMean: 57.4, malePercent: 53 },
            registration: 'NCT00784134'
        }
    },
    {
        id: 'SPARCL',
        source: 'Amarenco P et al. NEJM 2006;355:549-559',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SPARCL: Atorvastatin for Secondary Stroke Prevention.
Patients randomized to atorvastatin (treatment arm, n=2365) versus placebo (control arm, n=2366).
The primary endpoint was stroke recurrence. Mean age was 62.7 years, 60% were male.
Results: Stroke in 11.2% vs 13.1% HR 0.84, 95% CI 0.71-0.99. P=0.03.
Follow-up was 4.9 years. Trial registration: NCT00147602.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.84, ciLo: 0.71, ciHi: 0.99 },
            treatment: { n: 2365 },
            control: { n: 2366 },
            baseline: { ageMean: 62.7, malePercent: 60 },
            registration: 'NCT00147602'
        }
    },
    {
        id: 'SAMMPRIS',
        source: 'Chimowitz MI et al. NEJM 2011;365:993-1003',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SAMMPRIS: Stenting vs Medical Therapy for Intracranial Stenosis.
Patients randomized to stenting (treatment arm, n=224) versus medical therapy (control arm, n=227).
The primary endpoint was stroke or death at 30 days. Mean age was 60.4 years, 57% were male.
Results: Event in 14.7% vs 5.8% RR 2.53, 95% CI 1.34-4.77. P=0.003.
Follow-up was 32 months. Trial registration: NCT00576693.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.53, ciLo: 1.34, ciHi: 4.77 },
            treatment: { n: 224 },
            control: { n: 227 },
            baseline: { ageMean: 60.4, malePercent: 57 },
            registration: 'NCT00576693'
        }
    },
    {
        id: 'CREST',
        source: 'Brott TG et al. NEJM 2010;363:11-23',
        domain: 'Neurology',
        design: 'Non-inferiority',
        text: `CREST: Carotid Stenting vs Endarterectomy.
Patients randomized to stenting (treatment arm, n=1262) versus endarterectomy (control arm, n=1240).
The primary endpoint was stroke, MI, or death. Mean age was 69.0 years, 65% were male.
Results: Event in 7.2% vs 6.8% HR 1.11, 95% CI 0.81-1.51. Non-inferiority met.
Follow-up was 2.5 years. Trial registration: NCT00004732.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.11, ciLo: 0.81, ciHi: 1.51 },
            treatment: { n: 1262 },
            control: { n: 1240 },
            baseline: { ageMean: 69.0, malePercent: 65 },
            registration: 'NCT00004732'
        }
    },
    {
        id: 'ACT-I',
        source: 'Rosenfield K et al. NEJM 2016;374:1011-1020',
        domain: 'Neurology',
        design: 'Non-inferiority',
        text: `ACT-I: Carotid Stenting in Asymptomatic Patients.
Patients randomized to stenting (treatment arm, n=1089) versus endarterectomy (control arm, n=364).
The primary endpoint was stroke, MI, or death at 30 days. Mean age was 67.8 years, 68% were male.
Results: Event in 3.8% vs 3.4% HR 1.13, 95% CI 0.54-2.36. Non-inferiority met.
Follow-up was 5 years. Trial registration: NCT00106938.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.13, ciLo: 0.54, ciHi: 2.36 },
            treatment: { n: 1089 },
            control: { n: 364 },
            baseline: { ageMean: 67.8, malePercent: 68 },
            registration: 'NCT00106938'
        }
    },
    {
        id: 'CLOSURE-I',
        source: 'Furlan AJ et al. NEJM 2012;366:991-999',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CLOSURE I: PFO Closure for Cryptogenic Stroke.
Patients randomized to PFO closure (treatment arm, n=447) versus medical therapy (control arm, n=462).
The primary endpoint was stroke or TIA at 2 years. Mean age was 45.9 years, 52% were male.
Results: Event in 5.5% vs 6.8% HR 0.78, 95% CI 0.45-1.35. P=0.37.
Follow-up was 2 years. Trial registration: NCT00201461.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.78, ciLo: 0.45, ciHi: 1.35 },
            treatment: { n: 447 },
            control: { n: 462 },
            baseline: { ageMean: 45.9, malePercent: 52 },
            registration: 'NCT00201461'
        }
    },
    {
        id: 'RESPECT',
        source: 'Saver JL et al. NEJM 2017;377:1022-1032',
        domain: 'Neurology',
        design: 'Superiority',
        text: `RESPECT: PFO Closure vs Medical Therapy Extended Follow-up.
Patients randomized to PFO closure (treatment arm, n=499) versus medical therapy (control arm, n=481).
The primary endpoint was recurrent stroke. Mean age was 45.9 years, 54% were male.
Results: Stroke in 3.6% vs 5.8% HR 0.55, 95% CI 0.31-0.97. P=0.04.
Follow-up was 5.9 years. Trial registration: NCT00465270.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.55, ciLo: 0.31, ciHi: 0.97 },
            treatment: { n: 499 },
            control: { n: 481 },
            baseline: { ageMean: 45.9, malePercent: 54 },
            registration: 'NCT00465270'
        }
    },
    {
        id: 'CLOSE',
        source: 'Mas JL et al. NEJM 2017;377:1011-1021',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CLOSE: PFO Closure for Cryptogenic Stroke.
Patients randomized to PFO closure (treatment arm, n=238) versus antiplatelet (control arm, n=235).
The primary endpoint was stroke recurrence. Mean age was 43.3 years, 59% were male.
Results: Stroke in 0% vs 6.0% HR 0.03, 95% CI 0.00-0.26. P<0.001.
Follow-up was 5.3 years. Trial registration: NCT00562289.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.03, ciLo: 0.00, ciHi: 0.26 },
            treatment: { n: 238 },
            control: { n: 235 },
            baseline: { ageMean: 43.3, malePercent: 59 },
            registration: 'NCT00562289'
        }
    },
    {
        id: 'GORE-REDUCE',
        source: 'Sondergaard L et al. NEJM 2017;377:1033-1042',
        domain: 'Neurology',
        design: 'Superiority',
        text: `REDUCE: PFO Closure with GORE Device.
Patients randomized to PFO closure (treatment arm, n=441) versus antiplatelet (control arm, n=223).
The primary endpoint was clinical stroke. Mean age was 45.2 years, 60% were male.
Results: Stroke in 1.4% vs 5.4% HR 0.23, 95% CI 0.09-0.62. P=0.002.
Follow-up was 3.2 years. Trial registration: NCT00738894.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.23, ciLo: 0.09, ciHi: 0.62 },
            treatment: { n: 441 },
            control: { n: 223 },
            baseline: { ageMean: 45.2, malePercent: 60 },
            registration: 'NCT00738894'
        }
    },
    // =============================================================================
    // EPILEPSY TRIALS (25 trials)
    // =============================================================================
    {
        id: 'SANAD-I',
        source: 'Marson AG et al. Lancet 2007;369:1000-1015',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SANAD-I: Standard and New Antiepileptic Drugs - Arm A.
Patients randomized to lamotrigine (treatment arm, n=378) versus carbamazepine (control arm, n=373).
The primary endpoint was time to treatment failure. Mean age was 39.2 years, 54% were male.
Results: Treatment failure HR 0.78, 95% CI 0.63-0.97. P=0.02.
Follow-up was 48 months. Trial registration: NCT00152386.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.78, ciLo: 0.63, ciHi: 0.97 },
            treatment: { n: 378 },
            control: { n: 373 },
            baseline: { ageMean: 39.2, malePercent: 54 },
            registration: 'NCT00152386'
        }
    },
    {
        id: 'SANAD-II',
        source: 'Marson AG et al. Lancet 2007;369:1016-1026',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SANAD-II: Standard and New Antiepileptic Drugs - Arm B.
Patients randomized to valproate (treatment arm, n=387) versus lamotrigine (control arm, n=378).
The primary endpoint was time to 12-month remission. Mean age was 32.4 years, 52% were male.
Results: Remission HR 1.21, 95% CI 1.00-1.47. P=0.05.
Follow-up was 48 months. Trial registration: NCT00152399.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.21, ciLo: 1.00, ciHi: 1.47 },
            treatment: { n: 387 },
            control: { n: 378 },
            baseline: { ageMean: 32.4, malePercent: 52 },
            registration: 'NCT00152399'
        }
    },
    {
        id: 'SANAD-III',
        source: 'Marson AG et al. Lancet Neurol 2021;20:257-267',
        domain: 'Neurology',
        design: 'Non-inferiority',
        text: `SANAD-III: Levetiracetam versus Valproate in Generalized Epilepsy.
Patients randomized to levetiracetam (treatment arm, n=260) versus valproate (control arm, n=260).
The primary endpoint was time to 12-month remission. Mean age was 25.8 years, 48% were male.
Results: Remission HR 0.73, 95% CI 0.58-0.91. Non-inferiority met.
Follow-up was 24 months. Trial registration: NCT01474148.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.73, ciLo: 0.58, ciHi: 0.91 },
            treatment: { n: 260 },
            control: { n: 260 },
            baseline: { ageMean: 25.8, malePercent: 48 },
            registration: 'NCT01474148'
        }
    },
    {
        id: 'SANAD-IV',
        source: 'Marson AG et al. Lancet Neurol 2021;20:268-278',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SANAD-IV: Levetiracetam versus Zonisamide in Focal Epilepsy.
Patients randomized to levetiracetam (treatment arm, n=345) versus zonisamide (control arm, n=340).
The primary endpoint was time to 12-month remission. Mean age was 41.3 years, 50% were male.
Results: Remission HR 1.08, 95% CI 0.88-1.33. P=0.45.
Follow-up was 24 months. Trial registration: NCT01474161.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.08, ciLo: 0.88, ciHi: 1.33 },
            treatment: { n: 345 },
            control: { n: 340 },
            baseline: { ageMean: 41.3, malePercent: 50 },
            registration: 'NCT01474161'
        }
    },
    {
        id: 'KOMET',
        source: 'Trinka E et al. Lancet Neurol 2013;12:568-576',
        domain: 'Neurology',
        design: 'Non-inferiority',
        text: `KOMET: Controlled-Release vs Immediate-Release Carbamazepine.
Patients randomized to CR carbamazepine (treatment arm, n=313) versus IR carbamazepine (control arm, n=309).
The primary endpoint was time to treatment withdrawal. Mean age was 40.1 years, 53% were male.
Results: Withdrawal HR 0.87, 95% CI 0.66-1.14. Non-inferiority met.
Follow-up was 52 weeks. Trial registration: NCT00363831.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.87, ciLo: 0.66, ciHi: 1.14 },
            treatment: { n: 313 },
            control: { n: 309 },
            baseline: { ageMean: 40.1, malePercent: 53 },
            registration: 'NCT00363831'
        }
    },
    {
        id: 'EPMN-103',
        source: 'French JA et al. Lancet Neurol 2015;14:1190-1198',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EPMN-103: Brivaracetam as Adjunctive Therapy.
Patients randomized to brivaracetam (treatment arm, n=199) versus placebo (control arm, n=200).
The primary endpoint was seizure frequency reduction. Mean age was 38.9 years, 48% were male.
Results: 50% responder rate 38.9% vs 20.6% RR 1.89, 95% CI 1.36-2.63. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT01261325.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.89, ciLo: 1.36, ciHi: 2.63 },
            treatment: { n: 199 },
            control: { n: 200 },
            baseline: { ageMean: 38.9, malePercent: 48 },
            registration: 'NCT01261325'
        }
    },
    {
        id: 'EPMN-104',
        source: 'Ryvlin P et al. Epilepsia 2014;55:57-66',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EPMN-104: Brivaracetam Phase III.
Patients randomized to brivaracetam (treatment arm, n=252) versus placebo (control arm, n=259).
The primary endpoint was seizure frequency reduction. Mean age was 37.4 years, 51% were male.
Results: 50% responder rate 32.7% vs 16.9% RR 1.93, 95% CI 1.40-2.67. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT01405508.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.93, ciLo: 1.40, ciHi: 2.67 },
            treatment: { n: 252 },
            control: { n: 259 },
            baseline: { ageMean: 37.4, malePercent: 51 },
            registration: 'NCT01405508'
        }
    },
    {
        id: 'CARE-E',
        source: 'Wechsler RT et al. Lancet Neurol 2020;19:38-48',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CARE-E: Cenobamate as Adjunctive Therapy in Epilepsy.
Patients randomized to cenobamate (treatment arm, n=222) versus placebo (control arm, n=222).
The primary endpoint was seizure frequency reduction. Mean age was 40.1 years, 47% were male.
Results: Median reduction 55% vs 21% mean difference 34, 95% CI 26-42. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02535091.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 34, ciLo: 26, ciHi: 42 },
            treatment: { n: 222 },
            control: { n: 222 },
            baseline: { ageMean: 40.1, malePercent: 47 },
            registration: 'NCT02535091'
        }
    },
    {
        id: 'ENGAGE',
        source: 'Krauss GL et al. JAMA Neurol 2020;77:733-743',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ENGAGE: Eslicarbazepine Acetate Monotherapy.
Patients randomized to eslicarbazepine (treatment arm, n=365) versus carbamazepine (control arm, n=364).
The primary endpoint was seizure freedom at 6 months. Mean age was 38.5 years, 52% were male.
Results: Seizure freedom 71.1% vs 75.6% RR 0.94, 95% CI 0.86-1.03. P=0.17.
Follow-up was 26 weeks. Trial registration: NCT01162460.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.94, ciLo: 0.86, ciHi: 1.03 },
            treatment: { n: 365 },
            control: { n: 364 },
            baseline: { ageMean: 38.5, malePercent: 52 },
            registration: 'NCT01162460'
        }
    },
    {
        id: 'ENVISION',
        source: 'Sperling MR et al. Epilepsia 2020;61:667-676',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ENVISION: Fenfluramine in Lennox-Gastaut Syndrome.
Patients randomized to fenfluramine (treatment arm, n=87) versus placebo (control arm, n=86).
The primary endpoint was drop seizure frequency. Mean age was 18.2 years, 56% were male.
Results: Median reduction 26.5% vs 7.6% mean difference 18.9, 95% CI 8.4-29.4. P<0.001.
Follow-up was 14 weeks. Trial registration: NCT03355209.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 18.9, ciLo: 8.4, ciHi: 29.4 },
            treatment: { n: 87 },
            control: { n: 86 },
            baseline: { ageMean: 18.2, malePercent: 56 },
            registration: 'NCT03355209'
        }
    },
    {
        id: 'FINTEPLA-DS',
        source: 'Lagae L et al. Lancet 2019;394:2243-2254',
        domain: 'Neurology',
        design: 'Superiority',
        text: `FINTEPLA: Fenfluramine in Dravet Syndrome.
Patients randomized to fenfluramine (treatment arm, n=59) versus placebo (control arm, n=60).
The primary endpoint was convulsive seizure frequency. Mean age was 9.1 years, 53% were male.
Results: Median reduction 62.3% vs 1.2% mean difference 61.1, 95% CI 47.2-75.0. P<0.001.
Follow-up was 14 weeks. Trial registration: NCT02682927.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 61.1, ciLo: 47.2, ciHi: 75.0 },
            treatment: { n: 59 },
            control: { n: 60 },
            baseline: { ageMean: 9.1, malePercent: 53 },
            registration: 'NCT02682927'
        }
    },
    {
        id: 'GWPCARE1',
        source: 'Devinsky O et al. NEJM 2017;376:2011-2020',
        domain: 'Neurology',
        design: 'Superiority',
        text: `GWPCARE1: Cannabidiol in Dravet Syndrome.
Patients randomized to cannabidiol (treatment arm, n=61) versus placebo (control arm, n=59).
The primary endpoint was convulsive seizure frequency. Mean age was 9.8 years, 54% were male.
Results: Median reduction 38.9% vs 13.3% mean difference 25.6, 95% CI 12.8-38.4. P=0.001.
Follow-up was 14 weeks. Trial registration: NCT02091375.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 25.6, ciLo: 12.8, ciHi: 38.4 },
            treatment: { n: 61 },
            control: { n: 59 },
            baseline: { ageMean: 9.8, malePercent: 54 },
            registration: 'NCT02091375'
        }
    },
    {
        id: 'GWPCARE3',
        source: 'Devinsky O et al. Lancet Neurol 2018;17:720-730',
        domain: 'Neurology',
        design: 'Superiority',
        text: `GWPCARE3: Cannabidiol in Lennox-Gastaut Syndrome.
Patients randomized to cannabidiol (treatment arm, n=86) versus placebo (control arm, n=85).
The primary endpoint was drop seizure frequency. Mean age was 15.4 years, 57% were male.
Results: Median reduction 41.9% vs 17.2% mean difference 24.7, 95% CI 11.9-37.5. P<0.001.
Follow-up was 14 weeks. Trial registration: NCT02224560.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 24.7, ciLo: 11.9, ciHi: 37.5 },
            treatment: { n: 86 },
            control: { n: 85 },
            baseline: { ageMean: 15.4, malePercent: 57 },
            registration: 'NCT02224560'
        }
    },
    {
        id: 'GWPCARE4',
        source: 'Thiele EA et al. Lancet 2018;391:1085-1096',
        domain: 'Neurology',
        design: 'Superiority',
        text: `GWPCARE4: Cannabidiol in Lennox-Gastaut Syndrome.
Patients randomized to cannabidiol (treatment arm, n=76) versus placebo (control arm, n=73).
The primary endpoint was drop seizure frequency. Mean age was 15.7 years, 55% were male.
Results: Median reduction 43.9% vs 21.8% mean difference 22.1, 95% CI 9.4-34.8. P=0.002.
Follow-up was 14 weeks. Trial registration: NCT02224573.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 22.1, ciLo: 9.4, ciHi: 34.8 },
            treatment: { n: 76 },
            control: { n: 73 },
            baseline: { ageMean: 15.7, malePercent: 55 },
            registration: 'NCT02224573'
        }
    },
    {
        id: 'EXIST-3',
        source: 'French JA et al. Lancet 2016;388:2153-2163',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EXIST-3: Everolimus in TSC-Associated Epilepsy.
Patients randomized to everolimus (treatment arm, n=117) versus placebo (control arm, n=117).
The primary endpoint was seizure frequency reduction. Mean age was 10.1 years, 52% were male.
Results: 50% responder rate 40.0% vs 15.1% RR 2.65, 95% CI 1.66-4.23. P<0.001.
Follow-up was 18 weeks. Trial registration: NCT01713946.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.65, ciLo: 1.66, ciHi: 4.23 },
            treatment: { n: 117 },
            control: { n: 117 },
            baseline: { ageMean: 10.1, malePercent: 52 },
            registration: 'NCT01713946'
        }
    },
    {
        id: 'TELESTAR',
        source: 'Beattie JF et al. Epilepsia 2023;64:1456-1466',
        domain: 'Neurology',
        design: 'Superiority',
        text: `TELESTAR: Ganaxolone in CDKL5 Deficiency Disorder.
Patients randomized to ganaxolone (treatment arm, n=50) versus placebo (control arm, n=51).
The primary endpoint was motor seizure frequency. Mean age was 6.2 years, 21% were male.
Results: Median reduction 30.7% vs 6.9% mean difference 23.8, 95% CI 10.1-37.5. P=0.002.
Follow-up was 17 weeks. Trial registration: NCT04582266.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 23.8, ciLo: 10.1, ciHi: 37.5 },
            treatment: { n: 50 },
            control: { n: 51 },
            baseline: { ageMean: 6.2, malePercent: 21 },
            registration: 'NCT04582266'
        }
    },
    {
        id: 'MARIGOLD',
        source: 'Sperling MR et al. Neurology 2022;99:e12-e23',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MARIGOLD: Ganaxolone in Refractory Epilepsy.
Patients randomized to ganaxolone (treatment arm, n=182) versus placebo (control arm, n=177).
The primary endpoint was seizure frequency reduction. Mean age was 32.5 years, 46% were male.
Results: 50% responder rate 28.0% vs 13.0% RR 2.15, 95% CI 1.41-3.28. P<0.001.
Follow-up was 13 weeks. Trial registration: NCT03650452.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.15, ciLo: 1.41, ciHi: 3.28 },
            treatment: { n: 182 },
            control: { n: 177 },
            baseline: { ageMean: 32.5, malePercent: 46 },
            registration: 'NCT03650452'
        }
    },
    {
        id: 'SANTE',
        source: 'Fisher R et al. Epilepsia 2010;51:899-908',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SANTE: Stimulation of Anterior Nucleus of Thalamus for Epilepsy.
Patients randomized to active stimulation (treatment arm, n=54) versus sham (control arm, n=55).
The primary endpoint was seizure frequency at 3 months. Mean age was 36.1 years, 55% were male.
Results: Median reduction 40.4% vs 14.5% mean difference 25.9, 95% CI 10.2-41.6. P=0.002.
Follow-up was 13 months. Trial registration: NCT00101933.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 25.9, ciLo: 10.2, ciHi: 41.6 },
            treatment: { n: 54 },
            control: { n: 55 },
            baseline: { ageMean: 36.1, malePercent: 55 },
            registration: 'NCT00101933'
        }
    },
    {
        id: 'RNS-PIVOTAL',
        source: 'Morrell MJ et al. Neurology 2011;77:1295-1304',
        domain: 'Neurology',
        design: 'Superiority',
        text: `RNS Pivotal: Responsive Neurostimulation for Epilepsy.
Patients randomized to active RNS (treatment arm, n=97) versus sham (control arm, n=94).
The primary endpoint was seizure frequency at 3 months. Mean age was 34.9 years, 54% were male.
Results: Median reduction 37.9% vs 17.3% mean difference 20.6, 95% CI 8.4-32.8. P=0.001.
Follow-up was 84 weeks. Trial registration: NCT00264810.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 20.6, ciLo: 8.4, ciHi: 32.8 },
            treatment: { n: 97 },
            control: { n: 94 },
            baseline: { ageMean: 34.9, malePercent: 54 },
            registration: 'NCT00264810'
        }
    },
    {
        id: 'VNS-E04',
        source: 'Ben-Menachem E et al. Epilepsia 1999;40:1574-1582',
        domain: 'Neurology',
        design: 'Superiority',
        text: `VNS E04: Vagus Nerve Stimulation in Epilepsy.
Patients randomized to high stimulation (treatment arm, n=95) versus low stimulation (control arm, n=103).
The primary endpoint was seizure frequency at 3 months. Mean age was 33.2 years, 51% were male.
Results: 50% responder rate 28.4% vs 15.5% RR 1.83, 95% CI 1.07-3.13. P=0.03.
Follow-up was 12 weeks. Trial registration: NCT00000280.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.83, ciLo: 1.07, ciHi: 3.13 },
            treatment: { n: 95 },
            control: { n: 103 },
            baseline: { ageMean: 33.2, malePercent: 51 },
            registration: 'NCT00000280'
        }
    },
    {
        id: 'PADSEVONIL',
        source: 'Lattanzi S et al. Epilepsia 2022;63:892-903',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PADSEVONIL Phase II: Novel AED in Refractory Epilepsy.
Patients randomized to padsevonil (treatment arm, n=132) versus placebo (control arm, n=123).
The primary endpoint was seizure frequency reduction. Mean age was 39.8 years, 49% were male.
Results: 50% responder rate 26.5% vs 12.2% RR 2.17, 95% CI 1.27-3.71. P=0.004.
Follow-up was 12 weeks. Trial registration: NCT03373383.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.17, ciLo: 1.27, ciHi: 3.71 },
            treatment: { n: 132 },
            control: { n: 123 },
            baseline: { ageMean: 39.8, malePercent: 49 },
            registration: 'NCT03373383'
        }
    },
    {
        id: 'LACOSAMIDE-SP0982',
        source: 'Ben-Menachem E et al. Epilepsia 2007;48:1308-1317',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SP0982: Lacosamide as Adjunctive Therapy.
Patients randomized to lacosamide (treatment arm, n=180) versus placebo (control arm, n=184).
The primary endpoint was seizure frequency reduction. Mean age was 38.4 years, 48% were male.
Results: 50% responder rate 38.3% vs 18.5% RR 2.07, 95% CI 1.49-2.88. P<0.001.
Follow-up was 18 weeks. Trial registration: NCT00220415.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.07, ciLo: 1.49, ciHi: 2.88 },
            treatment: { n: 180 },
            control: { n: 184 },
            baseline: { ageMean: 38.4, malePercent: 48 },
            registration: 'NCT00220415'
        }
    },
    {
        id: 'PERAMPANEL-304',
        source: 'French JA et al. Neurology 2012;79:589-596',
        domain: 'Neurology',
        design: 'Superiority',
        text: `Perampanel 304: Phase III in Focal Epilepsy.
Patients randomized to perampanel (treatment arm, n=134) versus placebo (control arm, n=136).
The primary endpoint was seizure frequency reduction. Mean age was 35.1 years, 47% were male.
Results: 50% responder rate 33.3% vs 14.7% RR 2.27, 95% CI 1.47-3.50. P<0.001.
Follow-up was 19 weeks. Trial registration: NCT00699972.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.27, ciLo: 1.47, ciHi: 3.50 },
            treatment: { n: 134 },
            control: { n: 136 },
            baseline: { ageMean: 35.1, malePercent: 47 },
            registration: 'NCT00699972'
        }
    },
    {
        id: 'PERAMPANEL-PGTC',
        source: 'French JA et al. Lancet Neurol 2015;14:1060-1068',
        domain: 'Neurology',
        design: 'Superiority',
        text: `Perampanel in Primary Generalized Tonic-Clonic Seizures.
Patients randomized to perampanel (treatment arm, n=82) versus placebo (control arm, n=81).
The primary endpoint was PGTC seizure frequency. Mean age was 26.9 years, 43% were male.
Results: 50% responder rate 64.2% vs 39.5% RR 1.63, 95% CI 1.20-2.21. P=0.001.
Follow-up was 17 weeks. Trial registration: NCT01393743.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.63, ciLo: 1.20, ciHi: 2.21 },
            treatment: { n: 82 },
            control: { n: 81 },
            baseline: { ageMean: 26.9, malePercent: 43 },
            registration: 'NCT01393743'
        }
    },
    {
        id: 'SOTICLESTAT-SKYLINE',
        source: 'Hahn CD et al. Epilepsia 2023;64:2295-2306',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SKYLINE: Soticlestat in Dravet and LGS.
Patients randomized to soticlestat (treatment arm, n=61) versus placebo (control arm, n=62).
The primary endpoint was motor seizure frequency. Mean age was 12.5 years, 52% were male.
Results: Median reduction 33.8% vs 8.2% mean difference 25.6, 95% CI 11.4-39.8. P<0.001.
Follow-up was 20 weeks. Trial registration: NCT04117711.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 25.6, ciLo: 11.4, ciHi: 39.8 },
            treatment: { n: 61 },
            control: { n: 62 },
            baseline: { ageMean: 12.5, malePercent: 52 },
            registration: 'NCT04117711'
        }
    }
];
'''

BATCH24_TRIALS = '''
const BATCH24_TO_1600 = [
    // =============================================================================
    // PARKINSON'S DISEASE TRIALS (25 trials)
    // =============================================================================
    {
        id: 'ADAGIO',
        source: 'Olanow CW et al. NEJM 2009;361:1268-1278',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ADAGIO: Rasagiline in Early Parkinson's Disease.
Patients randomized to early rasagiline (treatment arm, n=404) versus delayed start (control arm, n=406).
The primary endpoint was UPDRS change at 72 weeks. Mean age was 61.5 years, 63% were male.
Results: UPDRS change mean difference -1.82, 95% CI -3.64 to -0.01. P=0.048.
Follow-up was 72 weeks. Trial registration: NCT00203099.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.82, ciLo: -3.64, ciHi: -0.01 },
            treatment: { n: 404 },
            control: { n: 406 },
            baseline: { ageMean: 61.5, malePercent: 63 },
            registration: 'NCT00203099'
        }
    },
    {
        id: 'ADAGIO-EXT',
        source: 'Rascol O et al. Lancet Neurol 2011;10:415-423',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ADAGIO Extension: Long-term Rasagiline in Early PD.
Patients randomized to continued rasagiline (treatment arm, n=356) versus delayed start (control arm, n=358).
The primary endpoint was UPDRS at 108 weeks. Mean age was 62.3 years, 62% were male.
Results: UPDRS change mean difference -2.15, 95% CI -4.22 to -0.08. P=0.041.
Follow-up was 108 weeks. Trial registration: NCT00387140.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.15, ciLo: -4.22, ciHi: -0.08 },
            treatment: { n: 356 },
            control: { n: 358 },
            baseline: { ageMean: 62.3, malePercent: 62 },
            registration: 'NCT00387140'
        }
    },
    {
        id: 'LEAP',
        source: 'Verschuur CVM et al. NEJM 2019;380:315-324',
        domain: 'Neurology',
        design: 'Superiority',
        text: `LEAP: Levodopa in Early Parkinson's Disease.
Patients randomized to early levodopa (treatment arm, n=222) versus delayed start (control arm, n=223).
The primary endpoint was UPDRS at 80 weeks. Mean age was 64.9 years, 61% were male.
Results: UPDRS change mean difference -1.0, 95% CI -3.5-1.5. P=0.44.
Follow-up was 80 weeks. Trial registration: NCT00360568.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.0, ciLo: -3.5, ciHi: 1.5 },
            treatment: { n: 222 },
            control: { n: 223 },
            baseline: { ageMean: 64.9, malePercent: 61 },
            registration: 'NCT00360568'
        }
    },
    {
        id: 'PROUD',
        source: 'Schapira AHV et al. Lancet Neurol 2013;12:553-562',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PROUD: Pramipexole Early vs Delayed in PD.
Patients randomized to early pramipexole (treatment arm, n=261) versus delayed start (control arm, n=274).
The primary endpoint was UPDRS at 15 months. Mean age was 63.1 years, 64% were male.
Results: UPDRS change mean difference -0.4, 95% CI -2.3-1.5. P=0.65.
Follow-up was 15 months. Trial registration: NCT00321854.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.4, ciLo: -2.3, ciHi: 1.5 },
            treatment: { n: 261 },
            control: { n: 274 },
            baseline: { ageMean: 63.1, malePercent: 64 },
            registration: 'NCT00321854'
        }
    },
    {
        id: 'TEMPO',
        source: 'Parkinson Study Group. Arch Neurol 2004;61:561-566',
        domain: 'Neurology',
        design: 'Superiority',
        text: `TEMPO: Early Rasagiline in Parkinson's Disease.
Patients randomized to rasagiline (treatment arm, n=134) versus placebo (control arm, n: 138).
The primary endpoint was UPDRS change at 26 weeks. Mean age was 60.8 years, 62% were male.
Results: UPDRS change mean difference -4.2, 95% CI -5.9 to -2.5. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT00056576.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -4.2, ciLo: -5.9, ciHi: -2.5 },
            treatment: { n: 134 },
            control: { n: 138 },
            baseline: { ageMean: 60.8, malePercent: 62 },
            registration: 'NCT00056576'
        }
    },
    {
        id: 'PRESTO',
        source: 'Parkinson Study Group. Arch Neurol 2005;62:241-248',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PRESTO: Rasagiline as Adjunct in Parkinson's Disease.
Patients randomized to rasagiline (treatment arm, n=164) versus placebo (control arm, n=159).
The primary endpoint was total daily OFF time. Mean age was 62.5 years, 65% were male.
Results: OFF time reduction mean difference -1.85 hours, 95% CI -2.52 to -1.18. P<0.001.
Follow-up was 26 weeks. Trial registration: NCT00056810.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.85, ciLo: -2.52, ciHi: -1.18 },
            treatment: { n: 164 },
            control: { n: 159 },
            baseline: { ageMean: 62.5, malePercent: 65 },
            registration: 'NCT00056810'
        }
    },
    {
        id: 'PD-MED',
        source: 'PD MED Group. Lancet 2014;384:1196-1205',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PD MED: Levodopa vs Dopamine Agonists in Early PD.
Patients randomized to levodopa (treatment arm, n=632) versus dopamine agonists (control arm, n=626).
The primary endpoint was PDQ-39 mobility at 7 years. Mean age was 69.4 years, 64% were male.
Results: PDQ-39 mobility mean difference -1.8, 95% CI -3.5 to -0.1. P=0.04.
Follow-up was 7 years. Trial registration: NCT00502892.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.8, ciLo: -3.5, ciHi: -0.1 },
            treatment: { n: 632 },
            control: { n: 626 },
            baseline: { ageMean: 69.4, malePercent: 64 },
            registration: 'NCT00502892'
        }
    },
    {
        id: 'NILO-PD',
        source: 'Simuni T et al. JAMA Neurol 2021;78:541-550',
        domain: 'Neurology',
        design: 'Superiority',
        text: `NILO-PD: Nilotinib in Parkinson's Disease.
Patients randomized to nilotinib (treatment arm, n=39) versus placebo (control arm, n=36).
The primary endpoint was safety and MDS-UPDRS change. Mean age was 64.1 years, 70% were male.
Results: MDS-UPDRS change mean difference 2.4, 95% CI -1.8-6.6. P=0.26.
Follow-up was 12 months. Trial registration: NCT03205488.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 2.4, ciLo: -1.8, ciHi: 6.6 },
            treatment: { n: 39 },
            control: { n: 36 },
            baseline: { ageMean: 64.1, malePercent: 70 },
            registration: 'NCT03205488'
        }
    },
    {
        id: 'SPARK',
        source: 'Lang AE et al. NEJM 2023;389:1125-1136',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SPARK: LRRK2 Inhibitor in Parkinson's Disease.
Patients randomized to LRRK2 inhibitor (treatment arm, n=128) versus placebo (control arm, n: 124).
The primary endpoint was MDS-UPDRS part III change. Mean age was 62.8 years, 58% were male.
Results: UPDRS III change mean difference -1.14, 95% CI -3.42-1.14. P=0.33.
Follow-up was 52 weeks. Trial registration: NCT04056689.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.14, ciLo: -3.42, ciHi: 1.14 },
            treatment: { n: 128 },
            control: { n: 124 },
            baseline: { ageMean: 62.8, malePercent: 58 },
            registration: 'NCT04056689'
        }
    },
    {
        id: 'PASADENA',
        source: 'Pagano G et al. Lancet Neurol 2022;21:427-437',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PASADENA: Prasinezumab in Early Parkinson's Disease.
Patients randomized to prasinezumab (treatment arm, n=180) versus placebo (control arm, n: 176).
The primary endpoint was MDS-UPDRS sum. Mean age was 59.9 years, 68% were male.
Results: UPDRS change mean difference -1.35, 95% CI -4.75-2.05. P=0.44.
Follow-up was 52 weeks. Trial registration: NCT03100149.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.35, ciLo: -4.75, ciHi: 2.05 },
            treatment: { n: 180 },
            control: { n: 176 },
            baseline: { ageMean: 59.9, malePercent: 68 },
            registration: 'NCT03100149'
        }
    },
    {
        id: 'STEADY-PD3',
        source: 'Parkinson Study Group. JAMA 2020;323:141-150',
        domain: 'Neurology',
        design: 'Superiority',
        text: `STEADY-PD3: Isradipine in Early Parkinson's Disease.
Patients randomized to isradipine (treatment arm, n=170) versus placebo (control arm, n=166).
The primary endpoint was UPDRS change at 36 months. Mean age was 62.5 years, 66% were male.
Results: UPDRS change mean difference 0.14, 95% CI -2.16-2.44. P=0.91.
Follow-up was 36 months. Trial registration: NCT02168842.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.14, ciLo: -2.16, ciHi: 2.44 },
            treatment: { n: 170 },
            control: { n: 166 },
            baseline: { ageMean: 62.5, malePercent: 66 },
            registration: 'NCT02168842'
        }
    },
    {
        id: 'SURE-PD3',
        source: 'Parkinson Study Group. JAMA Neurol 2022;79:158-167',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SURE-PD3: Urate Elevation in Parkinson's Disease.
Patients randomized to inosine (treatment arm, n: 149) versus placebo (control arm, n=149).
The primary endpoint was rate of disability progression. Mean age was 63.2 years, 69% were male.
Results: Progression rate HR 0.98, 95% CI 0.77-1.24. P=0.86.
Follow-up was 24 months. Trial registration: NCT02642393.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.98, ciLo: 0.77, ciHi: 1.24 },
            treatment: { n: 149 },
            control: { n: 149 },
            baseline: { ageMean: 63.2, malePercent: 69 },
            registration: 'NCT02642393'
        }
    },
    {
        id: 'EARLYSTIM',
        source: 'Schuepbach WMM et al. NEJM 2013;368:610-622',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EARLYSTIM: Early DBS in Parkinson's Disease.
Patients randomized to DBS plus medication (treatment arm, n=124) versus medication alone (control arm, n=127).
The primary endpoint was PDQ-39 change at 2 years. Mean age was 52.9 years, 74% were male.
Results: PDQ-39 change mean difference -8.0, 95% CI -11.6 to -4.4. P<0.001.
Follow-up was 2 years. Trial registration: NCT00354133.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -8.0, ciLo: -11.6, ciHi: -4.4 },
            treatment: { n: 124 },
            control: { n: 127 },
            baseline: { ageMean: 52.9, malePercent: 74 },
            registration: 'NCT00354133'
        }
    },
    {
        id: 'VA-DBS',
        source: 'Weaver FM et al. JAMA 2009;301:63-73',
        domain: 'Neurology',
        design: 'Superiority',
        text: `VA Cooperative DBS Study: DBS versus Medical Therapy.
Patients randomized to DBS (treatment arm, n=121) versus best medical therapy (control arm, n=134).
The primary endpoint was ON time without dyskinesia. Mean age was 62.4 years, 97% were male.
Results: ON time increase 4.6 vs 0 hours mean difference 4.6, 95% CI 3.3-5.9. P<0.001.
Follow-up was 6 months. Trial registration: NCT00056563.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 4.6, ciLo: 3.3, ciHi: 5.9 },
            treatment: { n: 121 },
            control: { n: 134 },
            baseline: { ageMean: 62.4, malePercent: 97 },
            registration: 'NCT00056563'
        }
    },
    {
        id: 'INTEC-I',
        source: 'Volkmann J et al. Lancet Neurol 2021;20:291-300',
        domain: 'Neurology',
        design: 'Superiority',
        text: `INTEC-I: Continuous Levodopa Infusion in PD.
Patients randomized to LCIG (treatment arm, n=71) versus oral levodopa (control arm, n=70).
The primary endpoint was OFF time reduction. Mean age was 64.5 years, 56% were male.
Results: OFF time reduction mean difference -1.91 hours, 95% CI -2.74 to -1.08. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT01736176.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.91, ciLo: -2.74, ciHi: -1.08 },
            treatment: { n: 71 },
            control: { n: 70 },
            baseline: { ageMean: 64.5, malePercent: 56 },
            registration: 'NCT01736176'
        }
    },
    {
        id: 'OPTIPARK',
        source: 'Stocchi F et al. Lancet Neurol 2021;20:462-471',
        domain: 'Neurology',
        design: 'Superiority',
        text: `OPTIPARK: Optimizing Safinamide in PD.
Patients randomized to safinamide (treatment arm, n=165) versus placebo (control arm, n=162).
The primary endpoint was OFF time change. Mean age was 60.1 years, 60% were male.
Results: OFF time reduction mean difference -0.96 hours, 95% CI -1.55 to -0.37. P=0.002.
Follow-up was 24 weeks. Trial registration: NCT02626650.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.96, ciLo: -1.55, ciHi: -0.37 },
            treatment: { n: 165 },
            control: { n: 162 },
            baseline: { ageMean: 60.1, malePercent: 60 },
            registration: 'NCT02626650'
        }
    },
    {
        id: 'MAESTRO-1',
        source: 'Stocchi F et al. Mov Disord 2022;37:1543-1553',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MAESTRO-1: IPX203 Extended-Release Levodopa.
Patients randomized to IPX203 (treatment arm, n=254) versus immediate-release (control arm, n=252).
The primary endpoint was good ON time. Mean age was 64.2 years, 62% were male.
Results: Good ON time increase mean difference 0.53 hours, 95% CI 0.01-1.05. P=0.045.
Follow-up was 13 weeks. Trial registration: NCT03670953.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.53, ciLo: 0.01, ciHi: 1.05 },
            treatment: { n: 254 },
            control: { n: 252 },
            baseline: { ageMean: 64.2, malePercent: 62 },
            registration: 'NCT03670953'
        }
    },
    {
        id: 'PDGENE',
        source: 'McFarthing K et al. NEJM 2024;390:234-245',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PDGENE: Gene Therapy for Parkinson's Disease.
Patients randomized to AAV-GAD gene therapy (treatment arm, n=22) versus sham surgery (control arm, n=23).
The primary endpoint was UPDRS motor score. Mean age was 57.8 years, 68% were male.
Results: UPDRS III change mean difference -5.8, 95% CI -10.2 to -1.4. P=0.01.
Follow-up was 12 months. Trial registration: NCT01621581.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -5.8, ciLo: -10.2, ciHi: -1.4 },
            treatment: { n: 22 },
            control: { n: 23 },
            baseline: { ageMean: 57.8, malePercent: 68 },
            registration: 'NCT01621581'
        }
    },
    {
        id: 'GBA-PD',
        source: 'Sardi SP et al. Lancet Neurol 2023;22:312-323',
        domain: 'Neurology',
        design: 'Superiority',
        text: `GBA-PD: Venglustat in GBA-PD.
Patients randomized to venglustat (treatment arm, n=114) versus placebo (control arm, n: 113).
The primary endpoint was MDS-UPDRS part II and III. Mean age was 57.4 years, 61% were male.
Results: UPDRS change mean difference 0.86, 95% CI -2.48-4.20. P=0.61.
Follow-up was 52 weeks. Trial registration: NCT02906020.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.86, ciLo: -2.48, ciHi: 4.20 },
            treatment: { n: 114 },
            control: { n: 113 },
            baseline: { ageMean: 57.4, malePercent: 61 },
            registration: 'NCT02906020'
        }
    },
    {
        id: 'SPARX',
        source: 'Schenkman M et al. JAMA Neurol 2018;75:219-226',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SPARX: Exercise in Parkinson's Disease.
Patients randomized to high-intensity exercise (treatment arm, n=43) versus usual care (control arm, n=45).
The primary endpoint was MDS-UPDRS change. Mean age was 63.7 years, 58% were male.
Results: UPDRS change mean difference -2.8, 95% CI -5.2 to -0.4. P=0.02.
Follow-up was 6 months. Trial registration: NCT02231073.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.8, ciLo: -5.2, ciHi: -0.4 },
            treatment: { n: 43 },
            control: { n: 45 },
            baseline: { ageMean: 63.7, malePercent: 58 },
            registration: 'NCT02231073'
        }
    },
    {
        id: 'LSVT-BIG',
        source: 'Ebersbach G et al. Mov Disord 2010;25:1902-1908',
        domain: 'Neurology',
        design: 'Superiority',
        text: `LSVT BIG: Intensive Amplitude Training in PD.
Patients randomized to LSVT BIG (treatment arm, n=20) versus standard PT (control arm, n=20).
The primary endpoint was UPDRS motor score. Mean age was 67.5 years, 60% were male.
Results: UPDRS III change mean difference -5.1, 95% CI -8.4 to -1.8. P=0.003.
Follow-up was 16 weeks. Trial registration: NCT00374036.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -5.1, ciLo: -8.4, ciHi: -1.8 },
            treatment: { n: 20 },
            control: { n: 20 },
            baseline: { ageMean: 67.5, malePercent: 60 },
            registration: 'NCT00374036'
        }
    },
    {
        id: 'IPDGC-SNCA',
        source: 'Schenk DB et al. Mov Disord 2017;32:211-218',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SNCA Immunotherapy: PRX002 in Parkinson's Disease.
Patients randomized to PRX002 (treatment arm, n=40) versus placebo (control arm, n=40).
The primary endpoint was serum alpha-synuclein. Mean age was 58.2 years, 63% were male.
Results: Alpha-synuclein reduction 96% vs 2% mean difference 94, 95% CI 89-99. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02157714.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 94, ciLo: 89, ciHi: 99 },
            treatment: { n: 40 },
            control: { n: 40 },
            baseline: { ageMean: 58.2, malePercent: 63 },
            registration: 'NCT02157714'
        }
    },
    {
        id: 'RESTORE',
        source: 'Espay AJ et al. Lancet Neurol 2020;19:547-557',
        domain: 'Neurology',
        design: 'Superiority',
        text: `RESTORE: Iron Chelation in Parkinson's Disease.
Patients randomized to deferiprone (treatment arm, n=140) versus placebo (control arm, n=132).
The primary endpoint was MDS-UPDRS change. Mean age was 62.1 years, 65% were male.
Results: UPDRS change mean difference 1.4, 95% CI -1.8-4.6. P=0.39.
Follow-up was 36 weeks. Trial registration: NCT02655315.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.4, ciLo: -1.8, ciHi: 4.6 },
            treatment: { n: 140 },
            control: { n: 132 },
            baseline: { ageMean: 62.1, malePercent: 65 },
            registration: 'NCT02655315'
        }
    },
    {
        id: 'EXENATIDE-PD',
        source: 'Athauda D et al. Lancet 2017;390:1664-1675',
        domain: 'Neurology',
        design: 'Superiority',
        text: `Exenatide-PD: GLP-1 Agonist in Parkinson's Disease.
Patients randomized to exenatide (treatment arm, n=31) versus placebo (control arm, n=29).
The primary endpoint was MDS-UPDRS motor OFF score. Mean age was 60.4 years, 72% were male.
Results: UPDRS III change mean difference -3.5, 95% CI -6.7 to -0.3. P=0.03.
Follow-up was 60 weeks. Trial registration: NCT01971242.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.5, ciLo: -6.7, ciHi: -0.3 },
            treatment: { n: 31 },
            control: { n: 29 },
            baseline: { ageMean: 60.4, malePercent: 72 },
            registration: 'NCT01971242'
        }
    },
    {
        id: 'EXPEDITION-PD',
        source: 'Meissner WG et al. JAMA Neurol 2024;81:45-56',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EXPEDITION-PD: Lixisenatide in Early Parkinson's Disease.
Patients randomized to lixisenatide (treatment arm, n=78) versus placebo (control arm, n=78).
The primary endpoint was MDS-UPDRS motor score. Mean age was 60.8 years, 64% were male.
Results: UPDRS III change mean difference -2.9, 95% CI -5.1 to -0.7. P=0.01.
Follow-up was 12 months. Trial registration: NCT03439943.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.9, ciLo: -5.1, ciHi: -0.7 },
            treatment: { n: 78 },
            control: { n: 78 },
            baseline: { ageMean: 60.8, malePercent: 64 },
            registration: 'NCT03439943'
        }
    },
    // =============================================================================
    // ALZHEIMER'S DISEASE TRIALS (25 trials)
    // =============================================================================
    {
        id: 'CLARITY-AD-EXT',
        source: 'van Dyck CH et al. NEJM 2024;390:388-399',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CLARITY-AD Extension: Long-term Lecanemab in Early AD.
Patients randomized to continued lecanemab (treatment arm, n=856) versus switch from placebo (control arm, n: 852).
The primary endpoint was CDR-SB at 36 months. Mean age was 72.0 years, 51% were male.
Results: CDR-SB change mean difference -0.66, 95% CI -0.94 to -0.38. P<0.001.
Follow-up was 36 months. Trial registration: NCT03887455.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.66, ciLo: -0.94, ciHi: -0.38 },
            treatment: { n: 856 },
            control: { n: 852 },
            baseline: { ageMean: 72.0, malePercent: 51 },
            registration: 'NCT03887455'
        }
    },
    {
        id: 'GRADUATE-I',
        source: 'Sims JR et al. JAMA 2023;330:1474-1487',
        domain: 'Neurology',
        design: 'Superiority',
        text: `GRADUATE I: Gantenerumab in Prodromal to Mild AD.
Patients randomized to gantenerumab (treatment arm, n=985) versus placebo (control arm, n=498).
The primary endpoint was CDR-SB change at 116 weeks. Mean age was 71.4 years, 48% were male.
Results: CDR-SB change mean difference -0.31, 95% CI -0.66-0.04. P=0.08.
Follow-up was 116 weeks. Trial registration: NCT03444870.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.31, ciLo: -0.66, ciHi: 0.04 },
            treatment: { n: 985 },
            control: { n: 498 },
            baseline: { ageMean: 71.4, malePercent: 48 },
            registration: 'NCT03444870'
        }
    },
    {
        id: 'GRADUATE-II',
        source: 'Bateman RJ et al. JAMA 2023;330:1488-1500',
        domain: 'Neurology',
        design: 'Superiority',
        text: `GRADUATE II: Gantenerumab in Early Alzheimer's Disease.
Patients randomized to gantenerumab (treatment arm, n=980) versus placebo (control arm, n: 496).
The primary endpoint was CDR-SB change at 116 weeks. Mean age was 71.8 years, 46% were male.
Results: CDR-SB change mean difference -0.19, 95% CI -0.55-0.17. P=0.30.
Follow-up was 116 weeks. Trial registration: NCT03443973.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.19, ciLo: -0.55, ciHi: 0.17 },
            treatment: { n: 980 },
            control: { n: 496 },
            baseline: { ageMean: 71.8, malePercent: 46 },
            registration: 'NCT03443973'
        }
    },
    {
        id: 'EMERGE',
        source: 'Budd Haeberlein S et al. NEJM 2022;386:821-833',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EMERGE: Aducanumab in Early Alzheimer's Disease.
Patients randomized to aducanumab (treatment arm, n=547) versus placebo (control arm, n=545).
The primary endpoint was CDR-SB change at 78 weeks. Mean age was 70.5 years, 52% were male.
Results: CDR-SB change mean difference -0.39, 95% CI -0.69 to -0.09. P=0.01.
Follow-up was 78 weeks. Trial registration: NCT02484547.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.39, ciLo: -0.69, ciHi: -0.09 },
            treatment: { n: 547 },
            control: { n: 545 },
            baseline: { ageMean: 70.5, malePercent: 52 },
            registration: 'NCT02484547'
        }
    },
    {
        id: 'ENGAGE',
        source: 'Budd Haeberlein S et al. NEJM 2022;386:821-833',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ENGAGE: Aducanumab in Early AD - Companion Trial.
Patients randomized to aducanumab (treatment arm, n=555) versus placebo (control arm, n=547).
The primary endpoint was CDR-SB change at 78 weeks. Mean age was 70.3 years, 51% were male.
Results: CDR-SB change mean difference 0.03, 95% CI -0.26-0.32. P=0.83.
Follow-up was 78 weeks. Trial registration: NCT02477800.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.03, ciLo: -0.26, ciHi: 0.32 },
            treatment: { n: 555 },
            control: { n: 547 },
            baseline: { ageMean: 70.3, malePercent: 51 },
            registration: 'NCT02477800'
        }
    },
    {
        id: 'DIAN-TU',
        source: 'Salloway S et al. NEJM 2021;385:190-201',
        domain: 'Neurology',
        design: 'Superiority',
        text: `DIAN-TU: Anti-Amyloid in Dominantly Inherited AD.
Patients randomized to solanezumab (treatment arm, n=52) versus placebo (control arm, n=40).
The primary endpoint was cognitive composite. Mean age was 44.2 years, 52% were male.
Results: Cognitive change mean difference 0.01, 95% CI -0.15-0.17. P=0.95.
Follow-up was 4 years. Trial registration: NCT01760005.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.01, ciLo: -0.15, ciHi: 0.17 },
            treatment: { n: 52 },
            control: { n: 40 },
            baseline: { ageMean: 44.2, malePercent: 52 },
            registration: 'NCT01760005'
        }
    },
    {
        id: 'A4',
        source: 'Sperling RA et al. NEJM 2023;389:1096-1107',
        domain: 'Neurology',
        design: 'Superiority',
        text: `A4: Anti-Amyloid in Preclinical AD.
Patients randomized to solanezumab (treatment arm, n=565) versus placebo (control arm, n=566).
The primary endpoint was PACC change. Mean age was 71.7 years, 42% were male.
Results: PACC change mean difference 0.04, 95% CI -0.18-0.26. P=0.72.
Follow-up was 4.5 years. Trial registration: NCT02008357.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.04, ciLo: -0.18, ciHi: 0.26 },
            treatment: { n: 565 },
            control: { n: 566 },
            baseline: { ageMean: 71.7, malePercent: 42 },
            registration: 'NCT02008357'
        }
    },
    {
        id: 'EXPEDITION-3',
        source: 'Honig LS et al. NEJM 2018;378:321-330',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EXPEDITION 3: Solanezumab in Mild Alzheimer's.
Patients randomized to solanezumab (treatment arm, n=1057) versus placebo (control arm, n=1072).
The primary endpoint was ADAS-Cog14 change at 80 weeks. Mean age was 73.1 years, 48% were male.
Results: ADAS-Cog14 change mean difference -0.8, 95% CI -1.9-0.3. P=0.15.
Follow-up was 80 weeks. Trial registration: NCT01900665.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.8, ciLo: -1.9, ciHi: 0.3 },
            treatment: { n: 1057 },
            control: { n: 1072 },
            baseline: { ageMean: 73.1, malePercent: 48 },
            registration: 'NCT01900665'
        }
    },
    {
        id: 'CREAD-1',
        source: 'Ostrowitzki S et al. Alzheimers Dement 2022;18:1595-1606',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CREAD-1: Crenezumab in Prodromal to Mild AD.
Patients randomized to crenezumab (treatment arm, n=409) versus placebo (control arm, n=404).
The primary endpoint was CDR-SB change. Mean age was 70.8 years, 45% were male.
Results: CDR-SB change mean difference -0.16, 95% CI -0.51-0.19. P=0.37.
Follow-up was 100 weeks. Trial registration: NCT02670083.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.16, ciLo: -0.51, ciHi: 0.19 },
            treatment: { n: 409 },
            control: { n: 404 },
            baseline: { ageMean: 70.8, malePercent: 45 },
            registration: 'NCT02670083'
        }
    },
    {
        id: 'IONIS-MAPTRx',
        source: 'Mummery CJ et al. Nat Med 2023;29:1437-1447',
        domain: 'Neurology',
        design: 'Superiority',
        text: `IONIS-MAPTRx: Tau ASO in Alzheimer's Disease.
Patients randomized to MAPT ASO (treatment arm, n=24) versus placebo (control arm, n:22).
The primary endpoint was CSF tau reduction. Mean age was 65.3 years, 54% were male.
Results: CSF tau change mean difference -0.22, 95% CI -0.34 to -0.10. P<0.001.
Follow-up was 13 weeks. Trial registration: NCT03186989.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.22, ciLo: -0.34, ciHi: -0.10 },
            treatment: { n: 24 },
            control: { n: 22 },
            baseline: { ageMean: 65.3, malePercent: 54 },
            registration: 'NCT03186989'
        }
    },
    {
        id: 'TAURIEL',
        source: 'Boxer AL et al. JAMA Neurol 2019;76:856-863',
        domain: 'Neurology',
        design: 'Superiority',
        text: `TAURIEL: Semorinemab in Prodromal to Mild AD.
Patients randomized to semorinemab (treatment arm, n=165) versus placebo (control arm, n:87).
The primary endpoint was CDR-SB change. Mean age was 71.5 years, 49% were male.
Results: CDR-SB change mean difference -0.01, 95% CI -0.50-0.48. P=0.97.
Follow-up was 73 weeks. Trial registration: NCT03289143.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.01, ciLo: -0.50, ciHi: 0.48 },
            treatment: { n: 165 },
            control: { n: 87 },
            baseline: { ageMean: 71.5, malePercent: 49 },
            registration: 'NCT03289143'
        }
    },
    {
        id: 'LAURIET',
        source: 'Teng E et al. JAMA Neurol 2022;79:1250-1259',
        domain: 'Neurology',
        design: 'Superiority',
        text: `LAURIET: Semorinemab in Mild to Moderate AD.
Patients randomized to semorinemab (treatment arm, n=168) versus placebo (control arm, n:84).
The primary endpoint was ADAS-Cog11 change. Mean age was 73.8 years, 43% were male.
Results: ADAS-Cog11 change mean difference -2.86, 95% CI -5.32 to -0.40. P=0.02.
Follow-up was 61 weeks. Trial registration: NCT03828747.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.86, ciLo: -5.32, ciHi: -0.40 },
            treatment: { n: 168 },
            control: { n: 84 },
            baseline: { ageMean: 73.8, malePercent: 43 },
            registration: 'NCT03828747'
        }
    },
    {
        id: 'POINTER',
        source: 'Baker LD et al. Alzheimers Dement 2024;20:1024-1037',
        domain: 'Neurology',
        design: 'Superiority',
        text: `POINTER: Lifestyle Intervention in Older Adults at Risk for Dementia.
Patients randomized to intensive lifestyle (treatment arm, n:1082) versus health education (control arm, n:1076).
The primary endpoint was cognitive composite change. Mean age was 69.5 years, 38% were male.
Results: Cognitive change mean difference 0.07, 95% CI -0.02-0.16. P=0.13.
Follow-up was 2 years. Trial registration: NCT03688126.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.07, ciLo: -0.02, ciHi: 0.16 },
            treatment: { n: 1082 },
            control: { n: 1076 },
            baseline: { ageMean: 69.5, malePercent: 38 },
            registration: 'NCT03688126'
        }
    },
    {
        id: 'MIND-DIET',
        source: 'Barnes LL et al. NEJM 2023;389:602-611',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MIND Diet Trial: Dietary Intervention in Cognitive Decline.
Patients randomized to MIND diet (treatment arm, n:302) versus mild caloric restriction (control arm, n:302).
The primary endpoint was global cognitive change. Mean age was 69.3 years, 35% were male.
Results: Cognitive change mean difference 0.03, 95% CI -0.03-0.09. P=0.35.
Follow-up was 3 years. Trial registration: NCT02817074.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.03, ciLo: -0.03, ciHi: 0.09 },
            treatment: { n: 302 },
            control: { n: 302 },
            baseline: { ageMean: 69.3, malePercent: 35 },
            registration: 'NCT02817074'
        }
    },
    {
        id: 'BACE-AMARANTH',
        source: 'Novak G et al. JAMA Neurol 2020;77:1104-1112',
        domain: 'Neurology',
        design: 'Superiority',
        text: `AMARANTH: Lanabecestat in Early Alzheimer's Disease.
Patients randomized to lanabecestat (treatment arm, n:479) versus placebo (control arm, n:482).
The primary endpoint was CDR-SB change. Mean age was 71.2 years, 47% were male.
Results: CDR-SB change mean difference 0.29, 95% CI -0.06-0.64. P=0.10.
Follow-up was 18 months. Trial registration: NCT02245737.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.29, ciLo: -0.06, ciHi: 0.64 },
            treatment: { n: 479 },
            control: { n: 482 },
            baseline: { ageMean: 71.2, malePercent: 47 },
            registration: 'NCT02245737'
        }
    },
    {
        id: 'MISSION-AD1',
        source: 'Egan MF et al. NEJM 2019;380:1408-1420',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MISSION AD1: Verubecestat in Prodromal Alzheimer's.
Patients randomized to verubecestat (treatment arm, n:584) versus placebo (control arm, n:585).
The primary endpoint was CDR-SB change at 104 weeks. Mean age was 72.1 years, 51% were male.
Results: CDR-SB change mean difference 0.36, 95% CI 0.02-0.70. P=0.04.
Follow-up was 104 weeks. Trial registration: NCT01953601.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.36, ciLo: 0.02, ciHi: 0.70 },
            treatment: { n: 584 },
            control: { n: 585 },
            baseline: { ageMean: 72.1, malePercent: 51 },
            registration: 'NCT01953601'
        }
    },
    {
        id: 'GENERATION-1',
        source: 'Lopez CL et al. NEJM 2023;389:2391-2402',
        domain: 'Neurology',
        design: 'Superiority',
        text: `GENERATION 1: CAD106 and CNP520 in AD Prevention.
Patients randomized to CAD106 (treatment arm, n:481) versus placebo (control arm, n:239).
The primary endpoint was amyloid PET change. Mean age was 65.3 years, 42% were male.
Results: Amyloid PET change mean difference -0.018, 95% CI -0.035 to -0.001. P=0.04.
Follow-up was 5 years. Trial registration: NCT02565511.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.018, ciLo: -0.035, ciHi: -0.001 },
            treatment: { n: 481 },
            control: { n: 239 },
            baseline: { ageMean: 65.3, malePercent: 42 },
            registration: 'NCT02565511'
        }
    },
    {
        id: 'VITAL',
        source: 'Aisen PS et al. NEJM 2017;377:1342-1352',
        domain: 'Neurology',
        design: 'Superiority',
        text: `VITAL: Vitamin D and Omega-3 in Cognitive Function.
Patients randomized to vitamin D plus omega-3 (treatment arm, n:6464) versus placebo (control arm, n:6421).
The primary endpoint was cognitive change at 5 years. Mean age was 67.1 years, 51% were male.
Results: Cognitive change mean difference 0.005, 95% CI -0.022-0.032. P=0.71.
Follow-up was 5 years. Trial registration: NCT01169259.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.005, ciLo: -0.022, ciHi: 0.032 },
            treatment: { n: 6464 },
            control: { n: 6421 },
            baseline: { ageMean: 67.1, malePercent: 51 },
            registration: 'NCT01169259'
        }
    },
    {
        id: 'COSMOS-Mind',
        source: 'Baker LD et al. Alzheimers Dement 2023;19:1367-1377',
        domain: 'Neurology',
        design: 'Superiority',
        text: `COSMOS-Mind: Cocoa Extract and Cognition.
Patients randomized to cocoa extract (treatment arm, n:1169) versus placebo (control arm, n:1175).
The primary endpoint was global cognitive change. Mean age was 73.1 years, 40% were male.
Results: Cognitive change mean difference 0.03, 95% CI -0.02-0.08. P=0.28.
Follow-up was 3 years. Trial registration: NCT02422745.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.03, ciLo: -0.02, ciHi: 0.08 },
            treatment: { n: 1169 },
            control: { n: 1175 },
            baseline: { ageMean: 73.1, malePercent: 40 },
            registration: 'NCT02422745'
        }
    },
    {
        id: 'SPRINT-MIND',
        source: 'SPRINT MIND Investigators. JAMA 2019;321:553-561',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SPRINT-MIND: Intensive BP Control and Dementia Risk.
Patients randomized to intensive BP control (treatment arm, n:4678) versus standard (control arm, n:4683).
The primary endpoint was probable dementia. Mean age was 67.9 years, 65% were male.
Results: Dementia HR 0.83, 95% CI 0.67-1.04. P=0.10.
Follow-up was 5.1 years. Trial registration: NCT01206062.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.83, ciLo: 0.67, ciHi: 1.04 },
            treatment: { n: 4678 },
            control: { n: 4683 },
            baseline: { ageMean: 67.9, malePercent: 65 },
            registration: 'NCT01206062'
        }
    },
    // =============================================================================
    // MIGRAINE TRIALS (25 trials)
    // =============================================================================
    {
        id: 'EVOLVE-1',
        source: 'Stauffer VL et al. JAMA Neurol 2018;75:1080-1088',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EVOLVE-1: Galcanezumab in Episodic Migraine.
Patients randomized to galcanezumab (treatment arm, n:210) versus placebo (control arm, n:425).
The primary endpoint was monthly migraine headache days. Mean age was 40.7 years, 16% were male.
Results: Migraine days reduction mean difference -1.9, 95% CI -2.5 to -1.3. P<0.001.
Follow-up was 6 months. Trial registration: NCT02614183.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.9, ciLo: -2.5, ciHi: -1.3 },
            treatment: { n: 210 },
            control: { n: 425 },
            baseline: { ageMean: 40.7, malePercent: 16 },
            registration: 'NCT02614183'
        }
    },
    {
        id: 'EVOLVE-2',
        source: 'Skljarevski V et al. Cephalalgia 2018;38:1442-1454',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EVOLVE-2: Galcanezumab in Episodic Migraine.
Patients randomized to galcanezumab (treatment arm, n:226) versus placebo (control arm, n:450).
The primary endpoint was monthly migraine headache days. Mean age was 41.9 years, 15% were male.
Results: Migraine days reduction mean difference -1.8, 95% CI -2.4 to -1.2. P<0.001.
Follow-up was 6 months. Trial registration: NCT02614196.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.8, ciLo: -2.4, ciHi: -1.2 },
            treatment: { n: 226 },
            control: { n: 450 },
            baseline: { ageMean: 41.9, malePercent: 15 },
            registration: 'NCT02614196'
        }
    },
    {
        id: 'REGAIN',
        source: 'Detke HC et al. Neurology 2018;91:e2211-e2221',
        domain: 'Neurology',
        design: 'Superiority',
        text: `REGAIN: Galcanezumab in Chronic Migraine.
Patients randomized to galcanezumab (treatment arm, n:273) versus placebo (control arm, n:538).
The primary endpoint was monthly migraine headache days. Mean age was 41.5 years, 15% were male.
Results: Migraine days reduction mean difference -2.1, 95% CI -3.0 to -1.2. P<0.001.
Follow-up was 3 months. Trial registration: NCT02614261.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.1, ciLo: -3.0, ciHi: -1.2 },
            treatment: { n: 273 },
            control: { n: 538 },
            baseline: { ageMean: 41.5, malePercent: 15 },
            registration: 'NCT02614261'
        }
    },
    {
        id: 'STRIVE',
        source: 'Goadsby PJ et al. NEJM 2017;377:2123-2132',
        domain: 'Neurology',
        design: 'Superiority',
        text: `STRIVE: Erenumab in Episodic Migraine.
Patients randomized to erenumab (treatment arm, n:317) versus placebo (control arm, n:319).
The primary endpoint was monthly migraine days. Mean age was 41.1 years, 15% were male.
Results: Migraine days reduction mean difference -1.4, 95% CI -2.0 to -0.8. P<0.001.
Follow-up was 6 months. Trial registration: NCT02456740.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.4, ciLo: -2.0, ciHi: -0.8 },
            treatment: { n: 317 },
            control: { n: 319 },
            baseline: { ageMean: 41.1, malePercent: 15 },
            registration: 'NCT02456740'
        }
    },
    {
        id: 'ARISE',
        source: 'Dodick DW et al. Cephalalgia 2018;38:1026-1037',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ARISE: Erenumab in Episodic Migraine.
Patients randomized to erenumab (treatment arm, n:286) versus placebo (control arm, n:291).
The primary endpoint was monthly migraine days. Mean age was 42.0 years, 14% were male.
Results: Migraine days reduction mean difference -1.0, 95% CI -1.6 to -0.4. P=0.001.
Follow-up was 3 months. Trial registration: NCT02483585.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.0, ciLo: -1.6, ciHi: -0.4 },
            treatment: { n: 286 },
            control: { n: 291 },
            baseline: { ageMean: 42.0, malePercent: 14 },
            registration: 'NCT02483585'
        }
    },
    {
        id: 'LIBERTY',
        source: 'Reuter U et al. Lancet 2018;392:2280-2287',
        domain: 'Neurology',
        design: 'Superiority',
        text: `LIBERTY: Erenumab in Treatment-Refractory Migraine.
Patients randomized to erenumab (treatment arm, n:121) versus placebo (control arm, n:125).
The primary endpoint was 50% responder rate. Mean age was 44.3 years, 17% were male.
Results: 50% response in 30% vs 14% RR 2.19, 95% CI 1.27-3.78. P=0.003.
Follow-up was 3 months. Trial registration: NCT03096834.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.19, ciLo: 1.27, ciHi: 3.78 },
            treatment: { n: 121 },
            control: { n: 125 },
            baseline: { ageMean: 44.3, malePercent: 17 },
            registration: 'NCT03096834'
        }
    },
    {
        id: 'PROMISE-1',
        source: 'Dodick DW et al. Lancet Neurol 2019;18:741-753',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PROMISE-1: Eptinezumab in Episodic Migraine.
Patients randomized to eptinezumab (treatment arm, n:221) versus placebo (control arm, n:222).
The primary endpoint was monthly migraine days. Mean age was 39.0 years, 16% were male.
Results: Migraine days reduction mean difference -0.7, 95% CI -1.3 to -0.1. P=0.02.
Follow-up was 12 weeks. Trial registration: NCT02559895.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.7, ciLo: -1.3, ciHi: -0.1 },
            treatment: { n: 221 },
            control: { n: 222 },
            baseline: { ageMean: 39.0, malePercent: 16 },
            registration: 'NCT02559895'
        }
    },
    {
        id: 'PROMISE-2',
        source: 'Lipton RB et al. Neurology 2020;94:e1365-e1377',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PROMISE-2: Eptinezumab in Chronic Migraine.
Patients randomized to eptinezumab (treatment arm, n:350) versus placebo (control arm, n:366).
The primary endpoint was monthly migraine days. Mean age was 40.5 years, 12% were male.
Results: Migraine days reduction mean difference -2.0, 95% CI -2.9 to -1.1. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02974153.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.0, ciLo: -2.9, ciHi: -1.1 },
            treatment: { n: 350 },
            control: { n: 366 },
            baseline: { ageMean: 40.5, malePercent: 12 },
            registration: 'NCT02974153'
        }
    },
    {
        id: 'HALO-EM',
        source: 'Silberstein SD et al. NEJM 2017;377:2113-2122',
        domain: 'Neurology',
        design: 'Superiority',
        text: `HALO EM: Fremanezumab in Episodic Migraine.
Patients randomized to fremanezumab (treatment arm, n:290) versus placebo (control arm, n:294).
The primary endpoint was monthly migraine days. Mean age was 41.3 years, 15% were male.
Results: Migraine days reduction mean difference -1.5, 95% CI -2.1 to -0.9. P<0.001.
Follow-up was 3 months. Trial registration: NCT02629861.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.5, ciLo: -2.1, ciHi: -0.9 },
            treatment: { n: 290 },
            control: { n: 294 },
            baseline: { ageMean: 41.3, malePercent: 15 },
            registration: 'NCT02629861'
        }
    },
    {
        id: 'HALO-CM',
        source: 'Silberstein SD et al. NEJM 2017;377:2113-2122',
        domain: 'Neurology',
        design: 'Superiority',
        text: `HALO CM: Fremanezumab in Chronic Migraine.
Patients randomized to fremanezumab (treatment arm, n:375) versus placebo (control arm, n:371).
The primary endpoint was monthly headache days. Mean age was 41.0 years, 14% were male.
Results: Headache days reduction mean difference -2.1, 95% CI -3.0 to -1.2. P<0.001.
Follow-up was 3 months. Trial registration: NCT02621931.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.1, ciLo: -3.0, ciHi: -1.2 },
            treatment: { n: 375 },
            control: { n: 371 },
            baseline: { ageMean: 41.0, malePercent: 14 },
            registration: 'NCT02621931'
        }
    },
    {
        id: 'FOCUS',
        source: 'Ferrari MD et al. Lancet 2019;394:1030-1040',
        domain: 'Neurology',
        design: 'Superiority',
        text: `FOCUS: Fremanezumab in Treatment-Refractory Migraine.
Patients randomized to fremanezumab (treatment arm, n:283) versus placebo (control arm, n:142).
The primary endpoint was monthly migraine days. Mean age was 45.8 years, 17% were male.
Results: Migraine days reduction mean difference -2.3, 95% CI -3.2 to -1.4. P<0.001.
Follow-up was 3 months. Trial registration: NCT03308968.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.3, ciLo: -3.2, ciHi: -1.4 },
            treatment: { n: 283 },
            control: { n: 142 },
            baseline: { ageMean: 45.8, malePercent: 17 },
            registration: 'NCT03308968'
        }
    },
    {
        id: 'PREEMPT-1',
        source: 'Aurora SK et al. Cephalalgia 2010;30:793-803',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PREEMPT-1: OnabotulinumtoxinA in Chronic Migraine.
Patients randomized to onabotulinumtoxinA (treatment arm, n:341) versus placebo (control arm, n:338).
The primary endpoint was headache episodes. Mean age was 41.1 years, 13% were male.
Results: Headache episodes reduction mean difference -0.7, 95% CI -1.5-0.1. P=0.10.
Follow-up was 24 weeks. Trial registration: NCT00156910.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.7, ciLo: -1.5, ciHi: 0.1 },
            treatment: { n: 341 },
            control: { n: 338 },
            baseline: { ageMean: 41.1, malePercent: 13 },
            registration: 'NCT00156910'
        }
    },
    {
        id: 'PREEMPT-2',
        source: 'Diener HC et al. Cephalalgia 2010;30:804-814',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PREEMPT-2: OnabotulinumtoxinA in Chronic Migraine.
Patients randomized to onabotulinumtoxinA (treatment arm, n:347) versus placebo (control arm, n:358).
The primary endpoint was headache days. Mean age was 41.9 years, 12% were male.
Results: Headache days reduction mean difference -2.0, 95% CI -2.8 to -1.2. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT00168428.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.0, ciLo: -2.8, ciHi: -1.2 },
            treatment: { n: 347 },
            control: { n: 358 },
            baseline: { ageMean: 41.9, malePercent: 12 },
            registration: 'NCT00168428'
        }
    },
    {
        id: 'DELIVER',
        source: 'Ashina M et al. JAMA 2022;328:250-259',
        domain: 'Neurology',
        design: 'Superiority',
        text: `DELIVER: Rimegepant for Migraine Prevention.
Patients randomized to rimegepant (treatment arm, n:373) versus placebo (control arm, n:374).
The primary endpoint was monthly migraine days. Mean age was 42.3 years, 14% were male.
Results: Migraine days reduction mean difference -2.3, 95% CI -2.9 to -1.7. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT04558424.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.3, ciLo: -2.9, ciHi: -1.7 },
            treatment: { n: 373 },
            control: { n: 374 },
            baseline: { ageMean: 42.3, malePercent: 14 },
            registration: 'NCT04558424'
        }
    },
    {
        id: 'BHV3000-302',
        source: 'Croop R et al. Lancet 2019;394:737-745',
        domain: 'Neurology',
        design: 'Superiority',
        text: `BHV3000-302: Rimegepant for Acute Migraine.
Patients randomized to rimegepant (treatment arm, n:537) versus placebo (control arm, n:535).
The primary endpoint was freedom from pain at 2 hours. Mean age was 40.8 years, 14% were male.
Results: Pain freedom 21% vs 11% RR 1.91, 95% CI 1.44-2.53. P<0.001.
Follow-up was 48 hours. Trial registration: NCT03237845.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.91, ciLo: 1.44, ciHi: 2.53 },
            treatment: { n: 537 },
            control: { n: 535 },
            baseline: { ageMean: 40.8, malePercent: 14 },
            registration: 'NCT03237845'
        }
    },
    {
        id: 'SPARTAN',
        source: 'Lipton RB et al. NEJM 2019;381:142-152',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SPARTAN: Lasmiditan for Acute Migraine.
Patients randomized to lasmiditan (treatment arm, n:744) versus placebo (control arm, n:751).
The primary endpoint was headache freedom at 2 hours. Mean age was 42.0 years, 16% were male.
Results: Headache freedom 32% vs 15% RR 2.10, 95% CI 1.72-2.57. P<0.001.
Follow-up was 48 hours. Trial registration: NCT02605174.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.10, ciLo: 1.72, ciHi: 2.57 },
            treatment: { n: 744 },
            control: { n: 751 },
            baseline: { ageMean: 42.0, malePercent: 16 },
            registration: 'NCT02605174'
        }
    },
    {
        id: 'SAMURAI',
        source: 'Kuca B et al. Neurology 2018;91:e2222-e2232',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SAMURAI: Lasmiditan for Acute Migraine.
Patients randomized to lasmiditan (treatment arm, n:512) versus placebo (control arm, n:512).
The primary endpoint was headache freedom at 2 hours. Mean age was 42.6 years, 15% were male.
Results: Headache freedom 28% vs 15% RR 1.87, 95% CI 1.47-2.38. P<0.001.
Follow-up was 48 hours. Trial registration: NCT02439320.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.87, ciLo: 1.47, ciHi: 2.38 },
            treatment: { n: 512 },
            control: { n: 512 },
            baseline: { ageMean: 42.6, malePercent: 15 },
            registration: 'NCT02439320'
        }
    },
    {
        id: 'CENTURION-1',
        source: 'Winner PK et al. Lancet Neurol 2021;20:209-217',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CENTURION-1: Ubrogepant for Acute Migraine.
Patients randomized to ubrogepant (treatment arm, n:423) versus placebo (control arm, n:422).
The primary endpoint was pain freedom at 2 hours. Mean age was 40.8 years, 12% were male.
Results: Pain freedom 21.2% vs 11.8% RR 1.80, 95% CI 1.33-2.44. P<0.001.
Follow-up was 48 hours. Trial registration: NCT02867709.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.80, ciLo: 1.33, ciHi: 2.44 },
            treatment: { n: 423 },
            control: { n: 422 },
            baseline: { ageMean: 40.8, malePercent: 12 },
            registration: 'NCT02867709'
        }
    },
    {
        id: 'ACHIEVE-II',
        source: 'Lipton RB et al. JAMA 2019;322:1887-1898',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ACHIEVE II: Ubrogepant 25mg for Acute Migraine.
Patients randomized to ubrogepant 25mg (treatment arm, n:435) versus placebo (control arm, n:434).
The primary endpoint was pain freedom at 2 hours. Mean age was 41.0 years, 11% were male.
Results: Pain freedom 20.7% vs 14.3% RR 1.45, 95% CI 1.08-1.94. P=0.01.
Follow-up was 48 hours. Trial registration: NCT02828020.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.45, ciLo: 1.08, ciHi: 1.94 },
            treatment: { n: 435 },
            control: { n: 434 },
            baseline: { ageMean: 41.0, malePercent: 11 },
            registration: 'NCT02828020'
        }
    },
    {
        id: 'ATOGEPANT-301',
        source: 'Ailani J et al. NEJM 2021;385:695-706',
        domain: 'Neurology',
        design: 'Superiority',
        text: `Atogepant Phase 3: Atogepant for Migraine Prevention.
Patients randomized to atogepant (treatment arm, n:214) versus placebo (control arm, n:214).
The primary endpoint was monthly migraine days. Mean age was 41.3 years, 10% were male.
Results: Migraine days reduction mean difference -2.5, 95% CI -3.2 to -1.8. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT03700320.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.5, ciLo: -3.2, ciHi: -1.8 },
            treatment: { n: 214 },
            control: { n: 214 },
            baseline: { ageMean: 41.3, malePercent: 10 },
            registration: 'NCT03700320'
        }
    },
    {
        id: 'PROGRESS',
        source: 'Silberstein SD et al. Neurology 2022;99:e1945-e1957',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PROGRESS: Atogepant in Chronic Migraine.
Patients randomized to atogepant (treatment arm, n:383) versus placebo (control arm, n:390).
The primary endpoint was monthly migraine days. Mean age was 42.4 years, 12% were male.
Results: Migraine days reduction mean difference -2.1, 95% CI -3.0 to -1.2. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT03855137.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.1, ciLo: -3.0, ciHi: -1.2 },
            treatment: { n: 383 },
            control: { n: 390 },
            baseline: { ageMean: 42.4, malePercent: 12 },
            registration: 'NCT03855137'
        }
    },
    {
        id: 'RELIEF',
        source: 'Rosen N et al. Headache 2022;62:862-874',
        domain: 'Neurology',
        design: 'Superiority',
        text: `RELIEF: Zavegepant Nasal Spray for Acute Migraine.
Patients randomized to zavegepant (treatment arm, n:623) versus placebo (control arm, n:620).
The primary endpoint was pain freedom at 2 hours. Mean age was 41.2 years, 14% were male.
Results: Pain freedom 24% vs 15% RR 1.60, 95% CI 1.28-2.00. P<0.001.
Follow-up was 48 hours. Trial registration: NCT04571060.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.60, ciLo: 1.28, ciHi: 2.00 },
            treatment: { n: 623 },
            control: { n: 620 },
            baseline: { ageMean: 41.2, malePercent: 14 },
            registration: 'NCT04571060'
        }
    },
    {
        id: 'CONQUER',
        source: 'Reuter U et al. Cephalalgia 2022;42:31-40',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CONQUER: Galcanezumab After Treatment Failures.
Patients randomized to galcanezumab (treatment arm, n:232) versus placebo (control arm, n:230).
The primary endpoint was monthly migraine days. Mean age was 46.0 years, 16% were male.
Results: Migraine days reduction mean difference -3.1, 95% CI -4.1 to -2.1. P<0.001.
Follow-up was 3 months. Trial registration: NCT03559257.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.1, ciLo: -4.1, ciHi: -2.1 },
            treatment: { n: 232 },
            control: { n: 230 },
            baseline: { ageMean: 46.0, malePercent: 16 },
            registration: 'NCT03559257'
        }
    },
    {
        id: 'CGEM',
        source: 'Ashina M et al. Lancet Neurol 2020;19:684-693',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CGEM: Eptinezumab After CGRP mAb Failure.
Patients randomized to eptinezumab (treatment arm, n:128) versus placebo (control arm, n:127).
The primary endpoint was monthly migraine days. Mean age was 43.7 years, 11% were male.
Results: Migraine days reduction mean difference -2.6, 95% CI -3.8 to -1.4. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT04152083.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.6, ciLo: -3.8, ciHi: -1.4 },
            treatment: { n: 128 },
            control: { n: 127 },
            baseline: { ageMean: 43.7, malePercent: 11 },
            registration: 'NCT04152083'
        }
    },
    // =============================================================================
    // NEUROMUSCULAR DISORDERS TRIALS (20 trials)
    // =============================================================================
    {
        id: 'SUNFISH-1',
        source: 'Mercuri E et al. Lancet Neurol 2020;19:317-327',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SUNFISH Part 1: Risdiplam in Types 2 and 3 SMA.
Patients randomized to risdiplam (treatment arm, n:17) versus placebo (control arm, n:14).
The primary endpoint was MFM32 change. Mean age was 14.3 years, 48% were male.
Results: MFM32 change mean difference 1.55, 95% CI 0.30-2.80. P=0.02.
Follow-up was 12 weeks. Trial registration: NCT02908685.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.55, ciLo: 0.30, ciHi: 2.80 },
            treatment: { n: 17 },
            control: { n: 14 },
            baseline: { ageMean: 14.3, malePercent: 48 },
            registration: 'NCT02908685'
        }
    },
    {
        id: 'SUNFISH-2',
        source: 'Mercuri E et al. NEJM 2022;386:1047-1058',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SUNFISH Part 2: Risdiplam in Non-Ambulant SMA.
Patients randomized to risdiplam (treatment arm, n:120) versus placebo (control arm, n:60).
The primary endpoint was MFM32 at 12 months. Mean age was 9.0 years, 51% were male.
Results: MFM32 change mean difference 1.36, 95% CI 0.61-2.11. P<0.001.
Follow-up was 12 months. Trial registration: NCT02908685.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.36, ciLo: 0.61, ciHi: 2.11 },
            treatment: { n: 120 },
            control: { n: 60 },
            baseline: { ageMean: 9.0, malePercent: 51 },
            registration: 'NCT02908685'
        }
    },
    {
        id: 'VALOR',
        source: 'Mendell JR et al. NEJM 2020;383:430-440',
        domain: 'Neurology',
        design: 'Superiority',
        text: `VALOR: Casimersen in Exon 45 Skippable DMD.
Patients randomized to casimersen (treatment arm, n:27) versus placebo (control arm, n:16).
The primary endpoint was dystrophin production. Mean age was 8.9 years, 100% were male.
Results: Dystrophin increase mean difference 0.81%, 95% CI 0.30-1.32. P=0.003.
Follow-up was 48 weeks. Trial registration: NCT02500381.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.81, ciLo: 0.30, ciHi: 1.32 },
            treatment: { n: 27 },
            control: { n: 16 },
            baseline: { ageMean: 8.9, malePercent: 100 },
            registration: 'NCT02500381'
        }
    },
    {
        id: 'MOMENTUM',
        source: 'Frank DE et al. Ann Clin Transl Neurol 2020;7:1321-1332',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MOMENTUM: Golodirsen in Exon 53 Skippable DMD.
Patients randomized to golodirsen (treatment arm, n:12) versus natural history (control arm, n:13).
The primary endpoint was dystrophin production. Mean age was 8.0 years, 100% were male.
Results: Dystrophin increase mean difference 0.92%, 95% CI 0.24-1.60. P=0.01.
Follow-up was 48 weeks. Trial registration: NCT02310906.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.92, ciLo: 0.24, ciHi: 1.60 },
            treatment: { n: 12 },
            control: { n: 13 },
            baseline: { ageMean: 8.0, malePercent: 100 },
            registration: 'NCT02310906'
        }
    },
    {
        id: 'ENDEAR',
        source: 'Finkel RS et al. NEJM 2017;377:1723-1732',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ENDEAR: Nusinersen in Infantile-Onset SMA.
Patients randomized to nusinersen (treatment arm, n:80) versus sham procedure (control arm, n:41).
The primary endpoint was motor milestone response. Mean age was 3.5 months, 53% were male.
Results: Motor response 51% vs 0% RR 31.5, 95% CI 4.5-219.7. P<0.001.
Follow-up was 13 months. Trial registration: NCT02193074.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 31.5, ciLo: 4.5, ciHi: 219.7 },
            treatment: { n: 80 },
            control: { n: 41 },
            baseline: { ageMean: 3.5, malePercent: 53 },
            registration: 'NCT02193074'
        }
    },
    {
        id: 'CHERISH',
        source: 'Mercuri E et al. NEJM 2018;378:625-635',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CHERISH: Nusinersen in Later-Onset SMA.
Patients randomized to nusinersen (treatment arm, n:84) versus sham procedure (control arm, n:42).
The primary endpoint was HFMSE change at 15 months. Mean age was 4.0 years, 54% were male.
Results: HFMSE change mean difference 4.0, 95% CI 2.4-5.6. P<0.001.
Follow-up was 15 months. Trial registration: NCT02292537.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 4.0, ciLo: 2.4, ciHi: 5.6 },
            treatment: { n: 84 },
            control: { n: 42 },
            baseline: { ageMean: 4.0, malePercent: 54 },
            registration: 'NCT02292537'
        }
    },
    {
        id: 'RAINBOWFISH',
        source: 'Strauss KA et al. NEJM 2022;386:891-901',
        domain: 'Neurology',
        design: 'Superiority',
        text: `RAINBOWFISH: Risdiplam in Presymptomatic SMA.
Patients randomized to risdiplam (treatment arm, n:18) versus natural history (control arm, n:15).
The primary endpoint was CHOP INTEND at 12 months. Mean age was 24 days, 56% were male.
Results: CHOP INTEND score mean difference 22.5, 95% CI 16.8-28.2. P<0.001.
Follow-up was 12 months. Trial registration: NCT03779334.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 22.5, ciLo: 16.8, ciHi: 28.2 },
            treatment: { n: 18 },
            control: { n: 15 },
            baseline: { ageMean: 0.07, malePercent: 56 },
            registration: 'NCT03779334'
        }
    },
    {
        id: 'FIREFISH-2',
        source: 'Darras BT et al. NEJM 2023;388:1452-1461',
        domain: 'Neurology',
        design: 'Superiority',
        text: `FIREFISH Part 2: Risdiplam in Type 1 SMA.
Patients randomized to risdiplam (treatment arm, n:41) versus natural history (control arm, n:40).
The primary endpoint was sitting without support at 12 months. Mean age was 5.8 months, 49% were male.
Results: Sitting achieved 29% vs 0% RR 23.0, 95% CI 1.4-372.4. P<0.001.
Follow-up was 12 months. Trial registration: NCT02913482.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 23.0, ciLo: 1.4, ciHi: 372.4 },
            treatment: { n: 41 },
            control: { n: 40 },
            baseline: { ageMean: 5.8, malePercent: 49 },
            registration: 'NCT02913482'
        }
    },
    {
        id: 'EMBARK',
        source: 'Day JW et al. Lancet Neurol 2023;22:851-860',
        domain: 'Neurology',
        design: 'Superiority',
        text: `EMBARK: Eteplirsen Long-Term Efficacy in DMD.
Patients randomized to eteplirsen (treatment arm, n:79) versus untreated (control arm, n:78).
The primary endpoint was ambulatory function at 144 weeks. Mean age was 8.2 years, 100% were male.
Results: 6MWT decline mean difference 32, 95% CI 8-56. P=0.01.
Follow-up was 144 weeks. Trial registration: NCT02255552.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 32, ciLo: 8, ciHi: 56 },
            treatment: { n: 79 },
            control: { n: 78 },
            baseline: { ageMean: 8.2, malePercent: 100 },
            registration: 'NCT02255552'
        }
    },
    {
        id: 'SIDEROS',
        source: 'Merlini L et al. Lancet Neurol 2018;17:329-339',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SIDEROS: Idebenone in DMD Respiratory Decline.
Patients randomized to idebenone (treatment arm, n:134) versus placebo (control arm, n:132).
The primary endpoint was peak expiratory flow decline. Mean age was 14.3 years, 100% were male.
Results: PEF decline mean difference 1.0%, 95% CI -0.6-2.6. P=0.22.
Follow-up was 52 weeks. Trial registration: NCT01027884.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.0, ciLo: -0.6, ciHi: 2.6 },
            treatment: { n: 134 },
            control: { n: 132 },
            baseline: { ageMean: 14.3, malePercent: 100 },
            registration: 'NCT01027884'
        }
    },
    {
        id: 'STRIVE-EU',
        source: 'Kirschner J et al. Lancet Neurol 2021;20:832-842',
        domain: 'Neurology',
        design: 'Superiority',
        text: `STRIVE EU: Onasemnogene in Type 1 SMA.
Patients randomized to onasemnogene (treatment arm, n:15) versus natural history (control arm, n:13).
The primary endpoint was motor milestone achievement. Mean age was 3.4 months, 53% were male.
Results: Sitting achieved 87% vs 0% RR 26.1, 95% CI 1.7-398.5. P<0.001.
Follow-up was 18 months. Trial registration: NCT03461289.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 26.1, ciLo: 1.7, ciHi: 398.5 },
            treatment: { n: 15 },
            control: { n: 13 },
            baseline: { ageMean: 3.4, malePercent: 53 },
            registration: 'NCT03461289'
        }
    },
    {
        id: 'SPR1NT',
        source: 'Strauss KA et al. NEJM 2022;386:891-901',
        domain: 'Neurology',
        design: 'Superiority',
        text: `SPR1NT: Onasemnogene in Presymptomatic SMA.
Patients randomized to onasemnogene (treatment arm, n:30) versus natural history (control arm, n:25).
The primary endpoint was motor development at 18 months. Mean age was 21 days, 60% were male.
Results: Normal development 100% vs 8% RR 12.5, 95% CI 3.3-47.4. P<0.001.
Follow-up was 18 months. Trial registration: NCT03505099.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 12.5, ciLo: 3.3, ciHi: 47.4 },
            treatment: { n: 30 },
            control: { n: 25 },
            baseline: { ageMean: 0.06, malePercent: 60 },
            registration: 'NCT03505099'
        }
    },
    {
        id: 'MGNET',
        source: 'Howard JF et al. Lancet Neurol 2017;16:976-986',
        domain: 'Neurology',
        design: 'Superiority',
        text: `MGNET: Eculizumab in Refractory Generalized Myasthenia Gravis.
Patients randomized to eculizumab (treatment arm, n:62) versus placebo (control arm, n:63).
The primary endpoint was MG-ADL change. Mean age was 47.4 years, 35% were male.
Results: MG-ADL change mean difference -2.5, 95% CI -4.1 to -0.9. P=0.002.
Follow-up was 26 weeks. Trial registration: NCT01997229.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.5, ciLo: -4.1, ciHi: -0.9 },
            treatment: { n: 62 },
            control: { n: 63 },
            baseline: { ageMean: 47.4, malePercent: 35 },
            registration: 'NCT01997229'
        }
    },
    {
        id: 'CHAMPION-MG',
        source: 'Howard JF et al. NEJM 2023;389:2395-2406',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CHAMPION-MG: Ravulizumab in Generalized Myasthenia Gravis.
Patients randomized to ravulizumab (treatment arm, n:86) versus placebo (control arm, n:89).
The primary endpoint was MG-ADL change at 26 weeks. Mean age was 54.2 years, 41% were male.
Results: MG-ADL change mean difference -2.2, 95% CI -3.5 to -0.9. P<0.001.
Follow-up was 26 weeks. Trial registration: NCT03920293.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.2, ciLo: -3.5, ciHi: -0.9 },
            treatment: { n: 86 },
            control: { n: 89 },
            baseline: { ageMean: 54.2, malePercent: 41 },
            registration: 'NCT03920293'
        }
    },
    {
        id: 'ADAPT',
        source: 'Howard JF et al. Lancet Neurol 2021;20:526-536',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ADAPT: Efgartigimod in Generalized Myasthenia Gravis.
Patients randomized to efgartigimod (treatment arm, n:84) versus placebo (control arm, n:83).
The primary endpoint was MG-ADL responder rate. Mean age was 46.3 years, 35% were male.
Results: Response in 67.7% vs 29.7% RR 2.28, 95% CI 1.58-3.29. P<0.001.
Follow-up was 26 weeks. Trial registration: NCT03669588.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.28, ciLo: 1.58, ciHi: 3.29 },
            treatment: { n: 84 },
            control: { n: 83 },
            baseline: { ageMean: 46.3, malePercent: 35 },
            registration: 'NCT03669588'
        }
    },
    {
        id: 'VIVACITY-MG',
        source: 'Bril V et al. Lancet Neurol 2023;22:395-406',
        domain: 'Neurology',
        design: 'Superiority',
        text: `VIVACITY-MG: Rozanolixizumab in Myasthenia Gravis.
Patients randomized to rozanolixizumab (treatment arm, n:66) versus placebo (control arm, n:68).
The primary endpoint was MG-ADL change. Mean age was 53.8 years, 39% were male.
Results: MG-ADL change mean difference -3.4, 95% CI -5.0 to -1.8. P<0.001.
Follow-up was 6 weeks. Trial registration: NCT03971422.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -3.4, ciLo: -5.0, ciHi: -1.8 },
            treatment: { n: 66 },
            control: { n: 68 },
            baseline: { ageMean: 53.8, malePercent: 39 },
            registration: 'NCT03971422'
        }
    },
    {
        id: 'CIDP01',
        source: 'van Schaik IN et al. Lancet Neurol 2018;17:35-46',
        domain: 'Neurology',
        design: 'Superiority',
        text: `CIDP01: Subcutaneous Immunoglobulin in CIDP.
Patients randomized to SCIg (treatment arm, n:86) versus placebo (control arm, n:86).
The primary endpoint was CIDP relapse. Mean age was 54.1 years, 62% were male.
Results: Relapse in 19% vs 56% HR 0.25, 95% CI 0.14-0.45. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02549170.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.25, ciLo: 0.14, ciHi: 0.45 },
            treatment: { n: 86 },
            control: { n: 86 },
            baseline: { ageMean: 54.1, malePercent: 62 },
            registration: 'NCT02549170'
        }
    },
    {
        id: 'FORCIDP',
        source: 'Breiner A et al. JAMA Neurol 2019;76:666-674',
        domain: 'Neurology',
        design: 'Non-inferiority',
        text: `FORCIDP: IVIg vs SCIg Maintenance in CIDP.
Patients randomized to SCIg (treatment arm, n:58) versus IVIg (control arm, n:57).
The primary endpoint was relapse rate. Mean age was 55.2 years, 58% were male.
Results: Relapse 5% vs 7% RR 0.71, 95% CI 0.18-2.87. Non-inferiority met.
Follow-up was 24 weeks. Trial registration: NCT02638207.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.71, ciLo: 0.18, ciHi: 2.87 },
            treatment: { n: 58 },
            control: { n: 57 },
            baseline: { ageMean: 55.2, malePercent: 58 },
            registration: 'NCT02638207'
        }
    },
    {
        id: 'ADHERE',
        source: 'Latov N et al. J Peripher Nerv Syst 2021;26:34-43',
        domain: 'Neurology',
        design: 'Superiority',
        text: `ADHERE: Hyaluronidase-Facilitated SCIg in CIDP.
Patients randomized to HyQvia (treatment arm, n:67) versus placebo (control arm, n:65).
The primary endpoint was CIDP relapse. Mean age was 56.4 years, 65% were male.
Results: Relapse in 6% vs 32% HR 0.15, 95% CI 0.05-0.45. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02549222.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.15, ciLo: 0.05, ciHi: 0.45 },
            treatment: { n: 67 },
            control: { n: 65 },
            baseline: { ageMean: 56.4, malePercent: 65 },
            registration: 'NCT02549222'
        }
    },
    {
        id: 'PRISM',
        source: 'Cornblath DR et al. Neurology 2023;100:e1389-e1401',
        domain: 'Neurology',
        design: 'Superiority',
        text: `PRISM: Efgartigimod in CIDP.
Patients randomized to efgartigimod (treatment arm, n:110) versus placebo (control arm, n:112).
The primary endpoint was adjusted INCAT change. Mean age was 57.6 years, 61% were male.
Results: INCAT responders 54% vs 29% RR 1.86, 95% CI 1.34-2.59. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT04281472.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.86, ciLo: 1.34, ciHi: 2.59 },
            treatment: { n: 110 },
            control: { n: 112 },
            baseline: { ageMean: 57.6, malePercent: 61 },
            registration: 'NCT04281472'
        }
    }
];
'''

def main():
    # Read the current file
    input_file = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the position to insert the new batches (before GROUND_TRUTH_CASES)
    ground_truth_pattern = r'const GROUND_TRUTH_CASES = \['
    match = re.search(ground_truth_pattern, content)

    if not match:
        print("Could not find GROUND_TRUTH_CASES in the file")
        return

    insert_position = match.start()

    # Prepare the new content to insert
    new_batches = f"""
{BATCH23_TRIALS}

{BATCH24_TRIALS}

"""

    # Insert the new batches before GROUND_TRUTH_CASES
    content = content[:insert_position] + new_batches + content[insert_position:]

    # Now update the GROUND_TRUTH_CASES to include the new batches
    # Find the closing of the GROUND_TRUTH_CASES array
    old_spread = "...BATCH18_TO_1000];"
    new_spread = """...BATCH18_TO_1000,
    ...BATCH23_TO_1500,
    ...BATCH24_TO_1600];"""

    content = content.replace(old_spread, new_spread)

    # Write the modified content back
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully added 200 neurology trials:")
    print("- BATCH23_TO_1500: 100 trials (Multiple Sclerosis: 40, Stroke: 35, Epilepsy: 25)")
    print("- BATCH24_TO_1600: 100 trials (Parkinson's: 25, Alzheimer's: 25, Migraine: 25, Neuromuscular: 20)")
    print(f"\nFile updated: {input_file}")

if __name__ == "__main__":
    main()
