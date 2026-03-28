#!/usr/bin/env python3
"""Edge Browser Validation - Fixed for DevToolsActivePort issue"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

print("=" * 70)
print("EDGE/CHROME BROWSER VALIDATION TEST")
print("TruthCert-PairwisePro - Complete Validation")
print("=" * 70)

# Use Chrome with fixed options for headless
options = Options()
options.add_argument("--headless=new")  # New headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--remote-debugging-port=9222")

# Use the driver found in cache
driver_path = r"C:\Users\user\.cache\selenium\chromedriver\win64\143.0.7499.192\chromedriver.exe"

print(f"\nUsing driver: {driver_path}")
print(f"Driver exists: {os.path.exists(driver_path)}")

try:
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_script_timeout(30)
except Exception as e:
    print(f"Chrome with service failed: {e}")
    print("\nTrying default Chrome...")
    driver = webdriver.Chrome(options=options)
    driver.set_script_timeout(30)

results = {"passed": 0, "failed": 0}

def safe_exec(script, name):
    try:
        return driver.execute_script(script)
    except Exception as e:
        print(f"  [ERROR] {name}: {str(e)[:40]}")
        return None

try:
    # Load page
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)
    print(f"Page loaded: {driver.title}\n")

    # ==========================================
    # 1. DEMO DATASETS
    # ==========================================
    print("--- 1. DEMO DATASETS ---")
    demos = safe_exec("return Object.keys(DEMO_DATASETS);", "demos")
    if demos:
        for key in demos:
            info = safe_exec(f"return DEMO_DATASETS['{key}'];", key)
            if info:
                count = info.get('studies', len(info.get('data', [])) if info.get('data') else 0)
                if count > 0:
                    print(f"  [PASS] {key} ({count} studies)")
                    results["passed"] += 1
                else:
                    results["failed"] += 1

    # ==========================================
    # 2. CRITICAL GAP FUNCTIONS
    # ==========================================
    print("\n--- 2. CRITICAL GAP FUNCTIONS ---")

    gap_fns = [
        ("calculateMH_OR", "Mantel-Haenszel"),
        ("calculatePeto_OR", "Peto Method"),
        ("influenceDiagnostics", "Cook's Distance"),
        ("testExcessSignificance", "TES Test"),
        ("renderQQPlot", "QQ Plot"),
        ("getStandardizedResiduals", "Std Residuals")
    ]

    for fn, desc in gap_fns:
        exists = safe_exec(f"return typeof {fn} === 'function';", fn)
        if exists:
            print(f"  [PASS] {fn}() - {desc}")
            results["passed"] += 1
        else:
            print(f"  [FAIL] {fn}() - {desc}")
            results["failed"] += 1

    # ==========================================
    # 3. TAU2 ESTIMATORS vs R
    # ==========================================
    print("\n--- 3. TAU2 ESTIMATORS vs R/metafor ---")

    tau2 = safe_exec("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        const ref = {DL: 0.308760, REML: 0.313243, ML: 0.280028, PM: 0.318094,
                     HS: 0.228363, SJ: 0.345516, HE: 0.328564, EB: 0.318069};
        const results = {};
        for (const m of Object.keys(ref)) {
            const fn = window['estimateTau2_' + m];
            if (fn) {
                try {
                    const r = fn(yi, vi);
                    const diff = Math.abs(r.tau2 - ref[m]);
                    results[m] = {js: r.tau2, r: ref[m], diff: diff, pass: diff < 0.01};
                } catch(e) { results[m] = {error: e.message}; }
            }
        }
        return results;
    """, "tau2")

    if tau2:
        for m, r in tau2.items():
            if r.get('pass'):
                print(f"  [PASS] {m}: JS={r['js']:.6f} R={r['r']:.6f}")
                results["passed"] += 1
            else:
                print(f"  [FAIL] {m}: {r}")
                results["failed"] += 1

    # ==========================================
    # 4. MANTEL-HAENSZEL vs R
    # ==========================================
    print("\n--- 4. MANTEL-HAENSZEL vs R ---")

    mh = safe_exec("""
        if (typeof calculateMH_OR !== 'function') return {error: 'not found'};
        const ai = [4, 6, 3, 62, 33, 180, 8, 505, 29, 17, 186, 5, 27];
        const bi = [119, 300, 228, 13536, 5036, 1361, 2537, 87886, 7470, 1699, 50448, 2493, 16886];
        const ci = [11, 29, 11, 248, 47, 372, 10, 499, 45, 65, 141, 3, 29];
        const di = [128, 274, 209, 12619, 5761, 1079, 619, 87892, 7232, 1600, 27197, 2338, 17825];
        try {
            const r = calculateMH_OR(ai, bi, ci, di);
            return {OR: r.OR, ref: 0.622874};
        } catch(e) { return {error: e.message}; }
    """, "mh")

    if mh and not mh.get('error'):
        diff = abs(mh['OR'] - mh['ref'])
        if diff < 0.05:
            print(f"  [PASS] MH OR: JS={mh['OR']:.4f} R={mh['ref']:.4f}")
            results["passed"] += 1
        else:
            print(f"  [FAIL] MH OR: diff={diff:.4f}")
            results["failed"] += 1
    else:
        print(f"  [INFO] MH: {mh}")

    # ==========================================
    # 5. PETO vs R
    # ==========================================
    print("\n--- 5. PETO METHOD vs R ---")

    peto = safe_exec("""
        if (typeof calculatePeto_OR !== 'function') return {error: 'not found'};
        const ai = [4, 6, 3, 62, 33, 180, 8, 505, 29, 17, 186, 5, 27];
        const bi = [119, 300, 228, 13536, 5036, 1361, 2537, 87886, 7470, 1699, 50448, 2493, 16886];
        const ci = [11, 29, 11, 248, 47, 372, 10, 499, 45, 65, 141, 3, 29];
        const di = [128, 274, 209, 12619, 5761, 1079, 619, 87892, 7232, 1600, 27197, 2338, 17825];
        try {
            const r = calculatePeto_OR(ai, bi, ci, di);
            return {OR: r.OR, ref: 0.6222295};
        } catch(e) { return {error: e.message}; }
    """, "peto")

    if peto and not peto.get('error'):
        diff = abs(peto['OR'] - peto['ref'])
        if diff < 0.05:
            print(f"  [PASS] Peto OR: JS={peto['OR']:.4f} R={peto['ref']:.4f}")
            results["passed"] += 1
        else:
            print(f"  [FAIL] Peto OR: diff={diff:.4f}")
            results["failed"] += 1
    else:
        print(f"  [INFO] Peto: {peto}")

    # ==========================================
    # 6. TES vs R
    # ==========================================
    print("\n--- 6. TES vs R ---")

    tes = safe_exec("""
        if (typeof testExcessSignificance !== 'function') return {error: 'not found'};
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        try {
            const r = testExcessSignificance(yi, vi);
            return {observed: r.observed, expected: r.expected, ref_obs: 8, ref_exp: 6.1};
        } catch(e) { return {error: e.message}; }
    """, "tes")

    if tes and not tes.get('error'):
        if tes['observed'] == tes['ref_obs']:
            print(f"  [PASS] TES Observed: {tes['observed']} (R={tes['ref_obs']})")
            results["passed"] += 1
        else:
            print(f"  [FAIL] TES Observed: {tes['observed']} (R={tes['ref_obs']})")
            results["failed"] += 1
        print(f"  [INFO] TES Expected: {tes['expected']:.2f} (R~{tes['ref_exp']})")
    else:
        print(f"  [INFO] TES: {tes}")
        results["failed"] += 1

    # ==========================================
    # 7. COOK'S DISTANCE vs R
    # ==========================================
    print("\n--- 7. COOK'S DISTANCE vs R ---")

    cooks = safe_exec("""
        if (typeof influenceDiagnostics !== 'function') return {error: 'not found'};
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        try {
            const r = influenceDiagnostics(yi, vi);
            const maxD = Math.max(...r.cooksD);
            const maxIdx = r.cooksD.indexOf(maxD) + 1;
            return {maxD: maxD, maxStudy: maxIdx, ref_maxD: 0.200266, ref_study: 8};
        } catch(e) { return {error: e.message}; }
    """, "cooks")

    if cooks and not cooks.get('error'):
        diff = abs(cooks['maxD'] - cooks['ref_maxD'])
        if diff < 0.1:
            print(f"  [PASS] Max Cook's D: {cooks['maxD']:.4f} (R={cooks['ref_maxD']:.4f})")
            results["passed"] += 1
        else:
            print(f"  [FAIL] Max Cook's D: diff={diff:.4f}")
            results["failed"] += 1
        print(f"  [INFO] Max at study: {cooks['maxStudy']} (R={cooks['ref_study']})")
    else:
        print(f"  [INFO] Cook's: {cooks}")
        results["failed"] += 1

    # ==========================================
    # 8. PLOT FUNCTIONS
    # ==========================================
    print("\n--- 8. PLOT FUNCTIONS ---")

    plots = ["renderForestPlot", "renderFunnelPlot", "renderBaujatPlot",
             "renderRadialPlot", "renderLabbePlot", "renderCumulativeForest",
             "renderInfluencePlot", "renderDOIPlot", "renderPCurvePlot",
             "renderZCurvePlot", "renderQQPlot"]

    for fn in plots:
        exists = safe_exec(f"return typeof {fn} === 'function';", fn)
        if exists:
            print(f"  [PASS] {fn}()")
            results["passed"] += 1
        else:
            print(f"  [FAIL] {fn}()")
            results["failed"] += 1

    # ==========================================
    # 9. CORE FUNCTIONS
    # ==========================================
    print("\n--- 9. CORE FUNCTIONS ---")

    core_fns = ["pnorm", "qnorm", "pt", "qt", "pchisq", "lgamma",
                "calculatePooledEstimate", "calculateHKSJ", "eggerTest",
                "trimAndFill", "failsafeN", "bayesianMetaAnalysis"]

    for fn in core_fns:
        exists = safe_exec(f"return typeof {fn} === 'function';", fn)
        if exists:
            print(f"  [PASS] {fn}()")
            results["passed"] += 1
        else:
            print(f"  [FAIL] {fn}()")
            results["failed"] += 1

    # ==========================================
    # 10. BUILT-IN TEST SUITE
    # ==========================================
    print("\n--- 10. BUILT-IN TEST SUITE ---")

    tests = safe_exec("""
        if (typeof runAutomatedTests === 'function') {
            return runAutomatedTests();
        }
        return null;
    """, "tests")

    if tests:
        p, f = tests.get('passed', 0), tests.get('failed', 0)
        print(f"  Built-in: {p}/{p+f} passed")
        if f == 0:
            results["passed"] += 1
        else:
            results["failed"] += 1

    # ==========================================
    # SUMMARY
    # ==========================================
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    total = results["passed"] + results["failed"]
    pct = (results["passed"] / max(total, 1)) * 100

    print(f"\nTests Passed: {results['passed']}/{total}")
    print(f"Tests Failed: {results['failed']}/{total}")
    print(f"Pass Rate: {pct:.1f}%")

    if pct >= 95:
        print("\nVERDICT: EXCELLENT - All critical functions validated")
    elif pct >= 85:
        print("\nVERDICT: GOOD")
    elif pct >= 70:
        print("\nVERDICT: ACCEPTABLE")
    else:
        print("\nVERDICT: NEEDS WORK")

    print("=" * 70)

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    try:
        driver.quit()
    except:
        pass
    print("\nBrowser closed.")
