#!/usr/bin/env python3
"""
Batch Infectious Disease RCT Trial Generator
Generates 1000 unique infectious disease clinical trials for validation study
"""

import random
import json

# Set seed for reproducibility
random.seed(42)

# Drug databases by category
COVID_ANTIVIRALS = [
    ("Remdesivir", "200mg IV day 1, then 100mg daily"),
    ("Molnupiravir", "800mg twice daily"),
    ("Nirmatrelvir/Ritonavir", "300mg/100mg twice daily"),
    ("Favipiravir", "1800mg twice daily day 1, then 800mg twice daily"),
    ("Ensitrelvir", "375mg once daily"),
    ("Bemnifosbuvir", "550mg twice daily"),
    ("Sabizabulin", "9mg once daily"),
    ("Obeldesivir", "350mg once daily"),
    ("AT-527", "550mg twice daily"),
    ("PBI-0451", "400mg once daily"),
]

COVID_MONOCLONALS = [
    ("Sotrovimab", "500mg single IV infusion"),
    ("Bebtelovimab", "175mg single IV infusion"),
    ("Tixagevimab/Cilgavimab", "300mg/300mg IM"),
    ("Casirivimab/Imdevimab", "1200mg single IV infusion"),
    ("Bamlanivimab/Etesevimab", "700mg/1400mg IV infusion"),
    ("Regdanvimab", "40mg/kg single IV infusion"),
    ("Adintrevimab", "300mg single IM injection"),
    ("VIR-7832", "500mg single IV infusion"),
    ("LY-CoV1404", "700mg single IV infusion"),
    ("SAB-185", "3840mg single IV infusion"),
]

COVID_VACCINES = [
    ("BNT162b2 booster", "30mcg IM single dose"),
    ("mRNA-1273 bivalent", "50mcg IM single dose"),
    ("NVX-CoV2373", "5mcg IM two doses"),
    ("Ad26.COV2.S booster", "5x10^10 vp IM single dose"),
    ("CoronaVac booster", "3mcg IM single dose"),
    ("COVAXIN", "6mcg IM two doses"),
    ("SCB-2019", "9mcg IM two doses"),
    ("VLA2001", "35AU IM two doses"),
    ("INO-4800", "2mg intradermal two doses"),
    ("CVnCoV", "12mcg IM two doses"),
]

HIV_ART = [
    ("Bictegravir/Emtricitabine/TAF", "50mg/200mg/25mg once daily"),
    ("Dolutegravir/Lamivudine", "50mg/300mg once daily"),
    ("Cabotegravir/Rilpivirine LA", "600mg/900mg IM monthly"),
    ("Lenacapavir", "927mg SC every 6 months"),
    ("Islatravir", "0.75mg once weekly"),
    ("Doravirine/Lamivudine/TDF", "100mg/300mg/300mg once daily"),
    ("Darunavir/Cobicistat/TAF/FTC", "800mg/150mg/10mg/200mg once daily"),
    ("Fostemsavir", "600mg twice daily"),
    ("Ibalizumab", "2000mg IV every 2 weeks"),
    ("Elsulfavirine", "20mg once daily"),
]

HIV_PREVENTION = [
    ("Cabotegravir LA PrEP", "600mg IM every 2 months"),
    ("Lenacapavir PrEP", "927mg SC every 6 months"),
    ("TAF/FTC PrEP", "25mg/200mg once daily"),
    ("Dapivirine vaginal ring", "25mg monthly"),
    ("Islatravir PrEP", "60mg once monthly"),
    ("Long-acting rilpivirine", "900mg IM monthly"),
    ("Broadly neutralizing antibodies", "VRC01 10mg/kg IV every 8 weeks"),
    ("MK-8507 PrEP", "400mg once weekly"),
    ("Event-driven TDF/FTC", "2-1-1 dosing"),
    ("Tenofovir alafenamide implant", "62.5mg subcutaneous yearly"),
]

HCV_DAAS = [
    ("Sofosbuvir/Velpatasvir", "400mg/100mg once daily"),
    ("Glecaprevir/Pibrentasvir", "300mg/120mg once daily"),
    ("Sofosbuvir/Velpatasvir/Voxilaprevir", "400mg/100mg/100mg once daily"),
    ("Ledipasvir/Sofosbuvir", "90mg/400mg once daily"),
    ("Elbasvir/Grazoprevir", "50mg/100mg once daily"),
    ("Daclatasvir/Asunaprevir/Beclabuvir", "30mg/200mg/75mg twice daily"),
    ("Ombitasvir/Paritaprevir/Ritonavir/Dasabuvir", "25mg/150mg/100mg/250mg once daily"),
    ("Ravidasvir/Sofosbuvir", "200mg/400mg once daily"),
    ("Ruzasvir/Uprifosbuvir", "180mg/450mg once daily"),
    ("AL-335/Odalasvir/Simeprevir", "800mg/25mg/75mg once daily"),
]

HBV_DRUGS = [
    ("Tenofovir alafenamide", "25mg once daily"),
    ("Tenofovir disoproxil fumarate", "300mg once daily"),
    ("Entecavir", "0.5mg once daily"),
    ("Peginterferon alfa-2a", "180mcg SC weekly"),
    ("Besifovir", "150mg once daily"),
    ("Vebicorvir", "300mg twice daily"),
    ("Bepirovirsen", "300mg SC weekly"),
    ("JNJ-3989", "200mg SC monthly"),
    ("VIR-2218", "200mg SC every 4 weeks"),
    ("AB-729", "60mg SC every 4 weeks"),
]

ANTIBIOTICS_GRAM_POS = [
    ("Ceftaroline", "600mg IV every 12 hours"),
    ("Dalbavancin", "1500mg IV single dose"),
    ("Oritavancin", "1200mg IV single dose"),
    ("Tedizolid", "200mg once daily"),
    ("Delafloxacin", "450mg twice daily"),
    ("Lefamulin", "150mg IV every 12 hours"),
    ("Omadacycline", "200mg IV day 1, then 100mg daily"),
    ("Contezolid", "800mg twice daily"),
    ("Afabicin", "240mg once daily"),
    ("Gepotidacin", "1500mg twice daily"),
]

ANTIBIOTICS_GRAM_NEG = [
    ("Ceftazidime/Avibactam", "2.5g IV every 8 hours"),
    ("Ceftolozane/Tazobactam", "3g IV every 8 hours"),
    ("Meropenem/Vaborbactam", "4g IV every 8 hours"),
    ("Imipenem/Cilastatin/Relebactam", "1.25g IV every 6 hours"),
    ("Plazomicin", "15mg/kg IV once daily"),
    ("Eravacycline", "1mg/kg IV every 12 hours"),
    ("Cefiderocol", "2g IV every 8 hours"),
    ("Sulbactam/Durlobactam", "1g/1g IV every 6 hours"),
    ("Aztreonam/Avibactam", "500mg/167mg IV every 6 hours"),
    ("Zoliflodacin", "3g orally single dose"),
]

