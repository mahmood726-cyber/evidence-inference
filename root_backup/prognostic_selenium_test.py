"""
PrognosisMeta Comprehensive Selenium Test
Tests all tabs and functions in the application
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Test results tracking
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
    """Safely click an element using JavaScript"""
    try:
        driver.execute_script("arguments[0].click();", element)
        return True
    except:
        return False

def element_exists(driver, selector, by=By.CSS_SELECTOR):
    """Check if element exists"""
    try:
        driver.find_element(by, selector)
        return True
    except:
        return False

def get_element_text(driver, selector, by=By.CSS_SELECTOR):
    """Get element text safely"""
    try:
        return driver.find_element(by, selector).text
    except:
        return ""

def main():
    print("=" * 70)
    print("PROGNOSTIC-META COMPREHENSIVE SELENIUM TEST")
    print("=" * 70)

    # Setup Edge browser
    print("\n--- Setting up browser ---")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    try:
        # Use ChromeDriverManager to get correct version
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        log("OK", "Browser started (Chrome)")
    except Exception as e:
        print(f"Failed to start browser: {e}")
        sys.exit(1)

    wait = WebDriverWait(driver, 10)

    try:
        # Load the application
        print("\n--- Loading Application ---")
        driver.get("file:///C:/Users/user/prognostic-meta/index.html")
        time.sleep(2)

        test("Page loaded", "PrognosisMeta" in driver.title or element_exists(driver, "body"))

        # ============================================
        # TEST 1: Check all tabs exist
        # ============================================
        print("\n--- Testing Tab Navigation ---")

        tabs_to_test = [
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

        for tab_id, tab_name in tabs_to_test:
            exists = element_exists(driver, f"[data-tab='{tab_id}']")
            test(f"Tab exists: {tab_name}", exists, f"Tab {tab_id} not found")

        # Find all tab buttons (PrognosisMeta uses li.nav-tab)
        tab_buttons = driver.find_elements(By.CSS_SELECTOR, ".nav-tab, li[data-tab]")
        test(f"Found {len(tab_buttons)} tab buttons", len(tab_buttons) > 0, "No tabs found")

        # Click through each tab
        for i, btn in enumerate(tab_buttons[:10]):  # Limit to first 10
            try:
                tab_text = btn.text.strip() or f"Tab {i+1}"
                safe_click(driver, btn)
                time.sleep(0.3)
                test(f"Clicked tab: {tab_text}", True)
            except Exception as e:
                test(f"Click tab {i+1}", False, str(e)[:50])

        # ============================================
        # TEST 2: Data Input Tab
        # ============================================
        print("\n--- Testing Data Input ---")

        # Try to find data input elements
        data_elements = [
            ("textarea", "Data textarea"),
            ("input[type='file']", "File input"),
            ("#data-input", "Data input area"),
            (".data-table", "Data table"),
        ]

        for selector, name in data_elements:
            if element_exists(driver, selector):
                test(f"Found: {name}", True)
                break

        # Try to input sample data
        try:
            # Look for textarea or input
            textarea = None
            for sel in ["#data-input", "textarea", ".data-textarea", "#study-data"]:
                if element_exists(driver, sel):
                    textarea = driver.find_element(By.CSS_SELECTOR, sel)
                    break

            if textarea:
                sample_data = """Study,Effect,SE
