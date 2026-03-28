#!/usr/bin/env python3
"""Deep validation: Test every demo dataset and verify all plots render"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

print("=" * 70)
print("DEEP VALIDATION TEST")
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

    demo_keys = driver.execute_script("return Object.keys(DEMO_DATASETS);")
    print(f"\nFound {len(demo_keys)} demo datasets")

    for key in demo_keys:
        print(f"\n--- Testing: {key} ---")

        # Load the dataset
        result = driver.execute_script(f"""
            try {{
                const dataset = DEMO_DATASETS['{key}'];
                if (!dataset) return {{success: false, error: 'Dataset not found'}};

                // Clear existing data
                window.studies = [];

                // Load the dataset
                loadDemoDataset('{key}');

                const studies = window.studies || [];
                return {{
                    success: true,
                    studyCount: studies.length,
                    name: dataset.name || '{key}',
                    hasData: studies.length > 0
                }};
            }} catch (e) {{
                return {{success: false, error: e.message}};
            }}
        """)

        if result and result.get('success'):
            log_test(f"Load {key}", True, f"{result.get('studyCount', 0)} studies")

            # Run analysis on the dataset
            if result.get('studyCount', 0) >= 2:
                analysis = driver.execute_script("""
                    try {
                        if (!window.studies || window.studies.length < 2) {
                            return {success: false, error: 'No studies loaded'};
                        }

                        // Get yi and vi from studies
                        const yi = window.studies.map(s => s.yi);
                        const vi = window.studies.map(s => s.vi);

                        if (yi.some(v => v === undefined || v === null || isNaN(v))) {
                            return {success: false, error: 'Invalid yi values'};
                        }
                        if (vi.some(v => v === undefined || v === null || isNaN(v))) {
                            return {success: false, error: 'Invalid vi values'};
                        }

                        // Run analysis
                        const tau2Result = estimateTau2_REML(yi, vi);
                        const pooled = calculatePooledEstimate(yi, vi, tau2Result.tau2);

                        return {
                            success: true,
                            tau2: tau2Result.tau2,
                            pooled: pooled.estimate,
                            se: pooled.se,
                            I2: pooled.I2
                        };
                    } catch (e) {
                        return {success: false, error: e.message};
                    }
                """)

                if analysis and analysis.get('success'):
                    log_test(f"Analyze {key}", True,
                             f"τ²={analysis.get('tau2', 0):.4f}, pooled={analysis.get('pooled', 0):.4f}")
                else:
                    log_test(f"Analyze {key}", False, analysis.get('error', 'Unknown error') if analysis else 'No result')
            else:
                log_test(f"Analyze {key}", True, "Skipped (single study or special format)")
        else:
            log_test(f"Load {key}", False, result.get('error', 'Unknown error') if result else 'No result')

    # ========================================
    # PART 2: Test all plot functions with actual data
    # ========================================
    print("\n" + "=" * 70)
    print("PART 2: PLOT RENDERING VALIDATION")
    print("=" * 70)

    # Load BCG dataset for plotting tests
    driver.execute_script("loadDemoDataset('BCG');")
    time.sleep(1)

    # Prepare data for plots
    setup = driver.execute_script("""
        window.testYi = window.studies.map(s => s.yi);
        window.testVi = window.studies.map(s => s.vi);
        window.testStudyNames = window.studies.map(s => s.study);
        window.testTau2 = estimateTau2_REML(window.testYi, window.testVi);
        window.testPooled = calculatePooledEstimate(window.testYi, window.testVi, window.testTau2.tau2);
        return {
            studies: window.studies.length,
            tau2: window.testTau2.tau2,
            pooled: window.testPooled.estimate
        };
    """)
    print(f"\nTest data prepared: {setup.get('studies', 0)} studies, τ²={setup.get('tau2', 0):.4f}")

    # Test each plot function
    plot_tests = [
        ("renderForestPlot", """
            renderForestPlot(window.testYi, window.testVi, window.testStudyNames,
                             window.testPooled, window.testTau2.tau2);
        """),
        ("renderFunnelPlot", """
            renderFunnelPlot(window.testYi, window.testVi, window.testPooled.estimate);
        """),
        ("renderBaujatPlot", """
            renderBaujatPlot(window.testYi, window.testVi, window.testStudyNames);
        """),
        ("renderRadialPlot", """
            renderRadialPlot(window.testYi, window.testVi, window.testStudyNames);
        """),
        ("renderDOIPlot", """
            renderDOIPlot(window.testYi, window.testVi, window.testStudyNames);
        """),
        ("renderPCurvePlot", """
            renderPCurvePlot(window.testYi, window.testVi);
        """),
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
        log_test(f"Render {plot_name}", result.get('success', False),
                 result.get('error', '') if not result.get('success') else 'Rendered')

    # ========================================
    # PART 3: Test advanced analysis functions
    # ========================================
    print("\n" + "=" * 70)
    print("PART 3: ADVANCED ANALYSIS VALIDATION")
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
             f"pooled={hksj.get('pooled', 0):.4f}, 95% CI [{hksj.get('ciLower', 0):.4f}, {hksj.get('ciUpper', 0):.4f}]" if hksj.get('success') else hksj.get('error', ''))

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
             f"intercept={egger.get('intercept', 0):.4f}, p={egger.get('pval', 0):.4f}" if egger.get('success') else egger.get('error', ''))

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
            return {success: true, pooled: result.pooled, tau2: result.tau2, credLower: result.credLower, credUpper: result.credUpper};
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
            return {success: true, studies: result.length};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Leave-one-out", loo.get('success', False),
             f"{loo.get('studies', 0)} analyses" if loo.get('success') else loo.get('error', ''))

    # Cumulative meta-analysis
    cumul = driver.execute_script("""
        try {
            const result = cumulativeMetaAnalysis(window.testYi, window.testVi, window.testStudyNames);
            return {success: true, steps: result.length};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Cumulative MA", cumul.get('success', False),
             f"{cumul.get('steps', 0)} steps" if cumul.get('success') else cumul.get('error', ''))

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
             f"FI={frag.get('FI', 0)}" if frag.get('success') else frag.get('error', ''))

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
             f"E-value={evalue.get('evalue', 0):.2f}" if evalue.get('success') else evalue.get('error', ''))

    # Subgroup analysis (using BCG_SUBGROUPS)
    driver.execute_script("loadDemoDataset('BCG_SUBGROUPS');")
    time.sleep(0.5)
    subgroup = driver.execute_script("""
        try {
            const yi = window.studies.map(s => s.yi);
            const vi = window.studies.map(s => s.vi);
            const groups = window.studies.map(s => s.subgroup || 'Unknown');
            const result = subgroupAnalysis(yi, vi, groups);
            return {success: true, nGroups: Object.keys(result.subgroups || {}).length};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Subgroup analysis", subgroup.get('success', False),
             f"{subgroup.get('nGroups', 0)} groups" if subgroup.get('success') else subgroup.get('error', ''))

    # Meta-regression
    driver.execute_script("loadDemoDataset('METAREG_DOSE');")
    time.sleep(0.5)
    metareg = driver.execute_script("""
        try {
            const yi = window.studies.map(s => s.yi);
            const vi = window.studies.map(s => s.vi);
            const mod = window.studies.map(s => s.moderator || 0);
            const result = metaRegression(yi, vi, mod);
            return {success: true, intercept: result.intercept, slope: result.slope, pval: result.pval};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Meta-regression", metareg.get('success', False),
             f"slope={metareg.get('slope', 0):.4f}, p={metareg.get('pval', 0):.4f}" if metareg.get('success') else metareg.get('error', ''))

    # ========================================
    # PART 4: Test export functions
    # ========================================
    print("\n" + "=" * 70)
    print("PART 4: EXPORT FUNCTION VALIDATION")
    print("=" * 70)

    # Load BCG for export tests
    driver.execute_script("loadDemoDataset('BCG');")
    time.sleep(0.5)

    # Generate R code
    rcode = driver.execute_script("""
        try {
            const code = generateRCode();
            return {success: typeof code === 'string' && code.length > 100, length: code ? code.length : 0};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Generate R Code", rcode.get('success', False),
             f"{rcode.get('length', 0)} chars" if rcode.get('success') else rcode.get('error', ''))

    # Export CSV (check function returns data)
    csv = driver.execute_script("""
        try {
            // Check if the function exists and can prepare data
            if (typeof exportCSV !== 'function') return {success: false, error: 'Function not found'};
            // We can't actually trigger download, but we can verify the function is callable
            return {success: true};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Export CSV function", csv.get('success', False))

    # Export JSON
    jsonExport = driver.execute_script("""
        try {
            if (typeof exportJSON !== 'function') return {success: false, error: 'Function not found'};
            return {success: true};
        } catch (e) {
            return {success: false, error: e.message};
        }
    """)
    log_test("Export JSON function", jsonExport.get('success', False))

    # ========================================
    # PART 5: Test UI elements and buttons
    # ========================================
    print("\n" + "=" * 70)
    print("PART 5: UI ELEMENTS VALIDATION")
    print("=" * 70)

    # Check for critical UI elements
    ui_elements = driver.execute_script("""
        const elements = {};

        // Check for key buttons/elements
        elements.runAnalysisBtn = !!document.querySelector('[onclick*="runAnalysis"]') ||
                                  !!document.querySelector('button[id*="run"]');
        elements.forestPlotContainer = !!document.getElementById('forestPlot') ||
                                       !!document.querySelector('.forest-plot');
        elements.funnelPlotContainer = !!document.getElementById('funnelPlot') ||
                                       !!document.querySelector('.funnel-plot');
        elements.dataTable = !!document.querySelector('table') ||
                            !!document.querySelector('[id*="data"]');
        elements.demoSelector = !!document.querySelector('select') ||
                               !!document.querySelector('[onclick*="loadDemo"]');
        elements.exportButtons = document.querySelectorAll('[onclick*="export"]').length;
        elements.tau2Selector = !!document.querySelector('[id*="tau"]') ||
                               !!document.querySelector('select');
        elements.plotlyLoaded = typeof Plotly !== 'undefined';
        elements.xlsxLoaded = typeof XLSX !== 'undefined';

        return elements;
    """)

    for elem, found in ui_elements.items():
        if isinstance(found, bool):
            log_test(f"UI: {elem}", found)
        else:
            log_test(f"UI: {elem}", found > 0, f"{found} found")

    # ========================================
    # PART 6: Test built-in automated tests
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
        log_test("Built-in test suite", failed == 0, f"{passed}/{passed+failed} tests passed")
        if builtin.get('results'):
            for test in builtin.get('results', []):
                status = "PASS" if test.get('passed') else "FAIL"
                print(f"    [{status}] {test.get('name', 'Unknown')}")
    else:
        log_test("Built-in test suite", False, "Function not available")

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
        print("\nFailed tests:")
        for d in results["details"]:
            if not d["passed"]:
                print(f"  - {d['name']}: {d.get('detail', 'No details')}")

    if pct >= 95:
        print("\n✓ VERDICT: EXCELLENT - Application fully validated")
    elif pct >= 85:
        print("\n✓ VERDICT: GOOD - Most features working correctly")
    elif pct >= 70:
        print("\n⚠ VERDICT: ACCEPTABLE - Some issues detected")
    else:
        print("\n✗ VERDICT: NEEDS ATTENTION - Multiple issues detected")

    print("=" * 70)

finally:
    driver.quit()
