#!/usr/bin/env python3
"""
Batch Specialty RCT Generator - 1000 Trials
Generates specialty clinical trials across multiple medical domains.
"""

import random
import re

# Set seed for reproducibility
random.seed(42)

# Target file
TARGET_FILE = r"C:/Users/user/Downloads/Dataextractor/validation_study_expanded.js"

# NCT number starting point (unique range)
NCT_START = 20000001

# Trial configurations by specialty
SPECIALTIES = {
    'Ophthalmology': {
        'prefix': 'OPH',
        'count': 150,
        'conditions': [
            {'name': 'AMD', 'full': 'Age-related Macular Degeneration', 'treatments': ['anti-VEGF injection', 'aflibercept', 'ranibizumab', 'bevacizumab', 'brolucizumab', 'faricimab'], 'controls': ['sham injection', 'placebo', 'laser photocoagulation'], 'outcomes': ['BCVA change', 'visual acuity improvement', 'central retinal thickness reduction'], 'effect_type': 'MD', 'effect_range': (3.0, 15.0), 'journals': ['Ophthalmology', 'Am J Ophthalmol', 'JAMA Ophthalmol', 'Br J Ophthalmol']},
            {'name': 'Glaucoma', 'full': 'Primary Open-Angle Glaucoma', 'treatments': ['prostaglandin analog', 'latanoprost', 'timolol', 'brimonidine', 'trabeculectomy', 'MIGS'], 'controls': ['placebo drops', 'observation', 'conventional therapy'], 'outcomes': ['IOP reduction', 'visual field preservation', 'RNFL thickness'], 'effect_type': 'MD', 'effect_range': (2.0, 8.0), 'journals': ['Ophthalmology', 'J Glaucoma', 'Am J Ophthalmol']},
            {'name': 'DME', 'full': 'Diabetic Macular Edema', 'treatments': ['intravitreal dexamethasone', 'aflibercept', 'ranibizumab', 'laser therapy', 'anti-VEGF'], 'controls': ['sham injection', 'observation', 'laser alone'], 'outcomes': ['BCVA improvement', 'central subfield thickness', 'resolution of edema'], 'effect_type': 'MD', 'effect_range': (5.0, 12.0), 'journals': ['Ophthalmology', 'Retina', 'JAMA Ophthalmol']},
            {'name': 'Cataracts', 'full': 'Age-related Cataracts', 'treatments': ['femtosecond laser cataract surgery', 'premium IOL', 'multifocal IOL', 'toric IOL'], 'controls': ['conventional phacoemulsification', 'monofocal IOL', 'standard surgery'], 'outcomes': ['uncorrected visual acuity', 'spectacle independence', 'patient satisfaction'], 'effect_type': 'MD', 'effect_range': (0.1, 0.5), 'journals': ['J Cataract Refract Surg', 'Ophthalmology', 'Am J Ophthalmol']},
            {'name': 'Dry Eye', 'full': 'Dry Eye Disease', 'treatments': ['cyclosporine ophthalmic', 'lifitegrast', 'punctal plugs', 'autologous serum'], 'controls': ['artificial tears', 'placebo drops', 'vehicle'], 'outcomes': ['Schirmer test improvement', 'OSDI score reduction', 'tear breakup time'], 'effect_type': 'MD', 'effect_range': (5.0, 20.0), 'journals': ['Cornea', 'Am J Ophthalmol', 'Eye Contact Lens']}
        ],
        'age_range': (55, 78),
        'male_pct_range': (40, 55)
    },
    'Nephrology': {
        'prefix': 'NEPH',
        'count': 150,
        'conditions': [
            {'name': 'CKD', 'full': 'Chronic Kidney Disease', 'treatments': ['SGLT2 inhibitor', 'dapagliflozin', 'canagliflozin', 'finerenone', 'ACE inhibitor'], 'controls': ['placebo', 'standard care', 'ARB alone'], 'outcomes': ['eGFR decline', 'kidney failure', 'doubling of creatinine'], 'effect_type': 'HR', 'effect_range': (0.55, 0.85), 'journals': ['J Am Soc Nephrol', 'Kidney Int', 'NEJM', 'Am J Kidney Dis']},
            {'name': 'Dialysis', 'full': 'End-Stage Kidney Disease on Dialysis', 'treatments': ['high-flux hemodialysis', 'hemodiafiltration', 'nocturnal dialysis', 'ESA therapy'], 'controls': ['conventional hemodialysis', 'standard dialysis', 'placebo'], 'outcomes': ['all-cause mortality', 'cardiovascular events', 'hospitalization'], 'effect_type': 'HR', 'effect_range': (0.70, 0.92), 'journals': ['J Am Soc Nephrol', 'Kidney Int', 'Nephrol Dial Transplant']},
            {'name': 'Transplant', 'full': 'Kidney Transplantation', 'treatments': ['belatacept', 'tacrolimus', 'sirolimus', 'alemtuzumab induction'], 'controls': ['cyclosporine', 'standard immunosuppression', 'basiliximab'], 'outcomes': ['graft survival', 'acute rejection', 'patient survival'], 'effect_type': 'HR', 'effect_range': (0.60, 0.88), 'journals': ['Am J Transplant', 'Transplantation', 'Kidney Int']},
            {'name': 'IgAN', 'full': 'IgA Nephropathy', 'treatments': ['sparsentan', 'corticosteroids', 'budesonide', 'RAS blockade'], 'controls': ['placebo', 'supportive care', 'ARB alone'], 'outcomes': ['proteinuria reduction', 'eGFR slope', 'complete remission'], 'effect_type': 'MD', 'effect_range': (-1.5, -0.3), 'journals': ['J Am Soc Nephrol', 'Kidney Int', 'NEJM']},
            {'name': 'ADPKD', 'full': 'Autosomal Dominant Polycystic Kidney Disease', 'treatments': ['tolvaptan', 'somatostatin analog', 'mTOR inhibitor'], 'controls': ['placebo', 'standard care'], 'outcomes': ['total kidney volume', 'eGFR decline', 'kidney pain'], 'effect_type': 'MD', 'effect_range': (-3.0, -1.0), 'journals': ['J Am Soc Nephrol', 'Kidney Int', 'NEJM']}
        ],
        'age_range': (50, 72),
        'male_pct_range': (52, 65)
    },
    'Pulmonology': {
        'prefix': 'PULM',
        'count': 150,
        'conditions': [
            {'name': 'COPD', 'full': 'Chronic Obstructive Pulmonary Disease', 'treatments': ['triple therapy', 'LAMA/LABA', 'umeclidinium/vilanterol', 'tiotropium', 'roflumilast'], 'controls': ['placebo', 'LABA alone', 'standard care'], 'outcomes': ['FEV1 improvement', 'exacerbation reduction', 'SGRQ score'], 'effect_type': 'MD', 'effect_range': (50, 150), 'journals': ['Am J Respir Crit Care Med', 'Chest', 'Lancet Respir Med', 'Eur Respir J']},
            {'name': 'Asthma', 'full': 'Moderate-to-Severe Asthma', 'treatments': ['dupilumab', 'benralizumab', 'mepolizumab', 'tezepelumab', 'omalizumab'], 'controls': ['placebo', 'standard ICS/LABA', 'high-dose ICS'], 'outcomes': ['annual exacerbation rate', 'FEV1 improvement', 'ACQ score'], 'effect_type': 'RR', 'effect_range': (0.40, 0.75), 'journals': ['NEJM', 'Lancet', 'Am J Respir Crit Care Med', 'J Allergy Clin Immunol']},
            {'name': 'IPF', 'full': 'Idiopathic Pulmonary Fibrosis', 'treatments': ['pirfenidone', 'nintedanib', 'pamrevlumab', 'PBI-4050'], 'controls': ['placebo', 'supportive care'], 'outcomes': ['FVC decline', 'progression-free survival', 'acute exacerbations'], 'effect_type': 'MD', 'effect_range': (-150, -50), 'journals': ['NEJM', 'Am J Respir Crit Care Med', 'Lancet Respir Med']},
            {'name': 'Bronchiectasis', 'full': 'Non-Cystic Fibrosis Bronchiectasis', 'treatments': ['inhaled antibiotics', 'azithromycin', 'brensocatib', 'mucolytics'], 'controls': ['placebo', 'standard care'], 'outcomes': ['exacerbation frequency', 'quality of life', 'lung function'], 'effect_type': 'RR', 'effect_range': (0.55, 0.85), 'journals': ['Lancet Respir Med', 'Thorax', 'Chest']},
            {'name': 'PAH', 'full': 'Pulmonary Arterial Hypertension', 'treatments': ['selexipag', 'macitentan', 'riociguat', 'treprostinil'], 'controls': ['placebo', 'ERA alone', 'standard therapy'], 'outcomes': ['6-minute walk distance', 'clinical worsening', 'mPAP reduction'], 'effect_type': 'MD', 'effect_range': (15, 45), 'journals': ['NEJM', 'Lancet Respir Med', 'Chest', 'Eur Respir J']}
        ],
        'age_range': (55, 72),
        'male_pct_range': (48, 62)
    },
    'Hematology': {
        'prefix': 'HEME',
        'count': 150,
        'conditions': [
            {'name': 'Anemia', 'full': 'Iron Deficiency Anemia', 'treatments': ['ferric carboxymaltose', 'iron isomaltoside', 'ferumoxytol', 'oral iron'], 'controls': ['placebo', 'oral iron', 'standard care'], 'outcomes': ['hemoglobin increase', 'ferritin normalization', 'transfusion avoidance'], 'effect_type': 'MD', 'effect_range': (1.0, 2.5), 'journals': ['Blood', 'Am J Hematol', 'Lancet Haematol', 'Br J Haematol']},
            {'name': 'ITP', 'full': 'Immune Thrombocytopenia', 'treatments': ['eltrombopag', 'romiplostim', 'avatrombopag', 'fostamatinib', 'rituximab'], 'controls': ['placebo', 'standard care', 'corticosteroids'], 'outcomes': ['platelet response', 'durable response', 'bleeding events'], 'effect_type': 'RR', 'effect_range': (1.5, 4.0), 'journals': ['Blood', 'Lancet Haematol', 'Am J Hematol']},
            {'name': 'Hemophilia', 'full': 'Hemophilia A', 'treatments': ['emicizumab', 'gene therapy', 'extended half-life factor VIII', 'fitusiran'], 'controls': ['standard factor VIII', 'on-demand therapy', 'placebo'], 'outcomes': ['annualized bleeding rate', 'joint bleeds', 'target joint resolution'], 'effect_type': 'RR', 'effect_range': (0.15, 0.45), 'journals': ['NEJM', 'Blood', 'Lancet Haematol', 'Haemophilia']},
            {'name': 'SCD', 'full': 'Sickle Cell Disease', 'treatments': ['voxelotor', 'crizanlizumab', 'gene therapy', 'L-glutamine'], 'controls': ['placebo', 'hydroxyurea alone', 'standard care'], 'outcomes': ['vaso-occlusive crises', 'hemoglobin increase', 'pain episodes'], 'effect_type': 'RR', 'effect_range': (0.50, 0.80), 'journals': ['NEJM', 'Blood', 'Lancet Haematol']},
            {'name': 'MDS', 'full': 'Myelodysplastic Syndromes', 'treatments': ['luspatercept', 'azacitidine', 'lenalidomide', 'imetelstat'], 'controls': ['placebo', 'best supportive care', 'ESA'], 'outcomes': ['transfusion independence', 'hematologic improvement', 'overall survival'], 'effect_type': 'RR', 'effect_range': (1.5, 3.5), 'journals': ['NEJM', 'Blood', 'Lancet Oncol']}
        ],
        'age_range': (45, 68),
        'male_pct_range': (45, 58)
    },
    'Dermatology': {
        'prefix': 'DERM',
        'count': 150,
        'conditions': [
            {'name': 'Psoriasis', 'full': 'Moderate-to-Severe Plaque Psoriasis', 'treatments': ['risankizumab', 'guselkumab', 'secukinumab', 'ixekizumab', 'bimekizumab'], 'controls': ['placebo', 'adalimumab', 'ustekinumab'], 'outcomes': ['PASI 90 response', 'PASI 100 response', 'IGA 0/1'], 'effect_type': 'RR', 'effect_range': (3.0, 12.0), 'journals': ['NEJM', 'J Am Acad Dermatol', 'Lancet', 'Br J Dermatol']},
            {'name': 'Eczema', 'full': 'Moderate-to-Severe Atopic Dermatitis', 'treatments': ['dupilumab', 'tralokinumab', 'abrocitinib', 'upadacitinib', 'baricitinib'], 'controls': ['placebo', 'topical corticosteroids', 'cyclosporine'], 'outcomes': ['EASI-75 response', 'IGA 0/1', 'pruritus NRS improvement'], 'effect_type': 'RR', 'effect_range': (2.5, 8.0), 'journals': ['NEJM', 'Lancet', 'J Am Acad Dermatol', 'Br J Dermatol']},
            {'name': 'Acne', 'full': 'Moderate-to-Severe Acne Vulgaris', 'treatments': ['sarecycline', 'isotretinoin', 'clascoterone', 'trifarotene'], 'controls': ['placebo', 'vehicle', 'doxycycline'], 'outcomes': ['inflammatory lesion reduction', 'IGA success', 'total lesion count'], 'effect_type': 'MD', 'effect_range': (-25, -10), 'journals': ['J Am Acad Dermatol', 'JAMA Dermatol', 'Br J Dermatol']},
            {'name': 'Vitiligo', 'full': 'Non-Segmental Vitiligo', 'treatments': ['ruxolitinib cream', 'tofacitinib', 'NB-UVB phototherapy', 'afamelanotide'], 'controls': ['placebo', 'vehicle cream', 'observation'], 'outcomes': ['F-VASI improvement', 'repigmentation', 'facial response'], 'effect_type': 'MD', 'effect_range': (15, 40), 'journals': ['NEJM', 'J Am Acad Dermatol', 'JAMA Dermatol']},
            {'name': 'Hidradenitis', 'full': 'Hidradenitis Suppurativa', 'treatments': ['adalimumab', 'secukinumab', 'bimekizumab', 'infliximab'], 'controls': ['placebo', 'standard care'], 'outcomes': ['HiSCR response', 'abscess and nodule count', 'pain reduction'], 'effect_type': 'RR', 'effect_range': (2.0, 5.0), 'journals': ['NEJM', 'J Am Acad Dermatol', 'JAMA Dermatol', 'Br J Dermatol']}
        ],
        'age_range': (28, 55),
        'male_pct_range': (42, 55)
    },
    'Surgery': {
        'prefix': 'SURG',
        'count': 150,
        'conditions': [
            {'name': 'THA', 'full': 'Total Hip Arthroplasty', 'treatments': ['robotic-assisted surgery', 'anterior approach', 'cementless fixation', 'ceramic bearing'], 'controls': ['conventional surgery', 'posterior approach', 'cemented fixation', 'polyethylene bearing'], 'outcomes': ['Harris Hip Score', 'functional recovery', 'complication rate'], 'effect_type': 'MD', 'effect_range': (3.0, 12.0), 'journals': ['J Bone Joint Surg Am', 'J Arthroplasty', 'Bone Joint J', 'Clin Orthop Relat Res']},
            {'name': 'TKA', 'full': 'Total Knee Arthroplasty', 'treatments': ['robotic-assisted TKA', 'patient-specific instrumentation', 'kinematic alignment', 'cruciate-retaining'], 'controls': ['conventional TKA', 'standard instrumentation', 'mechanical alignment', 'posterior-stabilized'], 'outcomes': ['Knee Society Score', 'WOMAC improvement', 'range of motion'], 'effect_type': 'MD', 'effect_range': (4.0, 15.0), 'journals': ['J Bone Joint Surg Am', 'J Arthroplasty', 'Knee', 'Clin Orthop Relat Res']},
            {'name': 'Spine', 'full': 'Lumbar Spine Surgery', 'treatments': ['minimally invasive fusion', 'artificial disc replacement', 'endoscopic discectomy', 'robotic-guided pedicle screws'], 'controls': ['open fusion', 'standard discectomy', 'conventional surgery', 'freehand technique'], 'outcomes': ['ODI improvement', 'VAS pain reduction', 'fusion rate'], 'effect_type': 'MD', 'effect_range': (5.0, 18.0), 'journals': ['Spine', 'J Neurosurg Spine', 'Eur Spine J', 'Spine J']},
            {'name': 'Shoulder', 'full': 'Rotator Cuff Repair', 'treatments': ['arthroscopic repair', 'augmented repair', 'superior capsular reconstruction', 'patch augmentation'], 'controls': ['open repair', 'standard repair', 'debridement alone', 'conservative management'], 'outcomes': ['Constant score', 'ASES score', 'retear rate'], 'effect_type': 'MD', 'effect_range': (6.0, 20.0), 'journals': ['J Shoulder Elbow Surg', 'Am J Sports Med', 'Arthroscopy', 'J Bone Joint Surg Am']},
            {'name': 'ACL', 'full': 'ACL Reconstruction', 'treatments': ['quadriceps tendon graft', 'hamstring autograft', 'all-inside technique', 'anatomic double-bundle'], 'controls': ['bone-patellar tendon-bone', 'single-bundle', 'transtibial technique', 'allograft'], 'outcomes': ['IKDC score', 'graft failure rate', 'return to sport'], 'effect_type': 'MD', 'effect_range': (3.0, 12.0), 'journals': ['Am J Sports Med', 'Arthroscopy', 'Knee Surg Sports Traumatol Arthrosc', 'J Bone Joint Surg Am']}
        ],
        'age_range': (45, 72),
        'male_pct_range': (42, 58)
    },
    'Pediatrics': {
        'prefix': 'PEDS',
        'count': 100,
        'conditions': [
            {'name': 'Asthma', 'full': 'Pediatric Asthma', 'treatments': ['mepolizumab', 'dupilumab', 'omalizumab', 'tezepelumab'], 'controls': ['placebo', 'standard ICS', 'LTRA'], 'outcomes': ['exacerbation rate', 'FEV1 improvement', 'asthma control'], 'effect_type': 'RR', 'effect_range': (0.40, 0.70), 'journals': ['NEJM', 'Lancet', 'J Allergy Clin Immunol', 'Pediatrics']},
            {'name': 'JIA', 'full': 'Juvenile Idiopathic Arthritis', 'treatments': ['tocilizumab', 'adalimumab', 'etanercept', 'abatacept'], 'controls': ['placebo', 'methotrexate', 'standard care'], 'outcomes': ['ACR Pedi 70 response', 'joint count improvement', 'inactive disease'], 'effect_type': 'RR', 'effect_range': (2.0, 5.0), 'journals': ['NEJM', 'Lancet', 'Arthritis Rheumatol', 'Pediatrics']},
            {'name': 'Eczema', 'full': 'Pediatric Atopic Dermatitis', 'treatments': ['dupilumab', 'tralokinumab', 'upadacitinib', 'crisaborole'], 'controls': ['placebo', 'topical corticosteroids', 'vehicle'], 'outcomes': ['EASI-75 response', 'IGA 0/1', 'pruritus improvement'], 'effect_type': 'RR', 'effect_range': (2.5, 7.0), 'journals': ['NEJM', 'Lancet', 'J Am Acad Dermatol', 'Pediatr Dermatol']},
            {'name': 'ADHD', 'full': 'Attention-Deficit/Hyperactivity Disorder', 'treatments': ['viloxazine', 'lisdexamfetamine', 'guanfacine XR', 'atomoxetine'], 'controls': ['placebo', 'behavioral therapy alone'], 'outcomes': ['ADHD-RS-5 improvement', 'CGI-I response', 'functional improvement'], 'effect_type': 'MD', 'effect_range': (-15, -8), 'journals': ['J Am Acad Child Adolesc Psychiatry', 'Lancet Psychiatry', 'Pediatrics', 'J Child Psychol Psychiatry']},
            {'name': 'T1DM', 'full': 'Type 1 Diabetes Mellitus', 'treatments': ['closed-loop insulin', 'teplizumab', 'hybrid closed-loop', 'CGM-guided therapy'], 'controls': ['multiple daily injections', 'standard pump', 'placebo'], 'outcomes': ['HbA1c reduction', 'time in range', 'hypoglycemia events'], 'effect_type': 'MD', 'effect_range': (-0.8, -0.3), 'journals': ['NEJM', 'Lancet', 'Diabetes Care', 'Pediatr Diabetes']}
        ],
        'age_range': (6, 16),
        'male_pct_range': (48, 55)
    }
}


