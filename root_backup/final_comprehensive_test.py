#!/usr/bin/env python3
"""Final Comprehensive UI Test for TruthCert-PairwisePro Meta-Analysis Application"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

print("=" * 70)
print("FINAL COMPREHENSIVE UI TEST")
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

    # 2. Check SAMPLES availability
    print("\n[2] CHECKING SAMPLE DATA...")
    samples_info = driver.execute_script("""
        if (typeof SAMPLES !== 'undefined') {
            return {
                available: true,
                keys: Object.keys(SAMPLES),
                bcgStudies: SAMPLES.bcg && SAMPLES.bcg.studies ? SAMPLES.bcg.studies.length : 0
            };
        }
        return {available: false};
    """)
    log_result("SAMPLES object available", samples_info.get('available', False),
               f"Keys: {samples_info.get('keys', [])}")

    # 3. Test Core Statistical Functions
    print("\n[3] TESTING CORE STATISTICAL FUNCTIONS...")
    stat_funcs = driver.execute_script("""
        const tests = {};
        tests.pnorm = typeof pnorm === 'function' && Math.abs(pnorm(1.96) - 0.975) < 0.001;
        tests.qnorm = typeof qnorm === 'function' && Math.abs(qnorm(0.975) - 1.96) < 0.01;
        tests.dnorm = typeof dnorm === 'function' && Math.abs(dnorm(0) - 0.3989) < 0.001;
        tests.pt = typeof pt === 'function' && Math.abs(pt(2, 10) - 0.9633) < 0.001;
        tests.qt = typeof qt === 'function' && Math.abs(qt(0.975, 10) - 2.228) < 0.01;
        tests.pchisq = typeof pchisq === 'function' && Math.abs(pchisq(3.84, 1) - 0.95) < 0.01;
        tests.lgamma = typeof lgamma === 'function' && Math.abs(lgamma(5) - 3.178) < 0.01;
        tests.betainc = typeof betainc === 'function';
        tests.gammainc = typeof gammainc === 'function';
        return tests;
    """)
    for func, passed in stat_funcs.items():
        log_result(f"Statistical function: {func}", passed)

    # 4. Test tau² estimators
    print("\n[4] TESTING TAU² ESTIMATORS (8 methods)...")
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
                    results[method] = {computed: r.tau2, reference: refValues[method], match: diff < 0.001};
                } catch(e) {
                    results[method] = {error: e.message, match: false};
                }
            } else {
                results[method] = {missing: true, match: false};
            }
        }
        return results;
    """)
    for method, result in tau2_tests.items():
        if result.get('match'):
            log_result(f"Tau² {method}", True, f"{result['computed']:.6f} matches R")
        elif 'error' in result:
            log_result(f"Tau² {method}", False, f"Error: {result['error']}")
        elif result.get('missing'):
            log_result(f"Tau² {method}", False, "Not found")
        else:
            log_result(f"Tau² {method}", False, f"Got {result.get('computed')}, expected {result.get('reference')}")

    # 5. Test Pooled Estimate Functions (correct property: theta)
    print("\n[5] TESTING POOLED ESTIMATE FUNCTIONS...")
    pooled_tests = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547, -0.786116, -1.620898, 0.011952, -0.469418, -1.371345, -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210, 0.006906, 0.223017, 0.003962, 0.056434, 0.073025, 0.012412, 0.532506, 0.071405];
        const results = {};

        // Fixed effect (tau2=0)
        try {
            const r = calculatePooledEstimate(yi, vi, 0);
            results.fixedEffect = {theta: r.theta, se: r.se, success: !isNaN(r.theta)};
        } catch(e) {
            results.fixedEffect = {error: e.message};
        }

        // Random effects with DL tau²
        try {
            const tau2DL = estimateTau2_DL(yi, vi).tau2;
            const r = calculatePooledEstimate(yi, vi, tau2DL);
            results.randomEffects = {theta: r.theta, se: r.se, tau2: tau2DL, success: !isNaN(r.theta)};
        } catch(e) {
            results.randomEffects = {error: e.message};
        }

        // HKSJ
        try {
            const tau2DL = estimateTau2_DL(yi, vi).tau2;
            const r = calculateHKSJ(yi, vi, tau2DL);
            results.HKSJ = {pooled: r.pooled, ciLower: r.ciLower, ciUpper: r.ciUpper, success: !isNaN(r.pooled)};
        } catch(e) {
            results.HKSJ = {error: e.message};
        }

        return results;
    """)
    for test, result in pooled_tests.items():
        if 'error' in result:
            log_result(f"Pooled: {test}", False, f"Error: {result['error']}")
        elif result.get('success', False):
            val = result.get('theta') or result.get('pooled')
            log_result(f"Pooled: {test}", True, f"theta={val:.4f}")
        else:
            log_result(f"Pooled: {test}", False, "Returned NaN")

    # 6. Test Bayesian Analysis
    print("\n[6] TESTING BAYESIAN MCMC...")
    bayes_result = driver.execute_script("""
        if (typeof bayesianMetaAnalysis === 'function') {
            try {
                const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
                const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
                const r1 = bayesianMetaAnalysis(yi, vi, {nIter: 2000, seed: 42});
                const r2 = bayesianMetaAnalysis(yi, vi, {nIter: 2000, seed: 42});
                const diff = Math.abs(r1.summary.theta.mean - r2.summary.theta.mean);
                return {
                    available: true,
                    theta: r1.summary.theta.mean,
                    tau2: r1.summary.tau2.mean,
                    I2: r1.summary.I2.mean,
                    reproducible: diff < 0.0001,
                    success: !isNaN(r1.summary.theta.mean)
                };
            } catch(e) {
                return {available: true, error: e.message};
            }
        }
        return {available: false};
    """)
    if bayes_result.get('success', False):
        log_result("Bayesian MCMC", True,
                   f"theta={bayes_result['theta']:.4f}, tau2={bayes_result['tau2']:.4f}, repro={bayes_result['reproducible']}")
    elif 'error' in bayes_result:
        log_result("Bayesian MCMC", False, f"Error: {bayes_result['error']}")
    else:
        log_result("Bayesian MCMC", False, "Not available")

    # 7. Test Publication Bias Functions
    print("\n[7] TESTING PUBLICATION BIAS FUNCTIONS...")
    bias_tests = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547, -0.786116, -1.620898, 0.011952, -0.469418, -1.371345, -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210, 0.006906, 0.223017, 0.003962, 0.056434, 0.073025, 0.012412, 0.532506, 0.071405];
        const results = {};

        // Egger's test (note: takes yi, vi not yi, se)
        if (typeof eggerTest === 'function') {
            try {
                const r = eggerTest(yi, vi);
                results.egger = {intercept: r.intercept, pValue: r.pValue, success: !isNaN(r.pValue)};
            } catch(e) {
                results.egger = {error: e.message};
            }
        } else {
            results.egger = {missing: true};
        }

        // Trim and fill (note: takes yi, vi not studies array)
        if (typeof trimAndFill === 'function') {
            try {
                const r = trimAndFill(yi, vi);
                results.trimFill = {k0: r.k0, adjustedPooled: r.adjustedPooled, success: true};
            } catch(e) {
                results.trimFill = {error: e.message};
            }
        } else {
            results.trimFill = {missing: true};
        }

        // Rank correlation test
        if (typeof rankCorrelationTest === 'function') {
            try {
                const r = rankCorrelationTest(yi, vi);
                results.rankCorr = {tau: r.tau, pValue: r.pValue, success: true};
            } catch(e) {
                results.rankCorr = {error: e.message};
            }
        } else {
            results.rankCorr = {missing: true};
        }

        return results;
    """)
    for test, result in bias_tests.items():
        if 'error' in result:
            log_result(f"Pub bias: {test}", False, f"Error: {result['error']}")
        elif result.get('missing'):
            log_result(f"Pub bias: {test}", False, "Not available")
        elif result.get('success'):
            log_result(f"Pub bias: {test}", True)
        else:
            log_result(f"Pub bias: {test}", False, "Failed")

    # 8. Test Plot Functions
    print("\n[8] TESTING PLOT FUNCTIONS...")
    plot_tests = driver.execute_script("""
        return {
            plotlyAvailable: typeof Plotly !== 'undefined',
            forestPlot: typeof renderForestPlot === 'function',
            funnelPlot: typeof renderFunnelPlot === 'function',
            baujatPlot: typeof renderBaujatPlot === 'function',
            galbraithPlot: typeof renderGalbraithPlot === 'function',
            influencePlot: typeof renderInfluencePlot === 'function',
            cumulativePlot: typeof renderCumulativePlot === 'function',
            doiPlot: typeof renderDoiPlot === 'function'
        };
    """)
    for plot, available in plot_tests.items():
        log_result(f"Plot: {plot}", available)

    # 9. Test Export Functions
    print("\n[9] TESTING EXPORT FUNCTIONS...")
    export_tests = driver.execute_script("""
        return {
            exportAnalysisJSON: typeof exportAnalysisJSON === 'function',
            exportVerdictYAML: typeof exportVerdictYAML === 'function',
            exportVerdictJSON: typeof exportVerdictJSON === 'function',
            exportVerdictExcel: typeof exportVerdictExcel === 'function',
            exportHTACertificate: typeof exportHTACertificate === 'function',
            exportHTAExcel: typeof exportHTAExcel === 'function',
            exportHTAPDF: typeof exportHTAPDF === 'function',
            exportToR: typeof exportToR === 'function',
            XLSX_available: typeof XLSX !== 'undefined',
            jsPDF_available: typeof jspdf !== 'undefined',
            html2canvas_available: typeof html2canvas !== 'undefined'
        };
    """)
    for fn, available in export_tests.items():
        log_result(f"Export: {fn}", available)

    # 10. Test Automated Unit Tests
    print("\n[10] RUNNING AUTOMATED UNIT TESTS (14 tests)...")
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

    # 11. Test VALIDATION_STATUS
    print("\n[11] CHECKING VALIDATION STATUS...")
    val_status = driver.execute_script("""
        if (typeof VALIDATION_STATUS !== 'undefined') {
            return {
                available: true,
                version: VALIDATION_STATUS.version,
                methodCount: Object.keys(VALIDATION_STATUS.methods || {}).length,
                referenceDataset: VALIDATION_STATUS.referenceDataset,
                referencePackage: VALIDATION_STATUS.referencePackage
            };
        }
        return {available: false};
    """)
    if val_status.get('available'):
        log_result("VALIDATION_STATUS", True,
                   f"v{val_status.get('version')}, {val_status.get('methodCount')} methods, ref: {val_status.get('referencePackage')}")
    else:
        log_result("VALIDATION_STATUS", False, "Not defined")

    # 12. Test APPROXIMATION_WARNINGS
    print("\n[12] CHECKING APPROXIMATION WARNINGS...")
    approx_warnings = driver.execute_script("""
        if (typeof APPROXIMATION_WARNINGS !== 'undefined') {
            return {
                available: true,
                categories: Object.keys(APPROXIMATION_WARNINGS)
            };
        }
        return {available: false};
    """)
    if approx_warnings.get('available'):
        log_result("APPROXIMATION_WARNINGS", True,
                   f"{len(approx_warnings.get('categories', []))} categories")
    else:
        log_result("APPROXIMATION_WARNINGS", False, "Not defined")

    # 13. Test Verdict System
    print("\n[13] TESTING VERDICT SYSTEM...")
    verdict_tests = driver.execute_script("""
        return {
            buildThreatLedger: typeof buildThreatLedger === 'function',
            determineSeverity: typeof determineSeverity === 'function',
            determineVerdict: typeof determineVerdict === 'function',
            assessGRADE: typeof assessGRADE === 'function'
        };
    """)
    for fn, available in verdict_tests.items():
        log_result(f"Verdict: {fn}", available)

    # 14. Test HTA Functions
    print("\n[14] TESTING HTA FUNCTIONS...")
    hta_tests = driver.execute_script("""
        return {
            runHTA: typeof runHTA === 'function',
            runDSA: typeof runDSA === 'function',
            calculateNMB: typeof calculateNMB === 'function',
            determineRecommendation: typeof determineRecommendation === 'function',
            verdictToTier: typeof verdictToTier === 'function'
        };
    """)
    for fn, available in hta_tests.items():
        log_result(f"HTA: {fn}", available)

    # 15. Final error check
    print("\n[15] FINAL ERROR CHECK...")
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
    print("VERDICT: EXCELLENT - All major systems operational")
elif pass_rate >= 85:
    print("VERDICT: GOOD - Application working correctly")
elif pass_rate >= 70:
    print("VERDICT: ACCEPTABLE - Some features need attention")
else:
    print("VERDICT: NEEDS WORK - Significant issues detected")
print("=" * 70)
