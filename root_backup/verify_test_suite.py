#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify the automated test suite works via Selenium"""

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

print("=" * 70)
print("VERIFYING AUTOMATED TEST SUITE VIA SELENIUM")
print("=" * 70)

# Setup Edge
options = EdgeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = EdgeService(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

try:
    # Load the app
    file_path = "file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html"
    print(f"\nLoading: {file_path}")
    driver.get(file_path)
    time.sleep(3)

    # Run the automated tests
    print("\nRunning automated tests...")
    result = driver.execute_script("""
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

    if 'error' in result:
        print(f"\nERROR: {result['error']}")
    else:
        print(f"\n{'=' * 60}")
        print("TEST RESULTS")
        print(f"{'=' * 60}")

        for test in result['tests']:
            status = "PASS" if test['pass'] else "FAIL"
            print(f"{status:4} | {test['name']}")
            if not test['pass']:
                print(f"       Expected: {test['expected']}, Got: {test['actual']}")

        print(f"{'=' * 60}")
        print(f"SUMMARY: {result['summary']}")
        print(f"{'=' * 60}")

        if result['allPassed']:
            print("\n✓ ALL TESTS PASSED - Ready for 10/10!")
        else:
            print(f"\n✗ {result['failed']} tests failed")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()

print("\n" + "=" * 70)
