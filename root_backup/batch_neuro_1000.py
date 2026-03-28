#!/usr/bin/env python3
"""
Batch Neurology/Psychiatry RCT Trial Generator
Generates 1000 unique trials for RCTExtractor validation
"""

import random
import json

# Set seed for reproducibility
random.seed(42)

def generate_nct():
    """Generate unique NCT number"""
    return f"NCT{random.randint(10000000, 99999999):08d}"

def generate_ci(value, effect_type):
    """Generate confidence interval based on effect type"""
    if effect_type == 'MD':
        # Mean difference - negative values for improvement
        margin = random.uniform(0.8, 2.5)
        ci_lo = round(value - margin, 2)
        ci_hi = round(value + margin, 2)
    elif effect_type == 'HR':
        # Hazard ratio
        margin_lo = random.uniform(0.05, 0.15)
        margin_hi = random.uniform(0.05, 0.15)
        ci_lo = round(value - margin_lo, 2)
        ci_hi = round(value + margin_hi, 2)
    else:  # RR
        margin_lo = random.uniform(0.2, 0.5)
        margin_hi = random.uniform(0.2, 0.5)
        ci_lo = round(value - margin_lo, 2)
        ci_hi = round(value + margin_hi, 2)
    return ci_lo, ci_hi

# Disease-specific data
MS_DRUGS = [
    ("ocrelizumab", "placebo", "anti-CD20 monoclonal antibody"),
    ("natalizumab", "placebo", "alpha-4 integrin inhibitor"),
    ("fingolimod", "placebo", "S1P receptor modulator"),
    ("dimethyl fumarate", "placebo", "Nrf2 activator"),
    ("teriflunomide", "placebo", "dihydroorotate dehydrogenase inhibitor"),
    ("siponimod", "placebo", "S1P receptor modulator"),
    ("ozanimod", "placebo", "S1P receptor modulator"),
    ("ofatumumab", "placebo", "anti-CD20 monoclonal antibody"),
    ("cladribine", "placebo", "purine nucleoside analogue"),
    ("alemtuzumab", "interferon beta-1a", "anti-CD52 monoclonal antibody"),
    ("ponesimod", "teriflunomide", "S1P receptor modulator"),
    ("ublituximab", "teriflunomide", "anti-CD20 monoclonal antibody"),
    ("rituximab", "placebo", "anti-CD20 monoclonal antibody"),
    ("glatiramer acetate", "placebo", "immunomodulator"),
    ("interferon beta-1a", "placebo", "cytokine immunomodulator"),
]

MS_OUTCOMES = [
    ("annualized relapse rate", "ARR", "MD", -0.3, -0.8),
    ("EDSS progression", "disability", "HR", 0.5, 0.8),
    ("new T2 lesions", "MRI", "RR", 0.3, 0.6),
    ("gadolinium-enhancing lesions", "MRI", "RR", 0.2, 0.5),
    ("brain volume loss", "atrophy", "MD", -0.2, -0.5),
    ("time to first relapse", "relapse", "HR", 0.4, 0.7),
    ("confirmed disability worsening", "CDP", "HR", 0.5, 0.75),
    ("no evidence of disease activity", "NEDA", "RR", 1.5, 2.5),
]

STROKE_DRUGS = [
    ("alteplase", "placebo", "tissue plasminogen activator"),
    ("tenecteplase", "alteplase", "modified tPA"),
    ("endovascular thrombectomy", "medical management", "mechanical intervention"),
    ("aspirin", "placebo", "antiplatelet"),
    ("clopidogrel", "aspirin", "P2Y12 inhibitor"),
    ("ticagrelor", "aspirin", "P2Y12 inhibitor"),
    ("rivaroxaban", "warfarin", "factor Xa inhibitor"),
    ("apixaban", "warfarin", "factor Xa inhibitor"),
    ("dabigatran", "warfarin", "direct thrombin inhibitor"),
    ("edoxaban", "warfarin", "factor Xa inhibitor"),
    ("nerinetide", "placebo", "neuroprotectant"),
    ("edaravone", "placebo", "free radical scavenger"),
]

