#!/usr/bin/env python3
"""Test all 17 demo datasets in TruthCert-PairwisePro"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

print("=" * 70)
print("COMPREHENSIVE DEMO DATASET TESTING")
print("TruthCert-PairwisePro v1.0")
print("=" * 70)

# Setup Chrome
driver_path = r'C:\Users\user\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32\chromedriver.exe'
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Load app
    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
    time.sleep(3)

    # Check for JS errors
    logs = driver.get_log('browser')
    severe = [l for l in logs if l['level'] == 'SEVERE']
    if severe:
        print(f"\nWARNING: {len(severe)} severe JS errors on load")
        for err in severe[:3]:
            print(f"  {err['message'][:100]}")
    else:
        print("\n[OK] No JavaScript errors on page load")

    # Get all demo datasets
    datasets = driver.execute_script('''
        if (typeof DEMO_DATASETS !== 'undefined') {
            return Object.keys(DEMO_DATASETS).map(key => ({
                key: key,
                name: DEMO_DATASETS[key].name || key,
                studies: DEMO_DATASETS[key].studies ? DEMO_DATASETS[key].studies.length : 0,
                type: DEMO_DATASETS[key].type || 'unknown'
            }));
        }
        return [];
    ''')

    print(f"\nFound {len(datasets)} demo datasets:")
    for i, ds in enumerate(datasets, 1):
        print(f"  {i:2}. {ds['key']}: {ds['name']} ({ds['studies']} studies, {ds['type']})")

    # Test each dataset
    print("\n" + "=" * 70)
    print("TESTING EACH DATASET")
    print("=" * 70)

    results = []

    for ds in datasets:
        key = ds['key']
        print(f"\n[{key}]")

        result = {
            'key': key,
            'name': ds['name'],
            'loaded': False,
            'studies': 0,
            'analysis_ran': False,
            'pooled': None,
            'tau2': None,
            'i2': None,
            'forest_rendered': False,
            'funnel_rendered': False,
            'error': None
        }

        try:
            # Load the dataset
            load_result = driver.execute_script(f'''
                try {{
                    if (typeof loadDemoDataset === 'function') {{
                        loadDemoDataset('{key}');
                        return {{ success: true }};
                    }} else if (typeof DEMO_DATASETS !== 'undefined' && DEMO_DATASETS['{key}']) {{
                        // Manual load
                        const ds = DEMO_DATASETS['{key}'];
                        if (ds.studies && Array.isArray(ds.studies)) {{
                            window.currentStudies = ds.studies;
                            return {{ success: true, studies: ds.studies.length }};
                        }}
                    }}
                    return {{ success: false, error: 'No load function' }};
                }} catch (e) {{
                    return {{ success: false, error: e.message }};
                }}
            ''')

            if load_result and load_result.get('success'):
                result['loaded'] = True
                time.sleep(0.5)

                # Get study count
                study_count = driver.execute_script('''
                    if (window.currentStudies) return window.currentStudies.length;
                    if (typeof getStudyData === 'function') {
                        const data = getStudyData();
                        return data ? data.length : 0;
                    }
                    return 0;
                ''')
                result['studies'] = study_count or ds['studies']
                print(f"  Loaded: {result['studies']} studies")

                # Run analysis
                analysis = driver.execute_script('''
                    try {
                        if (typeof runAnalysis === 'function') {
                            const res = runAnalysis();
                            if (res) {
                                return {
                                    success: true,
                                    pooled: res.pooled,
                                    tau2: res.tau2,
                                    i2: res.I2 || res.i2,
                                    se: res.se
                                };
                            }
                        }
                        // Try calculatePooledEstimate
                        if (typeof calculatePooledEstimate === 'function' && window.currentStudies) {
                            const yi = window.currentStudies.map(s => s.yi || s.effect || 0);
                            const vi = window.currentStudies.map(s => s.vi || s.variance || 0.01);
                            const res = calculatePooledEstimate(yi, vi, 'REML');
                            if (res) {
                                return {
                                    success: true,
                                    pooled: res.pooled,
                                    tau2: res.tau2,
                                    i2: res.I2
                                };
                            }
                        }
                        return { success: false };
                    } catch (e) {
                        return { success: false, error: e.message };
                    }
                ''')

                if analysis and analysis.get('success'):
                    result['analysis_ran'] = True
                    result['pooled'] = analysis.get('pooled')
                    result['tau2'] = analysis.get('tau2')
                    result['i2'] = analysis.get('i2')
                    print(f"  Analysis: pooled={result['pooled']:.4f}, tau2={result['tau2']:.4f}" if result['pooled'] else "  Analysis: ran")
                else:
                    print(f"  Analysis: Could not run - {analysis.get('error', 'unknown')}")

                # Check forest plot
                forest = driver.execute_script('''
                    try {
                        const plot = document.getElementById('forestPlot');
                        if (plot && plot.data && plot.data.length > 0) {
                            return { rendered: true, traces: plot.data.length };
                        }
                        return { rendered: false };
                    } catch (e) {
                        return { rendered: false, error: e.message };
                    }
                ''')
                result['forest_rendered'] = forest.get('rendered', False) if forest else False

                # Check funnel plot
                funnel = driver.execute_script('''
                    try {
                        const plot = document.getElementById('funnelPlot');
                        if (plot && plot.data && plot.data.length > 0) {
                            return { rendered: true, traces: plot.data.length };
                        }
                        return { rendered: false };
                    } catch (e) {
                        return { rendered: false, error: e.message };
                    }
                ''')
                result['funnel_rendered'] = funnel.get('rendered', False) if funnel else False

            else:
                result['error'] = load_result.get('error', 'Failed to load') if load_result else 'Load failed'
                print(f"  ERROR: {result['error']}")

        except Exception as e:
            result['error'] = str(e)
            print(f"  ERROR: {e}")

        results.append(result)

    # Summary
    print("\n" + "=" * 70)
    print("DATASET TESTING SUMMARY")
    print("=" * 70)

    loaded = sum(1 for r in results if r['loaded'])
    analyzed = sum(1 for r in results if r['analysis_ran'])

    print(f"\nDatasets loaded:  {loaded}/{len(results)}")
    print(f"Analyses ran:     {analyzed}/{len(results)}")

    print("\nPer-dataset results:")
    for r in results:
        status = "OK" if r['loaded'] and r['analysis_ran'] else ("PARTIAL" if r['loaded'] else "FAIL")
        pooled_str = f"pooled={r['pooled']:.3f}" if r['pooled'] else "no pooled"
        print(f"  [{status:7}] {r['key']}: {r['studies']} studies, {pooled_str}")

    # Now test all buttons and functions
    print("\n" + "=" * 70)
    print("TESTING BUTTONS AND FUNCTIONS")
    print("=" * 70)

    # First load BCG dataset for testing
    driver.execute_script("if (typeof loadDemoDataset === 'function') loadDemoDataset('BCG');")
    time.sleep(0.5)

    # Test core functions
    functions_to_test = [
        ('pnorm', 'Math.abs(pnorm(1.96) - 0.975) < 0.01'),
        ('qnorm', 'Math.abs(qnorm(0.975) - 1.96) < 0.01'),
        ('pt', 'Math.abs(pt(2, 10) - 0.9633) < 0.01'),
        ('qt', 'Math.abs(qt(0.975, 10) - 2.228) < 0.01'),
        ('lgamma', 'Math.abs(lgamma(5) - 3.178) < 0.01'),
        ('estimateTau2_DL', 'typeof estimateTau2_DL === "function"'),
        ('estimateTau2_REML', 'typeof estimateTau2_REML === "function"'),
        ('estimateTau2_ML', 'typeof estimateTau2_ML === "function"'),
        ('estimateTau2_PM', 'typeof estimateTau2_PM === "function"'),
        ('estimateTau2_HS', 'typeof estimateTau2_HS === "function"'),
        ('estimateTau2_SJ', 'typeof estimateTau2_SJ === "function"'),
        ('estimateTau2_HE', 'typeof estimateTau2_HE === "function"'),
        ('estimateTau2_EB', 'typeof estimateTau2_EB === "function"'),
        ('calculateHKSJ', 'typeof calculateHKSJ === "function"'),
        ('eggerTest', 'typeof eggerTest === "function"'),
        ('trimAndFill', 'typeof trimAndFill === "function"'),
        ('bayesianMetaAnalysis', 'typeof bayesianMetaAnalysis === "function"'),
        ('renderForestPlot', 'typeof renderForestPlot === "function"'),
        ('renderFunnelPlot', 'typeof renderFunnelPlot === "function"'),
        ('exportCSV', 'typeof exportCSV === "function"'),
        ('exportJSON', 'typeof exportJSON === "function"'),
        ('generateRCode', 'typeof generateRCode === "function"'),
        ('runAutomatedTests', 'typeof runAutomatedTests === "function"'),
    ]

    print("\nCore functions:")
    func_pass = 0
    for name, test in functions_to_test:
        try:
            result = driver.execute_script(f'return {test};')
            status = "PASS" if result else "FAIL"
            if result:
                func_pass += 1
            print(f"  [{status}] {name}")
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")

    print(f"\nFunctions: {func_pass}/{len(functions_to_test)} passed")

    # Test tau2 estimators with BCG data
    print("\n" + "=" * 70)
    print("TAU-SQUARED ESTIMATOR VALIDATION")
    print("=" * 70)

    tau2_validation = driver.execute_script('''
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];

        const ref = {
            DL: 0.308760,
            REML: 0.313243,
            ML: 0.280028,
            PM: 0.318094,
            HS: 0.228363,
            SJ: 0.345516,
            HE: 0.328564,
            EB: 0.318069
        };

        const results = {};
        const methods = ['DL', 'REML', 'ML', 'PM', 'HS', 'SJ', 'HE', 'EB'];

        for (const m of methods) {
            const fn = window['estimateTau2_' + m];
            if (fn) {
                try {
                    const res = fn(yi, vi);
                    const tau2 = res.tau2;
                    const diff = Math.abs(tau2 - ref[m]);
                    results[m] = {
                        js: tau2,
                        r: ref[m],
                        diff: diff,
                        pass: diff < 0.01
                    };
                } catch (e) {
                    results[m] = { error: e.message };
                }
            } else {
                results[m] = { error: 'Function not found' };
            }
        }
        return results;
    ''')

    print("\nMethod      JS Value    R Value     Diff      Status")
    print("-" * 55)
    tau2_pass = 0
    for method in ['DL', 'REML', 'ML', 'PM', 'HS', 'SJ', 'HE', 'EB']:
        res = tau2_validation.get(method, {})
        if 'error' in res:
            print(f"{method:8}    ERROR: {res['error']}")
        else:
            js_val = res.get('js', 0)
            r_val = res.get('r', 0)
            diff = res.get('diff', 0)
            status = "PASS" if res.get('pass') else "FAIL"
            if res.get('pass'):
                tau2_pass += 1
            print(f"{method:8}    {js_val:.6f}    {r_val:.6f}    {diff:.6f}  {status}")

    print(f"\nTau2 estimators: {tau2_pass}/8 passed")

    # Test built-in test suite
    print("\n" + "=" * 70)
    print("BUILT-IN TEST SUITE")
    print("=" * 70)

    test_suite = driver.execute_script('''
        if (typeof runAutomatedTests === 'function') {
            return runAutomatedTests();
        }
        return null;
    ''')

    if test_suite:
        print(f"\nTests: {test_suite.get('passed', 0)}/{test_suite.get('passed', 0) + test_suite.get('failed', 0)} passed")
        if test_suite.get('results'):
            for test in test_suite['results']:
                status = "PASS" if test.get('passed') else "FAIL"
                print(f"  [{status}] {test.get('name', 'Unknown test')}")
    else:
        print("\nTest suite not available")

    # Test plot rendering
    print("\n" + "=" * 70)
    print("PLOT RENDERING TEST")
    print("=" * 70)

    # Render forest plot
    forest_test = driver.execute_script('''
        try {
            if (typeof renderForestPlot === 'function') {
                const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
                const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
                const names = ['Study 1', 'Study 2', 'Study 3', 'Study 4', 'Study 5'];
                renderForestPlot(yi, vi, names);

                // Wait a bit and check
                const plot = document.getElementById('forestPlot');
                if (plot && plot.data) {
                    return { success: true, traces: plot.data.length };
                }
            }
            return { success: false };
        } catch (e) {
            return { success: false, error: e.message };
        }
    ''')

    print(f"\nForest Plot: {'OK' if forest_test and forest_test.get('success') else 'FAIL'}")

    # Render funnel plot
    funnel_test = driver.execute_script('''
        try {
            if (typeof renderFunnelPlot === 'function') {
                const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
                const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
                renderFunnelPlot(yi, vi);

                const plot = document.getElementById('funnelPlot');
                if (plot && plot.data) {
                    return { success: true, traces: plot.data.length };
                }
            }
            return { success: false };
        } catch (e) {
            return { success: false, error: e.message };
        }
    ''')

    print(f"Funnel Plot: {'OK' if funnel_test and funnel_test.get('success') else 'FAIL'}")

    # Check other plot functions
    other_plots = [
        ('Baujat Plot', 'typeof renderBaujatPlot === "function"'),
        ('Radial Plot', 'typeof renderRadialPlot === "function"'),
        ('L\'Abbe Plot', 'typeof renderLabbePlot === "function"'),
        ('DOI Plot', 'typeof renderDOIPlot === "function"'),
        ('P-curve Plot', 'typeof renderPCurvePlot === "function"'),
        ('Z-curve Plot', 'typeof renderZCurvePlot === "function"'),
        ('GOSH Plot', 'typeof renderGOSHPlot === "function"'),
        ('Cumulative Plot', 'typeof renderCumulativePlot === "function"'),
        ('Leave-One-Out Plot', 'typeof renderLeaveOneOutPlot === "function"'),
    ]

    print("\nOther plot functions:")
    for name, test in other_plots:
        try:
            result = driver.execute_script(f'return {test};')
            print(f"  [{('OK' if result else 'N/A'):3}] {name}")
        except:
            print(f"  [N/A] {name}")

    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    total_tests = len(results) + len(functions_to_test) + 8 + 2  # datasets + functions + tau2 + plots
    passed_tests = loaded + func_pass + tau2_pass + (1 if forest_test and forest_test.get('success') else 0) + (1 if funnel_test and funnel_test.get('success') else 0)

    print(f"\nDemo datasets:       {loaded}/{len(results)} loaded successfully")
    print(f"Core functions:      {func_pass}/{len(functions_to_test)} available")
    print(f"Tau2 estimators:     {tau2_pass}/8 validated")
    print(f"Forest plot:         {'OK' if forest_test and forest_test.get('success') else 'FAIL'}")
    print(f"Funnel plot:         {'OK' if funnel_test and funnel_test.get('success') else 'FAIL'}")

    pct = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed ({pct:.1f}%)")

    if pct >= 90:
        print("\nVERDICT: EXCELLENT - Application fully functional")
    elif pct >= 75:
        print("\nVERDICT: GOOD - Most features working")
    elif pct >= 50:
        print("\nVERDICT: ACCEPTABLE - Core features working")
    else:
        print("\nVERDICT: NEEDS ATTENTION - Issues detected")

    print("=" * 70)

finally:
    driver.quit()
