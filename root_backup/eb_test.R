# Find exact EB formula
library(metafor)

data(dat.bcg)
d <- escalc(measure='RR', ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- d$yi
vi <- d$vi
k <- length(yi)

# EB target: 0.3180685
fit_eb <- rma(yi, vi, method='EB')
cat('EB metafor:', fit_eb$tau2, '\n\n')

# PM result
fit_pm <- rma(yi, vi, method='PM')
cat('PM metafor:', fit_pm$tau2, '\n\n')

# EB is very close to PM (0.318094 vs 0.318069)
# Let me check if EB is just PM with slight modification

# PM iteration with Q_tau = Q statistic computed with updated weights
wi <- 1/vi
W <- sum(wi)
theta <- sum(wi*yi)/W
Q <- sum(wi*(yi-theta)^2)
C <- W - sum(wi^2)/W

cat('--- PM/EB Iteration ---\n')
tau2 <- max(0.0001, (Q - (k-1)) / C)  # Start with DL

for (iter in 1:50) {
  wi_t <- 1 / (vi + tau2)
  W_t <- sum(wi_t)
  theta_t <- sum(wi_t * yi) / W_t
  Q_t <- sum(wi_t * (yi - theta_t)^2)
  C_t <- W_t - sum(wi_t^2) / W_t

  # PM/EB update
  tau2_new <- max(0, (Q_t - (k-1)) / C_t)

  if (abs(tau2_new - tau2) < 1e-10) {
    cat(sprintf('Converged at iter %d: tau2 = %.6f\n', iter, tau2_new))
    break
  }
  if (iter <= 5 || iter %% 10 == 0) {
    cat(sprintf('Iter %d: tau2 = %.6f\n', iter, tau2_new))
  }
  tau2 <- tau2_new
}

cat('\nFinal tau2:', tau2, '\n')
cat('PM target:', fit_pm$tau2, '\n')
cat('EB target:', fit_eb$tau2, '\n')

# So PM iteration converges to PM = 0.318094
# EB gives 0.318069 which is almost identical

# The small difference might be due to different update formulas
# Let me try the Morris (1983) EB formula:
# tau2_new = max(0, (1/k) * sum((yi - theta)^2 - vi * (1 - wi*vi)))

cat('\n--- Morris EB Iteration ---\n')
tau2 <- (Q - (k-1)) / C  # Start with DL

for (iter in 1:50) {
  wi_t <- 1 / (vi + tau2)
  W_t <- sum(wi_t)
  theta_t <- sum(wi_t * yi) / W_t

  # Morris EB formula
  ss <- sum((yi - theta_t)^2 - vi * (1 - vi * wi_t))
  tau2_new <- max(0, ss / k)

  if (abs(tau2_new - tau2) < 1e-10) {
    cat(sprintf('Morris EB converged at iter %d: tau2 = %.6f\n', iter, tau2_new))
    break
  }
  if (iter <= 5) {
    cat(sprintf('Iter %d: tau2 = %.6f\n', iter, tau2_new))
  }
  tau2 <- tau2_new
}

# The Morris formula gives 0.360... not 0.318
# So metafor uses a different EB formula

# Let me try: Paule-Mandel style iteration (Q_tau = k-1 criterion)
cat('\n--- Paule-Mandel Style EB ---\n')
tau2 <- 0

for (iter in 1:100) {
  wi_t <- 1 / (vi + tau2)
  W_t <- sum(wi_t)
  theta_t <- sum(wi_t * yi) / W_t
  Q_t <- sum(wi_t * (yi - theta_t)^2)

  # Find tau2 such that Q_t = k - 1
  # For small tau2, Q_t > k-1; for large tau2, Q_t < k-1

  if (Q_t < k - 1) {
    tau2 <- tau2 * 0.9
  } else {
    tau2 <- tau2 * 1.1 + 0.01
  }

  if (iter <= 5 || iter %% 20 == 0) {
    cat(sprintf('Iter %d: Q=%.2f, tau2=%.6f\n', iter, Q_t, tau2))
  }

  if (abs(Q_t - (k-1)) < 0.001) {
    cat(sprintf('Converged: Q=%.4f, tau2=%.6f\n', Q_t, tau2))
    break
  }
}
