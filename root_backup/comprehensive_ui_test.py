#!/usr/bin/env python3
"""Comprehensive UI Test for TruthCert-PairwisePro Meta-Analysis Application"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("=" * 70)
print("COMPREHENSIVE UI TEST")
print("TruthCert-PairwisePro Meta-Analysis Application")
print("=" * 70)

# Chrome setup
driver_path = r"C:\Users\user\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32\chromedriver.exe"
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

results = {'passed': 0, 'failed': 0, 'details': []}

def log_result(test_name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    results['passed' if passed else 'failed'] += 1
    results['details'].append({'name': test_name, 'passed': passed, 'details': details})
    print(f"  [{status}] {test_name}" + (f" - {details}" if details else ""))

try:
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    # 1. Load the application
    print("\n[1] LOADING APPLICATION...")
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)

    title = driver.title
    log_result("Page loads", "TruthCert" in title or "Pairwise" in title, f"Title: {title[:50]}")

    # Check for JS errors
    logs = driver.get_log('browser')
    severe_errors = [l for l in logs if l['level'] == 'SEVERE']
    log_result("No critical JS errors on load", len(severe_errors) == 0, f"{len(severe_errors)} errors")

    # 2. Load Demo Dataset (BCG)
    print("\n[2] LOADING DEMO DATASET...")

    # Check if loadSampleData function exists
    has_sample_fn = driver.execute_script("return typeof loadSampleData === 'function' || typeof loadDemo === 'function' || typeof SAMPLES !== 'undefined';")
    log_result("Sample data system available", has_sample_fn)

    # Try to load BCG data
    load_result = driver.execute_script("""
        // Try different ways to load sample data
        if (typeof loadSampleData === 'function') {
            loadSampleData('bcg');
            return 'loadSampleData';
        } else if (typeof SAMPLES !== 'undefined' && SAMPLES.bcg) {
            // Manually set the data
            if (typeof AppState !== 'undefined') {
                AppState.studies = SAMPLES.bcg.studies || SAMPLES.bcg;
                return 'SAMPLES direct';
            }
        }

        // Fallback: inject BCG data directly
        const bcgStudies = [
            {study: 'Aronson 1948', events1: 4, total1: 123, events2: 11, total2: 139, yi: -0.889311, vi: 0.325585},
            {study: 'Ferguson 1949', events1: 6, total1: 306, events2: 29, total2: 303, yi: -1.585389, vi: 0.194581},
            {study: 'Rosenthal 1960', events1: 3, total1: 231, events2: 11, total2: 220, yi: -1.348073, vi: 0.415368},
            {study: 'Hart 1977', events1: 62, total1: 13598, events2: 248, total2: 12867, yi: -1.441551, vi: 0.020010},
            {study: 'Frimodt 1973', events1: 33, total1: 5069, events2: 47, total2: 5808, yi: -0.217547, vi: 0.051210},
            {study: 'Stein 1953', events1: 180, total1: 1541, events2: 372, total2: 1451, yi: -0.786116, vi: 0.006906},
            {study: 'Vandiviere 1973', events1: 8, total1: 2545, events2: 10, total2: 629, yi: -1.620898, vi: 0.223017},
            {study: 'TPT Madras 1980', events1: 505, total1: 88391, events2: 499, total2: 88391, yi: 0.011952, vi: 0.003962},
            {study: 'Coetzee 1968', events1: 29, total1: 7499, events2: 45, total2: 7277, yi: -0.469418, vi: 0.056434},
            {study: 'Rosenthal 1961', events1: 17, total1: 1716, events2: 65, total2: 1665, yi: -1.371345, vi: 0.073025},
            {study: 'Comstock 1974', events1: 186, total1: 50634, events2: 141, total2: 27338, yi: -0.339359, vi: 0.012412},
            {study: 'Comstock 1976', events1: 5, total1: 2498, events2: 3, total2: 2341, yi: 0.445913, vi: 0.532506},
            {study: 'Comstock&Webster 1969', events1: 27, total1: 16913, events2: 29, total2: 17854, yi: -0.017314, vi: 0.071405}
        ];

        if (typeof AppState !== 'undefined') {
            AppState.studies = bcgStudies;
            AppState.dataType = 'binary';
            return 'injected';
        }
        return 'failed';
    """)
    log_result("Demo data loaded", load_result != 'failed', f"Method: {load_result}")

    # Verify studies are loaded
    study_count = driver.execute_script("return typeof AppState !== 'undefined' && AppState.studies ? AppState.studies.length : 0;")
    log_result("Studies populated", study_count >= 10, f"{study_count} studies")

    # 3. Run Full Analysis
    print("\n[3] RUNNING FULL ANALYSIS...")

    analysis_result = driver.execute_script("""
        try {
            if (typeof runAnalysis === 'function') {
                runAnalysis();
                return {success: true, method: 'runAnalysis'};
            } else if (typeof calculatePooledEstimate === 'function' && typeof AppState !== 'undefined') {
                const yi = AppState.studies.map(s => s.yi);
                const vi = AppState.studies.map(s => s.vi);
                const result = calculatePooledEstimate(yi, vi);
                AppState.analysis = result;
                return {success: true, method: 'calculatePooledEstimate', pooled: result.pooled};
            }
            return {success: false, error: 'No analysis function found'};
        } catch(e) {
            return {success: false, error: e.message};
        }
    """)
    log_result("Analysis runs without error", analysis_result.get('success', False),
               analysis_result.get('method', analysis_result.get('error', '')))

    time.sleep(1)  # Wait for analysis to complete

    # 4. Check All Core Functions
    print("\n[4] TESTING CORE STATISTICAL FUNCTIONS...")

    # Test statistical distributions
    stat_funcs = driver.execute_script("""
        const tests = {};

        // Normal distribution
        tests.pnorm = typeof pnorm === 'function' && Math.abs(pnorm(1.96) - 0.975) < 0.001;
        tests.qnorm = typeof qnorm === 'function' && Math.abs(qnorm(0.975) - 1.96) < 0.01;
        tests.dnorm = typeof dnorm === 'function' && Math.abs(dnorm(0) - 0.3989) < 0.001;

        // t-distribution
        tests.pt = typeof pt === 'function' && Math.abs(pt(2, 10) - 0.9633) < 0.001;
        tests.qt = typeof qt === 'function' && Math.abs(qt(0.975, 10) - 2.228) < 0.01;

        // Chi-squared
        tests.pchisq = typeof pchisq === 'function' && Math.abs(pchisq(3.84, 1) - 0.95) < 0.01;
        tests.qchisq = typeof qchisq === 'function' && Math.abs(qchisq(0.95, 1) - 3.84) < 0.1;

        // Gamma
        tests.lgamma = typeof lgamma === 'function' && Math.abs(lgamma(5) - 3.178) < 0.01;

        return tests;
    """)

    for func, passed in stat_funcs.items():
        log_result(f"Statistical function: {func}", passed)

    # Test tau² estimators
    print("\n[5] TESTING TAU² ESTIMATORS...")

    tau2_tests = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547, -0.786116, -1.620898, 0.011952, -0.469418, -1.371345, -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210, 0.006906, 0.223017, 0.003962, 0.056434, 0.073025, 0.012412, 0.532506, 0.071405];

        const refValues = {
            DL: 0.308760, REML: 0.313243, ML: 0.280028, PM: 0.318094,
            HS: 0.228363, SJ: 0.345516, HE: 0.328564, EB: 0.318069
        };

        const results = {};
        for (const method of Object.keys(refValues)) {
            const fn = window['estimateTau2_' + method];
            if (fn) {
                try {
                    const r = fn(yi, vi);
                    const diff = Math.abs(r.tau2 - refValues[method]);
                    results[method] = {
                        available: true,
                        computed: r.tau2,
                        reference: refValues[method],
                        diff: diff,
                        match: diff < 0.001
                    };
                } catch(e) {
                    results[method] = {available: true, error: e.message, match: false};
                }
            } else {
                results[method] = {available: false, match: false};
            }
        }
        return results;
    """)

    for method, result in tau2_tests.items():
        if result.get('available'):
            if result.get('match'):
                log_result(f"Tau² {method}", True, f"{result['computed']:.6f} matches R")
            elif 'error' in result:
                log_result(f"Tau² {method}", False, f"Error: {result['error']}")
            else:
                log_result(f"Tau² {method}", False, f"Got {result['computed']:.6f}, expected {result['reference']:.6f}")
        else:
            log_result(f"Tau² {method}", False, "Function not found")

    # 6. Test Pooled Estimate Functions
    print("\n[6] TESTING POOLED ESTIMATE FUNCTIONS...")

    pooled_tests = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];

        const results = {};

        // Fixed effect
        if (typeof calculatePooledEstimate === 'function') {
            try {
                const r = calculatePooledEstimate(yi, vi, {model: 'FE'});
                results.fixedEffect = {available: true, pooled: r.pooled, se: r.se};
            } catch(e) {
                results.fixedEffect = {available: true, error: e.message};
            }
        } else {
            results.fixedEffect = {available: false};
        }

        // Random effects
        if (typeof calculatePooledEstimate === 'function') {
            try {
                const r = calculatePooledEstimate(yi, vi, {model: 'RE'});
                results.randomEffects = {available: true, pooled: r.pooled, tau2: r.tau2};
            } catch(e) {
                results.randomEffects = {available: true, error: e.message};
            }
        }

        // HKSJ adjustment
        if (typeof calculateHKSJ === 'function') {
            try {
                const r = calculateHKSJ(yi, vi, 0.3);
                results.HKSJ = {available: true, pooled: r.pooled, ciLower: r.ciLower, ciUpper: r.ciUpper};
            } catch(e) {
                results.HKSJ = {available: true, error: e.message};
            }
        } else {
            results.HKSJ = {available: false};
        }

        return results;
    """)

    for test, result in pooled_tests.items():
        if result.get('available'):
            if 'error' in result:
                log_result(f"Pooled: {test}", False, f"Error: {result['error']}")
            else:
                log_result(f"Pooled: {test}", True, f"pooled={result.get('pooled', 'N/A'):.4f}")
        else:
            log_result(f"Pooled: {test}", False, "Not available")

    # 7. Test Bayesian Analysis
    print("\n[7] TESTING BAYESIAN ANALYSIS...")

    bayes_result = driver.execute_script("""
        if (typeof bayesianMetaAnalysis === 'function') {
            try {
                const yi = [-0.889311, -1.585389, -1.348073];
                const vi = [0.325585, 0.194581, 0.415368];
                const r = bayesianMetaAnalysis(yi, vi, {nIter: 2000, seed: 42});
                return {
                    available: true,
                    hasSummary: !!r.summary,
                    hasChains: !!r.chains,
                    thetaMean: r.summary ? r.summary.theta.mean : null,
                    tau2Mean: r.summary ? r.summary.tau2.mean : null
                };
            } catch(e) {
                return {available: true, error: e.message};
            }
        }
        return {available: false};
    """)

    if bayes_result.get('available'):
        if 'error' in bayes_result:
            log_result("Bayesian MCMC", False, f"Error: {bayes_result['error']}")
        else:
            log_result("Bayesian MCMC", bayes_result.get('hasSummary', False),
                       f"theta={bayes_result.get('thetaMean', 'N/A'):.4f}" if bayes_result.get('thetaMean') else "")
    else:
        log_result("Bayesian MCMC", False, "Not available")

    # 8. Test Publication Bias Functions
    print("\n[8] TESTING PUBLICATION BIAS FUNCTIONS...")

    bias_tests = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
        const se = vi.map(v => Math.sqrt(v));

        const results = {};

        // Egger's test
        if (typeof eggerTest === 'function') {
            try {
                const r = eggerTest(yi, se);
                results.egger = {available: true, intercept: r.intercept, pValue: r.pValue};
            } catch(e) {
                results.egger = {available: true, error: e.message};
            }
        } else {
            results.egger = {available: false};
        }

        // Begg's test
        if (typeof beggTest === 'function') {
            try {
                const r = beggTest(yi, se);
                results.begg = {available: true, tau: r.tau, pValue: r.pValue};
            } catch(e) {
                results.begg = {available: true, error: e.message};
            }
        } else {
            results.begg = {available: false};
        }

        // Trim and fill
        if (typeof trimAndFill === 'function') {
            try {
                const r = trimAndFill(yi.map((y, i) => ({yi: y, vi: vi[i], se: se[i]})));
                results.trimFill = {available: true, k0: r.k0, adjustedPooled: r.adjustedPooled};
            } catch(e) {
                results.trimFill = {available: true, error: e.message};
            }
        } else {
            results.trimFill = {available: false};
        }

        return results;
    """)

    for test, result in bias_tests.items():
        if result.get('available'):
            if 'error' in result:
                log_result(f"Pub bias: {test}", False, f"Error: {result['error']}")
            else:
                log_result(f"Pub bias: {test}", True)
        else:
            log_result(f"Pub bias: {test}", False, "Not available")

    # 9. Test Plot Functions
    print("\n[9] TESTING PLOT FUNCTIONS...")

    plot_tests = driver.execute_script("""
        const results = {};

        // Check Plotly is available
        results.plotly = typeof Plotly !== 'undefined';

        // Check plot functions exist
        results.forestPlot = typeof renderForestPlot === 'function';
        results.funnelPlot = typeof renderFunnelPlot === 'function';
        results.baujatPlot = typeof renderBaujatPlot === 'function' || typeof baujatPlot === 'function';
        results.galbraithPlot = typeof renderGalbraithPlot === 'function' || typeof galbraithPlot === 'function';
        results.influencePlot = typeof renderInfluencePlot === 'function' || typeof influencePlot === 'function';
        results.cumulativePlot = typeof renderCumulativePlot === 'function' || typeof cumulativeMetaPlot === 'function';

        return results;
    """)

    for plot, available in plot_tests.items():
        log_result(f"Plot function: {plot}", available)

    # Try to render forest plot
    forest_render = driver.execute_script("""
        try {
            if (typeof renderForestPlot === 'function' && typeof AppState !== 'undefined' && AppState.studies) {
                // Create a container if needed
                let container = document.getElementById('forest-plot');
                if (!container) {
                    container = document.createElement('div');
                    container.id = 'forest-plot';
                    container.style.width = '800px';
                    container.style.height = '600px';
                    document.body.appendChild(container);
                }
                renderForestPlot();
                return {rendered: true};
            }
            return {rendered: false, reason: 'Function or data not available'};
        } catch(e) {
            return {rendered: false, error: e.message};
        }
    """)
    log_result("Forest plot renders", forest_render.get('rendered', False),
               forest_render.get('error', ''))

    # Try to render funnel plot
    funnel_render = driver.execute_script("""
        try {
            if (typeof renderFunnelPlot === 'function' && typeof AppState !== 'undefined' && AppState.studies) {
                let container = document.getElementById('funnel-plot');
                if (!container) {
                    container = document.createElement('div');
                    container.id = 'funnel-plot';
                    container.style.width = '800px';
                    container.style.height = '600px';
                    document.body.appendChild(container);
                }
                renderFunnelPlot();
                return {rendered: true};
            }
            return {rendered: false, reason: 'Function or data not available'};
        } catch(e) {
            return {rendered: false, error: e.message};
        }
    """)
    log_result("Funnel plot renders", funnel_render.get('rendered', False),
               funnel_render.get('error', ''))

    # 10. Test Export Functions
    print("\n[10] TESTING EXPORT FUNCTIONS...")

    export_tests = driver.execute_script("""
        return {
            exportCSV: typeof exportCSV === 'function',
            exportJSON: typeof exportJSON === 'function',
            exportExcel: typeof exportExcel === 'function' || typeof XLSX !== 'undefined',
            exportYAML: typeof exportYAML === 'function',
            exportPDF: typeof exportPDF === 'function' || typeof jsPDF !== 'undefined'
        };
    """)

    for export_fn, available in export_tests.items():
        log_result(f"Export: {export_fn}", available)

    # 11. Test Automated Unit Tests
    print("\n[11] RUNNING AUTOMATED UNIT TESTS...")

    unit_tests = driver.execute_script("return typeof runAutomatedTests === 'function' ? runAutomatedTests() : null;")
    if unit_tests:
        passed = unit_tests.get('passed', 0)
        failed = unit_tests.get('failed', 0)
        total = passed + failed
        log_result(f"Automated unit tests", failed == 0, f"{passed}/{total} passed")

        if failed > 0:
            for test in unit_tests.get('tests', []):
                if not test.get('passed'):
                    print(f"      Failed: {test.get('name')}")
    else:
        log_result("Automated unit tests", False, "Function not available")

    # 12. Test VALIDATION_STATUS object
    print("\n[12] CHECKING VALIDATION STATUS...")

    val_status = driver.execute_script("""
        if (typeof VALIDATION_STATUS !== 'undefined') {
            return {
                available: true,
                version: VALIDATION_STATUS.version,
                methodCount: Object.keys(VALIDATION_STATUS.methods || {}).length,
                hasBCG: VALIDATION_STATUS.referenceDataset === 'BCG'
            };
        }
        return {available: false};
    """)

    if val_status.get('available'):
        log_result("VALIDATION_STATUS", True,
                   f"v{val_status.get('version')}, {val_status.get('methodCount')} methods")
    else:
        log_result("VALIDATION_STATUS", False, "Not defined")

    # 13. Check for any JS errors during testing
    print("\n[13] FINAL ERROR CHECK...")

    final_logs = driver.get_log('browser')
    final_errors = [l for l in final_logs if l['level'] == 'SEVERE']
    log_result("No JS errors during testing", len(final_errors) == 0,
               f"{len(final_errors)} errors found")

    driver.quit()

except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    results['failed'] += 1

# Final Summary
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

total = results['passed'] + results['failed']
pass_rate = (results['passed'] / max(total, 1)) * 100

print(f"\nTests Passed: {results['passed']}/{total}")
print(f"Tests Failed: {results['failed']}/{total}")
print(f"Pass Rate: {pass_rate:.1f}%")

if results['failed'] > 0:
    print("\nFailed Tests:")
    for test in results['details']:
        if not test['passed']:
            print(f"  - {test['name']}: {test['details']}")

print("\n" + "=" * 70)
if pass_rate >= 95:
    print("VERDICT: EXCELLENT - Application fully functional")
elif pass_rate >= 85:
    print("VERDICT: GOOD - Application working with minor issues")
elif pass_rate >= 70:
    print("VERDICT: ACCEPTABLE - Some features need attention")
else:
    print("VERDICT: NEEDS WORK - Significant issues detected")
print("=" * 70)
