import requests
import os
import time
import json
from urllib.parse import quote

# Configuration
OUTPUT_DIR = "C:/Users/user/cardiology_rcts"
MIN_FILE_SIZE = 50 * 1024  # 50KB minimum
DELAY_BETWEEN_DOWNLOADS = 0.3  # seconds

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get existing PMC IDs to avoid re-downloading
existing_files = os.listdir(OUTPUT_DIR)
existing_pmcids = set()
for f in existing_files:
    if f.startswith("PMC") and f.endswith(".pdf"):
        pmcid = f.replace(".pdf", "")
        existing_pmcids.add(pmcid)

print(f"Found {len(existing_pmcids)} existing PDFs")

# Search queries for cardiology RCTs - more specific for RCT results
search_queries = [
    'heart failure trial results OPEN_ACCESS:Y',
    'myocardial infarction outcomes randomized OPEN_ACCESS:Y',
    'cardiovascular efficacy trial results OPEN_ACCESS:Y',
    'coronary stent randomized results OPEN_ACCESS:Y',
    'atrial fibrillation randomized trial OPEN_ACCESS:Y',
    'acute coronary syndrome trial OPEN_ACCESS:Y',
    'percutaneous coronary intervention randomized OPEN_ACCESS:Y',
    'cardiac clinical trial OPEN_ACCESS:Y',
    'hypertension randomized controlled trial OPEN_ACCESS:Y',
    'arrhythmia clinical trial OPEN_ACCESS:Y',
    'heart valve randomized OPEN_ACCESS:Y',
    'cardiomyopathy trial OPEN_ACCESS:Y',
    'angina randomized trial OPEN_ACCESS:Y',
    'anticoagulation cardiovascular OPEN_ACCESS:Y',
    'STEMI randomized trial OPEN_ACCESS:Y',
    'NSTEMI trial outcomes OPEN_ACCESS:Y',
    'coronary artery bypass randomized OPEN_ACCESS:Y',
    'cardiac surgery trial OPEN_ACCESS:Y',
    'beta blocker heart trial OPEN_ACCESS:Y',
    'ACE inhibitor heart failure OPEN_ACCESS:Y',
    'statin cardiovascular trial OPEN_ACCESS:Y',
    'antiplatelet coronary trial OPEN_ACCESS:Y',
    'defibrillator randomized trial OPEN_ACCESS:Y',
    'pacemaker clinical trial OPEN_ACCESS:Y',
    'cardiac resynchronization trial OPEN_ACCESS:Y',
    'pulmonary hypertension trial OPEN_ACCESS:Y',
    'endocarditis trial OPEN_ACCESS:Y',
    'aortic stenosis trial OPEN_ACCESS:Y',
    'mitral regurgitation trial OPEN_ACCESS:Y',
    'TAVI randomized trial OPEN_ACCESS:Y',
]

def search_europepmc(query, cursor="*", page_size=1000):
    """Search Europe PMC and return PMC IDs"""
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": query,
        "resultType": "idlist",
        "pageSize": page_size,
        "format": "json",
        "cursorMark": cursor
    }

    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Search error: {e}")
        return None

def download_pdf(pmcid):
    """Download PDF from Europe PMC"""
    url = f"https://europepmc.org/backend/ptpmcrender.fcgi?accid={pmcid}&blobtype=pdf"

    try:
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()

        content = response.content

        # Validate PDF
        if len(content) < MIN_FILE_SIZE:
            print(f"  {pmcid}: Too small ({len(content)} bytes), skipping")
            return False

        if not content.startswith(b'%PDF'):
            print(f"  {pmcid}: Not a valid PDF, skipping")
            return False

        # Save PDF
        filepath = os.path.join(OUTPUT_DIR, f"{pmcid}.pdf")
        with open(filepath, 'wb') as f:
            f.write(content)

        print(f"  {pmcid}: Downloaded ({len(content) // 1024} KB)")
        return True

    except Exception as e:
        print(f"  {pmcid}: Download error - {e}")
        return False

def main():
    total_downloaded = 0
    all_pmcids = set()

    # Collect PMC IDs from all queries
    for query in search_queries:
        print(f"\nSearching: {query}")
        cursor = "*"
        query_count = 0
        pages = 0

        while pages < 10:  # Limit pages per query
            data = search_europepmc(query, cursor)
            if not data:
                break

            # Extract results from the correct structure
            result_list = data.get("resultList", {}).get("result", [])
            if not result_list:
                break

            for item in result_list:
                pmcid = item.get("pmcid")
                if pmcid and pmcid not in existing_pmcids and pmcid not in all_pmcids:
                    all_pmcids.add(pmcid)
                    query_count += 1

            pages += 1

            # Check for next page
            next_cursor = data.get("nextCursorMark")
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor

            print(f"  Page {pages}: Found {query_count} new PMC IDs so far...")
            time.sleep(0.2)

        print(f"  Total new from this query: {query_count}")

    print(f"\n{'='*50}")
    print(f"Total unique new PMC IDs to download: {len(all_pmcids)}")
    print(f"{'='*50}\n")

    # Download PDFs
    pmcid_list = list(all_pmcids)
    for i, pmcid in enumerate(pmcid_list):
        if total_downloaded >= 3500:  # Target + buffer
            print(f"\nReached target of {total_downloaded} downloads")
            break

        print(f"[{i+1}/{len(pmcid_list)}] Downloading {pmcid}...")
        if download_pdf(pmcid):
            total_downloaded += 1
            existing_pmcids.add(pmcid)

        time.sleep(DELAY_BETWEEN_DOWNLOADS)

        if (i + 1) % 100 == 0:
            print(f"\n--- Progress: {total_downloaded} successful downloads out of {i+1} attempts ---\n")

    print(f"\n{'='*50}")
    print(f"Download complete!")
    print(f"Successfully downloaded: {total_downloaded} PDFs")
    print(f"Total PDFs now in folder: {len(existing_pmcids)}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
