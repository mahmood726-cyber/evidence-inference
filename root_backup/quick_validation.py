#\!/usr/bin/env python3
"""Full validation test"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

print("=" * 70)
print("FULL VALIDATION TEST")
print("=" * 70)

driver_path = r"C:\Users\user\.wdm\drivers\chromedriver\win64\143.0.7499.192\chromedriver-win32\chromedriver.exe"
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

results = {"passed": 0, "failed": 0}

def log_test(name, passed):
    status = "PASS" if passed else "FAIL"
    if passed: results["passed"] += 1
    else: results["failed"] += 1
    print(f"  [{status}] {name}")

try:
    driver.get("file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
    time.sleep(3)

    # Test demo datasets
    demo_keys = driver.execute_script("return Object.keys(DEMO_DATASETS);")
    print(f"\n--- DEMO DATASETS ({len(demo_keys)} available) ---")
    for key in demo_keys:
        result = driver.execute_script(f'try {{ loadDemoDataset("{key}"); return true; }} catch(e) {{ return false; }}')
        log_test(f"Load {key}", result)

    # Test plot rendering
    print("\n--- PLOT RENDERING ---")
    driver.execute_script("""
        window.yi = [-0.889311, -1.585389, -1.348073];
        window.vi = [0.325585, 0.194581, 0.415368];
        window.names = ["Study 1", "Study 2", "Study 3"];
        window.tau2 = estimateTau2_REML(window.yi, window.vi);
        window.pooled = calculatePooledEstimate(window.yi, window.vi, window.tau2.tau2);
    """)

    plots = ["Forest", "Funnel", "Baujat", "Radial", "DOI"]
    for p in plots:
        code = f"render{p}Plot(window.yi, window.vi, window.names" + (", window.pooled, window.tau2.tau2)" if p == "Forest" else ", window.pooled.theta)" if p == "Funnel" else ")")
        result = driver.execute_script(f"try {{ {code}; return true; }} catch(e) {{ return false; }}")
        log_test(f"Render {p}", result)

    # Summary
    print("\n" + "=" * 70)
    total = results["passed"] + results["failed"]
    pct = (results["passed"] / total) * 100
    print(f"Tests: {results['passed']}/{total} ({pct:.1f}%)")
    if pct >= 95: print("VERDICT: EXCELLENT")
    print("=" * 70)

finally:
    driver.quit()
