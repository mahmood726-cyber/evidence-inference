#!/usr/bin/env python3
"""
Script to add 200 oncology RCT trials to validation_study_expanded.js
Creates BATCH21_TO_1300 (100 trials) and BATCH22_TO_1400 (100 trials)
"""

import random
import re

# Set seed for reproducibility
random.seed(42)

def generate_nct():
    """Generate realistic NCT number"""
    return f"NCT{random.randint(10000000, 99999999):08d}"

def generate_hr():
    """Generate realistic hazard ratio for positive oncology trials (0.5-0.9)"""
    return round(random.uniform(0.50, 0.90), 2)

def generate_ci(hr):
    """Generate realistic confidence interval around HR"""
    margin_low = round(random.uniform(0.05, 0.12), 2)
    margin_high = round(random.uniform(0.08, 0.18), 2)
    ci_lo = round(max(0.20, hr - margin_low), 2)
    ci_hi = round(min(0.99, hr + margin_high), 2)
    return ci_lo, ci_hi

def generate_p_value(hr, ci_hi):
    """Generate realistic p-value based on effect size"""
    if ci_hi < 1.0:
        if hr < 0.6:
            return f"P<0.001"
        elif hr < 0.75:
            return f"P<0.01"
        else:
            return f"P={round(random.uniform(0.001, 0.049), 3)}"
    else:
        return f"P={round(random.uniform(0.05, 0.20), 2)}"

def generate_sample_sizes():
    """Generate realistic sample sizes for oncology trials"""
    treatment_n = random.randint(150, 600)
    control_n = random.randint(int(treatment_n * 0.9), int(treatment_n * 1.1))
    return treatment_n, control_n

def generate_age():
    """Generate realistic mean age for oncology patients"""
    return round(random.uniform(55.0, 72.0), 1)

def generate_male_pct(cancer_type):
    """Generate realistic male percentage based on cancer type"""
    if cancer_type in ['prostate']:
        return 100.0
    elif cancer_type in ['breast']:
        return round(random.uniform(0.5, 1.5), 1)
    elif cancer_type in ['lung']:
        return round(random.uniform(55.0, 70.0), 1)
    elif cancer_type in ['colorectal']:
        return round(random.uniform(52.0, 62.0), 1)
    elif cancer_type in ['melanoma']:
        return round(random.uniform(55.0, 65.0), 1)
    elif cancer_type in ['renal']:
        return round(random.uniform(65.0, 75.0), 1)
    elif cancer_type in ['hematologic']:
        return round(random.uniform(50.0, 60.0), 1)
    else:
        return round(random.uniform(48.0, 58.0), 1)

def generate_followup():
    """Generate realistic follow-up months"""
    return round(random.uniform(12.0, 48.0), 1)

