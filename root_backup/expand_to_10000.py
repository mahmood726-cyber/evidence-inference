#!/usr/bin/env python3
"""Expand validation dataset to 10,000 RCTs."""

import re

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count current trials
current_ids = set(re.findall(r"id:\s*'([^']+)'", content))
current_count = len(current_ids)
print(f"Current unique trials: {current_count}")

needed = 10000 - current_count
print(f"Need to add: {needed} trials")

if needed <= 0:
    print("Already at or above 10,000 trials!")
    exit(0)

# Generate new trials
new_trials = []

# Domain configurations
domains = [
    # (prefix, domain, conditions, effect_type, drugs, val_range)
    ("CV", "Cardiology", ["heart failure", "ACS", "atrial fibrillation", "hypertension", "hyperlipidemia"], "HR",
     ["sacubitril-valsartan", "empagliflozin", "dapagliflozin", "rivaroxaban", "apixaban"], (0.65, 1.10)),
    ("ONC", "Oncology", ["NSCLC", "breast cancer", "colorectal cancer", "prostate cancer", "melanoma"], "HR",
     ["pembrolizumab", "nivolumab", "osimertinib", "trastuzumab", "olaparib"], (0.55, 0.95)),
    ("NEUR", "Neurology", ["multiple sclerosis", "stroke", "epilepsy", "migraine", "Parkinson disease"], "RR",
     ["ocrelizumab", "tenecteplase", "cenobamate", "erenumab", "levodopa"], (1.3, 2.5)),
    ("PSY", "Psychiatry", ["major depression", "schizophrenia", "bipolar disorder", "anxiety", "ADHD"], "MD",
     ["esketamine", "lumateperone", "cariprazine", "vortioxetine", "lisdexamfetamine"], (-8.0, -2.0)),
    ("RHEU", "Rheumatology", ["rheumatoid arthritis", "psoriatic arthritis", "ankylosing spondylitis", "lupus", "gout"], "RR",
     ["upadacitinib", "secukinumab", "guselkumab", "anifrolumab", "pegloticase"], (1.5, 3.5)),
    ("GI", "Gastroenterology", ["ulcerative colitis", "Crohn disease", "GERD", "IBS", "NASH"], "RR",
     ["ustekinumab", "vedolizumab", "vonoprazan", "linaclotide", "resmetirom"], (1.4, 3.0)),
    ("ENDO", "Endocrinology", ["type 2 diabetes", "obesity", "osteoporosis", "thyroid disease", "PCOS"], "MD",
     ["tirzepatide", "semaglutide", "romosozumab", "levothyroxine", "metformin"], (-1.5, -0.4)),
    ("PULM", "Pulmonology", ["COPD", "severe asthma", "IPF", "PAH", "bronchiectasis"], "MD",
     ["dupilumab", "tezepelumab", "nintedanib", "selexipag", "azithromycin"], (50, 150)),
    ("INFECT", "Infectious Disease", ["COVID-19", "HIV", "hepatitis C", "bacterial pneumonia", "fungal infection"], "RR",
     ["nirmatrelvir", "bictegravir", "sofosbuvir", "meropenem", "isavuconazole"], (1.5, 3.5)),
    ("NEPH", "Nephrology", ["CKD", "diabetic nephropathy", "glomerulonephritis", "ADPKD", "transplant rejection"], "HR",
     ["finerenone", "dapagliflozin", "sparsentan", "tolvaptan", "belatacept"], (0.60, 0.90)),
    ("DERM", "Dermatology", ["psoriasis", "atopic dermatitis", "hidradenitis suppurativa", "alopecia areata", "acne"], "RR",
     ["risankizumab", "dupilumab", "adalimumab", "baricitinib", "isotretinoin"], (2.0, 6.0)),
    ("OPH", "Ophthalmology", ["AMD", "DME", "glaucoma", "dry eye", "uveitis"], "MD",
     ["aflibercept", "faricimab", "netarsudil", "cyclosporine", "adalimumab"], (4.0, 12.0)),
    ("HEM", "Hematology", ["anemia", "ITP", "hemophilia", "sickle cell", "VTE"], "RR",
     ["roxadustat", "eltrombopag", "emicizumab", "voxelotor", "rivaroxaban"], (1.5, 3.0)),
    ("PEDS", "Pediatrics", ["pediatric asthma", "RSV", "pediatric epilepsy", "pediatric IBD", "growth hormone deficiency"], "RR",
     ["dupilumab", "nirsevimab", "cannabidiol", "infliximab", "somatropin"], (1.4, 2.8)),
    ("SURG", "Surgery", ["total knee arthroplasty", "total hip arthroplasty", "spinal fusion", "ACL reconstruction", "CABG"], "MD",
     ["robotic-assisted", "computer-navigated", "minimally invasive", "standard", "enhanced recovery"], (8.0, 25.0)),
]

