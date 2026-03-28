#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug why plots aren't rendering - v2 with alert handling"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

def main():
    print("=" * 70)
    print("DEBUGGING PLOT RENDERING - V2")
    print("=" * 70)

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Edge(options=options)

    try:
        # Load app
        file_path = Path("C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
        driver.get(f"file:///{file_path}")
        time.sleep(3)
        print("App loaded")

        # Load demo data directly via JavaScript (bypass the prompt)
        print("\n--- Loading Demo Data via JS ---")
        load_result = driver.execute_script("""
            // Check if loadDemoData function exists
            if (typeof loadDemoData === 'function') {
                loadDemoData(1);  // Load first demo (SGLT2i - CV Death)
                return { success: true, method: 'loadDemoData(1)' };
            }

            // Alternative: Load via SAMPLE_DATASETS
            if (typeof SAMPLE_DATASETS !== 'undefined' && SAMPLE_DATASETS.length > 0) {
                const sample = SAMPLE_DATASETS[0];
                if (typeof AppState !== 'undefined') {
                    AppState.studies = sample.studies || sample.data;
                    return { success: true, method: 'SAMPLE_DATASETS', name: sample.name };
                }
            }

            // Try to find and trigger load sample
            if (typeof loadSample === 'function') {
                loadSample('bcg');
                return { success: true, method: 'loadSample(bcg)' };
            }

            return { success: false, error: 'No load method found' };
        """)
        print(f"Load result: {load_result}")
        time.sleep(2)

        # Check AppState
        print("\n--- Checking AppState after load ---")
        app_state = driver.execute_script("""
            if (typeof AppState !== 'undefined') {
                return {
                    hasStudies: AppState.studies && AppState.studies.length > 0,
                    studyCount: AppState.studies ? AppState.studies.length : 0,
                    firstStudy: AppState.studies && AppState.studies[0] ? AppState.studies[0] : null,
                    hasResults: AppState.results !== null,
                    resultsKeys: AppState.results ? Object.keys(AppState.results) : []
                };
            }
            return { error: 'AppState not defined' };
        """)
        print(f"AppState: {app_state}")

        # If no studies loaded, manually create test data
        if not app_state.get('hasStudies'):
            print("\n--- Creating test data manually ---")
            driver.execute_script("""
                AppState.studies = [
                    { study: 'Study 1', yi: 0.5, vi: 0.04, label: 'Study 1' },
                    { study: 'Study 2', yi: 0.3, vi: 0.05, label: 'Study 2' },
                    { study: 'Study 3', yi: 0.6, vi: 0.03, label: 'Study 3' },
                    { study: 'Study 4', yi: 0.2, vi: 0.06, label: 'Study 4' },
                    { study: 'Study 5', yi: 0.4, vi: 0.04, label: 'Study 5' }
                ];
            """)
            print("Test data created")
            time.sleep(1)

        # Run analysis
        print("\n--- Running Analysis ---")
        analysis_result = driver.execute_script("""
            try {
                if (typeof runAnalysis === 'function') {
                    runAnalysis();
                    return { success: true, method: 'runAnalysis()' };
                }
                return { error: 'runAnalysis not found' };
            } catch (e) {
                return { error: e.message };
            }
        """)
        print(f"Analysis result: {analysis_result}")
        time.sleep(3)

        # Check results
        print("\n--- Checking Results After Analysis ---")
        results = driver.execute_script("""
            if (typeof AppState !== 'undefined' && AppState.results) {
                return {
                    pooled: AppState.results.pooled ? {
                        estimate: AppState.results.pooled.estimate,
                        se: AppState.results.pooled.se,
                        ci_lower: AppState.results.pooled.ci_lower,
                        ci_upper: AppState.results.pooled.ci_upper,
                        method: AppState.results.pooled.method
                    } : null,
                    heterogeneity: AppState.results.heterogeneity ? {
                        I2: AppState.results.heterogeneity.I2,
                        tau2: AppState.results.heterogeneity.tau2
                    } : null,
                    keys: Object.keys(AppState.results)
                };
            }
            return { error: 'No results' };
        """)
        print(f"Results: {results}")

        # Check for plot containers
        print("\n--- Checking Plot Containers ---")
        containers = driver.execute_script("""
            const containers = [];
            const divs = document.querySelectorAll('[id*="plot"], [id*="chart"], [id*="forest"], [id*="funnel"]');
            divs.forEach(d => {
                containers.push({
                    id: d.id,
                    visible: d.offsetParent !== null,
                    hasChildren: d.children.length,
                    hasSVG: d.querySelector('svg') !== null,
                    hasPlotly: d.classList.contains('js-plotly-plot'),
                    display: window.getComputedStyle(d).display,
                    width: d.offsetWidth,
                    height: d.offsetHeight
                });
            });
            return containers;
        """)
        for c in containers[:15]:
            print(f"  {c['id']}: visible={c['visible']}, children={c['hasChildren']}, svg={c['hasSVG']}, plotly={c['hasPlotly']}, size={c['width']}x{c['height']}")

        # Check if Plotly is available
        print("\n--- Checking Plotly ---")
        plotly_check = driver.execute_script("""
            return {
                plotlyExists: typeof Plotly !== 'undefined',
                plotlyVersion: typeof Plotly !== 'undefined' ? Plotly.version : 'N/A'
            };
        """)
        print(f"Plotly: {plotly_check}")

        # Check if renderForestPlot exists and what it does
        print("\n--- Checking renderForestPlot ---")
        forest_check = driver.execute_script("""
            if (typeof renderForestPlot === 'function') {
                return {
                    exists: true,
                    length: renderForestPlot.length,  // number of parameters
                    code: renderForestPlot.toString().substring(0, 500)
                };
            }
            return { exists: false };
        """)
        print(f"renderForestPlot exists: {forest_check.get('exists')}")
        if forest_check.get('exists'):
            print(f"  Params: {forest_check.get('length')}")
            print(f"  Code preview: {forest_check.get('code', '')[:200]}...")

        # Try to manually render a forest plot
        print("\n--- Attempting Manual Forest Plot Render ---")
        result = driver.execute_script("""
            try {
                // Get the studies data
                if (typeof AppState === 'undefined' || !AppState.studies || AppState.studies.length === 0) {
                    return { error: 'No study data in AppState' };
                }

                const studies = AppState.studies;
                const yi = studies.map(s => s.yi);
                const vi = studies.map(s => s.vi);
                const labels = studies.map((s, i) => s.label || s.study || `Study ${i+1}`);

                console.log('Studies:', studies.length, 'yi:', yi, 'vi:', vi);

                // Find a container for the plot
                let container = document.getElementById('forest-plot') ||
                               document.getElementById('forestPlot') ||
                               document.getElementById('forest-plot-container') ||
                               document.querySelector('[id*="forest"]');

                if (!container) {
                    // Create one
                    container = document.createElement('div');
                    container.id = 'test-forest-plot';
                    container.style.width = '800px';
                    container.style.height = '500px';
                    container.style.backgroundColor = '#fff';
                    container.style.position = 'fixed';
                    container.style.top = '100px';
                    container.style.left = '100px';
                    container.style.zIndex = '9999';
                    container.style.border = '2px solid red';
                    document.body.appendChild(container);
                    console.log('Created test container');
                }

                console.log('Container:', container.id, container.offsetWidth, container.offsetHeight);

                // Check if renderForestPlot exists
                if (typeof renderForestPlot === 'function') {
                    console.log('Calling renderForestPlot...');
                    renderForestPlot(yi, vi, labels, container.id);
                    return { success: true, method: 'renderForestPlot', container: container.id };
                }

                // Try direct Plotly
                if (typeof Plotly !== 'undefined') {
                    console.log('Using direct Plotly...');
                    const se = vi.map(v => Math.sqrt(v));

                    const trace = {
                        x: yi,
                        y: labels,
                        error_x: {
                            type: 'data',
                            array: se.map(s => 1.96 * s),
                            visible: true
                        },
                        mode: 'markers',
                        type: 'scatter',
                        marker: { size: 10 }
                    };

                    Plotly.newPlot(container.id, [trace], {
                        title: 'Forest Plot (Debug)',
                        xaxis: { title: 'Effect Size', zeroline: true },
                        yaxis: { title: 'Study' },
                        showlegend: false
                    });

                    return { success: true, method: 'direct Plotly', container: container.id };
                }

                return { error: 'No plot method available' };
            } catch (e) {
                console.error('Plot error:', e);
                return { error: e.message, stack: e.stack };
            }
        """)
        print(f"Manual plot result: {result}")
        time.sleep(2)

        # Check for any console errors
        print("\n--- Console Logs ---")
        try:
            logs = driver.get_log('browser')
            for log in logs[-20:]:  # Last 20 logs
                level = log['level']
                msg = log['message'][:150]
                if level == 'SEVERE':
                    print(f"  ERROR: {msg}")
                elif 'plot' in msg.lower() or 'forest' in msg.lower() or 'plotly' in msg.lower():
                    print(f"  {level}: {msg}")
        except Exception as e:
            print(f"  Could not get logs: {e}")

        # Now check if plot appeared
        print("\n--- Checking for Plotly Plots After Manual Render ---")
        plots_after = driver.execute_script("""
            const plots = document.querySelectorAll('.js-plotly-plot');
            const svgs = document.querySelectorAll('svg.main-svg');
            return {
                plotlyPlots: plots.length,
                plotIds: Array.from(plots).map(p => p.id),
                svgCount: svgs.length,
                testContainer: document.getElementById('test-forest-plot') ? {
                    exists: true,
                    html: document.getElementById('test-forest-plot').innerHTML.substring(0, 200),
                    hasPlotly: document.getElementById('test-forest-plot').classList.contains('js-plotly-plot')
                } : { exists: false }
            };
        """)
        print(f"Plotly plots found: {plots_after}")

        # Keep browser open
        print("\n" + "=" * 70)
        print("Browser will stay open. Check manually and press Enter to close.")
        print("=" * 70)
        input()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        try:
            input("Press Enter to close...")
        except:
            pass

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
