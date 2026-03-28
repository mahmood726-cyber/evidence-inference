"""Quick JS error check"""
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

# Check for JS errors
logs = driver.get_log('browser')
errors = [l for l in logs if l['level'] == 'SEVERE']
print(f'Found {len(errors)} errors:')
for e in errors[:10]:
    print(f'  {e["message"]}')

# Check what's defined
checks = [
    'DEMO_DATASETS',
    'loadDemoDataset',
    'runAnalysis',
    'AppState',
    'FrequentistNMA',
    'TrimAndFill',
    'EggersTest'
]

print('\nModule checks:')
for check in checks:
    exists = driver.execute_script(f"return typeof {check}")
    print(f'  {check}: {exists}')

driver.quit()
