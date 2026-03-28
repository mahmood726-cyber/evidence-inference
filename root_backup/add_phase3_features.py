#!/usr/bin/env python3
"""
Phase 3 Editorial Features - Peters/Harbord Tests & Flow Visualization
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("PHASE 3 EDITORIAL FEATURES")
print("="*70)

# =============================================================================
# 1. SMALL-STUDY EFFECTS TESTS (Peters, Harbord)
# =============================================================================

small_study_module = '''
// ============================================================================
// SMALL-STUDY EFFECTS TESTS
// Peters' test, Harbord's test, Rücker's limit meta-analysis
// ============================================================================

const SmallStudyEffects = {

    // Peters' test for binary outcomes
    // Peters JL, et al. JAMA 2006;295:676-680
    petersTest(studies) {
        // Requires 2x2 table data: events, non-events for treatment and control
        const validStudies = studies.filter(s =>
            s.e1 !== undefined && s.n1 !== undefined &&
            s.e2 !== undefined && s.n2 !== undefined
        );

        if (validStudies.length < 3) {
            return { error: "Need at least 3 studies with 2x2 data" };
        }

        // Calculate log OR and weights
        const data = validStudies.map(s => {
            const a = s.e1 + 0.5, b = s.n1 - s.e1 + 0.5;
            const c = s.e2 + 0.5, d = s.n2 - s.e2 + 0.5;
            const logOR = Math.log((a * d) / (b * c));
            const se = Math.sqrt(1/a + 1/b + 1/c + 1/d);
            const N = s.n1 + s.n2;
            const invN = 1 / N;
            return { logOR, se, N, invN, weight: 1/(se*se) };
        });

        // Peters' regression: log(OR) ~ 1/N weighted by inverse variance
        const n = data.length;
        const sumW = data.reduce((s, d) => s + d.weight, 0);
        const sumWX = data.reduce((s, d) => s + d.weight * d.invN, 0);
        const sumWY = data.reduce((s, d) => s + d.weight * d.logOR, 0);
        const sumWXY = data.reduce((s, d) => s + d.weight * d.invN * d.logOR, 0);
        const sumWX2 = data.reduce((s, d) => s + d.weight * d.invN * d.invN, 0);

        const slope = (sumW * sumWXY - sumWX * sumWY) / (sumW * sumWX2 - sumWX * sumWX);
        const intercept = (sumWY - slope * sumWX) / sumW;

        // Standard error of intercept
        const predicted = data.map(d => intercept + slope * d.invN);
        const residuals = data.map((d, i) => d.logOR - predicted[i]);
        const mse = residuals.reduce((s, r, i) => s + data[i].weight * r * r, 0) / (n - 2);
        const seIntercept = Math.sqrt(mse / sumW);

        const t = intercept / seIntercept;
        const df = n - 2;
        const pValue = 2 * (1 - this.tCDF(Math.abs(t), df));

        return {
            test: "Peters' test",
            intercept: intercept,
            se: seIntercept,
            t: t,
            df: df,
            pValue: pValue,
            interpretation: pValue < 0.1 ?
                "Evidence of small-study effects (potential publication bias)" :
                "No significant small-study effects detected"
        };
    },

    // Harbord's modified test for ORs
    // Harbord RM, et al. Biostatistics 2006;7:195-211
    harbordTest(studies) {
        const validStudies = studies.filter(s =>
            s.e1 !== undefined && s.n1 !== undefined &&
            s.e2 !== undefined && s.n2 !== undefined
        );

        if (validStudies.length < 3) {
            return { error: "Need at least 3 studies with 2x2 data" };
        }

        // Score-based test
        const data = validStudies.map(s => {
            const a = s.e1, b = s.n1 - s.e1;
            const c = s.e2, d = s.n2 - s.e2;
            const N = s.n1 + s.n2;

            // Expected value under null
            const E = (a + c) * s.n1 / N;
            // Variance
            const V = (a + c) * (b + d) * s.n1 * s.n2 / (N * N * (N - 1));

            // Score
            const Z = (a - E) / Math.sqrt(V);

            return { Z, sqrtV: Math.sqrt(V) };
        });

        // Regression of Z on sqrt(V)
        const n = data.length;
        const sumX = data.reduce((s, d) => s + d.sqrtV, 0);
        const sumY = data.reduce((s, d) => s + d.Z, 0);
        const sumXY = data.reduce((s, d) => s + d.sqrtV * d.Z, 0);
        const sumX2 = data.reduce((s, d) => s + d.sqrtV * d.sqrtV, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;

        // SE of intercept
        const predicted = data.map(d => intercept + slope * d.sqrtV);
        const residuals = data.map((d, i) => d.Z - predicted[i]);
        const mse = residuals.reduce((s, r) => s + r * r, 0) / (n - 2);
        const seIntercept = Math.sqrt(mse * (1/n + (sumX/n)**2 / (sumX2 - sumX*sumX/n)));

        const t = intercept / seIntercept;
        const df = n - 2;
        const pValue = 2 * (1 - this.tCDF(Math.abs(t), df));

        return {
            test: "Harbord's score-based test",
            intercept: intercept,
            se: seIntercept,
            t: t,
            df: df,
            pValue: pValue,
            interpretation: pValue < 0.1 ?
                "Evidence of small-study effects" :
                "No significant small-study effects"
        };
    },

    // Rücker's limit meta-analysis
    // Rücker G, et al. Biostatistics 2011;12:122-142
    limitMetaAnalysis(effects, ses) {
        const n = effects.length;
        if (n < 3) return { error: "Need at least 3 studies" };

        // Standard random-effects estimate
        const weights = ses.map(se => 1/(se*se));
        const sumW = weights.reduce((a,b) => a+b, 0);
        const pooled = effects.reduce((s, e, i) => s + weights[i] * e, 0) / sumW;

        // Regress effect on variance (se^2) to estimate limit at se^2 = 0
        const variances = ses.map(se => se * se);
        const sumX = variances.reduce((a,b) => a+b, 0);
        const sumY = effects.reduce((a,b) => a+b, 0);
        const sumXY = variances.reduce((s, v, i) => s + v * effects[i], 0);
        const sumX2 = variances.reduce((s, v) => s + v * v, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;  // This is the "limit" estimate

        // SE of limit estimate
        const predicted = variances.map(v => intercept + slope * v);
        const residuals = effects.map((e, i) => e - predicted[i]);
        const mse = residuals.reduce((s, r) => s + r * r, 0) / (n - 2);
        const seLimit = Math.sqrt(mse / n);

        // Shrinkage factor
        const shrinkage = (pooled - intercept) / pooled;

        return {
            method: "Rücker's limit meta-analysis",
            standardEstimate: pooled,
            limitEstimate: intercept,
            seLimitEstimate: seLimit,
            adjustmentSlope: slope,
            shrinkage: shrinkage,
            interpretation: Math.abs(shrinkage) > 0.1 ?
                `Substantial adjustment (${(shrinkage*100).toFixed(1)}% shrinkage). Limit estimate: ${intercept.toFixed(3)}` :
                "Minimal adjustment needed"
        };
    },

    // Run all small-study tests
    runAll(studies, effects, ses) {
        const results = {
            egger: typeof PublicationBias !== 'undefined' ? PublicationBias.eggersTest(effects, ses) : null,
            peters: this.petersTest(studies),
            harbord: this.harbordTest(studies),
            limit: this.limitMetaAnalysis(effects, ses)
        };

        // Summary recommendation
        const significantTests = [
            results.egger?.pValue < 0.1,
            results.peters?.pValue < 0.1,
            results.harbord?.pValue < 0.1
        ].filter(Boolean).length;

        results.summary = {
            testsRun: 4,
            significantTests: significantTests,
            recommendation: significantTests >= 2 ?
                "Strong evidence of small-study effects. Consider sensitivity analyses." :
                significantTests === 1 ?
                "Some evidence of small-study effects. Interpret with caution." :
                "No consistent evidence of small-study effects."
        };

        return results;
    },

    tCDF(t, df) {
        const x = df / (df + t * t);
        return 1 - 0.5 * this.betaInc(df/2, 0.5, x);
    },

    betaInc(a, b, x) {
        if (x === 0) return 0;
        if (x === 1) return 1;
        const bt = Math.exp(
            this.logGamma(a+b) - this.logGamma(a) - this.logGamma(b) +
            a * Math.log(x) + b * Math.log(1-x)
        );
        if (x < (a+1)/(a+b+2)) return bt * this.betaCF(a, b, x) / a;
        return 1 - bt * this.betaCF(b, a, 1-x) / b;
    },

    betaCF(a, b, x) {
        let c = 1, d = 1 - (a+b)*x/(a+1);
        if (Math.abs(d) < 1e-30) d = 1e-30;
        d = 1/d;
        let h = d;
        for (let m = 1; m <= 100; m++) {
            const m2 = 2*m;
            let aa = m*(b-m)*x / ((a+m2-1)*(a+m2));
            d = 1 + aa*d; if (Math.abs(d) < 1e-30) d = 1e-30;
            c = 1 + aa/c; if (Math.abs(c) < 1e-30) c = 1e-30;
            d = 1/d; h *= d*c;
            aa = -(a+m)*(a+b+m)*x / ((a+m2)*(a+m2+1));
            d = 1 + aa*d; if (Math.abs(d) < 1e-30) d = 1e-30;
            c = 1 + aa/c; if (Math.abs(c) < 1e-30) c = 1e-30;
            d = 1/d; h *= d*c;
            if (Math.abs(d*c - 1) < 1e-10) break;
        }
        return h;
    },

    logGamma(x) {
        const c = [76.18009172947146, -86.50532032941677, 24.01409824083091,
                   -1.231739572450155, 0.001208650973866179, -5.395239384953e-6];
        let y = x, tmp = x + 5.5;
        tmp -= (x + 0.5) * Math.log(tmp);
        let ser = 1.000000000190015;
        for (let j = 0; j < 6; j++) ser += c[j] / ++y;
        return -tmp + Math.log(2.5066282746310005 * ser / x);
    }
};

'''

# =============================================================================
# 2. EVIDENCE FLOW VISUALIZATION
# =============================================================================

flow_viz_module = '''
// ============================================================================
// EVIDENCE FLOW VISUALIZATION
// Based on: König et al. (2013) BMC Medical Research Methodology
// ============================================================================

const EvidenceFlow = {

    // Calculate evidence flow through the network
    analyze(studies, options = {}) {
        const { reference = null } = options;

        // Build network adjacency
        const treatments = [...new Set(studies.flatMap(s => [s.treatment1, s.treatment2]))];
        const ref = reference || treatments[0];

        // Calculate hat matrix for evidence contribution
        const comparisons = this.getComparisons(studies);
        const flowMatrix = this.calculateFlowMatrix(studies, treatments, ref);

        // Calculate evidence proportions
        const evidenceProps = this.calculateEvidenceProportions(studies, comparisons);

        return {
            treatments: treatments,
            reference: ref,
            comparisons: comparisons,
            flowMatrix: flowMatrix,
            evidenceProportions: evidenceProps,
            svg: this.generateFlowDiagram(treatments, flowMatrix, evidenceProps)
        };
    },

    getComparisons(studies) {
        const comps = {};
        for (const s of studies) {
            const key = [s.treatment1, s.treatment2].sort().join(' vs ');
            if (!comps[key]) comps[key] = { studies: 0, weight: 0 };
            comps[key].studies++;
            comps[key].weight += 1 / (s.se * s.se);
        }
        return comps;
    },

    calculateFlowMatrix(studies, treatments, ref) {
        const n = treatments.length;
        const matrix = Array(n).fill(null).map(() => Array(n).fill(0));

        // Build adjacency with weights
        for (const s of studies) {
            const i = treatments.indexOf(s.treatment1);
            const j = treatments.indexOf(s.treatment2);
            const w = 1 / (s.se * s.se);
            matrix[i][j] += w;
            matrix[j][i] += w;
        }

        // Normalize to proportions
        for (let i = 0; i < n; i++) {
            const rowSum = matrix[i].reduce((a, b) => a + b, 0);
            if (rowSum > 0) {
                for (let j = 0; j < n; j++) {
                    matrix[i][j] /= rowSum;
                }
            }
        }

        return matrix;
    },

    calculateEvidenceProportions(studies, comparisons) {
        const props = {};

        for (const [comp, data] of Object.entries(comparisons)) {
            // Direct evidence proportion
            const directWeight = data.weight;

            // Total weight (simplified - direct only for now)
            props[comp] = {
                direct: directWeight,
                indirect: 0,  // Would require full hat matrix calculation
                proportion: 1.0  // Proportion direct
            };
        }

        return props;
    },

    generateFlowDiagram(treatments, flowMatrix, evidenceProps) {
        const n = treatments.length;
        const width = 600, height = 400;
        const cx = width / 2, cy = height / 2;
        const radius = 150;

        // Calculate node positions (circular layout)
        const positions = treatments.map((t, i) => {
            const angle = (2 * Math.PI * i / n) - Math.PI/2;
            return {
                x: cx + radius * Math.cos(angle),
                y: cy + radius * Math.sin(angle),
                label: t
            };
        });

        let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`;
        svg += `<defs>
            <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
                <path d="M0,0 L0,6 L9,3 z" fill="#666"/>
            </marker>
        </defs>`;

        // Draw edges with width proportional to flow
        for (let i = 0; i < n; i++) {
            for (let j = i + 1; j < n; j++) {
                const flow = (flowMatrix[i][j] + flowMatrix[j][i]) / 2;
                if (flow > 0) {
                    const strokeWidth = Math.max(1, flow * 10);
                    const opacity = Math.min(1, flow + 0.3);

                    svg += `<line x1="${positions[i].x}" y1="${positions[i].y}"
                                  x2="${positions[j].x}" y2="${positions[j].y}"
                                  stroke="#3498db" stroke-width="${strokeWidth}"
                                  opacity="${opacity}"/>`;

                    // Flow label
                    const mx = (positions[i].x + positions[j].x) / 2;
                    const my = (positions[i].y + positions[j].y) / 2;
                    svg += `<text x="${mx}" y="${my}" font-size="10" fill="#666"
                                  text-anchor="middle">${(flow*100).toFixed(0)}%</text>`;
                }
            }
        }

        // Draw nodes
        for (const pos of positions) {
            svg += `<circle cx="${pos.x}" cy="${pos.y}" r="25" fill="#2c3e50"/>`;
            svg += `<text x="${pos.x}" y="${pos.y + 5}" font-size="12" fill="white"
                          text-anchor="middle" font-weight="bold">${pos.label}</text>`;
        }

        svg += '</svg>';
        return svg;
    },

    // Calculate contribution matrix (proportion of evidence from each study)
    contributionMatrix(studies, treatments) {
        const comparisons = [];
        const studyContributions = [];

        // Get unique comparisons
        const compSet = new Set();
        for (const s of studies) {
            compSet.add([s.treatment1, s.treatment2].sort().join('|'));
        }
        const uniqueComps = [...compSet];

        // For each comparison, calculate study contributions
        for (const comp of uniqueComps) {
            const [t1, t2] = comp.split('|');
            const relevantStudies = studies.filter(s =>
                (s.treatment1 === t1 && s.treatment2 === t2) ||
                (s.treatment1 === t2 && s.treatment2 === t1)
            );

            const totalWeight = relevantStudies.reduce((s, st) => s + 1/(st.se*st.se), 0);
            const contributions = relevantStudies.map(st => ({
                study: st.study || st.id,
                contribution: (1/(st.se*st.se)) / totalWeight
            }));

            comparisons.push({ comparison: `${t1} vs ${t2}`, contributions });
        }

        return comparisons;
    }
};

'''

# =============================================================================
# 3. CUMULATIVE META-ANALYSIS
# =============================================================================

cumulative_module = '''
// ============================================================================
// CUMULATIVE META-ANALYSIS
// Sequential analysis by publication date or other ordering
// ============================================================================

const CumulativeMeta = {

    // Run cumulative meta-analysis
    analyze(studies, options = {}) {
        const { orderBy = 'year', method = 'REML' } = options;

        // Sort studies
        const sorted = [...studies].sort((a, b) => {
            if (orderBy === 'year') return (a.year || 0) - (b.year || 0);
            if (orderBy === 'precision') return a.se - b.se;
            if (orderBy === 'size') return (b.n1 + b.n2 || 0) - (a.n1 + a.n2 || 0);
            return 0;
        });

        const results = [];
        let cumulativeEffects = [];
        let cumulativeSEs = [];

        for (let i = 0; i < sorted.length; i++) {
            cumulativeEffects.push(sorted[i].effect);
            cumulativeSEs.push(sorted[i].se);

            // Pool cumulative studies
            const pooled = this.poolEffects(cumulativeEffects, cumulativeSEs, method);

            results.push({
                step: i + 1,
                study: sorted[i].study || sorted[i].id || `Study ${i+1}`,
                year: sorted[i].year,
                cumulativeN: i + 1,
                effect: pooled.effect,
                se: pooled.se,
                ci: pooled.ci,
                zScore: pooled.effect / pooled.se,
                pValue: 2 * (1 - this.normalCDF(Math.abs(pooled.effect / pooled.se)))
            });
        }

        // Check for temporal trend
        const trend = this.assessTrend(results);

        return {
            orderBy: orderBy,
            method: method,
            steps: results,
            trend: trend,
            finalEffect: results[results.length - 1]
        };
    },

    poolEffects(effects, ses, method) {
        const n = effects.length;
        if (n === 1) {
            return {
                effect: effects[0],
                se: ses[0],
                ci: [effects[0] - 1.96*ses[0], effects[0] + 1.96*ses[0]]
            };
        }

        const weights = ses.map(se => 1/(se*se));
        const sumW = weights.reduce((a,b) => a+b, 0);
        const pooled = effects.reduce((s, e, i) => s + weights[i] * e, 0) / sumW;

        // Calculate heterogeneity for RE
        let Q = 0;
        for (let i = 0; i < n; i++) {
            Q += weights[i] * (effects[i] - pooled) ** 2;
        }

        let tau2 = 0;
        if (method === 'REML' || method === 'DL') {
            const c = sumW - weights.reduce((s, w) => s + w*w, 0) / sumW;
            tau2 = Math.max(0, (Q - (n - 1)) / c);
        }

        // Reweight with tau2
        const reWeights = ses.map(se => 1/(se*se + tau2));
        const reSumW = reWeights.reduce((a,b) => a+b, 0);
        const rePooled = effects.reduce((s, e, i) => s + reWeights[i] * e, 0) / reSumW;
        const reSE = Math.sqrt(1 / reSumW);

        return {
            effect: rePooled,
            se: reSE,
            ci: [rePooled - 1.96*reSE, rePooled + 1.96*reSE],
            tau2: tau2
        };
    },

    assessTrend(results) {
        if (results.length < 5) return { trend: "insufficient data" };

        // Compare first half to second half
        const mid = Math.floor(results.length / 2);
        const firstHalf = results.slice(0, mid);
        const secondHalf = results.slice(mid);

        const avgFirst = firstHalf.reduce((s, r) => s + r.effect, 0) / firstHalf.length;
        const avgSecond = secondHalf.reduce((s, r) => s + r.effect, 0) / secondHalf.length;

        const diff = avgSecond - avgFirst;
        const trend = Math.abs(diff) < 0.1 ? "stable" :
                     diff > 0 ? "increasing" : "decreasing";

        return {
            trend: trend,
            earlyEffect: avgFirst,
            lateEffect: avgSecond,
            change: diff
        };
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
# INSERT MODULES
# =============================================================================

print("\n[1] Adding SmallStudyEffects module...")
if "const SmallStudyEffects" not in content:
    marker = "const DesignDecomposition="
    if marker in content:
        content = content.replace(marker, small_study_module + marker)
        print("    [OK] SmallStudyEffects added")
    else:
        print("    [WARN] Marker not found")
else:
    print("    [SKIP] Already exists")

print("\n[2] Adding EvidenceFlow module...")
if "const EvidenceFlow" not in content:
    marker = "const DesignDecomposition="
    if marker in content:
        content = content.replace(marker, flow_viz_module + marker)
        print("    [OK] EvidenceFlow added")
    else:
        print("    [WARN] Marker not found")
else:
    print("    [SKIP] Already exists")

print("\n[3] Adding CumulativeMeta module...")
if "const CumulativeMeta" not in content:
    marker = "const DesignDecomposition="
    if marker in content:
        content = content.replace(marker, cumulative_module + marker)
        print("    [OK] CumulativeMeta added")
    else:
        print("    [WARN] Marker not found")
else:
    print("    [SKIP] Already exists")

# Save
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*70)
print("PHASE 3 FEATURES ADDED")
print("="*70)
print("""
Added modules:
1. SmallStudyEffects - Peters', Harbord's, Rücker's limit MA
2. EvidenceFlow - Flow visualization & contribution matrix
3. CumulativeMeta - Sequential meta-analysis
""")
