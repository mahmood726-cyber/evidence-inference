"""
Test Clustered IPD Handling and Validation Studies
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

def test_clustered_ipd_validation():
    print("=" * 70)
    print("TESTING CLUSTERED IPD AND VALIDATION FEATURES")
    print("=" * 70)

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

        # ========================================
        # CLUSTERED IPD FUNCTIONS
        # ========================================
        print("\n1. Clustered IPD Functions:")

        test("calculateICC function exists",
             js("return typeof calculateICC === 'function'"))

        test("calculateDesignEffect function exists",
             js("return typeof calculateDesignEffect === 'function'"))

        test("calculateEffectiveSampleSize function exists",
             js("return typeof calculateEffectiveSampleSize === 'function'"))

        test("runOneStageIPD function exists",
             js("return typeof runOneStageIPD === 'function'"))

        test("runTwoStageIPD function exists",
             js("return typeof runTwoStageIPD === 'function'"))

        test("calculateSandwichSE function exists",
             js("return typeof calculateSandwichSE === 'function'"))

        test("runGEE function exists",
             js("return typeof runGEE === 'function'"))

        test("showClusteredIPDAnalysis function exists",
             js("return typeof showClusteredIPDAnalysis === 'function'"))

        # ========================================
        # VALIDATION FUNCTIONS
        # ========================================
        print("\n2. Validation Functions:")

        test("BENCHMARK_DATASETS object exists",
             js("return typeof BENCHMARK_DATASETS !== 'undefined'"))

        test("BCG dataset exists",
             js("return BENCHMARK_DATASETS && BENCHMARK_DATASETS.bcg"))

        test("BCG has expected results",
             js("return BENCHMARK_DATASETS && BENCHMARK_DATASETS.bcg && BENCHMARK_DATASETS.bcg.expected && BENCHMARK_DATASETS.bcg.expected.DL"))

        test("runValidationStudy function exists",
             js("return typeof runValidationStudy === 'function'"))

        test("validateDataset function exists",
             js("return typeof validateDataset === 'function'"))

        test("runFixedEffects function exists",
             js("return typeof runFixedEffects === 'function'"))

        test("runRandomEffectsDL function exists",
             js("return typeof runRandomEffectsDL === 'function'"))

        test("runRandomEffectsREML function exists",
             js("return typeof runRandomEffectsREML === 'function'"))

        test("runRandomEffectsPM function exists",
             js("return typeof runRandomEffectsPM === 'function'"))

        test("showValidationStudy function exists",
             js("return typeof showValidationStudy === 'function'"))

        # ========================================
        # NUMERICAL VALIDATION
        # ========================================
        print("\n3. Numerical Validation:")

        # Test DL estimator against BCG benchmark
        dl_test = js("""
            var bcg = BENCHMARK_DATASETS.bcg;
            var studies = bcg.studies.map(s => ({yi: s.yi, vi: s.sei * s.sei, sei: s.sei}));
            var result = runRandomEffectsDL(studies);
            var expected = bcg.expected.DL;
            var dev_est = Math.abs(result.estimate - expected.estimate);
            var dev_tau2 = Math.abs(result.tau2 - expected.tau2);
            return {
                estimate: result.estimate,
                expected_est: expected.estimate,
                dev_est: dev_est,
                tau2: result.tau2,
                expected_tau2: expected.tau2,
                dev_tau2: dev_tau2,
                passed_est: dev_est < 0.01,
                passed_tau2: dev_tau2 < 0.02
            };
        """)

        if dl_test:
            print(f"\n    BCG DL Validation:")
            print(f"      Estimate: {dl_test['estimate']:.4f} (expected: {dl_test['expected_est']:.4f}, dev: {dl_test['dev_est']:.4f})")
            print(f"      Tau2: {dl_test['tau2']:.4f} (expected: {dl_test['expected_tau2']:.4f}, dev: {dl_test['dev_tau2']:.4f})")

            test("DL estimate within tolerance",
                 dl_test['passed_est'])

            test("DL tau2 within tolerance",
                 dl_test['passed_tau2'])

        # Test REML estimator
        reml_test = js("""
            var bcg = BENCHMARK_DATASETS.bcg;
            var studies = bcg.studies.map(s => ({yi: s.yi, vi: s.sei * s.sei, sei: s.sei}));
            var result = runRandomEffectsREML(studies);
            var expected = bcg.expected.REML;
            var dev = Math.abs(result.estimate - expected.estimate);
            return {
                estimate: result.estimate,
                expected: expected.estimate,
                deviation: dev,
                passed: dev < 0.01
            };
        """)

        if reml_test:
            print(f"\n    BCG REML Validation:")
            print(f"      Estimate: {reml_test['estimate']:.4f} (expected: {reml_test['expected']:.4f}, dev: {reml_test['deviation']:.4f})")

            test("REML estimate within tolerance",
                 reml_test['passed'])

        # Test ICC calculation
        icc_test = js("""
            // Create test clustered data
            var testData = [];
            // Cluster 1
            for (var i = 0; i < 20; i++) {
                testData.push({outcome: 5 + Math.random(), treatment: i < 10 ? 1 : 0, study: 'A'});
            }
            // Cluster 2
            for (var i = 0; i < 25; i++) {
                testData.push({outcome: 7 + Math.random(), treatment: i < 12 ? 1 : 0, study: 'B'});
            }
            // Cluster 3
            for (var i = 0; i < 15; i++) {
                testData.push({outcome: 4 + Math.random(), treatment: i < 8 ? 1 : 0, study: 'C'});
            }

            var result = calculateICC(testData, 'outcome', 'study');
            return {
                ICC: result.ICC,
                design_effect: result.design_effect,
                n_clusters: result.n_clusters,
                valid: result.ICC >= 0 && result.ICC <= 1 && result.design_effect >= 1
            };
        """)

        if icc_test:
            print(f"\n    ICC Calculation Test:")
            print(f"      ICC: {icc_test['ICC']:.4f}")
            print(f"      Design Effect: {icc_test['design_effect']:.2f}")
            print(f"      N Clusters: {icc_test['n_clusters']}")

            test("ICC calculation valid",
                 icc_test['valid'])

        # ========================================
        # RUN FULL VALIDATION
        # ========================================
        print("\n4. Full Validation Study:")

        validation_result = js("""
            var results = runValidationStudy();
            return {
                total: results.summary.total,
                passed: results.summary.passed,
                passRate: results.summary.passRate,
                maxDeviation: results.summary.maxDeviation
            };
        """)

        if validation_result:
            print(f"\n    Validation Summary:")
            print(f"      Tests: {validation_result['passed']}/{validation_result['total']}")
            print(f"      Pass Rate: {validation_result['passRate']}%")
            print(f"      Max Deviation: {validation_result['maxDeviation']:.4f}")

            test("Validation pass rate >= 80%",
                 float(validation_result['passRate']) >= 80)

            test("Max deviation acceptable",
                 validation_result['maxDeviation'] < 0.1)

        # ========================================
        # HEADER BUTTONS
        # ========================================
        print("\n5. Header Buttons:")

        test("Clustered IPD button exists",
             js("return !!document.querySelector('button[onclick*=\"showClusteredIPDAnalysis\"]')"))

        test("Validation button exists",
             js("return !!document.querySelector('button[onclick*=\"showValidationStudy\"]')"))

        # ========================================
        # MODAL FUNCTIONALITY
        # ========================================
        print("\n6. Modal Functionality:")

        # Test Validation modal opens
        js("try { showValidationStudy(); } catch(e) { console.log(e); }")
        time.sleep(1)
        test("Validation modal opens",
             js("return document.body.innerHTML.includes('Validation') || document.body.innerHTML.includes('metafor')"))
        js("var m = document.getElementById('validationModal'); if(m) m.remove();")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

    # Summary
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    pass_rate = 100 * passed / total if total > 0 else 0

    print("\n" + "=" * 70)
    print(f"CLUSTERED IPD & VALIDATION TEST RESULTS: {passed}/{total} ({pass_rate:.1f}%)")
    print("=" * 70)

    # Save results
    with open('C:/Users/user/clustered_validation_test.json', 'w') as f:
        json.dump({
            'passed': passed,
            'total': total,
            'pass_rate': pass_rate,
            'results': results
        }, f, indent=2)

    return passed == total

if __name__ == '__main__':
    test_clustered_ipd_validation()