def generate_nct(index):
    """Generate a unique NCT number."""
    return f"NCT{NCT_START + index:08d}"


def generate_sample_sizes():
    """Generate realistic sample sizes for treatment and control arms."""
    base = random.randint(80, 350)
    treatment_n = base + random.randint(-20, 50)
    control_n = base + random.randint(-20, 50)
    return treatment_n, control_n


def generate_effect_value(effect_type, effect_range):
    """Generate a realistic effect value based on type."""
    low, high = effect_range
    value = random.uniform(low, high)

    if effect_type == 'HR':
        value = round(value, 2)
        # Generate CI for HR
        ci_width = random.uniform(0.08, 0.18)
        ci_lo = round(max(0.1, value - ci_width), 2)
        ci_hi = round(min(1.5, value + ci_width), 2)
    elif effect_type == 'RR':
        value = round(value, 2)
        if value < 1:  # Protective effect
            ci_width = random.uniform(0.08, 0.15)
            ci_lo = round(max(0.1, value - ci_width), 2)
            ci_hi = round(min(0.99, value + ci_width), 2)
        else:  # Increased effect
            ci_width = random.uniform(0.3, 1.0)
            ci_lo = round(max(1.01, value - ci_width), 2)
            ci_hi = round(value + ci_width, 2)
    elif effect_type == 'MD':
        value = round(value, 1)
        ci_width = random.uniform(abs(value) * 0.2, abs(value) * 0.5)
        if value >= 0:
            ci_lo = round(max(0.1, value - ci_width), 1)
            ci_hi = round(value + ci_width, 1)
        else:
            ci_lo = round(value - ci_width, 1)
            ci_hi = round(min(-0.1, value + ci_width), 1)
    else:
        value = round(value, 2)
        ci_width = random.uniform(0.1, 0.3)
        ci_lo = round(value - ci_width, 2)
        ci_hi = round(value + ci_width, 2)

    return value, ci_lo, ci_hi


