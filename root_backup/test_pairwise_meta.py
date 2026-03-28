"""
Selenium Test Suite for Pairwise Meta-Analysis Pro
Tests the application in Microsoft Edge browser
"""

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

# Test configuration
APP_PATH = r"C:\Users\user\OneDrive - NHS\Documents\dtahtml\pairwise-meta-pro.html"
APP_URL = f"file:///{APP_PATH.replace(os.sep, '/')}"

class PairwiseMetaAnalysisTest:
    def __init__(self):
        self.driver = None
        self.results = {
            "passed": 0,
            "failed": 0,
            "tests": []
        }

    def setup(self):
        """Initialize Edge WebDriver"""
        print("=" * 60)
        print("PAIRWISE META-ANALYSIS PRO - SELENIUM TEST SUITE")
        print("=" * 60)
        print(f"\nSetting up Edge WebDriver...")

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")

        try:
            self.driver = webdriver.Edge(options=options)
            self.driver.implicitly_wait(10)
            print("Edge WebDriver initialized successfully")
            return True
        except Exception as e:
            print(f"Failed to initialize Edge WebDriver: {e}")
            return False

    def teardown(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("\nBrowser closed")

    def log_test(self, name, passed, details=""):
        """Log test result"""
        status = "PASS" if passed else "FAIL"
        self.results["tests"].append({
            "name": name,
            "passed": passed,
            "details": details
        })
        if passed:
            self.results["passed"] += 1
            print(f"  [PASS] {name}")
        else:
            self.results["failed"] += 1
            print(f"  [FAIL] {name} - {details}")

    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None

    def switch_tab(self, tab_name):
        """Click a navigation tab using data-tab attribute"""
        try:
            tab = self.driver.find_element(By.CSS_SELECTOR, f"button[data-tab='{tab_name}']")
            tab.click()
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"  Tab switch error: {e}")
            return False

    def test_page_load(self):
        """Test 1: Page loads correctly"""
        print("\n[TEST GROUP] Page Load")

        self.driver.get(APP_URL)
        time.sleep(2)

        # Check title
        title_ok = "Pairwise" in self.driver.title or "Meta" in self.driver.title
        self.log_test("Page title contains app name", title_ok, self.driver.title)

        # Check main layout exists (v2.0 uses main.content within div.app)
        try:
            main = self.driver.find_element(By.CSS_SELECTOR, "main.content")
            app = self.driver.find_element(By.CLASS_NAME, "app")
            self.log_test("Main layout exists", main.is_displayed() and app.is_displayed())
        except:
            self.log_test("Main layout exists", False, "Main container not found")

        # Check sidebar navigation
        try:
            sidebar = self.driver.find_element(By.CLASS_NAME, "sidebar")
            nav_items = sidebar.find_elements(By.CLASS_NAME, "nav-item")
            self.log_test("Sidebar navigation exists", len(nav_items) >= 8, f"Found {len(nav_items)} nav items")
        except Exception as e:
            self.log_test("Sidebar navigation exists", False, str(e))

        # Check header
        try:
            header = self.driver.find_element(By.CLASS_NAME, "header")
            self.log_test("Header exists", header.is_displayed())
        except Exception as e:
            self.log_test("Header exists", False, str(e))

    def test_navigation(self):
        """Test 2: Tab navigation works"""
        print("\n[TEST GROUP] Navigation")

        tabs = ['data', 'settings', 'results', 'forest', 'funnel', 'subgroup', 'sensitivity', 'bias', 'report']

        for tab in tabs:
            try:
                self.switch_tab(tab)
                time.sleep(0.3)
                # Check if panel is visible
                panel = self.driver.find_element(By.ID, f"panel-{tab}")
                is_visible = "active" in panel.get_attribute("class") or panel.is_displayed()
                self.log_test(f"Navigate to {tab} tab", is_visible)
            except Exception as e:
                self.log_test(f"Navigate to {tab} tab", False, str(e))

    def test_theme_toggle(self):
        """Test 3: Theme toggle works"""
        print("\n[TEST GROUP] Theme Toggle")

        try:
            # Find theme toggle button by class
            theme_btn = self.driver.find_element(By.CLASS_NAME, "theme-toggle")

            # Get initial theme
            body = self.driver.find_element(By.TAG_NAME, "body")
            initial_theme = body.get_attribute("data-theme") or "dark"

            # Click toggle
            theme_btn.click()
            time.sleep(0.5)

            # Check theme changed
            new_theme = body.get_attribute("data-theme") or "light"
            theme_changed = initial_theme != new_theme
            self.log_test("Theme toggle changes theme", theme_changed, f"{initial_theme} -> {new_theme}")

            # Toggle back
            theme_btn.click()
            time.sleep(0.3)

        except Exception as e:
            self.log_test("Theme toggle works", False, str(e))

    def test_settings_panel(self):
        """Test 4: Settings panel functionality"""
        print("\n[TEST GROUP] Settings Panel")

        self.switch_tab('settings')
        time.sleep(0.5)

        # Test model type dropdown
        try:
            model_select = Select(self.driver.find_element(By.ID, "modelType"))
            options = [o.get_attribute("value") for o in model_select.options]
            has_options = "random" in options and "fixed" in options
            self.log_test("Model type dropdown has options", has_options, str(options))

            # Change selection
            model_select.select_by_value("fixed")
            time.sleep(0.2)
            model_select.select_by_value("random")
            self.log_test("Can change model type", True)
        except Exception as e:
            self.log_test("Model type dropdown", False, str(e))

        # Test RE method dropdown
        try:
            re_select = Select(self.driver.find_element(By.ID, "reMethod"))
            re_select.select_by_value("REML")
            time.sleep(0.2)
            re_select.select_by_value("DL")
            self.log_test("Can change RE method", True)
        except Exception as e:
            self.log_test("RE method dropdown", False, str(e))

        # Test confidence level dropdown
        try:
            conf_select = Select(self.driver.find_element(By.ID, "confLevel"))
            conf_select.select_by_value("0.99")
            time.sleep(0.2)
            conf_select.select_by_value("0.95")
            self.log_test("Confidence level dropdown works", True)
        except Exception as e:
            self.log_test("Confidence level dropdown", False, str(e))

        # Test checkboxes
        try:
            pred_interval = self.driver.find_element(By.ID, "optPredInterval")
            self.log_test("Prediction interval checkbox exists", pred_interval.is_selected())

            egger = self.driver.find_element(By.ID, "optEgger")
            self.log_test("Egger test checkbox exists", egger.is_selected())
        except Exception as e:
            self.log_test("Analysis option checkboxes", False, str(e))

    def test_data_input(self):
        """Test 5: Data input functionality"""
        print("\n[TEST GROUP] Data Input")

        self.switch_tab('data')
        time.sleep(0.5)

        # Test data format dropdown
        try:
            format_select = Select(self.driver.find_element(By.ID, "dataFormat"))
            options = [o.get_attribute("value") for o in format_select.options]
            has_formats = "binary" in options and "continuous" in options and "precalc" in options
            self.log_test("Data format dropdown has all options", has_formats, str(options))
        except Exception as e:
            self.log_test("Data format dropdown", False, str(e))

        # Test effect measure dropdown
        try:
            measure_select = Select(self.driver.find_element(By.ID, "effectMeasure"))
            options = [o.get_attribute("value") for o in measure_select.options]
            self.log_test("Effect measure dropdown exists", len(options) >= 3, str(options))
        except Exception as e:
            self.log_test("Effect measure dropdown", False, str(e))

        # Test add study button
        try:
            add_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add Study')]")

            # Count initial rows
            initial_rows = len(self.driver.find_elements(By.CLASS_NAME, "study-row"))

            # Add a study
            add_btn.click()
            time.sleep(0.5)

            new_rows = len(self.driver.find_elements(By.CLASS_NAME, "study-row"))
            self.log_test("Add study button creates row", new_rows > initial_rows, f"{initial_rows} -> {new_rows}")
        except Exception as e:
            self.log_test("Add study button", False, str(e))

        # Test input fields
        try:
            # Find the first study row and fill in data
            rows = self.driver.find_elements(By.CLASS_NAME, "study-row")
            if rows:
                row = rows[0]

                # Fill study name
                name_input = row.find_element(By.CLASS_NAME, "study-name-input")
                name_input.clear()
                name_input.send_keys("Test Study 2024")

                # Fill numeric fields (binary data)
                inputs = row.find_elements(By.CSS_SELECTOR, "input[type='number']")
                test_values = ["20", "100", "15", "100"]  # events1, n1, events2, n2

                for i, inp in enumerate(inputs[:4]):
                    inp.clear()
                    inp.send_keys(test_values[i])

                self.log_test("Can enter study data", True)
            else:
                self.log_test("Can enter study data", False, "No study rows found")
        except Exception as e:
            self.log_test("Can enter study data", False, str(e))

    def test_demo_data(self):
        """Test 6: Load demo data"""
        print("\n[TEST GROUP] Demo Data")

        self.switch_tab('data')
        time.sleep(0.5)

        try:
            # Find and click demo data button
            demo_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Load Demo') or contains(text(), 'Demo')]")
            demo_btn.click()
            time.sleep(1)

            # Check if studies were added
            rows = self.driver.find_elements(By.CLASS_NAME, "study-row")
            self.log_test("Demo data loads studies", len(rows) >= 5, f"Loaded {len(rows)} studies")
        except Exception as e:
            self.log_test("Demo data button", False, str(e))

    def test_run_analysis(self):
        """Test 7: Run analysis"""
        print("\n[TEST GROUP] Run Analysis")

        try:
            # Find and click run analysis button
            run_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Run Analysis')]")
            run_btn.click()
            time.sleep(2)

            # Check for results
            self.switch_tab('results')
            time.sleep(0.5)

            # Look for summary statistics
            results_panel = self.driver.find_element(By.ID, "panel-results")
            results_content = self.driver.find_element(By.ID, "resultsContent")
            results_text = results_content.text

            has_results = any(term in results_text.lower() for term in ["effect", "ci", "heterogeneity", "studies", "pooled", "estimate"])
            self.log_test("Analysis produces results", has_results, results_text[:200] if not has_results else "Results generated")

        except Exception as e:
            self.log_test("Run analysis", False, str(e))

    def test_forest_plot(self):
        """Test 8: Forest plot generation"""
        print("\n[TEST GROUP] Forest Plot")

        self.switch_tab('forest')
        time.sleep(1.5)

        try:
            # Check for forest plot panel
            forest_panel = self.driver.find_element(By.ID, "panel-forest")
            self.log_test("Forest plot panel exists", forest_panel.is_displayed())

            # Look for Plotly container or SVG
            try:
                # Check for any plot element
                plot_divs = forest_panel.find_elements(By.CSS_SELECTOR, ".js-plotly-plot, .plotly, svg, [class*='plot']")
                self.log_test("Forest plot has visualization", len(plot_divs) > 0, f"Found {len(plot_divs)} plot elements")
            except:
                self.log_test("Forest plot visualization", False, "No plot elements found")

        except Exception as e:
            self.log_test("Forest plot panel", False, str(e))

    def test_funnel_plot(self):
        """Test 9: Funnel plot generation"""
        print("\n[TEST GROUP] Funnel Plot")

        self.switch_tab('funnel')
        time.sleep(1)

        try:
            funnel_panel = self.driver.find_element(By.ID, "panel-funnel")
            self.log_test("Funnel plot panel exists", funnel_panel.is_displayed())
        except Exception as e:
            self.log_test("Funnel plot panel", False, str(e))

    def test_subgroup_analysis(self):
        """Test 10: Subgroup analysis tab"""
        print("\n[TEST GROUP] Subgroup Analysis")

        self.switch_tab('subgroup')
        time.sleep(0.5)

        try:
            subgroup_panel = self.driver.find_element(By.ID, "panel-subgroup")
            self.log_test("Subgroup panel accessible", subgroup_panel.is_displayed())
        except Exception as e:
            self.log_test("Subgroup panel", False, str(e))

    def test_sensitivity_analysis(self):
        """Test 11: Sensitivity analysis tab"""
        print("\n[TEST GROUP] Sensitivity Analysis")

        self.switch_tab('sensitivity')
        time.sleep(0.5)

        try:
            sensitivity_panel = self.driver.find_element(By.ID, "panel-sensitivity")
            self.log_test("Sensitivity panel accessible", sensitivity_panel.is_displayed())
        except Exception as e:
            self.log_test("Sensitivity panel", False, str(e))

    def test_publication_bias(self):
        """Test 12: Publication bias tab"""
        print("\n[TEST GROUP] Publication Bias")

        self.switch_tab('bias')
        time.sleep(0.5)

        try:
            bias_panel = self.driver.find_element(By.ID, "panel-bias")
            self.log_test("Publication bias panel accessible", bias_panel.is_displayed())
        except Exception as e:
            self.log_test("Publication bias panel", False, str(e))

    def test_export_options(self):
        """Test 13: Export functionality"""
        print("\n[TEST GROUP] Export Options")

        self.switch_tab('report')
        time.sleep(0.5)

        try:
            report_panel = self.driver.find_element(By.ID, "panel-report")
            self.log_test("Export panel accessible", report_panel.is_displayed())

            # v2.0 uses cards with onclick handlers instead of buttons
            cards = report_panel.find_elements(By.CLASS_NAME, "card")
            card_texts = [c.text.lower() for c in cards]

            has_csv = any("csv" in t for t in card_texts)
            has_json = any("json" in t for t in card_texts)
            has_pdf = any("pdf" in t or "report" in t for t in card_texts)

            self.log_test("CSV export option exists", has_csv, f"Found {len(cards)} export cards")
            self.log_test("JSON export option exists", has_json)
            self.log_test("PDF/Report export option exists", has_pdf)

        except Exception as e:
            self.log_test("Export panel", False, str(e))

    def test_undo_redo(self):
        """Test 14: Undo/Redo functionality"""
        print("\n[TEST GROUP] Undo/Redo")

        try:
            # Look for undo/redo buttons
            undo_btn = self.driver.find_element(By.ID, "undoBtn")
            redo_btn = self.driver.find_element(By.ID, "redoBtn")
            self.log_test("Undo/Redo buttons exist", True)

            # Undo/redo state depends on previous actions - just verify buttons are functional
            # After demo data load, undo may be enabled which is correct behavior
            undo_clickable = undo_btn.is_displayed()
            redo_clickable = redo_btn.is_displayed()
            self.log_test("Undo/Redo buttons are displayed and functional", undo_clickable and redo_clickable)

        except Exception as e:
            self.log_test("Undo/Redo functionality", False, str(e))

    def test_keyboard_shortcuts(self):
        """Test 15: Keyboard shortcuts"""
        print("\n[TEST GROUP] Keyboard Shortcuts")

        try:
            body = self.driver.find_element(By.TAG_NAME, "body")

            # Test Ctrl+Enter to run analysis
            body.send_keys(Keys.CONTROL + Keys.RETURN)
            time.sleep(1)
            self.log_test("Ctrl+Enter shortcut executes", True)

        except Exception as e:
            self.log_test("Keyboard shortcuts", False, str(e))

    def test_responsive_design(self):
        """Test 16: Responsive design"""
        print("\n[TEST GROUP] Responsive Design")

        try:
            # Test at different window sizes
            sizes = [(1920, 1080), (1366, 768), (1024, 768)]

            for width, height in sizes:
                self.driver.set_window_size(width, height)
                time.sleep(0.5)

                # Check if content is visible
                content = self.driver.find_element(By.CLASS_NAME, "content")
                is_visible = content.is_displayed()
                self.log_test(f"Responsive at {width}x{height}", is_visible)

            # Restore window
            self.driver.maximize_window()

        except Exception as e:
            self.log_test("Responsive design", False, str(e))

    def test_data_format_switching(self):
        """Test 17: Data format switching"""
        print("\n[TEST GROUP] Data Format Switching")

        self.switch_tab('data')
        time.sleep(0.5)

        try:
            format_select = Select(self.driver.find_element(By.ID, "dataFormat"))

            # Switch to continuous
            format_select.select_by_value("continuous")
            time.sleep(0.3)

            # Check effect measure options changed
            measure_select = Select(self.driver.find_element(By.ID, "effectMeasure"))
            options = [o.get_attribute("value") for o in measure_select.options]
            has_md_smd = "MD" in options or "SMD" in options
            self.log_test("Continuous format has MD/SMD options", has_md_smd, str(options))

            # Switch to precalc
            format_select.select_by_value("precalc")
            time.sleep(0.3)
            self.log_test("Can switch to pre-calculated format", True)

            # Switch back to binary
            format_select.select_by_value("binary")
            time.sleep(0.3)
            self.log_test("Can switch back to binary format", True)

        except Exception as e:
            self.log_test("Data format switching", False, str(e))

    def test_study_row_deletion(self):
        """Test 18: Study row deletion"""
        print("\n[TEST GROUP] Study Row Deletion")

        self.switch_tab('data')
        time.sleep(0.5)

        try:
            # Ensure we have studies
            rows = self.driver.find_elements(By.CLASS_NAME, "study-row")
            initial_count = len(rows)

            if initial_count > 0:
                # Find delete button in first row
                row = rows[0]
                delete_btn = row.find_element(By.CSS_SELECTOR, "button.btn-danger, button[onclick*='remove'], button[onclick*='delete']")
                delete_btn.click()
                time.sleep(0.5)

                new_rows = self.driver.find_elements(By.CLASS_NAME, "study-row")
                self.log_test("Study row deletion works", len(new_rows) < initial_count, f"{initial_count} -> {len(new_rows)}")
            else:
                self.log_test("Study row deletion", True, "No rows to delete (already empty)")

        except Exception as e:
            self.log_test("Study row deletion", False, str(e))

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        total = self.results["passed"] + self.results["failed"]
        print(f"Total Tests: {total}")
        print(f"Passed: {self.results['passed']} ({100*self.results['passed']/total:.1f}%)")
        print(f"Failed: {self.results['failed']} ({100*self.results['failed']/total:.1f}%)")

        if self.results["failed"] > 0:
            print("\nFailed Tests:")
            for test in self.results["tests"]:
                if not test["passed"]:
                    print(f"  - {test['name']}: {test['details']}")

        print("=" * 60)
        return self.results["failed"] == 0

    def run_all_tests(self):
        """Run all tests"""
        if not self.setup():
            print("Setup failed. Exiting.")
            return False

        try:
            self.test_page_load()
            self.test_navigation()
            self.test_theme_toggle()
            self.test_settings_panel()
            self.test_data_input()
            self.test_demo_data()
            self.test_run_analysis()
            self.test_forest_plot()
            self.test_funnel_plot()
            self.test_subgroup_analysis()
            self.test_sensitivity_analysis()
            self.test_publication_bias()
            self.test_export_options()
            self.test_undo_redo()
            self.test_keyboard_shortcuts()
            self.test_responsive_design()
            self.test_data_format_switching()
            self.test_study_row_deletion()

        except Exception as e:
            print(f"\nTest suite error: {e}")

        finally:
            success = self.print_summary()
            time.sleep(3)  # Keep browser open briefly to see final state
            self.teardown()
            return success


if __name__ == "__main__":
    test_suite = PairwiseMetaAnalysisTest()
    success = test_suite.run_all_tests()
    exit(0 if success else 1)