STROKE_OUTCOMES = [
    ("modified Rankin Scale", "mRS", "MD", -0.5, -1.5),
    ("NIHSS improvement", "NIHSS", "MD", -2, -6),
    ("functional independence", "mRS 0-2", "RR", 1.3, 2.0),
    ("recurrent stroke", "prevention", "HR", 0.5, 0.8),
    ("major bleeding", "safety", "HR", 0.7, 1.3),
    ("mortality", "death", "HR", 0.6, 0.9),
    ("symptomatic ICH", "sICH", "RR", 0.5, 1.5),
]

EPILEPSY_DRUGS = [
    ("levetiracetam", "placebo", "SV2A ligand"),
    ("brivaracetam", "placebo", "SV2A ligand"),
    ("lacosamide", "placebo", "sodium channel blocker"),
    ("perampanel", "placebo", "AMPA antagonist"),
    ("cenobamate", "placebo", "sodium channel modulator"),
    ("cannabidiol", "placebo", "cannabinoid"),
    ("fenfluramine", "placebo", "serotonin releaser"),
    ("stiripentol", "placebo", "GABAergic"),
    ("everolimus", "placebo", "mTOR inhibitor"),
    ("eslicarbazepine", "placebo", "sodium channel blocker"),
    ("zonisamide", "placebo", "multi-mechanism"),
    ("topiramate", "placebo", "multi-mechanism"),
]

EPILEPSY_OUTCOMES = [
    ("seizure frequency reduction", "seizures", "MD", -30, -70),
    ("50% responder rate", "response", "RR", 1.5, 3.0),
    ("seizure-free rate", "freedom", "RR", 2.0, 5.0),
    ("median percent reduction", "reduction", "MD", -25, -55),
    ("convulsive seizure frequency", "convulsive", "MD", -20, -50),
    ("time to first seizure", "retention", "HR", 0.5, 0.8),
]

PARKINSONS_DRUGS = [
    ("pramipexole", "placebo", "dopamine agonist"),
    ("ropinirole", "placebo", "dopamine agonist"),
    ("rotigotine", "placebo", "dopamine agonist"),
    ("rasagiline", "placebo", "MAO-B inhibitor"),
    ("safinamide", "placebo", "MAO-B inhibitor"),
    ("opicapone", "placebo", "COMT inhibitor"),
    ("istradefylline", "placebo", "adenosine A2A antagonist"),
    ("amantadine ER", "placebo", "NMDA antagonist"),
    ("apomorphine", "placebo", "dopamine agonist"),
    ("levodopa-carbidopa intestinal gel", "oral levodopa", "continuous infusion"),
    ("foslevodopa-foscarbidopa", "oral levodopa", "subcutaneous infusion"),
]

PARKINSONS_OUTCOMES = [
    ("UPDRS Part III", "motor", "MD", -3, -8),
    ("OFF time reduction", "fluctuations", "MD", -1, -3),
    ("ON time without dyskinesia", "ON time", "MD", 0.5, 2.5),
    ("dyskinesia rating scale", "UDysRS", "MD", -2, -6),
    ("PDQ-39 improvement", "QoL", "MD", -2, -8),
    ("CGI-I responder rate", "response", "RR", 1.5, 2.5),
]

ALZHEIMERS_DRUGS = [
    ("lecanemab", "placebo", "anti-amyloid antibody"),
    ("donanemab", "placebo", "anti-amyloid antibody"),
    ("aducanumab", "placebo", "anti-amyloid antibody"),
    ("gantenerumab", "placebo", "anti-amyloid antibody"),
    ("solanezumab", "placebo", "anti-amyloid antibody"),
    ("donepezil", "placebo", "acetylcholinesterase inhibitor"),
    ("rivastigmine", "placebo", "acetylcholinesterase inhibitor"),
    ("galantamine", "placebo", "acetylcholinesterase inhibitor"),
    ("memantine", "placebo", "NMDA antagonist"),
    ("brexpiprazole", "placebo", "atypical antipsychotic"),
]

ALZHEIMERS_OUTCOMES = [
    ("CDR-SB change", "cognition", "MD", -0.3, -0.8),
    ("ADAS-Cog14 change", "cognition", "MD", -1.5, -4.0),
    ("ADCS-ADL change", "function", "MD", -1, -3),
    ("amyloid PET reduction", "biomarker", "MD", -20, -60),
    ("MMSE change", "cognition", "MD", -0.5, -2.0),
    ("NPI improvement", "behavior", "MD", -2, -6),
    ("ARIA-E incidence", "safety", "RR", 2.0, 5.0),
]

