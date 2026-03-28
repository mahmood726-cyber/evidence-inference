"""
Extract REAL RCT data from ClinicalTrials.gov API v2
Focus on interventional randomized trials with statistical analyses
"""

import requests
import json
import time
import os

OUTPUT_DIR = r"C:\Users\user\Downloads\Dataextractor"

def fetch_rcts_with_results(page_token=None, page_size=100):
    """Fetch completed RCTs with results"""
    url = "https://clinicaltrials.gov/api/v2/studies"

    # Query for interventional, randomized, completed studies with results
    params = {
        'format': 'json',
        'pageSize': page_size,
        'query.term': 'AREA[StudyType]INTERVENTIONAL AND AREA[DesignAllocation]RANDOMIZED AND AREA[ResultsFirstPostDate]RANGE[MIN,MAX]'
    }

    if page_token:
        params['pageToken'] = page_token

    try:
        resp = requests.get(url, params=params, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"  API error: {resp.status_code}")
            return None
    except Exception as e:
        print(f"  Request error: {e}")
        return None


def extract_statistical_results(study):
    """Extract effect sizes and CIs from study results"""
    results = []

    try:
        proto = study.get('protocolSection', {})
        results_section = study.get('resultsSection', {})

        if not results_section:
            return []

        # Get study info
        ident = proto.get('identificationModule', {})
        nct_id = ident.get('nctId', '')
        title = ident.get('briefTitle', '')

        # Get conditions
        conditions = proto.get('conditionsModule', {}).get('conditions', [])
        condition = conditions[0] if conditions else 'Unknown'

        # Get enrollment
        design = proto.get('designModule', {})
        enrollment = design.get('enrollmentInfo', {}).get('count', 0)

        # Get outcome measures
        outcomes_module = results_section.get('outcomeMeasuresModule', {})
        outcome_measures = outcomes_module.get('outcomeMeasures', [])

        for outcome in outcome_measures:
            # Only primary outcomes
            if outcome.get('type') != 'PRIMARY':
                continue

            outcome_title = outcome.get('title', '')

            # Check for statistical analyses
            analyses = outcome.get('analyses', [])
            for analysis in analyses:
                stat_method = analysis.get('statisticalMethod', '')
                param_type = analysis.get('paramType', '')
                param_value = analysis.get('paramValue')
                ci_pct = analysis.get('ciPctValue')
                ci_lower = analysis.get('ciLowerLimit')
                ci_upper = analysis.get('ciUpperLimit')
                p_value = analysis.get('pValue')

                # Skip if no effect size or CI
                if param_value is None or ci_lower is None or ci_upper is None:
                    continue

                # Try to parse numeric values
                try:
                    val = float(param_value)
                    lo = float(ci_lower)
                    hi = float(ci_upper)
                except (ValueError, TypeError):
                    continue

                # Skip invalid CIs
                if lo >= hi:
                    continue

                # Determine effect type from method/paramType
                effect_type = None
                method_lower = stat_method.lower() if stat_method else ''
                param_lower = param_type.lower() if param_type else ''

                if 'odds ratio' in method_lower or param_lower == 'odds ratio':
                    effect_type = 'OR'
                elif 'hazard ratio' in method_lower or param_lower == 'hazard ratio':
                    effect_type = 'HR'
                elif 'risk ratio' in method_lower or 'relative risk' in method_lower:
                    effect_type = 'RR'
                elif 'risk difference' in method_lower:
                    effect_type = 'RD'
                elif 'mean difference' in method_lower or param_lower == 'mean difference':
                    effect_type = 'MD'
                elif 'standardized mean' in method_lower:
                    effect_type = 'SMD'
                elif 'ratio' in method_lower and val > 0:
                    effect_type = 'RR'  # Generic ratio
                elif 'difference' in method_lower:
                    effect_type = 'MD'  # Generic difference

                if not effect_type:
                    continue

                # Get group sample sizes if available
                groups = outcome.get('groups', [])
                n_treatment = None
                n_control = None

                if len(groups) >= 2:
                    # Try to identify treatment and control groups
                    for g in groups:
                        g_title = g.get('title', '').lower()
                        g_desc = g.get('description', '').lower()
                        # This is approximate - would need more context

                results.append({
                    'nct_id': nct_id,
                    'title': title,
                    'condition': condition[:50],
                    'outcome': outcome_title[:100],
                    'effect_type': effect_type,
                    'value': round(val, 4),
                    'ci_lo': round(lo, 4),
                    'ci_hi': round(hi, 4),
                    'ci_pct': ci_pct,
                    'p_value': p_value,
                    'method': stat_method[:50] if stat_method else None,
                    'enrollment': enrollment
                })

    except Exception as e:
        pass

    return results


def main():
    print("=" * 70)
    print("  EXTRACTING CLINICALTRIALS.GOV RCT RESULTS")
    print("  Focus: Interventional, Randomized, with Statistical Analyses")
    print("=" * 70)

    all_results = []
    next_token = None
    page = 0
    max_pages = 500  # Up to 50,000 studies
    studies_checked = 0

    print("\nFetching randomized controlled trials with results...")

    while page < max_pages:
        data = fetch_rcts_with_results(next_token)

        if not data:
            print("  No data returned")
            break

        studies = data.get('studies', [])
        if not studies:
            print("  No more studies")
            break

        for study in studies:
            studies_checked += 1
            extracted = extract_statistical_results(study)
            all_results.extend(extracted)

        next_token = data.get('nextPageToken')
        if not next_token:
            print("  Reached end of results")
            break

        page += 1
        if page % 10 == 0:
            print(f"  Page {page}: Checked {studies_checked:,} studies, extracted {len(all_results):,} results")

        time.sleep(0.2)  # Rate limiting

    print(f"\nTotal studies checked: {studies_checked:,}")
    print(f"Total results extracted: {len(all_results):,}")

    if all_results:
        # Count by effect type
        type_counts = {}
        for r in all_results:
            et = r['effect_type']
            type_counts[et] = type_counts.get(et, 0) + 1

        print("\nBy effect type:")
        for et, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {et:10} {count:,}")

        # Save to JSON
        json_path = os.path.join(OUTPUT_DIR, "ctgov_rct_results.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)
        print(f"\nSaved to {json_path}")

        # Show sample results
        print("\nSample results:")
        for r in all_results[:5]:
            print(f"  {r['nct_id']}: {r['effect_type']} {r['value']} ({r['ci_lo']}-{r['ci_hi']})")


if __name__ == '__main__':
    main()
