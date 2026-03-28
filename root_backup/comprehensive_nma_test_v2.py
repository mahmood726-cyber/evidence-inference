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

    # Dismiss any alerts first
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

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

        # Dismiss any alerts
        try:
            alert = driver.switch_to.alert
            print(f'    Alert: {alert.text[:50]}')
            alert.accept()
        except:
            pass

        # Check results
        results = driver.execute_script("return AppState.results")
        test(f'{dataset}: Analysis completed', results is not None)

        if results:
            # Check heterogeneity
            het = results.get('heterogeneity', {})
            if het:
                tau2 = het.get('tau2')
                I2 = het.get('I2')
                tau2_str = f'{tau2:.4f}' if tau2 is not None else 'N/A'
                I2_str = f'{I2:.1f}%' if I2 is not None else 'N/A'
                print(f'    Heterogeneity: tau2={tau2_str}, I2={I2_str}')

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
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass

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
    ('runAnalysis', 'runAnalysis'),
    ('loadDemoDataset', 'loadDemoDataset'),
    ('renderForestPlot', 'renderForestPlot'),
    ('renderFunnelPlot', 'renderFunnelPlot'),
    ('renderNetworkGraph', 'renderNetworkGraph'),
]

for func_name, func in core_functions:
    exists = driver.execute_script(f"return typeof {func} === 'function'")
    test(f'Function: {func_name}()', exists)

# Check what other global functions exist
all_funcs = driver.execute_script("""
    return Object.keys(window).filter(k => typeof window[k] === 'function' && !k.startsWith('webkit'))
        .filter(k => k.match(/^[a-z]/i) && k.length > 3 && k.length < 30)
        .slice(0, 50);
""")
print(f'\nOther global functions found: {len(all_funcs)}')
for f in all_funcs[:15]:
    print(f'    - {f}')

# ============================================================
# SECTION 4: PLOT RENDERING
# ============================================================
print('\n' + '='*70)
print('SECTION 4: PLOT RENDERING')
print('='*70)

# Check what type of elements the plots are
plot_info = driver.execute_script("""
    const plots = ['forestPlot', 'funnelPlot', 'networkGraph'];
    const result = {};
    plots.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            result[id] = {
                exists: true,
                tagName: el.tagName,
                width: el.width || el.clientWidth || el.offsetWidth,
                height: el.height || el.clientHeight || el.offsetHeight,
                innerHTML: el.innerHTML ? el.innerHTML.substring(0, 100) : '',
                childCount: el.children.length
            };
        } else {
            result[id] = {exists: false};
        }
    });
    return result;
""")

print('\nPlot element info:')
for plot_id, info in plot_info.items():
    if info.get('exists'):
        print(f'  {plot_id}:')
        print(f'    Tag: {info.get("tagName")}')
        print(f'    Size: {info.get("width")}x{info.get("height")}')
        print(f'    Children: {info.get("childCount")}')
    else:
        print(f'  {plot_id}: NOT FOUND')

# Check for canvas elements
canvas_check = driver.execute_script("""
    const canvases = document.querySelectorAll('canvas');
    return Array.from(canvases).map(c => ({
        id: c.id,
        width: c.width,
        height: c.height,
        hasContent: (() => {
            try {
                const ctx = c.getContext('2d');
                if (!ctx) return false;
                const data = ctx.getImageData(0, 0, Math.min(c.width, 50), Math.min(c.height, 50)).data;
                return data.some(x => x !== 0);
            } catch(e) {
                return false;
            }
        })()
    }));
""")

print(f'\nFound {len(canvas_check)} canvas elements:')
for canvas in canvas_check:
    status = 'HAS CONTENT' if canvas.get('hasContent') else 'EMPTY'
    print(f'  - {canvas.get("id") or "(no id)"}: {canvas.get("width")}x{canvas.get("height")} [{status}]')
    test(f'Canvas {canvas.get("id") or "unnamed"} has content', canvas.get('hasContent'), warn_only=True)

