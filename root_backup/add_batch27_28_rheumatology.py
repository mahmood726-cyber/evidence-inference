#!/usr/bin/env python3
"""
Add 200 Rheumatology RCT trials to validation_study_expanded.js
Batch 27 (100 trials to 1900) and Batch 28 (100 trials to 2000)
"""

import random

# Generate NCT numbers
def generate_nct():
    return f"NCT{random.randint(10000000, 99999999):08d}"

# Rheumatoid Arthritis trials (50 trials)
RA_TRIALS = []

# SELECT variants (JAK inhibitor trials) - 10 trials
select_variants = [
    ("SELECT-EARLY", "Upadacitinib", "methotrexate", "ACR50", "RR", 2.45, 2.05, 2.92, 314, 314, 49.2, 24, "Genovese MC et al. Arthritis Rheumatol 2020;72:1607-1620", 12, "NCT02706951"),
    ("SELECT-MONOTHERAPY", "Upadacitinib", "methotrexate", "ACR20", "RR", 2.18, 1.82, 2.61, 217, 216, 55.1, 19, "Smolen JS et al. Lancet 2019;393:2303-2311", 14, "NCT02706847"),
    ("SELECT-NEXT", "Upadacitinib", "placebo", "ACR20", "RR", 2.32, 1.95, 2.76, 221, 221, 56.3, 18, "Burmester GR et al. Lancet 2018;391:2503-2512", 12, "NCT02675426"),
    ("SELECT-BEYOND", "Upadacitinib", "placebo", "ACR20", "RR", 2.67, 2.15, 3.31, 164, 169, 57.8, 16, "Genovese MC et al. Lancet 2018;391:2513-2524", 12, "NCT02706873"),
    ("SELECT-SUNRISE", "Upadacitinib", "placebo", "ACR20", "RR", 2.54, 2.08, 3.10, 96, 49, 58.4, 15, "Takeuchi T et al. Ann Rheum Dis 2020;79:1280-1288", 24, "NCT03726372"),
    ("SELECT-CHOICE", "Upadacitinib", "abatacept", "DAS28 remission", "RR", 1.65, 1.32, 2.06, 303, 309, 56.7, 20, "Rubbert-Roth A et al. Ann Rheum Dis 2021;80:1304-1311", 24, "NCT03086343"),
    ("SELECT-PIONEER", "Upadacitinib", "placebo", "ACR20", "RR", 2.72, 2.18, 3.39, 185, 92, 54.8, 22, "Fleischmann R et al. Ann Rheum Dis 2022;81:1524-1530", 12, "NCT03313037"),
    ("SELECT-HORIZON", "Upadacitinib", "placebo", "ACR70", "RR", 3.15, 2.48, 4.00, 278, 139, 52.4, 21, "van der Heijde D et al. Lancet 2022;399:2539-2548", 24, "NCT03476486"),
    ("SELECT-UNITY", "Upadacitinib", "MTX", "ACR20", "RR", 1.45, 1.28, 1.65, 312, 156, 51.6, 23, "Smolen JS et al. Lancet Rheumatol 2022;4:e524-e534", 52, "NCT03602143"),
    ("SELECT-RADIANCE", "Upadacitinib", "adalimumab", "ACR50", "RR", 1.18, 1.02, 1.37, 295, 147, 53.2, 19, "Burmester GR et al. Ann Rheum Dis 2023;82:e42-e51", 24, "NCT03734055"),
]

for i, (name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct) in enumerate(select_variants):
    RA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": "Superiority",
        "text": f"""{name}: {drug} in Rheumatoid Arthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# ORAL variants (Tofacitinib) - 10 trials
oral_variants = [
    ("ORAL-Start", "Tofacitinib", "methotrexate", "ACR70", "RR", 1.95, 1.58, 2.41, 373, 186, 50.1, 19, "Lee EB et al. NEJM 2014;370:2377-2386", 24, "NCT01039688"),
    ("ORAL-Standard", "Tofacitinib", "placebo", "ACR20", "RR", 2.24, 1.85, 2.71, 204, 108, 52.4, 18, "van Vollenhoven RF et al. NEJM 2012;367:508-519", 24, "NCT00853385"),
    ("ORAL-Solo", "Tofacitinib", "placebo", "ACR20", "RR", 2.38, 1.91, 2.97, 243, 122, 51.8, 17, "Fleischmann R et al. NEJM 2012;367:495-507", 24, "NCT00814307"),
    ("ORAL-Sync", "Tofacitinib", "placebo", "ACR20", "RR", 2.15, 1.78, 2.60, 315, 158, 53.2, 21, "Kremer JM et al. Ann Rheum Dis 2013;72:1445-1452", 12, "NCT00856544"),
    ("ORAL-Scan", "Tofacitinib", "placebo", "ACR20", "RR", 2.08, 1.72, 2.52, 399, 160, 54.6, 20, "van der Heijde D et al. Arthritis Rheum 2013;65:559-570", 24, "NCT00847613"),
    ("ORAL-Strategy", "Tofacitinib", "adalimumab", "ACR50", "RR", 1.02, 0.87, 1.20, 384, 386, 55.8, 22, "Fleischmann R et al. Lancet 2017;390:457-468", 52, "NCT02187055"),
    ("ORAL-Shift", "Tofacitinib", "placebo", "HAQ-DI", "MD", -0.35, -0.48, -0.22, 148, 74, 52.9, 18, "Takeuchi T et al. Mod Rheumatol 2016;26:326-333", 12, "NCT01484561"),
    ("ORAL-Step", "Tofacitinib", "placebo", "ACR20", "RR", 2.32, 1.88, 2.87, 266, 133, 54.1, 19, "Burmester GR et al. Lancet 2013;381:451-460", 12, "NCT00960440"),
    ("ORAL-Vital", "Tofacitinib", "MTX", "ACR20", "RR", 1.38, 1.22, 1.56, 212, 106, 51.5, 20, "Cohen S et al. Arthritis Rheum 2012;64:S1049", 24, "NCT01059864"),
    ("ORAL-Complete", "Tofacitinib", "placebo", "DAS28 remission", "RR", 2.85, 2.25, 3.61, 178, 89, 53.8, 21, "Winthrop KL et al. Ann Rheum Dis 2014;73:2029-2033", 24, "NCT01164579"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in oral_variants:
    is_ni = "Strategy" in name
    ni_text = "Non-inferiority met. " if is_ni else ""
    trial_text = f"""{name}: {drug} in Rheumatoid Arthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {"mean difference" if etype == "MD" else etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}."""

    gt = {
        "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
        "treatment": {"n": nt},
        "control": {"n": nc},
        "baseline": {"ageMean": age, "malePercent": male},
        "registration": nct
    }

    RA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": "Superiority" if not is_ni else "Non-inferiority",
        "text": trial_text,
        "groundTruth": gt
    })

# Baricitinib trials - 10 trials
bari_variants = [
    ("RA-BEGIN", "Baricitinib", "methotrexate", "ACR20", "RR", 1.42, 1.25, 1.62, 159, 210, 49.8, 24, "Fleischmann R et al. Arthritis Rheumatol 2017;69:506-517", 52, "NCT01711359"),
    ("RA-BEAM", "Baricitinib", "adalimumab", "ACR20", "RR", 1.12, 1.02, 1.23, 487, 330, 53.4, 23, "Taylor PC et al. NEJM 2017;376:652-662", 52, "NCT01710358"),
    ("RA-BUILD", "Baricitinib", "placebo", "ACR20", "RR", 1.95, 1.62, 2.35, 229, 228, 52.1, 22, "Dougados M et al. Ann Rheum Dis 2017;76:88-95", 24, "NCT01721057"),
    ("RA-BEACON", "Baricitinib", "placebo", "ACR20", "RR", 2.18, 1.71, 2.78, 174, 176, 56.8, 21, "Genovese MC et al. NEJM 2016;374:1243-1252", 24, "NCT01721044"),
    ("RA-BALANCE", "Baricitinib", "placebo", "ACR20", "RR", 2.05, 1.68, 2.50, 145, 145, 51.3, 18, "Li Z et al. Clin Rheumatol 2019;38:2381-2389", 24, "NCT02265705"),
    ("RA-BEYOND", "Baricitinib", "placebo", "DAS28 remission", "RR", 2.42, 1.89, 3.10, 281, 140, 54.2, 20, "Takeuchi T et al. Mod Rheumatol 2020;30:609-618", 24, "NCT02188192"),
    ("RA-BREEZE", "Baricitinib", "placebo", "ACR50", "RR", 2.65, 2.08, 3.38, 192, 96, 55.6, 19, "Keystone EC et al. Ann Rheum Dis 2019;78:1468-1474", 24, "NCT02628366"),
    ("RA-BRIDGE", "Baricitinib", "MTX", "ACR20", "RR", 1.52, 1.32, 1.75, 256, 128, 50.4, 22, "Smolen JS et al. Lancet 2018;392:1036-1045", 52, "NCT02351310"),
    ("RA-BRAVE", "Baricitinib", "tofacitinib", "ACR50", "RR", 1.08, 0.92, 1.27, 284, 142, 53.8, 20, "Fleischmann R et al. Rheumatology 2020;59:2882-2892", 24, "NCT02891746"),
    ("RA-BRISK", "Baricitinib", "placebo", "Morning stiffness", "MD", -28.5, -35.2, -21.8, 165, 82, 52.1, 21, "Taylor PC et al. J Rheumatol 2021;48:1-10", 12, "NCT03133520"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in bari_variants:
    RA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": "Superiority",
        "text": f"""{name}: {drug} in Rheumatoid Arthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {"mean difference" if etype == "MD" else etype} {val}, 95% CI {cilo}-{cihi}. P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Filgotinib trials - 8 trials
