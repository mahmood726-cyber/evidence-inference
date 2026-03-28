#!/usr/bin/env python3
"""Test new R-equivalent features in NMA Pro v6.2"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("="*70)
print("NMA Pro v6.2 - TESTING NEW R-EQUIVALENT FEATURES")
print("="*70)

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Edge(options=options)
driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html")
time.sleep(3)

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
        return driver.execute_script(s)
    except Exception as e:
        print(f"    Error: {str(e)[:50]}")
        return None

# Setup test data
print("\n[SETUP] Loading test data...")
js("""
AppState.studies = [
    {id:1, name:'Study 1', treatment1:'A', treatment2:'B', events1:20, n1:100, events2:10, n2:100, year:2018},
    {id:2, name:'Study 2', treatment1:'A', treatment2:'C', events1:25, n1:100, events2:15, n2:100, year:2019},
    {id:3, name:'Study 3', treatment1:'B', treatment2:'C', events1:12, n1:100, events2:18, n2:100, year:2020},
    {id:4, name:'Study 4', treatment1:'A', treatment2:'B', events1:30, n1:120, events2:15, n2:120, year:2021},
    {id:5, name:'Study 5', treatment1:'A', treatment2:'C', events1:22, n1:90, events2:12, n2:90, year:2021}
];
AppState.reference = 'A';
""")
print(f"  Studies loaded: {js('return AppState.studies.length')}")

# ==== TEST NEW MODULES ====
print("\n[1] MODULE EXISTENCE")
test("DesignDecomposition exists", js("return typeof DesignDecomposition !== 'undefined'"))
test("MantelHaenszelNMA exists", js("return typeof MantelHaenszelNMA !== 'undefined'"))
test("CustomLikelihood exists", js("return typeof CustomLikelihood !== 'undefined'"))
test("PopulationAdjustedIC exists", js("return typeof PopulationAdjustedIC !== 'undefined'"))
test("HierarchicalNMA exists", js("return typeof HierarchicalNMA !== 'undefined'"))

# ==== TEST DESIGN DECOMPOSITION ====
print("\n[2] DESIGN DECOMPOSITION (Krahn et al.)")
dd_result = js("""
try {
    var result = DesignDecomposition.analyze(AppState.studies, {reference: 'A'});
    return {
        success: true,
        Qtotal: result.Qtotal,
        Qwithin: result.Qwithin,
        Qbetween: result.Qbetween,
        nDesigns: result.designs.length
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("DesignDecomposition.analyze() works", dd_result and dd_result.get('success'))
if dd_result and dd_result.get('success'):
    print(f"    Q_total={dd_result.get('Qtotal'):.3f}, Q_within={dd_result.get('Qwithin'):.3f}, Q_between={dd_result.get('Qbetween'):.3f}")

# ==== TEST MANTEL-HAENSZEL NMA ====
print("\n[3] MANTEL-HAENSZEL NMA")
mh_result = js("""
try {
    var result = MantelHaenszelNMA.analyze(AppState.studies, {reference: 'A'});
    return {
        success: true,
        method: result.method,
        nTreatments: result.treatments.length,
        hasEffects: Object.keys(result.effects).length > 0
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("MantelHaenszelNMA.analyze() works", mh_result and mh_result.get('success'))
if mh_result and mh_result.get('success'):
    print(f"    Method: {mh_result.get('method')}, Treatments: {mh_result.get('nTreatments')}")

# ==== TEST CUSTOM LIKELIHOOD ====
print("\n[4] CUSTOM LIKELIHOOD")
cl_result = js("""
try {
    var model = CustomLikelihood.createModel('binomial', 'logit');
    return {
        success: true,
        family: model.family.name,
        hasLogLik: typeof model.family.logLik === 'function'
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("CustomLikelihood.createModel() works", cl_result and cl_result.get('success'))

# Test fitting
cl_fit = js("""
try {
    var result = CustomLikelihood.fitNMA(AppState.studies, {
        likelihood: 'binomial',
        reference: 'A'
    });
    return {
        success: true,
        model: result.model,
        hasEffects: Object.keys(result.effects).length > 0
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("CustomLikelihood.fitNMA() works", cl_fit and cl_fit.get('success'))

# ==== TEST POPULATION-ADJUSTED IC ====
print("\n[5] POPULATION-ADJUSTED INDIRECT COMPARISONS")
test("PopulationAdjustedIC.maic exists", js("return typeof PopulationAdjustedIC.maic === 'function'"))
test("PopulationAdjustedIC.stc exists", js("return typeof PopulationAdjustedIC.stc === 'function'"))
test("PopulationAdjustedIC.bucher exists", js("return typeof PopulationAdjustedIC.bucher === 'function'"))

# ==== TEST HIERARCHICAL NMA ====
print("\n[6] HIERARCHICAL NMA (Class Effects)")
hier_result = js("""
try {
    var result = HierarchicalNMA.analyze(AppState.studies, {
        reference: 'A',
        nIter: 200,
        burnin: 50
    });
    return {
        success: true,
        model: result.model,
        nTreatments: result.treatments.length,
        hasTau2: result.tau2 !== undefined
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("HierarchicalNMA.analyze() works", hier_result and hier_result.get('success'))

# Test class effect model
class_result = js("""
try {
    var result = HierarchicalNMA.analyze(AppState.studies, {
        reference: 'A',
        classStructure: {
            'Active': ['A', 'B'],
            'Control': ['C']
        },
        nIter: 200,
        burnin: 50
    });
    return {
        success: true,
        model: result.model,
        hasClassEffects: result.classEffects !== undefined
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("HierarchicalNMA class-effect model works", class_result and class_result.get('success'))

# ==== CHECK FOR ERRORS ====
print("\n[7] ERROR CHECK")
try:
    errors = driver.get_log("browser")
    severe = [e for e in errors if e["level"] == "SEVERE"]
    test("No SEVERE JavaScript errors", len(severe) == 0)
    if severe:
        for e in severe[:3]:
            print(f"    [ERROR] {e['message'][:80]}")
except:
    test("Browser log accessible", False)

# ==== ORIGINAL FEATURES STILL WORK ====
print("\n[8] ORIGINAL FEATURES INTACT")
test("FrequentistNMA exists", js("return typeof FrequentistNMA !== 'undefined'"))
test("BayesianNMA exists", js("return typeof BayesianNMA !== 'undefined'"))
test("NetworkGuardian exists", js("return typeof NetworkGuardian !== 'undefined'"))
test("PublicationBias exists", js("return typeof PublicationBias !== 'undefined'"))

# Quick test of original FrequentistNMA
freq_test = js("""
try {
    var result = FrequentistNMA.analyze(AppState.studies, {reference: 'A', effectMeasure: 'OR'});
    return {success: true, hasTreatments: result.treatments.length > 0};
} catch(e) {
    return {success: false, error: e.message};
}
""")
test("FrequentistNMA.analyze() still works", freq_test and freq_test.get('success'))

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

if rate == 100:
    print("\n  STATUS: PERFECT - All R-equivalent features working!")
elif rate >= 90:
    print("\n  STATUS: EXCELLENT (>90%)")
else:
    print("\n  STATUS: NEEDS ATTENTION")

print("="*70)