ANTIBIOTICS_RESISTANT = [
    ("Cefepime/Taniborbactam", "2g/0.5g IV every 8 hours"),
    ("Cefepime/Enmetazobactam", "2g/0.5g IV every 8 hours"),
    ("Sulopenem", "500mg orally twice daily"),
    ("Murepavadin", "2mg/kg IV every 8 hours"),
    ("Brilacidin", "0.6mg/kg IV every 12 hours"),
    ("Debio-1452", "400mg orally twice daily"),
    ("TP-6076", "1.25mg/kg IV every 12 hours"),
    ("VNRX-5133 + cefepime", "2g IV every 8 hours"),
    ("SPR994", "600mg orally twice daily"),
    ("ETX0914", "2g orally single dose"),
]

ANTIFUNGALS = [
    ("Isavuconazole", "200mg once daily"),
    ("Posaconazole", "300mg once daily"),
    ("Ibrexafungerp", "300mg twice daily day 1, then 300mg once daily"),
    ("Fosmanogepix", "1000mg once daily"),
    ("Rezafungin", "400mg IV weekly"),
    ("Olorofim", "150mg twice daily"),
    ("Oteseconazole", "600mg once daily"),
    ("VT-1598", "200mg once daily"),
    ("PC945", "5mg nebulized twice daily"),
    ("MAT2203", "400mg twice daily"),
    ("Encochleated Amphotericin B", "400mg twice daily"),
    ("Anidulafungin", "200mg day 1, then 100mg daily"),
    ("Micafungin", "100mg once daily"),
    ("Caspofungin", "70mg day 1, then 50mg daily"),
]

TB_DRUGS = [
    ("Bedaquiline", "400mg daily x2 weeks, then 200mg 3x/week"),
    ("Pretomanid", "200mg once daily"),
    ("Linezolid", "600mg once daily"),
    ("Delamanid", "100mg twice daily"),
    ("Sutezolid", "600mg twice daily"),
    ("Telacebec", "75mg once daily"),
    ("Delpazolid", "800mg twice daily"),
    ("BTZ-043", "160mg once daily"),
    ("TBA-7371", "200mg once daily"),
    ("Macozinone", "160mg once daily"),
    ("SQ109", "300mg once daily"),
    ("OPC-167832", "30mg once daily"),
]

INFLUENZA_DRUGS = [
    ("Baloxavir marboxil", "40-80mg single dose"),
    ("Oseltamivir", "75mg twice daily"),
    ("Zanamivir", "10mg inhaled twice daily"),
    ("Peramivir", "600mg IV single dose"),
    ("Favipiravir", "1600mg day 1, then 600mg twice daily"),
    ("Pimodivir", "600mg twice daily"),
    ("CC-42344", "400mg once daily"),
    ("AV5080", "600mg once daily"),
    ("ZSP1273", "800mg once daily"),
    ("Umifenovir", "200mg three times daily"),
]

RSV_DRUGS = [
    ("Nirsevimab", "50-100mg IM single dose"),
    ("Palivizumab", "15mg/kg IM monthly"),
    ("Rilematovir", "350mg once daily"),
    ("Ziresovir", "350mg once daily"),
    ("EDP-938", "300mg twice daily"),
    ("JNJ-53718678", "500mg once daily"),
    ("RV521", "350mg twice daily"),
    ("Sisunatovir", "600mg twice daily"),
    ("AK0529", "700mg twice daily"),
    ("Presatovir", "200mg once daily"),
]

HERPES_DRUGS = [
    ("Pritelivir", "100mg once daily"),
    ("Amenamevir", "400mg once daily"),
    ("Brincidofovir", "200mg once weekly"),
    ("Maribavir", "400mg twice daily"),
    ("Valacyclovir", "1000mg twice daily"),
    ("Famciclovir", "500mg twice daily"),
    ("Letermovir", "480mg once daily"),
    ("Filociclovir", "300mg twice daily"),
    ("Cyclopropavir", "200mg twice daily"),
    ("Valomaciclovir", "500mg twice daily"),
]

