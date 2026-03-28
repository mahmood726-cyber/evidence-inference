#!/usr/bin/env python3
"""
Batch generator for 1000 Metabolic/Endocrine RCT trials
Appends to validation_study_expanded.js
"""

import random
import os

# Set seed for reproducibility
random.seed(42)

# Target file
TARGET_FILE = "C:/Users/user/Downloads/Dataextractor/validation_study_expanded.js"

# Trial categories and counts
CATEGORIES = {
    'T2D': 300,      # Type 2 Diabetes
    'OBS': 200,      # Obesity
    'OST': 150,      # Osteoporosis
    'THY': 100,      # Thyroid
    'LIP': 150,      # Lipid disorders
    'OTH': 100       # Other endocrine
}

# Drug classes by category
DRUGS = {
    'T2D': {
        'GLP1': ['semaglutide', 'liraglutide', 'dulaglutide', 'exenatide', 'lixisenatide', 'albiglutide'],
        'SGLT2': ['empagliflozin', 'dapagliflozin', 'canagliflozin', 'ertugliflozin', 'sotagliflozin'],
        'INSULIN': ['insulin glargine', 'insulin degludec', 'insulin detemir', 'insulin aspart', 'insulin lispro'],
        'DPP4': ['sitagliptin', 'saxagliptin', 'linagliptin', 'alogliptin', 'vildagliptin'],
        'TZD': ['pioglitazone', 'rosiglitazone'],
        'METFORMIN': ['metformin XR', 'metformin IR']
    },
    'OBS': {
        'GLP1': ['semaglutide 2.4mg', 'liraglutide 3.0mg'],
        'DUAL': ['tirzepatide', 'retatrutide', 'survodutide'],
        'OTHER': ['orlistat', 'phentermine-topiramate', 'naltrexone-bupropion', 'setmelanotide']
    },
    'OST': {
        'BISPHOS': ['alendronate', 'risedronate', 'ibandronate', 'zoledronic acid'],
        'DENOS': ['denosumab'],
        'ROMO': ['romosozumab'],
        'TERIPAR': ['teriparatide', 'abaloparatide'],
        'SERM': ['raloxifene', 'bazedoxifene']
    },
    'THY': {
        'HYPER': ['methimazole', 'propylthiouracil', 'radioactive iodine', 'propranolol'],
        'HYPO': ['levothyroxine', 'liothyronine', 'desiccated thyroid'],
        'NODULE': ['ethanol ablation', 'radiofrequency ablation', 'levothyroxine suppression']
    },
    'LIP': {
        'PCSK9': ['evolocumab', 'alirocumab', 'inclisiran'],
        'STATIN': ['atorvastatin', 'rosuvastatin', 'simvastatin', 'pravastatin', 'pitavastatin'],
        'BEMP': ['bempedoic acid', 'bempedoic acid/ezetimibe'],
        'OTHER': ['ezetimibe', 'icosapent ethyl', 'fenofibrate', 'lomitapide', 'evinacumab']
    },
    'OTH': {
        'ADRENAL': ['hydrocortisone', 'fludrocortisone', 'mitotane', 'osilodrostat', 'levoketoconazole'],
        'PITUITARY': ['pegvisomant', 'pasireotide', 'cabergoline', 'bromocriptine', 'lanreotide'],
        'PCOS': ['metformin', 'spironolactone', 'letrozole', 'clomiphene', 'inositol'],
        'HYPOPARA': ['recombinant PTH', 'calcium/vitamin D', 'thiazide diuretics']
    }
}

# Comparators
COMPARATORS = {
    'T2D': ['placebo', 'sitagliptin', 'glimepiride', 'insulin glargine', 'metformin', 'standard care'],
    'OBS': ['placebo', 'lifestyle intervention', 'diet alone', 'orlistat'],
    'OST': ['placebo', 'alendronate', 'calcium/vitamin D', 'standard care'],
    'THY': ['placebo', 'standard care', 'propranolol alone', 'levothyroxine'],
    'LIP': ['placebo', 'ezetimibe', 'standard statin therapy', 'atorvastatin 10mg'],
    'OTH': ['placebo', 'standard care', 'observation', 'lifestyle modification']
}

# Journals
JOURNALS = [
    'N Engl J Med', 'Lancet', 'JAMA', 'Lancet Diabetes Endocrinol',
    'Diabetes Care', 'Diabetologia', 'J Clin Endocrinol Metab',
    'Obesity', 'Int J Obes', 'J Bone Miner Res', 'Osteoporos Int',
    'Thyroid', 'Eur J Endocrinol', 'Endocr Rev', 'J Lipid Res',
    'Atherosclerosis', 'Circulation', 'Eur Heart J', 'Ann Intern Med',
    'BMJ', 'JAMA Intern Med', 'Diabetes Obes Metab'
]

# Author last names
LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
    'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
    'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
    'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
    'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
    'Carter', 'Roberts', 'Muller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer',
    'Wagner', 'Becker', 'Schulz', 'Hoffmann', 'Schaefer', 'Koch', 'Bauer', 'Richter',
    'Klein', 'Wolf', 'Schroeder', 'Neumann', 'Schwarz', 'Zimmermann', 'Braun', 'Kruger',
    'Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci',
    'Marino', 'Greco', 'Bruno', 'Gallo', 'Conti', 'DeLuca', 'Mancini', 'Costa',
    'Yamamoto', 'Tanaka', 'Suzuki', 'Watanabe', 'Ito', 'Nakamura', 'Kobayashi', 'Kato',
    'Chen', 'Wang', 'Zhang', 'Liu', 'Yang', 'Huang', 'Wu', 'Zhou', 'Xu', 'Sun',
    'Patel', 'Shah', 'Kumar', 'Singh', 'Sharma', 'Gupta', 'Mehta', 'Joshi', 'Rao'
]

