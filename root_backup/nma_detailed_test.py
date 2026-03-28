# Detailed Selenium test for NMA Pro v6.2

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.set_capability('ms:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Edge(options=options)

try:
    file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'
    driver.get(f'file:///{file_path}')
    time.sleep(3)

    # Get ALL console logs
    logs = driver.get_log('browser')

    print("=" * 70)
    print("ALL BROWSER CONSOLE LOGS:")
    print("=" * 70)
    for log in logs:
        level = log['level']
        msg = log['message'][:200]
        print(f"[{level}] {msg}")

    print("\n" + "=" * 70)
    print("PAGE CHECK:")
    print("=" * 70)
    print(f"Title: {driver.title}")

    # Check global objects
    checks = [
        ("window.FrequentistNMA !== undefined", "FrequentistNMA exists"),
        ("window.BayesianNMA !== undefined", "BayesianNMA exists"),
        ("window.AppState !== undefined", "AppState exists"),
        ("window.Matrix !== undefined", "Matrix exists"),
        ("window.jStat !== undefined", "jStat exists"),
        ("typeof FrequentistNMA === 'object'", "FrequentistNMA is object"),
        ("typeof FrequentistNMA.analyze === 'function'", "analyze() exists"),
    ]

    for js_check, desc in checks:
        try:
            result = driver.execute_script(f"return {js_check}")
            status = "[OK]" if result else "[FAIL]"
            print(f"{status} {desc}")
        except Exception as e:
            print(f"[ERROR] {desc}: {str(e)[:50]}")

    # Try to get list of FrequentistNMA methods
    try:
        methods = driver.execute_script("return Object.keys(FrequentistNMA)")
        print(f"\nFrequentistNMA methods: {methods[:10]}...")
    except Exception as e:
        print(f"\n[ERROR] Getting methods: {str(e)[:100]}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

except Exception as e:
    print(f"[FATAL ERROR] {e}")

finally:
    driver.quit()
