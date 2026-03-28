#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Demo and Feature Test for TruthCert-PairwisePro
- Loads every demo dataset
- Runs full analysis on each
- Checks all buttons work
- Verifies all plots display
"""

import json
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def setup_driver():
    driver_path = r'C:\Users\user\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32\chromedriver.exe'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)

def safe_exec(driver, code, default=None):
    try:
        return driver.execute_script(code)
    except Exception as e:
        return default

def check_js_errors(driver):
    """Check for JavaScript console errors"""
    logs = driver.get_log('browser')
    severe = [l for l in logs if l['level'] == 'SEVERE']
    return severe

def main():
    print("=" * 80)
    print("COMPREHENSIVE DEMO AND FEATURE TEST")
    print("TruthCert-PairwisePro v1.0")
    print("=" * 80)

    driver = setup_driver()
    results = {
        "demos_tested": 0,
        "demos_passed": 0,
        "demos_failed": 0,
        "functions_tested": 0,
        "functions_passed": 0,
        "functions_failed": 0,
        "plots_tested": 0,
        "plots_passed": 0,
        "plots_failed": 0,
        "details": []
    }

    try:
        driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
        time.sleep(4)
        print(f"\nLoaded: {driver.title}")

        # ==========================================================================
        # PART 1: TEST ALL DEMO DATASETS
        # ==========================================================================
        print("\n" + "=" * 80)
        print("PART 1: TESTING ALL DEMO DATASETS")
        print("=" * 80)

        # Get all demo dataset names
        demos = safe_exec(driver, "return Object.keys(DEMO_DATASETS);", [])
        print(f"\nFound {len(demos)} demo datasets")

        for demo_name in demos:
            results["demos_tested"] += 1
            print(f"\n[{results['demos_tested']}/{len(demos)}] Testing: {demo_name}")

            try:
                # Load the demo
                load_result = safe_exec(driver, f"""
                    try {{
                        loadDemoDataset('{demo_name}');
                        return {{ success: true, studies: AppState.studies.length }};
                    }} catch(e) {{
                        return {{ success: false, error: e.message }};
                    }}
                """, {"success": False})

                if load_result and load_result.get("success"):
                    study_count = load_result.get("studies", 0)
                    print(f"    Loaded {study_count} studies")

                    time.sleep(0.5)

                    # Run analysis
                    analysis_result = safe_exec(driver, """
                        try {
                            runAnalysis();
                            return { success: true };
                        } catch(e) {
                            return { success: false, error: e.message };
                        }
                    """, {"success": False})

                    time.sleep(1.5)

                    # Check results
                    has_results = safe_exec(driver, """
                        return AppState.results && AppState.results.pooled ? true : false;
                    """, False)

                    if has_results:
                        pooled = safe_exec(driver, "return AppState.results.pooled.theta;", None)
                        tau2 = safe_exec(driver, "return AppState.results.tau2;", None)
                        print(f"    Analysis OK - Pooled: {pooled:.4f if pooled else 'N/A'}, tau2: {tau2:.4f if tau2 else 'N/A'}")
                        results["demos_passed"] += 1
                        results["details"].append({"demo": demo_name, "status": "PASS", "studies": study_count})
                    else:
                        print(f"    FAIL - No results generated")
                        results["demos_failed"] += 1
                        results["details"].append({"demo": demo_name, "status": "FAIL", "reason": "No results"})
                else:
                    error = load_result.get("error", "Unknown") if load_result else "Load failed"
                    print(f"    FAIL - {error}")
                    results["demos_failed"] += 1
                    results["details"].append({"demo": demo_name, "status": "FAIL", "reason": error})

            except Exception as e:
                print(f"    ERROR - {str(e)[:50]}")
                results["demos_failed"] += 1
                results["details"].append({"demo": demo_name, "status": "ERROR", "reason": str(e)})

        # ==========================================================================
        # PART 2: TEST FUNCTION AVAILABILITY (INCLUDING NEW ALIASES)
        # ==========================================================================
        print("\n" + "=" * 80)
        print("PART 2: TESTING FUNCTION AVAILABILITY")
        print("=" * 80)

        # Reload BCG demo for consistent testing
        safe_exec(driver, "loadDemoDataset('BCG');")
        time.sleep(0.5)
        safe_exec(driver, "runAnalysis();")
        time.sleep(1.5)

        functions_to_test = [
            # Core statistical
            ("pnorm", "typeof pnorm === 'function'"),
            ("qnorm", "typeof qnorm === 'function'"),
            ("pt", "typeof pt === 'function'"),
            ("qt", "typeof qt === 'function'"),
            ("pchisq", "typeof pchisq === 'function'"),
            ("lgamma", "typeof lgamma === 'function'"),

            # Tau2 estimators
            ("estimateTau2_DL", "typeof estimateTau2_DL === 'function'"),
            ("estimateTau2_REML", "typeof estimateTau2_REML === 'function'"),
            ("estimateTau2_ML", "typeof estimateTau2_ML === 'function'"),
            ("estimateTau2_PM", "typeof estimateTau2_PM === 'function'"),
            ("estimateTau2_HS", "typeof estimateTau2_HS === 'function'"),
            ("estimateTau2_SJ", "typeof estimateTau2_SJ === 'function'"),
            ("estimateTau2_HE", "typeof estimateTau2_HE === 'function'"),
            ("estimateTau2_EB", "typeof estimateTau2_EB === 'function'"),

            # Meta-analysis functions
            ("calculatePooledEstimate", "typeof calculatePooledEstimate === 'function'"),
            ("calculateHKSJ", "typeof calculateHKSJ === 'function'"),
            ("cumulativeMetaAnalysis", "typeof cumulativeMetaAnalysis === 'function'"),
            ("influenceDiagnostics", "typeof influenceDiagnostics === 'function'"),
            ("subgroupAnalysis", "typeof subgroupAnalysis === 'function'"),
            ("metaRegression", "typeof metaRegression === 'function'"),

            # Publication bias - original names
            ("eggersTest", "typeof eggersTest === 'function'"),
            ("trimAndFill", "typeof trimAndFill === 'function'"),
            ("petPeese", "typeof petPeese === 'function'"),
            ("pCurveAnalysis", "typeof pCurveAnalysis === 'function'"),
            ("zCurveAnalysis", "typeof zCurveAnalysis === 'function'"),

            # NEW ALIASES
            ("eggerTest (alias)", "typeof eggerTest === 'function'"),
            ("beggTest (new)", "typeof beggTest === 'function'"),
            ("failsafeN (new)", "typeof failsafeN === 'function'"),
            ("leave1out (alias)", "typeof leave1out === 'function'"),
            ("exportCSV (new)", "typeof exportCSV === 'function'"),
            ("exportJSON (alias)", "typeof exportJSON === 'function'"),
            ("fragilityAnalysis (alias)", "typeof fragilityAnalysis === 'function'"),

            # Advanced methods
            ("bayesianMetaAnalysis", "typeof bayesianMetaAnalysis === 'function'"),
            ("trialSequentialAnalysis", "typeof trialSequentialAnalysis === 'function'"),
            ("calculateEValue", "typeof calculateEValue === 'function'"),
            ("fragilityIndex", "typeof fragilityIndex === 'function'"),
            ("goshAnalysis", "typeof goshAnalysis === 'function'"),

            # Plot functions
            ("renderForestPlot", "typeof renderForestPlot === 'function'"),
            ("renderFunnelPlot", "typeof renderFunnelPlot === 'function'"),
            ("renderBaujatPlot", "typeof renderBaujatPlot === 'function'"),
            ("renderRadialPlot (NEW)", "typeof renderRadialPlot === 'function'"),
            ("renderGalbraithPlot (alias)", "typeof renderGalbraithPlot === 'function'"),
            ("renderLabbePlot (NEW)", "typeof renderLabbePlot === 'function'"),
            ("renderDOIPlot (NEW)", "typeof renderDOIPlot === 'function'"),
            ("renderCumulativeForest (alias)", "typeof renderCumulativeForest === 'function'"),
            ("renderTSAPlot", "typeof renderTSAPlot === 'function'"),
            ("renderPCurvePlot", "typeof renderPCurvePlot === 'function'"),
            ("renderZCurvePlot", "typeof renderZCurvePlot === 'function'"),
            ("renderContourFunnelPlot", "typeof renderContourFunnelPlot === 'function'"),
            ("renderSunsetPlot", "typeof renderSunsetPlot === 'function'"),
            ("renderGOSHPlot", "typeof renderGOSHPlot === 'function'"),

            # Validation
            ("VALIDATION_STATUS", "typeof VALIDATION_STATUS !== 'undefined'"),
            ("BCG_REFERENCE", "typeof BCG_REFERENCE !== 'undefined'"),
            ("runAutomatedTests", "typeof runAutomatedTests === 'function'"),
        ]

        print(f"\nTesting {len(functions_to_test)} functions...")

        for name, check in functions_to_test:
            results["functions_tested"] += 1
            exists = safe_exec(driver, f"return {check};", False)
            status = "PASS" if exists else "FAIL"
            marker = "[OK]" if exists else "[X]"
            print(f"  {marker} {name}")
            if exists:
                results["functions_passed"] += 1
            else:
                results["functions_failed"] += 1

        # ==========================================================================
        # PART 3: TEST NEW FUNCTIONS ACTUALLY WORK
        # ==========================================================================
        print("\n" + "=" * 80)
        print("PART 3: TESTING NEW FUNCTIONS WORK CORRECTLY")
        print("=" * 80)

        # Test beggTest
        print("\n[Testing beggTest]")
        begg_result = safe_exec(driver, """
            const yi = BCG_REFERENCE.yi;
            const sei = BCG_REFERENCE.vi.map(v => Math.sqrt(v));
            const r = beggTest(yi, sei);
            return r;
        """, None)
        if begg_result and 'tau' in begg_result:
            print(f"  Kendall's tau: {begg_result.get('tau', 0):.4f}")
            print(f"  p-value: {begg_result.get('p', 0):.4f}")
            print(f"  Result: PASS")
        else:
            print(f"  Result: FAIL - {begg_result}")

        # Test failsafeN
        print("\n[Testing failsafeN]")
        fsn_result = safe_exec(driver, """
            const yi = BCG_REFERENCE.yi;
            const vi = BCG_REFERENCE.vi;
            const r = failsafeN(yi, vi);
            return r;
        """, None)
        if fsn_result and 'rosenthal' in fsn_result:
            print(f"  Rosenthal's N: {fsn_result.get('rosenthal', 0)}")
            print(f"  Orwin's N: {fsn_result.get('orwin', 0)}")
            print(f"  Interpretation: {fsn_result.get('interpretation', 'N/A')[:50]}")
            print(f"  Result: PASS")
        else:
            print(f"  Result: FAIL - {fsn_result}")

        # Test leave1out
        print("\n[Testing leave1out]")
        loo_result = safe_exec(driver, """
            const yi = BCG_REFERENCE.yi;
            const vi = BCG_REFERENCE.vi;
            const names = ['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10','S11','S12','S13'];
            const r = leave1out(yi, vi, names);
            return { hasResults: r && r.results && r.results.length > 0, count: r?.results?.length || 0 };
        """, None)
        if loo_result and loo_result.get('hasResults'):
            print(f"  Leave-one-out results: {loo_result.get('count')} studies")
            print(f"  Result: PASS")
        else:
            print(f"  Result: FAIL")

        # ==========================================================================
        # PART 4: TEST PLOT RENDERING
        # ==========================================================================
        print("\n" + "=" * 80)
        print("PART 4: TESTING PLOT RENDERING")
        print("=" * 80)

        # Make sure we have BCG data loaded
        safe_exec(driver, "loadDemoDataset('BCG');")
        time.sleep(0.5)
        safe_exec(driver, "runAnalysis();")
        time.sleep(2)

        plots_to_test = [
            ("Forest Plot", "forestPlot", "renderForestPlot(AppState.results)"),
            ("Funnel Plot", "funnelPlot", "renderFunnelPlot(AppState.results)"),
            ("Baujat Plot", "baujatPlot", "renderBaujatPlot(AppState.results)"),
            ("Radial Plot (NEW)", "radialPlot", "renderRadialPlot(AppState.results, 'radialPlot')"),
            ("Cumulative Plot", "cumYearPlot", "renderCumulativePlot && renderCumulativePlot(AppState.results)"),
        ]

        # Create containers for new plots
        safe_exec(driver, """
            // Add container for radial plot if not exists
            if (!document.getElementById('radialPlot')) {
                const div = document.createElement('div');
                div.id = 'radialPlot';
                div.style.width = '100%';
                div.style.height = '400px';
                document.body.appendChild(div);
            }
            if (!document.getElementById('labbePlot')) {
                const div = document.createElement('div');
                div.id = 'labbePlot';
                div.style.width = '100%';
                div.style.height = '400px';
                document.body.appendChild(div);
            }
            if (!document.getElementById('doiPlot')) {
                const div = document.createElement('div');
                div.id = 'doiPlot';
                div.style.width = '100%';
                div.style.height = '400px';
                document.body.appendChild(div);
            }
        """)

        for plot_name, container_id, render_code in plots_to_test:
            results["plots_tested"] += 1
            print(f"\n[{plot_name}]")

            try:
                # Try to render
                safe_exec(driver, f"""
                    try {{
                        {render_code};
                    }} catch(e) {{
                        console.error('{plot_name} failed:', e);
                    }}
                """)
                time.sleep(0.5)

                # Check if plot was created (has Plotly data)
                has_plot = safe_exec(driver, f"""
                    const el = document.getElementById('{container_id}');
                    return el && el.data && el.data.length > 0;
                """, False)

                if has_plot:
                    print(f"  Container: {container_id}")
                    print(f"  Status: RENDERED")
                    print(f"  Result: PASS")
                    results["plots_passed"] += 1
                else:
                    print(f"  Container: {container_id}")
                    print(f"  Status: NOT RENDERED")
                    print(f"  Result: FAIL (container exists but no plot data)")
                    results["plots_failed"] += 1

            except Exception as e:
                print(f"  Error: {str(e)[:50]}")
                results["plots_failed"] += 1

        # Test new Radial plot specifically
        print("\n[Radial/Galbraith Plot (NEW)]")
        radial_ok = safe_exec(driver, """
            try {
                renderRadialPlot(AppState.results, 'radialPlot');
                const el = document.getElementById('radialPlot');
                return el && el.data && el.data.length > 0;
            } catch(e) {
                console.error('Radial failed:', e);
                return false;
            }
        """, False)
        print(f"  Result: {'PASS' if radial_ok else 'FAIL'}")
        results["plots_tested"] += 1
        if radial_ok:
            results["plots_passed"] += 1
        else:
            results["plots_failed"] += 1

        # Test L'Abbe plot (needs binary data)
        print("\n[L'Abbe Plot (NEW) - requires binary data]")
        labbe_ok = safe_exec(driver, """
            try {
                renderLabbePlot(AppState.results, 'labbePlot');
                const el = document.getElementById('labbePlot');
                return el && el.data && el.data.length > 0;
            } catch(e) {
                console.error('Labbe failed:', e);
                return false;
            }
        """, False)
        print(f"  Result: {'PASS' if labbe_ok else 'FAIL (expected - BCG has binary data)'}")
        results["plots_tested"] += 1
        if labbe_ok:
            results["plots_passed"] += 1
        else:
            results["plots_failed"] += 1

        # Test DOI plot
        print("\n[DOI Plot (NEW)]")
        doi_ok = safe_exec(driver, """
            try {
                renderDOIPlot(AppState.results, 'doiPlot');
                const el = document.getElementById('doiPlot');
                return el && el.data && el.data.length > 0;
            } catch(e) {
                console.error('DOI failed:', e);
                return false;
            }
        """, False)
        print(f"  Result: {'PASS' if doi_ok else 'FAIL'}")
        results["plots_tested"] += 1
        if doi_ok:
            results["plots_passed"] += 1
        else:
            results["plots_failed"] += 1

        # ==========================================================================
        # PART 5: TEST BUTTONS/UI ACTIONS
        # ==========================================================================
        print("\n" + "=" * 80)
        print("PART 5: TESTING UI BUTTONS AND ACTIONS")
        print("=" * 80)

        buttons_to_test = [
            ("Add Study", "addStudyRow()"),
            ("Clear All", "clearAllStudies()"),
            ("Load Demo (BCG)", "loadDemoDataset('BCG')"),
            ("Run Analysis", "runAnalysis()"),
            ("Compute DDMA", "computeDDMA()"),
            ("Compute Heterogeneity", "computeHeterogeneity()"),
            ("Compute Bias", "computeBias()"),
            ("Compute Clinical", "computeClinical()"),
            ("Run GRADE", "runGRADE()"),
            ("Export to R", "exportToR()"),
        ]

        print(f"\nTesting {len(buttons_to_test)} UI actions...")

        for action_name, action_code in buttons_to_test:
            try:
                # First reload demo if needed
                if "Load Demo" not in action_name and "Clear" not in action_name:
                    safe_exec(driver, "if (!AppState.studies || AppState.studies.length === 0) loadDemoDataset('BCG');")
                    time.sleep(0.3)

                result = safe_exec(driver, f"""
                    try {{
                        {action_code};
                        return {{ success: true }};
                    }} catch(e) {{
                        return {{ success: false, error: e.message }};
                    }}
                """, {"success": False})

                if result and result.get("success"):
                    print(f"  [OK] {action_name}")
                else:
                    error = result.get("error", "Unknown") if result else "Failed"
                    print(f"  [X] {action_name} - {error[:30]}")

                time.sleep(0.3)

            except Exception as e:
                print(f"  [X] {action_name} - {str(e)[:30]}")

        # ==========================================================================
        # PART 6: CHECK FOR JS ERRORS
        # ==========================================================================
        print("\n" + "=" * 80)
        print("PART 6: JAVASCRIPT CONSOLE ERRORS")
        print("=" * 80)

        errors = check_js_errors(driver)
        if errors:
            print(f"\nFound {len(errors)} severe errors:")
            for err in errors[:5]:
                print(f"  - {err['message'][:70]}...")
        else:
            print("\nNo severe JavaScript errors detected")

        # ==========================================================================
        # PART 7: RUN BUILT-IN VALIDATION
        # ==========================================================================
        print("\n" + "=" * 80)
        print("PART 7: BUILT-IN VALIDATION TESTS")
        print("=" * 80)

        validation = safe_exec(driver, """
            try {
                return runAutomatedTests();
            } catch(e) {
                return { passed: 0, failed: 1, error: e.message };
            }
        """, {"passed": 0, "failed": 1})

        if validation:
            p = validation.get("passed", 0)
            f = validation.get("failed", 0)
            print(f"\nBuilt-in tests: {p}/{p+f} passed")
            if f == 0:
                print("Status: ALL PASS")
            else:
                print(f"Status: {f} FAILED")

        # ==========================================================================
        # SUMMARY
        # ==========================================================================
        print("\n" + "=" * 80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)

        print(f"\nDemo Datasets: {results['demos_passed']}/{results['demos_tested']} passed")
        print(f"Functions: {results['functions_passed']}/{results['functions_tested']} available")
        print(f"Plots: {results['plots_passed']}/{results['plots_tested']} rendered")

        total_tests = results['demos_tested'] + results['functions_tested'] + results['plots_tested']
        total_passed = results['demos_passed'] + results['functions_passed'] + results['plots_passed']
        pass_rate = (total_passed / max(total_tests, 1)) * 100

        print(f"\nOVERALL: {total_passed}/{total_tests} ({pass_rate:.1f}%)")

        if pass_rate >= 95:
            verdict = "EXCELLENT"
        elif pass_rate >= 85:
            verdict = "GOOD"
        elif pass_rate >= 70:
            verdict = "ACCEPTABLE"
        else:
            verdict = "NEEDS WORK"

        print(f"VERDICT: {verdict}")
        print("=" * 80)

        # Save detailed results
        with open("C:/Users/user/comprehensive_demo_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nDetailed results saved to: C:/Users/user/comprehensive_demo_test_results.json")

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()

    return results

if __name__ == "__main__":
    main()