# Trial name prefixes by category
TRIAL_PREFIXES = {
    'T2D': ['SUSTAIN', 'PIONEER', 'AWARD', 'HARMONY', 'CANVAS', 'CREDENCE', 'VERTIS',
            'GRADE', 'ORIGIN', 'DEVOTE', 'LEADER', 'REWIND', 'EXSCEL', 'CAROLINA',
            'TECOS', 'SAVOR', 'EXAMINE', 'ELIXA', 'SURPASS', 'AMPLITUDE', 'BRIGHT',
            'BEGIN', 'EDITION', 'SWITCH', 'ONSET', 'STEP-D', 'DURATION', 'LIBERATE'],
    'OBS': ['STEP', 'SCALE', 'SURMOUNT', 'ACTION', 'OASIS', 'CONQUER', 'BLOOM',
            'MOMENTUM', 'TRIUMPH', 'ASPIRE', 'SEQUEL', 'EMERGE', 'HORIZON', 'ACHIEVE'],
    'OST': ['FREEDOM', 'ARCH', 'FRAME', 'BRIDGE', 'VERO', 'ACTIVE', 'HORIZON',
            'BONE', 'FORTEO', 'TYMLOS', 'STRUCTURE', 'FOUNDATION', 'CORE', 'SOLID'],
    'THY': ['CATALYST', 'LIBERTY', 'TRUTH', 'GRAVES', 'THRIVE', 'RESTORE', 'BALANCE',
            'OPTIMAL', 'THYROID', 'CALM', 'RELIEF', 'STEADY', 'NORM', 'REGAIN'],
    'LIP': ['FOURIER', 'ODYSSEY', 'ORION', 'CLEAR', 'GAUSS', 'DESCARTES', 'TESLA',
            'LAPLACE', 'NEWTON', 'MENDEL', 'RUTHERFORD', 'OSLER', 'GLAGOV', 'REDUCE'],
    'OTH': ['ACRO', 'CLARITY', 'CUSHING', 'OPTIMA', 'ADRENAL', 'PITUITARY', 'ENDO',
            'HARMONY', 'BALANCE', 'RESTORE', 'REGULATE', 'CONTROL', 'MANAGE', 'CARE']
}

# Institutions
INSTITUTIONS = [
    'Harvard Medical School', 'Stanford University', 'Johns Hopkins University',
    'Mayo Clinic', 'Cleveland Clinic', 'Massachusetts General Hospital',
    'UCLA Medical Center', 'UCSF Medical Center', 'Duke University Medical Center',
    'University of Pennsylvania', 'Columbia University', 'Yale School of Medicine',
    'University of Michigan', 'University of Chicago', 'Northwestern University',
    'University of Pittsburgh', 'Vanderbilt University', 'Emory University',
    'University of Toronto', 'McGill University', 'University of Oxford',
    'University of Cambridge', 'Imperial College London', 'Kings College London',
    'Karolinska Institute', 'University of Copenhagen', 'University of Amsterdam',
    'Charite Berlin', 'University of Munich', 'University of Heidelberg',
    'University of Sydney', 'University of Melbourne', 'University of Tokyo',
    'Peking University', 'Seoul National University', 'National University of Singapore'
]

# Funding sources
FUNDERS = {
    'T2D': ['Novo Nordisk', 'Eli Lilly', 'Sanofi', 'AstraZeneca', 'Boehringer Ingelheim',
            'Merck', 'Takeda', 'Janssen', 'Bristol-Myers Squibb'],
    'OBS': ['Novo Nordisk', 'Eli Lilly', 'Rhythm Pharmaceuticals', 'Vivus'],
    'OST': ['Amgen', 'UCB', 'Radius Health', 'Pfizer', 'Merck'],
    'THY': ['Merck', 'AbbVie', 'Pfizer', 'Genzyme', 'Recordati'],
    'LIP': ['Amgen', 'Regeneron', 'Sanofi', 'Novartis', 'Esperion', 'Pfizer', 'AstraZeneca'],
    'OTH': ['Pfizer', 'Novartis', 'Recordati', 'HRA Pharma', 'Crinetics', 'Xeris']
}

def generate_nct():
    """Generate unique NCT number"""
    return f"NCT{random.randint(10000000, 99999999):08d}"

def generate_author():
    """Generate author citation"""
    author = random.choice(LAST_NAMES)
    year = random.randint(2015, 2024)
    journal = random.choice(JOURNALS)
    vol = random.randint(300, 450)
    page1 = random.randint(100, 2000)
    page2 = page1 + random.randint(8, 15)
    return f"{author} et al. {journal} {year};{vol}:{page1}-{page2}"

