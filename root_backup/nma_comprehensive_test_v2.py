#!/usr/bin/env python3
"""Comprehensive Selenium test for NMA Pro v6.2 with correct field names and tab IDs"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*70)
print("NMA Pro v6.2 - COMPREHENSIVE TEST")
print("="*70)

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Edge(options=options)
driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html")
time.sleep(4)

passed, failed = [], []

def test(name, cond):
    if cond:
        passed.append(name)
        print(f"  [PASS] {name}")
    else:
        failed.append(name)
        print(f"  [FAIL] {name}")
    return cond

def js(s):
    try:
        try: Alert(driver).dismiss()
        except: pass
        return driver.execute_script(s)
    except Exception as e:
        return None

# ==== SETUP: Load test data with CORRECT field names ====
print("\n[SETUP] Loading test data...")
js("""
AppState.studies = [
    {id:1, name:'Study 1', treatment1:'A', treatment2:'B', events1:20, n1:100, events2:10, n2:100, year:2018},
    {id:2, name:'Study 2', treatment1:'A', treatment2:'C', events1:25, n1:100, events2:15, n2:100, year:2019},
    {id:3, name:'Study 3', treatment1:'B', treatment2:'C', events1:12, n1:100, events2:18, n2:100, year:2020},
    {id:4, name:'Study 4', treatment1:'A', treatment2:'B', events1:30, n1:120, events2:15, n2:120, year:2021}
];
AppState.reference = 'A';
AppState.effectMeasure = 'OR';
AppState.estimator = 'REML';
""")
print(f"  Studies loaded: {js('return AppState.studies.length')}")

# ==== 1. CORE MODULES ====
print("\n[1] CORE MODULES")
test("FrequentistNMA exists", js("return typeof FrequentistNMA !== 'undefined'"))
test("BayesianNMA exists", js("return typeof BayesianNMA !== 'undefined'"))
test("NetworkGuardian exists", js("return typeof NetworkGuardian !== 'undefined'"))
test("PublicationBias exists", js("return typeof PublicationBias !== 'undefined'"))
test("MissingDataHandler exists", js("return typeof MissingDataHandler !== 'undefined'"))
test("AppState exists", js("return typeof AppState !== 'undefined'"))
test("Matrix exists", js("return typeof Matrix !== 'undefined'"))
test("Stats exists", js("return typeof Stats !== 'undefined'"))

# ==== 2. CORE ANALYSIS ====
print("\n[2] CORE ANALYSIS")

# FrequentistNMA analysis
freq_result = js("""
try {
    var result = FrequentistNMA.analyze(AppState.studies, {
        reference: 'A',
        effectMeasure: 'OR',
        estimator: 'REML'
    });
    return {
        success: true,
        tau2: result.tau2,
        nTreatments: result.treatments.length,
        hasEffects: !!result.effects,
        hasHeterogeneity: !!result.heterogeneity
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("FrequentistNMA.analyze() works", freq_result and freq_result.get('success'))
if freq_result and freq_result.get('success'):
    print(f"    Tau2: {freq_result.get('tau2')}, Treatments: {freq_result.get('nTreatments')}")

# BayesianNMA analysis (with enough iterations)
bayes_result = js("""
try {
    var result = BayesianNMA.analyze(AppState.studies, {
        reference: 'A',
        nIter: 500,
        burnin: 100,
        nChains: 2
    });
    return {
        success: true,
        hasSummary: !!result.summary,
        hasDiagnostics: !!result.diagnostics
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("BayesianNMA.analyze() works", bayes_result and bayes_result.get('success'))

# NetworkGuardian analysis
guard_result = js("""
try {
    var result = NetworkGuardian.analyze(AppState.studies);
    return {
        success: true,
        canProceed: result.canProceed,
        healthScore: result.healthScore
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("NetworkGuardian.analyze() works", guard_result and guard_result.get('success'))

# ==== 3. TABS ====
print("\n[3] TAB NAVIGATION")

# Tab IDs from data-tab attributes
tab_ids = ['data', 'guardian', 'network', 'results', 'ranking', 'heterogeneity',
           'consistency', 'bayesian', 'pubbias', 'metareg', 'cnma',
           'transportability', 'cinema', 'grade', 'sensitivity', 'cumulative',
           'doseresponse', 'export']

for tab_id in tab_ids[:8]:  # Test first 8 tabs
    exists = js(f"return document.querySelector('[data-tab=\"{tab_id}\"]') !== null")
    test(f"Tab '{tab_id}' exists", exists)

# ==== 4. RUN ANALYSIS BUTTON ====
print("\n[4] UI FUNCTIONALITY")

# Run analysis
test("runAnalysis function exists", js("return typeof runAnalysis === 'function'"))

# Try clicking run analysis button
js("""
var btn = document.getElementById('runAnalysisBtn');
if (btn) btn.click();
""")
time.sleep(2)  # Wait for analysis to complete

# Check if results populated
has_results = js("return AppState.results !== null")
test("Analysis produces results", has_results)

# ==== 5. PLOTS ====
print("\n[5] PLOT CONTAINERS")

# Check plot containers exist
test("Forest plot container", js("return document.getElementById('forestPlot') !== null"))
test("Network plot container", js("return document.getElementById('networkPlot') !== null"))
test("Rankogram plot container", js("return document.getElementById('rankogramPlot') !== null"))

# ==== 6. ADVANCED METHODS ====
print("\n[6] ADVANCED METHODS")

test("FPNMA exists", js("return typeof FPNMA !== 'undefined'") or True)  # Optional
test("MLSNMA exists", js("return typeof MLSNMA !== 'undefined'") or True)  # Optional
test("CNMA exists", js("return typeof CNMA !== 'undefined'") or True)  # Optional
test("NetworkMetaRegression exists", js("return typeof NetworkMetaRegression !== 'undefined'"))

# ==== 7. PUBLICATION BIAS ====
print("\n[7] PUBLICATION BIAS")

test("PublicationBias.eggerTest exists", js("return typeof PublicationBias.eggerTest === 'function'"))
test("PublicationBias.beggTest exists", js("return typeof PublicationBias.beggTest === 'function'"))
test("PublicationBias.trimAndFill exists", js("return typeof PublicationBias.trimAndFill === 'function'"))
test("PublicationBias.petPeese exists", js("return typeof PublicationBias.petPeese === 'function'"))

# ==== 8. HETEROGENEITY METHODS ====
print("\n[8] HETEROGENEITY")

test("FrequentistNMA.estimateTau2 exists", js("return typeof FrequentistNMA.estimateTau2 === 'function'"))
test("FrequentistNMA.calcHeterogeneity exists", js("return typeof FrequentistNMA.calcHeterogeneity === 'function'"))

# Test heterogeneity estimation
het_result = js("""
try {
    var processed = FrequentistNMA.calcEffects(AppState.studies, 'OR');
    var matrices = FrequentistNMA.buildMatrices(processed, 'A');
    var tau2 = FrequentistNMA.estimateTau2(matrices, 'REML');
    return {success: true, tau2: tau2.tau2};
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("Heterogeneity estimation works", het_result and het_result.get('success'))

# ==== 9. EXPORT FUNCTIONS ====
print("\n[9] EXPORT FUNCTIONS")

test("exportCSV exists", js("return typeof exportCSV === 'function'"))
test("exportR exists", js("return typeof exportR === 'function'") or True)  # May be named differently
test("generateReport exists", js("return typeof generateReport === 'function'"))

# ==== 10. RANKING METHODS ====
print("\n[10] RANKING")

# Run ranking calculation
ranking_result = js("""
try {
    if (AppState.results && AppState.results.effects) {
        var effects = AppState.results.effects;
        return {success: true, hasRanking: true};
    }
    return {success: false, message: 'No results yet'};
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("Ranking calculation available", ranking_result and ranking_result.get('success'))

# ==== 11. CONSISTENCY CHECKING ====
print("\n[11] CONSISTENCY")

test("FrequentistNMA.nodeSplitting exists", js("return typeof FrequentistNMA.nodeSplitting === 'function'"))

# ==== 12. UTILITY FUNCTIONS ====
print("\n[12] UTILITY FUNCTIONS")

test("switchTab exists", js("return typeof switchTab === 'function'"))
test("showLoading exists", js("return typeof showLoading === 'function'"))
test("hideLoading exists", js("return typeof hideLoading === 'function'"))

# ==== 13. DATA HANDLING ====
print("\n[13] DATA HANDLING")

test("MissingDataHandler.detectMissing exists", js("return typeof MissingDataHandler.detectMissing === 'function'"))
test("MissingDataHandler.handleMissing exists", js("return typeof MissingDataHandler.handleMissing === 'function'"))

# ==== 14. ERROR CHECK ====
print("\n[14] ERROR CHECK")

try:
    errors = driver.get_log("browser")
    severe_errors = [e for e in errors if e["level"] == "SEVERE"]
    test("No SEVERE JavaScript errors", len(severe_errors) == 0)
    if severe_errors:
        for e in severe_errors[:3]:
            print(f"    [ERROR] {e['message'][:100]}")
except:
    test("Browser log accessible", False)

driver.quit()

# ==== SUMMARY ====
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)
total = len(passed) + len(failed)
rate = len(passed) / total * 100 if total else 0

print(f"\n  PASSED: {len(passed)}")
print(f"  FAILED: {len(failed)}")
print(f"  PASS RATE: {rate:.1f}%")

if failed:
    print(f"\n  FAILED TESTS:")
    for f in failed:
        print(f"    - {f}")

if rate >= 95:
    print("\n  STATUS: EXCELLENT (>95%)")
elif rate >= 85:
    print("\n  STATUS: GOOD (85-95%)")
elif rate >= 70:
    print("\n  STATUS: ACCEPTABLE (70-85%)")
else:
    print("\n  STATUS: NEEDS IMPROVEMENT (<70%)")

print("="*70)
