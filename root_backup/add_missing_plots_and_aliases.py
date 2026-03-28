#!/usr/bin/env python3
"""Add missing plots (Radial, L'Abbé) and function name aliases to TruthCert-PairwisePro"""

def main():
    print("=" * 70)
    print("Adding Missing Plots and Function Aliases")
    print("=" * 70)

    with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
        content = f.read()

    additions = []

    # ==========================================================================
    # 1. RADIAL (GALBRAITH) PLOT
    # ==========================================================================
    if 'renderRadialPlot' not in content:
        print("\n[1] Adding Radial/Galbraith Plot...")
        radial_plot = '''

// =============================================================================
// RADIAL (GALBRAITH) PLOT
// Reference: Galbraith RF. A note on graphical presentation of estimated odds ratios
//            from several clinical trials. Stat Med. 1988;7(8):889-894.
// =============================================================================

function renderRadialPlot(results, containerId = 'radialPlot') {
  try {
    if (typeof Plotly === 'undefined') {
      console.error('Plotly not loaded for Radial plot');
      return;
    }

    const container = document.getElementById(containerId);
    if (!container) {
      console.error('Radial plot container not found:', containerId);
      return;
    }

    // Clear existing plot
    if (container._fullLayout) Plotly.purge(container);

    const colors = getThemeColors();
    const yi = results.yi || results.studies.map(s => s.yi);
    const vi = results.vi || results.studies.map(s => s.vi);
    const sei = vi.map(v => Math.sqrt(v));
    const names = results.studyNames || results.studies.map(s => s.name);
    const pooled = results.pooled?.theta || results.theta;

    // Radial plot: x = 1/SE (precision), y = yi/SE (z-score)
    const precision = sei.map(se => 1 / se);
    const zScores = yi.map((y, i) => y / sei[i]);

    // Regression line through origin with slope = pooled effect
    const maxPrecision = Math.max(...precision) * 1.1;

    // Study points
    const studyTrace = {
      x: precision,
      y: zScores,
      mode: 'markers+text',
      type: 'scatter',
      marker: {
        size: 10,
        color: '#4a7ab8',
        line: { color: '#1b263b', width: 1 }
      },
      text: names,
      textposition: 'top right',
      textfont: { size: 9, color: colors.text },
      hovertemplate: '%{text}<br>Precision (1/SE): %{x:.2f}<br>Z-score: %{y:.2f}<extra></extra>',
      name: 'Studies'
    };

    // Regression line (slope = pooled effect)
    const regressionTrace = {
      x: [0, maxPrecision],
      y: [0, pooled * maxPrecision],
      mode: 'lines',
      type: 'scatter',
      line: { color: '#ef4444', width: 2 },
      hoverinfo: 'skip',
      name: 'Pooled Effect'
    };

    // 95% CI bounds (slope = pooled ± 1.96)
    const ciUpper = {
      x: [0, maxPrecision],
      y: [1.96, 1.96 + pooled * maxPrecision],
      mode: 'lines',
      type: 'scatter',
      line: { color: '#94a3b8', width: 1, dash: 'dash' },
      hoverinfo: 'skip',
      showlegend: false
    };

    const ciLower = {
      x: [0, maxPrecision],
      y: [-1.96, -1.96 + pooled * maxPrecision],
      mode: 'lines',
      type: 'scatter',
      line: { color: '#94a3b8', width: 1, dash: 'dash' },
      hoverinfo: 'skip',
      showlegend: false
    };

    // Zero line
    const zeroLine = {
      x: [0, maxPrecision],
      y: [0, 0],
      mode: 'lines',
      type: 'scatter',
      line: { color: colors.grid, width: 1 },
      hoverinfo: 'skip',
      showlegend: false
    };

    const layout = {
      title: {
        text: 'Radial (Galbraith) Plot',
        font: { family: 'Plus Jakarta Sans', size: 14, color: colors.text }
      },
      xaxis: {
        title: 'Precision (1/SE)',
        zeroline: true,
        zerolinecolor: colors.grid,
        gridcolor: colors.grid,
        tickfont: { family: 'JetBrains Mono', size: 11, color: colors.text },
        range: [0, maxPrecision]
      },
      yaxis: {
        title: 'Standardized Effect (z = yi/SE)',
        zeroline: true,
        zerolinecolor: colors.grid,
        gridcolor: colors.grid,
        tickfont: { family: 'JetBrains Mono', size: 11, color: colors.text }
      },
      showlegend: true,
      legend: { x: 0.02, y: 0.98, font: { size: 10, color: colors.text } },
      margin: { l: 70, r: 40, t: 50, b: 50 },
      paper_bgcolor: colors.background,
      plot_bgcolor: colors.background,
      hoverlabel: {
        bgcolor: colors.hoverBg,
        bordercolor: colors.hoverBorder,
        font: { family: 'Plus Jakarta Sans', color: colors.hoverText }
      },
      annotations: [{
        x: maxPrecision * 0.95,
        y: pooled * maxPrecision * 0.95,
        text: 'Pooled: ' + pooled.toFixed(3),
        showarrow: false,
        font: { size: 10, color: '#ef4444' }
      }]
    };

    Plotly.newPlot(containerId, [zeroLine, ciLower, ciUpper, regressionTrace, studyTrace], layout, {
      displayModeBar: false,
      responsive: true
    });

    console.log('Radial plot rendered successfully');

  } catch (e) {
    console.error('Radial plot rendering failed:', e);
    showPlotError(containerId, 'Failed to render Radial plot: ' + e.message);
  }
}

// Alias for common naming
var renderGalbraithPlot = renderRadialPlot;

if (typeof window !== 'undefined') {
  window.renderRadialPlot = renderRadialPlot;
  window.renderGalbraithPlot = renderGalbraithPlot;
}
'''
        additions.append(('Radial Plot', radial_plot))
        print("    OK - Added renderRadialPlot function")
    else:
        print("\n[1] Radial plot already exists - skipping")

    # ==========================================================================
    # 2. L'ABBÉ PLOT
    # ==========================================================================
    if 'renderLabbePlot' not in content:
        print("\n[2] Adding L'Abbé Plot...")
        labbe_plot = '''

// =============================================================================
// L'ABBÉ PLOT
// Reference: L'Abbé KA, Detsky AS, O'Rourke K. Meta-analysis in clinical research.
//            Ann Intern Med. 1987;107(2):224-233.
// Shows treatment vs control event rates - useful for binary outcomes
// =============================================================================

function renderLabbePlot(results, containerId = 'labbePlot') {
  try {
    if (typeof Plotly === 'undefined') {
      console.error('Plotly not loaded for L\\'Abbé plot');
      return;
    }

    const container = document.getElementById(containerId);
    if (!container) {
      console.error('L\\'Abbé plot container not found:', containerId);
      return;
    }

    // Clear existing plot
    if (container._fullLayout) Plotly.purge(container);

    const colors = getThemeColors();
    const studies = results.studies || AppState.studies || [];

    // Check if we have binary data
    if (!studies.length || studies[0].events_t === undefined) {
      showPlotError(containerId, 'L\\'Abbé plot requires binary outcome data (events and totals)');
      return;
    }

    // Calculate event rates
    const data = studies.filter(s => s.n_t > 0 && s.n_c > 0).map(s => ({
      name: s.name,
      rate_c: s.events_c / s.n_c,  // Control event rate
      rate_t: s.events_t / s.n_t,  // Treatment event rate
      weight: s.n_t + s.n_c,        // Total sample size for bubble size
      n_t: s.n_t,
      n_c: s.n_c,
      events_t: s.events_t,
      events_c: s.events_c
    }));

    if (data.length === 0) {
      showPlotError(containerId, 'No valid studies with binary data for L\\'Abbé plot');
      return;
    }

    const maxWeight = Math.max(...data.map(d => d.weight));
    const sizes = data.map(d => 8 + (d.weight / maxWeight) * 25);

    // Study points (bubble plot)
    const studyTrace = {
      x: data.map(d => d.rate_c),
      y: data.map(d => d.rate_t),
      mode: 'markers+text',
      type: 'scatter',
      marker: {
        size: sizes,
        color: data.map(d => d.rate_t < d.rate_c ? '#22c55e' : d.rate_t > d.rate_c ? '#ef4444' : '#94a3b8'),
        opacity: 0.7,
        line: { color: '#1b263b', width: 1 }
      },
      text: data.map(d => d.name),
      textposition: 'top right',
      textfont: { size: 8, color: colors.text },
      hovertemplate: '%{text}<br>Control rate: %{x:.1%}<br>Treatment rate: %{y:.1%}<br>' +
                     'Events: %{customdata[0]}/%{customdata[1]} vs %{customdata[2]}/%{customdata[3]}<extra></extra>',
      customdata: data.map(d => [d.events_t, d.n_t, d.events_c, d.n_c]),
      name: 'Studies'
    };

    // Line of equality (no effect)
    const equalityLine = {
      x: [0, 1],
      y: [0, 1],
      mode: 'lines',
      type: 'scatter',
      line: { color: '#64748b', width: 2, dash: 'dash' },
      hoverinfo: 'skip',
      name: 'No Effect (RR=1)'
    };

    // RR = 0.5 line (treatment halves risk)
    const rr05Line = {
      x: [0, 1],
      y: [0, 0.5],
      mode: 'lines',
      type: 'scatter',
      line: { color: '#22c55e', width: 1, dash: 'dot' },
      hoverinfo: 'skip',
      name: 'RR = 0.5'
    };

    // RR = 2 line (treatment doubles risk)
    const rr2Line = {
      x: [0, 0.5],
      y: [0, 1],
      mode: 'lines',
      type: 'scatter',
      line: { color: '#ef4444', width: 1, dash: 'dot' },
      hoverinfo: 'skip',
      name: 'RR = 2'
    };

    const layout = {
      title: {
        text: 'L\\'Abbé Plot',
        font: { family: 'Plus Jakarta Sans', size: 14, color: colors.text }
      },
      xaxis: {
        title: 'Control Event Rate',
        range: [0, Math.min(1, Math.max(...data.map(d => d.rate_c)) * 1.2)],
        zeroline: false,
        gridcolor: colors.grid,
        tickformat: '.0%',
        tickfont: { family: 'JetBrains Mono', size: 11, color: colors.text }
      },
      yaxis: {
        title: 'Treatment Event Rate',
        range: [0, Math.min(1, Math.max(...data.map(d => d.rate_t)) * 1.2)],
        zeroline: false,
        gridcolor: colors.grid,
        tickformat: '.0%',
        tickfont: { family: 'JetBrains Mono', size: 11, color: colors.text }
      },
      showlegend: true,
      legend: { x: 0.02, y: 0.98, font: { size: 10, color: colors.text } },
      margin: { l: 70, r: 40, t: 50, b: 50 },
      paper_bgcolor: colors.background,
      plot_bgcolor: colors.background,
      hoverlabel: {
        bgcolor: colors.hoverBg,
        bordercolor: colors.hoverBorder,
        font: { family: 'Plus Jakarta Sans', color: colors.hoverText }
      },
      annotations: [{
        x: 0.85,
        y: 0.15,
        text: 'Treatment<br>better',
        showarrow: false,
        font: { size: 10, color: '#22c55e' }
      }, {
        x: 0.15,
        y: 0.85,
        text: 'Control<br>better',
        showarrow: false,
        font: { size: 10, color: '#ef4444' }
      }]
    };

    Plotly.newPlot(containerId, [equalityLine, rr05Line, rr2Line, studyTrace], layout, {
      displayModeBar: false,
      responsive: true
    });

    console.log('L\\'Abbé plot rendered successfully');

  } catch (e) {
    console.error('L\\'Abbé plot rendering failed:', e);
    showPlotError(containerId, 'Failed to render L\\'Abbé plot: ' + e.message);
  }
}

if (typeof window !== 'undefined') {
  window.renderLabbePlot = renderLabbePlot;
}
'''
        additions.append(("L'Abbé Plot", labbe_plot))
        print("    OK - Added renderLabbePlot function")
    else:
        print("\n[2] L'Abbé plot already exists - skipping")

    # ==========================================================================
    # 3. FUNCTION ALIASES
    # ==========================================================================
    print("\n[3] Adding Function Aliases...")

    aliases_code = '''

// =============================================================================
// FUNCTION ALIASES FOR COMMON NAMING CONVENTIONS
// Maps common function names to their actual implementations
// =============================================================================

// Publication bias test aliases
if (typeof eggersTest === 'function' && typeof eggerTest === 'undefined') {
  var eggerTest = eggersTest;
  if (typeof window !== 'undefined') window.eggerTest = eggersTest;
}

// Begg's rank correlation test (alias to existing if available)
if (typeof beggTest === 'undefined') {
  function beggTest(yi, sei) {
    // Begg and Mazumdar rank correlation test
    // Reference: Begg CB, Mazumdar M. Operating characteristics of a rank correlation
    //            test for publication bias. Biometrics. 1994;50(4):1088-1101.
    try {
      const n = yi.length;
      if (n < 3) return { tau: NaN, p: NaN, note: 'Requires at least 3 studies' };

      // Standardize effect sizes
      const zi = yi.map((y, i) => y / sei[i]);

      // Calculate ranks
      const rankY = getRanks(yi);
      const rankV = getRanks(sei.map(s => s * s));  // Rank variances

      // Kendall's tau
      let concordant = 0, discordant = 0;
      for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
          const diffY = rankY[i] - rankY[j];
          const diffV = rankV[i] - rankV[j];
          if (diffY * diffV > 0) concordant++;
          else if (diffY * diffV < 0) discordant++;
        }
      }

      const tau = (concordant - discordant) / (n * (n - 1) / 2);

      // Approximate p-value using normal approximation
      const se_tau = Math.sqrt(2 * (2 * n + 5) / (9 * n * (n - 1)));
      const z = tau / se_tau;
      const p = 2 * (1 - pnorm(Math.abs(z)));

      return {
        tau: tau,
        z: z,
        p: p,
        n: n,
        interpretation: p < 0.05 ? 'Significant asymmetry detected (p < 0.05)' : 'No significant asymmetry',
        method: 'Begg-Mazumdar rank correlation'
      };
    } catch (e) {
      return { tau: NaN, p: NaN, error: e.message };
    }
  }

  // Helper function for ranks
  function getRanks(arr) {
    const sorted = arr.map((v, i) => ({ v, i })).sort((a, b) => a.v - b.v);
    const ranks = new Array(arr.length);
    for (let i = 0; i < sorted.length; i++) {
      ranks[sorted[i].i] = i + 1;
    }
    return ranks;
  }

  if (typeof window !== 'undefined') window.beggTest = beggTest;
}

// Rosenthal's failsafe N
if (typeof failsafeN === 'undefined') {
  function failsafeN(yi, vi, alpha = 0.05) {
    // Rosenthal's failsafe N (file drawer analysis)
    // Reference: Rosenthal R. The file drawer problem and tolerance for null results.
    //            Psychol Bull. 1979;86(3):638-641.
    try {
      const n = yi.length;
      const sei = vi.map(v => Math.sqrt(v));
      const zi = yi.map((y, i) => y / sei[i]);
      const sumZ = zi.reduce((a, b) => a + b, 0);
      const meanZ = sumZ / n;

      // Critical z for alpha
      const zCrit = qnorm(1 - alpha / 2);

      // Rosenthal's formula: N_fs = (sum(z)/z_crit)^2 - k
      const fsn = Math.max(0, Math.pow(sumZ / zCrit, 2) - n);

      // Orwin's failsafe N (how many null studies to reduce effect to trivial)
      const pooledZ = sumZ / Math.sqrt(n);
      const trivialZ = 0.1;  // Z corresponding to trivial effect
      const orwinN = n * (Math.abs(meanZ) - trivialZ) / trivialZ;

      return {
        rosenthal: Math.round(fsn),
        orwin: Math.max(0, Math.round(orwinN)),
        sumZ: sumZ,
        meanZ: meanZ,
        k: n,
        interpretation: fsn > 5 * n + 10 ?
          'Robust: Would need ' + Math.round(fsn) + ' null studies to nullify' :
          'Potentially fragile: Only ' + Math.round(fsn) + ' null studies needed',
        method: 'Rosenthal failsafe N'
      };
    } catch (e) {
      return { rosenthal: NaN, orwin: NaN, error: e.message };
    }
  }

  if (typeof window !== 'undefined') window.failsafeN = failsafeN;
}

// Leave-one-out alias
if (typeof influenceDiagnostics === 'function' && typeof leave1out === 'undefined') {
  function leave1out(yi, vi, names) {
    // Wrapper that returns leave-one-out format
    const diag = influenceDiagnostics(yi, vi, names);
    return {
      results: diag.leave_one_out || diag.studies,
      influential: diag.influential_studies || [],
      method: 'leave-one-out'
    };
  }
  if (typeof window !== 'undefined') window.leave1out = leave1out;
}

// Export aliases
if (typeof exportAnalysisJSON === 'function' && typeof exportJSON === 'undefined') {
  var exportJSON = exportAnalysisJSON;
  if (typeof window !== 'undefined') window.exportJSON = exportAnalysisJSON;
}

// Fragility analysis alias
if (typeof fragilityIndex === 'function' && typeof fragilityAnalysis === 'undefined') {
  var fragilityAnalysis = fragilityIndex;
  if (typeof window !== 'undefined') window.fragilityAnalysis = fragilityIndex;
}

// Multiverse alias
if (typeof multiverseMetaAnalysis === 'undefined' && typeof runMultiverseAnalysis === 'function') {
  var multiverseMetaAnalysis = runMultiverseAnalysis;
  if (typeof window !== 'undefined') window.multiverseMetaAnalysis = runMultiverseAnalysis;
}

// DOI Plot (Doi plot for publication bias)
if (typeof renderDOIPlot === 'undefined') {
  function renderDOIPlot(results, containerId = 'doiPlot') {
    try {
      if (typeof Plotly === 'undefined') return;

      const container = document.getElementById(containerId);
      if (!container) return;

      if (container._fullLayout) Plotly.purge(container);

      const colors = getThemeColors();
      const yi = results.yi || results.studies.map(s => s.yi);
      const vi = results.vi || results.studies.map(s => s.vi);
      const sei = vi.map(v => Math.sqrt(v));
      const names = results.studyNames || results.studies.map(s => s.name);
      const pooled = results.pooled?.theta || results.theta;

      // DOI plot: Normal quantile vs standardized effect
      const n = yi.length;
      const zi = yi.map((y, i) => (y - pooled) / sei[i]);
      const sorted = zi.map((z, i) => ({ z, i, name: names[i] })).sort((a, b) => a.z - b.z);

      // Expected quantiles
      const expectedQ = sorted.map((_, i) => qnorm((i + 0.5) / n));

      const trace = {
        x: expectedQ,
        y: sorted.map(s => s.z),
        mode: 'markers+text',
        type: 'scatter',
        marker: { size: 10, color: '#4a7ab8' },
        text: sorted.map(s => s.name),
        textposition: 'right',
        textfont: { size: 8, color: colors.text },
        hovertemplate: '%{text}<br>Expected: %{x:.2f}<br>Observed: %{y:.2f}<extra></extra>'
      };

      // Reference line (perfect symmetry)
      const refLine = {
        x: [-3, 3],
        y: [-3, 3],
        mode: 'lines',
        line: { color: '#ef4444', width: 2, dash: 'dash' },
        hoverinfo: 'skip'
      };

      const layout = {
        title: { text: 'DOI Plot (Publication Bias)', font: { size: 14, color: colors.text } },
        xaxis: { title: 'Expected Normal Quantile', gridcolor: colors.grid },
        yaxis: { title: 'Observed Z-score', gridcolor: colors.grid },
        showlegend: false,
        margin: { l: 60, r: 40, t: 50, b: 50 },
        paper_bgcolor: colors.background,
        plot_bgcolor: colors.background
      };

      Plotly.newPlot(containerId, [refLine, trace], layout, { displayModeBar: false, responsive: true });

    } catch (e) {
      console.error('DOI plot failed:', e);
    }
  }

  if (typeof window !== 'undefined') window.renderDOIPlot = renderDOIPlot;
}

// Cumulative forest plot alias
if (typeof renderCumulativePlot === 'function' && typeof renderCumulativeForest === 'undefined') {
  var renderCumulativeForest = renderCumulativePlot;
  if (typeof window !== 'undefined') window.renderCumulativeForest = renderCumulativePlot;
}

// CSV export function
if (typeof exportCSV === 'undefined') {
  function exportCSV() {
    try {
      const studies = AppState.studies || [];
      if (studies.length === 0) {
        showToast('No data to export', 'warning');
        return;
      }

      const dataType = AppState.settings?.dataType || 'binary';
      let headers, rows;

      if (dataType === 'binary') {
        headers = ['study', 'events_t', 'n_t', 'events_c', 'n_c', 'subgroup'];
        rows = studies.map(s => [s.name, s.events_t, s.n_t, s.events_c, s.n_c, s.subgroup || ''].join(','));
      } else if (dataType === 'continuous') {
        headers = ['study', 'mean_t', 'sd_t', 'n_t', 'mean_c', 'sd_c', 'n_c', 'subgroup'];
        rows = studies.map(s => [s.name, s.mean_t, s.sd_t, s.n_t, s.mean_c, s.sd_c, s.n_c, s.subgroup || ''].join(','));
      } else if (dataType === 'hr') {
        headers = ['study', 'hr', 'ci_lower', 'ci_upper', 'subgroup'];
        rows = studies.map(s => [s.name, s.hr, s.ci_lower, s.ci_upper, s.subgroup || ''].join(','));
      } else {
        headers = ['study', 'yi', 'vi', 'subgroup'];
        rows = studies.map(s => [s.name, s.yi, s.vi, s.subgroup || ''].join(','));
      }

      const csv = [headers.join(','), ...rows].join('\\n');
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'meta_analysis_data.csv';
      a.click();
      URL.revokeObjectURL(url);
      showToast('CSV exported successfully', 'success');
    } catch (e) {
      showToast('Export failed: ' + e.message, 'error');
    }
  }

  if (typeof window !== 'undefined') window.exportCSV = exportCSV;
}

// Excel export wrapper
if (typeof exportToExcel === 'undefined' && typeof XLSX !== 'undefined') {
  function exportToExcel() {
    try {
      const studies = AppState.studies || [];
      if (studies.length === 0) {
        showToast('No data to export', 'warning');
        return;
      }

      const ws = XLSX.utils.json_to_sheet(studies);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Studies');

      if (AppState.results) {
        const summary = [{
          pooled: AppState.results.pooled?.theta,
          se: AppState.results.pooled?.se,
          ci_lower: AppState.results.pooled?.ci_lower,
          ci_upper: AppState.results.pooled?.ci_upper,
          tau2: AppState.results.tau2,
          I2: AppState.results.heterogeneity?.I2,
          Q: AppState.results.heterogeneity?.Q
        }];
        const ws2 = XLSX.utils.json_to_sheet(summary);
        XLSX.utils.book_append_sheet(wb, ws2, 'Summary');
      }

      XLSX.writeFile(wb, 'meta_analysis.xlsx');
      showToast('Excel file exported', 'success');
    } catch (e) {
      showToast('Excel export failed: ' + e.message, 'error');
    }
  }

  if (typeof window !== 'undefined') window.exportToExcel = exportToExcel;
}

console.log('Function aliases loaded successfully');
'''

    if 'FUNCTION ALIASES FOR COMMON NAMING' not in content:
        additions.append(('Function Aliases', aliases_code))
        print("    OK - Added function aliases")
    else:
        print("    Function aliases already exist - skipping")

    # ==========================================================================
    # APPLY ALL ADDITIONS
    # ==========================================================================
    if additions:
        for name, code in additions:
            content += code

        with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
            f.write(content)

        print("\n" + "=" * 70)
        print(f"SUCCESS: Added {len(additions)} components")
        for name, _ in additions:
            print(f"  - {name}")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("All components already exist - no changes made")
        print("=" * 70)

if __name__ == '__main__':
    main()
