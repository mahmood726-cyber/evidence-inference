#!/usr/bin/env python3
"""
Batch generator for 1000 Inflammatory/Autoimmune RCT trials
Appends to validation_study_expanded.js
"""

import random
import os

# Set seed for reproducibility
random.seed(42)

# Target file
TARGET_FILE = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

# Disease categories with trial counts
DISEASE_CATEGORIES = {
    'RA': 200,      # Rheumatoid arthritis
    'PSO': 150,     # Psoriasis/PsA
    'IBD': 150,     # IBD (UC, Crohn's)
    'LUPUS': 100,   # Lupus/CTD
    'AS': 100,      # Ankylosing spondylitis
    'AD': 150,      # Atopic dermatitis
    'AUTO': 150     # Other autoimmune (MS, MG, vasculitis)
}

# Drug databases by disease
RA_DRUGS = {
    'JAK': ['tofacitinib', 'baricitinib', 'upadacitinib', 'filgotinib', 'peficitinib'],
    'TNF': ['adalimumab', 'etanercept', 'infliximab', 'certolizumab', 'golimumab'],
    'IL6': ['tocilizumab', 'sarilumab'],
    'CD20': ['rituximab', 'ocrelizumab'],
    'CTLA4': ['abatacept'],
    'csDMARD': ['methotrexate', 'leflunomide', 'sulfasalazine', 'hydroxychloroquine']
}

PSO_DRUGS = {
    'IL17': ['secukinumab', 'ixekizumab', 'brodalumab', 'bimekizumab'],
    'IL23': ['guselkumab', 'risankizumab', 'tildrakizumab', 'mirikizumab'],
    'IL12_23': ['ustekinumab'],
    'TNF': ['adalimumab', 'etanercept', 'infliximab', 'certolizumab'],
    'JAK': ['tofacitinib', 'deucravacitinib', 'brepocitinib'],
    'PDE4': ['apremilast']
}

IBD_DRUGS = {
    'TNF': ['infliximab', 'adalimumab', 'certolizumab', 'golimumab'],
    'INTEGRIN': ['vedolizumab', 'natalizumab'],
    'IL12_23': ['ustekinumab'],
    'IL23': ['risankizumab', 'mirikizumab', 'guselkumab'],
    'JAK': ['tofacitinib', 'filgotinib', 'upadacitinib'],
    'S1P': ['ozanimod', 'etrasimod']
}

LUPUS_DRUGS = {
    'BLYS': ['belimumab', 'blisibimod'],
    'CNI': ['voclosporin', 'tacrolimus', 'cyclosporine'],
    'IFNAR': ['anifrolumab'],
    'CD20': ['rituximab', 'obinutuzumab'],
    'MMF': ['mycophenolate mofetil'],
    'OTHER': ['hydroxychloroquine', 'azathioprine']
}

AS_DRUGS = {
    'TNF': ['adalimumab', 'etanercept', 'infliximab', 'certolizumab', 'golimumab'],
    'IL17': ['secukinumab', 'ixekizumab', 'bimekizumab'],
    'JAK': ['tofacitinib', 'upadacitinib', 'filgotinib']
}

AD_DRUGS = {
    'IL4_13': ['dupilumab', 'tralokinumab', 'lebrikizumab'],
    'JAK': ['baricitinib', 'upadacitinib', 'abrocitinib', 'ruxolitinib'],
    'IL13': ['cendakimab'],
    'IL31': ['nemolizumab'],
    'PDE4': ['crisaborole', 'roflumilast', 'difamilast']
}

AUTO_DRUGS = {
    'MS': ['ocrelizumab', 'ofatumumab', 'natalizumab', 'alemtuzumab', 'siponimod', 'ozanimod', 'ponesimod', 'dimethyl fumarate', 'teriflunomide'],
    'MG': ['eculizumab', 'ravulizumab', 'efgartigimod', 'rozanolixizumab', 'zilucoplan'],
    'VASC': ['rituximab', 'avacopan', 'mepolizumab', 'tocilizumab'],
    'SSC': ['tocilizumab', 'nintedanib', 'rituximab'],
    'SJOGREN': ['belimumab', 'rituximab', 'ianalumab']
}

# Outcome measures by disease
RA_OUTCOMES = ['ACR20', 'ACR50', 'ACR70', 'DAS28-CRP', 'DAS28-ESR', 'HAQ-DI', 'CDAI', 'SDAI', 'mTSS', 'radiographic progression']
PSO_OUTCOMES = ['PASI75', 'PASI90', 'PASI100', 'IGA 0/1', 'BSA', 'DLQI', 'ACR20 (PsA)', 'ACR50 (PsA)', 'MDA', 'DAPSA']
IBD_OUTCOMES = ['clinical remission', 'clinical response', 'endoscopic remission', 'mucosal healing', 'CDAI remission', 'Mayo score', 'partial Mayo score', 'histologic remission']
LUPUS_OUTCOMES = ['SRI-4', 'BICLA', 'complete renal response', 'partial renal response', 'SLEDAI', 'BILAG', 'flare reduction', 'steroid sparing']
AS_OUTCOMES = ['ASAS20', 'ASAS40', 'BASDAI50', 'ASDAS-CRP', 'ASDAS inactive disease', 'partial remission', 'MRI inflammation', 'BASFI']
AD_OUTCOMES = ['EASI-75', 'EASI-90', 'IGA 0/1', 'NRS pruritus', 'DLQI', 'SCORAD', 'vIGA-AD', 'PP-NRS']
AUTO_OUTCOMES = {
    'MS': ['annualized relapse rate', 'EDSS progression', 'MRI lesions', 'brain atrophy', 'no evidence of disease activity'],
    'MG': ['MG-ADL', 'QMG', 'MGC', 'MG-QoL15', 'clinical improvement'],
    'VASC': ['remission', 'GPA response', 'BVAS', 'steroid-free remission'],
    'SSC': ['mRSS', 'FVC decline', 'skin score'],
    'SJOGREN': ['ESSDAI', 'ESSPRI', 'salivary flow', 'fatigue VAS']
}

