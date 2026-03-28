"""
Extract REAL RCT data from ClinicalTrials.gov API v2
Fixed version with proper API parameters
"""

import requests
import json
import time
import os

OUTPUT_PATH = r"C:\Users\user\ctgov_results.json"

def fetch_studies_with_results(page_token=None, page_size=100):
    """Fetch completed studies WITH results from ClinicalTrials.gov API v2"""
    base_url = "https://clinicaltrials.gov/api/v2/studies"

    params = {
        'format': 'json',
        'pageSize': page_size,
        'query.term': 'AREA[StudyType]INTERVENTIONAL AND AREA[OverallStatus]COMPLETED AND AREA[ResultsFirstSubmitDate]RANGE[MIN,MAX]',
        'fields': 'NCTId,BriefTitle,Condition,Phase,EnrollmentInfo,OutcomeMeasuresModule'
    }

    if page_token:
        params['pageToken'] = page_token

    try:
        response = requests.get(base_url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  API returned status {response.status_code}")
            print(f"  URL: {response.url[:200]}...")
            return None
    except Exception as e:
        print(f"  Request error: {e}")
        return None


def extract_outcome_results(study):
    """Extract primary outcome results from study"""
    results = []

    try:
        protocol = study.get('protocolSection', {})
        results_section = study.get('resultsSection', {})

        if not results_section:
            return []

        # Get identification
        ident = protocol.get('identificationModule', {})
        nct_id = ident.get('nctId', '')
        title = ident.get('briefTitle', '')

        # Get outcome measures from results
        outcome_measures = results_section.get('outcomeMeasuresModule', {})
        outcome_list = outcome_measures.get('outcomeMeasures', [])

        for outcome in outcome_list:
            outcome_type = outcome.get('type', '')
            if outcome_type != 'Primary':
                continue

            title_outcome = outcome.get('title', '')
            classes = outcome.get('classes', [])

            for cls in classes:
                categories = cls.get('categories', [])
                for cat in categories:
                    measurements = cat.get('measurements', [])

                    # Look for statistical analysis
                    analyses = outcome.get('analyses', [])
                    for analysis in analyses:
                        stat_method = analysis.get('statisticalMethod', '')
                        param_type = analysis.get('paramType', '')
                        param_value = analysis.get('paramValue')
                        ci_lower = analysis.get('ciLowerLimit')
                        ci_upper = analysis.get('ciUpperLimit')
                        ci_pct = analysis.get('ciPctValue')
                        p_value = analysis.get('pValue')

                        if param_value and ci_lower and ci_upper:
                            # Determine effect type
                            if 'odds' in stat_method.lower() or 'OR' in param_type:
                                effect_type = 'OR'
                            elif 'hazard' in stat_method.lower() or 'HR' in param_type:
                                effect_type = 'HR'
                            elif 'risk ratio' in stat_method.lower() or 'RR' in param_type:
                                effect_type = 'RR'
                            elif 'mean diff' in stat_method.lower() or 'MD' in param_type:
                                effect_type = 'MD'
                            else:
                                effect_type = 'Unknown'

                            results.append({
                                'nct_id': nct_id,
                                'title': title,
                                'outcome': title_outcome,
                                'effect_type': effect_type,
                                'value': param_value,
                                'ci_lo': ci_lower,
                                'ci_hi': ci_upper,
                                'p_value': p_value,
                                'method': stat_method
                            })
    except Exception as e:
        pass

    return results


def main():
    print("=" * 70)
    print("  EXTRACTING CLINICALTRIALS.GOV COMPLETED STUDIES WITH RESULTS")
    print("=" * 70 + "\n")

    # First, let's check API connectivity with a simple query
    print("Testing API connection...")
    test_url = "https://clinicaltrials.gov/api/v2/studies?format=json&pageSize=1"
    try:
        resp = requests.get(test_url, timeout=10)
        print(f"  API Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            total = data.get('totalCount', 0)
            print(f"  Total studies in database: {total:,}")
    except Exception as e:
        print(f"  Connection error: {e}")
        return

    # Now try to get studies with results
    print("\nFetching completed interventional studies with results...")

    all_results = []
    next_token = None
    page = 0
    max_pages = 100  # Limit for testing

    while page < max_pages:
        data = fetch_studies_with_results(next_token)

        if not data:
            print("  No data returned, stopping.")
            break

        studies = data.get('studies', [])
        if not studies:
            print("  No more studies.")
            break

        for study in studies:
            outcomes = extract_outcome_results(study)
            all_results.extend(outcomes)

        next_token = data.get('nextPageToken')
        if not next_token:
            print("  Reached end of results.")
            break

        page += 1
        if page % 10 == 0:
            print(f"  Page {page}: {len(all_results)} results extracted")

        time.sleep(0.2)

    print(f"\nTotal outcome results extracted: {len(all_results)}")

    if all_results:
        # Count by effect type
        type_counts = {}
        for r in all_results:
            et = r['effect_type']
            type_counts[et] = type_counts.get(et, 0) + 1

        print("\nBy effect type:")
        for et, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {et:15} {count:,}")

        # Save to JSON
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)
        print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
