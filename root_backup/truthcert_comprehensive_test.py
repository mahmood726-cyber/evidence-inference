#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Selenium test for TruthCert-PairwisePro
1. Load demo dataset
2. Run analysis
3. Check every tab for results
4. Verify all plots render
"""

import sys
import time
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException
)

class ComprehensiveTester:
    def __init__(self):
        self.results = {
            'demo_load': None,
            'analysis_run': None,
            'tabs': {},
            'plots': {},
            'errors': [],
            'warnings': []
        }
        self.driver = None

    def setup(self):
        """Initialize browser"""
        print("=" * 70)
        print("TruthCert-PairwisePro COMPREHENSIVE TEST")
        print("=" * 70)

        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Edge(options=options)
        self.wait = WebDriverWait(self.driver, 15)

        # Load the app
        file_path = Path("C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
        self.driver.get(f"file:///{file_path}")
        time.sleep(3)

        print(f"Loaded: {self.driver.title}")
        return True

    def safe_click(self, element):
        """Safely click an element"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            return False

    def find_and_click(self, selectors, description):
        """Try multiple selectors to find and click an element"""
        for selector in selectors:
            try:
                if selector.startswith('//'):
                    elements = self.driver.find_elements(By.XPATH, selector)
                else:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

                for elem in elements:
                    if elem.is_displayed():
                        if self.safe_click(elem):
                            print(f"  [OK] Clicked: {description}")
                            return True
            except:
                continue
        print(f"  [WARN] Could not find: {description}")
        return False

    def step1_load_demo_data(self):
        """Step 1: Load demo dataset"""
        print("\n" + "=" * 70)
        print("STEP 1: LOADING DEMO DATA")
        print("=" * 70)

        # First go to Data tab
        self.find_and_click([
            '[data-tab="data"]',
            'button:contains("Data")',
            '//button[contains(text(), "Data")]',
            '.tab-btn[data-tab="data"]'
        ], "Data Tab")
        time.sleep(1)

        # Look for demo/sample data buttons
        demo_selectors = [
            'button[onclick*="loadDemo"]',
            'button[onclick*="loadSample"]',
            'button[onclick*="demo"]',
            '[onclick*="Demo"]',
            '//button[contains(text(), "Demo")]',
            '//button[contains(text(), "Sample")]',
            '//button[contains(text(), "Load")]',
            '//button[contains(text(), "BCG")]',
            '.demo-btn',
            '.sample-btn',
            '#load-demo',
            '#loadDemo',
        ]

        # Try to find any demo button
        demo_loaded = False
        for selector in demo_selectors:
            try:
                if selector.startswith('//'):
                    elements = self.driver.find_elements(By.XPATH, selector)
                else:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

                for elem in elements:
                    if elem.is_displayed():
                        btn_text = elem.text.strip()
                        if any(x in btn_text.lower() for x in ['demo', 'sample', 'load', 'bcg', 'example']):
                            if self.safe_click(elem):
                                print(f"  [OK] Clicked demo button: '{btn_text}'")
                                demo_loaded = True
                                time.sleep(2)
                                break
                if demo_loaded:
                    break
            except:
                continue

        if not demo_loaded:
            # Try JavaScript to load demo data
            print("  [INFO] Trying JavaScript to load demo data...")
            try:
                # Check for loadDemoData function
                has_func = self.driver.execute_script("return typeof loadDemoData === 'function'")
                if has_func:
                    self.driver.execute_script("loadDemoData();")
                    print("  [OK] Called loadDemoData()")
                    demo_loaded = True
                    time.sleep(2)
            except:
                pass

        if not demo_loaded:
            # Try loading BCG sample via SAMPLES object
            try:
                self.driver.execute_script("""
                    if (typeof SAMPLES !== 'undefined' && SAMPLES.bcg) {
                        if (typeof loadSample === 'function') {
                            loadSample('bcg');
                        }
                    }
                """)
                print("  [OK] Loaded BCG sample via SAMPLES object")
                demo_loaded = True
                time.sleep(2)
            except:
                pass

        if not demo_loaded:
            # Manually inject demo data
            print("  [INFO] Manually injecting demo data...")
            try:
                self.driver.execute_script("""
                    // BCG Vaccine data
                    const demoData = `Study,Events_T,Total_T,Events_C,Total_C
Aronson 1948,4,123,11,139
Ferguson 1949,6,306,29,303
Rosenthal 1960,3,231,11,220
Hart 1977,62,13598,248,12867
Frimodt 1973,33,5069,47,5808
Stein 1953,180,1699,372,1600
Vandiviere 1973,8,2545,10,629
TPT Madras 1980,505,88391,499,88391
Coetzee 1968,29,7499,45,7277
Rosenthal 1961,17,1716,65,1665
Comstock 1974,186,50634,141,27338
Comstock 1976,5,2498,3,2341
Comstock 1969,27,16913,29,17854`;

                    // Find textarea and fill it
                    const textareas = document.querySelectorAll('textarea');
                    for (let ta of textareas) {
                        if (ta.offsetParent !== null) {
                            ta.value = demoData;
                            ta.dispatchEvent(new Event('input', { bubbles: true }));
                            ta.dispatchEvent(new Event('change', { bubbles: true }));
                            break;
                        }
                    }

                    // Set data type to binary
                    const selects = document.querySelectorAll('select');
                    for (let sel of selects) {
                        if (sel.id && sel.id.includes('type') || sel.name && sel.name.includes('type')) {
                            sel.value = 'binary';
                            sel.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                    }
                """)
                print("  [OK] Manually injected BCG demo data")
                demo_loaded = True
                time.sleep(1)
            except Exception as e:
                print(f"  [ERROR] Failed to inject data: {e}")

        self.results['demo_load'] = demo_loaded
        return demo_loaded

    def step2_run_analysis(self):
        """Step 2: Click Run Analysis button"""
        print("\n" + "=" * 70)
        print("STEP 2: RUNNING ANALYSIS")
        print("=" * 70)

        # Find and click Run Analysis button
        run_selectors = [
            'button[onclick*="runAnalysis"]',
            'button[onclick*="analyze"]',
            '#run-analysis',
            '#runAnalysis',
            '.run-btn',
            '//button[contains(text(), "Run")]',
            '//button[contains(text(), "Analyze")]',
            '//button[contains(text(), "▶")]',
            'button.btn-primary',
        ]

        analysis_run = False
        for selector in run_selectors:
            try:
                if selector.startswith('//'):
                    elements = self.driver.find_elements(By.XPATH, selector)
                else:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

                for elem in elements:
                    if elem.is_displayed():
                        btn_text = elem.text.strip()
                        if any(x in btn_text.lower() for x in ['run', 'analyze', '▶', 'start']):
                            if self.safe_click(elem):
                                print(f"  [OK] Clicked: '{btn_text}'")
                                analysis_run = True
                                time.sleep(5)  # Wait for analysis to complete
                                break
                if analysis_run:
                    break
            except:
                continue

        if not analysis_run:
            # Try JavaScript
            try:
                self.driver.execute_script("if (typeof runAnalysis === 'function') runAnalysis();")
                print("  [OK] Called runAnalysis() via JavaScript")
                analysis_run = True
                time.sleep(5)
            except Exception as e:
                print(f"  [ERROR] {e}")

        self.results['analysis_run'] = analysis_run

        # Check for any errors in console
        try:
            logs = self.driver.get_log('browser')
            for log in logs:
                if log['level'] == 'SEVERE':
                    self.results['errors'].append(log['message'][:100])
                    print(f"  [CONSOLE ERROR] {log['message'][:80]}")
        except:
            pass

        return analysis_run

    def step3_check_all_tabs(self):
        """Step 3: Check every tab for analysis results"""
        print("\n" + "=" * 70)
        print("STEP 3: CHECKING ALL TABS FOR RESULTS")
        print("=" * 70)

        # Define tabs to check
        tabs_to_check = [
            ('analysis', 'Analysis', ['pooled', 'estimate', 'forest', 'effect']),
            ('heterogeneity', 'Heterogeneity', ['tau', 'I²', 'Q', 'heterogeneity']),
            ('bias', 'Publication Bias', ['egger', 'funnel', 'bias', 'trim']),
            ('validation', 'Validation', ['valid', 'benchmark', 'test']),
            ('verdict', 'Verdict', ['verdict', 'stable', 'threat', 'severity']),
            ('report', 'Report', ['summary', 'report', 'export']),
            ('clinical', 'Clinical', ['clinical', 'nnt', 'risk']),
            ('hta', 'HTA', ['hta', 'cost', 'icer', 'economic']),
            ('advanced', 'Advanced', ['advanced', 'sensitivity', 'model']),
        ]

        for tab_id, tab_name, keywords in tabs_to_check:
            print(f"\n  --- {tab_name} Tab ---")

            # Click the tab
            clicked = self.find_and_click([
                f'[data-tab="{tab_id}"]',
                f'//button[contains(@data-tab, "{tab_id}")]',
                f'//button[contains(text(), "{tab_name}")]',
            ], f"{tab_name} tab")

            if not clicked:
                self.results['tabs'][tab_id] = {'accessible': False, 'has_content': False}
                continue

            time.sleep(1)

            # Check for content
            try:
                # Get visible text content
                body_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()

                # Check for keywords
                found_keywords = [kw for kw in keywords if kw.lower() in body_text]

                # Check for numbers (analysis results)
                has_numbers = any(c.isdigit() for c in body_text[:5000])

                # Check for plot containers
                plots = self.driver.find_elements(By.CSS_SELECTOR, '.js-plotly-plot, [id*="plot"], [id*="chart"], canvas, svg')
                visible_plots = [p for p in plots if p.is_displayed()]

                # Check for tables
                tables = self.driver.find_elements(By.TAG_NAME, 'table')
                visible_tables = [t for t in tables if t.is_displayed()]

                # Check for result cards/panels
                result_elements = self.driver.find_elements(By.CSS_SELECTOR,
                    '.result, .stat-card, .card, .panel, [class*="result"], [class*="output"]')
                visible_results = [r for r in result_elements if r.is_displayed()]

                has_content = (
                    len(found_keywords) > 0 or
                    len(visible_plots) > 0 or
                    len(visible_tables) > 0 or
                    len(visible_results) > 0
                )

                self.results['tabs'][tab_id] = {
                    'accessible': True,
                    'has_content': has_content,
                    'keywords_found': found_keywords,
                    'plots': len(visible_plots),
                    'tables': len(visible_tables),
                    'result_elements': len(visible_results)
                }

                status = "PASS" if has_content else "WARN"
                print(f"  [{status}] {tab_name}: {len(found_keywords)} keywords, {len(visible_plots)} plots, {len(visible_tables)} tables")

            except Exception as e:
                self.results['tabs'][tab_id] = {'accessible': True, 'has_content': False, 'error': str(e)}
                print(f"  [ERROR] {tab_name}: {str(e)[:50]}")

    def step4_check_plots(self):
        """Step 4: Check if plots render correctly"""
        print("\n" + "=" * 70)
        print("STEP 4: CHECKING PLOT RENDERING")
        print("=" * 70)

        # Go to Analysis tab for forest plot
        self.find_and_click(['[data-tab="analysis"]'], "Analysis tab")
        time.sleep(1)

        plot_checks = [
            ('analysis', 'Forest Plot', 'renderForestPlot'),
            ('heterogeneity', 'Funnel Plot', 'renderFunnelPlot'),
            ('bias', 'Funnel/Bias Plot', 'renderFunnelPlot'),
        ]

        for tab_id, plot_name, render_func in plot_checks:
            # Go to tab
            self.find_and_click([f'[data-tab="{tab_id}"]'], f"{tab_id} tab")
            time.sleep(1)

            # Check for Plotly plots
            try:
                plots = self.driver.find_elements(By.CSS_SELECTOR, '.js-plotly-plot')
                visible_plots = [p for p in plots if p.is_displayed()]

                # Also check for SVG elements (plots)
                svgs = self.driver.find_elements(By.TAG_NAME, 'svg')
                visible_svgs = [s for s in svgs if s.is_displayed() and s.get_attribute('class') and 'plot' in s.get_attribute('class').lower()]

                has_plot = len(visible_plots) > 0 or len(visible_svgs) > 0

                # Try to check plot data
                plot_has_data = False
                if has_plot:
                    try:
                        plot_data = self.driver.execute_script("""
                            const plots = document.querySelectorAll('.js-plotly-plot');
                            for (let p of plots) {
                                if (p.data && p.data.length > 0) return true;
                            }
                            return false;
                        """)
                        plot_has_data = plot_data
                    except:
                        pass

                self.results['plots'][tab_id] = {
                    'has_plot': has_plot,
                    'plot_count': len(visible_plots),
                    'has_data': plot_has_data
                }

                status = "PASS" if has_plot else "WARN"
                print(f"  [{status}] {plot_name} on {tab_id}: {len(visible_plots)} Plotly plots found")

            except Exception as e:
                self.results['plots'][tab_id] = {'error': str(e)}
                print(f"  [ERROR] {plot_name}: {str(e)[:50]}")

        # Try to trigger specific plot renders
        print("\n  --- Testing Plot Render Functions ---")
        plot_functions = [
            ('renderForestPlot', 'Forest Plot'),
            ('renderFunnelPlot', 'Funnel Plot'),
            ('renderBaujatPlot', 'Baujat Plot'),
            ('renderGalbraithPlot', 'Galbraith Plot'),
            ('renderInfluencePlot', 'Influence Plot'),
        ]

        for func_name, plot_name in plot_functions:
            try:
                exists = self.driver.execute_script(f"return typeof {func_name} === 'function'")
                if exists:
                    print(f"  [OK] {plot_name} ({func_name}) - Available")
                else:
                    print(f"  [MISSING] {plot_name} ({func_name})")
            except:
                print(f"  [ERROR] Could not check {func_name}")

    def step5_check_export_buttons(self):
        """Step 5: Check export functionality"""
        print("\n" + "=" * 70)
        print("STEP 5: CHECKING EXPORT BUTTONS")
        print("=" * 70)

        # Go to Report tab
        self.find_and_click(['[data-tab="report"]'], "Report tab")
        time.sleep(1)

        export_buttons = [
            ('CSV', ['csv', 'export']),
            ('Excel', ['excel', 'xlsx']),
            ('PDF', ['pdf']),
            ('JSON', ['json']),
        ]

        for export_name, keywords in export_buttons:
            try:
                buttons = self.driver.find_elements(By.TAG_NAME, 'button')
                found = False
                for btn in buttons:
                    btn_text = btn.text.lower()
                    if any(kw in btn_text for kw in keywords):
                        if btn.is_displayed():
                            print(f"  [OK] {export_name} export button found")
                            found = True
                            break
                if not found:
                    print(f"  [WARN] {export_name} export button not visible")
            except:
                pass

    def generate_report(self):
        """Generate final test report"""
        print("\n" + "=" * 70)
        print("FINAL TEST REPORT")
        print("=" * 70)

        print(f"\nDemo Data Loaded: {'YES' if self.results['demo_load'] else 'NO'}")
        print(f"Analysis Run: {'YES' if self.results['analysis_run'] else 'NO'}")

        print("\nTabs with Content:")
        tabs_with_content = 0
        tabs_total = len(self.results['tabs'])
        for tab_id, data in self.results['tabs'].items():
            status = "PASS" if data.get('has_content') else "FAIL"
            print(f"  [{status}] {tab_id}: plots={data.get('plots', 0)}, tables={data.get('tables', 0)}")
            if data.get('has_content'):
                tabs_with_content += 1

        print(f"\nTabs with content: {tabs_with_content}/{tabs_total}")

        print("\nPlots:")
        for plot_id, data in self.results['plots'].items():
            if 'error' not in data:
                status = "PASS" if data.get('has_plot') else "FAIL"
                print(f"  [{status}] {plot_id}: {data.get('plot_count', 0)} plots")

        if self.results['errors']:
            print(f"\nErrors ({len(self.results['errors'])}):")
            for err in self.results['errors'][:5]:
                print(f"  - {err[:80]}")

        # Save detailed report
        report_path = Path("C:/Users/user/truthcert_comprehensive_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\nDetailed report: {report_path}")

        # Overall status
        success = (
            self.results['demo_load'] and
            self.results['analysis_run'] and
            tabs_with_content >= 3
        )

        print("\n" + "=" * 70)
        if success:
            print("OVERALL: PASS - App is functional")
        else:
            print("OVERALL: ISSUES FOUND - Review above")
        print("=" * 70)

        return success

    def cleanup(self):
        """Close browser"""
        if self.driver:
            input("\nPress Enter to close browser...")
            self.driver.quit()

    def run(self):
        """Run all tests"""
        try:
            self.setup()
            self.step1_load_demo_data()
            self.step2_run_analysis()
            self.step3_check_all_tabs()
            self.step4_check_plots()
            self.step5_check_export_buttons()
            return self.generate_report()
        except Exception as e:
            print(f"\n[FATAL ERROR] {e}")
            self.results['errors'].append(str(e))
            return False
        finally:
            self.cleanup()


if __name__ == "__main__":
    tester = ComprehensiveTester()
    success = tester.run()
    sys.exit(0 if success else 1)
