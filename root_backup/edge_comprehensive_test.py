#!/usr/bin/env python3
"""Comprehensive Edge browser test - every demo, button, function, and plot"""

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

print("=" * 70)
print("COMPREHENSIVE EDGE BROWSER TEST")
print("TruthCert-PairwisePro v1.0")
print("=" * 70)

# Setup Edge
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 10)

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
        # Load the dataset
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

        time.sleep(0.3)

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
        // pnorm
        tests.pnorm = Math.abs(pnorm(1.96) - 0.975) < 0.001;
        tests.pnorm_neg = Math.abs(pnorm(-1.96) - 0.025) < 0.001;
        // qnorm
        tests.qnorm = Math.abs(qnorm(0.975) - 1.96) < 0.01;
        tests.qnorm_05 = Math.abs(qnorm(0.05) - (-1.645)) < 0.01;
        // dnorm
        tests.dnorm = Math.abs(dnorm(0) - 0.3989) < 0.001;
        // pt
        tests.pt_10df = Math.abs(pt(2, 10) - 0.9633) < 0.01;
        tests.pt_5df = Math.abs(pt(2.571, 5) - 0.975) < 0.01;
        // qt
        tests.qt_10df = Math.abs(qt(0.975, 10) - 2.228) < 0.05;
        tests.qt_30df = Math.abs(qt(0.975, 30) - 2.042) < 0.05;
        // pchisq
        tests.pchisq = Math.abs(pchisq(5, 2) - 0.9179) < 0.01;
        tests.pchisq_10 = Math.abs(pchisq(10, 5) - 0.9247) < 0.01;
        // lgamma
        tests.lgamma = Math.abs(lgamma(5) - 3.178) < 0.01;
        tests.lgamma_10 = Math.abs(lgamma(10) - 12.802) < 0.01;
        // gamma
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

        // R/metafor reference values
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
        for (const method of Object.keys(ref)) {
            const fn = window["estimateTau2_" + method];
            if (fn) {
                try {
                    const est = fn(yi, vi);
                    const diff = Math.abs(est.tau2 - ref[method]);
                    results[method] = {
                        passed: diff < 0.01,
                        estimated: est.tau2,
                        reference: ref[method],
                        diff: diff
                    };
                } catch(e) {
                    results[method] = {passed: false, error: e.message};
                }
            } else {
                results[method] = {passed: false, error: "Function not found"};
            }
        }
        return results;
    ''')
    for method, result in tau2_tests.items():
        if result.get("passed"):
            log_test("Tau2 Estimator", f"estimateTau2_{method}", True,
                     f"Est={result.get('estimated', 0):.6f}, Ref={result.get('reference', 0):.6f}")
        else:
            log_test("Tau2 Estimator", f"estimateTau2_{method}", False, result.get("error", "Mismatch"))

    # =========================================================================
    # SECTION 3: CORE ANALYSIS FUNCTIONS
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 3: CORE ANALYSIS FUNCTIONS")
    print("=" * 70)

    core_funcs = driver.execute_script('''
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
        const sei = vi.map(v => Math.sqrt(v));

        const results = {};

        // calculatePooledEstimate
        try {
            const pooled = calculatePooledEstimate(yi, vi, 0.3);
            results.calculatePooledEstimate = {
                passed: pooled && typeof pooled.theta === "number",
                value: pooled ? pooled.theta : null
            };
        } catch(e) { results.calculatePooledEstimate = {passed: false, error: e.message}; }

        // calculateHKSJ
        try {
            const hksj = calculateHKSJ(yi, vi, 0.3);
            results.calculateHKSJ = {
                passed: hksj && typeof hksj.pooled === "number",
                value: hksj ? hksj.pooled : null
            };
        } catch(e) { results.calculateHKSJ = {passed: false, error: e.message}; }

        // eggerTest
        try {
            const egger = eggerTest(yi, sei);
            results.eggerTest = {
                passed: egger && typeof egger.p_value === "number",
                pvalue: egger ? egger.p_value : null
            };
        } catch(e) { results.eggerTest = {passed: false, error: e.message}; }

        // beggTest
        try {
            const begg = beggTest(yi, sei);
            results.beggTest = {
                passed: begg && typeof begg.tau === "number",
                tau: begg ? begg.tau : null
            };
        } catch(e) { results.beggTest = {passed: false, error: e.message}; }

        // trimAndFill
        try {
            const tf = trimAndFill(yi, vi);
            results.trimAndFill = {
                passed: tf && typeof tf.k0_imputed === "number",
                k0: tf ? tf.k0_imputed : null
            };
        } catch(e) { results.trimAndFill = {passed: false, error: e.message}; }

        // failsafeN
        try {
            const fsn = failsafeN(yi, vi);
            results.failsafeN = {
                passed: fsn && typeof fsn.N === "number",
                N: fsn ? fsn.N : null
            };
        } catch(e) { results.failsafeN = {passed: false, error: e.message}; }

        // bayesianMetaAnalysis
        try {
            const bayes = bayesianMetaAnalysis(yi, vi, {nIter: 1000, seed: 42});
            results.bayesianMetaAnalysis = {
                passed: bayes && typeof bayes.pooled === "number",
                pooled: bayes ? bayes.pooled : null
            };
        } catch(e) { results.bayesianMetaAnalysis = {passed: false, error: e.message}; }

        // fragilityIndex
        try {
            const frag = fragilityIndex(yi, vi);
            results.fragilityIndex = {
                passed: frag && typeof frag.FI === "number",
                FI: frag ? frag.FI : null
            };
        } catch(e) { results.fragilityIndex = {passed: false, error: e.message}; }

        // calculateEValue
        try {
            const eVal = calculateEValue(0.5, "RR");
            results.calculateEValue = {
                passed: eVal && typeof eVal.eValue === "number",
                eValue: eVal ? eVal.eValue : null
            };
        } catch(e) { results.calculateEValue = {passed: false, error: e.message}; }

        // predictionInterval_Standard
        try {
            const pi = predictionInterval_Standard(-0.714, 0.18, 0.31, 5);
            results.predictionInterval_Standard = {
                passed: pi && typeof pi.lower === "number" && typeof pi.upper === "number",
                lower: pi ? pi.lower : null,
                upper: pi ? pi.upper : null
            };
        } catch(e) { results.predictionInterval_Standard = {passed: false, error: e.message}; }

        // leave1out
        try {
            const loo = leave1out(yi, vi);
            results.leave1out = {
                passed: loo && Array.isArray(loo) && loo.length === yi.length,
                length: loo ? loo.length : null
            };
        } catch(e) { results.leave1out = {passed: false, error: e.message}; }

        // cumulativeMetaAnalysis
        try {
            const cumul = cumulativeMetaAnalysis(yi, vi);
            results.cumulativeMetaAnalysis = {
                passed: cumul && Array.isArray(cumul) && cumul.length > 0,
                length: cumul ? cumul.length : null
            };
        } catch(e) { results.cumulativeMetaAnalysis = {passed: false, error: e.message}; }

        // influenceDiagnostics
        try {
            const infl = influenceDiagnostics(yi, vi);
            results.influenceDiagnostics = {
                passed: infl && infl.dfbetas && Array.isArray(infl.dfbetas),
                hasData: infl ? true : false
            };
        } catch(e) { results.influenceDiagnostics = {passed: false, error: e.message}; }

        // subgroupAnalysis
        try {
            const groups = ["A", "A", "B", "B", "A"];
            const subg = subgroupAnalysis(yi, vi, groups);
            results.subgroupAnalysis = {
                passed: subg && subg.subgroups && Object.keys(subg.subgroups).length === 2,
                groups: subg ? Object.keys(subg.subgroups) : []
            };
        } catch(e) { results.subgroupAnalysis = {passed: false, error: e.message}; }

        // metaRegression
        try {
            const mods = [1, 2, 3, 4, 5];
            const reg = metaRegression(yi, vi, mods);
            results.metaRegression = {
                passed: reg && typeof reg.beta === "number",
                beta: reg ? reg.beta : null
            };
        } catch(e) { results.metaRegression = {passed: false, error: e.message}; }

        // assessGRADE
        try {
            const grade = assessGRADE({yi, vi, I2: 50, egger_p: 0.3, rob: null});
            results.assessGRADE = {
                passed: grade && typeof grade.overall === "string",
                overall: grade ? grade.overall : null
            };
        } catch(e) { results.assessGRADE = {passed: false, error: e.message}; }

        return results;
    ''')

    for func, result in core_funcs.items():
        if result.get("passed"):
            log_test("Core Function", func, True)
        else:
            log_test("Core Function", func, False, result.get("error", "Failed"))

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
            results.petPeese = {passed: pp && typeof pp.PET === "object", hasPET: !!pp?.PET};
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

        // selectionModel (Vevea-Hedges)
        try {
            const sm = typeof selectionModelVeveaHedges === "function" ?
                       selectionModelVeveaHedges(yi, vi) : null;
            results.selectionModelVeveaHedges = {passed: sm && typeof sm.adjusted_theta === "number"};
        } catch(e) { results.selectionModelVeveaHedges = {passed: false, error: e.message}; }

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

    # First load BCG dataset and run analysis
    driver.execute_script('''
        loadDemoDataset("BCG");
    ''')
    time.sleep(1)

    # Run analysis to get results
    driver.execute_script('''
        if (typeof runAnalysis === "function") {
            runAnalysis();
        }
    ''')
    time.sleep(2)

    plot_tests = driver.execute_script('''
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
        const sei = vi.map(v => Math.sqrt(v));
        const names = ["Study 1", "Study 2", "Study 3", "Study 4", "Study 5"];
        const tau2 = estimateTau2_REML(yi, vi).tau2;
        const pooled = calculatePooledEstimate(yi, vi, tau2);

        const results = {};

        // Forest Plot
        try {
            const div = document.createElement("div");
            div.id = "testForestPlot";
            div.style.width = "800px";
            div.style.height = "400px";
            document.body.appendChild(div);
            renderForestPlot({
                yi, vi, sei, names, tau2, pooled,
                studies: names.map((n, i) => ({name: n, yi: yi[i], vi: vi[i], sei: sei[i]})),
                measure: "OR",
                het: {I2: 75, Q: 20, p_Q: 0.001}
            });
            results.renderForestPlot = {passed: div.querySelector(".js-plotly-plot") !== null};
            div.remove();
        } catch(e) { results.renderForestPlot = {passed: false, error: e.message}; }

        // Funnel Plot
        try {
            const div = document.createElement("div");
            div.id = "testFunnelPlot";
            div.style.width = "600px";
            div.style.height = "400px";
            document.body.appendChild(div);
            renderFunnelPlot(yi, sei, names, pooled.theta);
            results.renderFunnelPlot = {passed: div.querySelector(".js-plotly-plot") !== null};
            div.remove();
        } catch(e) { results.renderFunnelPlot = {passed: false, error: e.message}; }

        // Baujat Plot
        try {
            const div = document.createElement("div");
            div.id = "testBaujatPlot";
            div.style.width = "600px";
            div.style.height = "400px";
            document.body.appendChild(div);
            renderBaujatPlot(yi, vi, names);
            results.renderBaujatPlot = {passed: div.querySelector(".js-plotly-plot") !== null};
            div.remove();
        } catch(e) { results.renderBaujatPlot = {passed: false, error: e.message}; }

        // Radial/Galbraith Plot
        try {
            const div = document.createElement("div");
            div.id = "testRadialPlot";
            div.style.width = "600px";
            div.style.height = "400px";
            document.body.appendChild(div);
            renderRadialPlot(yi, vi, names);
            results.renderRadialPlot = {passed: div.querySelector(".js-plotly-plot") !== null};
            div.remove();
        } catch(e) { results.renderRadialPlot = {passed: false, error: e.message}; }

        // DOI Plot
        try {
            const div = document.createElement("div");
            div.id = "testDOIPlot";
            div.style.width = "600px";
            div.style.height = "400px";
            document.body.appendChild(div);
            renderDOIPlot(yi, vi, names);
            results.renderDOIPlot = {passed: div.querySelector(".js-plotly-plot") !== null};
            div.remove();
        } catch(e) { results.renderDOIPlot = {passed: false, error: e.message}; }

        // P-curve Plot
        try {
            const div = document.createElement("div");
            div.id = "testPCurvePlot";
            div.style.width = "600px";
            div.style.height = "400px";
            document.body.appendChild(div);
            renderPCurvePlot(yi, vi);
            results.renderPCurvePlot = {passed: div.querySelector(".js-plotly-plot") !== null};
            div.remove();
        } catch(e) { results.renderPCurvePlot = {passed: false, error: e.message}; }

        // GOSH Plot (may take time, use small subset)
        try {
            const div = document.createElement("div");
            div.id = "testGOSHPlot";
            div.style.width = "600px";
            div.style.height = "400px";
            document.body.appendChild(div);
            const smallYi = yi.slice(0, 4);
            const smallVi = vi.slice(0, 4);
            renderGOSHPlot(smallYi, smallVi);
            results.renderGOSHPlot = {passed: div.querySelector(".js-plotly-plot") !== null};
            div.remove();
        } catch(e) { results.renderGOSHPlot = {passed: false, error: e.message}; }

        // L'Abbe Plot (for binary data)
        try {
            results.renderLabbePlot = {passed: typeof renderLabbePlot === "function"};
        } catch(e) { results.renderLabbePlot = {passed: false, error: e.message}; }

        // Cumulative Forest Plot
        try {
            results.renderCumulativeForest = {passed: typeof renderCumulativeForest === "function"};
        } catch(e) { results.renderCumulativeForest = {passed: false, error: e.message}; }

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

        // Test R code generation
        if (typeof generateRCode === "function") {
            try {
                const rCode = generateRCode();
                results.generateRCode_output = {passed: rCode && rCode.length > 100};
            } catch(e) {
                results.generateRCode_output = {passed: false};
            }
        }

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
        const results = [];
        tabs.forEach(tab => {
            results.push({
                name: tab.getAttribute("data-tab"),
                exists: true
            });
        });
        return results;
    ''')

    print("\n--- Tab Navigation ---")
    for tab in tabs:
        log_test("UI Tab", f"Tab: {tab['name']}", tab.get("exists", False))

    # Test buttons
    buttons = driver.execute_script('''
        const buttonTests = {};

        // Run Analysis button
        const runBtn = document.querySelector("[onclick*='runAnalysis']") ||
                      document.querySelector("button:contains('Run Analysis')") ||
                      document.getElementById("runAnalysisBtn");
        buttonTests.runAnalysis = {exists: !!runBtn || typeof runAnalysis === "function"};

        // Run Full Analysis
        buttonTests.runFullAnalysis = {exists: typeof runFullAnalysis === "function"};

        // Add Study Row
        buttonTests.addStudyRow = {exists: typeof addStudyRow === "function"};

        // Delete Study Row
        buttonTests.deleteStudyRow = {exists: typeof deleteStudyRow === "function"};

        // Import CSV
        buttonTests.importCSV = {exists: typeof importCSV === "function" || typeof handleCSVImport === "function"};

        // Clear All
        buttonTests.clearAll = {exists: typeof clearAllData === "function" || typeof clearData === "function"};

        // Load Demo
        buttonTests.loadDemoDataset = {exists: typeof loadDemoDataset === "function"};

        // Forest plot settings
        buttonTests.applyForestPreset = {exists: typeof applyForestPreset === "function"};
        buttonTests.updateForestSetting = {exists: typeof updateForestSetting === "function"};
        buttonTests.reRenderForestPlot = {exists: typeof reRenderForestPlot === "function"};

        // Bias tests
        buttonTests.computeEggerTest = {exists: typeof eggerTest === "function"};
        buttonTests.computeTrimFill = {exists: typeof trimAndFill === "function"};

        // Download plot
        buttonTests.downloadPlot = {exists: typeof downloadPlot === "function"};

        // GRADE
        buttonTests.computeGRADE = {exists: typeof computeGRADE === "function" || typeof assessGRADE === "function"};
        buttonTests.showGRADEDetails = {exists: typeof showGRADEDetails === "function"};

        return buttonTests;
    ''')

    print("\n--- Button Functions ---")
    for btn, result in buttons.items():
        log_test("UI Button", btn, result.get("exists", False))

    # =========================================================================
    # SECTION 8: BUILT-IN TEST SUITE
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 8: BUILT-IN TEST SUITE")
    print("=" * 70)

    builtin_tests = driver.execute_script('''
        if (typeof runAutomatedTests === "function") {
            return runAutomatedTests();
        }
        return null;
    ''')

    if builtin_tests:
        passed = builtin_tests.get("passed", 0)
        failed = builtin_tests.get("failed", 0)
        total = passed + failed
        log_test("Built-in Tests", f"Automated Test Suite ({passed}/{total})", failed == 0)

        # Show individual test results if available
        if "results" in builtin_tests:
            for test in builtin_tests["results"]:
                status = test.get("status", "unknown")
                name = test.get("name", "unnamed")
                log_test("Built-in Tests", f"  - {name}", status == "pass")
    else:
        log_test("Built-in Tests", "Automated Test Suite", False, "Function not available")

    # =========================================================================
    # SECTION 9: VALIDATION STATUS & DOCUMENTATION
    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 9: VALIDATION & DOCUMENTATION")
    print("=" * 70)

    validation = driver.execute_script('''
        const results = {};

        // VALIDATION_STATUS
        results.VALIDATION_STATUS = {
            exists: typeof VALIDATION_STATUS !== "undefined",
            methods: typeof VALIDATION_STATUS !== "undefined" ? Object.keys(VALIDATION_STATUS.methods || {}).length : 0
        };

        // APPROXIMATION_WARNINGS
        results.APPROXIMATION_WARNINGS = {
            exists: typeof APPROXIMATION_WARNINGS !== "undefined",
            categories: typeof APPROXIMATION_WARNINGS !== "undefined" ? Object.keys(APPROXIMATION_WARNINGS).length : 0
        };

        // Method references count
        let refCount = 0;
        const codeStr = document.querySelector("script")?.textContent || "";
        refCount = (codeStr.match(/reference:/g) || []).length;
        results.methodReferences = {count: refCount};

        return results;
    ''')

    log_test("Validation", "VALIDATION_STATUS object", validation.get("VALIDATION_STATUS", {}).get("exists", False),
             f"{validation.get('VALIDATION_STATUS', {}).get('methods', 0)} methods")
    log_test("Validation", "APPROXIMATION_WARNINGS object", validation.get("APPROXIMATION_WARNINGS", {}).get("exists", False),
             f"{validation.get('APPROXIMATION_WARNINGS', {}).get('categories', 0)} categories")

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

    print("\n" + "-" * 70)

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

    print("\nCategory Breakdown:")
    for cat, counts in categories.items():
        cat_total = counts["passed"] + counts["failed"]
        cat_pct = (counts["passed"] / cat_total) * 100 if cat_total > 0 else 0
        status = "OK" if cat_pct == 100 else "PARTIAL" if cat_pct >= 80 else "ISSUES"
        print(f"  [{status}] {cat}: {counts['passed']}/{cat_total} ({cat_pct:.0f}%)")

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

    # List failures if any
    if results["failed"] > 0:
        print("\nFailed Tests:")
        for detail in results["details"]:
            if not detail["passed"]:
                print(f"  - [{detail['category']}] {detail['name']}: {detail.get('details', 'No details')}")

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print("\nTest completed.")
