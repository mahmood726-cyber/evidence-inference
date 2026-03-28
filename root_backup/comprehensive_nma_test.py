"""Comprehensive NMA Pro v6.2 Test - All Datasets, Buttons, Functions, and Plots"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(3)

print('='*70)
print('COMPREHENSIVE NMA PRO v6.2 TEST')
print('='*70)

passed = 0
failed = 0
warnings = 0

def test(name, condition, warn_only=False):
    global passed, failed, warnings
    if condition:
        print(f'[PASS] {name}')
        passed += 1
        return True
    else:
        if warn_only:
            print(f'[WARN] {name}')
            warnings += 1
        else:
            print(f'[FAIL] {name}')
            failed += 1
        return False

# Check for initial JS errors
logs = driver.get_log('browser')
errors = [l for l in logs if l['level'] == 'SEVERE']
test('No initial JS errors', len(errors) == 0)
if errors:
    for e in errors[:5]:
        print(f'  Error: {e["message"][:100]}')

# ============================================================
# SECTION 1: DEMO DATASETS
# ============================================================
print('\n' + '='*70)
print('SECTION 1: DEMO DATASETS')
print('='*70)

datasets = driver.execute_script("return typeof DEMO_DATASETS !== 'undefined' ? Object.keys(DEMO_DATASETS) : []")
print(f'\nFound {len(datasets)} demo datasets: {datasets}')

for dataset in datasets:
    print(f'\n--- Testing dataset: {dataset} ---')

    # Load dataset
    try:
        driver.execute_script(f"loadDemoDataset('{dataset}')")
        time.sleep(0.5)

        # Check if studies loaded
        studies = driver.execute_script("return AppState.studies")
        test(f'{dataset}: Data loaded', studies is not None and len(studies) > 0)
        if studies:
            print(f'    Loaded {len(studies)} studies')

        # Run analysis
        driver.execute_script("document.getElementById('runAnalysisBtn').click()")
        time.sleep(2)

        # Check results
        results = driver.execute_script("return AppState.results")
        test(f'{dataset}: Analysis completed', results is not None)

        if results:
            # Check heterogeneity
            het = results.get('heterogeneity', {})
            if het:
                tau2 = het.get('tau2')
                I2 = het.get('I2')
                print(f'    Heterogeneity: tau2={tau2:.4f if tau2 else "N/A"}, I2={I2:.1f}% if I2 else "N/A"')

            # Check league table
            league = results.get('leagueTable')
            test(f'{dataset}: League table generated', league is not None, warn_only=True)

            # Check effects
            effects = results.get('effects', {}).get('effects', [])
            test(f'{dataset}: Treatment effects computed', len(effects) > 0)
            if effects:
                print(f'    Computed {len(effects)} treatment effects')

        # Clear JS errors from this run
        driver.get_log('browser')

    except Exception as e:
        print(f'[FAIL] {dataset}: Error - {str(e)[:50]}')
        failed += 1

# ============================================================
# SECTION 2: CORE MODULES
# ============================================================
print('\n' + '='*70)
print('SECTION 2: CORE MODULES')
print('='*70)

# Load thrombolytics for testing
driver.execute_script("loadDemoDataset('thrombolytics')")
time.sleep(0.5)
driver.execute_script("document.getElementById('runAnalysisBtn').click()")
time.sleep(2)

core_modules = [
    'FrequentistNMA', 'BayesianNMA', 'ThresholdAnalysis', 'CINeMA',
    'ProfileLikelihood', 'NetworkMetaRegression', 'LeaveOneOut', 'DataQuality',
    'PRISMANMAChecklist', 'GradeNMA', 'InfluenceDiagnostics', 'ROBSensitivity',
    'NetworkWarnings', 'MethodologyTooltips', 'RValidationDoc',
    'TrimAndFill', 'EggersTest', 'BeggsTest', 'PETPEESE', 'SelectionModels',
    'ComparisonAdjustedFunnel', 'ComponentNMA', 'HierarchicalNMA',
    'DoseResponse', 'RobustVariance', 'MultipleImputation', 'NodeSplittingTest'
]

for module in core_modules:
    exists = driver.execute_script(f"return typeof {module} !== 'undefined'")
    test(f'Module: {module}', exists)

# ============================================================
# SECTION 3: CORE FUNCTIONS
# ============================================================
print('\n' + '='*70)
print('SECTION 3: CORE FUNCTIONS')
print('='*70)

core_functions = [
    'runAnalysis', 'loadDemoDataset', 'renderForestPlot', 'renderFunnelPlot',
    'renderNetworkGraph', 'exportResults', 'parseCSV', 'calculatePooledEffect'
]

for func in core_functions:
    exists = driver.execute_script(f"return typeof {func} === 'function'")
    test(f'Function: {func}()', exists)

# ============================================================
# SECTION 4: PLOT RENDERING
# ============================================================
print('\n' + '='*70)
print('SECTION 4: PLOT RENDERING')
print('='*70)

# Forest Plot
print('\n--- Forest Plot ---')
forest_canvas = driver.execute_script("""
    const canvas = document.getElementById('forestPlot');
    if (!canvas) return null;
    return {
        exists: true,
        width: canvas.width,
        height: canvas.height,
        hasContent: canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data.some(x => x !== 0)
    };
