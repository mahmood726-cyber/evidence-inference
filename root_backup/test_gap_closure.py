"""Test TruthCert Gap Closure Functions - GLMM, Network MA, Profile Likelihood"""
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

print('=== Testing Gap Closure Functions ===\n')

tests = []

# Test 1: GLMM Meta-Analysis
result = driver.execute_script('''
    try {
        // BCG data - use raw counts
        const ai = [4, 6, 3, 62, 33, 180];
        const bi = [119, 300, 228, 13536, 5036, 1361];
        const ci = [11, 29, 11, 248, 47, 372];
        const di = [128, 274, 209, 12619, 5765, 1079];
        const r = glmmMetaAnalysis(ai, bi, ci, di);
        return {
            success: true,
            method: r.method,
            estimate: r.estimate.exp,
            tau2: r.tau2,
            hasZeroCells: r.hasZeroCells
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('GLMM Meta-Analysis', result.get('success', False)))
print(f"1. GLMM: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 2: Beta-Binomial MA
result = driver.execute_script('''
    try {
        const ai = [4, 6, 3, 62, 33, 180];
        const bi = [119, 300, 228, 13536, 5036, 1361];
        const ci = [11, 29, 11, 248, 47, 372];
        const di = [128, 274, 209, 12619, 5765, 1079];
        const r = betaBinomialMA(ai, bi, ci, di);
        return {
            success: true,
            method: r.method,
            OR: r.estimate.OR,
            overdispersion: r.overdispersion.interpretation
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Beta-Binomial MA', result.get('success', False)))
print(f"2. Beta-Binomial: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 3: Network MA Consistency
result = driver.execute_script('''
    try {
        const treatments = ['A', 'B', 'C', 'D'];
        const comparisons = [
            {t1: 'A', t2: 'B', effect: -0.5, se: 0.2, design: 'AB'},
            {t1: 'A', t2: 'C', effect: -0.3, se: 0.25, design: 'AC'},
            {t1: 'B', t2: 'C', effect: 0.1, se: 0.15, design: 'BC'},
            {t1: 'B', t2: 'D', effect: -0.4, se: 0.3, design: 'BD'},
            {t1: 'C', t2: 'D', effect: -0.2, se: 0.2, design: 'CD'}
        ];
        const r = networkMAConsistency(treatments, comparisons);
        return {
            success: true,
            method: r.method,
            nTreatments: r.nTreatments,
            globalPvalue: r.globalInconsistency.pValue,
            interpretation: r.interpretation
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Network MA Consistency', result.get('success', False)))
print(f"3. NMA Consistency: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 4: Side-Splitting Test
result = driver.execute_script('''
    try {
        const network = {
            treatments: ['Placebo', 'DrugA', 'DrugB'],
            comparisons: [
                {t1: 'Placebo', t2: 'DrugA', effect: -0.8, se: 0.2, design: 'PA'},
                {t1: 'Placebo', t2: 'DrugB', effect: -0.6, se: 0.25, design: 'PB'},
                {t1: 'DrugA', t2: 'DrugB', effect: 0.1, se: 0.15, design: 'AB'}
            ]
        };
        const r = sideSplittingTest(network);
        return {
            success: true,
            method: r.method,
            nInconsistent: r.nodeSplitting.nInconsistent
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Side-Splitting Test', result.get('success', False)))
print(f"4. Side-Splitting: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 5: Net Heat Plot Data
result = driver.execute_script('''
    try {
        const consistencyResults = {
            nodeSplitting: {
                results: [
                    {comparison: 'A-B', z: 1.5, inconsistent: false},
                    {comparison: 'A-C', z: 2.1, inconsistent: true},
                    {comparison: 'B-C', z: 0.8, inconsistent: false}
                ]
            }
        };
        const r = netHeatPlotData(consistencyResults);
        return {
            success: true,
            method: r.method,
            matrixSize: r.matrix.length,
            hotspots: r.hotspots
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Net Heat Plot', result.get('success', False)))
print(f"5. Net Heat Plot: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 6: Profile Likelihood (tau2)
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = profileLikelihood(yi, vi, 'tau2');
        return {
            success: true,
            method: r.method,
            parameter: r.parameter,
            estimate: r.estimate,
            ci: r.ci,
            nPoints: r.nPoints
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Profile Likelihood (tau2)', result.get('success', False)))
print(f"6. Profile tau2: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 7: Profile Likelihood (mu)
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = profileLikelihood(yi, vi, 'mu');
        return {
            success: true,
            method: r.method,
            parameter: r.parameter,
            estimate: r.estimate,
            ci: r.ci
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Profile Likelihood (mu)', result.get('success', False)))
print(f"7. Profile mu: {'PASS' if result.get('success') else 'FAIL'} - {result}")

# Test 8: Likelihood Ratio Test
result = driver.execute_script('''
    try {
        const yi = AppState.studies.map(s => s.yi);
        const vi = AppState.studies.map(s => s.vi);
        const r = likelihoodRatioTest(yi, vi);
        return {
            success: true,
            method: r.method,
            LR: r.LR_statistic,
            pValue: r.pValue,
            significant: r.significant
        };
    } catch(e) { return {success: false, error: e.message}; }
''')
tests.append(('Likelihood Ratio Test', result.get('success', False)))
print(f"8. LR Test: {'PASS' if result.get('success') else 'FAIL'} - {result}")

driver.quit()

# Summary
print('\n' + '='*60)
print('GAP CLOSURE SUMMARY')
print('='*60)
passed = sum(1 for _, s in tests if s)
total = len(tests)
print(f'Passed: {passed}/{total} ({100*passed/total:.1f}%)')
print('='*60)

for name, status in tests:
    print(f"  [{'PASS' if status else 'FAIL'}] {name}")