# Condition and endpoint definitions
CONDITION_ENDPOINTS = {
    "COVID-19": {
        "conditions": [
            "mild-to-moderate COVID-19",
            "severe COVID-19 pneumonia",
            "hospitalized COVID-19",
            "COVID-19 with hypoxemia",
            "high-risk outpatient COVID-19",
            "COVID-19 in immunocompromised patients",
            "COVID-19 post-exposure prophylaxis",
        ],
        "primary_endpoints": [
            ("hospitalization or death", "RR"),
            ("viral clearance at day 5", "RR"),
            ("time to clinical improvement", "HR"),
            ("all-cause mortality", "RR"),
            ("progression to severe disease", "RR"),
            ("time to sustained recovery", "HR"),
            ("symptom resolution by day 7", "RR"),
        ],
        "secondary_endpoints": [
            "duration of hospitalization",
            "ICU admission rate",
            "mechanical ventilation rate",
            "viral load reduction at day 3",
            "time to negative PCR",
            "WHO ordinal scale improvement",
        ],
    },
    "HIV": {
        "conditions": [
            "treatment-naive HIV-1 infection",
            "virologically suppressed HIV-1",
            "treatment-experienced HIV-1",
            "HIV-1 with resistance mutations",
            "HIV-1 in adolescents",
            "acute HIV-1 infection",
            "HIV-1 prevention in high-risk individuals",
        ],
        "primary_endpoints": [
            ("virologic suppression at week 48", "RR"),
            ("HIV-1 RNA <50 copies/mL at week 96", "RR"),
            ("virologic failure", "RR"),
            ("HIV-1 acquisition", "HR"),
            ("maintenance of suppression", "RR"),
            ("time to virologic failure", "HR"),
        ],
        "secondary_endpoints": [
            "CD4 count change from baseline",
            "treatment-emergent resistance",
            "drug discontinuation rate",
            "patient satisfaction score",
            "injection site reactions",
            "lipid profile changes",
        ],
    },
    "HCV": {
        "conditions": [
            "treatment-naive HCV genotype 1",
            "HCV with compensated cirrhosis",
            "HCV genotype 3 infection",
            "HCV/HIV coinfection",
            "treatment-experienced HCV",
            "HCV genotype 2/4/5/6",
            "decompensated cirrhosis",
        ],
        "primary_endpoints": [
            ("SVR12", "RR"),
            ("SVR24", "RR"),
            ("virologic cure", "RR"),
            ("HCV RNA undetectable at week 12", "RR"),
        ],
        "secondary_endpoints": [
            "on-treatment virologic response",
            "relapse rate",
            "breakthrough rate",
            "liver fibrosis improvement",
            "quality of life improvement",
            "ALT normalization",
        ],
    },
    "HBV": {
        "conditions": [
            "chronic HBV infection",
            "HBeAg-positive chronic hepatitis B",
            "HBeAg-negative chronic hepatitis B",
            "HBV with advanced fibrosis",
            "HBV/HDV coinfection",
            "lamivudine-resistant HBV",
        ],
        "primary_endpoints": [
            ("HBsAg loss at week 48", "RR"),
            ("HBV DNA suppression", "RR"),
            ("HBeAg seroconversion", "RR"),
            ("functional cure", "RR"),
            ("ALT normalization", "RR"),
        ],
        "secondary_endpoints": [
            "HBsAg reduction",
            "HBV DNA undetectable rate",
            "histological improvement",
            "fibrosis regression",
            "HBcrAg reduction",
            "pgRNA reduction",
        ],
    },
    "bacterial_gram_pos": {
        "conditions": [
            "acute bacterial skin and skin structure infection",
            "community-acquired pneumonia",
            "hospital-acquired pneumonia",
            "MRSA bacteremia",
            "osteomyelitis",
            "infective endocarditis",
            "complicated skin infection",
        ],
        "primary_endpoints": [
            ("clinical cure at test of cure", "RR"),
            ("early clinical response at 48-72h", "RR"),
            ("microbiological eradication", "RR"),
            ("investigator-assessed cure", "RR"),
            ("all-cause mortality at day 28", "RR"),
        ],
        "secondary_endpoints": [
            "time to clinical stability",
            "hospital length of stay",
            "recurrence rate",
            "microbiological response",
            "fever resolution time",
            "inflammatory marker normalization",
        ],
    },
    "bacterial_gram_neg": {
        "conditions": [
            "complicated urinary tract infection",
            "complicated intra-abdominal infection",
            "hospital-acquired pneumonia",
            "ventilator-associated pneumonia",
            "carbapenem-resistant Enterobacterales",
            "bloodstream infection",
            "healthcare-associated pneumonia",
        ],
        "primary_endpoints": [
            ("clinical cure at test of cure", "RR"),
            ("composite clinical and microbiological response", "RR"),
            ("28-day all-cause mortality", "RR"),
            ("microbiological eradication", "RR"),
            ("clinical success at end of treatment", "RR"),
        ],
        "secondary_endpoints": [
            "per-pathogen microbiological response",
            "time to defervescence",
            "clinical relapse rate",
            "resistance emergence",
            "hospital-free days",
            "ICU-free days",
        ],
    },
    "fungal": {
        "conditions": [
            "invasive aspergillosis",
            "invasive candidiasis",
            "candidemia",
            "vulvovaginal candidiasis",
            "cryptococcal meningitis",
            "mucormycosis",
            "chronic pulmonary aspergillosis",
        ],
        "primary_endpoints": [
            ("all-cause mortality at day 30", "RR"),
            ("global success at end of treatment", "RR"),
            ("clinical cure rate", "RR"),
            ("mycological eradication", "RR"),
            ("treatment success at week 6", "RR"),
        ],
        "secondary_endpoints": [
            "time to clinical response",
            "galactomannan clearance",
            "recurrence rate at 90 days",
            "fungal-free survival",
            "biomarker response",
            "radiological improvement",
        ],
    },
    "TB": {
        "conditions": [
            "drug-susceptible pulmonary TB",
            "multidrug-resistant TB",
            "extensively drug-resistant TB",
            "latent TB infection",
            "TB meningitis",
            "rifampin-resistant TB",
            "pre-XDR TB",
        ],
        "primary_endpoints": [
            ("favorable outcome at month 12", "RR"),
            ("culture conversion at week 8", "RR"),
            ("treatment success rate", "RR"),
            ("sputum culture negativity at month 6", "RR"),
            ("TB-free survival", "HR"),
        ],
        "secondary_endpoints": [
            "time to culture conversion",
            "smear conversion rate",
            "relapse-free survival",
            "treatment completion rate",
            "acquired resistance",
            "radiological improvement",
        ],
    },
    "influenza": {
        "conditions": [
            "uncomplicated influenza",
            "hospitalized influenza",
            "high-risk influenza",
            "influenza in elderly",
            "influenza post-exposure prophylaxis",
            "influenza in immunocompromised",
        ],
        "primary_endpoints": [
            ("time to alleviation of symptoms", "HR"),
            ("influenza complications", "RR"),
            ("hospitalization rate", "RR"),
            ("viral shedding duration", "HR"),
        ],
        "secondary_endpoints": [
            "duration of fever",
            "return to normal activities",
            "antiviral resistance",
            "secondary complications",
            "viral load reduction",
        ],
    },
    "RSV": {
        "conditions": [
            "RSV lower respiratory tract infection",
            "RSV bronchiolitis in infants",
            "RSV in high-risk infants",
            "RSV in elderly adults",
            "RSV in immunocompromised",
            "RSV prophylaxis",
        ],
        "primary_endpoints": [
            ("medically attended RSV LRTI", "RR"),
            ("RSV hospitalization", "RR"),
            ("severe RSV disease", "RR"),
            ("time to symptom resolution", "HR"),
        ],
        "secondary_endpoints": [
            "ICU admission rate",
            "supplemental oxygen requirement",
            "duration of hospitalization",
            "mechanical ventilation rate",
            "outpatient visit rate",
        ],
    },
    "herpes": {
        "conditions": [
            "genital herpes recurrence",
            "herpes labialis",
            "herpes zoster",
            "CMV infection in transplant",
            "HSV encephalitis",
            "neonatal herpes",
            "resistant CMV infection",
        ],
        "primary_endpoints": [
            ("time to lesion healing", "HR"),
            ("recurrence rate", "RR"),
            ("CMV viremia clearance", "RR"),
            ("prevention of CMV disease", "RR"),
        ],
        "secondary_endpoints": [
            "duration of viral shedding",
            "pain resolution time",
            "postherpetic neuralgia incidence",
            "asymptomatic shedding reduction",
            "time to next recurrence",
        ],
    },
}

# Journal sources
JOURNALS = [
    "N Engl J Med",
    "Lancet",
    "JAMA",
    "Lancet Infect Dis",
    "Clin Infect Dis",
    "J Infect Dis",
    "Antimicrob Agents Chemother",
    "J Antimicrob Chemother",
    "Open Forum Infect Dis",
    "AIDS",
    "J Acquir Immune Defic Syndr",
    "Hepatology",
    "J Hepatol",
    "J Viral Hepat",
    "Chest",
    "Am J Respir Crit Care Med",
    "Crit Care Med",
    "Intensive Care Med",
    "Ann Intern Med",
    "BMJ",
    "PLoS Med",
    "Nature Med",
    "Cell Host Microbe",
    "Emerg Infect Dis",
    "Euro Surveill",
]

AUTHOR_FIRST = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Chen", "Wang", "Li", "Zhang", "Liu", "Kumar",
    "Singh", "Patel", "Kim", "Park", "Lee", "Nguyen", "Thompson", "White",
    "Harris", "Martin", "Jackson", "Clark", "Lewis", "Robinson", "Walker",
    "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill",
    "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell",
    "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards",
]

