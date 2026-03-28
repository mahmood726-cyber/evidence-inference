"""Test editorial improvements - v2"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.alert import Alert
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

def dismiss_alert():
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
        return True
    except:
        return False

# Check for JS errors
logs = driver.get_log('browser')
errors = [l for l in logs if l['level'] == 'SEVERE']
test('No JS errors', len(errors) == 0)

# 1. DEMO DATASETS
print('\n[1] DEMO DATASETS')
demo_exists = driver.execute_script('return typeof DEMO_DATASETS !== "undefined"')
test('DEMO_DATASETS object exists', demo_exists)

# Load thrombolytics
driver.execute_script("loadDemoDataset('thrombolytics')")
time.sleep(0.5)
studies = driver.execute_script('return AppState.studies?.length || 0')
test('Thrombolytics loaded (12 studies)', studies == 12)

# Check study field names
first_study = driver.execute_script('return AppState.studies?.[0] || null')
if first_study:
    test('Study has name field', 'name' in first_study)
    test('Study has treatment1 field', 'treatment1' in first_study)
    test('Study has treatment2 field', 'treatment2' in first_study)
else:
    test('First study exists', False)
    test('Study has name field', False)
    test('Study has treatment1 field', False)

# Run analysis
dismiss_alert()
driver.execute_script("document.getElementById('runAnalysisBtn').click()")
time.sleep(3)
dismiss_alert()
results = driver.execute_script('return AppState.results !== null')
test('Analysis produces results', results)

# 2. INFLUENCE DIAGNOSTICS
print('\n[2] INFLUENCE DIAGNOSTICS')
infl = driver.execute_script('return typeof InfluenceDiagnostics !== "undefined"')
test('InfluenceDiagnostics module exists', infl)

if results:
    infl_calc = driver.execute_script('return InfluenceDiagnostics.calculate(AppState.results)')
    test('InfluenceDiagnostics.calculate() works', infl_calc is not None)
else:
    test('InfluenceDiagnostics.calculate() works', False)

# 3. ROB SENSITIVITY
print('\n[3] ROB SENSITIVITY')
rob = driver.execute_script('return typeof ROBSensitivity !== "undefined"')
test('ROBSensitivity module exists', rob)

rob_result = driver.execute_script('return ROBSensitivity.analyze(AppState.studies, AppState.effectMeasure)')
test('ROBSensitivity.analyze() works', rob_result is not None)

# 4. PRISMA-NMA CHECKLIST
print('\n[4] PRISMA-NMA CHECKLIST')
prisma = driver.execute_script('return typeof PRISMANMAChecklist !== "undefined"')
test('PRISMANMAChecklist module exists', prisma)

prisma_items = driver.execute_script('return PRISMANMAChecklist.items?.length')
test('PRISMA checklist has items (23)', prisma_items and prisma_items >= 20)

# 5. NETWORK WARNINGS
print('\n[5] NETWORK WARNINGS')
warn = driver.execute_script('return typeof NetworkWarnings !== "undefined"')
test('NetworkWarnings module exists', warn)

warnings = driver.execute_script('return NetworkWarnings.assess(AppState.studies)')
test('NetworkWarnings.assess() works', warnings is not None)

# 6. METHODOLOGY TOOLTIPS
print('\n[6] METHODOLOGY TOOLTIPS')
tips = driver.execute_script('return typeof MethodologyTooltips !== "undefined"')
test('MethodologyTooltips module exists', tips)

tips_count = driver.execute_script('return Object.keys(MethodologyTooltips.tips).length')
test('Has tooltip definitions (10+)', tips_count and tips_count >= 10)

# 7. R VALIDATION DOCS
print('\n[7] R VALIDATION DOCS')
rval = driver.execute_script('return typeof RValidationDoc !== "undefined"')
test('RValidationDoc module exists', rval)

if results:
    rval_html = driver.execute_script('return RValidationDoc.generateHTML(AppState.results, "thrombolytics")')
    test('generateHTML() produces output', rval_html and len(rval_html) > 50)
else:
    test('generateHTML() produces output', False)

# 8. TEST OTHER DATASETS
print('\n[8] TEST OTHER DATASETS')
dismiss_alert()
driver.execute_script("loadDemoDataset('vaccines_rr')")
time.sleep(0.5)
dismiss_alert()
vaccines = driver.execute_script('return AppState.studies?.length || 0')
test('Vaccines dataset loads (5 studies)', vaccines == 5)

driver.quit()

print()
print('='*70)
print(f'SUMMARY: {passed}/{passed+failed} tests passed ({100*passed/(passed+failed):.0f}%)')
print('='*70)
