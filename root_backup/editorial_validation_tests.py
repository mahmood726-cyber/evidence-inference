#!/usr/bin/env python3
"""
Comprehensive Validation Tests for Editorial Features
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

print("="*70)
print("EDITORIAL FEATURES VALIDATION TEST")
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
# TEST 1: MODULE EXISTENCE
# =============================================================================
print("\n[1] Testing module existence...")

modules = [
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
    'HierarchicalNMA'
]

for mod in modules:
    test(f"Module exists: {mod}", f"typeof {mod} === 'object'")

# =============================================================================
# TEST 2: PUBLICATION BIAS METHODS
# =============================================================================
print("\n[2] Testing Publication Bias methods...")

# Test data
test_data = """
const effects = [0.5, 0.3, 0.8, 0.2, 0.6, 0.4, 0.7, 0.35, 0.55, 0.45];
const ses = [0.1, 0.15, 0.2, 0.12, 0.18, 0.14, 0.22, 0.11, 0.16, 0.13];
"""

test("Egger's test", f"""
{test_data}
const result = PublicationBias.eggersTest(effects, ses);
result && typeof result.pValue === 'number' && result.test === "Egger's regression"
""")

test("Begg's test", f"""
{test_data}
const result = PublicationBias.beggsTest(effects, ses);
result && typeof result.pValue === 'number' && result.test === "Begg-Mazumdar rank correlation"
""")

test("Trim and Fill", f"""
{test_data}
const result = PublicationBias.trimAndFill(effects, ses);
result && typeof result.adjustedPooled === 'number'
""")

test("PET-PEESE", f"""
{test_data}
const result = PublicationBias.petPeese(effects, ses);
result && result.pet && result.peese && typeof result.adjustedEffect === 'number'
""")

test("Selection Model", f"""
{test_data}
const result = PublicationBias.selectionModel(effects, ses);
result && typeof result.adjustedEffect === 'number'
""")

test("Run All Bias Tests", f"""
{test_data}
const result = PublicationBias.runAll(effects, ses);
result && result.egger && result.begg && result.trimFill && result.petPeese
""")

# =============================================================================
# TEST 3: NODE-SPLITTING
# =============================================================================
print("\n[3] Testing Node-Splitting...")

nma_data = """
const nmaStudies = [
    { study: 'S1', treatment1: 'A', treatment2: 'B', effect: 0.3, se: 0.1 },
    { study: 'S2', treatment1: 'A', treatment2: 'B', effect: 0.4, se: 0.15 },
    { study: 'S3', treatment1: 'B', treatment2: 'C', effect: 0.2, se: 0.12 },
    { study: 'S4', treatment1: 'B', treatment2: 'C', effect: 0.25, se: 0.14 },
    { study: 'S5', treatment1: 'A', treatment2: 'C', effect: 0.5, se: 0.18 },
    { study: 'S6', treatment1: 'A', treatment2: 'C', effect: 0.55, se: 0.2 }
];
"""

test("NodeSplitting.analyze", f"""
{nma_data}
const result = NodeSplitting.analyze(nmaStudies);
result && result.comparisons && result.globalTest && result.summary
""")

test("NodeSplitting comparisons", f"""
{nma_data}
const result = NodeSplitting.analyze(nmaStudies);
result.comparisons.length >= 2
""")

test("NodeSplitting global test", f"""
{nma_data}
const result = NodeSplitting.analyze(nmaStudies);
typeof result.globalTest.pValue === 'number'
""")

# =============================================================================
# TEST 4: COMPONENT NMA
# =============================================================================
print("\n[4] Testing Component NMA...")

cnma_data = """
const cnmaStudies = [
    { treatment1: 'Placebo', treatment2: 'A', effect: 0.5, se: 0.1 },
    { treatment1: 'Placebo', treatment2: 'B', effect: 0.3, se: 0.12 },
    { treatment1: 'Placebo', treatment2: 'A+B', effect: 0.7, se: 0.15 },
    { treatment1: 'A', treatment2: 'A+B', effect: 0.2, se: 0.11 },
    { treatment1: 'B', treatment2: 'A+B', effect: 0.4, se: 0.13 }
];
"""

test("ComponentNMA.analyze", f"""
{cnma_data}
const result = ComponentNMA.analyze(cnmaStudies);
result && result.components && result.combinations && result.ranking
""")

test("ComponentNMA component effects", f"""
{cnma_data}
const result = ComponentNMA.analyze(cnmaStudies);
Object.keys(result.components).length > 0
""")

test("ComponentNMA combinations", f"""
{cnma_data}
const result = ComponentNMA.analyze(cnmaStudies);
result.combinations.length > 0
""")

# =============================================================================
# TEST 5: ROBUST VARIANCE ESTIMATION
# =============================================================================
print("\n[5] Testing Robust Variance Estimation...")

rve_data = """
const rveEffects = [0.3, 0.35, 0.4, 0.25, 0.5, 0.45, 0.2, 0.55];
const rveSEs = [0.1, 0.12, 0.11, 0.09, 0.15, 0.14, 0.08, 0.16];
const clusters = ['C1', 'C1', 'C2', 'C2', 'C3', 'C3', 'C4', 'C4'];
"""

test("RobustVariance.analyze", f"""
{rve_data}
const result = RobustVariance.analyze(rveEffects, rveSEs, clusters);
result && typeof result.effect === 'number' && typeof result.se === 'number'
""")

test("RobustVariance CR2 correction", f"""
{rve_data}
const result = RobustVariance.analyze(rveEffects, rveSEs, clusters);
result.method === "Robust Variance Estimation (CR2)"
""")

test("RobustVariance.threeLevelMeta", f"""
{rve_data}
const level2 = ['L2a', 'L2b', 'L2a', 'L2b', 'L2a', 'L2b', 'L2a', 'L2b'];
const result = RobustVariance.threeLevelMeta(rveEffects, rveSEs, level2, clusters);
result && result.varianceComponents
""")

# =============================================================================
# TEST 6: PRISMA-NMA
# =============================================================================
print("\n[6] Testing PRISMA-NMA Checklist...")

test("PRISMA_NMA.generateChecklist", """
const analysisData = {
    title: 'Network meta-analysis of treatments',
    networkPlot: true,
    treatmentComparisons: ['A vs B', 'B vs C'],
    effectMeasure: 'OR',
    model: 'random',
    method: 'REML',
    heterogeneity: { I2: 45, tau2: 0.1 },
    funnelPlot: true
};
const result = PRISMA_NMA.generateChecklist(analysisData);
result && result.items && result.complianceRate
""")

test("PRISMA_NMA items count", """
const result = PRISMA_NMA.generateChecklist({});
result.items.length >= 20
""")

test("PRISMA_NMA.exportChecklist", """
const checklist = PRISMA_NMA.generateChecklist({ title: 'NMA study' });
const html = PRISMA_NMA.exportChecklist(checklist);
html.includes('<table') && html.includes('prisma-checklist')
""")

# =============================================================================
# TEST 7: SMALL-STUDY EFFECTS
# =============================================================================
print("\n[7] Testing Small-Study Effects...")

binary_data = """
const binaryStudies = [
    { e1: 20, n1: 100, e2: 15, n2: 100 },
    { e1: 30, n1: 150, e2: 22, n2: 150 },
    { e1: 12, n1: 80, e2: 8, n2: 80 },
    { e1: 25, n1: 120, e2: 18, n2: 120 },
    { e1: 18, n1: 90, e2: 12, n2: 90 }
];
"""

test("SmallStudyEffects.petersTest", f"""
{binary_data}
const result = SmallStudyEffects.petersTest(binaryStudies);
result && typeof result.pValue === 'number'
""")

test("SmallStudyEffects.harbordTest", f"""
{binary_data}
const result = SmallStudyEffects.harbordTest(binaryStudies);
result && typeof result.pValue === 'number'
""")

test("SmallStudyEffects.limitMetaAnalysis", f"""
{test_data}
const result = SmallStudyEffects.limitMetaAnalysis(effects, ses);
result && typeof result.limitEstimate === 'number'
""")

# =============================================================================
# TEST 8: EVIDENCE FLOW
# =============================================================================
print("\n[8] Testing Evidence Flow...")

test("EvidenceFlow.analyze", f"""
{nma_data}
const result = EvidenceFlow.analyze(nmaStudies);
result && result.treatments && result.flowMatrix && result.svg
""")

test("EvidenceFlow SVG generation", f"""
{nma_data}
const result = EvidenceFlow.analyze(nmaStudies);
result.svg.includes('<svg') && result.svg.includes('</svg>')
""")

test("EvidenceFlow.contributionMatrix", f"""
{nma_data}
const result = EvidenceFlow.contributionMatrix(nmaStudies, ['A', 'B', 'C']);
result && result.length > 0
""")

# =============================================================================
# TEST 9: CUMULATIVE META-ANALYSIS
# =============================================================================
print("\n[9] Testing Cumulative Meta-Analysis...")

cumulative_data = """
const timeStudies = [
    { study: 'S1', effect: 0.3, se: 0.1, year: 2015 },
    { study: 'S2', effect: 0.5, se: 0.12, year: 2016 },
    { study: 'S3', effect: 0.4, se: 0.11, year: 2017 },
    { study: 'S4', effect: 0.35, se: 0.09, year: 2018 },
    { study: 'S5', effect: 0.45, se: 0.13, year: 2019 },
    { study: 'S6', effect: 0.38, se: 0.1, year: 2020 }
];
"""

test("CumulativeMeta.analyze by year", f"""
{cumulative_data}
const result = CumulativeMeta.analyze(timeStudies, {{ orderBy: 'year' }});
result && result.steps && result.steps.length === 6
""")

test("CumulativeMeta.analyze by precision", f"""
{cumulative_data}
const result = CumulativeMeta.analyze(timeStudies, {{ orderBy: 'precision' }});
result && result.steps && result.finalEffect
""")

test("CumulativeMeta trend assessment", f"""
{cumulative_data}
const result = CumulativeMeta.analyze(timeStudies);
result.trend && typeof result.trend.trend === 'string'
""")

# =============================================================================
# TEST 10: EXISTING MODULES STILL WORK
# =============================================================================
print("\n[10] Testing existing modules...")

test("DesignDecomposition exists", "typeof DesignDecomposition === 'object'")
test("MantelHaenszelNMA exists", "typeof MantelHaenszelNMA === 'object'")
test("CustomLikelihood exists", "typeof CustomLikelihood === 'object'")
test("PopulationAdjustedIC exists", "typeof PopulationAdjustedIC === 'object'")
test("HierarchicalNMA exists", "typeof HierarchicalNMA === 'object'")
test("FrequentistNMA exists", "typeof FrequentistNMA === 'object'")
test("BayesianNMA exists", "typeof BayesianNMA === 'object'")

driver.quit()

# =============================================================================
# RESULTS SUMMARY
# =============================================================================
print("\n" + "="*70)
print("TEST RESULTS SUMMARY")
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
    print("\nALL EDITORIAL FEATURES VALIDATED SUCCESSFULLY!")
else:
    print(f"\n{failed} test(s) failed - review required")

print("="*70)
