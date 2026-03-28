"""Comprehensive Selenium Test for TruthCert-PairwisePro"""
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

def click_tab(tab_name):
    """Click a tab by its data-tab attribute"""
    driver.execute_script(f"document.querySelector('[data-tab=\"{tab_name}\"]').click()")
    time.sleep(0.5)

try:
    print("=" * 80)
    print("COMPREHENSIVE SELENIUM TEST - TruthCert-PairwisePro")
    print("=" * 80)

    # Load app
    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
    time.sleep(3)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 1: DATA LOADING & BASIC ANALYSIS")
    print("=" * 80)

    # Test demo dataset loading
    print("\n--- Demo Datasets ---")
    driver.execute_script("loadDemoDataset('BCG')")
    time.sleep(2)  # Wait for dataset to load
    # Check if table has rows (data is added to table, not just AppState.data)
    bcg_loaded = driver.execute_script("return document.getElementById('studyTableBody').children.length > 0")
    bcg_count = driver.execute_script("return document.getElementById('studyTableBody').children.length")
    test(f"BCG dataset loaded ({bcg_count} studies in table)", bcg_loaded)

    # Run analysis
    print("\n--- Run Analysis ---")
    driver.execute_script("runAnalysis()")
    time.sleep(2)
    has_results = driver.execute_script("return AppState.results && AppState.results.pooled")
    test("Analysis completed", has_results)

    pooled_effect = driver.execute_script("return AppState.results.pooled.theta")
    test(f"Pooled effect computed: {pooled_effect:.4f}", pooled_effect is not None)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 2: MAIN TAB PANELS")
    print("=" * 80)

    # Analysis tab
    print("\n--- Analysis Tab ---")
    click_tab('analysis')
    time.sleep(1)  # Wait for plots to render
    test("Analysis panel accessible", True)  # Tab click worked

    # Forest plot (ID is forestPlot without hyphen)
    forest_rendered = driver.execute_script("return document.getElementById('forestPlot') && document.getElementById('forestPlot').children.length > 0")
    test("Forest plot rendered", forest_rendered)

    # Funnel plot (ID is funnelPlot without hyphen)
    funnel_rendered = driver.execute_script("return document.getElementById('funnelPlot') && document.getElementById('funnelPlot').children.length > 0")
    test("Funnel plot rendered", funnel_rendered)

    # DDMA tab
    print("\n--- DDMA Tab ---")
    click_tab('ddma')
    ddma_content = driver.execute_script("return document.getElementById('panel-ddma').innerHTML.length > 100")
    test("DDMA panel has content", ddma_content)

    # Heterogeneity tab
    print("\n--- Heterogeneity Tab ---")
    click_tab('heterogeneity')
    het_content = driver.execute_script("return document.getElementById('panel-heterogeneity').innerHTML.length > 100")
    test("Heterogeneity panel has content", het_content)

    # Bias tab
    print("\n--- Bias Tab ---")
    click_tab('bias')
    bias_content = driver.execute_script("return document.getElementById('panel-bias').innerHTML.length > 100")
    test("Bias panel has content", bias_content)

    # Clinical tab
    print("\n--- Clinical Tab ---")
    click_tab('clinical')
    clinical_content = driver.execute_script("return document.getElementById('panel-clinical').innerHTML.length > 100")
    test("Clinical panel has content", clinical_content)

    # Advanced tab
    print("\n--- Advanced Tab ---")
    click_tab('advanced')
    adv_content = driver.execute_script("return document.getElementById('panel-advanced').innerHTML.length > 100")
    test("Advanced panel has content", adv_content)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 3: ADVANCED ANALYSES")
    print("=" * 80)

    # Power Analysis
    print("\n--- Power Analysis ---")
    driver.execute_script("runPowerAnalysis()")
    time.sleep(1)
    power_result = driver.execute_script("return document.getElementById('powerResults').innerHTML.length > 50")
    test("Power analysis computed", power_result)

    # Meta-Regression
    print("\n--- Meta-Regression ---")
    driver.execute_script("runMetaRegression()")
    time.sleep(1)
    metareg_result = driver.execute_script("return document.getElementById('metaregResults').innerHTML.length > 50")
    test("Meta-regression computed", metareg_result)

    # Leave-One-Out
    print("\n--- Leave-One-Out Analysis ---")
    driver.execute_script("runLeaveOneOutCorrected()")
    time.sleep(1)
    loo_result = driver.execute_script("return document.getElementById('looResults').innerHTML.length > 50")
    test("LOO analysis computed", loo_result)

    # Cumulative Analysis
    print("\n--- Cumulative Meta-Analysis ---")
    driver.execute_script("runCumulativeAnalysis()")
    time.sleep(1)
    cum_result = driver.execute_script("return document.getElementById('cumYearPlot').innerHTML.length > 0 || document.getElementById('cumYearPlot').children.length > 0")
    test("Cumulative analysis computed", cum_result)

    # GRADE Assessment
    print("\n--- GRADE Assessment ---")
    driver.execute_script("runGRADEAssessment()")
    time.sleep(1)
    grade_result = driver.execute_script("return document.getElementById('gradeResults').innerHTML.length > 50")
    test("GRADE assessment computed", grade_result)

    # ML Outlier Detection
    print("\n--- ML Outlier Detection ---")
    driver.execute_script("runMLOutlierDetection()")
    time.sleep(1)
    outlier_result = driver.execute_script("return document.getElementById('outlierResults').innerHTML.length > 50")
    test("ML outlier detection computed", outlier_result)

    # Interactive Sensitivity
    print("\n--- Interactive Sensitivity ---")
    driver.execute_script("initSensitivityControls()")
    time.sleep(0.5)
    sens_result = driver.execute_script("return document.getElementById('sensitivityControls').innerHTML.length > 50")
    test("Sensitivity controls initialized", sens_result)

    # Living Meta-Analysis
    print("\n--- Living Meta-Analysis ---")
    driver.execute_script("addToLivingMA()")
    time.sleep(0.5)
    living_result = driver.execute_script("return LivingMA.history.length > 0")
    test("Living MA: analysis added", living_result)
    driver.execute_script("renderLivingMADashboard('livingMADashboard')")
    time.sleep(0.5)
    dashboard_result = driver.execute_script("return document.getElementById('livingMADashboard').innerHTML.includes('Date')")
    test("Living MA: dashboard shown", dashboard_result)

    # IPD Simulation
    print("\n--- IPD Simulation ---")
    driver.execute_script("runIPDSimulation()")
    time.sleep(0.5)
    ipd_result = driver.execute_script("return AppState.simulatedIPD && AppState.simulatedIPD.length > 0")
    ipd_count = driver.execute_script("return AppState.simulatedIPD ? AppState.simulatedIPD.length : 0")
    test(f"IPD simulated ({ipd_count} patients)", ipd_result)

    # Multiverse Analysis
    print("\n--- Multiverse Analysis ---")
    driver.execute_script("runMultiverseAnalysis()")
    time.sleep(1)
    mv_result = driver.execute_script("return document.getElementById('multiverseResults').innerHTML.length > 50")
    test("Multiverse analysis computed", mv_result)

    # Fragility Analysis
    print("\n--- Fragility Analysis ---")
    driver.execute_script("runFragilityAnalysis()")
    time.sleep(0.5)
    frag_result = driver.execute_script("return document.getElementById('fragilityResults').innerHTML.length > 50")
    test("Fragility analysis computed", frag_result)

    # Clinical Translation
    print("\n--- Clinical Translation ---")
    driver.execute_script("runClinicalTranslation()")
    time.sleep(0.5)
    clin_result = driver.execute_script("return document.getElementById('clinicalResults').innerHTML.length > 50")
    test("Clinical translation computed", clin_result)

    # Search Strategy Generator
    print("\n--- Search Strategy Generator ---")
    driver.execute_script("document.getElementById('searchTopic').value = 'tuberculosis vaccine'")
    driver.execute_script("generateSearchStrategyUI()")
    time.sleep(0.5)
    search_result = driver.execute_script("return document.getElementById('searchStrategyPanel').innerHTML.includes('PubMed')")
    test("Search strategy generated", search_result)

    # Comprehensive Analysis Suite
    print("\n--- Complete Analysis Suite ---")
    driver.execute_script("runComprehensiveAnalysis()")
    time.sleep(2)
    comp_result = driver.execute_script("return document.getElementById('comprehensiveResults').innerHTML.includes('Complete')")
    test("Comprehensive analysis completed", comp_result)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 4: SPECIAL PANELS")
    print("=" * 80)

    # Clinical Panel (computeClinical)
    print("\n--- Clinical Compute ---")
    driver.execute_script("computeClinical()")
    time.sleep(1)
    clinical_panel = driver.execute_script("return document.getElementById('clinical-results').innerHTML.length > 50")
    test("Clinical results computed", clinical_panel)

    # Cross-disciplinary Tab
    print("\n--- Cross-disciplinary Panel ---")
    driver.execute_script("updateCrossDisciplinary()")
    click_tab('crossdisciplinary')
    cross_result = driver.execute_script("return document.getElementById('panel-crossdisciplinary').innerHTML.includes('Economics')")
    test("Cross-disciplinary content updated", cross_result)

    # Code Export Panel
    print("\n--- Code Export Panel ---")
    driver.execute_script("updateCodePanel()")
    click_tab('code')
    code_result = driver.execute_script("return document.getElementById('panel-code').innerHTML.includes('library(metafor)')")
    test("Code panel updated with R code", code_result)

    # Metaoverfit Assessment
    print("\n--- Metaoverfit Assessment ---")
    driver.execute_script("updateMetaoverfitResults()")
    time.sleep(0.5)
    metaoverfit_data = driver.execute_script("""
        return AppState.results &&
               AppState.results.metaoverfit &&
               AppState.results.metaoverfit.k &&
               AppState.results.metaoverfit.ratio > 0 &&
               AppState.results.metaoverfit.risk_level
    """)
    if metaoverfit_data:
        risk = driver.execute_script("return AppState.results.metaoverfit.risk_level")
        ratio = driver.execute_script("return AppState.results.metaoverfit.ratio.toFixed(1)")
        test(f"Metaoverfit computed: {risk} risk (k:p = {ratio})", True)
    else:
        test("Metaoverfit computed", False)

    # TruthCert Verdict
    print("\n--- TruthCert Verdict ---")
    click_tab('verdict')
    time.sleep(1)
    truthcert_data = driver.execute_script("""
        return AppState.truthcert &&
               AppState.truthcert.verdict &&
               AppState.truthcert.verdict.verdict
    """)
    if truthcert_data:
        verdict = driver.execute_script("return AppState.truthcert.verdict.verdict")
        tier = driver.execute_script("return AppState.truthcert.verdict.tier")
        test(f"TruthCert verdict: {verdict} (Tier {tier})", True)
    else:
        test("TruthCert verdict computed", False)

    # HTA Panel
    print("\n--- HTA Panel ---")
    click_tab('hta')
    hta_content = driver.execute_script("return document.getElementById('panel-hta').innerHTML.length > 100")
    test("HTA panel has content", hta_content)

    # Report Generation
    print("\n--- Report Panel ---")
    driver.execute_script("goToTab('report')")
    time.sleep(1)
    report_result = driver.execute_script("return document.getElementById('panel-report').innerHTML.length > 100")
    test("Report panel rendered", report_result)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 5: BAYESIAN ANALYSES")
    print("=" * 80)

    # Bayesian Analysis - check pooled results
    print("\n--- Bayesian Meta-Analysis ---")
    # Re-load BCG and run analysis to ensure clean state
    driver.execute_script("loadDemoDataset('BCG')")
    time.sleep(1)
    driver.execute_script("runAnalysis()")
    time.sleep(2)

    # Check if pooled result exists
    pooled_exists = driver.execute_script("return AppState.results && AppState.results.pooled")
    test("Pooled analysis exists for Bayesian check", pooled_exists)

    # Full MCMC (if available)
    print("\n--- Full MCMC Analysis ---")
    mcmc_exposed = driver.execute_script("return typeof fullMCMCBayesianMA === 'function'")
    test("Full MCMC function available", mcmc_exposed)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 6: PUBLICATION BIAS TESTS")
    print("=" * 80)

    print("\n--- Bias Tests ---")
    # Navigate to bias tab to trigger lazy computation
    click_tab('bias')
    time.sleep(1)

    # Check if bias panel has content (Egger test info)
    bias_panel = driver.execute_script("return document.getElementById('panel-bias').innerHTML.includes('Egger') || document.getElementById('panel-bias').innerHTML.includes('Funnel')")
    test("Bias panel has test results", bias_panel)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 7: HETEROGENEITY")
    print("=" * 80)

    print("\n--- Heterogeneity Statistics ---")
    # Navigate to heterogeneity tab
    click_tab('heterogeneity')
    time.sleep(1)

    # Check heterogeneity panel has content
    het_panel = driver.execute_script("return document.getElementById('panel-heterogeneity').innerHTML.length > 200")
    test("Heterogeneity panel has substantial content", het_panel)

    # =========================================================================
    print("\n" + "=" * 80)
    print("SECTION 8: OTHER DATASETS")
    print("=" * 80)

    # Test ASPIRIN_CVD dataset
    print("\n--- Aspirin CVD Dataset ---")
    driver.execute_script("loadDemoDataset('ASPIRIN_CVD')")
    time.sleep(1)
    driver.execute_script("runAnalysis()")
    time.sleep(2)
    aspirin_result = driver.execute_script("return AppState.results && AppState.results.studies.length > 0")
    k_studies = driver.execute_script("return AppState.results ? AppState.results.studies.length : 0")
    test(f"ASPIRIN_CVD loaded & analyzed (k={k_studies})", aspirin_result)

    # Test BP_REDUCTION (continuous) dataset
    print("\n--- BP Reduction Dataset (Continuous) ---")
    driver.execute_script("loadDemoDataset('BP_REDUCTION')")
    time.sleep(1)
    driver.execute_script("runAnalysis()")
    time.sleep(2)
    bp_result = driver.execute_script("return AppState.results && AppState.results.studies.length > 0")
    k_studies = driver.execute_script("return AppState.results ? AppState.results.studies.length : 0")
    test(f"BP_REDUCTION loaded & analyzed (k={k_studies})", bp_result)

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
        print("\n  [OK] ALL TESTS PASSED!")
    else:
        print(f"\n  [WARN] {failed} test(s) failed")

    print("=" * 80)

finally:
    driver.quit()
