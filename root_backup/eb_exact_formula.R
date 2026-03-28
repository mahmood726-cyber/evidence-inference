library(metafor)
data(dat.bcg)
d <- escalc(measure='RR', ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)
yi <- d$yi
vi <- d$vi
k <- length(yi)

cat("=== EB EXACT FORMULA FROM METAFOR ===\n\n")

# metafor's EB estimator uses iterative approach similar to PM
# but with the Morris (1983) formula

# The EB estimator finds tau2 such that:
# RSS_w / (k-1) = 1 (weighted residual SS equals expected value)

# Actually, metafor's EB is based on finding tau2 where:
# sum(w_i * (y_i - theta_w)^2) / (k-1) = 1

# Let's trace through metafor manually
res_eb <- rma(yi, vi, method="EB")
cat(sprintf("metafor EB: tau2=%.6f\n", res_eb$tau2))

# The EB estimator iterates to find tau2 where the
# weighted residual variance equals 1
# Similar to PM but with slight differences in the criterion function

# Manual implementation of EB-like formula
# Start with DL
tau2 <- rma(yi, vi, method="DL")$tau2

for(iter in 1:100) {
  wi <- 1 / (vi + tau2)
  sumW <- sum(wi)
  theta <- sum(wi * yi) / sumW

  # EB criterion: weighted RSS should equal k-1
  RSS <- sum(wi * (yi - theta)^2)

  # Adjustment factor
  adj <- RSS / (k - 1)

  # Update tau2 (PM-style iteration)
  tau2_new <- tau2 * adj

  # Also try the direct formula
  # tau2 should make RSS/df = 1

  if(abs(tau2_new - tau2) < 1e-8) break
  tau2 <- tau2_new
}

cat(sprintf("\nManual EB iteration: %.6f (after %d iter)\n", tau2, iter))

# Actually, let me look at the source code approach
# The EB estimator in metafor uses a different iteration

# From Viechtbauer's paper, EB uses:
# tau2_{n+1} = max(0, sum[(y_i - theta)^2 - vi] / k)
# But this doesn't account for the weights properly

# Let's try the formula from Morris (1983)
tau2 <- rma(yi, vi, method="DL")$tau2

for(iter in 1:100) {
  wi <- 1 / (vi + tau2)
  sumW <- sum(wi)
  theta <- sum(wi * yi) / sumW

  # Morris formula
  # tau2_new = max(0, sum[(y_i - theta)^2 * wi^2] / sum(wi) - mean(vi*wi^2/sum(wi)))
  # Simplified: find tau2 where the "expected" variance matches

  num <- sum(wi * (yi - theta)^2) - (k - 1)
  denom <- sum(wi) - sum(wi^2) / sum(wi)

  tau2_new <- tau2 + num / denom
  tau2_new <- max(0, tau2_new)

  if(abs(tau2_new - tau2) < 1e-8) break
  tau2 <- tau2_new
}

cat(sprintf("Morris-style EB: %.6f (after %d iter)\n", tau2, iter))

# The actual EB is very similar to PM
# PM finds tau2 where Q = k-1 (where Q uses random-effects weights)
# EB uses the same criterion but may start differently or use slight variant

cat("\n=== CONCLUSION ===\n")
cat("EB and PM are nearly identical for BCG data\n")
cat(sprintf("EB: %.6f, PM: %.6f, diff: %.6f\n",
    res_eb$tau2, rma(yi, vi, method="PM")$tau2,
    abs(res_eb$tau2 - rma(yi, vi, method="PM")$tau2)))
