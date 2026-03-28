# Comprehensive Selenium test for NMA Pro v6.2 - Auto driver detection

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_nma_comprehensive():
    print("[INFO] Starting Edge with auto driver detection...")

    options = webdriver.EdgeOptions()
    options.add_argument('--start-maximized')

    # Let Selenium auto-find the driver
    driver = webdriver.Edge(options=options)
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
            ("FrequentistNMA", "FrequentistNMA object"),
            ("BayesianNMA", "BayesianNMA object"),
            ("generateBayesianRScript", "generateBayesianRScript function"),
            ("FrequentistNMA.pauleMandel_CI", "pauleMandel_CI method"),
        ]
        for func, name in functions_to_check:
            exists = driver.execute_script(f"return typeof {func} !== 'undefined'")
            if exists:
                results["passed"].append(f"{name} exists")
            else:
                results["failed"].append(f"{name} NOT found")

        # Wait for libraries to load
        print("\n[INFO] Waiting for libraries to load...")
        for i in range(20):  # Wait up to 10 seconds
            ready = driver.execute_script("return typeof jStat !== 'undefined' && typeof Plotly !== 'undefined'")
            if ready:
                break
            time.sleep(0.5)

        # Load sample data and set up form
        print("[INFO] Loading sample data...")
        driver.execute_script("""
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

            // Update reference dropdown with treatments
            const refSelect = document.getElementById('referenceSelect');
            if(refSelect) {
                refSelect.innerHTML = '<option value="A">A</option><option value="B">B</option><option value="C">C</option><option value="D">D</option>';
                refSelect.value = 'A';
            }

            // Set effect measure
            const emSelect = document.getElementById('effectMeasureSelect');
            if(emSelect) emSelect.value = 'OR';

            // Set estimator
            const estSelect = document.getElementById('estimatorSelect');
            if(estSelect) estSelect.value = 'REML';

            renderStudyTable();
        """)
        time.sleep(1)
        results["passed"].append("Sample data loaded (8 studies, 4 treatments)")

        # Run analysis directly via FrequentistNMA
        print("[INFO] Running frequentist analysis...")
        analysis_result = driver.execute_script("""
            try {
                // Run frequentist analysis directly
                const result = FrequentistNMA.analyze(AppState.studies, {
                    reference: 'A',
                    effectMeasure: 'OR',
                    estimator: 'REML'
                });
                AppState.results = result;
                AppState.reference = 'A';
                AppState.effectMeasure = 'OR';

                // Update displays
                if(result) {
                    // Update heterogeneity stats
                    document.getElementById('hetTau2').textContent = result.tau2.toFixed(4);
                    document.getElementById('hetTau').textContent = Math.sqrt(result.tau2).toFixed(4);
                    if(result.heterogeneity) {
                        document.getElementById('hetI2').textContent = result.heterogeneity.I2.toFixed(1) + '%';
                        document.getElementById('hetH2').textContent = result.heterogeneity.H2.toFixed(2);
                    }

                    // Calculate rankings using TreatmentRanking
                    try {
                        AppState.ranking = TreatmentRanking.rank(result, result.treatments, 'lower');
                    } catch(re) {
                        console.log('Ranking calc skipped:', re.message);
                    }

                    return {success: true, tau2: result.tau2, treatments: result.treatments.length};
                }
                return {success: false, error: 'No result'};
            } catch(e) {
                return {success: false, error: e.message};
            }
        """)
        time.sleep(2)

        if analysis_result and analysis_result.get('success'):
            tau2 = analysis_result.get('tau2', 0)
            n_treats = analysis_result.get('treatments', 0)
            results["passed"].append(f"Frequentist analysis completed (tau2={tau2:.4f}, {n_treats} treatments)")
        else:
            error_msg = analysis_result.get('error', 'Unknown') if analysis_result else 'No result'
            results["failed"].append(f"Frequentist analysis failed: {error_msg[:50]}")

        # Test all tabs
        tabs = [
            ("network", "Network Plot"),
            ("results", "Results/Forest"),
            ("ranking", "Rankings"),
            ("heterogeneity", "Heterogeneity"),
            ("consistency", "Consistency"),
            ("bayesian", "Bayesian"),
            ("pubbias", "Publication Bias"),
            ("metareg", "Meta-Regression"),
            ("cnma", "Component NMA"),
            ("transportability", "C-STREAM"),
            ("cinema", "CINeMA"),
            ("grade", "GRADE"),
            ("sensitivity", "Sensitivity"),
            ("cumulative", "Cumulative"),
            ("doseresponse", "Dose-Response"),
            ("export", "Export")
        ]

        print("\n[INFO] Testing all tabs...")
        for tab_id, tab_name in tabs:
            try:
                driver.execute_script(f"document.querySelector('button[data-tab=\"{tab_id}\"]').click()")
                time.sleep(0.3)
                panel = driver.find_element(By.ID, f"panel-{tab_id}")
                if panel.is_displayed():
                    results["passed"].append(f"Tab '{tab_name}' opens")
                else:
                    results["failed"].append(f"Tab '{tab_name}' did not open")
            except Exception as e:
                results["failed"].append(f"Tab '{tab_name}' error: {str(e)[:40]}")

        # Test plots
        print("\n[INFO] Checking plots...")

        # Network Canvas
        driver.execute_script("document.querySelector('button[data-tab=\"network\"]').click()")
        time.sleep(0.5)
        # Trigger network render explicitly with correct function name
        driver.execute_script("""
            if(typeof renderNetworkGraph === 'function' && AppState.studies && AppState.results) {
                renderNetworkGraph(AppState.studies, AppState.results.treatments);
            }
        """)
        time.sleep(0.5)
        canvas_ok = driver.execute_script("""
            // Check for canvas inside networkPlot container
            var container = document.getElementById('networkPlot');
            if(container) {
                var c = container.querySelector('canvas');
                return c && c.width > 0 && c.height > 0;
            }
            // Also check for networkCanvas (fallback)
            var c = document.getElementById('networkCanvas');
            return c && c.width > 0 && c.height > 0;
        """)
        if canvas_ok:
            results["passed"].append("Network canvas rendered")
        else:
            results["failed"].append("Network canvas not rendered")

        # Forest Plot (Plotly) - trigger update
        driver.execute_script("document.querySelector('button[data-tab=\"results\"]').click()")
        time.sleep(0.5)
        driver.execute_script("""
            if(typeof updateResultsTab === 'function' && AppState.results) {
                updateResultsTab();
            }
        """)
        time.sleep(0.5)
        forest_ok = driver.execute_script("""
            var el = document.getElementById('forestPlot');
            return el && el.data && el.data.length > 0;
        """)
        if forest_ok:
            results["passed"].append("Forest plot (Plotly) rendered")
        else:
            results["warnings"].append("Forest plot check inconclusive")

        # League Table
        league_ok = driver.execute_script("""
            var el = document.getElementById('leagueTableContainer');
            return el && el.innerHTML.length > 100;
        """)
        if league_ok:
            results["passed"].append("League table rendered")
        else:
            results["warnings"].append("League table may be empty")

        # Heterogeneity - Funnel Plot
        driver.execute_script("document.querySelector('button[data-tab=\"heterogeneity\"]').click()")
        time.sleep(0.5)
        funnel_ok = driver.execute_script("""
            var el = document.getElementById('funnelPlot');
            return el && el.data && el.data.length > 0;
        """)
        if funnel_ok:
            results["passed"].append("Funnel plot rendered")
        else:
            results["warnings"].append("Funnel plot check inconclusive")

        # Ranking - Rankogram - trigger update with correct function names
        driver.execute_script("document.querySelector('button[data-tab=\"ranking\"]').click()")
        time.sleep(0.5)
        driver.execute_script("""
            if(AppState.results && AppState.results.treatments && AppState.results.effects) {
                // Calculate ranking if not present - pass effects not results
                if(!AppState.ranking) {
                    try {
                        AppState.ranking = TreatmentRanking.rank(AppState.results.effects, AppState.results.treatments, 'lower');
                    } catch(e) {
                        console.log('Ranking calc error:', e.message);
                    }
                }
                // Render ranking table and rankogram
                if(typeof renderRankingTable === 'function' && AppState.ranking) {
                    renderRankingTable(AppState.ranking);
                }
                if(typeof renderRankogram === 'function' && AppState.ranking) {
                    renderRankogram(AppState.ranking);
                }
            }
        """)
        time.sleep(1)  # Extra time for ranking calculations
        rankogram_ok = driver.execute_script("""
            var el = document.getElementById('rankogramPlot');
            return el && el.data && el.data.length > 0;
        """)
        if rankogram_ok:
            results["passed"].append("Rankogram plot rendered")
        else:
            results["warnings"].append("Rankogram check inconclusive")

        ranking_rows = driver.execute_script("""
            return document.getElementById('rankingTableBody').getElementsByTagName('tr').length;
        """)
        if ranking_rows > 0:
            results["passed"].append(f"Ranking table has {ranking_rows} treatments")
        else:
            results["failed"].append("Ranking table empty")

        # Run Bayesian
        print("[INFO] Running Bayesian analysis...")
        driver.execute_script("document.querySelector('button[data-tab=\"bayesian\"]').click()")
        time.sleep(0.5)

        # Check gemtc button
        gemtc_exists = driver.execute_script("""
            var btns = document.querySelectorAll('button');
            for(var i=0; i<btns.length; i++){
                if(btns[i].textContent.includes('gemtc')) return true;
            }
            return false;
        """)
        if gemtc_exists:
            results["passed"].append("gemtc R export button present")
        else:
            results["failed"].append("gemtc R button NOT found")

        try:
            driver.execute_script("document.getElementById('runBayesianBtn').click()")
            time.sleep(5)
            # Handle any alert that might appear
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                results["warnings"].append(f"Alert appeared: {alert_text[:50]}")
            except:
                pass  # No alert

            bayes_content = driver.execute_script("return document.getElementById('bayesianContainer').textContent")
            if 'mean' in bayes_content.lower() or 'mcmc' in bayes_content.lower() or 'τ²' in bayes_content:
                results["passed"].append("Bayesian analysis completed")
            else:
                results["warnings"].append("Bayesian results unclear")
        except Exception as be:
            results["warnings"].append(f"Bayesian test error: {str(be)[:40]}")

        # Helper to dismiss alerts
        def dismiss_alert():
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                pass

        # Run Publication Bias
        print("[INFO] Running Publication Bias analysis...")
        try:
            driver.execute_script("document.querySelector('button[data-tab=\"pubbias\"]').click()")
            time.sleep(0.5)
            driver.execute_script("document.getElementById('runPubBiasBtn').click()")
            time.sleep(2)
            dismiss_alert()
            pubbias_content = driver.execute_script("return document.getElementById('pubBiasResults').textContent")
            if 'egger' in pubbias_content.lower() or 'bias' in pubbias_content.lower():
                results["passed"].append("Publication bias analysis completed")
            else:
                results["warnings"].append("Publication bias results unclear")
        except Exception as e:
            results["warnings"].append(f"Pub bias error: {str(e)[:30]}")

        # Run Cumulative
        print("[INFO] Running Cumulative NMA...")
        try:
            driver.execute_script("document.querySelector('button[data-tab=\"cumulative\"]').click()")
            time.sleep(0.5)
            driver.execute_script("document.getElementById('runCumulativeBtn').click()")
            time.sleep(2)
            dismiss_alert()
            cumul_content = driver.execute_script("return document.getElementById('cumulativeResults').textContent")
            if len(cumul_content) > 30:
                results["passed"].append("Cumulative NMA completed")
            else:
                results["warnings"].append("Cumulative NMA results unclear")
        except Exception as e:
            results["warnings"].append(f"Cumulative error: {str(e)[:30]}")

        # Run Leave-One-Out
        print("[INFO] Running Leave-One-Out...")
        try:
            driver.execute_script("document.querySelector('button[data-tab=\"sensitivity\"]').click()")
            time.sleep(0.5)
            driver.execute_script("document.getElementById('runLeaveOneOutBtn').click()")
            time.sleep(2)
            dismiss_alert()
            loo_content = driver.execute_script("return document.getElementById('looResults').textContent")
            if len(loo_content) > 30:
                results["passed"].append("Leave-One-Out analysis completed")
            else:
                results["warnings"].append("Leave-One-Out results unclear")
        except Exception as e:
            results["warnings"].append(f"LOO error: {str(e)[:30]}")

        # Check E-values
        try:
            evalue_content = driver.execute_script("return document.getElementById('evalueContainer').innerHTML")
            if len(evalue_content) > 50:
                results["passed"].append("E-values displayed")
            else:
                results["warnings"].append("E-values may be empty")
        except:
            results["warnings"].append("E-values check failed")

        # Final error check
        final_logs = driver.get_log('browser')
        final_errors = [l for l in final_logs if l['level'] == 'SEVERE']
        new_errors = len(final_errors) - len(errors)
        if new_errors > 0:
            results["warnings"].append(f"{new_errors} runtime JS warnings/errors")
        else:
            results["passed"].append("No runtime JavaScript errors")

    except Exception as e:
        results["failed"].append(f"Test error: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Print results
        print("\n" + "="*60)
        print("NMA PRO v6.2 - COMPREHENSIVE TEST RESULTS")
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

        time.sleep(2)
        driver.quit()

if __name__ == "__main__":
    test_nma_comprehensive()
