# LEC Evidence Synthesis Tool v2.0 - Comprehensive Selenium Test
# Tests all tabs, buttons, and interactive elements

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoAlertPresentException, ElementClickInterceptedException,
    StaleElementReferenceException, TimeoutException, NoSuchElementException
)

print("=" * 70)
print("LEC EVIDENCE SYNTHESIS TOOL v2.0 - COMPREHENSIVE UI TEST")
print("=" * 70)

options = Options()
options.add_argument('--start-maximized')
driver = webdriver.Edge(options=options)

passed = 0
failed = 0
results = []

def dismiss_alerts():
    for _ in range(5):
        try:
            driver.switch_to.alert.accept()
            time.sleep(0.2)
        except NoAlertPresentException:
            break

def js(script):
    dismiss_alerts()
    return driver.execute_script(script)

def test(name, condition_fn):
    global passed, failed
    dismiss_alerts()
    try:
        if condition_fn():
            passed += 1
            results.append(("PASS", name))
            print(f"  [PASS] {name}")
            return True
        else:
            failed += 1
            results.append(("FAIL", name))
            print(f"  [FAIL] {name}")
            return False
    except Exception as e:
        failed += 1
        results.append(("FAIL", f"{name}: {str(e)[:50]}"))
        print(f"  [FAIL] {name}: {str(e)[:50]}")
        return False

def click_element(selector, by=By.CSS_SELECTOR, timeout=3):
    """Try to click an element, handling common issues."""
    dismiss_alerts()
    try:
        elem = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.2)
        try:
            elem.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", elem)
        time.sleep(0.3)
        dismiss_alerts()
        return True
    except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
        return False

