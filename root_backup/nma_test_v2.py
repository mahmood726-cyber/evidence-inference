
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time

print("="*70)
print("NMA PRO v6.2 - COMPREHENSIVE TEST")
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
        print(f"  [OK] {name}")
    else:
        failed.append(name)
        print(f"  [FAIL] {name}")

def js(s):
    try:
        # Dismiss any alerts first
        try:
            Alert(driver).dismiss()
        except:
            pass
        return driver.execute_script(s)
    except Exception as e:
        if "alert" in str(e).lower():
            try:
                Alert(driver).dismiss()
            except:
                pass
        return None

# Check core objects exist
print("\n[CORE] Checking core objects...")
test("FrequentistNMA exists", js("return typeof FrequentistNMA !== 'undefined'"))
test("BayesianNMA exists", js("return typeof BayesianNMA !== 'undefined'"))
test("AppState exists", js("return typeof AppState !== 'undefined'"))

# Check advanced methods
print("\n[ADVANCED METHODS] Checking all advanced NMA methods...")
test("FPNMA", js("return typeof FPNMA !== 'undefined'"))
test("MLSNMA", js("return typeof MLSNMA !== 'undefined'"))
test("FPNMA_FractionalPolynomial", js("return typeof FPNMA_FractionalPolynomial !== 'undefined'"))
test("MLNMR", js("return typeof MLNMR !== 'undefined'"))
test("PROSPERO", js("return typeof PROSPERO !== 'undefined'"))

# Check FPNMA methods
print("\n[FPNMA] Checking FPNMA module...")
test("FPNMA.analyze", js("return typeof FPNMA.analyze === 'function'"))
test("FPNMA.buildNetworkGraph", js("return typeof FPNMA.buildNetworkGraph === 'function'"))

# Check MLSNMA methods
print("\n[MLSNMA] Checking MLSNMA module...")
test("MLSNMA.analyze", js("return typeof MLSNMA.analyze === 'function'"))
test("MLSNMA.buildCovarianceMatrix", js("return typeof MLSNMA.buildCovarianceMatrix === 'function'"))

# Check FPNMA_FractionalPolynomial methods
print("\n[FP-NMA] Checking Fractional Polynomial module...")
test("FPNMA_FractionalPolynomial.analyze", js("return typeof FPNMA_FractionalPolynomial.analyze === 'function'"))
test("FPNMA_FractionalPolynomial.fitFractionalPolynomial", js("return typeof FPNMA_FractionalPolynomial.fitFractionalPolynomial === 'function'"))

# Check MLNMR methods
print("\n[MLNMR] Checking ML-NMR module...")
test("MLNMR.analyze", js("return typeof MLNMR.analyze === 'function'"))
test("MLNMR.performMAIC", js("return typeof MLNMR.performMAIC === 'function'"))
test("MLNMR.performSTC", js("return typeof MLNMR.performSTC === 'function'"))

# Check PROSPERO methods
print("\n[PROSPERO] Checking PROSPERO module...")
test("PROSPERO.validateRegistration", js("return typeof PROSPERO.validateRegistration === 'function'"))
test("PROSPERO.trackDeviations", js("return typeof PROSPERO.trackDeviations === 'function'"))

# Check UI functions
print("\n[UI] Checking UI functions...")
test("switchTab function", js("return typeof switchTab === 'function'"))
test("generateBayesianRScript", js("return typeof generateBayesianRScript === 'function'"))

# Try to load data using the correct method
print("\n[DATA] Loading sample data...")
# First try to find load buttons
load_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Load') or contains(text(),'Sample') or contains(text(),'Demo')]")
print(f"  Found {len(load_buttons)} potential load buttons")

