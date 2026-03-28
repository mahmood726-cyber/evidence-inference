# ============================================================================
# NMA Pro v6.2 - Comprehensive R Validation
# Validates JavaScript implementations against R packages
# ============================================================================

# Install required packages if needed
required_packages <- c("metafor", "netmeta", "meta", "jsonlite")
for (pkg in required_packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    install.packages(pkg, repos = "https://cloud.r-project.org", quiet = TRUE)
    library(pkg, character.only = TRUE)
  }
}

cat("="," NMA PRO v6.2 - R VALIDATION ", "=", "\n", sep = paste(rep("=", 25), collapse = ""))
cat("\n")

# ============================================================================
# TEST DATA (same as JavaScript tests)
# ============================================================================
test_effects <- c(0.5, 0.3, 0.8, 0.2, 0.6, 0.4, 0.7, 0.35, 0.55, 0.45)
test_ses <- c(0.1, 0.15, 0.2, 0.12, 0.18, 0.14, 0.22, 0.11, 0.16, 0.13)
test_labels <- paste0("S", 1:10)

# Binary data for small study tests
binary_data <- data.frame(
  e1 = c(20, 30, 12, 25, 18),
  n1 = c(100, 150, 80, 120, 90),
  e2 = c(15, 22, 8, 18, 12),
  n2 = c(100, 150, 80, 120, 90)
)

results <- list()

