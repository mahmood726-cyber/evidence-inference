#!/usr/bin/env python3
"""Complete Edge Browser Validation - Using webdriver_manager"""

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

print("=" * 70)
print("COMPLETE EDGE BROWSER VALIDATION TEST v3")
print("TruthCert-PairwisePro - All Functions, Plots & Critical Gaps")
print("=" * 70)

# Setup Edge with auto driver management
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

print("\nInitializing Edge driver...")
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)
driver.set_script_timeout(30)

results = {"passed": 0, "failed": 0, "errors": []}

def safe_execute(script, test_name):
    """Execute script with timeout handling"""
    try:
        return driver.execute_script(script)
    except Exception as e:
        results["errors"].append(f"{test_name}: {str(e)[:50]}")
        return None

try:
    # Load page
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)
    print(f"Page loaded: {driver.title}")

    # ==========================================
    # SECTION 1: DEMO DATASETS (17)
    # ==========================================
    print("\n--- SECTION 1: DEMO DATASETS (17) ---")

    demos = safe_execute("return Object.keys(DEMO_DATASETS);", "demo_keys")
    if demos:
        for key in demos:
            info = safe_execute(f"return DEMO_DATASETS['{key}'];", f"demo_{key}")
            if info:
                count = info.get('studies', len(info.get('data', [])) if info.get('data') else 0)
                if count > 0:
                    print(f"  [PASS] {key} ({count} studies)")
                    results["passed"] += 1
                else:
                    print(f"  [FAIL] {key} (no studies)")
                    results["failed"] += 1

    # ==========================================
    # SECTION 2: CORE STATISTICAL FUNCTIONS
    # ==========================================
    print("\n--- SECTION 2: CORE FUNCTIONS ---")

    core_functions = [
        "pnorm", "qnorm", "dnorm", "pt", "qt", "pchisq", "lgamma",
        "estimateTau2_DL", "estimateTau2_REML", "estimateTau2_ML",
        "estimateTau2_PM", "estimateTau2_HS", "estimateTau2_SJ",
        "estimateTau2_HE", "estimateTau2_EB",
        "calculateHKSJ", "calculatePooledEstimate", "eggerTest",
        "trimAndFill", "failsafeN", "bayesianMetaAnalysis"
    ]

    for fn in core_functions:
        exists = safe_execute(f"return typeof {fn} === 'function';", f"fn_{fn}")
        if exists:
            print(f"  [PASS] {fn}()")
            results["passed"] += 1
        else:
            print(f"  [FAIL] {fn}() - not found")
            results["failed"] += 1

    # ==========================================
    # SECTION 3: CRITICAL GAP FUNCTIONS
    # ==========================================
    print("\n--- SECTION 3: CRITICAL GAP FUNCTIONS ---")

    gap_functions = [
        ("calculateMH_OR", "Mantel-Haenszel"),
        ("calculatePeto_OR", "Peto Method"),
        ("testExcessSignificance", "TES Test"),
        ("renderQQPlot", "QQ Plot"),
        ("getStandardizedResiduals", "Std Residuals"),
        ("influenceDiagnostics", "Cook's Distance")
    ]

    for fn, desc in gap_functions:
        exists = safe_execute(f"return typeof {fn} === 'function';", f"gap_{fn}")
        if exists:
            print(f"  [PASS] {fn}() - {desc}")
            results["passed"] += 1
        else:
            print(f"  [FAIL] {fn}() - {desc} NOT FOUND")
            results["failed"] += 1

    # ==========================================
    # SECTION 4: TAU2 VALIDATION vs R
    # ==========================================
    print("\n--- SECTION 4: TAU2 vs R/metafor ---")

    tau2_results = safe_execute("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        const ref = {
            DL: 0.308760, REML: 0.313243, ML: 0.280028, PM: 0.318094,
            HS: 0.228363, SJ: 0.345516, HE: 0.328564, EB: 0.318069
        };
        const results = {};
        for (const m of Object.keys(ref)) {
            const fn = window['estimateTau2_' + m];
            if (fn) {
                try {
                    const r = fn(yi, vi);
                    results[m] = {
                        js: r.tau2,
                        r: ref[m],
                        diff: Math.abs(r.tau2 - ref[m]),
                        pass: Math.abs(r.tau2 - ref[m]) < 0.01
                    };
                } catch(e) { results[m] = {error: e.message}; }
            }
        }
        return results;
    """, "tau2_validation")

    if tau2_results:
        for m, r in tau2_results.items():
            if r.get('pass'):
                print(f"  [PASS] {m}: JS={r['js']:.6f} R={r['r']:.6f}")
                results["passed"] += 1
            elif r.get('error'):
                print(f"  [FAIL] {m}: Error - {r['error']}")
                results["failed"] += 1
            else:
                print(f"  [FAIL] {m}: diff={r.get('diff', 'N/A')}")
                results["failed"] += 1
    else:
        print("  [ERROR] Could not run tau2 validation")
        results["failed"] += 8

    # ==========================================
    # SECTION 5: MANTEL-HAENSZEL vs R
    # ==========================================
    print("\n--- SECTION 5: MANTEL-HAENSZEL vs R ---")

    mh_result = safe_execute("""
        if (typeof calculateMH_OR !== 'function') return {error: 'MH not found'};
        const ai = [4, 6, 3, 62, 33, 180, 8, 505, 29, 17, 186, 5, 27];
        const bi = [119, 300, 228, 13536, 5036, 1361, 2537, 87886, 7470, 1699, 50448, 2493, 16886];
        const ci = [11, 29, 11, 248, 47, 372, 10, 499, 45, 65, 141, 3, 29];
        const di = [128, 274, 209, 12619, 5761, 1079, 619, 87892, 7232, 1600, 27197, 2338, 17825];
        try {
            const r = calculateMH_OR(ai, bi, ci, di);
            return { OR: r.OR, ref_OR: 0.622874 };
        } catch(e) { return {error: e.message}; }
    """, "mh_validation")

    if mh_result and not mh_result.get('error'):
        or_diff = abs(mh_result['OR'] - mh_result['ref_OR'])
        if or_diff < 0.05:
            print(f"  [PASS] MH OR: JS={mh_result['OR']:.4f} R={mh_result['ref_OR']:.4f}")
            results["passed"] += 1
        else:
            print(f"  [FAIL] MH OR: JS={mh_result['OR']:.4f} R={mh_result['ref_OR']:.4f}")
            results["failed"] += 1
    else:
        print(f"  [INFO] MH: {mh_result}")
        results["failed"] += 1

    # ==========================================
    # SECTION 6: PETO METHOD vs R
    # ==========================================
    print("\n--- SECTION 6: PETO METHOD vs R ---")

    peto_result = safe_execute("""
        if (typeof calculatePeto_OR !== 'function') return {error: 'Peto not found'};
        const ai = [4, 6, 3, 62, 33, 180, 8, 505, 29, 17, 186, 5, 27];
        const bi = [119, 300, 228, 13536, 5036, 1361, 2537, 87886, 7470, 1699, 50448, 2493, 16886];
        const ci = [11, 29, 11, 248, 47, 372, 10, 499, 45, 65, 141, 3, 29];
        const di = [128, 274, 209, 12619, 5761, 1079, 619, 87892, 7232, 1600, 27197, 2338, 17825];
        try {
            const r = calculatePeto_OR(ai, bi, ci, di);
            return { OR: r.OR, ref_OR: 0.6222295 };
        } catch(e) { return {error: e.message}; }
    """, "peto_validation")

    if peto_result and not peto_result.get('error'):
        or_diff = abs(peto_result['OR'] - peto_result['ref_OR'])
        if or_diff < 0.05:
            print(f"  [PASS] Peto OR: JS={peto_result['OR']:.4f} R={peto_result['ref_OR']:.4f}")
            results["passed"] += 1
        else:
            print(f"  [FAIL] Peto OR: JS={peto_result['OR']:.4f} R={peto_result['ref_OR']:.4f}")
            results["failed"] += 1
    else:
        print(f"  [INFO] Peto: {peto_result}")
        results["failed"] += 1

    # ==========================================
    # SECTION 7: TES vs R
    # ==========================================
    print("\n--- SECTION 7: TES vs R ---")

    tes_result = safe_execute("""
        if (typeof testExcessSignificance !== 'function') return {error: 'TES not found'};
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        try {
            const r = testExcessSignificance(yi, vi);
            return { observed: r.observed, expected: r.expected, ref_observed: 8 };
        } catch(e) { return {error: e.message}; }
    """, "tes_validation")

    if tes_result and not tes_result.get('error'):
        if tes_result['observed'] == tes_result['ref_observed']:
            print(f"  [PASS] TES Observed: {tes_result['observed']} (R={tes_result['ref_observed']})")
            results["passed"] += 1
        else:
            print(f"  [FAIL] TES Observed: {tes_result['observed']} (R={tes_result['ref_observed']})")
            results["failed"] += 1
    else:
        print(f"  [INFO] TES: {tes_result}")
        results["failed"] += 1

    # ==========================================
    # SECTION 8: COOK'S DISTANCE vs R
    # ==========================================
    print("\n--- SECTION 8: COOK'S DISTANCE vs R ---")

    cooks_result = safe_execute("""
        if (typeof influenceDiagnostics !== 'function') return {error: 'influence not found'};
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        try {
            const r = influenceDiagnostics(yi, vi);
            const maxCooksD = Math.max(...r.cooksD);
            return { maxCooksD: maxCooksD, ref_maxCooksD: 0.200266 };
        } catch(e) { return {error: e.message}; }
    """, "cooks_validation")

    if cooks_result and not cooks_result.get('error'):
        diff = abs(cooks_result['maxCooksD'] - cooks_result['ref_maxCooksD'])
        if diff < 0.1:
            print(f"  [PASS] Max Cook's D: {cooks_result['maxCooksD']:.4f} (R={cooks_result['ref_maxCooksD']:.4f})")
            results["passed"] += 1
        else:
            print(f"  [FAIL] Max Cook's D: {cooks_result['maxCooksD']:.4f} (R={cooks_result['ref_maxCooksD']:.4f})")
            results["failed"] += 1
    else:
        print(f"  [INFO] Cook's: {cooks_result}")
        results["failed"] += 1

    # ==========================================
    # SECTION 9: PLOT FUNCTIONS
    # ==========================================
    print("\n--- SECTION 9: PLOT FUNCTIONS ---")

    plot_functions = [
        "renderForestPlot", "renderFunnelPlot", "renderBaujatPlot",
        "renderRadialPlot", "renderLabbePlot", "renderCumulativeForest",
        "renderInfluencePlot", "renderDOIPlot", "renderPCurvePlot",
        "renderZCurvePlot", "renderQQPlot"
    ]

    for fn in plot_functions:
        exists = safe_execute(f"return typeof {fn} === 'function';", f"plot_{fn}")
        if exists:
            print(f"  [PASS] {fn}()")
            results["passed"] += 1
        else:
            print(f"  [FAIL] {fn}()")
            results["failed"] += 1

    # ==========================================
    # SECTION 10: BUILT-IN TEST SUITE
    # ==========================================
    print("\n--- SECTION 10: BUILT-IN TEST SUITE ---")

    test_suite = safe_execute("""
        if (typeof runAutomatedTests === 'function') {
            return runAutomatedTests();
        }
        return null;
    """, "builtin_tests")

    if test_suite:
        p = test_suite.get('passed', 0)
        f = test_suite.get('failed', 0)
        print(f"  Built-in tests: {p}/{p+f} passed")
        if f == 0:
            results["passed"] += 1
        else:
            results["failed"] += 1

    # ==========================================
    # FINAL SUMMARY
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
        print("\nVERDICT: EXCELLENT - All major systems validated")
    elif pct >= 85:
        print("\nVERDICT: GOOD - Application functioning correctly")
    elif pct >= 70:
        print("\nVERDICT: ACCEPTABLE - Minor issues detected")
    else:
        print("\nVERDICT: NEEDS ATTENTION - Issues detected")

    print("=" * 70)

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print("\nBrowser closed.")
