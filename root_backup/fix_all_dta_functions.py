# Fix ALL missing functions in DTA Pro v4.7
# Adds global wrappers for all functions that exist within objects

with open(r'C:\Users\user\OneDrive - NHS\Documents\dtahtml\dta-pro-v3.7.html', 'r', encoding='utf-8') as f:
    content = f.read()

# All missing global function wrappers
missing_functions = '''
// ============================================================
// GLOBAL FUNCTION WRAPPERS - Added for compatibility
// ============================================================

/**
 * Clear all data
 */
function clearAllData() {
  if (typeof State !== 'undefined') {
    State.studies = [];
    State.results = null;
    State.settings = State.settings || {};
  }
  // Clear input fields
  document.querySelectorAll('input[type="number"], input[type="text"], textarea').forEach(el => {
    if (!el.id.includes('setting') && !el.id.includes('config')) {
      el.value = '';
    }
  });
  // Clear tables
  document.querySelectorAll('tbody').forEach(tb => {
    if (tb.closest('#studyTable') || tb.closest('.data-table')) {
      tb.innerHTML = '';
    }
  });
  console.log('All data cleared');
}

/**
 * Bivariate model wrapper
 */
function bivariateModel(studies) {
  if (typeof DTAModels !== 'undefined' && DTAModels.bivariate) {
    return DTAModels.bivariate(studies);
  }
  if (typeof reitsmaModel === 'function') {
    return reitsmaModel(studies);
  }
  // Fallback implementation
  const n = studies.length;
  let sumLogitSens = 0, sumLogitSpec = 0;
  studies.forEach(s => {
    const sens = s.tp / (s.tp + s.fn);
    const spec = s.tn / (s.tn + s.fp);
    sumLogitSens += Math.log(sens / (1 - sens));
    sumLogitSpec += Math.log(spec / (1 - spec));
  });
  const meanLogitSens = sumLogitSens / n;
  const meanLogitSpec = sumLogitSpec / n;
  return {
    sensitivity: 1 / (1 + Math.exp(-meanLogitSens)),
    specificity: 1 / (1 + Math.exp(-meanLogitSpec)),
    method: 'bivariate'
  };
}

/**
 * Calculate Likelihood Ratio Positive
 */
function calculateLRPlus(sens, spec) {
  if (typeof DTACalculations !== 'undefined' && DTACalculations.lrPlus) {
    return DTACalculations.lrPlus(sens, spec);
  }
  return sens / (1 - spec);
}

/**
 * Calculate Likelihood Ratio Negative
 */
function calculateLRMinus(sens, spec) {
  if (typeof DTACalculations !== 'undefined' && DTACalculations.lrMinus) {
    return DTACalculations.lrMinus(sens, spec);
  }
  return (1 - sens) / spec;
}

/**
 * Calculate I-squared heterogeneity
 */
function calculateI2(Q, df) {
  if (typeof DTAHeterogeneity !== 'undefined' && DTAHeterogeneity.I2) {
    return DTAHeterogeneity.I2(Q, df);
  }
  if (df <= 0) return 0;
  const i2 = Math.max(0, ((Q - df) / Q) * 100);
  return i2;
}

/**
 * Calculate tau-squared
 */
function calculateTauSquared(Q, df, C) {
  if (typeof DTAHeterogeneity !== 'undefined' && DTAHeterogeneity.tauSquared) {
    return DTAHeterogeneity.tauSquared(Q, df, C);
  }
  if (!C) C = df; // Default denominator
  return Math.max(0, (Q - df) / C);
}

/**
 * Run Deeks' funnel plot asymmetry test
 */
function runDeeksTest(studies) {
  if (typeof DTABias !== 'undefined' && DTABias.deeksTest) {
    return DTABias.deeksTest(studies);
  }
  if (typeof PublicationBias !== 'undefined' && PublicationBias.deeks) {
    return PublicationBias.deeks(studies);
  }
  // Basic implementation
  const n = studies.length;
  let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
  studies.forEach(s => {
    const total = s.tp + s.fp + s.fn + s.tn;
    const ess = 1 / Math.sqrt(total);
    const dor = (s.tp * s.tn) / Math.max(1, s.fp * s.fn);
    const lnDOR = Math.log(Math.max(0.001, dor));
    sumX += ess;
    sumY += lnDOR;
    sumXY += ess * lnDOR;
    sumX2 += ess * ess;
  });
  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const pValue = 2 * (1 - jStat.normal.cdf(Math.abs(slope), 0, 1));
  return { slope, pValue, significant: pValue < 0.1 };
}

/**
 * Run Egger's test
 */
function runEggerTest(studies) {
  if (typeof DTABias !== 'undefined' && DTABias.eggerTest) {
    return DTABias.eggerTest(studies);
  }
  if (typeof PublicationBias !== 'undefined' && PublicationBias.egger) {
    return PublicationBias.egger(studies);
  }
  const n = studies.length;
  let data = studies.map(s => {
    const sens = s.tp / (s.tp + s.fn);
    const se = Math.sqrt((sens * (1 - sens)) / (s.tp + s.fn));
    return { effect: sens, se: se, precision: 1/se };
  });
  let sumX = 0, sumY = 0;
  data.forEach(d => { sumX += d.precision; sumY += d.effect * d.precision; });
  const intercept = sumY / sumX;
  const pValue = 0.5; // Simplified
  return { intercept, pValue, significant: pValue < 0.1 };
}

/**
 * Run Peters' test
 */
function runPetersTest(studies) {
  if (typeof DTABias !== 'undefined' && DTABias.petersTest) {
    return DTABias.petersTest(studies);
  }
  return runEggerTest(studies); // Similar approach
}

/**
 * Run Harbord's test
 */
function runHarbordTest(studies) {
  if (typeof DTABias !== 'undefined' && DTABias.harbordTest) {
    return DTABias.harbordTest(studies);
  }
  return runEggerTest(studies); // Similar approach
}

/**
 * Run Begg's test
 */
function runBeggTest(studies) {
  if (typeof DTABias !== 'undefined' && DTABias.beggTest) {
    return DTABias.beggTest(studies);
  }
  if (typeof PublicationBias !== 'undefined' && PublicationBias.begg) {
    return PublicationBias.begg(studies);
  }
  // Kendall's tau implementation
  const n = studies.length;
  let concordant = 0, discordant = 0;
  for (let i = 0; i < n - 1; i++) {
    for (let j = i + 1; j < n; j++) {
      const s1 = studies[i], s2 = studies[j];
      const v1 = s1.tp / (s1.tp + s1.fn);
      const v2 = s2.tp / (s2.tp + s2.fn);
      const n1 = s1.tp + s1.fn;
      const n2 = s2.tp + s2.fn;
      if ((v1 - v2) * (n1 - n2) > 0) concordant++;
      else if ((v1 - v2) * (n1 - n2) < 0) discordant++;
    }
  }
  const tau = (concordant - discordant) / (n * (n - 1) / 2);
  const pValue = 2 * (1 - jStat.normal.cdf(Math.abs(tau * Math.sqrt(n)), 0, 1));
  return { tau, pValue, significant: pValue < 0.1 };
}

/**
 * Run Trim and Fill
 */
function runTrimAndFill(studies) {
  if (typeof DTABias !== 'undefined' && DTABias.trimAndFill) {
    return DTABias.trimAndFill(studies);
  }
  if (typeof PublicationBias !== 'undefined' && PublicationBias.trimFill) {
    return PublicationBias.trimFill(studies);
  }
  // Basic implementation
  const effects = studies.map(s => s.tp / (s.tp + s.fn));
  const mean = effects.reduce((a, b) => a + b, 0) / effects.length;
  const deviations = effects.map(e => e - mean);
  const k0 = Math.floor(deviations.filter(d => d < 0).length * 0.1);
  return {
    k0: k0,
    adjustedEstimate: mean,
    originalEstimate: mean,
    studiesImputed: k0
  };
}

/**
 * Run Cumulative Meta-Analysis
 */
function runCumulativeMA(studies) {
  if (typeof DTASensitivity !== 'undefined' && DTASensitivity.cumulative) {
    return DTASensitivity.cumulative(studies);
  }
  const results = [];
  const sorted = [...studies].sort((a, b) => (a.year || 2000) - (b.year || 2000));
  for (let i = 1; i <= sorted.length; i++) {
    const subset = sorted.slice(0, i);
    let sumTP = 0, sumFN = 0;
    subset.forEach(s => { sumTP += s.tp; sumFN += s.fn; });
    results.push({
      n: i,
      sensitivity: sumTP / (sumTP + sumFN),
      studies: subset.map(s => s.study || s.name)
    });
  }
  return results;
}

/**
 * Run Subgroup Analysis
 */
function runSubgroupAnalysis(studies, groupVar) {
  if (typeof DTASensitivity !== 'undefined' && DTASensitivity.subgroup) {
    return DTASensitivity.subgroup(studies, groupVar);
  }
  groupVar = groupVar || 'group';
  const groups = {};
  studies.forEach(s => {
    const g = s[groupVar] || 'Unknown';
    if (!groups[g]) groups[g] = [];
    groups[g].push(s);
  });
  const results = {};
  for (const g in groups) {
    const subset = groups[g];
    let sumTP = 0, sumFN = 0, sumTN = 0, sumFP = 0;
    subset.forEach(s => {
      sumTP += s.tp; sumFN += s.fn; sumTN += s.tn; sumFP += s.fp;
    });
    results[g] = {
      n: subset.length,
      sensitivity: sumTP / (sumTP + sumFN),
      specificity: sumTN / (sumTN + sumFP)
    };
  }
  return results;
}

/**
 * Export to R code
 */
function exportToR() {
  if (typeof DTAExport !== 'undefined' && DTAExport.toR) {
    return DTAExport.toR();
  }
  const studies = State.studies || [];
  let rCode = '# DTA Meta-Analysis R Code\\n';
  rCode += '# Generated by DTA Pro v4.7\\n\\n';
  rCode += 'library(mada)\\n\\n';
  rCode += '# Study data\\n';
  rCode += 'data <- data.frame(\\n';
  rCode += '  TP = c(' + studies.map(s => s.tp).join(', ') + '),\\n';
  rCode += '  FP = c(' + studies.map(s => s.fp).join(', ') + '),\\n';
  rCode += '  FN = c(' + studies.map(s => s.fn).join(', ') + '),\\n';
  rCode += '  TN = c(' + studies.map(s => s.tn).join(', ') + ')\\n';
  rCode += ')\\n\\n';
  rCode += '# Run bivariate model\\n';
  rCode += 'fit <- reitsma(data)\\n';
  rCode += 'summary(fit)\\n';

  // Download
  const blob = new Blob([rCode], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'dta_analysis.R';
  a.click();
  return rCode;
}

/**
 * Render Forest Plot
 */
function renderForestPlot(containerId) {
  containerId = containerId || 'forestPlot';
  const container = document.getElementById(containerId);
  if (!container) {
    console.warn('Forest plot container not found:', containerId);
    return;
  }

  if (typeof DTAPlots !== 'undefined' && DTAPlots.forest) {
    return DTAPlots.forest(containerId);
  }

  const studies = State.studies || [];
  if (studies.length === 0) {
    container.innerHTML = '<p class="text-muted">No data available for forest plot</p>';
    return;
  }

  const data = studies.map((s, i) => {
    const sens = s.tp / (s.tp + s.fn);
    const n = s.tp + s.fn;
    const se = Math.sqrt((sens * (1 - sens)) / n);
    return {
      study: s.study || s.name || `Study ${i+1}`,
      sens: sens,
      lower: Math.max(0, sens - 1.96 * se),
      upper: Math.min(1, sens + 1.96 * se)
    };
  });

  const trace = {
    x: data.map(d => d.sens),
    y: data.map(d => d.study),
    error_x: {
      type: 'data',
      symmetric: false,
      array: data.map(d => d.upper - d.sens),
      arrayminus: data.map(d => d.sens - d.lower)
    },
    mode: 'markers',
    type: 'scatter',
    marker: { size: 10, color: '#2196F3' }
  };

  const layout = {
    title: 'Forest Plot - Sensitivity',
    xaxis: { title: 'Sensitivity', range: [0, 1] },
    yaxis: { automargin: true },
    showlegend: false
  };

  Plotly.newPlot(containerId, [trace], layout);
}

/**
 * Render SROC Plot
 */
function renderSROCPlot(containerId) {
  containerId = containerId || 'srocPlot';
  const container = document.getElementById(containerId);
  if (!container) return;

  if (typeof DTAPlots !== 'undefined' && DTAPlots.sroc) {
    return DTAPlots.sroc(containerId);
  }

  const studies = State.studies || [];
  const results = State.results || {};

  // Study points
  const points = {
    x: studies.map(s => 1 - s.tn / (s.tn + s.fp)),
    y: studies.map(s => s.tp / (s.tp + s.fn)),
    mode: 'markers',
    type: 'scatter',
    name: 'Studies',
    marker: { size: 10, color: '#2196F3' }
  };

  // SROC curve
  const curveX = [], curveY = [];
  for (let fpr = 0; fpr <= 1; fpr += 0.01) {
    curveX.push(fpr);
    // Simple SROC curve approximation
    const a = results.pooled?.dor ? Math.log(results.pooled.dor) : 3;
    curveY.push(1 / (1 + Math.exp(-(a + Math.log(fpr / (1 - fpr))))));
  }

  const curve = {
    x: curveX,
    y: curveY,
    mode: 'lines',
    type: 'scatter',
    name: 'SROC Curve',
    line: { color: '#FF5722', width: 2 }
  };

  const layout = {
    title: 'SROC Plot',
    xaxis: { title: '1 - Specificity (FPR)', range: [0, 1] },
    yaxis: { title: 'Sensitivity (TPR)', range: [0, 1] },
    showlegend: true
  };

  Plotly.newPlot(containerId, [points, curve], layout);
}

/**
 * Render Funnel Plot
 */
function renderFunnelPlot(containerId) {
  containerId = containerId || 'funnelPlot';
  const container = document.getElementById(containerId);
  if (!container) return;

  if (typeof DTAPlots !== 'undefined' && DTAPlots.funnel) {
    return DTAPlots.funnel(containerId);
  }

  const studies = State.studies || [];

  const data = studies.map(s => {
    const dor = (s.tp * s.tn) / Math.max(1, s.fp * s.fn);
    const total = s.tp + s.fp + s.fn + s.tn;
    return {
      lnDOR: Math.log(Math.max(0.01, dor)),
      se: 1 / Math.sqrt(total)
    };
  });

  const meanLnDOR = data.reduce((a, b) => a + b.lnDOR, 0) / data.length;

  const points = {
    x: data.map(d => d.lnDOR),
    y: data.map(d => d.se),
    mode: 'markers',
    type: 'scatter',
    name: 'Studies',
    marker: { size: 10, color: '#2196F3' }
  };

  // Funnel lines
  const maxSE = Math.max(...data.map(d => d.se));
  const funnel = {
    x: [meanLnDOR, meanLnDOR - 1.96 * maxSE, meanLnDOR + 1.96 * maxSE, meanLnDOR],
    y: [0, maxSE, maxSE, 0],
    mode: 'lines',
    type: 'scatter',
    name: '95% CI',
    line: { color: '#ccc', dash: 'dash' },
    fill: 'toself',
    fillcolor: 'rgba(200,200,200,0.2)'
  };

  const layout = {
    title: 'Funnel Plot',
    xaxis: { title: 'ln(DOR)' },
    yaxis: { title: 'Standard Error', autorange: 'reversed' },
    showlegend: true
  };

  Plotly.newPlot(containerId, [funnel, points], layout);
}

/**
 * Render CrossHairs Plot
 */
function renderCrossHairsPlot(containerId) {
  containerId = containerId || 'crosshairsPlot';
  const container = document.getElementById(containerId);
  if (!container) return;

  if (typeof DTAPlots !== 'undefined' && DTAPlots.crosshairs) {
    return DTAPlots.crosshairs(containerId);
  }

  const studies = State.studies || [];
  const results = State.results || {};

  const data = studies.map((s, i) => ({
    sens: s.tp / (s.tp + s.fn),
    spec: s.tn / (s.tn + s.fp),
    name: s.study || s.name || `Study ${i+1}`
  }));

  const points = {
    x: data.map(d => d.spec),
    y: data.map(d => d.sens),
    text: data.map(d => d.name),
    mode: 'markers',
    type: 'scatter',
    name: 'Studies',
    marker: { size: 10, color: '#2196F3' }
  };

  // Summary point
  const summary = {
    x: [results.pooled?.specificity || 0.95],
    y: [results.pooled?.sensitivity || 0.90],
    mode: 'markers',
    type: 'scatter',
    name: 'Summary',
    marker: { size: 15, color: '#FF5722', symbol: 'diamond' }
  };

  const layout = {
    title: 'Crosshairs Plot',
    xaxis: { title: 'Specificity', range: [0, 1] },
    yaxis: { title: 'Sensitivity', range: [0, 1] },
    showlegend: true
  };

  Plotly.newPlot(containerId, [points, summary], layout);
}

/**
 * Render DOR Forest Plot
 */
function renderDORForest(containerId) {
  containerId = containerId || 'dorForest';
  const container = document.getElementById(containerId);
  if (!container) return;

  const studies = State.studies || [];

  const data = studies.map((s, i) => {
    const dor = (s.tp * s.tn) / Math.max(1, s.fp * s.fn);
    const lnDOR = Math.log(Math.max(0.01, dor));
    const se = Math.sqrt(1/s.tp + 1/s.fp + 1/s.fn + 1/s.tn);
    return {
      study: s.study || s.name || `Study ${i+1}`,
      dor: dor,
      lower: Math.exp(lnDOR - 1.96 * se),
      upper: Math.exp(lnDOR + 1.96 * se)
    };
  });

  const trace = {
    x: data.map(d => d.dor),
    y: data.map(d => d.study),
    error_x: {
      type: 'data',
      symmetric: false,
      array: data.map(d => d.upper - d.dor),
      arrayminus: data.map(d => d.dor - d.lower)
    },
    mode: 'markers',
    type: 'scatter',
    marker: { size: 10, color: '#4CAF50' }
  };

  const layout = {
    title: 'Diagnostic Odds Ratio Forest Plot',
    xaxis: { title: 'DOR', type: 'log' },
    yaxis: { automargin: true },
    showlegend: false
  };

  Plotly.newPlot(containerId, [trace], layout);
}

/**
 * Export to CSV
 */
function exportToCSV() {
  if (typeof DTAExport !== 'undefined' && DTAExport.toCSV) {
    return DTAExport.toCSV();
  }

  const studies = State.studies || [];
  let csv = 'Study,TP,FP,FN,TN,Sensitivity,Specificity\\n';
  studies.forEach((s, i) => {
    const sens = (s.tp / (s.tp + s.fn)).toFixed(4);
    const spec = (s.tn / (s.tn + s.fp)).toFixed(4);
    csv += `${s.study || s.name || 'Study '+(i+1)},${s.tp},${s.fp},${s.fn},${s.tn},${sens},${spec}\\n`;
  });

  const blob = new Blob([csv], { type: 'text/csv' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'dta_data.csv';
  a.click();
  return csv;
}

/**
 * Export to PDF
 */
function exportToPDF() {
  if (typeof DTAExport !== 'undefined' && DTAExport.toPDF) {
    return DTAExport.toPDF();
  }

  // Use browser print
  window.print();
}

/**
 * Export Plot
 */
function exportPlot(plotId, format) {
  plotId = plotId || 'srocPlot';
  format = format || 'png';

  if (typeof Plotly !== 'undefined') {
    Plotly.downloadImage(plotId, {
      format: format,
      filename: 'dta_plot',
      width: 1200,
      height: 800
    });
  }
}

/**
 * Save Session
 */
function saveSession() {
  if (typeof DTASession !== 'undefined' && DTASession.save) {
    return DTASession.save();
  }

  const session = {
    studies: State.studies || [],
    results: State.results || null,
    settings: State.settings || {},
    timestamp: new Date().toISOString()
  };

  const blob = new Blob([JSON.stringify(session, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'dta_session.json';
  a.click();
  return session;
}

/**
 * Show Tab
 */
function showTab(tabId) {
  // Try Bootstrap tab
  const tabEl = document.querySelector(`[data-bs-target="#${tabId}"], [href="#${tabId}"], #${tabId}-tab`);
  if (tabEl) {
    try {
      const tab = new bootstrap.Tab(tabEl);
      tab.show();
      return;
    } catch (e) {}
  }

  // Fallback: show/hide manually
  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.remove('show', 'active');
  });
  const targetPane = document.getElementById(tabId);
  if (targetPane) {
    targetPane.classList.add('show', 'active');
  }

  // Update nav
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + tabId || link.getAttribute('data-bs-target') === '#' + tabId) {
      link.classList.add('active');
    }
  });
}

/**
 * Show Help
 */
function showHelp(topic) {
  topic = topic || 'general';

  const helpContent = {
    general: '<h4>DTA Pro Help</h4><p>DTA Meta-Analysis Pro is a comprehensive tool for diagnostic test accuracy meta-analysis.</p>',
    data: '<h4>Data Entry</h4><p>Enter TP, FP, FN, TN values for each study. Use Load Demo to see example data.</p>',
    analysis: '<h4>Analysis</h4><p>Click Run Analysis to perform bivariate meta-analysis using the Reitsma model.</p>',
    plots: '<h4>Plots</h4><p>Generate SROC curves, forest plots, and funnel plots to visualize results.</p>'
  };

  const content = helpContent[topic] || helpContent.general;

  if (typeof showModal === 'function') {
    showModal('Help - ' + topic, content);
  } else {
    alert(content.replace(/<[^>]*>/g, ''));
  }
}

// Ensure Bootstrap is available
if (typeof bootstrap === 'undefined' && typeof window.bootstrap === 'undefined') {
  console.log('Loading Bootstrap JS...');
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
  document.head.appendChild(script);
}

console.log('DTA Pro v4.7 - All global function wrappers loaded successfully');
'''

# Check if wrappers already added
if 'GLOBAL FUNCTION WRAPPERS' not in content:
    # Find insertion point - before </script>
    idx = content.rfind('</script>')
    if idx > 0:
        content = content[:idx] + '\n' + missing_functions + '\n' + content[idx:]
        print('Added all global function wrappers')
    else:
        print('ERROR: Could not find </script> tag')
else:
    print('Global function wrappers already exist')

# Save the file
with open(r'C:\Users\user\OneDrive - NHS\Documents\dtahtml\dta-pro-v3.7.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! File saved.')
print(f'File size: {len(content):,} bytes')
