#!/usr/bin/env Rscript
# =============================================================================
# R Validation Script for TruthCert-PairwisePro
# Generates reference values using metafor package
# =============================================================================

cat("======================================================================\n")
cat("TruthCert-PairwisePro R Validation Script\n")
cat("======================================================================\n\n")

# Load packages
suppressPackageStartupMessages({
  library(metafor)
  library(jsonlite)
})

cat("metafor version:", as.character(packageVersion("metafor")), "\n\n")

# =============================================================================
# BCG Vaccine Dataset (dat.bcg from metafor)
# =============================================================================
cat("======================================================================\n")
cat("DATASET: BCG Vaccine Trials (dat.bcg)\n")
cat("======================================================================\n\n")

data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

cat("Studies:", nrow(dat), "\n")
cat("\nEffect sizes (yi) and variances (vi):\n")
print(data.frame(
  study = dat.bcg$author,
  yi = round(dat$yi, 6),
  vi = round(dat$vi, 6)
))

# =============================================================================
# Tau-squared Estimators
# =============================================================================
cat("\n======================================================================\n")
cat("TAU-SQUARED ESTIMATORS\n")
cat("======================================================================\n\n")

methods <- c("DL", "REML", "ML", "PM", "HS", "SJ", "HE", "EB")
tau2_results <- list()

for (m in methods) {
  fit <- rma(yi, vi, data=dat, method=m)
  tau2_results[[m]] <- list(
    tau2 = fit$tau2,
    se_tau2 = fit$se.tau2,
    I2 = fit$I2,
    H2 = fit$H2,
    QE = fit$QE,
    QEp = fit$QEp
  )
  cat(sprintf("%-6s tau2 = %.6f  (I2 = %.2f%%)\n", m, fit$tau2, fit$I2))
}

# =============================================================================
# Pooled Estimates with Different Methods
# =============================================================================
cat("\n======================================================================\n")
cat("POOLED ESTIMATES\n")
cat("======================================================================\n\n")

# Standard random-effects (REML)
fit_reml <- rma(yi, vi, data=dat, method="REML")
cat("REML Pooled:\n")
cat(sprintf("  theta = %.6f\n", fit_reml$b[1]))
cat(sprintf("  SE = %.6f\n", fit_reml$se))
cat(sprintf("  95%% CI = [%.6f, %.6f]\n", fit_reml$ci.lb, fit_reml$ci.ub))
cat(sprintf("  z = %.6f, p = %.6f\n", fit_reml$zval, fit_reml$pval))

# HKSJ adjustment
fit_hksj <- rma(yi, vi, data=dat, method="REML", test="knha")
cat("\nHKSJ Adjusted (Knapp-Hartung):\n")
cat(sprintf("  theta = %.6f\n", fit_hksj$b[1]))
cat(sprintf("  SE = %.6f\n", fit_hksj$se))
cat(sprintf("  95%% CI = [%.6f, %.6f]\n", fit_hksj$ci.lb, fit_hksj$ci.ub))
cat(sprintf("  t = %.6f, df = %d, p = %.6f\n", fit_hksj$tval, fit_hksj$dfs, fit_hksj$pval))

# Fixed-effect
fit_fe <- rma(yi, vi, data=dat, method="FE")
cat("\nFixed-Effect:\n")
cat(sprintf("  theta = %.6f\n", fit_fe$b[1]))
cat(sprintf("  SE = %.6f\n", fit_fe$se))
cat(sprintf("  95%% CI = [%.6f, %.6f]\n", fit_fe$ci.lb, fit_fe$ci.ub))

# =============================================================================
# Heterogeneity Statistics
# =============================================================================
cat("\n======================================================================\n")
cat("HETEROGENEITY STATISTICS\n")
cat("======================================================================\n\n")

cat(sprintf("Q = %.6f (df = %d, p = %.6f)\n", fit_reml$QE, fit_reml$k - 1, fit_reml$QEp))
cat(sprintf("I2 = %.2f%%\n", fit_reml$I2))
cat(sprintf("H2 = %.4f\n", fit_reml$H2))
cat(sprintf("tau2 = %.6f\n", fit_reml$tau2))
cat(sprintf("tau = %.6f\n", sqrt(fit_reml$tau2)))

# Prediction interval
pred <- predict(fit_reml)
cat(sprintf("\nPrediction Interval: [%.6f, %.6f]\n", pred$pi.lb, pred$pi.ub))

# =============================================================================
# Publication Bias Tests
# =============================================================================
cat("\n======================================================================\n")
cat("PUBLICATION BIAS TESTS\n")
cat("======================================================================\n\n")

# Egger's test
egger <- regtest(fit_reml, model="lm")
cat("Egger's Regression Test:\n")
cat(sprintf("  intercept = %.6f\n", egger$est))
cat(sprintf("  se = %.6f\n", egger$se))
cat(sprintf("  t = %.6f, p = %.6f\n", egger$zval, egger$pval))

# Begg's test (rank correlation)
begg <- ranktest(fit_reml)
cat("\nBegg's Rank Correlation Test:\n")
cat(sprintf("  tau = %.6f, p = %.6f\n", begg$tau, begg$pval))

# Fail-safe N
fsn_result <- fsn(yi, vi, data=dat)
cat("\nFail-Safe N (Rosenthal):\n")
cat(sprintf("  N = %d\n", fsn_result$fsnum))

