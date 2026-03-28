"""
Quick RCTExtractor test on a sample of PDFs
"""
import os
import re
import json
import pdfplumber
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Patterns for effect sizes
PATTERNS = [
    ('HR', r'HR\s*[=:]?\s*([\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*([\d.]+)\s*(?:[-–]|to)\s*([\d.]+)', False),
    ('RR', r'RR\s*[=:]?\s*([\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*([\d.]+)\s*(?:[-–]|to)\s*([\d.]+)', False),
    ('OR', r'(?<!log)OR\s*[=:]?\s*([\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*([\d.]+)\s*(?:[-–]|to)\s*([\d.]+)', False),
    ('MD', r'(?<![S])MD\s*[=:]?\s*(-?[\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*(-?[\d.]+)\s*(?:[-–]|to)\s*(-?[\d.]+)', True),
    ('SMD', r'SMD\s*[=:]?\s*(-?[\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*(-?[\d.]+)\s*(?:[-–]|to)\s*(-?[\d.]+)', True),
]

def extract_effects(text):
    results = []
    for effect_type, pattern, allows_neg in PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            try:
                value = float(m[0])
                ci_lo = float(m[1])
                ci_hi = float(m[2])
                if ci_lo <= ci_hi and (allows_neg or value >= 0):
                    results.append({'type': effect_type, 'value': value, 'ci_lo': ci_lo, 'ci_hi': ci_hi})
            except:
                pass
    return results

def main():
    # Get all PDF directories
    dirs = [
        "C:/Users/user/cardiology_rcts",
        "C:/Users/user/oncology_rcts",
        "C:/Users/user/respiratory_rcts",
        "C:/Users/user/diabetes_rcts",
        "C:/Users/user/rheumatology_rcts",
        "C:/Users/user/infectious_rcts",
    ]

    all_pdfs = []
    for d in dirs:
        if os.path.exists(d):
            pdfs = list(Path(d).glob("PMC*.pdf"))
            all_pdfs.extend(pdfs)

    print(f"Total PDFs found: {len(all_pdfs)}")

    # Sample 500 PDFs for quick test
    import random
    sample = random.sample(all_pdfs, min(500, len(all_pdfs)))

    print(f"\nTesting on {len(sample)} sample PDFs...\n")

    success = 0
    with_effects = 0
    total_effects = 0
    by_type = {}
    sample_effects = []

    for i, pdf in enumerate(sample):
        try:
            with pdfplumber.open(pdf) as f:
                text = ""
                for page in f.pages[:10]:  # First 10 pages only
                    t = page.extract_text()
                    if t:
                        text += t + "\n"

            effects = extract_effects(text)
            success += 1

            if effects:
                with_effects += 1
                total_effects += len(effects)
                for e in effects:
                    by_type[e['type']] = by_type.get(e['type'], 0) + 1
                    if len(sample_effects) < 30:
                        sample_effects.append((pdf.stem, e))
        except Exception as ex:
            pass

        if (i + 1) % 100 == 0:
            print(f"  Processed {i+1}/{len(sample)}...")

    # Results
    print("\n" + "="*60)
    print("QUICK EXTRACTION TEST RESULTS")
    print("="*60)
    print(f"\nSample size: {len(sample)} PDFs")
    print(f"Successfully processed: {success}")
    print(f"PDFs with effects found: {with_effects} ({100*with_effects/success:.1f}%)")
    print(f"Total effects extracted: {total_effects}")

    print("\nBy Effect Type:")
    print("-"*40)
    for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
        pct = 100 * c / total_effects if total_effects > 0 else 0
        print(f"  {t:8} {c:5,} ({pct:5.1f}%)")

    print("\nSample Extracted Effects:")
    print("-"*40)
    for pmcid, e in sample_effects[:15]:
        print(f"  {pmcid}: {e['type']} = {e['value']} (CI: {e['ci_lo']} - {e['ci_hi']})")

    print("\n" + "="*60)
    print(f"EXTRACTION RATE: {100*with_effects/success:.1f}% of PDFs contain effect sizes")
    print("="*60)

if __name__ == "__main__":
    main()