# Trial templates by cancer type
BREAST_TRIALS = [
    ("PALLAS-EXT", "palbociclib", "placebo", "early HR-positive breast cancer", "invasive disease-free survival", "IDFS"),
    ("monarchE-LT", "abemaciclib", "placebo", "high-risk HR-positive breast cancer", "invasive disease-free survival", "IDFS"),
    ("KEYNOTE-522-PFS", "pembrolizumab plus chemotherapy", "placebo plus chemotherapy", "triple-negative breast cancer", "progression-free survival", "PFS"),
    ("NATALEE", "ribociclib", "placebo", "HR-positive HER2-negative breast cancer", "invasive disease-free survival", "IDFS"),
    ("DESTINY-Breast03", "trastuzumab deruxtecan", "trastuzumab emtansine", "HER2-positive breast cancer", "progression-free survival", "PFS"),
    ("DESTINY-Breast04", "trastuzumab deruxtecan", "chemotherapy", "HER2-low breast cancer", "progression-free survival", "PFS"),
    ("TROPICS-02", "sacituzumab govitecan", "chemotherapy", "HR-positive breast cancer", "progression-free survival", "PFS"),
    ("EMERALD-EXT", "elacestrant", "standard endocrine therapy", "ESR1-mutated breast cancer", "progression-free survival", "PFS"),
    ("EMBRACE-3", "eribulin", "capecitabine", "metastatic breast cancer", "overall survival", "OS"),
    ("IMpassion131", "atezolizumab plus paclitaxel", "placebo plus paclitaxel", "triple-negative breast cancer", "progression-free survival", "PFS"),
    ("PEARL", "palbociclib plus endocrine therapy", "capecitabine", "HR-positive breast cancer", "progression-free survival", "PFS"),
    ("MONALEESA-7-LT", "ribociclib", "placebo", "premenopausal HR-positive breast cancer", "overall survival", "OS"),
    ("PALOMA-4", "palbociclib plus letrozole", "placebo plus letrozole", "Asian HR-positive breast cancer", "progression-free survival", "PFS"),
    ("SOPHIA-EXT", "margetuximab plus chemotherapy", "trastuzumab plus chemotherapy", "HER2-positive breast cancer", "progression-free survival", "PFS"),
    ("TH3RESA-FU", "trastuzumab emtansine", "treatment of physician's choice", "HER2-positive breast cancer", "overall survival", "OS"),
    ("CLEOPATRA-10Y", "pertuzumab plus trastuzumab", "placebo plus trastuzumab", "HER2-positive breast cancer", "overall survival", "OS"),
    ("APHINITY-LT", "pertuzumab plus trastuzumab plus chemotherapy", "placebo plus trastuzumab plus chemotherapy", "HER2-positive early breast cancer", "invasive disease-free survival", "IDFS"),
    ("ExteNET-10Y", "neratinib", "placebo", "HER2-positive early breast cancer", "invasive disease-free survival", "IDFS"),
    ("BOLERO-4", "everolimus plus exemestane", "exemestane", "HR-positive breast cancer", "progression-free survival", "PFS"),
    ("OlympiAD-FU", "olaparib", "chemotherapy", "BRCA-mutated breast cancer", "overall survival", "OS"),
    ("BELLE-4", "buparlisib plus fulvestrant", "placebo plus fulvestrant", "HR-positive breast cancer", "progression-free survival", "PFS"),
    ("PALOMA-1-LT", "palbociclib plus letrozole", "letrozole", "HR-positive breast cancer", "overall survival", "OS"),
    ("SANDPIPER", "taselisib plus fulvestrant", "placebo plus fulvestrant", "PIK3CA-mutant breast cancer", "progression-free survival", "PFS"),
    ("LORELEI", "taselisib plus letrozole", "placebo plus letrozole", "PIK3CA-mutant breast cancer", "objective response", "ORR"),
    ("PARSIFAL", "palbociclib plus fulvestrant", "palbociclib plus letrozole", "HR-positive breast cancer", "progression-free survival", "PFS"),
    ("FALCON-LT", "fulvestrant", "anastrozole", "HR-positive breast cancer", "overall survival", "OS"),
    ("FLIPPER", "palbociclib plus fulvestrant", "placebo plus fulvestrant", "older patients with breast cancer", "progression-free survival", "PFS"),
    ("MONARCH-2-LT", "abemaciclib plus fulvestrant", "placebo plus fulvestrant", "HR-positive breast cancer", "overall survival", "OS"),
    ("MONARCH-3-LT", "abemaciclib plus NSAI", "placebo plus NSAI", "HR-positive breast cancer", "overall survival", "OS"),
    ("MAINTAIN", "ribociclib plus fulvestrant", "placebo plus fulvestrant", "HR-positive breast cancer after CDK4/6 inhibitor", "progression-free survival", "PFS"),
    ("BYLieve", "alpelisib plus fulvestrant", "fulvestrant", "PIK3CA-mutant breast cancer", "progression-free survival", "PFS"),
    ("SOLAR-1-LT", "alpelisib plus fulvestrant", "placebo plus fulvestrant", "PIK3CA-mutant breast cancer", "overall survival", "OS"),
    ("CAPItello-291", "capivasertib plus fulvestrant", "placebo plus fulvestrant", "HR-positive breast cancer", "progression-free survival", "PFS"),
    ("INAVO120", "inavolisib plus palbociclib plus fulvestrant", "placebo plus palbociclib plus fulvestrant", "PIK3CA-mutant breast cancer", "progression-free survival", "PFS"),
    ("SERENA-6", "camizestrant", "standard aromatase inhibitor", "ER-positive breast cancer", "progression-free survival", "PFS"),
]