# Trim and Fill
tf <- trimfill(fit_reml)
cat("\nTrim and Fill:\n")
cat(sprintf("  Studies imputed: %d (side = %s)\n", tf$k0, tf$side))
cat(sprintf("  Adjusted theta = %.6f\n", tf$b[1]))
cat(sprintf("  Adjusted 95%% CI = [%.6f, %.6f]\n", tf$ci.lb, tf$ci.ub))

# =============================================================================
# Leave-One-Out Analysis
# =============================================================================
cat("\n======================================================================\n")
cat("LEAVE-ONE-OUT ANALYSIS\n")
cat("======================================================================\n\n")

l1o <- leave1out(fit_reml)
cat("Estimates when each study is removed:\n")
for (i in 1:nrow(dat)) {
  cat(sprintf("  Study %d: theta = %.6f, I2 = %.2f%%\n", i, l1o$estimate[i], l1o$I2[i]))
}

# =============================================================================
# Influence Diagnostics
# =============================================================================
cat("\n======================================================================\n")
cat("INFLUENCE DIAGNOSTICS\n")
cat("======================================================================\n\n")

inf <- influence(fit_reml)
cat("Hat values (leverage) and Cook's distance:\n")
for (i in 1:nrow(dat)) {
  cat(sprintf("  Study %d: hat = %.6f, Cook's D = %.6f\n", i, inf$inf$hat[i], inf$inf$cook.d[i]))
}

# =============================================================================
# Model Fit Statistics
# =============================================================================
cat("\n======================================================================\n")
cat("MODEL FIT STATISTICS\n")
cat("======================================================================\n\n")

cat("Random-Effects (REML):\n")
cat(sprintf("  Log-Likelihood = %.6f\n", fit_reml$fit.stats$REML[1]))
cat(sprintf("  Deviance = %.6f\n", fit_reml$fit.stats$REML[2]))
cat(sprintf("  AIC = %.6f\n", fit_reml$fit.stats$REML[3]))
cat(sprintf("  BIC = %.6f\n", fit_reml$fit.stats$REML[4]))
cat(sprintf("  AICc = %.6f\n", fit_reml$fit.stats$REML[5]))

# =============================================================================
# JSON Output for Comparison
# =============================================================================
cat("\n======================================================================\n")
cat("SAVING JSON REFERENCE VALUES\n")
cat("======================================================================\n\n")

# Create reference object
reference <- list(
  dataset = "BCG Vaccine (dat.bcg)",
  k = nrow(dat),
  yi = as.numeric(dat$yi),
  vi = as.numeric(dat$vi),

  tau2 = list(
    DL = tau2_results$DL$tau2,
    REML = tau2_results$REML$tau2,
    ML = tau2_results$ML$tau2,
    PM = tau2_results$PM$tau2,
    HS = tau2_results$HS$tau2,
    SJ = tau2_results$SJ$tau2,
    HE = tau2_results$HE$tau2,
    EB = tau2_results$EB$tau2
  ),

  pooled = list(
    theta = as.numeric(fit_reml$b),
    se = fit_reml$se,
    ci_lower = fit_reml$ci.lb,
    ci_upper = fit_reml$ci.ub,
    z = fit_reml$zval,
    p = fit_reml$pval
  ),

  hksj = list(
    theta = as.numeric(fit_hksj$b),
    se = fit_hksj$se,
    ci_lower = fit_hksj$ci.lb,
    ci_upper = fit_hksj$ci.ub,
    t = fit_hksj$tval,
    df = fit_hksj$dfs,
    p = fit_hksj$pval
  ),

  heterogeneity = list(
    Q = fit_reml$QE,
    Q_df = fit_reml$k - 1,
    Q_p = fit_reml$QEp,
    I2 = fit_reml$I2,
    H2 = fit_reml$H2,
    tau2 = fit_reml$tau2,
    tau = sqrt(fit_reml$tau2)
  ),

  prediction = list(
    pi_lower = pred$pi.lb,
    pi_upper = pred$pi.ub
  ),

  egger = list(
    intercept = egger$est,
    se = egger$se,
    t = egger$zval,
    p = egger$pval
  ),

  begg = list(
    tau = begg$tau,
    p = begg$pval
  ),

  failsafe_n = fsn_result$fsnum,

  trim_fill = list(
    k0 = tf$k0,
    side = tf$side,
    theta = as.numeric(tf$b),
    ci_lower = tf$ci.lb,
    ci_upper = tf$ci.ub
  ),

  leave1out = lapply(1:nrow(dat), function(i) list(
    theta = l1o$estimate[i],
    se = l1o$se[i],
    I2 = l1o$I2[i]
  )),

  influence = lapply(1:nrow(dat), function(i) list(
    hat = inf$inf$hat[i],
    cooks_d = inf$inf$cook.d[i]
  ))
)

# Output JSON
json_output <- toJSON(reference, pretty = TRUE, auto_unbox = TRUE)

# Save to file
writeLines(json_output, "C:/Users/user/r_validation_reference.json")
cat("Saved to: C:/Users/user/r_validation_reference.json\n")

cat("\n======================================================================\n")
cat("VALIDATION COMPLETE\n")
cat("======================================================================\n")