MIGRAINE_DRUGS = [
    ("erenumab", "placebo", "CGRP receptor antagonist"),
    ("fremanezumab", "placebo", "anti-CGRP antibody"),
    ("galcanezumab", "placebo", "anti-CGRP antibody"),
    ("eptinezumab", "placebo", "anti-CGRP antibody"),
    ("atogepant", "placebo", "oral CGRP antagonist"),
    ("rimegepant", "placebo", "oral CGRP antagonist"),
    ("ubrogepant", "placebo", "oral CGRP antagonist"),
    ("lasmiditan", "placebo", "5-HT1F agonist"),
    ("topiramate", "placebo", "antiepileptic"),
    ("onabotulinumtoxinA", "placebo", "neurotoxin"),
    ("valproate", "placebo", "antiepileptic"),
]

MIGRAINE_OUTCOMES = [
    ("monthly migraine days reduction", "MMD", "MD", -2, -5),
    ("50% responder rate", "response", "RR", 1.5, 2.5),
    ("acute medication use days", "medication", "MD", -1.5, -4),
    ("pain freedom at 2 hours", "acute", "RR", 1.5, 2.5),
    ("most bothersome symptom freedom", "MBS", "RR", 1.3, 2.0),
    ("HIT-6 improvement", "disability", "MD", -3, -8),
    ("monthly headache days", "MHD", "MD", -2, -6),
]

DEPRESSION_DRUGS = [
    ("escitalopram", "placebo", "SSRI"),
    ("sertraline", "placebo", "SSRI"),
    ("paroxetine", "placebo", "SSRI"),
    ("fluoxetine", "placebo", "SSRI"),
    ("citalopram", "placebo", "SSRI"),
    ("venlafaxine", "placebo", "SNRI"),
    ("duloxetine", "placebo", "SNRI"),
    ("desvenlafaxine", "placebo", "SNRI"),
    ("mirtazapine", "placebo", "NaSSA"),
    ("bupropion", "placebo", "NDRI"),
    ("vortioxetine", "placebo", "multimodal"),
    ("vilazodone", "placebo", "SPARI"),
    ("esketamine", "placebo", "NMDA antagonist"),
    ("psilocybin", "placebo", "psychedelic"),
    ("brexanolone", "placebo", "neurosteroid"),
    ("zuranolone", "placebo", "neurosteroid"),
    ("cariprazine", "placebo", "atypical antipsychotic"),
    ("aripiprazole augmentation", "placebo augmentation", "atypical antipsychotic"),
    ("quetiapine XR", "placebo", "atypical antipsychotic"),
]

DEPRESSION_OUTCOMES = [
    ("MADRS change", "depression", "MD", -3, -8),
    ("HAM-D17 change", "depression", "MD", -2, -6),
    ("PHQ-9 change", "depression", "MD", -2, -5),
    ("response rate", "response", "RR", 1.3, 2.0),
    ("remission rate", "remission", "RR", 1.4, 2.5),
    ("CGI-S improvement", "global", "MD", -0.5, -1.5),
    ("time to response", "onset", "HR", 1.3, 2.0),
    ("SDS improvement", "function", "MD", -2, -6),
]

SCHIZOPHRENIA_DRUGS = [
    ("risperidone", "placebo", "atypical antipsychotic"),
    ("olanzapine", "placebo", "atypical antipsychotic"),
    ("quetiapine", "placebo", "atypical antipsychotic"),
    ("aripiprazole", "placebo", "atypical antipsychotic"),
    ("paliperidone", "placebo", "atypical antipsychotic"),
    ("lurasidone", "placebo", "atypical antipsychotic"),
    ("cariprazine", "placebo", "atypical antipsychotic"),
    ("brexpiprazole", "placebo", "atypical antipsychotic"),
    ("lumateperone", "placebo", "atypical antipsychotic"),
    ("xanomeline-trospium", "placebo", "muscarinic agonist"),
    ("clozapine", "chlorpromazine", "atypical antipsychotic"),
    ("aripiprazole LAI", "oral aripiprazole", "long-acting injectable"),
    ("paliperidone palmitate", "oral paliperidone", "long-acting injectable"),
]

