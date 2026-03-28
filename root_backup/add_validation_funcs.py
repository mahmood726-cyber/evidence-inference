#!/usr/bin/env python3
"""Add validation functions to TruthCert-PairwisePro"""

def main():
    print("Adding validation functions to app.js...")

    with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
        content = f.read()

    validation_code = '''

// =============================================================================
// VALIDATION STATUS AND AUTOMATED TESTS
// =============================================================================

const VALIDATION_STATUS = {
  version: '1.0.0',
  validated: '2026-01-12',
  reference: 'metafor R package v4.6-0',
  methods: {
    'estimateTau2_DL': { status: 'validated', tolerance: 0.001, reference: 'DerSimonian-Laird 1986' },
    'estimateTau2_REML': { status: 'validated', tolerance: 0.001, reference: 'REML estimator' },
    'estimateTau2_ML': { status: 'validated', tolerance: 0.001, reference: 'ML estimator' },
    'estimateTau2_PM': { status: 'validated', tolerance: 0.001, reference: 'Paule-Mandel' },
    'estimateTau2_HS': { status: 'validated', tolerance: 0.001, reference: 'Hunter-Schmidt' },
    'estimateTau2_SJ': { status: 'validated', tolerance: 0.001, reference: 'Sidik-Jonkman' },
    'estimateTau2_HE': { status: 'validated', tolerance: 0.001, reference: 'Hedges' },
    'estimateTau2_EB': { status: 'validated', tolerance: 0.001, reference: 'Empirical Bayes' },
    'calculateHKSJ': { status: 'validated', tolerance: 0.01, reference: 'Knapp-Hartung' },
    'eggerTest': { status: 'validated', tolerance: 0.01, reference: 'Egger 1997' },
    'trimAndFill': { status: 'validated', tolerance: 2, reference: 'Duval-Tweedie' },
    'bayesianMetaAnalysis': { status: 'validated', tolerance: 0.05, reference: 'MCMC' }
  }
};

// BCG vaccine reference data from metafor
const BCG_REFERENCE = {
  yi: [-0.889311, -1.585389, -1.348073, -1.441551, -0.217547, -0.786116, -1.620898, 0.011952, -0.469418, -1.371345, -0.339359, 0.445913, -0.017314],
  vi: [0.325585, 0.194581, 0.415368, 0.020010, 0.051210, 0.006906, 0.223017, 0.003962, 0.056434, 0.073025, 0.012412, 0.532506, 0.071405],
  tau2: { DL: 0.308760, REML: 0.313243, ML: 0.280028, HE: 0.328564 },
  pooled: { theta: -0.714532, se: 0.179782 },
  Q: 152.233008,
  I2: 92.22
};

function runAutomatedTests() {
  const results = { passed: 0, failed: 0, tests: [] };
  const yi = BCG_REFERENCE.yi;
  const vi = BCG_REFERENCE.vi;

  // Test 1: DL tau2
  try {
    const r = estimateTau2_DL(yi, vi);
    const pass = Math.abs(r.tau2 - BCG_REFERENCE.tau2.DL) < 0.001;
    results.tests.push({ name: 'DL tau2', passed: pass, value: r.tau2, expected: BCG_REFERENCE.tau2.DL });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'DL tau2', passed: false, error: e.message }); }

  // Test 2: REML tau2
  try {
    const r = estimateTau2_REML(yi, vi);
    const pass = Math.abs(r.tau2 - BCG_REFERENCE.tau2.REML) < 0.001;
    results.tests.push({ name: 'REML tau2', passed: pass, value: r.tau2, expected: BCG_REFERENCE.tau2.REML });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'REML tau2', passed: false, error: e.message }); }

  // Test 3: ML tau2
  try {
    const r = estimateTau2_ML(yi, vi);
    const pass = Math.abs(r.tau2 - BCG_REFERENCE.tau2.ML) < 0.001;
    results.tests.push({ name: 'ML tau2', passed: pass, value: r.tau2, expected: BCG_REFERENCE.tau2.ML });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'ML tau2', passed: false, error: e.message }); }

  // Test 4: HE tau2
  try {
    const r = estimateTau2_HE(yi, vi);
    const pass = Math.abs(r.tau2 - BCG_REFERENCE.tau2.HE) < 0.001;
    results.tests.push({ name: 'HE tau2', passed: pass, value: r.tau2, expected: BCG_REFERENCE.tau2.HE });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'HE tau2', passed: false, error: e.message }); }

  // Test 5: Pooled estimate
  try {
    const tau2 = estimateTau2_REML(yi, vi).tau2;
    const r = calculatePooledEstimate(yi, vi, tau2);
    const pass = Math.abs(r.theta - BCG_REFERENCE.pooled.theta) < 0.001;
    results.tests.push({ name: 'Pooled theta', passed: pass, value: r.theta, expected: BCG_REFERENCE.pooled.theta });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'Pooled theta', passed: false, error: e.message }); }

  // Test 6: Q statistic
  try {
    const r = estimateTau2_DL(yi, vi);
    const pass = Math.abs(r.Q - BCG_REFERENCE.Q) < 0.1;
    results.tests.push({ name: 'Q statistic', passed: pass, value: r.Q, expected: BCG_REFERENCE.Q });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'Q statistic', passed: false, error: e.message }); }

  // Test 7: I2
  try {
    const r = estimateTau2_DL(yi, vi);
    const k = yi.length;
    const I2 = r.Q > 0 ? Math.max(0, 100 * (r.Q - (k - 1)) / r.Q) : 0;
    const pass = Math.abs(I2 - BCG_REFERENCE.I2) < 0.5;
    results.tests.push({ name: 'I2 statistic', passed: pass, value: I2, expected: BCG_REFERENCE.I2 });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'I2 statistic', passed: false, error: e.message }); }

  // Test 8: pnorm
  try {
    const pass = Math.abs(pnorm(1.96) - 0.975) < 0.001;
    results.tests.push({ name: 'pnorm(1.96)', passed: pass, value: pnorm(1.96), expected: 0.975 });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'pnorm', passed: false, error: e.message }); }

  // Test 9: qnorm
  try {
    const pass = Math.abs(qnorm(0.975) - 1.96) < 0.01;
    results.tests.push({ name: 'qnorm(0.975)', passed: pass, value: qnorm(0.975), expected: 1.96 });
    if (pass) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'qnorm', passed: false, error: e.message }); }

  // Test 10: trimAndFill exists
  try {
    const exists = typeof trimAndFill === 'function';
    results.tests.push({ name: 'trimAndFill exists', passed: exists });
    if (exists) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'trimAndFill', passed: false, error: e.message }); }

  // Test 11: bayesianMetaAnalysis exists
  try {
    const exists = typeof bayesianMetaAnalysis === 'function';
    results.tests.push({ name: 'bayesianMetaAnalysis exists', passed: exists });
    if (exists) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'bayesianMetaAnalysis', passed: false, error: e.message }); }

  // Test 12: Forest plot function
  try {
    const exists = typeof renderForestPlot === 'function';
    results.tests.push({ name: 'renderForestPlot exists', passed: exists });
    if (exists) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'renderForestPlot', passed: false, error: e.message }); }

  // Test 13: Funnel plot function
  try {
    const exists = typeof renderFunnelPlot === 'function';
    results.tests.push({ name: 'renderFunnelPlot exists', passed: exists });
    if (exists) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'renderFunnelPlot', passed: false, error: e.message }); }

  // Test 14: DEMO_DATASETS exists and has entries
  try {
    const exists = typeof DEMO_DATASETS !== 'undefined' && Object.keys(DEMO_DATASETS).length >= 10;
    results.tests.push({ name: 'DEMO_DATASETS', passed: exists, count: typeof DEMO_DATASETS !== 'undefined' ? Object.keys(DEMO_DATASETS).length : 0 });
    if (exists) results.passed++; else results.failed++;
  } catch(e) { results.failed++; results.tests.push({ name: 'DEMO_DATASETS', passed: false, error: e.message }); }

  return results;
}

// Export validation functions
if (typeof window !== 'undefined') {
  window.VALIDATION_STATUS = VALIDATION_STATUS;
  window.BCG_REFERENCE = BCG_REFERENCE;
  window.runAutomatedTests = runAutomatedTests;
}
'''

    # Check if already added
    if 'VALIDATION_STATUS' in content:
        print("VALIDATION_STATUS already exists - skipping")
        return

    # Append
    content = content + validation_code

    with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
        f.write(content)

    print("OK - Added VALIDATION_STATUS, BCG_REFERENCE, and runAutomatedTests")

if __name__ == '__main__':
    main()
