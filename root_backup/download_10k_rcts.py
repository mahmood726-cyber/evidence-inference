"""
Download 10,000 Cardiology RCT PDFs from Europe PMC
"""
import os
import json
import time
import urllib.request
import urllib.parse
import ssl
import concurrent.futures
from pathlib import Path

# Disable SSL verification for downloads
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

OUTPUT_DIR = Path("C:/Users/user/cardiology_rcts")
OUTPUT_DIR.mkdir(exist_ok=True)

# Search queries for cardiology RCTs
SEARCH_QUERIES = [
    "heart failure randomized controlled trial",
    "myocardial infarction randomized trial",
    "atrial fibrillation randomized controlled trial",
    "hypertension blood pressure randomized trial",
    "coronary artery disease randomized trial",
    "cardiac surgery randomized controlled trial",
    "arrhythmia randomized trial",
    "cardiomyopathy randomized trial",
    "angina randomized controlled trial",
    "stroke prevention cardiovascular randomized",
    "acute coronary syndrome randomized trial",
    "heart valve randomized trial",
    "percutaneous coronary intervention randomized",
    "coronary bypass surgery randomized trial",
    "anticoagulation cardiovascular randomized",
    "statin cardiovascular randomized trial",
    "beta blocker heart failure randomized",
    "ACE inhibitor cardiovascular randomized",
    "SGLT2 inhibitor heart failure randomized",
    "cardiac rehabilitation randomized trial",
]

def fetch_pmcids(query, page_size=1000, cursor_mark="*"):
    """Fetch PMCIDs from Europe PMC API"""
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": f"{query} OPEN_ACCESS:Y",
        "resultType": "idlist",
        "pageSize": page_size,
        "cursorMark": cursor_mark,
        "format": "json"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            results = data.get("resultList", {}).get("result", [])
            next_cursor = data.get("nextCursorMark", "")
            pmcids = [r.get("pmcid") for r in results if r.get("pmcid")]
            return pmcids, next_cursor
    except Exception as e:
        print(f"Error fetching: {e}")
        return [], ""

def download_pdf(pmcid):
    """Download PDF from Europe PMC"""
    pdf_path = OUTPUT_DIR / f"{pmcid}.pdf"
    if pdf_path.exists() and pdf_path.stat().st_size > 50000:
        return pmcid, "exists"

    pdf_url = f"https://europepmc.org/backend/ptpmcrender.fcgi?accid={pmcid}&blobtype=pdf"

    try:
        req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60, context=ssl_context) as response:
            content = response.read()
            if len(content) > 50000 and content[:4] == b'%PDF':
                with open(pdf_path, 'wb') as f:
                    f.write(content)
                return pmcid, "downloaded"
            else:
                return pmcid, "invalid"
    except Exception as e:
        return pmcid, f"error: {str(e)[:30]}"

def main():
    print("="*60)
    print("DOWNLOADING 10,000 CARDIOLOGY RCT PDFs")
    print("="*60)

    # Collect all PMCIDs
    all_pmcids = set()
    print("\nFetching PMCIDs from Europe PMC...")

    for query in SEARCH_QUERIES:
        print(f"  Query: {query[:50]}...")
        cursor = "*"
        query_count = 0

        while len(all_pmcids) < 15000 and query_count < 5000:
            pmcids, cursor = fetch_pmcids(query, page_size=1000, cursor_mark=cursor)
            if not pmcids:
                break
            all_pmcids.update(pmcids)
            query_count += len(pmcids)
            print(f"    Got {len(pmcids)} (total: {len(all_pmcids)})")
            if not cursor or cursor == "*":
                break
            time.sleep(0.5)

        if len(all_pmcids) >= 15000:
            break

    print(f"\nTotal unique PMCIDs: {len(all_pmcids)}")

    # Download PDFs
    print("\nDownloading PDFs...")
    pmcid_list = list(all_pmcids)[:12000]  # Try 12k to get 10k valid

    downloaded = 0
    exists = 0
    failed = 0

    # Use thread pool for parallel downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_pdf, pmcid): pmcid for pmcid in pmcid_list}

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            pmcid, status = future.result()
            if status == "downloaded":
                downloaded += 1
            elif status == "exists":
                exists += 1
            else:
                failed += 1

            if (i + 1) % 100 == 0:
                total_valid = downloaded + exists
                print(f"  Progress: {i+1}/{len(pmcid_list)} | Valid: {total_valid} | Failed: {failed}")

                # Check if we have enough
                if total_valid >= 10000:
                    print(f"\n  Reached 10,000 PDFs! Stopping early.")
                    executor.shutdown(wait=False, cancel_futures=True)
                    break

    # Final count
    pdf_files = list(OUTPUT_DIR.glob("*.pdf"))
    valid_pdfs = [f for f in pdf_files if f.stat().st_size > 50000]

    print("\n" + "="*60)
    print("DOWNLOAD COMPLETE")
    print("="*60)
    print(f"Total valid PDFs: {len(valid_pdfs)}")
    print(f"New downloads: {downloaded}")
    print(f"Already existed: {exists}")
    print(f"Failed: {failed}")

    # Save list of PMCIDs
    with open(OUTPUT_DIR / "pmcid_list.txt", "w") as f:
        for pdf in valid_pdfs:
            f.write(pdf.stem + "\n")

    print(f"\nPMCID list saved to: {OUTPUT_DIR / 'pmcid_list.txt'}")

if __name__ == "__main__":
    main()