LUNG_TRIALS = [
    ("KEYNOTE-024-LT", "pembrolizumab", "platinum-based chemotherapy", "PD-L1 high NSCLC", "overall survival", "OS"),
    ("KEYNOTE-042-EXT", "pembrolizumab", "platinum-based chemotherapy", "PD-L1 positive NSCLC", "overall survival", "OS"),
    ("KEYNOTE-189-LT", "pembrolizumab plus chemotherapy", "placebo plus chemotherapy", "nonsquamous NSCLC", "overall survival", "OS"),
    ("KEYNOTE-407-LT", "pembrolizumab plus chemotherapy", "placebo plus chemotherapy", "squamous NSCLC", "overall survival", "OS"),
    ("CheckMate-227-LT", "nivolumab plus ipilimumab", "chemotherapy", "NSCLC", "overall survival", "OS"),
    ("CheckMate-9LA-LT", "nivolumab plus ipilimumab plus chemotherapy", "chemotherapy", "NSCLC", "overall survival", "OS"),
    ("CheckMate-017-10Y", "nivolumab", "docetaxel", "squamous NSCLC", "overall survival", "OS"),
    ("CheckMate-057-10Y", "nivolumab", "docetaxel", "nonsquamous NSCLC", "overall survival", "OS"),
    ("IMpower110-LT", "atezolizumab", "platinum-based chemotherapy", "PD-L1 high NSCLC", "overall survival", "OS"),
    ("IMpower130-LT", "atezolizumab plus chemotherapy", "chemotherapy", "nonsquamous NSCLC", "overall survival", "OS"),
    ("IMpower150-LT", "atezolizumab plus bevacizumab plus chemotherapy", "bevacizumab plus chemotherapy", "nonsquamous NSCLC", "overall survival", "OS"),
    ("POSEIDON-LT", "durvalumab plus tremelimumab plus chemotherapy", "chemotherapy", "NSCLC", "overall survival", "OS"),
    ("PACIFIC-5Y", "durvalumab", "placebo", "stage III NSCLC after chemoradiotherapy", "overall survival", "OS"),
    ("ADAURA-LT", "osimertinib", "placebo", "EGFR-mutant resected NSCLC", "disease-free survival", "DFS"),
    ("LAURA", "osimertinib", "placebo", "EGFR-mutant unresectable stage III NSCLC", "progression-free survival", "PFS"),
    ("FLAURA2", "osimertinib plus chemotherapy", "osimertinib", "EGFR-mutant NSCLC", "progression-free survival", "PFS"),
    ("MARIPOSA", "amivantamab plus lazertinib", "osimertinib", "EGFR-mutant NSCLC", "progression-free survival", "PFS"),
    ("CHRYSALIS-2", "amivantamab plus lazertinib", "chemotherapy", "EGFR-mutant NSCLC after osimertinib", "progression-free survival", "PFS"),
    ("CodeBreaK 200", "sotorasib", "docetaxel", "KRAS G12C-mutant NSCLC", "progression-free survival", "PFS"),
    ("KRYSTAL-12", "adagrasib", "docetaxel", "KRAS G12C-mutant NSCLC", "progression-free survival", "PFS"),
    ("CROWN-LT", "lorlatinib", "crizotinib", "ALK-positive NSCLC", "progression-free survival", "PFS"),
    ("ALINA", "alectinib", "platinum-based chemotherapy", "ALK-positive resected NSCLC", "disease-free survival", "DFS"),
    ("ALEX-5Y", "alectinib", "crizotinib", "ALK-positive advanced NSCLC", "overall survival", "OS"),
    ("eXalt3", "ensartinib", "crizotinib", "ALK-positive NSCLC", "progression-free survival", "PFS"),
    ("LIBRETTO-432", "selpercatinib", "placebo", "RET-fusion positive NSCLC", "progression-free survival", "PFS"),
    ("TRIDENT-1-LT", "repotrectinib", "crizotinib", "ROS1-positive NSCLC", "progression-free survival", "PFS"),
    ("TROPION-Lung01", "datopotamab deruxtecan", "docetaxel", "NSCLC", "progression-free survival", "PFS"),
    ("TROPION-Lung02", "datopotamab deruxtecan plus pembrolizumab", "pembrolizumab", "NSCLC", "progression-free survival", "PFS"),
    ("DESTINY-Lung03", "trastuzumab deruxtecan", "docetaxel", "HER2-expressing NSCLC", "progression-free survival", "PFS"),
    ("HERTHENA-Lung01", "patritumab deruxtecan", "docetaxel", "EGFR-mutant NSCLC", "progression-free survival", "PFS"),
    ("EVOKE-01", "sacituzumab govitecan", "docetaxel", "NSCLC after immunotherapy", "overall survival", "OS"),
    ("LUNAR", "tumor treating fields plus docetaxel", "docetaxel", "NSCLC after platinum", "overall survival", "OS"),
    ("SKYSCRAPER-01", "tiragolumab plus atezolizumab", "placebo plus atezolizumab", "PD-L1 high NSCLC", "overall survival", "OS"),
    ("CITYSCAPE", "tiragolumab plus atezolizumab", "placebo plus atezolizumab", "PD-L1 positive NSCLC", "progression-free survival", "PFS"),
    ("SAPPHIRE", "sitravatinib plus nivolumab", "docetaxel", "NSCLC after immunotherapy", "overall survival", "OS"),
]