# Try to inject sample data directly
sample_data = """
AppState.studies = [
    {id: 1, study: 'Study1', treat1: 'A', treat2: 'B', effect: 0.5, se: 0.2, year: 2020},
    {id: 2, study: 'Study2', treat1: 'A', treat2: 'C', effect: 0.3, se: 0.25, year: 2019},
    {id: 3, study: 'Study3', treat1: 'B', treat2: 'C', effect: -0.2, se: 0.18, year: 2021},
    {id: 4, study: 'Study4', treat1: 'A', treat2: 'B', effect: 0.45, se: 0.22, year: 2020},
    {id: 5, study: 'Study5', treat1: 'A', treat2: 'D', effect: 0.8, se: 0.3, year: 2018},
    {id: 6, study: 'Study6', treat1: 'B', treat2: 'D', effect: 0.35, se: 0.28, year: 2019},
    {id: 7, study: 'Study7', treat1: 'C', treat2: 'D', effect: 0.15, se: 0.2, year: 2021},
    {id: 8, study: 'Study8', treat1: 'A', treat2: 'C', effect: 0.25, se: 0.23, year: 2020}
];
AppState.reference = 'A';
return true;
"""
js(sample_data)
time.sleep(0.5)
test("Studies loaded", js("return AppState.studies && AppState.studies.length >= 8"))
test("Reference set", js("return AppState.reference === 'A'"))

# Run analysis
print("\n[ANALYSIS] Running frequentist analysis...")
js("try { AppState.results = FrequentistNMA.analyze(AppState.studies, {reference: AppState.reference}); } catch(e) { console.error(e); }")
time.sleep(1)
test("Analysis completed", js("return AppState.results !== null && AppState.results !== undefined"))
test("Treatments extracted", js("return AppState.results && AppState.results.treatments && AppState.results.treatments.length >= 4"))
test("Tau2 calculated", js("return AppState.results && AppState.results.tau2 !== undefined"))

# Test FPNMA with loaded data
print("\n[FPNMA RUN] Testing FPNMA analysis...")
fpnma_result = js("""
try {
    var result = FPNMA.analyze(AppState.studies, {reference: AppState.reference});
    return result && result.applicable !== false;
} catch(e) {
    console.error('FPNMA error:', e);
    return false;
}
""")
test("FPNMA analysis runs", fpnma_result)

# Test MLSNMA
print("\n[MLSNMA RUN] Testing MLSNMA analysis...")
mlsnma_result = js("""
try {
    var result = MLSNMA.analyze(AppState.studies, {reference: AppState.reference});
    return result && result.applicable !== false;
} catch(e) {
    console.error('MLSNMA error:', e);
    return false;
}
""")
test("MLSNMA analysis runs", mlsnma_result)

# Test Bayesian
print("\n[BAYESIAN] Testing Bayesian NMA...")
bayesian_result = js("""
try {
    var result = BayesianNMA.analyze(AppState.studies, {
        reference: AppState.reference,
        nIter: 200,
        burnin: 50
    });
    return result && result.samples && result.samples.tau2 && result.samples.tau2.length > 0;
} catch(e) {
    console.error('Bayesian error:', e);
    return false;
}
""")
test("Bayesian NMA runs", bayesian_result)

# Check tabs exist
print("\n[TABS] Checking tab elements...")
tabs_to_check = ['network', 'results', 'rankings', 'heterogeneity', 'consistency',
                 'bayesian', 'bias', 'regression', 'cnma', 'cstream', 'cinema',
                 'grade', 'sensitivity', 'cumulative', 'dose', 'export']

for tab in tabs_to_check:
    exists = js(f"return document.getElementById('{tab}') !== null || document.querySelector('[data-tab=\"{tab}\"]') !== null")
    test(f"Tab '{tab}'", exists)

driver.quit()

print("\n" + "="*70)
total = len(passed) + len(failed)
rate = len(passed) / total * 100 if total else 0
print(f"\nPASSED: {len(passed)} | FAILED: {len(failed)}")
print(f"PASS RATE: {rate:.1f}% ({len(passed)}/{total})")
if failed:
    print("\nFailed tests:")
    for f in failed:
        print(f"  - {f}")
print("="*70)
