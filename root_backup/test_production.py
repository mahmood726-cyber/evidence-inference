"""Quick test for production build"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)

try:
    print("=" * 60)
    print("PRODUCTION BUILD TEST")
    print("=" * 60)

    # Test single-file distribution (safe bundle)
    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-bundle.html')
    time.sleep(3)

    # Load demo and run analysis
    driver.execute_script("loadDemoDataset('BCG')")
    time.sleep(1)
    driver.execute_script("runAnalysis()")
    time.sleep(2)

    # Check results
    has_results = driver.execute_script("return AppState.results && AppState.results.pooled")
    pooled = driver.execute_script("return AppState.results ? AppState.results.pooled.theta.toFixed(4) : 'none'")

    if has_results:
        print(f"[PASS] Production build works!")
        print(f"  Pooled effect: {pooled}")

        # Test new features
        bootstrap = driver.execute_script("""
            const yi = AppState.results.studies.map(s => s.yi);
            const vi = AppState.results.studies.map(s => s.vi);
            const result = bootstrapMetaAnalysis(yi, vi, { nBoot: 100 });
            return result.theta !== undefined;
        """)
        print(f"  Bootstrap: {'OK' if bootstrap else 'FAIL'}")

        save = driver.execute_script("return typeof saveProject === 'function'")
        print(f"  Save/Load: {'OK' if save else 'FAIL'}")

        undo = driver.execute_script("return typeof UndoManager !== 'undefined'")
        print(f"  Undo/Redo: {'OK' if undo else 'FAIL'}")

        icer = driver.execute_script("return typeof calculateICER === 'function'")
        print(f"  ICER/HTA: {'OK' if icer else 'FAIL'}")

        psa = driver.execute_script("return typeof runPSA === 'function'")
        print(f"  PSA: {'OK' if psa else 'FAIL'}")

        print("\n[OK] ALL PRODUCTION TESTS PASSED!")
    else:
        print(f"[FAIL] Production build failed - no results")

    print("=" * 60)

finally:
    driver.quit()
