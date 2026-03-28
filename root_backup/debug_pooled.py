#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug the pooled result structure"""

import sys
import time
from pathlib import Path
import json

sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def main():
    print("=" * 70)
    print("DEBUGGING POOLED RESULT STRUCTURE")
    print("=" * 70)

    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Edge(options=options)

    try:
        file_path = Path("C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html")
        driver.get(f"file:///{file_path}")
        time.sleep(3)
        print("App loaded")

        # Load BCG demo
        driver.execute_script("loadDemoDataset('BCG');")
        time.sleep(2)
        print("BCG demo loaded")

        # Run analysis
        driver.execute_script("runAnalysis();")
        time.sleep(4)
        print("Analysis run")

        # Get full pooled result
        pooled = driver.execute_script("""
            if (AppState.results && AppState.results.pooled) {
                return JSON.parse(JSON.stringify(AppState.results.pooled));
            }
            return null;
        """)
        print("\n--- Pooled Result ---")
        if pooled:
            for key, value in pooled.items():
                if isinstance(value, (list, dict)):
                    print(f"  {key}: {type(value).__name__} (len={len(value) if hasattr(value, '__len__') else 'N/A'})")
                else:
                    print(f"  {key}: {value}")
        else:
            print("  No pooled result!")

        # Check studies structure
        studies = driver.execute_script("""
            if (AppState.results && AppState.results.studies) {
                return AppState.results.studies.slice(0, 2).map(s => {
                    return {
                        name: s.name,
                        yi: s.yi,
                        vi: s.vi,
                        sei: s.sei,
                        keys: Object.keys(s)
                    };
                });
            }
            return null;
        """)
        print("\n--- First 2 Studies ---")
        for s in (studies or []):
            print(f"  {s}")

        # Check if forest plot function exists and what it returns
        render_test = driver.execute_script("""
            try {
                const r = AppState.results;
                if (!r) return { error: 'No results' };
                if (!r.studies) return { error: 'No studies in results' };
                if (!r.pooled) return { error: 'No pooled in results' };

                return {
                    hasStudies: true,
                    studiesCount: r.studies.length,
                    hasPooled: true,
                    pooledTheta: r.pooled.theta,
                    pooledEstimate: r.pooled.estimate,
                    forestSettingsExist: typeof AppState.forestSettings !== 'undefined'
                };
            } catch (e) {
                return { error: e.message };
            }
        """)
        print("\n--- Forest Plot Data Check ---")
        print(f"  {render_test}")

        time.sleep(1)
        driver.quit()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        driver.quit()

if __name__ == "__main__":
    main()
