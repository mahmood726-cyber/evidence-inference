#!/usr/bin/env python3
"""Deep validation v2: Test every demo dataset and verify all plots render"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

print("=" * 70)
print("DEEP VALIDATION TEST v2")
print("TruthCert-PairwisePro v1.0")
print("=" * 70)

driver_path = r"C:\Users\user\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32\chromedriver.exe"
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

results = {"passed": 0, "failed": 0, "details": []}

def log_test(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    if passed: results["passed"] += 1
    else: results["failed"] += 1
    results["details"].append({"name": name, "passed": passed, "detail": detail})
    print(f"  [{status}] {name}" + (f" - {detail}" if detail else ""))

try:
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)

    # ========================================
    # PART 1: Test each demo dataset individually
    # ========================================
    print("\n" + "=" * 70)
    print("PART 1: DEMO DATASET VALIDATION")
    print("=" * 70)

    demo_info = driver.execute_script("""
        const info = [];
        for (const [key, dataset] of Object.entries(DEMO_DATASETS)) {
            info.push({
                key: key,
                name: dataset.name,
                studyCount: dataset.studies ? dataset.studies.length : 0,
                dataType: dataset.dataType || 'binary',
                hasYi: dataset.studies && dataset.studies[0] && dataset.studies[0].yi !== undefined
            });
        }
        return info;
    """)
    print(f"\nFound {len(demo_info)} demo datasets")

    for ds in demo_info:
        key = ds['key']
        print(f"\n--- Testing: {key} ({ds['name']}) ---")
        print(f"    Studies: {ds['studyCount']}, Type: {ds['dataType']}, Has yi: {ds['hasYi']}")

        # Load the dataset and run analysis
        result = driver.execute_script(f"""
            try {{
                // Load the dataset
                loadDemoDataset('{key}');

                // Get the demo data directly
                const dataset = DEMO_DATASETS['{key}'];
                const studies = dataset.studies || [];

                if (studies.length < 2) {{
                    return {{success: true, studyCount: studies.length, skipped: true}};
                }}

                // Get yi and vi values
                let yi, vi;
                if (studies[0].yi !== undefined) {{
                    yi = studies.map(s => s.yi);
                    vi = studies.map(s => s.vi);
                }} else {{
                    // Need to calculate effect sizes
                    return {{success: true, studyCount: studies.length, needsCalculation: true}};
                }}

                // Run analysis
                const tau2Result = estimateTau2_REML(yi, vi);
                const pooled = calculatePooledEstimate(yi, vi, tau2Result.tau2);

                return {{
                    success: true,
                    studyCount: studies.length,
                    tau2: tau2Result.tau2,
                    pooled: pooled.estimate,
                    se: pooled.se,
                    I2: pooled.I2
                }};
            }} catch (e) {{
                return {{success: false, error: e.message}};
            }}
        """)

        if result:
            if result.get('success'):
                if result.get('skipped'):
                    log_test(f"Load {key}", True, f"{result.get('studyCount', 0)} studies (skip analysis)")
                elif result.get('needsCalculation'):
                    log_test(f"Load {key}", True, f"{result.get('studyCount', 0)} studies (needs effect calculation)")
                else:
                    tau2 = result.get('tau2', 0)
                    pooled = result.get('pooled', 0)
                    log_test(f"Analyze {key}", True, f"n={result.get('studyCount')}, τ²={tau2:.4f}, pooled={pooled:.4f}")
            else:
                log_test(f"Load {key}", False, result.get('error', 'Unknown error'))
        else:
            log_test(f"Load {key}", False, "No result returned")

    # ========================================
    # PART 2: Test all plot functions with BCG data
    # ========================================
    print("\n" + "=" * 70)
    print("PART 2: PLOT RENDERING VALIDATION")
    print("=" * 70)

    # Get BCG data directly from DEMO_DATASETS
    setup = driver.execute_script("""
        const bcg = DEMO_DATASETS.BCG;
        if (!bcg || !bcg.studies) return {error: 'BCG data not found'};

        window.testStudies = bcg.studies;
        window.testYi = bcg.studies.map(s => s.yi);
        window.testVi = bcg.studies.map(s => s.vi);
        window.testStudyNames = bcg.studies.map(s => s.study);
        window.testTau2 = estimateTau2_REML(window.testYi, window.testVi);
        window.testPooled = calculatePooledEstimate(window.testYi, window.testVi, window.testTau2.tau2);

        return {
            studies: bcg.studies.length,
            tau2: window.testTau2.tau2,
            pooled: window.testPooled.estimate
        };
    """)

    if setup and not setup.get('error'):
        print(f"\nBCG test data prepared: {setup.get('studies', 0)} studies")
        print(f"  τ²={setup.get('tau2', 0):.4f}, pooled={setup.get('pooled', 0):.4f}")

        # Test each plot function
        plot_tests = [
            ("Forest Plot", "renderForestPlot(window.testYi, window.testVi, window.testStudyNames, window.testPooled, window.testTau2.tau2);"),
            ("Funnel Plot", "renderFunnelPlot(window.testYi, window.testVi, window.testPooled.estimate);"),
            ("Baujat Plot", "renderBaujatPlot(window.testYi, window.testVi, window.testStudyNames);"),
            ("Radial Plot", "renderRadialPlot(window.testYi, window.testVi, window.testStudyNames);"),
            ("DOI Plot", "renderDOIPlot(window.testYi, window.testVi, window.testStudyNames);"),
            ("P-Curve Plot", "renderPCurvePlot(window.testYi, window.testVi);"),
        ]

        for plot_name, plot_code in plot_tests:
            result = driver.execute_script(f"""
                try {{
                    {plot_code}
                    return {{success: true}};
                }} catch (e) {{
                    return {{success: false, error: e.message}};
                }}
            """)
            log_test(plot_name, result.get('success', False),
                     "Rendered" if result.get('success') else result.get('error', ''))
    else:
        print(f"\nFailed to setup test data: {setup.get('error', 'Unknown')}")

    # ========================================
    # PART 3: Test advanced analysis functions
    # ========================================
    print("\n" + "=" * 70)
    print("PART 3: ADVANCED ANALYSIS FUNCTIONS")
    print("=" * 70)

    # HKSJ adjustment
    hksj = driver.execute_script("""
        try {
            const result = calculateHKSJ(window.testYi, window.testVi, window.testTau2.tau2);
            return {success: true, pooled: result.pooled, ciLower: result.ciLower, ciUpper: result.ciUpper};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("HKSJ adjustment", hksj.get('success', False),
             f"pooled={hksj.get('pooled', 0):.4f}, CI [{hksj.get('ciLower', 0):.4f}, {hksj.get('ciUpper', 0):.4f}]" if hksj.get('success') else hksj.get('error', ''))

    # Egger test
    egger = driver.execute_script("""
        try {
            const result = eggerTest(window.testYi, window.testVi);
            return {success: true, intercept: result.intercept, pval: result.pval};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Egger test", egger.get('success', False),
             f"intercept={egger.get('intercept', 0):.3f}, p={egger.get('pval', 0):.4f}" if egger.get('success') else egger.get('error', ''))

    # Trim and fill
    tf = driver.execute_script("""
        try {
            const result = trimAndFill(window.testYi, window.testVi);
            return {success: true, k0: result.k0, adjustedEstimate: result.adjustedEstimate};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Trim and Fill", tf.get('success', False),
             f"k0={tf.get('k0', 0)}, adjusted={tf.get('adjustedEstimate', 0):.4f}" if tf.get('success') else tf.get('error', ''))

    # Bayesian meta-analysis
    bayes = driver.execute_script("""
        try {
            const result = bayesianMetaAnalysis(window.testYi, window.testVi, {nIter: 2000, seed: 42});
            return {success: true, pooled: result.pooled, tau2: result.tau2};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Bayesian MA", bayes.get('success', False),
             f"pooled={bayes.get('pooled', 0):.4f}, τ²={bayes.get('tau2', 0):.4f}" if bayes.get('success') else bayes.get('error', ''))

    # Leave-one-out
    loo = driver.execute_script("""
        try {
            const result = leave1out(window.testYi, window.testVi, window.testStudyNames);
            return {success: Array.isArray(result), count: result ? result.length : 0};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Leave-one-out", loo.get('success', False),
             f"{loo.get('count', 0)} analyses" if loo.get('success') else loo.get('error', ''))

    # Cumulative meta-analysis
    cumul = driver.execute_script("""
        try {
            const result = cumulativeMetaAnalysis(window.testYi, window.testVi, window.testStudyNames);
            return {success: Array.isArray(result), count: result ? result.length : 0};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Cumulative MA", cumul.get('success', False),
             f"{cumul.get('count', 0)} steps" if cumul.get('success') else cumul.get('error', ''))

    # Fragility index
    frag = driver.execute_script("""
        try {
            const result = fragilityIndex(window.testYi, window.testVi);
            return {success: true, FI: result.FI};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Fragility Index", frag.get('success', False),
             f"FI={frag.get('FI', 'N/A')}" if frag.get('success') else frag.get('error', ''))

    # E-value
    evalue = driver.execute_script("""
        try {
            const rr = Math.exp(window.testPooled.estimate);
            const result = calculateEValue(rr);
            return {success: true, evalue: result.evalue, threshold: result.threshold};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("E-value", evalue.get('success', False),
             f"E={evalue.get('evalue', 0):.2f}" if evalue.get('success') else evalue.get('error', ''))

    # Influence diagnostics
    influence = driver.execute_script("""
        try {
            if (typeof influenceDiagnostics === 'function') {
                const result = influenceDiagnostics(window.testYi, window.testVi, window.testStudyNames);
                return {success: true, hasResult: !!result};
            }
            return {success: false, error: 'Function not found'};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Influence diagnostics", influence.get('success', False),
             "Calculated" if influence.get('success') else influence.get('error', ''))

    # Prediction interval
    pi = driver.execute_script("""
        try {
            if (typeof calculatePredictionInterval === 'function') {
                const result = calculatePredictionInterval(window.testPooled.estimate, window.testPooled.se,
                                                           window.testTau2.tau2, window.testYi.length);
                return {success: true, lower: result.lower, upper: result.upper};
            }
            return {success: false, error: 'Function not found'};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Prediction interval", pi.get('success', False),
             f"[{pi.get('lower', 0):.3f}, {pi.get('upper', 0):.3f}]" if pi.get('success') else pi.get('error', ''))

    # Subgroup analysis
    print("\n--- Testing Subgroup Analysis ---")
    subgroup = driver.execute_script("""
        try {
            // Use BCG_SUBGROUPS which has subgroup data
            const ds = DEMO_DATASETS.BCG_SUBGROUPS;
            if (!ds || !ds.studies) return {success: false, error: 'Dataset not found'};

            const yi = ds.studies.map(s => s.yi);
            const vi = ds.studies.map(s => s.vi);
            const groups = ds.studies.map(s => s.subgroup || 'Unknown');

            const result = subgroupAnalysis(yi, vi, groups);
            const groupNames = Object.keys(result.subgroups || {});
            return {success: true, nGroups: groupNames.length, groups: groupNames};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Subgroup analysis", subgroup.get('success', False),
             f"{subgroup.get('nGroups', 0)} groups: {subgroup.get('groups', [])}" if subgroup.get('success') else subgroup.get('error', ''))

    # Meta-regression
    print("\n--- Testing Meta-regression ---")
    metareg = driver.execute_script("""
        try {
            // Use METAREG_DOSE which has moderator data
            const ds = DEMO_DATASETS.METAREG_DOSE;
            if (!ds || !ds.studies) return {success: false, error: 'Dataset not found'};

            const yi = ds.studies.map(s => s.yi);
            const vi = ds.studies.map(s => s.vi);
            const mod = ds.studies.map(s => s.moderator || s.dose || 0);

            const result = metaRegression(yi, vi, mod);
            return {success: true, intercept: result.intercept, slope: result.slope, pval: result.pval};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Meta-regression", metareg.get('success', False),
             f"slope={metareg.get('slope', 0):.4f}, p={metareg.get('pval', 0):.4f}" if metareg.get('success') else metareg.get('error', ''))

    # ========================================
    # PART 4: Test all tau² estimators
    # ========================================
    print("\n" + "=" * 70)
    print("PART 4: TAU-SQUARED ESTIMATORS")
    print("=" * 70)

    # Reference values from R/metafor for BCG dataset
    ref_tau2 = {
        "DL": 0.30876,
        "REML": 0.313243,
        "ML": 0.280028,
        "PM": 0.318094,
        "HS": 0.228363,
        "SJ": 0.345516,
        "HE": 0.328564,
        "EB": 0.318069
    }

    for method, expected in ref_tau2.items():
        result = driver.execute_script(f"""
            try {{
                const fn = window['estimateTau2_{method}'];
                if (!fn) return {{success: false, error: 'Function not found'}};
                const result = fn(window.testYi, window.testVi);
                return {{success: true, tau2: result.tau2, expected: {expected}}};
            }} catch (e) {{
                return {{success: false, error: e.message}};
            }}
        """)
        if result.get('success'):
            tau2 = result.get('tau2', 0)
            diff = abs(tau2 - expected)
            passed = diff < 0.01
            log_test(f"τ²_{method}", passed, f"JS={tau2:.6f}, R={expected:.6f}, Δ={diff:.6f}")
        else:
            log_test(f"τ²_{method}", False, result.get('error', ''))

    # ========================================
    # PART 5: Test export functions
    # ========================================
    print("\n" + "=" * 70)
    print("PART 5: EXPORT FUNCTIONS")
    print("=" * 70)

    # Generate R code
    rcode = driver.execute_script("""
        try {
            const code = generateRCode();
            return {success: typeof code === 'string' && code.length > 50, length: code ? code.length : 0,
                    hasMetafor: code.includes('metafor'), hasRma: code.includes('rma')};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Generate R Code", rcode.get('success', False),
             f"{rcode.get('length', 0)} chars, metafor={rcode.get('hasMetafor')}" if rcode.get('success') else rcode.get('error', ''))

    # Check export functions exist
    exports = driver.execute_script("""
        return {
            exportCSV: typeof exportCSV === 'function',
            exportJSON: typeof exportJSON === 'function',
            exportExcel: typeof exportExcel === 'function' || typeof XLSX !== 'undefined',
            exportPDF: typeof exportPDF === 'function' || typeof html2canvas !== 'undefined'
        };
    """)
    for name, exists in exports.items():
        log_test(name, exists)

    # ========================================
    # PART 6: Built-in test suite
    # ========================================
    print("\n" + "=" * 70)
    print("PART 6: BUILT-IN TEST SUITE")
    print("=" * 70)

    builtin = driver.execute_script("""
        if (typeof runAutomatedTests === 'function') {
            return runAutomatedTests();
        }
        return null;
    """)

    if builtin:
        passed = builtin.get('passed', 0)
        failed = builtin.get('failed', 0)
        log_test(f"Automated tests ({passed}/{passed+failed})", failed == 0)
        if builtin.get('results'):
            print("  Test details:")
            for test in builtin.get('results', []):
                status = "✓" if test.get('passed') else "✗"
                print(f"    {status} {test.get('name', 'Unknown')}")
    else:
        log_test("Automated tests", False, "Function not available")

    # ========================================
    # PART 7: UI and library checks
    # ========================================
    print("\n" + "=" * 70)
    print("PART 7: UI AND LIBRARIES")
    print("=" * 70)

    libs = driver.execute_script("""
        return {
            Plotly: typeof Plotly !== 'undefined',
            XLSX: typeof XLSX !== 'undefined',
            jStat: typeof jStat !== 'undefined',
            html2canvas: typeof html2canvas !== 'undefined',
            Chart: typeof Chart !== 'undefined'
        };
    """)
    for name, loaded in libs.items():
        log_test(f"Library: {name}", loaded)

    # ========================================
    # FINAL SUMMARY
    # ========================================
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    total = results["passed"] + results["failed"]
    pct = (results["passed"] / total) * 100 if total > 0 else 0

    print(f"\nTotal Tests: {total}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Pass Rate: {pct:.1f}%")

    if results["failed"] > 0:
        print("\n--- Failed Tests ---")
        for d in results["details"]:
            if not d["passed"]:
                print(f"  ✗ {d['name']}: {d.get('detail', '')}")

    print("\n" + "=" * 70)
    if pct >= 95:
        print("VERDICT: ✓ EXCELLENT - Application fully validated")
    elif pct >= 85:
        print("VERDICT: ✓ GOOD - Most features working correctly")
    elif pct >= 70:
        print("VERDICT: ⚠ ACCEPTABLE - Some issues detected")
    else:
        print("VERDICT: ✗ NEEDS ATTENTION - Multiple issues detected")
    print("=" * 70)

finally:
    driver.quit()
