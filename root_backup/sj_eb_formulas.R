# Find exact SJ and EB formulas
library(metafor)

data(dat.bcg)
d <- escalc(measure='RR', ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- d$yi
vi <- d$vi
k <- length(yi)

wi <- 1/vi
W <- sum(wi)
theta <- sum(wi*yi)/W
Q <- sum(wi*(yi-theta)^2)

# Verified: HS = (Q - k) / W
tau2_HS <- (Q - k) / W
cat('HS verified: (Q - k) / W =', tau2_HS, '\n')

# Now for SJ (Sidik-Jonkman)
# From Sidik & Jonkman (2005), the estimator is iterative:
# Starting with tau2_0 = tau2_DL or similar
# Then: tau2 = (1/k) * sum((yi - theta_w)^2)
# where theta_w uses weights wi = 1/(vi + tau2_0)

# metafor SJ
fit_sj <- rma(yi, vi, method='SJ')
cat('\nSJ metafor:', fit_sj$tau2, '\n')

# Try manual SJ calculation
# Step 1: Get DL estimate
tau2_DL <- max(0, (Q - (k-1)) / (W - sum(wi^2)/W))
cat('DL for SJ init:', tau2_DL, '\n')

# Step 2: Calculate with DL weights
wi_sj <- 1 / (vi + tau2_DL)
W_sj <- sum(wi_sj)
theta_sj <- sum(wi_sj * yi) / W_sj

# SJ formula: tau2 = (1/k) * sum((yi - theta_w)^2)
tau2_SJ <- sum((yi - theta_sj)^2) / k
cat('SJ manual (using DL):', tau2_SJ, '\n')

# Actually, looking at metafor source, SJ uses a different starting point
# Let me try with HE as initial
tau2_HE <- max(0, var(yi) - mean(vi))
wi_he <- 1 / (vi + tau2_HE)
W_he <- sum(wi_he)
theta_he <- sum(wi_he * yi) / W_he
tau2_SJ_he <- sum((yi - theta_he)^2) / k
cat('SJ manual (using HE):', tau2_SJ_he, '\n')

# From metafor source, SJ starts with 0 and iterates
# Let me trace through the exact metafor implementation
tau2_init <- 0
wi_init <- 1 / (vi + tau2_init)
W_init <- sum(wi_init)
theta_init <- sum(wi_init * yi) / W_init
tau2_SJ_step1 <- sum((yi - theta_init)^2) / k
cat('SJ step1 (from 0):', tau2_SJ_step1, '\n')

# Continue iteration
wi_step1 <- 1 / (vi + tau2_SJ_step1)
W_step1 <- sum(wi_step1)
theta_step1 <- sum(wi_step1 * yi) / W_step1
tau2_SJ_step2 <- sum((yi - theta_step1)^2) / k
cat('SJ step2:', tau2_SJ_step2, '\n')

# Continue
wi_step2 <- 1 / (vi + tau2_SJ_step2)
W_step2 <- sum(wi_step2)
theta_step2 <- sum(wi_step2 * yi) / W_step2
tau2_SJ_step3 <- sum((yi - theta_step2)^2) / k
cat('SJ step3:', tau2_SJ_step3, '\n')

# Keep going
for (i in 4:20) {
  wi_curr <- 1 / (vi + tau2_SJ_step3)
  W_curr <- sum(wi_curr)
  theta_curr <- sum(wi_curr * yi) / W_curr
  tau2_SJ_new <- sum((yi - theta_curr)^2) / k
  if (abs(tau2_SJ_new - tau2_SJ_step3) < 1e-10) {
    cat('SJ converged at iteration', i, ':', tau2_SJ_new, '\n')
    break
  }
  tau2_SJ_step3 <- tau2_SJ_new
}

# Now EB (Empirical Bayes)
cat('\n\n===== EB =====\n')
fit_eb <- rma(yi, vi, method='EB')
cat('EB metafor:', fit_eb$tau2, '\n')

# EB from metafor uses:
# tau2 = (1/k) * sum((yi - theta)^2 - vi*(1 - vi*wi))
# where wi = 1/(vi + tau2)

# Starting from DL
tau2_eb <- tau2_DL
cat('EB starting with DL:', tau2_eb, '\n')

for (i in 1:20) {
  wi_eb <- 1 / (vi + tau2_eb)
  W_eb <- sum(wi_eb)
  theta_eb <- sum(wi_eb * yi) / W_eb

  # EB update formula
  ss <- sum((yi - theta_eb)^2 - vi * (1 - vi * wi_eb))
  tau2_eb_new <- max(0, ss / k)

  cat(sprintf('EB iter %d: tau2 = %.6f\n', i, tau2_eb_new))

  if (abs(tau2_eb_new - tau2_eb) < 1e-10) {
    cat('EB converged at iteration', i, '\n')
    break
  }
  tau2_eb <- tau2_eb_new
}
