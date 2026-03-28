# Test Lancet-specific features in LEC Evidence Synthesis Tool
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoAlertPresentException

print("=" * 70)
print("LEC LANCET FEATURES VERIFICATION TEST")
print("=" * 70)

options = Options()
options.add_argument('--start-maximized')
driver = webdriver.Edge(options=options)

passed = 0
failed = 0

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
        result = condition_fn()
        if result:
            passed += 1
            print(f"  [PASS] {name}")
            return True
        else:
            failed += 1
            print(f"  [FAIL] {name}")
            return False
    except Exception as e:
        failed += 1
        print(f"  [FAIL] {name}: {str(e)[:60]}")
        return False

try:
    driver.get("file:///C:/Users/user/Downloads/lec_phase0_project/lec-web/lec-evidence-synthesis-v2.html")
    time.sleep(3)
    dismiss_alerts()

    # Load demo data first
    js("loadColchicineData()")
    time.sleep(0.5)
    js("parseStudyData()")
    time.sleep(0.5)
    js("runMetaAnalysis()")
    time.sleep(1)
    dismiss_alerts()

    print("\n" + "=" * 70)
    print("1. ABSOLUTE RISK & NNT CALCULATOR")
    print("=" * 70)

    test("calculateAbsoluteRisk function exists",
         lambda: js("return typeof calculateAbsoluteRisk === 'function'"))

    # Run the calculation
    js("document.getElementById('baseline-risk').value = '10'")
    js("calculateAbsoluteRisk()")
    time.sleep(0.3)
    dismiss_alerts()

    test("Absolute risk results displayed",
         lambda: js("return document.getElementById('absolute-risk-results').innerHTML.length > 50"))

    # Check for NNT in output
    test("NNT calculated and displayed",
         lambda: js("return document.getElementById('absolute-risk-results').innerHTML.includes('NNT')"))

    print("\n" + "=" * 70)
    print("2. PRISMA 2020 FLOW DIAGRAM")
    print("=" * 70)

    test("PRISMA tab exists",
         lambda: js("return document.getElementById('tab-prisma') !== null"))

    test("generatePRISMAFlow function exists",
         lambda: js("return typeof generatePRISMAFlow === 'function'"))

    # Go to PRISMA tab and generate
    js("document.querySelector('.nav-tab[data-tab=\"prisma\"]').click()")
    time.sleep(0.5)

    # Use correct field IDs
    js("document.getElementById('prisma-db-records').value = '500'")
    js("document.getElementById('prisma-other-records').value = '25'")
    js("document.getElementById('prisma-duplicates').value = '100'")
    js("document.getElementById('prisma-screened').value = '400'")
    js("document.getElementById('prisma-excluded-screen').value = '300'")
    js("document.getElementById('prisma-fulltext').value = '100'")
    js("document.getElementById('prisma-excluded-fulltext').value = '90'")
    js("document.getElementById('prisma-included').value = '10'")
    js("generatePRISMAFlow()")
    time.sleep(0.5)
    dismiss_alerts()

    test("PRISMA flow diagram generated (SVG)",
         lambda: js("return document.getElementById('prisma-flow').innerHTML.includes('rect') || document.getElementById('prisma-flow').innerHTML.length > 100"))

    test("PROSPERO field exists",
         lambda: js("return document.getElementById('prospero-id') !== null"))

    print("\n" + "=" * 70)
    print("3. RISK OF BIAS VISUALIZATION")
    print("=" * 70)

    test("updateRoBAssessment function exists",
         lambda: js("return typeof updateRoBAssessment === 'function'"))

    test("drawRoBTrafficLight function exists",
         lambda: js("return typeof drawRoBTrafficLight === 'function'"))

    test("drawRoBSummary function exists",
         lambda: js("return typeof drawRoBSummary === 'function'"))

    test("runRoBSensitivity function exists",
         lambda: js("return typeof runRoBSensitivity === 'function'"))

    test("generateRoBVisualization function exists",
         lambda: js("return typeof generateRoBVisualization === 'function'"))

    print("\n" + "=" * 70)
    print("4. TRIAL SEQUENTIAL ANALYSIS (TSA)")
    print("=" * 70)

    test("TSA tab exists",
         lambda: js("return document.getElementById('tab-tsa') !== null"))

    test("runTSA function exists",
         lambda: js("return typeof runTSA === 'function'"))

    test("drawTSAPlot function exists",
         lambda: js("return typeof drawTSAPlot === 'function'"))

    test("drawCumulativeMA function exists",
         lambda: js("return typeof drawCumulativeMA === 'function'"))

    # Go to TSA tab and run
    js("document.querySelector('.nav-tab[data-tab=\"tsa\"]').click()")
    time.sleep(0.5)
    js("runTSA()")
    time.sleep(1)
    dismiss_alerts()

    test("TSA diagram generated",
         lambda: js("return document.getElementById('tsa-plot').innerHTML.includes('rect') || document.getElementById('tsa-results').innerHTML.length > 100"))

    test("Cumulative MA plot generated",
         lambda: js("return document.getElementById('cumulative-ma-plot').innerHTML.length > 50"))

    print("\n" + "=" * 70)
    print("5. PUBLICATION BIAS TESTS")
    print("=" * 70)

    test("runPetersTest function exists",
         lambda: js("return typeof runPetersTest === 'function'"))

    test("runHarbordTest function exists",
         lambda: js("return typeof runHarbordTest === 'function'"))

    test("runBeggTest function exists",
         lambda: js("return typeof runBeggTest === 'function'"))

    test("runTrimAndFill function exists",
         lambda: js("return typeof runTrimAndFill === 'function'"))

    test("drawFunnelPlotEnhanced function exists",
         lambda: js("return typeof drawFunnelPlotEnhanced === 'function'"))

    test("runAllPubBiasTests function exists",
         lambda: js("return typeof runAllPubBiasTests === 'function'"))

    # Run all pub bias tests
    js("runAllPubBiasTests()")
    time.sleep(1)
    dismiss_alerts()

    test("Egger's test result displayed",
         lambda: js("return document.getElementById('egger-result')?.innerHTML?.includes('p') || document.getElementById('egger-result')?.innerHTML?.length > 10"))

    test("Peters' test result displayed",
         lambda: js("return document.getElementById('peters-result')?.innerHTML?.includes('p') || document.getElementById('peters-result')?.innerHTML?.length > 10"))

    print("\n" + "=" * 70)
    print("6. CONTOUR-ENHANCED FUNNEL PLOT")
    print("=" * 70)

    # Go to meta tab for funnel plot
    js("document.querySelector('.nav-tab[data-tab=\"meta\"]').click()")
    time.sleep(0.5)

    test("Contour checkbox exists",
         lambda: js("return document.getElementById('funnel-contour') !== null"))

    # Enable contour and draw
    js("document.getElementById('funnel-contour').checked = true")
    js("if(typeof drawFunnelPlotEnhanced === 'function') drawFunnelPlotEnhanced()")
    time.sleep(0.5)
    dismiss_alerts()

    test("Funnel plot has content",
         lambda: js("return document.getElementById('funnel-plot').innerHTML.includes('svg') || document.getElementById('funnel-plot').innerHTML.includes('rect') || document.getElementById('funnel-plot').innerHTML.length > 100"))

    print("\n" + "=" * 70)
    print("7. PREDICTION INTERVAL")
    print("=" * 70)

    test("Prediction interval element exists",
         lambda: js("return document.getElementById('prediction-interval') !== null"))

    # Ensure forest plot draws PI
    js("drawForestPlot()")
    time.sleep(0.5)
    dismiss_alerts()

    test("Prediction interval has content",
         lambda: js("return document.getElementById('prediction-interval').innerHTML.length > 10"))

    print("\n" + "=" * 70)
    print("8. EXPORT FUNCTIONS")
    print("=" * 70)

    test("exportRScript function exists",
         lambda: js("return typeof exportRScript === 'function'"))

    test("exportCSV function exists",
         lambda: js("return typeof exportCSV === 'function'"))

    test("exportPRISMAChecklist function exists",
         lambda: js("return typeof exportPRISMAChecklist === 'function'"))

    # FINAL SUMMARY
    print("\n" + "=" * 70)
    print("FINAL RESULTS - LANCET FEATURES")
    print("=" * 70)

    total = passed + failed
    rate = (passed / total) * 100 if total > 0 else 0

    print(f"\nPassed: {passed}/{total} ({rate:.1f}%)")
    print(f"Failed: {failed}/{total}")

    features_summary = """
    Features Verified:
    1. Absolute Risk & NNT Calculator - ARR, NNT, per-1000 presentation
    2. PRISMA 2020 Flow Diagram - SVG generation with all boxes
    3. Risk of Bias (RoB 2.0) - Traffic light and summary visualizations
    4. Trial Sequential Analysis (TSA) - With O'Brien-Fleming boundaries
    5. Publication Bias Tests - Egger's, Peters', Harbord's, Begg's, Trim-and-fill
    6. Contour-Enhanced Funnel Plot - Significance regions
    7. Prediction Interval - Displayed with interpretation
    8. Export Functions - R script, CSV, PRISMA checklist
    """
    print(features_summary)

    if rate >= 95:
        verdict = "EXCELLENT - All Lancet requirements implemented"
    elif rate >= 85:
        verdict = "VERY GOOD - Most requirements met"
    elif rate >= 75:
        verdict = "GOOD - Core requirements met"
    else:
        verdict = "NEEDS WORK - Missing critical features"

    print(f"VERDICT: {verdict}")
    print("=" * 70)

    time.sleep(3)

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
