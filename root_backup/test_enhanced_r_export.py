#!/usr/bin/env python3
"""Test enhanced R code export"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import re

driver_path = r"C:\Users\user\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32\chromedriver.exe"
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
time.sleep(3)

# Load sample data properly and generate R code
result = driver.execute_script("""
    // Load BCG sample data
    if (typeof SAMPLES !== 'undefined' && SAMPLES.bcg) {
        AppState.studies = SAMPLES.bcg.studies;
        AppState.dataType = 'binary';
        AppState.settings = AppState.settings || {};
        AppState.settings.tau2Method = 'REML';
    }

    // Generate R code
    if (typeof generateMetaforCode === 'function') {
        try {
            var code = generateMetaforCode();
            return {success: true, code: code, length: code ? code.length : 0};
        } catch(e) {
            return {success: false, error: e.message};
        }
    }
    return {success: false, error: 'generateMetaforCode not found'};
""")

print('=== Enhanced R Code Export Test ===')
if result.get('success') and result.get('code'):
    code = result['code']
    # Clean up excessive newlines
    code = re.sub(r'\n{3,}', '\n\n', code)
    print(f'Generated {len(code)} characters of R code\n')

    # Save to file
    with open('C:/Users/user/generated_metafor_code.R', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Saved to: C:/Users/user/generated_metafor_code.R\n')

    # Show the code
    print('=' * 70)
    print(code)
    print('=' * 70)

    # Count sections
    sections = code.count('# ===')
    print(f'\nCode contains {sections} major sections')
else:
    print(f'Failed: {result.get("error", "Unknown error")}')

driver.quit()
