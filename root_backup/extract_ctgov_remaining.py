"""
Extract REMAINING ClinicalTrials.gov results (pages 401-714)
Continue from where we left off
"""

import requests
import json
import time
import sys

OUTPUT_PATH = r"C:\Users\user\Downloads\Dataextractor\ctgov_rct_results_part2.json"
EXISTING_PATH = r"C:\Users\user\Downloads\Dataextractor\ctgov_rct_results.json"

def fetch_page(page_token=None):
    """Fetch one page of RCTs with results"""
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        'format': 'json',
        'pageSize': 100,
        'query.term': 'AREA[StudyType]INTERVENTIONAL AND AREA[ResultsFirstPostDate]RANGE[MIN,MAX]'
    }
    if page_token:
        params['pageToken'] = page_token

    try:
        resp = requests.get(url, params=params, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"  HTTP {resp.status_code}")
            return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def extract_complete_results(study):
    """Extract only COMPLETE results with effect size and CI"""
    results = []

    try:
        proto = study.get('protocolSection', {})
        results_sec = study.get('resultsSection', {})
        if not results_sec:
            return []

        nct_id = proto.get('identificationModule', {}).get('nctId', '')
        title = proto.get('identificationModule', {}).get('briefTitle', '')[:80]
        conditions = proto.get('conditionsModule', {}).get('conditions', ['Unknown'])
        condition = conditions[0][:40] if conditions else 'Unknown'
        enrollment = proto.get('designModule', {}).get('enrollmentInfo', {}).get('count', 0)

        outcomes = results_sec.get('outcomeMeasuresModule', {}).get('outcomeMeasures', [])

        for outcome in outcomes:
            outcome_type = outcome.get('type', '')
            outcome_title = outcome.get('title', '')[:60]

            analyses = outcome.get('analyses', [])
            for analysis in analyses:
                param_value = analysis.get('paramValue')
                ci_lower = analysis.get('ciLowerLimit')
                ci_upper = analysis.get('ciUpperLimit')
                method = analysis.get('statisticalMethod', '')
                param_type = analysis.get('paramType', '')
                p_value = analysis.get('pValue')

                if param_value is None or ci_lower is None or ci_upper is None:
                    continue

                try:
                    val = float(param_value)
                    lo = float(ci_lower)
                    hi = float(ci_upper)
                except:
                    continue

                if lo >= hi:
                    continue

                effect_type = None
                m = method.lower() if method else ''
                p = param_type.lower() if param_type else ''

                if 'odds ratio' in m or 'odds ratio' in p:
                    effect_type = 'OR'
                elif 'hazard ratio' in m or 'hazard ratio' in p:
                    effect_type = 'HR'
                elif 'risk ratio' in m or 'relative risk' in m or 'risk ratio' in p:
                    effect_type = 'RR'
                elif 'risk difference' in m or 'risk difference' in p:
                    effect_type = 'RD'
                elif 'mean difference' in m or 'mean difference' in p or 'difference in means' in p:
                    effect_type = 'MD'
                elif 'standardized mean' in m or 'standardized mean' in p:
                    effect_type = 'SMD'
                elif 'difference' in p and abs(val) < 100:
                    effect_type = 'MD'
                elif 'ratio' in p and val > 0:
                    effect_type = 'RR'

                if not effect_type:
                    continue

                results.append({
                    'nct_id': nct_id,
                    'title': title,
                    'condition': condition,
                    'outcome': outcome_title,
                    'outcome_type': outcome_type,
                    'effect_type': effect_type,
                    'value': round(val, 4),
                    'ci_lo': round(lo, 4),
                    'ci_hi': round(hi, 4),
                    'p_value': p_value,
                    'method': method[:40] if method else None,
                    'enrollment': enrollment
                })

    except:
        pass

    return results


def save_results(all_results):
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    print(f"  Saved {len(all_results):,} results")


def main():
    print("=" * 70)
    print("  CLINICALTRIALS.GOV - EXTRACTING REMAINING STUDIES (40K-71K)")
    print("=" * 70)
    print()
    sys.stdout.flush()

    # Skip first 400 pages (40,000 studies already done)
    print("Skipping to page 401...")
    next_token = None
    page = 0

    # Fast-forward through first 400 pages
    while page < 400:
        data = fetch_page(next_token)
        if not data:
            time.sleep(2)
            continue
        next_token = data.get('nextPageToken')
        if not next_token:
            print("Reached end during skip")
            return
        page += 1
        if page % 50 == 0:
            print(f"  Skipping page {page}...")
            sys.stdout.flush()
        time.sleep(0.1)

    print(f"Starting extraction from page {page + 1}...")

    all_results = []
    studies_checked = 0
    consecutive_errors = 0
    max_consecutive_errors = 5
    max_pages = 715  # Up to ~71,500 studies

    while page < max_pages:
        data = fetch_page(next_token)

        if not data:
            consecutive_errors += 1
            print(f"  Error {consecutive_errors}/{max_consecutive_errors}")
            if consecutive_errors >= max_consecutive_errors:
                print("  Too many errors, saving and stopping...")
                break
            time.sleep(5)
            continue

        consecutive_errors = 0

        studies = data.get('studies', [])
        if not studies:
            print("  No more studies")
            break

        for study in studies:
            studies_checked += 1
            extracted = extract_complete_results(study)
            all_results.extend(extracted)

        next_token = data.get('nextPageToken')
        if not next_token:
            print("  Reached end")
            break

        page += 1
        if page % 20 == 0:
            print(f"  Page {page}: {studies_checked:,} more studies, {len(all_results):,} results")
            sys.stdout.flush()
            if page % 100 == 0:
                save_results(all_results)

        time.sleep(0.2)

    print()
    print(f"Additional studies checked: {studies_checked:,}")
    print(f"Additional results extracted: {len(all_results):,}")

    if all_results:
        types = {}
        for r in all_results:
            t = r['effect_type']
            types[t] = types.get(t, 0) + 1

        print("\nBy effect type:")
        for t, c in sorted(types.items(), key=lambda x: -x[1]):
            print(f"  {t:10} {c:,}")

        save_results(all_results)
        print(f"\nFinal save to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