SCHIZOPHRENIA_OUTCOMES = [
    ("PANSS total change", "symptoms", "MD", -8, -20),
    ("PANSS positive subscale", "positive", "MD", -2, -6),
    ("PANSS negative subscale", "negative", "MD", -1, -4),
    ("CGI-S improvement", "global", "MD", -0.5, -1.5),
    ("response rate", "response", "RR", 1.5, 2.5),
    ("relapse prevention", "relapse", "HR", 0.3, 0.7),
    ("PSP improvement", "function", "MD", 3, 10),
]

ANXIETY_DRUGS = [
    ("escitalopram", "placebo", "SSRI"),
    ("paroxetine", "placebo", "SSRI"),
    ("sertraline", "placebo", "SSRI"),
    ("duloxetine", "placebo", "SNRI"),
    ("venlafaxine XR", "placebo", "SNRI"),
    ("pregabalin", "placebo", "calcium channel modulator"),
    ("buspirone", "placebo", "5-HT1A agonist"),
    ("vilazodone", "placebo", "SPARI"),
    ("vortioxetine", "placebo", "multimodal"),
    ("hydroxyzine", "placebo", "antihistamine"),
]

ANXIETY_OUTCOMES = [
    ("HAM-A change", "anxiety", "MD", -4, -10),
    ("LSAS change", "social anxiety", "MD", -10, -25),
    ("PDSS change", "panic", "MD", -3, -8),
    ("CGI-I response", "response", "RR", 1.5, 2.5),
    ("remission rate", "remission", "RR", 1.3, 2.0),
    ("SDS improvement", "function", "MD", -3, -8),
    ("Y-BOCS change", "OCD", "MD", -4, -10),
]

# Journal sources by domain
NEURO_JOURNALS = [
    "NEJM", "Lancet Neurol", "JAMA Neurol", "Ann Neurol", "Brain",
    "Neurology", "Lancet", "Mult Scler J", "Epilepsia", "Mov Disord",
    "Alzheimers Dement", "J Neurol Neurosurg Psychiatry", "Stroke",
    "Headache", "Cephalalgia", "J Headache Pain"
]

PSYCH_JOURNALS = [
    "NEJM", "Lancet Psychiatry", "JAMA Psychiatry", "Am J Psychiatry",
    "Br J Psychiatry", "Mol Psychiatry", "Biol Psychiatry", "J Clin Psychiatry",
    "Psychol Med", "Neuropsychopharmacology", "Int J Neuropsychopharmacol"
]