# Study acronym prefixes
RA_ACRONYMS = ['ORAL', 'SELECT', 'FINCH', 'GO', 'RAPID', 'TOWARD', 'ACT', 'REFLEX', 'RADIATE', 'ATTAIN', 'AMPLE', 'MONARCH', 'EXCEED', 'JAK-', 'RA-']
PSO_ACRONYMS = ['CLEAR', 'ECLIPSE', 'IXORA', 'FIXTURE', 'ERASURE', 'VOYAGE', 'ULTIMMA', 'ENCHANT', 'BE-', 'POETYK', 'DISCOVER', 'SPIRIT']
IBD_ACRONYMS = ['GEMINI', 'UNIFI', 'VARSITY', 'ADVANCE', 'MOTIVATE', 'U-', 'TRUE', 'VIVID', 'ELEVATE', 'LUCENT', 'GALAXI']
LUPUS_ACRONYMS = ['BLISS', 'AURORA', 'TULIP', 'EXPLORER', 'LUNAR', 'BELONG', 'ILLUMINATE', 'ADDRESS', 'NOBILITY']
AS_ACRONYMS = ['MEASURE', 'COAST', 'SELECT', 'BE-', 'ATLAS', 'RAPID', 'SPINE', 'ABILITY']
AD_ACRONYMS = ['SOLO', 'CAFÉ', 'CHRONOS', 'LIBERTY', 'BREEZE', 'JADE', 'ECZTRA', 'HEADS', 'MEASURE', 'ADEPT']
AUTO_ACRONYMS = ['OPERA', 'ASCLEPIOS', 'CHAMPION', 'SUNRISE', 'ADAPT', 'HAVEN', 'REGAIN', 'RAISE', 'ADVOCATE', 'SENSCIS']

# Journals and sources
JOURNALS = [
    'N Engl J Med', 'Lancet', 'JAMA', 'Ann Rheum Dis', 'Arthritis Rheumatol',
    'J Am Acad Dermatol', 'Br J Dermatol', 'Gastroenterology', 'Gut',
    'Lancet Rheumatol', 'Lancet Gastroenterol Hepatol', 'JAMA Dermatol',
    'Ann Intern Med', 'Rheumatology', 'J Crohns Colitis', 'Inflamm Bowel Dis',
    'Lupus', 'Lupus Sci Med', 'J Invest Dermatol', 'Mult Scler',
    'Neurology', 'JAMA Neurol', 'Muscle Nerve'
]

# Author last names
AUTHOR_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
    'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
    'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
    'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen',
    'Hill', 'Flores', 'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera',
    'Campbell', 'Mitchell', 'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans',
    'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart',
    'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz',
    'van der Berg', 'Fleischmann', 'Burmester', 'Smolen', 'Weinblatt', 'Kremer',
    'Kavanaugh', 'Strand', 'Curtis', 'Genovese', 'Cohen', 'Keystone', 'Emery',
    'Tanaka', 'Takeuchi', 'Yamanaka', 'Harigai', 'Reich', 'Blauvelt', 'Gordon',
    'Armstrong', 'Menter', 'Lebwohl', 'Griffiths', 'Warren', 'Papp', 'Langley',
    'Schreiber', 'Sands', 'Sandborn', 'Hanauer', 'Colombel', 'Feagan', 'Vermeire',
    'Danese', 'Lichtenstein', 'Panaccione', 'Peyrin-Biroulet', 'Furie', 'Morand',
    'Rovin', 'Jayne', 'Merkel', 'Hauser', 'Kappos', 'Comi', 'Montalban'
]

# Countries and sites
COUNTRIES = [
    'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Italy', 'Spain',
    'Netherlands', 'Belgium', 'Switzerland', 'Austria', 'Poland', 'Czech Republic',
    'Hungary', 'Russia', 'Ukraine', 'Japan', 'South Korea', 'Taiwan', 'China',
    'Australia', 'New Zealand', 'Brazil', 'Argentina', 'Mexico', 'South Africa',
    'Israel', 'Turkey', 'India', 'Singapore', 'Thailand', 'Malaysia'
]

# Generate NCT number
def generate_nct():
    return f"NCT{random.randint(10000000, 99999999)}"

# Generate trial ID
def generate_trial_id(category, index):
    return f"IMMUN-{category}-{index:03d}"

# Generate study acronym
def generate_acronym(category, drug_class, index):
    if category == 'RA':
        prefixes = RA_ACRONYMS
    elif category == 'PSO':
        prefixes = PSO_ACRONYMS
    elif category == 'IBD':
        prefixes = IBD_ACRONYMS
    elif category == 'LUPUS':
        prefixes = LUPUS_ACRONYMS
    elif category == 'AS':
        prefixes = AS_ACRONYMS
    elif category == 'AD':
        prefixes = AD_ACRONYMS
    else:
        prefixes = AUTO_ACRONYMS

    prefix = random.choice(prefixes)
    suffix = random.choice(['', '-I', '-II', '-III', '-IV', '-V', '-X', '-Y', '-Z',
                           'A', 'B', 'C', 'D', '1', '2', '3', '4', '5'])
    return f"{prefix}{drug_class.upper()}{suffix}"

# Generate author citation
def generate_citation(year):
    author = random.choice(AUTHOR_NAMES)
    journal = random.choice(JOURNALS)
    volume = random.randint(300, 400)
    page_start = random.randint(100, 2000)
    page_end = page_start + random.randint(8, 15)
    return f"{author} et al. {journal} {year};{volume}:{page_start}-{page_end}"

# Generate sample sizes
def generate_sample_sizes():
    base_n = random.choice([50, 75, 100, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800])
    ratio = random.choice([1.0, 1.0, 1.0, 2.0])  # 1:1 or 2:1 ratio
    treatment_n = int(base_n * ratio)
    control_n = base_n
    if random.random() < 0.3:  # Sometimes swap
        treatment_n, control_n = control_n, treatment_n
    return treatment_n, control_n

