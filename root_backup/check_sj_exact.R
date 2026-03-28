# Exact SJ formula analysis
library(metafor)
data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- dat$yi
vi <- dat$vi
k <- length(yi)

cat("=== SIDIK-JONKMAN EXACT FORMULA ===\n\n")

# Metafor SJ result
res_sj <- rma(yi, vi, method="SJ")
cat("Metafor SJ tau2:", res_sj$tau2, "\n\n")

# SJ uses an iterative approach similar to REML
# The original Sidik-Jonkman (2005) paper describes:
# Step 1: tau2_0 = max(0, (1/(k-1)) * sum((yi - ybar)^2) - (1/k) * sum(vi))
# Step 2: wi = 1/(vi + tau2_0), then apply DL formula

mean_y <- mean(yi)
s2 <- var(yi)  # This is sum((yi - mean_y)^2) / (k-1)
v_bar <- mean(vi)
tau2_0 <- max(0, s2 - v_bar)
cat("Step 1 - tau2_0 = s2 - v_bar:", tau2_0, "\n")

# Step 2 with DL-style calculation
wi_1 <- 1 / (vi + tau2_0)
sumW_1 <- sum(wi_1)
sumW2_1 <- sum(wi_1^2)
theta_1 <- sum(wi_1 * yi) / sumW_1
Q_1 <- sum(wi_1 * (yi - theta_1)^2)
C_1 <- sumW_1 - sumW2_1 / sumW_1

cat("\nStep 2 components:\n")
cat("  sum(wi_1):", sumW_1, "\n")
cat("  theta_1:", theta_1, "\n")
cat("  Q_1:", Q_1, "\n")
cat("  C_1:", C_1, "\n")
cat("  (Q_1 - (k-1)) / C_1:", (Q_1 - (k-1)) / C_1, "\n")

# Actually metafor SJ might use a different approach
# Let me try the paper's exact formula
# The corrected SJ estimator from the 2007 correction

# Alternative: Weighted residual sum of squares divided by df
# tau2 = (1/df) * sum(wi * (yi - theta)^2 / (1 + wi * tau2))
# This requires iteration

cat("\n=== TRYING ALTERNATIVE SJ FORMULAS ===\n")

# Formula from Sidik & Jonkman (2005) corrected:
# tau2 = (Q - (k-1)) / C where Q and C use weights 1/(vi + tau2_0)
# But we need to check if they use a different initialization

# Maybe SJ uses tau2_0 directly without step 2?
cat("\nJust tau2_0 (no step 2):", tau2_0, "\n")

# Or maybe SJ uses different weights in step 2
# Trying: wi = 1/vi (fixed effect weights) for step 2
wi_fe <- 1/vi
sumW_fe <- sum(wi_fe)
sumW2_fe <- sum(wi_fe^2)
theta_fe <- sum(wi_fe * yi) / sumW_fe
Q_fe <- sum(wi_fe * (yi - theta_fe)^2)

# Then adjust with tau2_0
# tau2_SJ = (Q - (k-1)) / (sum(wi^2)/sum(wi))
tau2_sj_alt <- Q_fe / (k-1)
cat("Q / (k-1):", tau2_sj_alt, "\n")

# Another try: The paper formula for tau2_1
# tau2_1 = (k / (k-1)) * tau2_0
tau2_sj_scaled <- (k / (k-1)) * tau2_0
cat("(k/(k-1)) * tau2_0:", tau2_sj_scaled, "\n")

# Check SJ2 as well (alternative SJ estimator in metafor)
res_sj2 <- rma(yi, vi, method="SJ2")
cat("\nMetafor SJ2 tau2:", res_sj2$tau2, "\n")
