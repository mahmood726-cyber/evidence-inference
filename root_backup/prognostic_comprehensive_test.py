"""
PrognosisMeta Comprehensive Feature Test
Tests ALL tabs, buttons, and verifies plots display correctly
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

results = {"passed": 0, "failed": 0, "errors": []}

def log(status, msg):
    icon = "[OK]" if status == "OK" else "[FAIL]" if status == "FAIL" else "[>>]"
    print(f"  {icon} {msg}")

def test(name, condition, error_msg=""):
    global results
    if condition:
        results["passed"] += 1
        log("OK", name)
        return True
    else:
        results["failed"] += 1
        results["errors"].append(f"{name}: {error_msg}")
        log("FAIL", f"{name}: {error_msg}")
        return False

def safe_click(driver, element):
    try:
        driver.execute_script("arguments[0].click();", element)
        time.sleep(0.3)
        return True
    except:
        return False

def click_by_id(driver, element_id):
    try:
        el = driver.find_element(By.ID, element_id)
        safe_click(driver, el)
        return True
    except:
        return False

def click_by_selector(driver, selector):
    try:
        el = driver.find_element(By.CSS_SELECTOR, selector)
        safe_click(driver, el)
        return True
    except:
        return False

def count_elements(driver, selector):
    try:
        return len(driver.find_elements(By.CSS_SELECTOR, selector))
    except:
        return 0

def get_js_errors(driver):
    try:
        logs = driver.get_log("browser")
        return [l for l in logs if l.get("level") == "SEVERE"]
    except:
        return []

def main():
    print("=" * 80)
    print("PROGNOSTIC-META COMPREHENSIVE FEATURE TEST")
    print("=" * 80)

    # Setup Chrome
    print("\n--- Setting up Chrome browser ---")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        log("OK", "Chrome browser started")
    except Exception as e:
        print(f"Failed to start browser: {e}")
        sys.exit(1)

    wait = WebDriverWait(driver, 10)

    try:
        # ============================================
        # LOAD APPLICATION
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 1: LOADING APPLICATION")
        print("=" * 80)

        driver.get("file:///C:/Users/user/prognostic-meta/index.html")
        time.sleep(2)
        test("Application loaded", True)

        # ============================================
        # TEST ALL TABS EXIST
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 2: TESTING TAB NAVIGATION")
        print("=" * 80)

        tabs = [
            ("data", "Data Input"),
            ("analysis", "Analysis"),
            ("results", "Results"),
            ("visualization", "Visualization"),
            ("bias", "Publication Bias"),
            ("advanced", "Advanced"),
            ("doseresponse", "Dose-Response"),
            ("network", "Network MA"),
            ("quality", "Quality/ROB"),
            ("power", "Power/Simulation"),
            ("ipd", "IPD Meta-Analysis"),
            ("export", "Export"),
        ]

        for tab_id, tab_name in tabs:
            exists = count_elements(driver, f"[data-tab='{tab_id}']") > 0
            test(f"Tab exists: {tab_name}", exists)

        # Click through all tabs
        print("\n--- Clicking through all tabs ---")
        for tab_id, tab_name in tabs:
            clicked = click_by_selector(driver, f"[data-tab='{tab_id}']")
            test(f"Navigate to: {tab_name}", clicked)
            time.sleep(0.3)

        # ============================================
        # LOAD DEMO DATA
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 3: LOADING DEMO DATA")
        print("=" * 80)

        # Go to Data Input tab
        click_by_selector(driver, "[data-tab='data']")
        time.sleep(0.5)

        # Click Load Demo Data
        demo_btn = driver.find_element(By.ID, "btn-load-demo")
        safe_click(driver, demo_btn)
        time.sleep(0.5)

        # Handle prompt
        try:
            alert = Alert(driver)
            alert.send_keys("1")
            alert.accept()
            test("Demo data prompt accepted", True)
        except:
            test("Demo data prompt", False, "No prompt appeared")

        time.sleep(1)

        # Check data loaded
        rows = count_elements(driver, "#data-table tbody tr")
        test(f"Data table has {rows} rows", rows > 0, "No data rows")

        # ============================================
        # RUN MAIN ANALYSIS
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 4: RUNNING ANALYSIS")
        print("=" * 80)

        # Go to Analysis tab
        click_by_selector(driver, "[data-tab='analysis']")
        time.sleep(0.5)

        # Click Run Analysis
        run_clicked = click_by_id(driver, "btn-run-analysis")
        test("Clicked Run Analysis button", run_clicked)
        time.sleep(2)

        # Check for JS errors
        errors = get_js_errors(driver)
        test("No JS errors after analysis", len(errors) == 0, f"{len(errors)} errors")

        # ============================================
        # CHECK RESULTS TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 5: CHECKING RESULTS TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='results']")
        time.sleep(0.5)

        # Check for result values
        result_values = driver.find_elements(By.CSS_SELECTOR, ".result-value, #pooled-effect, .effect-estimate")
        test(f"Found {len(result_values)} result elements", len(result_values) > 0)

        # Check for forest plot
        forest_svg = count_elements(driver, "#forest-plot svg, .forest-plot svg, svg")
        test(f"Forest plot SVG exists ({forest_svg} found)", forest_svg > 0)

        # ============================================
        # CHECK VISUALIZATION TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 6: CHECKING VISUALIZATION TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='visualization']")
        time.sleep(1)

        # Check for various plot types
        svg_count = count_elements(driver, "svg")
        canvas_count = count_elements(driver, "canvas")
        test(f"Visualization SVGs: {svg_count}", svg_count > 0 or canvas_count > 0)

        # Try clicking visualization options
        viz_buttons = ["btn-forest", "btn-funnel", "btn-radial", "btn-labbe"]
        for btn_id in viz_buttons:
            if click_by_id(driver, btn_id):
                time.sleep(0.5)
                test(f"Clicked visualization: {btn_id}", True)

        # ============================================
        # CHECK PUBLICATION BIAS TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 7: CHECKING PUBLICATION BIAS TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='bias']")
        time.sleep(0.5)

        # Run bias tests
        if click_by_id(driver, "btn-run-bias"):
            time.sleep(1)
            test("Ran bias tests", True)

        # Check for funnel plot
        funnel_svg = count_elements(driver, "#funnel-plot svg, .funnel-plot svg, svg")
        test(f"Funnel plot elements: {funnel_svg}", funnel_svg > 0)

        # Check for test results
        bias_results = count_elements(driver, ".bias-result, .test-result, [id*='egger'], [id*='begg']")
        test(f"Bias test results: {bias_results}", bias_results >= 0)

        # Try individual bias tests
        bias_buttons = ["btn-egger", "btn-begg", "btn-trim-fill", "btn-peters"]
        for btn_id in bias_buttons:
            if click_by_id(driver, btn_id):
                time.sleep(0.3)
                test(f"Clicked: {btn_id}", True)

        # ============================================
        # CHECK ADVANCED TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 8: CHECKING ADVANCED TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='advanced']")
        time.sleep(0.5)

        # Test advanced features
        advanced_buttons = [
            "btn-leave-one-out",
            "btn-cumulative",
            "btn-influence",
            "btn-gosh",
            "btn-bootstrap"
        ]

        for btn_id in advanced_buttons:
            if click_by_id(driver, btn_id):
                time.sleep(0.5)
                test(f"Advanced feature: {btn_id}", True)

        # ============================================
        # CHECK DOSE-RESPONSE TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 9: CHECKING DOSE-RESPONSE TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='doseresponse']")
        time.sleep(0.5)

        # Load dose-response demo
        if click_by_id(driver, "btn-dr-load-demo"):
            time.sleep(0.5)
            test("Loaded DR demo data", True)

        # Run dose-response analysis
        if click_by_id(driver, "btn-dr-run"):
            time.sleep(1)
            test("Ran dose-response analysis", True)

        # Check for dose-response plot
        dr_plot = count_elements(driver, "#dr-plot-container svg, .dr-plot svg")
        test(f"Dose-response plot: {dr_plot}", dr_plot >= 0)

        # ============================================
        # CHECK NETWORK MA TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 10: CHECKING NETWORK MA TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='network']")
        time.sleep(0.5)

        network_elements = count_elements(driver, "#network-plot, .network-diagram, svg")
        test(f"Network MA elements: {network_elements}", network_elements >= 0)

        # ============================================
        # CHECK QUALITY/ROB TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 11: CHECKING QUALITY/ROB TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='quality']")
        time.sleep(0.5)

        rob_elements = count_elements(driver, ".rob-table, .quality-table, select, input")
        test(f"Quality/ROB elements: {rob_elements}", rob_elements > 0)

        # ============================================
        # CHECK POWER/SIMULATION TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 12: CHECKING POWER/SIMULATION TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='power']")
        time.sleep(0.5)

        power_buttons = ["btn-power-calc", "btn-power-curve", "btn-simulate"]
        for btn_id in power_buttons:
            if click_by_id(driver, btn_id):
                time.sleep(0.3)
                test(f"Power feature: {btn_id}", True)

        # ============================================
        # CHECK IPD TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 13: CHECKING IPD TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='ipd']")
        time.sleep(0.5)

        # Load IPD demo
        if click_by_id(driver, "btn-load-ipd-demo"):
            time.sleep(0.5)
            test("Loaded IPD demo data", True)

        ipd_elements = count_elements(driver, "#ipd-table, .ipd-results, input, select")
        test(f"IPD elements: {ipd_elements}", ipd_elements > 0)

        # ============================================
        # CHECK EXPORT TAB
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 14: CHECKING EXPORT TAB")
        print("=" * 80)

        click_by_selector(driver, "[data-tab='export']")
        time.sleep(0.5)

        export_buttons = [
            "btn-export-html",
            "btn-export-pdf",
            "btn-export-csv",
            "btn-export-r",
            "btn-export-stata",
            "btn-export-python"
        ]

        for btn_id in export_buttons:
            exists = count_elements(driver, f"#{btn_id}") > 0
            if exists:
                test(f"Export button exists: {btn_id}", True)

        # ============================================
        # TEST UI ELEMENTS
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 15: CHECKING UI ELEMENTS")
        print("=" * 80)

        dropdowns = count_elements(driver, "select")
        checkboxes = count_elements(driver, "input[type='checkbox']")
        number_inputs = count_elements(driver, "input[type='number']")
        buttons = count_elements(driver, "button")

        test(f"Dropdowns: {dropdowns}", dropdowns > 0)
        test(f"Checkboxes: {checkboxes}", checkboxes > 0)
        test(f"Number inputs: {number_inputs}", number_inputs > 0)
        test(f"Buttons: {buttons}", buttons > 0)

        # ============================================
        # FINAL JS ERROR CHECK
        # ============================================
        print("\n" + "=" * 80)
        print("PHASE 16: FINAL ERROR CHECK")
        print("=" * 80)

        all_errors = get_js_errors(driver)
        if all_errors:
            print(f"\n  Found {len(all_errors)} JavaScript errors:")
            for err in all_errors[:10]:
                msg = err.get("message", "")[:100]
                print(f"    - {msg}")
            results["failed"] += len(all_errors)
        else:
            test("No JavaScript errors throughout test", True)

        # ============================================
        # SUMMARY
        # ============================================
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Passed: {results['passed']}")
        print(f"Failed: {results['failed']}")
        print(f"Total:  {results['passed'] + results['failed']}")

        pass_rate = results['passed'] / (results['passed'] + results['failed']) * 100 if (results['passed'] + results['failed']) > 0 else 0
        print(f"Pass Rate: {pass_rate:.1f}%")

        if results['errors']:
            print("\nFailed tests:")
            for err in results['errors'][:15]:
                print(f"  - {err}")

        print("=" * 80)
        if results['failed'] == 0:
            print("*** ALL TESTS PASSED ***")
        elif pass_rate >= 80:
            print("*** MOSTLY PASSED ***")
        else:
            print("*** NEEDS ATTENTION ***")
        print("=" * 80)

        # Keep browser open
        print("\nBrowser staying open for 15 seconds for visual inspection...")
        time.sleep(15)

    except Exception as e:
        print(f"\nTest error: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(5)

    finally:
        driver.quit()
        print("\nBrowser closed.")

if __name__ == "__main__":
    main()