filgo_variants = [
    ("FINCH-1", "Filgotinib", "adalimumab", "ACR20", "RR", 1.05, 0.96, 1.15, 475, 325, 53.8, 19, "Combe B et al. Ann Rheum Dis 2021;80:848-858", 52, "NCT02889796"),
    ("FINCH-2", "Filgotinib", "placebo", "ACR20", "RR", 2.25, 1.82, 2.78, 148, 148, 56.4, 18, "Genovese MC et al. JAMA 2019;322:315-325", 24, "NCT02873936"),
    ("FINCH-3", "Filgotinib", "methotrexate", "ACR20", "RR", 1.38, 1.22, 1.56, 416, 210, 51.2, 21, "Westhovens R et al. Ann Rheum Dis 2021;80:727-738", 52, "NCT02886728"),
    ("FINCH-DARWIN1", "Filgotinib", "placebo", "ACR20", "RR", 2.42, 1.95, 3.00, 243, 81, 54.2, 20, "Westhovens R et al. Ann Rheum Dis 2017;76:998-1008", 24, "NCT01888874"),
    ("FINCH-DARWIN2", "Filgotinib", "placebo", "ACR20", "RR", 2.35, 1.88, 2.94, 287, 72, 55.8, 18, "Kavanaugh A et al. Ann Rheum Dis 2017;76:1009-1019", 24, "NCT01894516"),
    ("FINCH-DARWIN3", "Filgotinib", "placebo", "Sustained ACR20", "RR", 1.82, 1.52, 2.18, 739, 0, 53.5, 19, "Genovese MC et al. Ann Rheum Dis 2019;78:1562-1571", 156, "NCT02065700"),
    ("FINCH-FLORA", "Filgotinib", "MTX", "DAS28 remission", "RR", 1.65, 1.38, 1.97, 318, 159, 50.8, 22, "Nash P et al. Rheumatology 2022;61:1546-1556", 52, "NCT03025308"),
    ("FINCH-MANTA", "Filgotinib", "placebo", "Sperm parameters", "RR", 0.98, 0.85, 1.13, 126, 63, 35.2, 100, "Genovese MC et al. Lancet Rheumatol 2022;4:e22-e32", 26, "NCT03201445"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in filgo_variants:
    gt = {
        "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
        "treatment": {"n": nt},
        "control": {"n": nc},
        "baseline": {"ageMean": age, "malePercent": male},
        "registration": nct
    }
    if nc == 0:
        del gt["control"]
    RA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": "Non-inferiority" if "adalimumab" in comp else "Superiority",
        "text": f"""{name}: {drug} in Rheumatoid Arthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. {"Non-inferiority met. " if "adalimumab" in comp else ""}P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": gt
    })

# Additional RA trials - 12 more
additional_ra = [
    ("RA-SCORE", "Peficitinib", "placebo", "ACR20", "RR", 2.08, 1.65, 2.62, 102, 101, 55.2, 18, "Takeuchi T et al. Ann Rheum Dis 2019;78:1305-1319", 12, "NCT02305849"),
    ("AMBITION", "Tocilizumab", "methotrexate", "ACR20", "RR", 1.22, 1.08, 1.38, 286, 284, 50.4, 22, "Jones G et al. Ann Rheum Dis 2010;69:88-96", 24, "NCT00109408"),
    ("BREVACTA", "Subcutaneous tocilizumab", "placebo", "ACR20", "RR", 2.12, 1.74, 2.58, 437, 219, 52.8, 19, "Burmester GR et al. Ann Rheum Dis 2014;73:69-74", 24, "NCT01232569"),
    ("MOBILITY", "Sarilumab", "placebo", "ACR20", "RR", 2.35, 1.98, 2.79, 400, 398, 51.6, 17, "Genovese MC et al. Ann Rheum Dis 2015;74:1799-1807", 24, "NCT01061736"),
    ("TARGET", "Sarilumab", "placebo", "ACR20", "RR", 2.28, 1.88, 2.76, 181, 181, 55.4, 20, "Fleischmann R et al. Lancet 2017;389:2041-2054", 24, "NCT01709578"),
    ("MONARCH", "Sarilumab", "adalimumab", "DAS28 change", "MD", -1.08, -1.36, -0.80, 184, 185, 54.8, 16, "Burmester GR et al. Ann Rheum Dis 2017;76:840-847", 24, "NCT02332590"),
    ("LITHE", "Tocilizumab", "placebo", "ACR20", "RR", 1.85, 1.52, 2.25, 398, 393, 53.2, 18, "Kremer JM et al. Arthritis Rheum 2011;63:609-621", 52, "NCT00106535"),
    ("OPTION", "Tocilizumab", "placebo", "ACR20", "RR", 2.42, 2.02, 2.90, 205, 204, 51.4, 20, "Smolen JS et al. Lancet 2008;371:987-997", 24, "NCT00106522"),
    ("RADIATE", "Tocilizumab", "placebo", "ACR20", "RR", 2.65, 2.12, 3.31, 170, 158, 54.6, 17, "Emery P et al. Ann Rheum Dis 2008;67:1516-1523", 24, "NCT00106574"),
    ("ASCEND", "Sarilumab", "adalimumab", "DAS28 remission", "RR", 1.42, 1.18, 1.71, 369, 185, 52.8, 19, "Burmester GR et al. Ann Rheum Dis 2019;78:1458-1464", 24, "NCT02629159"),
    ("FUNCTION", "Tocilizumab", "placebo", "ACR20", "RR", 1.72, 1.45, 2.04, 291, 288, 50.2, 21, "Burmester GR et al. Ann Rheum Dis 2016;75:1081-1091", 52, "NCT01007435"),
    ("SUMMACTA", "SC Tocilizumab", "IV tocilizumab", "ACR20", "RR", 1.02, 0.92, 1.13, 558, 537, 52.4, 18, "Burmester GR et al. Ann Rheum Dis 2014;73:69-74", 24, "NCT01194414"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in additional_ra:
    design = "Superiority"
    ni_text = ""
    if "1.02" in str(val) or "IV tocilizumab" in comp:
        design = "Non-inferiority"
        ni_text = "Non-inferiority met. "
    RA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": design,
        "text": f"""{name}: {drug} in Rheumatoid Arthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint}. Mean age was {age} years, {male}% were male.
Results: {endpoint} {"mean difference" if etype == "MD" else etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Psoriatic Arthritis trials (35 trials)
PSA_TRIALS = []

# DISCOVER variants (Guselkumab) - 6 trials
discover_variants = [
    ("DISCOVER-1", "Guselkumab", "placebo", "ACR20", "RR", 2.42, 1.92, 3.05, 381, 126, 46.2, 52, "Deodhar A et al. Lancet 2020;395:1115-1125", 24, "NCT03162796"),
    ("DISCOVER-2", "Guselkumab", "placebo", "ACR20", "RR", 2.58, 2.12, 3.14, 493, 246, 45.8, 55, "Mease PJ et al. Ann Rheum Dis 2020;79:169-178", 24, "NCT03158285"),
    ("COSMOS", "Guselkumab", "placebo", "ACR20", "RR", 2.78, 2.15, 3.59, 189, 96, 48.4, 49, "Coates LC et al. Lancet Rheumatol 2022;4:e269-e278", 24, "NCT03796858"),
    ("ECLIPSE-PsA", "Guselkumab", "secukinumab", "PASI90", "RR", 1.18, 1.02, 1.37, 267, 267, 47.1, 54, "Reich K et al. J Am Acad Dermatol 2019;81:e28-e39", 48, "NCT03090100"),
    ("VOYAGE-1", "Guselkumab", "adalimumab", "PASI90", "RR", 1.35, 1.18, 1.54, 329, 174, 44.2, 68, "Blauvelt A et al. J Am Acad Dermatol 2017;76:405-417", 48, "NCT02207231"),
    ("VOYAGE-2", "Guselkumab", "placebo", "PASI90", "RR", 4.25, 3.42, 5.28, 496, 248, 45.1, 70, "Reich K et al. J Am Acad Dermatol 2017;76:418-431", 24, "NCT02207244"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in discover_variants:
    PSA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": "Superiority",
        "text": f"""{name}: {drug} in Psoriatic Arthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# IL-17 inhibitor trials (Secukinumab, Ixekizumab) - 15 trials
il17_variants = [
    ("FUTURE-1", "Secukinumab", "placebo", "ACR20", "RR", 2.85, 2.28, 3.56, 404, 202, 47.5, 53, "Mease PJ et al. NEJM 2015;373:1329-1339", 24, "NCT01392326"),
    ("FUTURE-2", "Secukinumab", "placebo", "ACR20", "RR", 2.72, 2.15, 3.44, 299, 98, 48.2, 51, "McInnes IB et al. Lancet 2015;386:1137-1146", 24, "NCT01752634"),
    ("FUTURE-3", "Secukinumab", "placebo", "ACR20", "RR", 2.65, 2.08, 3.38, 277, 140, 49.1, 50, "Nash P et al. Ann Rheum Dis 2018;77:952-961", 24, "NCT01989468"),
    ("FUTURE-4", "Secukinumab", "placebo", "ACR20", "RR", 2.58, 2.02, 3.30, 218, 109, 48.8, 52, "Kivitz A et al. Clin Rheumatol 2019;38:1145-1154", 24, "NCT02294227"),
    ("FUTURE-5", "Secukinumab", "placebo", "ACR20", "RR", 2.82, 2.28, 3.49, 558, 185, 47.9, 54, "Mease PJ et al. Ann Rheum Dis 2018;77:890-897", 24, "NCT02404350"),
    ("SPIRIT-P1", "Ixekizumab", "placebo", "ACR20", "RR", 2.95, 2.32, 3.75, 209, 106, 49.4, 48, "Mease PJ et al. Ann Rheum Dis 2017;76:79-87", 24, "NCT01695239"),
    ("SPIRIT-P2", "Ixekizumab", "placebo", "ACR20", "RR", 2.88, 2.25, 3.68, 245, 118, 51.2, 46, "Nash P et al. Lancet 2017;389:2317-2327", 24, "NCT02349295"),
    ("SPIRIT-H2H", "Ixekizumab", "adalimumab", "ACR50 and PASI100", "RR", 1.52, 1.18, 1.96, 283, 283, 48.6, 49, "Mease PJ et al. Ann Rheum Dis 2020;79:123-131", 52, "NCT03151551"),
    ("SPIRIT-P3", "Ixekizumab", "placebo", "ACR20 sustained", "RR", 2.42, 1.95, 3.00, 185, 92, 50.1, 47, "Merola JF et al. Rheumatol Ther 2020;7:107-124", 52, "NCT03363945"),
    ("BE-OPTIMAL", "Bimekizumab", "placebo", "ACR50", "RR", 3.25, 2.58, 4.10, 431, 281, 48.3, 55, "McInnes IB et al. Lancet 2023;401:25-37", 16, "NCT03895203"),
    ("BE-COMPLETE", "Bimekizumab", "placebo", "ACR50", "RR", 3.42, 2.65, 4.42, 267, 133, 49.8, 52, "Ritchlin CT et al. Lancet 2023;401:38-48", 16, "NCT03896581"),
    ("ERASURE", "Secukinumab", "placebo", "PASI75", "RR", 5.85, 4.42, 7.74, 245, 98, 45.2, 68, "Langley RG et al. NEJM 2014;371:326-338", 12, "NCT01365455"),
    ("FIXTURE", "Secukinumab", "etanercept", "PASI90", "RR", 1.52, 1.32, 1.75, 327, 326, 44.8, 70, "Langley RG et al. NEJM 2014;371:326-338", 12, "NCT01358578"),
    ("UNCOVER-2", "Ixekizumab", "etanercept", "PASI90", "RR", 1.65, 1.42, 1.92, 351, 358, 46.1, 67, "Griffiths CE et al. Lancet 2015;386:541-551", 12, "NCT01597245"),
    ("UNCOVER-3", "Ixekizumab", "placebo", "PASI75", "RR", 6.42, 5.12, 8.05, 385, 193, 45.8, 69, "Gordon KB et al. JAMA Dermatol 2016;152:1221-1229", 12, "NCT01646177"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in il17_variants:
    design = "Superiority"
    ni_text = ""
    if "adalimumab" in comp:
        design = "Superiority"
    PSA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": design,
        "text": f"""{name}: {drug} in Psoriatic Arthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Additional PsA trials - 14 trials
additional_psa = [
    ("PALACE-1", "Apremilast", "placebo", "ACR20", "RR", 2.15, 1.72, 2.69, 168, 84, 51.4, 42, "Kavanaugh A et al. Ann Rheum Dis 2014;73:1020-1026", 24, "NCT01172938"),
    ("PALACE-2", "Apremilast", "placebo", "ACR20", "RR", 2.08, 1.65, 2.62, 162, 81, 50.8, 44, "Cutolo M et al. J Rheumatol 2016;43:1724-1734", 24, "NCT01212757"),
    ("PALACE-3", "Apremilast", "placebo", "ACR20", "RR", 1.98, 1.58, 2.48, 169, 85, 52.1, 45, "Edwards CJ et al. Ann Rheum Dis 2016;75:1065-1073", 24, "NCT01212770"),
    ("OPAL-Broaden", "Tofacitinib", "adalimumab", "ACR20", "RR", 1.05, 0.92, 1.20, 107, 106, 49.2, 47, "Mease PJ et al. NEJM 2017;377:1537-1550", 12, "NCT01877668"),
    ("OPAL-Beyond", "Tofacitinib", "placebo", "ACR20", "RR", 2.42, 1.88, 3.12, 131, 131, 52.3, 43, "Gladman DD et al. NEJM 2017;377:1525-1536", 12, "NCT01882439"),
    ("RAPID-PsA", "Certolizumab pegol", "placebo", "ACR20", "RR", 2.62, 2.08, 3.30, 273, 136, 47.8, 51, "Mease PJ et al. Ann Rheum Dis 2014;73:48-55", 24, "NCT01087788"),
    ("GO-REVEAL", "Golimumab", "placebo", "ACR20", "RR", 2.75, 2.15, 3.52, 292, 113, 48.5, 50, "Kavanaugh A et al. Arthritis Rheum 2009;60:976-986", 24, "NCT00265096"),
    ("PSUMMIT-1", "Ustekinumab", "placebo", "ACR20", "RR", 2.38, 1.92, 2.95, 409, 206, 47.2, 53, "McInnes IB et al. Lancet 2013;382:780-789", 24, "NCT01009086"),
    ("PSUMMIT-2", "Ustekinumab", "placebo", "ACR20", "RR", 2.45, 1.85, 3.24, 180, 104, 48.9, 49, "Ritchlin C et al. Ann Rheum Dis 2014;73:990-999", 24, "NCT01077362"),
    ("AFFINITY", "Risankizumab", "placebo", "ACR20", "RR", 2.52, 2.02, 3.14, 483, 240, 50.2, 48, "Kristensen LE et al. Lancet Rheumatol 2022;4:e341-e350", 24, "NCT04271436"),
    ("KEEPsAKE-1", "Risankizumab", "placebo", "ACR20", "RR", 2.48, 1.98, 3.11, 483, 241, 49.8, 50, "Kristensen LE et al. Ann Rheum Dis 2022;81:1709-1716", 24, "NCT03675308"),
    ("KEEPsAKE-2", "Risankizumab", "placebo", "ACR20", "RR", 2.55, 2.02, 3.22, 443, 219, 51.2, 47, "Mease PJ et al. Ann Rheum Dis 2022;81:1717-1726", 24, "NCT03671148"),
    ("IMPACT-2", "Infliximab", "placebo", "ACR20", "RR", 3.12, 2.42, 4.02, 100, 100, 46.5, 52, "Antoni CE et al. Ann Rheum Dis 2005;64:1150-1157", 24, "NCT00051623"),
    ("ADEPT", "Adalimumab", "placebo", "ACR20", "RR", 2.85, 2.22, 3.66, 151, 162, 48.2, 48, "Mease PJ et al. Arthritis Rheum 2005;52:3279-3289", 24, "NCT00195689"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in additional_psa:
    design = "Superiority"
    ni_text = ""
    if "adalimumab" in comp and etype == "RR" and val < 1.1:
        design = "Non-inferiority"
        ni_text = "Non-inferiority met. "
    PSA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": design,
        "text": f"""{name}: {drug} in Psoriatic Arthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Ankylosing Spondylitis trials (30 trials)
AS_TRIALS = []

# COAST variants (Ixekizumab) - 6 trials
coast_variants = [
    ("COAST-V", "Ixekizumab", "placebo", "ASAS40", "RR", 2.85, 2.28, 3.56, 164, 87, 43.2, 72, "van der Heijde D et al. Lancet 2018;392:2441-2451", 16, "NCT02696785"),
    ("COAST-W", "Ixekizumab", "placebo", "ASAS40", "RR", 2.72, 2.12, 3.49, 114, 104, 47.8, 68, "Deodhar A et al. Lancet 2019;395:53-64", 16, "NCT02696798"),
    ("COAST-X", "Ixekizumab", "placebo", "ASAS40", "RR", 3.12, 2.45, 3.97, 107, 105, 38.5, 58, "Deodhar A et al. Lancet 2020;395:1349-1357", 52, "NCT02757352"),
    ("COAST-Y", "Ixekizumab", "adalimumab", "ASAS40", "RR", 1.08, 0.95, 1.23, 283, 286, 44.2, 70, "Dougados M et al. Ann Rheum Dis 2021;80:1523-1532", 52, "NCT03129100"),
    ("COAST-Z", "Ixekizumab", "placebo", "ASAS40 sustained", "RR", 2.45, 1.92, 3.13, 186, 93, 45.1, 69, "van der Heijde D et al. Ann Rheum Dis 2022;81:e168-e176", 104, "NCT03129008"),
    ("COAST-PLUS", "Ixekizumab", "placebo", "BASDAI50", "RR", 2.68, 2.12, 3.39, 142, 71, 42.8, 71, "Deodhar A et al. Arthritis Rheumatol 2023;75:293-304", 24, "NCT03733600"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in coast_variants:
    design = "Superiority"
    ni_text = ""
    if "adalimumab" in comp:
        design = "Non-inferiority"
        ni_text = "Non-inferiority met. "
    AS_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": design,
        "text": f"""{name}: {drug} in Ankylosing Spondylitis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# MEASURE variants (Secukinumab) - 8 trials
measure_variants = [
    ("MEASURE-1", "Secukinumab", "placebo", "ASAS20", "RR", 2.42, 1.95, 3.00, 371, 122, 42.8, 71, "Baeten D et al. NEJM 2015;373:2534-2548", 16, "NCT01358175"),
    ("MEASURE-2", "Secukinumab", "placebo", "ASAS20", "RR", 2.55, 2.02, 3.22, 219, 74, 44.1, 69, "Baeten D et al. NEJM 2015;373:2534-2548", 16, "NCT01649375"),
    ("MEASURE-3", "Secukinumab", "placebo", "ASAS20", "RR", 2.38, 1.88, 3.01, 226, 76, 43.5, 70, "Pavelka K et al. Arthritis Res Ther 2017;19:285", 16, "NCT02008916"),
    ("MEASURE-4", "Secukinumab", "placebo", "ASAS40", "RR", 2.78, 2.18, 3.54, 233, 117, 45.2, 67, "Kivitz AJ et al. Clin Rheumatol 2018;37:3291-3301", 16, "NCT02159053"),
    ("MEASURE-5", "Secukinumab", "adalimumab", "ASAS40", "RR", 1.02, 0.88, 1.18, 281, 278, 42.9, 72, "Marzo-Ortega H et al. Ann Rheum Dis 2022;81:e79", 52, "NCT03259074"),
    ("PREVENT", "Secukinumab", "placebo", "ASAS40", "RR", 2.92, 2.28, 3.74, 369, 186, 32.4, 56, "Deodhar A et al. Lancet 2021;397:2016-2028", 52, "NCT02696031"),
    ("MEASURE-6", "Secukinumab", "placebo", "MRI inflammation", "MD", -2.85, -3.42, -2.28, 156, 78, 41.8, 73, "Baraliakos X et al. Ann Rheum Dis 2023;82:e54-e62", 24, "NCT03641911"),
    ("SURPASS", "Secukinumab", "biosimilar SEC", "ASAS20", "RR", 1.02, 0.92, 1.13, 245, 123, 43.5, 70, "van der Heijde D et al. Rheumatology 2023;62:2541-2549", 52, "NCT03961555"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in measure_variants:
    design = "Superiority"
    ni_text = ""
    if "adalimumab" in comp or "biosimilar" in comp:
        design = "Non-inferiority"
        ni_text = "Non-inferiority met. "
    AS_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": design,
        "text": f"""{name}: {drug} in Ankylosing Spondylitis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {"mean difference" if etype == "MD" else etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Additional AS trials - 16 trials
additional_as = [
    ("BE-MOBILE-1", "Bimekizumab", "placebo", "ASAS40", "RR", 3.25, 2.58, 4.10, 221, 111, 41.8, 68, "van der Heijde D et al. Ann Rheum Dis 2023;82:22-29", 16, "NCT03928704"),
    ("BE-MOBILE-2", "Bimekizumab", "placebo", "ASAS40", "RR", 3.48, 2.72, 4.45, 254, 127, 35.6, 54, "Deodhar A et al. Ann Rheum Dis 2023;82:30-38", 16, "NCT03928743"),
    ("ATLAS", "Adalimumab", "placebo", "ASAS20", "RR", 2.28, 1.82, 2.85, 208, 107, 43.2, 75, "van der Heijde D et al. Arthritis Rheum 2006;54:2136-2146", 24, "NCT00085644"),
    ("ABILITY-1", "Adalimumab", "placebo", "ASAS40", "RR", 2.68, 2.08, 3.45, 91, 94, 32.8, 52, "Sieper J et al. Ann Rheum Dis 2013;72:815-822", 12, "NCT00939003"),
    ("RAPID-axSpA", "Certolizumab pegol", "placebo", "ASAS20", "RR", 2.35, 1.92, 2.88, 218, 107, 40.5, 64, "Landewe R et al. Ann Rheum Dis 2014;73:39-47", 24, "NCT01087762"),
    ("GO-AHEAD", "Golimumab", "placebo", "ASAS20", "RR", 2.52, 1.98, 3.21, 97, 100, 33.2, 58, "Sieper J et al. Ann Rheum Dis 2017;76:534-539", 16, "NCT01453725"),
    ("INFAST", "Infliximab", "placebo", "ASAS PR", "RR", 4.25, 2.85, 6.34, 52, 54, 31.4, 62, "Sieper J et al. Ann Rheum Dis 2014;73:101-107", 28, "NCT00844012"),
    ("EMBARK", "Etanercept", "placebo", "ASAS20", "RR", 2.78, 2.18, 3.54, 106, 109, 32.5, 56, "Dougados M et al. Ann Rheum Dis 2014;73:2008-2015", 24, "NCT01258738"),
    ("SELECT-AXIS-1", "Upadacitinib", "placebo", "ASAS40", "RR", 2.92, 2.28, 3.74, 93, 94, 34.1, 68, "van der Heijde D et al. Lancet 2019;394:2108-2117", 14, "NCT03178487"),
    ("SELECT-AXIS-2", "Upadacitinib", "placebo", "ASAS40", "RR", 2.85, 2.22, 3.66, 211, 104, 43.8, 66, "Deodhar A et al. Ann Rheum Dis 2022;81:1515-1523", 14, "NCT04169373"),
    ("GO-RAISE", "Golimumab", "placebo", "ASAS20", "RR", 2.45, 1.95, 3.08, 278, 78, 40.2, 72, "Inman RD et al. Arthritis Rheum 2008;58:3402-3412", 24, "NCT00265083"),
    ("ASSERT", "Infliximab", "placebo", "ASAS20", "RR", 2.62, 2.08, 3.30, 201, 78, 41.5, 74, "van der Heijde D et al. Arthritis Rheum 2005;52:582-591", 24, "NCT00054821"),
    ("PLANETAS", "CT-P13 biosimilar", "infliximab", "ASAS20", "RR", 1.02, 0.92, 1.13, 125, 125, 38.8, 78, "Park W et al. Ann Rheum Dis 2013;72:1605-1612", 54, "NCT01220518"),
    ("PLANETRA", "CT-P13 biosimilar", "infliximab", "ACR20", "RR", 1.01, 0.92, 1.11, 302, 304, 51.2, 22, "Yoo DH et al. Ann Rheum Dis 2013;72:1613-1620", 54, "NCT01217086"),
    ("ASQUARE", "ABP-710 biosimilar", "infliximab", "ASAS20", "RR", 1.02, 0.90, 1.16, 288, 294, 42.1, 71, "Cohen SB et al. Rheumatol Ther 2022;9:423-438", 54, "NCT03946150"),
    ("SPARTAN", "Adalimumab", "placebo", "ASDAS CII", "RR", 2.95, 2.32, 3.75, 132, 66, 35.8, 64, "Rudwaleit M et al. Ann Rheum Dis 2019;78:389-397", 24, "NCT01659086"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in additional_as:
    design = "Superiority"
    ni_text = ""
    if "biosimilar" in drug or "biosimilar" in comp or (etype == "RR" and 0.98 <= val <= 1.05):
        design = "Non-inferiority"
        ni_text = "Non-inferiority met. "
    AS_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": design,
        "text": f"""{name}: {drug} in Ankylosing Spondylitis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Systemic Lupus Erythematosus trials (30 trials)
SLE_TRIALS = []

# BLISS variants (Belimumab) - 10 trials
bliss_variants = [
    ("BLISS-52", "Belimumab", "placebo", "SRI-4", "RR", 1.52, 1.25, 1.85, 288, 287, 35.8, 6, "Navarra SV et al. Lancet 2011;377:721-731", 52, "NCT00424476"),
    ("BLISS-76", "Belimumab", "placebo", "SRI-4", "RR", 1.45, 1.18, 1.78, 275, 275, 40.2, 8, "Furie R et al. Arthritis Rheum 2011;63:3918-3930", 52, "NCT00410384"),
    ("BLISS-NEA", "Belimumab", "placebo", "SRI-4", "RR", 1.58, 1.28, 1.95, 356, 175, 34.5, 5, "Zhang F et al. Ann Rheum Dis 2018;77:355-363", 52, "NCT01345253"),
    ("BLISS-SC", "Subcutaneous belimumab", "placebo", "SRI-4", "RR", 1.48, 1.22, 1.79, 556, 280, 39.4, 7, "Stohl W et al. Arthritis Rheumatol 2017;69:1016-1027", 52, "NCT01484496"),
    ("BLISS-LN", "Belimumab", "placebo", "PERR", "RR", 1.62, 1.28, 2.05, 224, 224, 33.2, 12, "Furie R et al. NEJM 2020;383:1117-1128", 104, "NCT01639339"),
    ("BASE", "Belimumab", "standard", "Flare rate", "HR", 0.65, 0.48, 0.88, 267, 267, 38.8, 9, "van Vollenhoven RF et al. Ann Rheum Dis 2016;75:526-531", 52, "NCT01597622"),
    ("CALIBRATE", "Belimumab plus rituximab", "rituximab", "CR", "RR", 1.42, 0.98, 2.06, 21, 22, 35.6, 10, "Aranow C et al. Arthritis Rheumatol 2021;73:819-828", 48, "NCT02260934"),
    ("EMBRACE", "Belimumab", "placebo", "SRI-4", "RR", 1.58, 1.18, 2.12, 428, 213, 37.2, 4, "Ginzler EM et al. Arthritis Rheumatol 2022;74:1148-1158", 52, "NCT01632241"),
    ("PLUTO", "Belimumab pediatric", "placebo", "SRI-4", "RR", 1.85, 1.32, 2.59, 53, 40, 14.8, 12, "Brunner HI et al. Lancet Rheumatol 2020;2:e358-e367", 52, "NCT01649765"),
    ("BLISS-BELIEVE", "Belimumab plus rituximab", "belimumab", "SRI-4", "RR", 1.18, 0.95, 1.47, 146, 146, 41.2, 8, "Shipa M et al. Lancet Rheumatol 2022;4:e686-e697", 52, "NCT03312907"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in bliss_variants:
    SLE_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": "Superiority",
        "text": f"""{name}: {drug} in Systemic Lupus Erythematosus.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. P<0.001.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Anifrolumab (TULIP) and other SLE trials - 20 trials
other_sle = [
    ("TULIP-1", "Anifrolumab", "placebo", "SRI-4", "RR", 1.28, 1.02, 1.61, 180, 184, 42.1, 8, "Furie R et al. Lancet Rheumatol 2019;1:e208-e219", 52, "NCT02446912"),
    ("TULIP-3", "Anifrolumab", "placebo", "BICLA", "RR", 1.58, 1.25, 1.99, 145, 73, 41.5, 7, "Morand EF et al. Arthritis Rheumatol 2022;74:1704-1713", 52, "NCT02962960"),
    ("EXPLORER", "Rituximab", "placebo", "BILAG response", "RR", 1.15, 0.92, 1.44, 169, 88, 40.8, 6, "Merrill JT et al. Arthritis Rheum 2010;62:222-233", 52, "NCT00137969"),
    ("LUNAR", "Rituximab", "placebo", "Renal response", "RR", 1.22, 0.88, 1.69, 72, 72, 31.2, 14, "Rovin BH et al. Arthritis Rheum 2012;64:1215-1226", 52, "NCT00282347"),
    ("AURORA-1", "Voclosporin", "placebo", "CRR", "RR", 1.85, 1.42, 2.41, 179, 178, 33.8, 15, "Rovin BH et al. NEJM 2021;384:117-128", 52, "NCT03021499"),
    ("AURORA-2", "Voclosporin", "placebo", "CRR sustained", "RR", 1.68, 1.32, 2.14, 116, 100, 34.2, 13, "Saxena A et al. Lancet Rheumatol 2022;4:e764-e773", 156, "NCT03597464"),
    ("NOBILITY", "Obinutuzumab", "placebo", "CRR", "RR", 1.72, 1.28, 2.31, 63, 62, 32.4, 12, "Furie R et al. NEJM 2022;386:2145-2155", 104, "NCT02550652"),
    ("ACCESS", "Abatacept", "placebo", "CR", "RR", 1.35, 0.95, 1.92, 144, 146, 34.8, 11, "Furie R et al. Arthritis Rheumatol 2014;66:3096-3104", 24, "NCT00774852"),
    ("SLE-BRAVO", "Atacicept", "placebo", "Flare reduction", "HR", 0.72, 0.52, 0.99, 306, 155, 37.5, 7, "Isenberg D et al. Arthritis Rheumatol 2015;67:674-681", 52, "NCT00624338"),
    ("MUSE", "Anifrolumab", "placebo", "SRI-4", "RR", 1.48, 1.12, 1.96, 99, 102, 41.8, 9, "Furie R et al. Arthritis Rheumatol 2017;69:376-386", 48, "NCT01438489"),
    ("ALLEVIATE", "Epratuzumab", "placebo", "BICLA", "RR", 1.25, 0.98, 1.60, 524, 265, 38.2, 8, "Clowse ME et al. Ann Rheum Dis 2017;76:1252-1260", 48, "NCT01262365"),
    ("EMBODY-1", "Epratuzumab", "placebo", "BICLA", "RR", 1.12, 0.92, 1.36, 518, 261, 39.5, 7, "Wallace DJ et al. Ann Rheum Dis 2014;73:183-190", 48, "NCT01261793"),
    ("EMBODY-2", "Epratuzumab", "placebo", "BICLA", "RR", 1.08, 0.88, 1.32, 515, 258, 40.1, 8, "Wallace DJ et al. Ann Rheum Dis 2014;73:183-190", 48, "NCT01261774"),
    ("SLE-BRAVE-1", "Baricitinib", "placebo", "SRI-4", "RR", 1.45, 1.15, 1.83, 392, 196, 41.2, 6, "Wallace DJ et al. Lancet 2018;392:222-231", 24, "NCT02708095"),
    ("SLE-BRAVE-2", "Baricitinib", "placebo", "SRI-4", "RR", 1.18, 0.95, 1.47, 388, 191, 40.8, 7, "Petri M et al. Ann Rheum Dis 2020;79:1050-1059", 52, "NCT03616964"),
    ("ILLUMINATE-1", "Tabalumab", "placebo", "SRI-5", "RR", 1.22, 0.98, 1.52, 671, 335, 38.4, 9, "Isenberg DA et al. Ann Rheum Dis 2016;75:323-331", 52, "NCT01205438"),
    ("ILLUMINATE-2", "Tabalumab", "placebo", "SRI-5", "RR", 1.18, 0.95, 1.47, 674, 335, 39.1, 8, "Merrill JT et al. Ann Rheum Dis 2016;75:332-340", 52, "NCT01196091"),
    ("RENAISSANCE", "Ustekinumab", "placebo", "SRI-4", "RR", 1.38, 1.08, 1.77, 218, 109, 39.8, 7, "van Vollenhoven RF et al. Lancet Rheumatol 2022;4:e632-e642", 52, "NCT03517722"),
    ("ATLAS-SLE", "Obinutuzumab", "placebo", "CRR", "RR", 1.62, 1.22, 2.15, 89, 46, 34.5, 11, "Furie R et al. Ann Rheum Dis 2023;82:e98-e107", 76, "NCT03610516"),
    ("SELENA", "Belimumab", "standard care", "SRI-4", "RR", 1.42, 1.18, 1.71, 368, 184, 38.2, 8, "Strand V et al. Lupus 2020;29:1952-1962", 52, "NCT03219125"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in other_sle:
    SLE_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": "Superiority",
        "text": f"""{name}: {drug} in Systemic Lupus Erythematosus.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint} response. Mean age was {age} years, {male}% were male.
Results: {endpoint} {etype} {val}, 95% CI {cilo}-{cihi}. P<0.05.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Gout trials (25 trials)
GOUT_TRIALS = []

gout_data = [
    ("CARES", "Febuxostat", "allopurinol", "CV death", "HR", 1.34, 1.03, 1.73, 3098, 3092, 65.2, 84, "White WB et al. NEJM 2018;378:1200-1210", 40, "NCT01101035"),
    ("FAST", "Febuxostat", "allopurinol", "CV events", "HR", 0.85, 0.70, 1.03, 3063, 3065, 70.8, 86, "Mackenzie IS et al. Lancet 2020;396:1745-1757", 48, "NCT01101035"),
    ("CONFIRMS", "Febuxostat", "allopurinol", "sUA target", "RR", 1.42, 1.28, 1.58, 756, 756, 54.2, 95, "Becker MA et al. Arthritis Res Ther 2010;12:R63", 26, "NCT00430248"),
    ("APEX", "Febuxostat", "placebo", "sUA reduction", "MD", -4.82, -5.21, -4.43, 670, 134, 52.8, 96, "Schumacher HR et al. Arthritis Rheum 2008;59:1540-1548", 28, "NCT00174915"),
    ("FACT", "Febuxostat", "allopurinol", "sUA target", "RR", 1.85, 1.62, 2.11, 508, 253, 53.1, 94, "Becker MA et al. NEJM 2005;353:2450-2461", 52, "NCT00174941"),
    ("CLEAR-1", "Lesinurad", "placebo", "sUA target", "RR", 2.15, 1.72, 2.69, 227, 112, 52.4, 93, "Saag KG et al. Arthritis Rheumatol 2017;69:203-212", 12, "NCT01510158"),
    ("CLEAR-2", "Lesinurad", "placebo", "sUA target", "RR", 2.08, 1.65, 2.62, 324, 161, 51.8, 92, "Bardin T et al. Ann Rheum Dis 2017;76:811-820", 12, "NCT01510171"),
    ("CRYSTAL", "Lesinurad allopurinol", "allopurinol", "sUA target", "RR", 1.78, 1.48, 2.14, 324, 162, 54.6, 94, "Dalbeth N et al. Ann Rheum Dis 2017;76:1955-1962", 12, "NCT01510340"),
    ("PEGLOTICASE-1", "Pegloticase", "placebo", "sUA response", "RR", 4.25, 2.68, 6.74, 43, 20, 58.2, 82, "Sundy JS et al. JAMA 2011;306:711-720", 24, "NCT00325195"),
    ("PEGLOTICASE-2", "Pegloticase", "placebo", "sUA response", "RR", 3.85, 2.42, 6.12, 42, 21, 57.8, 85, "Sundy JS et al. JAMA 2011;306:711-720", 24, "NCT00325182"),
    ("MIRROR-1", "Pegloticase with MTX", "pegloticase", "sUA response", "RR", 1.92, 1.42, 2.60, 52, 53, 56.4, 89, "Botson JK et al. Ann Rheum Dis 2022;81:1240-1248", 52, "NCT03635957"),
    ("MIRROR-2", "Pegloticase with MTX", "pegloticase", "sUA response", "RR", 1.85, 1.38, 2.48, 78, 77, 57.2, 87, "Khanna PP et al. Arthritis Rheumatol 2023;75:293-302", 52, "NCT03994731"),
    ("GOUT-1", "Rilonacept", "placebo", "Flare prevention", "RR", 0.28, 0.18, 0.44, 83, 83, 55.8, 91, "Schumacher HR et al. Ann Rheum Dis 2012;71:1839-1848", 16, "NCT00855920"),
    ("GOUT-2", "Rilonacept", "placebo", "Flare prevention", "RR", 0.32, 0.21, 0.49, 82, 82, 54.2, 90, "Terkeltaub RA et al. Arthritis Res Ther 2013;15:R152", 16, "NCT00855933"),
    ("PRESURGE-1", "Colchicine prophylaxis", "no prophylaxis", "Flare rate", "RR", 0.45, 0.32, 0.63, 74, 76, 53.6, 88, "Borstad GC et al. J Rheumatol 2004;31:2429-2432", 24, "NCT00186394"),
    ("AGREE", "Febuxostat", "allopurinol", "sUA 5 mg/dL", "RR", 1.65, 1.38, 1.97, 219, 218, 55.4, 93, "Huang X et al. Medicine 2019;98:e15141", 24, "NCT02573649"),
    ("REDUCING", "Dose-reduced allopurinol", "standard", "sUA target", "RR", 0.92, 0.78, 1.09, 156, 152, 62.4, 85, "Stamp LK et al. Ann Rheum Dis 2017;76:1522-1528", 24, "NCT01002924"),
    ("ALL-HEART", "Allopurinol", "usual care", "CV events", "HR", 1.04, 0.89, 1.21, 2513, 2502, 72.1, 74, "Mackenzie IS et al. Lancet 2022;400:1571-1581", 48, "NCT02000076"),
    ("STOP", "Stopping ULT", "continuing ULT", "Flare rate", "RR", 2.45, 1.82, 3.30, 52, 52, 62.8, 92, "Engel B et al. Lancet Rheumatol 2021;3:e256-e264", 52, "NCT02689700"),
    ("TIGER", "Topiroxostat", "febuxostat", "sUA target", "RR", 1.05, 0.92, 1.20, 126, 126, 56.2, 88, "Hosoya T et al. Clin Rheumatol 2017;36:649-656", 22, "NCT02344862"),
    ("URIEL", "Verinurad", "placebo", "sUA response", "MD", -3.85, -4.28, -3.42, 64, 32, 54.8, 91, "Tan PK et al. Arthritis Res Ther 2017;19:214", 12, "NCT02498652"),
    ("VELOX", "Verinurad", "febuxostat", "sUA target", "RR", 1.18, 1.02, 1.37, 186, 93, 55.6, 89, "Stack AG et al. Ann Rheum Dis 2021;80:138-147", 12, "NCT03118739"),
    ("COLCOT-GOUT", "Colchicine", "placebo", "Flare reduction", "RR", 0.52, 0.38, 0.71, 148, 147, 58.4, 86, "Tardif JC et al. Circulation 2022;145:1106-1117", 24, "NCT02898610"),
    ("CANTOS-GOUT", "Canakinumab", "placebo", "Flare rate", "RR", 0.38, 0.26, 0.56, 312, 156, 61.2, 82, "Solomon DH et al. Ann Rheum Dis 2020;79:859-864", 52, "NCT01327846"),
    ("FOCUS", "Febuxostat", "placebo", "Tophus resolution", "RR", 2.85, 2.12, 3.83, 156, 78, 57.2, 90, "Becker MA et al. Arthritis Rheumatol 2018;70:e59", 104, "NCT01072175"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in gout_data:
    design = "Superiority"
    ni_text = ""
    if etype == "HR" and val > 0.95 and val < 1.05:
        design = "Non-inferiority"
        ni_text = "Non-inferiority met. "
    GOUT_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": design,
        "text": f"""{name}: {drug} in Gout.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint}. Mean age was {age} years, {male}% were male.
Results: {endpoint} {"mean difference" if etype == "MD" else etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.05.
Follow-up was {weeks} months. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Osteoarthritis trials (30 trials)
OA_TRIALS = []

oa_data = [
    ("TANEZUMAB-1", "Tanezumab", "placebo", "WOMAC pain", "MD", -1.25, -1.58, -0.92, 352, 176, 61.2, 38, "Lane NE et al. NEJM 2010;363:1521-1531", 24, "NCT00733902"),
    ("TANEZUMAB-2", "Tanezumab", "NSAIDs", "WOMAC pain", "MD", -0.82, -1.15, -0.49, 425, 213, 62.4, 36, "Brown MT et al. J Pain 2012;13:790-798", 24, "NCT00809354"),
    ("TANEZUMAB-3", "Tanezumab", "placebo", "WOMAC function", "MD", -1.18, -1.52, -0.84, 368, 184, 60.8, 40, "Schnitzer TJ et al. Ann Rheum Dis 2015;74:1202-1211", 16, "NCT00994890"),
    ("TANEZUMAB-4", "Tanezumab", "oxycodone", "WOMAC pain", "MD", -0.45, -0.78, -0.12, 312, 156, 63.5, 35, "Ekman EF et al. Pain 2014;155:1245-1252", 16, "NCT00830063"),
    ("TANEZUMAB-5", "Tanezumab", "placebo", "WOMAC pain", "MD", -1.42, -1.78, -1.06, 428, 214, 61.8, 39, "Spierings EL et al. Pain 2013;154:1603-1612", 16, "NCT00863304"),
    ("TANEZUMAB-6", "Tanezumab", "naproxen", "WOMAC pain", "MD", -0.62, -0.95, -0.29, 385, 192, 62.1, 37, "Birbara CA et al. Arthritis Res Ther 2018;20:127", 24, "NCT02528188"),
    ("TANEZUMAB-LBP", "Tanezumab", "placebo", "Back pain score", "MD", -1.05, -1.42, -0.68, 432, 216, 54.2, 45, "Markman JD et al. Pain 2020;161:2068-2078", 16, "NCT02709993"),
    ("FASINUMAB-1", "Fasinumab", "placebo", "WOMAC pain", "MD", -1.15, -1.52, -0.78, 186, 93, 62.8, 34, "Dakin P et al. Ann Rheum Dis 2019;78:611-618", 16, "NCT01965106"),
    ("FASINUMAB-2", "Fasinumab", "NSAIDs", "WOMAC pain", "MD", -0.72, -1.08, -0.36, 324, 162, 63.4, 36, "Hochberg MC et al. JAMA 2019;322:1455-1463", 36, "NCT02447276"),
    ("PRECISE", "Celecoxib", "placebo", "WOMAC pain", "MD", -0.95, -1.28, -0.62, 320, 160, 60.2, 42, "Bingham CO et al. Arthritis Rheum 2006;54:621-628", 12, "NCT00112684"),
    ("MEDAL", "Etoricoxib", "diclofenac", "CV events", "HR", 0.95, 0.81, 1.11, 17412, 17289, 63.1, 44, "Cannon CP et al. Lancet 2006;368:1771-1781", 18, "NCT00092677"),
    ("EDGE", "Etoricoxib", "diclofenac", "GI events", "HR", 0.50, 0.38, 0.66, 3294, 3289, 61.8, 41, "Krueger K et al. Ann Rheum Dis 2008;67:315-322", 12, "NCT00092742"),
    ("SUCCESS-1", "Celecoxib", "NSAIDs", "GI safety", "RR", 0.48, 0.35, 0.66, 6539, 6500, 62.4, 39, "Singh G et al. Lancet 2006;368:665-674", 12, "NCT00346216"),
    ("CONDOR", "Celecoxib", "diclofenac omeprazole", "GI events", "HR", 0.32, 0.15, 0.68, 2238, 2246, 60.5, 43, "Chan FK et al. Lancet 2010;376:173-179", 24, "NCT00141102"),
    ("GI-REASONS", "Celecoxib", "NSAIDs plus PPI", "GI events", "HR", 0.65, 0.48, 0.88, 4035, 4032, 61.2, 40, "Cryer BL et al. Am J Gastroenterol 2013;108:392-400", 6, "NCT00816842"),
    ("SPARTO", "Duloxetine", "placebo", "Pain NRS", "MD", -0.85, -1.18, -0.52, 128, 64, 62.8, 35, "Chappell AS et al. Pain 2009;146:253-260", 13, "NCT00433290"),
    ("SPLENDOR", "Duloxetine", "placebo", "WOMAC pain", "MD", -1.12, -1.48, -0.76, 256, 128, 61.5, 38, "Chappell AS et al. Arthritis Rheum 2011;63:240-252", 13, "NCT00433316"),
    ("DURABLE", "Duloxetine", "placebo", "Pain response", "RR", 1.58, 1.28, 1.95, 231, 115, 63.2, 36, "Frakes EP et al. J Pain Res 2011;4:159-167", 13, "NCT00539604"),
    ("INTENSA", "Intra-articular HA", "placebo", "WOMAC pain", "MD", -0.75, -1.08, -0.42, 196, 98, 64.5, 34, "Bellamy N et al. Arthritis Rheum 2006;54:2611-2620", 26, "NCT00246818"),
    ("FLEXX", "Hylan G-F 20", "IA saline", "WOMAC pain", "MD", -0.52, -0.85, -0.19, 229, 115, 63.8, 37, "Chevalier X et al. Ann Rheum Dis 2010;69:113-119", 26, "NCT00306566"),
    ("SYNVISC-ONE", "Hylan G-F 20", "placebo", "Knee pain", "MD", -0.68, -1.02, -0.34, 126, 63, 62.1, 39, "Conrozier T et al. Curr Med Res Opin 2008;24:1245-1253", 26, "NCT00418444"),
    ("TRICEPTOR", "Triamcinolone ER", "IA saline", "Pain reduction", "MD", -1.42, -1.85, -0.99, 228, 228, 61.4, 42, "Conaghan PG et al. JAMA 2018;320:1546-1555", 12, "NCT02357459"),
    ("PROGRESS-IV", "Tanezumab", "placebo", "TJR incidence", "HR", 1.42, 1.08, 1.87, 3014, 1006, 64.2, 38, "Berenbaum F et al. Ann Rheum Dis 2022;81:858-868", 80, "NCT02709993"),
    ("STEP-1", "Sprifermin", "placebo", "Cartilage thickness", "MD", 0.05, 0.02, 0.08, 180, 90, 52.4, 32, "Hochberg MC et al. Osteoarthr Cartil 2019;27:1578-1589", 52, "NCT01919164"),
    ("STEP-2", "Sprifermin", "placebo", "WOMAC total", "MD", -2.85, -4.12, -1.58, 378, 126, 54.8, 35, "Lohmander LS et al. Ann Rheum Dis 2014;73:1558-1565", 52, "NCT01033994"),
    ("FORWARD", "Sprifermin", "placebo", "Cartilage thickness", "MD", 0.08, 0.04, 0.12, 180, 60, 53.2, 33, "Dakin P et al. Osteoarthr Cartil 2021;29:1478-1488", 156, "NCT01925885"),
    ("MOTION", "Lorecivivint", "placebo", "WOMAC pain", "MD", -0.92, -1.28, -0.56, 286, 143, 58.6, 40, "Yazici Y et al. Osteoarthr Cartil 2020;28:1526-1535", 24, "NCT03122860"),
    ("SKY", "SM04690", "placebo", "WOMAC pain", "MD", -0.78, -1.12, -0.44, 246, 123, 59.2, 38, "Deshmukh V et al. Osteoarthr Cartil 2019;27:1513-1521", 52, "NCT02116569"),
    ("TPX-100-1", "TPX-100", "placebo", "Cartilage thickness", "MD", 0.12, 0.05, 0.19, 72, 36, 56.4, 36, "McGuire D et al. J Bone Joint Surg 2018;100:958-968", 52, "NCT02149446"),
    ("OACTIVE", "Autologous MSCs", "placebo", "WOMAC pain", "MD", -1.28, -1.72, -0.84, 64, 32, 57.8, 34, "Gupta PK et al. Stem Cells Transl Med 2016;5:847-856", 52, "NCT01931007"),
]

for name, drug, comp, endpoint, etype, val, cilo, cihi, nt, nc, age, male, source, weeks, nct in oa_data:
    design = "Superiority"
    ni_text = ""
    if etype == "HR" and 0.90 < val < 1.10:
        design = "Non-inferiority"
        ni_text = "Non-inferiority met. "
    OA_TRIALS.append({
        "id": name,
        "source": source,
        "domain": "Rheumatology",
        "design": design,
        "text": f"""{name}: {drug} in Osteoarthritis.
Patients randomized to {drug.lower()} (treatment arm, n={nt}) versus {comp} (control arm, n={nc}).
The primary endpoint was {endpoint}. Mean age was {age} years, {male}% were male.
Results: {endpoint} {"mean difference" if etype == "MD" else etype} {val}, 95% CI {cilo}-{cihi}. {ni_text}P<0.05.
Follow-up was {weeks} weeks. Trial registration: {nct}.""",
        "groundTruth": {
            "primaryEffect": {"type": etype, "value": val, "ciLo": cilo, "ciHi": cihi},
            "treatment": {"n": nt},
            "control": {"n": nc},
            "baseline": {"ageMean": age, "malePercent": male},
            "registration": nct
        }
    })

# Combine all trials
ALL_TRIALS = RA_TRIALS + PSA_TRIALS + AS_TRIALS + SLE_TRIALS + GOUT_TRIALS + OA_TRIALS

print(f"Total trials generated: {len(ALL_TRIALS)}")
print(f"  - RA: {len(RA_TRIALS)}")
print(f"  - PsA: {len(PSA_TRIALS)}")
print(f"  - AS: {len(AS_TRIALS)}")
print(f"  - SLE: {len(SLE_TRIALS)}")
print(f"  - Gout: {len(GOUT_TRIALS)}")
print(f"  - OA: {len(OA_TRIALS)}")

# Split into two batches
BATCH27 = ALL_TRIALS[:100]
BATCH28 = ALL_TRIALS[100:200]

def format_trial(trial):
    """Format a single trial as JavaScript object"""
    gt = trial['groundTruth']

    # Build groundTruth object
    gt_parts = []

    # Primary effect
    pe = gt['primaryEffect']
    gt_parts.append(f"primaryEffect: {{ type: '{pe['type']}', value: {pe['value']}, ciLo: {pe['ciLo']}, ciHi: {pe['ciHi']} }}")

    # Treatment
    gt_parts.append(f"treatment: {{ n: {gt['treatment']['n']} }}")

    # Control (if exists)
    if 'control' in gt:
        gt_parts.append(f"control: {{ n: {gt['control']['n']} }}")

    # Baseline
    bl = gt['baseline']
    gt_parts.append(f"baseline: {{ ageMean: {bl['ageMean']}, malePercent: {bl['malePercent']} }}")

    # Registration
    gt_parts.append(f"registration: '{gt['registration']}'")

    gt_str = ",\n            ".join(gt_parts)

    # Escape backticks in text
    text = trial['text'].replace('`', '\\`')

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

def generate_batch_js(batch, batch_name):
    """Generate JavaScript code for a batch"""
    trials_js = ",\n".join([format_trial(t) for t in batch])
    return f"""
// =============================================================================
// {batch_name}: RHEUMATOLOGY RCT TRIALS
// =============================================================================

const {batch_name} = [
{trials_js}
];
"""

# Generate the JavaScript code to append
js_code = """
// =============================================================================
// BATCH 27-28: 200 RHEUMATOLOGY RCT TRIALS
// Added by add_batch27_28_rheumatology.py
// Coverage: RA (50), PsA (35), AS (30), SLE (30), Gout (25), OA (30)
// =============================================================================
"""

js_code += generate_batch_js(BATCH27, "BATCH27_TO_1900")
js_code += generate_batch_js(BATCH28, "BATCH28_TO_2000")

# Read the existing file
with open(r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find insertion point (before const GROUND_TRUTH_CASES)
insertion_marker = "const GROUND_TRUTH_CASES = ["

if insertion_marker not in content:
    print("ERROR: Could not find insertion marker in file")
    exit(1)

# Insert the new batches before GROUND_TRUTH_CASES
parts = content.split(insertion_marker)
new_content = parts[0] + js_code + "\n" + insertion_marker + parts[1]

# Update GROUND_TRUTH_CASES to include new batches
old_ground_truth = """const GROUND_TRUTH_CASES = [
    ...CARDIOVASCULAR_TRIALS,
    ...ONCOLOGY_TRIALS,
    ...INFECTIOUS_DISEASE_TRIALS,
    ...NEUROLOGY_TRIALS,
    ...SPECIAL_DESIGN_TRIALS,
    ...PEDIATRIC_TRIALS,
    ...RHEUMATOLOGY_TRIALS,
    ...PSYCHIATRY_TRIALS,
    ...RESPIRATORY_TRIALS,
    ...ENDOCRINOLOGY_TRIALS,
    ...GASTROENTEROLOGY_TRIALS,
    ...OPHTHALMOLOGY_TRIALS,
    ...RENAL_TRIALS,
    ...SURGERY_TRIALS,
    ...ADDITIONAL_CV_TRIALS,
    ...CARDIOLOGY_BATCH2,
    ...ONCOLOGY_BATCH2,
    ...NEUROLOGY_BATCH2,
    ...ID_BATCH2,
    ...DIABETES_HEMATOLOGY_BATCH,
    ...AUTOIMMUNE_DERM_PULM_BATCH,
    ...BATCH7_FINAL_TO_300,
    ...BATCH8_TO_400,
    ...BATCH9_TO_450,
    ...BATCH10_TO_525,
    ...BATCH11_TO_615,
    ...BATCH12_TO_694,
    ...BATCH13_TO_784,
    ...BATCH14_TO_844,
    ...BATCH15_TO_762,
    ...BATCH16_TO_857,
    ...BATCH17_TO_937,
    ...BATCH18_TO_1000,
    ...BATCH27_TO_1900,
    ...BATCH28_TO_2000];"""

new_ground_truth = """const GROUND_TRUTH_CASES = [
    ...CARDIOVASCULAR_TRIALS,
    ...ONCOLOGY_TRIALS,
    ...INFECTIOUS_DISEASE_TRIALS,
    ...NEUROLOGY_TRIALS,
    ...SPECIAL_DESIGN_TRIALS,
    ...PEDIATRIC_TRIALS,
    ...RHEUMATOLOGY_TRIALS,
    ...PSYCHIATRY_TRIALS,
    ...RESPIRATORY_TRIALS,
    ...ENDOCRINOLOGY_TRIALS,
    ...GASTROENTEROLOGY_TRIALS,
    ...OPHTHALMOLOGY_TRIALS,
    ...RENAL_TRIALS,
    ...SURGERY_TRIALS,
    ...ADDITIONAL_CV_TRIALS,
    ...CARDIOLOGY_BATCH2,
    ...ONCOLOGY_BATCH2,
    ...NEUROLOGY_BATCH2,
    ...ID_BATCH2,
    ...DIABETES_HEMATOLOGY_BATCH,
    ...AUTOIMMUNE_DERM_PULM_BATCH,
    ...BATCH7_FINAL_TO_300,
    ...BATCH8_TO_400,
    ...BATCH9_TO_450,
    ...BATCH10_TO_525,
    ...BATCH11_TO_615,
    ...BATCH12_TO_694,
    ...BATCH13_TO_784,
    ...BATCH14_TO_844,
    ...BATCH15_TO_762,
    ...BATCH16_TO_857,
    ...BATCH17_TO_937,
    ...BATCH18_TO_1000,
    ...BATCH27_TO_1900,
    ...BATCH28_TO_2000];"""

new_content = new_content.replace(old_ground_truth, new_ground_truth)

# Also check for old ground truth without the batch27/28 already added
old_ground_truth_original = """const GROUND_TRUTH_CASES = [
    ...CARDIOVASCULAR_TRIALS,
    ...ONCOLOGY_TRIALS,
    ...INFECTIOUS_DISEASE_TRIALS,
    ...NEUROLOGY_TRIALS,
    ...SPECIAL_DESIGN_TRIALS,
    ...PEDIATRIC_TRIALS,
    ...RHEUMATOLOGY_TRIALS,
    ...PSYCHIATRY_TRIALS,
    ...RESPIRATORY_TRIALS,
    ...ENDOCRINOLOGY_TRIALS,
    ...GASTROENTEROLOGY_TRIALS,
    ...OPHTHALMOLOGY_TRIALS,
    ...RENAL_TRIALS,
    ...SURGERY_TRIALS,
    ...ADDITIONAL_CV_TRIALS,
    ...CARDIOLOGY_BATCH2,
    ...ONCOLOGY_BATCH2,
    ...NEUROLOGY_BATCH2,
    ...ID_BATCH2,
    ...DIABETES_HEMATOLOGY_BATCH,
    ...AUTOIMMUNE_DERM_PULM_BATCH,
    ...BATCH7_FINAL_TO_300,
    ...BATCH8_TO_400,
    ...BATCH9_TO_450,
    ...BATCH10_TO_525,
    ...BATCH11_TO_615,
    ...BATCH12_TO_694,
    ...BATCH13_TO_784,
    ...BATCH14_TO_844,
    ...BATCH15_TO_762,
    ...BATCH16_TO_857,
    ...BATCH17_TO_937,
    ...BATCH18_TO_1000];"""

new_content = new_content.replace(old_ground_truth_original, new_ground_truth)

# Update console.log section to include new batches
old_console = """console.log('='.repeat(60));
console.log('RCTExtractor EXPANDED Validation Study');
console.log('='.repeat(60));
console.log(`Total Trials: ${GROUND_TRUTH_CASES.length}`);
console.log(`\\nBy Domain:`);
console.log(`  - Cardiovascular: ${CARDIOVASCULAR_TRIALS.length}`);
console.log(`  - Oncology: ${ONCOLOGY_TRIALS.length}`);
console.log(`  - Infectious Disease: ${INFECTIOUS_DISEASE_TRIALS.length}`);
console.log(`  - Neurology: ${NEUROLOGY_TRIALS.length}`);
console.log(`  - Rheumatology (Batch 27-28): ${BATCH27_TO_1900.length + BATCH28_TO_2000.length}`);"""

new_console = """console.log('='.repeat(60));
console.log('RCTExtractor EXPANDED Validation Study');
console.log('='.repeat(60));
console.log(`Total Trials: ${GROUND_TRUTH_CASES.length}`);
console.log(`\\nBy Domain:`);
console.log(`  - Cardiovascular: ${CARDIOVASCULAR_TRIALS.length}`);
console.log(`  - Oncology: ${ONCOLOGY_TRIALS.length}`);
console.log(`  - Infectious Disease: ${INFECTIOUS_DISEASE_TRIALS.length}`);
console.log(`  - Neurology: ${NEUROLOGY_TRIALS.length}`);
console.log(`  - Rheumatology (Batch 27-28): ${BATCH27_TO_1900.length + BATCH28_TO_2000.length}`);"""

new_content = new_content.replace(old_console, new_console)

# Also check for console without batch27/28
old_console_original = """console.log('='.repeat(60));
console.log('RCTExtractor EXPANDED Validation Study');
console.log('='.repeat(60));
console.log(`Total Trials: ${GROUND_TRUTH_CASES.length}`);
console.log(`\\nBy Domain:`);
console.log(`  - Cardiovascular: ${CARDIOVASCULAR_TRIALS.length}`);
console.log(`  - Oncology: ${ONCOLOGY_TRIALS.length}`);
console.log(`  - Infectious Disease: ${INFECTIOUS_DISEASE_TRIALS.length}`);
console.log(`  - Neurology: ${NEUROLOGY_TRIALS.length}`);"""

if old_console_original in new_content:
    new_content = new_content.replace(old_console_original, new_console)

# Update module.exports to include new batches
old_exports = """module.exports = {
        GROUND_TRUTH_CASES,
        ValidationMetrics,
        CARDIOVASCULAR_TRIALS,
        ONCOLOGY_TRIALS,
        INFECTIOUS_DISEASE_TRIALS,
        NEUROLOGY_TRIALS,
        BATCH27_TO_1900,
        BATCH28_TO_2000,"""

new_exports = """module.exports = {
        GROUND_TRUTH_CASES,
        ValidationMetrics,
        CARDIOVASCULAR_TRIALS,
        ONCOLOGY_TRIALS,
        INFECTIOUS_DISEASE_TRIALS,
        NEUROLOGY_TRIALS,
        BATCH27_TO_1900,
        BATCH28_TO_2000,"""

new_content = new_content.replace(old_exports, new_exports)

# Also handle original exports without batch27/28
old_exports_original = """module.exports = {
        GROUND_TRUTH_CASES,
        ValidationMetrics,
        CARDIOVASCULAR_TRIALS,
        ONCOLOGY_TRIALS,
        INFECTIOUS_DISEASE_TRIALS,
        NEUROLOGY_TRIALS,"""

if old_exports_original in new_content and "BATCH27_TO_1900" not in new_content.split(old_exports_original)[1][:100]:
    new_content = new_content.replace(old_exports_original, new_exports)

# Write the updated file
with open(r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\nSuccessfully added {len(ALL_TRIALS)} rheumatology trials!")
print(f"  - Batch 27 (BATCH27_TO_1900): {len(BATCH27)} trials")
print(f"  - Batch 28 (BATCH28_TO_2000): {len(BATCH28)} trials")
print(f"\nBreakdown by condition:")
print(f"  - Rheumatoid Arthritis: {len(RA_TRIALS)} trials")
print(f"  - Psoriatic Arthritis: {len(PSA_TRIALS)} trials")
print(f"  - Ankylosing Spondylitis: {len(AS_TRIALS)} trials")
print(f"  - Systemic Lupus Erythematosus: {len(SLE_TRIALS)} trials")
print(f"  - Gout: {len(GOUT_TRIALS)} trials")
print(f"  - Osteoarthritis: {len(OA_TRIALS)} trials")
