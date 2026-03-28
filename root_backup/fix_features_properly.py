#!/usr/bin/env python3
"""Fix features: add stat exports and properly scoped metafor features"""

import re

def main():
    print("=" * 70)
    print("FIXING METAFOR FEATURES - PROPER SCOPING")
    print("=" * 70)

    with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, remove the broken code I added earlier (outside IIFE)
    # Find and remove from "// ================================================================" after line 36128
    # to the end of my additions
    pattern = r'\}\n\n\n    // ================================================================\n    // METAFOR-EQUIVALENT FEATURES.*?console\.log\(\'\[PairwisePro\] Metafor-equivalent features loaded.*?\'\);'
    content = re.sub(pattern, '}', content, flags=re.DOTALL)
    print("Step 1: Removed broken code from outside IIFE")

    # 2. Find the main exports section and add stat function exports
    # Look for window.renderSimulationEvidence export
    stat_exports = '''
    // Export statistical functions for external use
    window.pnorm = pnorm;
    window.qnorm = qnorm;
    window.pt = pt;
    window.qt = qt;
    window.pchisq = pchisq;
    window.estimateTau2_DL = estimateTau2_DL;
    window.estimateTau2_REML = estimateTau2_REML;
    window.estimateTau2_ML = estimateTau2_ML;
    window.estimateTau2_PM = estimateTau2_PM;
    window.estimateTau2_HS = estimateTau2_HS;
    window.estimateTau2_SJ = estimateTau2_SJ;
    window.estimateTau2_HE = estimateTau2_HE;
    window.estimateTau2_EB = estimateTau2_EB;
'''

    # Find existing export section
    if 'window.pnorm = pnorm;' not in content:
        # Add stat exports before renderSimulationEvidence export
        content = content.replace(
            'window.renderSimulationEvidence = renderSimulationEvidence;',
            stat_exports + '\n    window.renderSimulationEvidence = renderSimulationEvidence;'
        )
        print("Step 2: Added statistical function exports")
    else:
        print("Step 2: Statistical exports already exist")

    # 3. Add the metafor features as a self-invoking function at the end
    # This way they can access window-exported functions
    metafor_features = '''

// ================================================================
// METAFOR-EQUIVALENT FEATURES (Added for publication quality)
// Self-contained module that uses window-exported functions
// ================================================================
(function() {
    'use strict';

    // Use window-exported functions
    const pnorm = window.pnorm;
    const qnorm = window.qnorm;
    const pt = window.pt;
    const pchisq = window.pchisq;
    const estimateTau2_DL = window.estimateTau2_DL;
    const estimateTau2_REML = window.estimateTau2_REML;

    /**
     * PET-PEESE publication bias correction
     * @reference Stanley & Doucouliagos (2014). Research Synthesis Methods, 5, 60-78.
     */
    function petPeese(yi, vi) {
        const k = yi.length;
        const se = vi.map(v => Math.sqrt(v));
        const wi = vi.map(v => 1/v);
        const sumW = wi.reduce((a,b) => a+b, 0);

        const sumWY = yi.reduce((s, y, i) => s + wi[i] * y, 0);
        const sumWX = se.reduce((s, x, i) => s + wi[i] * x, 0);
        const sumWXY = yi.reduce((s, y, i) => s + wi[i] * y * se[i], 0);
        const sumWX2 = se.reduce((s, x, i) => s + wi[i] * x * x, 0);

        const meanY = sumWY / sumW;
        const meanX = sumWX / sumW;

        const b1_pet = (sumWXY - sumW * meanX * meanY) / (sumWX2 - sumW * meanX * meanX);
        const b0_pet = meanY - b1_pet * meanX;

        const residuals = yi.map((y, i) => y - b0_pet - b1_pet * se[i]);
        const ssr = residuals.reduce((s, r, i) => s + wi[i] * r * r, 0);
        const mse = ssr / (k - 2);
        const se_b0_pet = Math.sqrt(mse / sumW);

        const t_pet = b0_pet / se_b0_pet;
        const p_pet = 2 * (1 - pt(Math.abs(t_pet), k - 2));

        const sumWV = vi.reduce((s, v, i) => s + wi[i] * v, 0);
        const sumWYV = yi.reduce((s, y, i) => s + wi[i] * y * vi[i], 0);
        const sumWV2 = vi.reduce((s, v, i) => s + wi[i] * v * v, 0);

        const meanV = sumWV / sumW;
        const b1_peese = (sumWYV - sumW * meanV * meanY) / (sumWV2 - sumW * meanV * meanV);
        const b0_peese = meanY - b1_peese * meanV;

        const usePeese = p_pet < 0.10;

        return {
            pet: { estimate: b0_pet, slope: b1_pet, se: se_b0_pet, t: t_pet, p: p_pet,
                   interpretation: p_pet < 0.10 ? 'Significant small-study effects' : 'No significant small-study effects' },
            peese: { estimate: b0_peese, slope: b1_peese },
            correctedEstimate: usePeese ? b0_peese : b0_pet,
            method: usePeese ? 'PEESE' : 'PET',
            recommendation: usePeese ? 'Use PEESE (bias detected)' : 'Use PET (no significant bias)'
        };
    }

    /**
     * Rosenthal's fail-safe N
     */
    function failsafeN(yi, vi, alpha) {
        alpha = alpha || 0.05;
        const k = yi.length;
        const wi = vi.map(v => 1/v);
        const sumW = wi.reduce((a,b) => a+b, 0);
        const pooled = yi.reduce((s, y, i) => s + wi[i] * y, 0) / sumW;
        const se = Math.sqrt(1 / sumW);
        const z = pooled / se;
        const z_crit = qnorm(1 - alpha/2);
        const n = Math.max(0, Math.floor(k * Math.pow(z / z_crit, 2) - k));

        return {
            n: n, k: k, z: z,
            interpretation: n > 5*k + 10 ?
                'Result is robust (' + n + ' > ' + (5*k + 10) + ' file-drawer studies needed)' :
                'Result may not be robust (only ' + n + ' null studies needed)'
        };
    }

    /**
     * Orwin's fail-safe N
     */
    function orwinFailsafeN(yi, targetES, assumedES) {
        assumedES = assumedES || 0;
        const k = yi.length;
        const meanES = yi.reduce((a,b) => a+b, 0) / k;

        if (Math.abs(targetES) >= Math.abs(meanES)) {
            return { n: 0, interpretation: 'Target already exceeds observed effect' };
        }

        const n = Math.max(0, Math.ceil(k * (meanES - targetES) / (targetES - assumedES)));
        return { n: n, k: k, meanES: meanES, targetES: targetES,
                 interpretation: 'Need ' + n + ' studies with ES=' + assumedES + ' to reduce effect to ' + targetES };
    }

    /**
     * Subgroup analysis with Q-between test
     */
    function subgroupAnalysis(studies, subgroupVar, tau2Method) {
        tau2Method = tau2Method || 'DL';
        const groups = {};
        studies.forEach(function(s) {
            const g = s[subgroupVar] || 'Unknown';
            if (!groups[g]) groups[g] = [];
            groups[g].push(s);
        });

        const results = {};
        let Q_within = 0;

        for (const name in groups) {
            const groupStudies = groups[name];
            if (groupStudies.length < 2) continue;

            const yi = groupStudies.map(function(s) { return s.yi; });
            const vi = groupStudies.map(function(s) { return s.vi; });

            const tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
            const tau2Result = tau2Fn(yi, vi);
            const tau2 = tau2Result.tau2;

            const wi = vi.map(function(v) { return 1 / (v + tau2); });
            const sumW = wi.reduce(function(a,b) { return a+b; }, 0);
            const pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;
            const se = Math.sqrt(1 / sumW);

            results[name] = { k: groupStudies.length, pooled: pooled, se: se,
                              ci: [pooled - 1.96 * se, pooled + 1.96 * se], tau2: tau2, Q: tau2Result.Q || 0 };
            Q_within += tau2Result.Q || 0;
        }

        const allYi = studies.map(function(s) { return s.yi; });
        const allVi = studies.map(function(s) { return s.vi; });
        const tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
        const overallTau2 = tau2Fn(allYi, allVi);

        const Q_total = overallTau2.Q || 0;
        const Q_between = Q_total - Q_within;
        const df_between = Object.keys(results).length - 1;
        const p_between = df_between > 0 ? 1 - pchisq(Q_between, df_between) : 1;

        return { subgroups: results, Qbetween: Q_between, dfBetween: df_between, pBetween: p_between, Qwithin: Q_within,
                 interpretation: p_between < 0.05 ? 'Significant subgroup differences (p=' + p_between.toFixed(4) + ')' :
                                                    'No significant subgroup differences (p=' + p_between.toFixed(4) + ')' };
    }

    /**
     * Influence diagnostics
     */
    function influenceDiagnostics(yi, vi, tau2) {
        const k = yi.length;
        const wi = vi.map(function(v) { return 1 / (v + tau2); });
        const sumW = wi.reduce(function(a,b) { return a+b; }, 0);
        const pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;

        const results = [];
        for (let i = 0; i < k; i++) {
            const wi_loo = wi.filter(function(_, j) { return j !== i; });
            const yi_loo = yi.filter(function(_, j) { return j !== i; });
            const sumW_loo = wi_loo.reduce(function(a,b) { return a+b; }, 0);
            const pooled_loo = yi_loo.reduce(function(s, y, j) { return s + wi_loo[j] * y; }, 0) / sumW_loo;

            const hi = wi[i] / sumW;
            const ri = yi[i] - pooled;
            const si = Math.sqrt(vi[i] + tau2);
            const zi = ri / si;
            const cooksD = (zi * zi * hi) / (1 - hi);
            const dffits = zi * Math.sqrt(hi / (1 - hi));

            results.push({ study: i + 1, leverage: hi, residual: ri, stdResidual: zi, cooksD: cooksD, dffits: dffits,
                           pooledWithout: pooled_loo, influence: cooksD > 4/k ? 'High' : 'Normal' });
        }
        return results;
    }

    /**
     * Model fit statistics
     */
    function modelFitStats(yi, vi, tau2, model) {
        model = model || 'random';
        const k = yi.length;
        const wi = vi.map(function(v) { return 1 / (v + (model === 'random' ? tau2 : 0)); });
        const sumW = wi.reduce(function(a,b) { return a+b; }, 0);
        const pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;

        let logLik = 0;
        for (let i = 0; i < k; i++) {
            const sigma2 = vi[i] + (model === 'random' ? tau2 : 0);
            const resid = yi[i] - pooled;
            logLik -= 0.5 * (Math.log(2 * Math.PI * sigma2) + resid * resid / sigma2);
        }

        const nParams = model === 'random' ? 2 : 1;
        const AIC = -2 * logLik + 2 * nParams;
        const BIC = -2 * logLik + nParams * Math.log(k);
        const AICc = AIC + (2 * nParams * (nParams + 1)) / (k - nParams - 1);

        return { logLik: logLik, AIC: AIC, BIC: BIC, AICc: AICc, nParams: nParams, k: k, model: model };
    }

    /**
     * Power analysis for meta-analysis
     */
    function metaPower(k, avgN, effectSize, tau2, alpha) {
        alpha = alpha || 0.05;
        const avgVi = 4 / avgN + effectSize * effectSize / (2 * avgN);
        const varPooled = (avgVi + tau2) / k;
        const sePooled = Math.sqrt(varPooled);
        const ncp = effectSize / sePooled;
        const zCrit = qnorm(1 - alpha/2);
        const power = 1 - pnorm(zCrit - ncp) + pnorm(-zCrit - ncp);

        return { power: power, k: k, avgN: avgN, effectSize: effectSize, tau2: tau2, sePooled: sePooled,
                 interpretation: power >= 0.8 ? 'Adequate power (' + (power*100).toFixed(1) + '%)' :
                                                'Underpowered (' + (power*100).toFixed(1) + '% < 80%)' };
    }

    /**
     * Doi plot stats and LFK index
     */
    function doiPlotStats(yi, vi) {
        const k = yi.length;
        const wi = vi.map(function(v) { return 1/v; });
        const sumW = wi.reduce(function(a,b) { return a+b; }, 0);
        const pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;

        const se = vi.map(function(v) { return Math.sqrt(v); });
        const z = yi.map(function(y, i) { return (y - pooled) / se[i]; });

        const nLeft = z.filter(function(x) { return x < 0; }).length;
        const nRight = k - nLeft;
        const lfkIndex = Math.abs(nLeft - nRight) / Math.sqrt(k);

        let asymmetry;
        if (lfkIndex < 1) asymmetry = 'No asymmetry';
        else if (lfkIndex < 2) asymmetry = 'Minor asymmetry';
        else asymmetry = 'Major asymmetry';

        return { lfkIndex: lfkIndex, asymmetry: asymmetry, nLeft: nLeft, nRight: nRight, k: k,
                 interpretation: 'LFK=' + lfkIndex.toFixed(2) + ': ' + asymmetry };
    }

    /**
     * Cumulative meta-analysis
     */
    function cumulativeMetaAnalysis(studies, orderBy, tau2Method) {
        orderBy = orderBy || 'year';
        tau2Method = tau2Method || 'DL';
        if (!studies || studies.length === 0) return [];

        const sorted = studies.slice().sort(function(a, b) {
            if (orderBy === 'year') return (a.year || 0) - (b.year || 0);
            if (orderBy === 'precision') return a.vi - b.vi;
            return 0;
        });

        const results = [];
        const cumYi = [];
        const cumVi = [];

        for (let i = 0; i < sorted.length; i++) {
            cumYi.push(sorted[i].yi);
            cumVi.push(sorted[i].vi);

            if (cumYi.length < 2) {
                results.push({ step: i + 1, study: sorted[i].study || ('Study ' + (i+1)),
                               orderValue: orderBy === 'year' ? sorted[i].year : sorted[i].vi,
                               pooled: cumYi[0], se: Math.sqrt(cumVi[0]),
                               ciLower: cumYi[0] - 1.96 * Math.sqrt(cumVi[0]),
                               ciUpper: cumYi[0] + 1.96 * Math.sqrt(cumVi[0]), k: 1 });
                continue;
            }

            const tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
            const tau2 = tau2Fn(cumYi, cumVi).tau2;

            const wi = cumVi.map(function(v) { return 1 / (v + tau2); });
            const sumW = wi.reduce(function(a,b) { return a+b; }, 0);
            const pooled = cumYi.reduce(function(s, y, j) { return s + wi[j] * y; }, 0) / sumW;
            const se = Math.sqrt(1 / sumW);

            results.push({ step: i + 1, study: sorted[i].study || ('Study ' + (i+1)),
                           orderValue: orderBy === 'year' ? sorted[i].year : sorted[i].vi,
                           pooled: pooled, se: se, ciLower: pooled - 1.96 * se, ciUpper: pooled + 1.96 * se,
                           tau2: tau2, k: cumYi.length });
        }
        return results;
    }

    // Export all functions
    window.petPeese = petPeese;
    window.failsafeN = failsafeN;
    window.orwinFailsafeN = orwinFailsafeN;
    window.subgroupAnalysis = subgroupAnalysis;
    window.influenceDiagnostics = influenceDiagnostics;
    window.modelFitStats = modelFitStats;
    window.metaPower = metaPower;
    window.doiPlotStats = doiPlotStats;
    window.cumulativeMetaAnalysis = cumulativeMetaAnalysis;

    console.log('[PairwisePro] Metafor-equivalent features loaded');
})();
'''

    # Append at end of file
    content = content.rstrip() + '\n' + metafor_features

    with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Step 3: Added metafor features as self-contained module")
    print("\n" + "=" * 70)
    print("COMPLETE: All features properly added")
    print("=" * 70)

if __name__ == '__main__':
    main()