def generate_trial(specialty_name, specialty_config, trial_index, global_index):
    """Generate a single trial entry."""
    condition = random.choice(specialty_config['conditions'])
    treatment = random.choice(condition['treatments'])
    control = random.choice(condition['controls'])
    outcome = random.choice(condition['outcomes'])
    journal = random.choice(condition['journals'])

    treatment_n, control_n = generate_sample_sizes()
    total_n = treatment_n + control_n

    age_min, age_max = specialty_config['age_range']
    mean_age = round(random.uniform(age_min, age_max), 1)

    male_min, male_max = specialty_config['male_pct_range']
    male_pct = random.randint(male_min, male_max)

    effect_value, ci_lo, ci_hi = generate_effect_value(
        condition['effect_type'],
        condition['effect_range']
    )

    nct = generate_nct(global_index)
    year = random.randint(2018, 2024)
    volume = random.randint(100, 450)
    page_start = random.randint(100, 2000)
    page_end = page_start + random.randint(8, 15)

    trial_id = f"SPEC-{specialty_config['prefix']}-{trial_index:03d}"
    author_num = 2000 + global_index

    followup_months = random.randint(6, 36)

    # Build trial text with required format
    effect_type = condition['effect_type']
    if effect_type == 'HR':
        effect_text = f"hazard ratio {effect_value}, 95% CI {ci_lo}-{ci_hi}"
        result_text = f"HR {effect_value}, 95% CI {ci_lo}-{ci_hi}"
    elif effect_type == 'RR':
        effect_text = f"relative risk {effect_value}, 95% CI {ci_lo}-{ci_hi}"
        result_text = f"RR {effect_value}, 95% CI {ci_lo}-{ci_hi}"
    elif effect_type == 'MD':
        effect_text = f"mean difference {effect_value}, 95% CI {ci_lo}-{ci_hi}"
        result_text = f"MD {effect_value}, 95% CI {ci_lo}-{ci_hi}"
    else:
        effect_text = f"effect {effect_value}, 95% CI {ci_lo}-{ci_hi}"
        result_text = f"{effect_value}, 95% CI {ci_lo}-{ci_hi}"

    p_value = "P<0.001" if random.random() > 0.3 else f"P={round(random.uniform(0.001, 0.049), 3)}"

    text = f"""{trial_id}: {treatment.title()} for {condition['full']}.
Patients with {condition['full'].lower()} were randomized to {treatment} (treatment arm, n={treatment_n}) versus {control} (control arm, n={control_n}).
The primary endpoint was {outcome}. Mean age was {mean_age} years, {male_pct}% were male.
Results: {outcome.capitalize()} showed {result_text}. {p_value}.
Follow-up was {followup_months} months. Trial registration: {nct}."""

    trial = {
        'id': trial_id,
        'source': f"Author{author_num} et al. {journal} {year};{volume}:{page_start}-{page_end}",
        'domain': specialty_name,
        'design': 'Superiority',
        'text': text,
        'groundTruth': {
            'primaryEffect': {
                'type': effect_type,
                'value': effect_value,
                'ciLo': ci_lo,
                'ciHi': ci_hi
            },
            'treatment': {'n': treatment_n},
            'control': {'n': control_n},
            'baseline': {
                'ageMean': mean_age,
                'malePercent': male_pct
            },
            'registration': nct
        }
    }

    return trial


