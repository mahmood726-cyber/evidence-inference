"""
Extract COMPLETE statistical results from ClinicalTrials.gov API v2
Saves incrementally to prevent data loss
"""

import requests
import json
import time
import sys
import os

OUTPUT_PATH = r"C:\Users\user\Downloads\Dataextractor\ctgov_rct_results.json"
CHECKPOINT_PATH = r"C:\Users\user\ctgov_checkpoint.json"

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

                # Skip if missing critical data
                if param_value is None or ci_lower is None or ci_upper is None:
                    continue

                # Parse values
                try:
                    val = float(param_value)
                    lo = float(ci_lower)
                    hi = float(ci_upper)
                except:
                    continue

                # Skip invalid CI
                if lo >= hi:
                    continue

                # Determine effect type
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

    except Exception as e:
        pass

    return results


def save_results(all_results):
    """Save results to file"""
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    print(f"  Saved {len(all_results):,} results")


def main():
    print("=" * 70)
    print("  CLINICALTRIALS.GOV - INCREMENTAL EXTRACTION")
    print("=" * 70)
    print()
    sys.stdout.flush()

    all_results = []
    next_token = None
    page = 0
    max_pages = 400  # Stop at 40,000 studies (where it was working)
    studies_checked = 0
    consecutive_errors = 0
    max_consecutive_errors = 5

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
            print(f"  Page {page}: {studies_checked:,} studies, {len(all_results):,} results")
            sys.stdout.flush()
            # Save checkpoint every 100 pages
            if page % 100 == 0:
                save_results(all_results)

        time.sleep(0.2)

    print()
    print(f"Total studies checked: {studies_checked:,}")
    print(f"Complete results extracted: {len(all_results):,}")

    if all_results:
        # Count by type
        types = {}
        for r in all_results:
            t = r['effect_type']
            types[t] = types.get(t, 0) + 1

        print("\nBy effect type:")
        for t, c in sorted(types.items(), key=lambda x: -x[1]):
            print(f"  {t:10} {c:,}")

        # Save
        save_results(all_results)
        print(f"\nFinal save to {OUTPUT_PATH}")

        # Samples
        print("\nSample results:")
        for r in all_results[:5]:
            print(f"  {r['nct_id']}: {r['effect_type']} {r['value']} ({r['ci_lo']}-{r['ci_hi']})")


if __name__ == '__main__':
    main()