def generate_trial(trial_id, domain, subdomain, drugs, outcomes, journals, prefix):
    """Generate a single trial"""
    drug_info = random.choice(drugs)
    treatment, control, moa = drug_info

    outcome_info = random.choice(outcomes)
    outcome_name, outcome_short, effect_type, val_min, val_max = outcome_info

    # Generate sample sizes
    n_treatment = random.randint(80, 600)
    n_control = random.randint(80, 600)
    total_n = n_treatment + n_control

    # Generate demographics
    age_mean = round(random.uniform(35, 72), 1)
    age_sd = round(random.uniform(8, 15), 1)
    male_pct = round(random.uniform(35, 65), 1)

    # Generate effect
    if effect_type == 'MD':
        if val_min < -10:  # Percentage changes
            effect_val = round(random.uniform(val_min, val_max), 1)
        else:
            effect_val = round(random.uniform(val_min, val_max), 2)
    elif effect_type == 'HR':
        effect_val = round(random.uniform(val_min, val_max), 2)
    else:  # RR
        effect_val = round(random.uniform(val_min, val_max), 2)

    ci_lo, ci_hi = generate_ci(effect_val, effect_type)

    # Generate p-value
    if (effect_type == 'HR' and effect_val < 0.9) or \
       (effect_type == 'MD' and effect_val < -1) or \
       (effect_type == 'RR' and effect_val > 1.2):
        p_val = random.choice(["P<0.001", "P<0.01", "P=0.002", "P=0.003", "P<0.0001"])
    else:
        p_val = f"P={random.uniform(0.01, 0.05):.3f}"

    # Generate follow-up
    followup_weeks = random.choice([8, 12, 16, 24, 48, 52, 96, 104])

    # Generate NNT for beneficial outcomes
    if (effect_type == 'HR' and effect_val < 0.8) or (effect_type == 'RR' and effect_val > 1.3):
        nnt = random.randint(5, 25)
    else:
        nnt = None

    # Registration
    nct = generate_nct()

    # Journal
    journal = random.choice(journals)
    year = random.randint(2018, 2024)

    # Generate acronym
    acronyms = [
        f"{treatment[:3].upper()}-{outcome_short}",
        f"{subdomain[:4].upper()}-{random.randint(1,9)}",
        f"{treatment[:4].upper()}{year-2000}",
        f"{outcome_short}-{treatment[:3].upper()}",
    ]
    acronym = random.choice(acronyms).replace(" ", "")

    # Generate author
    first_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
                   "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor", "Thomas", "Moore",
                   "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Patel", "Kim",
                   "Chen", "Wang", "Liu", "Zhang", "Mueller", "Schmidt", "Weber", "Hoffmann"]
    author = f"{random.choice(first_names)} et al."

    # Build the trial text
    trial_text = f"""{acronym} Trial: {treatment.title()} in {subdomain}

This was a randomized, double-blind, {'placebo-controlled' if control == 'placebo' else 'active-controlled'} trial evaluating {treatment} ({moa}) for {subdomain.lower()}.

A total of {total_n} patients were enrolled and randomly assigned to receive {treatment} (treatment arm, n={n_treatment}) or {control} (control arm, n={n_control}).

Baseline characteristics: Mean age was {age_mean} years (SD {age_sd}), {male_pct}% were {'male' if male_pct > 50 else 'female'}.

The primary endpoint was {outcome_name}. """

    if effect_type == 'MD':
        trial_text += f"""The mean change from baseline was {effect_val} in the {treatment} group versus {round(effect_val * random.uniform(0.2, 0.5), 2)} in the {control} group (mean difference {effect_val}; 95% CI {ci_lo}-{ci_hi}; {p_val})."""
    elif effect_type == 'HR':
        trial_text += f"""The hazard ratio for {outcome_name} was {effect_val} (95% CI {ci_lo}-{ci_hi}; {p_val}) favoring {treatment}."""
    else:  # RR
        rate_treat = round(random.uniform(30, 60), 1)
        rate_ctrl = round(rate_treat / effect_val, 1)
        trial_text += f"""The {outcome_name} was {rate_treat}% with {treatment} versus {rate_ctrl}% with {control} (RR {effect_val}; 95% CI {ci_lo}-{ci_hi}; {p_val})."""

    if nnt:
        trial_text += f"""

The number needed to treat was {nnt} (95% CI {nnt-3 if nnt > 5 else 3}-{nnt+10})."""

    trial_text += f"""

The study duration was {followup_weeks} weeks. The trial was registered at ClinicalTrials.gov ({nct}). Funded by {'industry sponsor' if random.random() > 0.3 else 'government grant'}."""

    # Build ground truth
    ground_truth = {
        "study": {"acronym": acronym},
        "treatment": {"n": n_treatment},
        "control": {"n": n_control},
        "totalN": total_n,
        "primaryEffect": {
            "type": effect_type,
            "value": effect_val,
            "ciLo": ci_lo,
            "ciHi": ci_hi
        },
        "baseline": {
            "ageMean": age_mean,
            "malePercent": male_pct
        },
        "followupWeeks": followup_weeks,
        "registration": nct,
        "fundingIndustry": random.random() > 0.3
    }

    if nnt:
        ground_truth["nnt"] = nnt

    trial = {
        "id": trial_id,
        "source": f"{author} {journal} {year}",
        "domain": domain,
        "design": "Superiority",
        "text": trial_text,
        "groundTruth": ground_truth
    }

    return trial


