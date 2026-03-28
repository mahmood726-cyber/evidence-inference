"""
Test Demo Data Loading in PrognosisMeta
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=" * 70)
    print("TESTING DEMO DATA FUNCTIONALITY")
    print("=" * 70)

    options = Options()
    options.add_argument("--start-maximized")
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load app
        print("\n[1] Loading application...")
        driver.get("file:///C:/Users/user/prognostic-meta/index.html")
        time.sleep(2)
        print("    Page loaded")

        # Find and click demo button
        print("\n[2] Looking for Demo Data button...")
        demo_btn = driver.find_element(By.ID, "btn-load-demo")
        print(f"    Found button: {demo_btn.text}")

        # Click the demo button
        driver.execute_script("arguments[0].click();", demo_btn)
        time.sleep(0.5)

        # Handle the prompt - enter "1" for prognostic_hr
        print("\n[3] Handling prompt dialog...")
        try:
            alert = Alert(driver)
            print(f"    Prompt text: {alert.text[:100]}...")
            alert.send_keys("1")
            alert.accept()
            print("    Selected option 1 (prognostic_hr)")
        except Exception as e:
            print(f"    No prompt or error: {e}")

        time.sleep(1)

        # Check if data was loaded
        print("\n[4] Checking if data was loaded...")
        table_rows = driver.find_elements(By.CSS_SELECTOR, "#data-table tbody tr")
        print(f"    Found {len(table_rows)} data rows")

        # Check for study names in table
        if table_rows:
            first_row = table_rows[0].text
            print(f"    First row: {first_row[:80]}...")

        # Go to Analysis tab
        print("\n[5] Navigating to Analysis tab...")
        analysis_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='analysis']")
        driver.execute_script("arguments[0].click();", analysis_tab)
        time.sleep(0.5)

        # Click Run Analysis
        print("\n[6] Running analysis...")
        run_btn = driver.find_element(By.ID, "btn-run-analysis")
        driver.execute_script("arguments[0].click();", run_btn)
        time.sleep(2)

        # Check for results
        print("\n[7] Checking Results tab...")
        results_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='results']")
        driver.execute_script("arguments[0].click();", results_tab)
        time.sleep(0.5)

        # Look for result content
        result_elements = driver.find_elements(By.CSS_SELECTOR, ".result-value, .effect-value, #pooled-effect")
        print(f"    Found {len(result_elements)} result elements")

        for el in result_elements[:5]:
            if el.text.strip():
                print(f"    Result: {el.text}")

        # Check Visualization tab
        print("\n[8] Checking Visualization tab...")
        viz_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='visualization']")
        driver.execute_script("arguments[0].click();", viz_tab)
        time.sleep(1)

        svg_elements = driver.find_elements(By.CSS_SELECTOR, "svg")
        print(f"    Found {len(svg_elements)} SVG elements")

        # Check for JS errors
        print("\n[9] Checking for JavaScript errors...")
        logs = driver.get_log("browser")
        errors = [l for l in logs if l.get("level") == "SEVERE"]
        if errors:
            print(f"    Found {len(errors)} errors:")
            for err in errors[:5]:
                print(f"      - {err.get('message', '')[:100]}")
        else:
            print("    No JavaScript errors!")

        # Check Publication Bias tab
        print("\n[10] Checking Publication Bias tab...")
        bias_tab = driver.find_element(By.CSS_SELECTOR, "[data-tab='bias']")
        driver.execute_script("arguments[0].click();", bias_tab)
        time.sleep(0.5)

        # Try running bias tests
        try:
            run_bias_btn = driver.find_element(By.ID, "btn-run-bias")
            driver.execute_script("arguments[0].click();", run_bias_btn)
            time.sleep(1)
            print("    Ran bias tests")
        except:
            print("    Could not find bias test button")

        # Final summary
        print("\n" + "=" * 70)
        print("TEST COMPLETE")
        print("=" * 70)

        # Check final state
        final_logs = driver.get_log("browser")
        final_errors = [l for l in final_logs if l.get("level") == "SEVERE"]
        if final_errors:
            print(f"\nWARNING: {len(final_errors)} JavaScript errors detected")
            for err in final_errors[:10]:
                print(f"  - {err.get('message', '')[:120]}")
        else:
            print("\nSUCCESS: All tests passed, no JavaScript errors!")

        print("\nBrowser staying open for 20 seconds...")
        time.sleep(20)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)

    finally:
        driver.quit()
        print("\nBrowser closed.")

if __name__ == "__main__":
    main()
