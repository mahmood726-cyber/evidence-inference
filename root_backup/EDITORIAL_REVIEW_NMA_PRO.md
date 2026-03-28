# Editorial Review: NMA Pro v6.2
## Research Synthesis Methods Perspective

**Reviewer:** AI Editorial Assessment
**Date:** January 2026
**Application:** NMA Pro v6.2 (Browser-based Network Meta-Analysis)

---

## EXECUTIVE SUMMARY

NMA Pro v6.2 represents a comprehensive browser-based network meta-analysis tool with impressive feature coverage. However, several methodological gaps exist that should be addressed before claiming superiority over established R packages.

**Overall Assessment:** Strong foundation with critical gaps in publication bias assessment and inconsistency testing.

---

## 1. CRITICAL METHODOLOGICAL GAPS

### 1.1 Publication Bias Assessment (HIGH PRIORITY)

**Current State:** The comparison document claims YES for Egger's test, Begg's test, Trim-and-Fill, and PET-PEESE, but code inventory shows these modules are **MISSING**.

**Required Additions:**
- [ ] **Egger's regression test** (Egger et al., 1997) - weighted linear regression of effect vs SE
- [ ] **Begg-Mazumdar test** (Begg & Mazumdar, 1994) - rank correlation test
- [ ] **Trim-and-Fill** (Duval & Tweedie, 2000) - imputation-based correction
- [ ] **PET-PEESE** (Stanley & Doucouliagos, 2014) - precision-effect tests
- [ ] **Selection Models** (Vevea & Hedges, 1995; Copas selection model)

**References:**
- Egger M, et al. BMJ 1997;315:629-634
- Stanley TD, Doucouliagos H. Res Synth Methods 2014;5:33-50

### 1.2 Inconsistency Assessment (HIGH PRIORITY)

**Current State:** Node-splitting is listed but NOT implemented.

**Required Additions:**
- [ ] **Node-splitting** (Dias et al., 2010) - comparison of direct vs indirect evidence
- [ ] **Loop-specific inconsistency** - assessment within closed loops
- [ ] **Global inconsistency test** - design-by-treatment interaction

**References:**
- Dias S, et al. Stat Med 2010;29:932-944
- White IR, et al. BMC Med Res Methodol 2012;12:175

### 1.3 Component NMA (MEDIUM PRIORITY)

**Current State:** Listed as feature but NOT implemented.

**Required Addition:**
- [ ] **Additive CNMA** (Rücker et al., 2020) - decomposition of multi-component interventions

**References:**
- Rücker G, et al. Biom J 2020;62:808-821

---

## 2. METHODOLOGICAL ENHANCEMENTS

### 2.1 Small-Study Effects

Current implementation lacks corrections for:
- [ ] **Peters' test** - alternative to Egger for binary outcomes
- [ ] **Harbord's test** - score-based test for ORs
- [ ] **Rücker's limit meta-analysis** - shrinkage estimation

### 2.2 Robust Variance Estimation

For handling correlated effect sizes:
- [ ] **Robust cluster variance** (Hedges et al., 2010)
- [ ] **Three-level meta-analysis** - for dependent effects

### 2.3 Network-Specific Methods

- [ ] **Net-splitting** - enhanced loop decomposition
- [ ] **Side-splitting** - treatment vs comparator separation
- [ ] **Flow decomposition** - evidence flow visualization

---

## 3. REPORTING STANDARDS

### 3.1 PRISMA-NMA Compliance

**Missing:** PRISMA-NMA extension checklist generator

Required items:
- [ ] Geometry of network description
- [ ] Assessment of transitivity assumption
- [ ] Presentation of all pairwise comparisons
- [ ] Ranking with uncertainty
- [ ] Inconsistency assessment results

### 3.2 GRADE-NMA

Current CINeMA implementation should be verified for:
- [ ] Within-study bias domain
- [ ] Across-study bias (reporting bias) domain
- [ ] Indirectness domain
- [ ] Imprecision with threshold considerations
- [ ] Heterogeneity domain
- [ ] Incoherence domain

---

## 4. RECOMMENDED IMPLEMENTATION PRIORITY

### Phase 1 (Critical - Immediate)
1. Egger's test for funnel plot asymmetry
2. Begg's rank correlation test
3. Trim-and-Fill algorithm
4. Node-splitting for inconsistency

### Phase 2 (Important - Short-term)
5. PET-PEESE regression
6. Selection models (3-parameter)
7. Component NMA (additive model)
8. PRISMA-NMA checklist

### Phase 3 (Enhancement - Medium-term)
9. Robust variance estimation
10. Three-level meta-analysis
11. Peters/Harbord tests
12. Advanced flow visualization

---

## 5. VALIDATION REQUIREMENTS

Before publication claims, the following validations are required:

1. **Numerical accuracy** - Compare all estimators against R metafor/netmeta to 4 decimal places
2. **Confidence interval coverage** - Simulation studies for CI calibration
3. **Edge cases** - Single-study comparisons, sparse networks, zero cells
4. **Reproducibility** - Same input should produce identical output

---

## 6. RECOMMENDATIONS

### For Software Development:
1. **Implement missing publication bias methods** - These are claimed but not present
2. **Add node-splitting** - Essential for NMA inconsistency assessment
3. **Validate against R packages** - Provide comparison test suite
4. **Add PRISMA-NMA export** - Required for systematic review publications

### For Documentation:
1. Clearly distinguish implemented vs planned features
2. Provide statistical methodology references
3. Document numerical algorithms used
4. Include validation test results

---

## CONCLUSION

NMA Pro v6.2 has excellent potential but requires immediate implementation of:
1. Publication bias methods (Egger, Begg, Trim-Fill, PET-PEESE)
2. Node-splitting for inconsistency
3. Component NMA

These are **essential features** for any serious NMA software and their absence undermines claims of superiority over R packages.

**Recommendation:** Address Phase 1 critical gaps before any publication or distribution claims.

---

*Review conducted according to Research Synthesis Methods editorial standards*
