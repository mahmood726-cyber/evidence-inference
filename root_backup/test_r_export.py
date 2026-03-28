#!/usr/bin/env python3
"""Test R code export"""

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

# Load sample data and generate R code
result = driver.execute_script("""
    // Load BCG sample data
    if (typeof SAMPLES !== 'undefined' && SAMPLES.bcg) {
        AppState.studies = SAMPLES.bcg.studies;
        AppState.dataType = 'binary';
        AppState.settings = AppState.settings || {};
        AppState.settings.tau2Method = 'REML';
        AppState.settings.effectMeasure = 'RR';

        // Create results object
        AppState.results = {
            studies: AppState.studies.map(function(s, i) {
                return {
                    name: s.study || s.name || ('Study ' + (i+1)),
                    yi: s.yi,
                    vi: s.vi
                };
            })
        };
    }

    // Generate R code
    if (typeof generateMetaforCode === 'function') {
        var code = generateMetaforCode();
        return {success: true, code: code};
    }
    return {success: false, error: 'generateMetaforCode not found'};
""")

print('=== Current R Code Export ===')
if result.get('success') and result.get('code'):
    code = result['code']
    # Clean up excessive newlines
    code = re.sub(r'\n{3,}', '\n\n', code)
    print(f'Length: {len(code)} characters\n')
    print(code)
else:
    print('Failed:', result.get('error', 'Unknown error'))

driver.quit()
