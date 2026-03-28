"""Test final editorial features"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(3)

print('='*70)
print('TESTING FINAL EDITORIAL FEATURES')
print('='*70)

passed = 0
failed = 0

def test(name, condition):
    global passed, failed
    if condition:
        print(f'[PASS] {name}')
        passed += 1
    else:
        print(f'[FAIL] {name}')
        failed += 1

# Check for JS errors
logs = driver.get_log('browser')
errors = [l for l in logs if l['level'] == 'SEVERE']
test('No JS errors', len(errors) == 0)
if errors:
    for e in errors[:3]:
        print(f'  Error: {e["message"]}')

# Load data and run analysis
driver.execute_script("loadDemoDataset('thrombolytics')")
time.sleep(0.5)
driver.execute_script("document.getElementById('runAnalysisBtn').click()")
time.sleep(3)

# 1. Profile Likelihood CI for tau-squared
print('\n[1] PROFILE LIKELIHOOD CI')
pl_exists = driver.execute_script("return typeof ProfileLikelihood !== 'undefined'")
test('ProfileLikelihood module exists', pl_exists)

if pl_exists:
    tau2 = driver.execute_script("return AppState.results?.heterogeneity?.tau2")
    processed = driver.execute_script("return AppState.results?.processed")

    pl_ci = driver.execute_script("""
        const tau2 = AppState.results?.heterogeneity?.tau2;
        const processed = AppState.results?.processed;
        return ProfileLikelihood.computeTau2CI(processed, tau2);
    """)
    test('computeTau2CI() works', pl_ci is not None)
    if pl_ci:
        test('Returns lower bound', 'lower' in pl_ci)
        test('Returns upper bound', 'upper' in pl_ci)
        print(f'  Tau² = {tau2:.4f}, 95% CI: [{pl_ci["lower"]:.4f}, {pl_ci["upper"]:.4f}]')

    qp_ci = driver.execute_script("""
        const tau2 = AppState.results?.heterogeneity?.tau2;
        const processed = AppState.results?.processed;
        return ProfileLikelihood.computeQProfile(processed, tau2);
    """)
    test('computeQProfile() works', qp_ci is not None)
    if qp_ci:
        print(f'  Q-Profile CI: [{qp_ci["lower"]:.4f}, {qp_ci["upper"]:.4f}]')

# 2. GRADE-NMA Assessment
print('\n[2] GRADE-NMA CERTAINTY ASSESSMENT')
grade_exists = driver.execute_script("return typeof GradeNMA !== 'undefined'")
test('GradeNMA module exists', grade_exists)

if grade_exists:
    grade_result = driver.execute_script("""
        const studies = AppState.studies;
        const results = AppState.results;
        return GradeNMA.assessCertainty('SK vs tPA', results, studies);
    """)
    test('assessCertainty() works', grade_result is not None)
    if grade_result:
        test('Returns overall rating', 'overall' in grade_result)
        test('Returns domain assessments', 'domains' in grade_result)
        print(f'  Overall certainty: {grade_result["overall"]}')
        for domain, assessment in grade_result.get('domains', {}).items():
            level = assessment.get('level', '?')
            reason = assessment.get('reason', '')
            print(f'    {domain}: {level} ({reason})')

# 3. Node-Splitting Inconsistency
print('\n[3] NODE-SPLITTING INCONSISTENCY TEST')
ns_exists = driver.execute_script("return typeof NodeSplittingTest !== 'undefined'")
test('NodeSplittingTest module exists', ns_exists)

if ns_exists:
    ns_result = driver.execute_script("""
        const studies = AppState.studies;
        const effectMeasure = AppState.effectMeasure || 'OR';
        const reference = AppState.reference || 'SK';
        return NodeSplittingTest.analyze(studies, effectMeasure, reference);
    """)
    test('analyze() works', ns_result is not None)
    if ns_result:
        test('Returns comparisons array', 'comparisons' in ns_result and len(ns_result['comparisons']) > 0)
        test('Returns global test', 'globalTest' in ns_result)
        print(f'  Comparisons tested: {len(ns_result.get("comparisons", []))}')
        print(f'  Global test: Chi²={ns_result["globalTest"]["chi2"]:.2f}, df={ns_result["globalTest"]["df"]}, p={ns_result["globalTest"]["pValue"]:.4f}')
        print(f'  Has inconsistency: {ns_result.get("hasInconsistency", False)}')

        # Show individual comparisons
        for comp in ns_result.get('comparisons', [])[:3]:
            status = 'INCONSISTENT' if comp.get('inconsistent') else 'consistent'
            print(f'    {comp["comparison"]}: direct={comp["direct"]["effect"]:.3f}, indirect={comp["indirect"]["effect"]:.3f}, p={comp["pValue"]:.4f} [{status}]')

driver.quit()

print()
print('='*70)
print(f'SUMMARY: {passed}/{passed+failed} tests passed ({100*passed/(passed+failed):.0f}%)')
print('='*70)
