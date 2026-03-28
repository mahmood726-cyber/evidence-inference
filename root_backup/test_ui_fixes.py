"""Test UI fixes for TruthCert-PairwisePro"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)

try:
    print("=" * 70)
    print("UI FIXES TEST")
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

    # Test 1: Clinical Translation
    print("\n=== Test: Clinical Translation ===")
    try:
        driver.execute_script("computeClinical()")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('clinical-results').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] Clinical translation computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 2: Power Analysis
    print("\n=== Test: Power Analysis ===")
    try:
        driver.execute_script("document.querySelector('[data-tab=\"advanced\"]').click()")
        time.sleep(0.5)
        btn_exists = driver.execute_script("return document.querySelector('button[onclick*=\"runPowerAnalysis\"]') !== null")
        print(f"  [{'PASS' if btn_exists else 'FAIL'}] Power Analysis button exists")
        driver.execute_script("runPowerAnalysis()")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('powerResults').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] Power analysis computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 3: ML Outlier Detection
    print("\n=== Test: ML Outlier Detection ===")
    try:
        driver.execute_script("runMLOutlierDetection()")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('outlierResults').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] ML outlier detection computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 4: Cumulative Analysis
    print("\n=== Test: Cumulative Analysis ===")
    try:
        driver.execute_script("runCumulativeAnalysis()")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('cumYearPlot').children.length > 0 || document.getElementById('cumYearPlot').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] Cumulative analysis computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 5: Meta-Regression
    print("\n=== Test: Meta-Regression ===")
    try:
        driver.execute_script("runMetaRegression()")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('metaregResults').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] Meta-regression computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 6: LOO Analysis
    print("\n=== Test: Leave-One-Out Analysis ===")
    try:
        driver.execute_script("runLeaveOneOutCorrected()")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('looResults').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] LOO analysis computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 7: GRADE Assessment
    print("\n=== Test: GRADE Assessment ===")
    try:
        driver.execute_script("runGRADEAssessment()")
        time.sleep(1)
        result = driver.execute_script("return document.getElementById('gradeResults').innerHTML.length > 50")
        print(f"  [{'PASS' if result else 'FAIL'}] GRADE assessment computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 8: Cross-disciplinary
    print("\n=== Test: Cross-Disciplinary ===")
    try:
        driver.execute_script("updateCrossDisciplinary()")
        driver.execute_script("document.querySelector('[data-tab=\"crossdisciplinary\"]').click()")
        time.sleep(0.5)
        result = driver.execute_script("return document.getElementById('panel-crossdisciplinary').innerHTML.includes('Economics')")
        print(f"  [{'PASS' if result else 'FAIL'}] Cross-disciplinary content updated")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 9: Code Panel
    print("\n=== Test: Code Export Panel ===")
    try:
        driver.execute_script("updateCodePanel()")
        driver.execute_script("document.querySelector('[data-tab=\"code\"]').click()")
        time.sleep(0.5)
        result = driver.execute_script("return document.getElementById('panel-code').innerHTML.includes('library(metafor)')")
        print(f"  [{'PASS' if result else 'FAIL'}] Code panel updated")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 10: Metaoverfit
    print("\n=== Test: Metaoverfit Assessment ===")
    try:
        # Metaoverfit is now computed automatically and stored in AppState.results
        driver.execute_script("updateMetaoverfitResults()")
        time.sleep(0.5)
        # Check if metaoverfit data is properly computed in AppState.results
        has_data = driver.execute_script("""
            return AppState.results &&
                   AppState.results.metaoverfit &&
                   AppState.results.metaoverfit.k &&
                   AppState.results.metaoverfit.ratio > 0 &&
                   AppState.results.metaoverfit.risk_level
        """)
        if has_data:
            risk = driver.execute_script("return AppState.results.metaoverfit.risk_level")
            ratio = driver.execute_script("return AppState.results.metaoverfit.ratio.toFixed(1)")
            print(f"  [PASS] Metaoverfit computed: {risk} risk (k:p ratio = {ratio})")
        else:
            print(f"  [FAIL] Metaoverfit data not properly computed")
    except Exception as e:
        print(f"  [FAIL] {e}")

    # Test 11: TruthCert Verdict (should be triggered automatically)
    print("\n=== Test: TruthCert Verdict ===")
    try:
        # Wait a bit more for TruthCert analysis to complete
        time.sleep(1.5)
        has_verdict = driver.execute_script("""
            return AppState.truthcert &&
                   AppState.truthcert.verdict &&
                   AppState.truthcert.verdict.verdict
        """)
        if has_verdict:
            verdict = driver.execute_script("return AppState.truthcert.verdict.verdict")
            tier = driver.execute_script("return AppState.truthcert.verdict.tier")
            print(f"  [PASS] TruthCert verdict: {verdict} (Tier {tier})")
        else:
            print(f"  [INFO] TruthCert verdict not auto-triggered (may need manual run)")
    except Exception as e:
        print(f"  [INFO] TruthCert check: {e}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

finally:
    driver.quit()
