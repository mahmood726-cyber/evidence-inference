"""Test restored version"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(3)

try:
    # Check if loadDemo works
    driver.execute_script('loadDemo()')
    time.sleep(0.5)
    studies = driver.execute_script('return AppState.studies?.length || 0')
    print(f'Studies loaded: {studies}')

    # Check if can run analysis
    driver.execute_script("document.getElementById('runAnalysisBtn').click()")
    time.sleep(3)
    results = driver.execute_script('return AppState.results !== null')
    print(f'Analysis works: {results}')

    # Check modules
    modules = ['ThresholdAnalysis', 'CINeMA', 'FrequentistNMA', 'InfluenceDiagnostics', 'ROBSensitivity']
    for mod in modules:
        exists = driver.execute_script(f'return typeof {mod} !== "undefined"')
        status = 'OK' if exists else 'MISSING'
        print(f'{mod}: {status}')

except Exception as e:
    print(f'Error: {e}')

driver.quit()