def format_trial_js(trial):
    """Format a trial as JavaScript object string."""
    text_escaped = trial['text'].replace('`', '\\`').replace('${', '\\${')

    gt = trial['groundTruth']

    js = f"""    {{
        id: '{trial["id"]}',
        source: '{trial["source"]}',
        domain: '{trial["domain"]}',
        design: '{trial["design"]}',
        text: `{text_escaped}`,
        groundTruth: {{
            primaryEffect: {{ type: '{gt["primaryEffect"]["type"]}', value: {gt["primaryEffect"]["value"]}, ciLo: {gt["primaryEffect"]["ciLo"]}, ciHi: {gt["primaryEffect"]["ciHi"]} }},
            treatment: {{ n: {gt["treatment"]["n"]} }},
            control: {{ n: {gt["control"]["n"]} }},
            baseline: {{ ageMean: {gt["baseline"]["ageMean"]}, malePercent: {gt["baseline"]["malePercent"]} }},
            registration: '{gt["registration"]}'
        }}
    }}"""

    return js


def main():
    print("Generating 1000 specialty RCT trials...")

    # Read the existing file
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the position to insert new trials (before the closing ];)
    # Look for the last trial entry and add after it
    insert_pattern = r'(\s*}\s*)\];(\s*//[^\n]*\n|\s*\n)*\s*(//[^\n]*\n)*\s*(if\s*\(typeof\s*module)'
    match = re.search(insert_pattern, content)

    if not match:
        # Alternative: find the closing of the array
        insert_pos = content.rfind('}')
        if insert_pos == -1:
            print("Error: Could not find insertion point in file")
            return
        # Find the next ]; after the last }
        array_close = content.find('];', insert_pos)
        if array_close == -1:
            print("Error: Could not find array closing")
            return
        insert_pos = array_close
    else:
        insert_pos = match.start() + len(match.group(1))

    # Find the closing "];" of the GROUND_TRUTH_CASES array
    # The file ends with "    }\n];" pattern
    array_close = content.rfind("];")
    if array_close == -1:
        print("Error: Could not find array closing '];'")
        return

    # Find the last "}" before "];" - this is the end of the last trial
    last_brace = content.rfind("}", 0, array_close)
    if last_brace == -1:
        print("Error: Could not find last trial closing brace")
        return

    insert_pos = last_brace + 1

    # Generate all trials
    trials_js = []
    global_index = 0

    for specialty_name, specialty_config in SPECIALTIES.items():
        count = specialty_config['count']
        print(f"  Generating {count} {specialty_name} trials...")

        for i in range(1, count + 1):
            trial = generate_trial(specialty_name, specialty_config, i, global_index)
            trial_js = format_trial_js(trial)
            trials_js.append(trial_js)
            global_index += 1

    print(f"Generated {len(trials_js)} trials total.")

    # Build the insertion string
    trials_text = ",\n".join(trials_js)
    insertion = ",\n" + trials_text

    # Insert the trials
    new_content = content[:insert_pos] + insertion + content[insert_pos:]

    # Write the updated file
    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Successfully added 1000 specialty trials to {TARGET_FILE}")
    print("\nBreakdown by specialty:")
    for specialty_name, specialty_config in SPECIALTIES.items():
        print(f"  - {specialty_name}: {specialty_config['count']} trials")


if __name__ == "__main__":
    main()
