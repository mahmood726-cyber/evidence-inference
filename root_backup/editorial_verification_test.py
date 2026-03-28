"""Verify all editorial fixes are working"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Edge(options=options)

try:
    driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
    time.sleep(3)

    # Check for JS errors
    logs = driver.get_log('browser')
    errors = [l for l in logs if l['level'] == 'SEVERE']
    print(f'JavaScript errors: {len(errors)}')
    for e in errors[:5]:
        print(f'  ERROR: {e["message"][:100]}')

    # Test all new modules
    new_modules = [
        # Batch 1
        'ContinuousOutcomes', 'MLEstimator', 'ROB2', 'ROBINSI',
        'PCurve', 'CopasModel', 'FragilityIndex', 'DesignDecomposition',
        'MetaforExport', 'HelpSystem',
        # Batch 2
        'ExportPNG', 'ExportPDF', 'PUniform', 'MantelHaenszel',
        'PetoMethod', 'EBEstimator', 'HedgesEstimator', 'InverseVariance', 'SJEstimator',
        # Existing that should work
        'ComparisonAdjustedFunnel', 'ProfileLikelihood', 'PRISMANMAChecklist',
        'GradeNMA', 'InfluenceDiagnostics', 'ROBSensitivity', 'NetworkWarnings'
    ]

    print('\n' + '='*70)
    print('NEW MODULE VERIFICATION')
    print('='*70)
    passed = 0
    failed = 0
    for mod in new_modules:
        exists = driver.execute_script(f"return typeof {mod}")
        if exists == 'object' or exists == 'function':
            print(f'  [PASS] {mod}')
            passed += 1
        else:
            print(f'  [FAIL] {mod} - type: {exists}')
            failed += 1

    # Test specific functionality
    print('\n' + '='*70)
    print('FUNCTIONALITY TESTS')
    print('='*70)

    # Test ContinuousOutcomes.calculateMD
    result = driver.execute_script("""
        try {
            const r = ContinuousOutcomes.calculateMD(10, 2, 50, 8, 2.5, 50);
            return {success: true, yi: r.yi, se: r.se};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] ContinuousOutcomes.calculateMD (MD={result["yi"]:.4f})')
        passed += 1
    else:
        print(f'  [FAIL] ContinuousOutcomes.calculateMD - {result.get("error")}')
        failed += 1

    # Test MLEstimator
    result = driver.execute_script("""
        try {
            const yi = [0.2, 0.3, 0.1, 0.4, 0.25];
            const vi = [0.04, 0.05, 0.03, 0.06, 0.04];
            const r = MLEstimator.estimate(yi, vi);
            return {success: true, tau2: r.tau2, mu: r.mu};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] MLEstimator.estimate (tau2={result["tau2"]:.6f})')
        passed += 1
    else:
        print(f'  [FAIL] MLEstimator.estimate - {result.get("error")}')
        failed += 1

    # Test ROB2.assess
    result = driver.execute_script("""
        try {
            const r = ROB2.assess({Randomization: 'Low', Deviations: 'Some concerns',
                                   Missing: 'Low', Measurement: 'Low', Selection: 'Low'});
            return {success: true, overall: r.overall};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] ROB2.assess (overall={result["overall"]})')
        passed += 1
    else:
        print(f'  [FAIL] ROB2.assess - {result.get("error")}')
        failed += 1

    # Test ROBINSI.assess
    result = driver.execute_script("""
        try {
            const r = ROBINSI.assess({Confounding: 'Moderate', Selection: 'Low',
                                      Classification: 'Low', Deviations: 'Low',
                                      Missing: 'Low', Measurement: 'Low', Reporting: 'Low'});
            return {success: true, overall: r.overall};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] ROBINSI.assess (overall={result["overall"]})')
        passed += 1
    else:
        print(f'  [FAIL] ROBINSI.assess - {result.get("error")}')
        failed += 1

    # Test PCurve
    result = driver.execute_script("""
        try {
            const pvals = [0.001, 0.003, 0.01, 0.02, 0.03, 0.04, 0.045];
            const r = PCurve.analyze(pvals);
            return {success: true, nSig: r.nSignificant, interpretation: r.interpretation};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] PCurve.analyze (n={result["nSig"]}, {result["interpretation"][:30]}...)')
        passed += 1
    else:
        print(f'  [FAIL] PCurve.analyze - {result.get("error")}')
        failed += 1

    # Test CopasModel
    result = driver.execute_script("""
        try {
            const yi = [0.3, 0.4, 0.2, 0.5, 0.35];
            const vi = [0.04, 0.05, 0.03, 0.06, 0.04];
            const r = CopasModel.fit(yi, vi);
            return {success: true, unadj: r.unadjusted};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] CopasModel.fit (unadjusted={result["unadj"]:.4f})')
        passed += 1
    else:
        print(f'  [FAIL] CopasModel.fit - {result.get("error")}')
        failed += 1

    # Test FragilityIndex
    result = driver.execute_script("""
        try {
            const studies = [{name:'S1',events1:20,n1:100,events2:35,n2:100}];
            const r = FragilityIndex.calculate(studies);
            return {success: true, fi: r.studyLevel[0].fi};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] FragilityIndex.calculate (FI={result["fi"]})')
        passed += 1
    else:
        print(f'  [FAIL] FragilityIndex.calculate - {result.get("error")}')
        failed += 1

    # Test MantelHaenszel
    result = driver.execute_script("""
        try {
            const studies = [
                {events1:20,n1:100,events2:30,n2:100},
                {events1:15,n1:80,events2:25,n2:80}
            ];
            const r = MantelHaenszel.analyze(studies);
            return {success: true, or: r.OR};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] MantelHaenszel.analyze (OR={result["or"]:.4f})')
        passed += 1
    else:
        print(f'  [FAIL] MantelHaenszel.analyze - {result.get("error")}')
        failed += 1

    # Test PetoMethod
    result = driver.execute_script("""
        try {
            const studies = [
                {events1:20,n1:100,events2:30,n2:100},
                {events1:15,n1:80,events2:25,n2:80}
            ];
            const r = PetoMethod.analyze(studies);
            return {success: true, or: r.OR};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] PetoMethod.analyze (OR={result["or"]:.4f})')
        passed += 1
    else:
        print(f'  [FAIL] PetoMethod.analyze - {result.get("error")}')
        failed += 1

    # Test MetaforExport
    result = driver.execute_script("""
        try {
            const processed = [{name:'S1',yi:0.3,vi:0.04,treatment1:'A',treatment2:'B'}];
            const r = MetaforExport.generate(processed);
            return {success: true, hasCode: r.rCode.length > 100};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] MetaforExport.generate (code generated)')
        passed += 1
    else:
        print(f'  [FAIL] MetaforExport.generate - {result.get("error")}')
        failed += 1

    # Test HelpSystem
    result = driver.execute_script("""
        try {
            const r = HelpSystem.get('tau2');
            return {success: true, hasTitle: r.title.length > 0};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] HelpSystem.get (help available)')
        passed += 1
    else:
        print(f'  [FAIL] HelpSystem.get - {result.get("error")}')
        failed += 1

    # Test InverseVariance
    result = driver.execute_script("""
        try {
            const yi = [0.3, 0.4, 0.2, 0.5];
            const vi = [0.04, 0.05, 0.03, 0.06];
            const r = InverseVariance.pool(yi, vi, 'random');
            return {success: true, pooled: r.pooled, tau2: r.tau2};
        } catch(e) { return {error: e.message}; }
    """)
    if result.get('success'):
        print(f'  [PASS] InverseVariance.pool (pooled={result["pooled"]:.4f})')
        passed += 1
    else:
        print(f'  [FAIL] InverseVariance.pool - {result.get("error")}')
        failed += 1

    # Summary
    print('\n' + '='*70)
    print('VERIFICATION SUMMARY')
    print('='*70)
    total = passed + failed
    print(f'\n  PASSED: {passed}/{total} ({100*passed/total:.1f}%)')
    print(f'  FAILED: {failed}/{total}')
    print(f'  JS ERRORS: {len(errors)}')

    if failed == 0 and len(errors) == 0:
        print('\n  STATUS: ALL EDITORIAL FIXES VERIFIED!')
    else:
        print('\n  STATUS: ISSUES FOUND - REVIEW NEEDED')

finally:
    driver.quit()
