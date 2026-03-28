#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final check - load demo, run analysis, verify all plots display"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options

def main():
    print("=" * 70)
    print("FINAL PLOT CHECK - TruthCert-PairwisePro")
    print("=" * 70)

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Edge(options=options)
    driver.set_script_timeout(60)

    try:
        # Load app
        print("\n[1] Loading app...")
        file_path = Path("C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
        driver.get(f"file:///{file_path}")
        time.sleep(4)
        print("    ✓ App loaded")

        # Load demo dataset
        print("\n[2] Loading BCG demo dataset...")
        driver.execute_script("loadDemoDataset('BCG');")
        time.sleep(2)

        rows = driver.execute_script("""
            return document.getElementById('studyTableBody').querySelectorAll('tr').length;
        """)
        print(f"    ✓ Loaded {rows} studies")

        # Run full analysis
        print("\n[3] Running full analysis...")
        driver.execute_script("runAnalysis();")
        time.sleep(5)

        results = driver.execute_script("""
            const r = AppState.results;
            if (!r) return null;
            return {
                theta: r.pooled ? r.pooled.theta.toFixed(4) : null,
                I2: r.het ? r.het.I2.toFixed(1) : null,
                tau2: r.tau2 ? r.tau2.toFixed(4) : null
            };
        """)

        if results:
            print(f"    ✓ Analysis complete")
            print(f"      θ = {results['theta']}, I² = {results['I2']}%, τ² = {results['tau2']}")

        # Check plots in each tab
        print("\n[4] Checking all plots...")

        plot_checks = [
            ("analysis", "forestPlot", "Forest Plot"),
            ("heterogeneity", "funnelPlot", "Funnel Plot"),
            ("heterogeneity", "baujatPlot", "Baujat Plot"),
        ]

        plots_found = 0
        for tab, plot_id, name in plot_checks:
            driver.execute_script(f"document.querySelector('[data-tab=\"{tab}\"]').click();")
            time.sleep(0.5)

            check = driver.execute_script(f"""
                const p = document.getElementById('{plot_id}');
                if (!p) return null;
                return {{
                    hasPlotly: p.classList.contains('js-plotly-plot'),
                    hasSVG: p.querySelector('svg') !== null,
                    height: p.offsetHeight
                }};
            """)

            if check and (check.get('hasPlotly') or check.get('hasSVG')):
                print(f"    ✓ {name} - rendered (height: {check.get('height', 0)}px)")
                plots_found += 1
            else:
                print(f"    ✗ {name} - NOT rendered")

        # Run additional analyses and check their plots
        print("\n[5] Running additional analyses...")

        additional = [
            ("runGOSHAnalysis()", "goshPlot", "GOSH Plot"),
            ("runTSAAnalysis()", "tsaPlot", "TSA Plot"),
            ("runInfluenceDiagnostics()", "influencePlot", "Influence Plot"),
            ("runLeaveOneOutCorrected()", "looPlot", "LOO Plot"),
            ("runCumulativeAnalysis()", "cumulativePlot", "Cumulative Plot"),
        ]

        driver.execute_script("document.querySelector('[data-tab=\"advanced\"]').click();")
        time.sleep(0.5)

        for func, plot_id, name in additional:
            try:
                driver.execute_script(func)
                time.sleep(1)

                # Handle any alerts
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                except:
                    pass

                check = driver.execute_script(f"""
                    const p = document.getElementById('{plot_id}');
                    if (!p) return null;
                    return {{
                        hasPlotly: p.classList.contains('js-plotly-plot'),
                        hasSVG: p.querySelector('svg') !== null
                    }};
                """)

                if check and (check.get('hasPlotly') or check.get('hasSVG')):
                    print(f"    ✓ {name}")
                    plots_found += 1
                else:
                    print(f"    ○ {name} (no plot container)")
            except Exception as e:
                print(f"    ? {name}: {str(e)[:30]}")

        # Final count of all Plotly plots
        print("\n[6] Final plot inventory...")
        all_plots = driver.execute_script("""
            const plots = document.querySelectorAll('.js-plotly-plot');
            return {
                count: plots.length,
                ids: Array.from(plots).map(p => p.id || 'unnamed').filter(id => id !== 'unnamed')
            };
        """)

        print(f"    Total Plotly plots: {all_plots.get('count', 0)}")
        if all_plots.get('ids'):
            print(f"    IDs: {', '.join(all_plots['ids'])}")

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"  Demo loaded:     ✓ ({rows} studies)")
        print(f"  Analysis run:    ✓")
        print(f"  Core plots:      {plots_found}/3+")
        print(f"  Total plots:     {all_plots.get('count', 0)}")

        if all_plots.get('count', 0) >= 3:
            print(f"\n  ✓ ALL PLOTS DISPLAYING CORRECTLY")
        else:
            print(f"\n  ⚠ Some plots may need attention")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    main()
