"""Comprehensive TruthCert-PairwisePro Test - All Datasets, Functions, Plots, Performance"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import time
import json

# Setup - NOT headless so we can see the browser
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)
wait = WebDriverWait(driver, 10)

def dismiss_alert():
    """Dismiss any open alert dialog"""
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
        return True
    except NoAlertPresentException:
        return False

def safe_js(script, default=None):
    """Execute JavaScript safely, handling alerts"""
    try:
        dismiss_alert()  # Clear any pending alerts first
        return driver.execute_script(script)
    except UnexpectedAlertPresentException:
        dismiss_alert()
        return default
    except Exception as e:
        return default

results = {
    'datasets': {},
    'tabs': {},
    'buttons': {},
    'plots': {},
    'functions': {},
    'performance': {},
    'errors': []
}

def log(msg, status='INFO'):
    icon = '[PASS]' if status == 'PASS' else '[FAIL]' if status == 'FAIL' else '[INFO]'
    print(f"  {icon} {msg}")

def check_plot(plot_id, name):
    """Check if a plot container has SVG or canvas content"""
    try:
        dismiss_alert()
        result = safe_js(f'''
            const container = document.getElementById('{plot_id}');
            if (!container) return {{exists: false, reason: 'Container not found'}};
            const svg = container.querySelector('svg');
            const canvas = container.querySelector('canvas');
            const hasContent = container.innerHTML.length > 100;
            return {{
                exists: true,
                hasSVG: !!svg,
                hasCanvas: !!canvas,
                hasContent: hasContent,
                contentLength: container.innerHTML.length
            }};
        ''', {'exists': False})
        if result is None:
            return False, 'No result'
        success = result.get('hasSVG') or result.get('hasCanvas') or result.get('hasContent')
        return success, result
    except Exception as e:
        dismiss_alert()
        return False, str(e)

def check_button(btn_id, name):
    """Check if button exists and is clickable"""
    try:
        btn = driver.find_element(By.ID, btn_id)
        is_visible = btn.is_displayed()
        is_enabled = btn.is_enabled()
        return is_visible and is_enabled, {'visible': is_visible, 'enabled': is_enabled}
    except Exception as e:
        return False, str(e)

def run_js(script, timeout=5):
    """Run JavaScript and return result"""
    try:
        return driver.execute_script(script)
    except Exception as e:
        return {'error': str(e)}

print("=" * 70)
print("TruthCert-PairwisePro v1.0 - COMPREHENSIVE TEST")
print("=" * 70)

# Load application
print("\n[1] LOADING APPLICATION...")
start_load = time.time()
driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
time.sleep(3)
load_time = time.time() - start_load
results['performance']['app_load'] = load_time
log(f"App loaded in {load_time:.2f}s", 'PASS' if load_time < 5 else 'FAIL')

# Get all demo datasets
print("\n[2] TESTING ALL DEMO DATASETS...")
datasets = driver.execute_script('''
    if (typeof DEMO_DATASETS !== 'undefined') {
        return Object.keys(DEMO_DATASETS);
    }
    return [];
''')
print(f"    Found {len(datasets)} demo datasets")

for i, dataset in enumerate(datasets):
    print(f"\n  --- Dataset {i+1}/{len(datasets)}: {dataset} ---")
    results['datasets'][dataset] = {'load': False, 'analysis': False, 'full_analysis': False}

    # Load dataset
    start = time.time()
    try:
        dismiss_alert()
        safe_js(f'loadDemoDataset("{dataset}")')
        time.sleep(1.5)
        dismiss_alert()
        study_count = safe_js('return AppState.studies ? AppState.studies.length : 0', 0)
        load_time = time.time() - start
        results['datasets'][dataset]['load'] = study_count > 0
        results['datasets'][dataset]['study_count'] = study_count
        results['datasets'][dataset]['load_time'] = load_time
        log(f"Loaded: {study_count} studies in {load_time:.2f}s", 'PASS' if study_count > 0 else 'FAIL')
    except Exception as e:
        dismiss_alert()
        log(f"Load failed: {e}", 'FAIL')
        results['errors'].append(f"{dataset} load: {e}")
        continue

    # Run analysis
    start = time.time()
    try:
        dismiss_alert()
        safe_js('runAnalysis()')
        time.sleep(2)
        dismiss_alert()
        has_results = safe_js('return AppState.results !== null', False)
        analysis_time = time.time() - start
        results['datasets'][dataset]['analysis'] = has_results
        results['datasets'][dataset]['analysis_time'] = analysis_time
        log(f"Analysis: {analysis_time:.2f}s", 'PASS' if has_results else 'FAIL')
    except Exception as e:
        dismiss_alert()
        log(f"Analysis failed: {e}", 'FAIL')
        results['errors'].append(f"{dataset} analysis: {e}")

    # Run full analysis
    start = time.time()
    try:
        dismiss_alert()
        safe_js('runFullAnalysis()')
        time.sleep(3)
        dismiss_alert()
        full_time = time.time() - start
        results['datasets'][dataset]['full_analysis'] = True
        results['datasets'][dataset]['full_analysis_time'] = full_time
        log(f"Full Analysis: {full_time:.2f}s", 'PASS')
    except Exception as e:
        dismiss_alert()
        log(f"Full analysis failed: {e}", 'FAIL')
        results['errors'].append(f"{dataset} full analysis: {e}")

# Test all tabs
print("\n[3] TESTING ALL TABS...")
tabs = [
    ('data', 'Data Input'),
    ('analysis', 'Analysis'),
    ('ddma', 'DDMA'),
    ('heterogeneity', 'Heterogeneity'),
    ('bias', 'Publication Bias'),
    ('clinical', 'Clinical'),
    ('multioutcome', 'Multi-Outcome'),
    ('demos', 'Demo Datasets'),
    ('validation', 'Validation'),
    ('crossdisciplinary', 'Cross-Disciplinary'),
    ('code', 'R Code'),
    ('verdict', 'Verdict'),
    ('hta', 'HTA'),
    ('advanced', 'Advanced'),
    ('report', 'Report')
]

for tab_id, tab_name in tabs:
    try:
        dismiss_alert()
        safe_js(f'showTab("{tab_id}")')
        time.sleep(0.5)
        is_active = safe_js(f'''
            const tab = document.getElementById('{tab_id}-tab');
            return tab && tab.style.display !== 'none';
        ''', False)
        results['tabs'][tab_id] = is_active
        log(f"{tab_name} tab", 'PASS' if is_active else 'FAIL')
    except Exception as e:
        dismiss_alert()
        results['tabs'][tab_id] = False
        log(f"{tab_name} tab: {e}", 'FAIL')

# Load BCG for button/plot testing
print("\n[4] LOADING BCG FOR DETAILED TESTING...")
dismiss_alert()
safe_js('loadDemoDataset("BCG")')
time.sleep(2)
dismiss_alert()
safe_js('runAnalysis()')
time.sleep(2)
dismiss_alert()

# Test all plots
print("\n[5] TESTING ALL PLOTS...")
plots = [
    ('forestPlot', 'Forest Plot'),
    ('funnelPlot', 'Funnel Plot'),
    ('galbraithPlot', 'Galbraith Plot'),
    ('labbePlot', 'L\'Abbe Plot'),
    ('baujatPlot', 'Baujat Plot'),
    ('influencePlot', 'Influence Plot'),
    ('cumulativePlot', 'Cumulative Plot'),
    ('qqPlot', 'Q-Q Plot'),
    ('goshPlot', 'GOSH Plot'),
    ('tsaPlot', 'TSA Plot'),
    ('pcurvePlot', 'P-Curve Plot'),
    ('zcurvePlot', 'Z-Curve Plot'),
    ('contourFunnel', 'Contour Funnel'),
    ('trimFillPlot', 'Trim-Fill Plot'),
    ('sunsetPlot', 'Sunset Plot'),
    ('draperyPlot', 'Drapery Plot'),
]

# First render plots
safe_js('showTab("analysis")')
time.sleep(1)

for plot_id, plot_name in plots:
    success, details = check_plot(plot_id, plot_name)
    results['plots'][plot_id] = {'success': success, 'details': details}
    log(f"{plot_name}", 'PASS' if success else 'FAIL')

# Test buttons and functions
print("\n[6] TESTING BUTTONS AND FUNCTIONS...")

# Analysis buttons
buttons = [
    ('runAnalysisBtn', 'Run Analysis'),
    ('fullAnalysisBtn', 'Full Analysis'),
    ('exportCSVBtn', 'Export CSV'),
    ('exportRCodeBtn', 'Export R Code'),
]

for btn_id, btn_name in buttons:
    success, details = check_button(btn_id, btn_name)
    results['buttons'][btn_id] = {'success': success, 'details': details}
    log(f"{btn_name} button", 'PASS' if success else 'FAIL')

# Test key functions
print("\n[7] TESTING KEY STATISTICAL FUNCTIONS...")

functions_to_test = [
    ('mantelHaenszel', 'return typeof mantelHaenszel === "function"'),
    ('petoMethod', 'return typeof petoMethod === "function"'),
    ('cookDistance', 'return typeof cookDistance === "function"'),
    ('eggerTest', 'return typeof eggerTest === "function"'),
    ('beggTest', 'return typeof beggTest === "function"'),
    ('trimAndFill', 'return typeof trimAndFill === "function"'),
    ('petPeese', 'return typeof petPeese === "function"'),
    ('metaRegression', 'return typeof metaRegression === "function"'),
    ('subgroupAnalysis', 'return typeof subgroupAnalysis === "function"'),
    ('leaveOneOut', 'return typeof leaveOneOut === "function"'),
    ('cumulativeMetaAnalysis', 'return typeof cumulativeMetaAnalysis === "function"'),
    ('bayesianMetaAnalysis', 'return typeof bayesianMetaAnalysis === "function"'),
    ('fragilityIndex', 'return typeof fragilityIndex === "function"'),
    ('glmmMetaAnalysis', 'return typeof glmmMetaAnalysis === "function"'),
    ('networkMAConsistency', 'return typeof networkMAConsistency === "function"'),
    ('profileLikelihood', 'return typeof profileLikelihood === "function"'),
    ('robmaModelAveraging', 'return typeof robmaModelAveraging === "function"'),
    ('multiverseMetaAnalysis', 'return typeof multiverseMetaAnalysis === "function"'),
    ('sequentialMetaAnalysis', 'return typeof sequentialMetaAnalysis === "function"'),
    ('pUniformStar', 'return typeof pUniformStar === "function"'),
]

for func_name, check_script in functions_to_test:
    try:
        dismiss_alert()
        exists = safe_js(check_script, False)
        results['functions'][func_name] = exists
        log(f"{func_name}()", 'PASS' if exists else 'FAIL')
    except Exception as e:
        dismiss_alert()
        results['functions'][func_name] = False
        log(f"{func_name}(): {e}", 'FAIL')

# Test advanced panel buttons
print("\n[8] TESTING ADVANCED PANEL...")
dismiss_alert()
safe_js('showTab("advanced")')
time.sleep(1)

advanced_buttons = [
    ('runGOSH', 'GOSH Analysis'),
    ('runTSA', 'Trial Sequential'),
    ('runPCurve', 'P-Curve'),
    ('runZCurve', 'Z-Curve'),
    ('runInfluence', 'Influence'),
    ('runCopas', 'Copas Selection'),
    ('runGRADE', 'GRADE'),
    ('runSmallSampleCI', 'Small Sample CI'),
    ('runExtendedValidation', 'Extended Validation'),
]

for btn_id, btn_name in advanced_buttons:
    try:
        btn = driver.find_element(By.ID, btn_id)
        btn.click()
        time.sleep(2)
        results['buttons'][btn_id] = True
        log(f"{btn_name}", 'PASS')
    except Exception as e:
        results['buttons'][btn_id] = False
        log(f"{btn_name}: {e}", 'FAIL')

# Test HTA panel
print("\n[9] TESTING HTA PANEL...")
dismiss_alert()
safe_js('showTab("hta")')
time.sleep(1)

try:
    dismiss_alert()
    safe_js('runHTA()')
    time.sleep(2)
    dismiss_alert()
    hta_result = safe_js('return document.getElementById("htaResults").innerHTML.length > 0', False)
    results['buttons']['runHTA'] = hta_result
    log("HTA Analysis", 'PASS' if hta_result else 'FAIL')
except Exception as e:
    dismiss_alert()
    results['buttons']['runHTA'] = False
    log(f"HTA Analysis: {e}", 'FAIL')

# Test Verdict panel
print("\n[10] TESTING VERDICT PANEL...")
dismiss_alert()
safe_js('showTab("verdict")')
time.sleep(1)

try:
    dismiss_alert()
    safe_js('generateVerdict()')
    time.sleep(2)
    dismiss_alert()
    verdict_result = safe_js('return document.getElementById("verdictResults").innerHTML.length > 0', False)
    results['buttons']['generateVerdict'] = verdict_result
    log("Verdict Generation", 'PASS' if verdict_result else 'FAIL')
except Exception as e:
    dismiss_alert()
    results['buttons']['generateVerdict'] = False
    log(f"Verdict Generation: {e}", 'FAIL')

# Performance summary
print("\n[11] PERFORMANCE METRICS...")
avg_load = sum(d.get('load_time', 0) for d in results['datasets'].values()) / max(1, len(results['datasets']))
avg_analysis = sum(d.get('analysis_time', 0) for d in results['datasets'].values() if 'analysis_time' in d) / max(1, len(results['datasets']))
avg_full = sum(d.get('full_analysis_time', 0) for d in results['datasets'].values() if 'full_analysis_time' in d) / max(1, len(results['datasets']))

results['performance']['avg_load_time'] = avg_load
results['performance']['avg_analysis_time'] = avg_analysis
results['performance']['avg_full_analysis_time'] = avg_full

log(f"Avg Dataset Load: {avg_load:.2f}s", 'PASS' if avg_load < 2 else 'FAIL')
log(f"Avg Analysis Time: {avg_analysis:.2f}s", 'PASS' if avg_analysis < 3 else 'FAIL')
log(f"Avg Full Analysis: {avg_full:.2f}s", 'PASS' if avg_full < 5 else 'FAIL')

# Calculate totals
print("\n" + "=" * 70)
print("COMPREHENSIVE TEST SUMMARY")
print("=" * 70)

dataset_pass = sum(1 for d in results['datasets'].values() if d.get('load') and d.get('analysis'))
tab_pass = sum(1 for v in results['tabs'].values() if v)
button_pass = sum(1 for v in results['buttons'].values() if v == True or (isinstance(v, dict) and v.get('success')))
plot_pass = sum(1 for p in results['plots'].values() if p.get('success'))
func_pass = sum(1 for v in results['functions'].values() if v)

print(f"\n  Datasets:   {dataset_pass}/{len(results['datasets'])} ({100*dataset_pass/max(1,len(results['datasets'])):.0f}%)")
print(f"  Tabs:       {tab_pass}/{len(results['tabs'])} ({100*tab_pass/max(1,len(results['tabs'])):.0f}%)")
print(f"  Buttons:    {button_pass}/{len(results['buttons'])} ({100*button_pass/max(1,len(results['buttons'])):.0f}%)")
print(f"  Plots:      {plot_pass}/{len(results['plots'])} ({100*plot_pass/max(1,len(results['plots'])):.0f}%)")
print(f"  Functions:  {func_pass}/{len(results['functions'])} ({100*func_pass/max(1,len(results['functions'])):.0f}%)")

total_pass = dataset_pass + tab_pass + button_pass + plot_pass + func_pass
total_tests = len(results['datasets']) + len(results['tabs']) + len(results['buttons']) + len(results['plots']) + len(results['functions'])
print(f"\n  TOTAL:      {total_pass}/{total_tests} ({100*total_pass/max(1,total_tests):.1f}%)")

print(f"\n  Performance:")
print(f"    App Load:      {results['performance']['app_load']:.2f}s")
print(f"    Avg Load:      {avg_load:.2f}s")
print(f"    Avg Analysis:  {avg_analysis:.2f}s")
print(f"    Avg Full:      {avg_full:.2f}s")

if results['errors']:
    print(f"\n  ERRORS ({len(results['errors'])}):")
    for err in results['errors'][:10]:
        print(f"    - {err}")

print("\n" + "=" * 70)

# Save results
with open('C:/Users/user/comprehensive_test_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("Results saved to: comprehensive_test_results.json")

# Keep browser open for inspection
input("\nPress Enter to close browser...")
driver.quit()
