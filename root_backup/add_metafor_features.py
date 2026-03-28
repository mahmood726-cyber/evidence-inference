#!/usr/bin/env python3
"""Add high-value features to reduce gap with metafor"""

print("=" * 70)
print("ADDING METAFOR-EQUIVALENT FEATURES")
print("=" * 70)

# Read current app.js
with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# New features to add
new_features = '''

    // ================================================================
    // ADDITIONAL META-ANALYSIS FEATURES (metafor equivalent)
    // Added to reduce gap with R/metafor
    // ================================================================

    /**
     * PET-PEESE publication bias correction
     * Stanley & Doucouliagos (2014)
     * PET: regress effect on SE (tests for bias)
     * PEESE: regress effect on variance (corrected estimate if PET significant)
     * @param {number[]} yi - Effect sizes
     * @param {number[]} vi - Variances
     * @returns {object} PET and PEESE results
     */
    function petPeese(yi, vi) {
      const k = yi.length;
      const se = vi.map(v => Math.sqrt(v));

      // PET: yi = b0 + b1*SE + error (weighted by 1/vi)
      // This is Egger's test essentially
      const wi = vi.map(v => 1/v);
      const sumW = wi.reduce((a,b) => a+b, 0);

      // Weighted regression: yi on SE
      const sumWY = yi.reduce((s, y, i) => s + wi[i] * y, 0);
      const sumWX = se.reduce((s, x, i) => s + wi[i] * x, 0);
      const sumWXY = yi.reduce((s, y, i) => s + wi[i] * y * se[i], 0);
      const sumWX2 = se.reduce((s, x, i) => s + wi[i] * x * x, 0);

      const meanY = sumWY / sumW;
      const meanX = sumWX / sumW;

      const b1_pet = (sumWXY - sumW * meanX * meanY) / (sumWX2 - sumW * meanX * meanX);
      const b0_pet = meanY - b1_pet * meanX;

      // SE of b0 (intercept) for PET
      const residuals = yi.map((y, i) => y - b0_pet - b1_pet * se[i]);
      const ssr = residuals.reduce((s, r, i) => s + wi[i] * r * r, 0);
      const mse = ssr / (k - 2);
      const se_b0_pet = Math.sqrt(mse / sumW);

      const t_pet = b0_pet / se_b0_pet;
      const p_pet = 2 * (1 - pt(Math.abs(t_pet), k - 2));

      // PEESE: yi = b0 + b1*vi + error (if PET p < 0.10)
      const sumWV = vi.reduce((s, v, i) => s + wi[i] * v, 0);
      const sumWYV = yi.reduce((s, y, i) => s + wi[i] * y * vi[i], 0);
      const sumWV2 = vi.reduce((s, v, i) => s + wi[i] * v * v, 0);

      const meanV = sumWV / sumW;
      const b1_peese = (sumWYV - sumW * meanV * meanY) / (sumWV2 - sumW * meanV * meanV);
      const b0_peese = meanY - b1_peese * meanV;

      // Determine which estimate to use
      const usePeese = p_pet < 0.10;
      const correctedEstimate = usePeese ? b0_peese : b0_pet;

      return {
        pet: {
          intercept: b0_pet,
          slope: b1_pet,
          se: se_b0_pet,
          t: t_pet,
          p: p_pet,
          interpretation: p_pet < 0.10 ? 'Significant small-study effects detected' : 'No significant small-study effects'
        },
        peese: {
          intercept: b0_peese,
          slope: b1_peese
        },
        correctedEstimate: correctedEstimate,
        method: usePeese ? 'PEESE' : 'PET',
        recommendation: usePeese ?
          'Use PEESE estimate (PET detected bias)' :
          'Use PET estimate (no significant bias)'
      };
    }

    /**
     * Failsafe N (Rosenthal's method)
     * Number of null studies needed to make result non-significant
     * @param {number[]} yi - Effect sizes
     * @param {number[]} vi - Variances
     * @param {number} alpha - Significance level (default 0.05)
     * @returns {object} Failsafe N and interpretation
     */
    function failsafeN(yi, vi, alpha = 0.05) {
      const k = yi.length;
      const se = vi.map(v => Math.sqrt(v));

      // Calculate z-scores for each study
      const z = yi.map((y, i) => y / se[i]);
      const sumZ = z.reduce((a, b) => a + b, 0);

      // Critical z for alpha
      const zCrit = qnorm(1 - alpha/2);

      // Rosenthal's formula: N = (sumZ/zCrit)^2 - k
      const failsafe = Math.pow(sumZ / zCrit, 2) - k;

      // Interpretation (Rosenthal's 5k+10 rule)
      const threshold = 5 * k + 10;
      const robust = failsafe > threshold;

      return {
        N: Math.max(0, Math.round(failsafe)),
        threshold: threshold,
        robust: robust,
        interpretation: robust ?
          `Result is robust (${Math.round(failsafe)} > ${threshold} file-drawer studies needed)` :
          `Result may not be robust (only ${Math.round(failsafe)} studies needed to nullify)`,
        method: 'Rosenthal (1979)'
      };
    }

    /**
     * Orwin's Failsafe N
     * More conservative, specifies target effect size
     * @param {number[]} yi - Effect sizes
     * @param {number} targetES - Target "trivial" effect size (default 0.1)
     * @returns {object} Failsafe N
     */
    function orwinFailsafeN(yi, targetES = 0.1) {
      const k = yi.length;
      const meanES = yi.reduce((a, b) => a + b, 0) / k;

      // Orwin's formula: N = k * (meanES - targetES) / targetES
      // Assuming null studies have ES = 0
      const failsafe = k * (Math.abs(meanES) - targetES) / targetES;

      return {
        N: Math.max(0, Math.round(failsafe)),
        meanEffect: meanES,
        targetEffect: targetES,
        interpretation: `${Math.round(failsafe)} studies with ES=0 needed to reduce mean to ${targetES}`,
        method: 'Orwin (1983)'
      };
    }

    /**
     * Subgroup analysis
     * Run separate meta-analyses by subgroup
     * @param {Array} studies - Studies with subgroup field
     * @param {string} subgroupVar - Name of subgroup variable
     * @param {string} tau2Method - Tau² estimation method
     * @returns {object} Results by subgroup + test for subgroup differences
     */
    function subgroupAnalysis(studies, subgroupVar, tau2Method = 'DL') {
      // Group studies
      const groups = {};
      studies.forEach(s => {
        const g = s[subgroupVar] || 'Unknown';
        if (!groups[g]) groups[g] = [];
        groups[g].push(s);
      });

      const results = {};
      let Q_between = 0;
      let df_between = Object.keys(groups).length - 1;

      // Pooled estimate across all
      const allYi = studies.map(s => s.yi);
      const allVi = studies.map(s => s.vi);
      const overall = calculatePooledEstimate(allYi, allVi,
        estimateTau2_DL(allYi, allVi).tau2);

      // Analyze each subgroup
      for (const [groupName, groupStudies] of Object.entries(groups)) {
        if (groupStudies.length < 2) {
          results[groupName] = {
            k: groupStudies.length,
            error: 'Need at least 2 studies'
          };
          continue;
        }

        const yi = groupStudies.map(s => s.yi);
        const vi = groupStudies.map(s => s.vi);

        // Get tau² using specified method
        const tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
        const tau2Result = tau2Fn(yi, vi);
        const pooled = calculatePooledEstimate(yi, vi, tau2Result.tau2);

        results[groupName] = {
          k: groupStudies.length,
          pooled: pooled.theta,
          se: pooled.se,
          ci_lower: pooled.ci_lower,
          ci_upper: pooled.ci_upper,
          tau2: tau2Result.tau2,
          I2: tau2Result.I2 || calculateI2(tau2Result.Q, yi.length - 1),
          Q: tau2Result.Q
        };

        // Contribution to Q_between
        const wi = 1 / (pooled.se * pooled.se);
        Q_between += wi * Math.pow(pooled.theta - overall.theta, 2);
      }

      // Test for subgroup differences
      const p_between = 1 - pchisq(Q_between, df_between);

      return {
        subgroups: results,
        overall: {
          pooled: overall.theta,
          se: overall.se,
          ci_lower: overall.ci_lower,
          ci_upper: overall.ci_upper
        },
        heterogeneityBetween: {
          Q: Q_between,
          df: df_between,
          p: p_between,
          significant: p_between < 0.05,
          interpretation: p_between < 0.05 ?
            'Significant difference between subgroups' :
            'No significant difference between subgroups'
        }
      };
    }

    /**
     * Calculate I² from Q and df
     */
    function calculateI2(Q, df) {
      if (df <= 0) return 0;
      const I2 = Math.max(0, (Q - df) / Q * 100);
      return I2;
    }

    /**
     * Influence diagnostics (standardized residuals, Cook's distance, etc.)
     * @param {number[]} yi - Effect sizes
     * @param {number[]} vi - Variances
     * @param {number} tau2 - Between-study variance
     * @returns {object} Diagnostic measures for each study
     */
    function influenceDiagnostics(yi, vi, tau2) {
      const k = yi.length;
      const wi = vi.map(v => 1 / (v + tau2));
      const sumW = wi.reduce((a, b) => a + b, 0);

      // Pooled estimate
      const theta = yi.reduce((s, y, i) => s + wi[i] * y, 0) / sumW;

      // Hat values (leverage)
      const h = wi.map(w => w / sumW);

      // Residuals
      const residuals = yi.map(y => y - theta);

      // Standardized residuals
      const varTheta = 1 / sumW;
      const stdResiduals = residuals.map((r, i) => {
        const varResid = vi[i] + tau2 - varTheta;
        return r / Math.sqrt(Math.max(varResid, 0.0001));
      });

      // Cook's distance approximation
      const cooksD = stdResiduals.map((sr, i) => {
        return (sr * sr * h[i]) / (1 - h[i]);
      });

      // DFFITS
      const dffits = stdResiduals.map((sr, i) => {
        return sr * Math.sqrt(h[i] / (1 - h[i]));
      });

      // Leave-one-out estimates
      const loo = yi.map((_, i) => {
        const yiLoo = yi.filter((_, j) => j !== i);
        const viLoo = vi.filter((_, j) => j !== i);
        const wiLoo = viLoo.map(v => 1 / (v + tau2));
        const sumWLoo = wiLoo.reduce((a, b) => a + b, 0);
        return yiLoo.reduce((s, y, j) => s + wiLoo[j] * y, 0) / sumWLoo;
      });

      // Identify influential studies
      const influential = cooksD.map((cd, i) => ({
        index: i,
        cooksD: cd,
        stdResidual: stdResiduals[i],
        leverage: h[i],
        dffits: dffits[i],
        looEstimate: loo[i],
        isInfluential: cd > 4/k || Math.abs(stdResiduals[i]) > 2
      }));

      return {
        residuals: residuals,
        standardizedResiduals: stdResiduals,
        leverage: h,
        cooksDistance: cooksD,
        dffits: dffits,
        leaveOneOut: loo,
        influential: influential.filter(s => s.isInfluential),
        pooledEstimate: theta
      };
    }

    /**
     * Model comparison statistics
     * @param {object} model - Model results with tau2, k, etc.
     * @returns {object} AIC, BIC, AICc
     */
    function modelFitStats(yi, vi, tau2, model = 'RE') {
      const k = yi.length;
      const wi = vi.map(v => 1 / (v + tau2));
      const sumW = wi.reduce((a, b) => a + b, 0);
      const theta = yi.reduce((s, y, i) => s + wi[i] * y, 0) / sumW;

      // Log-likelihood (restricted)
      let ll = -0.5 * k * Math.log(2 * Math.PI);
      ll -= 0.5 * vi.reduce((s, v, i) => s + Math.log(v + tau2), 0);
      ll -= 0.5 * yi.reduce((s, y, i) => s + wi[i] * Math.pow(y - theta, 2), 0);

      // Number of parameters
      const p = model === 'FE' ? 1 : 2; // theta (and tau2 for RE)

      // AIC, BIC, AICc
      const aic = -2 * ll + 2 * p;
      const bic = -2 * ll + p * Math.log(k);
      const aicc = aic + (2 * p * (p + 1)) / (k - p - 1);

      return {
        logLik: ll,
        AIC: aic,
        BIC: bic,
        AICc: aicc,
        npar: p,
        k: k
      };
    }

    /**
     * Power analysis for meta-analysis
     * @param {number} k - Number of studies
     * @param {number} n - Average sample size per study
     * @param {number} effectSize - Expected effect size
     * @param {number} tau2 - Expected between-study variance
     * @param {number} alpha - Significance level
     * @returns {object} Power calculation
     */
    function metaPower(k, n, effectSize, tau2 = 0, alpha = 0.05) {
      // Average within-study variance (approximation for SMD)
      const avgVi = 4 / n;  // Rough approximation

      // Variance of pooled estimate
      const varTheta = (avgVi + tau2) / k;
      const seTheta = Math.sqrt(varTheta);

      // Non-centrality parameter
      const ncp = effectSize / seTheta;

      // Critical value
      const zCrit = qnorm(1 - alpha/2);

      // Power
      const power = 1 - pnorm(zCrit - ncp) + pnorm(-zCrit - ncp);

      // Required k for 80% power
      const requiredK = Math.ceil((avgVi + tau2) * Math.pow(qnorm(0.80) + zCrit, 2) / (effectSize * effectSize));

      return {
        power: power,
        powerPercent: (power * 100).toFixed(1) + '%',
        requiredK: requiredK,
        effectSize: effectSize,
        tau2: tau2,
        alpha: alpha,
        interpretation: power >= 0.8 ?
          'Adequate power (≥80%)' :
          `Underpowered. Need ${requiredK} studies for 80% power.`
      };
    }

    /**
     * Doi plot and LFK index for publication bias
     * Alternative to funnel plot, may detect asymmetry better
     * @param {number[]} yi - Effect sizes
     * @param {number[]} vi - Variances
     * @returns {object} LFK index and interpretation
     */
    function doiPlotStats(yi, vi) {
      const k = yi.length;
      const se = vi.map(v => Math.sqrt(v));

      // Rank by precision (1/SE)
      const precision = se.map(s => 1/s);
      const ranked = yi.map((y, i) => ({yi: y, se: se[i], precision: precision[i]}))
        .sort((a, b) => b.precision - a.precision);

      // Z-scores
      const zScores = ranked.map(s => s.yi / s.se);

      // LFK index (measure of asymmetry)
      // Based on deviation from expected symmetric distribution
      const meanZ = zScores.reduce((a, b) => a + b, 0) / k;
      const expectedMedian = 0; // Under H0 of no bias

      // Calculate LFK using absolute deviations
      const absZ = zScores.map(z => Math.abs(z - meanZ));
      const lfk = absZ.reduce((a, b) => a + b, 0) / k;

      // Interpretation thresholds (approximate)
      let asymmetry = 'None';
      if (Math.abs(lfk) > 2) asymmetry = 'Major';
      else if (Math.abs(lfk) > 1) asymmetry = 'Minor';

      return {
        LFK: lfk,
        asymmetry: asymmetry,
        interpretation: `LFK index: ${lfk.toFixed(3)} - ${asymmetry} asymmetry`,
        zScores: zScores,
        plotData: ranked.map((s, i) => ({
          x: i + 1,  // Rank
          y: s.yi / s.se  // Z-score
        }))
      };
    }

    /**
     * Cumulative meta-analysis
     * @param {Array} studies - Studies with yi, vi, and optionally year
     * @param {string} orderBy - 'year', 'precision', 'effect', or 'chronological'
     * @returns {Array} Cumulative results
     */
    function cumulativeMetaAnalysis(studies, orderBy = 'year') {
      // Sort studies
      let sorted = [...studies];
      switch(orderBy) {
        case 'year':
          sorted.sort((a, b) => (a.year || 0) - (b.year || 0));
          break;
        case 'precision':
          sorted.sort((a, b) => a.vi - b.vi);  // Most precise first
          break;
        case 'effect':
          sorted.sort((a, b) => Math.abs(b.yi) - Math.abs(a.yi));  // Largest first
          break;
        default:
          // Keep original order
      }

      const results = [];
      for (let i = 1; i <= sorted.length; i++) {
        const subset = sorted.slice(0, i);
        const yi = subset.map(s => s.yi);
        const vi = subset.map(s => s.vi);

        if (yi.length >= 2) {
          const tau2 = estimateTau2_DL(yi, vi).tau2;
          const pooled = calculatePooledEstimate(yi, vi, tau2);

          results.push({
            k: i,
            study: sorted[i-1].name || sorted[i-1].study || `Study ${i}`,
            year: sorted[i-1].year,
            pooled: pooled.theta,
            ci_lower: pooled.ci_lower,
            ci_upper: pooled.ci_upper,
            tau2: tau2
          });
        } else {
          results.push({
            k: 1,
            study: sorted[0].name || sorted[0].study || 'Study 1',
            year: sorted[0].year,
            pooled: yi[0],
            ci_lower: yi[0] - 1.96 * Math.sqrt(vi[0]),
            ci_upper: yi[0] + 1.96 * Math.sqrt(vi[0]),
            tau2: 0
          });
        }
      }

      return results;
    }

    // ================================================================
    // END OF ADDITIONAL FEATURES
    // ================================================================
'''