def generate_all_trials():
    """Generate all 1000 trials"""
    trials = []

    # MS trials (150)
    for i in range(1, 151):
        trial_id = f"NEURO-MS-{i:03d}"
        subdomain = random.choice([
            "Relapsing Multiple Sclerosis", "Primary Progressive MS",
            "Secondary Progressive MS", "Clinically Isolated Syndrome",
            "Highly Active RRMS", "Treatment-Naive RRMS"
        ])
        trial = generate_trial(trial_id, "Neurology", subdomain, MS_DRUGS, MS_OUTCOMES, NEURO_JOURNALS, "MS")
        trials.append(trial)

    # Stroke trials (100)
    for i in range(1, 101):
        trial_id = f"NEURO-STROKE-{i:03d}"
        subdomain = random.choice([
            "Acute Ischemic Stroke", "Stroke Prevention",
            "Cardioembolic Stroke", "Lacunar Stroke",
            "Large Vessel Occlusion", "TIA Prevention"
        ])
        trial = generate_trial(trial_id, "Neurology", subdomain, STROKE_DRUGS, STROKE_OUTCOMES, NEURO_JOURNALS, "STROKE")
        trials.append(trial)

    # Epilepsy trials (100)
    for i in range(1, 101):
        trial_id = f"NEURO-EPI-{i:03d}"
        subdomain = random.choice([
            "Focal Epilepsy", "Drug-Resistant Epilepsy",
            "Generalized Epilepsy", "Lennox-Gastaut Syndrome",
            "Dravet Syndrome", "Juvenile Myoclonic Epilepsy"
        ])
        trial = generate_trial(trial_id, "Neurology", subdomain, EPILEPSY_DRUGS, EPILEPSY_OUTCOMES, NEURO_JOURNALS, "EPI")
        trials.append(trial)

    # Parkinson's trials (100)
    for i in range(1, 101):
        trial_id = f"NEURO-PD-{i:03d}"
        subdomain = random.choice([
            "Early Parkinson's Disease", "Advanced Parkinson's Disease",
            "Motor Fluctuations", "Levodopa-Induced Dyskinesia",
            "Parkinson's Disease Psychosis", "Off Episodes"
        ])
        trial = generate_trial(trial_id, "Neurology", subdomain, PARKINSONS_DRUGS, PARKINSONS_OUTCOMES, NEURO_JOURNALS, "PD")
        trials.append(trial)

    # Alzheimer's/Dementia trials (100)
    for i in range(1, 101):
        trial_id = f"NEURO-AD-{i:03d}"
        subdomain = random.choice([
            "Early Alzheimer's Disease", "Mild Cognitive Impairment",
            "Moderate Alzheimer's Disease", "Alzheimer's Disease Agitation",
            "Vascular Dementia", "Lewy Body Dementia"
        ])
        trial = generate_trial(trial_id, "Neurology", subdomain, ALZHEIMERS_DRUGS, ALZHEIMERS_OUTCOMES, NEURO_JOURNALS, "AD")
        trials.append(trial)

    # Migraine trials (100)
    for i in range(1, 101):
        trial_id = f"NEURO-MIG-{i:03d}"
        subdomain = random.choice([
            "Episodic Migraine Prevention", "Chronic Migraine Prevention",
            "Acute Migraine Treatment", "Medication Overuse Headache",
            "Migraine with Aura", "Cluster Headache"
        ])
        trial = generate_trial(trial_id, "Neurology", subdomain, MIGRAINE_DRUGS, MIGRAINE_OUTCOMES, NEURO_JOURNALS, "MIG")
        trials.append(trial)

    # Depression trials (150)
    for i in range(1, 151):
        trial_id = f"PSYCH-DEP-{i:03d}"
        subdomain = random.choice([
            "Major Depressive Disorder", "Treatment-Resistant Depression",
            "Bipolar Depression", "Postpartum Depression",
            "Anxious Depression", "Atypical Depression",
            "Geriatric Depression", "Adolescent Depression"
        ])
        trial = generate_trial(trial_id, "Psychiatry", subdomain, DEPRESSION_DRUGS, DEPRESSION_OUTCOMES, PSYCH_JOURNALS, "DEP")
        trials.append(trial)

    # Schizophrenia trials (100)
    for i in range(1, 101):
        trial_id = f"PSYCH-SCZ-{i:03d}"
        subdomain = random.choice([
            "Acute Schizophrenia", "Chronic Schizophrenia",
            "Negative Symptoms", "First-Episode Psychosis",
            "Relapse Prevention", "Treatment-Resistant Schizophrenia"
        ])
        trial = generate_trial(trial_id, "Psychiatry", subdomain, SCHIZOPHRENIA_DRUGS, SCHIZOPHRENIA_OUTCOMES, PSYCH_JOURNALS, "SCZ")
        trials.append(trial)

    # Anxiety/Other trials (100)
    for i in range(1, 101):
        trial_id = f"PSYCH-ANX-{i:03d}"
        subdomain = random.choice([
            "Generalized Anxiety Disorder", "Social Anxiety Disorder",
            "Panic Disorder", "Obsessive-Compulsive Disorder",
            "Post-Traumatic Stress Disorder", "Specific Phobia"
        ])
        trial = generate_trial(trial_id, "Psychiatry", subdomain, ANXIETY_DRUGS, ANXIETY_OUTCOMES, PSYCH_JOURNALS, "ANX")
        trials.append(trial)

    return trials


