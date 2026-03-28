#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug why plots aren't rendering - v3 with proper function calls"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    print("=" * 70)
    print("DEBUGGING PLOT RENDERING - V3")
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

        # Check what functions are available
        print("\n--- Checking Available Functions ---")
        funcs = driver.execute_script("""
            return {
                loadDemoDataset: typeof loadDemoDataset === 'function',
                DEMO_DATASETS: typeof DEMO_DATASETS !== 'undefined',
                runAnalysis: typeof runAnalysis === 'function',
                AppState: typeof AppState !== 'undefined',
                renderForestPlot: typeof renderForestPlot === 'function',
                Plotly: typeof Plotly !== 'undefined'
            };
        """)
        print(f"Functions: {funcs}")

        if not funcs.get('loadDemoDataset'):
            print("ERROR: loadDemoDataset not available")
            return

        # Load demo data directly
        print("\n--- Loading Demo Data via loadDemoDataset ---")
        load_result = driver.execute_script("""
            try {
                // Get first available demo key
                const keys = Object.keys(DEMO_DATASETS);
                console.log('Available demos:', keys);

                // Load BCG dataset (benchmark with multiple studies)
                if (keys.includes('BCG')) {
                    loadDemoDataset('BCG');
                    return { success: true, key: 'BCG', demo: DEMO_DATASETS['BCG'].name };
                } else {
                    loadDemoDataset(keys[0]);
                    return { success: true, key: keys[0], demo: DEMO_DATASETS[keys[0]].name };
                }
            } catch (e) {
                return { success: false, error: e.message };
            }
        """)
        print(f"Load result: {load_result}")
        time.sleep(2)

        # Check if data was loaded into the table
        print("\n--- Checking Table Data ---")
        table_data = driver.execute_script("""
            const tbody = document.getElementById('studyTableBody');
            if (!tbody) return { error: 'No table body found' };

            const rows = tbody.querySelectorAll('tr');
            return {
                rowCount: rows.length,
                firstRowContent: rows[0] ? rows[0].innerText.substring(0, 100) : 'No rows'
            };
        """)
        print(f"Table: {table_data}")

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
        time.sleep(4)

        # Handle any alerts that might appear
        try:
            alert = driver.switch_to.alert
            print(f"Alert appeared: {alert.text}")
            alert.accept()
            time.sleep(1)
        except:
            print("No alert appeared")

        # Check results
        print("\n--- Checking Results After Analysis ---")
        results = driver.execute_script("""
            if (typeof AppState !== 'undefined' && AppState.results) {
                return {
                    hasPooled: !!AppState.results.pooled,
                    pooledEstimate: AppState.results.pooled ? AppState.results.pooled.estimate : null,
                    hasHeterogeneity: !!AppState.results.heterogeneity,
                    I2: AppState.results.heterogeneity ? AppState.results.heterogeneity.I2 : null,
                    keys: Object.keys(AppState.results),
                    yi: AppState.results.yi ? AppState.results.yi.slice(0, 3) : null
                };
            }
            return { error: 'No results available' };
        """)
        print(f"Results: {results}")

        # Check for Plotly plots
        print("\n--- Checking for Plotly Plots ---")
        plots = driver.execute_script("""
            const plotlyPlots = document.querySelectorAll('.js-plotly-plot');
            const svgs = document.querySelectorAll('svg.main-svg');
            return {
                plotlyCount: plotlyPlots.length,
                svgCount: svgs.length,
                ids: Array.from(plotlyPlots).map(p => p.id)
            };
        """)
        print(f"Plots: {plots}")

        # Check all tabs
        print("\n--- Checking All Tabs ---")
        tabs = driver.execute_script("""
            const tabs = document.querySelectorAll('[data-tab]');
            return Array.from(tabs).map(t => ({
                tab: t.getAttribute('data-tab'),
                text: t.textContent.trim()
            }));
        """)
        print(f"Tabs: {tabs}")

        # Click on Analysis tab
        print("\n--- Switching to Analysis Tab ---")
        driver.execute_script("""
            const analysisTab = document.querySelector('[data-tab="analysis"]');
            if (analysisTab) analysisTab.click();
        """)
        time.sleep(1)

        # Check for forest plot container
        print("\n--- Checking Forest Plot Container ---")
        forest_info = driver.execute_script("""
            // Look for forest plot container
            const containers = [
                'forest-plot',
                'forestPlot',
                'forest-plot-container',
                'forest-chart'
            ];

            for (const id of containers) {
                const el = document.getElementById(id);
                if (el) {
                    return {
                        id: id,
                        visible: el.offsetParent !== null,
                        width: el.offsetWidth,
                        height: el.offsetHeight,
                        hasPlotly: el.classList.contains('js-plotly-plot'),
                        children: el.children.length,
                        innerHTML: el.innerHTML.substring(0, 200)
                    };
                }
            }

            // Check analysis panel
            const analysisPanel = document.getElementById('panel-analysis');
            if (analysisPanel) {
                const plots = analysisPanel.querySelectorAll('[id*="plot"], [id*="chart"], .js-plotly-plot');
                return {
                    inAnalysisPanel: true,
                    plotElements: Array.from(plots).map(p => p.id || p.className)
                };
            }

            return { error: 'No forest plot container found' };
        """)
        print(f"Forest info: {forest_info}")

        # Try to manually trigger forest plot render
        print("\n--- Attempting Manual Forest Plot Render ---")
        render_result = driver.execute_script("""
            try {
                const r = AppState.results;
                if (!r || !r.yi) {
                    return { error: 'No results data' };
                }

                const yi = r.yi;
                const vi = r.vi;
                const labels = r.labels || yi.map((_, i) => 'Study ' + (i+1));

                console.log('Manual render - yi:', yi, 'vi:', vi);

                // Find or create container
                let container = document.getElementById('forest-plot') ||
                               document.getElementById('forestPlot');

                if (!container) {
                    container = document.createElement('div');
                    container.id = 'manual-forest-plot';
                    container.style.width = '800px';
                    container.style.height = '500px';
                    container.style.position = 'fixed';
                    container.style.top = '50px';
                    container.style.left = '50px';
                    container.style.background = 'white';
                    container.style.border = '3px solid blue';
                    container.style.zIndex = '99999';
                    document.body.appendChild(container);
                }

                if (typeof renderForestPlot === 'function') {
                    renderForestPlot(yi, vi, labels, container.id);
                    return { success: true, method: 'renderForestPlot', container: container.id };
                }

                // Try direct Plotly
                if (typeof Plotly !== 'undefined') {
                    const se = vi.map(v => Math.sqrt(v));
                    const trace = {
                        x: yi,
                        y: labels,
                        error_x: { type: 'data', array: se.map(s => 1.96 * s) },
                        mode: 'markers',
                        type: 'scatter'
                    };

                    Plotly.newPlot(container.id, [trace], {
                        title: 'Forest Plot (Manual)',
                        xaxis: { title: 'Effect Size', zeroline: true },
                        yaxis: { title: '' }
                    });

                    return { success: true, method: 'direct Plotly', container: container.id };
                }

                return { error: 'No render method available' };
            } catch (e) {
                console.error('Render error:', e);
                return { error: e.message, stack: e.stack };
            }
        """)
        print(f"Manual render result: {render_result}")
        time.sleep(2)

        # Check for plots now
        print("\n--- Final Plot Check ---")
        final_plots = driver.execute_script("""
            const plots = document.querySelectorAll('.js-plotly-plot');
            return {
                count: plots.length,
                ids: Array.from(plots).map(p => p.id),
                visible: Array.from(plots).map(p => ({
                    id: p.id,
                    visible: p.offsetParent !== null,
                    width: p.offsetWidth,
                    height: p.offsetHeight
                }))
            };
        """)
        print(f"Final plots: {final_plots}")

        # Get console logs
        print("\n--- Console Logs ---")
        try:
            logs = driver.get_log('browser')
            for log in logs[-15:]:
                if log['level'] in ['SEVERE', 'WARNING']:
                    print(f"  {log['level']}: {log['message'][:120]}")
        except Exception as e:
            print(f"  Could not get logs: {e}")

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
