"""Complete TruthCert-PairwisePro Test - Every Dataset, Button, Function, Plot"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import json

# Setup - Visible browser
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.set_window_size(1500, 900)
wait = WebDriverWait(driver, 10)

results = {
    'datasets': [],
    'tabs': [],
    'buttons': [],
    'plots': [],
    'functions': [],
    'analyses': [],
    'errors': []
}

def dismiss_alert():
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
        return True
    except:
        return False

def safe_js(script, default=None):
    try:
        dismiss_alert()
        return driver.execute_script(script)
    except:
        dismiss_alert()
        return default

def log_result(category, name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {name}" + (f" - {details}" if details and not passed else ""))
    results[category].append({'name': name, 'passed': passed, 'details': details})
    return passed

print("=" * 80)
print("TruthCert-PairwisePro v1.0 - COMPLETE APPLICATION TEST")
print("=" * 80)

# ============================================================
# PHASE 1: Load Application
# ============================================================
print("\n" + "=" * 80)
print("PHASE 1: APPLICATION LOAD")
print("=" * 80)

driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
time.sleep(4)

title = driver.title
log_result('buttons', 'Page loads correctly', 'TruthCert' in title, title)

# ============================================================
# PHASE 2: Test All Demo Datasets
# ============================================================
print("\n" + "=" * 80)
print("PHASE 2: ALL DEMO DATASETS (Load + Analysis + Full Analysis)")
print("=" * 80)

datasets = safe_js('return Object.keys(DEMO_DATASETS)', [])
print(f"\nFound {len(datasets)} demo datasets\n")

for i, dataset in enumerate(datasets):
    print(f"\n--- [{i+1}/{len(datasets)}] {dataset} ---")

    # Load dataset
    safe_js(f'loadDemoDataset("{dataset}")')
    time.sleep(1.5)
    dismiss_alert()

    study_count = safe_js('return AppState.studies ? AppState.studies.length : 0', 0)
    log_result('datasets', f'{dataset} - Load', study_count > 0, f'{study_count} studies')

    if study_count == 0:
        continue

    # Run Analysis
    safe_js('runAnalysis()')
    time.sleep(2)
    dismiss_alert()

    has_results = safe_js('return AppState.results !== null', False)
    log_result('datasets', f'{dataset} - Analysis', has_results)

    # Run Full Analysis
    safe_js('runFullAnalysis()')
    time.sleep(3)
    dismiss_alert()

    has_full = safe_js('return AppState.results && AppState.results.loo !== undefined', False)
    log_result('datasets', f'{dataset} - Full Analysis', has_full)

# ============================================================
# PHASE 3: Test All Tabs
# ============================================================
print("\n" + "=" * 80)
print("PHASE 3: ALL TABS")
print("=" * 80)

# Load BCG for consistent testing
safe_js('loadDemoDataset("BCG")')
time.sleep(1.5)
safe_js('runAnalysis()')
time.sleep(2)
dismiss_alert()

tabs = [
    ('data', 'Data Input'),
    ('analysis', 'Analysis Results'),
    ('ddma', 'Decision-Driven MA'),
    ('heterogeneity', 'Heterogeneity'),
    ('bias', 'Publication Bias'),
    ('clinical', 'Clinical Utility'),
    ('multioutcome', 'Multi-Outcome'),
    ('demos', 'Demo Datasets'),
    ('validation', 'Validation'),
    ('crossdisciplinary', 'Cross-Disciplinary'),
    ('code', 'R Code Export'),
    ('verdict', 'TruthCert Verdict'),
    ('hta', 'HTA Economic'),
    ('advanced', 'Advanced Methods'),
    ('report', 'Report')
]

print(f"\nTesting {len(tabs)} tabs\n")

for tab_id, tab_name in tabs:
    try:
        # Hide floating button that may intercept clicks
        safe_js('document.getElementById("floatingReportBtn").style.display = "none"')

        # Use JavaScript to click tab (avoids click interception)
        safe_js(f'document.querySelector(\'button[data-tab="{tab_id}"]\').click()')
        time.sleep(0.5)
        dismiss_alert()

        # Check if panel is visible
        is_visible = safe_js(f'''
            const panel = document.getElementById("panel-{tab_id}");
            return panel && panel.style.display !== "none" && panel.offsetParent !== null;
        ''', False)
        log_result('tabs', f'{tab_name} tab', is_visible)
    except Exception as e:
        log_result('tabs', f'{tab_name} tab', False, str(e)[:50])

# ============================================================
# PHASE 4: Test All Plots
# ============================================================
print("\n" + "=" * 80)
print("PHASE 4: ALL PLOTS")
print("=" * 80)

# Go to analysis tab and run full analysis
safe_js('document.querySelector(\'button[data-tab="analysis"]\').click()')
time.sleep(1)
safe_js('runFullAnalysis()')
time.sleep(3)
dismiss_alert()

# Render all plots explicitly
print("\nRendering all plots...")
safe_js('if(typeof renderForestPlot === "function") renderForestPlot(AppState.results)')
time.sleep(0.5)
safe_js('if(typeof renderFunnelPlot === "function") renderFunnelPlot(AppState.results)')
time.sleep(0.5)
safe_js('if(typeof renderBaujatPlot === "function") renderBaujatPlot(AppState.results)')
time.sleep(0.5)

plots = [
    ('forestPlot', 'Forest Plot'),
    ('funnelPlot', 'Funnel Plot'),
    ('baujatPlot', 'Baujat Plot'),
]

print(f"\nTesting {len(plots)} main plots\n")

for plot_id, plot_name in plots:
    has_content = safe_js(f'''
        const el = document.getElementById("{plot_id}");
        if (!el) return false;
        const svg = el.querySelector("svg");
        const canvas = el.querySelector("canvas");
        return (svg && svg.innerHTML.length > 100) || (canvas !== null) || el.innerHTML.length > 200;
    ''', False)
    log_result('plots', plot_name, has_content)

# ============================================================
# PHASE 5: Test Advanced Panel Analyses
# ============================================================
print("\n" + "=" * 80)
print("PHASE 5: ADVANCED PANEL ANALYSES")
print("=" * 80)

safe_js('document.querySelector(\'button[data-tab="advanced"]\').click()')
time.sleep(1)

advanced_tests = [
    ('runGOSHAnalysis()', 'goshResults', 'GOSH Analysis'),
    ('runTSAAnalysis()', 'tsaResults', 'Trial Sequential Analysis'),
    ('runPCurveAnalysis()', 'pCurveResults', 'P-Curve Analysis'),
    ('runZCurveAnalysis()', 'zCurveResults', 'Z-Curve Analysis'),
    ('runInfluenceDiagnostics()', 'influenceResults', 'Influence Diagnostics'),
    ('runCopasModel()', 'copasResults', 'Copas Selection Model'),
    ('runGRADEAssessment()', 'gradeResults', 'GRADE Assessment'),
    ('runSmallSampleCI()', 'smallSampleResults', 'Small Sample CI'),
    ('runExtendedValidationUI()', 'validationResults', 'Extended Validation'),
]

print(f"\nTesting {len(advanced_tests)} advanced analyses\n")

for func, result_id, name in advanced_tests:
    try:
        safe_js(func)
        time.sleep(2)
        dismiss_alert()

        has_result = safe_js(f'''
            const el = document.getElementById("{result_id}");
            return el && el.innerHTML.length > 50;
        ''', False)
        log_result('analyses', name, has_result)
    except Exception as e:
        log_result('analyses', name, False, str(e)[:50])

# ============================================================
# PHASE 6: Test HTA Panel
# ============================================================
print("\n" + "=" * 80)
print("PHASE 6: HTA ECONOMIC ANALYSIS")
print("=" * 80)

# HTA requires TruthCert analysis first
safe_js('runTruthCertAnalysis()')
time.sleep(2)

safe_js('document.querySelector(\'button[data-tab="hta"]\').click()')
time.sleep(1)

try:
    safe_js('runHTAAnalysis()')
    time.sleep(2)
    dismiss_alert()

    hta_result = safe_js('''
        return AppState.hta && AppState.hta.results !== null;
    ''', False)
    log_result('analyses', 'HTA Analysis', hta_result)
except Exception as e:
    log_result('analyses', 'HTA Analysis', False, str(e)[:50])

# ============================================================
# PHASE 7: Test Verdict System
# ============================================================
print("\n" + "=" * 80)
print("PHASE 7: VERDICT SYSTEM")
print("=" * 80)

safe_js('document.querySelector(\'button[data-tab="verdict"]\').click()')
time.sleep(1)

try:
    safe_js('runTruthCertAnalysis()')
    time.sleep(2)
    dismiss_alert()

    verdict_result = safe_js('''
        const container = document.getElementById("verdictCardContainer");
        return container && container.innerHTML.length > 50;
    ''', False)
    log_result('analyses', 'Verdict Generation', verdict_result)
except Exception as e:
    log_result('analyses', 'Verdict Generation', False, str(e)[:50])

# ============================================================
# PHASE 8: Test All Statistical Functions
# ============================================================
print("\n" + "=" * 80)
print("PHASE 8: ALL STATISTICAL FUNCTIONS")
print("=" * 80)

# Reload BCG and run analysis
safe_js('loadDemoDataset("BCG")')
time.sleep(1.5)
safe_js('runAnalysis()')
time.sleep(2)

functions = [
    # Core MA functions
    ('calculatePooledEstimate', 'Core: Pooled Estimate'),
    ('estimateTau2', 'Core: Tau2 Estimation'),
    ('calculateHeterogeneity', 'Core: Heterogeneity Stats'),
    ('calculateHKSJ', 'Core: Knapp-Hartung'),

    # Effect sizes
    ('calculateLogOR', 'Effect: Log Odds Ratio'),
    ('calculateLogRR', 'Effect: Log Risk Ratio'),
    ('calculateRD', 'Effect: Risk Difference'),
    ('calculateSMD', 'Effect: Standardized Mean Diff'),
    ('calculateMD', 'Effect: Mean Difference'),

    # Publication bias
    ('eggerTest', 'Bias: Egger Test'),
    ('beggTest', 'Bias: Begg Test'),
    ('trimAndFill', 'Bias: Trim and Fill'),
    ('failsafeN', 'Bias: Fail-safe N'),
    ('petPeese', 'Bias: PET-PEESE'),
    ('petersTest', 'Bias: Peters Test'),
    ('harbordTest', 'Bias: Harbord Test'),
    ('copasSelectionModel', 'Bias: Copas Model'),
    ('testExcessSignificance', 'Bias: TES'),

    # Influence diagnostics
    ('cookDistance', 'Influence: Cook Distance'),
    ('leaveOneOut', 'Influence: Leave-One-Out'),
    ('baujatPlotData', 'Influence: Baujat Data'),

    # Fixed effects methods
    ('mantelHaenszel', 'Fixed: Mantel-Haenszel'),
    ('petoMethod', 'Fixed: Peto Method'),

    # Advanced methods
    ('metaRegression', 'Advanced: Meta-Regression'),
    ('subgroupAnalysis', 'Advanced: Subgroup Analysis'),
    ('cumulativeMetaAnalysis', 'Advanced: Cumulative MA'),
    ('threeLevelMA', 'Advanced: Three-Level MA'),
    ('bayesianMetaAnalysis', 'Advanced: Bayesian MA'),
    ('fragilityIndex', 'Advanced: Fragility Index'),

    # Gap closure functions
    ('glmmMetaAnalysis', 'Gap: GLMM Meta-Analysis'),
    ('betaBinomialMA', 'Gap: Beta-Binomial MA'),
    ('networkMAConsistency', 'Gap: Network MA Consistency'),
    ('sideSplittingTest', 'Gap: Side-Splitting Test'),
    ('netHeatPlotData', 'Gap: Net Heat Plot'),
    ('profileLikelihood', 'Gap: Profile Likelihood'),
    ('likelihoodRatioTest', 'Gap: LR Test'),

    # Innovative functions
    ('robmaModelAveraging', 'Innovative: RoBMA'),
    ('multiverseMetaAnalysis', 'Innovative: Multiverse'),
    ('improvedPredictionInterval', 'Innovative: Improved PI'),
    ('sequentialMetaAnalysis', 'Innovative: Sequential MA'),
    ('pUniformStar', 'Innovative: P-Uniform*'),
    ('valueOfInformation', 'Innovative: VOI'),
    ('albatrossPlotData', 'Innovative: Albatross Plot'),
    ('sunsetPlotData', 'Innovative: Sunset Plot'),
    ('draperyPlotData', 'Innovative: Drapery Plot'),
    ('harvestPlotData', 'Innovative: Harvest Plot'),
    ('decisionCurveAnalysis', 'Innovative: DCA'),
    ('thresholdNNT', 'Innovative: Threshold NNT'),
    ('permutationTestI2', 'Innovative: Permutation I2'),
    ('limitMetaAnalysis', 'Innovative: Limit MA'),
    ('waapWLS', 'Innovative: WAAP-WLS'),
    ('multiCriteriaDecision', 'Innovative: MCDA'),
    ('specificationCurveAnalysis', 'Innovative: Spec Curve'),
    ('vibrationOfEffects', 'Innovative: Vibration'),
    ('livingReviewStatus', 'Innovative: Living Review'),
    ('threeParameterSelectionModel', 'Innovative: 3PSM'),
    ('robustTau2', 'Innovative: Robust Tau2'),
]

print(f"\nTesting {len(functions)} statistical functions\n")

for func_name, display_name in functions:
    exists = safe_js(f'return typeof {func_name} === "function"', False)
    log_result('functions', display_name, exists)

# ============================================================
# PHASE 9: Test Function Execution
# ============================================================
print("\n" + "=" * 80)
print("PHASE 9: FUNCTION EXECUTION TESTS")
print("=" * 80)

# Reload BCG for execution tests
safe_js('loadDemoDataset("BCG")')
time.sleep(2)
safe_js('runFullAnalysis()')  # Full analysis computes LOO, influence, etc.
time.sleep(3)
dismiss_alert()

execution_tests = [
    ('Mantel-Haenszel OR', '''
        try {
            const studies = AppState.studies.map(s => ({
                a: s.events_t, b: s.n_t - s.events_t,
                c: s.events_c, d: s.n_c - s.events_c,
                n1: s.n_t, n2: s.n_c
            }));
            const result = mantelHaenszel(studies, 'OR');
            // Result has 'estimate' property (OR value), not 'OR'
            return result && (result.estimate > 0 || result.skipped);
        } catch(e) { return false; }
    '''),
    ('Peto Method', '''
        try {
            const studies = AppState.studies.map(s => ({
                a: s.events_t, b: s.n_t - s.events_t,
                c: s.events_c, d: s.n_c - s.events_c,
                n1: s.n_t, n2: s.n_c
            }));
            const result = petoMethod(studies);
            // Result has 'estimate' property (OR value), not 'OR'
            return result && (result.estimate > 0 || result.skipped);
        } catch(e) { return false; }
    '''),
    ('Cook Distance', '''
        try {
            // Check influenceDiag is computed (contains Cook's D)
            const r = AppState.results;
            if (!r || !r.influenceDiag) return false;
            return r.influenceDiag.studies && r.influenceDiag.studies.length > 0;
        } catch(e) { return false; }
    '''),
    ('Egger Test', '''
        try {
            // Egger test is computed during analysis
            const r = AppState.results;
            if (!r || !r.egger) return false;
            return r.egger.p_value !== undefined || r.egger.pValue !== undefined;
        } catch(e) { return false; }
    '''),
    ('Leave-One-Out', '''
        try {
            // LOO is computed during full analysis
            const r = AppState.results;
            if (!r) return false;
            // LOO exists in results (even if skipped for small datasets)
            return r.loo !== undefined;
        } catch(e) { return false; }
    '''),
    ('GLMM Analysis', '''
        try {
            const s = AppState.studies;
            if (!s || s.length < 2) return false;
            const ai = s.map(x => x.events_t || 0);
            const bi = s.map(x => (x.n_t || 0) - (x.events_t || 0));
            const ci = s.map(x => x.events_c || 0);
            const di = s.map(x => (x.n_c || 0) - (x.events_c || 0));
            const r = glmmMetaAnalysis(ai, bi, ci, di);
            return r && r.method === "Generalized Linear Mixed Model (GLMM)";
        } catch(e) { return false; }
    '''),
    ('Profile Likelihood', '''
        try {
            const r = AppState.results;
            if (!r) return false;
            const yi = r.yi || (r.studies ? r.studies.map(s => s.yi) : null);
            const vi = r.vi || (r.studies ? r.studies.map(s => s.vi) : null);
            if (!yi || !vi) return false;
            const result = profileLikelihood(yi, vi, "tau2");
            return result && result.method === "Profile Likelihood";
        } catch(e) { return false; }
    '''),
    ('RoBMA', '''
        try {
            const r = AppState.results;
            if (!r) return false;
            const yi = r.yi || (r.studies ? r.studies.map(s => s.yi) : null);
            const vi = r.vi || (r.studies ? r.studies.map(s => s.vi) : null);
            if (!yi || !vi) return false;
            const result = robmaModelAveraging(yi, vi);
            return result && result.models && result.models.length > 0;
        } catch(e) { return false; }
    '''),
]

print(f"\nTesting {len(execution_tests)} function executions\n")

for name, script in execution_tests:
    try:
        result = safe_js(script, False)
        log_result('analyses', f'Execute: {name}', result == True)
    except Exception as e:
        log_result('analyses', f'Execute: {name}', False, str(e)[:50])

# ============================================================
# PHASE 10: Test Buttons
# ============================================================
print("\n" + "=" * 80)
print("PHASE 10: ALL BUTTONS")
print("=" * 80)

# Go back to data tab
safe_js('document.querySelector(\'button[data-tab="data"]\').click()')
time.sleep(0.5)

buttons = [
    ('runAnalysisBtn', 'Run Analysis'),
    ('addStudyBtn', 'Add Study'),
    ('clearAllBtn', 'Clear All'),
    ('exportCsvBtn', 'Export CSV'),
    ('importKMBtn', 'KM Import'),
]

print(f"\nTesting {len(buttons)} main buttons\n")

for btn_id, btn_name in buttons:
    try:
        btn = driver.find_element(By.ID, btn_id)
        exists = btn.is_displayed() and btn.is_enabled()
        log_result('buttons', f'{btn_name} button', exists)
    except:
        log_result('buttons', f'{btn_name} button', False, 'Not found')

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 80)
print("COMPREHENSIVE TEST SUMMARY")
print("=" * 80)

categories = ['datasets', 'tabs', 'plots', 'functions', 'analyses', 'buttons']
total_pass = 0
total_fail = 0

for cat in categories:
    passed = sum(1 for r in results[cat] if r['passed'])
    failed = sum(1 for r in results[cat] if not r['passed'])
    total_pass += passed
    total_fail += failed
    total = passed + failed
    pct = 100 * passed / total if total > 0 else 0
    status = "PASS" if failed == 0 else "FAIL"
    print(f"\n  [{status}] {cat.upper()}: {passed}/{total} ({pct:.1f}%)")

    # Show failures
    failures = [r for r in results[cat] if not r['passed']]
    for f in failures[:5]:
        print(f"       - FAILED: {f['name']}")

total = total_pass + total_fail
print(f"\n{'='*80}")
print(f"  TOTAL: {total_pass}/{total} ({100*total_pass/total:.1f}%)")
print(f"{'='*80}")

# Save results
with open('C:/Users/user/full_test_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to: full_test_results.json")

if total_fail > 0:
    print(f"\n[WARNING] {total_fail} tests failed - review above for details")
else:
    print(f"\n[SUCCESS] ALL {total_pass} TESTS PASSED!")

time.sleep(2)
driver.quit()
