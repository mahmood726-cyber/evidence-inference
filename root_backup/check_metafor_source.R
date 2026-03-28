# Check metafor source for exact formulas
library(metafor)

# Get the rma.uni source code
# Looking at the tau2 estimation part

data(dat.bcg)
d <- escalc(measure='RR', ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- d$yi
vi <- d$vi
k <- length(yi)
p <- 1  # number of parameters (intercept only)

# For SJ, metafor uses (from source):
# tau2 <- (QE - (k-p)) / tr.P
# where QE is the Q statistic and tr.P is trace of projection matrix

wi <- 1/vi
W <- sum(wi)
theta <- sum(wi*yi)/W
Q <- sum(wi*(yi-theta)^2)

# For intercept-only model:
# P = W - wi %*% t(wi) / W = diagonal(wi) - outer(wi,wi)/W
# trace(P) = sum(wi) - sum(wi^2)/W = C

C <- W - sum(wi^2)/W
cat('Q =', Q, '\n')
cat('k =', k, '\n')
cat('C = trace(P) =', C, '\n')

# DL is: tau2 = (Q - (k-1)) / C
tau2_DL <- (Q - (k-1)) / C
cat('DL: (Q - (k-1)) / C =', tau2_DL, '\n')

# SJ might use different formula
# From Sidik-Jonkman 2005, their formula is iterative:
# tau2_{t+1} = (1/k) * sum(w_i * (y_i - theta_w)^2)
# where w_i = 1/(v_i + tau2_t)

# But metafor SJ seems to use a one-step version

# Let me check what metafor SJ actually does
# Trace the rma.uni function
fit_sj <- rma(yi, vi, method='SJ', verbose=TRUE)
cat('\nSJ result:', fit_sj$tau2, '\n')

# Try the formula from Sidik-Jonkman (2007):
# tau2 = k / (k-1) * (theta_w - mean(yi))^2 + (1/k) * sum((yi - mean(yi))^2)
# Hmm, that doesn't seem right either

# Let me try the "moment estimator" from SJ2006:
# tau2 = (1/k) * sum(wi * (yi - theta)^2 - vi + vi^2*wi)
wi_sj <- 1/vi
W_sj <- sum(wi_sj)
theta_sj <- sum(wi_sj*yi)/W_sj
tau2_SJ_try <- sum(wi_sj * (yi - theta_sj)^2 - vi + vi^2*wi_sj) / k
cat('\nSJ try: sum(wi*(yi-theta)^2 - vi + vi^2*wi)/k =', tau2_SJ_try, '\n')

# From metafor help ?rma:
# "SJ" = Sidik-Jonkman estimator
# Uses equation 9 from Sidik & Jonkman (2005)

# Looking at equation 9 from their paper:
# tau2_SJ = (1/k) * sum((yi - theta_bar)^2)
# where theta_bar is weighted mean using weights 1/(vi + tau2_0)
# and tau2_0 is some initial estimate (usually 0 or DL)

# But this is supposed to be iterative until convergence
# However, metafor might use a one-step version starting from 0

# One-step SJ from tau2=0:
tau2_0 <- 0
wi_0 <- 1/(vi + tau2_0)  # = 1/vi
W_0 <- sum(wi_0)
theta_0 <- sum(wi_0 * yi) / W_0
tau2_SJ_step <- sum((yi - theta_0)^2) / k
cat('SJ one-step from 0:', tau2_SJ_step, '\n')

# That gives 0.54, not 0.345. So metafor uses something else.

# Let me look at metafor's actual implementation by tracing
cat('\n--- Tracing metafor ---\n')
# Print internal values
fit <- rma(yi, vi, method='SJ')
cat('tau2:', fit$tau2, '\n')
cat('se.tau2:', fit$se.tau2, '\n')

# Check if metafor uses different starting value or formula
# From metafor source code in rma.uni.r, the SJ estimator is:
# if (method == "SJ") {
#    tau2 <- (QE - (k-p)) / trP
# }
# where QE is the residual heterogeneity Q statistic
# and trP is the trace of (W - W %*% X %*% solve(X'WX) %*% X' %*% W)

# For intercept model: trP = W - sum(wi)^2/W = W - W = 0? No...
# Actually trP = sum(wi) - sum(wi^2)/sum(wi) = C

# Wait, that's the same as DL formula!
# Unless SJ uses different weights...

# Let me check if SJ uses ni (sample sizes) as weights
# But we don't have sample sizes in metafor's formula...

# Check QE from fit
cat('QE from fit:', fit$QE, '\n')
cat('k-p:', k-1, '\n')

# Try: tau2 = (QE - (k-p)) / trP with different trP
# What trP gives us 0.3455?
needed_trP <- (Q - (k-1)) / fit$tau2
cat('Needed trP:', needed_trP, '\n')
cat('Actual C:', C, '\n')
