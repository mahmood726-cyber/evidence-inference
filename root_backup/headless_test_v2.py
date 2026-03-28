#!/usr/bin/env python3
"""Headless test with better options"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import subprocess
import os

print("=" * 70)
print("HEADLESS BROWSER TEST V2")
print("=" * 70)

# Kill any existing chrome processes
subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], capture_output=True)
subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'], capture_output=True)
time.sleep(2)

options = Options()
# Essential headless options
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-extensions")
options.add_argument("--disable-background-networking")
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")
options.add_argument("--silent")

# Set Chrome binary path explicitly
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
for path in chrome_paths:
    if os.path.exists(path):
        options.binary_location = path
        print(f"Using Chrome: {path}")
        break

driver_path = r"C:\Users\user\.cache\selenium\chromedriver\win64\143.0.7499.192\chromedriver.exe"
print(f"Using driver: {driver_path}")

results = {"passed": 0, "failed": 0}

try:
    service = Service(driver_path)
    service.start()
    print("Driver service started")

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    print("Browser started!")

    # Load page
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)
    print(f"Page loaded: {driver.title}\n")

    # ==========================================
    # TESTS
    # ==========================================

    # 1. Demo datasets
    print("--- DEMO DATASETS ---")
    demos = driver.execute_script("return Object.keys(DEMO_DATASETS);")
    print(f"  Found {len(demos)} demo datasets")
    for d in demos[:5]:
        print(f"    - {d}")
    results["passed"] += 1

    # 2. Critical gap functions
    print("\n--- CRITICAL GAP FUNCTIONS ---")
    gap_fns = ["calculateMH_OR", "calculatePeto_OR", "testExcessSignificance",
               "renderQQPlot", "influenceDiagnostics"]
    for fn in gap_fns:
        exists = driver.execute_script(f"return typeof {fn} === 'function';")
        if exists:
            print(f"  [PASS] {fn}()")
            results["passed"] += 1
        else:
            print(f"  [FAIL] {fn}()")
            results["failed"] += 1

    # 3. Tau2 estimators
    print("\n--- TAU2 ESTIMATORS ---")
    tau2_methods = ["DL", "REML", "ML", "PM", "HS", "SJ", "HE", "EB"]
    for m in tau2_methods:
        exists = driver.execute_script(f"return typeof estimateTau2_{m} === 'function';")
        if exists:
            print(f"  [PASS] estimateTau2_{m}()")
            results["passed"] += 1
        else:
            print(f"  [FAIL] estimateTau2_{m}()")
            results["failed"] += 1

    # 4. TES validation
    print("\n--- TES VALIDATION vs R ---")
    tes = driver.execute_script("""
        const yi = [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547,
                    -0.786116, -1.620898, 0.011952, -0.469418, -1.371345,
                    -0.339359, 0.445913, -0.017314];
        const vi = [0.325585, 0.194581, 0.415368, 0.020010, 0.051210,
                    0.006906, 0.223017, 0.003962, 0.056434, 0.073025,
                    0.012412, 0.532506, 0.071405];
        if (typeof testExcessSignificance === 'function') {
            return testExcessSignificance(yi, vi);
        }
        return null;
    """)
    if tes and tes.get('observed') == 8:
        print(f"  [PASS] TES observed={tes['observed']} (R=8)")
        print(f"         TES expected={tes.get('expected', 'N/A'):.2f} (R~6.1)")
        results["passed"] += 1
    else:
        print(f"  [FAIL] TES: {tes}")
        results["failed"] += 1

    # 5. Plot functions
    print("\n--- PLOT FUNCTIONS ---")
    plots = ["renderForestPlot", "renderFunnelPlot", "renderQQPlot"]
    for fn in plots:
        exists = driver.execute_script(f"return typeof {fn} === 'function';")
        if exists:
            print(f"  [PASS] {fn}()")
            results["passed"] += 1
        else:
            print(f"  [FAIL] {fn}()")
            results["failed"] += 1

    # Summary
    print("\n" + "=" * 70)
    total = results["passed"] + results["failed"]
    pct = (results["passed"] / max(total, 1)) * 100
    print(f"RESULTS: {results['passed']}/{total} passed ({pct:.0f}%)")
    print("=" * 70)

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    try:
        driver.quit()
    except:
        pass
    try:
        service.stop()
    except:
        pass
    print("\nDone.")