def generate_t2d_trial(idx):
    """Generate Type 2 Diabetes trial"""
    drug_class = random.choice(list(DRUGS['T2D'].keys()))
    drug = random.choice(DRUGS['T2D'][drug_class])
    comparator = random.choice(COMPARATORS['T2D'])

    # Sample sizes
    n_treatment = random.randint(150, 2500)
    n_control = random.randint(150, 2500)
    total_n = n_treatment + n_control

    # Demographics
    age = round(random.uniform(52, 68), 1)
    male_pct = round(random.uniform(45, 65), 1)
    bmi = round(random.uniform(28, 38), 1)
    hba1c_base = round(random.uniform(7.5, 10.0), 1)
    diabetes_duration = round(random.uniform(5, 15), 1)

    # Outcomes - HbA1c reduction
    hba1c_reduction = round(random.uniform(-1.5, -0.5), 2)
    hba1c_ci_lo = round(hba1c_reduction - random.uniform(0.1, 0.3), 2)
    hba1c_ci_hi = round(hba1c_reduction + random.uniform(0.1, 0.3), 2)

    # Weight change
    weight_change = round(random.uniform(-8, -1), 1)

    # Follow-up
    followup_weeks = random.choice([24, 26, 52, 56, 78, 104])

    # Generate trial name
    prefix = random.choice(TRIAL_PREFIXES['T2D'])
    suffix = random.choice(['', '-1', '-2', '-3', '-4', '-5', '-6', '-7', '-8', '-EXT', '-PLUS', '-CV', '-RENAL'])
    trial_name = f"{prefix}{suffix}"

    trial_id = f"ENDO-T2D-{idx:03d}"
    nct = generate_nct()
    source = generate_author()
    funder = random.choice(FUNDERS['T2D'])
    institution = random.choice(INSTITUTIONS)
    sites = random.randint(50, 500)
    countries = random.randint(10, 40)

    text = f"""{trial_name} Trial: {drug.title()} versus {comparator.title()} in Type 2 Diabetes

This was a randomized, double-blind, {random.choice(['placebo-controlled', 'active-controlled', 'parallel-group'])} trial conducted at {sites} sites across {countries} countries. We enrolled {total_n} patients with type 2 diabetes inadequately controlled on {random.choice(['metformin alone', 'metformin plus sulfonylurea', 'oral antidiabetic agents', 'basal insulin'])}.

Patients were randomly assigned to receive {drug} (treatment arm, n={n_treatment}) or {comparator} (control arm, n={n_control}).

Baseline characteristics: Mean age was {age} years (SD {round(random.uniform(8, 12), 1)}), {male_pct}% were male. Mean BMI was {bmi} kg/m2. Mean baseline HbA1c was {hba1c_base}% (SD {round(random.uniform(0.8, 1.2), 1)}). Mean diabetes duration was {diabetes_duration} years.

The primary endpoint was change in HbA1c from baseline to week {followup_weeks}. The {drug} group achieved a mean HbA1c reduction of {hba1c_reduction}% (95% CI {hba1c_ci_lo}-{hba1c_ci_hi}) compared with {comparator} (P<0.001).

Secondary outcomes: Mean weight change was {weight_change} kg with {drug}. {round(random.uniform(30, 70), 1)}% of patients achieved HbA1c <7.0%.

The study duration was {followup_weeks} weeks. Trial registration: {nct}. Funded by {funder}. Conducted by {institution}."""

    ground_truth = {
        'study': {'acronym': trial_name},
        'treatment': {'n': n_treatment},
        'control': {'n': n_control},
        'totalN': total_n,
        'primaryEffect': {
            'type': 'MD',
            'value': hba1c_reduction,
            'ciLo': hba1c_ci_lo,
            'ciHi': hba1c_ci_hi
        },
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct,
            'bmi': bmi,
            'hba1c': hba1c_base
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': source,
        'domain': 'Endocrinology/Diabetes',
        'design': random.choice(['Superiority', 'Non-inferiority']),
        'text': text,
        'groundTruth': ground_truth
    }

