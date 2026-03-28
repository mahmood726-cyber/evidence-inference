#!/usr/bin/env python3
"""Quick Selenium test to verify 14 tests pass"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

print("=" * 70)
print("VERIFYING 14-TEST SUITE")
print("=" * 70)

# Use cached ChromeDriver
driver_path = r"C:\Users\user\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32\chromedriver.exe"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

try:
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Load the app
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)

    # Run automated tests
    print("\nRunning automated tests...")
    result = driver.execute_script("return runAutomatedTests();")

    passed = result.get('passed', 0)
    failed = result.get('failed', 0)
    total = passed + failed

    print(f"\nResults: {passed}/{total} tests passed")

    if failed > 0:
        print("\nFailed tests:")
        for test in result.get('tests', []):
            if not test.get('passed'):
                print(f"  - {test.get('name')}: expected {test.get('expected')}, got {test.get('actual')}")

    # Check for JS errors
    logs = driver.get_log('browser')
    errors = [log for log in logs if log['level'] == 'SEVERE']
    if errors:
        print(f"\nJS Errors: {len(errors)}")
        for e in errors[:3]:
            print(f"  {e['message'][:100]}")
    else:
        print("\nNo JS errors")

    driver.quit()

    print("\n" + "=" * 70)
    if passed == total and total >= 14:
        print(f"SUCCESS: All {total} tests passed!")
    else:
        print(f"WARNING: {failed} tests failed")
    print("=" * 70)

except Exception as e:
    print(f"Error: {e}")
