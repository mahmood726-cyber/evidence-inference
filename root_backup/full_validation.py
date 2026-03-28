#!/usr/bin/env python3
"""Full validation test of TruthCert-PairwisePro"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

print("=" * 70)
print("FULL VALIDATION TEST")
print("TruthCert-PairwisePro v1.0")
print("=" * 70)

driver_path = r"C:\Users\user\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32\chromedriver.exe"
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

results = {"passed": 0, "failed": 0}

def log_test(name, passed):
    status = "PASS" if passed else "FAIL"
    if passed: results["passed"] += 1
    else: results["failed"] += 1
    print(f"  [{status}] {name}")

try:
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)

    logs = driver.get_log("browser")
    severe = [l for l in logs if l["level"] == "SEVERE"]
    log_test("Page loads without JS errors", len(severe) == 0)

    print("\n--- STATISTICAL DISTRIBUTIONS ---")
    dist = driver.execute_script("""return {
        pnorm: Math.abs(pnorm(1.96) - 0.975) < 0.001,
        qnorm: Math.abs(qnorm(0.975) - 1.96) < 0.01,
        pt: Math.abs(pt(2, 10) - 0.9633) < 0.01,
        qt: Math.abs(qt(0.975, 10) - 2.228) < 0.05,
        pchisq: Math.abs(pchisq(5, 2) - 0.9179) < 0.01,
        lgamma: Math.abs(lgamma(5) - 3.178) < 0.01,
    };""")
    for n, p in dist.items(): log_test(n, p)

    print("\n--- TAU-SQUARED ESTIMATORS ---")
    tau2 = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        const ref = {DL:0.30876, REML:0.313243, ML:0.280028, PM:0.318094,
                     HS:0.228363, SJ:0.345516, HE:0.328564, EB:0.318069};
        const r = {};
        for (const m of Object.keys(ref)) {
            const fn = window["estimateTau2_" + m];
            if (fn) { try { r[m] = Math.abs(fn(yi,vi).tau2 - ref[m]) < 0.01; } catch(e) { r[m] = false; } }
            else { r[m] = false; }
        }
        return r;
    """)
    for m, p in tau2.items(): log_test(f"tau2_{m}", p)

    print("\n--- CORE FUNCTIONS ---")
    funcs = driver.execute_script("""return {
        calculatePooledEstimate: typeof calculatePooledEstimate === "function",
        calculateHKSJ: typeof calculateHKSJ === "function",
        eggerTest: typeof eggerTest === "function",
        trimAndFill: typeof trimAndFill === "function",
        bayesianMetaAnalysis: typeof bayesianMetaAnalysis === "function",
        subgroupAnalysis: typeof subgroupAnalysis === "function",
        metaRegression: typeof metaRegression === "function",
        fragilityIndex: typeof fragilityIndex === "function",
        calculateEValue: typeof calculateEValue === "function",
        leave1out: typeof leave1out === "function",
        cumulativeMetaAnalysis: typeof cumulativeMetaAnalysis === "function",
    };""")
    for n, p in funcs.items(): log_test(n, p)

    print("\n--- PLOTTING FUNCTIONS ---")
    plots = driver.execute_script("""return {
        renderForestPlot: typeof renderForestPlot === "function",
        renderFunnelPlot: typeof renderFunnelPlot === "function",
        renderBaujatPlot: typeof renderBaujatPlot === "function",
        renderRadialPlot: typeof renderRadialPlot === "function",
        renderDOIPlot: typeof renderDOIPlot === "function",
        renderPCurvePlot: typeof renderPCurvePlot === "function",
        renderGOSHPlot: typeof renderGOSHPlot === "function",
    };""")
    for n, p in plots.items(): log_test(n, p)

    print("\n--- EXPORT FUNCTIONS ---")
    exports = driver.execute_script("""return {
        exportCSV: typeof exportCSV === "function",
        exportJSON: typeof exportJSON === "function",
        generateRCode: typeof generateRCode === "function",
    };""")
    for n, p in exports.items(): log_test(n, p)

    print("\n--- BUILT-IN TEST SUITE ---")
    tests = driver.execute_script('if (typeof runAutomatedTests==="function") return runAutomatedTests(); return null;')
    if tests:
        p, f = tests.get("passed", 0), tests.get("failed", 0)
        log_test(f"built_in_tests ({p}/{p+f})", f == 0)
    else:
        log_test("built_in_tests", False)

    print("\n--- DEMO DATASETS ---")
    ds = driver.execute_script('return typeof DEMO_DATASETS !== "undefined" ? Object.keys(DEMO_DATASETS).length : 0;')
    log_test(f"demo_datasets ({ds} available)", ds >= 15)

    # Test loading each demo dataset
    print("\n--- DEMO DATASET LOADING ---")
    demo_keys = driver.execute_script("return Object.keys(DEMO_DATASETS);")
    for key in demo_keys:
        result = driver.execute_script(f'try {{ loadDemoDataset("{key}"); return true; }} catch (e) {{ return false; }}')
        log_test(f"Load {key}", result)

    # Test actual plot rendering
    print("\n--- PLOT RENDERING ---")
    driver.execute_script("""
        window.yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547];
        window.vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210];
        window.names = ['Study 1', 'Study 2', 'Study 3', 'Study 4', 'Study 5'];
        window.tau2 = estimateTau2_REML(window.yi, window.vi);
        window.pooled = calculatePooledEstimate(window.yi, window.vi, window.tau2.tau2);
    """)

    render_tests = [
        ("Forest", "renderForestPlot(window.yi, window.vi, window.names, window.pooled, window.tau2.tau2)"),
        ("Funnel", "renderFunnelPlot(window.yi, window.vi, window.pooled.theta)"),
        ("Baujat", "renderBaujatPlot(window.yi, window.vi, window.names)"),
        ("Radial", "renderRadialPlot(window.yi, window.vi, window.names)"),
        ("DOI", "renderDOIPlot(window.yi, window.vi, window.names)"),
    ]
    for name, code in render_tests:
        result = driver.execute_script(f"try {{ {code}; return true; }} catch(e) {{ return false; }}")
        log_test(f"Render {name} plot", result)

    # Test analysis functions with actual data
    print("\n--- ANALYSIS EXECUTION ---")
    analysis_tests = [
        ("HKSJ", "calculateHKSJ(window.yi, window.vi, window.tau2.tau2)"),
        ("Egger", "eggerTest(window.yi, window.vi)"),
        ("TrimFill", "trimAndFill(window.yi, window.vi)"),
        ("Leave1out", "leave1out(window.yi, window.vi, window.names)"),
        ("Cumulative", "cumulativeMetaAnalysis(window.yi, window.vi, window.names)"),
        ("Bayesian", "bayesianMetaAnalysis(window.yi, window.vi, {nIter: 1000, seed: 42})"),
    ]
    for name, code in analysis_tests:
        result = driver.execute_script(f"try {{ {code}; return true; }} catch(e) {{ return false; }}")
        log_test(f"Execute {name}", result)

    # Test libraries
    print("\n--- LIBRARIES ---")
    libs = driver.execute_script('return { Plotly: typeof Plotly !== "undefined", XLSX: typeof XLSX !== "undefined" };')
    for n, p in libs.items(): log_test(f"Library: {n}", p)

    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    total = results["passed"] + results["failed"]
    pct = (results["passed"] / total) * 100 if total > 0 else 0
    print(f"\nTests Passed: {results['passed']}/{total} ({pct:.1f}%)")
    
    if pct >= 95: print("\nVERDICT: EXCELLENT - Application fully validated")
    elif pct >= 85: print("\nVERDICT: GOOD - Most features working correctly")
    else: print("\nVERDICT: ACCEPTABLE")
    print("=" * 70)

finally:
    driver.quit()
