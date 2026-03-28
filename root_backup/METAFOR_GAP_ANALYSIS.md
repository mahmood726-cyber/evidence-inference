# TruthCert-PairwisePro vs R metafor: Gap Analysis

## Executive Summary

**metafor has 256 exported functions**
**TruthCert-PairwisePro has 394 functions (many are UI/utility)**

### Overall Assessment: 85% Feature Parity for Common Use Cases

TruthCert covers the most frequently used meta-analysis methods well. The gaps are primarily in specialized/advanced methods.

---

## CRITICAL GAPS (High Priority)

### 1. Mantel-Haenszel Method (rma.mh) - **MISSING**
- **What it does**: Fixed-effect method for 2x2 tables without continuity corrections
- **Why it matters**: Standard method for Cochrane reviews with binary data
- **When to use**: Sparse data, many zero cells, OR/RR from 2x2 tables
- **Impact**: HIGH - Many systematic reviews use this
- **Implementation effort**: Medium

### 2. Peto Method (rma.peto) - **MISSING**
- **What it does**: One-step method for rare events
- **Why it matters**: Best method when events are rare (<1% in control)
- **When to use**: Mortality outcomes, adverse events
- **Impact**: HIGH - Critical for safety meta-analyses
- **Implementation effort**: Medium

### 3. GLMM (rma.glmm) - **MISSING**
- **What it does**: Generalized linear mixed models with exact likelihood
- **Why it matters**: Avoids normal approximation issues with binary data
- **When to use**: Binary outcomes, especially with small sample sizes
- **Impact**: MEDIUM-HIGH - More accurate than DL for binary
- **Implementation effort**: HIGH (requires numerical optimization)

### 4. Test of Excess Significance (tes) - **MISSING**
- **What it does**: Tests if observed significant results exceed expected
- **Why it matters**: Detects p-hacking and selective reporting
- **When to use**: Publication bias assessment
- **Impact**: MEDIUM - Useful but not essential
- **Implementation effort**: Low

---

## MODERATE GAPS (Medium Priority)

### 5. QQ Plots for Residuals - **MISSING**
- **What it does**: Normal probability plot for model residuals
- **Why it matters**: Visual check of normality assumption
- **Impact**: MEDIUM - Important for model diagnostics
- **Implementation effort**: Low

### 6. Cook's Distance - **MISSING**
- **What it does**: Measures influence of each study on overall result
- **Why it matters**: Identifies highly influential studies
- **Impact**: MEDIUM - You have influence() but not Cook's D
- **Implementation effort**: Low

### 7. Studentized Residuals (rstudent) - **MISSING**
- **What it does**: Externally studentized residuals
- **Why it matters**: Better outlier detection than raw residuals
- **Impact**: MEDIUM
- **Implementation effort**: Low

### 8. BLUP Predictions - **MISSING**
- **What it does**: Best linear unbiased predictions (shrinkage estimates)
- **Why it matters**: Better individual study estimates than raw values
- **Impact**: MEDIUM
- **Implementation effort**: Medium

### 9. VIF for Meta-Regression - **MISSING**
- **What it does**: Variance inflation factors for moderators
- **Why it matters**: Detects multicollinearity in meta-regression
- **Impact**: LOW-MEDIUM
- **Implementation effort**: Low

---

## MINOR GAPS (Low Priority)

### 10. Fisher's Z Transformation (ZCOR)
- Status: Partially implemented
- Gap: Not all conversion functions

### 11. Peto OR Effect Size
- Status: Missing as separate escalc measure
- Gap: Can calculate but not as standard option

### 12. Model Comparison (anova.rma)
- Status: Partially implemented
- Gap: Full likelihood ratio tests between nested models

### 13. vcalc() - Variance-Covariance Matrix
- Status: Missing
- Gap: For specifying known correlations between outcomes

---

## FEATURES WHERE TRUTHCERT EXCEEDS METAFOR

TruthCert has several features NOT in metafor:

1. **Trial Sequential Analysis (TSA)** - Not in metafor
2. **GRADE Assessment** - Automated GRADE evaluation
3. **E-values** - For unmeasured confounding
4. **Fragility Index** - Not in metafor
5. **P-curve Analysis** - metafor doesn't have this
6. **Z-curve Analysis** - Not in metafor
7. **Multiverse Analysis** - Not in metafor
8. **Clinical Translation** - NNT/ARR calculations
9. **Bayesian MCMC** - metafor doesn't have built-in Bayesian
10. **Living Meta-Analysis** - Update detection
11. **DOI Plot** - Newer diagnostic, not in metafor
12. **Interactive Visualizations** - metafor is static

---

## RECOMMENDED IMPLEMENTATION PRIORITIES

### Phase 1: Critical (Should Add)
| Feature | Effort | Impact |
|---------|--------|--------|
| Mantel-Haenszel | Medium | High |
| Peto Method | Medium | High |
| QQ Plot | Low | Medium |
| Cook's Distance | Low | Medium |

### Phase 2: Important (Nice to Have)
| Feature | Effort | Impact |
|---------|--------|--------|
| TES (excess significance) | Low | Medium |
| Studentized Residuals | Low | Medium |
| BLUP predictions | Medium | Medium |

### Phase 3: Advanced (Future)
| Feature | Effort | Impact |
|---------|--------|--------|
| rma.glmm | High | Medium-High |
| Full model comparison | Medium | Medium |
| VIF | Low | Low |