# ============================================================================
# 1. BASIC STATISTICS
# ============================================================================
cat("\n[1] BASIC STATISTICS\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

# Mean
r_mean <- mean(c(1, 2, 3, 4, 5))
results$stats_mean <- list(r_value = r_mean, expected = 3)
cat(sprintf("  Mean([1,2,3,4,5]): R = %.6f\n", r_mean))

# Standard Deviation
r_sd <- sd(c(1, 2, 3, 4, 5))
results$stats_sd <- list(r_value = r_sd, expected = sqrt(2.5))
cat(sprintf("  SD([1,2,3,4,5]): R = %.6f\n", r_sd))

# Normal CDF
r_pnorm <- pnorm(1.96)
results$stats_pnorm <- list(r_value = r_pnorm, expected = 0.975)
cat(sprintf("  pnorm(1.96): R = %.6f\n", r_pnorm))

# Normal Quantile
r_qnorm <- qnorm(0.975)
results$stats_qnorm <- list(r_value = r_qnorm, expected = 1.96)
cat(sprintf("  qnorm(0.975): R = %.6f\n", r_qnorm))

# Chi-square CDF
r_pchisq <- pchisq(3.84, 1)
results$stats_pchisq <- list(r_value = r_pchisq, expected = 0.95)
cat(sprintf("  pchisq(3.84, df=1): R = %.6f\n", r_pchisq))

# t CDF
r_pt <- pt(2.0, 10)
results$stats_pt <- list(r_value = r_pt, expected = 0.963)
cat(sprintf("  pt(2.0, df=10): R = %.6f\n", r_pt))

# ============================================================================
# 2. META-ANALYSIS (metafor)
# ============================================================================
cat("\n[2] META-ANALYSIS (metafor)\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

# Random effects meta-analysis
ma_re <- rma(yi = test_effects, sei = test_ses, method = "REML")
results$meta_pooled <- list(r_value = as.numeric(ma_re$beta), se = as.numeric(ma_re$se))
results$meta_tau2 <- list(r_value = ma_re$tau2)
results$meta_I2 <- list(r_value = ma_re$I2)
results$meta_Q <- list(r_value = ma_re$QE, df = ma_re$k - 1, pval = ma_re$QEp)

cat(sprintf("  Pooled Effect (REML): %.6f (SE: %.6f)\n", ma_re$beta, ma_re$se))
cat(sprintf("  Tau-squared: %.6f\n", ma_re$tau2))
cat(sprintf("  I-squared: %.2f%%\n", ma_re$I2))
cat(sprintf("  Q statistic: %.4f (df=%d, p=%.4f)\n", ma_re$QE, ma_re$k - 1, ma_re$QEp))

# Fixed effects
ma_fe <- rma(yi = test_effects, sei = test_ses, method = "FE")
results$meta_fixed <- list(r_value = as.numeric(ma_fe$beta), se = as.numeric(ma_fe$se))
cat(sprintf("  Fixed Effect: %.6f (SE: %.6f)\n", ma_fe$beta, ma_fe$se))

# ============================================================================
# 3. PUBLICATION BIAS (metafor)
# ============================================================================
cat("\n[3] PUBLICATION BIAS\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

# Egger's test
egger <- regtest(ma_re, model = "lm")
results$egger <- list(
  intercept = egger$est,
  se = egger$se,
  z = egger$zval,
  pvalue = egger$pval
)
cat(sprintf("  Egger's test: z = %.4f, p = %.4f\n", egger$zval, egger$pval))

# Begg's test (rank correlation)
begg <- ranktest(ma_re)
results$begg <- list(
  tau = begg$tau,
  pvalue = begg$pval
)
cat(sprintf("  Begg's test: tau = %.4f, p = %.4f\n", begg$tau, begg$pval))

# Trim and Fill
tf <- trimfill(ma_re)
results$trimfill <- list(
  k0 = tf$k0,
  adjusted_effect = as.numeric(tf$beta),
  adjusted_se = as.numeric(tf$se)
)
cat(sprintf("  Trim-Fill: k0 = %d, adjusted = %.6f\n", tf$k0, tf$beta))

# PET (precision-effect test)
pet <- rma(yi = test_effects, sei = test_ses, mods = ~ test_ses)
results$pet <- list(
  intercept = as.numeric(pet$beta[1]),
  slope = as.numeric(pet$beta[2])
)
cat(sprintf("  PET intercept: %.6f\n", pet$beta[1]))

# PEESE (precision-effect estimate with standard error)
peese <- rma(yi = test_effects, sei = test_ses, mods = ~ I(test_ses^2))
results$peese <- list(
  intercept = as.numeric(peese$beta[1]),
  slope = as.numeric(peese$beta[2])
)
cat(sprintf("  PEESE intercept: %.6f\n", peese$beta[1]))

# ============================================================================
# 4. HETEROGENEITY DIAGNOSTICS
# ============================================================================
cat("\n[4] HETEROGENEITY DIAGNOSTICS\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

# Prediction interval
pi_lower <- ma_re$beta - qt(0.975, ma_re$k - 2) * sqrt(ma_re$tau2 + ma_re$se^2)
pi_upper <- ma_re$beta + qt(0.975, ma_re$k - 2) * sqrt(ma_re$tau2 + ma_re$se^2)
results$prediction_interval <- list(lower = as.numeric(pi_lower), upper = as.numeric(pi_upper))
cat(sprintf("  Prediction Interval: [%.4f, %.4f]\n", pi_lower, pi_upper))

# H statistic
H <- sqrt(ma_re$QE / (ma_re$k - 1))
results$H_statistic <- list(value = H)
cat(sprintf("  H statistic: %.4f\n", H))

# ============================================================================
# 5. INFLUENCE DIAGNOSTICS
# ============================================================================
cat("\n[5] INFLUENCE DIAGNOSTICS (Outlier Detection)\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

# Studentized residuals
inf <- influence(ma_re)
results$studentized_residuals <- list(values = as.numeric(inf$inf$rstudent))
cat(sprintf("  Studentized residuals range: [%.4f, %.4f]\n",
            min(inf$inf$rstudent), max(inf$inf$rstudent)))

# Cook's distance
results$cooks_d <- list(values = as.numeric(inf$inf$cook.d))
cat(sprintf("  Cook's D range: [%.6f, %.6f]\n",
            min(inf$inf$cook.d), max(inf$inf$cook.d)))

# DFBETAS
results$dfbetas <- list(values = as.numeric(inf$inf$dfbs))
cat(sprintf("  DFBETAS range: [%.6f, %.6f]\n",
            min(inf$inf$dfbs), max(inf$inf$dfbs)))

# Leave-one-out
loo <- leave1out(ma_re)
results$leave_one_out <- list(
  estimates = as.numeric(loo$estimate),
  se = as.numeric(loo$se)
)
cat(sprintf("  Leave-one-out estimates range: [%.4f, %.4f]\n",
            min(loo$estimate), max(loo$estimate)))

# ============================================================================
# 6. SMALL STUDY EFFECTS (Binary data)
# ============================================================================
cat("\n[6] SMALL STUDY EFFECTS (Binary Data)\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

# Calculate log OR and SE for binary data
or_data <- escalc(measure = "OR", ai = binary_data$e1, bi = binary_data$n1 - binary_data$e1,
                  ci = binary_data$e2, di = binary_data$n2 - binary_data$e2)
ma_binary <- rma(yi = or_data$yi, vi = or_data$vi)

# Peters' test (for binary outcomes)
peters <- regtest(ma_binary, predictor = "ni", model = "lm")
results$peters <- list(
  z = peters$zval,
  pvalue = peters$pval
)
cat(sprintf("  Peters' test: z = %.4f, p = %.4f\n", peters$zval, peters$pval))

# ============================================================================
# 7. CUMULATIVE META-ANALYSIS
# ============================================================================
cat("\n[7] CUMULATIVE META-ANALYSIS\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

cum <- cumul(ma_re)
results$cumulative <- list(
  estimates = as.numeric(cum$estimate),
  se = as.numeric(cum$se)
)
cat(sprintf("  Cumulative estimates: first = %.4f, last = %.4f\n",
            cum$estimate[1], cum$estimate[length(cum$estimate)]))

# ============================================================================
# 8. NETWORK META-ANALYSIS (netmeta)
# ============================================================================
cat("\n[8] NETWORK META-ANALYSIS (netmeta)\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

# Create NMA data
nma_data <- data.frame(
  study = c("S1", "S2", "S3", "S4", "S5", "S6"),
  treat1 = c("A", "A", "B", "B", "A", "A"),
  treat2 = c("B", "B", "C", "C", "C", "C"),
  TE = c(0.3, 0.4, 0.2, 0.25, 0.5, 0.55),
  seTE = c(0.1, 0.15, 0.12, 0.14, 0.18, 0.2)
)

tryCatch({
  nma <- netmeta(TE = nma_data$TE, seTE = nma_data$seTE,
                 treat1 = nma_data$treat1, treat2 = nma_data$treat2,
                 studlab = nma_data$study, sm = "MD", reference.group = "A")

  results$nma_fixed <- list(
    AB = nma$TE.fixed["A", "B"],
    AC = nma$TE.fixed["A", "C"],
    BC = nma$TE.fixed["B", "C"]
  )
  results$nma_random <- list(
    AB = nma$TE.random["A", "B"],
    AC = nma$TE.random["A", "C"],
    BC = nma$TE.random["B", "C"]
  )
  results$nma_tau2 <- list(value = nma$tau^2)
  results$nma_I2 <- list(value = nma$I2)

  cat(sprintf("  A vs B (random): %.4f\n", nma$TE.random["A", "B"]))
  cat(sprintf("  A vs C (random): %.4f\n", nma$TE.random["A", "C"]))
  cat(sprintf("  B vs C (random): %.4f\n", nma$TE.random["B", "C"]))
  cat(sprintf("  NMA tau-squared: %.6f\n", nma$tau^2))
  cat(sprintf("  NMA I-squared: %.2f%%\n", nma$I2))

  # P-scores
  if (!is.null(nma$P.fixed)) {
    results$p_scores <- list(values = nma$P.random)
    cat(sprintf("  P-scores: A=%.3f, B=%.3f, C=%.3f\n",
                nma$P.random["A"], nma$P.random["B"], nma$P.random["C"]))
  }

}, error = function(e) {
  cat(sprintf("  NMA error: %s\n", e$message))
})

# ============================================================================
# 9. NODE-SPLITTING (if available)
# ============================================================================
cat("\n[9] NODE-SPLITTING\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

tryCatch({
  ns <- netsplit(nma)
  results$node_split <- list(
    comparisons = rownames(ns$compare.random),
    direct = ns$direct.random$TE,
    indirect = ns$indirect.random$TE,
    pvalues = ns$compare.random$p
  )
  cat(sprintf("  Node-split comparisons: %d\n", nrow(ns$compare.random)))
  for (i in 1:min(3, nrow(ns$compare.random))) {
    cat(sprintf("    %s: direct=%.4f, indirect=%.4f, p=%.4f\n",
                rownames(ns$compare.random)[i],
                ns$direct.random$TE[i],
                ns$indirect.random$TE[i],
                ns$compare.random$p[i]))
  }
}, error = function(e) {
  cat(sprintf("  Node-split error: %s\n", e$message))
})

# ============================================================================
# 10. SAVE RESULTS AS JSON
# ============================================================================
cat("\n[10] SAVING RESULTS\n")
cat(paste(rep("-", 50), collapse = ""), "\n")

# Add metadata
results$metadata <- list(
  generated = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
  r_version = R.version.string,
  packages = list(
    metafor = as.character(packageVersion("metafor")),
    netmeta = as.character(packageVersion("netmeta")),
    meta = as.character(packageVersion("meta"))
  )
)

# Save to JSON
json_output <- toJSON(results, pretty = TRUE, auto_unbox = TRUE)
writeLines(json_output, "C:/Users/user/r_validation_results.json")
cat("  Results saved to: C:/Users/user/r_validation_results.json\n")

cat("\n")
cat(paste(rep("=", 60), collapse = ""), "\n")
cat("R VALIDATION COMPLETE\n")
cat(paste(rep("=", 60), collapse = ""), "\n")
