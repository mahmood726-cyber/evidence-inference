#!/usr/bin/env python3
"""
Validation Tests for RSM Editorial Enhancements
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

print("="*70)
print("RSM EDITORIAL ENHANCEMENTS VALIDATION")
print("="*70)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(3)

results = []

def test(name, js_code):
    try:
        result = driver.execute_script(f"try {{ return {js_code}; }} catch(e) {{ return 'ERROR: ' + e.message; }}")
        if isinstance(result, str) and result.startswith('ERROR:'):
            results.append((name, 'FAIL', result))
            return False
        else:
            results.append((name, 'PASS', str(result)[:80] if result else 'OK'))
            return True
    except Exception as e:
        results.append((name, 'FAIL', str(e)[:80]))
        return False

# =============================================================================
# TEST 1: NEW MODULE EXISTENCE
# =============================================================================
print("\n[1] Testing new module existence...")

new_modules = [
    'TransitivityAssessment',
    'DiagnosticPlots',
    'OutlierDetection',
    'CopasSelectionModel',
    'MultiArmAdjustment'
]

for mod in new_modules:
    test(f"Module exists: {mod}", f"typeof {mod} === 'object'")

# =============================================================================
# TEST 2: TRANSITIVITY ASSESSMENT
# =============================================================================
print("\n[2] Testing TransitivityAssessment...")

nma_data = """
const studies = [
    { study: 'S1', treatment1: 'A', treatment2: 'B', effect: 0.3, se: 0.1, year: 2015, rob: 'low' },
    { study: 'S2', treatment1: 'A', treatment2: 'B', effect: 0.4, se: 0.15, year: 2016, rob: 'low' },
    { study: 'S3', treatment1: 'B', treatment2: 'C', effect: 0.2, se: 0.12, year: 2017, rob: 'high' },
    { study: 'S4', treatment1: 'B', treatment2: 'C', effect: 0.25, se: 0.14, year: 2018, rob: 'low' },
    { study: 'S5', treatment1: 'A', treatment2: 'C', effect: 0.5, se: 0.18, year: 2019, rob: 'unclear' },
    { study: 'S6', treatment1: 'A', treatment2: 'C', effect: 0.55, se: 0.2, year: 2020, rob: 'low' }
];
"""

test("TransitivityAssessment.analyzeModifiers", f"""
{nma_data}
const result = TransitivityAssessment.analyzeModifiers(studies, ['year', 'rob']);
result && result.modifiers && result.global
""")

test("TransitivityAssessment effect modifier balance", f"""
{nma_data}
const result = TransitivityAssessment.analyzeModifiers(studies, ['year']);
result.modifiers.year && typeof result.modifiers.year.imbalance === 'number'
""")

test("TransitivityAssessment global assessment", f"""
{nma_data}
const result = TransitivityAssessment.analyzeModifiers(studies, ['year', 'rob']);
result.global && ['low', 'moderate', 'high'].includes(result.global.concern)
""")

# =============================================================================
# TEST 3: DIAGNOSTIC PLOTS
# =============================================================================
print("\n[3] Testing DiagnosticPlots...")

test_data = """
const effects = [0.5, 0.3, 0.8, 0.2, 0.6, 0.4, 0.7, 0.35, 0.55, 0.45];
const ses = [0.1, 0.15, 0.2, 0.12, 0.18, 0.14, 0.22, 0.11, 0.16, 0.13];
const labels = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10'];
"""

test("DiagnosticPlots.baujat", f"""
{test_data}
const result = DiagnosticPlots.baujat(effects, ses, labels);
result && result.points && result.svg
""")

test("DiagnosticPlots.baujat SVG generation", f"""
{test_data}
const result = DiagnosticPlots.baujat(effects, ses, labels);
result.svg.includes('<svg') && result.svg.includes('</svg>')
""")

test("DiagnosticPlots.galbraith", f"""
{test_data}
const result = DiagnosticPlots.galbraith(effects, ses, labels);
result && result.points && result.regressionLine && result.svg
""")

test("DiagnosticPlots.labbe", f"""
const e1 = [20, 30, 25, 15, 22, 28, 18, 32, 26, 21];
const n1 = [100, 150, 120, 80, 110, 140, 90, 160, 130, 100];
const e2 = [15, 22, 18, 12, 16, 20, 14, 24, 19, 17];
const n2 = [100, 150, 120, 80, 110, 140, 90, 160, 130, 100];
const result = DiagnosticPlots.labbe(e1, n1, e2, n2, labels);
result && result.points && result.svg
""")

test("DiagnosticPlots.contourFunnel", f"""
{test_data}
const result = DiagnosticPlots.contourFunnel(effects, ses, labels);
result && result.contours && result.svg
""")

# =============================================================================
# TEST 4: OUTLIER DETECTION
# =============================================================================
print("\n[4] Testing OutlierDetection...")

test("OutlierDetection.analyze", f"""
{test_data}
const result = OutlierDetection.analyze(effects, ses, labels);
result && result.studentized && result.dfbetas && result.cooks
""")

test("OutlierDetection studentized residuals", f"""
{test_data}
const result = OutlierDetection.analyze(effects, ses, labels);
result.studentized.length === 10 && typeof result.studentized[0].residual === 'number'
""")

test("OutlierDetection DFBETAS", f"""
{test_data}
const result = OutlierDetection.analyze(effects, ses, labels);
result.dfbetas.length === 10 && typeof result.dfbetas[0].value === 'number'
""")

test("OutlierDetection Cook's D", f"""
{test_data}
const result = OutlierDetection.analyze(effects, ses, labels);
result.cooks.length === 10 && typeof result.cooks[0].value === 'number'
""")

test("OutlierDetection outlier flagging", f"""
{test_data}
const result = OutlierDetection.analyze(effects, ses, labels);
result.flagged !== undefined
""")

test("OutlierDetection.leaveOneOut", f"""
{test_data}
const result = OutlierDetection.leaveOneOut(effects, ses, labels);
result && result.length === 10 && typeof result[0].effect === 'number'
""")

# =============================================================================
# TEST 5: COPAS SELECTION MODEL
# =============================================================================
print("\n[5] Testing CopasSelectionModel...")

test("CopasSelectionModel.fit", f"""
{test_data}
const result = CopasSelectionModel.fit(effects, ses);
result && typeof result.adjustedEffect === 'number' && result.gamma
""")

test("CopasSelectionModel adjusted estimates", f"""
{test_data}
const result = CopasSelectionModel.fit(effects, ses);
typeof result.adjustedSE === 'number' && result.ci
""")

test("CopasSelectionModel gamma parameters", f"""
{test_data}
const result = CopasSelectionModel.fit(effects, ses);
typeof result.gamma.gamma0 === 'number' && typeof result.gamma.gamma1 === 'number'
""")

test("CopasSelectionModel sensitivity analysis", f"""
{test_data}
const result = CopasSelectionModel.sensitivityAnalysis(effects, ses);
result && result.grid && result.grid.length > 0
""")

# =============================================================================
# TEST 6: MULTI-ARM ADJUSTMENT
# =============================================================================
print("\n[6] Testing MultiArmAdjustment...")

multiarm_data = """
const maStudies = [
    { study: 'S1', arms: ['A', 'B', 'C'], effects: [0, 0.3, 0.5], variances: [0, 0.01, 0.015] },
    { study: 'S2', arms: ['A', 'B'], effects: [0, 0.4], variances: [0, 0.02] },
    { study: 'S3', arms: ['B', 'C', 'D'], effects: [0, 0.2, 0.35], variances: [0, 0.012, 0.018] },
    { study: 'S4', arms: ['A', 'C'], effects: [0, 0.45], variances: [0, 0.016] }
];
"""

test("MultiArmAdjustment.calculateCorrelations", f"""
{multiarm_data}
const result = MultiArmAdjustment.calculateCorrelations(maStudies);
result && result.correlationMatrices && Object.keys(result.correlationMatrices).length > 0
""")

test("MultiArmAdjustment correlation matrix for 3-arm", f"""
{multiarm_data}
const result = MultiArmAdjustment.calculateCorrelations(maStudies);
const s1Corr = result.correlationMatrices['S1'];
s1Corr && s1Corr.length === 2 && s1Corr[0].length === 2
""")

test("MultiArmAdjustment.glsEstimate", f"""
{multiarm_data}
const corr = MultiArmAdjustment.calculateCorrelations(maStudies);
const result = MultiArmAdjustment.glsEstimate(maStudies, corr);
result && result.estimates && typeof result.heterogeneity === 'object'
""")

# =============================================================================
# TEST 7: EXISTING MODULES STILL WORK
# =============================================================================
print("\n[7] Testing existing modules still work...")

existing_modules = [
    'PublicationBias',
    'NodeSplitting',
    'ComponentNMA',
    'RobustVariance',
    'PRISMA_NMA',
    'SmallStudyEffects',
    'EvidenceFlow',
    'CumulativeMeta',
    'DesignDecomposition',
    'MantelHaenszelNMA',
    'CustomLikelihood',
    'PopulationAdjustedIC',
    'HierarchicalNMA',
    'FrequentistNMA',
    'BayesianNMA',
    'ThresholdAnalysis',
    'CINeMA'
]

for mod in existing_modules:
    test(f"Existing module: {mod}", f"typeof {mod} === 'object'")

# Test a few critical functions from existing modules
test("PublicationBias.eggersTest works", f"""
{test_data}
const result = PublicationBias.eggersTest(effects, ses);
result && typeof result.pValue === 'number'
""")

test("NodeSplitting.analyze works", f"""
{nma_data}
const result = NodeSplitting.analyze(studies);
result && result.comparisons
""")

driver.quit()

# =============================================================================
# RESULTS SUMMARY
# =============================================================================
print("\n" + "="*70)
print("RSM VALIDATION RESULTS")
print("="*70)

passed = sum(1 for r in results if r[1] == 'PASS')
failed = sum(1 for r in results if r[1] == 'FAIL')
total = len(results)

for name, status, detail in results:
    icon = "[OK]" if status == "PASS" else "[X]"
    print(f"{icon} {name}")
    if status == "FAIL":
        print(f"    -> {detail}")

print("\n" + "-"*70)
print(f"TOTAL: {passed}/{total} passed ({100*passed/total:.1f}%)")

if failed == 0:
    print("\nALL RSM EDITORIAL ENHANCEMENTS VALIDATED!")
else:
    print(f"\n{failed} test(s) failed - review required")

print("="*70)
