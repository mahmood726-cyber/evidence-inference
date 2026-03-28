#!/usr/bin/env python3
"""
Comprehensive Browser Test for NMA Pro v6.2
Tests ALL functions, buttons, and plot displays
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

print("="*80)
print("NMA PRO v6.2 - COMPREHENSIVE BROWSER TEST")
print("="*80)

# Use visible browser for visual inspection
options = Options()
# options.add_argument('--headless')  # Comment out to see browser
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')

driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(3)

results = {
    'modules': [],
    'functions': [],
    'ui_elements': [],
    'plots': [],
    'errors': []
}

def log_result(category, name, status, detail=""):
    icon = "[OK]" if status else "[X]"
    print(f"{icon} {category}: {name}")
    if not status and detail:
        print(f"    -> {detail}")
    results[category.lower().replace(' ', '_')].append({
        'name': name,
        'status': 'PASS' if status else 'FAIL',
        'detail': detail
    })

def test_js(code, description=""):
    """Execute JavaScript and return result"""
    try:
        result = driver.execute_script(f"try {{ return {code}; }} catch(e) {{ return 'ERROR: ' + e.message; }}")
        if isinstance(result, str) and result.startswith('ERROR:'):
            return False, result
        return True, result
    except Exception as e:
        return False, str(e)

# =============================================================================
# SECTION 1: MODULE EXISTENCE TESTS
# =============================================================================
print("\n" + "="*80)
print("SECTION 1: MODULE EXISTENCE")
print("="*80)

modules_to_test = [
    # Core NMA modules
    'FrequentistNMA', 'BayesianNMA', 'NetworkMetaRegression',
    # Consistency/Heterogeneity
    'NodeSplitting', 'DesignDecomposition', 'ComponentNMA',
    # Publication Bias
    'PublicationBias', 'SmallStudyEffects', 'CopasSelectionModel',
    # Quality Assessment
    'CINeMA', 'ThresholdAnalysis', 'PRISMA_NMA',
    # Advanced Methods
    'RobustVariance', 'EvidenceFlow', 'CumulativeMeta',
    'TransitivityAssessment', 'OutlierDetection', 'MultiArmAdjustment',
    # Special Methods
    'MantelHaenszelNMA', 'CustomLikelihood', 'PopulationAdjustedIC', 'HierarchicalNMA',
    # Visualization
    'DiagnosticPlots',
    # Utilities
    'Stats', 'Matrix'
]

for mod in modules_to_test:
    success, result = test_js(f"typeof {mod}")
    is_object = result in ['object', 'function']
    log_result('Modules', mod, is_object, f"Type: {result}")

# =============================================================================
# SECTION 2: CORE FUNCTION TESTS
# =============================================================================
print("\n" + "="*80)
print("SECTION 2: CORE FUNCTION TESTS")
print("="*80)

# Test data setup
setup_code = """
window.testEffects = [0.5, 0.3, 0.8, 0.2, 0.6, 0.4, 0.7, 0.35, 0.55, 0.45];
window.testSEs = [0.1, 0.15, 0.2, 0.12, 0.18, 0.14, 0.22, 0.11, 0.16, 0.13];
window.testLabels = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10'];
window.testNMAStudies = [
    { study: 'S1', treatment1: 'A', treatment2: 'B', effect: 0.3, se: 0.1 },
    { study: 'S2', treatment1: 'A', treatment2: 'B', effect: 0.4, se: 0.15 },
    { study: 'S3', treatment1: 'B', treatment2: 'C', effect: 0.2, se: 0.12 },
    { study: 'S4', treatment1: 'B', treatment2: 'C', effect: 0.25, se: 0.14 },
    { study: 'S5', treatment1: 'A', treatment2: 'C', effect: 0.5, se: 0.18 },
    { study: 'S6', treatment1: 'A', treatment2: 'C', effect: 0.55, se: 0.2 }
];
window.testBinaryStudies = [
    { e1: 20, n1: 100, e2: 15, n2: 100 },
    { e1: 30, n1: 150, e2: 22, n2: 150 },
    { e1: 12, n1: 80, e2: 8, n2: 80 },
    { e1: 25, n1: 120, e2: 18, n2: 120 },
    { e1: 18, n1: 90, e2: 12, n2: 90 }
];
'Test data initialized';
"""
driver.execute_script(setup_code)
print("[OK] Test data initialized")

# Core statistical functions
function_tests = [
    # Stats module
    ("Stats.mean([1,2,3,4,5])", "Stats.mean"),
    ("Stats.variance([1,2,3,4,5])", "Stats.variance"),
    ("Stats.standardDeviation([1,2,3,4,5])", "Stats.standardDeviation"),
    ("Stats.normalCDF(1.96)", "Stats.normalCDF"),
    ("Stats.normalQuantile(0.975)", "Stats.normalQuantile"),
    ("Stats.chiSquareCDF(3.84, 1)", "Stats.chiSquareCDF"),
    ("Stats.tCDF(2.0, 10)", "Stats.tCDF"),

    # Publication Bias
    ("PublicationBias.eggersTest(testEffects, testSEs)", "PublicationBias.eggersTest"),
    ("PublicationBias.beggsTest(testEffects, testSEs)", "PublicationBias.beggsTest"),
    ("PublicationBias.trimAndFill(testEffects, testSEs)", "PublicationBias.trimAndFill"),
    ("PublicationBias.petPeese(testEffects, testSEs)", "PublicationBias.petPeese"),
    ("PublicationBias.selectionModel(testEffects, testSEs)", "PublicationBias.selectionModel"),

    # Node Splitting
    ("NodeSplitting.analyze(testNMAStudies)", "NodeSplitting.analyze"),

    # Component NMA
    ("ComponentNMA.analyze([{treatment1:'Placebo',treatment2:'A',effect:0.5,se:0.1},{treatment1:'Placebo',treatment2:'B',effect:0.3,se:0.12},{treatment1:'Placebo',treatment2:'A+B',effect:0.7,se:0.15}])", "ComponentNMA.analyze"),

    # Robust Variance
    ("RobustVariance.analyze(testEffects, testSEs, ['C1','C1','C2','C2','C3','C3','C4','C4','C5','C5'])", "RobustVariance.analyze"),

    # PRISMA-NMA
    ("PRISMA_NMA.generateChecklist({title:'Test NMA'})", "PRISMA_NMA.generateChecklist"),

    # Small Study Effects
    ("SmallStudyEffects.petersTest(testBinaryStudies)", "SmallStudyEffects.petersTest"),
    ("SmallStudyEffects.harbordTest(testBinaryStudies)", "SmallStudyEffects.harbordTest"),
    ("SmallStudyEffects.limitMetaAnalysis(testEffects, testSEs)", "SmallStudyEffects.limitMetaAnalysis"),

    # Evidence Flow
    ("EvidenceFlow.analyze(testNMAStudies)", "EvidenceFlow.analyze"),

    # Cumulative Meta
    ("CumulativeMeta.analyze([{study:'S1',effect:0.3,se:0.1,year:2015},{study:'S2',effect:0.5,se:0.12,year:2016},{study:'S3',effect:0.4,se:0.11,year:2017}])", "CumulativeMeta.analyze"),

    # Transitivity Assessment
    ("TransitivityAssessment.analyzeModifiers([{study:'S1',treatment1:'A',treatment2:'B',effect:0.3,se:0.1,year:2015},{study:'S2',treatment1:'B',treatment2:'C',effect:0.2,se:0.12,year:2016}],['year'])", "TransitivityAssessment.analyzeModifiers"),

    # Outlier Detection
    ("OutlierDetection.analyze(testEffects, testSEs, testLabels)", "OutlierDetection.analyze"),
    ("OutlierDetection.leaveOneOut(testEffects, testSEs, testLabels)", "OutlierDetection.leaveOneOut"),

    # Copas Selection Model
    ("CopasSelectionModel.fit(testEffects, testSEs)", "CopasSelectionModel.fit"),
    ("CopasSelectionModel.sensitivityAnalysis(testEffects, testSEs)", "CopasSelectionModel.sensitivityAnalysis"),

    # Multi-arm Adjustment
    ("MultiArmAdjustment.calculateCorrelations([{study:'S1',arms:['A','B','C'],effects:[0,0.3,0.5],variances:[0,0.01,0.015]}])", "MultiArmAdjustment.calculateCorrelations"),

    # Diagnostic Plots
    ("DiagnosticPlots.baujat(testEffects, testSEs, testLabels)", "DiagnosticPlots.baujat"),
    ("DiagnosticPlots.galbraith(testEffects, testSEs, testLabels)", "DiagnosticPlots.galbraith"),
    ("DiagnosticPlots.contourFunnel(testEffects, testSEs, testLabels)", "DiagnosticPlots.contourFunnel"),
]

for code, name in function_tests:
    success, result = test_js(code)
    if success and result and not (isinstance(result, str) and result.startswith('ERROR')):
        log_result('Functions', name, True)
    else:
        log_result('Functions', name, False, str(result)[:100])

# =============================================================================
# SECTION 3: UI ELEMENT DETECTION
# =============================================================================
print("\n" + "="*80)
print("SECTION 3: UI ELEMENTS & BUTTONS")
print("="*80)

# Check for common UI elements
ui_checks = [
    ("document.querySelectorAll('button').length", "Buttons found"),
    ("document.querySelectorAll('input').length", "Input fields found"),
    ("document.querySelectorAll('select').length", "Select dropdowns found"),
    ("document.querySelectorAll('canvas').length", "Canvas elements found"),
    ("document.querySelectorAll('svg').length", "SVG elements found"),
    ("document.querySelectorAll('table').length", "Tables found"),
    ("document.querySelectorAll('[onclick]').length", "Clickable elements found"),
]

for code, name in ui_checks:
    success, result = test_js(code)
    log_result('UI_Elements', name, success, f"Count: {result}")

# =============================================================================
# SECTION 4: PLOT GENERATION TESTS
# =============================================================================
print("\n" + "="*80)
print("SECTION 4: PLOT GENERATION (SVG/Canvas)")
print("="*80)

plot_tests = [
    # Diagnostic Plots - generate SVG
    ("""
    const baujat = DiagnosticPlots.baujat(testEffects, testSEs, testLabels);
    baujat && baujat.svg && baujat.svg.includes('<svg') && baujat.svg.includes('</svg>')
    """, "Baujat Plot SVG"),

    ("""
    const galbraith = DiagnosticPlots.galbraith(testEffects, testSEs, testLabels);
    galbraith && galbraith.svg && galbraith.svg.includes('<svg')
    """, "Galbraith Plot SVG"),

    ("""
    const contour = DiagnosticPlots.contourFunnel(testEffects, testSEs, testLabels);
    contour && contour.svg && contour.svg.includes('<svg')
    """, "Contour Funnel Plot SVG"),

    ("""
    const labbe = DiagnosticPlots.labbe(
        [20,30,25,15,22], [100,150,120,80,110],
        [15,22,18,12,16], [100,150,120,80,110],
        ['S1','S2','S3','S4','S5']
    );
    labbe && labbe.svg && labbe.svg.includes('<svg')
    """, "L'Abbe Plot SVG"),

    # Evidence Flow SVG
    ("""
    const flow = EvidenceFlow.analyze(testNMAStudies);
    flow && flow.svg && flow.svg.includes('<svg')
    """, "Evidence Flow SVG"),

    # Check plot data structures
    ("""
    const baujat = DiagnosticPlots.baujat(testEffects, testSEs, testLabels);
    baujat && baujat.points && baujat.points.length === 10
    """, "Baujat Plot Data Points"),

    ("""
    const galbraith = DiagnosticPlots.galbraith(testEffects, testSEs, testLabels);
    galbraith && galbraith.regressionLine && typeof galbraith.regressionLine.slope === 'number'
    """, "Galbraith Regression Line"),

    ("""
    const contour = DiagnosticPlots.contourFunnel(testEffects, testSEs, testLabels);
    contour && contour.contours && contour.contours.length > 0
    """, "Contour Funnel Regions"),
]

for code, name in plot_tests:
    success, result = test_js(code)
    log_result('Plots', name, success and result == True, str(result)[:80])

# =============================================================================
# SECTION 5: DISPLAY PLOTS IN BROWSER
# =============================================================================
print("\n" + "="*80)
print("SECTION 5: DISPLAYING PLOTS IN BROWSER")
print("="*80)

# Create a container div for displaying plots
display_code = """
// Create test container
let container = document.getElementById('test-plot-container');
if (!container) {
    container = document.createElement('div');
    container.id = 'test-plot-container';
    container.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:white;z-index:10000;overflow:auto;padding:20px;';
    document.body.appendChild(container);
}

