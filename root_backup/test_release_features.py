"""Test Release Enhancement Features for TruthCert-PairwisePro"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.set_window_size(1600, 1000)

passed = 0
failed = 0

def test(name, condition):
    global passed, failed
    if condition:
        print(f"  [PASS] {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name}")
        failed += 1

try:
    print("=" * 80)
    print("RELEASE FEATURES TEST - TruthCert-PairwisePro v1.0")
    print("=" * 80)

    # Load app
    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
    time.sleep(3)

    # Load demo dataset and run analysis
    print("\n=== Setup ===")
    driver.execute_script("loadDemoDataset('BCG')")
    time.sleep(1)
    driver.execute_script("runAnalysis()")
    time.sleep(2)
    print("  Dataset loaded and analysis complete")

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 1: BOOTSTRAP CONFIDENCE INTERVALS")
    print("=" * 80)

    # Test bootstrapMetaAnalysis function
    bootstrap_result = driver.execute_script("""
        try {
            const yi = AppState.results.studies.map(s => s.yi);
            const vi = AppState.results.studies.map(s => s.vi);
            const result = bootstrapMetaAnalysis(yi, vi, { nBoot: 500, ciMethod: 'percentile' });
            return {
                success: true,
                theta: result.theta,
                ci_lower: result.ci_lower,
                ci_upper: result.ci_upper,
                nBoot: result.nBoot,
                method: result.ciMethod
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if bootstrap_result['success']:
        test(f"Bootstrap CI computed (n={bootstrap_result['nBoot']})", True)
        test(f"Bootstrap theta: {bootstrap_result['theta']:.4f}", bootstrap_result['theta'] is not None)
        test(f"Bootstrap 95% CI: [{bootstrap_result['ci_lower']:.4f}, {bootstrap_result['ci_upper']:.4f}]",
             bootstrap_result['ci_lower'] < bootstrap_result['theta'] < bootstrap_result['ci_upper'])
    else:
        test("Bootstrap CI computed", False)
        print(f"    Error: {bootstrap_result.get('error', 'Unknown')}")

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 2: SAVE/LOAD PROJECT")
    print("=" * 80)

    # Test saveProject function
    save_result = driver.execute_script("""
        try {
            const state = saveProject('test_project');
            return {
                success: true,
                hasData: state.data && state.data.length > 0,
                hasResults: state.results !== null,
                version: state.version
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if save_result['success']:
        test("saveProject function works", True)
        test(f"Saved state has data: {save_result['hasData']}", save_result['hasData'])
        test(f"Saved state has results: {save_result['hasResults']}", save_result['hasResults'])
    else:
        test("saveProject function works", False)

    # Test checkAutosave function
    autosave_result = driver.execute_script("""
        try {
            const check = checkAutosave();
            return { success: true, available: check.available };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)
    test("checkAutosave function works", autosave_result['success'])

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 3: UNDO/REDO SYSTEM")
    print("=" * 80)

    undo_result = driver.execute_script("""
        try {
            UndoManager.clear();
            UndoManager.saveState('test state 1');
            UndoManager.saveState('test state 2');
            const historyLen = UndoManager.history.length;
            return {
                success: true,
                historyLength: historyLen,
                canUndo: UndoManager.currentIndex > 0
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if undo_result['success']:
        test(f"UndoManager initialized (history: {undo_result['historyLength']})", undo_result['historyLength'] >= 2)
    else:
        test("UndoManager initialized", False)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 4: ICER / COST-EFFECTIVENESS")
    print("=" * 80)

    icer_result = driver.execute_script("""
        try {
            const costs = [1000, 2500, 3000];
            const effects = [0.5, 0.7, 0.65];
            const result = calculateICER(costs, effects, { threshold: 30000 });
            return {
                success: true,
                method: result.method,
                numResults: result.results.length,
                optimalByNMB: result.optimalIntervention
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if icer_result['success']:
        test("calculateICER function works", True)
        test(f"ICER results computed: {icer_result['numResults']} comparisons", icer_result['numResults'] >= 1)
        test(f"Optimal intervention identified: {icer_result['optimalByNMB']}", icer_result['optimalByNMB'] is not None)
    else:
        test("calculateICER function works", False)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 5: QALY INTEGRATION")
    print("=" * 80)

    qaly_result = driver.execute_script("""
        try {
            const result = effectToQALY(0.7, { effectType: 'RR', baselineQoL: 0.7 });
            return {
                success: true,
                method: result.method,
                qalyGain: result.qalyGain
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if qaly_result['success']:
        test("effectToQALY function works", True)
        test(f"QALY gain calculated: {qaly_result['qalyGain']:.4f}", qaly_result['qalyGain'] is not None)
    else:
        test("effectToQALY function works", False)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 6: PROBABILISTIC SENSITIVITY ANALYSIS")
    print("=" * 80)

    psa_result = driver.execute_script("""
        try {
            const params = {
                cost: { distribution: 'gamma', mean: 1000, sd: 200 },
                effect: { distribution: 'normal', mean: 0.5, sd: 0.1 }
            };
            const model = function(p) {
                return { cost: p.cost, effect: p.effect, icer: p.cost / p.effect };
            };
            const result = runPSA(params, model, { nSim: 100 });
            return {
                success: true,
                method: result.method,
                nSimulations: result.nSimulations,
                hasSummary: result.summary && Object.keys(result.summary).length > 0
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if psa_result['success']:
        test("runPSA function works", True)
        test(f"PSA simulations: {psa_result['nSimulations']}", psa_result['nSimulations'] >= 50)
        test("PSA summary computed", psa_result['hasSummary'])
    else:
        test("runPSA function works", False)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 7: BUDGET IMPACT ANALYSIS")
    print("=" * 80)

    bia_result = driver.execute_script("""
        try {
            const result = budgetImpactAnalysis({
                population: 100000,
                eligibleProportion: 0.1,
                currentTreatmentCost: 500,
                newTreatmentCost: 1500,
                timeHorizon: 5
            });
            return {
                success: true,
                method: result.method,
                totalBudgetImpact: result.totalBudgetImpact,
                yearCount: result.yearlyResults.length
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if bia_result['success']:
        test("budgetImpactAnalysis function works", True)
        test(f"BIA years computed: {bia_result['yearCount']}", bia_result['yearCount'] >= 5)
        test(f"Total budget impact: ${bia_result['totalBudgetImpact']:,.0f}", bia_result['totalBudgetImpact'] > 0)
    else:
        test("budgetImpactAnalysis function works", False)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 8: VALUE OF INFORMATION (EVPI)")
    print("=" * 80)

    evpi_result = driver.execute_script("""
        try {
            // First run a small PSA
            const params = {
                cost: { distribution: 'gamma', mean: 1000, sd: 200 },
                effect: { distribution: 'normal', mean: 0.5, sd: 0.1 }
            };
            const model = function(p) {
                return { cost: p.cost, effect: p.effect };
            };
            const psaResults = runPSA(params, model, { nSim: 100 });

            // Then calculate EVPI
            const evpi = calculateEVPI(psaResults, 50000);
            return {
                success: true,
                method: evpi.method,
                evpiPerPatient: evpi.evpiPerPatient
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    """)

    if evpi_result['success']:
        test("calculateEVPI function works", True)
        test(f"EVPI per patient: ${evpi_result['evpiPerPatient']:.2f}", evpi_result['evpiPerPatient'] is not None)
    else:
        test("calculateEVPI function works", False)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 9: UI ELEMENTS")
    print("=" * 80)

    # Check for Save/Load buttons
    save_btn = driver.execute_script("return document.getElementById('saveBtn') !== null")
    test("Save button exists", save_btn)

    undo_btn = driver.execute_script("return document.getElementById('undoBtn') !== null")
    test("Undo button exists", undo_btn)

    redo_btn = driver.execute_script("return document.getElementById('redoBtn') !== null")
    test("Redo button exists", redo_btn)

    # Check for Quick Start wizard
    quick_start = driver.execute_script("return document.getElementById('quickStartModal') !== null")
    test("Quick Start wizard modal exists", quick_start)

    # Check for Toast container
    toast = driver.execute_script("return document.getElementById('toast-container') !== null")
    test("Toast container exists", toast)

    # Check Quick Start wizard functions
    qs_functions = driver.execute_script("""
        return typeof showQuickStartWizard === 'function' &&
               typeof closeQuickStartWizard === 'function' &&
               typeof nextQuickStartStep === 'function';
    """)
    test("Quick Start wizard functions available", qs_functions)

    # =========================================================================
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)

    total = passed + failed
    print(f"\n  Total Tests: {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Success Rate: {(passed/total*100):.1f}%")

    if failed == 0:
        print("\n  [OK] ALL RELEASE FEATURES WORKING!")
    else:
        print(f"\n  [WARN] {failed} test(s) failed")

    print("=" * 80)

finally:
    driver.quit()