# Generate RR (response rate ratio)
def generate_rr():
    rr = round(random.uniform(1.5, 4.0), 2)
    # CI width varies inversely with sample size simulation
    ci_width = round(random.uniform(0.3, 1.2), 2)
    ci_lo = round(max(1.01, rr - ci_width/2), 2)
    ci_hi = round(rr + ci_width/2, 2)
    return rr, ci_lo, ci_hi

# Generate MD (mean difference) for score changes
def generate_md(score_type):
    if score_type in ['DAS28-CRP', 'DAS28-ESR', 'CDAI', 'ASDAS-CRP']:
        md = round(random.uniform(-2.5, -0.8), 2)
        ci_width = round(random.uniform(0.3, 0.8), 2)
    elif score_type in ['HAQ-DI', 'DLQI', 'FACIT-F']:
        md = round(random.uniform(-0.5, -0.15), 2)
        ci_width = round(random.uniform(0.1, 0.3), 2)
    elif score_type in ['EASI', 'SCORAD', 'PASI']:
        md = round(random.uniform(-15, -5), 1)
        ci_width = round(random.uniform(2, 5), 1)
    elif score_type in ['SLEDAI', 'BILAG']:
        md = round(random.uniform(-8, -2), 1)
        ci_width = round(random.uniform(1, 3), 1)
    else:
        md = round(random.uniform(-5, -1), 2)
        ci_width = round(random.uniform(0.5, 2), 2)

    ci_lo = round(md - ci_width/2, 2)
    ci_hi = round(md + ci_width/2, 2)
    return md, ci_lo, ci_hi

# Generate percentage response
def generate_response_rate():
    treatment_rate = round(random.uniform(35, 85), 1)
    # Control is lower
    control_rate = round(treatment_rate / random.uniform(1.3, 2.5), 1)
    return treatment_rate, control_rate

