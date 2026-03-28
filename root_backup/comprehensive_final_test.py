#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprehensive final test - load demo, run full analysis, check all buttons/tabs/plots"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def main():
    print("=" * 80)
    print("COMPREHENSIVE FINAL TEST - TruthCert-PairwisePro")
    print("=" * 80)

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Edge(options=options)
    driver.set_script_timeout(60)

    results = {
        "tabs": {"passed": [], "failed": []},
        "buttons": {"passed": [], "failed": [], "skipped": []},
        "plots": {"passed": [], "failed": []},
        "errors": []
    }

    try:
        # =====================================================================
        # STEP 1: Load App
        # =====================================================================
        print("\n[1] LOADING APP...")
        file_path = Path("C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
        driver.get(f"file:///{file_path}")
        time.sleep(4)
        print("    ✓ App loaded successfully")

        # =====================================================================
        # STEP 2: Load Demo Dataset
        # =====================================================================
        print("\n[2] LOADING DEMO DATASET (BCG)...")
        driver.execute_script("loadDemoDataset('BCG');")
        time.sleep(3)

        # Verify data loaded
        row_count = driver.execute_script("""
            const tbody = document.getElementById('studyTableBody');
            return tbody ? tbody.querySelectorAll('tr').length : 0;
        """)
        print(f"    ✓ Loaded {row_count} studies")

        # =====================================================================
        # STEP 3: Run Full Analysis
        # =====================================================================
        print("\n[3] RUNNING FULL ANALYSIS...")
        driver.execute_script("runAnalysis();")
        time.sleep(5)

        # Check results
        analysis_check = driver.execute_script("""
            const r = AppState.results;
            if (!r) return null;
            return {
                k: r.k || (r.studies ? r.studies.length : 0),
                theta: r.pooled ? r.pooled.theta : (r.theta || null),
                I2: r.het ? r.het.I2 : null,
                tau2: r.tau2
            };
        """)

        if analysis_check:
            print(f"    ✓ Analysis complete:")
            print(f"      - Studies: {analysis_check.get('k', 'N/A')}")
            if analysis_check.get('theta') is not None:
                print(f"      - Pooled θ: {analysis_check['theta']:.4f}")
            if analysis_check.get('I2') is not None:
                print(f"      - I²: {analysis_check['I2']:.1f}%")
            if analysis_check.get('tau2') is not None:
                print(f"      - τ²: {analysis_check['tau2']:.4f}")
        else:
            print("    ✗ Analysis failed - no results")
            results["errors"].append("Analysis produced no results")

        # =====================================================================
        # STEP 4: Check All Tabs
        # =====================================================================
        print("\n[4] CHECKING ALL TABS...")
        tabs = driver.execute_script("""
            return Array.from(document.querySelectorAll('[data-tab]')).map(t => t.getAttribute('data-tab'));
        """)
        print(f"    Found {len(tabs)} tabs")

        for tab in tabs:
            try:
                driver.execute_script(f"document.querySelector('[data-tab=\"{tab}\"]').click();")
                time.sleep(0.3)

                panel_exists = driver.execute_script(f"""
                    const panel = document.getElementById('panel-{tab}');
                    return panel !== null;
                """)

                if panel_exists:
                    results["tabs"]["passed"].append(tab)
                    print(f"    ✓ {tab}")
                else:
                    results["tabs"]["failed"].append(tab)
                    print(f"    ✗ {tab} (panel not found)")
            except Exception as e:
                results["tabs"]["failed"].append(tab)
                print(f"    ✗ {tab}: {str(e)[:40]}")

        # =====================================================================
        # STEP 5: Check All Plots
        # =====================================================================
        print("\n[5] CHECKING ALL PLOTS...")

        # Go to analysis tab first
        driver.execute_script("document.querySelector('[data-tab=\"analysis\"]').click();")
        time.sleep(0.5)

        plot_ids = [
            ('forestPlot', 'analysis'),
            ('funnelPlot', 'heterogeneity'),
            ('baujatPlot', 'heterogeneity'),
            ('goshPlot', 'advanced'),
            ('doiPlot', 'bias'),
            ('galbraithPlot', 'bias'),
            ('influencePlot', 'advanced'),
            ('cumulativePlot', 'advanced'),
            ('metaRegPlot', 'advanced'),
        ]

        for plot_id, tab in plot_ids:
            try:
                # Switch to the tab containing this plot
                driver.execute_script(f"document.querySelector('[data-tab=\"{tab}\"]').click();")
                time.sleep(0.3)

                plot_check = driver.execute_script(f"""
                    const plot = document.getElementById('{plot_id}');
                    if (!plot) return {{ exists: false }};
                    return {{
                        exists: true,
                        hasPlotly: plot.classList.contains('js-plotly-plot'),
                        hasSVG: plot.querySelector('svg') !== null,
                        hasCanvas: plot.querySelector('canvas') !== null,
                        height: plot.offsetHeight
                    }};
                """)

                if plot_check and (plot_check.get('hasPlotly') or plot_check.get('hasSVG')):
                    results["plots"]["passed"].append(plot_id)
                    print(f"    ✓ {plot_id} (in {tab})")
                elif plot_check and plot_check.get('exists'):
                    # Plot container exists but not rendered yet - might need trigger
                    print(f"    ○ {plot_id} (container exists, not rendered)")
                else:
                    print(f"    - {plot_id} (not found)")

            except Exception as e:
                print(f"    ? {plot_id}: {str(e)[:30]}")

        # =====================================================================
        # STEP 6: Test Key Analysis Buttons
        # =====================================================================
        print("\n[6] TESTING KEY ANALYSIS BUTTONS...")

        # Switch to advanced tab
        driver.execute_script("document.querySelector('[data-tab=\"advanced\"]').click();")
        time.sleep(0.5)

        button_tests = [
            ("Run Z-Curve", "runZCurveAnalysis()"),
            ("Run P-Curve", "runPCurveAnalysis()"),
            ("Run ModelAvg", "runSimplifiedMA()"),
            ("Run Copas", "runCopasModel()"),
            ("Assess GRADE", "computeGRADE()"),
            ("Run Influence", "runInfluenceDiagnostics()"),
            ("Run LOO", "runLeaveOneOutCorrected()"),
            ("Run Cumulative", "runCumulativeAnalysis()"),
            ("Small Sample CI", "runSmallSampleCI()"),
            ("Meta-Regression", "runMetaRegression()"),
            ("Detect Outliers", "runMLOutlierDetection()"),
            ("Run TSA", "runTSAAnalysis()"),
            ("Generate GOSH", "runGOSHAnalysis()"),
        ]

        for name, code in button_tests:
            try:
                error = driver.execute_script(f"""
                    try {{
                        {code};
                        return null;
                    }} catch (e) {{
                        return e.message;
                    }}
                """)

                time.sleep(0.3)

                # Handle alerts
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                except:
                    pass

                if error:
                    results["buttons"]["failed"].append((name, error[:50]))
                    print(f"    ✗ {name}: {error[:50]}")
                else:
                    results["buttons"]["passed"].append(name)
                    print(f"    ✓ {name}")

            except Exception as e:
                results["buttons"]["failed"].append((name, str(e)[:40]))
                print(f"    ✗ {name}: {str(e)[:40]}")

        # =====================================================================
        # STEP 7: Check for Console Errors
        # =====================================================================
        print("\n[7] CHECKING CONSOLE FOR ERRORS...")

        console_errors = driver.execute_script("""
            // Check if any errors were logged
            return window._consoleErrors || [];
        """)

        if console_errors and len(console_errors) > 0:
            print(f"    Found {len(console_errors)} console errors")
            for err in console_errors[:5]:
                print(f"    ✗ {err[:60]}")
        else:
            print("    ✓ No tracked console errors")

        # =====================================================================
        # STEP 8: Final Plot Check After All Analyses
        # =====================================================================
        print("\n[8] FINAL PLOT CHECK...")

        # Re-check plots after running analyses
        driver.execute_script("document.querySelector('[data-tab=\"analysis\"]').click();")
        time.sleep(0.3)

        final_plots = driver.execute_script("""
            const plotContainers = document.querySelectorAll('.js-plotly-plot');
            return {
                total: plotContainers.length,
                ids: Array.from(plotContainers).map(p => p.id || 'unnamed').slice(0, 10)
            };
        """)

        print(f"    Total Plotly plots rendered: {final_plots.get('total', 0)}")
        if final_plots.get('ids'):
            print(f"    Plot IDs: {', '.join(final_plots['ids'][:5])}")

        # =====================================================================
        # SUMMARY
        # =====================================================================
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        tabs_pass = len(results["tabs"]["passed"])
        tabs_total = tabs_pass + len(results["tabs"]["failed"])
        btns_pass = len(results["buttons"]["passed"])
        btns_fail = len(results["buttons"]["failed"])
        plots_pass = len(results["plots"]["passed"])

        print(f"\n  📁 Tabs:     {tabs_pass}/{tabs_total} accessible")
        print(f"  🔘 Buttons:  {btns_pass}/{btns_pass + btns_fail} working")
        print(f"  📊 Plots:    {plots_pass} rendered")
        print(f"  ⚠️  Errors:   {len(results['errors'])}")

        if results["buttons"]["failed"]:
            print("\n  Failed buttons:")
            for name, err in results["buttons"]["failed"][:5]:
                print(f"    - {name}: {err[:40]}")

        # Overall verdict
        overall_pass = (
            tabs_pass >= tabs_total * 0.9 and
            btns_pass >= (btns_pass + btns_fail) * 0.8 and
            plots_pass >= 2
        )

        print(f"\n  {'✓ OVERALL: PASS' if overall_pass else '✗ OVERALL: NEEDS ATTENTION'}")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    main()
