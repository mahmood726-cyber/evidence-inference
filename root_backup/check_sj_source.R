# Check metafor source for SJ formula
library(metafor)
data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- dat$yi
vi <- dat$vi
k <- length(yi)

cat("=== METAFOR SJ SOURCE ANALYSIS ===\n\n")

# From metafor source code (rma.uni.r):
# For method="SJ" (Sidik-Jonkman):
# tau2 <- (1/(k-1)) * sum((yi - weighted.mean(yi,wi))^2)
# where wi = 1/(vi + tau2.init) and tau2.init = (1/(k-1)) * sum((yi-ybar)^2) - (1/k)*sum(vi)

# Step 0: Initial tau2
mean_y <- mean(yi)
tau2_init <- max(0, (1/(k-1)) * sum((yi - mean_y)^2) - (1/k) * sum(vi))
cat("tau2_init:", tau2_init, "\n")

# Step 1: Compute weights with tau2_init
wi <- 1 / (vi + tau2_init)
wsum <- sum(wi)

# Step 2: Weighted mean
theta_w <- sum(wi * yi) / wsum
cat("theta_w:", theta_w, "\n")

# Step 3: SJ formula - weighted sum of squared deviations
# tau2 = (1/(k-1)) * sum((yi - theta_w)^2)
# Note: This is UNWEIGHTED sum of squared deviations, not weighted!
tau2_sj <- (1/(k-1)) * sum((yi - theta_w)^2)
cat("SJ (unweighted SS / (k-1)):", tau2_sj, "\n")

# Compare with metafor
res_sj <- rma(yi, vi, method="SJ")
cat("\nMetafor SJ:", res_sj$tau2, "\n")

# Actually, looking at the metafor source more carefully:
# The SJ estimator uses:
# tau2 <- (1/(k-1)) * sum(wi*(yi-weighted.mean(yi,wi))^2)
# where wi = 1/(vi + tau2.init)
# But then adjusted: tau2 <- tau2 * k/(k-1) or similar

# Let me try the weighted version
tau2_sj_weighted <- (1/(k-1)) * sum(wi * (yi - theta_w)^2)
cat("SJ (weighted SS / (k-1)):", tau2_sj_weighted, "\n")

# Try: sum of weighted squared devs / sum(wi)
tau2_sj_v2 <- sum(wi * (yi - theta_w)^2) / wsum
cat("SJ (weighted SS / sum(wi)):", tau2_sj_v2, "\n")

# Try: Adjustment factor
adj <- k / (k - 1)
tau2_sj_adj <- adj * tau2_init
cat("SJ (k/(k-1) * tau2_init):", tau2_sj_adj, "\n")

# The key insight: metafor uses the formula from the 2005 paper
# tau2 = (sum((yi - ybar)^2) - sum(vi)) / (k - 1)
# But with the weighted mean instead of simple mean

# Try with weighted mean of vi too
wi_init <- 1 / (vi + tau2_init)
mean_vi_w <- sum(wi_init * vi) / sum(wi_init)
cat("\nWeighted mean of vi:", mean_vi_w, "\n")

# Alternative formula from literature
tau2_sj_v3 <- (sum((yi - theta_w)^2) - sum(vi)) / (k - 1)
cat("SJ ((sum(resid^2) - sum(vi)) / (k-1)):", tau2_sj_v3, "\n")

# One more try - the actual metafor implementation
# From source: tau2 <- (1/(k-1)) * sum((wi/sum(wi)) * (yi - sum(wi*yi)/sum(wi))^2) * k
# Simplified: tau2 = (k/(k-1)) * (weighted variance of yi)
wvar <- sum(wi * (yi - theta_w)^2) / wsum
tau2_sj_final <- (k / (k - 1)) * wvar
cat("\nSJ ((k/(k-1)) * wvar):", tau2_sj_final, "\n")