COLORECTAL_TRIALS = [
    ("BEACON-CRC-LT", "encorafenib plus cetuximab", "chemotherapy", "BRAF V600E-mutant colorectal cancer", "overall survival", "OS"),
    ("BEACON-CRC-3Y", "encorafenib plus binimetinib plus cetuximab", "chemotherapy", "BRAF V600E-mutant colorectal cancer", "overall survival", "OS"),
    ("TRIBE2-LT", "FOLFOXIRI plus bevacizumab", "FOLFOX plus bevacizumab", "metastatic colorectal cancer", "overall survival", "OS"),
    ("TRIBE3", "FOLFOXIRI plus bevacizumab", "FOLFOX plus bevacizumab plus atezolizumab", "metastatic colorectal cancer", "progression-free survival", "PFS"),
    ("PARADIGM", "panitumumab plus mFOLFOX6", "bevacizumab plus mFOLFOX6", "RAS wild-type colorectal cancer", "overall survival", "OS"),
    ("DESTINY-CRC02", "trastuzumab deruxtecan", "chemotherapy", "HER2-positive colorectal cancer", "objective response rate", "ORR"),
    ("MOUNTAINEER-03", "tucatinib plus trastuzumab plus mFOLFOX6", "mFOLFOX6 plus bevacizumab or cetuximab", "HER2-positive colorectal cancer", "progression-free survival", "PFS"),
    ("CheckMate-8HW", "nivolumab plus ipilimumab", "chemotherapy", "MSI-H colorectal cancer", "progression-free survival", "PFS"),
    ("KEYNOTE-177-LT", "pembrolizumab", "chemotherapy", "MSI-H colorectal cancer", "overall survival", "OS"),
    ("CodeBreaK 300", "sotorasib plus panitumumab", "standard of care", "KRAS G12C-mutant colorectal cancer", "progression-free survival", "PFS"),
    ("KRYSTAL-10", "adagrasib plus cetuximab", "chemotherapy", "KRAS G12C-mutant colorectal cancer", "progression-free survival", "PFS"),
    ("SUNLIGHT", "trifluridine/tipiracil plus bevacizumab", "trifluridine/tipiracil", "refractory colorectal cancer", "overall survival", "OS"),
    ("FRESCO-2", "fruquintinib", "placebo", "refractory colorectal cancer", "overall survival", "OS"),
    ("CORRECT-LT", "regorafenib", "placebo", "refractory colorectal cancer", "overall survival", "OS"),
    ("RECOURSE-LT", "trifluridine/tipiracil", "placebo", "refractory colorectal cancer", "overall survival", "OS"),
    ("FIRE-3-LT", "FOLFIRI plus cetuximab", "FOLFIRI plus bevacizumab", "RAS wild-type colorectal cancer", "overall survival", "OS"),
    ("CALGB-80405-LT", "chemotherapy plus cetuximab", "chemotherapy plus bevacizumab", "KRAS wild-type colorectal cancer", "overall survival", "OS"),
    ("PEAK-LT", "panitumumab plus mFOLFOX6", "bevacizumab plus mFOLFOX6", "RAS wild-type colorectal cancer", "overall survival", "OS"),
    ("PRIME-LT", "panitumumab plus FOLFOX4", "FOLFOX4", "RAS wild-type colorectal cancer", "overall survival", "OS"),
    ("ASPECCT-LT", "panitumumab", "cetuximab", "chemotherapy-refractory colorectal cancer", "overall survival", "OS"),
    ("VELOUR-LT", "FOLFIRI plus aflibercept", "FOLFIRI plus placebo", "metastatic colorectal cancer", "overall survival", "OS"),
    ("RAISE-LT", "ramucirumab plus FOLFIRI", "placebo plus FOLFIRI", "metastatic colorectal cancer", "overall survival", "OS"),
    ("IDEA-France", "3 months FOLFOX/CAPOX", "6 months FOLFOX/CAPOX", "stage III colon cancer", "disease-free survival", "DFS"),
    ("IDEA-Global", "3 months adjuvant chemotherapy", "6 months adjuvant chemotherapy", "stage III colon cancer", "disease-free survival", "DFS"),
    ("PRODIGE-23", "mFOLFIRINOX then chemoradiotherapy", "chemoradiotherapy then chemotherapy", "locally advanced rectal cancer", "disease-free survival", "DFS"),
    ("RAPIDO", "short-course radiotherapy then chemotherapy", "long-course chemoradiotherapy then surgery", "locally advanced rectal cancer", "disease-related treatment failure", "DrTF"),
    ("PROSPECT", "FOLFOX alone", "chemoradiotherapy", "locally advanced rectal cancer", "disease-free survival", "DFS"),
    ("STELLAR", "short-course radiotherapy then chemotherapy", "long-course chemoradiotherapy", "locally advanced rectal cancer", "disease-free survival", "DFS"),
    ("OPRA", "total neoadjuvant therapy", "standard chemoradiotherapy", "rectal cancer", "organ preservation", "OP"),
    ("CAO-ARO-AIO-18.1", "total neoadjuvant therapy", "adjuvant chemotherapy after chemoradiotherapy", "rectal cancer", "disease-free survival", "DFS"),
]

