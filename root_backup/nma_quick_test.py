# Quick Selenium test to verify NMA Pro v6.2 loads without errors

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Edge(options=options)

try:
    file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'
    driver.get(f'file:///{file_path}')

    # Wait for page to load
    time.sleep(2)

    # Check for JavaScript errors in console
    logs = driver.get_log('browser')
    js_errors = [log for log in logs if log['level'] == 'SEVERE']

    if js_errors:
        print("=" * 60)
        print("JAVASCRIPT ERRORS FOUND:")
        print("=" * 60)
        for err in js_errors:
            print(f"  {err['message'][:100]}")
        print("=" * 60)
    else:
        print("[OK] No JavaScript errors detected")

    # Check if main elements exist
    try:
        title = driver.title
        print(f"[OK] Page title: {title}")
    except:
        print("[ERROR] Could not get page title")

    # Try to find the analyze button
    try:
        analyze_btn = driver.find_element(By.ID, 'analyzeBtn')
        print("[OK] Analyze button found")
    except:
        print("[ERROR] Analyze button not found")

    # Try to find the Bayesian export button
    try:
        bayes_btn = driver.find_element(By.ID, 'exportBayesRBtn')
        print("[OK] Bayesian R export button found")
    except:
        print("[INFO] Bayesian R export button not found (may appear after analysis)")

    # Check if FrequentistNMA is defined
    result = driver.execute_script("return typeof FrequentistNMA !== 'undefined'")
    if result:
        print("[OK] FrequentistNMA class is defined")
    else:
        print("[ERROR] FrequentistNMA class is NOT defined")

    # Check if pauleMandel_CI exists
    result = driver.execute_script("return typeof FrequentistNMA.pauleMandel_CI === 'function'")
    if result:
        print("[OK] pauleMandel_CI function exists")
    else:
        print("[INFO] pauleMandel_CI function not directly accessible")

    print("\n" + "=" * 60)
    print("NMA Pro v6.2 - QUICK TEST COMPLETE")
    print("=" * 60)

except Exception as e:
    print(f"[ERROR] {e}")

finally:
    driver.quit()