COUNTRIES = [
    "United States", "United Kingdom", "Germany", "France", "Spain", "Italy",
    "Brazil", "Mexico", "Canada", "Australia", "Japan", "South Korea",
    "China", "India", "South Africa", "Argentina", "Poland", "Netherlands",
    "Belgium", "Sweden", "Switzerland", "Austria", "Denmark", "Norway",
]

SITES_RANGE = [(50, 100), (100, 200), (200, 400), (400, 600)]


def generate_nct():
    """Generate a random NCT number."""
    return f"NCT{random.randint(10000000, 99999999)}"


def generate_sample_size(category):
    """Generate appropriate sample sizes based on trial category."""
    sizes = {
        "COVID-19": (200, 3000),
        "HIV": (300, 1500),
        "HCV": (150, 800),
        "HBV": (150, 600),
        "bacterial": (300, 1200),
        "fungal": (100, 400),
        "TB": (200, 800),
        "viral": (150, 600),
    }
    min_n, max_n = sizes.get(category, (200, 800))
    total = random.randint(min_n, max_n)
    # Ensure even split with some variation
    treatment_n = total // 2 + random.randint(-20, 20)
    control_n = total - treatment_n
    return treatment_n, control_n, total


def generate_effect_size(effect_type, is_favorable=True):
    """Generate realistic effect sizes with confidence intervals."""
    if effect_type == "RR":
        if is_favorable:
            # Favorable RR for treatment (higher response/cure)
            rr = round(random.uniform(1.15, 2.80), 2)
            ci_width = random.uniform(0.15, 0.45)
        else:
            # Risk reduction
            rr = round(random.uniform(0.35, 0.85), 2)
            ci_width = random.uniform(0.10, 0.30)
    else:  # HR
        # Typically want HR < 1 for benefit
        rr = round(random.uniform(0.45, 0.88), 2)
        ci_width = random.uniform(0.12, 0.28)

    ci_lo = round(rr - ci_width / 2, 2)
    ci_hi = round(rr + ci_width / 2, 2)

    # Ensure reasonable bounds
    if effect_type == "RR" and is_favorable:
        ci_lo = max(1.01, ci_lo)
    elif effect_type == "HR" or not is_favorable:
        ci_hi = min(0.99, ci_hi) if rr < 1 else ci_hi

    return rr, ci_lo, ci_hi


def generate_baseline_characteristics():
    """Generate realistic baseline patient characteristics."""
    age_mean = round(random.uniform(35.0, 72.0), 1)
    age_sd = round(random.uniform(8.0, 16.0), 1)
    male_pct = round(random.uniform(40.0, 75.0), 1)

    return {
        "age_mean": age_mean,
        "age_sd": age_sd,
        "male_pct": male_pct,
    }


def generate_trial_text(trial_data):
    """Generate the full trial text in the expected format."""

    text = f"""{trial_data['acronym']} Trial: {trial_data['treatment_name']} in {trial_data['condition']}

This was a randomized, double-blind, placebo-controlled trial conducted at {trial_data['sites']} sites in {trial_data['countries']} countries. We enrolled {trial_data['total_n']} patients with {trial_data['condition']}. Patients were randomly assigned to receive {trial_data['treatment_name']} ({trial_data['treatment_dose']}) (treatment arm, n={trial_data['treatment_n']}) or placebo (control arm, n={trial_data['control_n']}).

Baseline characteristics: Mean age was {trial_data['baseline']['age_mean']} years (SD {trial_data['baseline']['age_sd']}), {trial_data['baseline']['male_pct']}% were male.{trial_data['additional_baseline']}

The primary outcome was {trial_data['primary_endpoint']}. {trial_data['primary_result']}

{trial_data['secondary_results']}

The median follow-up was {trial_data['followup_weeks']} weeks.{trial_data['funding_text']}
The trial was registered at ClinicalTrials.gov ({trial_data['nct']})."""

    return text


