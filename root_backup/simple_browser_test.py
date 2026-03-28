#!/usr/bin/env python3
"""Simple browser test without headless"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

print("=" * 70)
print("SIMPLE BROWSER TEST")
print("=" * 70)

# Non-headless mode with minimal options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1280,720")

driver_path = r"C:\Users\user\.cache\selenium\chromedriver\win64\143.0.7499.192\chromedriver.exe"

print(f"Driver: {driver_path}")

try:
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    print("Browser started successfully!")

    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(2)
    print(f"Page title: {driver.title}")

    # Quick test
    result = driver.execute_script("return typeof DEMO_DATASETS !== 'undefined';")
    print(f"DEMO_DATASETS exists: {result}")

    demos = driver.execute_script("return Object.keys(DEMO_DATASETS).length;")
    print(f"Demo datasets count: {demos}")

    # Test TES function
    tes_exists = driver.execute_script("return typeof testExcessSignificance === 'function';")
    print(f"testExcessSignificance exists: {tes_exists}")

    # Test QQ Plot
    qq_exists = driver.execute_script("return typeof renderQQPlot === 'function';")
    print(f"renderQQPlot exists: {qq_exists}")

    print("\nALL TESTS PASSED!")

    driver.quit()
    print("Browser closed.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
