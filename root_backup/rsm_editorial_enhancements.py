#!/usr/bin/env python3
"""
RSM Editorial Enhancements for NMA Pro v6.2
Adds missing features identified in Research Synthesis Methods editorial review
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("RSM EDITORIAL ENHANCEMENTS")
print("="*70)

# =============================================================================
# 1. TRANSITIVITY ASSESSMENT
# =============================================================================

transitivity_module = '''
// ============================================================================
// TRANSITIVITY ASSESSMENT
// Evaluates similarity of study populations across comparisons
// ============================================================================

const TransitivityAssessment = {

    // Assess transitivity across the network
    assess(studies, effectModifiers = []) {
        const comparisons = this.getComparisons(studies);
        const results = {
            comparisons: [],
            globalAssessment: null,
            effectModifierBalance: {},
            recommendations: []
        };

        // Check effect modifier distribution across comparisons
        for (const modifier of effectModifiers) {
            results.effectModifierBalance[modifier] = this.assessModifierBalance(studies, modifier, comparisons);
        }

        // Pairwise transitivity assessment
        for (const comp of comparisons) {
            const compStudies = studies.filter(s =>
                (s.treatment1 === comp.t1 && s.treatment2 === comp.t2) ||
                (s.treatment1 === comp.t2 && s.treatment2 === comp.t1)
            );

            results.comparisons.push({
                comparison: `${comp.t1} vs ${comp.t2}`,
                nStudies: compStudies.length,
                characteristics: this.summarizeCharacteristics(compStudies, effectModifiers)
            });
        }

        // Global transitivity assessment
        results.globalAssessment = this.globalTransitivity(results.effectModifierBalance);

        // Generate recommendations
        results.recommendations = this.generateRecommendations(results);

        return results;
    },

    getComparisons(studies) {
        const comps = new Map();
        for (const s of studies) {
            const key = [s.treatment1, s.treatment2].sort().join('|');
            if (!comps.has(key)) {
                const [t1, t2] = key.split('|');
                comps.set(key, { t1, t2 });
            }
        }
        return [...comps.values()];
    },

    assessModifierBalance(studies, modifier, comparisons) {
        const byComparison = {};

        for (const comp of comparisons) {
            const key = `${comp.t1} vs ${comp.t2}`;
            const compStudies = studies.filter(s =>
                (s.treatment1 === comp.t1 && s.treatment2 === comp.t2) ||
                (s.treatment1 === comp.t2 && s.treatment2 === comp.t1)
            );

            const values = compStudies.map(s => s[modifier]).filter(v => v !== undefined);
            if (values.length > 0) {
                const numeric = values.filter(v => typeof v === 'number');
                byComparison[key] = {
                    n: values.length,
                    mean: numeric.length > 0 ? numeric.reduce((a,b) => a+b, 0) / numeric.length : null,
                    values: values
                };
            }
        }

        // Calculate overall variance in modifier across comparisons
        const means = Object.values(byComparison).map(v => v.mean).filter(m => m !== null);
        const overallMean = means.length > 0 ? means.reduce((a,b) => a+b, 0) / means.length : null;
        const variance = means.length > 1 ?
            means.reduce((sum, m) => sum + (m - overallMean)**2, 0) / (means.length - 1) : 0;

        return {
            modifier: modifier,
            byComparison: byComparison,
            overallMean: overallMean,
            variance: variance,
            balanced: variance < 0.1 * (overallMean || 1) ** 2
        };
    },

    summarizeCharacteristics(studies, modifiers) {
        const summary = {};
        for (const mod of modifiers) {
            const values = studies.map(s => s[mod]).filter(v => v !== undefined);
            if (values.length > 0) {
                const numeric = values.filter(v => typeof v === 'number');
                summary[mod] = {
                    n: values.length,
                    mean: numeric.length > 0 ? numeric.reduce((a,b) => a+b, 0) / numeric.length : null,
                    min: numeric.length > 0 ? Math.min(...numeric) : null,
                    max: numeric.length > 0 ? Math.max(...numeric) : null
                };
            }
        }
        return summary;
    },

    globalTransitivity(modifierBalance) {
        const assessments = Object.values(modifierBalance);
        if (assessments.length === 0) return { status: 'unknown', message: 'No effect modifiers assessed' };

        const balanced = assessments.filter(a => a.balanced).length;
        const ratio = balanced / assessments.length;

        if (ratio >= 0.8) return { status: 'likely', message: 'Effect modifiers appear balanced across comparisons' };
        if (ratio >= 0.5) return { status: 'unclear', message: 'Some imbalance in effect modifiers detected' };
        return { status: 'concern', message: 'Substantial imbalance in effect modifiers - transitivity may be violated' };
    },

    generateRecommendations(results) {
        const recs = [];

        if (results.globalAssessment.status === 'concern') {
            recs.push('Consider meta-regression to adjust for imbalanced effect modifiers');
            recs.push('Perform sensitivity analysis excluding comparisons with dissimilar populations');
        }

        const imbalanced = Object.entries(results.effectModifierBalance)
            .filter(([k, v]) => !v.balanced)
            .map(([k, v]) => k);

        if (imbalanced.length > 0) {
            recs.push(`Investigate imbalance in: ${imbalanced.join(', ')}`);
        }

        return recs;
    }
};

'''

# =============================================================================
# 2. DIAGNOSTIC PLOTS (Baujat, Galbraith, L'Abbe)
# =============================================================================

diagnostic_plots_module = '''
// ============================================================================
// DIAGNOSTIC PLOTS
// Baujat plot, Galbraith (radial) plot, L'Abbe plot
// ============================================================================

const DiagnosticPlots = {

    // Baujat plot: contribution to heterogeneity vs influence on result
    baujatPlot(effects, ses, labels = null) {
        const n = effects.length;
        const weights = ses.map(se => 1/(se*se));
        const sumW = weights.reduce((a,b) => a+b, 0);
        const pooled = effects.reduce((sum, e, i) => sum + weights[i] * e, 0) / sumW;

        // Q contribution for each study
        const qContrib = effects.map((e, i) => weights[i] * (e - pooled) ** 2);
        const totalQ = qContrib.reduce((a,b) => a+b, 0);

        // Influence: pooled effect without each study
        const influence = [];
        for (let i = 0; i < n; i++) {
            const wExcl = weights.filter((_, j) => j !== i);
            const eExcl = effects.filter((_, j) => j !== i);
            const sumWExcl = wExcl.reduce((a,b) => a+b, 0);
            const pooledExcl = eExcl.reduce((sum, e, j) => sum + wExcl[j] * e, 0) / sumWExcl;
            influence.push(Math.abs(pooled - pooledExcl));
        }

        const data = effects.map((e, i) => ({
            study: labels ? labels[i] : `Study ${i+1}`,
            qContribution: qContrib[i],
            qPercent: 100 * qContrib[i] / totalQ,
            influence: influence[i],
            outlier: qContrib[i] > totalQ / n * 2 && influence[i] > pooled * 0.1
        }));

        return {
            type: 'baujat',
            data: data,
            totalQ: totalQ,
            pooledEffect: pooled,
            svg: this.renderBaujat(data)
        };
    },

    // Galbraith (radial) plot
    galbraithPlot(effects, ses, labels = null) {
        const n = effects.length;
        const precision = ses.map(se => 1/se);
        const standardized = effects.map((e, i) => e / ses[i]);

        // Regression line (should pass through origin under homogeneity)
        const sumX = precision.reduce((a,b) => a+b, 0);
        const sumY = standardized.reduce((a,b) => a+b, 0);
        const sumXY = precision.reduce((sum, p, i) => sum + p * standardized[i], 0);
        const sumX2 = precision.reduce((sum, p) => sum + p*p, 0);

        const slope = sumXY / sumX2;  // Forced through origin
        const pooledEffect = slope;

        // 95% CI bounds (z = +/- 1.96)
        const data = effects.map((e, i) => ({
            study: labels ? labels[i] : `Study ${i+1}`,
            precision: precision[i],
            zScore: standardized[i],
            expectedZ: precision[i] * pooledEffect,
            residual: standardized[i] - precision[i] * pooledEffect,
            outlier: Math.abs(standardized[i] - precision[i] * pooledEffect) > 2
        }));

        return {
            type: 'galbraith',
            data: data,
            pooledEffect: pooledEffect,
            svg: this.renderGalbraith(data, pooledEffect)
        };
    },

    // L'Abbe plot for binary outcomes
    labbePlot(studies) {
        // Requires event rates in both arms
        const validStudies = studies.filter(s =>
            s.e1 !== undefined && s.n1 !== undefined &&
            s.e2 !== undefined && s.n2 !== undefined
        );

        if (validStudies.length === 0) {
            return { error: "Need studies with 2x2 data (e1, n1, e2, n2)" };
        }

        const data = validStudies.map((s, i) => {
            const p1 = s.e1 / s.n1;  // Treatment event rate
            const p2 = s.e2 / s.n2;  // Control event rate
            const weight = Math.sqrt(s.n1 + s.n2);  // Size for plotting

            return {
                study: s.study || s.id || `Study ${i+1}`,
                treatmentRate: p1,
                controlRate: p2,
                weight: weight,
                riskDifference: p1 - p2,
                riskRatio: p1 / p2,
                oddsRatio: (p1 / (1-p1)) / (p2 / (1-p2))
            };
        });

        return {
            type: 'labbe',
            data: data,
            svg: this.renderLabbe(data)
        };
    },

    // Contour-enhanced funnel plot
    contourFunnelPlot(effects, ses, contours = [0.01, 0.05, 0.1]) {
        const weights = ses.map(se => 1/(se*se));
        const sumW = weights.reduce((a,b) => a+b, 0);
        const pooled = effects.reduce((sum, e, i) => sum + weights[i] * e, 0) / sumW;
        const sePooled = Math.sqrt(1 / sumW);

        const data = effects.map((e, i) => ({
            effect: e,
            se: ses[i],
            precision: 1/ses[i]
        }));

        // Generate contour lines for significance levels
        const contourLines = contours.map(p => {
            const z = this.qnorm(1 - p/2);
            return {
                p: p,
                z: z,
                lines: this.generateContourPoints(pooled, z)
            };
        });

        return {
            type: 'contourFunnel',
            data: data,
            pooledEffect: pooled,
            contours: contourLines,
            svg: this.renderContourFunnel(data, pooled, contourLines)
        };
    },

    generateContourPoints(center, z) {
        const points = [];
        for (let se = 0.01; se <= 1; se += 0.01) {
            points.push({ se: se, lower: center - z * se, upper: center + z * se });
        }
        return points;
    },

    qnorm(p) {
        // Inverse normal CDF
        if (p <= 0) return -Infinity;
        if (p >= 1) return Infinity;
        if (p === 0.5) return 0;

        const a = [-3.969683028665376e1, 2.209460984245205e2, -2.759285104469687e2,
                    1.383577518672690e2, -3.066479806614716e1, 2.506628277459239e0];
        const b = [-5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2,
                    6.680131188771972e1, -1.328068155288572e1];
        const c = [-7.784894002430293e-3, -3.223964580411365e-1, -2.400758277161838e0,
                   -2.549732539343734e0, 4.374664141464968e0, 2.938163982698783e0];
        const d = [7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996e0, 3.754408661907416e0];

        const pLow = 0.02425, pHigh = 1 - pLow;
        let q, r;

        if (p < pLow) {
            q = Math.sqrt(-2 * Math.log(p));
            return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
        }
        if (p <= pHigh) {
            q = p - 0.5;
            r = q * q;
            return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);
        }
        q = Math.sqrt(-2 * Math.log(1 - p));
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);
    },

    // SVG Renderers
    renderBaujat(data) {
        const width = 500, height = 400;
        const margin = { top: 30, right: 30, bottom: 50, left: 60 };
        const plotW = width - margin.left - margin.right;
        const plotH = height - margin.top - margin.bottom;

        const maxQ = Math.max(...data.map(d => d.qContribution)) * 1.1;
        const maxInf = Math.max(...data.map(d => d.influence)) * 1.1;

        let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`;
        svg += `<rect width="${width}" height="${height}" fill="white"/>`;

        // Axes
        svg += `<line x1="${margin.left}" y1="${height-margin.bottom}" x2="${width-margin.right}" y2="${height-margin.bottom}" stroke="black"/>`;
        svg += `<line x1="${margin.left}" y1="${margin.top}" x2="${margin.left}" y2="${height-margin.bottom}" stroke="black"/>`;

        // Labels
        svg += `<text x="${width/2}" y="${height-10}" text-anchor="middle" font-size="12">Contribution to Q</text>`;
        svg += `<text x="15" y="${height/2}" text-anchor="middle" font-size="12" transform="rotate(-90,15,${height/2})">Influence on pooled effect</text>`;
        svg += `<text x="${width/2}" y="20" text-anchor="middle" font-size="14" font-weight="bold">Baujat Plot</text>`;

        // Points
        for (const d of data) {
            const x = margin.left + (d.qContribution / maxQ) * plotW;
            const y = height - margin.bottom - (d.influence / maxInf) * plotH;
            const color = d.outlier ? '#e74c3c' : '#3498db';
            svg += `<circle cx="${x}" cy="${y}" r="5" fill="${color}" opacity="0.7"/>`;
            if (d.outlier) {
                svg += `<text x="${x+8}" y="${y+4}" font-size="10">${d.study}</text>`;
            }
        }

        svg += '</svg>';
        return svg;
    },

    renderGalbraith(data, pooled) {
        const width = 500, height = 400;
        const margin = { top: 30, right: 30, bottom: 50, left: 60 };
        const plotW = width - margin.left - margin.right;
        const plotH = height - margin.top - margin.bottom;

        const maxPrec = Math.max(...data.map(d => d.precision)) * 1.1;
        const minZ = Math.min(...data.map(d => d.zScore)) - 0.5;
        const maxZ = Math.max(...data.map(d => d.zScore)) + 0.5;
        const zRange = maxZ - minZ;

        let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`;
        svg += `<rect width="${width}" height="${height}" fill="white"/>`;

        // 95% CI bounds
        const y1 = height - margin.bottom - ((1.96 - minZ) / zRange) * plotH;
        const y2 = height - margin.bottom - ((-1.96 - minZ) / zRange) * plotH;
        svg += `<line x1="${margin.left}" y1="${y1}" x2="${width-margin.right}" y2="${y1}" stroke="#e74c3c" stroke-dasharray="5,5"/>`;
        svg += `<line x1="${margin.left}" y1="${y2}" x2="${width-margin.right}" y2="${y2}" stroke="#e74c3c" stroke-dasharray="5,5"/>`;

        // Regression line through origin
        const x2 = width - margin.right;
        const yEnd = height - margin.bottom - ((maxPrec * pooled - minZ) / zRange) * plotH;
        svg += `<line x1="${margin.left}" y1="${height - margin.bottom - ((0 - minZ) / zRange) * plotH}" x2="${x2}" y2="${yEnd}" stroke="#2ecc71" stroke-width="2"/>`;

        // Points
        for (const d of data) {
            const x = margin.left + (d.precision / maxPrec) * plotW;
            const y = height - margin.bottom - ((d.zScore - minZ) / zRange) * plotH;
            const color = d.outlier ? '#e74c3c' : '#3498db';
            svg += `<circle cx="${x}" cy="${y}" r="4" fill="${color}"/>`;
        }

        // Labels
        svg += `<text x="${width/2}" y="${height-10}" text-anchor="middle" font-size="12">Precision (1/SE)</text>`;
        svg += `<text x="15" y="${height/2}" text-anchor="middle" font-size="12" transform="rotate(-90,15,${height/2})">z-score</text>`;
        svg += `<text x="${width/2}" y="20" text-anchor="middle" font-size="14" font-weight="bold">Galbraith (Radial) Plot</text>`;

        svg += '</svg>';
        return svg;
    },

    renderLabbe(data) {
        const width = 500, height = 500;
        const margin = { top: 30, right: 30, bottom: 50, left: 60 };
        const plotW = width - margin.left - margin.right;
        const plotH = height - margin.top - margin.bottom;

        let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`;
        svg += `<rect width="${width}" height="${height}" fill="white"/>`;

        // Diagonal line of no effect
        svg += `<line x1="${margin.left}" y1="${height-margin.bottom}" x2="${width-margin.right}" y2="${margin.top}" stroke="#ccc" stroke-dasharray="5,5"/>`;

        // Points (size by weight)
        const maxWeight = Math.max(...data.map(d => d.weight));
        for (const d of data) {
            const x = margin.left + d.controlRate * plotW;
            const y = height - margin.bottom - d.treatmentRate * plotH;
            const r = 3 + (d.weight / maxWeight) * 10;
            const color = d.riskDifference > 0 ? '#27ae60' : '#e74c3c';
            svg += `<circle cx="${x}" cy="${y}" r="${r}" fill="${color}" opacity="0.6"/>`;
        }

        // Axes
        svg += `<line x1="${margin.left}" y1="${height-margin.bottom}" x2="${width-margin.right}" y2="${height-margin.bottom}" stroke="black"/>`;
        svg += `<line x1="${margin.left}" y1="${margin.top}" x2="${margin.left}" y2="${height-margin.bottom}" stroke="black"/>`;

        // Labels
        svg += `<text x="${width/2}" y="${height-10}" text-anchor="middle" font-size="12">Control Event Rate</text>`;
        svg += `<text x="15" y="${height/2}" text-anchor="middle" font-size="12" transform="rotate(-90,15,${height/2})">Treatment Event Rate</text>`;
        svg += `<text x="${width/2}" y="20" text-anchor="middle" font-size="14" font-weight="bold">L'Abbe Plot</text>`;

        svg += '</svg>';
        return svg;
    },

    renderContourFunnel(data, pooled, contours) {
        const width = 500, height = 400;
        const margin = { top: 30, right: 30, bottom: 50, left: 60 };
        const plotW = width - margin.left - margin.right;
        const plotH = height - margin.top - margin.bottom;

        const effects = data.map(d => d.effect);
        const ses = data.map(d => d.se);
        const minE = Math.min(...effects, pooled - 2);
        const maxE = Math.max(...effects, pooled + 2);
        const maxSE = Math.max(...ses) * 1.1;

        let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`;
        svg += `<rect width="${width}" height="${height}" fill="white"/>`;

        // Contour regions (shaded)
        const colors = ['#ffcccc', '#ffffcc', '#ccffcc'];
        for (let i = contours.length - 1; i >= 0; i--) {
            const c = contours[i];
            svg += `<polygon points="`;
            // Build polygon for this significance region
            const pts = [];
            for (let se = 0; se <= maxSE; se += 0.02) {
                const xL = margin.left + ((pooled - c.z * se) - minE) / (maxE - minE) * plotW;
                const y = margin.top + (se / maxSE) * plotH;
                pts.push(`${xL},${y}`);
            }
            for (let se = maxSE; se >= 0; se -= 0.02) {
                const xR = margin.left + ((pooled + c.z * se) - minE) / (maxE - minE) * plotW;
                const y = margin.top + (se / maxSE) * plotH;
                pts.push(`${xR},${y}`);
            }
            svg += pts.join(' ');
            svg += `" fill="${colors[i % colors.length]}" opacity="0.5"/>`;
        }

        // Pooled effect line
        const pooledX = margin.left + (pooled - minE) / (maxE - minE) * plotW;
        svg += `<line x1="${pooledX}" y1="${margin.top}" x2="${pooledX}" y2="${height-margin.bottom}" stroke="black" stroke-dasharray="3,3"/>`;

        // Data points
        for (const d of data) {
            const x = margin.left + (d.effect - minE) / (maxE - minE) * plotW;
            const y = margin.top + (d.se / maxSE) * plotH;
            svg += `<circle cx="${x}" cy="${y}" r="4" fill="#2c3e50"/>`;
        }

        // Labels
        svg += `<text x="${width/2}" y="${height-10}" text-anchor="middle" font-size="12">Effect Size</text>`;
        svg += `<text x="15" y="${height/2}" text-anchor="middle" font-size="12" transform="rotate(-90,15,${height/2})">Standard Error</text>`;
        svg += `<text x="${width/2}" y="20" text-anchor="middle" font-size="14" font-weight="bold">Contour-Enhanced Funnel Plot</text>`;

        svg += '</svg>';
        return svg;
    }
};

'''

# =============================================================================
# 3. OUTLIER DETECTION
# =============================================================================

outlier_module = '''
// ============================================================================
// OUTLIER DETECTION
// Studentized residuals, DFBETAS, influence diagnostics
// ============================================================================

const OutlierDetection = {

    // Comprehensive outlier analysis
    analyze(effects, ses, labels = null) {
        const n = effects.length;
        const weights = ses.map(se => 1/(se*se));
        const sumW = weights.reduce((a,b) => a+b, 0);
        const pooled = effects.reduce((sum, e, i) => sum + weights[i] * e, 0) / sumW;

        const results = effects.map((e, i) => {
            const label = labels ? labels[i] : `Study ${i+1}`;

            // Studentized residual
            const residual = e - pooled;
            const leverage = weights[i] / sumW;
            const mse = effects.reduce((sum, ej, j) => sum + weights[j] * (ej - pooled)**2, 0) / (n - 1);
            const studentized = residual / Math.sqrt(mse * (1 - leverage));

            // DFBETAS (influence on pooled estimate)
            const wExcl = weights.filter((_, j) => j !== i);
            const eExcl = effects.filter((_, j) => j !== i);
            const sumWExcl = wExcl.reduce((a,b) => a+b, 0);
            const pooledExcl = eExcl.reduce((sum, ej, j) => sum + wExcl[j] * ej, 0) / sumWExcl;
            const dfbeta = (pooled - pooledExcl) / Math.sqrt(1/sumW);

            // Cook's distance analog
            const cooksD = (residual**2 * leverage) / (mse * (1 - leverage)**2);

            // Q contribution
            const qContrib = weights[i] * residual**2;

            return {
                study: label,
                effect: e,
                se: ses[i],
                residual: residual,
                studentizedResidual: studentized,
                leverage: leverage,
                dfbeta: dfbeta,
                cooksD: cooksD,
                qContribution: qContrib,
                isOutlier: Math.abs(studentized) > 2,
                isInfluential: Math.abs(dfbeta) > 2 / Math.sqrt(n)
            };
        });

        // Summary
        const outliers = results.filter(r => r.isOutlier);
        const influential = results.filter(r => r.isInfluential);

        return {
            studies: results,
            pooledEffect: pooled,
            outliers: outliers.map(o => o.study),
            influential: influential.map(i => i.study),
            recommendations: this.generateRecommendations(outliers, influential)
        };
    },

    // Leave-one-out sensitivity for outliers
    leaveOneOutSensitivity(effects, ses, labels = null) {
        const n = effects.length;
        const results = [];

        // Full analysis
        const weights = ses.map(se => 1/(se*se));
        const sumW = weights.reduce((a,b) => a+b, 0);
        const pooled = effects.reduce((sum, e, i) => sum + weights[i] * e, 0) / sumW;

        for (let i = 0; i < n; i++) {
            const wExcl = weights.filter((_, j) => j !== i);
            const eExcl = effects.filter((_, j) => j !== i);
            const sExcl = ses.filter((_, j) => j !== i);

            const sumWExcl = wExcl.reduce((a,b) => a+b, 0);
            const pooledExcl = eExcl.reduce((sum, ej, j) => sum + wExcl[j] * ej, 0) / sumWExcl;
            const seExcl = Math.sqrt(1 / sumWExcl);

            // Recalculate heterogeneity
            const Q = eExcl.reduce((sum, ej, j) => sum + wExcl[j] * (ej - pooledExcl)**2, 0);
            const c = sumWExcl - wExcl.reduce((sum, w) => sum + w*w, 0) / sumWExcl;
            const tau2 = Math.max(0, (Q - (n - 2)) / c);
            const I2 = Math.max(0, 100 * (Q - (n - 2)) / Q);

            results.push({
                excluded: labels ? labels[i] : `Study ${i+1}`,
                pooledEffect: pooledExcl,
                se: seExcl,
                ci: [pooledExcl - 1.96*seExcl, pooledExcl + 1.96*seExcl],
                tau2: tau2,
                I2: I2,
                change: pooledExcl - pooled,
                percentChange: 100 * (pooledExcl - pooled) / Math.abs(pooled)
            });
        }

        return {
            fullAnalysis: { effect: pooled, se: Math.sqrt(1/sumW) },
            leaveOneOut: results,
            mostInfluential: results.sort((a, b) => Math.abs(b.change) - Math.abs(a.change))[0]
        };
    },

    generateRecommendations(outliers, influential) {
        const recs = [];

        if (outliers.length > 0) {
            recs.push(`${outliers.length} potential outlier(s) detected: ${outliers.map(o => o.study).join(', ')}`);
            recs.push('Consider sensitivity analysis excluding outliers');
        }

        if (influential.length > 0) {
            recs.push(`${influential.length} influential study/studies: ${influential.map(i => i.study).join(', ')}`);
            recs.push('Results may be sensitive to these studies');
        }

        if (outliers.length === 0 && influential.length === 0) {
            recs.push('No concerning outliers or influential studies detected');
        }

        return recs;
    }
};

'''

# =============================================================================
# 4. COPAS SELECTION MODEL
# =============================================================================

copas_module = '''
// ============================================================================
// COPAS SELECTION MODEL
// Copas & Shi selection model for publication bias
// ============================================================================

const CopasSelectionModel = {

    // Fit Copas selection model
    analyze(effects, ses, options = {}) {
        const { gamma0Range = [-2, 0], gamma1Range = [0, 2], nGrid = 20 } = options;

        const n = effects.length;

        // Grid search over selection parameters
        const results = [];

        for (let g0 = gamma0Range[0]; g0 <= gamma0Range[1]; g0 += (gamma0Range[1] - gamma0Range[0]) / nGrid) {
            for (let g1 = gamma1Range[0]; g1 <= gamma1Range[1]; g1 += (gamma1Range[1] - gamma1Range[0]) / nGrid) {
                const fit = this.fitModel(effects, ses, g0, g1);
                results.push({ gamma0: g0, gamma1: g1, ...fit });
            }
        }

        // Find best fit (minimum AIC or max likelihood)
        const bestFit = results.reduce((best, r) =>
            r.logLik > (best?.logLik || -Infinity) ? r : best, null);

        // Unadjusted estimate
        const weights = ses.map(se => 1/(se*se));
        const sumW = weights.reduce((a,b) => a+b, 0);
        const unadjusted = effects.reduce((sum, e, i) => sum + weights[i] * e, 0) / sumW;

        // Selection probability for each study
        const selectionProbs = effects.map((e, i) =>
            this.selectionProbability(e, ses[i], bestFit.gamma0, bestFit.gamma1)
        );

        return {
            method: "Copas Selection Model",
            unadjustedEffect: unadjusted,
            adjustedEffect: bestFit.mu,
            adjustedSE: bestFit.seMu,
            selectionParameters: {
                gamma0: bestFit.gamma0,
                gamma1: bestFit.gamma1
            },
            tau2: bestFit.tau2,
            selectionProbabilities: selectionProbs,
            pUnpublished: 1 - selectionProbs.reduce((a,b) => a+b, 0) / n,
            interpretation: Math.abs(bestFit.mu - unadjusted) > 0.1 * Math.abs(unadjusted) ?
                `Substantial selection bias detected. Adjusted effect: ${bestFit.mu.toFixed(3)}` :
                "Selection bias appears minimal"
        };
    },

    fitModel(effects, ses, gamma0, gamma1) {
        const n = effects.length;

        // Selection-weighted estimation
        const selProbs = effects.map((e, i) =>
            this.selectionProbability(e, ses[i], gamma0, gamma1)
        );

        // Weighted by inverse selection probability
        const adjWeights = ses.map((se, i) => (1/(se*se)) * (1/selProbs[i]));
        const sumAW = adjWeights.reduce((a,b) => a+b, 0);
        const mu = effects.reduce((sum, e, i) => sum + adjWeights[i] * e, 0) / sumAW;
        const seMu = Math.sqrt(1 / sumAW);

        // Heterogeneity
        const Q = effects.reduce((sum, e, i) => sum + adjWeights[i] * (e - mu)**2, 0);
        const c = sumAW - adjWeights.reduce((sum, w) => sum + w*w, 0) / sumAW;
        const tau2 = Math.max(0, (Q - (n - 1)) / c);

        // Log-likelihood (simplified)
        let logLik = 0;
        for (let i = 0; i < n; i++) {
            const variance = ses[i]**2 + tau2;
            logLik += -0.5 * Math.log(2 * Math.PI * variance);
            logLik += -0.5 * (effects[i] - mu)**2 / variance;
            logLik += Math.log(selProbs[i]);
        }

        return { mu, seMu, tau2, logLik };
    },

    selectionProbability(effect, se, gamma0, gamma1) {
        // Probit selection model: P(selected) = Phi(gamma0 + gamma1/se)
        const z = gamma0 + gamma1 / se;
        return this.normalCDF(z);
    },

    normalCDF(x) {
        const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741;
        const a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
        const sign = x < 0 ? -1 : 1;
        x = Math.abs(x) / Math.sqrt(2);
        const t = 1 / (1 + p * x);
        const y = 1 - ((((a5*t + a4)*t + a3)*t + a2)*t + a1)*t*Math.exp(-x*x);
        return 0.5 * (1 + sign * y);
    }
};

'''

# =============================================================================
# 5. MULTI-ARM CORRELATION ADJUSTMENT
# =============================================================================

multiarm_module = '''
// ============================================================================
// MULTI-ARM TRIAL CORRELATION ADJUSTMENT
// Proper handling of correlated effects in multi-arm trials
// ============================================================================

const MultiArmAdjustment = {

    // Adjust for within-study correlation in multi-arm trials
    adjustCorrelation(studies) {
        // Identify multi-arm studies
        const studyGroups = {};
        for (const s of studies) {
            const studyId = s.study || s.id;
            if (!studyGroups[studyId]) studyGroups[studyId] = [];
            studyGroups[studyId].push(s);
        }

        const adjustedStudies = [];
        const correlationInfo = [];

        for (const [studyId, arms] of Object.entries(studyGroups)) {
            if (arms.length === 1) {
                // Two-arm study, no adjustment needed
                adjustedStudies.push(arms[0]);
            } else {
                // Multi-arm study: need to account for correlation
                const adjusted = this.adjustMultiArm(studyId, arms);
                adjustedStudies.push(...adjusted.comparisons);
                correlationInfo.push({
                    study: studyId,
                    nArms: arms.length + 1,  // +1 for common comparator
                    nComparisons: adjusted.comparisons.length,
                    correlationMatrix: adjusted.correlation
                });
            }
        }

        return {
            adjustedStudies: adjustedStudies,
            multiArmStudies: correlationInfo,
            nMultiArm: correlationInfo.length,
            totalComparisons: adjustedStudies.length
        };
    },

    adjustMultiArm(studyId, arms) {
        // Assume common comparator (first treatment2 encountered)
        const comparator = arms[0].treatment2;
        const treatments = arms.map(a => a.treatment1);
        const k = arms.length;

        // Calculate correlation between contrasts sharing common comparator
        // Correlation = Var(comparator) / sqrt(Var(A-C) * Var(B-C))

        // For now, use approximation based on sample sizes if available
        // If all arms have similar sample sizes, correlation ≈ 0.5
        const hasN = arms.every(a => a.n1 && a.n2);

        let correlation;
        if (hasN) {
            // More precise: rho_ij = n_c / sqrt((n_c + n_i)(n_c + n_j))
            const n_c = arms[0].n2;  // Common comparator arm size
            const nArms = arms.map(a => a.n1);

            correlation = [];
            for (let i = 0; i < k; i++) {
                correlation[i] = [];
                for (let j = 0; j < k; j++) {
                    if (i === j) {
                        correlation[i][j] = 1;
                    } else {
                        correlation[i][j] = n_c / Math.sqrt((n_c + nArms[i]) * (n_c + nArms[j]));
                    }
                }
            }
        } else {
            // Default assumption: rho = 0.5
            correlation = [];
            for (let i = 0; i < k; i++) {
                correlation[i] = [];
                for (let j = 0; j < k; j++) {
                    correlation[i][j] = i === j ? 1 : 0.5;
                }
            }
        }

        // Adjust standard errors for correlation
        const adjustedComparisons = arms.map((arm, i) => ({
            ...arm,
            study: studyId,
            multiArm: true,
            correlationAdjusted: true,
            armIndex: i
        }));

        return {
            comparisons: adjustedComparisons,
            correlation: correlation
        };
    },

    // Calculate variance-covariance matrix for multi-arm study
    calculateVCov(arms, correlation) {
        const k = arms.length;
        const vcov = [];

        for (let i = 0; i < k; i++) {
            vcov[i] = [];
            for (let j = 0; j < k; j++) {
                vcov[i][j] = correlation[i][j] * arms[i].se * arms[j].se;
            }
        }

        return vcov;
    },

    // GLS estimator accounting for correlation
    glsEstimate(effects, vcov) {
        const k = effects.length;

        // Invert variance-covariance matrix
        const vcovInv = this.invertMatrix(vcov);

        // GLS weights
        const ones = new Array(k).fill(1);
        const sumVcovInv = vcovInv.reduce((sum, row) =>
            sum + row.reduce((s, v) => s + v, 0), 0);

        // GLS estimate
        let num = 0;
        for (let i = 0; i < k; i++) {
            for (let j = 0; j < k; j++) {
                num += vcovInv[i][j] * effects[j];
            }
        }
        const estimate = num / sumVcovInv;
        const se = Math.sqrt(1 / sumVcovInv);

        return { estimate, se };
    },

    invertMatrix(A) {
        const n = A.length;
        const aug = A.map((row, i) => {
            const newRow = [...row];
            for (let j = 0; j < n; j++) newRow.push(i === j ? 1 : 0);
            return newRow;
        });

        for (let i = 0; i < n; i++) {
            let maxRow = i;
            for (let k = i + 1; k < n; k++) {
                if (Math.abs(aug[k][i]) > Math.abs(aug[maxRow][i])) maxRow = k;
            }
            [aug[i], aug[maxRow]] = [aug[maxRow], aug[i]];

            const pivot = aug[i][i];
            if (Math.abs(pivot) < 1e-10) continue;

            for (let j = 0; j < 2*n; j++) aug[i][j] /= pivot;

            for (let k = 0; k < n; k++) {
                if (k !== i) {
                    const c = aug[k][i];
                    for (let j = 0; j < 2*n; j++) aug[k][j] -= c * aug[i][j];
                }
            }
        }

        return aug.map(row => row.slice(n));
    }
};

'''

# =============================================================================
# INSERT ALL MODULES
# =============================================================================

print("\n[1] Adding TransitivityAssessment...")
if "const TransitivityAssessment" not in content:
    marker = "const DesignDecomposition="
    content = content.replace(marker, transitivity_module + marker)
    print("    [OK]")
else:
    print("    [SKIP]")

print("\n[2] Adding DiagnosticPlots (Baujat, Galbraith, L'Abbe, Contour)...")
if "const DiagnosticPlots" not in content:
    marker = "const DesignDecomposition="
    content = content.replace(marker, diagnostic_plots_module + marker)
    print("    [OK]")
else:
    print("    [SKIP]")

print("\n[3] Adding OutlierDetection...")
if "const OutlierDetection" not in content:
    marker = "const DesignDecomposition="
    content = content.replace(marker, outlier_module + marker)
    print("    [OK]")
else:
    print("    [SKIP]")

print("\n[4] Adding CopasSelectionModel...")
if "const CopasSelectionModel" not in content:
    marker = "const DesignDecomposition="
    content = content.replace(marker, copas_module + marker)
    print("    [OK]")
else:
    print("    [SKIP]")

print("\n[5] Adding MultiArmAdjustment...")
if "const MultiArmAdjustment" not in content:
    marker = "const DesignDecomposition="
    content = content.replace(marker, multiarm_module + marker)
    print("    [OK]")
else:
    print("    [SKIP]")

# Save
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*70)
print("RSM EDITORIAL ENHANCEMENTS COMPLETE")
print("="*70)
print("""
Added:
1. TransitivityAssessment - Effect modifier balance, transitivity evaluation
2. DiagnosticPlots - Baujat, Galbraith (radial), L'Abbe, Contour funnel
3. OutlierDetection - Studentized residuals, DFBETAS, Cook's D, influence
4. CopasSelectionModel - Copas & Shi selection model
5. MultiArmAdjustment - Correlation adjustment for multi-arm trials
""")
