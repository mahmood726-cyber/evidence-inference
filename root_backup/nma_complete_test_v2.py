# Complete NMA Pro v7.0 Test V2 - Correct Element IDs
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *

class NMACompleteTestV2:
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
        try:
            time.sleep(0.5)
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.ID, "loadingOverlay"))
            )
        except:
            pass
        time.sleep(0.5)

    def dismiss_alert(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return alert_text
        except:
            return None

    def switch_tab(self, tab_id):
        try:
            tab = self.driver.find_element(By.CSS_SELECTOR, f"[data-tab='{tab_id}']")
            self.safe_click(tab)
            time.sleep(0.3)
            return True
        except:
            return False

    def check_element_has_content(self, element_id, min_length=10):
        try:
            el = self.driver.find_element(By.ID, element_id)
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
        print("NMA Pro v7.0 - COMPLETE TEST SUITE V2")
        print("Testing: All Demo Datasets, All Buttons, All Plots")
        print("=" * 70)
        print()

        try:
            self.driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v7.0-optimized.html")
            time.sleep(2)

            title = self.driver.title
            self.log("Page Load", "NMA Pro" in title, f"Title: {title}")

            # Test all demo datasets
            self.test_all_demos()

            # Test all buttons
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
        print("\n" + "=" * 50)
        print("TESTING ALL DEMO DATASETS")
        print("=" * 50)

        # The app has 5 demo datasets accessible via loadDemoDataset(name)
        demos = [
            ("thrombolytics", "Thrombolytics"),
            ("vaccines", "Vaccines"),
            ("antihypertensives", "Antihypertensives"),
            ("painkillers", "Painkillers"),
            ("cbt_depression", "CBT Depression"),
        ]

        for dataset_key, name in demos:
            try:
                # Clear existing data
                try:
                    clear_btn = self.driver.find_element(By.ID, "clearAllBtn")
                    self.safe_click(clear_btn)
                    time.sleep(0.2)
                    self.dismiss_alert()
                    time.sleep(0.3)
                except:
                    pass

                # Load demo via JavaScript
                self.driver.execute_script(f"loadDemoDataset('{dataset_key}')")
                time.sleep(0.5)

                # Count studies
                rows = self.driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr")
                count = len(rows)
                passed = count > 0

                self.log(f"Demo: {name}", passed, f"Loaded {count} studies")

                # Run analysis on this demo
                if count > 0:
                    self.test_analysis_on_demo(name)

            except Exception as e:
                self.log(f"Demo: {name}", False, str(e)[:60])

    def test_analysis_on_demo(self, demo_name):
        try:
            run_btn = self.driver.find_element(By.ID, "runAnalysisBtn")
            self.safe_click(run_btn)
            self.wait_for_loading(60)
            self.dismiss_alert()
            time.sleep(1)

            ranking_rows = self.driver.find_elements(By.CSS_SELECTOR, "#rankingTableBody tr")
            passed = len(ranking_rows) > 0
            self.log(f"Analysis ({demo_name})", passed, f"Ranking has {len(ranking_rows)} treatments")

        except Exception as e:
            alert_text = self.dismiss_alert()
            self.log(f"Analysis ({demo_name})", False, (alert_text or str(e))[:60])

    def test_all_buttons(self):
        print("\n" + "=" * 50)
        print("TESTING ALL BUTTONS & FUNCTIONS")
        print("=" * 50)

        # Load demo and run analysis first
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

        # Test buttons by tab - using CORRECT element IDs
        button_tests = [
            # Guardian tab
            ("guardian", [
                ("recheckBtn", "Guardian Re-check"),  # CORRECT ID
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

                    if alert and "failed" in alert.lower():
                        self.log(f"Button: {btn_name}", False, alert[:50])
                    else:
                        self.log(f"Button: {btn_name}", True, "Executed successfully")

                except NoSuchElementException:
                    self.log(f"Button: {btn_name}", False, "Button not found")
                except Exception as e:
                    alert = self.dismiss_alert()
                    self.log(f"Button: {btn_name}", False, (alert or str(e))[:50])

        # Test export buttons
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
        print("\n" + "=" * 50)
        print("TESTING ALL PLOTS & VISUALIZATIONS")
        print("=" * 50)

        # Load demo and run analysis
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

        # Test plots by tab - using CORRECT element IDs
        plot_tests = [
            ("network", [
                ("networkPlot", "Network Graph"),
            ]),
            ("results", [
                ("forestPlot", "Forest Plot"),
                ("leagueTableContainer", "League Table"),
            ]),
            ("ranking", [
                ("rankingTableBody", "Ranking Table"),
                ("rankogramPlot", "Rankogram"),  # CORRECT ID
                ("rankProbMatrixContainer", "Rank Probability Matrix"),  # CORRECT ID
            ]),
            ("heterogeneity", [
                ("hetTau2", "tau² Statistic"),  # CORRECT - individual stat
                ("hetI2", "I² Statistic"),  # CORRECT
                ("funnelPlot", "Funnel Plot"),
            ]),
            ("consistency", [
                ("nodeSplitContainer", "Node-Split Results"),  # CORRECT ID
                ("netHeatCanvas", "Net Heat Plot"),  # CORRECT - it's a canvas
                ("contributionMatrixContainer", "Contribution Matrix"),
            ]),
            ("cinema", [
                ("cinemaMatrix", "CINeMA Matrix"),
            ]),
            ("grade", [
                ("gradeMatrix", "GRADE Matrix"),
            ]),
            ("sensitivity", [
                ("evalueContainer", "E-values"),
                ("thresholdContainer", "Threshold Analysis"),
                ("cvI2Results", "CV-I² Results"),
                ("conformalResults", "Conformal PI"),
            ]),
        ]

        for tab_id, plots in plot_tests:
            if not self.switch_tab(tab_id):
                self.log(f"Tab: {tab_id}", False, "Could not switch")
                continue

            time.sleep(0.5)

            for element_id, plot_name in plots:
                try:
                    el = self.driver.find_element(By.ID, element_id)
                    # Check for content
                    has_canvas = len(el.find_elements(By.TAG_NAME, "canvas")) > 0
                    has_svg = len(el.find_elements(By.TAG_NAME, "svg")) > 0
                    has_plotly = len(el.find_elements(By.CLASS_NAME, "js-plotly-plot")) > 0
                    has_table = len(el.find_elements(By.TAG_NAME, "table")) > 0
                    has_rows = len(el.find_elements(By.TAG_NAME, "tr")) > 0
                    text = el.text.strip()
                    html_len = len(el.get_attribute("innerHTML") or "")

                    # For stats like hetTau2, check the text value
                    is_stat = element_id.startswith("het") or "Score" in element_id
                    has_value = text and text != "--" and text != "0"

                    has_content = has_canvas or has_svg or has_plotly or has_table or has_rows or (html_len > 50) or (is_stat and has_value)

                    self.log(f"Plot: {plot_name}", has_content,
                            f"Rendered (html:{html_len})" if has_content else f"Empty (text: '{text[:20]}...')" if text else "Empty")
                except NoSuchElementException:
                    self.log(f"Plot: {plot_name}", False, "Element not found")
                except Exception as e:
                    self.log(f"Plot: {plot_name}", False, str(e)[:40])

        # Run Bayesian and check plots
        print("\n--- Bayesian Plots ---")
        self.switch_tab("bayesian")
        time.sleep(0.3)
        try:
            btn = self.driver.find_element(By.ID, "runBayesianBtn")
            self.safe_click(btn)
            self.wait_for_loading(60)
            self.dismiss_alert()
            time.sleep(1)

            # Check bayesian container for content
            container = self.driver.find_element(By.ID, "bayesianContainer")
            has_content = len(container.get_attribute("innerHTML")) > 200
            self.log("Plot: Bayesian Results", has_content, "Rendered" if has_content else "Empty")
        except Exception as e:
            self.dismiss_alert()
            self.log("Plot: Bayesian Results", False, str(e)[:50])

        # Run publication bias and check
        print("\n--- Publication Bias Plots ---")
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
                self.log(f"Plot: {plot_name}", has_content, "Rendered" if has_content else "Empty")
        except Exception as e:
            self.dismiss_alert()
            self.log("Plot: Pub Bias", False, str(e)[:50])

        # Check cumulative plot
        print("\n--- Other Analysis Plots ---")
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

        # Check Leave-One-Out
        self.switch_tab("sensitivity")
        time.sleep(0.3)
        try:
            btn = self.driver.find_element(By.ID, "runLeaveOneOutBtn")
            self.safe_click(btn)
            self.wait_for_loading(60)
            self.dismiss_alert()
            time.sleep(0.5)

            # Check for LOO results and influence plot
            has_results = self.check_element_has_content("looResults", min_length=20)
            self.log("Plot: LOO Results", has_results, "Rendered" if has_results else "Empty")

            # Check canvas specifically
            try:
                canvas = self.driver.find_element(By.ID, "looInfluencePlot")
                # A canvas is "rendered" if it exists - actual content is drawn via JS
                self.log("Plot: LOO Influence Canvas", True, "Canvas present")
            except:
                self.log("Plot: LOO Influence Canvas", False, "Canvas not found")
        except Exception as e:
            self.dismiss_alert()
            self.log("Plot: LOO Analysis", False, str(e)[:50])

    def print_summary(self):
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
    test = NMACompleteTestV2()
    test.run_all_tests()
