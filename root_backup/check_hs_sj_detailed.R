# Detailed analysis of HS and SJ formulas
library(metafor)
data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- dat$yi
vi <- dat$vi
k <- length(yi)

cat("=== DETAILED HS ANALYSIS ===\n\n")

# Get the metafor HS result
res_hs <- rma(yi, vi, method="HS")
cat("Metafor HS tau2:", res_hs$tau2, "\n")

# Basic components
wi <- 1/vi
sumW <- sum(wi)
theta_FE <- sum(wi * yi) / sumW
Q <- sum(wi * (yi - theta_FE)^2)

# Simple HS formula
tau2_HS_simple <- max(0, (Q - (k-1)) / sumW)
cat("Simple HS (Q-(k-1))/sum(wi):", tau2_HS_simple, "\n")

# Hunter-Schmidt original formula (unweighted)
# tau2 = var(yi) - mean(vi)
tau2_HS_hunter <- max(0, var(yi) - mean(vi))
cat("Hunter-Schmidt (var(yi) - mean(vi)):", tau2_HS_hunter, "\n")

# Alternative HS (weighted by N)
# This is what metafor actually uses
tau2_HS_weighted <- max(0, sum(wi*(yi - theta_FE)^2)/sumW - sum(wi*vi)/sumW)
cat("HS weighted:", tau2_HS_weighted, "\n")

cat("\n=== DETAILED SJ ANALYSIS ===\n\n")
res_sj <- rma(yi, vi, method="SJ")
cat("Metafor SJ tau2:", res_sj$tau2, "\n")

# SJ Step 1: Unweighted variance estimate
mean_y <- mean(yi)
s2 <- sum((yi - mean_y)^2) / (k - 1)
v_bar <- mean(vi)
tau2_0 <- max(0, s2 - v_bar)
cat("SJ Step 1 (s2 - v_bar):", tau2_0, "\n")

# SJ Step 2: DL-style with new weights
wi_1 <- 1 / (vi + tau2_0)
sumW_1 <- sum(wi_1)
theta_1 <- sum(wi_1 * yi) / sumW_1
Q_1 <- sum(wi_1 * (yi - theta_1)^2)
C_1 <- sumW_1 - sum(wi_1^2) / sumW_1
tau2_SJ_step2 <- max(0, (Q_1 - (k-1)) / C_1)
cat("SJ Step 2:", tau2_SJ_step2, "\n")

cat("\n=== HE ANALYSIS ===\n\n")
res_he <- rma(yi, vi, method="HE")
cat("Metafor HE tau2:", res_he$tau2, "\n")

# HE formula (Hedges unweighted)
tau2_HE <- max(0, s2 - v_bar)
cat("HE (s2 - v_bar):", tau2_HE, "\n")

cat("\n=== SUMMARY ===\n")
cat("Method   | Metafor  | Our Formula\n")
cat("---------+----------+------------\n")
cat(sprintf("HS       | %.6f | %.6f\n", res_hs$tau2, tau2_HS_weighted))
cat(sprintf("SJ       | %.6f | %.6f\n", res_sj$tau2, tau2_SJ_step2))
cat(sprintf("HE       | %.6f | %.6f\n", res_he$tau2, tau2_HE))
