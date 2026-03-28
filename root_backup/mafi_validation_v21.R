# MAFI v2.1.0 Validation Script
library(MAFI)
library(metafor)

cat("============================================================\n")
cat("  MAFI v2.1.0 VALIDATION\n")
cat("============================================================\n\n")

# Test 1: Basic functionality with BCG
cat("TEST 1: BCG Data Analysis\n")
cat("------------------------------------------------------------\n")
data(dat.bcg)
dat <- escalc(measure = "RR", ai = tpos, bi = tneg, ci = cpos, di = cneg, data = dat.bcg)
result <- mafi(dat$yi, dat$vi)
print(result)

# Test 2: Check new signals
cat("\nTEST 2: New Signals (Bonferroni, Direction)\n")
cat("------------------------------------------------------------\n")
sig <- result$signals
cat("Selection min p:", round(sig$sel_min_pval, 4), "\n")
cat("Selection Bonferroni-adjusted p:", round(sig$sel_min_pval_adjusted, 4), "\n")
cat("Small study direction:", sig$small_study_direction, "\n")
cat("Small study magnitude:", round(sig$small_study_magnitude, 4), "\n")

# Test 3: Correction methods
cat("\nTEST 3: Correction Methods\n")
cat("------------------------------------------------------------\n")
for (nm in names(result$correction_methods)) {
  cat("  ", nm, ":", round(result$correction_methods[[nm]], 4), "\n")
}

# Test 4: Small simulation (10 sims x 2 k x 3 bias = 60 total)
cat("\nTEST 4: Mini Simulation (60 iterations)\n")
cat("------------------------------------------------------------\n")
val <- tryCatch({
  validate_mafi(n_sims = 10, k_range = c(10, 20),
                bias_levels = c(0, 0.5, 1.0),
                seed = 42, verbose = FALSE)
}, error = function(e) {
  cat("Simulation error:", conditionMessage(e), "\n")
  NULL
})

if (!is.null(val)) {
  cat("AUC:", val$auc, "\n")
  cat("RMSE:", val$rmse, "\n")
  cat("Correction effectiveness:", val$correction_effectiveness * 100, "%\n")
  cat("Successful sims:", val$n_sims_successful, "\n")
  cat("\nCalibration:\n")
  print(val$calibration)
}

# Test 5: Raudenbush data
cat("\nTEST 5: Raudenbush Data (Known Bias)\n")
cat("------------------------------------------------------------\n")
data(dat.raudenbush1985)
dat2 <- escalc(measure = "SMD", yi = yi, vi = vi, data = dat.raudenbush1985)
result2 <- mafi(dat2$yi, dat2$vi)
print(result2)

cat("\n============================================================\n")
cat("  MAFI v2.1.0 VALIDATION COMPLETE\n")
cat("============================================================\n")