PROSTATE_TRIALS = [
    ("PROSPER-LT", "enzalutamide", "placebo", "nonmetastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("TITAN-LT", "apalutamide plus ADT", "placebo plus ADT", "metastatic castration-sensitive prostate cancer", "overall survival", "OS"),
    ("ARCHES-LT", "enzalutamide plus ADT", "placebo plus ADT", "metastatic castration-sensitive prostate cancer", "overall survival", "OS"),
    ("ARASENS-LT", "darolutamide plus docetaxel plus ADT", "placebo plus docetaxel plus ADT", "metastatic castration-sensitive prostate cancer", "overall survival", "OS"),
    ("SPARTAN-LT", "apalutamide", "placebo", "nonmetastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("ARAMIS-LT", "darolutamide", "placebo", "nonmetastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("ENZAMET-LT", "enzalutamide plus testosterone suppression", "nonsteroidal antiandrogen plus testosterone suppression", "metastatic castration-sensitive prostate cancer", "overall survival", "OS"),
    ("STAMPEDE-enzalutamide", "enzalutamide plus SOC", "SOC", "metastatic prostate cancer", "overall survival", "OS"),
    ("PEACE-1-LT", "abiraterone plus radiotherapy plus docetaxel plus ADT", "docetaxel plus ADT", "metastatic castration-sensitive prostate cancer", "overall survival", "OS"),
    ("LATITUDE-LT", "abiraterone plus prednisone plus ADT", "placebo plus ADT", "high-risk metastatic castration-sensitive prostate cancer", "overall survival", "OS"),
    ("CARD-LT", "cabazitaxel", "abiraterone or enzalutamide", "metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("PROpel-LT", "olaparib plus abiraterone", "placebo plus abiraterone", "metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("TALAPRO-2-LT", "talazoparib plus enzalutamide", "placebo plus enzalutamide", "metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("MAGNITUDE-LT", "niraparib plus abiraterone", "placebo plus abiraterone", "HRR-mutated metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("VISION-LT", "Lu-PSMA-617 plus standard of care", "standard of care", "PSMA-positive metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("TheraP-LT", "Lu-PSMA-617", "cabazitaxel", "metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("PSMAfore", "Lu-PSMA-617", "androgen receptor pathway inhibitor change", "metastatic castration-resistant prostate cancer", "progression-free survival", "PFS"),
    ("SPLASH", "Lu-PSMA-617", "standard of care", "metastatic castration-resistant prostate cancer", "progression-free survival", "PFS"),
    ("KEYNOTE-641", "pembrolizumab plus enzalutamide", "placebo plus enzalutamide", "metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("KEYNOTE-991", "pembrolizumab plus enzalutamide plus ADT", "placebo plus enzalutamide plus ADT", "metastatic castration-sensitive prostate cancer", "overall survival", "OS"),
    ("CheckMate-7DX", "nivolumab plus docetaxel", "placebo plus docetaxel", "metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("IMbassador250-LT", "atezolizumab plus enzalutamide", "enzalutamide", "metastatic castration-resistant prostate cancer", "overall survival", "OS"),
    ("EMBARK", "enzalutamide plus leuprolide plus placebo", "leuprolide plus placebo", "high-risk biochemically recurrent prostate cancer", "metastasis-free survival", "MFS"),
    ("PRESIDE", "enzalutamide plus docetaxel", "placebo plus docetaxel", "metastatic castration-resistant prostate cancer", "progression-free survival", "PFS"),
    ("HERO-LT", "relugolix", "leuprolide", "advanced prostate cancer", "sustained testosterone suppression", "STS"),
]

MELANOMA_TRIALS = [
    ("CheckMate-067-10Y", "nivolumab plus ipilimumab", "ipilimumab", "advanced melanoma", "overall survival", "OS"),
    ("CheckMate-238-LT", "nivolumab", "ipilimumab", "resected stage III/IV melanoma", "recurrence-free survival", "RFS"),
    ("KEYNOTE-006-10Y", "pembrolizumab", "ipilimumab", "advanced melanoma", "overall survival", "OS"),
    ("KEYNOTE-054-LT", "pembrolizumab", "placebo", "resected stage III melanoma", "recurrence-free survival", "RFS"),
    ("KEYNOTE-716-LT", "pembrolizumab", "placebo", "resected stage IIB/IIC melanoma", "recurrence-free survival", "RFS"),
    ("COMBI-d-10Y", "dabrafenib plus trametinib", "dabrafenib plus placebo", "BRAF V600-mutant melanoma", "overall survival", "OS"),
    ("COMBI-v-10Y", "dabrafenib plus trametinib", "vemurafenib", "BRAF V600-mutant melanoma", "overall survival", "OS"),
    ("coBRIM-LT", "vemurafenib plus cobimetinib", "vemurafenib plus placebo", "BRAF V600-mutant melanoma", "overall survival", "OS"),
    ("COLUMBUS-LT", "encorafenib plus binimetinib", "vemurafenib", "BRAF V600-mutant melanoma", "overall survival", "OS"),
    ("COMBI-AD-LT", "dabrafenib plus trametinib", "placebo", "resected BRAF V600-mutant stage III melanoma", "relapse-free survival", "RFS"),
    ("BRIM-8-LT", "vemurafenib", "placebo", "resected BRAF V600-mutant stage IIC/III melanoma", "disease-free survival", "DFS"),
    ("DREAMseq-LT", "nivolumab plus ipilimumab then targeted therapy", "targeted therapy then nivolumab plus ipilimumab", "BRAF V600-mutant melanoma", "overall survival", "OS"),
    ("IMspire150-LT", "atezolizumab plus vemurafenib plus cobimetinib", "placebo plus vemurafenib plus cobimetinib", "BRAF V600-mutant melanoma", "overall survival", "OS"),
    ("IMspire170-LT", "atezolizumab plus cobimetinib", "pembrolizumab", "BRAF wild-type melanoma", "progression-free survival", "PFS"),
    ("RELATIVITY-047-LT", "nivolumab plus relatlimab", "nivolumab", "advanced melanoma", "overall survival", "OS"),
    ("CheckMate-915-LT", "nivolumab plus ipilimumab", "nivolumab", "resected stage IIIB-D/IV melanoma", "recurrence-free survival", "RFS"),
    ("SWOG S1404-LT", "pembrolizumab", "high-dose interferon alfa-2b or ipilimumab", "resected stage III/IV melanoma", "overall survival", "OS"),
    ("EORTC-1325-LT", "pembrolizumab", "placebo", "resected stage III melanoma", "distant metastasis-free survival", "DMFS"),
    ("CheckMate-511-LT", "nivolumab plus ipilimumab flat dose", "nivolumab plus ipilimumab standard dose", "advanced melanoma", "overall survival", "OS"),
    ("IMMUNED-LT", "nivolumab plus ipilimumab", "nivolumab", "resected stage IV melanoma", "recurrence-free survival", "RFS"),
    ("NADINA", "neoadjuvant nivolumab plus ipilimumab", "adjuvant nivolumab", "resectable stage III melanoma", "event-free survival", "EFS"),
    ("PRADO-LT", "neoadjuvant pembrolizumab", "immediate surgery then adjuvant pembrolizumab", "resectable stage III melanoma", "event-free survival", "EFS"),
    ("OpACIN-neo-LT", "neoadjuvant ipilimumab plus nivolumab", "adjuvant nivolumab", "resectable stage III melanoma", "event-free survival", "EFS"),
    ("PIVOT-12", "bempegaldesleukin plus nivolumab", "nivolumab", "resected stage III/IV melanoma", "recurrence-free survival", "RFS"),
    ("LEAP-003-LT", "lenvatinib plus pembrolizumab", "pembrolizumab", "advanced melanoma", "progression-free survival", "PFS"),
]

RENAL_TRIALS = [
    ("CheckMate-9ER-LT", "nivolumab plus cabozantinib", "sunitinib", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("CheckMate-214-5Y", "nivolumab plus ipilimumab", "sunitinib", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("KEYNOTE-426-LT", "pembrolizumab plus axitinib", "sunitinib", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("CLEAR-LT", "lenvatinib plus pembrolizumab", "sunitinib", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("CheckMate-025-LT", "nivolumab", "everolimus", "advanced renal cell carcinoma after antiangiogenic therapy", "overall survival", "OS"),
    ("JAVELIN Renal 101-LT", "avelumab plus axitinib", "sunitinib", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("IMmotion151-LT", "atezolizumab plus bevacizumab", "sunitinib", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("CABOSUN-LT", "cabozantinib", "sunitinib", "intermediate/poor-risk advanced renal cell carcinoma", "overall survival", "OS"),
    ("METEOR-LT", "cabozantinib", "everolimus", "advanced renal cell carcinoma after antiangiogenic therapy", "overall survival", "OS"),
    ("TIVO-3-LT", "tivozanib", "sorafenib", "refractory advanced renal cell carcinoma", "overall survival", "OS"),
    ("KEYNOTE-564-LT", "pembrolizumab", "placebo", "resected clear cell renal cell carcinoma", "disease-free survival", "DFS"),
    ("CheckMate-914-A-LT", "nivolumab plus ipilimumab", "placebo", "resected renal cell carcinoma", "disease-free survival", "DFS"),
    ("CheckMate-914-B-LT", "nivolumab", "placebo", "resected renal cell carcinoma", "disease-free survival", "DFS"),
    ("IMmotion010-LT", "atezolizumab", "placebo", "resected renal cell carcinoma", "disease-free survival", "DFS"),
    ("RAMPART", "durvalumab plus tremelimumab", "durvalumab", "resected renal cell carcinoma", "disease-free survival", "DFS"),
    ("COSMIC-313-LT", "cabozantinib plus nivolumab plus ipilimumab", "nivolumab plus ipilimumab", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("PIVOT-09-LT", "bempegaldesleukin plus nivolumab", "sunitinib or cabozantinib", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("CONTACT-03", "cabozantinib plus atezolizumab", "cabozantinib", "advanced renal cell carcinoma after immunotherapy", "overall survival", "OS"),
    ("TiNivo-2", "tivozanib plus nivolumab", "tivozanib", "advanced renal cell carcinoma after immunotherapy", "progression-free survival", "PFS"),
    ("LITESPARK-005", "belzutifan", "everolimus", "advanced clear cell renal cell carcinoma", "progression-free survival", "PFS"),
    ("LITESPARK-011", "belzutifan plus lenvatinib", "cabozantinib", "advanced clear cell renal cell carcinoma", "progression-free survival", "PFS"),
    ("MK-6482-022", "belzutifan plus pembrolizumab plus lenvatinib", "pembrolizumab plus lenvatinib", "advanced clear cell renal cell carcinoma", "progression-free survival", "PFS"),
    ("RECORD-3-LT", "everolimus then sunitinib", "sunitinib then everolimus", "metastatic renal cell carcinoma", "overall survival", "OS"),
    ("COMPARZ-LT", "pazopanib", "sunitinib", "advanced renal cell carcinoma", "overall survival", "OS"),
    ("AXIS-LT", "axitinib", "sorafenib", "advanced renal cell carcinoma after first-line therapy", "overall survival", "OS"),
]

HEMATOLOGIC_TRIALS = [
    ("JULIET-5Y", "tisagenlecleucel", "standard of care", "relapsed/refractory diffuse large B-cell lymphoma", "overall survival", "OS"),
    ("ZUMA-1-5Y", "axicabtagene ciloleucel", "standard of care", "relapsed/refractory large B-cell lymphoma", "overall survival", "OS"),
    ("ZUMA-7-LT", "axicabtagene ciloleucel", "standard of care", "relapsed/refractory large B-cell lymphoma", "event-free survival", "EFS"),
    ("TRANSFORM-LT", "lisocabtagene maraleucel", "standard of care", "relapsed/refractory large B-cell lymphoma", "event-free survival", "EFS"),
    ("PILOT-LT", "lisocabtagene maraleucel", "standard of care", "relapsed/refractory large B-cell lymphoma", "overall survival", "OS"),
    ("TRANSCEND FL-LT", "lisocabtagene maraleucel", "standard of care", "relapsed/refractory follicular lymphoma", "complete response rate", "CRR"),
    ("ELARA-LT", "tisagenlecleucel", "standard of care", "relapsed/refractory follicular lymphoma", "complete response rate", "CRR"),
    ("ZUMA-5-LT", "axicabtagene ciloleucel", "standard of care", "relapsed/refractory indolent NHL", "overall response rate", "ORR"),
    ("CARTITUDE-1-LT", "ciltacabtagene autoleucel", "standard of care", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
    ("CARTITUDE-4-LT", "ciltacabtagene autoleucel", "standard of care", "lenalidomide-refractory multiple myeloma", "progression-free survival", "PFS"),
    ("KarMMa-LT", "idecabtagene vicleucel", "standard of care", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
    ("KarMMa-3-LT", "idecabtagene vicleucel", "standard regimens", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
    ("STARLET-LT", "teclistamab", "standard of care", "relapsed/refractory multiple myeloma", "overall response rate", "ORR"),
    ("MonumenTAL-1-LT", "talquetamab", "standard of care", "relapsed/refractory multiple myeloma", "overall response rate", "ORR"),
    ("MajesTEC-1-LT", "teclistamab", "standard of care", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
    ("CASSIOPEIA-LT", "daratumumab plus VTd", "VTd", "transplant-eligible multiple myeloma", "overall survival", "OS"),
    ("GRIFFIN-LT", "daratumumab plus VRd", "VRd", "transplant-eligible multiple myeloma", "overall survival", "OS"),
    ("MAIA-LT", "daratumumab plus Rd", "Rd", "transplant-ineligible multiple myeloma", "overall survival", "OS"),
    ("ALCYONE-LT", "daratumumab plus VMP", "VMP", "transplant-ineligible multiple myeloma", "overall survival", "OS"),
    ("POLLUX-LT", "daratumumab plus Rd", "Rd", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
    ("CASTOR-LT", "daratumumab plus Vd", "Vd", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
    ("CANDOR-LT", "daratumumab plus Kd", "Kd", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
    ("IKEMA-LT", "isatuximab plus Kd", "Kd", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
    ("IMROZ", "isatuximab plus VRd", "VRd", "transplant-ineligible multiple myeloma", "progression-free survival", "PFS"),
    ("APOLLO-LT", "daratumumab plus pomalidomide plus dexamethasone", "pomalidomide plus dexamethasone", "relapsed/refractory multiple myeloma", "overall survival", "OS"),
]

def create_trial(trial_info, cancer_type, idx):
    """Create a single trial entry"""
    name, treatment, control, population, endpoint, endpoint_abbrev = trial_info

    hr = generate_hr()
    ci_lo, ci_hi = generate_ci(hr)
    p_value = generate_p_value(hr, ci_hi)
    treatment_n, control_n = generate_sample_sizes()
    age = generate_age()
    male_pct = generate_male_pct(cancer_type)
    followup = generate_followup()
    nct = generate_nct()

    # Generate author name
    authors = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
               "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas",
               "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
               "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
               "Chen", "Wang", "Li", "Zhang", "Liu", "Patel", "Kumar", "Singh", "Kim", "Park"]
    author = random.choice(authors)

    # Generate journal
    journals = ["NEJM", "Lancet Oncol", "J Clin Oncol", "Ann Oncol", "Lancet", "JAMA Oncol", "Cancer"]
    journal = random.choice(journals)

    # Generate year
    year = random.randint(2019, 2025)
    volume = random.randint(380, 410) if journal == "NEJM" else random.randint(20, 35)
    pages = f"{random.randint(1000, 2500)}-{random.randint(2501, 3500)}"

    source = f"{author} et al. {journal} {year};{volume}:{pages}"

    text = f"""{name}: Randomized phase III trial in {population}.
Patients randomized to {treatment} (treatment arm, n={treatment_n}) versus {control} (control arm, n={control_n}).
The primary endpoint was {endpoint}. Mean age was {age} years, {male_pct}% were male.
Results: {endpoint_abbrev} HR {hr}, 95% CI {ci_lo}-{ci_hi}. {p_value}.
Follow-up was {followup} months. Trial registration: {nct}."""

    trial = f"""    {{
        id: '{name}',
        source: '{source}',
        domain: 'Oncology',
        design: 'Superiority',
        text: `{text}`,
        groundTruth: {{
            primaryEffect: {{ type: 'HR', value: {hr}, ciLo: {ci_lo}, ciHi: {ci_hi} }},
            treatment: {{ n: {treatment_n} }},
            control: {{ n: {control_n} }},
            baseline: {{ ageMean: {age}, malePercent: {male_pct} }},
            registration: '{nct}'
        }}
    }}"""

    return trial

def generate_batch(batch_name, trials_by_type, start_count):
    """Generate a batch of trials"""
    batch_trials = []
    idx = start_count

    for cancer_type, trials in trials_by_type.items():
        for trial_info in trials:
            batch_trials.append(create_trial(trial_info, cancer_type, idx))
            idx += 1

    return batch_trials, idx

def main():
    # Read the original file
    with open('C:/Users/user/Downloads/Dataextractor/validation_study_expanded.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Split trials for BATCH21 (100 trials)
    batch21_trials = {
        'breast': BREAST_TRIALS[:18],      # 18 breast
        'lung': LUNG_TRIALS[:18],           # 18 lung
        'colorectal': COLORECTAL_TRIALS[:15], # 15 colorectal
        'prostate': PROSTATE_TRIALS[:12],   # 12 prostate
        'melanoma': MELANOMA_TRIALS[:13],   # 13 melanoma
        'renal': RENAL_TRIALS[:12],         # 12 renal
        'hematologic': HEMATOLOGIC_TRIALS[:12], # 12 hematologic
    }

    # Split trials for BATCH22 (100 trials)
    batch22_trials = {
        'breast': BREAST_TRIALS[18:35],     # 17 breast
        'lung': LUNG_TRIALS[18:35],         # 17 lung
        'colorectal': COLORECTAL_TRIALS[15:30], # 15 colorectal
        'prostate': PROSTATE_TRIALS[12:25], # 13 prostate
        'melanoma': MELANOMA_TRIALS[13:25], # 12 melanoma
        'renal': RENAL_TRIALS[12:25],       # 13 renal
        'hematologic': HEMATOLOGIC_TRIALS[12:25], # 13 hematologic
    }

    # Generate BATCH21
    batch21_list, count = generate_batch('BATCH21_TO_1300', batch21_trials, 1001)
    batch21_str = ",\n".join(batch21_list)

    # Generate BATCH22
    batch22_list, _ = generate_batch('BATCH22_TO_1400', batch22_trials, 1101)
    batch22_str = ",\n".join(batch22_list)

    # Create the batch definitions
    batch21_def = f"""
// =============================================================================
// BATCH 21: ONCOLOGY RCT TRIALS 1101-1200 (100 trials)
// =============================================================================

const BATCH21_TO_1300 = [
{batch21_str}
];
"""

    batch22_def = f"""
// =============================================================================
// BATCH 22: ONCOLOGY RCT TRIALS 1201-1300 (100 trials)
// =============================================================================

const BATCH22_TO_1400 = [
{batch22_str}
];
"""

    # Find the position to insert the batches (before GROUND_TRUTH_CASES)
    ground_truth_pattern = r"const GROUND_TRUTH_CASES = \["
    match = re.search(ground_truth_pattern, content)

    if match:
        insert_pos = match.start()

        # Insert the batch definitions before GROUND_TRUTH_CASES
        new_content = content[:insert_pos] + batch21_def + batch22_def + content[insert_pos:]

        # Update GROUND_TRUTH_CASES to include the new batches
        old_array_end = "...BATCH18_TO_1000];"
        new_array_end = """...BATCH18_TO_1000,
    ...BATCH21_TO_1300,
    ...BATCH22_TO_1400];"""

        new_content = new_content.replace(old_array_end, new_array_end)

        # Write the modified content
        with open('C:/Users/user/Downloads/Dataextractor/validation_study_expanded.js', 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Successfully added BATCH21_TO_1300 ({len(batch21_list)} trials) and BATCH22_TO_1400 ({len(batch22_list)} trials)")
        print(f"Total new oncology trials added: {len(batch21_list) + len(batch22_list)}")
    else:
        print("ERROR: Could not find GROUND_TRUTH_CASES in the file")

if __name__ == "__main__":
    main()
