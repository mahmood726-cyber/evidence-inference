#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug why plots aren't rendering"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def main():
    print("=" * 70)
    print("DEBUGGING PLOT RENDERING")
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

        # Click Load Demo
        demo_btns = driver.find_elements(By.XPATH, '//button[contains(text(), "Demo")]')
        for btn in demo_btns:
            if btn.is_displayed() and 'load' in btn.text.lower():
                btn.click()
                print(f"Clicked: {btn.text}")
                time.sleep(2)
                break

        # Run analysis
        driver.execute_script("if (typeof runAnalysis === 'function') runAnalysis();")
        print("Called runAnalysis()")
        time.sleep(3)

        # Check AppState
        print("\n--- Checking AppState ---")
        app_state = driver.execute_script("""
            if (typeof AppState !== 'undefined') {
                return {
                    hasStudies: AppState.studies && AppState.studies.length > 0,
                    studyCount: AppState.studies ? AppState.studies.length : 0,
                    hasResults: AppState.results !== null,
                    resultsKeys: AppState.results ? Object.keys(AppState.results) : []
                };
            }
            return null;
        """)
        print(f"AppState: {app_state}")

        # Check for plot containers
        print("\n--- Checking Plot Containers ---")
        containers = driver.execute_script("""
            const containers = [];
            const divs = document.querySelectorAll('[id*="plot"], [id*="chart"], [id*="forest"], [id*="funnel"]');
            divs.forEach(d => {
                containers.push({
                    id: d.id,
                    visible: d.offsetParent !== null,
                    hasChildren: d.children.length > 0,
                    innerHTML: d.innerHTML.substring(0, 100)
                });
            });
            return containers;
        """)
        for c in containers[:10]:
            print(f"  {c['id']}: visible={c['visible']}, children={c['hasChildren']}")

        # Check if Plotly is available
        print("\n--- Checking Plotly ---")
        plotly_check = driver.execute_script("""
            return {
                plotlyExists: typeof Plotly !== 'undefined',
                plotlyVersion: typeof Plotly !== 'undefined' ? Plotly.version : 'N/A'
            };
        """)
        print(f"Plotly: {plotly_check}")

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

                // Find a container for the plot
                let container = document.getElementById('forest-plot') ||
                               document.getElementById('forestPlot') ||
                               document.querySelector('[id*="forest"]');

                if (!container) {
                    // Create one
                    container = document.createElement('div');
                    container.id = 'test-forest-plot';
                    container.style.width = '100%';
                    container.style.height = '500px';
                    document.body.appendChild(container);
                }

                // Check if renderForestPlot exists
                if (typeof renderForestPlot === 'function') {
                    renderForestPlot(yi, vi, labels, container.id);
                    return { success: true, method: 'renderForestPlot', container: container.id };
                }

                // Try direct Plotly
                if (typeof Plotly !== 'undefined') {
                    const trace = {
                        x: yi,
                        y: labels,
                        error_x: {
                            type: 'data',
                            array: vi.map(v => 1.96 * Math.sqrt(v)),
                            visible: true
                        },
                        mode: 'markers',
                        type: 'scatter',
                        orientation: 'h'
                    };

                    Plotly.newPlot(container.id, [trace], {
                        title: 'Forest Plot',
                        xaxis: { title: 'Effect Size' },
                        yaxis: { title: 'Study' }
                    });

                    return { success: true, method: 'direct Plotly', container: container.id };
                }

                return { error: 'No plot method available' };
            } catch (e) {
                return { error: e.message };
            }
        """)
        print(f"Manual plot result: {result}")

        # Check for any console errors
        print("\n--- Console Errors ---")
        logs = driver.get_log('browser')
        for log in logs:
            if log['level'] == 'SEVERE':
                print(f"  ERROR: {log['message'][:100]}")

        # Now check if plot appeared
        print("\n--- Checking for Plotly Plots After Manual Render ---")
        plots_after = driver.execute_script("""
            const plots = document.querySelectorAll('.js-plotly-plot');
            return {
                count: plots.length,
                ids: Array.from(plots).map(p => p.id)
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

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
