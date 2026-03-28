# MAFI v2.1.0 Minimal Validation
library(MAFI)

cat("MAFI v2.1.0 MINIMAL SIMULATION VALIDATION\n")
cat("==========================================\n\n")

# Very small simulation: 5 sims x 2 k x 3 bias = 30 total
set.seed(42)
results <- data.frame()

for (k in c(10, 20)) {
  for (bias in c(0, 0.5, 1.0)) {
    for (i in 1:5) {
      dat <- tryCatch({
        simulate_biased_ma(k = k, theta = 0.3, tau = 0.1, bias_strength = bias)
      }, error = function(e) NULL)

      if (is.null(dat)) next

      mafi_result <- tryCatch({
        mafi(dat$yi, dat$vi)
      }, error = function(e) NULL)

      if (is.null(mafi_result)) next

      results <- rbind(results, data.frame(
        k = k,
        true_bias = bias,
        mafi_score = mafi_result$score,
        original = mafi_result$original,
        corrected = mafi_result$corrected,
        true_theta = dat$true_theta[1]
      ))
    }
  }
}

cat("Completed", nrow(results), "simulations\n\n")

# Calculate metrics
if (nrow(results) > 0) {
  # AUC (binary: bias > 0.25)
  results$bias_binary <- as.numeric(results$true_bias > 0.25)
  pos <- results$mafi_score[results$bias_binary == 1]
  neg <- results$mafi_score[results$bias_binary == 0]
  auc <- mean(outer(pos, neg, ">")) + 0.5 * mean(outer(pos, neg, "=="))

  # RMSE
  rmse <- sqrt(mean((results$mafi_score/100 - results$true_bias)^2))

  # Correction effectiveness
  results$naive_bias <- results$original - results$true_theta
  results$corr_bias <- results$corrected - results$true_theta
  correction_eff <- mean(abs(results$naive_bias) > abs(results$corr_bias), na.rm = TRUE)

  cat("METRICS:\n")
  cat("  AUC:", round(auc, 3), "\n")
  cat("  RMSE:", round(rmse, 3), "\n")
  cat("  Correction effectiveness:", round(correction_eff * 100, 1), "%\n\n")

  # Calibration
  cat("SCORE BY TRUE BIAS LEVEL:\n")
  agg <- aggregate(mafi_score ~ true_bias, data = results, FUN = mean)
  print(agg)
}

cat("\nDone.\n")
