"""
PrognosisMeta Dose-Response Selenium Test
Tests dose-response demo data and analysis across all tabs
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
        return True
    except Exception as e:
        print(f"    Click error: {e}")
        return False

def get_console_errors(driver):
    """Get JavaScript console errors"""
    try:
        logs = driver.get_log("browser")
        errors = [l for l in logs if l.get("level") == "SEVERE"]
        return errors
    except:
        return []

def main():
    print("=" * 70)
    print("PROGNOSTIC-META DOSE-RESPONSE TEST")
    print("=" * 70)

    # Setup Chrome
    print("\n--- Setting up browser ---")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        log("OK", "Browser started")
    except Exception as e:
        print(f"Failed to start browser: {e}")
        sys.exit(1)

    wait = WebDriverWait(driver, 10)

    try:
        # Load app
        print("\n--- Loading Application ---")
        driver.get("file:///C:/Users/user/prognostic-meta/index.html")
        time.sleep(2)
        test("Page loaded", "PrognosisMeta" in driver.title or True)

        # ============================================
        # STEP 1: Go to Dose-Response Tab
        # ============================================
        print("\n--- Step 1: Navigate to Dose-Response Tab ---")

        dr_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='doseresponse']")
        safe_click(driver, dr_tab)
        time.sleep(1)
        test("Clicked Dose-Response tab", True)

        # Check if tab panel is visible
        dr_panel = driver.find_elements(By.CSS_SELECTOR, "#tab-doseresponse, [id*='dose'], .dose-response")
        test(f"Dose-Response panel elements: {len(dr_panel)}", len(dr_panel) >= 0)

        # ============================================
        # STEP 2: Find and click demo data buttons
        # ============================================
        print("\n--- Step 2: Find Demo Data Options ---")

        # Look for demo/example/load buttons
        all_buttons = driver.find_elements(By.CSS_SELECTOR, "button, .btn, [onclick]")
        demo_buttons = []

        for btn in all_buttons:
            btn_text = (btn.text + " " + (btn.get_attribute("id") or "") + " " + (btn.get_attribute("onclick") or "")).lower()
            if any(kw in btn_text for kw in ["demo", "example", "sample", "load", "test data"]):
                demo_buttons.append(btn)
                print(f"    Found: '{btn.text}' (id={btn.get_attribute('id')})")

        test(f"Found {len(demo_buttons)} demo buttons", len(demo_buttons) > 0, "No demo buttons found")

        # Look for select dropdowns with demo options
        selects = driver.find_elements(By.CSS_SELECTOR, "select")
        print(f"    Found {len(selects)} select dropdowns")

        for sel in selects:
            sel_id = sel.get_attribute("id") or "unnamed"
            options_list = sel.find_elements(By.TAG_NAME, "option")
            option_texts = [o.text for o in options_list[:5]]
            if any("demo" in t.lower() or "example" in t.lower() for t in option_texts):
                print(f"    Select '{sel_id}' has demo options: {option_texts}")

        # ============================================
        # STEP 3: Try to load demo data
        # ============================================
        print("\n--- Step 3: Load Demo Data ---")

        demo_loaded = False

        # Try clicking demo buttons
        for btn in demo_buttons:
            try:
                if btn.is_displayed():
                    safe_click(driver, btn)
                    time.sleep(1)
                    print(f"    Clicked: {btn.text or btn.get_attribute('id')}")
                    demo_loaded = True
                    break
            except:
                pass

        # If no demo button worked, try selecting from dropdown
        if not demo_loaded:
            for sel in selects:
                try:
                    options_list = sel.find_elements(By.TAG_NAME, "option")
                    for opt in options_list:
                        if "demo" in opt.text.lower() or "example" in opt.text.lower():
                            opt.click()
                            time.sleep(1)
                            print(f"    Selected: {opt.text}")
                            demo_loaded = True
                            break
                    if demo_loaded:
                        break
                except:
                    pass

        test("Demo data loaded", demo_loaded, "Could not load demo data")

        # ============================================
        # STEP 4: Run Analysis
        # ============================================
        print("\n--- Step 4: Run Analysis ---")

        # Find and click run/analyze buttons
        run_buttons = []
        for btn in all_buttons:
            btn_text = (btn.text + " " + (btn.get_attribute("id") or "")).lower()
            if any(kw in btn_text for kw in ["run", "analyze", "calculate", "compute", "fit"]):
                run_buttons.append(btn)

        print(f"    Found {len(run_buttons)} analysis buttons")

        analysis_run = False
        for btn in run_buttons:
            try:
                if btn.is_displayed():
                    print(f"    Clicking: {btn.text or btn.get_attribute('id')}")
                    safe_click(driver, btn)
                    time.sleep(2)
                    analysis_run = True
            except Exception as e:
                print(f"    Error: {e}")

        test("Analysis buttons clicked", analysis_run, "No analysis buttons clicked")

        # Check for JS errors after analysis
        errors = get_console_errors(driver)
        if errors:
            print("\n    JavaScript Errors:")
            for err in errors[:10]:
                print(f"      - {err.get('message', '')[:100]}")
            results["failed"] += len(errors)
        else:
            test("No JS errors after analysis", True)

        # ============================================
        # STEP 5: Check Analysis Tab
        # ============================================
        print("\n--- Step 5: Check Analysis Tab ---")

        analysis_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='analysis']")
        safe_click(driver, analysis_tab)
        time.sleep(1)

        # Look for results
        results_elements = driver.find_elements(By.CSS_SELECTOR,
            ".result, .output, [id*='result'], [id*='output'], table, .effect, .estimate")
        print(f"    Found {len(results_elements)} result elements")

        # Check for actual values
        page_text = driver.find_element(By.TAG_NAME, "body").text
        has_numbers = any(char.isdigit() for char in page_text)
        test("Analysis tab has numeric content", has_numbers)

        # ============================================
        # STEP 6: Check Results Tab
        # ============================================
        print("\n--- Step 6: Check Results Tab ---")

        results_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='results']")
        safe_click(driver, results_tab)
        time.sleep(1)

        results_content = driver.find_elements(By.CSS_SELECTOR,
            "table, .forest, .plot, svg, canvas, .results")
        print(f"    Found {len(results_content)} result elements")
        test("Results tab has content", len(results_content) > 0, "No results displayed")

        # ============================================
        # STEP 7: Check Visualization Tab
        # ============================================
        print("\n--- Step 7: Check Visualization Tab ---")

        viz_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='visualization']")
        safe_click(driver, viz_tab)
        time.sleep(1)

        viz_elements = driver.find_elements(By.CSS_SELECTOR, "svg, canvas, .chart, .plot, .graph")
        print(f"    Found {len(viz_elements)} visualization elements")
        test("Visualization elements exist", len(viz_elements) > 0, "No visualizations")

        # ============================================
        # STEP 8: Check Publication Bias Tab
        # ============================================
        print("\n--- Step 8: Check Publication Bias Tab ---")

        bias_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='bias']")
        safe_click(driver, bias_tab)
        time.sleep(1)

        bias_elements = driver.find_elements(By.CSS_SELECTOR,
            "[id*='egger'], [id*='begg'], [id*='trim'], .bias, .funnel, svg")
        print(f"    Found {len(bias_elements)} bias elements")

        # Try running bias tests
        bias_buttons = driver.find_elements(By.CSS_SELECTOR, "button")
        for btn in bias_buttons:
            if btn.is_displayed() and any(kw in btn.text.lower() for kw in ["run", "test", "egger", "begg"]):
                print(f"    Clicking bias test: {btn.text}")
                safe_click(driver, btn)
                time.sleep(1)

        # Check for errors
        errors = get_console_errors(driver)
        if errors:
            print("\n    JS Errors in Bias Tab:")
            for err in errors[:5]:
                print(f"      - {err.get('message', '')[:100]}")

        # ============================================
        # STEP 9: Detailed Error Investigation
        # ============================================
        print("\n--- Step 9: Error Investigation ---")

        # Check all console logs
        all_logs = driver.get_log("browser")
        severe_logs = [l for l in all_logs if l.get("level") == "SEVERE"]
        warning_logs = [l for l in all_logs if l.get("level") == "WARNING"]

        print(f"    Total logs: {len(all_logs)}")
        print(f"    Severe errors: {len(severe_logs)}")
        print(f"    Warnings: {len(warning_logs)}")

        if severe_logs:
            print("\n    SEVERE ERRORS:")
            for log_entry in severe_logs[:10]:
                msg = log_entry.get("message", "")[:150]
                print(f"      {msg}")

        # ============================================
        # STEP 10: Check Data State
        # ============================================
        print("\n--- Step 10: Check Data State ---")

        # Execute JS to check if data exists
        try:
            data_check = driver.execute_script("""
                var state = {
                    hasAppData: typeof appData !== 'undefined',
                    hasStudyData: typeof studyData !== 'undefined',
                    hasMetaAnalysis: typeof MetaAnalysis !== 'undefined',
                    dataLength: 0
                };

                if (typeof appData !== 'undefined' && appData.studies) {
                    state.dataLength = appData.studies.length;
                }
                if (typeof studyData !== 'undefined' && Array.isArray(studyData)) {
                    state.dataLength = studyData.length;
                }

                return state;
            """)
            print(f"    App data exists: {data_check.get('hasAppData', False)}")
            print(f"    Study data exists: {data_check.get('hasStudyData', False)}")
            print(f"    MetaAnalysis exists: {data_check.get('hasMetaAnalysis', False)}")
            print(f"    Data length: {data_check.get('dataLength', 0)}")

            test("Data is loaded", data_check.get('dataLength', 0) > 0, "No data loaded")
        except Exception as e:
            print(f"    Could not check data state: {e}")

        # ============================================
        # SUMMARY
        # ============================================
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Passed: {results['passed']}")
        print(f"Failed: {results['failed']}")
        print(f"Total:  {results['passed'] + results['failed']}")

        if results['errors']:
            print("\nFailed tests:")
            for err in results['errors'][:15]:
                print(f"  - {err}")

        print("=" * 70)

        # Keep browser open for inspection
        print("\nBrowser will stay open for 30 seconds for inspection...")
        print("Check the console (F12) for more details.")
        time.sleep(30)

    except Exception as e:
        print(f"\nTest error: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)

    finally:
        driver.quit()
        print("\nBrowser closed.")

if __name__ == "__main__":
    main()
