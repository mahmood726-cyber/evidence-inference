# Validate Critical Gap Functions Against R metafor
library(metafor)

cat("=" , rep("=", 69), "\n", sep="")
cat("VALIDATION: TruthCert vs R metafor - Critical Gap Functions\n")
cat("=", rep("=", 69), "\n\n", sep="")

# BCG vaccine data for testing
dat <- escalc(measure="OR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

cat("Test Data: BCG Vaccine Trials (dat.bcg)\n")
cat("Studies: k =", nrow(dat), "\n\n")

# ============================================
# 1. MANTEL-HAENSZEL METHOD
# ============================================
cat("--- 1. MANTEL-HAENSZEL METHOD ---\n\n")

mh <- rma.mh(measure="OR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

cat("R metafor (rma.mh):\n")
cat("  OR =", exp(mh$beta), "\n")
cat("  logOR =", as.numeric(mh$beta), "\n")
cat("  SE =", as.numeric(mh$se), "\n")
cat("  95% CI: [", exp(mh$ci.lb), ",", exp(mh$ci.ub), "]\n")
cat("  Q =", mh$QE, ", p =", mh$QEp, "\n\n")

cat("REFERENCE VALUES FOR JS:\n")
cat("  MH_OR:", exp(mh$beta), "\n")
cat("  MH_logOR:", as.numeric(mh$beta), "\n")
cat("  MH_SE:", as.numeric(mh$se), "\n\n")

# ============================================
# 2. PETO METHOD
# ============================================
cat("--- 2. PETO METHOD ---\n\n")

peto <- rma.peto(ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

cat("R metafor (rma.peto):\n")
cat("  OR =", exp(peto$beta), "\n")
cat("  logOR =", as.numeric(peto$beta), "\n")
cat("  SE =", as.numeric(peto$se), "\n")
cat("  95% CI: [", exp(peto$ci.lb), ",", exp(peto$ci.ub), "]\n\n")

cat("REFERENCE VALUES FOR JS:\n")
cat("  PETO_OR:", exp(peto$beta), "\n")
cat("  PETO_logOR:", as.numeric(peto$beta), "\n")
cat("  PETO_SE:", as.numeric(peto$se), "\n\n")

# ============================================
# 3. COOK'S DISTANCE / INFLUENCE
# ============================================
cat("--- 3. COOK'S DISTANCE ---\n\n")

# Fit RE model
fit <- rma(yi, vi, data=dat, method="REML")
inf <- influence(fit)

cat("R metafor influence():\n")
cat("  Cook's D values:\n")
for(i in 1:nrow(dat)) {
  cat("    Study", i, ":", round(inf$inf$cook.d[i], 4), "\n")
}
cat("\n  Max Cook's D:", max(inf$inf$cook.d), "\n")
cat("  Study with max:", which.max(inf$inf$cook.d), "\n\n")

cat("REFERENCE VALUES FOR JS:\n")
cat("  cooksd:", paste(round(inf$inf$cook.d, 6), collapse=", "), "\n\n")

# ============================================
# 4. TEST OF EXCESS SIGNIFICANCE (TES)
# ============================================
cat("--- 4. TEST OF EXCESS SIGNIFICANCE (TES) ---\n\n")

tes_result <- tes(yi, vi, data=dat)

cat("R metafor tes():\n")
cat("  Observed significant:", tes_result$O, "\n")
cat("  Expected significant:", round(tes_result$E, 2), "\n")
cat("  Ratio O/E:", round(tes_result$O / tes_result$E, 2), "\n")
cat("  Chi-square:", round(tes_result$X2, 3), "\n")
cat("  p-value:", round(tes_result$pval, 4), "\n\n")

cat("REFERENCE VALUES FOR JS:\n")
cat("  TES_observed:", tes_result$O, "\n")
cat("  TES_expected:", round(tes_result$E, 4), "\n")
cat("  TES_chi2:", round(tes_result$X2, 4), "\n")
cat("  TES_pvalue:", round(tes_result$pval, 4), "\n\n")

# ============================================
# 5. STANDARDIZED RESIDUALS (for QQ Plot)
# ============================================
cat("--- 5. STANDARDIZED RESIDUALS ---\n\n")

# Get standardized residuals from metafor
rstd <- rstandard(fit)

cat("R metafor rstandard():\n")
cat("  Standardized residuals:\n")
for(i in 1:nrow(dat)) {
  cat("    Study", i, ":", round(rstd$z[i], 4), "\n")
}

cat("\nREFERENCE VALUES FOR JS:\n")
cat("  residuals:", paste(round(rstd$z, 6), collapse=", "), "\n\n")

# Shapiro-Wilk test on residuals
sw <- shapiro.test(rstd$z)
cat("Shapiro-Wilk test:\n")
cat("  W =", sw$statistic, "\n")
cat("  p =", sw$p.value, "\n\n")

# ============================================
# SUMMARY OUTPUT FOR SELENIUM VALIDATION
# ============================================
cat("=", rep("=", 69), "\n", sep="")
cat("SUMMARY: Reference Values for Selenium Validation\n")
cat("=", rep("=", 69), "\n\n", sep="")

cat("const R_REFERENCE = {\n")
cat("  mantelHaenszel: {\n")
cat("    OR:", exp(mh$beta), ",\n")
cat("    logOR:", as.numeric(mh$beta), ",\n")
cat("    se:", as.numeric(mh$se), "\n")
cat("  },\n")
cat("  peto: {\n")
cat("    OR:", exp(peto$beta), ",\n")
cat("    logOR:", as.numeric(peto$beta), ",\n")
cat("    se:", as.numeric(peto$se), "\n")
cat("  },\n")
cat("  tes: {\n")
cat("    observed:", tes_result$O, ",\n")
cat("    expected:", round(tes_result$E, 2), ",\n")
cat("    chi2:", round(tes_result$X2, 3), ",\n")
cat("    pvalue:", round(tes_result$pval, 4), "\n")
cat("  },\n")
cat("  cooksD: [", paste(round(inf$inf$cook.d, 6), collapse=", "), "],\n")
cat("  residuals: [", paste(round(rstd$z, 6), collapse=", "), "]\n")
cat("};\n")