""")
test('Forest plot canvas exists', forest_canvas is not None and forest_canvas.get('exists'))
if forest_canvas:
    test('Forest plot has dimensions', forest_canvas.get('width', 0) > 0 and forest_canvas.get('height', 0) > 0)
    test('Forest plot has content', forest_canvas.get('hasContent', False))
    print(f'    Dimensions: {forest_canvas.get("width")}x{forest_canvas.get("height")}')

# Funnel Plot
print('\n--- Funnel Plot ---')
funnel_canvas = driver.execute_script("""
    const canvas = document.getElementById('funnelPlot');
    if (!canvas) return null;
    return {
        exists: true,
        width: canvas.width,
        height: canvas.height,
        hasContent: canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data.some(x => x !== 0)
    };
""")
test('Funnel plot canvas exists', funnel_canvas is not None and funnel_canvas.get('exists'))
if funnel_canvas:
    test('Funnel plot has dimensions', funnel_canvas.get('width', 0) > 0 and funnel_canvas.get('height', 0) > 0)
    test('Funnel plot has content', funnel_canvas.get('hasContent', False))
    print(f'    Dimensions: {funnel_canvas.get("width")}x{funnel_canvas.get("height")}')

# Network Graph
print('\n--- Network Graph ---')
network_canvas = driver.execute_script("""
    const canvas = document.getElementById('networkGraph');
    if (!canvas) return null;
    return {
        exists: true,
        width: canvas.width,
        height: canvas.height,
        hasContent: canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data.some(x => x !== 0)
    };
""")
test('Network graph canvas exists', network_canvas is not None and network_canvas.get('exists'))
if network_canvas:
    test('Network graph has dimensions', network_canvas.get('width', 0) > 0 and network_canvas.get('height', 0) > 0)
    test('Network graph has content', network_canvas.get('hasContent', False))
    print(f'    Dimensions: {network_canvas.get("width")}x{network_canvas.get("height")}')

# ============================================================
# SECTION 5: BUTTONS AND UI ELEMENTS
# ============================================================
print('\n' + '='*70)
print('SECTION 5: BUTTONS AND UI ELEMENTS')
print('='*70)

buttons = [
    ('runAnalysisBtn', 'Run Analysis'),
    ('exportBtn', 'Export Results'),
    ('clearBtn', 'Clear Data'),
]

for btn_id, btn_name in buttons:
    btn = driver.execute_script(f"return document.getElementById('{btn_id}')")
    test(f'Button: {btn_name}', btn is not None)

# Check for tabs/sections
tabs = driver.execute_script("""
    return Array.from(document.querySelectorAll('.tab, [role="tab"], .nav-link, button[data-tab]'))
        .map(t => t.textContent.trim().substring(0, 30));