def generate_obesity_trial(idx):
    """Generate Obesity trial"""
    drug_class = random.choice(list(DRUGS['OBS'].keys()))
    drug = random.choice(DRUGS['OBS'][drug_class])
    comparator = random.choice(COMPARATORS['OBS'])

    n_treatment = random.randint(200, 1500)
    n_control = random.randint(200, 1500)
    total_n = n_treatment + n_control

    age = round(random.uniform(40, 58), 1)
    male_pct = round(random.uniform(25, 45), 1)
    bmi_base = round(random.uniform(32, 45), 1)
    weight_base = round(random.uniform(95, 130), 1)

    # Weight loss percentage
    weight_loss_pct = round(random.uniform(-22, -8), 1)
    weight_loss_ci_lo = round(weight_loss_pct - random.uniform(1, 3), 1)
    weight_loss_ci_hi = round(weight_loss_pct + random.uniform(1, 3), 1)

    followup_weeks = random.choice([52, 68, 72, 104])

    prefix = random.choice(TRIAL_PREFIXES['OBS'])
    suffix = random.choice(['', '-1', '-2', '-3', '-4', '-5', '-HFpEF', '-NASH', '-OSA', '-T2D'])
    trial_name = f"{prefix}{suffix}"

    trial_id = f"ENDO-OBS-{idx:03d}"
    nct = generate_nct()
    source = generate_author()
    funder = random.choice(FUNDERS['OBS'])
    institution = random.choice(INSTITUTIONS)
    sites = random.randint(40, 200)
    countries = random.randint(8, 25)

    text = f"""{trial_name} Trial: {drug.title()} for Weight Management in Obesity

This was a randomized, double-blind, placebo-controlled trial conducted at {sites} sites in {countries} countries. We enrolled {total_n} adults with obesity (BMI >=30 kg/m2) or overweight (BMI >=27 kg/m2) with at least one weight-related comorbidity.

Patients were randomly assigned to receive {drug} plus lifestyle intervention (treatment arm, n={n_treatment}) or {comparator} plus lifestyle intervention (control arm, n={n_control}).

Baseline characteristics: Mean age was {age} years (SD {round(random.uniform(10, 14), 1)}), {male_pct}% were male. Mean baseline BMI was {bmi_base} kg/m2. Mean baseline body weight was {weight_base} kg.

The co-primary endpoints were percentage change in body weight and proportion achieving >=5% weight loss at week {followup_weeks}. The {drug} group achieved a mean weight reduction of {weight_loss_pct}% (95% CI {weight_loss_ci_lo}-{weight_loss_ci_hi}) versus {round(random.uniform(-3, -1), 1)}% with {comparator} (P<0.001).

{round(random.uniform(75, 92), 1)}% of patients on {drug} achieved >=5% weight loss, and {round(random.uniform(45, 70), 1)}% achieved >=10% weight loss.

Improvements were also seen in waist circumference ({round(random.uniform(-10, -5), 1)} cm), systolic blood pressure ({round(random.uniform(-8, -3), 1)} mmHg), and lipid parameters.

Study duration was {followup_weeks} weeks. Trial registration: {nct}. Funded by {funder}."""

    ground_truth = {
        'study': {'acronym': trial_name},
        'treatment': {'n': n_treatment},
        'control': {'n': n_control},
        'totalN': total_n,
        'primaryEffect': {
            'type': 'MD',
            'value': weight_loss_pct,
            'ciLo': weight_loss_ci_lo,
            'ciHi': weight_loss_ci_hi,
            'unit': 'percent'
        },
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct,
            'bmi': bmi_base,
            'weightKg': weight_base
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': source,
        'domain': 'Endocrinology/Obesity',
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

def generate_osteoporosis_trial(idx):
    """Generate Osteoporosis trial"""
    drug_class = random.choice(list(DRUGS['OST'].keys()))
    drug = random.choice(DRUGS['OST'][drug_class])
    comparator = random.choice(COMPARATORS['OST'])

    n_treatment = random.randint(500, 4000)
    n_control = random.randint(500, 4000)
    total_n = n_treatment + n_control

    age = round(random.uniform(65, 78), 1)
    male_pct = round(random.uniform(0, 25), 1)  # Mostly female
    tscore_spine = round(random.uniform(-3.5, -2.0), 1)
    tscore_hip = round(random.uniform(-3.0, -1.8), 1)

    # Fracture reduction (HR)
    hr_fracture = round(random.uniform(0.30, 0.75), 2)
    hr_ci_lo = round(hr_fracture - random.uniform(0.05, 0.15), 2)
    hr_ci_hi = round(hr_fracture + random.uniform(0.05, 0.15), 2)

    # BMD increase
    bmd_increase = round(random.uniform(3, 15), 1)

    followup_months = random.choice([12, 24, 36, 48, 60])

    prefix = random.choice(TRIAL_PREFIXES['OST'])
    suffix = random.choice(['', '-1', '-2', '-EXT', '-PLUS', '-MEN', '-GIO'])
    trial_name = f"{prefix}{suffix}"

    trial_id = f"ENDO-OST-{idx:03d}"
    nct = generate_nct()
    source = generate_author()
    funder = random.choice(FUNDERS['OST'])
    institution = random.choice(INSTITUTIONS)
    sites = random.randint(100, 600)
    countries = random.randint(15, 45)

    fracture_type = random.choice(['vertebral', 'hip', 'nonvertebral', 'clinical'])

    text = f"""{trial_name} Trial: {drug.title()} for Fracture Prevention in Osteoporosis

This was a randomized, double-blind, {random.choice(['placebo-controlled', 'active-controlled'])} trial conducted at {sites} sites in {countries} countries. We enrolled {total_n} postmenopausal women with osteoporosis (T-score <=-2.5 at spine or hip).

Patients were randomly assigned to receive {drug} (treatment arm, n={n_treatment}) or {comparator} (control arm, n={n_control}).

Baseline characteristics: Mean age was {age} years (SD {round(random.uniform(6, 9), 1)}), {male_pct}% were male. Mean lumbar spine T-score was {tscore_spine}. Mean total hip T-score was {tscore_hip}. {round(random.uniform(20, 45), 1)}% had prevalent vertebral fractures.

The primary endpoint was incidence of new {fracture_type} fractures over {followup_months} months. {drug.title()} reduced the risk of {fracture_type} fractures by {round((1-hr_fracture)*100)}% (HR {hr_fracture}; 95% CI {hr_ci_lo}-{hr_ci_hi}; P<0.001).

BMD increased by {bmd_increase}% at the lumbar spine and {round(bmd_increase * 0.6, 1)}% at the total hip with {drug}.

NNT to prevent one {fracture_type} fracture was {random.randint(15, 50)} over {followup_months} months.

Median follow-up was {followup_months} months. Trial registration: {nct}. Funded by {funder}."""

    ground_truth = {
        'study': {'acronym': trial_name},
        'treatment': {'n': n_treatment},
        'control': {'n': n_control},
        'totalN': total_n,
        'primaryEffect': {
            'type': 'HR',
            'value': hr_fracture,
            'ciLo': hr_ci_lo,
            'ciHi': hr_ci_hi
        },
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct,
            'tscoreSpine': tscore_spine,
            'tscoreHip': tscore_hip
        },
        'followupMonths': followup_months,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': source,
        'domain': 'Endocrinology/Osteoporosis',
        'design': 'Superiority',
        'text': text,
        'groundTruth': ground_truth
    }

