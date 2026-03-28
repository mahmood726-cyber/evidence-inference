"""Test Advanced UI fixes for TruthCert-PairwisePro"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)

try:
    print("=" * 70)
    print("ADVANCED UI FIXES TEST")
    print("=" * 70)

    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
    time.sleep(3)

    # Load BCG dataset and run analysis
    print("\n=== Setup ===")
    driver.execute_script("loadDemoDataset('BCG')")
    time.sleep(1)
    driver.execute_script("runAnalysis()")
    time.sleep(2)
    print("  [OK] Dataset loaded and analyzed")

    # Navigate to Advanced tab
    driver.execute_script("document.querySelector('[data-tab=\"advanced\"]').click()")
    time.sleep(0.5)

    # Test 1: Interactive Sensitivity
    print("\n=== Test: Interactive Sensitivity ===")
    try:
        driver.execute_script("initSensitivityControls()")
        time.sleep(0.5)
        result = driver.execute_script("return document.getElementById('sensitivityControls').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] Sensitivity controls initialized")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 2: Living Meta-Analysis
    print("\n=== Test: Living Meta-Analysis ===")
    try:
        driver.execute_script("addToLivingMA()")
        time.sleep(0.5)
        result = driver.execute_script("return LivingMA.history.length > 0")
        print(f"  [{'PASS' if result else 'FAIL'}] Living MA: Analysis added (history = {driver.execute_script('return LivingMA.history.length')})")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 3: IPD Simulation
    print("\n=== Test: IPD Simulation ===")
    try:
        driver.execute_script("runIPDSimulation()")
        time.sleep(0.5)
        result = driver.execute_script("return AppState.simulatedIPD && AppState.simulatedIPD.length > 0")
        n_patients = driver.execute_script("return AppState.simulatedIPD ? AppState.simulatedIPD.length : 0")
        print(f"  [{'PASS' if result else 'FAIL'}] IPD simulated ({n_patients} patients)")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 4: Multiverse Analysis
    print("\n=== Test: Multiverse Analysis ===")
    try:
        driver.execute_script("runMultiverseAnalysis()")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('multiverseResults').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] Multiverse analysis computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 5: Fragility Analysis
    print("\n=== Test: Fragility Analysis ===")
    try:
        driver.execute_script("runFragilityAnalysis()")
        time.sleep(0.5)
        result = driver.execute_script("return document.getElementById('fragilityResults').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] Fragility analysis computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 6: Clinical Translation (Translate button)
    print("\n=== Test: Clinical Translation ===")
    try:
        driver.execute_script("runClinicalTranslation()")
        time.sleep(0.5)
        result = driver.execute_script("return document.getElementById('clinicalResults').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] Clinical translation computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 7: Search Strategy Generator
    print("\n=== Test: Search Strategy Generator ===")
    try:
        driver.execute_script("document.getElementById('searchTopic').value = 'tuberculosis vaccine'")
        driver.execute_script("generateSearchStrategyUI()")
        time.sleep(0.5)
        result = driver.execute_script("return document.getElementById('searchStrategyPanel').innerHTML.includes('PubMed')")
        print(f"  [{'PASS' if result else 'FAIL'}] Search strategy generated")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 8: Comprehensive Analysis Suite
    print("\n=== Test: Complete Analysis Suite ===")
    try:
        driver.execute_script("runComprehensiveAnalysis()")
        time.sleep(2)
        result = driver.execute_script("return document.getElementById('comprehensiveResults').innerHTML.includes('Complete')")
        print(f"  [{'PASS' if result else 'FAIL'}] Comprehensive analysis completed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 9: Report Generation
    print("\n=== Test: Report Generation ===")
    try:
        driver.execute_script("goToTab('report')")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('panel-report').innerHTML.includes('Generate Report')")
        print(f"  [{'PASS' if result else 'FAIL'}] Report panel rendered")
    except Exception as e:
        print(f"  [FAIL] {e}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

finally:
    driver.quit()
