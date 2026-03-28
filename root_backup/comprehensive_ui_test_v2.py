#!/usr/bin/env python3
"""Comprehensive UI Test for TruthCert-PairwisePro Meta-Analysis Application"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
import time

print("=" * 70)
print("COMPREHENSIVE UI TEST v2")
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

def dismiss_alerts(driver):
    """Dismiss any open alerts"""
    try:
        alert = driver.switch_to.alert
        alert.accept()
        return True
    except:
        return False

def safe_execute(driver, script):
    """Execute script with alert handling"""
    try:
        # Dismiss any pending alerts first
        dismiss_alerts(driver)
        return driver.execute_script(script)
    except UnexpectedAlertPresentException:
        dismiss_alerts(driver)
        # Retry after dismissing
        return driver.execute_script(script)

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

    # 2. Load Demo Dataset (BCG) properly
    print("\n[2] LOADING DEMO DATASET...")

    # Check SAMPLES structure
    samples_info = safe_execute(driver, """
        if (typeof SAMPLES !== 'undefined') {
            const keys = Object.keys(SAMPLES);
            const bcg = SAMPLES.bcg;
            return {
                available: true,
                keys: keys,
                bcgKeys: bcg ? Object.keys(bcg) : [],
                bcgStudiesCount: bcg && bcg.studies ? bcg.studies.length : 0
            };
        }
        return {available: false};
    """)
    log_result("SAMPLES object available", samples_info.get('available', False),
               f"Keys: {samples_info.get('keys', [])}")

    # Properly load BCG data
    load_result = safe_execute(driver, """
        if (typeof SAMPLES !== 'undefined' && SAMPLES.bcg) {
            // Check if studies have proper structure
            const bcg = SAMPLES.bcg;
            const studies = bcg.studies || bcg;

            if (Array.isArray(studies) && studies.length > 0) {
                // Ensure studies have yi and vi
                const validStudies = studies.filter(s => {
                    if (s.yi !== undefined && s.vi !== undefined) return true;
                    // Calculate yi/vi from binary data
                    if (s.events1 !== undefined && s.total1 !== undefined) {
                        const a = s.events1, b = s.total1 - s.events1;
                        const c = s.events2, d = s.total2 - s.events2;
                        if (a > 0 && b > 0 && c > 0 && d > 0) {
                            s.yi = Math.log((a/b) / (c/d));  // log odds ratio
                            s.vi = 1/a + 1/b + 1/c + 1/d;
                            return true;
                        }
                    }
                    return false;
                });

                AppState.studies = validStudies;
                AppState.dataType = 'binary';
                return {success: true, count: validStudies.length};
            }
        }
        return {success: false};
    """)
    log_result("BCG data loaded", load_result.get('success', False),
               f"{load_result.get('count', 0)} studies")

    # 3. Test Core Functions WITHOUT running full analysis (which may have UI dependencies)
    print("\n[3] TESTING CORE STATISTICAL FUNCTIONS...")

    # Test statistical distributions
    stat_funcs = safe_execute(driver, """
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

    # 4. Test tau² estimators
    print("\n[4] TESTING TAU² ESTIMATORS...")

    tau2_tests = safe_execute(driver, """
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

    # 5. Test Pooled Estimate Functions
    print("\n[5] TESTING POOLED ESTIMATE FUNCTIONS...")

    pooled_tests = safe_execute(driver, """
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547, -0.786116, -1.620898, 0.011952, -0.469418, -1.371345, -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210, 0.006906, 0.223017, 0.003962, 0.056434, 0.073025, 0.012412, 0.532506, 0.071405];

        const results = {};

        // Fixed effect
        if (typeof calculatePooledEstimate === 'function') {
            try {
                const r = calculatePooledEstimate(yi, vi, {model: 'FE'});
                results.fixedEffect = {available: true, pooled: r.pooled, se: r.se, success: !isNaN(r.pooled)};
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
                results.randomEffects = {available: true, pooled: r.pooled, tau2: r.tau2, success: !isNaN(r.pooled)};
            } catch(e) {
                results.randomEffects = {available: true, error: e.message};
            }
        }

        // HKSJ adjustment
        if (typeof calculateHKSJ === 'function') {
            try {
                const r = calculateHKSJ(yi, vi, 0.3);
                results.HKSJ = {available: true, pooled: r.pooled, ciLower: r.ciLower, ciUpper: r.ciUpper, success: !isNaN(r.pooled)};
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
            elif result.get('success', False):
                log_result(f"Pooled: {test}", True, f"pooled={result.get('pooled', 'N/A'):.4f}")
            else:
                log_result(f"Pooled: {test}", False, "Returned NaN")
        else:
            log_result(f"Pooled: {test}", False, "Not available")

    # 6. Test Bayesian Analysis
    print("\n[6] TESTING BAYESIAN ANALYSIS...")

    bayes_result = safe_execute(driver, """
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
                    tau2Mean: r.summary ? r.summary.tau2.mean : null,
                    success: r.summary && !isNaN(r.summary.theta.mean)
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
        elif bayes_result.get('success', False):
            log_result("Bayesian MCMC", True,
                       f"theta={bayes_result.get('thetaMean', 'N/A'):.4f}, tau2={bayes_result.get('tau2Mean', 'N/A'):.4f}")
        else:
            log_result("Bayesian MCMC", False, "Missing summary")
    else:
        log_result("Bayesian MCMC", False, "Not available")

    # 7. Test Publication Bias Functions
    print("\n[7] TESTING PUBLICATION BIAS FUNCTIONS...")

    bias_tests = safe_execute(driver, """
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547, -0.786116, -1.620898, 0.011952, -0.469418, -1.371345, -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210, 0.006906, 0.223017, 0.003962, 0.056434, 0.073025, 0.012412, 0.532506, 0.071405];
        const se = vi.map(v => Math.sqrt(v));

        const results = {};

        // Egger's test
        if (typeof eggerTest === 'function') {
            try {
                const r = eggerTest(yi, se);
                results.egger = {available: true, intercept: r.intercept, pValue: r.pValue, success: !isNaN(r.pValue)};
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
                results.begg = {available: true, tau: r.tau, pValue: r.pValue, success: !isNaN(r.pValue)};
            } catch(e) {
                results.begg = {available: true, error: e.message};
            }
        } else {
            results.begg = {available: false};
        }

        // Trim and fill
        if (typeof trimAndFill === 'function') {
            try {
                const studies = yi.map((y, i) => ({yi: y, vi: vi[i], se: se[i]}));
                const r = trimAndFill(studies);
                results.trimFill = {available: true, k0: r.k0, adjustedPooled: r.adjustedPooled, success: true};
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
            elif result.get('success', False):
                log_result(f"Pub bias: {test}", True)
            else:
                log_result(f"Pub bias: {test}", False, "Returned invalid values")
        else:
            log_result(f"Pub bias: {test}", False, "Not available")

    # 8. Test Plot Functions
    print("\n[8] TESTING PLOT FUNCTIONS...")

    plot_tests = safe_execute(driver, """
        const results = {};

        // Check Plotly is available
        results.plotlyAvailable = typeof Plotly !== 'undefined';

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

    # 9. Test Export Functions
    print("\n[9] TESTING EXPORT FUNCTIONS...")

    export_tests = safe_execute(driver, """
        return {
            exportCSV: typeof exportCSV === 'function',
            exportJSON: typeof exportJSON === 'function',
            XLSX_available: typeof XLSX !== 'undefined',
            jsPDF_available: typeof jspdf !== 'undefined' || typeof jsPDF !== 'undefined',
            html2canvas: typeof html2canvas !== 'undefined'
        };
    """)

    for export_fn, available in export_tests.items():
        log_result(f"Export: {export_fn}", available)

    # 10. Test Automated Unit Tests
    print("\n[10] RUNNING AUTOMATED UNIT TESTS...")

    unit_tests = safe_execute(driver, "return typeof runAutomatedTests === 'function' ? runAutomatedTests() : null;")
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

    # 11. Test VALIDATION_STATUS object
    print("\n[11] CHECKING VALIDATION STATUS...")

    val_status = safe_execute(driver, """
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

    # 12. Test APPROXIMATION_WARNINGS object
    print("\n[12] CHECKING APPROXIMATION WARNINGS...")

    approx_warnings = safe_execute(driver, """
        if (typeof APPROXIMATION_WARNINGS !== 'undefined') {
            return {
                available: true,
                categories: Object.keys(APPROXIMATION_WARNINGS).length
            };
        }
        return {available: false};
    """)

    if approx_warnings.get('available'):
        log_result("APPROXIMATION_WARNINGS", True,
                   f"{approx_warnings.get('categories')} categories")
    else:
        log_result("APPROXIMATION_WARNINGS", False, "Not defined")

    # 13. Test UI Elements
    print("\n[13] TESTING UI ELEMENTS...")

    ui_elements = safe_execute(driver, """
        const results = {};

        // Check for main containers
        results.hasDataPanel = !!document.getElementById('panel-data') || !!document.querySelector('[data-tab="data"]');
        results.hasAnalysisPanel = !!document.getElementById('panel-analysis') || !!document.querySelector('[data-tab="analysis"]');
        results.hasForestContainer = !!document.getElementById('forest-plot') || !!document.querySelector('.forest-plot');
        results.hasFunnelContainer = !!document.getElementById('funnel-plot') || !!document.querySelector('.funnel-plot');

        // Check for buttons
        results.hasRunButton = !!document.querySelector('[onclick*="runAnalysis"]') || !!document.getElementById('run-analysis');
        results.hasExportButtons = !!document.querySelector('[onclick*="export"]') || !!document.getElementById('export-csv');

        // Check for tabs
        const tabs = document.querySelectorAll('.tab, [data-tab], .tabs-nav button');
        results.tabCount = tabs.length;

        return results;
    """)

    for element, status in ui_elements.items():
        if element == 'tabCount':
            log_result(f"UI: Tab buttons", status >= 3, f"{status} tabs found")
        else:
            log_result(f"UI: {element}", status)

    # 14. Check for any JS errors during testing
    print("\n[14] FINAL ERROR CHECK...")

    final_logs = driver.get_log('browser')
    final_errors = [l for l in final_logs if l['level'] == 'SEVERE']
    log_result("No JS errors during testing", len(final_errors) == 0,
               f"{len(final_errors)} errors found")

    if final_errors:
        for err in final_errors[:3]:
            print(f"      Error: {err['message'][:80]}...")

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