def generate_thyroid_trial(idx):
    """Generate Thyroid disorder trial"""
    condition = random.choice(['HYPER', 'HYPO', 'NODULE'])
    drug = random.choice(DRUGS['THY'][condition])
    comparator = random.choice(COMPARATORS['THY'])

    n_treatment = random.randint(80, 600)
    n_control = random.randint(80, 600)
    total_n = n_treatment + n_control

    age = round(random.uniform(35, 58), 1)
    male_pct = round(random.uniform(15, 35), 1)

    followup_weeks = random.choice([12, 24, 48, 52])

    prefix = random.choice(TRIAL_PREFIXES['THY'])
    suffix = random.choice(['', '-1', '-2', '-GD', '-HT'])
    trial_name = f"{prefix}{suffix}"

    trial_id = f"ENDO-THY-{idx:03d}"
    nct = generate_nct()
    source = generate_author()
    funder = random.choice(FUNDERS['THY'])
    institution = random.choice(INSTITUTIONS)
    sites = random.randint(20, 150)
    countries = random.randint(5, 20)

    if condition == 'HYPER':
        tsh_base = round(random.uniform(0.01, 0.1), 3)
        ft4_base = round(random.uniform(2.5, 5.0), 1)
        remission_rate = round(random.uniform(45, 75), 1)
        remission_ci_lo = round(remission_rate - random.uniform(5, 10), 1)
        remission_ci_hi = round(remission_rate + random.uniform(5, 10), 1)
        outcome_desc = f"remission rate of {remission_rate}% (95% CI {remission_ci_lo}-{remission_ci_hi})"
        condition_name = "Graves' Disease"
        effect_type = 'RR'
        effect_value = round(random.uniform(1.5, 2.5), 2)
    elif condition == 'HYPO':
        tsh_base = round(random.uniform(8, 50), 1)
        ft4_base = round(random.uniform(0.3, 0.8), 1)
        normalization = round(random.uniform(80, 95), 1)
        normalization_ci_lo = round(normalization - random.uniform(3, 8), 1)
        normalization_ci_hi = min(100, round(normalization + random.uniform(3, 8), 1))
        outcome_desc = f"TSH normalization in {normalization}% (95% CI {normalization_ci_lo}-{normalization_ci_hi})"
        condition_name = "Hypothyroidism"
        effect_type = 'MD'
        effect_value = round(random.uniform(-15, -5), 1)
    else:
        nodule_size = round(random.uniform(2.5, 5.0), 1)
        reduction = round(random.uniform(40, 70), 1)
        reduction_ci_lo = round(reduction - random.uniform(5, 12), 1)
        reduction_ci_hi = round(reduction + random.uniform(5, 12), 1)
        outcome_desc = f"nodule volume reduction of {reduction}% (95% CI {reduction_ci_lo}-{reduction_ci_hi})"
        condition_name = "Thyroid Nodules"
        effect_type = 'MD'
        effect_value = -reduction
        tsh_base = round(random.uniform(0.5, 2.5), 1)
        ft4_base = round(random.uniform(1.0, 1.5), 1)

    text = f"""{trial_name} Trial: {drug.title()} for {condition_name}

This was a randomized, {random.choice(['double-blind', 'open-label'])}, controlled trial conducted at {sites} sites in {countries} countries. We enrolled {total_n} patients with {condition_name.lower()}.

Patients were randomly assigned to receive {drug} (treatment arm, n={n_treatment}) or {comparator} (control arm, n={n_control}).

Baseline characteristics: Mean age was {age} years (SD {round(random.uniform(10, 15), 1)}), {male_pct}% were male. Mean baseline TSH was {tsh_base} mIU/L. Mean free T4 was {ft4_base} ng/dL.

The primary endpoint was {outcome_desc} at week {followup_weeks}.

Quality of life scores improved significantly with {drug} (P<0.01). Symptom resolution was achieved in {round(random.uniform(60, 85), 1)}% of patients.

Study duration was {followup_weeks} weeks. Trial registration: {nct}. Funded by {funder}."""

    ground_truth = {
        'study': {'acronym': trial_name},
        'treatment': {'n': n_treatment},
        'control': {'n': n_control},
        'totalN': total_n,
        'primaryEffect': {
            'type': effect_type,
            'value': effect_value
        },
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': source,
        'domain': 'Endocrinology/Thyroid',
        'design': random.choice(['Superiority', 'Non-inferiority']),
        'text': text,
        'groundTruth': ground_truth
    }

