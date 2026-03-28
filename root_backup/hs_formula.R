# Exact HS (Hunter-Schmidt) formula derivation
library(metafor)
data(dat.bcg)
d <- escalc(measure='RR', ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- d$yi
vi <- d$vi
k <- length(yi)

# Inverse variance weights
wi <- 1/vi
W <- sum(wi)

# Q statistic
theta_w <- sum(wi * yi) / W
Q <- sum(wi * (yi - theta_w)^2)

cat('Step-by-step HS calculation:\n')
cat('============================\n')
cat(sprintf('k = %d\n', k))
cat(sprintf('W = sum(wi) = %.6f\n', W))
cat(sprintf('Q = %.6f\n', Q))
cat(sprintf('theta_w = %.6f\n', theta_w))

# For intercept-only model, the HS formula simplifies
# From metafor source, for simple RE model:
# P_i = w_i - w_i^2/W = w_i * (1 - w_i/W)
# vt = (sum(P * vi) - k) / sum(P * (1 - vi * P))
# tau2 = max(0, k/(k-1) * vt)

P <- wi - wi^2/W
cat(sprintf('\nP (projection weights):\n'))
cat(sprintf('sum(P) = %.6f\n', sum(P)))

numerator <- sum(P * vi) - k
cat(sprintf('\nNumerator: sum(P * vi) - k = %.6f - %d = %.6f\n', sum(P*vi), k, numerator))

denominator <- sum(P * (1 - vi * P))
cat(sprintf('Denominator: sum(P * (1 - vi*P)) = %.6f\n', denominator))

vt <- numerator / denominator
cat(sprintf('\nvt = %.6f\n', vt))

tau2_HS <- max(0, k/(k-1) * vt)
cat(sprintf('tau2_HS = max(0, k/(k-1) * vt) = max(0, %.6f * %.6f) = %.6f\n',
            k/(k-1), vt, tau2_HS))

# Verify against metafor
fit <- rma(yi, vi, method='HS')
cat(sprintf('\nmetafor HS tau2: %.6f\n', fit$tau2))

# Also show other formulas
cat('\n\n========================================\n')
cat('Other estimator formulas:\n')
cat('========================================\n')

# SJ (Sidik-Jonkman)
# From source: iterative formula
cat('\nSJ: Iterative method with specific starting value\n')
fit_sj <- rma(yi, vi, method='SJ')
cat(sprintf('metafor SJ tau2: %.6f\n', fit_sj$tau2))

# EB (Empirical Bayes)
cat('\nEB: Iterative method\n')
fit_eb <- rma(yi, vi, method='EB')
cat(sprintf('metafor EB tau2: %.6f\n', fit_eb$tau2))
