# MAFI v2.1.1 Validation
tryCatch(remove.packages("MAFI"), error = function(e) NULL)
install.packages("C:/Users/user/MAFI", repos = NULL, type = "source")

library(MAFI)
library(metafor)

cat("=== MAFI v2.1.1 Test ===\n\n")

# Test 1: BCG data
cat("Test 1: BCG Data\n")
data(dat.bcg)
dat <- escalc(measure = "RR", ai = tpos, bi = tneg, ci = cpos, di = cneg, data = dat.bcg)
result <- mafi(dat$yi, dat$vi)
print(result)

# Test 2: New bias types
cat("\nTest 2: New Bias Types (precision, time_lag)\n")
set.seed(42)
for (bt in c("significance", "direction", "precision", "time_lag")) {
  sim <- simulate_biased_ma(k = 15, theta = 0.3, tau = 0.1, bias_strength = 0.5, bias_type = bt)
  r <- mafi(sim$yi, sim$vi)
  cat(sprintf("  %s bias: Score = %.1f\n", bt, r$score))
}

cat("\n=== MAFI v2.1.1 Validated ===\n")