def generate_lipid_trial(idx):
    """Generate Lipid disorder trial"""
    drug_class = random.choice(list(DRUGS['LIP'].keys()))
    drug = random.choice(DRUGS['LIP'][drug_class])
    comparator = random.choice(COMPARATORS['LIP'])

    n_treatment = random.randint(500, 10000)
    n_control = random.randint(500, 10000)
    total_n = n_treatment + n_control

    age = round(random.uniform(55, 68), 1)
    male_pct = round(random.uniform(60, 80), 1)
    ldl_base = round(random.uniform(100, 180), 0)

    # LDL reduction
    ldl_reduction = round(random.uniform(-65, -25), 1)
    ldl_ci_lo = round(ldl_reduction - random.uniform(2, 5), 1)
    ldl_ci_hi = round(ldl_reduction + random.uniform(2, 5), 1)

    # MACE reduction for CV outcome trials
    cv_trial = random.random() < 0.4
    if cv_trial:
        hr_mace = round(random.uniform(0.75, 0.92), 2)
        hr_ci_lo = round(hr_mace - random.uniform(0.05, 0.10), 2)
        hr_ci_hi = round(hr_mace + random.uniform(0.05, 0.10), 2)
        followup_years = round(random.uniform(2.5, 5.0), 1)
    else:
        followup_weeks = random.choice([12, 24, 48, 52])

    prefix = random.choice(TRIAL_PREFIXES['LIP'])
    suffix = random.choice(['', '-1', '-2', '-3', '-LDL', '-CV', '-LONG', '-HIGH'])
    trial_name = f"{prefix}{suffix}"

    trial_id = f"ENDO-LIP-{idx:03d}"
    nct = generate_nct()
    source = generate_author()
    funder = random.choice(FUNDERS['LIP'])
    institution = random.choice(INSTITUTIONS)
    sites = random.randint(100, 1000)
    countries = random.randint(20, 50)

    if cv_trial:
        text = f"""{trial_name} Trial: {drug.title()} and Cardiovascular Outcomes

This was a randomized, double-blind, placebo-controlled cardiovascular outcomes trial conducted at {sites} sites in {countries} countries. We enrolled {total_n} patients with established atherosclerotic cardiovascular disease or high cardiovascular risk.

Patients were randomly assigned to receive {drug} (treatment arm, n={n_treatment}) or {comparator} (control arm, n={n_control}) on background statin therapy.

Baseline characteristics: Mean age was {age} years (SD {round(random.uniform(8, 11), 1)}), {male_pct}% were male. Mean baseline LDL-C was {ldl_base} mg/dL. {round(random.uniform(25, 45), 1)}% had diabetes.

{drug.title()} reduced LDL-C by {ldl_reduction}% (95% CI {ldl_ci_lo}-{ldl_ci_hi}) compared with {comparator}.

The primary endpoint of major adverse cardiovascular events (MACE) occurred in fewer patients on {drug} (HR {hr_mace}; 95% CI {hr_ci_lo}-{hr_ci_hi}; P<0.001).

NNT to prevent one MACE event was {random.randint(40, 80)} over {followup_years} years.

Median follow-up was {followup_years} years. Trial registration: {nct}. Funded by {funder}."""

        ground_truth = {
            'study': {'acronym': trial_name},
            'treatment': {'n': n_treatment},
            'control': {'n': n_control},
            'totalN': total_n,
            'primaryEffect': {
                'type': 'HR',
                'value': hr_mace,
                'ciLo': hr_ci_lo,
                'ciHi': hr_ci_hi
            },
            'ldlReduction': {
                'value': ldl_reduction,
                'ciLo': ldl_ci_lo,
                'ciHi': ldl_ci_hi
            },
            'baseline': {
                'ageMean': age,
                'malePercent': male_pct,
                'ldlBaseline': ldl_base
            },
            'followupYears': followup_years,
            'registration': nct,
            'fundingIndustry': True
        }
    else:
        text = f"""{trial_name} Trial: {drug.title()} for LDL-C Reduction

This was a randomized, double-blind, controlled trial conducted at {sites} sites in {countries} countries. We enrolled {total_n} patients with hypercholesterolemia inadequately controlled on maximally tolerated statin therapy.

Patients were randomly assigned to receive {drug} (treatment arm, n={n_treatment}) or {comparator} (control arm, n={n_control}).

Baseline characteristics: Mean age was {age} years (SD {round(random.uniform(9, 12), 1)}), {male_pct}% were male. Mean baseline LDL-C was {ldl_base} mg/dL.

The primary endpoint was percent change in LDL-C from baseline to week {followup_weeks}. {drug.title()} reduced LDL-C by {ldl_reduction}% (95% CI {ldl_ci_lo}-{ldl_ci_hi}) versus {round(random.uniform(-5, 5), 1)}% with {comparator} (P<0.001).

{round(random.uniform(70, 95), 1)}% of patients achieved LDL-C <70 mg/dL with {drug}.

Study duration was {followup_weeks} weeks. Trial registration: {nct}. Funded by {funder}."""

        ground_truth = {
            'study': {'acronym': trial_name},
            'treatment': {'n': n_treatment},
            'control': {'n': n_control},
            'totalN': total_n,
            'primaryEffect': {
                'type': 'MD',
                'value': ldl_reduction,
                'ciLo': ldl_ci_lo,
                'ciHi': ldl_ci_hi,
                'unit': 'percent'
            },
            'baseline': {
                'ageMean': age,
                'malePercent': male_pct,
                'ldlBaseline': ldl_base
            },
            'followupWeeks': followup_weeks,
            'registration': nct,
            'fundingIndustry': True
        }

    return {
        'id': trial_id,
        'source': source,
        'domain': 'Endocrinology/Lipids',
        'design': 'Superiority' if cv_trial else random.choice(['Superiority', 'Non-inferiority']),
        'text': text,
        'groundTruth': ground_truth
    }

