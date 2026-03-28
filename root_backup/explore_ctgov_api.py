"""
Explore ClinicalTrials.gov API v2 to understand results data structure
"""

import requests
import json

print("=" * 70)
print("  EXPLORING CLINICALTRIALS.GOV API v2 RESULTS STRUCTURE")
print("=" * 70)

# First, test basic API
print("\n1. Testing basic API connection...")
url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    'format': 'json',
    'pageSize': 1
}

resp = requests.get(url, params=params, timeout=30)
print(f"   Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    print(f"   Total studies: {data.get('totalCount', 0):,}")

# Try to get a study with results
print("\n2. Fetching studies WITH results posted...")
params = {
    'format': 'json',
    'pageSize': 3,
    'query.term': 'AREA[ResultsFirstPostDate]RANGE[2024-01-01,MAX]',
    'fields': 'NCTId|BriefTitle|HasResults'
}

resp = requests.get(url, params=params, timeout=30)
print(f"   Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    studies = data.get('studies', [])
    print(f"   Found {len(studies)} studies")
    for s in studies[:3]:
        proto = s.get('protocolSection', {})
        ident = proto.get('identificationModule', {})
        print(f"   - {ident.get('nctId')}: {ident.get('briefTitle', '')[:50]}...")

# Get full study with results section
print("\n3. Fetching full study with ResultsSection...")
params = {
    'format': 'json',
    'pageSize': 1,
    'query.term': 'AREA[ResultsFirstPostDate]RANGE[2024-01-01,MAX]'
}

resp = requests.get(url, params=params, timeout=30)
print(f"   Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    studies = data.get('studies', [])
    if studies:
        study = studies[0]

        # Check what sections are available
        print("\n   Available top-level keys:")
        for key in study.keys():
            print(f"     - {key}")

        # Check resultsSection
        results = study.get('resultsSection', {})
        if results:
            print("\n   ResultsSection keys:")
            for key in results.keys():
                print(f"     - {key}")

            # Check outcomeMeasuresModule
            outcomes = results.get('outcomeMeasuresModule', {})
            if outcomes:
                print("\n   OutcomeMeasuresModule keys:")
                for key in outcomes.keys():
                    print(f"     - {key}")

                # Check individual outcome measures
                measures = outcomes.get('outcomeMeasures', [])
                if measures:
                    print(f"\n   Found {len(measures)} outcome measures")
                    for i, m in enumerate(measures[:2]):
                        print(f"\n   Outcome {i+1} keys:")
                        for key in m.keys():
                            val = m.get(key)
                            if isinstance(val, (str, int, float, bool)):
                                print(f"     - {key}: {str(val)[:60]}")
                            elif isinstance(val, list):
                                print(f"     - {key}: [list with {len(val)} items]")
                            elif isinstance(val, dict):
                                print(f"     - {key}: {{dict with {len(val)} keys}}")

                        # Check for analyses (statistical results)
                        analyses = m.get('analyses', [])
                        if analyses:
                            print(f"\n     Analyses ({len(analyses)} found):")
                            for a in analyses[:2]:
                                print(f"       Analysis keys: {list(a.keys())}")
                                # Print interesting fields
                                for field in ['statisticalMethod', 'paramType', 'paramValue',
                                             'ciPctValue', 'ciLowerLimit', 'ciUpperLimit', 'pValue']:
                                    if field in a:
                                        print(f"         {field}: {a[field]}")
        else:
            print("\n   No resultsSection in this study")

# Save full response for inspection
print("\n4. Saving full study JSON for inspection...")
with open("C:/Users/user/ctgov_sample_study.json", 'w') as f:
    json.dump(study if studies else {}, f, indent=2)
print("   Saved to ctgov_sample_study.json")

print("\n" + "=" * 70)
print("  EXPLORATION COMPLETE")
print("=" * 70)
