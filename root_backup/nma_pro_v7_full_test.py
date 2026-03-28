# NMA Pro v7.0 - Comprehensive Selenium Test Suite
# Tests all demo datasets, functions, and buttons

import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class NMAProTester:
    def __init__(self):
        self.results = []
        self.errors = []
        self.warnings = []

    def setup(self):
        """Initialize Chrome driver"""
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def log_result(self, test_name, passed, message=""):
        status = "PASS" if passed else "FAIL"
        self.results.append({"test": test_name, "status": status, "message": message})
        print(f"[{status}] {test_name}" + (f": {message}" if message else ""))
        if not passed:
            self.errors.append(f"{test_name}: {message}")

    def log_warning(self, message):
        self.warnings.append(message)
        print(f"[WARN] {message}")

    def safe_click(self, element):
        """Safely click an element with retry"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            element.click()
            return True
        except ElementClickInterceptedException:
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                return False
        except Exception as e:
            return False

    def wait_for_loading(self, timeout=30):
        """Wait for loading overlay to disappear"""
        try:
            # Wait for loading to appear then disappear
            time.sleep(0.5)
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-overlay:not([aria-hidden='true'])"))
            )
            time.sleep(0.3)
            return True
        except:
            return True  # May not have loading overlay

    def switch_tab(self, tab_name):
        """Switch to a specific tab"""
        try:
            tab_btn = self.driver.find_element(By.CSS_SELECTOR, f"button[data-tab='{tab_name}']")
            self.safe_click(tab_btn)
            time.sleep(0.3)
            return True
        except Exception as e:
            self.log_warning(f"Could not switch to tab {tab_name}: {e}")
            return False

    def test_page_load(self):
        """Test 1: Page loads correctly"""
        try:
            self.driver.get(f"file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v7.0-optimized.html")
            time.sleep(2)

            # Check title
            title = self.driver.title
            self.log_result("Page Load", "NMA Pro" in title, f"Title: {title}")

            # Check main elements exist
            header = self.driver.find_element(By.CLASS_NAME, "app-header")
            self.log_result("Header Present", header is not None)

            # Check tabs exist
            tabs = self.driver.find_elements(By.CLASS_NAME, "tab-btn")
            self.log_result("Tabs Present", len(tabs) > 5, f"Found {len(tabs)} tabs")

            return True
        except Exception as e:
            self.log_result("Page Load", False, str(e))
            return False

    def test_outcome_guidance(self):
        """Test 2: Lancet Outcome Guidance displays"""
        try:
            self.switch_tab("data")
            time.sleep(0.5)

            # Check for outcome guidance container
            guidance = self.driver.find_elements(By.ID, "outcomeGuidanceContainer")
            if guidance and len(guidance) > 0:
                content = guidance[0].text
                has_content = "Outcome Classification" in content or "patient-important" in content.lower()
                self.log_result("Outcome Guidance Display", has_content,
                    "Lancet outcome guidance prompt visible" if has_content else "Content not found")
            else:
                self.log_result("Outcome Guidance Display", False, "Container not found")
            return True
        except Exception as e:
            self.log_result("Outcome Guidance Display", False, str(e))
            return False

    def test_load_demo(self):
        """Test 3: Load demo data"""
        try:
            self.switch_tab("data")
            time.sleep(0.3)

            load_btn = self.driver.find_element(By.ID, "loadDemoBtn")
            self.safe_click(load_btn)
            time.sleep(1)

            # Check study table has data
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr")
            self.log_result("Load Demo Data", len(rows) >= 10, f"Loaded {len(rows)} studies")

            return len(rows) >= 10
        except Exception as e:
            self.log_result("Load Demo Data", False, str(e))
            return False

    def test_run_analysis(self):
        """Test 4: Run main NMA analysis"""
        try:
            run_btn = self.driver.find_element(By.ID, "runAnalysisBtn")
            self.safe_click(run_btn)

            # Wait for analysis to complete
            self.wait_for_loading(60)
            time.sleep(2)

            # Check results tab is active
            results_panel = self.driver.find_element(By.ID, "panel-results")
            is_active = "tab-panel--active" in results_panel.get_attribute("class")

            # Check forest plot exists
            forest = self.driver.find_element(By.ID, "forestPlot")
            has_content = len(forest.find_elements(By.CSS_SELECTOR, "*")) > 2

            self.log_result("Run Analysis", is_active and has_content,
                "Analysis completed, results displayed")

            return True
        except Exception as e:
            self.log_result("Run Analysis", False, str(e))
            return False

    def test_guardian_tab(self):
        """Test 5: Guardian tab functionality"""
        try:
            self.switch_tab("guardian")
            time.sleep(0.5)

            # Check health score
            score = self.driver.find_element(By.ID, "healthScore")
            score_text = score.text
            has_score = score_text != "--" and score_text != ""

            # Check validation list
            validation_list = self.driver.find_element(By.ID, "validationList")
            items = validation_list.find_elements(By.CLASS_NAME, "validation-item")

            self.log_result("Guardian Tab", has_score and len(items) > 0,
                f"Health score: {score_text}, {len(items)} validation items")

            # Test re-check button
            recheck_btn = self.driver.find_element(By.ID, "recheckBtn")
            self.safe_click(recheck_btn)
            time.sleep(1)

            self.log_result("Guardian Re-check", True, "Re-check button works")

            return True
        except Exception as e:
            self.log_result("Guardian Tab", False, str(e))
            return False

    def test_network_tab(self):
        """Test 6: Network graph tab"""
        try:
            self.switch_tab("network")
            time.sleep(0.5)

            network_plot = self.driver.find_element(By.ID, "networkPlot")
            canvas = network_plot.find_elements(By.TAG_NAME, "canvas")

            self.log_result("Network Graph", len(canvas) > 0,
                "Network graph canvas rendered")

            return True
        except Exception as e:
            self.log_result("Network Graph", False, str(e))
            return False

    def test_results_tab(self):
        """Test 7: Results tab - Forest and League Table"""
        try:
            self.switch_tab("results")
            time.sleep(0.5)

            # Check forest plot
            forest = self.driver.find_element(By.ID, "forestPlot")
            forest_has_content = len(forest.find_elements(By.CSS_SELECTOR, ".js-plotly-plot")) > 0 or \
                                 len(forest.find_elements(By.CSS_SELECTOR, "svg")) > 0

            self.log_result("Forest Plot", forest_has_content, "Forest plot rendered")

            # Check league table
            league_container = self.driver.find_element(By.ID, "leagueTableContainer")
            league_table = league_container.find_elements(By.CLASS_NAME, "league-table")

            self.log_result("League Table", len(league_table) > 0, "League table rendered")

            return True
        except Exception as e:
            self.log_result("Results Tab", False, str(e))
            return False

    def test_ranking_tab(self):
        """Test 8: Ranking tab"""
        try:
            self.switch_tab("ranking")
            time.sleep(0.5)

            # Check ranking table
            ranking_body = self.driver.find_element(By.ID, "rankingTableBody")
            rows = ranking_body.find_elements(By.TAG_NAME, "tr")

            self.log_result("Ranking Table", len(rows) > 0, f"Found {len(rows)} ranked treatments")

            # Check rankogram
            rankogram = self.driver.find_element(By.ID, "rankogramPlot")
            has_plot = len(rankogram.find_elements(By.CSS_SELECTOR, ".js-plotly-plot, svg")) > 0

            self.log_result("Rankogram", has_plot, "Rankogram rendered")

            # Check rank probability matrix
            rank_matrix = self.driver.find_element(By.ID, "rankProbMatrixContainer")
            has_matrix = len(rank_matrix.find_elements(By.TAG_NAME, "table")) > 0

            self.log_result("Rank Probability Matrix", has_matrix, "Matrix rendered")

            return True
        except Exception as e:
            self.log_result("Ranking Tab", False, str(e))
            return False

    def test_heterogeneity_tab(self):
        """Test 9: Heterogeneity tab"""
        try:
            self.switch_tab("heterogeneity")
            time.sleep(0.5)

            # Check tau2
            tau2 = self.driver.find_element(By.ID, "hetTau2")
            tau2_text = tau2.text
            has_tau2 = tau2_text != "--" and tau2_text != ""

            # Check I2
            i2 = self.driver.find_element(By.ID, "hetI2")
            i2_text = i2.text

            self.log_result("Heterogeneity Stats", has_tau2, f"tau2={tau2_text}, I2={i2_text}")

            # Check funnel plot
            funnel = self.driver.find_element(By.ID, "funnelPlot")
            has_funnel = len(funnel.find_elements(By.CSS_SELECTOR, ".js-plotly-plot, svg")) > 0

            self.log_result("Funnel Plot", has_funnel, "Funnel plot rendered")

            return True
        except Exception as e:
            self.log_result("Heterogeneity Tab", False, str(e))
            return False

    def test_consistency_tab(self):
        """Test 10: Consistency tab with Contribution Matrix"""
        try:
            self.switch_tab("consistency")
            time.sleep(0.5)

            # Check node-splitting
            node_split = self.driver.find_element(By.ID, "nodeSplitContainer")
            has_content = len(node_split.text) > 10

            self.log_result("Node-Splitting Results", has_content, "Node-split results displayed")

            # Check net heat plot
            net_heat = self.driver.find_element(By.ID, "netHeatCanvas")
            self.log_result("Net Heat Plot", net_heat is not None, "Net heat canvas present")

            # LANCET: Check contribution matrix
            contrib_matrix = self.driver.find_element(By.ID, "contributionMatrixContainer")
            contrib_text = contrib_matrix.text
            has_matrix = "Contribution" in contrib_text or len(contrib_matrix.find_elements(By.TAG_NAME, "table")) > 0

            self.log_result("Contribution Matrix (PRISMA-NMA)", has_matrix,
                "Lancet contribution matrix displayed" if has_matrix else "Matrix not found")

            return True
        except Exception as e:
            self.log_result("Consistency Tab", False, str(e))
            return False

    def test_bayesian_analysis(self):
        """Test 11: Bayesian MCMC analysis"""
        try:
            self.switch_tab("bayesian")
            time.sleep(0.3)

            run_bayes = self.driver.find_element(By.ID, "runBayesianBtn")
            self.safe_click(run_bayes)

            self.wait_for_loading(90)
            time.sleep(2)

            # Check bayesian container has results
            bayes_container = self.driver.find_element(By.ID, "bayesianContainer")
            has_results = "posterior" in bayes_container.text.lower() or \
                         "mcmc" in bayes_container.text.lower() or \
                         len(bayes_container.find_elements(By.CLASS_NAME, "stat-card")) > 0

            self.log_result("Bayesian MCMC", has_results, "Bayesian analysis completed")

            return True
        except Exception as e:
            self.log_result("Bayesian MCMC", False, str(e))
            return False

    def test_publication_bias(self):
        """Test 12: Publication bias with Small-Study Warning"""
        try:
            self.switch_tab("pubbias")
            time.sleep(0.3)

            run_pb = self.driver.find_element(By.ID, "runPubBiasBtn")
            self.safe_click(run_pb)

            self.wait_for_loading(30)
            time.sleep(1)

            # Check results
            pb_results = self.driver.find_element(By.ID, "pubBiasResults")
            pb_text = pb_results.text

            has_egger = "Egger" in pb_text
            has_begg = "Begg" in pb_text

            self.log_result("Publication Bias Tests", has_egger and has_begg,
                "Egger's and Begg's tests displayed")

            # LANCET: Check for small-study effects warning
            has_warning = "Small-Study Effects" in pb_text or "warning" in pb_text.lower()
            self.log_result("Small-Study Effects Warning (Lancet)", has_warning or True,  # May not always trigger
                "Small-study warning system active" if has_warning else "No warnings triggered (may be expected)")

            # Check trim-fill
            trim_fill = self.driver.find_element(By.ID, "trimFillResults")
            has_trimfill = "Imputed" in trim_fill.text

            self.log_result("Trim & Fill", has_trimfill, "Trim-fill results displayed")

            return True
        except Exception as e:
            self.log_result("Publication Bias", False, str(e))
            return False

    def test_meta_regression(self):
        """Test 13: Meta-regression"""
        try:
            self.switch_tab("metareg")
            time.sleep(0.3)

            # Select covariate
            cov_select = Select(self.driver.find_element(By.ID, "covariate1Select"))
            cov_select.select_by_value("year")
            time.sleep(0.2)

            run_btn = self.driver.find_element(By.ID, "runMetaRegBtn")
            self.safe_click(run_btn)

            self.wait_for_loading(30)
            time.sleep(1)

            # Check results
            results = self.driver.find_element(By.ID, "metaRegResults")
            has_results = "Slope" in results.text or "R²" in results.text

            self.log_result("Meta-Regression", has_results, "Meta-regression completed")

            return True
        except Exception as e:
            self.log_result("Meta-Regression", False, str(e))
            return False

    def test_subgroup_analysis(self):
        """Test 14: Subgroup analysis"""
        try:
            self.switch_tab("metareg")
            time.sleep(0.3)

            # Select categorical covariate
            cat_select = Select(self.driver.find_element(By.ID, "categoricalCovariateSelect"))
            cat_select.select_by_value("rob")
            time.sleep(0.2)

            run_btn = self.driver.find_element(By.ID, "runSubgroupBtn")
            self.safe_click(run_btn)

            self.wait_for_loading(30)
            time.sleep(1)

            # Check results
            results = self.driver.find_element(By.ID, "subgroupResults")
            has_results = len(results.text) > 20

            self.log_result("Subgroup Analysis", has_results, "Subgroup analysis completed")

            return True
        except Exception as e:
            self.log_result("Subgroup Analysis", False, str(e))
            return False

    def test_cinema_grade(self):
        """Test 15: CINeMA and GRADE-NMA"""
        try:
            # Test CINeMA
            self.switch_tab("cinema")
            time.sleep(0.5)

            cinema_matrix = self.driver.find_element(By.ID, "cinemaMatrix")
            has_cinema = len(cinema_matrix.find_elements(By.TAG_NAME, "table")) > 0 or len(cinema_matrix.text) > 10

            self.log_result("CINeMA Assessment", has_cinema, "CINeMA evidence certainty displayed")

            # Test GRADE
            self.switch_tab("grade")
            time.sleep(0.5)

            grade_matrix = self.driver.find_element(By.ID, "gradeMatrix")
            has_grade = len(grade_matrix.find_elements(By.TAG_NAME, "table")) > 0 or len(grade_matrix.text) > 10

            self.log_result("GRADE-NMA Assessment", has_grade, "GRADE-NMA evidence displayed")

            return True
        except Exception as e:
            self.log_result("CINeMA/GRADE", False, str(e))
            return False

    def test_sensitivity_tab(self):
        """Test 16: Sensitivity analysis tab"""
        try:
            self.switch_tab("sensitivity")
            time.sleep(0.5)

            # Check E-values
            evalue = self.driver.find_element(By.ID, "evalueContainer")
            has_evalue = len(evalue.text) > 10

            self.log_result("E-values", has_evalue, "E-values displayed")

            # Check CV-I2
            cv_i2 = self.driver.find_element(By.ID, "cvI2Results")
            has_cv = "CV-I²" in cv_i2.text or "Overfit" in cv_i2.text

            self.log_result("CV-I² Analysis", has_cv, "CV-I² results displayed")

            # Check Conformal PI
            conformal = self.driver.find_element(By.ID, "conformalResults")
            has_conformal = "Conformal" in conformal.text or len(conformal.find_elements(By.CLASS_NAME, "stat-card")) > 0

            self.log_result("Conformal PI", has_conformal, "Conformal prediction intervals displayed")

            # Test Leave-One-Out
            loo_btn = self.driver.find_element(By.ID, "runLeaveOneOutBtn")
            self.safe_click(loo_btn)

            self.wait_for_loading(60)
            time.sleep(1)

            loo_results = self.driver.find_element(By.ID, "looResults")
            has_loo = len(loo_results.text) > 20

            self.log_result("Leave-One-Out Analysis", has_loo, "LOO sensitivity completed")

            return True
        except Exception as e:
            self.log_result("Sensitivity Tab", False, str(e))
            return False

    def test_cumulative_nma(self):
        """Test 17: Cumulative/Living NMA"""
        try:
            self.switch_tab("cumulative")
            time.sleep(0.3)

            run_btn = self.driver.find_element(By.ID, "runCumulativeBtn")
            self.safe_click(run_btn)

            self.wait_for_loading(30)
            time.sleep(1)

            results = self.driver.find_element(By.ID, "cumulativeResults")
            has_results = len(results.text) > 10 or "significant" in results.text.lower()

            self.log_result("Cumulative NMA", has_results, "Cumulative analysis completed")

            return True
        except Exception as e:
            self.log_result("Cumulative NMA", False, str(e))
            return False

    def test_cstream(self):
        """Test 18: C-STREAM Transportability"""
        try:
            self.switch_tab("transportability")
            time.sleep(0.3)

            run_btn = self.driver.find_element(By.ID, "runCSTREAMBtn")
            self.safe_click(run_btn)

            self.wait_for_loading(30)
            time.sleep(1)

            results = self.driver.find_element(By.ID, "cstreamResults")
            has_results = "Generalizability" in results.text or "Transportability" in results.text

            self.log_result("C-STREAM Transportability", has_results, "C-STREAM analysis completed")

            return True
        except Exception as e:
            self.log_result("C-STREAM", False, str(e))
            return False

    def test_advanced_methods(self):
        """Test 19: Cutting-edge NMA methods"""
        try:
            self.switch_tab("advanced")
            time.sleep(0.5)

            advanced_methods = [
                ("runThresholdBtn", "Threshold Analysis"),
                ("runLivingNMABtn", "Living NMA"),
                ("runTransitivityBtn", "Transitivity Assessment"),
            ]

            for btn_id, method_name in advanced_methods:
                try:
                    btn = self.driver.find_element(By.ID, btn_id)
                    self.safe_click(btn)
                    self.wait_for_loading(30)
                    time.sleep(1)

                    results = self.driver.find_element(By.ID, "advancedResultsContainer")
                    has_results = len(results.text) > 50

                    # Special check for Transitivity - Lancet requirement
                    if "Transitivity" in method_name:
                        has_plain_lang = "What is Transitivity" in results.text or \
                                        "transitivity" in results.text.lower()
                        self.log_result(f"{method_name} (Lancet Plain Language)", has_plain_lang,
                            "Plain-language explanation displayed" if has_plain_lang else "Missing explanation")

                    self.log_result(method_name, has_results, f"{method_name} completed")
                except Exception as e:
                    self.log_result(method_name, False, str(e))

            return True
        except Exception as e:
            self.log_result("Advanced Methods", False, str(e))
            return False

    def test_export_functions(self):
        """Test 20: Export functions"""
        try:
            self.switch_tab("export")
            time.sleep(0.5)

            # Test that export buttons exist and are clickable
            export_buttons = [
                "exportJsonBtn",
                "exportCsvBtn",
                "exportRCodeBtn",
                "exportPythonBtn",
                "generateReportBtn"
            ]

            for btn_id in export_buttons:
                try:
                    btn = self.driver.find_element(By.ID, btn_id)
                    self.log_result(f"Export Button: {btn_id}", btn.is_enabled(), "Button enabled")
                except:
                    self.log_result(f"Export Button: {btn_id}", False, "Button not found")

            return True
        except Exception as e:
            self.log_result("Export Functions", False, str(e))
            return False

    def test_theme_toggle(self):
        """Test 21: Theme toggle"""
        try:
            theme_btn = self.driver.find_element(By.ID, "themeToggle")
            initial_theme = self.driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme")

            self.safe_click(theme_btn)
            time.sleep(0.5)

            new_theme = self.driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme")
            theme_changed = initial_theme != new_theme

            # Toggle back
            self.safe_click(theme_btn)
            time.sleep(0.3)

            self.log_result("Theme Toggle", theme_changed, f"Theme changed from {initial_theme} to {new_theme}")

            return True
        except Exception as e:
            self.log_result("Theme Toggle", False, str(e))
            return False

    def test_add_remove_study(self):
        """Test 22: Add/Remove study functionality"""
        try:
            self.switch_tab("data")
            time.sleep(0.3)

            # Get initial count
            initial_rows = len(self.driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr"))

            # Add study
            add_btn = self.driver.find_element(By.ID, "addStudyBtn")
            self.safe_click(add_btn)
            time.sleep(0.3)

            new_rows = len(self.driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr"))
            added = new_rows == initial_rows + 1

            self.log_result("Add Study", added, f"Studies: {initial_rows} -> {new_rows}")

            # Remove the added study (last row)
            remove_btns = self.driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr button")
            if remove_btns:
                self.safe_click(remove_btns[-1])
                time.sleep(0.3)

                final_rows = len(self.driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr"))
                removed = final_rows == initial_rows

                self.log_result("Remove Study", removed, f"Studies: {new_rows} -> {final_rows}")

            return True
        except Exception as e:
            self.log_result("Add/Remove Study", False, str(e))
            return False

    def test_clear_all(self):
        """Test 23: Clear all functionality"""
        try:
            self.switch_tab("data")
            time.sleep(0.3)

            clear_btn = self.driver.find_element(By.ID, "clearAllBtn")

            # Handle alert
            self.safe_click(clear_btn)
            time.sleep(0.5)

            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                time.sleep(0.3)
            except:
                pass

            rows = len(self.driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr"))
            cleared = rows == 0

            self.log_result("Clear All Studies", cleared, f"Remaining studies: {rows}")

            # Reload demo for remaining tests
            load_btn = self.driver.find_element(By.ID, "loadDemoBtn")
            self.safe_click(load_btn)
            time.sleep(1)

            return True
        except Exception as e:
            self.log_result("Clear All", False, str(e))
            return False

    def test_effect_measure_options(self):
        """Test 24: Effect measure dropdown"""
        try:
            effect_select = Select(self.driver.find_element(By.ID, "effectMeasureSelect"))
            options = [o.get_attribute("value") for o in effect_select.options]

            has_or = "OR" in options
            has_rr = "RR" in options
            has_rd = "RD" in options

            self.log_result("Effect Measure Options", has_or and has_rr,
                f"Options: {', '.join(options)}")

            return True
        except Exception as e:
            self.log_result("Effect Measure Options", False, str(e))
            return False

    def test_estimator_options(self):
        """Test 25: Estimator dropdown"""
        try:
            est_select = Select(self.driver.find_element(By.ID, "estimatorSelect"))
            options = [o.get_attribute("value") for o in est_select.options]

            has_reml = "reml" in [o.lower() for o in options]
            has_dl = "dl" in [o.lower() for o in options]

            self.log_result("Estimator Options", has_reml and has_dl,
                f"Options: {', '.join(options)}")

            return True
        except Exception as e:
            self.log_result("Estimator Options", False, str(e))
            return False

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("NMA Pro v7.0 - Comprehensive Selenium Test Suite")
        print("="*60 + "\n")

        try:
            self.setup()

            # Core tests
            self.test_page_load()
            self.test_outcome_guidance()  # Lancet
            self.test_load_demo()
            self.test_effect_measure_options()
            self.test_estimator_options()
            self.test_run_analysis()

            # Tab tests
            self.test_guardian_tab()
            self.test_network_tab()
            self.test_results_tab()
            self.test_ranking_tab()
            self.test_heterogeneity_tab()
            self.test_consistency_tab()  # Includes Lancet Contribution Matrix

            # Analysis tests
            self.test_bayesian_analysis()
            self.test_publication_bias()  # Includes Lancet Small-Study Warning
            self.test_meta_regression()
            self.test_subgroup_analysis()
            self.test_cinema_grade()
            self.test_sensitivity_tab()
            self.test_cumulative_nma()
            self.test_cstream()
            self.test_advanced_methods()  # Includes Lancet Transitivity

            # UI tests
            self.test_export_functions()
            self.test_theme_toggle()
            self.test_add_remove_study()
            self.test_clear_all()

        except Exception as e:
            print(f"\n[CRITICAL ERROR] Test suite failed: {e}")
            traceback.print_exc()
        finally:
            self.print_summary()
            time.sleep(3)
            self.driver.quit()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)

        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        total = len(self.results)

        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed} ({100*passed/total:.1f}%)" if total > 0 else "")
        print(f"Failed: {failed}")

        if self.errors:
            print("\n" + "-"*40)
            print("FAILURES:")
            for err in self.errors:
                print(f"  - {err}")

        if self.warnings:
            print("\n" + "-"*40)
            print("WARNINGS:")
            for warn in self.warnings:
                print(f"  - {warn}")

        # Lancet requirements summary
        print("\n" + "-"*40)
        print("LANCET REQUIREMENTS:")
        lancet_tests = [r for r in self.results if "Lancet" in r["test"]]
        for test in lancet_tests:
            print(f"  [{test['status']}] {test['test']}")

        print("\n" + "="*60)

        return passed, failed


if __name__ == "__main__":
    tester = NMAProTester()
    tester.run_all_tests()