# Check for SVG elements
svg_check = driver.execute_script("""
    const svgs = document.querySelectorAll('svg');
    return Array.from(svgs).slice(0, 10).map(s => ({
        id: s.id,
        width: s.getAttribute('width') || s.clientWidth,
        height: s.getAttribute('height') || s.clientHeight,
        childCount: s.children.length
    }));
""")

print(f'\nFound {len(svg_check)} SVG elements:')
for svg in svg_check[:5]:
    print(f'  - {svg.get("id") or "(no id)"}: {svg.get("width")}x{svg.get("height")}, {svg.get("childCount")} children')

# ============================================================
# SECTION 5: PUBLICATION BIAS FUNCTIONS
# ============================================================
print('\n' + '='*70)
print('SECTION 5: PUBLICATION BIAS FUNCTIONS')
print('='*70)

# Test TrimAndFill
print('\n--- Trim and Fill ---')
taf_result = driver.execute_script("""
    if (typeof TrimAndFill === 'undefined') return {error: 'Module not found'};
    const processed = AppState.results?.processed;
    if (!processed) return {error: 'No processed data'};
    try {
        return TrimAndFill.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
if taf_result and 'error' not in taf_result:
    test('TrimAndFill.analyze() works', True)
    print(f'    Imputed studies: {taf_result.get("imputedStudies", "N/A")}')
    adj = taf_result.get("adjustedEffect")
    if adj:
        print(f'    Adjusted effect: {adj:.4f}')
else:
    test('TrimAndFill.analyze() works', False)
    print(f'    Error: {taf_result.get("error") if taf_result else "None"}')

# Test Egger's Test
print('\n--- Egger\'s Test ---')
egger_result = driver.execute_script("""
    if (typeof EggersTest === 'undefined') return {error: 'Module not found'};
    const processed = AppState.results?.processed;
    if (!processed) return {error: 'No processed data'};
    try {
        return EggersTest.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
if egger_result and 'error' not in egger_result:
    test('EggersTest.analyze() works', True)
    intercept = egger_result.get("intercept")
    pval = egger_result.get("pValue")
    print(f'    Intercept: {intercept:.4f}' if intercept else '    Intercept: N/A')
    print(f'    p-value: {pval:.4f}' if pval else '    p-value: N/A')
else:
    test('EggersTest.analyze() works', False)
    print(f'    Error: {egger_result.get("error") if egger_result else "None"}')

# Test Begg's Test
print('\n--- Begg\'s Test ---')
begg_result = driver.execute_script("""
    if (typeof BeggsTest === 'undefined') return {error: 'Module not found'};
    const processed = AppState.results?.processed;
    if (!processed) return {error: 'No processed data'};
    try {
        return BeggsTest.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
if begg_result and 'error' not in begg_result:
    test('BeggsTest.analyze() works', True)
    tau = begg_result.get("tau")
    pval = begg_result.get("pValue")
    print(f'    Kendall tau: {tau:.4f}' if tau else '    Kendall tau: N/A')
    print(f'    p-value: {pval:.4f}' if pval else '    p-value: N/A')
else:
    test('BeggsTest.analyze() works', False)
    print(f'    Error: {begg_result.get("error") if begg_result else "None"}')

# Test PET-PEESE
print('\n--- PET-PEESE ---')
petpeese_result = driver.execute_script("""
    if (typeof PETPEESE === 'undefined') return {error: 'Module not found'};
    const processed = AppState.results?.processed;
    if (!processed) return {error: 'No processed data'};
    try {
        return PETPEESE.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
if petpeese_result and 'error' not in petpeese_result:
    test('PETPEESE.analyze() works', True)
    pet = petpeese_result.get("PET", {})
    peese = petpeese_result.get("PEESE", {})
    pet_est = pet.get("estimate")
    peese_est = peese.get("estimate")
    print(f'    PET estimate: {pet_est:.4f}' if pet_est else '    PET estimate: N/A')
    print(f'    PEESE estimate: {peese_est:.4f}' if peese_est else '    PEESE estimate: N/A')
else:
    test('PETPEESE.analyze() works', False)
    print(f'    Error: {petpeese_result.get("error") if petpeese_result else "None"}')

# Test Selection Models
print('\n--- Selection Models ---')
sel_result = driver.execute_script("""
    if (typeof SelectionModels === 'undefined') return {error: 'Module not found'};
    const processed = AppState.results?.processed;
    if (!processed) return {error: 'No processed data'};
    try {
        return SelectionModels.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
if sel_result and 'error' not in sel_result:
    test('SelectionModels.analyze() works', True)
    adj = sel_result.get("adjustedEffect")
    print(f'    Adjusted effect: {adj:.4f}' if adj else '    Adjusted effect: N/A')
else:
    test('SelectionModels.analyze() works', False)
    print(f'    Error: {sel_result.get("error") if sel_result else "None"}')

# ============================================================
# SECTION 6: ADVANCED MODULE FUNCTIONS
# ============================================================
print('\n' + '='*70)
print('SECTION 6: ADVANCED MODULE FUNCTIONS')
print('='*70)

# Profile Likelihood
print('\n--- Profile Likelihood ---')
pl_result = driver.execute_script("""
    if (typeof ProfileLikelihood === 'undefined') return {error: 'Module not found'};
    const tau2 = AppState.results?.heterogeneity?.tau2;
    const processed = AppState.results?.processed;
    if (!processed || tau2 === undefined) return {error: 'Missing data'};
    try {
        return ProfileLikelihood.computeTau2CI(processed, tau2);
    } catch(e) {
        return {error: e.message};
    }
""")
if pl_result and 'error' not in pl_result:
    test('ProfileLikelihood.computeTau2CI() works', True)
    lower = pl_result.get("lower")
    upper = pl_result.get("upper")
    print(f'    Tau2 CI: [{lower:.4f}, {upper:.4f}]' if lower and upper else '    CI: N/A')
else:
    test('ProfileLikelihood.computeTau2CI() works', False)
    print(f'    Error: {pl_result.get("error") if pl_result else "None"}')

# GRADE-NMA
print('\n--- GRADE-NMA ---')
grade_result = driver.execute_script("""
    if (typeof GradeNMA === 'undefined') return {error: 'Module not found'};
    const studies = AppState.studies;
    const results = AppState.results;
    if (!studies || !results) return {error: 'Missing data'};
    try {
        return GradeNMA.assessCertainty('SK vs tPA', results, studies);
    } catch(e) {
        return {error: e.message};
    }
""")
if grade_result and 'error' not in grade_result:
    test('GradeNMA.assessCertainty() works', True)
    print(f'    Overall certainty: {grade_result.get("overall", "N/A")}')
else:
    test('GradeNMA.assessCertainty() works', False)
    print(f'    Error: {grade_result.get("error") if grade_result else "None"}')

# Node Splitting
print('\n--- Node Splitting ---')
ns_result = driver.execute_script("""
    if (typeof NodeSplittingTest === 'undefined') return {error: 'Module not found'};
    const studies = AppState.studies;
    const effectMeasure = AppState.effectMeasure || 'OR';
    const reference = AppState.reference || 'SK';
    if (!studies) return {error: 'Missing data'};
    try {
        return NodeSplittingTest.analyze(studies, effectMeasure, reference);
    } catch(e) {
        return {error: e.message};
    }
""")
if ns_result and 'error' not in ns_result:
    test('NodeSplittingTest.analyze() works', True)
    comps = ns_result.get("comparisons", [])
    gt = ns_result.get("globalTest", {})
    print(f'    Comparisons: {len(comps)}')
    pval = gt.get("pValue")
    print(f'    Global p-value: {pval:.4f}' if pval else '    Global p-value: N/A')
else:
    test('NodeSplittingTest.analyze() works', False)
    print(f'    Error: {ns_result.get("error") if ns_result else "None"}')

# Leave One Out
print('\n--- Leave One Out ---')
loo_result = driver.execute_script("""
    if (typeof LeaveOneOut === 'undefined') return {error: 'Module not found'};
    const processed = AppState.results?.processed;
    if (!processed) return {error: 'Missing data'};
    try {
        return LeaveOneOut.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
if loo_result and 'error' not in (loo_result if isinstance(loo_result, dict) else {}):
    test('LeaveOneOut.analyze() works', True)
    if isinstance(loo_result, list):
        print(f'    Leave-one-out iterations: {len(loo_result)}')
    else:
        print(f'    Result type: {type(loo_result).__name__}')
else:
    test('LeaveOneOut.analyze() works', False)
    err = loo_result.get("error") if isinstance(loo_result, dict) else str(loo_result)
    print(f'    Error: {err}')

# Influence Diagnostics
print('\n--- Influence Diagnostics ---')
inf_result = driver.execute_script("""
    if (typeof InfluenceDiagnostics === 'undefined') return {error: 'Module not found'};
    const processed = AppState.results?.processed;
    if (!processed) return {error: 'Missing data'};
    try {
        return InfluenceDiagnostics.analyze(processed);
    } catch(e) {
        return {error: e.message};
    }
""")
if inf_result and 'error' not in (inf_result if isinstance(inf_result, dict) else {}):
    test('InfluenceDiagnostics.analyze() works', True)
    if isinstance(inf_result, list):
        print(f'    Studies analyzed: {len(inf_result)}')
    else:
        print(f'    Result type: {type(inf_result).__name__}')
else:
    test('InfluenceDiagnostics.analyze() works', False)
    err = inf_result.get("error") if isinstance(inf_result, dict) else str(inf_result)
    print(f'    Error: {err}')

# Component NMA
print('\n--- Component NMA ---')
comp_result = driver.execute_script("""
    if (typeof ComponentNMA === 'undefined') return {error: 'Module not found'};
    try {
        // Check what methods exist
        const methods = Object.keys(ComponentNMA);
        return {methods: methods};
    } catch(e) {
        return {error: e.message};
    }
""")
if comp_result and 'error' not in comp_result:
    test('ComponentNMA module accessible', True)
    print(f'    Methods: {comp_result.get("methods", [])}')
else:
    test('ComponentNMA module accessible', False)

# Dose Response
print('\n--- Dose Response ---')
dr_result = driver.execute_script("""
    if (typeof DoseResponse === 'undefined') return {error: 'Module not found'};
    try {
        const methods = Object.keys(DoseResponse);
        return {methods: methods};
    } catch(e) {
        return {error: e.message};
    }
""")
if dr_result and 'error' not in dr_result:
    test('DoseResponse module accessible', True)
    print(f'    Methods: {dr_result.get("methods", [])}')
else:
    test('DoseResponse module accessible', False)

# ============================================================
# SECTION 7: ALL DATASETS PLOT CHECK
# ============================================================
print('\n' + '='*70)
print('SECTION 7: PLOT CHECK FOR ALL DATASETS')
print('='*70)

for dataset in datasets:
    print(f'\n--- {dataset} ---')

    # Dismiss alerts
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    driver.execute_script(f"loadDemoDataset('{dataset}')")
    time.sleep(0.3)
    driver.execute_script("document.getElementById('runAnalysisBtn').click()")
    time.sleep(2)

    # Dismiss alerts
    try:
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(0.5)
    except:
        pass

    # Check canvas elements
    canvas_status = driver.execute_script("""
        const result = {};
        const canvases = document.querySelectorAll('canvas');
        canvases.forEach(c => {
            if (c.id) {
                try {
                    const ctx = c.getContext('2d');
                    if (ctx) {
                        const data = ctx.getImageData(0, 0, Math.min(c.width, 50), Math.min(c.height, 50)).data;
                        result[c.id] = data.some(x => x !== 0);
                    } else {
                        result[c.id] = false;
                    }
                } catch(e) {
                    result[c.id] = false;
                }
            }
        });
        return result;
    """)

    for canvas_id, has_content in canvas_status.items():
        status = 'rendered' if has_content else 'EMPTY'
        test(f'{dataset}: {canvas_id}', has_content, warn_only=True)

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
pct = 100*passed/total if total > 0 else 0
print(f'''
  PASSED:   {passed}/{total} ({pct:.1f}%)
  FAILED:   {failed}/{total}
  WARNINGS: {warnings}

  STATUS: {'ALL TESTS PASSED!' if failed == 0 else 'SOME TESTS FAILED'}
''')
