"""Run Unit Tests for TruthCert-PairwisePro"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)

try:
    print("=" * 70)
    print("UNIT TESTS - TruthCert-PairwisePro v1.0")
    print("=" * 70)

    # Load app (test bundle version)
    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-bundle.html')
    time.sleep(3)

    # Read and inject unit test file
    with open(r'C:\Truthcert1\unit_tests.js', 'r', encoding='utf-8') as f:
        unit_test_code = f.read()

    driver.execute_script(unit_test_code)
    time.sleep(1)

    # Run unit tests
    result = driver.execute_script("""
        try {
            const result = UnitTests.runAll();
            return {
                success: true,
                passed: result.passed,
                failed: result.failed,
                total: result.total,
                results: UnitTests.results
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if result['success']:
        print(f"\nTotal Tests: {result['total']}")
        print(f"Passed: {result['passed']}")
        print(f"Failed: {result['failed']}")
        print(f"Success Rate: {(result['passed']/result['total']*100):.1f}%")

        if result['failed'] > 0:
            print("\nFailed Tests:")
            for r in result['results']:
                if r['status'] == 'FAIL':
                    print(f"  - {r['name']}: expected {r['expected']}, got {r['actual']}")

        if result['failed'] == 0:
            print("\n[OK] ALL UNIT TESTS PASSED!")
        else:
            print(f"\n[WARN] {result['failed']} test(s) failed")
    else:
        print(f"[ERROR] Unit tests failed to run: {result.get('error', 'Unknown')}")

    print("=" * 70)

finally:
    driver.quit()
