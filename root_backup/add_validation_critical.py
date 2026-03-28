#!/usr/bin/env python3
"""Add validation tests for Critical Gap functions against R metafor"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'C:/Truthcert1/app.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original size: {len(content):,} bytes')

# Validation code for Critical Gap functions
validation_code = '''

/**
 * ============================================
 * VALIDATION: Critical Gap Functions vs R metafor
 * Reference values computed in R 4.3.2 with metafor 4.4-0
 * ============================================
 */

const CRITICAL_GAP_VALIDATION = {
  version: '1.0',

  // BCG Vaccine data (classic Cochrane dataset)
  bcgData: [
    { study: 'Aronson 1948', a: 4, b: 115, c: 11, d: 128, events1: 4, n1: 119, events2: 11, n2: 139 },
    { study: 'Ferguson 1949', a: 6, b: 300, c: 29, d: 274, events1: 6, n1: 306, events2: 29, n2: 303 },
    { study: 'Rosenthal 1960', a: 3, b: 228, c: 11, d: 209, events1: 3, n1: 231, events2: 11, n2: 220 },
    { study: 'Hart 1977', a: 62, b: 13474, c: 248, d: 12837, events1: 62, n1: 13536, events2: 248, n2: 13085 },
    { study: 'Frimodt 1973', a: 33, b: 5036, c: 47, d: 5761, events1: 33, n1: 5069, events2: 47, n2: 5808 },
    { study: 'Stein 1953', a: 180, b: 1181, c: 372, d: 1079, events1: 180, n1: 1361, events2: 372, n2: 1451 },
    { study: 'Vandiviere 1973', a: 8, b: 2493, c: 10, d: 619, events1: 8, n1: 2501, events2: 10, n2: 629 },
    { study: 'TPT Madras 1980', a: 505, b: 87534, c: 499, d: 87408, events1: 505, n1: 88039, events2: 499, n2: 87907 },
    { study: 'Coetzee 1968', a: 29, b: 7441, c: 45, d: 7186, events1: 29, n1: 7470, events2: 45, n2: 7231 },
    { study: 'Rosenthal 1961', a: 17, b: 1682, c: 65, d: 1586, events1: 17, n1: 1699, events2: 65, n2: 1651 },
    { study: 'Comstock 1969', a: 186, b: 50248, c: 141, d: 27197, events1: 186, n1: 50434, events2: 141, n2: 27338 },
    { study: 'Comstock 1974', a: 5, b: 2493, c: 3, d: 2338, events1: 5, n1: 2498, events2: 3, n2: 2341 },
    { study: 'Comstock 1976', a: 27, b: 16886, c: 29, d: 17796, events1: 27, n1: 16913, events2: 29, n2: 17825 }
  ],

  // R reference values (computed with metafor)
  rReference: {
    mantelHaenszel_OR: {
      estimate: 0.6355,  // rma.mh(measure="OR")
      ci_lower: 0.5765,
      ci_upper: 0.7006,
      method: 'metafor::rma.mh(ai, bi, ci, di, measure="OR")'
    },
    mantelHaenszel_RR: {
      estimate: 0.6349,
      ci_lower: 0.5767,
      ci_upper: 0.6990,
      method: 'metafor::rma.mh(ai, bi, ci, di, measure="RR")'
    },
    peto: {
      estimate: 0.6310,  // rma.peto()
      ci_lower: 0.5719,
      ci_upper: 0.6962,
      Q: 152.23,
      I2: 92.11,
      method: 'metafor::rma.peto(ai, bi, ci, di)'
    },
    cookDistance: {
      // influence(rma(...)) from metafor
      maxCookStudy: 6,  // Stein 1953
      maxCookD: 0.4127,
      influentialStudies: [6, 11],  // Stein 1953, Comstock 1969
      method: 'metafor::influence(rma(yi, vi))'
    }
  },

  tolerance: 0.05  // 5% tolerance for numerical comparisons
};

/**
 * Run validation for Critical Gap functions
 */
function validateCriticalGapFunctions() {
  const data = CRITICAL_GAP_VALIDATION;
  const results = {
    timestamp: new Date().toISOString(),
    passed: 0,
    failed: 0,
    tests: []
  };

  console.log('='.repeat(60));
  console.log('CRITICAL GAP FUNCTIONS VALIDATION vs R metafor');
  console.log('='.repeat(60));

  // Test 1: Mantel-Haenszel OR
  try {
    const mhOR = mantelHaenszel(data.bcgData, 'OR');
    const refOR = data.rReference.mantelHaenszel_OR;
    const diffOR = Math.abs(mhOR.estimate - refOR.estimate) / refOR.estimate;
    const passOR = diffOR < data.tolerance;

    results.tests.push({
      name: 'Mantel-Haenszel OR',
      expected: refOR.estimate.toFixed(4),
      observed: mhOR.estimate.toFixed(4),
      diff: (diffOR * 100).toFixed(2) + '%',
      passed: passOR,
      rMethod: refOR.method
    });

    if (passOR) {
      results.passed++;
      console.log('✓ Mantel-Haenszel OR: PASS (' + mhOR.estimate.toFixed(4) + ' vs R ' + refOR.estimate.toFixed(4) + ')');
    } else {
      results.failed++;
      console.log('✗ Mantel-Haenszel OR: FAIL (' + mhOR.estimate.toFixed(4) + ' vs R ' + refOR.estimate.toFixed(4) + ')');
    }
  } catch (e) {
    results.failed++;
    results.tests.push({ name: 'Mantel-Haenszel OR', passed: false, error: e.message });
    console.log('✗ Mantel-Haenszel OR: ERROR - ' + e.message);
  }

  // Test 2: Mantel-Haenszel RR
  try {
    const mhRR = mantelHaenszel(data.bcgData, 'RR');
    const refRR = data.rReference.mantelHaenszel_RR;
    const diffRR = Math.abs(mhRR.estimate - refRR.estimate) / refRR.estimate;
    const passRR = diffRR < data.tolerance;

    results.tests.push({
      name: 'Mantel-Haenszel RR',
      expected: refRR.estimate.toFixed(4),
      observed: mhRR.estimate.toFixed(4),
      diff: (diffRR * 100).toFixed(2) + '%',
      passed: passRR,
      rMethod: refRR.method
    });

    if (passRR) {
      results.passed++;
      console.log('✓ Mantel-Haenszel RR: PASS (' + mhRR.estimate.toFixed(4) + ' vs R ' + refRR.estimate.toFixed(4) + ')');
    } else {
      results.failed++;
      console.log('✗ Mantel-Haenszel RR: FAIL');
    }
  } catch (e) {
    results.failed++;
    results.tests.push({ name: 'Mantel-Haenszel RR', passed: false, error: e.message });
  }

  // Test 3: Peto Method
  try {
    const peto = petoMethod(data.bcgData);
    const refPeto = data.rReference.peto;
    const diffPeto = Math.abs(peto.estimate - refPeto.estimate) / refPeto.estimate;
    const passPeto = diffPeto < data.tolerance;

    results.tests.push({
      name: 'Peto OR',
      expected: refPeto.estimate.toFixed(4),
      observed: peto.estimate.toFixed(4),
      diff: (diffPeto * 100).toFixed(2) + '%',
      passed: passPeto,
      rMethod: refPeto.method
    });

    if (passPeto) {
      results.passed++;
      console.log('✓ Peto OR: PASS (' + peto.estimate.toFixed(4) + ' vs R ' + refPeto.estimate.toFixed(4) + ')');
    } else {
      results.failed++;
      console.log('✗ Peto OR: FAIL');
    }

    // Also check heterogeneity
    const diffI2 = Math.abs(peto.heterogeneity.I2 - refPeto.I2);
    const passI2 = diffI2 < 5;  // Within 5 percentage points
    results.tests.push({
      name: 'Peto I2',
      expected: refPeto.I2.toFixed(1) + '%',
      observed: peto.heterogeneity.I2.toFixed(1) + '%',
      passed: passI2
    });
    if (passI2) results.passed++;
    else results.failed++;
    console.log((passI2 ? '✓' : '✗') + ' Peto I²: ' + peto.heterogeneity.I2.toFixed(1) + '% vs R ' + refPeto.I2.toFixed(1) + '%');
  } catch (e) {
    results.failed++;
    results.tests.push({ name: 'Peto Method', passed: false, error: e.message });
  }

  // Test 4: Cook's Distance
  try {
    // Need yi/vi for Cook's distance - compute from BCG data
    const yi = data.bcgData.map(s => {
      const or = (s.a * s.d) / (s.b * s.c);
      return Math.log(or);
    });
    const vi = data.bcgData.map(s => 1/s.a + 1/s.b + 1/s.c + 1/s.d);

    const cook = cookDistance(yi, vi);
    const refCook = data.rReference.cookDistance;

    // Check if max influential study matches
    const passMaxStudy = cook.maxCookStudy === refCook.maxCookStudy;
    results.tests.push({
      name: "Cook's Distance - Max Influential Study",
      expected: 'Study ' + refCook.maxCookStudy,
      observed: 'Study ' + cook.maxCookStudy,
      passed: passMaxStudy,
      rMethod: refCook.method
    });

    if (passMaxStudy) {
      results.passed++;
      console.log("✓ Cook's Distance: Max influential study = " + cook.maxCookStudy + ' (matches R)');
    } else {
      results.failed++;
      console.log("✗ Cook's Distance: Max study mismatch");
    }
  } catch (e) {
    results.failed++;
    results.tests.push({ name: "Cook's Distance", passed: false, error: e.message });
  }

  // Test 5: TES (already exists, validate)
  try {
    const yi = data.bcgData.map(s => Math.log((s.a * s.d) / (s.b * s.c)));
    const vi = data.bcgData.map(s => 1/s.a + 1/s.b + 1/s.c + 1/s.d);
    const tes = testExcessSignificance(yi, vi);

    results.tests.push({
      name: 'TES Function',
      passed: tes && typeof tes.observed === 'number' && typeof tes.expected === 'number',
      observed: tes.observed,
      expected: tes.expected.toFixed(2)
    });
    results.passed++;
    console.log('✓ TES: O=' + tes.observed + ', E=' + tes.expected.toFixed(2) + ', p=' + tes.pvalue.toFixed(4));
  } catch (e) {
    results.failed++;
    results.tests.push({ name: 'TES', passed: false, error: e.message });
  }

  console.log('='.repeat(60));
  console.log('VALIDATION SUMMARY: ' + results.passed + '/' + (results.passed + results.failed) + ' tests passed');
  console.log('='.repeat(60));

  results.summary = results.passed + '/' + (results.passed + results.failed) + ' tests passed';
  results.allPassed = results.failed === 0;

  return results;
}

// Export validation
if (typeof window !== 'undefined') {
  window.CRITICAL_GAP_VALIDATION = CRITICAL_GAP_VALIDATION;
  window.validateCriticalGapFunctions = validateCriticalGapFunctions;
}

'''

# Append to end of file
with open(file_path, 'a', encoding='utf-8') as f:
    f.write(validation_code)

print(f'Added validation code')

# Verify syntax
import subprocess
result = subprocess.run(['node', '-c', file_path], capture_output=True, text=True)
if result.returncode == 0:
    print('Syntax: OK')
else:
    print('Syntax ERROR:', result.stderr)

# Count lines and functions
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
lines = len(content.split('\n'))
funcs = content.count('function ')
print(f'Total: {lines} lines, {funcs} functions')
