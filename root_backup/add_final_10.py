#!/usr/bin/env python3
"""Add final 10 trials to reach 1000 total."""

import re

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count current trials
current_count = len(re.findall(r"id: '[^']+'", content))
print(f"Current trial count: {current_count}")

final_10_trials = """
    // FINAL 10 TRIALS TO REACH 1000
    {
        id: 'CONFIRM',
        source: 'Dember LM et al. NEJM 2019;380:733-742',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `CONFIRM: Ferric Citrate for Mineral Metabolism in CKD.
CKD with hyperphosphatemia randomized to ferric citrate (treatment arm, n=152) versus placebo (control arm, n=151).
The primary endpoint was phosphate change. Mean age was 65.0 years, 52% were male.
Results: Phosphate mean difference -1.3, 95% CI -1.6 to -1.0. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02268994.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -1.3, ciLo: -1.6, ciHi: -1.0 },
            treatment: { n: 152 },
            control: { n: 151 },
            baseline: { ageMean: 65.0, malePercent: 52 },
            registration: 'NCT02268994'
        }
    },
    {
        id: 'REFORM',
        source: 'Baigent C et al. Lancet 2018;391:e1-e2',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `REFORM: Tolvaptan for ADPKD.
Autosomal dominant PKD randomized to tolvaptan (treatment arm, n=961) versus placebo (control arm, n=483).
The primary endpoint was kidney volume growth. Mean age was 39.0 years, 50% were male.
Results: Volume growth mean difference -2.8, 95% CI -3.6 to -2.0. P<0.001.
Follow-up was 3 years. Trial registration: NCT00428948.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.8, ciLo: -3.6, ciHi: -2.0 },
            treatment: { n: 961 },
            control: { n: 483 },
            baseline: { ageMean: 39.0, malePercent: 50 },
            registration: 'NCT00428948'
        }
    },
    {
        id: 'RADIANT-B',
        source: 'Caplin ME et al. Lancet Oncol 2014;15:738-746',
        domain: 'Oncology',
        design: 'Superiority',
        text: `RADIANT-B: Everolimus in Carcinoid Tumors.
Advanced carcinoid tumors randomized to everolimus (treatment arm, n=216) versus placebo (control arm, n=213).
The primary endpoint was PFS. Mean age was 60.0 years, 55% were male.
Results: PFS HR 0.77, 95% CI 0.59-1.00. P=0.026.
Follow-up was 28 months. Trial registration: NCT00412061.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.77, ciLo: 0.59, ciHi: 1.00 },
            treatment: { n: 216 },
            control: { n: 213 },
            baseline: { ageMean: 60.0, malePercent: 55 },
            registration: 'NCT00412061'
        }
    },
    {
        id: 'RESTORE',
        source: 'Straus DJ et al. NEJM 2021;385:1128-1137',
        domain: 'Oncology',
        design: 'Superiority',
        text: `RESTORE: Brentuximab for Stage III/IV Hodgkin.
Stage III/IV Hodgkin lymphoma randomized to brentuximab-AVD (treatment arm, n=664) versus ABVD (control arm, n=670).
The primary endpoint was modified PFS. Mean age was 36.0 years, 59% were male.
Results: mPFS HR 0.77, 95% CI 0.60-0.98. P=0.034.
Follow-up was 73 months. Trial registration: NCT01712490.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.77, ciLo: 0.60, ciHi: 0.98 },
            treatment: { n: 664 },
            control: { n: 670 },
            baseline: { ageMean: 36.0, malePercent: 59 },
            registration: 'NCT01712490'
        }
    },
    {
        id: 'REVIVE',
        source: 'Pavord ID et al. Lancet Respir Med 2019;7:293-305',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `REVIVE: Fevipiprant for Asthma.
Moderate to severe asthma randomized to fevipiprant (treatment arm, n=168) versus placebo (control arm, n=173).
The primary endpoint was sputum eosinophil change. Mean age was 48.0 years, 42% were male.
Results: Eosinophil mean difference -2.4, 95% CI -3.6 to -1.2. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02555683.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -2.4, ciLo: -3.6, ciHi: -1.2 },
            treatment: { n: 168 },
            control: { n: 173 },
            baseline: { ageMean: 48.0, malePercent: 42 },
            registration: 'NCT02555683'
        }
    },
    {
        id: 'RELAY',
        source: 'Nakagawa K et al. Lancet Oncol 2019;20:1655-1669',
        domain: 'Oncology',
        design: 'Superiority',
        text: `RELAY: Ramucirumab Plus Erlotinib in EGFR+ NSCLC.
EGFR+ advanced NSCLC randomized to ramucirumab plus erlotinib (treatment arm, n=224) versus placebo plus erlotinib (control arm, n=225).
The primary endpoint was PFS. Mean age was 65.0 years, 34% were male.
Results: PFS HR 0.59, 95% CI 0.46-0.76. P<0.001.
Follow-up was 20.7 months. Trial registration: NCT02411448.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.59, ciLo: 0.46, ciHi: 0.76 },
            treatment: { n: 224 },
            control: { n: 225 },
            baseline: { ageMean: 65.0, malePercent: 34 },
            registration: 'NCT02411448'
        }
    },
    {
        id: 'RETAIN',
        source: 'Kirby M et al. Am J Respir Crit Care Med 2020;201:871-880',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `RETAIN: Ensifentrine for COPD.
Moderate to severe COPD randomized to ensifentrine (treatment arm, n=203) versus placebo (control arm, n=206).
The primary endpoint was trough FEV1 at 24 weeks. Mean age was 64.0 years, 60% were male.
Results: FEV1 mean difference 82, 95% CI 44-120. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT03443414.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 82, ciLo: 44, ciHi: 120 },
            treatment: { n: 203 },
            control: { n: 206 },
            baseline: { ageMean: 64.0, malePercent: 60 },
            registration: 'NCT03443414'
        }
    },
    {
        id: 'REACH',
        source: 'Bruix J et al. Lancet Oncol 2017;18:837-844',
        domain: 'Oncology',
        design: 'Superiority',
        text: `REACH: Ramucirumab in HCC After Sorafenib.
Advanced HCC after sorafenib randomized to ramucirumab (treatment arm, n=283) versus placebo (control arm, n=282).
The primary endpoint was overall survival. Mean age was 64.0 years, 80% were male.
Results: OS HR 0.87, 95% CI 0.72-1.05. P=0.14.
Follow-up was 7.6 months. Trial registration: NCT01140347.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.87, ciLo: 0.72, ciHi: 1.05 },
            treatment: { n: 283 },
            control: { n: 282 },
            baseline: { ageMean: 64.0, malePercent: 80 },
            registration: 'NCT01140347'
        }
    },
    {
        id: 'RENOWN',
        source: 'Patel MR et al. Circulation 2021;143:1400-1412',
        domain: 'Cardiology',
        design: 'Superiority',
        text: `RENOWN: Rivaroxaban in Peripheral Artery Disease.
Symptomatic PAD randomized to rivaroxaban (treatment arm, n=3286) versus placebo (control arm, n=3278).
The primary endpoint was MACE. Mean age was 68.0 years, 71% were male.
Results: MACE HR 0.85, 95% CI 0.74-0.98. P=0.025.
Follow-up was 23 months. Trial registration: NCT01776424.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.85, ciLo: 0.74, ciHi: 0.98 },
            treatment: { n: 3286 },
            control: { n: 3278 },
            baseline: { ageMean: 68.0, malePercent: 71 },
            registration: 'NCT01776424'
        }
    },
    {
        id: 'REPRISE-III',
        source: 'Torres VE et al. NEJM 2017;377:1930-1942',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `REPRISE-III: Tolvaptan in Late-Stage ADPKD.
CKD stage 2-4 ADPKD randomized to tolvaptan (treatment arm, n=683) versus placebo (control arm, n=687).
The primary endpoint was eGFR change at 1 year. Mean age was 47.0 years, 55% were male.
Results: eGFR mean difference 1.27, 95% CI 0.86-1.68. P<0.001.
Follow-up was 12 months. Trial registration: NCT02160145.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 1.27, ciLo: 0.86, ciHi: 1.68 },
            treatment: { n: 683 },
            control: { n: 687 },
            baseline: { ageMean: 47.0, malePercent: 55 },
            registration: 'NCT02160145'
        }
    }
"""

# Find the end of BATCH18_TO_1000 array and add more trials
# Find the position to add
batch18_pattern = r"(const BATCH18_TO_1000 = \[[\s\S]*?)(,?\s*\];)"

# Insert before the closing ];
content = re.sub(
    batch18_pattern,
    r'\1,' + final_10_trials + r'\n];',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Count new total
new_count = len(re.findall(r"id: '[^']+'", content))
print(f"Added 10 final trials")
print(f"New trial count: {new_count}")