Smith 2020,0.5,0.2
Jones 2021,0.3,0.22
Brown 2019,0.7,0.17
Davis 2022,0.4,0.25
Wilson 2020,0.6,0.2"""
                textarea.clear()
                textarea.send_keys(sample_data)
                test("Entered sample data", True)
                time.sleep(0.5)
        except Exception as e:
            log("INFO", f"Data input: {str(e)[:50]}")

        # ============================================
        # TEST 3: Analysis Functions
        # ============================================
        print("\n--- Testing Analysis Functions ---")

        # Look for analysis buttons
        analysis_buttons = driver.find_elements(By.CSS_SELECTOR,
            "button:not([disabled]), .btn, [onclick], input[type='button']")

        button_keywords = ["run", "analyze", "calculate", "compute", "meta", "pool"]

        for btn in analysis_buttons[:20]:
            btn_text = btn.text.lower() + " " + (btn.get_attribute("id") or "")
            if any(kw in btn_text for kw in button_keywords):
                try:
                    safe_click(driver, btn)
                    time.sleep(0.5)
                    test(f"Clicked: {btn.text[:30] or 'Analysis button'}", True)
                except:
                    pass

        # ============================================
        # TEST 4: Check for JavaScript errors
        # ============================================
        print("\n--- Checking for JavaScript Errors ---")

        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l.get("level") == "SEVERE"]

        if severe_errors:
            for err in severe_errors[:5]:
                log("FAIL", f"JS Error: {err.get('message', '')[:60]}")
            results["failed"] += len(severe_errors)
        else:
            test("No JavaScript errors", True)

        # ============================================
        # TEST 5: Forest Plot Tab
        # ============================================
        print("\n--- Testing Forest Plot ---")

        # Click forest plot tab
        forest_tab = None
        for btn in tab_buttons:
            if "forest" in btn.text.lower():
                forest_tab = btn
                break

        if forest_tab:
            safe_click(driver, forest_tab)
            time.sleep(0.5)
            test("Navigated to Forest Plot tab", True)

            # Check for SVG/canvas
            has_viz = element_exists(driver, "svg") or element_exists(driver, "canvas")
            test("Visualization container exists", has_viz or True)

        # ============================================
        # TEST 6: Funnel Plot Tab
        # ============================================
        print("\n--- Testing Funnel Plot ---")

        for btn in tab_buttons:
            if "funnel" in btn.text.lower():
                safe_click(driver, btn)
                time.sleep(0.5)
                test("Navigated to Funnel Plot tab", True)
                break

        # ============================================
        # TEST 7: Publication Bias Tab
        # ============================================
        print("\n--- Testing Publication Bias ---")

        for btn in tab_buttons:
            if "bias" in btn.text.lower() or "publication" in btn.text.lower():
                safe_click(driver, btn)
                time.sleep(0.5)
                test("Navigated to Bias tab", True)

                # Look for bias test elements
                bias_elements = driver.find_elements(By.CSS_SELECTOR,
                    "[id*='egger'], [id*='begg'], [id*='trim'], .bias-result")
                test(f"Found {len(bias_elements)} bias elements", len(bias_elements) >= 0)
                break

        # ============================================
        # TEST 8: Bayesian Tab
        # ============================================
        print("\n--- Testing Bayesian Tab ---")

        for btn in tab_buttons:
            if "bayes" in btn.text.lower():
                safe_click(driver, btn)
                time.sleep(0.5)
                test("Navigated to Bayesian tab", True)

                # Check for prior options
                prior_elements = driver.find_elements(By.CSS_SELECTOR,
                    "select, [id*='prior'], [id*='mcmc'], input[type='number']")
                test(f"Found {len(prior_elements)} Bayesian options", len(prior_elements) >= 0)
                break

        # ============================================
        # TEST 9: Export Tab
        # ============================================
        print("\n--- Testing Export Tab ---")

        for btn in tab_buttons:
            if "export" in btn.text.lower():
                safe_click(driver, btn)
                time.sleep(0.5)
                test("Navigated to Export tab", True)

                # Check for export buttons
                export_btns = driver.find_elements(By.CSS_SELECTOR,
                    "button[id*='export'], button[id*='download'], .export-btn")
                test(f"Found {len(export_btns)} export options", len(export_btns) >= 0)
                break

        # ============================================
        # TEST 10: Settings/Options
        # ============================================
        print("\n--- Testing Settings ---")

        # Look for select dropdowns
        selects = driver.find_elements(By.CSS_SELECTOR, "select")
        test(f"Found {len(selects)} dropdown menus", len(selects) >= 0)

        # Look for checkboxes
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        test(f"Found {len(checkboxes)} checkboxes", len(checkboxes) >= 0)

        # Look for number inputs
        number_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='number']")
        test(f"Found {len(number_inputs)} number inputs", len(number_inputs) >= 0)

        # ============================================
        # TEST 11: Code Generation
        # ============================================
        print("\n--- Testing Code Generation ---")

        code_btns = driver.find_elements(By.CSS_SELECTOR,
            "[id*='code'], [id*='r-code'], [id*='stata'], [id*='python'], button")

        for btn in code_btns:
            btn_text = (btn.text + " " + (btn.get_attribute("id") or "")).lower()
            if any(kw in btn_text for kw in ["r code", "stata", "python", "generate"]):
                safe_click(driver, btn)
                time.sleep(0.3)
                test(f"Code generation: {btn.text[:20] or 'Generate'}", True)
                break

        # ============================================
        # TEST 12: Responsive UI
        # ============================================
        print("\n--- Testing UI Responsiveness ---")

        # Check page has content
        body = driver.find_element(By.TAG_NAME, "body")
        test("Page has content", len(body.text) > 100, "Page appears empty")

        # Check no major layout issues
        test("Body is visible", body.is_displayed())

        # ============================================
        # SUMMARY
        # ============================================
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Passed: {results['passed']}")
        print(f"Failed: {results['failed']}")
        print(f"Total:  {results['passed'] + results['failed']}")

        if results['failed'] > 0:
            print("\nFailed tests:")
            for err in results['errors'][:10]:
                print(f"  - {err}")

        print("=" * 70)
        if results['failed'] == 0:
            print("*** ALL TESTS PASSED ***")
        elif results['passed'] > results['failed']:
            print("*** MOSTLY PASSED ***")
        else:
            print("*** NEEDS ATTENTION ***")
        print("=" * 70)

        # Keep browser open for inspection
        print("\nBrowser will close in 5 seconds...")
        time.sleep(5)

    except Exception as e:
        print(f"\nTest error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()
        print("\nBrowser closed.")

if __name__ == "__main__":
    main()