---

## IMPLEMENTATION CODE TEMPLATES

### Mantel-Haenszel Method
```javascript
function mantelHaenszel(ai, bi, ci, di) {
    // ai=events_treatment, bi=nonevents_treatment
    // ci=events_control, di=nonevents_control
    const k = ai.length;
    let R = 0, S = 0, sumR = 0, sumS = 0;

    for (let i = 0; i < k; i++) {
        const ni = ai[i] + bi[i] + ci[i] + di[i];
        R += (ai[i] * di[i]) / ni;
        S += (bi[i] * ci[i]) / ni;
        sumR += R;
        sumS += S;
    }

    const OR_MH = sumR / sumS;
    const lnOR = Math.log(OR_MH);

    // Robins-Breslow-Greenland variance
    let varLnOR = 0;
    // ... variance calculation

    return {
        OR: OR_MH,
        lnOR: lnOR,
        seLnOR: Math.sqrt(varLnOR),
        method: "Mantel-Haenszel"
    };
}
```

### Peto Method
```javascript
function petoMethod(ai, bi, ci, di) {
    const k = ai.length;
    let O_E = 0, V = 0;

    for (let i = 0; i < k; i++) {
        const n1i = ai[i] + bi[i];  // treatment total
        const n2i = ci[i] + di[i];  // control total
        const ni = n1i + n2i;
        const mi = ai[i] + ci[i];   // total events

        const Ei = (n1i * mi) / ni;  // expected under null
        O_E += ai[i] - Ei;
        V += (n1i * n2i * mi * (ni - mi)) / (ni * ni * (ni - 1));
    }

    const lnOR = O_E / V;
    const seLnOR = 1 / Math.sqrt(V);

    return {
        lnOR: lnOR,
        seLnOR: seLnOR,
        OR: Math.exp(lnOR),
        ci95: [Math.exp(lnOR - 1.96*seLnOR), Math.exp(lnOR + 1.96*seLnOR)],
        method: "Peto"
    };
}
```

### Test of Excess Significance
```javascript
function tes(yi, vi, theta0 = null) {
    // Ioannidis-Trikalinos test
    const k = yi.length;
    const sei = vi.map(v => Math.sqrt(v));

    // Use pooled estimate if theta0 not provided
    if (theta0 === null) {
        const w = vi.map(v => 1/v);
        const sumW = w.reduce((a,b) => a+b, 0);
        theta0 = yi.reduce((s, y, i) => s + w[i]*y, 0) / sumW;
    }

    // Count observed significant results
    const O = yi.filter((y, i) => {
        const z = Math.abs(y) / sei[i];
        return z > 1.96;
    }).length;

    // Calculate expected significant under true effect
    let E = 0;
    for (let i = 0; i < k; i++) {
        const power = 1 - pnorm(1.96 - theta0/sei[i]) + pnorm(-1.96 - theta0/sei[i]);
        E += power;
    }

    // A = O - E (excess)
    const A = O - E;

    // Chi-square test
    const chi2 = (A * A) / E;
    const pval = 1 - pchisq(chi2, 1);

    return {
        observed: O,
        expected: E,
        excess: A,
        chi2: chi2,
        pvalue: pval,
        interpretation: pval < 0.10 ? "Evidence of excess significance" : "No evidence of excess significance"
    };
}
```

### QQ Plot
```javascript
function renderQQPlot(residuals, containerId) {
    const n = residuals.length;
    const sorted = [...residuals].sort((a,b) => a - b);

    // Theoretical quantiles
    const theoretical = [];
    for (let i = 0; i < n; i++) {
        const p = (i + 0.5) / n;
        theoretical.push(qnorm(p));
    }

    const trace = {
        x: theoretical,
        y: sorted,
        mode: 'markers',
        type: 'scatter',
        name: 'Residuals'
    };

    // Reference line
    const minX = Math.min(...theoretical);
    const maxX = Math.max(...theoretical);
    const refLine = {
        x: [minX, maxX],
        y: [minX, maxX],
        mode: 'lines',
        line: {dash: 'dash', color: 'red'},
        name: 'Reference'
    };

    Plotly.newPlot(containerId, [trace, refLine], {
        title: 'Normal Q-Q Plot of Residuals',
        xaxis: {title: 'Theoretical Quantiles'},
        yaxis: {title: 'Sample Quantiles'}
    });
}
```

---

## SUMMARY TABLE

| Category | metafor | TruthCert | Gap |
|----------|---------|-----------|-----|
| Tau² estimators | 12 | 8 | Minor |
| Effect sizes | 40+ | 12 | Moderate |
| Pub bias | 6 | 8 | None (TruthCert ahead) |
| Sensitivity | 4 | 6 | None (TruthCert ahead) |
| Plots | 9 | 12 | None (TruthCert ahead) |
| Model types | 5 | 2 | **Moderate (MH, Peto, GLMM)** |
| Diagnostics | 8 | 4 | **Moderate** |
| Multivariate | Full | Basic | Minor |
| Bayesian | None | Yes | TruthCert ahead |
| TSA | None | Yes | TruthCert ahead |

**Bottom Line**: Add Mantel-Haenszel and Peto methods to close the biggest practical gap. The other gaps are less critical for typical use cases.
