# Verify exact SJ formula from metafor source
library(metafor)
data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- dat$yi
vi <- dat$vi
k <- length(yi)
p <- 1  # intercept only model

cat("=== EXACT SJ FORMULA FROM METAFOR SOURCE ===\n\n")

# Step 1: tau2_0 = var(yi) * (k-1)/k = sum((yi - mean(yi))^2) / k
mean_y <- mean(yi)
tau2_0 <- sum((yi - mean_y)^2) / k
cat("tau2_0 = var(yi)*(k-1)/k:", tau2_0, "\n")

# Step 2: weights wi = 1/(vi + tau2_0)
wi <- 1 / (vi + tau2_0)
cat("sum(wi):", sum(wi), "\n")

# Step 3: Compute RSS using weighted projection
# For intercept-only model: P = W - W*1*inv(1'W1)*1'W = W - w*w'/sum(w)
# RSS = y'Py = sum(wi * yi^2) - (sum(wi*yi))^2 / sum(wi)
sumW <- sum(wi)
yPy <- sum(wi * yi^2) - (sum(wi * yi))^2 / sumW
cat("RSS (y'Py):", yPy, "\n")

# Step 4: tau2 = tau2_0 * RSS / (k - p)
tau2_sj <- tau2_0 * yPy / (k - p)
cat("\ntau2_SJ = tau2_0 * RSS / (k-p):", tau2_sj, "\n")

# Compare with metafor
res_sj <- rma(yi, vi, method="SJ")
cat("Metafor SJ:", res_sj$tau2, "\n")
cat("\nMatch:", abs(tau2_sj - res_sj$tau2) < 1e-6, "\n")

cat("\n=== ALSO VERIFY HS ===\n")
# HS formula: tau2 = sum(wi*(yi - theta_FE)^2)/sumW - sum(wi*vi)/sumW
wi_fe <- 1/vi
sumW_fe <- sum(wi_fe)
theta_fe <- sum(wi_fe * yi) / sumW_fe
tau2_hs <- sum(wi_fe * (yi - theta_fe)^2) / sumW_fe - sum(wi_fe * vi) / sumW_fe
tau2_hs <- max(0, tau2_hs)
cat("HS formula:", tau2_hs, "\n")
res_hs <- rma(yi, vi, method="HS")
cat("Metafor HS:", res_hs$tau2, "\n")
cat("Match:", abs(tau2_hs - res_hs$tau2) < 1e-6, "\n")
