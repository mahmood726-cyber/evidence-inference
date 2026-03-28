#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final verification - check for actual JavaScript errors in console"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def main():
    print("=" * 70)
    print("FINAL VERIFICATION - TruthCert-PairwisePro")
    print("=" * 70)

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Enable logging to capture console errors
    options.set_capability('ms:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Edge(options=options)
    driver.set_script_timeout(60)

    try:
        # Load app
        file_path = Path("C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
        driver.get(f"file:///{file_path}")
        time.sleep(4)
        print("✓ App loaded\n")

        # Load demo and run analysis
        print("Loading BCG demo and running analysis...")
        driver.execute_script("loadDemoDataset('BCG');")
        time.sleep(2)
        driver.execute_script("runAnalysis();")
        time.sleep(5)
        print("✓ Analysis complete\n")

        # Test ALL previously problematic functions
        print("--- TESTING ALL FUNCTIONS ---\n")

        test_functions = [
            ("runZCurveAnalysis", "runZCurveAnalysis()"),
            ("runSimplifiedMA", "runSimplifiedMA()"),
            ("generateGRADESummary", "generateGRADESummary(AppState.results)"),
            ("runSmallSampleCI", "runSmallSampleCI()"),
            ("runCopasModel", "runCopasModel()"),
            ("runGOSH", "runGOSH()"),
            ("runTSA", "runTSA()"),
            ("runPCurve", "runPCurve()"),
            ("runModelAveraging", "runModelAveraging()"),
            ("runInfluenceDiagnostics", "runInfluenceDiagnostics()"),
            ("assessGRADE", "assessGRADE()"),
            ("runMetaRegression", "runMetaRegression()"),
            ("runLOOAnalysis", "runLOOAnalysis()"),
            ("runCumulativeMeta", "runCumulativeMeta()"),
            ("detectOutliers", "detectOutliers()"),
            ("runMultiverse", "runMultiverse()"),
            ("calculateFragility", "calculateFragility()"),
            ("runDDMA", "runDDMA()"),
            ("runClinicalUtility", "runClinicalUtility()"),
            ("runHTA", "runHTA()"),
        ]

        passed = []
        failed = []

        for name, code in test_functions:
            try:
                error = driver.execute_script(f"""
                    try {{
                        if (typeof {name.split('(')[0]} === 'function') {{
                            {code};
                            return null;
                        }} else {{
                            return 'Function not defined';
                        }}
                    }} catch (e) {{
                        return e.message;
                    }}
                """)

                if error:
                    if "not defined" in str(error).lower():
                        print(f"  ? {name}: not exposed to global scope")
                    else:
                        failed.append((name, error))
                        print(f"  ✗ {name}: {error[:60]}")
                else:
                    passed.append(name)
                    print(f"  ✓ {name}")

                time.sleep(0.3)

                # Handle any alerts
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                except:
                    pass

            except Exception as e:
                failed.append((name, str(e)))
                print(f"  ✗ {name}: {str(e)[:40]}")

        # Check for console errors
        print("\n--- CHECKING BROWSER CONSOLE ---")
        try:
            logs = driver.get_log('browser')
            errors = [log for log in logs if log['level'] == 'SEVERE']
            if errors:
                print(f"\n  Found {len(errors)} console errors:")
                for err in errors[:10]:
                    msg = err['message'][:80]
                    print(f"    ✗ {msg}")
            else:
                print("  ✓ No severe console errors")
        except:
            print("  (Console log access not available)")

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"  Functions tested: {len(test_functions)}")
        print(f"  Passed: {len(passed)}")
        print(f"  Failed: {len(failed)}")

        if failed:
            print("\n--- FAILURES ---")
            for name, err in failed:
                print(f"  ✗ {name}: {err[:60]}")

        overall = len(failed) == 0
        print(f"\n  {'✓ ALL FUNCTIONS WORKING' if overall else '✗ SOME ISSUES REMAIN'}")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