def generate_covid_trials(start_idx):
    """Generate 200 COVID-19 trials."""
    trials = []
    trial_num = start_idx

    # 70 antiviral trials
    for i in range(70):
        drug, dose = random.choice(COVID_ANTIVIRALS)
        condition_data = CONDITION_ENDPOINTS["COVID-19"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("COVID-19")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=(effect_type == "RR"))
        baseline = generate_baseline_characteristics()

        # Calculate event rates
        if effect_type == "RR":
            control_rate = round(random.uniform(15, 35), 1)
            treatment_rate = round(control_rate * effect, 1) if effect > 1 else round(control_rate * effect, 1)
        else:
            control_rate = round(random.uniform(20, 40), 1)
            treatment_rate = round(control_rate * effect, 1)

        primary_result = f"The primary endpoint of {endpoint} occurred in {round(treatment_rate)}% of the treatment group vs {round(control_rate)}% of the placebo group ({effect_type} {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"For secondary endpoints, {secondary[0]} showed improvement (P=0.00{random.randint(1,9)}). {secondary[1].capitalize()} was also significantly different between groups."

        additional_baseline = f" Median symptom duration was {random.randint(2, 5)} days. {random.randint(30, 60)}% had at least one risk factor for severe disease."

        trial_data = {
            "acronym": f"INFECT-COVID-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE)),
            "countries": random.randint(8, 25),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(4, 24),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Pfizer', 'Gilead Sciences', 'Merck', 'Roche', 'AstraZeneca', 'GSK', 'Moderna', 'BioNTech'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 202{random.randint(1,5)};{random.randint(380,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - COVID-19",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": effect_type, "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    # 70 monoclonal antibody trials
    for i in range(70):
        drug, dose = random.choice(COVID_MONOCLONALS)
        condition_data = CONDITION_ENDPOINTS["COVID-19"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("COVID-19")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=(effect_type == "RR"))
        baseline = generate_baseline_characteristics()

        if effect_type == "RR":
            control_rate = round(random.uniform(12, 30), 1)
            treatment_rate = round(control_rate * effect, 1) if effect > 1 else round(control_rate * effect, 1)
        else:
            control_rate = round(random.uniform(18, 35), 1)
            treatment_rate = round(control_rate * effect, 1)

        primary_result = f"The primary endpoint of {endpoint} occurred in {round(treatment_rate)}% of the treatment group vs {round(control_rate)}% of the placebo group ({effect_type} {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"For secondary endpoints, {secondary[0]} was significantly reduced with treatment (P=0.00{random.randint(1,9)}). {secondary[1].capitalize()} also favored the treatment group."

        additional_baseline = f" {random.randint(40, 70)}% were unvaccinated. Time from symptom onset was {random.randint(2, 6)} days."

        trial_data = {
            "acronym": f"INFECT-COVID-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE)),
            "countries": random.randint(6, 20),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(4, 16),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Regeneron', 'Eli Lilly', 'Vir Biotechnology', 'GSK', 'AstraZeneca', 'AbCellera'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 202{random.randint(1,5)};{random.randint(380,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - COVID-19",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": effect_type, "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    # 60 vaccine trials
    for i in range(60):
        drug, dose = random.choice(COVID_VACCINES)
        condition = random.choice(["COVID-19 prevention", "COVID-19 booster immunization", "variant-specific COVID-19 prevention"])
        endpoint = random.choice(["symptomatic COVID-19", "severe COVID-19", "COVID-19 hospitalization", "any SARS-CoV-2 infection"])
        effect_type = "RR"
        secondary = ["neutralizing antibody titers", "T-cell responses", "vaccine efficacy against variants"]

        treatment_n, control_n, total_n = generate_sample_size("COVID-19")

        # Vaccine efficacy typically expressed differently
        ve = round(random.uniform(55, 95), 1)
        ci_lo_ve = round(ve - random.uniform(5, 15), 1)
        ci_hi_ve = round(min(99.9, ve + random.uniform(3, 10)), 1)

        baseline = generate_baseline_characteristics()

        primary_result = f"Vaccine efficacy against {endpoint} was {ve}% (95% CI {ci_lo_ve}-{ci_hi_ve}). The incidence was {round(random.uniform(0.5, 3.0), 1)}% in the vaccine group vs {round(random.uniform(3.0, 12.0), 1)}% in the placebo group."

        secondary_results = f"Neutralizing antibody titers increased {random.randint(8, 50)}-fold from baseline. Cellular immune responses were detected in {random.randint(80, 98)}% of vaccine recipients."

        additional_baseline = f" {random.randint(20, 50)}% had prior SARS-CoV-2 infection. Median time since last vaccine dose was {random.randint(4, 12)} months."

        trial_data = {
            "acronym": f"INFECT-COVID-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE)),
            "countries": random.randint(5, 15),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": f"prevention of {endpoint}",
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(8, 52),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Pfizer/BioNTech', 'Moderna', 'Novavax', 'Johnson & Johnson', 'Sinovac', 'Bharat Biotech'])}.",
        }

        text = generate_trial_text(trial_data)

        # Convert VE to RR for standardized storage
        rr = round(1 - ve/100, 2)
        ci_lo = round(1 - ci_hi_ve/100, 2)
        ci_hi = round(1 - ci_lo_ve/100, 2)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 202{random.randint(1,5)};{random.randint(380,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - COVID-19",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": "RR", "value": rr, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    return trials, trial_num


def generate_hiv_trials(start_idx):
    """Generate 150 HIV trials."""
    trials = []
    trial_num = start_idx

    # 90 ART trials
    for i in range(90):
        drug, dose = random.choice(HIV_ART)
        condition_data = CONDITION_ENDPOINTS["HIV"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("HIV")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=True)
        baseline = generate_baseline_characteristics()

        treatment_rate = round(random.uniform(85, 96), 1)
        control_rate = round(treatment_rate / effect, 1) if effect > 1 else round(treatment_rate * effect, 1)

        primary_result = f"The primary endpoint of {endpoint} was achieved in {treatment_rate}% of the treatment group vs {control_rate}% of the control group ({effect_type} {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Mean CD4 count increase was {random.randint(150, 350)} cells/mm3. {secondary[0].capitalize()} occurred in {round(random.uniform(0.5, 5.0), 1)}% of participants."

        additional_baseline = f" Mean baseline CD4 count was {random.randint(200, 550)} cells/mm3. Mean HIV-1 RNA was {round(random.uniform(4.2, 5.8), 1)} log10 copies/mL."

        trial_data = {
            "acronym": f"INFECT-HIV-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE)),
            "countries": random.randint(8, 30),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.choice([48, 96, 144]),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Gilead Sciences', 'ViiV Healthcare', 'Merck', 'Janssen', 'Bristol-Myers Squibb'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 202{random.randint(0,5)};{random.randint(380,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - HIV",
            "design": "Non-inferiority" if random.random() > 0.5 else "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": effect_type, "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    # 60 prevention trials
    for i in range(60):
        drug, dose = random.choice(HIV_PREVENTION)
        condition_data = CONDITION_ENDPOINTS["HIV"]
        condition = "HIV-1 prevention in high-risk individuals"
        endpoint = "HIV-1 acquisition"
        effect_type = "HR"
        secondary = ["adherence rate", "drug resistance in breakthrough infections", "STI incidence"]

        treatment_n, control_n, total_n = generate_sample_size("HIV")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=False)
        baseline = generate_baseline_characteristics()

        incidence_control = round(random.uniform(2.0, 6.0), 2)
        incidence_treatment = round(incidence_control * effect, 2)

        primary_result = f"HIV-1 incidence was {incidence_treatment} per 100 person-years in the treatment group vs {incidence_control} per 100 person-years in the control group ({effect_type} {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Adherence to the prevention regimen was {random.randint(75, 95)}%. No treatment-emergent resistance was detected in breakthrough infections."

        additional_baseline = f" {random.randint(60, 90)}% reported condomless receptive anal intercourse. {random.randint(20, 40)}% had a history of STI in the past year."

        trial_data = {
            "acronym": f"INFECT-HIV-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE)),
            "countries": random.randint(5, 15),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.choice([52, 96, 144]),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Gilead Sciences', 'ViiV Healthcare', 'NIAID', 'Bill & Melinda Gates Foundation'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 202{random.randint(0,5)};{random.randint(380,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - HIV Prevention",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": effect_type, "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    return trials, trial_num


def generate_hepatitis_trials(start_idx):
    """Generate 150 hepatitis trials (HCV and HBV)."""
    trials = []
    trial_num = start_idx

    # 85 HCV trials
    for i in range(85):
        drug, dose = random.choice(HCV_DAAS)
        condition_data = CONDITION_ENDPOINTS["HCV"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("HCV")

        # HCV DAAs have very high SVR rates
        svr_treatment = round(random.uniform(94, 99.5), 1)
        svr_control = round(random.uniform(85, 94), 1)
        effect = round(svr_treatment / svr_control, 2)
        ci_lo = round(effect - random.uniform(0.02, 0.08), 2)
        ci_hi = round(effect + random.uniform(0.02, 0.06), 2)

        baseline = generate_baseline_characteristics()

        primary_result = f"{endpoint} was achieved in {svr_treatment}% of patients in the treatment group vs {svr_control}% in the control group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Relapse occurred in {round(random.uniform(0.5, 4.0), 1)}% of treatment responders. ALT normalized in {random.randint(85, 98)}% of patients."

        cirrhosis_pct = random.randint(15, 45)
        additional_baseline = f" {cirrhosis_pct}% had compensated cirrhosis. Mean baseline HCV RNA was {round(random.uniform(5.5, 7.0), 1)} log10 IU/mL."

        treatment_duration = random.choice([8, 12, 16, 24])

        trial_data = {
            "acronym": f"INFECT-HCV-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": f"{dose} for {treatment_duration} weeks",
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:3])),
            "countries": random.randint(5, 20),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": treatment_duration + 12,
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Gilead Sciences', 'AbbVie', 'Merck', 'Bristol-Myers Squibb', 'Janssen'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(18,24)};{random.randint(370,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Hepatitis C",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": "RR", "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    # 65 HBV trials
    for i in range(65):
        drug, dose = random.choice(HBV_DRUGS)
        condition_data = CONDITION_ENDPOINTS["HBV"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("HBV")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=True)
        baseline = generate_baseline_characteristics()

        treatment_rate = round(random.uniform(25, 65), 1)
        control_rate = round(treatment_rate / effect, 1)

        primary_result = f"The primary endpoint of {endpoint} was achieved in {treatment_rate}% of the treatment group vs {control_rate}% of the control group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"HBV DNA was undetectable in {random.randint(70, 95)}% of treatment recipients. Mean HBsAg reduction was {round(random.uniform(0.5, 2.5), 1)} log10 IU/mL."

        additional_baseline = f" Mean baseline HBV DNA was {round(random.uniform(5.0, 8.0), 1)} log10 IU/mL. Mean ALT was {random.randint(60, 150)} U/L."

        trial_data = {
            "acronym": f"INFECT-HBV-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:3])),
            "countries": random.randint(5, 18),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.choice([48, 96, 144]),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Gilead Sciences', 'GSK', 'Janssen', 'Arrowhead Pharmaceuticals', 'Assembly Biosciences'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(19,25)};{random.randint(370,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Hepatitis B",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": "RR", "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    return trials, trial_num


def generate_bacterial_trials(start_idx):
    """Generate 200 bacterial infection trials."""
    trials = []
    trial_num = start_idx

    # 70 gram-positive trials
    for i in range(70):
        drug, dose = random.choice(ANTIBIOTICS_GRAM_POS)
        condition_data = CONDITION_ENDPOINTS["bacterial_gram_pos"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("bacterial")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=True)
        baseline = generate_baseline_characteristics()

        treatment_rate = round(random.uniform(78, 92), 1)
        control_rate = round(treatment_rate / effect, 1)

        primary_result = f"The primary endpoint of {endpoint} was achieved in {treatment_rate}% of the treatment group vs {control_rate}% of the comparator group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Microbiological eradication was achieved in {random.randint(75, 95)}% of evaluable patients. {secondary[0].capitalize()} was {round(random.uniform(2, 5), 1)} days."

        mrsa_pct = random.randint(20, 60)
        additional_baseline = f" {mrsa_pct}% of isolates were MRSA. Mean lesion size was {random.randint(50, 200)} cm2."

        comparator = random.choice(["vancomycin", "linezolid", "daptomycin", "ceftaroline"])

        trial_data = {
            "acronym": f"INFECT-BACT-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:3])),
            "countries": random.randint(8, 25),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(2, 8),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Pfizer', 'Merck', 'AbbVie', 'Paratek', 'Melinta', 'Nabriva', 'Allergan'])}.",
        }

        # Modify text to mention comparator instead of placebo
        text = generate_trial_text(trial_data).replace("placebo", comparator)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(18,25)};{random.randint(370,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Bacterial (Gram-positive)",
            "design": "Non-inferiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": "RR", "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    # 70 gram-negative trials
    for i in range(70):
        drug, dose = random.choice(ANTIBIOTICS_GRAM_NEG)
        condition_data = CONDITION_ENDPOINTS["bacterial_gram_neg"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("bacterial")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=True)
        baseline = generate_baseline_characteristics()

        treatment_rate = round(random.uniform(70, 88), 1)
        control_rate = round(treatment_rate / effect, 1)

        primary_result = f"The primary endpoint of {endpoint} was achieved in {treatment_rate}% of the treatment group vs {control_rate}% of the comparator group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Per-pathogen response rates ranged from {random.randint(65, 85)}% to {random.randint(86, 95)}%. {secondary[1].capitalize()} occurred in {round(random.uniform(1, 8), 1)}% of patients."

        cre_pct = random.randint(15, 50)
        additional_baseline = f" {cre_pct}% had carbapenem-resistant isolates. APACHE II score was {round(random.uniform(12, 22), 1)}."

        comparator = random.choice(["meropenem", "imipenem", "piperacillin-tazobactam", "ceftazidime"])

        trial_data = {
            "acronym": f"INFECT-BACT-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:3])),
            "countries": random.randint(10, 30),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(2, 6),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Shionogi', 'Merck', 'Pfizer', 'Entasis', 'Achaogen', 'Tetraphase'])}.",
        }

        text = generate_trial_text(trial_data).replace("placebo", comparator)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(18,25)};{random.randint(370,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Bacterial (Gram-negative)",
            "design": "Non-inferiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": "RR", "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    # 60 resistant pathogen trials
    for i in range(60):
        drug, dose = random.choice(ANTIBIOTICS_RESISTANT)
        condition_data = CONDITION_ENDPOINTS["bacterial_gram_neg"]
        condition = random.choice(["carbapenem-resistant Enterobacterales infection", "ESBL-producing organism infection",
                                   "pan-drug resistant Acinetobacter infection", "difficult-to-treat resistance infection"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("bacterial")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=True)
        baseline = generate_baseline_characteristics()

        treatment_rate = round(random.uniform(55, 78), 1)
        control_rate = round(treatment_rate / effect, 1)

        primary_result = f"The primary endpoint of {endpoint} was achieved in {treatment_rate}% of the treatment group vs {control_rate}% of the best available therapy group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P=0.00{random.randint(1,9)})."

        secondary_results = f"Mortality at day 28 was {random.randint(8, 25)}% vs {random.randint(20, 40)}% with best available therapy. Microbiological eradication was {random.randint(50, 80)}%."

        additional_baseline = f" All patients had infections caused by carbapenem-resistant organisms. {random.randint(40, 70)}% were in the ICU."

        trial_data = {
            "acronym": f"INFECT-BACT-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:2])),
            "countries": random.randint(5, 15),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(4, 12),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Qpex Biopharma', 'Venatorx', 'Spero Therapeutics', 'Entasis', 'Iterum'])}.",
        }

        text = generate_trial_text(trial_data).replace("placebo", "best available therapy")

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(20,25)};{random.randint(380,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Bacterial (Resistant)",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": "RR", "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    return trials, trial_num


def generate_fungal_trials(start_idx):
    """Generate 100 fungal infection trials."""
    trials = []
    trial_num = start_idx

    for i in range(100):
        drug, dose = random.choice(ANTIFUNGALS)
        condition_data = CONDITION_ENDPOINTS["fungal"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("fungal")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=True)
        baseline = generate_baseline_characteristics()

        treatment_rate = round(random.uniform(55, 85), 1)
        control_rate = round(treatment_rate / effect, 1)

        primary_result = f"The primary endpoint of {endpoint} was achieved in {treatment_rate}% of the treatment group vs {control_rate}% of the comparator group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Time to clinical response was median {random.randint(5, 15)} days. {secondary[0].capitalize()} was observed in {random.randint(60, 90)}% of patients."

        underlying = random.choice(["hematologic malignancy", "solid organ transplant", "stem cell transplant", "AIDS", "prolonged neutropenia"])
        additional_baseline = f" {random.randint(60, 90)}% had {underlying}. Median duration of neutropenia was {random.randint(7, 21)} days."

        comparator = random.choice(["voriconazole", "liposomal amphotericin B", "caspofungin", "fluconazole"])

        trial_data = {
            "acronym": f"INFECT-FUNG-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:2])),
            "countries": random.randint(8, 20),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(6, 16),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Pfizer', 'Astellas', 'Cidara', 'Amplyx', 'F2G', 'Mycovia', 'Scynexis'])}.",
        }

        text = generate_trial_text(trial_data).replace("placebo", comparator)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(18,25)};{random.randint(370,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Fungal",
            "design": "Non-inferiority" if random.random() > 0.4 else "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": "RR", "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    return trials, trial_num


def generate_tb_trials(start_idx):
    """Generate 100 TB trials."""
    trials = []
    trial_num = start_idx

    for i in range(100):
        drug, dose = random.choice(TB_DRUGS)
        condition_data = CONDITION_ENDPOINTS["TB"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("TB")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=True)
        baseline = generate_baseline_characteristics()

        treatment_rate = round(random.uniform(75, 95), 1)
        control_rate = round(treatment_rate / effect, 1)

        primary_result = f"The primary endpoint of {endpoint} was achieved in {treatment_rate}% of the treatment group vs {control_rate}% of the control group ({effect_type} {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Time to culture conversion was median {random.randint(4, 12)} weeks vs {random.randint(8, 20)} weeks. {secondary[1].capitalize()} was {round(random.uniform(2, 10), 1)}%."

        hiv_pct = random.randint(10, 40)
        additional_baseline = f" {hiv_pct}% had HIV coinfection. Cavitary disease was present in {random.randint(30, 60)}% of patients."

        trial_data = {
            "acronym": f"INFECT-TB-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:2])),
            "countries": random.randint(5, 15),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.choice([24, 52, 78, 104]),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['TB Alliance', 'Janssen', 'Otsuka', 'NIAID', 'Bill & Melinda Gates Foundation', 'Unitaid'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(18,25)};{random.randint(370,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Tuberculosis",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": effect_type, "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": random.random() > 0.4,
            }
        }
        trials.append(trial)
        trial_num += 1

    return trials, trial_num


def generate_other_viral_trials(start_idx):
    """Generate 100 other viral trials (influenza, RSV, herpes)."""
    trials = []
    trial_num = start_idx

    # 40 influenza trials
    for i in range(40):
        drug, dose = random.choice(INFLUENZA_DRUGS)
        condition_data = CONDITION_ENDPOINTS["influenza"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("viral")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=False if effect_type == "HR" else True)
        baseline = generate_baseline_characteristics()

        if effect_type == "HR":
            treatment_time = round(random.uniform(48, 72), 1)
            control_time = round(treatment_time / effect, 1)
            primary_result = f"Time to {endpoint} was {treatment_time} hours in the treatment group vs {control_time} hours in the placebo group (HR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."
        else:
            treatment_rate = round(random.uniform(5, 15), 1)
            control_rate = round(treatment_rate / effect, 1) if effect < 1 else round(treatment_rate * effect, 1)
            primary_result = f"{endpoint.capitalize()} occurred in {treatment_rate}% of the treatment group vs {control_rate}% of the placebo group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Duration of fever was reduced by {round(random.uniform(12, 36), 1)} hours. Return to normal activities was {round(random.uniform(1, 2.5), 1)} days earlier."

        additional_baseline = f" Median time from symptom onset was {random.randint(24, 48)} hours. {random.randint(40, 70)}% had received influenza vaccination."

        trial_data = {
            "acronym": f"INFECT-VIRAL-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:2])),
            "countries": random.randint(5, 15),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(2, 8),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['Shionogi', 'Roche', 'Janssen', 'Aviragen', 'Visterra'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(18,25)};{random.randint(370,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Influenza",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": effect_type, "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    # 30 RSV trials
    for i in range(30):
        drug, dose = random.choice(RSV_DRUGS)
        condition_data = CONDITION_ENDPOINTS["RSV"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("viral")
        effect, ci_lo, ci_hi = generate_effect_size("RR", is_favorable=False)
        baseline = generate_baseline_characteristics()
        baseline["age_mean"] = round(random.uniform(0.5, 75.0), 1)  # Can be infants or elderly

        treatment_rate = round(random.uniform(2, 10), 1)
        control_rate = round(treatment_rate / effect, 1)

        primary_result = f"The primary endpoint of {endpoint} occurred in {treatment_rate}% of the treatment group vs {control_rate}% of the control group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Hospitalization duration was {round(random.uniform(2, 5), 1)} days vs {round(random.uniform(4, 8), 1)} days. {secondary[0].capitalize()} was reduced by {random.randint(40, 70)}%."

        additional_baseline = f" {random.randint(30, 60)}% were born prematurely. {random.randint(20, 40)}% had chronic lung disease."

        trial_data = {
            "acronym": f"INFECT-VIRAL-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:2])),
            "countries": random.randint(5, 15),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(12, 52),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['AstraZeneca', 'Sanofi', 'Merck', 'Janssen', 'Enanta', 'ReViral'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(20,25)};{random.randint(380,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - RSV",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": "RR", "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    # 30 herpes trials
    for i in range(30):
        drug, dose = random.choice(HERPES_DRUGS)
        condition_data = CONDITION_ENDPOINTS["herpes"]
        condition = random.choice(condition_data["conditions"])
        endpoint, effect_type = random.choice(condition_data["primary_endpoints"])
        secondary = random.sample(condition_data["secondary_endpoints"], 2)

        treatment_n, control_n, total_n = generate_sample_size("viral")
        effect, ci_lo, ci_hi = generate_effect_size(effect_type, is_favorable=True if effect_type == "RR" else False)
        baseline = generate_baseline_characteristics()

        if effect_type == "HR":
            treatment_time = round(random.uniform(3, 7), 1)
            control_time = round(treatment_time / effect, 1)
            primary_result = f"Time to {endpoint} was {treatment_time} days in the treatment group vs {control_time} days in the placebo group (HR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."
        else:
            treatment_rate = round(random.uniform(70, 95), 1)
            control_rate = round(treatment_rate / effect, 1)
            primary_result = f"{endpoint.capitalize()} was achieved in {treatment_rate}% of the treatment group vs {control_rate}% of the placebo group (RR {effect}; 95% CI {ci_lo}-{ci_hi}; P<0.001)."

        secondary_results = f"Viral shedding duration was reduced by {round(random.uniform(1, 4), 1)} days. {secondary[0].capitalize()} was {round(random.uniform(20, 50), 1)}% lower."

        additional_baseline = f" Mean number of recurrences in past year was {round(random.uniform(4, 10), 1)}. {random.randint(50, 80)}% were on suppressive therapy previously."

        trial_data = {
            "acronym": f"INFECT-VIRAL-{str(trial_num).zfill(3)}",
            "treatment_name": drug,
            "treatment_dose": dose,
            "condition": condition,
            "sites": random.randint(*random.choice(SITES_RANGE[:2])),
            "countries": random.randint(5, 15),
            "total_n": total_n,
            "treatment_n": treatment_n,
            "control_n": control_n,
            "baseline": baseline,
            "additional_baseline": additional_baseline,
            "primary_endpoint": endpoint,
            "primary_result": primary_result,
            "secondary_results": secondary_results,
            "followup_weeks": random.randint(12, 52),
            "nct": generate_nct(),
            "funding_text": f" This trial was funded by {random.choice(['AiCuris', 'Maruho', 'Chimerix', 'Takeda', 'GlaxoSmithKline'])}.",
        }

        text = generate_trial_text(trial_data)

        trial = {
            "id": trial_data["acronym"],
            "source": f"{random.choice(AUTHOR_FIRST)} {random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} et al. {random.choice(JOURNALS)} 20{random.randint(18,25)};{random.randint(370,395)}:{random.randint(100,2000)}-{random.randint(2001,3000)}",
            "domain": "Infectious Disease - Herpesvirus",
            "design": "Superiority",
            "text": text,
            "groundTruth": {
                "study": {"acronym": trial_data["acronym"]},
                "treatment": {"n": treatment_n},
                "control": {"n": control_n},
                "totalN": total_n,
                "primaryEffect": {"type": effect_type, "value": effect, "ciLo": ci_lo, "ciHi": ci_hi},
                "baseline": {
                    "ageMean": baseline["age_mean"],
                    "malePercent": baseline["male_pct"],
                },
                "followupWeeks": trial_data["followup_weeks"],
                "registration": trial_data["nct"],
                "fundingIndustry": True,
            }
        }
        trials.append(trial)
        trial_num += 1

    return trials, trial_num


def format_trial_for_js(trial):
    """Format a trial object as JavaScript code."""
    # Escape backticks and backslashes in text
    text = trial["text"].replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    js = f"""    {{
        id: '{trial["id"]}',
        source: '{trial["source"]}',
        domain: '{trial["domain"]}',
        design: '{trial["design"]}',
        text: `{text}`,

        groundTruth: {{
            study: {{ acronym: '{trial["groundTruth"]["study"]["acronym"]}' }},
            treatment: {{ n: {trial["groundTruth"]["treatment"]["n"]} }},
            control: {{ n: {trial["groundTruth"]["control"]["n"]} }},
            totalN: {trial["groundTruth"]["totalN"]},
            primaryEffect: {{ type: '{trial["groundTruth"]["primaryEffect"]["type"]}', value: {trial["groundTruth"]["primaryEffect"]["value"]}, ciLo: {trial["groundTruth"]["primaryEffect"]["ciLo"]}, ciHi: {trial["groundTruth"]["primaryEffect"]["ciHi"]} }},
            baseline: {{
                ageMean: {trial["groundTruth"]["baseline"]["ageMean"]},
                malePercent: {trial["groundTruth"]["baseline"]["malePercent"]},
            }},
            followupWeeks: {trial["groundTruth"]["followupWeeks"]},
            registration: '{trial["groundTruth"]["registration"]}',
            fundingIndustry: {"true" if trial["groundTruth"]["fundingIndustry"] else "false"},
        }}
    }}"""
    return js


def main():
    """Main function to generate all trials and append to validation file."""
    print("Generating 1000 infectious disease RCT trials...")

    all_trials = []
    trial_num = 1

    # Generate COVID-19 trials (200)
    print("Generating COVID-19 trials...")
    covid_trials, trial_num = generate_covid_trials(trial_num)
    all_trials.extend(covid_trials)
    print(f"  Generated {len(covid_trials)} COVID-19 trials")

    # Generate HIV trials (150)
    print("Generating HIV trials...")
    hiv_trials, trial_num = generate_hiv_trials(trial_num)
    all_trials.extend(hiv_trials)
    print(f"  Generated {len(hiv_trials)} HIV trials")

    # Generate Hepatitis trials (150)
    print("Generating Hepatitis trials...")
    hep_trials, trial_num = generate_hepatitis_trials(trial_num)
    all_trials.extend(hep_trials)
    print(f"  Generated {len(hep_trials)} Hepatitis trials")

    # Generate Bacterial trials (200)
    print("Generating Bacterial infection trials...")
    bact_trials, trial_num = generate_bacterial_trials(trial_num)
    all_trials.extend(bact_trials)
    print(f"  Generated {len(bact_trials)} Bacterial trials")

    # Generate Fungal trials (100)
    print("Generating Fungal infection trials...")
    fung_trials, trial_num = generate_fungal_trials(trial_num)
    all_trials.extend(fung_trials)
    print(f"  Generated {len(fung_trials)} Fungal trials")

    # Generate TB trials (100)
    print("Generating TB trials...")
    tb_trials, trial_num = generate_tb_trials(trial_num)
    all_trials.extend(tb_trials)
    print(f"  Generated {len(tb_trials)} TB trials")

    # Generate Other viral trials (100)
    print("Generating Other viral trials...")
    viral_trials, trial_num = generate_other_viral_trials(trial_num)
    all_trials.extend(viral_trials)
    print(f"  Generated {len(viral_trials)} Other viral trials")

    print(f"\nTotal trials generated: {len(all_trials)}")

    # Read existing file
    target_file = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"
    print(f"\nReading existing file: {target_file}")

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the position to insert new trials (before the closing ];)
    # Look for the last trial's closing brace followed by the array close
    insert_marker = "];"

    # Find the last occurrence of ]; which closes GROUND_TRUTH_CASES
    last_bracket_pos = content.rfind("];")

    if last_bracket_pos == -1:
        print("ERROR: Could not find closing bracket of GROUND_TRUTH_CASES array")
        return

    # Generate JavaScript code for new trials
    print("Formatting trials as JavaScript...")
    trials_js = ",\n".join(format_trial_for_js(trial) for trial in all_trials)

    # Insert new trials before the closing ];
    new_content = content[:last_bracket_pos] + ",\n" + trials_js + "\n" + content[last_bracket_pos:]

    # Write updated file
    print(f"Writing updated file...")
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nSuccessfully added {len(all_trials)} infectious disease trials to {target_file}")

    # Print summary
    print("\n=== SUMMARY ===")
    print(f"COVID-19 trials: {len(covid_trials)} (antivirals: 70, monoclonals: 70, vaccines: 60)")
    print(f"HIV trials: {len(hiv_trials)} (ART: 90, prevention: 60)")
    print(f"Hepatitis trials: {len(hep_trials)} (HCV: 85, HBV: 65)")
    print(f"Bacterial trials: {len(bact_trials)} (gram-pos: 70, gram-neg: 70, resistant: 60)")
    print(f"Fungal trials: {len(fung_trials)}")
    print(f"TB trials: {len(tb_trials)}")
    print(f"Other viral trials: {len(viral_trials)} (influenza: 40, RSV: 30, herpes: 30)")
    print(f"TOTAL: {len(all_trials)} trials")


if __name__ == "__main__":
    main()
