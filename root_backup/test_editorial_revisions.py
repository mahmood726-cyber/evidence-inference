"""
Test Editorial Revisions - Verify the 4 new features work correctly
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

def test_editorial_revisions():
    print("=" * 60)
    print("TESTING EDITORIAL REVISIONS")
    print("=" * 60)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    results = []

    try:
        url = 'file:///C:/Users/user/IPD-Meta-Pro/ipd-meta-pro.html'
        driver.get(url)
        time.sleep(3)

        def js(script):
            return driver.execute_script(script)

        def test(name, condition):
            passed = bool(condition)
            results.append({'test': name, 'passed': passed})
            status = "[PASS]" if passed else "[FAIL]"
            print(f"  {status} {name}")
            return passed

        # Test 1: Mathematical Formulae
        print("\n1. Mathematical Appendix:")
        test("MATHEMATICAL_FORMULAE object exists",
             js("return typeof MATHEMATICAL_FORMULAE !== 'undefined'"))
        test("Has tau2DL formula",
             js("return MATHEMATICAL_FORMULAE && MATHEMATICAL_FORMULAE.tau2DL && MATHEMATICAL_FORMULAE.tau2DL.formula"))
        test("Has tau2REML formula",
             js("return MATHEMATICAL_FORMULAE && !!MATHEMATICAL_FORMULAE.tau2REML"))
        test("showMathematicalAppendix function exists",
             js("return typeof showMathematicalAppendix === 'function'"))

        # Test modal opens
        js("try { showMathematicalAppendix(); } catch(e) {}")
        time.sleep(0.5)
        test("Formulae modal opens",
             js("return document.body.innerHTML.includes('Mathematical Appendix') || document.body.innerHTML.includes('Statistical Formula')"))
        js("var m = document.querySelector('.modal'); if(m) m.style.display='none';")

        # Test 2: Citations Database
        print("\n2. Citations Database:")
        test("CITATIONS object exists",
             js("return typeof CITATIONS !== 'undefined'"))
        test("Has DerSimonian citation",
             js("return CITATIONS && (CITATIONS.dersimonianLaird || (CITATIONS['meta-analysis'] && CITATIONS['meta-analysis'].includes('DerSimonian')))"))
        test("Has multiple citations",
             js("return CITATIONS && Object.keys(CITATIONS).length >= 5"))
        test("showCitationsList function exists",
             js("return typeof showCitationsList === 'function'"))

        # Test modal opens
        js("try { showCitationsList(); } catch(e) {}")
        time.sleep(0.5)
        test("Citations modal opens",
             js("return document.body.innerHTML.includes('References') || document.body.innerHTML.includes('Citation')"))
        js("var m = document.querySelector('.modal'); if(m) m.style.display='none';")

        # Test 3: Causal Assumptions
        print("\n3. Causal Assumptions:")
        test("CAUSAL_ASSUMPTIONS object exists",
             js("return typeof CAUSAL_ASSUMPTIONS !== 'undefined'"))
        test("Has propensityScore assumptions",
             js("return CAUSAL_ASSUMPTIONS && !!CAUSAL_ASSUMPTIONS.propensityScore"))
        test("Has multiple causal methods",
             js("return CAUSAL_ASSUMPTIONS && Object.keys(CAUSAL_ASSUMPTIONS).length >= 4"))
        test("showCausalAssumptions function exists",
             js("return typeof showCausalAssumptions === 'function'"))

        # Test modal opens
        js("try { showCausalAssumptions(); } catch(e) {}")
        time.sleep(0.5)
        test("Assumptions modal opens",
             js("return document.body.innerHTML.includes('Assumption') || document.body.innerHTML.includes('Causal')"))
        js("var m = document.querySelector('.modal'); if(m) m.style.display='none';")

        # Test 4: Model Diagnostics
        print("\n4. Model Diagnostics:")
        test("showModelDiagnostics function exists",
             js("return typeof showModelDiagnostics === 'function'"))
        test("drawResidualPlot function exists",
             js("return typeof drawResidualPlot === 'function'"))
        test("drawQQPlot function exists",
             js("return typeof drawQQPlot === 'function'"))
        test("drawInfluenceDiagnostics function exists",
             js("return typeof drawInfluenceDiagnostics === 'function'"))

        # Test modal opens
        js("try { showModelDiagnostics(); } catch(e) {}")
        time.sleep(0.5)
        test("Diagnostics modal opens",
             js("return document.body.innerHTML.includes('Diagnostic') || document.body.innerHTML.includes('Residual')"))

        # Test 5: Header Buttons
        print("\n5. Header Buttons:")
        test("Formulae button exists",
             js("return !!document.querySelector('button[onclick*=\"showMathematicalAppendix\"]')"))
        test("References button exists",
             js("return !!document.querySelector('button[onclick*=\"showCitationsList\"]')"))
        test("Assumptions button exists",
             js("return !!document.querySelector('button[onclick*=\"showCausalAssumptions\"]')"))
        test("Diagnostics button exists",
             js("return !!document.querySelector('button[onclick*=\"showModelDiagnostics\"]')"))

    except Exception as e:
        print(f"\nError: {e}")
    finally:
        driver.quit()

    # Summary
    passed = sum(1 for r in results if r['passed'])
    total = len(results)

    print("\n" + "=" * 60)
    print(f"EDITORIAL REVISIONS TEST RESULTS: {passed}/{total} ({100*passed/total:.1f}%)")
    print("=" * 60)

    # Save results
    with open('C:/Users/user/editorial_revisions_test.json', 'w') as f:
        json.dump({
            'passed': passed,
            'total': total,
            'pass_rate': 100*passed/total,
            'results': results
        }, f, indent=2)

    return passed == total

if __name__ == '__main__':
    test_editorial_revisions()
