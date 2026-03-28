#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify UI button functions work correctly"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options

def main():
    print("=" * 70)
    print("UI BUTTON VERIFICATION - TruthCert-PairwisePro")
    print("=" * 70)

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

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

        # Test UI wrapper functions (the ones attached to buttons)
        print("--- TESTING UI FUNCTIONS ---\n")

        ui_functions = [
            ("computeGRADE", "computeGRADE()"),
            ("runGRADEAssessment", "runGRADEAssessment()"),
            ("runZCurveAnalysis", "runZCurveAnalysis()"),
            ("runSimplifiedMA", "runSimplifiedMA()"),
            ("runSmallSampleCI", "runSmallSampleCI()"),
            ("runCopasModel", "runCopasModel()"),
            ("runInfluenceDiagnostics", "runInfluenceDiagnostics()"),
            ("runMetaRegression", "runMetaRegression()"),
            ("showGRADEDetails", "showGRADEDetails()"),
        ]

        passed = []
        failed = []

        for name, code in ui_functions:
            try:
                error = driver.execute_script(f"""
                    try {{
                        if (typeof {name} === 'function') {{
                            {code};
                            return null;
                        }} else {{
                            return '{name} not defined';
                        }}
                    }} catch (e) {{
                        return e.message;
                    }}
                """)

                if error:
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

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"  Passed: {len(passed)}/{len(ui_functions)}")
        print(f"  Failed: {len(failed)}/{len(ui_functions)}")

        if failed:
            print("\n--- FAILURES ---")
            for name, err in failed:
                print(f"  ✗ {name}: {err[:60]}")
        else:
            print("\n  ✓ ALL UI BUTTONS WORKING CORRECTLY!")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
