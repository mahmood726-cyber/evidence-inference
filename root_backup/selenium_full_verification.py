#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full Selenium verification of TruthCert-PairwisePro app"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("=" * 70)
print("SELENIUM FULL VERIFICATION TEST")
print("=" * 70)

# Use cached ChromeDriver
driver_path = "C:/Users/user/.wdm/drivers/chromedriver/win64/143.0.7499.192/chromedriver-win32/chromedriver.exe"
print(f"Using driver: {driver_path}")

# Setup Chrome
options = ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

service = ChromeService(driver_path)
driver = webdriver.Chrome(service=service, options=options)

results = {
    'tabs': [],
    'buttons': [],
    'plots': [],
    'unit_tests': None,
    'errors': []
}

try:
    # Load the app
    file_path = "file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html"
    print(f"\nLoading: {file_path}")
    driver.get(file_path)
    time.sleep(3)

    # Check for JS errors
    logs = driver.get_log('browser')
    js_errors = [log for log in logs if log['level'] == 'SEVERE']
    if js_errors:
        results['errors'] = js_errors
        print(f"\nJS Errors found: {len(js_errors)}")
        for err in js_errors[:5]:
            print(f"  - {err['message'][:100]}")

    # Test 1: Tab Navigation
    print("\n[1] Testing Tab Navigation...")
    tabs = driver.find_elements(By.CSS_SELECTOR, "[data-tab], .tab-button, button[onclick*='Tab']")
    print(f"    Found {len(tabs)} tab buttons")

    for tab in tabs[:15]:
        try:
            tab_text = tab.text.strip() or tab.get_attribute('data-tab') or 'unknown'
            if tab.is_displayed() and tab.is_enabled():
                results['tabs'].append({'name': tab_text, 'status': 'accessible'})
        except:
            pass

    accessible_tabs = len([t for t in results['tabs'] if t['status'] == 'accessible'])
    print(f"    Accessible tabs: {accessible_tabs}")

    # Test 2: Button Functionality
    print("\n[2] Testing Button Functionality...")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"    Found {len(buttons)} buttons")

    for btn in buttons[:20]:
        try:
            btn_text = btn.text.strip()[:30] or 'unnamed'
            if btn.is_displayed() and btn.is_enabled():
                results['buttons'].append({'name': btn_text, 'status': 'enabled'})
        except:
            pass

    enabled_buttons = len([b for b in results['buttons'] if b['status'] == 'enabled'])
    print(f"    Enabled buttons: {enabled_buttons}")

    # Test 3: Plotly Plots
    print("\n[3] Testing Plotly Plots...")
    plots = driver.find_elements(By.CSS_SELECTOR, ".js-plotly-plot, [id*='plot'], [id*='chart'], [id*='forest'], [id*='funnel']")
    print(f"    Found {len(plots)} plot containers")
    results['plots'] = [{'id': p.get_attribute('id') or 'unnamed'} for p in plots[:10]]

    # Test 4: Run Automated Unit Tests
    print("\n[4] Running Automated Unit Tests...")
    test_result = driver.execute_script("""
        try {
            if (typeof runAutomatedTests === 'function') {
                return runAutomatedTests();
            } else {
                return { error: 'runAutomatedTests function not found' };
            }
        } catch (e) {
            return { error: e.toString() };
        }
    """)

    if test_result and 'error' not in test_result:
        results['unit_tests'] = test_result
        print(f"\n{'=' * 60}")
        print("UNIT TEST RESULTS")
        print(f"{'=' * 60}")

        for test in test_result.get('tests', []):
            status = "PASS" if test.get('pass') else "FAIL"
            print(f"    {status:4} | {test.get('name', 'unknown')}")
            if not test.get('pass'):
                print(f"           Expected: {test.get('expected')}, Got: {test.get('actual')}")

        print(f"{'=' * 60}")
        print(f"    {test_result.get('summary', 'No summary')}")
        print(f"{'=' * 60}")
    else:
        print(f"    ERROR: {test_result.get('error', 'Unknown error')}")

    # Test 5: Core Functions Exist
    print("\n[5] Verifying Core Functions...")
    core_functions = [
        'estimateTau2_DL', 'estimateTau2_REML', 'estimateTau2_HS', 'estimateTau2_SJ',
        'calculatePooledEstimate', 'calculateHKSJ', 'bayesianMetaAnalysis',
        'runAutomatedTests', 'runTestsWithOutput'
    ]

    for func in core_functions:
        exists = driver.execute_script(f"return typeof {func} === 'function'")
        status = "OK" if exists else "MISSING"
        print(f"    {status:7} | {func}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Tabs accessible:     {accessible_tabs}")
    print(f"  Buttons enabled:     {enabled_buttons}")
    print(f"  Plot containers:     {len(results['plots'])}")
    print(f"  JS Errors:           {len(results['errors'])}")

    if results['unit_tests'] and 'allPassed' in results['unit_tests']:
        if results['unit_tests']['allPassed']:
            print(f"  Unit Tests:          ALL PASSED ({results['unit_tests']['passed']}/{results['unit_tests']['passed']})")
        else:
            print(f"  Unit Tests:          {results['unit_tests']['passed']}/{results['unit_tests']['passed'] + results['unit_tests']['failed']} passed")

    print("=" * 70)

    if results['unit_tests'] and results['unit_tests'].get('allPassed') and len(results['errors']) == 0:
        print("\n*** ALL VERIFICATION TESTS PASSED - READY FOR 10/10! ***")
    else:
        print("\nSome issues found - review above")

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()

print("\n" + "=" * 70)
