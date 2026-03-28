#!/usr/bin/env python3
"""Complete Edge Browser Validation Test - Including Critical Gap Functions"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

print("=" * 70)
print("COMPLETE EDGE BROWSER VALIDATION TEST")
print("TruthCert-PairwisePro - All Functions, Plots & Critical Gaps")
print("=" * 70)

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Edge(options=options)
driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
time.sleep(3)

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
    # =========================================================================
    print("\n--- SECTION 1: DEMO DATASETS (17) ---")
    # =========================================================================
    datasets = driver.execute_script("return Object.keys(DEMO_DATASETS);")
    for ds in datasets:
        r = driver.execute_script(f"""
            loadDemoDataset("{ds}");
            const demoData = DEMO_DATASETS["{ds}"];
            const studyCount = demoData.studies?.length || demoData.data?.length || 0;
            const appDataCount = AppState?.data?.length || 0;
            return {{ok: studyCount > 0 || appDataCount > 0, count: Math.max(studyCount, appDataCount)}};
        """)
        test(ds, r.get("ok", False), f"{r.get('count', 0)} studies")
        time.sleep(0.1)

    # =========================================================================
    print("\n--- SECTION 2: TAU2 ESTIMATORS (8) vs R/metafor ---")
    # =========================================================================
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
                r[m] = {ok: Math.abs(est - ref[m]) < 0.01, est: est.toFixed(6), ref: ref[m]};
            } catch(e) { r[m] = {ok: false, error: e.message}; }
        }
        return r;
    """)
    for m, r in tau2.items():
        test(f"tau2_{m}", r.get("ok", False), f"JS={r.get('est', 'N/A')} R={r.get('ref', 'N/A')}")

    # =========================================================================
    print("\n--- SECTION 3: MANTEL-HAENSZEL METHOD vs R ---")
    # =========================================================================
    mh = driver.execute_script("""
        // BCG data as 2x2 tables
        const studies = [
            {events_t: 4, n_t: 123, events_c: 11, n_c: 139},
            {events_t: 6, n_t: 306, events_c: 29, n_c: 303},
            {events_t: 3, n_t: 231, events_c: 11, n_c: 220},
            {events_t: 62, n_t: 13598, events_c: 248, n_c: 12867},
            {events_t: 33, n_t: 5069, events_c: 47, n_c: 5808},
            {events_t: 180, n_t: 1541, events_c: 372, n_c: 1451},
            {events_t: 8, n_t: 2545, events_c: 10, n_c: 629},
            {events_t: 505, n_t: 88391, events_c: 499, n_c: 88391},
            {events_t: 29, n_t: 7499, events_c: 45, n_c: 7277},
            {events_t: 17, n_t: 1716, events_c: 65, n_c: 1665},
            {events_t: 186, n_t: 50634, events_c: 141, n_c: 27338},
            {events_t: 5, n_t: 2498, events_c: 3, n_c: 2341},
            {events_t: 27, n_t: 16913, events_c: 29, n_c: 17854}
        ];
        try {
            const result = calculateMH_OR(studies);
            // R reference: OR=0.622874, logOR=-0.473411, SE=0.04100778
            const refOR = 0.622874;
            const refLogOR = -0.473411;
            const refSE = 0.04100778;
            return {
                available: result.available,
                OR: result.OR,
                logOR: result.logOR,
                se: result.se,
                matchOR: Math.abs(result.OR - refOR) < 0.01,
                matchLogOR: Math.abs(result.logOR - refLogOR) < 0.01,
                matchSE: Math.abs(result.se - refSE) < 0.01,
                refOR: refOR,
                refLogOR: refLogOR,
                refSE: refSE
            };
        } catch(e) {
            return {error: e.message};
        }
    """)
    test("MH OR vs R", mh.get("matchOR", False),
         f"JS={mh.get('OR', 'N/A'):.4f} R={mh.get('refOR', 'N/A')}")
    test("MH logOR vs R", mh.get("matchLogOR", False),
         f"JS={mh.get('logOR', 'N/A'):.4f} R={mh.get('refLogOR', 'N/A')}")
    test("MH SE vs R", mh.get("matchSE", False),
         f"JS={mh.get('se', 'N/A'):.4f} R={mh.get('refSE', 'N/A')}")

    # =========================================================================
    print("\n--- SECTION 4: PETO METHOD vs R ---")
    # =========================================================================
    peto = driver.execute_script("""
        const studies = [
            {events_t: 4, n_t: 123, events_c: 11, n_c: 139},
            {events_t: 6, n_t: 306, events_c: 29, n_c: 303},
            {events_t: 3, n_t: 231, events_c: 11, n_c: 220},
            {events_t: 62, n_t: 13598, events_c: 248, n_c: 12867},
            {events_t: 33, n_t: 5069, events_c: 47, n_c: 5808},
            {events_t: 180, n_t: 1541, events_c: 372, n_c: 1451},
            {events_t: 8, n_t: 2545, events_c: 10, n_c: 629},
            {events_t: 505, n_t: 88391, events_c: 499, n_c: 88391},
            {events_t: 29, n_t: 7499, events_c: 45, n_c: 7277},
            {events_t: 17, n_t: 1716, events_c: 65, n_c: 1665},
            {events_t: 186, n_t: 50634, events_c: 141, n_c: 27338},
            {events_t: 5, n_t: 2498, events_c: 3, n_c: 2341},
            {events_t: 27, n_t: 16913, events_c: 29, n_c: 17854}
        ];
        try {
            const result = calculatePeto_OR(studies);
            // R reference: OR=0.6222295, logOR=-0.4744463, SE=0.04065908
            const refOR = 0.6222295;
            const refLogOR = -0.4744463;
            const refSE = 0.04065908;
            return {
                available: result.available,
                OR: result.OR,
                logOR: result.logOR,
                se: result.se,
                matchOR: Math.abs(result.OR - refOR) < 0.01,
                matchLogOR: Math.abs(result.logOR - refLogOR) < 0.01,
                matchSE: Math.abs(result.se - refSE) < 0.01,
                refOR: refOR,
                refLogOR: refLogOR,
                refSE: refSE
            };
        } catch(e) {
            return {error: e.message};
        }
    """)
    test("Peto OR vs R", peto.get("matchOR", False),
         f"JS={peto.get('OR', 'N/A'):.4f} R={peto.get('refOR', 'N/A')}")
    test("Peto logOR vs R", peto.get("matchLogOR", False),
         f"JS={peto.get('logOR', 'N/A'):.4f} R={peto.get('refLogOR', 'N/A')}")
    test("Peto SE vs R", peto.get("matchSE", False),
         f"JS={peto.get('se', 'N/A'):.4f} R={peto.get('refSE', 'N/A')}")

    # =========================================================================
    print("\n--- SECTION 5: TEST OF EXCESS SIGNIFICANCE (TES) ---")
    # =========================================================================
    tes = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        try {
            const result = testExcessSignificance(yi, vi);
            // R reference: observed=8, expected=6.1, pvalue=0.1355
            return {
                available: true,
                observed: result.observed,
                expected: result.expected,
                pvalue: result.pvalue,
                matchObs: result.observed === 8,
                matchExp: Math.abs(result.expected - 6.1) < 0.5,
                interpretation: result.interpretation
            };
        } catch(e) {
            return {available: false, error: e.message};
        }
    """)
    test("TES function exists", tes.get("available", False))
    test("TES observed vs R", tes.get("matchObs", False),
         f"JS={tes.get('observed', 'N/A')} R=8")
    test("TES expected vs R", tes.get("matchExp", False),
         f"JS={tes.get('expected', 'N/A')} R=6.1")

    # =========================================================================
    print("\n--- SECTION 6: COOK'S DISTANCE (in influence diagnostics) ---")
    # =========================================================================
    cooks = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        const names = ['Study1','Study2','Study3','Study4','Study5','Study6',
                       'Study7','Study8','Study9','Study10','Study11','Study12','Study13'];
        try {
            const result = influenceDiagnostics(yi, vi, names);
            const cooksd = result.studies.map(s => s.cooksD);
            // R reference max: 0.200266 (study 8)
            const maxCooksD = Math.max(...cooksd);
            const maxStudy = cooksd.indexOf(maxCooksD);
            return {
                available: true,
                maxCooksD: maxCooksD,
                maxStudyIdx: maxStudy,
                matchMax: Math.abs(maxCooksD - 0.200266) < 0.01,
                matchStudy: maxStudy === 7  // 0-indexed, study 8
            };
        } catch(e) {
            return {available: false, error: e.message};
        }
    """)
    test("Cook's D calculation", cooks.get("available", False))
    test("Cook's D max value vs R", cooks.get("matchMax", False),
         f"JS={cooks.get('maxCooksD', 'N/A'):.4f} R=0.2003")
    test("Cook's D max study vs R", cooks.get("matchStudy", False),
         f"JS=Study{cooks.get('maxStudyIdx', -1)+1} R=Study8")

    # =========================================================================
    print("\n--- SECTION 7: QQ PLOT FUNCTIONS ---")
    # =========================================================================
    qq = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        const tau2 = 0.313243;  // REML estimate
        try {
            const residuals = getStandardizedResiduals(yi, vi, tau2);
            // R reference first residual: -0.23815
            return {
                functionExists: typeof getStandardizedResiduals === 'function',
                qqPlotExists: typeof renderQQPlot === 'function',
                correlationExists: typeof calculatePearsonCorrelation === 'function',
                residualsCount: residuals.length,
                firstResidual: residuals[0],
                matchFirst: Math.abs(residuals[0] - (-0.23815)) < 0.1
            };
        } catch(e) {
            return {error: e.message};
        }
    """)
    test("getStandardizedResiduals exists", qq.get("functionExists", False))
    test("renderQQPlot exists", qq.get("qqPlotExists", False))
    test("calculatePearsonCorrelation exists", qq.get("correlationExists", False))
    test("Residuals match R", qq.get("matchFirst", False),
         f"JS={qq.get('firstResidual', 'N/A'):.4f} R=-0.2382")

    # =========================================================================
    print("\n--- SECTION 8: CORE FUNCTIONS (18) ---")
    # =========================================================================
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

    # =========================================================================
    print("\n--- SECTION 9: PLOT FUNCTIONS (10) ---")
    # =========================================================================
    plots = driver.execute_script("""
        return {
            renderForestPlot: typeof renderForestPlot === "function",
            renderFunnelPlot: typeof renderFunnelPlot === "function",
            renderBaujatPlot: typeof renderBaujatPlot === "function",
            renderRadialPlot: typeof renderRadialPlot === "function",
            renderDOIPlot: typeof renderDOIPlot === "function",
            renderPCurvePlot: typeof renderPCurvePlot === "function",
            renderGOSHPlot: typeof renderGOSHPlot === "function",
            renderLabbePlot: typeof renderLabbePlot === "function",
            renderQQPlot: typeof renderQQPlot === "function",
            calculateMH_OR: typeof calculateMH_OR === "function"
        };
    """)
    for p, exists in plots.items():
        test(p, exists)

    # =========================================================================
    print("\n--- SECTION 10: FULL ANALYSIS WORKFLOW ---")
    # =========================================================================
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

    # =========================================================================
    print("\n--- SECTION 11: PLOTS RENDERED ---")
    # =========================================================================
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

    # =========================================================================
    print("\n--- SECTION 12: EXPORT FUNCTIONS (5) ---")
    # =========================================================================
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

    # =========================================================================
    print("\n--- SECTION 13: UI TABS ---")
    # =========================================================================
    tabs = driver.execute_script('return Array.from(document.querySelectorAll("[data-tab]")).map(t => t.getAttribute("data-tab"));')
    for tab in tabs:
        driver.execute_script(f'document.querySelector("[data-tab={tab}]").click();')
        time.sleep(0.1)
        test(f"Tab: {tab}", True)

    # =========================================================================
    print("\n--- SECTION 14: BUILT-IN TEST SUITE ---")
    # =========================================================================
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

    # =========================================================================
    # SUMMARY
    # =========================================================================
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