""")
print(f'\nFound {len(tabs)} tab elements')
for tab in tabs[:10]:
    print(f'    - {tab}')

# ============================================================
# SECTION 6: PUBLICATION BIAS FUNCTIONS
# ============================================================
print('\n' + '='*70)
print('SECTION 6: PUBLICATION BIAS FUNCTIONS')
print('='*70)

# Test TrimAndFill
print('\n--- Trim and Fill ---')
taf_result = driver.execute_script("""
    if (typeof TrimAndFill === 'undefined') return null;
    const processed = AppState.results?.processed;
    if (!processed) return null;
    try {
        return TrimAndFill.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
test('TrimAndFill.analyze() works', taf_result is not None and 'error' not in (taf_result or {}))
if taf_result and 'error' not in taf_result:
    print(f'    Imputed studies: {taf_result.get("imputedStudies", "N/A")}')
    print(f'    Adjusted effect: {taf_result.get("adjustedEffect", "N/A")}')

# Test Egger's Test
print('\n--- Egger\'s Test ---')
egger_result = driver.execute_script("""
    if (typeof EggersTest === 'undefined') return null;
    const processed = AppState.results?.processed;
    if (!processed) return null;
    try {
        return EggersTest.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
test('EggersTest.analyze() works', egger_result is not None and 'error' not in (egger_result or {}))
if egger_result and 'error' not in egger_result:
    print(f'    Intercept: {egger_result.get("intercept", "N/A")}')
    print(f'    p-value: {egger_result.get("pValue", "N/A")}')

# Test Begg's Test
print('\n--- Begg\'s Test ---')
begg_result = driver.execute_script("""
    if (typeof BeggsTest === 'undefined') return null;
    const processed = AppState.results?.processed;
    if (!processed) return null;
    try {
        return BeggsTest.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
test('BeggsTest.analyze() works', begg_result is not None and 'error' not in (begg_result or {}))
if begg_result and 'error' not in begg_result:
    print(f'    Kendall tau: {begg_result.get("tau", "N/A")}')
    print(f'    p-value: {begg_result.get("pValue", "N/A")}')

# Test PET-PEESE
print('\n--- PET-PEESE ---')
petpeese_result = driver.execute_script("""
    if (typeof PETPEESE === 'undefined') return null;
    const processed = AppState.results?.processed;
    if (!processed) return null;
    try {
        return PETPEESE.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
test('PETPEESE.analyze() works', petpeese_result is not None and 'error' not in (petpeese_result or {}))
if petpeese_result and 'error' not in petpeese_result:
    print(f'    PET estimate: {petpeese_result.get("PET", {}).get("estimate", "N/A")}')
    print(f'    PEESE estimate: {petpeese_result.get("PEESE", {}).get("estimate", "N/A")}')

# ============================================================
# SECTION 7: ADVANCED MODULE FUNCTIONS
# ============================================================
print('\n' + '='*70)
print('SECTION 7: ADVANCED MODULE FUNCTIONS')
print('='*70)

# Profile Likelihood
print('\n--- Profile Likelihood ---')
pl_result = driver.execute_script("""
    if (typeof ProfileLikelihood === 'undefined') return null;
    const tau2 = AppState.results?.heterogeneity?.tau2;
    const processed = AppState.results?.processed;
    if (!processed || tau2 === undefined) return null;
    try {
        return ProfileLikelihood.computeTau2CI(processed, tau2);
    } catch(e) {
        return {error: e.message};
    }
""")
test('ProfileLikelihood.computeTau2CI() works', pl_result is not None and 'error' not in (pl_result or {}))
if pl_result and 'error' not in pl_result:
    print(f'    Tau2 CI: [{pl_result.get("lower", "N/A"):.4f}, {pl_result.get("upper", "N/A"):.4f}]')

# GRADE-NMA
print('\n--- GRADE-NMA ---')
grade_result = driver.execute_script("""
    if (typeof GradeNMA === 'undefined') return null;
    const studies = AppState.studies;
    const results = AppState.results;
    if (!studies || !results) return null;
    try {
        return GradeNMA.assessCertainty('SK vs tPA', results, studies);
    } catch(e) {
        return {error: e.message};
    }
""")
test('GradeNMA.assessCertainty() works', grade_result is not None and 'error' not in (grade_result or {}))
if grade_result and 'error' not in grade_result:
    print(f'    Overall certainty: {grade_result.get("overall", "N/A")}')

# Node Splitting
print('\n--- Node Splitting ---')
ns_result = driver.execute_script("""
    if (typeof NodeSplittingTest === 'undefined') return null;
    const studies = AppState.studies;
    const effectMeasure = AppState.effectMeasure || 'OR';
    const reference = AppState.reference || 'SK';
    if (!studies) return null;
    try {
        return NodeSplittingTest.analyze(studies, effectMeasure, reference);
    } catch(e) {
        return {error: e.message};
    }
""")
test('NodeSplittingTest.analyze() works', ns_result is not None and 'error' not in (ns_result or {}))
if ns_result and 'error' not in ns_result:
    print(f'    Comparisons: {len(ns_result.get("comparisons", []))}')
    print(f'    Global p-value: {ns_result.get("globalTest", {}).get("pValue", "N/A")}')

# Leave One Out
print('\n--- Leave One Out ---')
loo_result = driver.execute_script("""
    if (typeof LeaveOneOut === 'undefined') return null;
    const processed = AppState.results?.processed;
    if (!processed) return null;
    try {
        return LeaveOneOut.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
test('LeaveOneOut.analyze() works', loo_result is not None and 'error' not in (loo_result or {}))
if loo_result and 'error' not in loo_result:
    print(f'    Leave-one-out iterations: {len(loo_result) if isinstance(loo_result, list) else "N/A"}')

# Influence Diagnostics
print('\n--- Influence Diagnostics ---')
inf_result = driver.execute_script("""
    if (typeof InfluenceDiagnostics === 'undefined') return null;
    const processed = AppState.results?.processed;
    if (!processed) return null;
    try {
        return InfluenceDiagnostics.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
test('InfluenceDiagnostics.analyze() works', inf_result is not None and 'error' not in (inf_result or {}))
if inf_result and 'error' not in inf_result:
    print(f'    Studies analyzed: {len(inf_result) if isinstance(inf_result, list) else "N/A"}')

# ============================================================
# SECTION 8: ALL DATASETS PLOT CHECK
# ============================================================
print('\n' + '='*70)
print('SECTION 8: PLOT CHECK FOR ALL DATASETS')
print('='*70)

for dataset in datasets:
    print(f'\n--- {dataset} plots ---')

    driver.execute_script(f"loadDemoDataset('{dataset}')")
    time.sleep(0.3)
    driver.execute_script("document.getElementById('runAnalysisBtn').click()")
    time.sleep(2)

    # Check all three plots
    plots_check = driver.execute_script("""
        const checkCanvas = (id) => {
            const canvas = document.getElementById(id);
            if (!canvas) return {exists: false};
            try {
                const ctx = canvas.getContext('2d');
                const data = ctx.getImageData(0, 0, Math.min(canvas.width, 100), Math.min(canvas.height, 100)).data;
                const hasContent = data.some(x => x !== 0);
                return {exists: true, width: canvas.width, height: canvas.height, hasContent};
            } catch(e) {
                return {exists: true, error: e.message};
            }
        };
        return {
            forest: checkCanvas('forestPlot'),
            funnel: checkCanvas('funnelPlot'),
            network: checkCanvas('networkGraph')
        };
    """)

    forest = plots_check.get('forest', {})
    funnel = plots_check.get('funnel', {})
    network = plots_check.get('network', {})

    test(f'{dataset}: Forest plot rendered', forest.get('hasContent', False))
    test(f'{dataset}: Funnel plot rendered', funnel.get('hasContent', False))
    test(f'{dataset}: Network graph rendered', network.get('hasContent', False))

# ============================================================
# FINAL JS ERROR CHECK
# ============================================================
print('\n' + '='*70)
print('FINAL ERROR CHECK')
print('='*70)

final_logs = driver.get_log('browser')
final_errors = [l for l in final_logs if l['level'] == 'SEVERE']
test('No JS errors after all tests', len(final_errors) == 0)
if final_errors:
    print(f'  Found {len(final_errors)} errors:')
    for e in final_errors[:5]:
        print(f'    {e["message"][:80]}')

driver.quit()

# ============================================================
# SUMMARY
# ============================================================
print('\n' + '='*70)
print('TEST SUMMARY')
print('='*70)
total = passed + failed
print(f'''
  PASSED:   {passed}/{total} ({100*passed/total:.1f}%)
  FAILED:   {failed}/{total}
  WARNINGS: {warnings}

  STATUS: {'ALL TESTS PASSED!' if failed == 0 else 'SOME TESTS FAILED'}
''')
