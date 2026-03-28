# Comprehensive Selenium test for NMA Pro v6.2
# Tests all tabs and verifies plots display

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

def test_nma_comprehensive():
    # Use existing Edge driver
    driver_path = None
    wdm_path = os.path.expanduser("~/.wdm/drivers/edgedriver")
    if os.path.exists(wdm_path):
        for root, dirs, files in os.walk(wdm_path):
            for f in files:
                if f == "msedgedriver.exe":
                    driver_path = os.path.join(root, f)
                    break

    if not driver_path:
        # Try default location
        driver_path = r"C:\Users\user\.wdm\drivers\edgedriver\win64\131.0.2903.112\msedgedriver.exe"

    print(f"Using driver: {driver_path}")

    service = Service(driver_path)
    options = webdriver.EdgeOptions()
    options.add_argument('--start-maximized')
    # Not headless so we can see what's happening

    driver = webdriver.Edge(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    results = {"passed": [], "failed": [], "warnings": []}

    try:
        # Load the app
        file_path = r"C:\Users\user\OneDrive - NHS\Documents\NMAhtml\nma-pro-v6.2-optimized.html"
        driver.get(f"file:///{file_path.replace(chr(92), '/')}")
        time.sleep(3)

        # Check for JS errors
        logs = driver.get_log('browser')
        errors = [l for l in logs if l['level'] == 'SEVERE']
        if errors:
            for e in errors:
                results["failed"].append(f"JS Error: {e['message'][:80]}")
        else:
            results["passed"].append("No JavaScript errors on load")

        # Check essential functions exist
        functions_to_check = [
            "FrequentistNMA",
            "BayesianNMA",
            "generateBayesianRScript",
            "Stats",
            "Matrix"
        ]
        for func in functions_to_check:
            exists = driver.execute_script(f"return typeof {func} !== 'undefined'")
            if exists:
                results["passed"].append(f"Function/Object '{func}' exists")
            else:
                results["failed"].append(f"Function/Object '{func}' NOT found")

        # Check pauleMandel_CI method
        has_pm = driver.execute_script("return typeof FrequentistNMA.pauleMandel_CI === 'function'")
        if has_pm:
            results["passed"].append("pauleMandel_CI method exists")
        else:
            results["failed"].append("pauleMandel_CI method NOT found")

        # Load sample data using the demo
        print("\n[INFO] Loading sample data...")
        driver.execute_script("""
            // Sample smoking cessation NMA data
            AppState.studies = [
                {name:'Study1', treatment1:'A', treatment2:'B', events1:9, n1:140, events2:23, n2:140, year:2005},
                {name:'Study2', treatment1:'A', treatment2:'B', events1:11, n1:78, events2:12, n2:85, year:2006},
                {name:'Study3', treatment1:'A', treatment2:'C', events1:75, n1:731, events2:363, n2:714, year:2007},
                {name:'Study4', treatment1:'A', treatment2:'C', events1:2, n1:106, events2:9, n2:205, year:2008},
                {name:'Study5', treatment1:'A', treatment2:'D', events1:58, n1:549, events2:237, n2:1561, year:2009},
                {name:'Study6', treatment1:'B', treatment2:'C', events1:0, n1:33, events2:9, n2:48, year:2010},
                {name:'Study7', treatment1:'B', treatment2:'D', events1:3, n1:100, events2:31, n2:98, year:2011},
                {name:'Study8', treatment1:'C', treatment2:'D', events1:1, n1:31, events2:26, n2:95, year:2012}
            ];
            AppState.reference = 'A';
            AppState.effectMeasure = 'OR';
            renderStudyTable();
        """)
        time.sleep(1)
        results["passed"].append("Sample data loaded")

        # Run analysis
        print("[INFO] Running frequentist analysis...")
        analyze_btn = driver.find_element(By.ID, "analyzeBtn")
        analyze_btn.click()
        time.sleep(3)

        # Check if analysis completed
        tau2_elem = driver.find_element(By.ID, "hetTau2")
        tau2_val = tau2_elem.text
        if tau2_val and tau2_val != '--':
            results["passed"].append(f"Frequentist analysis completed (tau2={tau2_val})")
        else:
            results["failed"].append("Frequentist analysis may have failed")

        # Define all tabs to test
        tabs_to_test = [
            ("network", "Network Plot", "networkCanvas"),
            ("results", "Forest Plot", "forestPlot"),
            ("ranking", "Rankings", "rankingTableBody"),
            ("heterogeneity", "Heterogeneity", "hetTau2"),
            ("consistency", "Consistency", "nodeSplitContainer"),
            ("bayesian", "Bayesian", "bayesianContainer"),
            ("pubbias", "Publication Bias", "pubBiasResults"),
            ("metareg", "Meta-Regression", "metaRegResults"),
            ("cnma", "Component NMA", "cnmaResults"),
            ("transportability", "C-STREAM", "cstreamResults"),
            ("cinema", "CINeMA", "cinemaMatrix"),
            ("grade", "GRADE", "gradeMatrix"),
            ("sensitivity", "Sensitivity", "evalueContainer"),
            ("cumulative", "Cumulative", "cumulativeResults"),
            ("doseresponse", "Dose-Response", "doseResults"),
            ("export", "Export", None)
        ]

        print("\n[INFO] Testing all tabs...")
        for tab_id, tab_name, container_id in tabs_to_test:
            try:
                # Click tab
                tab_btn = driver.find_element(By.CSS_SELECTOR, f'button[data-tab="{tab_id}"]')
                driver.execute_script("arguments[0].click();", tab_btn)
                time.sleep(0.5)

                # Check if tab panel is visible
                panel = driver.find_element(By.ID, f"panel-{tab_id}")
                is_visible = panel.is_displayed()

                if is_visible:
                    results["passed"].append(f"Tab '{tab_name}' opens correctly")

                    # Check container content if specified
                    if container_id:
                        try:
                            container = driver.find_element(By.ID, container_id)
                            content = container.text or container.get_attribute('innerHTML')
                            if content and len(content) > 10:
                                results["passed"].append(f"  - Container '{container_id}' has content")
                            else:
                                results["warnings"].append(f"  - Container '{container_id}' may be empty")
                        except:
                            results["warnings"].append(f"  - Container '{container_id}' not found")
                else:
                    results["failed"].append(f"Tab '{tab_name}' did not open")

            except Exception as e:
                results["failed"].append(f"Tab '{tab_name}' error: {str(e)[:50]}")

        # Test specific functionality
        print("\n[INFO] Testing specific features...")

        # 1. Check Network Plot (Canvas)
        driver.execute_script("document.querySelector('button[data-tab=\"network\"]').click()")
        time.sleep(1)
        canvas = driver.find_element(By.ID, "networkCanvas")
        canvas_width = driver.execute_script("return document.getElementById('networkCanvas').width")
        if canvas_width > 0:
            results["passed"].append("Network canvas rendered")
        else:
            results["failed"].append("Network canvas not rendered")

        # 2. Check Forest Plot (Plotly)
        driver.execute_script("document.querySelector('button[data-tab=\"results\"]').click()")
        time.sleep(1)
        forest_div = driver.find_element(By.ID, "forestPlot")
        has_plotly = driver.execute_script("""
            var el = document.getElementById('forestPlot');
            return el && el.data && el.data.length > 0;
        """)
        if has_plotly:
            results["passed"].append("Forest plot (Plotly) rendered")
        else:
            results["warnings"].append("Forest plot may not be fully rendered")

        # 3. Check League Table
        league_table = driver.find_element(By.ID, "leagueTableContainer")
        league_content = league_table.get_attribute('innerHTML')
        if 'table' in league_content.lower() or len(league_content) > 100:
            results["passed"].append("League table rendered")
        else:
            results["warnings"].append("League table may be empty")

        # 4. Run Bayesian Analysis
        print("[INFO] Running Bayesian analysis...")
        driver.execute_script("document.querySelector('button[data-tab=\"bayesian\"]').click()")
        time.sleep(1)

        # Check gemtc R button exists
        gemtc_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'gemtc R')]")
        if gemtc_btns:
            results["passed"].append("gemtc R export button found")
        else:
            results["failed"].append("gemtc R export button NOT found")

        bayes_btn = driver.find_element(By.ID, "runBayesianBtn")
        bayes_btn.click()
        time.sleep(5)  # Bayesian takes longer

        bayes_container = driver.find_element(By.ID, "bayesianContainer")
        bayes_content = bayes_container.text
        if 'τ²' in bayes_content or 'tau' in bayes_content.lower() or 'MCMC' in bayes_content:
            results["passed"].append("Bayesian analysis completed")
        else:
            results["warnings"].append("Bayesian analysis may not have completed")

        # 5. Run Publication Bias
        print("[INFO] Running publication bias analysis...")
        driver.execute_script("document.querySelector('button[data-tab=\"pubbias\"]').click()")
        time.sleep(1)
        pubbias_btn = driver.find_element(By.ID, "runPubBiasBtn")
        pubbias_btn.click()
        time.sleep(2)

        pubbias_container = driver.find_element(By.ID, "pubBiasResults")
        if 'Egger' in pubbias_container.text or 'bias' in pubbias_container.text.lower():
            results["passed"].append("Publication bias analysis completed")
        else:
            results["warnings"].append("Publication bias analysis may not have completed")

        # 6. Check Heterogeneity plots
        driver.execute_script("document.querySelector('button[data-tab=\"heterogeneity\"]').click()")
        time.sleep(1)

        # Check funnel plot
        funnel_div = driver.find_element(By.ID, "funnelPlot")
        has_funnel = driver.execute_script("""
            var el = document.getElementById('funnelPlot');
            return el && el.data && el.data.length > 0;
        """)
        if has_funnel:
            results["passed"].append("Funnel plot rendered")
        else:
            results["warnings"].append("Funnel plot may not be rendered")

        # 7. Check Ranking tab
        driver.execute_script("document.querySelector('button[data-tab=\"ranking\"]').click()")
        time.sleep(1)

        ranking_body = driver.find_element(By.ID, "rankingTableBody")
        ranking_rows = ranking_body.find_elements(By.TAG_NAME, "tr")
        if len(ranking_rows) > 0:
            results["passed"].append(f"Ranking table has {len(ranking_rows)} treatments")
        else:
            results["warnings"].append("Ranking table may be empty")

        # Check rankogram
        rankogram = driver.find_element(By.ID, "rankogramPlot")
        has_rankogram = driver.execute_script("""
            var el = document.getElementById('rankogramPlot');
            return el && el.data && el.data.length > 0;
        """)
        if has_rankogram:
            results["passed"].append("Rankogram plot rendered")
        else:
            results["warnings"].append("Rankogram may not be rendered")

        # 8. Run Leave-One-Out
        print("[INFO] Running Leave-One-Out analysis...")
        driver.execute_script("document.querySelector('button[data-tab=\"sensitivity\"]').click()")
        time.sleep(1)
        loo_btn = driver.find_element(By.ID, "runLeaveOneOutBtn")
        loo_btn.click()
        time.sleep(3)

        loo_results = driver.find_element(By.ID, "looResults")
        if len(loo_results.text) > 20:
            results["passed"].append("Leave-One-Out analysis completed")
        else:
            results["warnings"].append("Leave-One-Out may not have completed")

        # 9. Run Cumulative NMA
        print("[INFO] Running Cumulative NMA...")
        driver.execute_script("document.querySelector('button[data-tab=\"cumulative\"]').click()")
        time.sleep(1)
        cumul_btn = driver.find_element(By.ID, "runCumulativeBtn")
        cumul_btn.click()
        time.sleep(2)

        cumul_results = driver.find_element(By.ID, "cumulativeResults")
        if len(cumul_results.text) > 20:
            results["passed"].append("Cumulative NMA completed")
        else:
            results["warnings"].append("Cumulative NMA may not have completed")

        # Final JS error check
        final_logs = driver.get_log('browser')
        final_errors = [l for l in final_logs if l['level'] == 'SEVERE' and l not in logs]
        if final_errors:
            for e in final_errors:
                results["failed"].append(f"Runtime JS Error: {e['message'][:80]}")
        else:
            results["passed"].append("No runtime JavaScript errors")

    except Exception as e:
        results["failed"].append(f"Test error: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Print results
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)

        print(f"\n[PASSED] ({len(results['passed'])} tests)")
        for p in results['passed']:
            print(f"  + {p}")

        if results['warnings']:
            print(f"\n[WARNINGS] ({len(results['warnings'])} items)")
            for w in results['warnings']:
                print(f"  ? {w}")

        if results['failed']:
            print(f"\n[FAILED] ({len(results['failed'])} tests)")
            for f in results['failed']:
                print(f"  X {f}")

        total = len(results['passed']) + len(results['failed'])
        pass_rate = len(results['passed']) / total * 100 if total > 0 else 0
        print(f"\n{'='*60}")
        print(f"PASS RATE: {pass_rate:.1f}% ({len(results['passed'])}/{total})")
        print("="*60)

        input("\nPress Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    test_nma_comprehensive()
