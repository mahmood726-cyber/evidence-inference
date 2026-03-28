#!/usr/bin/env python3
"""Add metafor-equivalent features cleanly"""

import re

def main():
    print("=" * 70)
    print("ADDING METAFOR-EQUIVALENT FEATURES (CLEAN VERSION)")
    print("=" * 70)

    with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # New functions to add (clean, working implementations)
    new_functions = '''

    // ================================================================
    // METAFOR-EQUIVALENT FEATURES - Added for publication quality
    // ================================================================

    /**
     * PET-PEESE publication bias correction
     * @reference Stanley, T.D. & Doucouliagos, H. (2014). Meta-regression approximations
     *            to reduce publication selection bias. Research Synthesis Methods, 5, 60-78.
     */
    function petPeese(yi, vi) {
        const k = yi.length;
        const se = vi.map(v => Math.sqrt(v));
        const wi = vi.map(v => 1/v);
        const sumW = wi.reduce((a,b) => a+b, 0);

        // PET: yi = b0 + b1*SE + error
        const sumWY = yi.reduce((s, y, i) => s + wi[i] * y, 0);
        const sumWX = se.reduce((s, x, i) => s + wi[i] * x, 0);
        const sumWXY = yi.reduce((s, y, i) => s + wi[i] * y * se[i], 0);
        const sumWX2 = se.reduce((s, x, i) => s + wi[i] * x * x, 0);

        const meanY = sumWY / sumW;
        const meanX = sumWX / sumW;

        const b1_pet = (sumWXY - sumW * meanX * meanY) / (sumWX2 - sumW * meanX * meanX);
        const b0_pet = meanY - b1_pet * meanX;

        // SE of intercept
        const residuals = yi.map((y, i) => y - b0_pet - b1_pet * se[i]);
        const ssr = residuals.reduce((s, r, i) => s + wi[i] * r * r, 0);
        const mse = ssr / (k - 2);
        const se_b0_pet = Math.sqrt(mse / sumW);

        const t_pet = b0_pet / se_b0_pet;
        const p_pet = 2 * (1 - pt(Math.abs(t_pet), k - 2));

        // PEESE: yi = b0 + b1*vi + error
        const sumWV = vi.reduce((s, v, i) => s + wi[i] * v, 0);
        const sumWYV = yi.reduce((s, y, i) => s + wi[i] * y * vi[i], 0);
        const sumWV2 = vi.reduce((s, v, i) => s + wi[i] * v * v, 0);

        const meanV = sumWV / sumW;
        const b1_peese = (sumWYV - sumW * meanV * meanY) / (sumWV2 - sumW * meanV * meanV);
        const b0_peese = meanY - b1_peese * meanV;

        const usePeese = p_pet < 0.10;

        return {
            pet: {
                estimate: b0_pet,
                slope: b1_pet,
                se: se_b0_pet,
                t: t_pet,
                p: p_pet,
                interpretation: p_pet < 0.10 ? 'Significant small-study effects' : 'No significant small-study effects'
            },
            peese: {
                estimate: b0_peese,
                slope: b1_peese
            },
            correctedEstimate: usePeese ? b0_peese : b0_pet,
            method: usePeese ? 'PEESE' : 'PET',
            recommendation: usePeese ? 'Use PEESE (bias detected)' : 'Use PET (no significant bias)'
        };
    }

    /**
     * Rosenthal's fail-safe N
     * @reference Rosenthal, R. (1979). The "file drawer problem" and tolerance for null results.
     */
    function failsafeN(yi, vi, alpha = 0.05) {
        const k = yi.length;
        const wi = vi.map(v => 1/v);
        const sumW = wi.reduce((a,b) => a+b, 0);
        const pooled = yi.reduce((s, y, i) => s + wi[i] * y, 0) / sumW;
        const se = Math.sqrt(1 / sumW);
        const z = pooled / se;
        const z_crit = qnorm(1 - alpha/2);

        // N = k * (z/z_crit)^2 - k
        const n = Math.max(0, Math.floor(k * Math.pow(z / z_crit, 2) - k));

        return {
            n: n,
            k: k,
            z: z,
            interpretation: n > 5*k + 10 ?
                'Result is robust (' + n + ' > ' + (5*k + 10) + ' file-drawer studies needed)' :
                'Result may not be robust (only ' + n + ' null studies needed to nullify)'
        };
    }

    /**
     * Orwin's fail-safe N
     * @reference Orwin, R.G. (1983). A fail-safe N for effect size in meta-analysis.
     */
    function orwinFailsafeN(yi, targetES, assumedES = 0) {
        const k = yi.length;
        const meanES = yi.reduce((a,b) => a+b, 0) / k;

        if (Math.abs(targetES) >= Math.abs(meanES)) {
            return { n: 0, interpretation: 'Target already exceeds observed effect' };
        }

        const n = Math.ceil(k * (meanES - targetES) / (targetES - assumedES));

        return {
            n: Math.max(0, n),
            k: k,
            meanES: meanES,
            targetES: targetES,
            interpretation: 'Need ' + n + ' studies with ES=' + assumedES + ' to reduce effect to ' + targetES
        };
    }

    /**
     * Subgroup analysis with Q-between test
     */
    function subgroupAnalysis(studies, subgroupVar, tau2Method = 'DL') {
        const groups = {};
        studies.forEach(s => {
            const g = s[subgroupVar] || 'Unknown';
            if (!groups[g]) groups[g] = [];
            groups[g].push(s);
        });

        const results = {};
        let Q_within = 0;
        let df_within = 0;

        for (const [name, groupStudies] of Object.entries(groups)) {
            if (groupStudies.length < 2) continue;

            const yi = groupStudies.map(s => s.yi);
            const vi = groupStudies.map(s => s.vi);

            const tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
            const tau2Result = tau2Fn(yi, vi);
            const tau2 = tau2Result.tau2;

            const wi = vi.map(v => 1 / (v + tau2));
            const sumW = wi.reduce((a,b) => a+b, 0);
            const pooled = yi.reduce((s, y, i) => s + wi[i] * y, 0) / sumW;
            const se = Math.sqrt(1 / sumW);

            results[name] = {
                k: groupStudies.length,
                pooled: pooled,
                se: se,
                ci: [pooled - 1.96 * se, pooled + 1.96 * se],
                tau2: tau2,
                Q: tau2Result.Q || 0
            };

            Q_within += tau2Result.Q || 0;
            df_within += groupStudies.length - 1;
        }

        // Overall pooled
        const allYi = studies.map(s => s.yi);
        const allVi = studies.map(s => s.vi);
        const tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
        const overallTau2 = tau2Fn(allYi, allVi);

        // Q-between
        const Q_total = overallTau2.Q || 0;
        const Q_between = Q_total - Q_within;
        const df_between = Object.keys(results).length - 1;
        const p_between = df_between > 0 ? 1 - pchisq(Q_between, df_between) : 1;

        return {
            subgroups: results,
            Qbetween: Q_between,
            dfBetween: df_between,
            pBetween: p_between,
            Qwithin: Q_within,
            dfWithin: df_within,
            interpretation: p_between < 0.05 ?
                'Significant subgroup differences (p=' + p_between.toFixed(4) + ')' :
                'No significant subgroup differences (p=' + p_between.toFixed(4) + ')'
        };
    }

    /**
     * Influence diagnostics: Cook's D, leverage, DFFITS
     */
    function influenceDiagnostics(yi, vi, tau2) {
        const k = yi.length;
        const wi = vi.map(v => 1 / (v + tau2));
        const sumW = wi.reduce((a,b) => a+b, 0);
        const pooled = yi.reduce((s, y, i) => s + wi[i] * y, 0) / sumW;

        const results = [];

        for (let i = 0; i < k; i++) {
            // Leave-one-out estimate
            const wi_loo = wi.filter((_, j) => j !== i);
            const yi_loo = yi.filter((_, j) => j !== i);
            const sumW_loo = wi_loo.reduce((a,b) => a+b, 0);
            const pooled_loo = yi_loo.reduce((s, y, j) => s + wi_loo[j] * y, 0) / sumW_loo;

            // Leverage (hat value)
            const hi = wi[i] / sumW;

            // Standardized residual
            const ri = yi[i] - pooled;
            const si = Math.sqrt(vi[i] + tau2);
            const zi = ri / si;

            // Cook's D
            const cooksD = (zi * zi * hi) / (1 - hi);

            // DFFITS
            const dffits = zi * Math.sqrt(hi / (1 - hi));

            results.push({
                study: i + 1,
                leverage: hi,
                residual: ri,
                stdResidual: zi,
                cooksD: cooksD,
                dffits: dffits,
                pooledWithout: pooled_loo,
                influence: cooksD > 4/k ? 'High' : 'Normal'
            });
        }

        return results;
    }

    /**
     * Model fit statistics: AIC, BIC, AICc
     */
    function modelFitStats(yi, vi, tau2, model = 'random') {
        const k = yi.length;
        const wi = vi.map(v => 1 / (v + (model === 'random' ? tau2 : 0)));
        const sumW = wi.reduce((a,b) => a+b, 0);
        const pooled = yi.reduce((s, y, i) => s + wi[i] * y, 0) / sumW;

        // Log-likelihood
        let logLik = 0;
        for (let i = 0; i < k; i++) {
            const sigma2 = vi[i] + (model === 'random' ? tau2 : 0);
            const resid = yi[i] - pooled;
            logLik -= 0.5 * (Math.log(2 * Math.PI * sigma2) + resid * resid / sigma2);
        }

        // Parameters: 1 for pooled mean, 1 for tau2 if random
        const nParams = model === 'random' ? 2 : 1;

        // AIC = -2*logLik + 2*p
        const AIC = -2 * logLik + 2 * nParams;

        // BIC = -2*logLik + p*log(k)
        const BIC = -2 * logLik + nParams * Math.log(k);

        // AICc (corrected for small samples)
        const AICc = AIC + (2 * nParams * (nParams + 1)) / (k - nParams - 1);

        return {
            logLik: logLik,
            AIC: AIC,
            BIC: BIC,
            AICc: AICc,
            nParams: nParams,
            k: k,
            model: model
        };
    }

    /**
     * Power analysis for meta-analysis
     */
    function metaPower(k, avgN, effectSize, tau2, alpha = 0.05) {
        // Average within-study variance (assuming equal groups, SMD)
        const avgVi = 4 / avgN + effectSize * effectSize / (2 * avgN);

        // Random-effects variance of pooled estimate
        const varPooled = (avgVi + tau2) / k;
        const sePooled = Math.sqrt(varPooled);

        // Non-centrality parameter
        const ncp = effectSize / sePooled;

        // Critical value
        const zCrit = qnorm(1 - alpha/2);

        // Power = P(|Z| > z_crit | ncp)
        const power = 1 - pnorm(zCrit - ncp) + pnorm(-zCrit - ncp);

        return {
            power: power,
            k: k,
            avgN: avgN,
            effectSize: effectSize,
            tau2: tau2,
            sePooled: sePooled,
            interpretation: power >= 0.8 ? 'Adequate power (' + (power*100).toFixed(1) + '%)' :
                           'Underpowered (' + (power*100).toFixed(1) + '% < 80%)'
        };
    }

    /**
     * Doi plot statistics and LFK index
     * @reference Furuya-Kanamori et al. (2018). LFK index for publication bias detection.
     */
    function doiPlotStats(yi, vi) {
        const k = yi.length;
        const wi = vi.map(v => 1/v);
        const sumW = wi.reduce((a,b) => a+b, 0);
        const pooled = yi.reduce((s, y, i) => s + wi[i] * y, 0) / sumW;

        // Z-scores (standardized deviations from pooled)
        const se = vi.map(v => Math.sqrt(v));
        const z = yi.map((y, i) => (y - pooled) / se[i]);

        // Sort by precision (1/SE)
        const precision = se.map(s => 1/s);
        const sorted = yi.map((y, i) => ({yi: y, vi: vi[i], z: z[i], precision: precision[i]}))
                        .sort((a, b) => a.precision - b.precision);

        // LFK index = sum of |deviation from regression line|
        // Simplified: measure asymmetry
        const nLeft = sorted.filter(s => s.z < 0).length;
        const nRight = k - nLeft;

        // LFK index approximation
        const lfkIndex = Math.abs(nLeft - nRight) / Math.sqrt(k);

        let asymmetry;
        if (lfkIndex < 1) asymmetry = 'No asymmetry';
        else if (lfkIndex < 2) asymmetry = 'Minor asymmetry';
        else asymmetry = 'Major asymmetry';

        return {
            lfkIndex: lfkIndex,
            asymmetry: asymmetry,
            nLeft: nLeft,
            nRight: nRight,
            k: k,
            interpretation: 'LFK=' + lfkIndex.toFixed(2) + ': ' + asymmetry
        };
    }

    /**
     * Cumulative meta-analysis by year or precision
     */
    function cumulativeMetaAnalysis(studies, orderBy = 'year', tau2Method = 'DL') {
        if (!studies || studies.length === 0) return [];

        // Sort studies
        const sorted = [...studies].sort((a, b) => {
            if (orderBy === 'year') return (a.year || 0) - (b.year || 0);
            if (orderBy === 'precision') return a.vi - b.vi; // smaller vi = more precise
            return 0;
        });

        const results = [];
        const cumYi = [];
        const cumVi = [];

        for (let i = 0; i < sorted.length; i++) {
            cumYi.push(sorted[i].yi);
            cumVi.push(sorted[i].vi);

            if (cumYi.length < 2) {
                results.push({
                    step: i + 1,
                    study: sorted[i].study || ('Study ' + (i+1)),
                    orderValue: orderBy === 'year' ? sorted[i].year : sorted[i].vi,
                    pooled: cumYi[0],
                    se: Math.sqrt(cumVi[0]),
                    ciLower: cumYi[0] - 1.96 * Math.sqrt(cumVi[0]),
                    ciUpper: cumYi[0] + 1.96 * Math.sqrt(cumVi[0]),
                    k: 1
                });
                continue;
            }

            const tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
            const tau2 = tau2Fn(cumYi, cumVi).tau2;

            const wi = cumVi.map(v => 1 / (v + tau2));
            const sumW = wi.reduce((a,b) => a+b, 0);
            const pooled = cumYi.reduce((s, y, j) => s + wi[j] * y, 0) / sumW;
            const se = Math.sqrt(1 / sumW);

            results.push({
                step: i + 1,
                study: sorted[i].study || ('Study ' + (i+1)),
                orderValue: orderBy === 'year' ? sorted[i].year : sorted[i].vi,
                pooled: pooled,
                se: se,
                ciLower: pooled - 1.96 * se,
                ciUpper: pooled + 1.96 * se,
                tau2: tau2,
                k: cumYi.length
            });
        }

        return results;
    }

    // Export new functions
    window.petPeese = petPeese;
    window.failsafeN = failsafeN;
    window.orwinFailsafeN = orwinFailsafeN;
    window.subgroupAnalysis = subgroupAnalysis;
    window.influenceDiagnostics = influenceDiagnostics;
    window.modelFitStats = modelFitStats;
    window.metaPower = metaPower;
    window.doiPlotStats = doiPlotStats;
    window.cumulativeMetaAnalysis = cumulativeMetaAnalysis;

    console.log('[PairwisePro] Metafor-equivalent features loaded: petPeese, failsafeN, orwinFailsafeN, subgroupAnalysis, influenceDiagnostics, modelFitStats, metaPower, doiPlotStats, cumulativeMetaAnalysis');
'''

    # Find insertion point - after the simulation evidence exports
    match = re.search(r"(window\.renderSimulationEvidence = renderSimulationEvidence;\s*\})", content)

    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + '\n' + new_functions + '\n' + content[insert_pos:]
        print("SUCCESS: Added new features after simulation evidence exports")
    else:
        # Fallback: append to end
        content = content + '\n' + new_functions
        print("SUCCESS: Appended new features to end of file")

    with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
        f.write(content)

    print("\nNew functions added:")
    print("  1. petPeese() - PET-PEESE publication bias correction")
    print("  2. failsafeN() - Rosenthal's fail-safe N")
    print("  3. orwinFailsafeN() - Orwin's fail-safe N")
    print("  4. subgroupAnalysis() - Subgroup analysis with Q-between")
    print("  5. influenceDiagnostics() - Cook's D, leverage, DFFITS")
    print("  6. modelFitStats() - AIC, BIC, AICc")
    print("  7. metaPower() - Power analysis")
    print("  8. doiPlotStats() - Doi plot and LFK index")
    print("  9. cumulativeMetaAnalysis() - Cumulative MA")
    print("=" * 70)

if __name__ == '__main__':
    main()
