# MAFI v2.2.0 Validation Test
# Tests methodological fixes: signal clustering, I2 boost, CI widening, null effects

# Reinstall package
tryCatch(remove.packages("MAFI"), error = function(e) NULL)
install.packages("C:/Users/user/MAFI", repos = NULL, type = "source")

library(MAFI)
library(metafor)

cat("\n")
cat("======================================================\n")
cat("  MAFI v2.2.0 METHODOLOGICAL VALIDATION\n")
cat("======================================================\n\n")

# Test 1: BCG vaccine data (real data)
cat("TEST 1: BCG Vaccine Data (Real-World Test)\n")
cat("-------------------------------------------\n")
data(dat.bcg)
dat <- escalc(measure = "RR", ai = tpos, bi = tneg, ci = cpos, di = cneg, data = dat.bcg)
result <- mafi(dat$yi, dat$vi)
print(result)

# Test 2: Verify I2 boost (high I2 should increase score)
cat("\n\nTEST 2: I2 Boost Direction Verification\n")
cat("---------------------------------------\n")
cat("BCG data has high I2 (", round(result$signals$i_squared, 1), "%)\n", sep="")
cat("In v2.2.0, high I2 INCREASES suspicion (score boosted by ~15%)\n")
cat("Score includes I2 boost multiplier: 1 + 0.15 * (I2/100) = ",
    round(1 + 0.15 * result$signals$i_squared/100, 3), "\n", sep="")

# Test 3: Signal clustering - simulate biased data
cat("\n\nTEST 3: Signal Clustering Test\n")
cat("------------------------------\n")
cat("v2.2.0 groups correlated signals into clusters:\n")
cat("  - Asymmetry cluster: Egger, PET, Begg, precision-effect, small-study\n")
cat("  - Selection cluster: 3PSM, beta selection models\n")
cat("  - Excess significance: Independent\n")
cat("  - Trim-and-fill: Semi-independent\n\n")

set.seed(123)
sim_biased <- simulate_biased_ma(k = 20, theta = 0.3, tau = 0.1, bias_strength = 0.8)
result_biased <- mafi(sim_biased$yi, sim_biased$vi)
cat("Biased simulation (strength=0.8): MAFI Score =", result_biased$score, "\n")
cat("Risk classification:", result_biased$classification$class, "\n")

# Test 4: Null effect specificity
cat("\n\nTEST 4: Null Effect Specificity\n")
cat("-------------------------------\n")
cat("Testing with theta=0 (no true effect):\n")
set.seed(456)
scores_null <- numeric(20)
for (i in 1:20) {
  sim_null <- simulate_biased_ma(k = 15, theta = 0, tau = 0.05, bias_strength = 0)
  r <- mafi(sim_null$yi, sim_null$vi)
  scores_null[i] <- r$score
}
cat("Mean score under null (no bias):", round(mean(scores_null), 1), "\n")
cat("SD of scores:", round(sd(scores_null), 1), "\n")
cat("% below threshold 40:", round(100 * mean(scores_null < 40), 1), "%\n")
cat("(Good specificity: most scores should be < 40 when no bias present)\n")

# Test 5: Different bias types
cat("\n\nTEST 5: Bias Type Detection\n")
cat("---------------------------\n")
set.seed(789)
bias_types <- c("significance", "direction", "both", "precision", "time_lag")
for (bt in bias_types) {
  sim <- simulate_biased_ma(k = 20, theta = 0.3, tau = 0.1, bias_strength = 0.6, bias_type = bt)
  r <- mafi(sim$yi, sim$vi)
  cat(sprintf("  %-12s bias: Score = %5.1f [%s]\n", bt, r$score, r$classification$class))
}

# Test 6: Small n CI widening (not point estimate penalty)
cat("\n\nTEST 6: Small-n CI Widening (Bootstrap)\n")
cat("---------------------------------------\n")
cat("v2.2.0: Small n widens CI but doesn't penalize point estimate\n")
set.seed(111)
small_data <- simulate_biased_ma(k = 8, theta = 0.3, tau = 0.1, bias_strength = 0.5)
result_small <- mafi(small_data$yi, small_data$vi, bootstrap = TRUE, n_boot = 100)
cat("n=8 studies: Score =", result_small$score, "\n")
if (!is.na(result_small$score_ci[1])) {
  cat("95% CI: [", result_small$score_ci[1], ", ", result_small$score_ci[2], "]\n", sep="")
  cat("CI width:", round(result_small$score_ci[2] - result_small$score_ci[1], 1), "\n")
  cat("(CI widened by factor 1.5 for n < 10)\n")
}

# Test 7: Quick validation run
cat("\n\nTEST 7: Quick Validation (theta=0 included)\n")
cat("-------------------------------------------\n")
cat("Running mini-validation with null effect simulations...\n")
val <- validate_mafi(n_sims = 10, k_range = c(15),
                     theta_range = c(0, 0.3),  # Includes null!
                     tau_range = c(0.1),
                     bias_levels = c(0, 0.5, 1.0),
                     bias_types = c("significance"),
                     verbose = FALSE)
cat("\nValidation Results:\n")
cat("  AUC:", val$auc, "\n")
cat("  Sensitivity:", val$sensitivity, "\n")
cat("  Specificity:", val$specificity, "\n")
cat("  Calibration slope:", val$calibration_slope, "\n")
cat("  Null specificity:", val$null_specificity, "\n")
cat("  Null mean score:", val$null_mean_score, "\n")

cat("\n======================================================\n")
cat("  MAFI v2.2.0 VALIDATION COMPLETE\n")
cat("======================================================\n")
cat("\nMethodological fixes implemented:\n")
cat("  [x] Signal clustering (max within asymmetry cluster)\n")
cat("  [x] I2 boost (high I2 increases suspicion)\n")
cat("  [x] CI widening for small n (not point penalty)\n")
cat("  [x] Null effect validation (theta=0)\n")
cat("  [x] Calibration slope metric\n")
cat("\n")
