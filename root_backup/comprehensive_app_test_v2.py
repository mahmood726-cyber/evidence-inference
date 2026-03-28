"""
Comprehensive NMA Pro v6.2 App Testing - Updated Selectors
"""

import sys
import time
import json
sys.stdout.reconfigure(encoding="utf-8")

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

results = {"passed": [], "failed": [], "skipped": []}

def log(msg, status="INFO"):
    symbols = {"PASS": "[PASS]", "FAIL": "[FAIL]", "INFO": "[INFO]", "SKIP": "[SKIP]"}
    print(f"{symbols.get(status, "[INFO]")} {msg}")

def test_element_exists(driver, selector, name, by=By.CSS_SELECTOR):
    try:
        el = driver.find_element(by, selector)
        if el.is_displayed():
            log(f"{name} - visible", "PASS")
            results["passed"].append(name)
            return True
        else:
            log(f"{name} - hidden", "SKIP")
            results["skipped"].append(name)
            return False
    except NoSuchElementException:
        log(f"{name} - not found", "FAIL")
        results["failed"].append(name)
        return False

def test_button_click(driver, selector, name, wait_after=1):
    try:
        el = driver.find_element(By.CSS_SELECTOR, selector)
        el.click()
        time.sleep(wait_after)
        log(f"{name} - clicked", "PASS")
        results["passed"].append(name)
        return True
    except Exception as e:
        log(f"{name} - failed: {str(e)[:50]}", "FAIL")
        results["failed"].append(name)
        return False

def test_plot_rendered(driver, plot_id, name):
    try:
        plot = driver.find_element(By.ID, plot_id)
        has_svg = len(plot.find_elements(By.CSS_SELECTOR, "svg")) > 0
        has_canvas = len(plot.find_elements(By.CSS_SELECTOR, "canvas")) > 0
        children = plot.find_elements(By.CSS_SELECTOR, "*")
        if has_svg or has_canvas or len(children) > 5:
            log(f"{name} - rendered (svg={has_svg}, canvas={has_canvas})", "PASS")
            results["passed"].append(name)
            return True
        else:
            log(f"{name} - empty", "FAIL")
            results["failed"].append(name)
            return False
    except Exception as e:
        log(f"{name} - error: {str(e)[:50]}", "FAIL")
        results["failed"].append(name)
        return False

def switch_tab(driver, tab_name):
    try:
        tab_btn = driver.find_element(By.CSS_SELECTOR, f'button[data-tab="{tab_name}"]')
        tab_btn.click()
        time.sleep(0.5)
        return True
    except:
        return False

def main():
    print("="*70)
    print("NMA PRO v6.2 - COMPREHENSIVE APP TESTING (v2)")
    print("="*70)

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Edge(options=options)
    driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html")
    time.sleep(3)

    print("
[1] DATA TAB")
    test_button_click(driver, "#loadDemoBtn", "Load Demo Button")
    time.sleep(1)
    rows = driver.find_elements(By.CSS_SELECTOR, "#studyTableBody tr")
    if len(rows) >= 10:
        log(f"Study table ({len(rows)} rows)", "PASS")
        results["passed"].append("Study table")
    else:
        results["failed"].append("Study table")
    test_element_exists(driver, "#effectMeasureSelect", "Effect Measure Selector")

    print("
[2] RUN ANALYSIS")
    test_button_click(driver, "#runAnalysisBtn", "Run Analysis", wait_after=3)

    print("
[3] NETWORK TAB")
    switch_tab(driver, "network")
    time.sleep(1)
    test_plot_rendered(driver, "networkPlot", "Network Graph")

    print("
[4] RESULTS TAB")
    switch_tab(driver, "results")
    time.sleep(1)
    test_plot_rendered(driver, "forestPlot", "Forest Plot")
    test_element_exists(driver, "#leagueTableContainer table", "League Table")

    print("
[5] RANKING TAB")
    switch_tab(driver, "ranking")
    time.sleep(1)
    test_element_exists(driver, "#rankingTableBody tr", "Ranking Table")
    test_plot_rendered(driver, "rankogramPlot", "Rankogram")

    print("
[6] HETEROGENEITY TAB")
    switch_tab(driver, "heterogeneity")
    time.sleep(1)
    try:
        tau2 = driver.find_element(By.ID, "hetTau2").text
        i2 = driver.find_element(By.ID, "hetI2").text
        if tau2 and tau2 != "-":
            log(f"Tau2: {tau2}", "PASS")
            results["passed"].append("Tau2")
        else:
            results["failed"].append("Tau2")
        if i2 and i2 != "-":
            log(f"I2: {i2}", "PASS")
            results["passed"].append("I2")
        else:
            results["failed"].append("I2")
    except Exception as e:
        log(f"Het Stats - error: {str(e)[:50]}", "FAIL")
        results["failed"].append("Het Stats")

    print("
[7] CONSISTENCY TAB")
    switch_tab(driver, "consistency")
    time.sleep(1)
    test_element_exists(driver, "#nodeSplitContainer table", "Node-Split Table")

    print("
[8] PUB BIAS TAB")
    switch_tab(driver, "pubbias")
    time.sleep(1)
    test_plot_rendered(driver, "funnelPlot", "Funnel Plot")

    print("
[9] META-REG TAB")
    switch_tab(driver, "metareg")
    time.sleep(1)
    test_element_exists(driver, "#covariate1Select", "Covariate Selector")

    print("
[10] CINeMA TAB")
    switch_tab(driver, "cinema")
    time.sleep(1)
    test_element_exists(driver, "#cinemaHighCount", "CINeMA Stats")

    print("
[11] SENSITIVITY TAB")
    switch_tab(driver, "sensitivity")
    time.sleep(1)
    test_element_exists(driver, "#runLeaveOneOutBtn", "LOO Button")

    print("
[12] CUMULATIVE TAB")
    switch_tab(driver, "cumulative")
    time.sleep(1)
    test_element_exists(driver, "#runCumulativeBtn", "Cumulative Button")

    print("
[13] EXPORT TAB")
    switch_tab(driver, "export")
    time.sleep(1)
    test_element_exists(driver, "#exportJsonBtn", "Export JSON")
    test_element_exists(driver, "#exportRCodeBtn", "Export R")

    print("
[14] R VALIDATION TAB")
    switch_tab(driver, "rvalidation")
    time.sleep(1)
    try:
        panel = driver.find_element(By.ID, "panel-rvalidation")
        panel_text = panel.text
        if "15" in panel_text:
            log("R Validation panel (15 tests)", "PASS")
            results["passed"].append("R Validation")
        else:
            log(f"R Validation panel text: {panel_text[:100]}", "FAIL")
            results["failed"].append("R Validation")
    except Exception as e:
        log(f"R Validation - error: {str(e)[:50]}", "FAIL")
        results["failed"].append("R Validation")

    print("
[15] THEME TOGGLE")
    test_button_click(driver, "#themeToggle", "Theme Toggle")

    print("
" + "="*70)
    print("SUMMARY")
    print("="*70)
    total = len(results["passed"]) + len(results["failed"])
    print(f"  PASSED:  {len(results['passed'])}/{total}")
    print(f"  FAILED:  {len(results['failed'])}/{total}")
    if results["failed"]:
        print("  Failed:")
        for f in results["failed"]:
            print(f"    - {f}")
    pct = len(results["passed"])/total*100 if total > 0 else 0
    print(f"
  Pass Rate: {pct:.1f}%")

    with open("C:/Users/user/app_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    driver.quit()

if __name__ == "__main__":
    main()
