"""Check for JS errors in bundle"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--no-sandbox')
# Enable console log capture
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)

try:
    print("Loading bundle...")
    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-bundle.html')
    time.sleep(3)

    # Get browser console logs
    logs = driver.get_log('browser')
    print(f"\nBrowser console logs ({len(logs)} entries):")
    for log in logs:
        level = log.get('level', 'UNKNOWN')
        message = log.get('message', '')
        print(f"[{level}] {message[:200]}")

finally:
    driver.quit()
