#!/usr/bin/env python3
"""Add Critical Gap functions: Mantel-Haenszel, Peto, Cook's Distance"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'C:/Truthcert1/app.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original size: {len(content):,} bytes')

# Check what already exists
existing = []
for func in ['mantelHaenszel', 'petoMethod', 'cookDistance', 'testExcessSignificance', 'renderQQPlot']:
    if func in content:
        existing.append(func)
print(f'Already exists: {existing}')

# New Critical Gap functions
critical_functions = '''
/**
 * ============================================
 * CRITICAL GAP FUNCTIONS
 * Added for Research Synthesis Methods compliance
 * ============================================
 */

/**
 * Mantel-Haenszel Method for Binary Outcomes
 * Standard method for Cochrane reviews with 2x2 data
 * No continuity corrections needed - handles zero cells naturally
 * @reference Mantel N, Haenszel W. J Natl Cancer Inst 1959;22:719-748
 * @reference Robins J, Greenland S, Breslow NE. Biometrics 1986;42:311-323
 */
function mantelHaenszel(studies, measure = 'OR') {
  // studies: array of {a, b, c, d, n1, n2} where:
  // a = events in treatment, b = non-events in treatment
  // c = events in control, d = non-events in control
  const k = studies.length;

  if (measure === 'OR') {
    // Mantel-Haenszel Odds Ratio
    let sumR = 0, sumS = 0, sumP = 0, sumQ = 0, sumPR = 0, sumQS = 0, sumPRS = 0;

    for (const s of studies) {
      const { a, b, c, d } = s;
      const n = a + b + c + d;
      if (n === 0) continue;

      const R = (a * d) / n;
      const S = (b * c) / n;
      const P = (a + d) / n;
      const Q = (b + c) / n;

      sumR += R;
      sumS += S;
      sumP += P * R;
      sumQ += Q * S;
      sumPR += P * R;
      sumQS += Q * S;
      sumPRS += (P * S + Q * R);
    }

    const OR_MH = sumR / sumS;
    const logOR = Math.log(OR_MH);

    // Robins-Breslow-Greenland variance estimator
    const varLogOR = (sumP * sumR) / (2 * sumR * sumR) +
                     (sumPRS) / (2 * sumR * sumS) +
                     (sumQ * sumS) / (2 * sumS * sumS);
    const seLogOR = Math.sqrt(varLogOR);

    const z = logOR / seLogOR;
    const pvalue = 2 * (1 - pnorm(Math.abs(z)));

    return {
      method: 'Mantel-Haenszel',
      measure: 'OR',
      estimate: OR_MH,
      logEstimate: logOR,
      se: seLogOR,
      ci_lower: Math.exp(logOR - 1.96 * seLogOR),
      ci_upper: Math.exp(logOR + 1.96 * seLogOR),
      z: z,
      pvalue: pvalue,
      k: k,
      reference: 'Mantel N, Haenszel W. J Natl Cancer Inst 1959;22:719-748'
    };
  }

  if (measure === 'RR') {
    // Mantel-Haenszel Risk Ratio
    let sumR = 0, sumS = 0, sumVar = 0;

    for (const s of studies) {
      const { a, b, c, d } = s;
      const n1 = a + b;
      const n2 = c + d;
      const n = n1 + n2;
      if (n === 0 || n1 === 0 || n2 === 0) continue;

      sumR += (a * n2) / n;
      sumS += (c * n1) / n;
      sumVar += ((a + c) * n1 * n2 - a * c * n) / (n * n);
    }

    const RR_MH = sumR / sumS;
    const logRR = Math.log(RR_MH);
    const seLogRR = Math.sqrt(sumVar / (sumR * sumS));

    const z = logRR / seLogRR;
    const pvalue = 2 * (1 - pnorm(Math.abs(z)));

    return {
      method: 'Mantel-Haenszel',
      measure: 'RR',
      estimate: RR_MH,
      logEstimate: logRR,
      se: seLogRR,
      ci_lower: Math.exp(logRR - 1.96 * seLogRR),
      ci_upper: Math.exp(logRR + 1.96 * seLogRR),
      z: z,
      pvalue: pvalue,
      k: k,
      reference: 'Greenland S, Robins JM. Stat Med 1985;4:181-200'
    };
  }

  if (measure === 'RD') {
    // Mantel-Haenszel Risk Difference
    let sumNum = 0, sumDen = 0, sumVar = 0;

    for (const s of studies) {
      const { a, b, c, d } = s;
      const n1 = a + b;
      const n2 = c + d;
      const n = n1 + n2;
      if (n === 0) continue;

      sumNum += (a * n2 - c * n1) / n;
      sumDen += (n1 * n2) / n;

      const p1 = a / n1;
      const p2 = c / n2;
      sumVar += (n1 * n2 * (p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)) / (n * n);
    }

    const RD_MH = sumNum / sumDen;
    const seRD = Math.sqrt(sumVar) / sumDen * Math.sqrt(sumDen);

    const z = RD_MH / seRD;
    const pvalue = 2 * (1 - pnorm(Math.abs(z)));

    return {
      method: 'Mantel-Haenszel',
      measure: 'RD',
      estimate: RD_MH,
      se: seRD,
      ci_lower: RD_MH - 1.96 * seRD,
      ci_upper: RD_MH + 1.96 * seRD,
      z: z,
      pvalue: pvalue,
      k: k,
      reference: 'Greenland S, Robins JM. Stat Med 1985;4:181-200'
    };
  }

  return { error: 'Unknown measure. Use OR, RR, or RD' };
}

/**
 * Peto Method for Rare Events
 * Best method for rare events (<1% event rate)
 * Critical for safety/mortality meta-analyses
 * One-step method, handles zero cells without continuity corrections
 * @reference Peto R, et al. Br J Cancer 1977;35:1-39
 * @reference Yusuf S, et al. JAMA 1985;254:1337-1343
 */
function petoMethod(studies) {
  // studies: array of {a, b, c, d} or {events1, n1, events2, n2}
  const k = studies.length;
  let sumO_E = 0;  // Sum of (O - E)
  let sumV = 0;    // Sum of variances

  const studyResults = [];

  for (let i = 0; i < k; i++) {
    const s = studies[i];

    // Handle both input formats
    const a = s.a !== undefined ? s.a : s.events1;
    const c = s.c !== undefined ? s.c : s.events2;
    const n1 = s.n1 !== undefined ? s.n1 : (s.a + s.b);
    const n2 = s.n2 !== undefined ? s.n2 : (s.c + s.d);

    const n = n1 + n2;
    const O = a;  // Observed events in treatment
    const total_events = a + c;

    if (n === 0 || total_events === 0) {
      studyResults.push({ study: i + 1, O, E: 0, V: 0, O_E: 0, excluded: true });
      continue;
    }

    // Expected under null (hypergeometric)
    const E = (n1 * total_events) / n;

    // Hypergeometric variance
    const V = (n1 * n2 * total_events * (n - total_events)) / (n * n * (n - 1));

    if (V > 0) {
      sumO_E += (O - E);
      sumV += V;
      studyResults.push({ study: i + 1, O, E: E.toFixed(2), V: V.toFixed(4), O_E: (O - E).toFixed(3), excluded: false });
    }
  }

  // Peto log odds ratio
  const logOR = sumO_E / sumV;
  const seLogOR = 1 / Math.sqrt(sumV);
  const OR = Math.exp(logOR);

  const z = logOR / seLogOR;
  const pvalue = 2 * (1 - pnorm(Math.abs(z)));

  // Heterogeneity test
  let Q = 0;
  for (const sr of studyResults) {
    if (!sr.excluded && parseFloat(sr.V) > 0) {
      const oe = parseFloat(sr.O_E);
      const v = parseFloat(sr.V);
      Q += (oe - logOR * v) * (oe - logOR * v) / v;
    }
  }
  const df = studyResults.filter(s => !s.excluded).length - 1;
  const pQ = df > 0 ? 1 - pchisq(Q, df) : 1;
  const I2 = df > 0 ? Math.max(0, (Q - df) / Q * 100) : 0;

  return {
    method: 'Peto',
    measure: 'OR',
    estimate: OR,
    logEstimate: logOR,
    se: seLogOR,
    ci_lower: Math.exp(logOR - 1.96 * seLogOR),
    ci_upper: Math.exp(logOR + 1.96 * seLogOR),
    z: z,
    pvalue: pvalue,
    k: k,
    kIncluded: studyResults.filter(s => !s.excluded).length,
    heterogeneity: {
      Q: Q,
      df: df,
      pvalue: pQ,
      I2: I2
    },
    studyDetails: studyResults,
    sumO_E: sumO_E,
    sumV: sumV,
    note: 'Best for rare events (<1% rate). Uses hypergeometric distribution.',
    reference: 'Yusuf S, et al. JAMA 1985;254:1337-1343'
  };
}

/**
 * Cook's Distance for Influence Diagnostics
 * Quantifies the influence of each study on the pooled estimate
 * @reference Cook RD. Technometrics 1977;19:15-18
 * @reference Viechtbauer W, Cheung MW. Res Synth Methods 2010;1:112-125
 */
function cookDistance(yi, vi, tau2 = null) {
  const k = yi.length;

  // Estimate tau2 if not provided (DerSimonian-Laird)
  if (tau2 === null) {
    const w = vi.map(v => 1 / v);
    const sumW = w.reduce((a, b) => a + b, 0);
    const sumW2 = w.reduce((a, b) => a + b * b, 0);
    const theta_fe = yi.reduce((s, y, i) => s + w[i] * y, 0) / sumW;
    let Q = 0;
    for (let i = 0; i < k; i++) {
      Q += w[i] * (yi[i] - theta_fe) ** 2;
    }
    tau2 = Math.max(0, (Q - (k - 1)) / (sumW - sumW2 / sumW));
  }

  // Calculate full model estimate
  const wFull = vi.map(v => 1 / (v + tau2));
  const sumWFull = wFull.reduce((a, b) => a + b, 0);
  const thetaFull = yi.reduce((s, y, i) => s + wFull[i] * y, 0) / sumWFull;
  const varThetaFull = 1 / sumWFull;

  const results = [];
  let maxCook = 0;
  let maxCookIdx = -1;

  for (let i = 0; i < k; i++) {
    // Leave-one-out estimate
    let sumW_loo = 0, sumWY_loo = 0;
    for (let j = 0; j < k; j++) {
      if (j !== i) {
        sumW_loo += wFull[j];
        sumWY_loo += wFull[j] * yi[j];
      }
    }
    const theta_loo = sumWY_loo / sumW_loo;

    // Cook's distance
    const diff = thetaFull - theta_loo;
    const cookD = (diff * diff) / varThetaFull;

    // Standardized residual
    const r = (yi[i] - thetaFull) / Math.sqrt(vi[i] + tau2);

    // Leverage (hat value)
    const h = wFull[i] / sumWFull;

    // DFBETAS (standardized difference in coefficient)
    const dfbetas = diff / Math.sqrt(varThetaFull);

    // DFFITS
    const dffits = r * Math.sqrt(h / (1 - h));

    // Covariance ratio
    const covRatio = (1 - h) * (k - 1) / (k - 2);

    results.push({
      study: i + 1,
      cookD: parseFloat(cookD.toFixed(4)),
      dfbetas: parseFloat(dfbetas.toFixed(4)),
      dffits: parseFloat(dffits.toFixed(4)),
      leverage: parseFloat(h.toFixed(4)),
      residual: parseFloat(r.toFixed(4)),
      covRatio: parseFloat(covRatio.toFixed(4)),
      theta_loo: parseFloat(theta_loo.toFixed(4)),
      influential: cookD > 4 / k  // Common threshold
    });

    if (cookD > maxCook) {
      maxCook = cookD;
      maxCookIdx = i;
    }
  }

  // Threshold for influential studies (4/k is common)
  const threshold = 4 / k;
  const influentialStudies = results.filter(r => r.influential);

  return {
    method: "Cook's Distance",
    results: results,
    threshold: parseFloat(threshold.toFixed(4)),
    maxCookD: parseFloat(maxCook.toFixed(4)),
    maxCookStudy: maxCookIdx + 1,
    influentialCount: influentialStudies.length,
    influentialStudies: influentialStudies.map(s => s.study),
    thetaFull: parseFloat(thetaFull.toFixed(4)),
    tau2: parseFloat(tau2.toFixed(4)),
    interpretation: influentialStudies.length === 0
      ? "No overly influential studies detected"
      : `${influentialStudies.length} influential study(ies) detected (Cook's D > ${threshold.toFixed(3)})`,
    reference: "Viechtbauer W, Cheung MW. Res Synth Methods 2010;1:112-125"
  };
}

/**
 * Convert 2x2 table to effect sizes for M-H and Peto methods
 */
function convertToABCD(studies) {
  return studies.map(s => {
    if (s.a !== undefined) return s;
    return {
      a: s.events1 || 0,
      b: (s.n1 || 0) - (s.events1 || 0),
      c: s.events2 || 0,
      d: (s.n2 || 0) - (s.events2 || 0),
      n1: s.n1,
      n2: s.n2,
      name: s.name || s.study
    };
  });
}

'''

# Find insertion point - before testExcessSignificance
marker = '/**\n * Test of Excess Significance (TES)'
idx = content.find(marker)

if idx == -1:
    # Try alternate marker
    marker = 'function testExcessSignificance'
    idx = content.find(marker)
    if idx != -1:
        # Find the comment block before it
        idx = content.rfind('/**', 0, idx)

if idx == -1:
    print("ERROR: Could not find insertion point")
else:
    # Check if already added
    if 'mantelHaenszel' in content:
        print("Mantel-Haenszel already exists - skipping")
    elif 'petoMethod' in content:
        print("Peto Method already exists - skipping")
    elif 'cookDistance' in content:
        print("Cook's Distance already exists - skipping")
    else:
        new_content = content[:idx] + critical_functions + '\n' + content[idx:]

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f'Final size: {len(new_content):,} bytes')
        print(f'Added {len(critical_functions):,} characters')
        print('SUCCESS: Added Mantel-Haenszel, Peto, and Cook\'s Distance!')

# Verify
with open(file_path, 'r', encoding='utf-8') as f:
    final = f.read()

for func in ['mantelHaenszel', 'petoMethod', 'cookDistance', 'testExcessSignificance', 'renderQQPlot']:
    status = 'FOUND' if func in final else 'MISSING'
    print(f'{func}: {status}')