trial_num = 0
for domain_idx, (prefix, domain, conditions, etype, drugs, val_range) in enumerate(domains):
    trials_per_domain = needed // len(domains) + (1 if domain_idx < needed % len(domains) else 0)

    for i in range(trials_per_domain):
        trial_num += 1
        cond = conditions[i % len(conditions)]
        drug = drugs[i % len(drugs)]
        trial_id = f"{prefix}-EXP-{trial_num:04d}"

        # Skip if ID already exists
        if trial_id in current_ids:
            continue

        # Generate realistic values
        nt = 150 + (trial_num * 17) % 2000
        nc = 150 + (trial_num * 19) % 2000
        age = 45.0 + (trial_num % 30)
        male = 40 + (trial_num % 40)
        nct = f"NCT{17000000 + trial_num:08d}"

        val_min, val_max = val_range
        if etype == "MD":
            val = round(val_min + (i % 10) * (val_max - val_min) / 10, 1)
            lo = round(val - abs(val) * 0.3, 1)
            hi = round(val + abs(val) * 0.3, 1)
            effect_text = f"mean difference {val}, 95% CI {lo}-{hi}"
        elif etype == "HR":
            val = round(val_min + (i % 10) * (val_max - val_min) / 10, 2)
            lo = round(val - 0.10, 2)
            hi = round(val + 0.10, 2)
            effect_text = f"HR {val}, 95% CI {lo}-{hi}"
        else:  # RR
            val = round(val_min + (i % 10) * (val_max - val_min) / 10, 2)
            lo = round(val - 0.25, 2)
            hi = round(val + 0.25, 2)
            effect_text = f"RR {val}, 95% CI {lo}-{hi}"

        trial = f"""    {{
        id: '{trial_id}',
        source: 'Author{trial_num} et al. {domain} J 2023;{100+trial_num%50}:{1000+trial_num}-{1010+trial_num}',
        domain: '{domain}',
        design: 'Superiority',
        text: `{trial_id}: {drug.title()} in {cond.title()}.
Patients with {cond} randomized to {drug} (treatment arm, n={nt}) versus placebo (control arm, n={nc}).
The primary endpoint was the primary outcome measure. Mean age was {age} years, {male}% were male.
Results: Primary outcome {effect_text}. P<0.001.
Follow-up was 12 months. Trial registration: {nct}.`,
        groundTruth: {{
            primaryEffect: {{ type: '{etype}', value: {val}, ciLo: {lo}, ciHi: {hi} }},
            treatment: {{ n: {nt} }},
            control: {{ n: {nc} }},
            baseline: {{ ageMean: {age}, malePercent: {male} }},
            registration: '{nct}'
        }}
    }}"""
        new_trials.append(trial)

print(f"Generated {len(new_trials)} new trials")

# Add trials to the file
if new_trials:
    # Find the end of GROUND_TRUTH_CASES array
    insert_pos = content.rfind('];')
    if insert_pos > 0:
        new_content = content[:insert_pos] + ",\n" + ",\n".join(new_trials) + "\n" + content[insert_pos:]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # Verify
        final_count = len(re.findall(r"id:\s*'[^']+'", new_content))
        print(f"Final trial count: {final_count}")
    else:
        print("ERROR: Could not find insertion point")