def generate_other_endo_trial(idx):
    """Generate Other endocrine disorder trial"""
    condition = random.choice(['ADRENAL', 'PITUITARY', 'PCOS', 'HYPOPARA'])
    drug = random.choice(DRUGS['OTH'][condition])
    comparator = random.choice(COMPARATORS['OTH'])

    n_treatment = random.randint(50, 400)
    n_control = random.randint(50, 400)
    total_n = n_treatment + n_control

    age = round(random.uniform(30, 55), 1)

    followup_weeks = random.choice([12, 24, 48, 52])

    prefix = random.choice(TRIAL_PREFIXES['OTH'])
    suffix = random.choice(['', '-1', '-2', '-3'])
    trial_name = f"{prefix}{suffix}"

    trial_id = f"ENDO-OTH-{idx:03d}"
    nct = generate_nct()
    source = generate_author()
    funder = random.choice(FUNDERS['OTH'])
    institution = random.choice(INSTITUTIONS)
    sites = random.randint(15, 100)
    countries = random.randint(5, 20)

    if condition == 'ADRENAL':
        male_pct = round(random.uniform(35, 55), 1)
        condition_name = random.choice(["Cushing's Syndrome", "Adrenal Insufficiency", "Primary Aldosteronism"])
        if "Cushing" in condition_name:
            cortisol_base = round(random.uniform(25, 40), 1)
            cortisol_reduction = round(random.uniform(-50, -30), 1)
            cortisol_ci_lo = round(cortisol_reduction - random.uniform(5, 10), 1)
            cortisol_ci_hi = round(cortisol_reduction + random.uniform(5, 10), 1)
            outcome_desc = f"mean urinary free cortisol reduction of {cortisol_reduction}% (95% CI {cortisol_ci_lo}-{cortisol_ci_hi})"
        else:
            normalization = round(random.uniform(65, 85), 1)
            normalization_ci_lo = round(normalization - random.uniform(5, 10), 1)
            normalization_ci_hi = round(normalization + random.uniform(5, 10), 1)
            outcome_desc = f"hormone normalization in {normalization}% (95% CI {normalization_ci_lo}-{normalization_ci_hi})"
        effect_value = round(random.uniform(-45, -25), 1)
    elif condition == 'PITUITARY':
        male_pct = round(random.uniform(40, 60), 1)
        condition_name = random.choice(["Acromegaly", "Prolactinoma", "Cushing's Disease"])
        if "Acromegaly" in condition_name:
            igf1_reduction = round(random.uniform(-45, -25), 1)
            igf1_ci_lo = round(igf1_reduction - random.uniform(5, 10), 1)
            igf1_ci_hi = round(igf1_reduction + random.uniform(5, 10), 1)
            outcome_desc = f"IGF-1 normalization with reduction of {igf1_reduction}% (95% CI {igf1_ci_lo}-{igf1_ci_hi})"
        elif "Prolactinoma" in condition_name:
            prolactin_norm = round(random.uniform(70, 90), 1)
            prolactin_ci_lo = round(prolactin_norm - random.uniform(5, 10), 1)
            prolactin_ci_hi = round(prolactin_norm + random.uniform(5, 10), 1)
            outcome_desc = f"prolactin normalization in {prolactin_norm}% (95% CI {prolactin_ci_lo}-{prolactin_ci_hi})"
        else:
            ufc_norm = round(random.uniform(50, 75), 1)
            ufc_ci_lo = round(ufc_norm - random.uniform(8, 12), 1)
            ufc_ci_hi = round(ufc_norm + random.uniform(8, 12), 1)
            outcome_desc = f"urinary free cortisol normalization in {ufc_norm}% (95% CI {ufc_ci_lo}-{ufc_ci_hi})"
        effect_value = round(random.uniform(-40, -20), 1)
    elif condition == 'PCOS':
        male_pct = 0
        condition_name = "Polycystic Ovary Syndrome"
        ovulation_rate = round(random.uniform(50, 80), 1)
        ovulation_ci_lo = round(ovulation_rate - random.uniform(8, 12), 1)
        ovulation_ci_hi = round(ovulation_rate + random.uniform(8, 12), 1)
        outcome_desc = f"ovulation rate of {ovulation_rate}% (95% CI {ovulation_ci_lo}-{ovulation_ci_hi})"
        effect_value = round(random.uniform(1.5, 2.5), 2)
    else:  # HYPOPARA
        male_pct = round(random.uniform(20, 40), 1)
        condition_name = "Hypoparathyroidism"
        calcium_norm = round(random.uniform(60, 85), 1)
        calcium_ci_lo = round(calcium_norm - random.uniform(5, 10), 1)
        calcium_ci_hi = round(calcium_norm + random.uniform(5, 10), 1)
        outcome_desc = f"calcium normalization in {calcium_norm}% (95% CI {calcium_ci_lo}-{calcium_ci_hi})"
        effect_value = round(random.uniform(1.8, 3.0), 2)

    text = f"""{trial_name} Trial: {drug.title()} for {condition_name}

This was a randomized, {random.choice(['double-blind', 'open-label'])}, controlled trial conducted at {sites} sites in {countries} countries. We enrolled {total_n} patients with {condition_name.lower()}.

Patients were randomly assigned to receive {drug} (treatment arm, n={n_treatment}) or {comparator} (control arm, n={n_control}).

Baseline characteristics: Mean age was {age} years (SD {round(random.uniform(10, 15), 1)}), {male_pct}% were male.

The primary endpoint was {outcome_desc} at week {followup_weeks}.

Quality of life improved significantly with {drug} (P<0.01). Treatment was well tolerated with discontinuation rate of {round(random.uniform(5, 15), 1)}%.

Study duration was {followup_weeks} weeks. Trial registration: {nct}. Funded by {funder}."""

    ground_truth = {
        'study': {'acronym': trial_name},
        'treatment': {'n': n_treatment},
        'control': {'n': n_control},
        'totalN': total_n,
        'primaryEffect': {
            'type': 'RR' if condition in ['PCOS', 'HYPOPARA'] else 'MD',
            'value': effect_value
        },
        'baseline': {
            'ageMean': age,
            'malePercent': male_pct
        },
        'followupWeeks': followup_weeks,
        'registration': nct,
        'fundingIndustry': True
    }

    return {
        'id': trial_id,
        'source': source,
        'domain': f'Endocrinology/{condition_name}',
        'design': random.choice(['Superiority', 'Non-inferiority']),
        'text': text,
        'groundTruth': ground_truth
    }