# Generate RA trial
def generate_ra_trial(index):
    drug_class = random.choice(list(RA_DRUGS.keys()))
    drug = random.choice(RA_DRUGS[drug_class])
    comparator = random.choice(['placebo', 'placebo', 'placebo', 'methotrexate', 'adalimumab'])

    treatment_n, control_n = generate_sample_sizes()
    total_n = treatment_n + control_n

    outcome = random.choice(RA_OUTCOMES[:7])  # Primary efficacy outcomes

    age = round(random.uniform(48, 62), 1)
    female_pct = round(random.uniform(72, 85), 1)
    disease_duration = round(random.uniform(4, 15), 1)
    rf_positive = round(random.uniform(65, 90), 1)

    treatment_rate, control_rate = generate_response_rate()
    rr, rr_lo, rr_hi = generate_rr()

    das28_md, das28_lo, das28_hi = generate_md('DAS28-CRP')
    haq_md, haq_lo, haq_hi = generate_md('HAQ-DI')

    followup_weeks = random.choice([12, 14, 16, 24, 52, 104])
    year = random.randint(2015, 2024)

    nct = generate_nct()
    acronym = generate_acronym('RA', drug_class, index)
    trial_id = generate_trial_id('RA', index)

    dose = random.choice(['5 mg', '10 mg', '15 mg', '50 mg', '100 mg', '150 mg', '200 mg'])
    frequency = random.choice(['once daily', 'twice daily', 'every two weeks', 'monthly'])

    sites = random.randint(80, 350)
    countries = random.randint(10, 35)

    text = f"""{acronym} Trial: {drug.title()} in Active Rheumatoid Arthritis

This was a randomized, double-blind, {comparator}-controlled, phase 3 trial conducted at {sites} sites across {countries} countries.
We enrolled {total_n} patients with moderate-to-severe active rheumatoid arthritis who had inadequate response to conventional DMARDs.

Patients were randomly assigned to receive {drug} {dose} {frequency} ({treatment_n} patients, treatment arm, n={treatment_n})
or {comparator} ({control_n} patients, control arm, n={control_n}). Background methotrexate was continued in both groups.

Mean age was {age} years, {female_pct}% were female. Mean disease duration was {disease_duration} years.
{rf_positive}% were RF-positive. Mean baseline DAS28-CRP was {round(random.uniform(5.2, 6.5), 1)}.

The primary endpoint was {outcome} response at week {followup_weeks}. {outcome} was achieved by {treatment_rate}%
of patients in the {drug} group versus {control_rate}% in the {comparator} group
(RR {rr}; 95% CI {rr_lo}-{rr_hi}; P<0.001).

Change from baseline in DAS28-CRP: {drug} {das28_md} vs {comparator} {round(das28_md/2, 2)}
(MD {das28_md}; 95% CI {das28_lo}-{das28_hi}).

HAQ-DI improvement: MD {haq_md} (95% CI {haq_lo}-{haq_hi}) favoring {drug}.

Safety: Serious adverse events occurred in {round(random.uniform(3, 12), 1)}% vs {round(random.uniform(2, 8), 1)}%.
Serious infections: {round(random.uniform(1, 4), 1)}% vs {round(random.uniform(0.5, 2), 1)}%.

The trial was registered at ClinicalTrials.gov ({nct})."""

    ground_truth = {
        'study': {'acronym': acronym},
        'treatment': {'n': treatment_n, 'name': drug},
        'control': {'n': control_n, 'name': comparator},
        'totalN': total_n,
        'primaryEffect': {'type': 'RR', 'value': rr, 'ciLo': rr_lo, 'ciHi': rr_hi},
        'baseline': {
            'ageMean': age,
            'femalePercent': female_pct,
            'diseaseDuration': disease_duration
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': generate_citation(year),
        'domain': 'Rheumatology',
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

# Generate Psoriasis/PsA trial
def generate_pso_trial(index):
    is_psa = random.random() < 0.35
    drug_class = random.choice(list(PSO_DRUGS.keys()))
    drug = random.choice(PSO_DRUGS[drug_class])
    comparator = random.choice(['placebo', 'placebo', 'placebo', 'adalimumab', 'ustekinumab', 'etanercept'])

    treatment_n, control_n = generate_sample_sizes()
    total_n = treatment_n + control_n

    if is_psa:
        outcome = random.choice(['ACR20', 'ACR50', 'MDA', 'DAPSA'])
        disease = 'psoriatic arthritis'
    else:
        outcome = random.choice(['PASI75', 'PASI90', 'PASI100', 'IGA 0/1'])
        disease = 'moderate-to-severe plaque psoriasis'

    age = round(random.uniform(42, 55), 1)
    male_pct = round(random.uniform(55, 72), 1)
    bsa = round(random.uniform(18, 35), 1)
    pasi_baseline = round(random.uniform(18, 28), 1)

    treatment_rate, control_rate = generate_response_rate()
    rr, rr_lo, rr_hi = generate_rr()

    followup_weeks = random.choice([12, 16, 24, 52])
    year = random.randint(2016, 2024)

    nct = generate_nct()
    acronym = generate_acronym('PSO', drug_class, index)
    trial_id = generate_trial_id('PSO', index)

    dose = random.choice(['45 mg', '90 mg', '100 mg', '150 mg', '300 mg', '320 mg'])
    frequency = random.choice(['every 4 weeks', 'every 8 weeks', 'every 12 weeks', 'at weeks 0, 4, then every 12 weeks'])

    sites = random.randint(60, 250)
    countries = random.randint(8, 25)

    text = f"""{acronym} Trial: {drug.title()} for {disease.title()}

This was a randomized, double-blind, {comparator}-controlled, phase 3 trial conducted at {sites} sites in {countries} countries.
We enrolled {total_n} adults with {disease} who were candidates for systemic therapy or phototherapy.

Patients were randomly assigned to {drug} {dose} {frequency} ({treatment_n} patients, treatment arm, n={treatment_n})
or {comparator} ({control_n} patients, control arm, n={control_n}).

Mean age was {age} years, {male_pct}% were male. Mean body surface area affected was {bsa}%.
Mean baseline PASI score was {pasi_baseline}.

The primary endpoint was {outcome} response at week {followup_weeks}. The {outcome} response rate was {treatment_rate}%
in the {drug} group versus {control_rate}% in the {comparator} group
(RR {rr}; 95% CI {rr_lo}-{rr_hi}; P<0.001).

DLQI 0/1 (no impact on quality of life): {round(treatment_rate * 0.7, 1)}% vs {round(control_rate * 0.5, 1)}%.

Adverse events were reported in {round(random.uniform(45, 65), 1)}% vs {round(random.uniform(40, 55), 1)}% of patients.
Serious adverse events: {round(random.uniform(1.5, 5), 1)}% vs {round(random.uniform(1, 4), 1)}%.
Injection site reactions: {round(random.uniform(1, 8), 1)}% vs {round(random.uniform(0.5, 3), 1)}%.

Trial registration: {nct}. Funded by pharmaceutical sponsor."""

    ground_truth = {
        'study': {'acronym': acronym},
        'treatment': {'n': treatment_n, 'name': drug},
        'control': {'n': control_n, 'name': comparator},
        'totalN': total_n,
        'primaryEffect': {'type': 'RR', 'value': rr, 'ciLo': rr_lo, 'ciHi': rr_hi},
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct,
            'bsa': bsa
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': generate_citation(year),
        'domain': 'Dermatology/Rheumatology' if is_psa else 'Dermatology',
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

# Generate IBD trial
def generate_ibd_trial(index):
    is_cd = random.random() < 0.5
    drug_class = random.choice(list(IBD_DRUGS.keys()))
    drug = random.choice(IBD_DRUGS[drug_class])
    comparator = random.choice(['placebo', 'placebo', 'placebo', 'adalimumab'])

    treatment_n, control_n = generate_sample_sizes()
    total_n = treatment_n + control_n

    if is_cd:
        outcome = random.choice(['clinical remission', 'CDAI remission', 'endoscopic response', 'endoscopic remission'])
        disease = "Crohn's disease"
        score_type = 'CDAI'
    else:
        outcome = random.choice(['clinical remission', 'Mayo score remission', 'endoscopic improvement', 'mucosal healing'])
        disease = 'ulcerative colitis'
        score_type = 'Mayo'

    age = round(random.uniform(35, 48), 1)
    male_pct = round(random.uniform(45, 58), 1)
    disease_duration = round(random.uniform(5, 15), 1)
    prior_biologic = round(random.uniform(25, 60), 1)

    treatment_rate, control_rate = generate_response_rate()
    rr, rr_lo, rr_hi = generate_rr()

    induction_weeks = random.choice([8, 10, 12, 14])
    maintenance_weeks = random.choice([44, 52, 54])
    year = random.randint(2016, 2024)

    nct = generate_nct()
    acronym = generate_acronym('IBD', drug_class, index)
    trial_id = generate_trial_id('IBD', index)

    dose = random.choice(['100 mg', '200 mg', '300 mg', '5 mg/kg', '10 mg/kg'])
    frequency = random.choice(['every 8 weeks', 'every 4 weeks', 'once daily', 'at weeks 0, 2, 6 then every 8 weeks'])

    sites = random.randint(100, 400)
    countries = random.randint(15, 40)

    text = f"""{acronym} Trial: {drug.title()} for Moderate-to-Severe {disease}

This was a randomized, double-blind, {comparator}-controlled, phase 3 trial conducted at {sites} sites in {countries} countries.
We enrolled {total_n} patients with moderate-to-severe {disease} who had inadequate response or intolerance to conventional therapy.

Patients were randomly assigned to {drug} {dose} {frequency} ({treatment_n} patients, treatment arm, n={treatment_n})
or {comparator} ({control_n} patients, control arm, n={control_n}).

Mean age was {age} years, {male_pct}% were male. Mean disease duration was {disease_duration} years.
{prior_biologic}% had prior biologic exposure. Mean baseline {score_type} score was {round(random.uniform(280, 380) if is_cd else random.uniform(8, 11), 1)}.

Induction phase (week {induction_weeks}): {outcome} was achieved by {treatment_rate}% of patients receiving {drug}
versus {control_rate}% receiving {comparator} (RR {rr}; 95% CI {rr_lo}-{rr_hi}; P<0.001).

Maintenance phase (week {maintenance_weeks}): Among induction responders, {round(treatment_rate * 0.9, 1)}% maintained
remission with {drug} versus {round(control_rate * 1.2, 1)}% with {comparator}.

Endoscopic improvement: {round(treatment_rate * 0.65, 1)}% vs {round(control_rate * 0.4, 1)}%.
Corticosteroid-free remission: {round(treatment_rate * 0.75, 1)}% vs {round(control_rate * 0.5, 1)}%.

Serious adverse events: {round(random.uniform(5, 12), 1)}% vs {round(random.uniform(6, 14), 1)}%.
Serious infections: {round(random.uniform(2, 5), 1)}% vs {round(random.uniform(1.5, 4), 1)}%.

Trial registration: {nct}."""

    ground_truth = {
        'study': {'acronym': acronym},
        'treatment': {'n': treatment_n, 'name': drug},
        'control': {'n': control_n, 'name': comparator},
        'totalN': total_n,
        'primaryEffect': {'type': 'RR', 'value': rr, 'ciLo': rr_lo, 'ciHi': rr_hi},
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct,
            'diseaseDuration': disease_duration
        },
        'inductionWeeks': induction_weeks,
        'maintenanceWeeks': maintenance_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': generate_citation(year),
        'domain': 'Gastroenterology',
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

# Generate Lupus/CTD trial
def generate_lupus_trial(index):
    is_ln = random.random() < 0.4  # Lupus nephritis
    drug_class = random.choice(list(LUPUS_DRUGS.keys()))
    drug = random.choice(LUPUS_DRUGS[drug_class])
    comparator = random.choice(['placebo', 'placebo', 'standard of care'])

    treatment_n, control_n = generate_sample_sizes()
    total_n = treatment_n + control_n

    if is_ln:
        outcome = random.choice(['complete renal response', 'partial renal response', 'overall renal response'])
        disease = 'lupus nephritis'
    else:
        outcome = random.choice(['SRI-4', 'BICLA', 'SRI-6', 'flare reduction'])
        disease = 'systemic lupus erythematosus'

    age = round(random.uniform(32, 45), 1)
    female_pct = round(random.uniform(88, 96), 1)
    disease_duration = round(random.uniform(4, 12), 1)
    sledai = round(random.uniform(8, 14), 1)

    treatment_rate, control_rate = generate_response_rate()
    rr, rr_lo, rr_hi = generate_rr()

    followup_weeks = random.choice([52, 76, 104])
    year = random.randint(2017, 2024)

    nct = generate_nct()
    acronym = generate_acronym('LUPUS', drug_class, index)
    trial_id = generate_trial_id('LUPUS', index)

    dose = random.choice(['10 mg/kg', '200 mg', '400 mg', '23.4 mg'])
    frequency = random.choice(['every 4 weeks', 'twice daily', 'weekly', 'every 2 weeks'])

    sites = random.randint(80, 200)
    countries = random.randint(15, 35)

    text = f"""{acronym} Trial: {drug.title()} in {disease.title()}

This was a randomized, double-blind, {comparator}-controlled, phase 3 trial at {sites} sites across {countries} countries.
We enrolled {total_n} patients with active {disease} despite standard therapy.

Patients were randomly assigned to {drug} {dose} {frequency} plus standard of care ({treatment_n} patients, treatment arm, n={treatment_n})
or {comparator} plus standard of care ({control_n} patients, control arm, n={control_n}).

Mean age was {age} years, {female_pct}% were female. Mean disease duration was {disease_duration} years.
Mean SLEDAI-2K score at baseline was {sledai}. {round(random.uniform(30, 55), 1)}% had prior biologic use.

The primary endpoint was {outcome} at week {followup_weeks}. Response rates were {treatment_rate}% with {drug}
versus {control_rate}% with {comparator} (RR {rr}; 95% CI {rr_lo}-{rr_hi}; P<0.001).

Severe flare rate: {round(random.uniform(8, 18), 1)}% vs {round(random.uniform(15, 28), 1)}% (P<0.01).
Steroid dose reduction to ≤7.5 mg/day: {round(treatment_rate * 0.6, 1)}% vs {round(control_rate * 0.7, 1)}%.

Change in SLEDAI-2K from baseline: -{round(random.uniform(4, 8), 1)} vs -{round(random.uniform(2, 5), 1)} points.

Serious adverse events: {round(random.uniform(12, 22), 1)}% vs {round(random.uniform(14, 25), 1)}%.
Serious infections: {round(random.uniform(4, 9), 1)}% vs {round(random.uniform(5, 10), 1)}%.

Trial registration: {nct}."""

    ground_truth = {
        'study': {'acronym': acronym},
        'treatment': {'n': treatment_n, 'name': drug},
        'control': {'n': control_n, 'name': comparator},
        'totalN': total_n,
        'primaryEffect': {'type': 'RR', 'value': rr, 'ciLo': rr_lo, 'ciHi': rr_hi},
        'baseline': {
            'ageMean': age,
            'femalePercent': female_pct,
            'sledai': sledai
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': generate_citation(year),
        'domain': 'Rheumatology',
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

# Generate Ankylosing Spondylitis trial
def generate_as_trial(index):
    is_nraxspa = random.random() < 0.3  # Non-radiographic axial SpA
    drug_class = random.choice(list(AS_DRUGS.keys()))
    drug = random.choice(AS_DRUGS[drug_class])
    comparator = random.choice(['placebo', 'placebo', 'placebo', 'adalimumab'])

    treatment_n, control_n = generate_sample_sizes()
    total_n = treatment_n + control_n

    outcome = random.choice(AS_OUTCOMES[:5])
    disease = 'non-radiographic axial spondyloarthritis' if is_nraxspa else 'ankylosing spondylitis'

    age = round(random.uniform(38, 48), 1)
    male_pct = round(random.uniform(58, 78), 1)
    disease_duration = round(random.uniform(5, 15), 1)
    hla_b27_pos = round(random.uniform(75, 95), 1)
    basdai = round(random.uniform(6.2, 7.8), 1)

    treatment_rate, control_rate = generate_response_rate()
    rr, rr_lo, rr_hi = generate_rr()

    asdas_md, asdas_lo, asdas_hi = generate_md('ASDAS-CRP')

    followup_weeks = random.choice([12, 16, 24, 52])
    year = random.randint(2016, 2024)

    nct = generate_nct()
    acronym = generate_acronym('AS', drug_class, index)
    trial_id = generate_trial_id('AS', index)

    dose = random.choice(['15 mg', '75 mg', '150 mg', '300 mg'])
    frequency = random.choice(['once daily', 'every 4 weeks', 'every 2 weeks'])

    sites = random.randint(60, 180)
    countries = random.randint(10, 25)

    text = f"""{acronym} Trial: {drug.title()} in {disease.title()}

This was a randomized, double-blind, {comparator}-controlled, phase 3 trial at {sites} sites in {countries} countries.
We enrolled {total_n} adults with active {disease} who had inadequate response to NSAIDs.

Patients were randomly assigned to {drug} {dose} {frequency} ({treatment_n} patients, treatment arm, n={treatment_n})
or {comparator} ({control_n} patients, control arm, n={control_n}).

Mean age was {age} years, {male_pct}% were male. Mean disease duration was {disease_duration} years.
{hla_b27_pos}% were HLA-B27 positive. Mean BASDAI was {basdai}.

The primary endpoint was {outcome} response at week {followup_weeks}. {outcome} was achieved by {treatment_rate}%
in the {drug} group versus {control_rate}% in the {comparator} group
(RR {rr}; 95% CI {rr_lo}-{rr_hi}; P<0.001).

Change in ASDAS-CRP: {drug} {asdas_md} vs {comparator} {round(asdas_md * 0.4, 2)}
(MD {asdas_md}; 95% CI {asdas_lo}-{asdas_hi}).

BASDAI50 response: {round(treatment_rate * 0.85, 1)}% vs {round(control_rate * 0.6, 1)}%.
ASDAS inactive disease (<1.3): {round(treatment_rate * 0.35, 1)}% vs {round(control_rate * 0.15, 1)}%.

MRI SPARCC spine score change: -{round(random.uniform(5, 15), 1)} vs -{round(random.uniform(0.5, 3), 1)}.

Adverse events: {round(random.uniform(50, 70), 1)}% vs {round(random.uniform(45, 60), 1)}%.
Serious adverse events: {round(random.uniform(2, 7), 1)}% vs {round(random.uniform(2, 5), 1)}%.

Trial registration: {nct}."""

    ground_truth = {
        'study': {'acronym': acronym},
        'treatment': {'n': treatment_n, 'name': drug},
        'control': {'n': control_n, 'name': comparator},
        'totalN': total_n,
        'primaryEffect': {'type': 'RR', 'value': rr, 'ciLo': rr_lo, 'ciHi': rr_hi},
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct,
            'basdai': basdai
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': generate_citation(year),
        'domain': 'Rheumatology',
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

# Generate Atopic Dermatitis trial
def generate_ad_trial(index):
    drug_class = random.choice(list(AD_DRUGS.keys()))
    drug = random.choice(AD_DRUGS[drug_class])
    comparator = random.choice(['placebo', 'placebo', 'placebo', 'dupilumab'])

    treatment_n, control_n = generate_sample_sizes()
    total_n = treatment_n + control_n

    outcome = random.choice(AD_OUTCOMES[:4])

    age = round(random.uniform(32, 45), 1)
    male_pct = round(random.uniform(45, 58), 1)
    easi_baseline = round(random.uniform(25, 40), 1)
    bsa = round(random.uniform(40, 70), 1)
    pruritus_baseline = round(random.uniform(6.5, 8.5), 1)

    treatment_rate, control_rate = generate_response_rate()
    rr, rr_lo, rr_hi = generate_rr()

    easi_md, easi_lo, easi_hi = generate_md('EASI')

    followup_weeks = random.choice([12, 16, 24, 52])
    year = random.randint(2018, 2024)

    nct = generate_nct()
    acronym = generate_acronym('AD', drug_class, index)
    trial_id = generate_trial_id('AD', index)

    dose = random.choice(['100 mg', '200 mg', '300 mg', '400 mg'])
    frequency = random.choice(['once daily', 'twice daily', 'every 2 weeks'])

    sites = random.randint(80, 250)
    countries = random.randint(12, 30)

    text = f"""{acronym} Trial: {drug.title()} for Moderate-to-Severe Atopic Dermatitis

This was a randomized, double-blind, {comparator}-controlled, phase 3 trial at {sites} sites in {countries} countries.
We enrolled {total_n} adults with moderate-to-severe atopic dermatitis inadequately controlled with topical therapy.

Patients were randomly assigned to {drug} {dose} {frequency} ({treatment_n} patients, treatment arm, n={treatment_n})
or {comparator} ({control_n} patients, control arm, n={control_n}). Topical corticosteroids were permitted.

Mean age was {age} years, {male_pct}% were male. Mean EASI score at baseline was {easi_baseline}.
Mean body surface area affected was {bsa}%. Mean peak pruritus NRS was {pruritus_baseline}.

The primary endpoint was {outcome} at week {followup_weeks}. {outcome} was achieved by {treatment_rate}%
in the {drug} group versus {control_rate}% in the {comparator} group
(RR {rr}; 95% CI {rr_lo}-{rr_hi}; P<0.001).

EASI percent change from baseline: {round(random.uniform(-75, -55), 1)}% vs {round(random.uniform(-25, -10), 1)}%
(MD {easi_md}; 95% CI {easi_lo}-{easi_hi}).

Peak pruritus NRS improvement ≥4 points: {round(treatment_rate * 0.75, 1)}% vs {round(control_rate * 0.4, 1)}%.
IGA 0/1: {round(treatment_rate * 0.55, 1)}% vs {round(control_rate * 0.3, 1)}%.
DLQI improvement: -{round(random.uniform(8, 14), 1)} vs -{round(random.uniform(2, 5), 1)} points.

Adverse events: {round(random.uniform(55, 75), 1)}% vs {round(random.uniform(50, 65), 1)}%.
Conjunctivitis: {round(random.uniform(3, 12), 1)}% vs {round(random.uniform(1, 4), 1)}%.
Nasopharyngitis: {round(random.uniform(8, 18), 1)}% vs {round(random.uniform(6, 12), 1)}%.

Trial registration: {nct}."""

    ground_truth = {
        'study': {'acronym': acronym},
        'treatment': {'n': treatment_n, 'name': drug},
        'control': {'n': control_n, 'name': comparator},
        'totalN': total_n,
        'primaryEffect': {'type': 'RR', 'value': rr, 'ciLo': rr_lo, 'ciHi': rr_hi},
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct,
            'easi': easi_baseline
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': generate_citation(year),
        'domain': 'Dermatology',
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

# Generate Other Autoimmune trial (MS, MG, Vasculitis)
def generate_auto_trial(index):
    disease_type = random.choice(['MS', 'MG', 'VASC', 'SSC', 'SJOGREN'])
    drug = random.choice(AUTO_DRUGS[disease_type])
    comparator = random.choice(['placebo', 'placebo', 'interferon beta-1a', 'standard care'])

    treatment_n, control_n = generate_sample_sizes()
    total_n = treatment_n + control_n

    outcome = random.choice(AUTO_OUTCOMES[disease_type])

    if disease_type == 'MS':
        disease = 'relapsing multiple sclerosis'
        age = round(random.uniform(35, 45), 1)
        female_pct = round(random.uniform(65, 75), 1)
        domain = 'Neurology'
    elif disease_type == 'MG':
        disease = 'generalized myasthenia gravis'
        age = round(random.uniform(45, 58), 1)
        female_pct = round(random.uniform(55, 68), 1)
        domain = 'Neurology'
    elif disease_type == 'VASC':
        disease = random.choice(['ANCA-associated vasculitis', 'giant cell arteritis', 'Takayasu arteritis'])
        age = round(random.uniform(55, 68), 1)
        female_pct = round(random.uniform(45, 65), 1)
        domain = 'Rheumatology'
    elif disease_type == 'SSC':
        disease = 'systemic sclerosis'
        age = round(random.uniform(48, 58), 1)
        female_pct = round(random.uniform(78, 88), 1)
        domain = 'Rheumatology'
    else:  # SJOGREN
        disease = "Sjogren's syndrome"
        age = round(random.uniform(48, 58), 1)
        female_pct = round(random.uniform(88, 95), 1)
        domain = 'Rheumatology'

    treatment_rate, control_rate = generate_response_rate()
    rr, rr_lo, rr_hi = generate_rr()

    followup_weeks = random.choice([24, 48, 52, 96, 104])
    year = random.randint(2017, 2024)

    nct = generate_nct()
    acronym = generate_acronym('AUTO', disease_type, index)
    trial_id = generate_trial_id('AUTO', index)

    dose = random.choice(['10 mg', '20 mg', '300 mg', '600 mg', '900 mg', '1200 mg'])
    frequency = random.choice(['once daily', 'every 4 weeks', 'every 6 months', 'every 2 weeks'])

    sites = random.randint(60, 200)
    countries = random.randint(10, 30)

    # Disease-specific text
    if disease_type == 'MS':
        specific_outcome = f"""Annualized relapse rate: {round(random.uniform(0.08, 0.18), 2)} vs {round(random.uniform(0.22, 0.35), 2)} (rate ratio {round(random.uniform(0.35, 0.55), 2)}).
Confirmed disability progression at 12 weeks: {round(random.uniform(8, 15), 1)}% vs {round(random.uniform(12, 22), 1)}%.
New or enlarging T2 lesions: {round(random.uniform(0.3, 1.2), 1)} vs {round(random.uniform(3, 8), 1)} mean number."""
    elif disease_type == 'MG':
        specific_outcome = f"""MG-ADL score change: -{round(random.uniform(3, 6), 1)} vs -{round(random.uniform(0.5, 2), 1)} points (P<0.001).
QMG score improvement: -{round(random.uniform(4, 8), 1)} vs -{round(random.uniform(1, 3), 1)} points.
Clinical improvement (≥3-point MG-ADL reduction): {treatment_rate}% vs {control_rate}%."""
    else:
        specific_outcome = f"""Primary endpoint ({outcome}): {treatment_rate}% vs {control_rate}% (RR {rr}; 95% CI {rr_lo}-{rr_hi}).
Sustained remission: {round(treatment_rate * 0.7, 1)}% vs {round(control_rate * 0.5, 1)}%.
Glucocorticoid-free remission: {round(treatment_rate * 0.5, 1)}% vs {round(control_rate * 0.25, 1)}%."""

    text = f"""{acronym} Trial: {drug.title()} in {disease.title()}

This was a randomized, double-blind, {comparator}-controlled, phase 3 trial at {sites} sites in {countries} countries.
We enrolled {total_n} patients with {disease}.

Patients were randomly assigned to {drug} {dose} {frequency} ({treatment_n} patients, treatment arm, n={treatment_n})
or {comparator} ({control_n} patients, control arm, n={control_n}).

Mean age was {age} years, {female_pct}% were female. Mean disease duration was {round(random.uniform(3, 12), 1)} years.

Primary analysis at week {followup_weeks}:
{specific_outcome}

Overall response rate: {treatment_rate}% vs {control_rate}%
(RR {rr}; 95% CI {rr_lo}-{rr_hi}; P<0.001).

Serious adverse events: {round(random.uniform(8, 18), 1)}% vs {round(random.uniform(10, 20), 1)}%.
Infusion/injection reactions: {round(random.uniform(5, 20), 1)}% vs {round(random.uniform(2, 8), 1)}%.
Serious infections: {round(random.uniform(2, 7), 1)}% vs {round(random.uniform(2, 6), 1)}%.

Trial registration: {nct}."""

    ground_truth = {
        'study': {'acronym': acronym},
        'treatment': {'n': treatment_n, 'name': drug},
        'control': {'n': control_n, 'name': comparator},
        'totalN': total_n,
        'primaryEffect': {'type': 'RR', 'value': rr, 'ciLo': rr_lo, 'ciHi': rr_hi},
        'baseline': {
            'ageMean': age,
            'femalePercent': female_pct
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': generate_citation(year),
        'domain': domain,
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

def format_trial_js(trial):
    """Format a trial as JavaScript object string"""
    gt = trial['groundTruth']

    # Format groundTruth object
    gt_parts = []
    gt_parts.append(f"            study: {{ acronym: '{gt['study']['acronym']}' }}")
    gt_parts.append(f"            treatment: {{ n: {gt['treatment']['n']}, name: '{gt['treatment']['name']}' }}")
    gt_parts.append(f"            control: {{ n: {gt['control']['n']}, name: '{gt['control']['name']}' }}")
    gt_parts.append(f"            totalN: {gt['totalN']}")
    gt_parts.append(f"            primaryEffect: {{ type: '{gt['primaryEffect']['type']}', value: {gt['primaryEffect']['value']}, ciLo: {gt['primaryEffect']['ciLo']}, ciHi: {gt['primaryEffect']['ciHi']} }}")

    # Baseline
    bl = gt['baseline']
    bl_items = []
    for k, v in bl.items():
        bl_items.append(f"{k}: {v}")
    gt_parts.append(f"            baseline: {{ {', '.join(bl_items)} }}")

    # Follow-up
    if 'followupWeeks' in gt:
        gt_parts.append(f"            followupWeeks: {gt['followupWeeks']}")
    if 'inductionWeeks' in gt:
        gt_parts.append(f"            inductionWeeks: {gt['inductionWeeks']}")
    if 'maintenanceWeeks' in gt:
        gt_parts.append(f"            maintenanceWeeks: {gt['maintenanceWeeks']}")

    gt_parts.append(f"            registration: '{gt['registration']}'")
    gt_parts.append(f"            fundingIndustry: {str(gt['fundingIndustry']).lower()}")

    gt_str = ',\n'.join(gt_parts)

    # Escape backticks and special characters in text
    text_escaped = trial['text'].replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

    js = f"""    {{
        id: '{trial['id']}',
        source: '{trial['source']}',
        domain: '{trial['domain']}',
        design: '{trial['design']}',
        text: `{text_escaped}`,

        groundTruth: {{
{gt_str}
        }}
    }}"""

    return js

def main():
    print("Generating 1000 Inflammatory/Autoimmune RCT trials...")

    all_trials = []

    # Generate trials by category
    print("Generating 200 Rheumatoid Arthritis trials...")
    for i in range(1, 201):
        all_trials.append(generate_ra_trial(i))

    print("Generating 150 Psoriasis/PsA trials...")
    for i in range(1, 151):
        all_trials.append(generate_pso_trial(i))

    print("Generating 150 IBD trials...")
    for i in range(1, 151):
        all_trials.append(generate_ibd_trial(i))

    print("Generating 100 Lupus/CTD trials...")
    for i in range(1, 101):
        all_trials.append(generate_lupus_trial(i))

    print("Generating 100 Ankylosing Spondylitis trials...")
    for i in range(1, 101):
        all_trials.append(generate_as_trial(i))

    print("Generating 150 Atopic Dermatitis trials...")
    for i in range(1, 151):
        all_trials.append(generate_ad_trial(i))

    print("Generating 150 Other Autoimmune trials...")
    for i in range(1, 151):
        all_trials.append(generate_auto_trial(i))

    print(f"\nTotal trials generated: {len(all_trials)}")

    # Read existing file
    print(f"\nReading {TARGET_FILE}...")
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the position to insert (before the closing bracket and semicolon)
    # Look for the last occurrence of "}," followed by "];" or similar pattern

    # Find the position just before the final ];
    insert_pos = content.rfind('];')
    if insert_pos == -1:
        insert_pos = content.rfind(']')

    if insert_pos == -1:
        print("ERROR: Could not find insertion point in file")
        return

    # Find the position after the last trial entry
    last_brace = content.rfind('}', 0, insert_pos)

    # Format all trials
    print("Formatting trials as JavaScript...")
    trial_strings = [format_trial_js(t) for t in all_trials]

    # Create the new content
    new_trials_str = ',\n' + ',\n'.join(trial_strings)

    # Insert new trials
    new_content = content[:last_brace+1] + new_trials_str + content[last_brace+1:]

    # Write back
    print(f"Writing to {TARGET_FILE}...")
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("\nDone! 1000 inflammatory/autoimmune trials added successfully.")
    print("\nBreakdown:")
    print("  - Rheumatoid Arthritis (IMMUN-RA-001 to IMMUN-RA-200): 200 trials")
    print("  - Psoriasis/PsA (IMMUN-PSO-001 to IMMUN-PSO-150): 150 trials")
    print("  - IBD (IMMUN-IBD-001 to IMMUN-IBD-150): 150 trials")
    print("  - Lupus/CTD (IMMUN-LUPUS-001 to IMMUN-LUPUS-100): 100 trials")
    print("  - Ankylosing Spondylitis (IMMUN-AS-001 to IMMUN-AS-100): 100 trials")
    print("  - Atopic Dermatitis (IMMUN-AD-001 to IMMUN-AD-150): 150 trials")
    print("  - Other Autoimmune (IMMUN-AUTO-001 to IMMUN-AUTO-150): 150 trials")

if __name__ == '__main__':
    main()
