"""Add release enhancement features to TruthCert app.js"""

new_code = '''

// ============================================================================
// RELEASE ENHANCEMENTS v1.0 - Bootstrapping, Save/Load, HTA, PSA, VOI
// ============================================================================

// ============================================================================
// 1. BOOTSTRAP CONFIDENCE INTERVALS
// ============================================================================

/**
 * Bootstrap confidence intervals for meta-analysis
 * Implements percentile, BCa, and studentized bootstrap methods
 */
function bootstrapMetaAnalysis(yi, vi, options = {}) {
  const {
    nBoot = 2000,
    ciMethod = 'percentile',
    alpha = 0.05,
    seed = null
  } = options;

  const k = yi.length;
  const rng = seed ? seedRandom(seed) : Math.random;

  // Original estimate
  const original = metaAnalysisDL_boot(yi, vi);
  const theta_orig = original.theta;
  const tau2_orig = original.tau2;

  // Bootstrap samples
  const bootTheta = [];
  const bootTau2 = [];
  const bootSE = [];

  for (let b = 0; b < nBoot; b++) {
    const indices = [];
    for (let i = 0; i < k; i++) {
      indices.push(Math.floor(rng() * k));
    }

    const yi_boot = indices.map(i => yi[i]);
    const vi_boot = indices.map(i => vi[i]);

    try {
      const result = metaAnalysisDL_boot(yi_boot, vi_boot);
      bootTheta.push(result.theta);
      bootTau2.push(result.tau2);
      bootSE.push(result.se);
    } catch (e) {}
  }

  const sortedTheta = [...bootTheta].sort((a, b) => a - b);
  const sortedTau2 = [...bootTau2].sort((a, b) => a - b);

  const lower_idx = Math.floor(alpha / 2 * sortedTheta.length);
  const upper_idx = Math.floor((1 - alpha / 2) * sortedTheta.length);

  let ci_lower, ci_upper, ci_method_used;

  if (ciMethod === 'percentile') {
    ci_lower = sortedTheta[lower_idx];
    ci_upper = sortedTheta[upper_idx];
    ci_method_used = 'Percentile';
  } else if (ciMethod === 'bca') {
    const propBelow = bootTheta.filter(t => t < theta_orig).length / bootTheta.length;
    const z0 = qnorm(propBelow);

    const jackTheta = [];
    for (let i = 0; i < k; i++) {
      const yi_jack = yi.filter((_, j) => j !== i);
      const vi_jack = vi.filter((_, j) => j !== i);
      const jackResult = metaAnalysisDL_boot(yi_jack, vi_jack);
      jackTheta.push(jackResult.theta);
    }
    const jackMean = jackTheta.reduce((a, b) => a + b, 0) / k;
    const num = Math.pow(jackTheta.reduce((s, t) => s + Math.pow(jackMean - t, 3), 0), 1);
    const den = 6 * Math.pow(jackTheta.reduce((s, t) => s + Math.pow(jackMean - t, 2), 0), 1.5);
    const a = num / (den + 1e-10);

    const z_alpha_lower = qnorm(alpha / 2);
    const z_alpha_upper = qnorm(1 - alpha / 2);
    const adj_lower = pnorm(z0 + (z0 + z_alpha_lower) / (1 - a * (z0 + z_alpha_lower)));
    const adj_upper = pnorm(z0 + (z0 + z_alpha_upper) / (1 - a * (z0 + z_alpha_upper)));

    const idx_lower = Math.max(0, Math.floor(adj_lower * sortedTheta.length));
    const idx_upper = Math.min(sortedTheta.length - 1, Math.floor(adj_upper * sortedTheta.length));

    ci_lower = sortedTheta[idx_lower];
    ci_upper = sortedTheta[idx_upper];
    ci_method_used = 'BCa';
  } else {
    const t_stats = bootTheta.map((t, i) => (t - theta_orig) / (bootSE[i] + 1e-10));
    const sorted_t = [...t_stats].sort((a, b) => a - b);
    ci_lower = theta_orig - sorted_t[upper_idx] * original.se;
    ci_upper = theta_orig - sorted_t[lower_idx] * original.se;
    ci_method_used = 'Studentized';
  }

  const bootMean = bootTheta.reduce((a, b) => a + b, 0) / bootTheta.length;
  const bootVar = bootTheta.reduce((s, t) => s + Math.pow(t - bootMean, 2), 0) / (bootTheta.length - 1);
  const bootSE_theta = Math.sqrt(bootVar);

  return {
    method: 'Bootstrap Meta-Analysis',
    nBoot: bootTheta.length,
    ciMethod: ci_method_used,
    theta: theta_orig,
    se: original.se,
    se_bootstrap: bootSE_theta,
    ci_lower,
    ci_upper,
    ci_level: 1 - alpha,
    tau2: tau2_orig,
    tau2_ci: [sortedTau2[lower_idx], sortedTau2[upper_idx]],
    I2: original.I2,
    interpretation: 'Bootstrap ' + ci_method_used + ' ' + ((1-alpha)*100).toFixed(0) + '% CI: [' + ci_lower.toFixed(4) + ', ' + ci_upper.toFixed(4) + ']',
    reference: 'Davison & Hinkley (1997) Bootstrap Methods'
  };
}

function metaAnalysisDL_boot(yi, vi) {
  const k = yi.length;
  const w = vi.map(v => 1 / v);
  const sumW = w.reduce((a, b) => a + b, 0);
  const theta_fe = yi.reduce((s, y, i) => s + w[i] * y, 0) / sumW;
  const Q = yi.reduce((s, y, i) => s + w[i] * Math.pow(y - theta_fe, 2), 0);
  const c = sumW - w.reduce((a, b) => a + b * b, 0) / sumW;
  const tau2 = Math.max(0, (Q - (k - 1)) / c);
  const w_re = vi.map(v => 1 / (v + tau2));
  const sumW_re = w_re.reduce((a, b) => a + b, 0);
  const theta = yi.reduce((s, y, i) => s + w_re[i] * y, 0) / sumW_re;
  const se = Math.sqrt(1 / sumW_re);
  const I2 = k > 1 ? Math.max(0, (Q - (k - 1)) / Q * 100) : 0;
  return { theta, se, tau2, I2, Q, k };
}

// ============================================================================
// 2. SAVE/LOAD PROJECT
// ============================================================================

function saveProject(filename = null) {
  const projectState = {
    version: '1.0',
    timestamp: new Date().toISOString(),
    appVersion: 'TruthCert-PairwisePro-v1.0',
    settings: AppState.settings,
    data: AppState.data,
    studies: AppState.studies,
    results: AppState.results ? {
      pooled: AppState.results.pooled,
      heterogeneity: AppState.results.heterogeneity,
      studies: AppState.results.studies,
      yi: AppState.results.yi,
      vi: AppState.results.vi,
      names: AppState.results.names
    } : null,
    truthcert: AppState.truthcert
  };

  const json = JSON.stringify(projectState, null, 2);
  const blob = new Blob([json], { type: 'application/json' });

  if (filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename.endsWith('.json') ? filename : filename + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Project saved: ' + a.download, 'success');
  }

  try {
    localStorage.setItem('truthcert_autosave', json);
    localStorage.setItem('truthcert_autosave_time', new Date().toISOString());
  } catch (e) {}

  return projectState;
}

function loadProject(jsonOrFile) {
  return new Promise((resolve, reject) => {
    if (typeof jsonOrFile === 'string') {
      try {
        const state = JSON.parse(jsonOrFile);
        applyProjectState(state);
        resolve(state);
      } catch (e) {
        reject(new Error('Invalid JSON: ' + e.message));
      }
    } else if (jsonOrFile instanceof File) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const state = JSON.parse(e.target.result);
          applyProjectState(state);
          resolve(state);
        } catch (err) {
          reject(new Error('Invalid project file: ' + err.message));
        }
      };
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsText(jsonOrFile);
    }
  });
}

function applyProjectState(state) {
  if (state.settings) {
    AppState.settings = { ...AppState.settings, ...state.settings };
    if (state.settings.dataType) {
      document.getElementById('dataTypeSelect').value = state.settings.dataType;
      updateEffectMeasures();
      updateTableHeaders();
    }
  }
  if (state.data && state.data.length > 0) {
    document.getElementById('studyTableBody').innerHTML = '';
    state.data.forEach(study => addStudyRow(study));
  }
  if (state.results) {
    AppState.results = state.results;
    if (typeof renderAnalysisPanel === 'function') {
      safeRender(renderAnalysisPanel, 'panel-analysis', AppState.results);
    }
  }
  showToast('Project loaded successfully', 'success');
}

function checkAutosave() {
  try {
    const autosave = localStorage.getItem('truthcert_autosave');
    const autosaveTime = localStorage.getItem('truthcert_autosave_time');
    if (autosave && autosaveTime) {
      const age = (new Date() - new Date(autosaveTime)) / 1000 / 60;
      if (age < 60 * 24) {
        return { available: true, time: autosaveTime, age: age, data: autosave };
      }
    }
  } catch (e) {}
  return { available: false };
}

function loadAutosave() {
  const autosave = checkAutosave();
  if (autosave.available) {
    loadProject(autosave.data);
    return true;
  }
  return false;
}

// ============================================================================
// 3. UNDO/REDO SYSTEM
// ============================================================================

const UndoManager = {
  history: [],
  currentIndex: -1,
  maxHistory: 50,

  saveState(action = 'unknown') {
    if (this.currentIndex < this.history.length - 1) {
      this.history = this.history.slice(0, this.currentIndex + 1);
    }
    const state = {
      action,
      timestamp: new Date().toISOString(),
      data: JSON.parse(JSON.stringify(AppState.data || [])),
      settings: JSON.parse(JSON.stringify(AppState.settings || {})),
      tableHTML: document.getElementById('studyTableBody') ? document.getElementById('studyTableBody').innerHTML : ''
    };
    this.history.push(state);
    this.currentIndex = this.history.length - 1;
    if (this.history.length > this.maxHistory) {
      this.history.shift();
      this.currentIndex--;
    }
    this.updateButtons();
  },

  undo() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.restoreState(this.history[this.currentIndex]);
      showToast('Undo: ' + (this.history[this.currentIndex + 1] ? this.history[this.currentIndex + 1].action : 'action'), 'info');
    }
    this.updateButtons();
  },

  redo() {
    if (this.currentIndex < this.history.length - 1) {
      this.currentIndex++;
      this.restoreState(this.history[this.currentIndex]);
      showToast('Redo: ' + (this.history[this.currentIndex] ? this.history[this.currentIndex].action : 'action'), 'info');
    }
    this.updateButtons();
  },

  restoreState(state) {
    if (!state) return;
    AppState.data = JSON.parse(JSON.stringify(state.data || []));
    AppState.settings = { ...AppState.settings, ...state.settings };
    if (state.tableHTML && document.getElementById('studyTableBody')) {
      document.getElementById('studyTableBody').innerHTML = state.tableHTML;
    }
  },

  updateButtons() {
    const undoBtn = document.getElementById('undoBtn');
    const redoBtn = document.getElementById('redoBtn');
    if (undoBtn) undoBtn.disabled = this.currentIndex <= 0;
    if (redoBtn) redoBtn.disabled = this.currentIndex >= this.history.length - 1;
  },

  clear() {
    this.history = [];
    this.currentIndex = -1;
    this.updateButtons();
  }
};

// ============================================================================
// 4. COST-EFFECTIVENESS / ICER
// ============================================================================

function calculateICER(costs, effects, options = {}) {
  const { comparator = 0, currency = '\\u00A3', effectUnit = 'QALY', threshold = 20000 } = options;
  const n = costs.length;
  const results = [];
  const comparatorCost = costs[comparator];
  const comparatorEffect = effects[comparator];

  for (let i = 0; i < n; i++) {
    if (i === comparator) continue;
    const deltaCost = costs[i] - comparatorCost;
    const deltaEffect = effects[i] - comparatorEffect;
    const icer = deltaEffect !== 0 ? deltaCost / deltaEffect : Infinity;

    let quadrant, decision;
    if (deltaCost <= 0 && deltaEffect >= 0) {
      quadrant = 'SE (Dominant)';
      decision = 'Adopt - More effective and less costly';
    } else if (deltaCost >= 0 && deltaEffect <= 0) {
      quadrant = 'NW (Dominated)';
      decision = 'Reject - Less effective and more costly';
    } else if (deltaCost > 0 && deltaEffect > 0) {
      quadrant = 'NE';
      decision = icer <= threshold ? 'Adopt - ICER below threshold' : 'Uncertain - ICER above threshold';
    } else {
      quadrant = 'SW';
      decision = 'Trade-off: cost savings vs effectiveness loss';
    }

    results.push({ intervention: i, deltaCost, deltaEffect, icer: isFinite(icer) ? icer : null, quadrant, decision, costEffective: quadrant === 'SE (Dominant)' || (quadrant === 'NE' && icer <= threshold) });
  }

  const nmb = effects.map((e, i) => threshold * e - costs[i]);
  const optimalByNMB = nmb.indexOf(Math.max(...nmb));

  return { method: 'Incremental Cost-Effectiveness Analysis', comparator, threshold, currency, effectUnit, results, nmb, optimalIntervention: optimalByNMB, reference: 'Drummond et al. (2015)' };
}

function calculateCEAC(deltaCosts, deltaEffects, thresholds = null) {
  if (!thresholds) thresholds = Array.from({ length: 101 }, (_, i) => i * 1000);
  const n = deltaCosts.length;
  const ceac = thresholds.map(lambda => {
    const nbPositive = deltaCosts.filter((dc, i) => lambda * deltaEffects[i] - dc > 0).length;
    return nbPositive / n;
  });
  return { method: 'Cost-Effectiveness Acceptability Curve', thresholds, probabilities: ceac };
}

// ============================================================================
// 5. QALY INTEGRATION
// ============================================================================

function effectToQALY(effectSize, options = {}) {
  const { effectType = 'SMD', baselineQoL = 0.7, timeHorizon = 1, mortalityEffect = false, baselineMortality = 0.1, discountRate = 0.035 } = options;
  let qalyGain = 0, lifeYearsGained = 0, qualityGain = 0;

  if (effectType === 'SMD' || effectType === 'MD') {
    qualityGain = effectSize * 0.1;
    qalyGain = qualityGain * timeHorizon;
  } else if (effectType === 'OR' || effectType === 'RR') {
    if (mortalityEffect) {
      const newMortality = baselineMortality * effectSize;
      lifeYearsGained = (baselineMortality - newMortality) * timeHorizon / discountRate;
      qalyGain = lifeYearsGained * baselineQoL;
    } else {
      qualityGain = (1 - effectSize) * (1 - baselineQoL) * 0.5;
      qalyGain = qualityGain * timeHorizon;
    }
  } else if (effectType === 'HR' && mortalityEffect) {
    const medianSurvivalControl = -Math.log(0.5) / baselineMortality;
    const medianSurvivalTreatment = medianSurvivalControl / effectSize;
    lifeYearsGained = medianSurvivalTreatment - medianSurvivalControl;
    qalyGain = lifeYearsGained * baselineQoL;
  }

  const discountedQALY = qalyGain * (1 - Math.exp(-discountRate * timeHorizon)) / discountRate;
  return { method: 'Effect to QALY Conversion', effectSize, effectType, qalyGain, discountedQALY, reference: 'Ara & Brazier (2010)' };
}

// ============================================================================
// 6. PROBABILISTIC SENSITIVITY ANALYSIS
// ============================================================================

function runPSA(parameters, model, options = {}) {
  const { nSim = 1000, seed = null, outputMetrics = ['cost', 'effect', 'icer', 'nmb'] } = options;
  const rng = seed ? seedRandom(seed) : Math.random;
  const results = [];

  for (let i = 0; i < nSim; i++) {
    const sampledParams = {};
    for (const [name, param] of Object.entries(parameters)) {
      sampledParams[name] = sampleFromDistribution(param, rng);
    }
    try {
      const output = model(sampledParams);
      results.push({ iteration: i, parameters: sampledParams, outputs: output });
    } catch (e) {}
  }

  const summary = {};
  for (const metric of outputMetrics) {
    const values = results.map(r => r.outputs[metric]).filter(v => v !== undefined && isFinite(v));
    if (values.length > 0) {
      const sorted = [...values].sort((a, b) => a - b);
      summary[metric] = {
        mean: values.reduce((a, b) => a + b, 0) / values.length,
        median: sorted[Math.floor(sorted.length / 2)],
        ci_lower: sorted[Math.floor(0.025 * sorted.length)],
        ci_upper: sorted[Math.floor(0.975 * sorted.length)]
      };
    }
  }

  return { method: 'Probabilistic Sensitivity Analysis', nSimulations: results.length, summary, rawResults: results, reference: 'Briggs et al. (2006)' };
}

function sampleFromDistribution(param, rng = Math.random) {
  const { distribution, mean, sd, alpha, beta, min, max } = param;
  switch (distribution) {
    case 'normal': return rnorm_psa(mean, sd, rng);
    case 'lognormal':
      const muLog = Math.log(mean) - 0.5 * Math.log(1 + (sd * sd) / (mean * mean));
      const sigmaLog = Math.sqrt(Math.log(1 + (sd * sd) / (mean * mean)));
      return Math.exp(rnorm_psa(muLog, sigmaLog, rng));
    case 'beta': return rbeta_psa(alpha, beta, rng);
    case 'gamma':
      const shape = (mean * mean) / (sd * sd);
      const scale = (sd * sd) / mean;
      return rgamma_psa(shape, scale, rng);
    case 'uniform': return min + rng() * (max - min);
    default: return mean || 0;
  }
}

function rnorm_psa(mean, sd, rng) {
  const u1 = rng(), u2 = rng();
  return mean + sd * Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}

function rgamma_psa(shape, scale, rng) {
  if (shape < 1) return rgamma_psa(shape + 1, scale, rng) * Math.pow(rng(), 1 / shape);
  const d = shape - 1/3, c = 1 / Math.sqrt(9 * d);
  while (true) {
    let x, v;
    do { x = rnorm_psa(0, 1, rng); v = 1 + c * x; } while (v <= 0);
    v = v * v * v;
    const u = rng();
    if (u < 1 - 0.0331 * x * x * x * x) return d * v * scale;
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v * scale;
  }
}

function rbeta_psa(alpha, beta, rng) {
  const x = rgamma_psa(alpha, 1, rng);
  const y = rgamma_psa(beta, 1, rng);
  return x / (x + y);
}

// ============================================================================
// 7. BUDGET IMPACT ANALYSIS
// ============================================================================

function budgetImpactAnalysis(options = {}) {
  const { population = 100000, eligibleProportion = 0.1, currentTreatmentCost = 1000, newTreatmentCost = 2000, marketUptake = [0.1, 0.2, 0.3, 0.4, 0.5], timeHorizon = 5, discountRate = 0.035, currency = '\\u00A3' } = options;

  const eligiblePopulation = population * eligibleProportion;
  const results = [];
  let cumulativeBudgetImpact = 0;

  for (let year = 1; year <= timeHorizon; year++) {
    const uptake = marketUptake[year - 1] || marketUptake[marketUptake.length - 1];
    const patientsOnNew = eligiblePopulation * uptake;
    const costWithNew = patientsOnNew * newTreatmentCost + (eligiblePopulation - patientsOnNew) * currentTreatmentCost;
    const costWithoutNew = eligiblePopulation * currentTreatmentCost;
    const incrementalCost = costWithNew - costWithoutNew;
    const discountFactor = 1 / Math.pow(1 + discountRate, year - 1);
    cumulativeBudgetImpact += incrementalCost * discountFactor;
    results.push({ year, uptake: uptake * 100, patientsOnNew, incrementalCost, cumulativeBudgetImpact });
  }

  return { method: 'Budget Impact Analysis', population, eligiblePopulation, timeHorizon, currency, yearlyResults: results, totalBudgetImpact: results.reduce((s, r) => s + r.incrementalCost, 0), reference: 'Sullivan et al. (2014) ISPOR Guidelines' };
}

// ============================================================================
// 8. VALUE OF INFORMATION (EVPI/EVPPI)
// ============================================================================

function calculateEVPI(psaResults, threshold = 20000) {
  const iterations = psaResults.rawResults;
  if (!iterations || iterations.length === 0) return { error: 'No PSA results' };

  const nmbByIteration = iterations.map(iter => threshold * (iter.outputs.effect || 0) - (iter.outputs.cost || 0));
  const meanNMB = nmbByIteration.reduce((a, b) => a + b, 0) / nmbByIteration.length;
  const perfectInfoNMB = nmbByIteration.map(nmb => Math.max(nmb, 0));
  const expectedPerfectNMB = perfectInfoNMB.reduce((a, b) => a + b, 0) / perfectInfoNMB.length;
  const evpi = expectedPerfectNMB - Math.max(meanNMB, 0);

  return { method: 'Expected Value of Perfect Information', threshold, evpiPerPatient: evpi, researchWorthwhile: evpi > 100, reference: 'Claxton et al. (2002)' };
}

function calculateEVPPI(psaResults, parameterName, threshold = 20000) {
  const iterations = psaResults.rawResults;
  if (!iterations || iterations.length === 0) return { error: 'No PSA results' };

  const paramValues = iterations.map(iter => iter.parameters[parameterName]);
  const nmbValues = iterations.map(iter => threshold * (iter.outputs.effect || 0) - (iter.outputs.cost || 0));
  const n = paramValues.length;
  const meanParam = paramValues.reduce((a, b) => a + b, 0) / n;
  const meanNMB = nmbValues.reduce((a, b) => a + b, 0) / n;

  const covXY = paramValues.reduce((s, x, i) => s + (x - meanParam) * (nmbValues[i] - meanNMB), 0) / n;
  const varX = paramValues.reduce((s, x) => s + Math.pow(x - meanParam, 2), 0) / n;
  const beta = covXY / (varX + 1e-10);
  const predictedNMB = paramValues.map(x => meanNMB + beta * (x - meanParam));
  const residualVar = nmbValues.reduce((s, y, i) => s + Math.pow(y - predictedNMB[i], 2), 0) / n;
  const totalVar = nmbValues.reduce((s, y) => s + Math.pow(y - meanNMB, 2), 0) / n;
  const explainedVar = totalVar - residualVar;
  const evppi = Math.sqrt(Math.max(0, explainedVar) / (2 * Math.PI));

  return { method: 'Expected Value of Partial Perfect Information', parameter: parameterName, evppiPerPatient: evppi, varianceExplained: ((explainedVar / totalVar) * 100).toFixed(1) + '%', researchPriority: evppi > 50 ? 'High' : evppi > 10 ? 'Medium' : 'Low', reference: 'Brennan et al. (2007)' };
}

// ============================================================================
// EXPORT ALL FUNCTIONS
// ============================================================================

if (typeof window !== 'undefined') {
  window.bootstrapMetaAnalysis = bootstrapMetaAnalysis;
  window.metaAnalysisDL_boot = metaAnalysisDL_boot;
  window.saveProject = saveProject;
  window.loadProject = loadProject;
  window.applyProjectState = applyProjectState;
  window.checkAutosave = checkAutosave;
  window.loadAutosave = loadAutosave;
  window.UndoManager = UndoManager;
  window.calculateICER = calculateICER;
  window.calculateCEAC = calculateCEAC;
  window.effectToQALY = effectToQALY;
  window.runPSA = runPSA;
  window.sampleFromDistribution = sampleFromDistribution;
  window.rnorm_psa = rnorm_psa;
  window.rgamma_psa = rgamma_psa;
  window.rbeta_psa = rbeta_psa;
  window.budgetImpactAnalysis = budgetImpactAnalysis;
  window.calculateEVPI = calculateEVPI;
  window.calculateEVPPI = calculateEVPPI;
  console.log('TruthCert Release Enhancements v1.0 loaded - Bootstrap, Save/Load, HTA, PSA, VOI');
}
'''

# Append to app.js
with open(r'C:\Truthcert1\app.js', 'a', encoding='utf-8') as f:
    f.write(new_code)

print("Release enhancement functions added to app.js")