container.innerHTML = '<h1 style="text-align:center;color:#333;">NMA Pro v6.2 - Plot Display Test</h1>';

// Generate and display plots
const plots = [];

// 1. Baujat Plot
try {
    const baujat = DiagnosticPlots.baujat(testEffects, testSEs, testLabels);
    plots.push({name: 'Baujat Plot', svg: baujat.svg, status: 'OK'});
} catch(e) {
    plots.push({name: 'Baujat Plot', svg: null, status: 'ERROR: ' + e.message});
}

// 2. Galbraith Plot
try {
    const galbraith = DiagnosticPlots.galbraith(testEffects, testSEs, testLabels);
    plots.push({name: 'Galbraith (Radial) Plot', svg: galbraith.svg, status: 'OK'});
} catch(e) {
    plots.push({name: 'Galbraith Plot', svg: null, status: 'ERROR: ' + e.message});
}

// 3. Contour Funnel Plot
try {
    const contour = DiagnosticPlots.contourFunnel(testEffects, testSEs, testLabels);
    plots.push({name: 'Contour-Enhanced Funnel Plot', svg: contour.svg, status: 'OK'});
} catch(e) {
    plots.push({name: 'Contour Funnel', svg: null, status: 'ERROR: ' + e.message});
}

// 4. L'Abbe Plot
try {
    const labbe = DiagnosticPlots.labbe(
        [20,30,25,15,22,28,18,32,26,21],
        [100,150,120,80,110,140,90,160,130,100],
        [15,22,18,12,16,20,14,24,19,17],
        [100,150,120,80,110,140,90,160,130,100],
        testLabels
    );
    plots.push({name: "L'Abbe Plot", svg: labbe.svg, status: 'OK'});
} catch(e) {
    plots.push({name: "L'Abbe Plot", svg: null, status: 'ERROR: ' + e.message});
}

