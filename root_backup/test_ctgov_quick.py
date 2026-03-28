"""
Quick test of ClinicalTrials.gov API - find studies with statistical analyses
"""

import requests
import json

print("Testing ClinicalTrials.gov API...")

url = "https://clinicaltrials.gov/api/v2/studies"

# Simple query for randomized trials with results
params = {
    'format': 'json',
    'pageSize': 20,
    'query.term': 'AREA[StudyType]INTERVENTIONAL AND AREA[ResultsFirstPostDate]RANGE[2024-01-01,MAX]'
}

print(f"Fetching studies...")
resp = requests.get(url, params=params, timeout=60)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    studies = data.get('studies', [])
    print(f"Got {len(studies)} studies")

    found_analyses = 0
    for study in studies:
        results_section = study.get('resultsSection', {})
        if not results_section:
            continue

        outcomes_module = results_section.get('outcomeMeasuresModule', {})
        outcomes = outcomes_module.get('outcomeMeasures', [])

        for outcome in outcomes:
            analyses = outcome.get('analyses', [])
            if analyses:
                found_analyses += 1
                nct = study.get('protocolSection', {}).get('identificationModule', {}).get('nctId', 'Unknown')
                print(f"\nStudy {nct} has {len(analyses)} analyses:")
                for a in analyses[:2]:
                    print(f"  Method: {a.get('statisticalMethod', 'N/A')}")
                    print(f"  ParamType: {a.get('paramType', 'N/A')}")
                    print(f"  Value: {a.get('paramValue', 'N/A')}")
                    print(f"  CI: {a.get('ciLowerLimit', 'N/A')} - {a.get('ciUpperLimit', 'N/A')}")
                    print(f"  P-value: {a.get('pValue', 'N/A')}")
                break  # Just show first outcome with analyses

    print(f"\nStudies with analyses: {found_analyses}")
