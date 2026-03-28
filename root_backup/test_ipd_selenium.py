#!/usr/bin/env python3
"""
Comprehensive Selenium Test Suite for IPD Meta-Analysis Pro
Tests all features to verify 100/100 score
"""

import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class IPDMetaProTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.driver = None
        self.wait = None

    def setup(self):
        """Initialize Chrome WebDriver"""
        print("\n" + "="*70)
        print("IPD META-ANALYSIS PRO - COMPREHENSIVE SELENIUM TEST SUITE")
        print("="*70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*70)

        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')  # Uncomment for headless mode

        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            print("[OK] Chrome WebDriver initialized")
            return True
        except Exception as e:
            print(f"[FAIL] Could not initialize Chrome: {e}")
            return False

    def load_app(self):
        """Load the IPD Meta-Analysis Pro application"""
        filepath = r'C:\Users\user\IPD-Meta-Pro\ipd-meta-pro.html'
        url = f'file:///{filepath.replace(os.sep, "/")}'

        try:
            self.driver.get(url)
            time.sleep(2)

            # Check if page loaded
            title = self.driver.title
            if 'IPD Meta-Analysis Pro' in title:
                self.log_result("App Load", True, f"Title: {title}")
                return True
            else:
                self.log_result("App Load", False, f"Unexpected title: {title}")
                return False
        except Exception as e:
            self.log_result("App Load", False, str(e))
            return False

    def log_result(self, test_name, passed, details=""):
        """Log test result"""
        status = "PASS" if passed else "FAIL"
        self.results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        if passed:
            self.passed += 1
            print(f"  [PASS] {test_name}")
        else:
            self.failed += 1
            print(f"  [FAIL] {test_name}: {details}")

    def click_element(self, selector, by=By.CSS_SELECTOR, timeout=5):
        """Safely click an element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.3)
            element.click()
            return True
        except Exception as e:
            return False

    def element_exists(self, selector, by=By.CSS_SELECTOR, timeout=3):
        """Check if element exists"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return True
        except:
            return False

    def get_text(self, selector, by=By.CSS_SELECTOR, timeout=3):
        """Get text from element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element.text
        except:
            return ""

    def close_modal(self):
        """Close any open modal"""
        try:
            close_btns = self.driver.find_elements(By.CSS_SELECTOR, '.modal-close, .modal-overlay')
            for btn in close_btns:
                try:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(0.3)
                except:
                    pass
        except:
            pass

    # =========================================================================
    # TEST CATEGORIES
    # =========================================================================

    def test_ui_elements(self):
        """Test UI elements are present"""
        print("\n[1] Testing UI Elements...")

        # Header elements
        self.log_result("Logo present",
            self.element_exists('.logo'))

        self.log_result("Theme toggle present",
            self.element_exists('.theme-toggle'))

        self.log_result("Export button present",
            self.element_exists('button[onclick*="Export"]'))

        self.log_result("Help button present",
            self.element_exists('button[onclick*="showHelp"]'))

        # Navigation tabs
        nav_tabs = self.driver.find_elements(By.CSS_SELECTOR, '.nav-tab')
        self.log_result(f"Navigation tabs present ({len(nav_tabs)} tabs)",
            len(nav_tabs) >= 10, f"Found {len(nav_tabs)} tabs")

        # Data panel elements
        self.log_result("Drop zone present",
            self.element_exists('#dropZone'))

        self.log_result("Example data buttons present",
            len(self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="loadExampleData"]')) >= 5)

    def test_theme_toggle(self):
        """Test theme switching"""
        print("\n[2] Testing Theme Toggle...")

        try:
            body = self.driver.find_element(By.TAG_NAME, 'body')
            initial_class = body.get_attribute('class') or ''

            self.click_element('.theme-toggle')
            time.sleep(0.5)

            new_class = body.get_attribute('class') or ''
            theme_changed = initial_class != new_class or 'light-theme' in new_class

            self.log_result("Theme toggle works", theme_changed)

            # Toggle back
            self.click_element('.theme-toggle')
            time.sleep(0.3)

        except Exception as e:
            self.log_result("Theme toggle", False, str(e))

    def test_load_example_datasets(self):
        """Test loading example datasets"""
        print("\n[3] Testing Example Datasets...")

        datasets = [
            ('survival', 'Lung Cancer'),
            ('binary', 'SGLT2'),
            ('continuous', 'Depression'),
        ]

        for dataset_type, name in datasets:
            try:
                btn = self.driver.find_element(
                    By.CSS_SELECTOR, f'button[onclick*="loadExampleData(\'{dataset_type}\')"]'
                )
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(1.5)

                # Check if data loaded
                stats_visible = self.element_exists('#dataPreviewCard[style*="block"], #dataPreviewCard:not([style*="none"])')
                patient_count = self.get_text('#statPatients')

                if patient_count and int(patient_count.replace(',', '')) > 0:
                    self.log_result(f"Load {name} dataset", True, f"{patient_count} patients")
                else:
                    self.log_result(f"Load {name} dataset", stats_visible, "Data preview shown")

            except Exception as e:
                self.log_result(f"Load {name} dataset", False, str(e))

    def test_run_analysis(self):
        """Test running meta-analysis"""
        print("\n[4] Testing Meta-Analysis...")

        try:
            # First load survival data
            btn = self.driver.find_element(
                By.CSS_SELECTOR, 'button[onclick*="loadExampleData(\'survival\')"]'
            )
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(2)

            # Click Run Analysis button
            run_btn = self.driver.find_element(
                By.CSS_SELECTOR, 'button[onclick*="runAnalysis()"]'
            )
            self.driver.execute_script("arguments[0].click();", run_btn)
            time.sleep(3)

            # Check for results
            pooled_effect = self.get_text('#pooledEffect')
            pooled_ci = self.get_text('#pooledCI')
            i2 = self.get_text('#pooledI2')

            if pooled_effect and pooled_effect != '0':
                self.log_result("Run analysis", True, f"Effect: {pooled_effect}, CI: {pooled_ci}, I2: {i2}")
            else:
                self.log_result("Run analysis", False, "No results generated")

        except Exception as e:
            self.log_result("Run analysis", False, str(e))

    def test_navigation_tabs(self):
        """Test all navigation tabs"""
        print("\n[5] Testing Navigation Tabs...")

        tabs = [
            ('data', 'Data'),
            ('covariates', 'Covariates'),
            ('guardian', 'Guardian'),
            ('network', 'Network'),
            ('results', 'Results'),
            ('ranking', 'Ranking'),
            ('heterogeneity', 'Heterogeneity'),
            ('consistency', 'Consistency'),
            ('bayesian', 'Bayesian'),
            ('pubbias', 'Pub Bias'),
            ('metareg', 'Meta-Reg')
        ]

        for panel_id, name in tabs:
            try:
                tab = self.driver.find_element(
                    By.CSS_SELECTOR, f'.nav-tab[data-panel="{panel_id}"]'
                )
                self.driver.execute_script("arguments[0].click();", tab)
                time.sleep(0.5)

                # Check if panel is visible
                panel = self.driver.find_element(By.ID, f'panel-{panel_id}')
                is_active = 'active' in panel.get_attribute('class')

                self.log_result(f"Tab: {name}", is_active)

            except Exception as e:
                self.log_result(f"Tab: {name}", False, str(e))

    def test_help_modal(self):
        """Test help modal"""
        print("\n[6] Testing Help Modal...")

        try:
            self.click_element('button[onclick*="showHelp"]')
            time.sleep(1)

            modal_visible = self.element_exists('.modal-overlay.active, #helpModal.active')
            self.log_result("Help modal opens", modal_visible)

            # Check help tabs
            help_tabs = self.driver.find_elements(By.CSS_SELECTOR, '#helpTabs .inner-tab, #helpModal .inner-tab')
            self.log_result(f"Help tabs present ({len(help_tabs)})", len(help_tabs) >= 3)

            self.close_modal()
            time.sleep(0.5)

        except Exception as e:
            self.log_result("Help modal", False, str(e))

    def test_export_functions(self):
        """Test export functionality"""
        print("\n[7] Testing Export Functions...")

        try:
            # Click enhanced export button
            export_btn = self.driver.find_element(
                By.CSS_SELECTOR, 'button[onclick*="Export"]'
            )
            self.driver.execute_script("arguments[0].click();", export_btn)
            time.sleep(1)

            modal_visible = self.element_exists('.modal-overlay.active')
            self.log_result("Export modal opens", modal_visible)

            # Check for export options
            export_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.modal-overlay.active button')
            self.log_result(f"Export options present ({len(export_buttons)})", len(export_buttons) >= 4)

            self.close_modal()
            time.sleep(0.5)

        except Exception as e:
            self.log_result("Export functions", False, str(e))

    def test_bayesian_analysis(self):
        """Test Bayesian analysis"""
        print("\n[8] Testing Bayesian Analysis...")

        try:
            # Go to Bayesian tab
            tab = self.driver.find_element(By.CSS_SELECTOR, '.nav-tab[data-panel="bayesian"]')
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.5)

            # Check for Bayesian controls
            prior_mean = self.element_exists('#priorMean')
            prior_sd = self.element_exists('#priorSD')
            mcmc_iter = self.element_exists('#mcmcIter')

            self.log_result("Bayesian controls present", prior_mean and prior_sd and mcmc_iter)

            # Run Bayesian analysis
            run_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[onclick*="runBayesian"]')
            self.driver.execute_script("arguments[0].click();", run_btn)
            time.sleep(3)

            # Check for results
            results_visible = self.element_exists('#bayesianResults[style*="block"], #bayesianResults:not([style*="none"])')
            self.log_result("Bayesian analysis runs", results_visible or self.element_exists('#bayesMean'))

        except Exception as e:
            self.log_result("Bayesian analysis", False, str(e))

    def test_publication_bias(self):
        """Test publication bias methods"""
        print("\n[9] Testing Publication Bias...")

        try:
            # Go to pub bias tab
            tab = self.driver.find_element(By.CSS_SELECTOR, '.nav-tab[data-panel="pubbias"]')
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.5)

            # Check for Egger's test results
            egger_z = self.get_text('#eggerZ')
            egger_p = self.get_text('#eggerP')

            self.log_result("Egger's test results", bool(egger_z), f"Z={egger_z}, p={egger_p}")

            # Check for Begg's test
            begg_z = self.get_text('#beggZ')
            self.log_result("Begg's test results", bool(begg_z), f"Z={begg_z}")

            # Test P-Curve analysis button
            pcurve_btn = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="runPCurveAnalysis"]')
            self.log_result("P-Curve button present", len(pcurve_btn) > 0)

            if len(pcurve_btn) > 0:
                self.driver.execute_script("arguments[0].click();", pcurve_btn[0])
                time.sleep(1)
                pcurve_modal = self.element_exists('.modal-overlay.active')
                self.log_result("P-Curve analysis runs", pcurve_modal)
                self.close_modal()

            # Test Excess Significance button
            excess_btn = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="runExcessSignificanceTest"]')
            self.log_result("Excess Significance button present", len(excess_btn) > 0)

        except Exception as e:
            self.log_result("Publication bias", False, str(e))

    def test_meta_regression(self):
        """Test meta-regression"""
        print("\n[10] Testing Meta-Regression...")

        try:
            # Go to meta-reg tab
            tab = self.driver.find_element(By.CSS_SELECTOR, '.nav-tab[data-panel="metareg"]')
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.5)

            # Check for moderator selection
            moderators = self.element_exists('#moderatorVars')
            reg_type = self.element_exists('#metaregType')

            self.log_result("Meta-regression controls present", moderators and reg_type)

            # Run meta-regression
            run_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[onclick*="runMetaRegression"]')
            self.driver.execute_script("arguments[0].click();", run_btn)
            time.sleep(2)

            # Check for results
            r2 = self.get_text('#metaregR2')
            self.log_result("Meta-regression runs", bool(r2), f"R2={r2}")

        except Exception as e:
            self.log_result("Meta-regression", False, str(e))

    def test_network_meta_analysis(self):
        """Test network meta-analysis"""
        print("\n[11] Testing Network Meta-Analysis...")

        try:
            # Go to network tab
            tab = self.driver.find_element(By.CSS_SELECTOR, '.nav-tab[data-panel="network"]')
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.5)

            # Check for network stats
            nodes = self.get_text('#networkNodes')
            edges = self.get_text('#networkEdges')

            self.log_result("Network statistics present", bool(nodes) and bool(edges), f"Nodes={nodes}, Edges={edges}")

            # Check for network plot canvas
            canvas = self.element_exists('#networkPlot')
            self.log_result("Network plot canvas present", canvas)

        except Exception as e:
            self.log_result("Network meta-analysis", False, str(e))

    def test_advanced_features(self):
        """Test advanced features menu"""
        print("\n[12] Testing Advanced Features...")

        try:
            # Go back to data panel
            tab = self.driver.find_element(By.CSS_SELECTOR, '.nav-tab[data-panel="data"]')
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.5)

            # Click Advanced Features button
            adv_btn = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="showAdvancedFeaturesMenu"]')
            if len(adv_btn) > 0:
                self.driver.execute_script("arguments[0].click();", adv_btn[0])
                time.sleep(1)

                modal_visible = self.element_exists('.modal-overlay.active')
                self.log_result("Advanced features menu opens", modal_visible)

                # Count feature buttons
                feature_btns = self.driver.find_elements(By.CSS_SELECTOR, '.modal-overlay.active button')
                self.log_result(f"Advanced features available ({len(feature_btns)})", len(feature_btns) >= 30)

                self.close_modal()
            else:
                self.log_result("Advanced features button", False, "Not found")

        except Exception as e:
            self.log_result("Advanced features", False, str(e))

    def test_power_calculator(self):
        """Test power calculator"""
        print("\n[13] Testing Power Calculator...")

        try:
            # Click power calculator button
            power_btn = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="showPowerCalculator"]')
            if len(power_btn) > 0:
                self.driver.execute_script("arguments[0].click();", power_btn[0])
                time.sleep(1)

                modal_visible = self.element_exists('.modal-overlay.active')
                self.log_result("Power calculator opens", modal_visible)

                # Check for power tabs
                power_tabs = self.driver.find_elements(By.CSS_SELECTOR, '#powerTabs .inner-tab, .modal-overlay.active .inner-tab')
                self.log_result(f"Power calculator tabs ({len(power_tabs)})", len(power_tabs) >= 2)

                # Test calculate power
                calc_btn = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="calculatePower"]')
                if len(calc_btn) > 0:
                    self.driver.execute_script("arguments[0].click();", calc_btn[0])
                    time.sleep(1)

                    result = self.element_exists('#powerResult .stat-value, #powerResult')
                    self.log_result("Power calculation runs", result)

                self.close_modal()
            else:
                self.log_result("Power calculator button", False, "Not found")

        except Exception as e:
            self.log_result("Power calculator", False, str(e))

    def test_sensitivity_analysis(self):
        """Test sensitivity analysis export"""
        print("\n[14] Testing Sensitivity Analysis...")

        try:
            # Check if function exists
            result = self.driver.execute_script("return typeof exportSensitivityAnalysis === 'function'")
            self.log_result("exportSensitivityAnalysis function exists", result)

            result = self.driver.execute_script("return typeof generatePRISMAFlowchart === 'function'")
            self.log_result("generatePRISMAFlowchart function exists", result)

        except Exception as e:
            self.log_result("Sensitivity analysis", False, str(e))

    def test_integrated_test_suite(self):
        """Test the integrated test suite"""
        print("\n[15] Testing Integrated Test Suite...")

        try:
            # Check if function exists
            result = self.driver.execute_script("return typeof runIntegratedTestSuite === 'function'")
            self.log_result("runIntegratedTestSuite function exists", result)

            # Run the integrated test suite
            self.driver.execute_script("runIntegratedTestSuite()")
            time.sleep(2)

            modal_visible = self.element_exists('.modal-overlay.active')
            self.log_result("Integrated test suite runs", modal_visible)

            if modal_visible:
                # Get test results
                passed_text = self.driver.find_elements(By.CSS_SELECTOR, '.modal-overlay.active .stat-value')
                if len(passed_text) >= 2:
                    self.log_result(f"Test suite results shown", True,
                        f"Passed: {passed_text[0].text}, Failed: {passed_text[1].text}")

            self.close_modal()

        except Exception as e:
            self.log_result("Integrated test suite", False, str(e))

    def test_tooltips(self):
        """Test tooltip system"""
        print("\n[16] Testing Tooltip System...")

        try:
            # Check if tooltip initialization function exists
            result = self.driver.execute_script("return typeof initTooltips === 'function'")
            self.log_result("initTooltips function exists", result)

            # Check if TOOLTIPS object exists
            result = self.driver.execute_script("return typeof TOOLTIPS === 'object'")
            self.log_result("TOOLTIPS object exists", result)

            # Check for tooltip icons
            tooltip_icons = self.driver.find_elements(By.CSS_SELECTOR, '.tooltip-icon, [title]')
            self.log_result(f"Tooltip elements present ({len(tooltip_icons)})", len(tooltip_icons) > 0)

        except Exception as e:
            self.log_result("Tooltip system", False, str(e))

    def test_grade_assessment(self):
        """Test GRADE assessment"""
        print("\n[17] Testing GRADE Assessment...")

        try:
            grade_btn = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="GRADE"], button[title*="GRADE"]')
            self.log_result("GRADE button present", len(grade_btn) > 0)

            if len(grade_btn) > 0:
                self.driver.execute_script("arguments[0].click();", grade_btn[0])
                time.sleep(1)

                modal_visible = self.element_exists('.modal-overlay.active')
                self.log_result("GRADE assessment runs", modal_visible)
                self.close_modal()

        except Exception as e:
            self.log_result("GRADE assessment", False, str(e))

    def test_masem(self):
        """Test MASEM mediation analysis"""
        print("\n[18] Testing MASEM Mediation...")

        try:
            masem_btn = self.driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="MASEM"], button[title*="MASEM"]')
            self.log_result("MASEM button present", len(masem_btn) > 0)

        except Exception as e:
            self.log_result("MASEM", False, str(e))

    def test_heterogeneity_panel(self):
        """Test heterogeneity panel"""
        print("\n[19] Testing Heterogeneity Panel...")

        try:
            # Go to heterogeneity tab
            tab = self.driver.find_element(By.CSS_SELECTOR, '.nav-tab[data-panel="heterogeneity"]')
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.5)

            # Check stats
            i2 = self.get_text('#hetI2')
            tau2 = self.get_text('#hetTau2')
            q = self.get_text('#hetQ')

            self.log_result("Heterogeneity statistics", bool(i2), f"I2={i2}, tau2={tau2}, Q={q}")

            # Check for plots
            baujat = self.element_exists('#baujatPlot')
            loo = self.element_exists('#looPlot')
            self.log_result("Heterogeneity plots present", baujat and loo)

        except Exception as e:
            self.log_result("Heterogeneity panel", False, str(e))

    def test_ranking_panel(self):
        """Test ranking panel"""
        print("\n[20] Testing Ranking Panel...")

        try:
            # Go to ranking tab
            tab = self.driver.find_element(By.CSS_SELECTOR, '.nav-tab[data-panel="ranking"]')
            self.driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.5)

            # Check for ranking table
            ranking_table = self.element_exists('#rankingTable, #rankingTableBody')
            self.log_result("Ranking table present", ranking_table)

            # Check for rankogram
            rankogram = self.element_exists('#rankogramPlot')
            cumulative = self.element_exists('#cumulativeRankPlot')
            self.log_result("Ranking plots present", rankogram and cumulative)

        except Exception as e:
            self.log_result("Ranking panel", False, str(e))

    def test_javascript_functions(self):
        """Test key JavaScript functions exist"""
        print("\n[21] Testing JavaScript Functions...")

        functions = [
            'runAnalysis',
            'runBayesian',
            'runMetaRegression',
            'runNetworkMetaAnalysis',
            'exportAnalysis',
            'showAdvancedFeaturesMenu',
            'showPowerCalculator',
            'exportSensitivityAnalysis',
            'generatePRISMAFlowchart',
            'runPCurveAnalysis',
            'runExcessSignificanceTest',
            'runIntegratedTestSuite',
            'initTooltips',
            'showEnhancedExportModal'
        ]

        for func in functions:
            try:
                result = self.driver.execute_script(f"return typeof {func} === 'function'")
                self.log_result(f"Function: {func}", result)
            except Exception as e:
                self.log_result(f"Function: {func}", False, str(e))

    def test_math_utils(self):
        """Test MathUtils statistical functions"""
        print("\n[22] Testing MathUtils Functions...")

        tests = [
            ("MathUtils.normCDF(0) ≈ 0.5", "Math.abs(MathUtils.normCDF(0) - 0.5) < 0.001"),
            ("MathUtils.normCDF(1.96) ≈ 0.975", "Math.abs(MathUtils.normCDF(1.96) - 0.975) < 0.001"),
            ("MathUtils.normQuantile(0.5) ≈ 0", "Math.abs(MathUtils.normQuantile(0.5)) < 0.001"),
            ("MathUtils.normQuantile(0.975) ≈ 1.96", "Math.abs(MathUtils.normQuantile(0.975) - 1.96) < 0.01"),
        ]

        for name, test_code in tests:
            try:
                result = self.driver.execute_script(f"return {test_code}")
                self.log_result(name, result)
            except Exception as e:
                self.log_result(name, False, str(e))

    def run_all_tests(self):
        """Run all tests"""
        if not self.setup():
            return

        if not self.load_app():
            self.cleanup()
            return

        try:
            self.test_ui_elements()
            self.test_theme_toggle()
            self.test_load_example_datasets()
            self.test_run_analysis()
            self.test_navigation_tabs()
            self.test_help_modal()
            self.test_export_functions()
            self.test_bayesian_analysis()
            self.test_publication_bias()
            self.test_meta_regression()
            self.test_network_meta_analysis()
            self.test_advanced_features()
            self.test_power_calculator()
            self.test_sensitivity_analysis()
            self.test_integrated_test_suite()
            self.test_tooltips()
            self.test_grade_assessment()
            self.test_masem()
            self.test_heterogeneity_panel()
            self.test_ranking_panel()
            self.test_javascript_functions()
            self.test_math_utils()

        except Exception as e:
            print(f"\n[ERROR] Test suite error: {e}")

        self.print_summary()
        self.save_results()
        self.cleanup()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0

        print(f"  Total Tests: {total}")
        print(f"  Passed:      {self.passed}")
        print(f"  Failed:      {self.failed}")
        print(f"  Pass Rate:   {pass_rate:.1f}%")
        print("-"*70)

        if pass_rate >= 95:
            print("  STATUS: EXCELLENT - App is fully functional!")
        elif pass_rate >= 80:
            print("  STATUS: GOOD - Minor issues detected")
        elif pass_rate >= 60:
            print("  STATUS: FAIR - Some features need attention")
        else:
            print("  STATUS: NEEDS WORK - Multiple issues detected")

        print("="*70)

    def save_results(self):
        """Save test results to JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': self.passed + self.failed,
                'passed': self.passed,
                'failed': self.failed,
                'pass_rate': (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0
            },
            'tests': self.results
        }

        filepath = r'C:\Users\user\ipd_selenium_test_results.json'
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nResults saved to: {filepath}")

    def cleanup(self):
        """Clean up WebDriver"""
        if self.driver:
            time.sleep(2)  # Allow user to see final state
            self.driver.quit()
            print("\n[OK] Browser closed")


if __name__ == '__main__':
    tester = IPDMetaProTester()
    tester.run_all_tests()
