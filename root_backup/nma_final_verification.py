
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.alert import Alert
import time

print("="*70)
print("NMA PRO v6.2 - FINAL VERIFICATION")
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

def js(s):
    try:
        try: Alert(driver).dismiss()
        except: pass
        return driver.execute_script(s)
    except: return None

# ============== CORE MODULES ==============
print("\n[1] CORE MODULES")
test("FrequentistNMA", js("return typeof FrequentistNMA !== 'undefined'"))
test("BayesianNMA", js("return typeof BayesianNMA !== 'undefined'"))
test("AppState", js("return typeof AppState !== 'undefined'"))

# ============== ADVANCED NMA METHODS ==============
print("\n[2] ADVANCED NMA METHODS (Editorial Requirements)")
test("FPNMA module", js("return typeof FPNMA !== 'undefined' && typeof FPNMA.analyze === 'function'"))
test("MLSNMA module", js("return typeof MLSNMA !== 'undefined' && typeof MLSNMA.analyze === 'function'"))
test("FPNMA_FractionalPolynomial module", js("return typeof FPNMA_FractionalPolynomial !== 'undefined' && typeof FPNMA_FractionalPolynomial.analyze === 'function'"))
test("MLNMR module", js("return typeof MLNMR !== 'undefined' && typeof MLNMR.analyze === 'function'"))
test("PROSPERO module", js("return typeof PROSPERO !== 'undefined'"))

# ============== KEY FUNCTIONS ==============
print("\n[3] KEY FUNCTIONS")
test("switchTab", js("return typeof switchTab === 'function'"))
test("generateBayesianRScript", js("return typeof generateBayesianRScript === 'function'"))
test("pauleMandel_CI method", js("return typeof FrequentistNMA.pauleMandel_CI === 'function'"))

# ============== LOAD DATA ==============
print("\n[4] DATA LOADING")
js("""
AppState.studies = [
    {id:1, study:'Study1', treat1:'A', treat2:'B', effect:0.5, se:0.2, year:2020, n1:50, n2:50},
    {id:2, study:'Study2', treat1:'A', treat2:'C', effect:0.3, se:0.25, year:2019, n1:45, n2:45},
    {id:3, study:'Study3', treat1:'B', treat2:'C', effect:-0.2, se:0.18, year:2021, n1:60, n2:60},
    {id:4, study:'Study4', treat1:'A', treat2:'B', effect:0.45, se:0.22, year:2020, n1:55, n2:55},
    {id:5, study:'Study5', treat1:'A', treat2:'D', effect:0.8, se:0.3, year:2018, n1:40, n2:40},
    {id:6, study:'Study6', treat1:'B', treat2:'D', effect:0.35, se:0.28, year:2019, n1:48, n2:48},
    {id:7, study:'Study7', treat1:'C', treat2:'D', effect:0.15, se:0.2, year:2021, n1:52, n2:52},
    {id:8, study:'Study8', treat1:'A', treat2:'C', effect:0.25, se:0.23, year:2020, n1:47, n2:47}
];
AppState.reference = 'A';
""")
time.sleep(0.5)
test("8 studies loaded", js("return AppState.studies && AppState.studies.length === 8"))
test("Reference = A", js("return AppState.reference === 'A'"))

# ============== ANALYSIS EXECUTION ==============
print("\n[5] ANALYSIS EXECUTION")

# FPNMA
fpnma_ok = js("""
try {
    var r = FPNMA.analyze(AppState.studies, {reference: 'A'});
    return r !== null && r !== undefined;
} catch(e) { return false; }
""")
test("FPNMA.analyze() executes", fpnma_ok)

# MLSNMA
mlsnma_ok = js("""
try {
    var r = MLSNMA.analyze(AppState.studies, {reference: 'A'});
    return r !== null && r !== undefined;
} catch(e) { return false; }
""")
test("MLSNMA.analyze() executes", mlsnma_ok)

# FPNMA_FractionalPolynomial
fpnma_fp_ok = js("""
try {
    var r = FPNMA_FractionalPolynomial.analyze(AppState.studies, {reference: 'A'});
    return r !== null && r !== undefined;
} catch(e) { return false; }
""")
test("FPNMA_FractionalPolynomial.analyze() executes", fpnma_fp_ok)

# MLNMR
mlnmr_ok = js("""
try {
    var r = MLNMR.analyze(AppState.studies, {reference: 'A'});
    return r !== null && r !== undefined;
} catch(e) { return false; }
""")
test("MLNMR.analyze() executes", mlnmr_ok)

# Bayesian
bayesian_ok = js("""
try {
    var r = BayesianNMA.analyze(AppState.studies, {reference: 'A', nIter: 200, burnin: 50});
    return r && r.samples && r.samples.tau2 && r.samples.tau2.length > 0;
} catch(e) { return false; }
""")
test("BayesianNMA.analyze() executes", bayesian_ok)

# ============== TAB NAVIGATION ==============
print("\n[6] TAB NAVIGATION")
# Get actual tab IDs from the page
tab_ids = js("""
var tabs = document.querySelectorAll('[data-tab], .tab-content, [id]');
var ids = [];
tabs.forEach(function(t) {
    if (t.id) ids.push(t.id);
});
return ids.filter(function(id) {
    return id.includes('Tab') || ['network','results','forest','rankings','heterogeneity',
           'consistency','bayesian','bias','regression','cnma','cinema','grade',
           'sensitivity','cumulative','dose','export','cstream'].includes(id);
}).slice(0, 20);
""")
if tab_ids:
    print(f"  Found tab IDs: {tab_ids[:10]}...")

# Test known working tabs
test("Tab navigation works", js("try { switchTab('network'); return true; } catch(e) { return false; }"))
test("Tab 'results' exists", js("return document.getElementById('results') !== null"))

# ============== CANVAS/PLOT ELEMENTS ==============
print("\n[7] VISUALIZATION ELEMENTS")
test("Network plot container", js("return document.getElementById('networkPlot') !== null"))
test("Forest plot container", js("return document.getElementById('forestPlot') !== null"))

# ============== CONSOLE ERRORS ==============
print("\n[8] JAVASCRIPT ERRORS")
errors = [e for e in driver.get_log("browser") if e["level"] == "SEVERE"]
test("No SEVERE JS errors", len(errors) == 0)
if errors:
    print(f"  Errors: {len(errors)}")
    for e in errors[:3]:
        print(f"    {e['message'][:80]}")

driver.quit()

# ============== SUMMARY ==============
print("\n" + "="*70)
print("VERIFICATION SUMMARY")
print("="*70)
total = len(passed) + len(failed)
rate = len(passed) / total * 100 if total else 0

print(f"\n  PASSED: {len(passed)}")
print(f"  FAILED: {len(failed)}")
print(f"  PASS RATE: {rate:.1f}%")

if rate == 100:
    print("\n  STATUS: ALL TESTS PASSED")
elif rate >= 90:
    print("\n  STATUS: EXCELLENT (>90%)")
elif rate >= 75:
    print("\n  STATUS: GOOD (>75%)")
else:
    print("\n  STATUS: NEEDS ATTENTION")

if failed:
    print(f"\n  Failed: {failed}")

print("="*70)
