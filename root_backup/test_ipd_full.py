#!/usr/bin/env python3
"""
FULL SELENIUM TEST FOR IPD META-ANALYSIS PRO
Tests all buttons, functions, and plots with proper dynamic handling
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class IPDFullTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.driver = None

    def setup(self):
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
        print("[OK] Chrome initialized")

    def teardown(self):
        if self.driver:
            self.driver.quit()
            print("\n[OK] Browser closed")

    def log(self, test, passed, details="", cat=""):
        if passed:
            self.passed += 1
            s = "PASS"
        else:
            self.failed += 1
            s = "FAIL"
        self.results.append({"category": cat, "test": test, "passed": passed, "details": details})
        safe = details.encode('ascii', 'replace').decode('ascii')[:40] if details else ""
        print(f"  [{s}] {test}" + (f": {safe}" if safe else ""))

    def js(self, script):
        """Execute JavaScript and return result"""
        return self.driver.execute_script(script)

    def click_button(self, text):
        """Click button containing text"""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//button[contains(., '{text}')]")))
            btn.click()
            return True
        except:
            return False

    def run_tests(self):
        print("=" * 70)
        print("IPD META-ANALYSIS PRO - FULL SELENIUM TEST")
        print("=" * 70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)

        try:
            self.setup()

            # Load app
            self.driver.get(f'file:///C:/Users/user/IPD-Meta-Pro/ipd-meta-pro.html')
            time.sleep(3)
            self.log("App Loads", "IPD Meta-Analysis" in self.driver.title, self.driver.title, "Setup")

            # ===== SECTION 1: UI ELEMENTS =====
            print("\n[1] UI ELEMENTS")

            # Check header elements
            self.log("Logo exists", self.js("return document.querySelector('.logo, h1') !== null"), "", "UI")
            self.log("Theme toggle", self.js("return document.querySelector('#themeToggle, [onclick*=\"toggleTheme\"]') !== null"), "", "UI")
            self.log("Export button", len(self.driver.find_elements(By.XPATH, "//button[contains(., 'Export')]")) > 0, "", "UI")
            self.log("Help button", len(self.driver.find_elements(By.XPATH, "//button[contains(., 'Help')]")) > 0, "", "UI")

            # Check navigation tabs
            tabs = self.js("return document.querySelectorAll('.nav-tab, .tab-btn, [class*=\"tab\"]').length")
            self.log("Navigation tabs", tabs >= 10, f"{tabs} tabs", "UI")

            # Check drop zone
            self.log("Drop zone", self.js("return document.querySelector('.drop-zone, [class*=\"drop\"]') !== null"), "", "UI")

            # ===== SECTION 2: EXAMPLE DATA =====
            print("\n[2] EXAMPLE DATA LOADING")

            # Test Lung Cancer dataset
            self.click_button("Lung Cancer")
            time.sleep(2)
            count = self.js("return APP && APP.data ? APP.data.length : 0")
            self.log("Lung Cancer loads", count > 0, f"{count} patients", "Data")

            # Test SGLT2 dataset
            self.click_button("SGLT2")
            time.sleep(2)
            count = self.js("return APP && APP.data ? APP.data.length : 0")
            self.log("SGLT2 loads", count > 0, f"{count} patients", "Data")

            # Test Depression dataset
            self.click_button("Depression")
            time.sleep(2)
            count = self.js("return APP && APP.data ? APP.data.length : 0")
            self.log("Depression loads", count > 0, f"{count} patients", "Data")

            # Reload Lung Cancer for analysis
            self.click_button("Lung Cancer")
            time.sleep(2)

            # ===== SECTION 3: RUN ANALYSIS =====
            print("\n[3] MAIN ANALYSIS")

            # Find and click Run Analysis button
            try:
                btns = self.driver.find_elements(By.TAG_NAME, "button")
                for btn in btns:
                    txt = btn.text.lower()
                    if 'run' in txt and 'analysis' in txt and btn.is_displayed():
                        btn.click()
                        time.sleep(4)
                        break
                has_results = self.js("return APP && APP.results !== null")
                self.log("Analysis runs", has_results, "", "Analysis")
            except Exception as e:
                self.log("Analysis runs", False, str(e)[:30], "Analysis")

            # Check statistical results - handle different result structures
            try:
                effect = self.js("""
                    if (!APP || !APP.results) return null;
                    if (APP.results.pooled && APP.results.pooled.effect !== undefined) return APP.results.pooled.effect;
                    if (APP.results.effect !== undefined) return APP.results.effect;
                    return null;
                """)
                self.log("Pooled effect", effect is not None, f"{effect:.4f}" if effect else "", "Analysis")
            except:
                self.log("Pooled effect", False, "", "Analysis")

            try:
                ci = self.js("""
                    if (!APP || !APP.results) return null;
                    var p = APP.results.pooled || APP.results;
                    if (p.lower !== undefined && p.upper !== undefined) return [p.lower, p.upper];
                    return null;
                """)
                self.log("95% CI", ci is not None, f"[{ci[0]:.3f}, {ci[1]:.3f}]" if ci else "", "Analysis")
            except:
                self.log("95% CI", False, "", "Analysis")

            try:
                i2 = self.js("""
                    if (!APP || !APP.results) return null;
                    if (APP.results.heterogeneity && APP.results.heterogeneity.I2 !== undefined) return APP.results.heterogeneity.I2;
                    if (APP.results.pooled && APP.results.pooled.I2 !== undefined) return APP.results.pooled.I2;
                    return null;
                """)
                self.log("I-squared", i2 is not None, f"{i2:.1f}%" if i2 else "", "Analysis")
            except:
                self.log("I-squared", False, "", "Analysis")

            try:
                tau2 = self.js("""
                    if (!APP || !APP.results) return null;
                    if (APP.results.heterogeneity && APP.results.heterogeneity.tau2 !== undefined) return APP.results.heterogeneity.tau2;
                    if (APP.results.pooled && APP.results.pooled.tau2 !== undefined) return APP.results.pooled.tau2;
                    return null;
                """)
                self.log("Tau-squared", tau2 is not None, f"{tau2:.4f}" if tau2 else "", "Analysis")
            except:
                self.log("Tau-squared", False, "", "Analysis")

            try:
                Q = self.js("""
                    if (!APP || !APP.results) return null;
                    if (APP.results.heterogeneity && APP.results.heterogeneity.Q !== undefined) return APP.results.heterogeneity.Q;
                    if (APP.results.pooled && APP.results.pooled.Q !== undefined) return APP.results.pooled.Q;
                    return null;
                """)
                self.log("Q statistic", Q is not None, f"{Q:.2f}" if Q else "", "Analysis")
            except:
                self.log("Q statistic", False, "", "Analysis")

            # ===== SECTION 4: FOREST PLOT =====
            print("\n[4] FOREST PLOT")

            self.log("Forest canvas exists", self.js("return document.getElementById('forestPlot') !== null"), "", "Plots")
            rendered = self.js("""
                var c = document.getElementById('forestPlot');
                if (!c) return false;
                try {
                    var ctx = c.getContext('2d');
                    var d = ctx.getImageData(0, 0, 10, 10).data;
                    for (var i = 0; i < d.length; i++) if (d[i] > 0) return true;
                    return false;
                } catch(e) { return false; }
            """)
            self.log("Forest plot rendered", rendered, "", "Plots")

            # ===== SECTION 5: NAVIGATION TABS =====
            print("\n[5] NAVIGATION TABS")

            tab_names = ['Data', 'Covariates', 'Network', 'Results', 'Ranking',
                        'Heterogeneity', 'Bayesian', 'Pub Bias', 'Meta-Reg']

            for tab in tab_names:
                try:
                    btns = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{tab}')]")
                    clicked = False
                    for btn in btns:
                        if btn.is_displayed() and btn.is_enabled():
                            try:
                                btn.click()
                                clicked = True
                                time.sleep(0.5)
                                break
                            except:
                                pass
                    self.log(f"Tab: {tab}", clicked, "", "Tabs")
                except Exception as e:
                    self.log(f"Tab: {tab}", False, str(e)[:20], "Tabs")

            # ===== SECTION 6: NETWORK META-ANALYSIS =====
            print("\n[6] NETWORK META-ANALYSIS")

            # Click Network tab
            try:
                net_btns = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Network')]")
                for btn in net_btns:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(1)
                        break
            except:
                pass

            self.log("Network canvas", self.js("return document.getElementById('networkPlot') !== null"), "", "Network")

            net_stats = self.js("return document.body.innerHTML.includes('nodes') || document.body.innerHTML.includes('Nodes')")
            self.log("Network stats shown", net_stats, "", "Network")

            # Check ranking
            try:
                rank_btns = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Ranking')]")
                for btn in rank_btns:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(1)
                        break
            except:
                pass

            self.log("Rankogram canvas", self.js("return document.getElementById('rankogramPlot') !== null"), "", "Network")
            self.log("Cumulative rank canvas", self.js("return document.getElementById('cumulativeRankPlot') !== null"), "", "Network")

            # ===== SECTION 7: PUBLICATION BIAS =====
            print("\n[7] PUBLICATION BIAS")

            try:
                pb_btns = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Pub Bias') or contains(text(), 'Publication')]")
                for btn in pb_btns:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(1)
                        break
            except:
                pass

            self.log("Funnel canvas", self.js("return document.getElementById('funnelPlot') !== null"), "", "PubBias")
            self.log("Trim-fill canvas", self.js("return document.getElementById('trimFillPlot') !== null"), "", "PubBias")

            egger = self.js("return document.body.innerHTML.includes('Egger')")
            self.log("Egger test shown", egger, "", "PubBias")

            begg = self.js("return document.body.innerHTML.includes('Begg')")
            self.log("Begg test shown", begg, "", "PubBias")

            # ===== SECTION 8: BAYESIAN ANALYSIS =====
            print("\n[8] BAYESIAN ANALYSIS")

            try:
                bay_btns = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Bayesian')]")
                for btn in bay_btns:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(1)
                        break
            except:
                pass

            self.log("Trace plot canvas", self.js("return document.getElementById('tracePlot') !== null"), "", "Bayesian")
            self.log("Posterior canvas", self.js("return document.getElementById('posteriorPlot') !== null"), "", "Bayesian")

            # Run Bayesian
            try:
                run_btns = self.driver.find_elements(By.XPATH, "//button[contains(., 'Run') and contains(., 'Bayesian')]")
                for btn in run_btns:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(3)
                        break
                bay_result = self.js("return APP && APP.bayesianResults !== null")
                self.log("Bayesian analysis runs", bay_result, "", "Bayesian")
            except:
                self.log("Bayesian analysis runs", False, "", "Bayesian")

            # ===== SECTION 9: META-REGRESSION =====
            print("\n[9] META-REGRESSION")

            try:
                mr_btns = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Meta-Reg')]")
                for btn in mr_btns:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(1)
                        break
            except:
                pass

            self.log("Bubble plot canvas", self.js("return document.getElementById('bubblePlot') !== null"), "", "MetaReg")

            # ===== SECTION 10: HELP MODAL =====
            print("\n[10] HELP SYSTEM")

            self.js("if (typeof showHelp === 'function') showHelp()")
            time.sleep(1)
            help_vis = self.js("var m = document.getElementById('helpModal'); return m && m.style.display !== 'none'")
            self.log("Help modal opens", help_vis, "", "Help")

            help_tabs = self.js("return document.querySelectorAll('#helpModal .tab, #helpModal [class*=\"tab\"]').length")
            self.log("Help has tabs", help_tabs >= 2, f"{help_tabs} tabs", "Help")

            self.js("if (typeof closeHelp === 'function') closeHelp()")
            time.sleep(0.5)

            # ===== SECTION 11: ADVANCED FEATURES =====
            print("\n[11] ADVANCED FEATURES")

            self.js("if (typeof showAdvancedFeaturesMenu === 'function') showAdvancedFeaturesMenu()")
            time.sleep(1)

            adv_vis = self.js("""
                var m = document.getElementById('advancedFeaturesModal');
                if (m && m.style.display !== 'none') return true;
                var modals = document.querySelectorAll('[id*=\"advanced\"], [id*=\"features\"]');
                for (var i = 0; i < modals.length; i++) {
                    if (modals[i].style.display !== 'none') return true;
                }
                return false;
            """)
            self.log("Advanced features modal", adv_vis, "", "Advanced")

            feat_count = self.js("""
                var btns = document.querySelectorAll('[id*=\"advanced\"] button, [id*=\"features\"] button');
                return btns.length;
            """)
            self.log("Feature buttons", feat_count > 20, f"{feat_count} buttons", "Advanced")

            # Close modal
            self.js("""
                var modals = document.querySelectorAll('[id*=\"Modal\"]');
                for (var i = 0; i < modals.length; i++) modals[i].style.display = 'none';
            """)

            # ===== SECTION 12: POWER CALCULATOR =====
            print("\n[12] POWER CALCULATOR")

            self.js("if (typeof showPowerCalculator === 'function') showPowerCalculator()")
            time.sleep(1)

            pwr_vis = self.js("""
                var m = document.getElementById('powerCalculatorModal');
                if (m && m.style.display !== 'none') return true;
                var modals = document.querySelectorAll('[id*=\"power\"]');
                for (var i = 0; i < modals.length; i++) {
                    if (modals[i].style.display !== 'none') return true;
                }
                return false;
            """)
            self.log("Power calculator opens", pwr_vis, "", "Power")

            pwr_tabs = self.js("""
                return document.querySelectorAll('[id*=\"power\"] .tab, [id*=\"power\"] [onclick*=\"switchPower\"]').length
            """)
            self.log("Power calc has tabs", pwr_tabs >= 2, f"{pwr_tabs} tabs", "Power")

            # Close
            self.js("var m = document.getElementById('powerCalculatorModal'); if (m) m.style.display = 'none'")

            # ===== SECTION 13: ENHANCED EXPORT =====
            print("\n[13] EXPORT SYSTEM")

            self.js("if (typeof showEnhancedExportModal === 'function') showEnhancedExportModal()")
            time.sleep(1)

            exp_vis = self.js("""
                var m = document.getElementById('enhancedExportModal');
                if (m && m.style.display !== 'none') return true;
                var modals = document.querySelectorAll('[id*=\"export\"]');
                for (var i = 0; i < modals.length; i++) {
                    if (modals[i].style.display !== 'none' && modals[i].innerHTML.length > 100) return true;
                }
                return false;
            """)
            self.log("Export modal opens", exp_vis, "", "Export")

            exp_opts = self.js("""
                var btns = document.querySelectorAll('[id*=\"export\"] button, [id*=\"Export\"] button');
                return btns.length;
            """)
            self.log("Export options", exp_opts >= 5, f"{exp_opts} options", "Export")

            # Close
            self.js("var m = document.getElementById('enhancedExportModal'); if (m) m.style.display = 'none'")

            # ===== SECTION 14: P-CURVE ANALYSIS =====
            print("\n[14] P-CURVE ANALYSIS")

            self.js("if (typeof runPCurveAnalysis === 'function') runPCurveAnalysis()")
            time.sleep(2)

            pcurve_vis = self.js("""
                var m = document.getElementById('pcurveModal');
                return m && m.style.display !== 'none';
            """)
            self.log("P-Curve modal opens", pcurve_vis, "", "PCurve")

            self.js("var m = document.getElementById('pcurveModal'); if (m) m.style.display = 'none'")

            # ===== SECTION 15: EXCESS SIGNIFICANCE =====
            print("\n[15] EXCESS SIGNIFICANCE TEST")

            self.js("if (typeof runExcessSignificanceTest === 'function') runExcessSignificanceTest()")
            time.sleep(2)

            exsig_vis = self.js("""
                var m = document.getElementById('excessSigModal');
                return m && m.style.display !== 'none';
            """)
            self.log("Excess sig modal opens", exsig_vis, "", "ExcessSig")

            self.js("var m = document.getElementById('excessSigModal'); if (m) m.style.display = 'none'")

            # ===== SECTION 16: INTEGRATED TEST SUITE =====
            print("\n[16] INTEGRATED TEST SUITE")

            self.js("if (typeof runIntegratedTestSuite === 'function') runIntegratedTestSuite()")
            time.sleep(3)

            test_vis = self.js("""
                var m = document.getElementById('testSuiteModal');
                return m && m.style.display !== 'none';
            """)
            self.log("Test suite modal opens", test_vis, "", "TestSuite")

            # ===== SECTION 17: JAVASCRIPT FUNCTIONS =====
            print("\n[17] CORE JAVASCRIPT FUNCTIONS")

            core_funcs = [
                'runAnalysis', 'runBayesian', 'runMetaRegression', 'runNetworkMetaAnalysis',
                'runTrimAndFill', 'exportAnalysis', 'exportResults', 'exportPDF', 'exportHTML',
                'exportRCode', 'downloadForest', 'downloadFunnel', 'downloadNetwork',
                'showHelp', 'showAdvancedFeaturesMenu', 'showPowerCalculator', 'toggleTheme',
                'clearData', 'calculateI2', 'calculatePredictionInterval', 'calculateFragilityIndex',
                'calculateNNT', 'calculateRMST', 'calculateKaplanMeier', 'calculateCoxPH',
                'runPCurveAnalysis', 'runExcessSignificanceTest', 'runIntegratedTestSuite',
                'generatePRISMAFlowchart', 'exportSensitivityAnalysis', 'showEnhancedExportModal',
                'initTooltips'
            ]

            for f in core_funcs:
                exists = self.js(f"return typeof {f} === 'function'")
                self.log(f"Function: {f}", exists, "", "Functions")

            # ===== SECTION 18: MATHUTILS =====
            print("\n[18] MATHUTILS LIBRARY")

            self.log("MathUtils exists", self.js("return typeof MathUtils !== 'undefined'"), "", "MathUtils")
            self.log("normCDF(0)=0.5", self.js("return Math.abs(MathUtils.normCDF(0) - 0.5) < 0.001"), "", "MathUtils")
            self.log("normCDF(1.96)=0.975", self.js("return Math.abs(MathUtils.normCDF(1.96) - 0.975) < 0.01"), "", "MathUtils")
            self.log("chi2CDF exists", self.js("return typeof MathUtils.chi2CDF === 'function'"), "", "MathUtils")
            self.log("tCDF exists", self.js("return typeof MathUtils.tCDF === 'function'"), "", "MathUtils")

            # ===== SECTION 19: TOOLTIPS =====
            print("\n[19] TOOLTIP SYSTEM")

            self.log("TOOLTIPS object", self.js("return typeof TOOLTIPS !== 'undefined'"), "", "Tooltips")
            tt_count = self.js("return Object.keys(TOOLTIPS || {}).length")
            self.log("TOOLTIPS entries", tt_count > 10, f"{tt_count} entries", "Tooltips")
            tt_els = self.js("return document.querySelectorAll('[title], [data-tooltip]').length")
            self.log("Tooltip elements", tt_els > 30, f"{tt_els} elements", "Tooltips")

            # ===== SECTION 20: THEME TOGGLE =====
            print("\n[20] THEME SYSTEM")

            initial = self.js("return document.body.classList.contains('dark-theme')")
            self.js("toggleTheme()")
            time.sleep(0.5)
            after = self.js("return document.body.classList.contains('dark-theme')")
            self.log("Theme toggle works", initial != after, f"Dark: {initial} -> {after}", "Theme")
            self.js("toggleTheme()")  # Toggle back

            # ===== SECTION 21: HETEROGENEITY PANEL =====
            print("\n[21] HETEROGENEITY ANALYSIS")

            try:
                het_btns = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Heterogeneity')]")
                for btn in het_btns:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(1)
                        break
            except:
                pass

            self.log("I2 shown", self.js("return document.body.innerHTML.includes('I2') || document.body.innerHTML.includes('I<sup>2</sup>')"), "", "Heterogeneity")
            self.log("Tau2 shown", self.js("return document.body.innerHTML.toLowerCase().includes('tau')"), "", "Heterogeneity")
            self.log("Baujat canvas", self.js("return document.getElementById('baujatPlot') !== null"), "", "Heterogeneity")
            self.log("LOO canvas", self.js("return document.getElementById('looPlot') !== null"), "", "Heterogeneity")

            # ===== SECTION 22: ALL CANVAS ELEMENTS =====
            print("\n[22] CANVAS ELEMENTS")

            core_canvases = [
                'forestPlot', 'funnelPlot', 'networkPlot', 'survivalPlot',
                'rankogramPlot', 'cumulativeRankPlot', 'baujatPlot', 'looPlot',
                'netHeatPlot', 'tracePlot', 'posteriorPlot', 'trimFillPlot',
                'bubblePlot', 'missingPlot'
            ]

            for canvas in core_canvases:
                exists = self.js(f"return document.getElementById('{canvas}') !== null")
                self.log(f"Canvas: {canvas}", exists, "", "Canvas")

            # ===== SECTION 23: DATA DISPLAY =====
            print("\n[23] DATA DISPLAY")

            # Go to Data tab
            try:
                data_btns = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Data')]")
                for btn in data_btns:
                    if btn.is_displayed() and 'Data' in btn.text:
                        btn.click()
                        time.sleep(1)
                        break
            except:
                pass

            table_rows = self.js("""
                var tables = document.querySelectorAll('table');
                var max = 0;
                for (var i = 0; i < tables.length; i++) {
                    if (tables[i].rows && tables[i].rows.length > max) max = tables[i].rows.length;
                }
                return max;
            """)
            self.log("Data table rows", table_rows > 5, f"{table_rows} rows", "Data")

            # ===== SECTION 24: SENSITIVITY ANALYSIS =====
            print("\n[24] SENSITIVITY ANALYSIS")

            self.log("exportSensitivityAnalysis exists", self.js("return typeof exportSensitivityAnalysis === 'function'"), "", "Sensitivity")
            self.log("generatePRISMAFlowchart exists", self.js("return typeof generatePRISMAFlowchart === 'function'"), "", "Sensitivity")

            # ===== SUMMARY =====
            print("\n" + "=" * 70)
            print("TEST SUMMARY")
            print("=" * 70)

            total = self.passed + self.failed
            rate = (self.passed / total * 100) if total > 0 else 0

            print(f"  Total Tests: {total}")
            print(f"  Passed:      {self.passed}")
            print(f"  Failed:      {self.failed}")
            print(f"  Pass Rate:   {rate:.1f}%")
            print("-" * 70)

            if rate >= 95:
                print("  STATUS: EXCELLENT - App is fully functional!")
            elif rate >= 85:
                print("  STATUS: VERY GOOD - Minor issues only")
            elif rate >= 75:
                print("  STATUS: GOOD - Some issues to address")
            else:
                print("  STATUS: NEEDS IMPROVEMENT")

            print("=" * 70)

            # Print failures
            if self.failed > 0:
                print("\nFAILED TESTS:")
                for r in self.results:
                    if not r['passed']:
                        print(f"  - {r['category']}: {r['test']}")

            # Save results
            output = {
                "timestamp": datetime.now().isoformat(),
                "summary": {"total": total, "passed": self.passed, "failed": self.failed, "pass_rate": rate},
                "tests": self.results
            }
            with open(r'C:\Users\user\ipd_full_test_results.json', 'w') as f:
                json.dump(output, f, indent=2)
            print(f"\nResults saved to: C:\\Users\\user\\ipd_full_test_results.json")

        except Exception as e:
            print(f"\n[ERROR] {str(e)[:60]}")
        finally:
            self.teardown()


if __name__ == "__main__":
    IPDFullTester().run_tests()
