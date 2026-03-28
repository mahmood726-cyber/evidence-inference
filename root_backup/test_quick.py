"""Quick test to compare original vs bundle"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)

try:
    print("=" * 60)
    print("Testing ORIGINAL (fast.html)")
    print("=" * 60)

    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
    time.sleep(3)

    # Check if function exists
    has_func = driver.execute_script("return typeof loadDemoDataset === 'function'")
    print(f"loadDemoDataset exists: {has_func}")

    if has_func:
        driver.execute_script("loadDemoDataset('BCG')")
        time.sleep(1)
        driver.execute_script("runAnalysis()")
        time.sleep(2)
        has_results = driver.execute_script("return AppState.results && AppState.results.pooled")
        print(f"Results generated: {has_results}")

    print("\n" + "=" * 60)
    print("Testing BUNDLE (bundle.html)")
    print("=" * 60)

    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-bundle.html')
    time.sleep(3)

    # Check if function exists
    has_func = driver.execute_script("return typeof loadDemoDataset === 'function'")
    print(f"loadDemoDataset exists: {has_func}")

    # Check for JS errors
    errors = driver.execute_script("""
        var errors = [];
        window.onerror = function(msg) { errors.push(msg); };
        return errors;
    """)
    print(f"JS Errors: {errors}")

    # Try to see what's available globally
    funcs = driver.execute_script("""
        var available = [];
        if (typeof runAnalysis !== 'undefined') available.push('runAnalysis');
        if (typeof loadDemoDataset !== 'undefined') available.push('loadDemoDataset');
        if (typeof AppState !== 'undefined') available.push('AppState');
        if (typeof saveProject !== 'undefined') available.push('saveProject');
        return available;
    """)
    print(f"Available globals: {funcs}")

finally:
    driver.quit()
