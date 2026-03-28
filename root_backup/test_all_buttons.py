#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test ALL buttons in TruthCert-PairwisePro to find any remaining errors"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

def main():
    print("=" * 70)
    print("BUTTON CLICK TEST - TruthCert-PairwisePro")
    print("=" * 70)

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Edge(options=options)
    driver.set_script_timeout(30)

    passed = []
    failed = []
    skipped = []

    try:
        # Load app
        file_path = Path("C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
        driver.get(f"file:///{file_path}")
        time.sleep(4)
        print("✓ App loaded\n")

        # Load demo and run analysis
        driver.execute_script("loadDemoDataset('BCG');")
        time.sleep(2)
        driver.execute_script("runAnalysis();")
        time.sleep(4)
        print("✓ BCG demo loaded and analyzed\n")

        # Clear any initial console errors
        driver.execute_script("console.clear();")

        # Get all tabs
        tabs = driver.execute_script("""
            return Array.from(document.querySelectorAll('[data-tab]')).map(t => t.getAttribute('data-tab'));
        """)

        print(f"Testing {len(tabs)} tabs...\n")

        for tab in tabs:
            print(f"\n--- TAB: {tab} ---")

            # Click the tab
            try:
                driver.execute_script(f"document.querySelector('[data-tab=\"{tab}\"]').click();")
                time.sleep(0.5)
            except:
                print(f"  Could not click tab {tab}")
                continue

            # Find all buttons in this tab's panel
            buttons = driver.execute_script(f"""
                const panel = document.getElementById('panel-{tab}');
                if (!panel) return [];
                const btns = panel.querySelectorAll('button:not([data-tab])');
                return Array.from(btns).map((b, i) => ({{
                    index: i,
                    text: b.innerText.trim().substring(0, 40),
                    onclick: b.getAttribute('onclick') || '',
                    id: b.id || '',
                    disabled: b.disabled
                }}));
            """)

            if not buttons:
                print(f"  No buttons found in panel-{tab}")
                continue

            print(f"  Found {len(buttons)} buttons")

            for btn in buttons:
                if btn.get('disabled'):
                    skipped.append(f"{tab}: {btn['text'][:25]} (disabled)")
                    continue

                btn_text = btn['text'][:30] if btn['text'] else f"button_{btn['index']}"
                onclick = btn.get('onclick', '')

                # Skip certain buttons
                skip_keywords = ['export', 'download', 'save', 'copy', 'print', 'share']
                if any(kw in btn_text.lower() or kw in onclick.lower() for kw in skip_keywords):
                    skipped.append(f"{tab}: {btn_text}")
                    continue

                try:
                    # Clear console before click
                    driver.execute_script("window._lastError = null;")

                    # Click the button
                    result = driver.execute_script(f"""
                        try {{
                            const panel = document.getElementById('panel-{tab}');
                            const btns = panel.querySelectorAll('button:not([data-tab])');
                            const btn = btns[{btn['index']}];
                            if (btn && !btn.disabled) {{
                                btn.click();
                                return {{ clicked: true }};
                            }}
                            return {{ clicked: false, reason: 'not found or disabled' }};
                        }} catch (e) {{
                            window._lastError = e.message;
                            return {{ clicked: false, error: e.message }};
                        }}
                    """)

                    time.sleep(0.3)

                    # Check for errors
                    error = driver.execute_script("return window._lastError;")

                    if error:
                        failed.append(f"{tab}: {btn_text} - {error[:50]}")
                        print(f"    ✗ {btn_text}: {error[:40]}")
                    elif result.get('clicked'):
                        passed.append(f"{tab}: {btn_text}")
                        print(f"    ✓ {btn_text}")
                    else:
                        skipped.append(f"{tab}: {btn_text} - {result.get('reason', 'unknown')}")

                except Exception as e:
                    failed.append(f"{tab}: {btn_text} - {str(e)[:40]}")
                    print(f"    ✗ {btn_text}: {str(e)[:40]}")

            # Handle any alerts
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except:
                pass

        # Test specific functions that had errors
        print("\n\n--- TESTING PREVIOUSLY BROKEN FUNCTIONS ---")

        specific_tests = [
            ("runZCurveAnalysis", "runZCurveAnalysis()"),
            ("runSimplifiedMA", "runSimplifiedMA()"),
            ("generateGRADESummary", "generateGRADESummary(AppState.results)"),
            ("runSmallSampleCI", "runSmallSampleCI()"),
            ("runCopasModel", "runCopasModel()"),
        ]

        for name, code in specific_tests:
            try:
                error = driver.execute_script(f"""
                    try {{
                        {code};
                        return null;
                    }} catch (e) {{
                        return e.message;
                    }}
                """)

                if error:
                    failed.append(f"FUNCTION: {name} - {error[:50]}")
                    print(f"  ✗ {name}: {error[:50]}")
                else:
                    passed.append(f"FUNCTION: {name}")
                    print(f"  ✓ {name}")

                time.sleep(0.5)
            except Exception as e:
                failed.append(f"FUNCTION: {name} - {str(e)[:40]}")
                print(f"  ✗ {name}: {str(e)[:40]}")

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"  Passed:  {len(passed)}")
        print(f"  Failed:  {len(failed)}")
        print(f"  Skipped: {len(skipped)}")

        if failed:
            print("\n--- FAILURES ---")
            for f in failed[:20]:
                print(f"  ✗ {f}")
            if len(failed) > 20:
                print(f"  ... and {len(failed) - 20} more")

        overall = len(failed) == 0
        print(f"\n  Overall: {'✓ ALL PASS' if overall else '✗ SOME FAILURES'}")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
