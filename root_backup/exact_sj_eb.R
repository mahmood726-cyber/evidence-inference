# Deep dive into exact SJ and EB formulas
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
C <- W - sum(wi^2)/W

cat('Base values:\n')
cat('k =', k, '\n')
cat('W =', W, '\n')
cat('Q =', Q, '\n')
cat('C =', C, '\n')
cat('DL = (Q-k+1)/C =', (Q-(k-1))/C, '\n')

# Get metafor results
fit_sj <- rma(yi, vi, method='SJ')
fit_eb <- rma(yi, vi, method='EB')

cat('\nmetafor results:\n')
cat('SJ:', fit_sj$tau2, '\n')
cat('EB:', fit_eb$tau2, '\n')

# Try to reverse-engineer SJ
# SJ = 0.3455, Q-(k-1) = 140.233
# If tau2 = (Q-(k-1))/X, then X = 140.233/0.3455 = 405.87
# C = 454.18, so the adjustment is 454.18 - 405.87 = 48.31

cat('\n--- Reverse engineering SJ ---\n')
sj_denom <- (Q - (k-1)) / fit_sj$tau2
cat('SJ denominator needed:', sj_denom, '\n')
cat('C =', C, '\n')
cat('Adjustment =', C - sj_denom, '\n')

# What's 48.31?
cat('\nPossible factors:\n')
cat('k*mean(vi) =', k * mean(vi), '\n')
cat('sum(vi) =', sum(vi), '\n')
cat('sum(wi)/k =', sum(wi)/k, '\n')
cat('k^2/sum(wi) =', k^2/sum(wi), '\n')

# Let me try: SJ = (Q-(k-1)) / (C - k + sum(vi)/vi_avg * k)
# Nope, that doesn't make sense

# Try from metafor trace output
# Looking at metafor source, SJ uses:
# tau2 = (QE - (k-p)) / trP
# where trP is trace of projection matrix

# For intercept-only model:
# P_i = wi - wi^2/W
# trP = sum(P_i) = sum(wi - wi^2/W) = W - sum(wi^2)/W = C

# So SJ and DL should be same? But they're not...

# Let me check if there's an iteration involved
cat('\n--- Checking SJ iteration ---\n')

# From Sidik & Jonkman (2005) original paper:
# tau2^(new) = (1/k) * sum_i (y_i - theta_tau)^2
# where theta_tau uses weights 1/(vi + tau2)

# Starting from tau2 = 0:
tau2 <- 0
for (iter in 1:10) {
  wi_t <- 1 / (vi + tau2)
  W_t <- sum(wi_t)
  theta_t <- sum(wi_t * yi) / W_t

  # Original SJ formula
  tau2_new <- sum((yi - theta_t)^2) / k

  cat(sprintf('Iter %d: tau2 = %.6f\n', iter, tau2_new))

  if (abs(tau2_new - tau2) < 1e-10) break
  tau2 <- tau2_new
}

cat('\nSJ iteration converges to:', tau2, '\n')
cat('metafor SJ:', fit_sj$tau2, '\n')

# That gives 0.4446, not 0.3455. So metafor uses different formula.

# Let me try weighted version
cat('\n--- Trying weighted SJ ---\n')
tau2 <- 0
for (iter in 1:10) {
  wi_t <- 1 / (vi + tau2)
  W_t <- sum(wi_t)
  theta_t <- sum(wi_t * yi) / W_t

  # Weighted SJ formula
  tau2_new <- sum(wi_t * (yi - theta_t)^2) / W_t

  cat(sprintf('Iter %d: tau2 = %.6f\n', iter, tau2_new))

  if (abs(tau2_new - tau2) < 1e-10) break
  tau2 <- tau2_new
}

# Let me try Q-based formula
cat('\n--- Trying Q-based SJ ---\n')
tau2 <- 0
for (iter in 1:10) {
  wi_t <- 1 / (vi + tau2)
  W_t <- sum(wi_t)
  theta_t <- sum(wi_t * yi) / W_t
  Q_t <- sum(wi_t * (yi - theta_t)^2)
  C_t <- W_t - sum(wi_t^2) / W_t

  tau2_new <- max(0, (Q_t - (k-1)) / C_t)

  cat(sprintf('Iter %d: Q=%.2f, C=%.2f, tau2 = %.6f\n', iter, Q_t, C_t, tau2_new))

  if (abs(tau2_new - tau2) < 1e-10) break
  tau2 <- tau2_new
}

# That's iterative DL, which gives same as PM

# Let me check if metafor SJ uses one-step from specific starting value
cat('\n--- One-step SJ from different starts ---\n')

# From var(yi)
tau2_start <- var(yi)
wi_t <- 1 / (vi + tau2_start)
W_t <- sum(wi_t)
theta_t <- sum(wi_t * yi) / W_t
Q_t <- sum(wi_t * (yi - theta_t)^2)
C_t <- W_t - sum(wi_t^2) / W_t
tau2_sj <- (Q_t - (k-1)) / C_t
cat(sprintf('From var(yi)=%.4f: tau2 = %.6f\n', tau2_start, tau2_sj))

# From DL
tau2_start <- (Q - (k-1)) / C
wi_t <- 1 / (vi + tau2_start)
W_t <- sum(wi_t)
theta_t <- sum(wi_t * yi) / W_t
Q_t <- sum(wi_t * (yi - theta_t)^2)
C_t <- W_t - sum(wi_t^2) / W_t
tau2_sj <- (Q_t - (k-1)) / C_t
cat(sprintf('From DL=%.4f: tau2 = %.6f\n', tau2_start, tau2_sj))