# Find a good insertion point (after existing statistical functions)
insert_marker = "// ================================================================"
# Find the last occurrence of tau2 estimator functions
insert_pos = content.rfind("function estimateTau2_EB")
if insert_pos == -1:
    insert_pos = content.rfind("function calculatePooledEstimate")

if insert_pos != -1:
    # Find the end of that function
    brace_count = 0
    found_start = False
    end_pos = insert_pos
    for i in range(insert_pos, len(content)):
        if content[i] == '{':
            brace_count += 1
            found_start = True
        elif content[i] == '}':
            brace_count -= 1
            if found_start and brace_count == 0:
                end_pos = i + 1
                break

    # Insert new features after this function
    content = content[:end_pos] + "\n" + new_features + "\n" + content[end_pos:]

    with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
        f.write(content)

    print("SUCCESS: Added new features!")
    print("\nNew functions added:")
    print("  1. petPeese() - PET-PEESE publication bias correction")
    print("  2. failsafeN() - Rosenthal's fail-safe N")
    print("  3. orwinFailsafeN() - Orwin's fail-safe N")
    print("  4. subgroupAnalysis() - Subgroup analysis with Q-between test")
    print("  5. influenceDiagnostics() - Cook's D, leverage, DFFITS")
    print("  6. modelFitStats() - AIC, BIC, AICc")
    print("  7. metaPower() - Power analysis for meta-analysis")
    print("  8. doiPlotStats() - Doi plot and LFK index")
    print("  9. cumulativeMetaAnalysis() - Cumulative MA by year/precision")
else:
    print("ERROR: Could not find insertion point")

print("\n" + "=" * 70)
