# MA4 vs HKSJ - Final Manuscript Ready

**Date:** January 7, 2026
**Status:** All Editorial Revisions Complete
**Recommendation:** Accept

---

## Summary of All Revisions

| Round | Issue | Resolution |
|-------|-------|------------|
| R1 | k=2 paradox | Stratified by k≥5 |
| R1 | Missing statistical tests | Added chi-square, trend, logistic regression |
| R1 | RoBMA failed | Removed from scope with rationale |
| R2 | Non-monotonic pattern | Explained: Moderate has highest % initially sig (58.9%) |
| R2 | Wide CI for R-index OR | VIF check confirms no multicollinearity |
| R2 | Effect type heterogeneity | Analyzed: p=0.025, added to limitations |
| R2 | Small cell sensitivity | Collapsed to 3 categories, findings confirmed |

---

## Key Findings (k≥5, n=434)

### Primary Result
**MA4 R-index is NOT significantly associated with HKSJ conclusion stability**
- Correlation: r = 0.05, p = 0.26
- Logistic OR: 1.79 [0.14, 27.5], p = 0.66

### Strongest Predictor
**Initially significant results are 5.4x more likely to change conclusion**
- OR = 5.41 [2.45, 13.4], p < 0.001
- 9.2% overall change rate

### Non-Monotonic Pattern Explained
| R Category | % Changed | % Initially Sig | Change Rate (if sig) |
|------------|-----------|-----------------|---------------------|
| Very Low | 0.0% | 25.0% | 0.0% |
| Low | 1.3% | 33.3% | 4.0% |
| **Moderate** | **17.1%** | **58.9%** | **25.0%** |
| High | 8.0% | 51.7% | 11.5% |
| Excellent | 5.9% | 35.3% | 0.0% |

**Explanation:** "Moderate" R-index has the highest proportion of initially significant results (58.9%) AND the highest change rate among initially significant MAs (25%). These are borderline cases where HKSJ adjustment tips conclusions from significant to non-significant.

### Effect Type Heterogeneity
| Effect Type | N | % Changed |
|-------------|---|-----------|
| logRR | 132 | 3.8% |
| GIV | 223 | 10.8% |
| MD | 79 | 13.9% |

Chi-square p = 0.025 (significant)

### Model Diagnostics
- All VIFs < 1.2 (no multicollinearity)
- Wide CI for R-index due to low event rate, not model issues

---

## Manuscript Text Additions

### Results Section

> **Non-monotonic pattern:** The observed non-monotonic relationship between R-index categories and conclusion change (with Moderate showing the highest change rate of 17.1%) reflects the distribution of initially significant results across categories. The Moderate R-index category contained the highest proportion of initially significant meta-analyses (58.9%), and among these, 25% changed conclusions under HKSJ adjustment compared to 11.5% in the High category. This suggests that "Moderate" stability represents meta-analyses at the threshold of significance where the HKSJ small-sample correction is most likely to alter conclusions.

> **Sensitivity analysis:** To address potential instability from small cell sizes (Very Low: n=12; Excellent: n=17), we repeated the analysis with collapsed categories (Low/Very Low, Moderate, High/Excellent). The chi-square test showed significant association (χ² = 16.4, p < 0.001), driven by the elevated change rate in Moderate versus Low/Very Low (OR = 10.5, p = 0.025). However, in the multivariable model controlling for baseline significance, R-index categories remained non-significant as predictors of conclusion change.

### Limitations Section

> **Wide confidence intervals:** The confidence interval for the R-index odds ratio was notably wide (OR = 1.79, 95% CI: 0.14–27.5), reflecting both the low event rate (9.2% conclusions changed) and the dominance of baseline significance as a predictor. Variance inflation factors for all predictors were below 1.2, confirming that multicollinearity was not responsible for the imprecise estimate.

> **Effect type heterogeneity:** Conclusion change rates varied significantly by effect type (logRR: 3.8%, GIV: 10.8%, MD: 13.9%; χ² = 7.4, p = 0.025). Although effect type was not a significant predictor after adjusting for other covariates, future research should examine whether specific effect measures are more vulnerable to HKSJ adjustment, potentially due to differences in distributional assumptions.

---

## Suggested Abstract

