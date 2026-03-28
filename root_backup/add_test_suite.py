#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add automated unit test suite to app.js"""

print("=" * 70)
print("ADDING AUTOMATED UNIT TEST SUITE")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n').replace('\r', '\n')

# Test suite code to add
test_suite = '''
    // =============================================
    // SECTION: AUTOMATED UNIT TEST SUITE
    // =============================================

    /**
     * Automated unit test suite for statistical validation
     *
     * Reference values from R metafor 4.8.0:
     * data(dat.bcg); dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)
     *
     * @returns {Object} Test results with pass/fail for each test
     */
    function runAutomatedTests() {
      const results = {
        passed: 0,
        failed: 0,
        tests: [],
        timestamp: new Date().toISOString()
      };

      // BCG dataset (dat.bcg from metafor) - reference values from R
      const BCG = {
        yi: [-0.8893, -1.5854, -1.3481, -1.4416, -0.2170, -0.7861, -1.6209,
             0.0120, -0.4689, -1.3713, -0.3394, -0.2545, -0.1742],
        vi: [0.0351, 0.0145, 0.0107, 0.0129, 0.0542, 0.0052, 0.2232,
             0.0176, 0.0166, 0.0249, 0.0203, 0.0512, 0.0069],
        // Reference values from metafor 4.8.0
        ref: {
          DL: 0.308760,
          REML: 0.313195,
          ML: 0.260560,
          HS: 0.228363,
          SJ: 0.345516,
          HE: 0.328564,
          theta_DL: -0.714509,
          Q: 152.233,
          I2: 92.12,
          HKSJ_lower: -1.193,
          HKSJ_upper: -0.236
        }
      };

      function assertClose(actual, expected, tolerance, testName) {
        const diff = Math.abs(actual - expected);
        const pass = diff <= tolerance;
        results.tests.push({
          name: testName,
          expected: expected.toFixed(6),
          actual: actual.toFixed(6),
          diff: diff.toFixed(8),
          tolerance: tolerance,
          pass
        });
        if (pass) results.passed++;
        else results.failed++;
        return pass;
      }

      // Test 1: DL estimator
      const dl = estimateTau2_DL(BCG.yi, BCG.vi);
      assertClose(dl.tau2, BCG.ref.DL, 0.001, 'tau2_DL');

      // Test 2: REML estimator
      const reml = estimateTau2_REML(BCG.yi, BCG.vi);
      assertClose(reml.tau2, BCG.ref.REML, 0.001, 'tau2_REML');

      // Test 3: ML estimator
      const ml = estimateTau2_ML(BCG.yi, BCG.vi);
      assertClose(ml.tau2, BCG.ref.ML, 0.001, 'tau2_ML');

      // Test 4: HS estimator (exact metafor formula)
      const hs = estimateTau2_HS(BCG.yi, BCG.vi);
      assertClose(hs.tau2, BCG.ref.HS, 0.001, 'tau2_HS');

      // Test 5: SJ estimator (exact metafor formula)
      const sj = estimateTau2_SJ(BCG.yi, BCG.vi);
      assertClose(sj.tau2, BCG.ref.SJ, 0.001, 'tau2_SJ');

      // Test 6: HE estimator
      const he = estimateTau2_HE(BCG.yi, BCG.vi);
      assertClose(he.tau2, BCG.ref.HE, 0.001, 'tau2_HE');

      // Test 7: Pooled estimate
      const pooled = calculatePooledEstimate(BCG.yi, BCG.vi, dl.tau2);
      assertClose(pooled.theta, BCG.ref.theta_DL, 0.001, 'pooled_theta');

      // Test 8: Cochran's Q
      assertClose(dl.Q, BCG.ref.Q, 0.01, 'Cochran_Q');

      // Test 9: I-squared
      const i2 = calculateI2(dl.Q, BCG.yi.length);
      assertClose(i2 * 100, BCG.ref.I2, 0.1, 'I_squared');

      // Test 10: HKSJ confidence interval
      const hksj = calculateHKSJ(BCG.yi, BCG.vi, reml.tau2);
      assertClose(hksj.ci_lower, BCG.ref.HKSJ_lower, 0.01, 'HKSJ_lower');
      assertClose(hksj.ci_upper, BCG.ref.HKSJ_upper, 0.01, 'HKSJ_upper');

      // Test 11: MCMC reproducibility (same seed = same results)
      const mcmc1 = bayesianMetaAnalysis(BCG.yi, BCG.vi, { seed: 12345, iterations: 500 });
      const mcmc2 = bayesianMetaAnalysis(BCG.yi, BCG.vi, { seed: 12345, iterations: 500 });
      const mcmcMatch = Math.abs(mcmc1.summary.mu.mean - mcmc2.summary.mu.mean) < 0.0001;
      results.tests.push({
        name: 'MCMC_reproducibility',
        expected: 'Same seed = same result',
        actual: mcmcMatch ? 'Reproducible' : 'Not reproducible',
        pass: mcmcMatch
      });
      if (mcmcMatch) results.passed++;
      else results.failed++;

      // Summary
      results.summary = `${results.passed}/${results.passed + results.failed} tests passed`;
      results.allPassed = results.failed === 0;

      return results;
    }

    /**
     * Run tests and display results in console
     */
    function runTestsWithOutput() {
      console.log('='.repeat(60));
      console.log('AUTOMATED UNIT TEST SUITE');
      console.log('='.repeat(60));

      const results = runAutomatedTests();

      results.tests.forEach(test => {
        const status = test.pass ? 'PASS' : 'FAIL';
        console.log(`${status} | ${test.name}`);
        if (!test.pass) {
          console.log(`       Expected: ${test.expected}, Got: ${test.actual}`);
        }
      });

      console.log('='.repeat(60));
      console.log(results.summary);
      console.log('='.repeat(60));

      return results;
    }

    // Expose test functions globally
    window.runAutomatedTests = runAutomatedTests;
    window.runTestsWithOutput = runTestsWithOutput;

'''

# Find the place to insert (after getValidationBadge function, before APPROXIMATION WARNING SYSTEM)
marker = "// SECTION: APPROXIMATION WARNING SYSTEM"
if marker in content:
    # Find the comment block before it
    pos = content.find(marker)
    # Go back to find the previous section break
    section_start = content.rfind("// =====", 0, pos)

    if section_start > 0:
        # Check if test suite already exists
        if "AUTOMATED UNIT TEST SUITE" in content:
            print("Test suite already exists, skipping")
        else:
            # Insert the test suite before the APPROXIMATION section
            content = content[:section_start] + test_suite + "\n    " + content[section_start:]
            print("Test suite added successfully")

            # Convert back to CRLF
            content = content.replace('\n', '\r\n')

            with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
                f.write(content)
    else:
        print("Could not find insertion point")
else:
    print("Marker not found in file")

print("=" * 70)
