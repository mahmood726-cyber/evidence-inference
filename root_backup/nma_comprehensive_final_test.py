"""Comprehensive NMA Pro v6.2 Test Suite - Final Editorial Verification"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Edge(options=options)

passed = 0
failed = 0
results = []

def test(name, condition, detail=''):
    global passed, failed, results
    if condition:
        passed += 1
        results.append(f'  [PASS] {name}')
    else:
        failed += 1
        results.append(f'  [FAIL] {name} - {detail}')

try:
    driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
    time.sleep(3)

    # Check JS errors
    logs = driver.get_log('browser')
    js_errors = [l for l in logs if l['level'] == 'SEVERE']
    test('No JavaScript errors on load', len(js_errors) == 0, f'{len(js_errors)} errors')

    print('=' * 70)
    print('NMA PRO v6.2 - COMPREHENSIVE TEST SUITE')
    print('=' * 70)

    # ========================================================================
    # CORE STATISTICAL MODULES
    # ========================================================================
    print('\n[1/8] CORE STATISTICAL MODULES')
    print('-' * 40)

    core_modules = [
        'FrequentistNMA', 'BayesianNMA', 'NetworkMetaRegression', 'ComponentNMA',
        'NodeSplitting', 'Stats', 'Matrix', 'NMAHelpers'
    ]
    for mod in core_modules:
        exists = driver.execute_script(f"return typeof {mod}")
        test(f'{mod}', exists in ['object', 'function'], f'type={exists}')

    # ========================================================================
    # PUBLICATION BIAS MODULES
    # ========================================================================
    print('\n[2/8] PUBLICATION BIAS MODULES')
    print('-' * 40)

    pub_bias = [
        'TrimAndFill', 'EggersTest', 'BeggsTest', 'PETPEESE',
        'SelectionModels', 'PCurve', 'PUniform', 'CopasModel'
    ]
    for mod in pub_bias:
        exists = driver.execute_script(f"return typeof {mod}")
        test(f'{mod}', exists in ['object', 'function'], f'type={exists}')

    # ========================================================================
    # HETEROGENEITY ESTIMATORS
    # ========================================================================
    print('\n[3/8] HETEROGENEITY ESTIMATORS')
    print('-' * 40)

    estimators = [
        'MLEstimator', 'EBEstimator', 'HedgesEstimator', 'SJEstimator',
        'InverseVariance', 'ProfileLikelihood'
    ]
    for mod in estimators:
        exists = driver.execute_script(f"return typeof {mod}")
        test(f'{mod}', exists in ['object', 'function'], f'type={exists}')

    # ========================================================================
    # RISK OF BIAS & REPORTING
    # ========================================================================
    print('\n[4/8] RISK OF BIAS & REPORTING')
    print('-' * 40)

    rob_modules = [
        'ROB2', 'ROBINSI', 'PRISMANMAChecklist', 'GradeNMA',
        'ROBSensitivity', 'NetworkWarnings', 'InfluenceDiagnostics'
    ]
    for mod in rob_modules:
        exists = driver.execute_script(f"return typeof {mod}")
        test(f'{mod}', exists in ['object', 'function'], f'type={exists}')

    # ========================================================================
    # EXPORT & VISUALIZATION
    # ========================================================================
    print('\n[5/8] EXPORT & VISUALIZATION')
    print('-' * 40)

    export_modules = [
        'ExportPNG', 'ExportPDF', 'MetaforExport', 'ComparisonAdjustedFunnel',
        'HelpSystem', 'MethodologyTooltips', 'RValidationDoc'
    ]
    for mod in export_modules:
        exists = driver.execute_script(f"return typeof {mod}")
        test(f'{mod}', exists in ['object', 'function'], f'type={exists}')

    # ========================================================================
    # EFFECT SIZE METHODS
    # ========================================================================
    print('\n[6/8] EFFECT SIZE METHODS')
    print('-' * 40)

    effect_modules = [
        'ContinuousOutcomes', 'MantelHaenszel', 'PetoMethod',
        'FragilityIndex', 'DesignDecomposition'
    ]
    for mod in effect_modules:
        exists = driver.execute_script(f"return typeof {mod}")
        test(f'{mod}', exists in ['object', 'function'], f'type={exists}')

    # ========================================================================
    # FUNCTIONALITY TESTS
    # ========================================================================
    print('\n[7/8] FUNCTIONALITY TESTS')
    print('-' * 40)

    # Test Stats functions
    r = driver.execute_script("try { return Stats.pnorm(1.96); } catch(e) { return null; }")
    test('Stats.pnorm', r is not None and abs(r - 0.975) < 0.01, f'got {r}')

    r = driver.execute_script("try { return Stats.qnorm(0.975); } catch(e) { return null; }")
    test('Stats.qnorm', r is not None and abs(r - 1.96) < 0.01, f'got {r}')

    r = driver.execute_script("try { return Stats.chiSquareCDF(5.99, 2); } catch(e) { return null; }")
    test('Stats.chiSquareCDF', r is not None and r > 0.94 and r < 0.96, f'got {r}')

    # Test Matrix operations
    r = driver.execute_script("""
        try {
            const A = [[1, 2], [3, 4]];
            const inv = Matrix.inverse(A);
            return inv !== null && inv.length === 2;
        } catch(e) { return false; }
    """)
    test('Matrix.inverse', r == True)

    # Test TrimAndFill
    r = driver.execute_script("""
        try {
            const yi = [0.3, 0.5, 0.2, 0.4, 0.35];
            const vi = [0.04, 0.05, 0.03, 0.06, 0.04];
            const result = TrimAndFill.analyze(yi, vi);
            return result && typeof result.adjusted !== 'undefined';
        } catch(e) { return false; }
    """)
    test('TrimAndFill.analyze', r == True)

    # Test EggersTest
    r = driver.execute_script("""
        try {
            const yi = [0.3, 0.5, 0.2, 0.4, 0.35];
            const vi = [0.04, 0.05, 0.03, 0.06, 0.04];
            const result = EggersTest.test(yi, vi);
            return result && typeof result.pValue !== 'undefined';
        } catch(e) { return false; }
    """)
    test('EggersTest.test', r == True)

    # Test ContinuousOutcomes
    r = driver.execute_script("""
        try {
            const result = ContinuousOutcomes.calculateMD(10, 2, 50, 8, 2.5, 50);
            return result && Math.abs(result.yi - 2) < 0.01;
        } catch(e) { return false; }
    """)
    test('ContinuousOutcomes.calculateMD', r == True)

    # Test ROB2
    r = driver.execute_script("""
        try {
            const result = ROB2.assess({
                Randomization: 'Low', Deviations: 'Low',
                Missing: 'Low', Measurement: 'Low', Selection: 'Low'
            });
            return result && result.overall === 'Low';
        } catch(e) { return false; }
    """)
    test('ROB2.assess (Low)', r == True)

    # Test ROBINSI
    r = driver.execute_script("""
        try {
            const result = ROBINSI.assess({
                Confounding: 'Low', Selection: 'Low',
                Classification: 'Low', Deviations: 'Low',
                Missing: 'Low', Measurement: 'Low', Reporting: 'Low'
            });
            return result && result.overall === 'Low';
        } catch(e) { return false; }
    """)
    test('ROBINSI.assess (Low)', r == True)

    # Test PCurve
    r = driver.execute_script("""
        try {
            const pvals = [0.001, 0.003, 0.01, 0.02, 0.03];
            const result = PCurve.analyze(pvals);
            return result && typeof result.nSignificant !== 'undefined';
        } catch(e) { return false; }
    """)
    test('PCurve.analyze', r == True)

    # Test FragilityIndex
    r = driver.execute_script("""
        try {
            const studies = [{name:'S1', events1:20, n1:100, events2:35, n2:100}];
            const result = FragilityIndex.calculate(studies);
            return result && result.studyLevel[0].fi >= 0;
        } catch(e) { return false; }
    """)
    test('FragilityIndex.calculate', r == True)

    # Test MantelHaenszel
    r = driver.execute_script("""
        try {
            const studies = [
                {events1:20, n1:100, events2:30, n2:100},
                {events1:15, n1:80, events2:25, n2:80}
            ];
            const result = MantelHaenszel.analyze(studies);
            return result && typeof result.OR !== 'undefined';
        } catch(e) { return false; }
    """)
    test('MantelHaenszel.analyze', r == True)

    # Test MetaforExport
    r = driver.execute_script("""
        try {
            const processed = [{name:'S1', yi:0.3, vi:0.04, treatment1:'A', treatment2:'B'}];
            const result = MetaforExport.generate(processed);
            return result && result.rCode.includes('metafor');
        } catch(e) { return false; }
    """)
    test('MetaforExport.generate', r == True)

    # Test HelpSystem
    r = driver.execute_script("""
        try {
            const result = HelpSystem.get('tau2');
            return result && result.title && result.description;
        } catch(e) { return false; }
    """)
    test('HelpSystem.get', r == True)

    # Test InverseVariance pooling
    r = driver.execute_script("""
        try {
            const yi = [0.3, 0.4, 0.2, 0.5];
            const vi = [0.04, 0.05, 0.03, 0.06];
            const result = InverseVariance.pool(yi, vi, 'random');
            return result && typeof result.pooled !== 'undefined' && typeof result.tau2 !== 'undefined';
        } catch(e) { return false; }
    """)
    test('InverseVariance.pool (random)', r == True)

    # Test ProfileLikelihood
    r = driver.execute_script("""
        try {
            const processed = [
                {yi: 0.3, vi: 0.04}, {yi: 0.4, vi: 0.05},
                {yi: 0.2, vi: 0.03}, {yi: 0.5, vi: 0.06}
            ];
            const tau2 = 0.01;
            const result = ProfileLikelihood.computeTau2CI(processed, tau2);
            return result && result.ci && result.ci.length === 2;
        } catch(e) { return false; }
    """)
    test('ProfileLikelihood.computeTau2CI', r == True)

    # ========================================================================
    # DEMO DATASETS
    # ========================================================================
    print('\n[8/8] DEMO DATASETS')
    print('-' * 40)

    r = driver.execute_script("return typeof DEMO_DATASETS")
    test('DEMO_DATASETS exists', r == 'object')

    datasets = ['thrombolytics', 'vaccines', 'antihypertensives', 'painkillers', 'cbt_depression']
    for ds in datasets:
        r = driver.execute_script(f"""
            try {{
                return DEMO_DATASETS.{ds} && DEMO_DATASETS.{ds}.length > 0;
            }} catch(e) {{ return false; }}
        """)
        test(f'DEMO_DATASETS.{ds}', r == True)

    r = driver.execute_script("return typeof loadDemoDataset")
    test('loadDemoDataset function', r == 'function')

    # ========================================================================
    # PRINT RESULTS
    # ========================================================================
    print('\n' + '=' * 70)
    print('TEST RESULTS')
    print('=' * 70)

    for r in results:
        print(r)

    print('\n' + '=' * 70)
    print('SUMMARY')
    print('=' * 70)
    total = passed + failed
    pct = 100 * passed / total if total > 0 else 0
    print(f'\n  PASSED: {passed}/{total} ({pct:.1f}%)')
    print(f'  FAILED: {failed}/{total}')
    print(f'  JS ERRORS: {len(js_errors)}')

    if failed == 0 and len(js_errors) == 0:
        print('\n  STATUS: ALL TESTS PASSED!')
    else:
        print('\n  STATUS: SOME TESTS FAILED')

finally:
    driver.quit()
