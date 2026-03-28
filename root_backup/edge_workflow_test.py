#!/usr/bin/env python3
"""Edge browser workflow test - tests through actual app workflow"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("=" * 70)
print("EDGE BROWSER WORKFLOW TEST")
print("TruthCert-PairwisePro v1.0")
print("Testing via actual application workflow")
print("=" * 70)

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Edge(options=options)

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
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)

    logs = driver.get_log("browser")
    severe = [l for l in logs if l["level"] == "SEVERE"]
    test("Page loads without JS errors", len(severe) == 0)

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 1: DEMO DATASETS - Load and Verify Each")
    print("=" * 70)

    datasets = driver.execute_script("return Object.keys(DEMO_DATASETS);")
    print(f"Testing {len(datasets)} demo datasets...\n")

    for ds in datasets:
        result = driver.execute_script(f'''
            try {{
                loadDemoDataset("{ds}");
                const demoData = DEMO_DATASETS["{ds}"];
                const count = demoData.studies?.length || demoData.data?.length || AppState?.data?.length || 0;
                return {{ok: count > 0, count: count}};
            }} catch(e) {{ return {{ok: false, error: e.message}}; }}
        ''')
        test(f"Load {ds}", result.get("ok", False), f"{result.get('count', 0)} studies")

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 2: FULL ANALYSIS WORKFLOW (BCG Dataset)")
    print("=" * 70)

    # Load BCG and run full analysis
    driver.execute_script("loadDemoDataset('BCG');")
    time.sleep(0.5)

    # Run analysis via actual button/function
    analysis_result = driver.execute_script('''
        try {
            runAnalysis();
            return {ok: true};
        } catch(e) {
            return {ok: false, error: e.message};
        }
    ''')
    time.sleep(2)
    test("Run Analysis", analysis_result.get("ok", False))

    # Check AppState.results
    results_check = driver.execute_script('''
        if (!AppState.results) return {ok: false, error: "No results"};
        const r = AppState.results;
        return {
            ok: true,
            hasPooled: !!r.pooled,
            pooledTheta: r.pooled?.theta,
            hasTau2: typeof r.tau2 === "number",
            tau2: r.tau2,
            hasHet: !!r.het,
            I2: r.het?.I2,
            hasStudies: Array.isArray(r.studies),
            studyCount: r.studies?.length,
            hasPI: !!r.pi,
            hasHKSJ: !!r.hksj
        };
    ''')
    test("Pooled estimate calculated", results_check.get("hasPooled", False),
         f"theta={results_check.get('pooledTheta', 'N/A'):.4f}" if results_check.get('pooledTheta') else "")
    test("Tau-squared estimated", results_check.get("hasTau2", False),
         f"tau2={results_check.get('tau2', 'N/A'):.4f}" if results_check.get('tau2') else "")
    test("Heterogeneity computed", results_check.get("hasHet", False),
         f"I2={results_check.get('I2', 'N/A'):.1f}%" if results_check.get('I2') else "")
    test("Prediction intervals", results_check.get("hasPI", False))
    test("HKSJ adjustment", results_check.get("hasHKSJ", False))

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 3: TAU-SQUARED ESTIMATORS (Direct Test)")
    print("=" * 70)

    tau2_results = driver.execute_script('''
        const yi = AppState.results.yi;
        const vi = AppState.results.vi;
        const ref = {DL:0.308760, REML:0.313243, ML:0.280028, PM:0.318094,
                     HS:0.228363, SJ:0.345516, HE:0.328564, EB:0.318069};
        const results = {};
        for (const m of Object.keys(ref)) {
            try {
                const fn = window["estimateTau2_" + m];
                const est = fn(yi, vi).tau2;
                results[m] = {ok: Math.abs(est - ref[m]) < 0.01, est: est, ref: ref[m]};
            } catch(e) { results[m] = {ok: false, error: e.message}; }
        }
        return results;
    ''')
    for method, r in tau2_results.items():
        test(f"tau2_{method}", r.get("ok", False),
             f"est={r.get('est',0):.4f} ref={r.get('ref',0):.4f}" if r.get("ok") else r.get("error", ""))

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 4: PLOTS RENDERED")
    print("=" * 70)

    # Check if forest plot rendered
    forest_check = driver.execute_script('''
        const fp = document.getElementById("forestPlot");
        return fp && (fp.querySelector(".js-plotly-plot") || fp.innerHTML.length > 500);
    ''')
    test("Forest Plot rendered", forest_check)

    # Navigate to heterogeneity tab and check funnel
    driver.execute_script("document.querySelector('[data-tab=\"heterogeneity\"]').click();")
    time.sleep(1)

    funnel_check = driver.execute_script('''
        const fp = document.getElementById("funnelPlot");
        return fp && (fp.querySelector(".js-plotly-plot") || fp.innerHTML.length > 100);
    ''')
    test("Funnel Plot rendered", funnel_check)

    # Check other plots exist
    other_plots = driver.execute_script('''
        return {
            baujat: document.getElementById("baujatPlot") !== null,
            radial: document.getElementById("radialPlot") !== null ||
                    document.getElementById("galbraithPlot") !== null,
            doi: document.getElementById("doiPlot") !== null,
            pcurve: document.getElementById("pCurvePlot") !== null
        };
    ''')
    for plot, exists in other_plots.items():
        test(f"{plot} plot container", exists)

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 5: PUBLICATION BIAS TESTS")
    print("=" * 70)

    bias_results = driver.execute_script('''
        const r = AppState.results;
        return {
            hasEgger: !!r.egger,
            eggerP: r.egger?.p_value,
            hasTrimFill: !!r.trimfill,
            trimFillK0: r.trimfill?.k0_imputed,
            hasFailsafe: r.rosenthal_fsn || r.failsafe
        };
    ''')
    test("Egger's test", bias_results.get("hasEgger", False),
         f"p={bias_results.get('eggerP', 'N/A'):.4f}" if bias_results.get('eggerP') else "")
    test("Trim-and-Fill", bias_results.get("hasTrimFill", False),
         f"k0={bias_results.get('trimFillK0', 0)}" if bias_results.get('hasTrimFill') else "")

    # Test Begg directly
    begg_result = driver.execute_script('''
        try {
            const r = AppState.results;
            const sei = r.vi.map(v => Math.sqrt(v));
            const b = beggTest(r.yi, sei);
            return {ok: typeof b.tau === "number", tau: b.tau, p: b.p};
        } catch(e) { return {ok: false, error: e.message}; }
    ''')
    test("Begg's rank correlation", begg_result.get("ok", False),
         f"tau={begg_result.get('tau', 0):.3f}" if begg_result.get("ok") else "")

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 6: SENSITIVITY ANALYSES")
    print("=" * 70)

    sens_results = driver.execute_script('''
        const r = AppState.results;
        return {
            hasLOO: !!r.loo || !!r.leaveOneOut,
            hasCumul: !!r.cumulative,
            hasInfluence: !!r.influence,
            hasBaujat: !!r.baujat
        };
    ''')
    test("Leave-one-out analysis", sens_results.get("hasLOO", False))
    test("Cumulative meta-analysis", sens_results.get("hasCumul", False))
    test("Influence diagnostics", sens_results.get("hasInfluence", False))

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 7: ADVANCED FEATURES")
    print("=" * 70)

    # Test Bayesian
    bayes_result = driver.execute_script('''
        try {
            const r = AppState.results;
            const bay = bayesianMetaAnalysis(r.yi, r.vi, {nIter: 500, seed: 42});
            return {ok: typeof bay.pooled === "number", pooled: bay.pooled};
        } catch(e) { return {ok: false, error: e.message}; }
    ''')
    test("Bayesian meta-analysis", bayes_result.get("ok", False))

    # Test GRADE
    grade_result = driver.execute_script('''
        try {
            const r = AppState.results;
            if (r.grade) return {ok: true, overall: r.grade.overall};
            const g = assessGRADE({yi: r.yi, vi: r.vi, I2: r.het.I2, egger_p: r.egger?.p_value});
            return {ok: !!g.overall, overall: g.overall};
        } catch(e) { return {ok: false, error: e.message}; }
    ''')
    test("GRADE assessment", grade_result.get("ok", False), grade_result.get("overall", ""))

    # Test E-value
    evalue_result = driver.execute_script('''
        try {
            const r = AppState.results;
            const ev = calculateEValue(Math.exp(r.pooled.theta), "RR");
            return {ok: typeof ev.eValue === "number", eValue: ev.eValue};
        } catch(e) { return {ok: false, error: e.message}; }
    ''')
    test("E-value calculation", evalue_result.get("ok", False))

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 8: EXPORT FUNCTIONS")
    print("=" * 70)

    export_check = driver.execute_script('''
        return {
            csv: typeof exportCSV === "function",
            json: typeof exportJSON === "function",
            xlsx: typeof XLSX !== "undefined",
            rCode: typeof generateRCode === "function",
            python: typeof generatePythonCode === "function",
            download: typeof downloadPlot === "function"
        };
    ''')
    for exp, exists in export_check.items():
        test(f"Export {exp}", exists)

    # Test R code generation
    rcode_result = driver.execute_script('''
        try {
            const code = generateRCode();
            return {ok: code && code.length > 100, length: code?.length};
        } catch(e) { return {ok: false, error: e.message}; }
    ''')
    test("R code generation works", rcode_result.get("ok", False),
         f"{rcode_result.get('length', 0)} chars" if rcode_result.get("ok") else "")

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 9: UI NAVIGATION")
    print("=" * 70)

    tabs = ["data", "analysis", "heterogeneity", "bias", "validation", "advanced", "report"]
    for tab in tabs:
        try:
            driver.execute_script(f"document.querySelector('[data-tab=\"{tab}\"]').click();")
            time.sleep(0.3)
            is_active = driver.execute_script(f'''
                const panel = document.getElementById("panel-{tab}");
                return panel && !panel.classList.contains("hidden");
            ''')
            test(f"Navigate to {tab} tab", is_active)
        except:
            test(f"Navigate to {tab} tab", False)

    # =========================================================================
    print("\n" + "=" * 70)
    print("SECTION 10: BUILT-IN TEST SUITE")
    print("=" * 70)

    builtin = driver.execute_script('''
        if (typeof runAutomatedTests === "function") {
            return runAutomatedTests();
        }
        return null;
    ''')
    if builtin:
        p, f = builtin.get("passed", 0), builtin.get("failed", 0)
        test(f"Built-in test suite", f == 0, f"{p}/{p+f} passed")
    else:
        test("Built-in test suite", False, "Not available")

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

    print("\n" + "=" * 70)
    if pct >= 95:
        print("VERDICT: EXCELLENT - Application fully operational")
    elif pct >= 85:
        print("VERDICT: GOOD - Minor issues only")
    elif pct >= 70:
        print("VERDICT: ACCEPTABLE - Some features need attention")
    else:
        print("VERDICT: NEEDS WORK")
    print("=" * 70)

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
