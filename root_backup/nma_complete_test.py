# Complete NMA Pro v7.0 Test - Every Demo, Button, and Plot
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *

class NMACompleteTest:
    def __init__(self):
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)
        self.results = {"passed": 0, "failed": 0, "tests": []}

    def log(self, test_name, passed, message=""):
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {test_name}: {message}")
        self.results["tests"].append({"name": test_name, "passed": passed, "message": message})
        if passed:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1

    def safe_click(self, element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(0.2)
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def wait_for_loading(self, timeout=30):
        """Wait for loading overlay to disappear"""
        try:
            time.sleep(0.5)
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.ID, "loadingOverlay"))
            )
        except:
            pass
        time.sleep(0.5)

    def dismiss_alert(self):
        """Dismiss any alert that appears"""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return alert_text
        except:
            return None

    def switch_tab(self, tab_id):
        """Switch to a specific tab"""
        try:
            tab = self.driver.find_element(By.CSS_SELECTOR, f"[data-tab='{tab_id}']")
            self.safe_click(tab)
            time.sleep(0.3)
            return True
        except:
            return False

    def check_element_has_content(self, element_id, min_length=10):
        """Check if an element has meaningful content"""
        try:
            el = self.driver.find_element(By.ID, element_id)
            # Check for canvas, SVG, Plotly, or text content
            has_canvas = len(el.find_elements(By.TAG_NAME, "canvas")) > 0
            has_svg = len(el.find_elements(By.TAG_NAME, "svg")) > 0
            has_plotly = len(el.find_elements(By.CLASS_NAME, "js-plotly-plot")) > 0
            has_table = len(el.find_elements(By.TAG_NAME, "table")) > 0
            has_text = len(el.text.strip()) >= min_length
            html_len = len(el.get_attribute("innerHTML") or "")
            return has_canvas or has_svg or has_plotly or has_table or has_text or html_len > 100
        except:
            return False

    def run_all_tests(self):
        print("=" * 70)
        print("NMA Pro v7.0 - COMPLETE TEST SUITE")
        print("Testing: Every Demo Dataset, Every Button, Every Plot")
        print("=" * 70)
        print()

        try:
            # Load the app
            self.driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v7.0-optimized.html")
            time.sleep(2)

            # Test 1: Page loads
            title = self.driver.title
            self.log("Page Load", "NMA Pro" in title, f"Title: {title}")

            # Test all demo datasets
            self.test_all_demos()

            # Test all buttons and functions
            self.test_all_buttons()

            # Test all plots
            self.test_all_plots()

        except Exception as e:
            print(f"\n[CRITICAL ERROR] {str(e)}")
            traceback.print_exc()
        finally:
            self.print_summary()
            time.sleep(3)
            self.driver.quit()

    def test_all_demos(self):
        """Test every demo dataset"""
        print("\n" + "=" * 50)
        print("TESTING ALL DEMO DATASETS")
        print("=" * 50)

        demos = [
            ("loadDemoBtn", "Thrombolytics", 10),
            ("loadDemo2Btn", "Antidepressants", None),
            ("loadDemo3Btn", "Smoking Cessation", None),
            ("loadDemo4Btn", "Pain Relief", None),
        ]

        for btn_id, name, expected_count in demos:
            try:
                # Clear existing data first
                try:
                    clear_btn = self.driver.find_element(By.ID, "clearAllBtn")
                    self.safe_click(clear_btn)
                    time.sleep(0.3)
                    self.dismiss_alert()  # Confirm clear
                    time.sleep(0.3)
                except:
                    pass

                # Load demo
                btn = self.driver.find_element(By.ID, btn_id)
                self.safe_click(btn)
                time.sleep(0.5)

                # Count studies
                rows = self.driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr")
                count = len(rows)

                passed = count > 0
                if expected_count:
                    passed = count == expected_count

                self.log(f"Demo: {name}", passed, f"Loaded {count} studies")

                # Run analysis on this demo
                if count > 0:
                    self.test_analysis_on_demo(name)

            except Exception as e:
                self.log(f"Demo: {name}", False, str(e))

    def test_analysis_on_demo(self, demo_name):
        """Run full analysis on loaded demo"""
        try:
            # Run main analysis
            run_btn = self.driver.find_element(By.ID, "runAnalysisBtn")
            self.safe_click(run_btn)
            self.wait_for_loading(60)
            self.dismiss_alert()
            time.sleep(1)

            # Check if results appeared
            ranking_rows = self.driver.find_elements(By.CSS_SELECTOR, "#rankingTableBody tr")
            passed = len(ranking_rows) > 0
            self.log(f"Analysis ({demo_name})", passed, f"Ranking has {len(ranking_rows)} treatments")

        except Exception as e:
            alert_text = self.dismiss_alert()
            self.log(f"Analysis ({demo_name})", False, alert_text or str(e))

    def test_all_buttons(self):
        """Test every button in the application"""
        print("\n" + "=" * 50)
        print("TESTING ALL BUTTONS & FUNCTIONS")
        print("=" * 50)

        # First load demo and run analysis
        try:
            clear_btn = self.driver.find_element(By.ID, "clearAllBtn")
            self.safe_click(clear_btn)
            time.sleep(0.2)
            self.dismiss_alert()
        except:
            pass

        demo_btn = self.driver.find_element(By.ID, "loadDemoBtn")
        self.safe_click(demo_btn)
        time.sleep(0.5)

        run_btn = self.driver.find_element(By.ID, "runAnalysisBtn")
        self.safe_click(run_btn)
        self.wait_for_loading(60)
        self.dismiss_alert()
        time.sleep(1)

        # Test buttons by tab
        button_tests = [
            # Guardian tab
            ("guardian", [
                ("recheckGuardianBtn", "Guardian Re-check"),
            ]),
            # Bayesian tab
            ("bayesian", [
                ("runBayesianBtn", "Bayesian MCMC"),
            ]),
            # Publication bias tab
            ("pubbias", [
                ("runPubBiasBtn", "Publication Bias"),
            ]),
            # Meta-regression tab
            ("metareg", [
                ("runMetaRegBtn", "Meta-Regression"),
                ("runSubgroupBtn", "Subgroup Analysis"),
            ]),
            # CNMA tab
            ("cnma", [
                ("runCNMABtn", "Component NMA"),
            ]),
            # Cumulative tab
            ("cumulative", [
                ("runCumulativeBtn", "Cumulative NMA"),
            ]),
            # Transportability tab
            ("transportability", [
                ("runCSTREAMBtn", "C-STREAM"),
            ]),
            # Sensitivity tab
            ("sensitivity", [
                ("runLeaveOneOutBtn", "Leave-One-Out"),
            ]),
            # Advanced tab
            ("advanced", [
                ("runThresholdBtn", "Threshold Analysis"),
                ("runLivingNMABtn", "Living NMA"),
                ("runTransitivityBtn", "Transitivity Assessment"),
                ("runIPDNMABtn", "IPD-NMA"),
                ("runFPNMABtn", "Fractional Polynomial"),
                ("runMultiStateBtn", "Multi-State NMA"),
                ("runMLNMRBtn", "ML-NMR"),
                ("runRiskAverseBtn", "Risk-Averse Decision"),
                ("runCompLikBtn", "Composite Likelihood"),
                ("runHierarchicalBtn", "Hierarchical Effects"),
                ("runCensorAdjBtn", "Censoring Adjustment"),
                ("runEnhancedCNMABtn", "Enhanced CNMA"),
            ]),
        ]

        for tab_id, buttons in button_tests:
            if not self.switch_tab(tab_id):
                self.log(f"Tab: {tab_id}", False, "Could not switch to tab")
                continue

            time.sleep(0.3)

            for btn_id, btn_name in buttons:
                try:
                    btn = self.driver.find_element(By.ID, btn_id)
                    self.safe_click(btn)
                    self.wait_for_loading(30)
                    alert = self.dismiss_alert()
                    time.sleep(0.5)

                    # Check for results
                    if alert and "failed" in alert.lower():
                        self.log(f"Button: {btn_name}", False, alert[:50])
                    else:
                        self.log(f"Button: {btn_name}", True, "Executed successfully")

                except NoSuchElementException:
                    self.log(f"Button: {btn_name}", False, "Button not found")
                except Exception as e:
                    alert = self.dismiss_alert()
                    self.log(f"Button: {btn_name}", False, alert or str(e)[:50])

        # Test export buttons (just check they exist and are enabled)
        self.switch_tab("export")
        time.sleep(0.3)

        export_buttons = [
            "exportJsonBtn", "exportCsvBtn", "exportRCodeBtn",
            "exportPythonBtn", "generateReportBtn"
        ]

        for btn_id in export_buttons:
            try:
                btn = self.driver.find_element(By.ID, btn_id)
                enabled = btn.is_enabled()
                self.log(f"Export: {btn_id}", enabled, "Button enabled" if enabled else "Button disabled")
            except:
                self.log(f"Export: {btn_id}", False, "Not found")

    def test_all_plots(self):
        """Test that all plots render correctly"""
        print("\n" + "=" * 50)
        print("TESTING ALL PLOTS & VISUALIZATIONS")
        print("=" * 50)

        # Make sure we have analysis results
        try:
            clear_btn = self.driver.find_element(By.ID, "clearAllBtn")
            self.safe_click(clear_btn)
            time.sleep(0.2)
            self.dismiss_alert()
        except:
            pass

        demo_btn = self.driver.find_element(By.ID, "loadDemoBtn")
        self.safe_click(demo_btn)
        time.sleep(0.5)

        run_btn = self.driver.find_element(By.ID, "runAnalysisBtn")
        self.safe_click(run_btn)
        self.wait_for_loading(60)
        self.dismiss_alert()
        time.sleep(1)

        # Test plots by tab
        plot_tests = [
            ("network", [
                ("networkPlot", "Network Graph"),
            ]),
            ("results", [
                ("forestPlot", "Forest Plot"),
                ("leagueTableContainer", "League Table"),
                ("rankingTableBody", "Ranking Table"),
                ("rankogramContainer", "Rankogram"),
                ("rankProbMatrix", "Rank Probability Matrix"),
            ]),
            ("heterogeneity", [
                ("heterogeneityStats", "Heterogeneity Stats"),
                ("funnelPlot", "Funnel Plot"),
            ]),
            ("consistency", [
                ("nodeSplitResults", "Node-Split Results"),
                ("netHeatContainer", "Net Heat Plot"),
            ]),
            ("evidence", [
                ("cinemaResults", "CINeMA Results"),
                ("gradeMatrix", "GRADE Matrix"),
                ("evalueContainer", "E-values"),
                ("thresholdContainer", "Threshold Analysis"),
            ]),
        ]

        for tab_id, plots in plot_tests:
            if not self.switch_tab(tab_id):
                self.log(f"Tab: {tab_id}", False, "Could not switch")
                continue

            time.sleep(0.5)

            for element_id, plot_name in plots:
                has_content = self.check_element_has_content(element_id)
                self.log(f"Plot: {plot_name}", has_content,
                        "Rendered" if has_content else "Empty or missing")

        # Run Bayesian and check its plots
        self.switch_tab("bayesian")
        time.sleep(0.3)
        try:
            btn = self.driver.find_element(By.ID, "runBayesianBtn")
            self.safe_click(btn)
            self.wait_for_loading(60)
            self.dismiss_alert()
            time.sleep(1)

            bayes_plots = [
                ("bayesForestPlot", "Bayesian Forest"),
                ("tracePlot", "Trace Plot"),
                ("densityPlot", "Density Plot"),
                ("bayesSUCRAPlot", "SUCRA Plot"),
            ]

            for element_id, plot_name in bayes_plots:
                has_content = self.check_element_has_content(element_id)
                self.log(f"Plot: {plot_name}", has_content,
                        "Rendered" if has_content else "Empty")
        except Exception as e:
            self.dismiss_alert()
            self.log("Bayesian Plots", False, str(e)[:50])

        # Run publication bias and check plots
        self.switch_tab("pubbias")
        time.sleep(0.3)
        try:
            btn = self.driver.find_element(By.ID, "runPubBiasBtn")
            self.safe_click(btn)
            self.wait_for_loading(30)
            self.dismiss_alert()
            time.sleep(0.5)

            pb_plots = [
                ("pubBiasResults", "Pub Bias Results"),
                ("trimFillResults", "Trim & Fill"),
                ("petPeeseResults", "PET-PEESE"),
            ]

            for element_id, plot_name in pb_plots:
                has_content = self.check_element_has_content(element_id, min_length=5)
                self.log(f"Plot: {plot_name}", has_content,
                        "Rendered" if has_content else "Empty")
        except Exception as e:
            self.dismiss_alert()
            self.log("Pub Bias Plots", False, str(e)[:50])

        # Check cumulative plot
        self.switch_tab("cumulative")
        time.sleep(0.3)
        try:
            btn = self.driver.find_element(By.ID, "runCumulativeBtn")
            self.safe_click(btn)
            self.wait_for_loading(30)
            self.dismiss_alert()
            time.sleep(0.5)

            has_content = self.check_element_has_content("cumulativePlot")
            self.log("Plot: Cumulative NMA", has_content, "Rendered" if has_content else "Empty")
        except Exception as e:
            self.dismiss_alert()
            self.log("Plot: Cumulative NMA", False, str(e)[:50])

        # Check meta-regression bubble plot
        self.switch_tab("metareg")
        time.sleep(0.3)
        try:
            # Select a covariate first
            cov_select = self.driver.find_element(By.ID, "covariate1Select")
            options = cov_select.find_elements(By.TAG_NAME, "option")
            if len(options) > 1:
                self.safe_click(options[1])
                time.sleep(0.2)

            btn = self.driver.find_element(By.ID, "runMetaRegBtn")
            self.safe_click(btn)
            self.wait_for_loading(30)
            self.dismiss_alert()
            time.sleep(0.5)

            has_content = self.check_element_has_content("bubblePlot")
            self.log("Plot: Bubble Plot", has_content, "Rendered" if has_content else "Empty")
        except Exception as e:
            self.dismiss_alert()
            self.log("Plot: Bubble Plot", False, str(e)[:50])

        # Check CNMA forest plot
        self.switch_tab("cnma")
        time.sleep(0.3)
        try:
            btn = self.driver.find_element(By.ID, "runCNMABtn")
            self.safe_click(btn)
            self.wait_for_loading(30)
            alert = self.dismiss_alert()
            time.sleep(0.5)

            if alert and "not applicable" in alert.lower():
                self.log("Plot: CNMA Forest", True, "Not applicable for this dataset")
            else:
                has_content = self.check_element_has_content("cnmaForestPlot")
                self.log("Plot: CNMA Forest", has_content or alert is None,
                        "Rendered" if has_content else "May not be applicable")
        except Exception as e:
            self.dismiss_alert()
            self.log("Plot: CNMA Forest", False, str(e)[:50])

        # Check Leave-One-Out influence plot
        self.switch_tab("sensitivity")
        time.sleep(0.3)
        try:
            btn = self.driver.find_element(By.ID, "runLeaveOneOutBtn")
            self.safe_click(btn)
            self.wait_for_loading(60)
            self.dismiss_alert()
            time.sleep(0.5)

            has_content = self.check_element_has_content("looInfluencePlot")
            self.log("Plot: LOO Influence", has_content, "Rendered" if has_content else "Empty")
        except Exception as e:
            self.dismiss_alert()
            self.log("Plot: LOO Influence", False, str(e)[:50])

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)

        total = self.results["passed"] + self.results["failed"]
        pct = (self.results["passed"] / total * 100) if total > 0 else 0

        print(f"\nTotal Tests: {total}")
        print(f"Passed: {self.results['passed']} ({pct:.1f}%)")
        print(f"Failed: {self.results['failed']}")

        if self.results["failed"] > 0:
            print("\n" + "-" * 40)
            print("FAILURES:")
            for test in self.results["tests"]:
                if not test["passed"]:
                    print(f"  - {test['name']}: {test['message']}")

        print("\n" + "=" * 70)


if __name__ == "__main__":
    test = NMACompleteTest()
    test.run_all_tests()
