"""
Test RCTExtractor on Downloaded Cardiology PDFs
"""
import os
import re
import json
import pdfplumber
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

PDF_DIR = Path("C:/Users/user/cardiology_rcts")
OUTPUT_FILE = PDF_DIR / "extraction_results.json"

# RCTExtractor patterns (same as validation)
PATTERNS = [
    ('SMD', r'SMD\s*[=:]?\s*(-?[\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*(-?[\d.]+)\s*(?:[-–]|to)\s*(-?[\d.]+)', True),
    ('logOR', r'logOR\s*[=:]?\s*(-?[\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*(-?[\d.]+)\s*(?:[-–]|to)\s*(-?[\d.]+)', True),
    ('HR', r'HR\s*[=:]?\s*([\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*([\d.]+)\s*(?:[-–]|to)\s*([\d.]+)', False),
    ('RR', r'RR\s*[=:]?\s*([\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*([\d.]+)\s*(?:[-–]|to)\s*([\d.]+)', False),
    ('OR', r'(?<!log)OR\s*[=:]?\s*([\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*([\d.]+)\s*(?:[-–]|to)\s*([\d.]+)', False),
    ('MD', r'(?<![S])MD\s*[=:]?\s*(-?[\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*(-?[\d.]+)\s*(?:[-–]|to)\s*(-?[\d.]+)', True),
    ('RD', r'RD\s*[=:]?\s*(-?[\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*(-?[\d.]+)\s*(?:[-–]|to)\s*(-?[\d.]+)', True),
    ('RateRatio', r'(?:rate\s*ratio|IRR)\s*[=:]?\s*([\d.]+)\s*[,;]?\s*(?:95%\s*)?CI\s*[:\s]*([\d.]+)\s*(?:[-–]|to)\s*([\d.]+)', False),
]

def extract_effects(text):
    """Extract all effect sizes from text"""
    results = []
    seen = set()

    for effect_type, pattern, allows_negative in PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            try:
                value = float(m[0])
                ci_lo = float(m[1])
                ci_hi = float(m[2])

                # Validate
                if not allows_negative and value < 0:
                    continue
                if ci_lo > ci_hi:
                    continue

                key = (effect_type, round(value, 3), round(ci_lo, 3), round(ci_hi, 3))
                if key not in seen:
                    seen.add(key)
                    results.append({
                        'type': effect_type,
                        'value': value,
                        'ci_lo': ci_lo,
                        'ci_hi': ci_hi
                    })
            except:
                continue

    return results

def process_pdf(pdf_path):
    """Process a single PDF"""
    pmcid = pdf_path.stem

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"

        effects = extract_effects(text)

        return {
            'pmcid': pmcid,
            'pages': len(pdf.pages),
            'chars': len(text),
            'effects_count': len(effects),
            'effects': effects,
            'status': 'success'
        }
    except Exception as e:
        return {
            'pmcid': pmcid,
            'status': 'error',
            'error': str(e)[:100]
        }

def main():
    print("="*70)
    print("TESTING RCT EXTRACTOR ON DOWNLOADED PDFs")
    print("="*70)

    # Get all PDFs
    pdf_files = sorted(PDF_DIR.glob("PMC*.pdf"))
    valid_pdfs = [f for f in pdf_files if f.stat().st_size > 50000]

    print(f"\nTotal PDFs found: {len(pdf_files)}")
    print(f"Valid PDFs (>50KB): {len(valid_pdfs)}")

    if len(valid_pdfs) == 0:
        print("No PDFs to process!")
        return

    # Process PDFs
    print(f"\nProcessing {len(valid_pdfs)} PDFs...")

    all_results = []

    # Use multiprocessing for speed
    num_workers = min(8, multiprocessing.cpu_count())

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(process_pdf, pdf): pdf for pdf in valid_pdfs}

        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            all_results.append(result)

            if (i + 1) % 100 == 0:
                success = sum(1 for r in all_results if r.get('status') == 'success')
                with_effects = sum(1 for r in all_results if r.get('effects_count', 0) > 0)
                print(f"  Progress: {i+1}/{len(valid_pdfs)} | Success: {success} | With effects: {with_effects}")

    # Analysis
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)

    successful = [r for r in all_results if r.get('status') == 'success']
    with_effects = [r for r in successful if r.get('effects_count', 0) > 0]
    total_effects = sum(r.get('effects_count', 0) for r in successful)

    print(f"\nTotal PDFs processed: {len(all_results)}")
    print(f"Successful extractions: {len(successful)}")
    print(f"PDFs with effects found: {len(with_effects)} ({100*len(with_effects)/len(successful):.1f}%)")
    print(f"Total effects extracted: {total_effects}")

    # By effect type
    by_type = {}
    for r in successful:
        for e in r.get('effects', []):
            by_type[e['type']] = by_type.get(e['type'], 0) + 1

    print("\nBy Effect Type:")
    print("-"*40)
    for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
        pct = 100 * c / total_effects if total_effects > 0 else 0
        print(f"  {t:12} {c:6,} ({pct:5.1f}%)")

    # Sample effects
    print("\nSample Extracted Effects:")
    print("-"*40)
    sample_count = 0
    for r in with_effects[:20]:
        for e in r.get('effects', [])[:2]:
            print(f"  {r['pmcid']}: {e['type']} = {e['value']} (CI: {e['ci_lo']} - {e['ci_hi']})")
            sample_count += 1
            if sample_count >= 15:
                break
        if sample_count >= 15:
            break

    # Save results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump({
            'summary': {
                'total_pdfs': len(all_results),
                'successful': len(successful),
                'with_effects': len(with_effects),
                'total_effects': total_effects,
                'by_type': by_type
            },
            'results': all_results
        }, f, indent=2)

    print(f"\nFull results saved to: {OUTPUT_FILE}")

    # Final verdict
    print("\n" + "="*70)
    extraction_rate = 100 * len(with_effects) / len(successful) if successful else 0
    print(f"EXTRACTION SUCCESS RATE: {extraction_rate:.1f}%")
    print(f"TOTAL EFFECTS FROM {len(successful)} PDFs: {total_effects}")
    print("="*70)

if __name__ == "__main__":
    main()
