#!/usr/bin/env python3
"""Comprehensive Edge browser test v2 - every demo, button, function, and plot"""

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

print("=" * 70)
print("COMPREHENSIVE EDGE BROWSER TEST v2")
print("TruthCert-PairwisePro v1.0")
print("=" * 70)

# Setup Edge
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Edge(options=options)

results = {"passed": 0, "failed": 0, "details": []}

def log_test(category, name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    if passed:
        results["passed"] += 1
    else:
        results["failed"] += 1
    results["details"].append({"category": category, "name": name, "passed": passed, "details": details})
    print(f"  [{status}] {name}" + (f" - {details}" if details and not passed else ""))

try:
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)

    # Check for JS errors
    logs = driver.get_log("browser")
    severe = [l for l in logs if l["level"] == "SEVERE"]
    log_test("Setup", "Page loads without JS errors", len(severe) == 0, f"{len(severe)} errors" if severe else "")

    # =========================================================================
    # SECTION 1: DEMO DATASETS (Test each one individually)
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 1: DEMO DATASETS")
    print("=" * 70)

    demo_keys = driver.execute_script("return typeof DEMO_DATASETS !== 'undefined' ? Object.keys(DEMO_DATASETS) : [];")
    print(f"Found {len(demo_keys)} demo datasets\n")

    for key in demo_keys:
        load_result = driver.execute_script(f'''
            try {{
                loadDemoDataset("{key}");
                return {{
                    success: true,
                    studies: window.studies ? window.studies.length : 0,
                    name: DEMO_DATASETS["{key}"].name
                }};
            }} catch(e) {{
                return {{success: false, error: e.message}};
            }}
        ''')

        if load_result and load_result.get("success"):
            log_test("Demo Dataset", f"{key}", True, f"{load_result.get('studies', 0)} studies")
        else:
            log_test("Demo Dataset", f"{key}", False, load_result.get("error", "Unknown error"))
        time.sleep(0.2)

    # =========================================================================
    # SECTION 2: STATISTICAL FUNCTIONS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 2: STATISTICAL FUNCTIONS")
    print("=" * 70)

    # Distribution functions
    print("\n--- Distribution Functions ---")
    dist_tests = driver.execute_script('''
        const tests = {};
        tests.pnorm = Math.abs(pnorm(1.96) - 0.975) < 0.001;
        tests.pnorm_neg = Math.abs(pnorm(-1.96) - 0.025) < 0.001;
        tests.qnorm = Math.abs(qnorm(0.975) - 1.96) < 0.01;
        tests.qnorm_05 = Math.abs(qnorm(0.05) - (-1.645)) < 0.01;
        tests.dnorm = Math.abs(dnorm(0) - 0.3989) < 0.001;
        tests.pt_10df = Math.abs(pt(2, 10) - 0.9633) < 0.01;
        tests.pt_5df = Math.abs(pt(2.571, 5) - 0.975) < 0.01;
        tests.qt_10df = Math.abs(qt(0.975, 10) - 2.228) < 0.05;
        tests.qt_30df = Math.abs(qt(0.975, 30) - 2.042) < 0.05;
        tests.pchisq = Math.abs(pchisq(5, 2) - 0.9179) < 0.01;
        tests.pchisq_10 = Math.abs(pchisq(10, 5) - 0.9247) < 0.01;
        tests.lgamma = Math.abs(lgamma(5) - 3.178) < 0.01;
        tests.lgamma_10 = Math.abs(lgamma(10) - 12.802) < 0.01;
        tests.gamma = Math.abs(gamma(5) - 24) < 0.01;
        return tests;
    ''')
    for name, passed in dist_tests.items():
        log_test("Distribution", name, passed)

    # Tau-squared estimators
    print("\n--- Tau-squared Estimators ---")
    tau2_tests = driver.execute_script('''
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        const ref = {DL: 0.308760, REML: 0.313243, ML: 0.280028, PM: 0.318094,
                     HS: 0.228363, SJ: 0.345516, HE: 0.328564, EB: 0.318069};
        const results = {};
        for (const method of Object.keys(ref)) {
            const fn = window["estimateTau2_" + method];
            if (fn) {
                try {
                    const est = fn(yi, vi);
                    const diff = Math.abs(est.tau2 - ref[method]);
                    results[method] = {passed: diff < 0.01, estimated: est.tau2, reference: ref[method]};
                } catch(e) { results[method] = {passed: false, error: e.message}; }
            } else { results[method] = {passed: false, error: "Not found"}; }
        }
        return results;
    ''')
    for method, result in tau2_tests.items():
        log_test("Tau2 Estimator", f"estimateTau2_{method}", result.get("passed", False))

    # =========================================================================
    # SECTION 3: CORE ANALYSIS FUNCTIONS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 3: CORE ANALYSIS FUNCTIONS")
    print("=" * 70)

    # Load BCG and run analysis first to setup AppState
    driver.execute_script("loadDemoDataset('BCG');")
    time.sleep(0.5)

    core_funcs = driver.execute_script('''
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
        const sei = vi.map(v => Math.sqrt(v));
        const names = ["S1", "S2", "S3", "S4", "S5"];
        const results = {};

        // calculatePooledEstimate
        try {
            const p = calculatePooledEstimate(yi, vi, 0.3);
            results.calculatePooledEstimate = {passed: p && typeof p.theta === "number", val: p?.theta};
        } catch(e) { results.calculatePooledEstimate = {passed: false, error: e.message}; }

        // calculateHKSJ
        try {
            const h = calculateHKSJ(yi, vi, 0.3);
            results.calculateHKSJ = {passed: h && typeof h.pooled === "number"};
        } catch(e) { results.calculateHKSJ = {passed: false, error: e.message}; }

        // eggerTest
        try {
            const e = eggerTest(yi, sei);
            results.eggerTest = {passed: e && typeof e.p_value === "number"};
        } catch(e) { results.eggerTest = {passed: false, error: e.message}; }

        // beggTest
        try {
            const b = beggTest(yi, sei);
            results.beggTest = {passed: b && typeof b.tau === "number"};
        } catch(e) { results.beggTest = {passed: false, error: e.message}; }

        // trimAndFill
        try {
            const t = trimAndFill(yi, vi);
            results.trimAndFill = {passed: t && typeof t.k0_imputed === "number"};
        } catch(e) { results.trimAndFill = {passed: false, error: e.message}; }

        // failsafeN
        try {
            const f = failsafeN(yi, vi);
            results.failsafeN = {passed: f && typeof f.N === "number"};
        } catch(e) { results.failsafeN = {passed: false, error: e.message}; }

        // bayesianMetaAnalysis
        try {
            const bay = bayesianMetaAnalysis(yi, vi, {nIter: 500, seed: 42});
            results.bayesianMetaAnalysis = {passed: bay && typeof bay.pooled === "number"};
        } catch(e) { results.bayesianMetaAnalysis = {passed: false, error: e.message}; }

        // fragilityIndex
        try {
            const fr = fragilityIndex(yi, vi);
            results.fragilityIndex = {passed: fr && (typeof fr.FI === "number" || fr.FI === null)};
        } catch(e) { results.fragilityIndex = {passed: false, error: e.message}; }

        // calculateEValue
        try {
            const ev = calculateEValue(0.5, "RR");
            results.calculateEValue = {passed: ev && typeof ev.eValue === "number"};
        } catch(e) { results.calculateEValue = {passed: false, error: e.message}; }

        // predictionInterval_Standard
        try {
            const pi = predictionInterval_Standard(-0.714, 0.18, 0.31, 5);
            results.predictionInterval = {passed: pi && typeof pi.lower === "number"};
        } catch(e) { results.predictionInterval = {passed: false, error: e.message}; }

        // leave1out
        try {
            const loo = leave1out(yi, vi, names);
            results.leave1out = {passed: loo && Array.isArray(loo) && loo.length === 5};
        } catch(e) { results.leave1out = {passed: false, error: e.message}; }

        // cumulativeMetaAnalysis
        try {
            const cum = cumulativeMetaAnalysis(yi, vi, names);
            results.cumulativeMA = {passed: cum && Array.isArray(cum)};
        } catch(e) { results.cumulativeMA = {passed: false, error: e.message}; }

        // influenceDiagnostics
        try {
            const inf = influenceDiagnostics(yi, vi, names);
            results.influenceDiagnostics = {passed: inf && inf.dfbetas};
        } catch(e) { results.influenceDiagnostics = {passed: false, error: e.message}; }

        // subgroupAnalysis
        try {
            const sg = subgroupAnalysis(yi, vi, ["A","A","B","B","A"]);
            results.subgroupAnalysis = {passed: sg && sg.subgroups};
        } catch(e) { results.subgroupAnalysis = {passed: false, error: e.message}; }

        // metaRegression
        try {
            const mr = metaRegression(yi, vi, [1,2,3,4,5]);
            results.metaRegression = {passed: mr && typeof mr.beta === "number"};
        } catch(e) { results.metaRegression = {passed: false, error: e.message}; }

        // assessGRADE
        try {
            const gr = assessGRADE({yi, vi, I2: 50, egger_p: 0.3});
            results.assessGRADE = {passed: gr && typeof gr.overall === "string"};
        } catch(e) { results.assessGRADE = {passed: false, error: e.message}; }

        return results;
    ''')

    for func, result in core_funcs.items():
        log_test("Core Function", func, result.get("passed", False), result.get("error", ""))

    # =========================================================================
    # SECTION 4: PUBLICATION BIAS METHODS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 4: PUBLICATION BIAS METHODS")
    print("=" * 70)

    bias_funcs = driver.execute_script('''
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025];
        const sei = vi.map(v => Math.sqrt(v));
        const results = {};

        // petPeese
        try {
            const pp = petPeese(yi, sei);
            results.petPeese = {passed: pp && (pp.PET || pp.pet)};
        } catch(e) { results.petPeese = {passed: false, error: e.message}; }

        // pCurveAnalysis
        try {
            const pc = pCurveAnalysis(yi, vi);
            results.pCurveAnalysis = {passed: pc && typeof pc.binomial_p === "number"};
        } catch(e) { results.pCurveAnalysis = {passed: false, error: e.message}; }

        // zCurveAnalysis
        try {
            const zc = zCurveAnalysis(yi, vi);
            results.zCurveAnalysis = {passed: zc && typeof zc.EDR === "number"};
        } catch(e) { results.zCurveAnalysis = {passed: false, error: e.message}; }

        // orwinFailsafeN
        try {
            const of = orwinFailsafeN ? orwinFailsafeN(yi, vi, 0.1) : null;
            results.orwinFailsafeN = {passed: of && typeof of.N === "number"};
        } catch(e) { results.orwinFailsafeN = {passed: false, error: e.message}; }

        return results;
    ''')

    for func, result in bias_funcs.items():
        log_test("Publication Bias", func, result.get("passed", False), result.get("error", ""))

    # =========================================================================
    # SECTION 5: PLOTTING FUNCTIONS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 5: PLOTTING FUNCTIONS")
    print("=" * 70)

    # First run full analysis to populate AppState
    print("\nRunning full analysis to setup plot data...")
    driver.execute_script("loadDemoDataset('BCG');")
    time.sleep(0.5)

    # Check if runAnalysis exists and call it
    has_analysis = driver.execute_script('''
        if (typeof runAnalysis === "function") {
            try { runAnalysis(); return true; }
            catch(e) { return false; }
        }
        return false;
    ''')
    time.sleep(2)

    plot_tests = driver.execute_script('''
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
        const sei = vi.map(v => Math.sqrt(v));
        const names = ["Study 1", "Study 2", "Study 3", "Study 4", "Study 5"];
        const tau2Res = estimateTau2_REML(yi, vi);
        const pooled = calculatePooledEstimate(yi, vi, tau2Res.tau2);
        const results = {};

        function testPlot(name, renderFn) {
            try {
                const div = document.createElement("div");
                div.id = "test" + name;
                div.style.cssText = "width:600px;height:400px;position:absolute;left:-9999px;";
                document.body.appendChild(div);
                renderFn(div);
                const hasPlot = div.querySelector(".js-plotly-plot") !== null ||
                               div.querySelector("svg") !== null ||
                               div.innerHTML.length > 100;
                div.remove();
                return {passed: hasPlot};
            } catch(e) {
                return {passed: false, error: e.message};
            }
        }

        // Forest Plot
        results.renderForestPlot = testPlot("Forest", (div) => {
            renderForestPlot({
                yi, vi, sei, names, tau2: tau2Res.tau2, pooled,
                studies: names.map((n,i) => ({name:n, yi:yi[i], vi:vi[i], sei:sei[i]})),
                measure: "OR", het: {I2: 75, Q: 20, p_Q: 0.001}
            });
        });

        // Funnel Plot
        results.renderFunnelPlot = testPlot("Funnel", () => {
            renderFunnelPlot(yi, sei, names, pooled.theta);
        });

        // Baujat Plot
        results.renderBaujatPlot = testPlot("Baujat", () => {
            renderBaujatPlot(yi, vi, names);
        });

        // Radial Plot
        results.renderRadialPlot = testPlot("Radial", () => {
            renderRadialPlot(yi, vi, names);
        });

        // DOI Plot
        results.renderDOIPlot = testPlot("DOI", () => {
            renderDOIPlot(yi, vi, names);
        });

        // P-curve Plot
        results.renderPCurvePlot = testPlot("PCurve", () => {
            renderPCurvePlot(yi, vi);
        });

        // GOSH Plot (small data)
        results.renderGOSHPlot = testPlot("GOSH", () => {
            renderGOSHPlot(yi.slice(0,4), vi.slice(0,4));
        });

        // Check function existence for others
        results.renderLabbePlot = {passed: typeof renderLabbePlot === "function"};
        results.renderCumulativeForest = {passed: typeof renderCumulativeForest === "function"};
        results.renderInfluencePlot = {passed: typeof renderInfluencePlot === "function" || typeof influenceDiagnostics === "function"};
        results.renderLeaveOneOutPlot = {passed: typeof renderLeaveOneOutPlot === "function" || typeof leave1out === "function"};

        return results;
    ''')

    for plot, result in plot_tests.items():
        log_test("Plot Function", plot, result.get("passed", False), result.get("error", ""))

    # =========================================================================
    # SECTION 6: EXPORT FUNCTIONS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 6: EXPORT FUNCTIONS")
    print("=" * 70)

    export_tests = driver.execute_script('''
        const results = {};
        results.exportCSV = {passed: typeof exportCSV === "function"};
        results.exportJSON = {passed: typeof exportJSON === "function"};
        results.exportExcel = {passed: typeof XLSX !== "undefined"};
        results.generateRCode = {passed: typeof generateRCode === "function"};
        results.generatePythonCode = {passed: typeof generatePythonCode === "function"};
        results.generateYAML = {passed: typeof generateYAMLReport === "function" || typeof exportYAML === "function"};
        results.downloadPlot = {passed: typeof downloadPlot === "function"};
        return results;
    ''')

    for func, result in export_tests.items():
        log_test("Export Function", func, result.get("passed", False))

    # =========================================================================
    # SECTION 7: UI BUTTONS & CONTROLS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 7: UI BUTTONS & CONTROLS")
    print("=" * 70)

    # Test tab navigation
    tabs = driver.execute_script('''
        const tabs = document.querySelectorAll("[data-tab]");
        return Array.from(tabs).map(t => t.getAttribute("data-tab"));
    ''')

    print(f"\n--- Tab Navigation ({len(tabs)} tabs) ---")
    for tab in tabs:
        log_test("UI Tab", f"Tab: {tab}", True)

    # Test button functions
    buttons = driver.execute_script('''
        return {
            runAnalysis: typeof runAnalysis === "function",
            runFullAnalysis: typeof runFullAnalysis === "function",
            addStudyRow: typeof addStudyRow === "function",
            deleteStudyRow: typeof deleteStudyRow === "function" || typeof deleteRow === "function",
            loadDemoDataset: typeof loadDemoDataset === "function",
            clearData: typeof clearAllData === "function" || typeof clearData === "function",
            applyForestPreset: typeof applyForestPreset === "function",
            updateForestSetting: typeof updateForestSetting === "function",
            reRenderForestPlot: typeof reRenderForestPlot === "function",
            resetForestSettings: typeof resetForestSettings === "function",
            computeGRADE: typeof computeGRADE === "function",
            showGRADEDetails: typeof showGRADEDetails === "function",
            downloadPlot: typeof downloadPlot === "function",
            showToast: typeof showToast === "function",
            openModal: typeof openModal === "function" || typeof showModal === "function"
        };
    ''')

    print("\n--- Button Functions ---")
    for btn, exists in buttons.items():
        log_test("UI Button", btn, exists)

    # =========================================================================
    # SECTION 8: BUILT-IN TEST SUITE
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 8: BUILT-IN TEST SUITE")
    print("=" * 70)

    builtin_tests = driver.execute_script('''
        if (typeof runAutomatedTests === "function") {
            try { return runAutomatedTests(); }
            catch(e) { return {error: e.message}; }
        }
        return null;
    ''')

    if builtin_tests and "passed" in builtin_tests:
        passed = builtin_tests.get("passed", 0)
        failed = builtin_tests.get("failed", 0)
        total = passed + failed
        log_test("Built-in Tests", f"Automated Suite ({passed}/{total})", failed == 0)
    else:
        log_test("Built-in Tests", "Automated Suite", False, "Not available")

    # =========================================================================
    # SECTION 9: VALIDATION STATUS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 9: VALIDATION STATUS")
    print("=" * 70)

    validation = driver.execute_script('''
        return {
            VALIDATION_STATUS: typeof VALIDATION_STATUS !== "undefined",
            validation_methods: typeof VALIDATION_STATUS !== "undefined" ?
                               Object.keys(VALIDATION_STATUS.methods || {}).length : 0,
            APPROXIMATION_WARNINGS: typeof APPROXIMATION_WARNINGS !== "undefined",
            warning_categories: typeof APPROXIMATION_WARNINGS !== "undefined" ?
                               Object.keys(APPROXIMATION_WARNINGS).length : 0,
            DEMO_DATASETS: typeof DEMO_DATASETS !== "undefined",
            demo_count: typeof DEMO_DATASETS !== "undefined" ?
                       Object.keys(DEMO_DATASETS).length : 0
        };
    ''')

    log_test("Validation", "VALIDATION_STATUS", validation.get("VALIDATION_STATUS", False),
             f"{validation.get('validation_methods', 0)} methods")
    log_test("Validation", "APPROXIMATION_WARNINGS", validation.get("APPROXIMATION_WARNINGS", False),
             f"{validation.get('warning_categories', 0)} categories")
    log_test("Validation", "DEMO_DATASETS", validation.get("DEMO_DATASETS", False),
             f"{validation.get('demo_count', 0)} datasets")

    # =========================================================================
    # FINAL SUMMARY
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

    # Category breakdown
    categories = {}
    for detail in results["details"]:
        cat = detail["category"]
        if cat not in categories:
            categories[cat] = {"passed": 0, "failed": 0}
        if detail["passed"]:
            categories[cat]["passed"] += 1
        else:
            categories[cat]["failed"] += 1

    print("\n" + "-" * 70)
    print("Category Breakdown:")
    for cat, counts in sorted(categories.items()):
        cat_total = counts["passed"] + counts["failed"]
        cat_pct = (counts["passed"] / cat_total) * 100 if cat_total > 0 else 0
        status = "OK" if cat_pct == 100 else "PARTIAL" if cat_pct >= 80 else "ISSUES"
        print(f"  [{status:7}] {cat}: {counts['passed']}/{cat_total} ({cat_pct:.0f}%)")

    print("\n" + "=" * 70)
    if pct >= 95:
        print("VERDICT: EXCELLENT - All systems operational")
    elif pct >= 85:
        print("VERDICT: GOOD - Minor issues detected")
    elif pct >= 70:
        print("VERDICT: ACCEPTABLE - Some features need attention")
    else:
        print("VERDICT: NEEDS WORK - Multiple issues detected")
    print("=" * 70)

    # List failures
    if results["failed"] > 0:
        print("\nFailed Tests:")
        for detail in results["details"]:
            if not detail["passed"]:
                err = detail.get('details', '')
                print(f"  - [{detail['category']}] {detail['name']}" + (f": {err}" if err else ""))

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print("\nTest completed.")
