#!/usr/bin/env python3
"""Add metafor-equivalent features to app.js"""

import shutil
from datetime import datetime

# Copy beautified to app.js
shutil.copy('C:/Truthcert1/app_beautified.js', 'C:/Truthcert1/app.js')
print('Copied beautified JS to app.js')

# Read app.js
with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Base file size: {len(content):,} chars')

# Metafor-equivalent features module
metafor_module = '''

// ================================================================
// METAFOR-EQUIVALENT FEATURES MODULE
// Additional statistical functions matching metafor R package
// Added: ''' + datetime.now().strftime('%Y-%m-%d %H:%M') + '''
// ================================================================
(function() {
    'use strict';

    // Reference window-exported functions with fallbacks
    var pnorm = window.pnorm || function(x) {
        var t = 1/(1+0.2316419*Math.abs(x));
        var d = 0.3989423*Math.exp(-x*x/2);
        var p = d*t*(0.3193815+t*(-0.3565638+t*(1.781478+t*(-1.821256+t*1.330274))));
        return x > 0 ? 1-p : p;
    };

    var qnorm = window.qnorm || function(p) {
        if (p <= 0) return -Infinity;
        if (p >= 1) return Infinity;
        var a = [0, -3.969683028665376e1, 2.209460984245205e2, -2.759285104469687e2,
                 1.383577518672690e2, -3.066479806614716e1, 2.506628277459239e0];
        var b = [0, -5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2,
                 6.680131188771972e1, -1.328068155288572e1];
        var c = [0, -7.784894002430293e-3, -3.223964580411365e-1, -2.400758277161838,
                 -2.549732539343734, 4.374664141464968, 2.938163982698783];
        var d = [0, 7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996,
                 3.754408661907416];
        var pLow = 0.02425, pHigh = 1 - pLow;
        var q, r;
        if (p < pLow) {
            q = Math.sqrt(-2*Math.log(p));
            return (((((c[1]*q+c[2])*q+c[3])*q+c[4])*q+c[5])*q+c[6]) /
                   ((((d[1]*q+d[2])*q+d[3])*q+d[4])*q+1);
        } else if (p <= pHigh) {
            q = p - 0.5;
            r = q*q;
            return (((((a[1]*r+a[2])*r+a[3])*r+a[4])*r+a[5])*r+a[6])*q /
                   (((((b[1]*r+b[2])*r+b[3])*r+b[4])*r+b[5])*r+1);
        } else {
            q = Math.sqrt(-2*Math.log(1-p));
            return -(((((c[1]*q+c[2])*q+c[3])*q+c[4])*q+c[5])*q+c[6]) /
                    ((((d[1]*q+d[2])*q+d[3])*q+d[4])*q+1);
        }
    };

    var pt = window.pt || function(t, df) {
        var x = df / (df + t*t);
        return t < 0 ? 0.5 * betainc(x, df/2, 0.5) : 1 - 0.5 * betainc(x, df/2, 0.5);
    };

    // Incomplete beta function
    function betainc(x, a, b) {
        if (x === 0) return 0;
        if (x === 1) return 1;
        var bt = Math.exp(a*Math.log(x) + b*Math.log(1-x) - lbeta(a,b));
        if (x < (a+1)/(a+b+2)) {
            return bt * betacf(x, a, b) / a;
        } else {
            return 1 - bt * betacf(1-x, b, a) / b;
        }
    }

    function lbeta(a, b) {
        return lgamma(a) + lgamma(b) - lgamma(a+b);
    }

    function lgamma(x) {
        var cof = [76.18009172947146, -86.50532032941677, 24.01409824083091,
                   -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
        var y = x, tmp = x + 5.5;
        tmp -= (x + 0.5) * Math.log(tmp);
        var ser = 1.000000000190015;
        for (var j = 0; j < 6; j++) ser += cof[j] / ++y;
        return -tmp + Math.log(2.5066282746310005 * ser / x);
    }

    function betacf(x, a, b) {
        var qab = a + b, qap = a + 1, qam = a - 1;
        var c = 1, d = 1 - qab * x / qap;
        if (Math.abs(d) < 1e-30) d = 1e-30;
        d = 1 / d;
        var h = d;
        for (var m = 1; m <= 100; m++) {
            var m2 = 2 * m;
            var aa = m * (b - m) * x / ((qam + m2) * (a + m2));
            d = 1 + aa * d;
            if (Math.abs(d) < 1e-30) d = 1e-30;
            c = 1 + aa / c;
            if (Math.abs(c) < 1e-30) c = 1e-30;
            d = 1 / d;
            h *= d * c;
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
            d = 1 + aa * d;
            if (Math.abs(d) < 1e-30) d = 1e-30;
            c = 1 + aa / c;
            if (Math.abs(c) < 1e-30) c = 1e-30;
            d = 1 / d;
            var del = d * c;
            h *= del;
            if (Math.abs(del - 1) < 3e-7) break;
        }
        return h;
    }

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
                   interpretation: p_pet < 0.10 ? "Significant small-study effects" : "No significant effects" },
            peese: { estimate: b0_peese, slope: b1_peese },
            correctedEstimate: usePeese ? b0_peese : b0_pet,
            method: usePeese ? "PEESE" : "PET"
        };
    }

    // Rosenthal fail-safe N
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
            interpretation: n > 5*k + 10 ? "Robust (" + n + " null studies needed)" : "May not be robust"
        };
    }

    // Orwin fail-safe N
    function orwinFailsafeN(yi, targetES, assumedES) {
        assumedES = assumedES || 0;
        var k = yi.length;
        var meanES = yi.reduce(function(a,b) { return a+b; }, 0) / k;
        if (Math.abs(targetES) >= Math.abs(meanES)) {
            return { n: 0, interpretation: "Target exceeds observed effect" };
        }
        var n = Math.max(0, Math.ceil(k * (meanES - targetES) / (targetES - assumedES)));
        return { n: n, k: k, meanES: meanES, targetES: targetES };
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

            results.push({ study: i + 1, leverage: hi, cooksD: cooksD,
                          influence: cooksD > 4/k ? "High" : "Normal" });
        }
        return results;
    }

    // Model fit statistics
    function modelFitStats(yi, vi, tau2, model) {
        model = model || "random";
        var k = yi.length;
        var wi = vi.map(function(v) { return 1 / (v + (model === "random" ? tau2 : 0)); });
        var sumW = wi.reduce(function(a,b) { return a+b; }, 0);
        var pooled = yi.reduce(function(s, y, i) { return s + wi[i] * y; }, 0) / sumW;

        var logLik = 0;
        for (var i = 0; i < k; i++) {
            var sigma2 = vi[i] + (model === "random" ? tau2 : 0);
            var resid = yi[i] - pooled;
            logLik -= 0.5 * (Math.log(2 * Math.PI * sigma2) + resid * resid / sigma2);
        }

        var nParams = model === "random" ? 2 : 1;
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
        return { power: power, interpretation: power >= 0.8 ? "Adequate" : "Underpowered" };
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
            asymmetry: lfkIndex < 1 ? "None" : lfkIndex < 2 ? "Minor" : "Major"
        };
    }

    // Cumulative meta-analysis
    function cumulativeMetaAnalysis(studies, orderBy, tau2Method) {
        orderBy = orderBy || "year";
        tau2Method = tau2Method || "DL";
        if (!studies || studies.length === 0) return [];

        var sorted = studies.slice().sort(function(a, b) {
            if (orderBy === "year") return (a.year || 0) - (b.year || 0);
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

            var tau2Fn = window["estimateTau2_" + tau2Method];
            var tau2 = tau2Fn ? tau2Fn(cumYi, cumVi).tau2 : 0;

            var wi = cumVi.map(function(v) { return 1 / (v + tau2); });
            var sumW = wi.reduce(function(a,b) { return a+b; }, 0);
            var pooled = cumYi.reduce(function(s, y, j) { return s + wi[j] * y; }, 0) / sumW;

            results.push({ step: i + 1, pooled: pooled, tau2: tau2, k: cumYi.length });
        }
        return results;
    }

    // Subgroup analysis
    function subgroupAnalysis(studies, subgroupVar, tau2Method) {
        tau2Method = tau2Method || "DL";
        var groups = {};
        studies.forEach(function(s) {
            var g = s[subgroupVar] || "Unknown";
            if (!groups[g]) groups[g] = [];
            groups[g].push(s);
        });

        var results = {};
        var Q_within = 0;
        var tau2Fn = window["estimateTau2_" + tau2Method] || window.estimateTau2_DL;

        for (var name in groups) {
            var gs = groups[name];
            if (gs.length < 2) continue;

            var gyi = gs.map(function(s) { return s.yi; });
            var gvi = gs.map(function(s) { return s.vi; });

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

    // Export all functions to window
    window.petPeese = petPeese;
    window.failsafeN = failsafeN;
    window.orwinFailsafeN = orwinFailsafeN;
    window.influenceDiagnostics = influenceDiagnostics;
    window.modelFitStats = modelFitStats;
    window.metaPower = metaPower;
    window.doiPlotStats = doiPlotStats;
    window.cumulativeMetaAnalysis = cumulativeMetaAnalysis;
    window.subgroupAnalysis = subgroupAnalysis;

    console.log("[PairwisePro] Metafor-equivalent features loaded: petPeese, failsafeN, orwinFailsafeN, influenceDiagnostics, modelFitStats, metaPower, doiPlotStats, cumulativeMetaAnalysis, subgroupAnalysis");
})();
'''

# Append to content
new_content = content + metafor_module

with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Final file size: {len(new_content):,} chars')
print('Added metafor-equivalent features module')
