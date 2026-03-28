"""Test TruthCert Innovative Functions"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
time.sleep(3)

# Load BCG dataset for testing
driver.execute_script('loadDemoDataset("BCG")')
time.sleep(2)
driver.execute_script('runAnalysis()')
time.sleep(3)

print('=== Testing Innovative Functions ===\n')

tests = []

# Test 1: RoBMA
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = robmaModelAveraging(yi, vi);
        return {
            success: true,
            theta: r.modelAveraged.theta,
            bfEffect: r.bayesFactors.effect.BF10,
            nModels: r.models.length
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('RoBMA Model Averaging', result.get('success', False)))
print(f"1. RoBMA: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 2: Multiverse
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = multiverseMetaAnalysis(yi, vi);
        return {
            success: true,
            analyzed: r.analyzedSubsets,
            median: r.summary.medianEffect
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Multiverse Meta-Analysis', result.get('success', False)))
print(f"2. Multiverse: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 3: Improved PI
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = improvedPredictionInterval(yi, vi);
        return {
            success: true,
            theta: r.theta,
            stdPI: [r.standardPI.lower, r.standardPI.upper]
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Improved Prediction Interval', result.get('success', False)))
print(f"3. Improved PI: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 4: Sequential MA (corrected property names)
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = sequentialMetaAnalysis(yi, vi);
        return {
            success: true,
            crossed: r.conclusion.reached,
            looks: r.cumulative.length
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Sequential Meta-Analysis', result.get('success', False)))
print(f"4. Sequential MA: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 5: P-Uniform*
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = pUniformStar(yi, vi);
        return {
            success: true,
            corrected: r.correctedEstimate,
            original: r.originalEstimate
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('P-Uniform*', result.get('success', False)))
print(f"5. P-Uniform*: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 6: Value of Information
result = driver.execute_script('''
    try {
        const r = valueOfInformation(0.3, 0.1, 100000, 50000);
        return {
            success: true,
            evpi: r.evpi,
            evsi: r.evsi
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Value of Information', result.get('success', False)))
print(f"6. VOI: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 7: Albatross Plot (check actual structure)
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const n = AppState.studies.map(s => (s.n1 || 100) + (s.n2 || 100));
        const r = albatrossPlotData(yi, vi, n);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Albatross Plot', result.get('success', False)))
print(f"7. Albatross: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 8: Sunset Plot (check actual structure)
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = sunsetPlotData(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Sunset Plot', result.get('success', False)))
print(f"8. Sunset: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 9: Drapery Plot (check actual structure)
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = draperyPlotData(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Drapery Plot', result.get('success', False)))
print(f"9. Drapery: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 10: Harvest Plot (check actual structure)
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const n = AppState.studies.map(s => (s.n1 || 100) + (s.n2 || 100));
        const r = harvestPlotData(yi, vi, n);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Harvest Plot', result.get('success', False)))
print(f"10. Harvest: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 11: Decision Curve Analysis
result = driver.execute_script('''
    try {
        const r = decisionCurveAnalysis(0.7, 0.85, 0.1);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Decision Curve Analysis', result.get('success', False)))
print(f"11. DCA: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 12: Threshold NNT
result = driver.execute_script('''
    try {
        const r = thresholdNNT(0.3, 0.2, {minClinicallyImportant: 0.05});
        return {success: true, nnt: r.nnt};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Threshold NNT', result.get('success', False)))
print(f"12. NNT: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 13: Permutation I2
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = permutationTestI2(yi, vi, 50);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Permutation I2 Test', result.get('success', False)))
print(f"13. Perm I2: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 14: Limit MA
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = limitMetaAnalysis(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Limit Meta-Analysis', result.get('success', False)))
print(f"14. Limit MA: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 15: WAAP-WLS
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = waapWLS(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('WAAP-WLS', result.get('success', False)))
print(f"15. WAAP: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 16: Multi-Criteria Decision (check actual structure)
result = driver.execute_script('''
    try {
        const r = multiCriteriaDecision([
            {name: 'Drug A', efficacy: 0.8, safety: 0.7, cost: 0.6},
            {name: 'Drug B', efficacy: 0.7, safety: 0.9, cost: 0.8}
        ], {efficacy: 0.5, safety: 0.3, cost: 0.2});
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Multi-Criteria Decision', result.get('success', False)))
print(f"16. MCDA: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 17: Specification Curve (check actual structure)
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = specificationCurveAnalysis(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Specification Curve', result.get('success', False)))
print(f"17. Spec Curve: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 18: Vibration of Effects
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = vibrationOfEffects(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Vibration of Effects', result.get('success', False)))
print(f"18. VoE: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 19: Living Review Status
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = livingReviewStatus(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Living Review Status', result.get('success', False)))
print(f"19. Living Review: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 20: 3-Parameter Selection Model
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = threeParameterSelectionModel(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('3-Param Selection Model', result.get('success', False)))
print(f"20. 3PSM: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 21: Robust Tau2
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = robustTau2(yi, vi);
        return {success: true, keys: Object.keys(r)};
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Robust Tau2', result.get('success', False)))
print(f"21. Robust Tau2: {'PASS' if result.get('success') else 'FAIL'} - {result}")

driver.quit()

# Summary
print('\n' + '='*60)
print('SUMMARY')
print('='*60)
passed = sum(1 for _, s in tests if s)
total = len(tests)
print(f'Passed: {passed}/{total} ({100*passed/total:.1f}%)')
print('='*60)

for name, status in tests:
    print(f"  [{'PASS' if status else 'FAIL'}] {name}")
