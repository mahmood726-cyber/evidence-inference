#!/usr/bin/env python3
"""Add TES and QQ Plot functions to app.js"""

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if already added
if 'testExcessSignificance' in content:
    print("TES already exists!")
elif 'renderQQPlot' in content:
    print("QQ Plot already exists!")
else:
    # Find the insertion point (before DEMO_DATASETS)
    marker = 'const DEMO_DATASETS = {'
    idx = content.find(marker)

    if idx == -1:
        print("ERROR: Could not find DEMO_DATASETS marker")
    else:
        new_functions = '''
/**
 * Test of Excess Significance (TES)
 * Ioannidis-Trikalinos test for detecting publication bias / p-hacking
 * @reference Ioannidis JPA, Trikalinos TA. Clin Trials 2007;4:245-253
 */
function testExcessSignificance(yi, vi, theta0 = null) {
  const k = yi.length;
  const sei = vi.map(v => Math.sqrt(v));
  if (theta0 === null) {
    const w = vi.map(v => 1 / v);
    const sumW = w.reduce((a, b) => a + b, 0);
    theta0 = yi.reduce((s, y, i) => s + w[i] * y, 0) / sumW;
  }
  let O = 0;
  for (let i = 0; i < k; i++) {
    const z = Math.abs(yi[i]) / sei[i];
    if (z > 1.96) O++;
  }
  let E = 0;
  for (let i = 0; i < k; i++) {
    const ncp = Math.abs(theta0) / sei[i];
    const power = 1 - pnorm(1.96 - ncp) + pnorm(-1.96 - ncp);
    E += power;
  }
  if (E < 0.001) E = 0.001;
  const A = O - E;
  const chi2 = (A * A) / E;
  const pval = 1 - pchisq(chi2, 1);
  const avgPower = E / k;
  return {
    observed: O,
    expected: parseFloat(E.toFixed(2)),
    excess: parseFloat(A.toFixed(2)),
    chi2: parseFloat(chi2.toFixed(3)),
    pvalue: parseFloat(pval.toFixed(4)),
    avgPower: parseFloat((avgPower * 100).toFixed(1)),
    theta0: parseFloat(theta0.toFixed(4)),
    k: k,
    ratio: parseFloat((O / Math.max(E, 0.01)).toFixed(2)),
    interpretation: pval < 0.10 ? "Evidence of excess significance (possible publication bias or p-hacking)" : "No evidence of excess significance",
    significant: pval < 0.10,
    method: "Ioannidis-Trikalinos TES",
    reference: "Ioannidis JPA, Trikalinos TA. Clin Trials 2007;4:245-253"
  };
}

/**
 * Get standardized residuals for QQ plot
 */
function getStandardizedResiduals(yi, vi, tau2) {
  const k = yi.length;
  const w = vi.map(v => 1 / (v + tau2));
  const sumW = w.reduce((a, b) => a + b, 0);
  const theta = yi.reduce((s, y, i) => s + w[i] * y, 0) / sumW;
  return yi.map((y, i) => (y - theta) / Math.sqrt(vi[i] + tau2));
}

/**
 * Calculate Pearson correlation for QQ plot
 */
function calculatePearsonCorrelation(x, y) {
  const n = x.length;
  const meanX = x.reduce((a, b) => a + b, 0) / n;
  const meanY = y.reduce((a, b) => a + b, 0) / n;
  let num = 0, denX = 0, denY = 0;
  for (let i = 0; i < n; i++) {
    const dx = x[i] - meanX;
    const dy = y[i] - meanY;
    num += dx * dy;
    denX += dx * dx;
    denY += dy * dy;
  }
  return num / Math.sqrt(denX * denY);
}

/**
 * Render QQ Plot for standardized residuals
 * Tests normality assumption of random effects model
 */
function renderQQPlot(residuals, containerId, studyNames = null) {
  const n = residuals.length;
  const indexed = residuals.map((r, i) => ({ r, i, name: studyNames ? studyNames[i] : "Study " + (i + 1) }));
  indexed.sort((a, b) => a.r - b.r);
  const sorted = indexed.map(x => x.r);
  const names = indexed.map(x => x.name);
  const theoretical = [];
  for (let i = 0; i < n; i++) {
    const p = (i + 0.375) / (n + 0.25);
    theoretical.push(qnorm(p));
  }
  const q1Idx = Math.floor(n * 0.25);
  const q3Idx = Math.floor(n * 0.75);
  const slope = (sorted[q3Idx] - sorted[q1Idx]) / (theoretical[q3Idx] - theoretical[q1Idx]);
  const intercept = sorted[q1Idx] - slope * theoretical[q1Idx];
  const correlation = calculatePearsonCorrelation(theoretical, sorted);
  const W = correlation * correlation;
  const pointsTrace = {
    x: theoretical,
    y: sorted,
    mode: "markers",
    type: "scatter",
    name: "Residuals",
    text: names,
    hovertemplate: "%{text}<br>Theoretical: %{x:.2f}<br>Sample: %{y:.2f}<extra></extra>",
    marker: { size: 10, color: "#3B82F6", line: { color: "#1E40AF", width: 1 } }
  };
  const minX = Math.min(...theoretical) - 0.2;
  const maxX = Math.max(...theoretical) + 0.2;
  const refLineTrace = {
    x: [minX, maxX],
    y: [intercept + slope * minX, intercept + slope * maxX],
    mode: "lines",
    type: "scatter",
    name: "Reference Line",
    line: { dash: "dash", color: "#EF4444", width: 2 }
  };
  const bandX = [], bandUpper = [], bandLower = [];
  for (let x = minX; x <= maxX; x += 0.1) {
    bandX.push(x);
    const se = Math.sqrt(1 / n) * (1 + 0.5 * x * x);
    bandUpper.push(intercept + slope * x + 1.96 * se);
    bandLower.push(intercept + slope * x - 1.96 * se);
  }
  const bandTrace = {
    x: [...bandX, ...bandX.reverse()],
    y: [...bandUpper, ...bandLower.reverse()],
    fill: "toself",
    fillcolor: "rgba(239, 68, 68, 0.1)",
    line: { color: "transparent" },
    type: "scatter",
    name: "95% CI",
    showlegend: true,
    hoverinfo: "skip"
  };
  const layout = {
    title: { text: "Normal Q-Q Plot of Standardized Residuals", font: { size: 16 } },
    xaxis: { title: "Theoretical Quantiles", zeroline: true, zerolinecolor: "#ccc" },
    yaxis: { title: "Sample Quantiles", zeroline: true, zerolinecolor: "#ccc" },
    showlegend: true,
    legend: { x: 0.02, y: 0.98 },
    annotations: [{
      x: maxX - 0.3,
      y: Math.min(...sorted) + 0.5,
      text: "W = " + W.toFixed(3) + "<br>" + (W > 0.95 ? "Normal" : W > 0.90 ? "Borderline" : "Non-normal"),
      showarrow: false,
      font: { size: 11 },
      bgcolor: "rgba(255,255,255,0.8)",
      bordercolor: "#ccc",
      borderwidth: 1
    }],
    hovermode: "closest"
  };
  Plotly.newPlot(containerId, [bandTrace, refLineTrace, pointsTrace], layout, { responsive: true });
  return {
    W: W,
    correlation: correlation,
    interpretation: W > 0.95 ? "Residuals appear normally distributed" : W > 0.90 ? "Residuals show slight departure from normality" : "Residuals show significant departure from normality",
    n: n
  };
}

'''
        # Insert before DEMO_DATASETS
        new_content = content[:idx] + new_functions + content[idx:]

        with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("SUCCESS: Added testExcessSignificance and renderQQPlot functions!")
        print(f"Inserted {len(new_functions)} characters before DEMO_DATASETS")