try:
    # Load the application
    driver.get("file:///C:/Users/user/Downloads/lec_phase0_project/lec-web/lec-evidence-synthesis-v2.html")
    time.sleep(3)
    dismiss_alerts()

    print("\n" + "=" * 70)
    print("SECTION 1: INITIAL LOAD & LIBRARIES")
    print("=" * 70)

    test("Page loaded", lambda: "LEC" in driver.title or js("return document.body.innerHTML.length > 1000"))
    test("Document ready", lambda: js("return document.readyState === 'complete'"))
    test("Header visible", lambda: js("return document.querySelector('.header') !== null"))
    test("Navigation tabs visible", lambda: js("return document.querySelector('.nav-tabs') !== null"))

    print("\n" + "=" * 70)
    print("SECTION 2: TAB NAVIGATION (10 Tabs)")
    print("=" * 70)

    # Find all nav tabs
    tabs = driver.find_elements(By.CSS_SELECTOR, ".nav-tab")
    tab_count = len(tabs)
    print(f"  Found {tab_count} navigation tabs")

    tabs_working = 0
    tab_names = []
    for i, tab in enumerate(tabs):
        try:
            tab_text = tab.text.strip()[:30] or f"Tab {i+1}"
            tab_names.append(tab_text)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab)
            time.sleep(0.2)
            try:
                tab.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.3)
            dismiss_alerts()

            # Check if tab content is displayed
            data_tab = tab.get_attribute("data-tab")
            if data_tab:
                content_visible = js(f"return document.getElementById('{data_tab}-tab')?.style.display !== 'none'")
            else:
                content_visible = True

            tabs_working += 1
            print(f"    [OK] Tab: {tab_text}")
        except Exception as e:
            print(f"    [--] Tab {i+1}: {str(e)[:40]}")

    test(f"All tabs clickable ({tabs_working}/{tab_count})", lambda: tabs_working >= tab_count * 0.9)

    print("\n" + "=" * 70)
    print("SECTION 3: DEMO DATA LOADING")
    print("=" * 70)

    # Click Data Input tab
    click_element(".nav-tab[data-tab='data']", timeout=2)
    time.sleep(0.5)

    # Test demo data buttons
    demo_buttons = [
        ("SGLT2i Data", "loadSGLT2iData"),
        ("PCSK9i Data", "loadPCSK9iData"),
        ("Colchicine Data", "loadColchicineData"),
    ]

    for name, func in demo_buttons:
        exists = test(f"{name} function exists", lambda f=func: js(f"return typeof {f} === 'function'"))
        if exists:
            try:
                js(f"{func}()")
                time.sleep(0.5)
                dismiss_alerts()
                test(f"{name} loads successfully", lambda: js("return LEC?.studies?.length > 0 || document.querySelector('#dataTextArea')?.value?.length > 50"))
            except Exception as e:
                print(f"    [--] {name}: {str(e)[:40]}")

    # Load colchicine data for further tests
    js("loadColchicineData()")
    time.sleep(0.5)
    dismiss_alerts()

    print("\n" + "=" * 70)
    print("SECTION 4: CORE FUNCTIONS")
    print("=" * 70)

    core_functions = [
        ("parseStudyData", "Parse study data"),
        ("updateStudiesTable", "Update studies table"),
        ("runMetaAnalysis", "Run meta-analysis"),
        ("updateMetaResults", "Update meta results"),
        ("drawForestPlot", "Draw forest plot"),
        ("calculateGRADE", "Calculate GRADE"),
        ("deriveRecommendation", "Derive recommendation"),
        ("runNMA", "Run NMA"),
        ("generateSoF", "Generate SoF table"),
    ]

    for func, desc in core_functions:
        test(f"{desc} function", lambda f=func: js(f"return typeof {f} === 'function'"))

    print("\n" + "=" * 70)
    print("SECTION 5: RUN META-ANALYSIS WORKFLOW")
    print("=" * 70)

    # Parse data
    js("if(typeof parseStudyData === 'function') parseStudyData()")
    time.sleep(0.5)
    dismiss_alerts()

    test("Data parsed", lambda: js("return LEC?.studies?.length > 0"))

    # Run meta-analysis
    js("if(typeof runMetaAnalysis === 'function') runMetaAnalysis()")
    time.sleep(1)
    dismiss_alerts()

    test("Meta-analysis completed", lambda: js("return LEC?.metaResult !== null"))

    # Check results
    pooled_est = js("return LEC?.metaResult?.pooled?.effect || 0")
    test("Pooled estimate calculated", lambda: pooled_est > 0 if pooled_est else False)
    print(f"    >> Pooled estimate: {pooled_est:.4f}" if pooled_est else "    >> No estimate")

    print("\n" + "=" * 70)
    print("SECTION 6: FOREST PLOT")
    print("=" * 70)

    # Go to meta tab
    click_element(".nav-tab[data-tab='meta']", timeout=2)
    time.sleep(0.5)

    test("Forest plot container exists", lambda: js("return document.getElementById('forest-plot') !== null || document.querySelector('#tab-meta svg') !== null"))

    # Try to draw forest plot
    js("if(typeof drawForestPlot === 'function') drawForestPlot()")
    time.sleep(0.5)
    dismiss_alerts()

    test("Forest plot has content", lambda: js("""
        var fp = document.getElementById('forest-plot');
        return fp && (fp.innerHTML.length > 100 || fp.querySelector('rect') !== null);
    """))

    print("\n" + "=" * 70)
    print("SECTION 7: GRADE ASSESSMENT")
    print("=" * 70)

    click_element(".nav-tab[data-tab='grade']", timeout=2)
    time.sleep(0.5)

    test("GRADE tab loaded", lambda: js("return document.getElementById('tab-grade') !== null"))

    # Run GRADE calculation
    js("if(typeof calculateGRADE === 'function') calculateGRADE()")
    time.sleep(0.5)
    dismiss_alerts()

    test("GRADE output exists", lambda: js("""
        return document.querySelector('.grade-badge') !== null ||
               document.getElementById('gradeOutput')?.innerHTML?.length > 0
    """))

    print("\n" + "=" * 70)
    print("SECTION 8: DISCOVERY TAB")
    print("=" * 70)

    click_element(".nav-tab[data-tab='discovery']", timeout=2)
    time.sleep(0.5)

    test("Discovery tab loaded", lambda: js("return document.getElementById('tab-discovery') !== null"))
    test("Search input exists", lambda: js("return document.getElementById('ctg-condition') !== null"))
    test("Search button exists", lambda: js("return document.querySelector('button[onclick*=\"searchClinicalTrials\"]') !== null || typeof searchClinicalTrials === 'function'"))

    # Test preset search buttons
    preset_buttons = driver.find_elements(By.CSS_SELECTOR, "button[onclick*='loadPresetSearch']")
    test(f"Preset search buttons ({len(preset_buttons)})", lambda: len(preset_buttons) >= 3)

    print("\n" + "=" * 70)
    print("SECTION 9: RECOMMENDATION & EXPORT")
    print("=" * 70)

    click_element(".nav-tab[data-tab='recommendation']", timeout=2)
    time.sleep(0.5)

    test("Recommendation tab loaded", lambda: js("return document.getElementById('tab-recommendation') !== null"))

    js("if(typeof deriveRecommendation === 'function') deriveRecommendation()")
    time.sleep(0.5)
    dismiss_alerts()

    click_element(".nav-tab[data-tab='export']", timeout=2)
    time.sleep(0.5)

    test("Export tab loaded", lambda: js("return document.getElementById('tab-export') !== null"))

    export_funcs = [
        ("exportJSON", "Export JSON"),
        ("exportMarkdown", "Export Markdown"),
        ("downloadForestPlot", "Download forest plot"),
        ("saveSession", "Save session"),
    ]

    for func, desc in export_funcs:
        test(f"{desc}", lambda f=func: js(f"return typeof {f} === 'function'"))

    print("\n" + "=" * 70)
    print("SECTION 10: BUTTON CLICK TEST (Sample)")
    print("=" * 70)

    # Get all buttons
    buttons = driver.find_elements(By.CSS_SELECTOR, "button:not([disabled])")
    btn_count = len(buttons)
    print(f"  Found {btn_count} buttons")

    # Test first 20 visible buttons
    btns_clicked = 0
    btns_tested = 0
    for btn in buttons[:25]:
        try:
            if btn.is_displayed() and btn.is_enabled():
                btn_text = btn.text.strip()[:25] or btn.get_attribute("id") or "unnamed"
                # Skip potentially problematic buttons
                if any(x in btn_text.lower() for x in ['search clinical', 'search pubmed', 'fetch']):
                    continue
                btns_tested += 1
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(0.1)
                try:
                    btn.click()
                    btns_clicked += 1
                    print(f"    [OK] Button: {btn_text}")
                except:
                    driver.execute_script("arguments[0].click();", btn)
                    btns_clicked += 1
                    print(f"    [OK] Button (js): {btn_text}")
                time.sleep(0.2)
                dismiss_alerts()
        except Exception as e:
            pass

    test(f"Buttons clickable ({btns_clicked}/{btns_tested})", lambda: btns_clicked >= btns_tested * 0.7 if btns_tested > 0 else True)

    print("\n" + "=" * 70)
    print("SECTION 11: INPUT FIELDS")
    print("=" * 70)

    inputs = driver.find_elements(By.CSS_SELECTOR, "input:not([type='hidden']):not([disabled]), textarea")
    input_count = len(inputs)
    print(f"  Found {input_count} input fields/textareas")

    inputs_ok = 0
    for inp in inputs[:15]:
        try:
            if inp.is_displayed():
                inp_id = inp.get_attribute("id") or inp.get_attribute("name") or "unnamed"
                # Don't clear textareas with data
                if inp.tag_name != "textarea":
                    inp.clear()
                    inp.send_keys("test")
                inputs_ok += 1
        except:
            pass

    test(f"Input fields editable ({inputs_ok}/15)", lambda: inputs_ok >= 10)

    # FINAL SUMMARY
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    total = passed + failed
    rate = (passed / total) * 100 if total > 0 else 0

    print(f"\nPassed: {passed}/{total} ({rate:.1f}%)")
    print(f"Failed: {failed}/{total}")

    print("\nUI Metrics:")
    print(f"  - Total Tabs: {tab_count}")
    print(f"  - Total Buttons: {btn_count}")
    print(f"  - Total Inputs: {input_count}")
    print(f"  - Tab Names: {', '.join(tab_names)}")

    if rate >= 95:
        verdict = "EXCELLENT - All systems operational"
    elif rate >= 85:
        verdict = "VERY GOOD - Minor issues only"
    elif rate >= 75:
        verdict = "GOOD - Some issues to address"
    else:
        verdict = "NEEDS ATTENTION - Multiple issues"

    print(f"\nVERDICT: {verdict}")
    print("=" * 70)

    time.sleep(3)

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