def format_trial_js(trial):
    """Format a trial as JavaScript object string"""
    # Escape backticks and special characters in text
    text = trial['text'].replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

    gt = trial['groundTruth']

    # Build groundTruth string
    gt_lines = []
    gt_lines.append(f"            study: {{ acronym: '{gt['study']['acronym']}' }}")
    gt_lines.append(f"            treatment: {{ n: {gt['treatment']['n']} }}")
    gt_lines.append(f"            control: {{ n: {gt['control']['n']} }}")
    gt_lines.append(f"            totalN: {gt['totalN']}")

    # Primary effect
    pe = gt['primaryEffect']
    if 'ciLo' in pe and 'ciHi' in pe:
        if 'unit' in pe:
            gt_lines.append(f"            primaryEffect: {{ type: '{pe['type']}', value: {pe['value']}, ciLo: {pe['ciLo']}, ciHi: {pe['ciHi']}, unit: '{pe['unit']}' }}")
        else:
            gt_lines.append(f"            primaryEffect: {{ type: '{pe['type']}', value: {pe['value']}, ciLo: {pe['ciLo']}, ciHi: {pe['ciHi']} }}")
    else:
        gt_lines.append(f"            primaryEffect: {{ type: '{pe['type']}', value: {pe['value']} }}")

    # LDL reduction if present
    if 'ldlReduction' in gt:
        lr = gt['ldlReduction']
        gt_lines.append(f"            ldlReduction: {{ value: {lr['value']}, ciLo: {lr['ciLo']}, ciHi: {lr['ciHi']} }}")

    # Baseline
    bl = gt['baseline']
    bl_parts = []
    for key, val in bl.items():
        bl_parts.append(f"{key}: {val}")
    gt_lines.append(f"            baseline: {{ {', '.join(bl_parts)} }}")

    # Follow-up
    if 'followupWeeks' in gt:
        gt_lines.append(f"            followupWeeks: {gt['followupWeeks']}")
    elif 'followupMonths' in gt:
        gt_lines.append(f"            followupMonths: {gt['followupMonths']}")
    elif 'followupYears' in gt:
        gt_lines.append(f"            followupYears: {gt['followupYears']}")

    gt_lines.append(f"            registration: '{gt['registration']}'")
    gt_lines.append(f"            fundingIndustry: {str(gt['fundingIndustry']).lower()}")

    gt_str = ',\n'.join(gt_lines)

    return f"""    {{
        id: '{trial['id']}',
        source: '{trial['source']}',
        domain: '{trial['domain']}',
        design: '{trial['design']}',
        text: `{text}`,

        groundTruth: {{
{gt_str}
        }}
    }}"""

def main():
    """Generate 1000 metabolic/endocrine trials and append to validation file"""

    print("Generating 1000 Metabolic/Endocrine RCT trials...")

    trials = []

    # Generate T2D trials (300)
    print("  Generating 300 Type 2 Diabetes trials...")
    for i in range(1, 301):
        trials.append(generate_t2d_trial(i))

    # Generate Obesity trials (200)
    print("  Generating 200 Obesity trials...")
    for i in range(1, 201):
        trials.append(generate_obesity_trial(i))

    # Generate Osteoporosis trials (150)
    print("  Generating 150 Osteoporosis trials...")
    for i in range(1, 151):
        trials.append(generate_osteoporosis_trial(i))

    # Generate Thyroid trials (100)
    print("  Generating 100 Thyroid trials...")
    for i in range(1, 101):
        trials.append(generate_thyroid_trial(i))

    # Generate Lipid trials (150)
    print("  Generating 150 Lipid disorder trials...")
    for i in range(1, 151):
        trials.append(generate_lipid_trial(i))

    # Generate Other endocrine trials (100)
    print("  Generating 100 Other endocrine trials...")
    for i in range(1, 101):
        trials.append(generate_other_endo_trial(i))

    print(f"\nTotal trials generated: {len(trials)}")

    # Read existing file
    print(f"\nReading existing file: {TARGET_FILE}")
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the position to insert (before the closing ];)
    # Look for the last trial entry
    insert_pos = content.rfind('}')
    if insert_pos == -1:
        print("ERROR: Could not find insertion point in file")
        return

    # Find the closing of GROUND_TRUTH_CASES array
    array_end = content.rfind('];')
    if array_end == -1:
        print("ERROR: Could not find GROUND_TRUTH_CASES array end")
        return

    # Format all trials
    print("Formatting trials as JavaScript...")
    trial_strings = [format_trial_js(t) for t in trials]

    # Create the insertion content
    insertion = ',\n' + ',\n'.join(trial_strings)

    # Insert before the ];
    new_content = content[:array_end] + insertion + '\n' + content[array_end:]

    # Write back
    print(f"Writing updated file...")
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nSuccessfully added {len(trials)} metabolic/endocrine trials!")
    print("\nTrial ID ranges:")
    print("  ENDO-T2D-001 to ENDO-T2D-300 (Type 2 Diabetes)")
    print("  ENDO-OBS-001 to ENDO-OBS-200 (Obesity)")
    print("  ENDO-OST-001 to ENDO-OST-150 (Osteoporosis)")
    print("  ENDO-THY-001 to ENDO-THY-100 (Thyroid)")
    print("  ENDO-LIP-001 to ENDO-LIP-150 (Lipid disorders)")
    print("  ENDO-OTH-001 to ENDO-OTH-100 (Other endocrine)")

if __name__ == "__main__":
    main()