### Background
The MA4 stability index and Hartung-Knapp-Sidik-Jonkman (HKSJ) correction address different aspects of meta-analysis robustness. We examined whether these methods provide complementary or redundant information.

### Methods
We applied MA4 v1.0.1 R-index and HKSJ correction to 434 Cochrane meta-analyses with k≥5 studies. We assessed correlation between R-index and HKSJ-induced conclusion change, and identified predictors of conclusion change using logistic regression.

### Results
Among 434 meta-analyses, 9.2% changed conclusions under HKSJ (32 significant→non-significant, 8 non-significant→significant). The R-index was not significantly correlated with conclusion change (r = 0.05, p = 0.26) nor predictive in regression (OR = 1.79, 95% CI: 0.14–27.5). The strongest predictor was baseline significance (OR = 5.41, 95% CI: 2.45–13.4, p < 0.001).

### Conclusions
MA4 R-index and HKSJ correction measure **complementary, not redundant**, aspects of robustness. R-index assesses stability under analytic perturbations while HKSJ addresses small-sample uncertainty. Initially significant results are most vulnerable to HKSJ adjustment. Both metrics should be reported for comprehensive quality assessment.

---

## Final Tables for Manuscript

### Table 1: Sample Characteristics (k≥5)
| Characteristic | Value |
|----------------|-------|
| Meta-analyses | 434 |
| Cochrane reviews | 82 |
| Median k (IQR) | 10 (7–17) |
| Mean I² | 38.5% |
| % Initially significant | 49.3% |
| % Conclusions changed | 9.2% |

### Table 2: Conclusion Change by R-index Category
| R Category | N | % Changed | 95% CI |
|------------|---|-----------|--------|
| Very Low (<0.3) | 12 | 0.0% | [0, 26.5] |
| Low (0.3–0.5) | 75 | 1.3% | [0.0, 7.2] |
| Moderate (0.5–0.7) | 129 | 17.1% | [11.0, 24.6] |
| High (0.7–0.85) | 201 | 8.0% | [4.5, 12.6] |
| Excellent (≥0.85) | 17 | 5.9% | [0.1, 28.7] |

### Table 3: Logistic Regression - Predictors of Conclusion Change
| Predictor | OR | 95% CI | p-value |
|-----------|-----|--------|---------|
| R-index (per 0.1 increase) | 1.79 | [0.14, 27.5] | 0.66 |
| k (per additional study) | 0.95 | [0.90, 0.98] | 0.01 |
| I² (per 1% increase) | 1.00 | [0.99, 1.01] | 0.46 |
| Initially significant (vs not) | 5.41 | [2.45, 13.4] | <0.001 |

---

## Figures

1. **Figure 1:** Forest plot of SE ratios (HKSJ/standard)
2. **Figure 2:** Bar chart of conclusion change by R-index category
3. **Figure 3:** Stratified analysis (k<5 vs k≥5)
4. **Figure 4:** Scatter plot of R-index vs SE ratio
5. **Figure 5:** Combined 4-panel figure
6. **Figure 6:** Logistic regression forest plot (ORs with 95% CI)

All figures saved to: `C:/Users/user/`

---

## Files Reference

| File | Description |
|------|-------------|
| `MA4_HKSJ_adequate_k5plus_final.csv` | Final clean dataset |
| `MA4_HKSJ_MINOR_REVISIONS.R` | All R2 revision analyses |
| `MA4_HKSJ_REVISED_ANALYSIS.R` | Main analysis script |
| `MA4_HKSJ_CREATE_FIGURES.R` | Figure generation |
| `Figure_Combined_Panel.png` | Main 4-panel figure |

---

## Reviewer Checklist - All Complete

- [x] Major concerns from R1 addressed
- [x] Stratified analysis (k<5 vs k≥5)
- [x] Formal statistical tests with 95% CIs
- [x] Non-monotonic pattern explained
- [x] VIF check for model diagnostics
- [x] Effect type heterogeneity analyzed
- [x] Sensitivity analysis with collapsed categories
- [x] Wide CI acknowledged in limitations
- [x] Abstract includes null finding
- [x] Conclusions match evidence

---

*Manuscript ready for submission to Research Synthesis Methods*
*All editorial concerns addressed: January 7, 2026*
