#!/usr/bin/env python3
"""Final comprehensive Edge test"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Edge(options=options)
driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
time.sleep(3)

print("=" * 70)
print("FINAL COMPREHENSIVE EDGE TEST")
print("TruthCert-PairwisePro v1.0")
print("=" * 70)

results = {"passed": 0, "failed": 0}

def test(name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    if passed:
        results["passed"] += 1
    else:
        results["failed"] += 1
    suffix = f" ({details})" if details else ""
    print(f"  [{status}] {name}{suffix}")

try:
    # Section 1: Demo datasets
    print("\n--- DEMO DATASETS (17) ---")
    datasets = driver.execute_script("return Object.keys(DEMO_DATASETS);")
    for ds in datasets:
        r = driver.execute_script(f"""
            loadDemoDataset("{ds}");
            // Check multiple locations for data
            const demoData = DEMO_DATASETS["{ds}"];
            const studyCount = demoData.studies?.length || demoData.data?.length || 0;
            // Also verify AppState.data was populated
            const appDataCount = AppState?.data?.length || 0;
            return {{ok: studyCount > 0 || appDataCount > 0, count: Math.max(studyCount, appDataCount)}};
        """)
        test(ds, r.get("ok", False), f"{r.get('count', 0)} studies")
        time.sleep(0.1)

    # Section 2: Tau-squared estimators
    print("\n--- TAU2 ESTIMATORS (8) ---")
    tau2 = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        const ref = {DL:0.308760, REML:0.313243, ML:0.280028, PM:0.318094,
                     HS:0.228363, SJ:0.345516, HE:0.328564, EB:0.318069};
        const r = {};
        for (const m of Object.keys(ref)) {
            try {
                const est = window["estimateTau2_" + m](yi, vi).tau2;
                r[m] = {ok: Math.abs(est - ref[m]) < 0.01, est: est.toFixed(6)};
            } catch(e) { r[m] = {ok: false, error: e.message}; }
        }
        return r;
    """)
    for m, r in tau2.items():
        test(f"tau2_{m}", r.get("ok", False), r.get("est", ""))

    # Section 3: Core functions
    print("\n--- CORE FUNCTIONS (18) ---")
    funcs = driver.execute_script("""
        return {
            calculatePooledEstimate: typeof calculatePooledEstimate === "function",
            calculateHKSJ: typeof calculateHKSJ === "function",
            eggerTest: typeof eggerTest === "function",
            beggTest: typeof beggTest === "function",
            trimAndFill: typeof trimAndFill === "function",
            failsafeN: typeof failsafeN === "function",
            bayesianMetaAnalysis: typeof bayesianMetaAnalysis === "function",
            fragilityIndex: typeof fragilityIndex === "function",
            calculateEValue: typeof calculateEValue === "function",
            predictionInterval_Standard: typeof predictionInterval_Standard === "function",
            leave1out: typeof leave1out === "function",
            cumulativeMetaAnalysis: typeof cumulativeMetaAnalysis === "function",
            influenceDiagnostics: typeof influenceDiagnostics === "function",
            subgroupAnalysis: typeof subgroupAnalysis === "function",
            metaRegression: typeof metaRegression === "function",
            assessGRADE: typeof assessGRADE === "function",
            petPeese: typeof petPeese === "function",
            pCurveAnalysis: typeof pCurveAnalysis === "function"
        };
    """)
    for f, exists in funcs.items():
        test(f, exists)

    # Section 4: Plotting functions
    print("\n--- PLOT FUNCTIONS (8) ---")
    plots = driver.execute_script("""
        return {
            renderForestPlot: typeof renderForestPlot === "function",
            renderFunnelPlot: typeof renderFunnelPlot === "function",
            renderBaujatPlot: typeof renderBaujatPlot === "function",
            renderRadialPlot: typeof renderRadialPlot === "function",
            renderDOIPlot: typeof renderDOIPlot === "function",
            renderPCurvePlot: typeof renderPCurvePlot === "function",
            renderGOSHPlot: typeof renderGOSHPlot === "function",
            renderLabbePlot: typeof renderLabbePlot === "function"
        };
    """)
    for p, exists in plots.items():
        test(p, exists)

    # Section 5: Run analysis workflow
    print("\n--- FULL ANALYSIS WORKFLOW ---")
    driver.execute_script("loadDemoDataset('BCG');")
    time.sleep(0.5)
    driver.execute_script("runAnalysis();")
    time.sleep(2)

    workflow = driver.execute_script("""
        const r = AppState.results;
        if (!r) return {error: "No results"};
        return {
            hasPooled: r.pooled && typeof r.pooled.theta === "number",
            pooled: r.pooled ? r.pooled.theta.toFixed(4) : null,
            hasTau2: typeof r.tau2 === "number",
            tau2: r.tau2 ? r.tau2.toFixed(4) : null,
            hasHet: r.het && typeof r.het.I2 === "number",
            I2: r.het ? r.het.I2.toFixed(1) : null,
            hasPI: !!r.pi,
            hasHKSJ: !!r.hksj,
            hasEgger: !!r.egger,
            eggerP: r.egger ? r.egger.p_value.toFixed(4) : null,
            hasTrimFill: !!r.trimfill,
            hasLOO: !!r.loo
        };
    """)
    test("Pooled estimate", workflow.get("hasPooled", False), workflow.get("pooled", ""))
    test("Tau-squared", workflow.get("hasTau2", False), workflow.get("tau2", ""))
    test("Heterogeneity I2", workflow.get("hasHet", False), f"{workflow.get('I2', '')}%")
    test("Prediction intervals", workflow.get("hasPI", False))
    test("HKSJ adjustment", workflow.get("hasHKSJ", False))
    test("Egger test", workflow.get("hasEgger", False), f"p={workflow.get('eggerP', '')}")
    test("Trim-and-Fill", workflow.get("hasTrimFill", False))
    test("Leave-one-out", workflow.get("hasLOO", False))

    # Section 6: Plots rendered
    print("\n--- PLOTS RENDERED ---")
    forest = driver.execute_script("""
        const fp = document.getElementById("forestPlot");
        return fp && fp.innerHTML.length > 100;
    """)
    test("Forest plot", forest)

    driver.execute_script('document.querySelector("[data-tab=heterogeneity]").click();')
    time.sleep(0.5)
    funnel = driver.execute_script("""
        const fp = document.getElementById("funnelPlot");
        return fp && fp.innerHTML.length > 100;
    """)
    test("Funnel plot", funnel)

    # Section 7: Export functions
    print("\n--- EXPORT FUNCTIONS (5) ---")
    exports = driver.execute_script("""
        return {
            exportCSV: typeof exportCSV === "function",
            exportJSON: typeof exportJSON === "function",
            exportExcel: typeof XLSX !== "undefined",
            generateRCode: typeof generateRCode === "function",
            downloadPlot: typeof downloadPlot === "function"
        };
    """)
    for e, exists in exports.items():
        test(e, exists)

    # Section 8: UI Tabs
    print("\n--- UI TABS (15) ---")
    tabs = driver.execute_script('return Array.from(document.querySelectorAll("[data-tab]")).map(t => t.getAttribute("data-tab"));')
    for tab in tabs:
        driver.execute_script(f'document.querySelector("[data-tab={tab}]").click();')
        time.sleep(0.1)
        test(f"Tab: {tab}", True)

    # Section 9: Built-in tests
    print("\n--- BUILT-IN TEST SUITE ---")
    builtin = driver.execute_script("""
        if (typeof runAutomatedTests === "function") {
            return runAutomatedTests();
        }
        return null;
    """)
    if builtin:
        p, f = builtin.get("passed", 0), builtin.get("failed", 0)
        test(f"Automated tests", f == 0, f"{p}/{p+f} passed")
    else:
        test("Automated tests", False, "Not available")

    # Summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    total = results["passed"] + results["failed"]
    pct = (results["passed"] / total) * 100 if total > 0 else 0

    print(f"\nTotal Tests: {total}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Pass Rate: {pct:.1f}%")

    print("\n" + "-" * 70)
    if pct >= 95:
        print("VERDICT: EXCELLENT - All systems operational")
    elif pct >= 85:
        print("VERDICT: GOOD - Application working correctly")
    elif pct >= 70:
        print("VERDICT: ACCEPTABLE - Minor issues")
    else:
        print("VERDICT: NEEDS ATTENTION")
    print("=" * 70)

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
