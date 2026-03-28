# Check HS and SJ formulas
library(metafor)
data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- dat$yi
vi <- dat$vi
k <- length(yi)

cat("=== METAFOR TAU2 COMPARISON ===\n\n")

# All methods
methods <- c("DL", "HS", "SJ", "HE")
for (m in methods) {
  res <- rma(yi, vi, method=m)
  cat(sprintf("%s: tau2 = %.6f\n", m, res$tau2))
}

# Manual calculations
cat("\n=== MANUAL CALCULATIONS ===\n")

wi <- 1/vi
sumW <- sum(wi)
sumW2 <- sum(wi^2)
theta_FE <- sum(wi * yi) / sumW
Q <- sum(wi * (yi - theta_FE)^2)

cat(sprintf("Q = %.4f, k = %d\n", Q, k))
cat(sprintf("sum(wi) = %.4f\n", sumW))
cat(sprintf("C (DL denominator) = %.4f\n", sumW - sumW2/sumW))

# DL formula
tau2_DL <- max(0, (Q - (k-1)) / (sumW - sumW2/sumW))
cat(sprintf("\nDL: (Q-(k-1))/C = %.6f\n", tau2_DL))

# HS formula - metafor uses different denominator
tau2_HS_simple <- max(0, (Q - (k-1)) / sumW)
cat(sprintf("HS simple: (Q-(k-1))/sum(wi) = %.6f\n", tau2_HS_simple))

# Check metafor source for HS
cat("\nMetafor HS actual:\n")
res_hs <- rma(yi, vi, method="HS")
cat(sprintf("  tau2 = %.6f\n", res_hs$tau2))
