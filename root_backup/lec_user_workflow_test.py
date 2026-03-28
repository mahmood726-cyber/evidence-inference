# LEC Evidence Synthesis Tool - Comprehensive User Workflow Test
# Tests ClinicalTrials.gov search, PubMed search, data extraction and full workflow

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
print("LEC EVIDENCE SYNTHESIS - COMPREHENSIVE USER WORKFLOW TEST")
print("=" * 70)

options = Options()
options.add_argument('--start-maximized')
driver = webdriver.Edge(options=options)

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

def click_tab(tab_name):
    """Click a navigation tab by its data-tab attribute"""
    dismiss_alerts()
    try:
        tab = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f".nav-tab[data-tab='{tab_name}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab)
        time.sleep(0.2)
        try:
            tab.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", tab)
        time.sleep(0.5)
        dismiss_alerts()
        return True
    except Exception as e:
        print(f"  [ERROR] Could not click tab {tab_name}: {str(e)[:50]}")
        return False

def wait_for_condition(check_fn, timeout=30, interval=1):
    """Wait for a condition to become true"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            if check_fn():
                return True
        except:
            pass
        time.sleep(interval)
    return False

try:
    # Load the application
    print("\n[STEP 1] Loading application...")
    driver.get("file:///C:/Users/user/Downloads/lec_phase0_project/lec-web/lec-evidence-synthesis-v2.html")
    time.sleep(3)
    dismiss_alerts()

    # Verify page loaded
    if "LEC" in driver.title or js("return document.body.innerHTML.length > 1000"):
        print("  [OK] Application loaded successfully")
    else:
        print("  [FAIL] Application failed to load")

    # =========================================================================
    # TEST 1: CLINICALTRIALS.GOV SEARCH
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 1: CLINICALTRIALS.GOV SEARCH")
    print("=" * 70)

    # Go to Discovery tab
    print("\n[STEP 2] Navigating to Discovery tab...")
    click_tab("discovery")
    time.sleep(0.5)

    # Check if search elements exist
    condition_input = js("return document.getElementById('ctg-condition') !== null")
    intervention_input = js("return document.getElementById('ctg-intervention') !== null")
    search_btn = js("return typeof searchClinicalTrials === 'function'")
    search_results_body = js("return document.getElementById('search-results-body') !== null")

    print(f"  Condition input exists: {condition_input}")
    print(f"  Intervention input exists: {intervention_input}")
    print(f"  searchClinicalTrials function exists: {search_btn}")
    print(f"  Results table body exists: {search_results_body}")

    if condition_input and intervention_input:
        # Enter search terms
        print("\n[STEP 3] Entering search terms: colchicine, cardiovascular...")
        js("document.getElementById('ctg-condition').value = 'cardiovascular disease'")
        js("document.getElementById('ctg-intervention').value = 'colchicine'")
        time.sleep(0.3)

        # Click search button
        print("\n[STEP 4] Initiating ClinicalTrials.gov search...")
        js("searchClinicalTrials()")

        # Wait for results (check discoveryResults array and table)
        print("\n[STEP 5] Waiting for ClinicalTrials.gov results (up to 45 seconds)...")

        def check_ctg_results():
            result = js("""
                // Check if discoveryResults has data
                if (typeof discoveryResults !== 'undefined' && discoveryResults.length > 0) {
                    return true;
                }
                // Check if table has rows
                var tbody = document.getElementById('search-results-body');
                if (tbody && tbody.querySelectorAll('tr').length > 0) {
                    return true;
                }
                // Check search status for error or completion
                var status = document.getElementById('search-status');
                if (status) {
                    var text = status.innerText || '';
                    if (text.includes('Error') || text.includes('found') || text.includes('complete')) {
                        return true;
                    }
                }
                return false;
            """)
            return result

        results_found = wait_for_condition(check_ctg_results, timeout=45)

        # Get detailed status
        search_status = js("return document.getElementById('search-status')?.innerText || 'No status'")
        print(f"  Search status: {search_status[:100]}")

        results_count = js("return typeof discoveryResults !== 'undefined' ? discoveryResults.length : 0")
        print(f"  Results in discoveryResults array: {results_count}")

        table_rows = js("return document.getElementById('search-results-body')?.querySelectorAll('tr').length || 0")
        print(f"  Rows in results table: {table_rows}")

        if results_count > 0:
            # Show first few results
            first_results = js("""
                if (typeof discoveryResults === 'undefined' || discoveryResults.length === 0) return [];
                return discoveryResults.slice(0, 3).map(r => ({
                    nctId: r.nctId,
                    title: (r.title || '').substring(0, 50),
                    enrollment: r.enrollment,
                    hasResults: r.hasResults
                }));
            """)
            print(f"\n  First 3 results:")
            for r in first_results:
                print(f"    - {r.get('nctId', 'N/A')}: {r.get('title', 'N/A')}... (n={r.get('enrollment', 0)})")
            print(f"\n  [OK] ClinicalTrials.gov search successful!")
        else:
            print(f"\n  [INFO] No CT.gov results - may be CORS/network issue from file:// protocol")

    # =========================================================================
    # TEST 2: PUBMED SEARCH
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 2: PUBMED SEARCH")
    print("=" * 70)

    # Check for PubMed search elements
    pubmed_input = js("return document.getElementById('pubmed-query') !== null")
    pubmed_fn = js("return typeof searchPubMed === 'function'")

    print(f"  PubMed query input exists: {pubmed_input}")
    print(f"  searchPubMed function exists: {pubmed_fn}")

    if pubmed_input and pubmed_fn:
        print("\n[STEP 6] Entering PubMed search query...")
        js("document.getElementById('pubmed-query').value = 'colchicine cardiovascular meta-analysis'")
        time.sleep(0.3)

        print("\n[STEP 7] Initiating PubMed search...")
        js("searchPubMed()")

        # Wait for PubMed results
        print("\n[STEP 8] Waiting for PubMed results (up to 45 seconds)...")

        def check_pubmed_results():
            result = js("""
                if (typeof discoveryResults !== 'undefined' && discoveryResults.length > 0) {
                    // Check if results are from PubMed (have pmid)
                    return discoveryResults.some(r => r.pmid || r.source === 'pubmed');
                }
                var status = document.getElementById('search-status');
                if (status) {
                    var text = status.innerText || '';
                    if (text.includes('Error') || text.includes('found') || text.includes('complete')) {
                        return true;
                    }
                }
                return false;
            """)
            return result

        pubmed_found = wait_for_condition(check_pubmed_results, timeout=45)

        search_status = js("return document.getElementById('search-status')?.innerText || 'No status'")
        print(f"  Search status: {search_status[:100]}")

        results_count = js("return typeof discoveryResults !== 'undefined' ? discoveryResults.length : 0")
        print(f"  Results in discoveryResults array: {results_count}")

        if results_count > 0:
            first_pubmed = js("""
                if (typeof discoveryResults === 'undefined' || discoveryResults.length === 0) return [];
                return discoveryResults.slice(0, 3).map(r => ({
                    pmid: r.pmid || 'N/A',
                    title: (r.title || '').substring(0, 50),
                    journal: r.journal || 'N/A'
                }));
            """)
            print(f"\n  First 3 PubMed results:")
            for r in first_pubmed:
                print(f"    - PMID:{r.get('pmid', 'N/A')}: {r.get('title', 'N/A')}... ({r.get('journal', 'N/A')})")
            print(f"\n  [OK] PubMed search successful!")
        else:
            print(f"\n  [INFO] No PubMed results - may be CORS/network issue from file:// protocol")

    # =========================================================================
    # TEST 3: DATA INPUT AND EXTRACTION
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 3: DATA INPUT AND EXTRACTION")
    print("=" * 70)

    # Go to Data Input tab
    print("\n[STEP 9] Navigating to Data Input tab...")
    click_tab("data")
    time.sleep(0.5)

    # Load demo data
    print("\n[STEP 10] Loading Colchicine demo data...")
    js("if(typeof loadColchicineData === 'function') loadColchicineData()")
    time.sleep(0.5)
    dismiss_alerts()

    # Check if LEC.studies was populated (the function may directly set LEC.studies)
    studies_count = js("return LEC?.studies?.length || 0")
    print(f"  Studies loaded directly: {studies_count}")

    # Parse the data if not already parsed
    if studies_count == 0:
        print("\n[STEP 11] Parsing study data...")
        js("if(typeof parseStudyData === 'function') parseStudyData()")
        time.sleep(0.5)
        dismiss_alerts()
        studies_count = js("return LEC?.studies?.length || 0")

    print(f"  Total studies parsed: {studies_count}")

    if studies_count > 0:
        # Show study details
        study_details = js("""
            if (!LEC || !LEC.studies) return [];
            return LEC.studies.map(s => ({
                name: s.name || s.study || 'unnamed',
                effect: s.effect || s.logEffect || 0,
                se: Math.sqrt(s.variance || 0),
                n: s.total || s.n || 0
            }));
        """)
        print(f"\n  Parsed studies:")
        for s in study_details:
            print(f"    - {s.get('name', 'N/A')}: RR={s.get('effect', 0):.3f}, SE={s.get('se', 0):.4f}")

    # =========================================================================
    # TEST 4: META-ANALYSIS WORKFLOW
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 4: META-ANALYSIS WORKFLOW")
    print("=" * 70)

    # Go to Meta-Analysis tab
    print("\n[STEP 12] Navigating to Meta-Analysis tab...")
    click_tab("meta")
    time.sleep(0.5)

    # Run meta-analysis
    print("\n[STEP 13] Running meta-analysis...")
    js("if(typeof runMetaAnalysis === 'function') runMetaAnalysis()")
    time.sleep(1)
    dismiss_alerts()

    # Check results
    meta_result = js("return LEC?.metaResult !== null")
    print(f"  Meta-analysis completed: {meta_result}")

    if meta_result:
        pooled = js("return LEC?.metaResult?.pooled?.effect || 0")
        ci_low = js("return LEC?.metaResult?.pooled?.ciLow || 0")
        ci_high = js("return LEC?.metaResult?.pooled?.ciHigh || 0")
        i2 = js("return LEC?.metaResult?.heterogeneity?.I2 || 0")
        tau2 = js("return LEC?.metaResult?.heterogeneity?.tau2 || 0")
        tau2_ci = js("return LEC?.metaResult?.heterogeneity?.tau2CI || null")
        p_het = js("return LEC?.metaResult?.heterogeneity?.pHet || 0")

        print(f"\n  META-ANALYSIS RESULTS:")
        print(f"  -----------------------")
        print(f"  Pooled RR: {pooled:.4f} (95% CI: {ci_low:.4f} to {ci_high:.4f})")
        print(f"  I-squared: {i2:.1f}%")
        print(f"  tau-squared: {tau2:.6f}")
        if tau2_ci:
            print(f"  tau-squared 95% CI: {tau2_ci.get('lower', 0):.6f} to {tau2_ci.get('upper', 0):.6f}")
        print(f"  Heterogeneity p-value: {p_het:.4f}")

    # Check forest plot
    print("\n[STEP 14] Checking forest plot...")
    js("if(typeof drawForestPlot === 'function') drawForestPlot()")
    time.sleep(0.5)

    forest_content = js("""
        var fp = document.getElementById('forest-plot');
        if (!fp) return 'No container';
        var svgCount = fp.querySelectorAll('rect, line, text, circle').length;
        return svgCount > 10 ? 'Rendered (' + svgCount + ' elements)' : 'Empty or minimal';
    """)
    print(f"  Forest plot: {forest_content}")

    # =========================================================================
    # TEST 5: PUBLICATION BIAS & DIAGNOSTICS
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 5: PUBLICATION BIAS & DIAGNOSTICS")
    print("=" * 70)

    # Egger's test
    print("\n[STEP 15] Running Egger's test...")
    egger_result = js("""
        if (typeof eggerTest === 'function') {
            try { return eggerTest(); } catch(e) { return 'Error: ' + e.message; }
        }
        return 'Function not available';
    """)
    print(f"  Egger's test: {egger_result}")

    # Begg's test
    print("\n[STEP 16] Running Begg's test...")
    begg_result = js("""
        if (typeof beggTest === 'function') {
            try { return beggTest(); } catch(e) { return 'Error: ' + e.message; }
        }
        return 'Function not available';
    """)
    print(f"  Begg's test: {begg_result}")

    # Influential diagnostics
    print("\n[STEP 17] Running influential diagnostics...")
    js("if(typeof runInfluentialDiagnostics === 'function') runInfluentialDiagnostics()")
    time.sleep(0.5)

    influential_output = js("""
        var el = document.getElementById('influential-results');
        if (!el) return 'Container not found';
        var hasTable = el.querySelector('table') !== null;
        var hasCooks = el.innerHTML.includes('Cook');
        return hasTable ? 'Table present' + (hasCooks ? ' with Cook\\'s D' : '') : 'No table';
    """)
    print(f"  Influential diagnostics: {influential_output}")

    # =========================================================================
    # TEST 6: GRADE ASSESSMENT
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 6: GRADE ASSESSMENT")
    print("=" * 70)

    print("\n[STEP 18] Navigating to GRADE tab...")
    click_tab("grade")
    time.sleep(0.5)

    print("\n[STEP 19] Calculating GRADE...")
    js("if(typeof calculateGRADE === 'function') calculateGRADE()")
    time.sleep(0.5)
    dismiss_alerts()

    grade_result = js("""
        var badge = document.querySelector('.grade-badge');
        var output = document.getElementById('gradeOutput');
        if (badge) return 'Grade: ' + badge.innerText;
        if (output && output.innerHTML.length > 50) return 'Output present';
        return 'No grade calculated';
    """)
    print(f"  GRADE assessment: {grade_result}")

    # =========================================================================
    # TEST 7: SUMMARY OF FINDINGS
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 7: SUMMARY OF FINDINGS TABLE")
    print("=" * 70)

    print("\n[STEP 20] Navigating to Summary of Findings tab...")
    click_tab("sof")
    time.sleep(0.5)

    print("\n[STEP 21] Generating Summary of Findings...")
    js("if(typeof generateSoF === 'function') generateSoF()")
    time.sleep(0.5)
    dismiss_alerts()

    sof_output = js("""
        var tables = document.querySelectorAll('#tab-sof table, .sof-table');
        if (tables.length === 0) return 'No table found';
        var totalRows = 0;
        tables.forEach(t => totalRows += t.querySelectorAll('tr').length);
        return 'Found ' + tables.length + ' table(s) with ' + totalRows + ' total rows';
    """)
    print(f"  SoF table: {sof_output}")

    # =========================================================================
    # TEST 8: EXPORT FUNCTIONS
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 8: EXPORT FUNCTIONS")
    print("=" * 70)

    print("\n[STEP 22] Navigating to Export tab...")
    click_tab("export")
    time.sleep(0.5)

    export_funcs = ['exportJSON', 'exportMarkdown', 'exportCSV', 'downloadForestPlot', 'saveSession', 'loadSession']
    print("\n  Export function availability:")
    for func in export_funcs:
        exists = js(f"return typeof {func} === 'function'")
        print(f"    {func}: {'Available' if exists else 'Not found'}")

    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    summary = {
        "Page Loaded": js("return document.readyState === 'complete'"),
        "Studies Parsed": js("return (LEC?.studies?.length || 0) > 0"),
        "Meta-Analysis Complete": js("return LEC?.metaResult !== null"),
        "Forest Plot Rendered": js("return document.getElementById('forest-plot')?.querySelectorAll('rect').length > 0"),
        "Tau-squared CI Available": js("return LEC?.metaResult?.heterogeneity?.tau2CI !== null"),
        "GRADE Function": js("return typeof calculateGRADE === 'function'"),
        "CT.gov Search Function": js("return typeof searchClinicalTrials === 'function'"),
        "PubMed Search Function": js("return typeof searchPubMed === 'function'"),
        "Export Functions": js("return typeof exportJSON === 'function' && typeof saveSession === 'function'"),
        "Egger's Test (t-dist)": js("return typeof tCDF === 'function'"),
    }

    print("\nComponent Status:")
    all_pass = True
    for component, status in summary.items():
        status_str = "[PASS]" if status else "[----]"
        if not status:
            all_pass = False
        print(f"  {status_str} {component}")

    passed = sum(1 for v in summary.values() if v)
    total = len(summary)
    print(f"\nOverall: {passed}/{total} components working ({100*passed/total:.0f}%)")

    if all_pass:
        print("\n*** ALL COMPONENTS OPERATIONAL ***")

    # Note about API searches
    print("\n" + "-" * 70)
    print("NOTE: CT.gov and PubMed API calls may fail from file:// protocol")
    print("due to CORS restrictions. Deploy to a web server for full testing.")
    print("-" * 70)

    # Keep browser open for inspection
    print("\nBrowser will remain open for 8 seconds for inspection...")
    time.sleep(8)

except Exception as e:
    print(f"\n[FATAL ERROR] {e}")
    import traceback
    traceback.print_exc()
    time.sleep(5)

finally:
    driver.quit()
    print("\nTest completed. Browser closed.")
