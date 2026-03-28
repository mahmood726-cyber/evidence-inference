"""Test all editorial improvements"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(3)

print('='*70)
print('TESTING ALL EDITORIAL IMPROVEMENTS')
print('='*70)

passed = 0
failed = 0

def test(name, condition):
    global passed, failed
    if condition:
        print(f'[PASS] {name}')
        passed += 1
    else:
        print(f'[FAIL] {name}')
        failed += 1

# Load demo dataset
print('\n[1] DEMO DATASETS')
demo_exists = driver.execute_script('return typeof DEMO_DATASETS !== "undefined"')
test('DEMO_DATASETS object exists', demo_exists)

dropdown = driver.execute_script('return document.getElementById("demoDatasetSelect") !== null')
test('Demo dataset dropdown exists', dropdown)

# Load thrombolytics
driver.execute_script("loadDemoDataset('thrombolytics')")
time.sleep(0.5)
studies = driver.execute_script('return AppState.studies?.length || 0')
test('Thrombolytics loaded (12 studies)', studies == 12)

# Run analysis
driver.execute_script("document.getElementById('runAnalysisBtn').click()")
time.sleep(3)
results = driver.execute_script('return AppState.results !== null')
test('Analysis produces results', results)

print('\n[2] INFLUENCE DIAGNOSTICS')
infl = driver.execute_script('return typeof InfluenceDiagnostics !== "undefined"')
test('InfluenceDiagnostics module exists', infl)

infl_calc = driver.execute_script('return InfluenceDiagnostics.calculate(AppState.results)')
test('InfluenceDiagnostics.calculate() works', infl_calc is not None)
if infl_calc:
    test('Returns Cook\'s D values', all('cooksD' in r for r in infl_calc))
    test('Returns DFBETAS values', all('dfbetas' in r for r in infl_calc))
    test('Returns influence level', all('influence' in r for r in infl_calc))

print('\n[3] ROB SENSITIVITY')
rob = driver.execute_script('return typeof ROBSensitivity !== "undefined"')
test('ROBSensitivity module exists', rob)

rob_result = driver.execute_script('return ROBSensitivity.analyze(AppState.studies, AppState.effectMeasure)')
test('ROBSensitivity.analyze() works', rob_result is not None)
if rob_result:
    test('Has full analysis', rob_result.get('full') is not None)
    test('Has ROB counts', rob_result.get('robCounts') is not None)

print('\n[4] PRISMA-NMA CHECKLIST')
prisma = driver.execute_script('return typeof PRISMANMAChecklist !== "undefined"')
test('PRISMANMAChecklist module exists', prisma)

prisma_items = driver.execute_script('return PRISMANMAChecklist.items?.length')
test('PRISMA checklist has items', prisma_items and prisma_items > 0)

prisma_html = driver.execute_script('return PRISMANMAChecklist.generateHTML(AppState.results, AppState)')
test('generateHTML() produces output', prisma_html and len(prisma_html) > 100)

print('\n[5] NETWORK WARNINGS')
warn = driver.execute_script('return typeof NetworkWarnings !== "undefined"')
test('NetworkWarnings module exists', warn)

warnings = driver.execute_script('return NetworkWarnings.assess(AppState.studies)')
test('NetworkWarnings.assess() works', warnings is not None)

print('\n[6] METHODOLOGY TOOLTIPS')
tips = driver.execute_script('return typeof MethodologyTooltips !== "undefined"')
test('MethodologyTooltips module exists', tips)

tips_count = driver.execute_script('return Object.keys(MethodologyTooltips.tips).length')
test('Has multiple tooltip definitions', tips_count and tips_count >= 5)

print('\n[7] R VALIDATION DOCS')
rval = driver.execute_script('return typeof RValidationDoc !== "undefined"')
test('RValidationDoc module exists', rval)

rval_html = driver.execute_script('return RValidationDoc.generateHTML(AppState.results, "thrombolytics")')
test('generateHTML() produces output', rval_html and len(rval_html) > 50)

print('\n[8] TEST OTHER DATASETS')
# Test vaccines
driver.execute_script("loadDemoDataset('vaccines_rr')")
time.sleep(0.5)
vaccines = driver.execute_script('return AppState.studies?.length || 0')
test('Vaccines dataset loads', vaccines > 0)

# Test antihypertensives
driver.execute_script("loadDemoDataset('antihypertensives')")
time.sleep(0.5)
antihyp = driver.execute_script('return AppState.studies?.length || 0')
test('Antihypertensives dataset loads', antihyp > 0)

driver.quit()

print()
print('='*70)
print(f'SUMMARY: {passed}/{passed+failed} tests passed ({100*passed/(passed+failed):.0f}%)')
print('='*70)
