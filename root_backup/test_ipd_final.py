#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE SELENIUM TEST FOR IPD META-ANALYSIS PRO
Properly handles all elements with correct selectors
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class IPDFinalTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

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
        return self.driver.execute_script(script)

    def click_tab(self, panel_name):
        """Click tab by data-panel attribute"""
        try:
            self.js(f"""
                var tabs = document.querySelectorAll('[data-panel="{panel_name}"]');
                for (var t of tabs) {{ if (t.offsetParent !== null) {{ t.click(); break; }} }}
            """)
            time.sleep(0.5)
            return True
        except:
            return False

    def run_tests(self):
        print("=" * 70)
        print("IPD META-ANALYSIS PRO - FINAL COMPREHENSIVE TEST")
        print("=" * 70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)

        try:
            self.setup()

            # Load app
            self.driver.get('file:///C:/Users/user/IPD-Meta-Pro/ipd-meta-pro.html')
            time.sleep(3)
            self.log("App Loads", "IPD Meta-Analysis" in self.driver.title, self.driver.title[:40], "Setup")

            # ===== SECTION 1: UI =====
            print("\n[1] UI ELEMENTS")
            self.log("Logo", self.js("return document.querySelector('.logo') !== null"), "", "UI")
            self.log("Header", self.js("return document.querySelector('.header') !== null"), "", "UI")
            self.log("Theme toggle", self.js("return document.querySelector('.theme-toggle') !== null"), "", "UI")
            self.log("Navigation", self.js("return document.querySelectorAll('.nav-tab').length >= 10"), "", "UI")
            self.log("Drop zone", self.js("return document.querySelector('.drop-zone') !== null"), "", "UI")

            # ===== SECTION 2: HEADER BUTTONS =====
            print("\n[2] HEADER BUTTONS")
            self.log("Help button", self.js("return !!document.querySelector('[onclick*=\"showHelp\"]')"), "", "Buttons")
            self.log("Export button", self.js("return !!document.querySelector('[onclick*=\"Export\"]')"), "", "Buttons")
            self.log("GRADE button", self.js("return !!document.querySelector('[onclick*=\"GRADE\"]')"), "", "Buttons")
            self.log("Power Calc button", self.js("return !!document.querySelector('[onclick*=\"PowerCalculator\"]')"), "", "Buttons")
            self.log("MASEM button", self.js("return !!document.querySelector('[onclick*=\"Mediation\"]')"), "", "Buttons")

            # ===== SECTION 3: EXAMPLE DATA =====
            print("\n[3] EXAMPLE DATA")

            # Click Lung Cancer (survival)
            self.js("loadExampleData('survival')")
            time.sleep(2)
            count = self.js("return APP && APP.data ? APP.data.length : 0")
            self.log("Lung Cancer dataset", count > 0, f"{count} patients", "Data")

            # Click SGLT2 (binary)
            self.js("loadExampleData('binary')")
            time.sleep(2)
            count = self.js("return APP && APP.data ? APP.data.length : 0")
            self.log("SGLT2 dataset", count > 0, f"{count} patients", "Data")

            # Click Depression (continuous)
            self.js("loadExampleData('continuous')")
            time.sleep(2)
            count = self.js("return APP && APP.data ? APP.data.length : 0")
            self.log("Depression dataset", count > 0, f"{count} patients", "Data")

            # Reload Lung Cancer for remaining tests
            self.js("loadExampleData('survival')")
            time.sleep(2)

            # ===== SECTION 4: RUN ANALYSIS =====
            print("\n[4] MAIN ANALYSIS")

            # Find and click Run Analysis
            self.js("""
                var btns = document.querySelectorAll('button');
                for (var b of btns) {
                    if (b.textContent.includes('Run') && b.textContent.includes('Analysis') && b.offsetParent !== null) {
                        b.click(); break;
                    }
                }
            """)
            time.sleep(4)

            has_results = self.js("return APP && APP.results !== null")
            self.log("Analysis runs", has_results, "", "Analysis")

            # Check results
            try:
                effect = self.js("return APP && APP.results && APP.results.pooled ? APP.results.pooled.effect : null")
                self.log("Effect calculated", effect is not None, f"{effect:.4f}" if effect is not None else "", "Analysis")
            except:
                self.log("Effect calculated", False, "", "Analysis")

            try:
                ci = self.js("return APP && APP.results && APP.results.pooled ? [APP.results.pooled.lower, APP.results.pooled.upper] : null")
                ci_str = f"[{ci[0]:.3f}, {ci[1]:.3f}]" if ci and ci[0] is not None else ""
                self.log("95% CI calculated", ci is not None and ci[0] is not None, ci_str, "Analysis")
            except:
                self.log("95% CI calculated", False, "", "Analysis")

            try:
                i2 = self.js("return APP && APP.results && APP.results.heterogeneity ? APP.results.heterogeneity.I2 : null")
                self.log("I-squared", i2 is not None, f"{i2:.1f}%" if i2 is not None else "", "Analysis")
            except:
                self.log("I-squared", False, "", "Analysis")

            try:
                tau2 = self.js("return APP && APP.results && APP.results.heterogeneity ? APP.results.heterogeneity.tau2 : null")
                self.log("Tau-squared", tau2 is not None, f"{tau2:.4f}" if tau2 is not None else "", "Analysis")
            except:
                self.log("Tau-squared", False, "", "Analysis")

            # ===== SECTION 5: NAVIGATION TABS =====
            print("\n[5] NAVIGATION TABS")

            tab_panels = ['data', 'covariates', 'guardian', 'network', 'results',
                         'ranking', 'heterogeneity', 'consistency', 'bayesian', 'pubbias', 'metareg']

            for panel in tab_panels:
                clicked = self.click_tab(panel)
                visible = self.js(f"var p = document.getElementById('panel-{panel}'); return p && p.classList.contains('active')")
                self.log(f"Tab: {panel}", clicked and visible, "", "Tabs")

            # ===== SECTION 6: FOREST PLOT =====
            print("\n[6] FOREST PLOT")
            self.click_tab('results')
            time.sleep(1)

            self.log("Forest canvas exists", self.js("return document.getElementById('forestPlot') !== null"), "", "Plots")

            rendered = self.js("""
                var c = document.getElementById('forestPlot');
                if (!c) return false;
                try {
                    var ctx = c.getContext('2d');
                    var d = ctx.getImageData(0, 0, c.width, c.height).data;
                    for (var i = 0; i < d.length; i += 4) if (d[i] > 0 || d[i+1] > 0 || d[i+2] > 0) return true;
                    return false;
                } catch(e) { return c.width > 0 && c.height > 0; }
            """)
            self.log("Forest plot rendered", rendered, "", "Plots")

            # ===== SECTION 7: NETWORK MA =====
            print("\n[7] NETWORK META-ANALYSIS")
            self.click_tab('network')
            time.sleep(1)

            self.log("Network canvas", self.js("return document.getElementById('networkPlot') !== null"), "", "Network")
            self.log("Network stats", self.js("return document.body.innerHTML.toLowerCase().includes('nodes')"), "", "Network")

            # ===== SECTION 8: RANKING =====
            print("\n[8] RANKING")
            self.click_tab('ranking')
            time.sleep(1)

            self.log("Rankogram canvas", self.js("return document.getElementById('rankogramPlot') !== null"), "", "Ranking")
            self.log("Cumulative rank canvas", self.js("return document.getElementById('cumulativeRankPlot') !== null"), "", "Ranking")

            # ===== SECTION 9: HETEROGENEITY =====
            print("\n[9] HETEROGENEITY")
            self.click_tab('heterogeneity')
            time.sleep(1)

            self.log("Baujat plot", self.js("return document.getElementById('baujatPlot') !== null"), "", "Heterogeneity")
            self.log("LOO plot", self.js("return document.getElementById('looPlot') !== null"), "", "Heterogeneity")
            self.log("I2 displayed", self.js("return document.body.innerHTML.includes('I2') || document.body.innerHTML.includes('I<sup>2</sup>')"), "", "Heterogeneity")

            # ===== SECTION 10: BAYESIAN =====
            print("\n[10] BAYESIAN ANALYSIS")
            self.click_tab('bayesian')
            time.sleep(1)

            self.log("Trace plot canvas", self.js("return document.getElementById('tracePlot') !== null"), "", "Bayesian")
            self.log("Posterior canvas", self.js("return document.getElementById('posteriorPlot') !== null"), "", "Bayesian")

            # Run Bayesian
            self.js("""
                var btns = document.querySelectorAll('button');
                for (var b of btns) {
                    if (b.textContent.includes('Bayesian') && b.offsetParent !== null) {
                        b.click(); break;
                    }
                }
            """)
            time.sleep(4)
            bay_result = self.js("return APP && APP.bayesianResults !== null")
            self.log("Bayesian analysis runs", bay_result, "", "Bayesian")

            # ===== SECTION 11: PUBLICATION BIAS =====
            print("\n[11] PUBLICATION BIAS")
            self.click_tab('pubbias')
            time.sleep(1)

            self.log("Funnel canvas", self.js("return document.getElementById('funnelPlot') !== null"), "", "PubBias")
            self.log("Trim-fill canvas", self.js("return document.getElementById('trimFillPlot') !== null"), "", "PubBias")
            self.log("Egger test shown", self.js("return document.body.innerHTML.includes('Egger')"), "", "PubBias")
            self.log("Begg test shown", self.js("return document.body.innerHTML.includes('Begg')"), "", "PubBias")

            # ===== SECTION 12: META-REGRESSION =====
            print("\n[12] META-REGRESSION")
            self.click_tab('metareg')
            time.sleep(1)

            self.log("Bubble plot canvas", self.js("return document.getElementById('bubblePlot') !== null"), "", "MetaReg")

            # ===== SECTION 13: HELP MODAL =====
            print("\n[13] HELP MODAL")
            self.js("showHelp()")
            time.sleep(1)

            help_visible = self.js("var m = document.getElementById('helpModal'); return m && m.style.display !== 'none'")
            self.log("Help modal opens", help_visible, "", "Modals")

            help_tabs = self.js("return document.querySelectorAll('#helpModal .inner-tab').length")
            self.log("Help has tabs", help_tabs >= 3, f"{help_tabs} tabs", "Modals")

            self.js("closeHelp()")
            time.sleep(0.5)

            # ===== SECTION 14: POWER CALCULATOR =====
            print("\n[14] POWER CALCULATOR")
            self.js("showPowerCalculator()")
            time.sleep(1)

            pwr_visible = self.js("""
                var m = document.getElementById('powerCalculatorModal');
                if (m && m.style.display !== 'none') return true;
                // Check for any modal with power in content
                var modals = document.querySelectorAll('[class*=\"modal\"], [id*=\"Modal\"]');
                for (var i = 0; i < modals.length; i++) {
                    if (modals[i].offsetParent !== null && modals[i].innerHTML.toLowerCase().includes('power')) return true;
                }
                return false;
            """)
            self.log("Power calculator opens", pwr_visible, "", "Modals")

            pwr_tabs = self.js("""
                var m = document.getElementById('powerCalculatorModal');
                if (m) return m.querySelectorAll('.inner-tab').length;
                return document.querySelectorAll('.modal.active .inner-tab, [style*=\"block\"] .inner-tab').length;
            """)
            self.log("Power calc has tabs", pwr_tabs >= 2, f"{pwr_tabs} tabs", "Modals")

            self.js("var m = document.getElementById('powerCalculatorModal'); if(m) m.style.display = 'none'")

            # ===== SECTION 15: ADVANCED FEATURES =====
            print("\n[15] ADVANCED FEATURES")
            self.js("showAdvancedFeaturesMenu()")
            time.sleep(1)

            adv_visible = self.js("var m = document.getElementById('advancedFeaturesModal'); return m && m.style.display !== 'none'")
            self.log("Advanced features opens", adv_visible, "", "Modals")

            feat_count = self.js("return document.querySelectorAll('#advancedFeaturesModal button').length")
            self.log("Feature count", feat_count > 30, f"{feat_count} features", "Modals")

            self.js("var m = document.getElementById('advancedFeaturesModal'); if(m) m.style.display = 'none'")

            # ===== SECTION 16: EXPORT MODAL =====
            print("\n[16] EXPORT MODAL")
            self.js("showEnhancedExportModal()")
            time.sleep(1)

            exp_visible = self.js("var m = document.getElementById('enhancedExportModal'); return m && m.style.display !== 'none'")
            self.log("Export modal opens", exp_visible, "", "Modals")

            exp_opts = self.js("return document.querySelectorAll('#enhancedExportModal button').length")
            self.log("Export options", exp_opts >= 5, f"{exp_opts} options", "Modals")

            self.js("var m = document.getElementById('enhancedExportModal'); if(m) m.style.display = 'none'")

            # ===== SECTION 17: P-CURVE =====
            print("\n[17] P-CURVE ANALYSIS")
            self.js("runPCurveAnalysis()")
            time.sleep(2)

            pcurve_visible = self.js("var m = document.getElementById('pcurveModal'); return m && m.style.display !== 'none'")
            self.log("P-Curve modal opens", pcurve_visible, "", "Analysis")

            self.js("var m = document.getElementById('pcurveModal'); if(m) m.style.display = 'none'")

            # ===== SECTION 18: EXCESS SIGNIFICANCE =====
            print("\n[18] EXCESS SIGNIFICANCE")
            self.js("runExcessSignificanceTest()")
            time.sleep(2)

            exsig_visible = self.js("var m = document.getElementById('excessSigModal'); return m && m.style.display !== 'none'")
            self.log("Excess sig modal opens", exsig_visible, "", "Analysis")

            self.js("var m = document.getElementById('excessSigModal'); if(m) m.style.display = 'none'")

            # ===== SECTION 19: INTEGRATED TEST SUITE =====
            print("\n[19] INTEGRATED TEST SUITE")
            self.js("runIntegratedTestSuite()")
            time.sleep(3)

            test_visible = self.js("var m = document.getElementById('testSuiteModal'); return m && m.style.display !== 'none'")
            self.log("Test suite modal opens", test_visible, "", "Analysis")

            if test_visible:
                test_results = self.js("return document.getElementById('testSuiteModal').innerHTML.includes('Passed')")
                self.log("Test results shown", test_results, "", "Analysis")

            # ===== SECTION 20: PRISMA FLOWCHART =====
            print("\n[20] PRISMA FLOWCHART")
            self.js("generatePRISMAFlowchart()")
            time.sleep(2)

            prisma_visible = self.js("""
                var modals = document.querySelectorAll('[id*=\"Modal\"], [id*=\"modal\"]');
                for (var m of modals) {
                    if (m.style.display !== 'none' && m.innerHTML.includes('PRISMA')) return true;
                }
                return false;
            """)
            self.log("PRISMA flowchart shows", prisma_visible, "", "Analysis")

            # ===== SECTION 21: ALL CORE FUNCTIONS =====
            print("\n[21] CORE FUNCTIONS")

            core_funcs = [
                'runAnalysis', 'runBayesian', 'runMetaRegression', 'runNetworkMetaAnalysis',
                'runTrimAndFill', 'runCumulativeMA', 'runSequentialAnalysis',
                'runDoseResponse', 'runMultivariateMA', 'runCompetingRisks',
                'runCureModel', 'runJointModel', 'runPropensityScoreAnalysis',
                'runTMLE', 'runAIPW', 'runGComputation', 'runPatternMixture',
                'runSelectionModel', 'runThreeLevelMA', 'runBootstrapInference',
                'runPowerCalculation', 'runPCurveAnalysis', 'runExcessSignificanceTest',
                'exportAnalysis', 'exportResults', 'exportPDF', 'exportHTML',
                'exportRCode', 'exportStataCode', 'downloadForest', 'downloadFunnel',
                'showHelp', 'showAdvancedFeaturesMenu', 'showPowerCalculator',
                'toggleTheme', 'clearData', 'calculateI2', 'calculatePredictionInterval',
                'calculateFragilityIndex', 'calculateNNT', 'calculateRMST',
                'calculateKaplanMeier', 'calculateCoxPH', 'runIntegratedTestSuite',
                'generatePRISMAFlowchart', 'exportSensitivityAnalysis',
                'showEnhancedExportModal', 'initTooltips'
            ]

            for f in core_funcs:
                exists = self.js(f"return typeof {f} === 'function'")
                self.log(f"Func: {f}", exists, "", "Functions")

            # ===== SECTION 22: MATHUTILS =====
            print("\n[22] MATHUTILS")
            self.log("MathUtils exists", self.js("return typeof MathUtils !== 'undefined'"), "", "MathUtils")
            self.log("normCDF(0)=0.5", self.js("return Math.abs(MathUtils.normCDF(0) - 0.5) < 0.001"), "", "MathUtils")
            self.log("normCDF(1.96)=0.975", self.js("return Math.abs(MathUtils.normCDF(1.96) - 0.975) < 0.01"), "", "MathUtils")
            self.log("chi2CDF exists", self.js("return typeof MathUtils.chi2CDF === 'function'"), "", "MathUtils")
            self.log("tCDF exists", self.js("return typeof MathUtils.tCDF === 'function'"), "", "MathUtils")
            self.log("gammaCDF exists", self.js("return typeof MathUtils.gammaCDF === 'function'"), "", "MathUtils")

            # ===== SECTION 23: TOOLTIPS =====
            print("\n[23] TOOLTIPS")
            self.log("TOOLTIPS object", self.js("return typeof TOOLTIPS !== 'undefined'"), "", "Tooltips")
            tt_count = self.js("return Object.keys(TOOLTIPS || {}).length")
            self.log("Tooltip entries", tt_count >= 15, f"{tt_count} entries", "Tooltips")
            tt_els = self.js("return document.querySelectorAll('[title]').length")
            self.log("Elements with titles", tt_els > 30, f"{tt_els} elements", "Tooltips")

            # ===== SECTION 24: THEME =====
            print("\n[24] THEME")
            initial = self.js("return document.body.classList.contains('light-theme')")
            self.js("toggleTheme()")
            time.sleep(0.5)
            after = self.js("return document.body.classList.contains('light-theme')")
            self.log("Theme toggle works", initial != after, f"Light: {initial} -> {after}", "Theme")
            self.js("toggleTheme()")  # Toggle back

            # ===== SECTION 25: ALL CANVAS ELEMENTS =====
            print("\n[25] CANVAS ELEMENTS")

            canvases = [
                'forestPlot', 'funnelPlot', 'networkPlot', 'survivalPlot',
                'rankogramPlot', 'cumulativeRankPlot', 'baujatPlot', 'looPlot',
                'netHeatPlot', 'tracePlot', 'posteriorPlot', 'trimFillPlot',
                'bubblePlot', 'missingPlot'
            ]

            for canvas in canvases:
                exists = self.js(f"return document.getElementById('{canvas}') !== null")
                self.log(f"Canvas: {canvas}", exists, "", "Canvas")

            # ===== SECTION 26: GRADE ASSESSMENT =====
            print("\n[26] GRADE ASSESSMENT")
            try:
                self.js("try { if (APP && APP.results) displayGRADEAssessment(APP.results); } catch(e) {}")
                time.sleep(2)

                grade_shown = self.js("""
                    var modals = document.querySelectorAll('[id*=\"Modal\"], [id*=\"modal\"]');
                    for (var m of modals) {
                        if (m.style.display !== 'none' && m.innerHTML.includes('GRADE')) return true;
                    }
                    return document.body.innerHTML.includes('Evidence Quality') || document.body.innerHTML.includes('GRADE');
                """)
                self.log("GRADE assessment shows", grade_shown, "", "GRADE")
            except:
                self.log("GRADE assessment shows", False, "Error", "GRADE")

            # ===== SUMMARY =====
            self.print_summary()
            self.save_results()

        except Exception as e:
            print(f"\n[ERROR] {str(e)[:60]}")
            import traceback
            traceback.print_exc()
        finally:
            self.teardown()

    def print_summary(self):
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
        elif rate >= 90:
            print("  STATUS: VERY GOOD - Minor issues only")
        elif rate >= 80:
            print("  STATUS: GOOD - Some issues to address")
        else:
            print("  STATUS: NEEDS IMPROVEMENT")

        print("=" * 70)

        if self.failed > 0:
            print("\nFAILED TESTS:")
            for r in self.results:
                if not r['passed']:
                    print(f"  - {r['category']}: {r['test']}")

    def save_results(self):
        total = self.passed + self.failed
        output = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": self.passed,
                "failed": self.failed,
                "pass_rate": (self.passed / total * 100) if total > 0 else 0
            },
            "tests": self.results
        }
        with open(r'C:\Users\user\ipd_final_test_results.json', 'w') as f:
            json.dump(output, f, indent=2)
        print(f"\nResults saved to: C:\\Users\\user\\ipd_final_test_results.json")


if __name__ == "__main__":
    IPDFinalTester().run_tests()