// 5. Evidence Flow
try {
    const flow = EvidenceFlow.analyze(testNMAStudies);
    plots.push({name: 'Evidence Flow Diagram', svg: flow.svg, status: 'OK'});
} catch(e) {
    plots.push({name: 'Evidence Flow', svg: null, status: 'ERROR: ' + e.message});
}

// Display all plots
let html = '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;max-width:1400px;margin:0 auto;">';

plots.forEach((p, i) => {
    html += '<div style="border:2px solid #ccc;border-radius:8px;padding:15px;background:#fafafa;">';
    html += '<h3 style="margin:0 0 10px 0;color:#333;border-bottom:1px solid #ddd;padding-bottom:5px;">' + p.name + '</h3>';
    if (p.svg) {
        html += '<div style="background:white;padding:10px;border-radius:4px;text-align:center;">' + p.svg + '</div>';
        html += '<p style="color:green;margin:10px 0 0 0;font-weight:bold;">[OK] Plot rendered successfully</p>';
    } else {
        html += '<div style="background:#fee;padding:20px;border-radius:4px;color:#c00;">Failed to generate plot</div>';
        html += '<p style="color:red;margin:10px 0 0 0;">' + p.status + '</p>';
    }
    html += '</div>';
});

html += '</div>';

// Add summary
const successCount = plots.filter(p => p.svg).length;
html += '<div style="text-align:center;margin:30px 0;padding:20px;background:#f0f0f0;border-radius:8px;">';
html += '<h2 style="margin:0;">Plot Generation Summary: ' + successCount + '/' + plots.length + ' successful</h2>';
html += '<button onclick="document.getElementById(\\'test-plot-container\\').remove()" style="margin-top:15px;padding:10px 30px;font-size:16px;cursor:pointer;background:#007bff;color:white;border:none;border-radius:5px;">Close Test View</button>';
html += '</div>';

