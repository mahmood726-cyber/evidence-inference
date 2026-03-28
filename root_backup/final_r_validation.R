# Final R Validation of Fixed HS and SJ Estimators
# Tests the exact formulas we implemented in JavaScript

library(metafor)
data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- dat$yi
vi <- dat$vi
k <- length(yi)

cat("=" , rep("=", 68), "\\n", sep="")
cat("FINAL VALIDATION: HS AND SJ ESTIMATORS\\n")
cat("=", rep("=", 68), "\\n\\n", sep="")

# Get metafor reference values
res_dl <- rma(yi, vi, method="DL")
res_reml <- rma(yi, vi, method="REML")
res_ml <- rma(yi, vi, method="ML")
res_hs <- rma(yi, vi, method="HS")
res_sj <- rma(yi, vi, method="SJ")
res_he <- rma(yi, vi, method="HE")

cat("METAFOR REFERENCE VALUES (v4.8.0):\\n")
cat("-", rep("-", 68), "\\n", sep="")
cat(sprintf("DL:   tau2 = %.6f\\n", res_dl$tau2))
cat(sprintf("REML: tau2 = %.6f\\n", res_reml$tau2))
cat(sprintf("ML:   tau2 = %.6f\\n", res_ml$tau2))
cat(sprintf("HS:   tau2 = %.6f\\n", res_hs$tau2))
cat(sprintf("SJ:   tau2 = %.6f\\n", res_sj$tau2))
cat(sprintf("HE:   tau2 = %.6f\\n", res_he$tau2))

cat("\\n")

# Replicate HS formula
cat("HS FORMULA VERIFICATION:\\n")
cat("-", rep("-", 68), "\\n", sep="")
wi <- 1/vi
sumW <- sum(wi)
theta_FE <- sum(wi * yi) / sumW
Q <- sum(wi * (yi - theta_FE)^2)
weighted_mean_vi <- sum(wi * vi) / sumW
tau2_HS_js <- max(0, Q / sumW - weighted_mean_vi)
cat(sprintf("  Q/sum(wi) - weighted_mean(vi) = %.6f\\n", tau2_HS_js))
cat(sprintf("  metafor HS                     = %.6f\\n", res_hs$tau2))
cat(sprintf("  Difference                     = %.9f\\n", abs(tau2_HS_js - res_hs$tau2)))
hs_pass <- abs(tau2_HS_js - res_hs$tau2) < 1e-6
cat(sprintf("  Status: %s\\n", ifelse(hs_pass, "PASS", "FAIL")))

cat("\\n")

# Replicate SJ formula
cat("SJ FORMULA VERIFICATION:\\n")
cat("-", rep("-", 68), "\\n", sep="")
y_bar <- mean(yi)
tau2_0 <- sum((yi - y_bar)^2) / k  # divide by k, not k-1
wi_sj <- 1 / (vi + tau2_0)
sumW_sj <- sum(wi_sj)
sumWY <- sum(wi_sj * yi)
sumWY2 <- sum(wi_sj * yi^2)
RSS <- sumWY2 - (sumWY^2) / sumW_sj
tau2_SJ_js <- max(0, tau2_0 * RSS / (k - 1))
cat(sprintf("  tau2_0                         = %.6f\\n", tau2_0))
cat(sprintf("  RSS                            = %.6f\\n", RSS))
cat(sprintf("  tau2_0 * RSS / (k-1)           = %.6f\\n", tau2_SJ_js))
cat(sprintf("  metafor SJ                     = %.6f\\n", res_sj$tau2))
cat(sprintf("  Difference                     = %.9f\\n", abs(tau2_SJ_js - res_sj$tau2)))
sj_pass <- abs(tau2_SJ_js - res_sj$tau2) < 1e-6
cat(sprintf("  Status: %s\\n", ifelse(sj_pass, "PASS", "FAIL")))

cat("\\n")
cat("=", rep("=", 68), "\\n", sep="")
if (hs_pass && sj_pass) {
  cat("ALL TESTS PASSED - HS and SJ match metafor exactly!\\n")
} else {
  cat("SOME TESTS FAILED\\n")
}
cat("=", rep("=", 68), "\\n", sep="")
