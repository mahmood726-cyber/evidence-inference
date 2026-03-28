#!/usr/bin/env python3
"""Comprehensive fix: repair syntax errors and add new features"""

def main():
    print("=" * 70)
    print("COMPREHENSIVE FIX - TruthCert-PairwisePro")
    print("=" * 70)

    with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # STEP 1: Fix all literal newlines inside single-quoted strings
    # Pattern: 'LITERAL_NEWLINE' should become '\n'
    print("\n[1] Fixing literal newlines in strings...")

    # Find patterns like .join('\n') where \n is actual newline
    import re

    # Fix .join('NEWLINE') patterns
    # Match: .join(' followed by newline followed by ');
    def fix_join_newlines(text):
        lines = text.split('\n')
        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Check if line ends with join(' (incomplete)
            if line.rstrip().endswith("join('"):
                # Check if next line is ');
                if i + 1 < len(lines) and lines[i+1].strip() == "');":
                    # Fix: merge with \n
                    fixed_line = line.rstrip()[:-1] + "'\\n');"
                    fixed_lines.append(fixed_line)
                    i += 2  # Skip next line
                    print(f"    Fixed join at line {i}")
                    continue
            fixed_lines.append(line)
            i += 1
        return '\n'.join(fixed_lines)

    content = fix_join_newlines(content)

    # STEP 2: Add statistical function exports
    print("\n[2] Adding statistical function exports...")

    stat_exports = '''
    // Export core statistical functions for external use
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

    if 'window.pnorm = pnorm;' not in content:
        # Add before renderSimulationEvidence export
        content = content.replace(
            'window.renderSimulationEvidence = renderSimulationEvidence;',
            stat_exports + '\n  window.renderSimulationEvidence = renderSimulationEvidence;'
        )
        print("    Added stat exports")
    else:
        print("    Stat exports already exist")

    # STEP 3: Add metafor-equivalent features as a separate IIFE at the end
    print("\n[3] Adding metafor-equivalent features...")

    metafor_module = '''

// ================================================================
// METAFOR-EQUIVALENT FEATURES MODULE
// Self-contained module using window-exported functions
// ================================================================
(function() {
    'use strict';

    // Reference window-exported functions
    var pnorm = window.pnorm;
    var qnorm = window.qnorm;
    var pt = window.pt;
    var pchisq = window.pchisq;
    var estimateTau2_DL = window.estimateTau2_DL;

    // PET-PEESE publication bias correction
    function petPeese(yi, vi) {
        var k = yi.length;
        var se = vi.map(function(v) { return Math.sqrt(v); });
        var wi = vi.map(function(v) { return 1/v; });
        var sumW = wi.reduce(function(a,b) { return a+b; }, 0);

        var sumWY = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0);
        var sumWX = se.reduce(function(s, x, i) { return s + wi[i] * x; }, 0);
        var sumWXY = yi.reduce(function(s, y, i) { return s + wi[i] * y * se[i]; }, 0);
        var sumWX2 = se.reduce(function(s, x, i) { return s + wi[i] * x * x; }, 0);

        var meanY = sumWY / sumW;
        var meanX = sumWX / sumW;

        var b1_pet = (sumWXY - sumW * meanX * meanY) / (sumWX2 - sumW * meanX * meanX);
        var b0_pet = meanY - b1_pet * meanX;

        var residuals = yi.map(function(y, i) { return y - b0_pet - b1_pet * se[i]; });
        var ssr = residuals.reduce(function(s, r, i) { return s + wi[i] * r * r; }, 0);
        var mse = ssr / (k - 2);
        var se_b0_pet = Math.sqrt(mse / sumW);

        var t_pet = b0_pet / se_b0_pet;
        var p_pet = 2 * (1 - pt(Math.abs(t_pet), k - 2));

        var sumWV = vi.reduce(function(s, v, i) { return s + wi[i] * v; }, 0);
        var sumWYV = yi.reduce(function(s, y, i) { return s + wi[i] * y * vi[i]; }, 0);
        var sumWV2 = vi.reduce(function(s, v, i) { return s + wi[i] * v * v; }, 0);

        var meanV = sumWV / sumW;
        var b1_peese = (sumWYV - sumW * meanV * meanY) / (sumWV2 - sumW * meanV * meanV);
        var b0_peese = meanY - b1_peese * meanV;

        var usePeese = p_pet < 0.10;

        return {
            pet: { estimate: b0_pet, slope: b1_pet, se: se_b0_pet, t: t_pet, p: p_pet,
                   interpretation: p_pet < 0.10 ? 'Significant small-study effects' : 'No significant effects' },
            peese: { estimate: b0_peese, slope: b1_peese },
            correctedEstimate: usePeese ? b0_peese : b0_pet,
            method: usePeese ? 'PEESE' : 'PET'
        };
    }

    // Rosenthal's fail-safe N
    function failsafeN(yi, vi, alpha) {
        alpha = alpha || 0.05;
        var k = yi.length;
        var wi = vi.map(function(v) { return 1/v; });
        var sumW = wi.reduce(function(a,b) { return a+b; }, 0);
        var pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;
        var se = Math.sqrt(1 / sumW);
        var z = pooled / se;
        var z_crit = qnorm(1 - alpha/2);
        var n = Math.max(0, Math.floor(k * Math.pow(z / z_crit, 2) - k));

        return {
            n: n, k: k, z: z,
            interpretation: n > 5*k + 10 ? 'Robust (' + n + ' null studies needed)' : 'May not be robust'
        };
    }

    // Orwin's fail-safe N
    function orwinFailsafeN(yi, targetES, assumedES) {
        assumedES = assumedES || 0;
        var k = yi.length;
        var meanES = yi.reduce(function(a,b) { return a+b; }, 0) / k;
        if (Math.abs(targetES) >= Math.abs(meanES)) {
            return { n: 0, interpretation: 'Target exceeds observed effect' };
        }
        var n = Math.max(0, Math.ceil(k * (meanES - targetES) / (targetES - assumedES)));
        return { n: n, k: k, meanES: meanES, targetES: targetES };
    }

    // Subgroup analysis
    function subgroupAnalysis(studies, subgroupVar, tau2Method) {
        tau2Method = tau2Method || 'DL';
        var groups = {};
        studies.forEach(function(s) {
            var g = s[subgroupVar] || 'Unknown';
            if (!groups[g]) groups[g] = [];
            groups[g].push(s);
        });

        var results = {};
        var Q_within = 0;

        for (var name in groups) {
            var gs = groups[name];
            if (gs.length < 2) continue;

            var gyi = gs.map(function(s) { return s.yi; });
            var gvi = gs.map(function(s) { return s.vi; });

            var tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
            var tau2Result = tau2Fn(gyi, gvi);
            var tau2 = tau2Result.tau2;

            var gwi = gvi.map(function(v) { return 1 / (v + tau2); });
            var gsumW = gwi.reduce(function(a,b) { return a+b; }, 0);
            var gpooled = gyi.reduce(function(s, y, i) { return s + gwi[i] * y; }, 0) / gsumW;
            var gse = Math.sqrt(1 / gsumW);

            results[name] = { k: gs.length, pooled: gpooled, se: gse, tau2: tau2 };
            Q_within += tau2Result.Q || 0;
        }

        return { subgroups: results, Qwithin: Q_within };
    }

    // Influence diagnostics
    function influenceDiagnostics(yi, vi, tau2) {
        var k = yi.length;
        var wi = vi.map(function(v) { return 1 / (v + tau2); });
        var sumW = wi.reduce(function(a,b) { return a+b; }, 0);
        var pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;

        var results = [];
        for (var i = 0; i < k; i++) {
            var hi = wi[i] / sumW;
            var ri = yi[i] - pooled;
            var si = Math.sqrt(vi[i] + tau2);
            var zi = ri / si;
            var cooksD = (zi * zi * hi) / (1 - hi);

            results.push({ study: i + 1, leverage: hi, cooksD: cooksD, influence: cooksD > 4/k ? 'High' : 'Normal' });
        }
        return results;
    }

    // Model fit statistics
    function modelFitStats(yi, vi, tau2, model) {
        model = model || 'random';
        var k = yi.length;
        var wi = vi.map(function(v) { return 1 / (v + (model === 'random' ? tau2 : 0)); });
        var sumW = wi.reduce(function(a,b) { return a+b; }, 0);
        var pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;

        var logLik = 0;
        for (var i = 0; i < k; i++) {
            var sigma2 = vi[i] + (model === 'random' ? tau2 : 0);
            var resid = yi[i] - pooled;
            logLik -= 0.5 * (Math.log(2 * Math.PI * sigma2) + resid * resid / sigma2);
        }

        var nParams = model === 'random' ? 2 : 1;
        return {
            logLik: logLik,
            AIC: -2 * logLik + 2 * nParams,
            BIC: -2 * logLik + nParams * Math.log(k),
            AICc: -2 * logLik + 2 * nParams + (2 * nParams * (nParams + 1)) / (k - nParams - 1)
        };
    }

    // Meta power analysis
    function metaPower(k, avgN, effectSize, tau2, alpha) {
        alpha = alpha || 0.05;
        var avgVi = 4 / avgN + effectSize * effectSize / (2 * avgN);
        var varPooled = (avgVi + tau2) / k;
        var sePooled = Math.sqrt(varPooled);
        var ncp = effectSize / sePooled;
        var zCrit = qnorm(1 - alpha/2);
        var power = 1 - pnorm(zCrit - ncp) + pnorm(-zCrit - ncp);
        return { power: power, interpretation: power >= 0.8 ? 'Adequate' : 'Underpowered' };
    }

    // Doi plot stats and LFK index
    function doiPlotStats(yi, vi) {
        var k = yi.length;
        var wi = vi.map(function(v) { return 1/v; });
        var sumW = wi.reduce(function(a,b) { return a+b; }, 0);
        var pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;

        var se = vi.map(function(v) { return Math.sqrt(v); });
        var z = yi.map(function(y, i) { return (y - pooled) / se[i]; });

        var nLeft = z.filter(function(x) { return x < 0; }).length;
        var lfkIndex = Math.abs(nLeft - (k - nLeft)) / Math.sqrt(k);

        return {
            lfkIndex: lfkIndex,
            asymmetry: lfkIndex < 1 ? 'None' : lfkIndex < 2 ? 'Minor' : 'Major'
        };
    }

    // Cumulative meta-analysis
    function cumulativeMetaAnalysis(studies, orderBy, tau2Method) {
        orderBy = orderBy || 'year';
        tau2Method = tau2Method || 'DL';
        if (!studies || studies.length === 0) return [];

        var sorted = studies.slice().sort(function(a, b) {
            if (orderBy === 'year') return (a.year || 0) - (b.year || 0);
            return a.vi - b.vi;
        });

        var results = [];
        var cumYi = [], cumVi = [];

        for (var i = 0; i < sorted.length; i++) {
            cumYi.push(sorted[i].yi);
            cumVi.push(sorted[i].vi);

            if (cumYi.length < 2) {
                results.push({ step: i + 1, pooled: cumYi[0], k: 1 });
                continue;
            }

            var tau2Fn = window['estimateTau2_' + tau2Method] || estimateTau2_DL;
            var tau2 = tau2Fn(cumYi, cumVi).tau2;

            var wi = cumVi.map(function(v) { return 1 / (v + tau2); });
            var sumW = wi.reduce(function(a,b) { return a+b; }, 0);
            var pooled = cumYi.reduce(function(s, y, j) { return s + wi[j] * y; }, 0) / sumW;

            results.push({ step: i + 1, pooled: pooled, tau2: tau2, k: cumYi.length });
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

    # Append to file
    content = content.rstrip() + '\n' + metafor_module

    # Save
    with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
        f.write(content)

    print("    Added metafor module")
    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    main()