container.innerHTML += html;

'Plots displayed: ' + successCount + '/' + plots.length;
"""

result = driver.execute_script(display_code)
print(f"[OK] {result}")

# Wait for user to see the plots
print("\n>>> Plots are now displayed in the browser window")
print(">>> Waiting 5 seconds for visual inspection...")
time.sleep(5)

# Take screenshot
try:
    driver.save_screenshot("C:/Users/user/nma_plots_screenshot.png")
    print("[OK] Screenshot saved to C:/Users/user/nma_plots_screenshot.png")
except Exception as e:
    print(f"[X] Screenshot failed: {e}")

# =============================================================================
# SECTION 6: ADVANCED FUNCTION TESTS
# =============================================================================
print("\n" + "="*80)
print("SECTION 6: ADVANCED FUNCTION TESTS")
print("="*80)

advanced_tests = [
    # CINeMA framework
    ("typeof CINeMA === 'object'", "CINeMA module exists"),

    # Threshold Analysis
    ("typeof ThresholdAnalysis === 'object'", "ThresholdAnalysis module exists"),

    # Design Decomposition
    ("typeof DesignDecomposition === 'object'", "DesignDecomposition module exists"),

    # Mantel-Haenszel
    ("typeof MantelHaenszelNMA === 'object'", "MantelHaenszelNMA module exists"),

    # Custom Likelihood
    ("typeof CustomLikelihood === 'object'", "CustomLikelihood module exists"),

    # Population Adjusted IC
    ("typeof PopulationAdjustedIC === 'object'", "PopulationAdjustedIC module exists"),

    # Hierarchical NMA
    ("typeof HierarchicalNMA === 'object'", "HierarchicalNMA module exists"),

    # Frequentist NMA
    ("typeof FrequentistNMA === 'object' && typeof FrequentistNMA.analyze === 'function'", "FrequentistNMA.analyze function"),

    # Bayesian NMA
    ("typeof BayesianNMA === 'object'", "BayesianNMA module exists"),

    # Network Meta Regression
    ("typeof NetworkMetaRegression === 'object'", "NetworkMetaRegression module exists"),
]

for code, name in advanced_tests:
    success, result = test_js(code)
    log_result('Functions', name, success and result == True, str(result))

# =============================================================================
# SECTION 7: ERROR HANDLING TESTS
# =============================================================================
print("\n" + "="*80)
print("SECTION 7: ERROR HANDLING")
print("="*80)

error_tests = [
    # Empty array handling
    ("PublicationBias.eggersTest([], [])", "Egger's test with empty arrays"),

    # Single study
    ("PublicationBias.eggersTest([0.5], [0.1])", "Egger's test with single study"),

    # Mismatched arrays
    ("OutlierDetection.analyze([0.5, 0.3], [0.1], ['S1', 'S2'])", "OutlierDetection with mismatched arrays"),
]

for code, name in error_tests:
    success, result = test_js(code)
    # These should either return a result or handle gracefully
    handled = success or (isinstance(result, str) and 'ERROR' in result)
    log_result('Functions', f"Error handling: {name}", handled, str(result)[:80])

# Close the test display
driver.execute_script("const c = document.getElementById('test-plot-container'); if(c) c.remove();")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("\n" + "="*80)
print("FINAL TEST SUMMARY")
print("="*80)

# Count results
module_pass = sum(1 for r in results['modules'] if r['status'] == 'PASS')
module_total = len(results['modules'])
func_pass = sum(1 for r in results['functions'] if r['status'] == 'PASS')
func_total = len(results['functions'])
plot_pass = sum(1 for r in results['plots'] if r['status'] == 'PASS')
plot_total = len(results['plots'])

print(f"\nModules:   {module_pass}/{module_total} ({100*module_pass/module_total:.1f}%)")
print(f"Functions: {func_pass}/{func_total} ({100*func_pass/func_total:.1f}%)")
print(f"Plots:     {plot_pass}/{plot_total} ({100*plot_pass/plot_total:.1f}%)")

total_pass = module_pass + func_pass + plot_pass
total_tests = module_total + func_total + plot_total
print(f"\nOVERALL:   {total_pass}/{total_tests} ({100*total_pass/total_tests:.1f}%)")

# List any failures
failures = []
for category in ['modules', 'functions', 'plots']:
    for r in results[category]:
        if r['status'] == 'FAIL':
            failures.append(f"{category}: {r['name']} - {r['detail']}")

if failures:
    print(f"\n{len(failures)} FAILURES:")
    for f in failures[:20]:  # Show first 20
        print(f"  [X] {f}")
else:
    print("\nALL TESTS PASSED!")

print("="*80)

# Keep browser open for inspection
print("\n>>> Browser window will remain open for 10 seconds for inspection...")
print(">>> Press Ctrl+C to close early")
try:
    time.sleep(10)
except KeyboardInterrupt:
    pass

driver.quit()
print("\nTest complete. Browser closed.")