def format_trial_js(trial):
    """Format a trial as JavaScript object"""
    # Escape backticks in text
    text = trial['text'].replace('`', '\\`').replace('${', '\\${')

    gt = trial['groundTruth']

    js = f"""    {{
        id: '{trial['id']}',
        source: '{trial['source']}',
        domain: '{trial['domain']}',
        design: '{trial['design']}',
        text: `{text}`,

        groundTruth: {{
            study: {{ acronym: '{gt['study']['acronym']}' }},
            treatment: {{ n: {gt['treatment']['n']} }},
            control: {{ n: {gt['control']['n']} }},
            totalN: {gt['totalN']},
            primaryEffect: {{ type: '{gt['primaryEffect']['type']}', value: {gt['primaryEffect']['value']}, ciLo: {gt['primaryEffect']['ciLo']}, ciHi: {gt['primaryEffect']['ciHi']} }},
            baseline: {{
                ageMean: {gt['baseline']['ageMean']},
                malePercent: {gt['baseline']['malePercent']}
            }},"""

    if 'nnt' in gt:
        js += f"""
            nnt: {gt['nnt']},"""

    js += f"""
            followupWeeks: {gt['followupWeeks']},
            registration: '{gt['registration']}',
            fundingIndustry: {'true' if gt['fundingIndustry'] else 'false'}
        }}
    }}"""

    return js


def main():
    """Main function to generate trials and append to validation file"""
    print("Generating 1000 Neurology/Psychiatry RCT trials...")

    trials = generate_all_trials()

    print(f"Generated {len(trials)} trials")
    print(f"  - MS trials: 150")
    print(f"  - Stroke trials: 100")
    print(f"  - Epilepsy trials: 100")
    print(f"  - Parkinson's trials: 100")
    print(f"  - Alzheimer's trials: 100")
    print(f"  - Migraine trials: 100")
    print(f"  - Depression trials: 150")
    print(f"  - Schizophrenia trials: 100")
    print(f"  - Anxiety trials: 100")

    # Read the existing file
    input_file = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the closing of the array
    # Look for the last occurrence of "}," or "}" before "];"
    insert_pos = content.rfind('];')

    if insert_pos == -1:
        print("Error: Could not find end of array in validation file")
        return

    # Check if we need a comma before new entries
    # Find the last } before ];
    last_brace = content.rfind('}', 0, insert_pos)
    needs_comma = True

    # Generate JavaScript for new trials
    trials_js = []
    for trial in trials:
        trials_js.append(format_trial_js(trial))

    # Join with commas
    new_content = ",\n" + ",\n".join(trials_js)

    # Insert before ];
    updated_content = content[:insert_pos] + new_content + "\n" + content[insert_pos:]

    # Update the header comment
    updated_content = updated_content.replace(
        "// 3000 Clinical Trials",
        "// 4000 Clinical Trials (including 1000 Neurology/Psychiatry)"
    )

    # Write back
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"\nSuccessfully appended 1000 trials to {input_file}")
    print("Trial ID range: NEURO-MS-001 to PSYCH-ANX-100")

    # Print sample trial IDs
    print("\nSample trial IDs:")
    for trial in trials[:5]:
        print(f"  {trial['id']}: {trial['groundTruth']['study']['acronym']}")
    print("  ...")
    for trial in trials[-5:]:
        print(f"  {trial['id']}: {trial['groundTruth']['study']['acronym']}")


if __name__ == "__main__":
    main()
