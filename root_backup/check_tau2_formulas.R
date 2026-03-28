library(metafor)
data(dat.bcg)
d <- escalc(measure='RR', ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

cat('BCG Dataset Reference Values:\n')
cat('=============================\n\n')

methods <- c('DL', 'REML', 'ML', 'PM', 'HS', 'SJ', 'HE', 'EB')
for (m in methods) {
  fit <- rma(yi, vi, data=d, method=m)
  cat(sprintf('%s: tau2 = %.6f\n', m, fit$tau2))
}

# Get raw values for manual calculation
yi <- d$yi
vi <- d$vi
k <- length(yi)

cat('\nRaw values for formula verification:\n')
cat('=====================================\n')
cat(sprintf('k = %d\n', k))
cat(sprintf('mean(yi) = %.6f\n', mean(yi)))
cat(sprintf('var(yi) = %.6f\n', var(yi)))
cat(sprintf('mean(vi) = %.6f\n', mean(vi)))

# Q statistic
wi <- 1/vi
W <- sum(wi)
theta <- sum(wi * yi) / W
Q <- sum(wi * (yi - theta)^2)
cat(sprintf('Q = %.6f\n', Q))
cat(sprintf('sum(wi) = %.6f\n', W))

# Manual HE calculation
s2 <- var(yi)
vbar <- mean(vi)
cat(sprintf('\nHE manual: max(0, var(yi) - mean(vi)) = max(0, %.6f - %.6f) = %.6f\n',
            s2, vbar, max(0, s2 - vbar)))

# Print yi and vi
cat('\nyi values:\n')
cat(paste(sprintf('%.6f', yi), collapse=', '))
cat('\n\nvi values:\n')
cat(paste(sprintf('%.6f', vi), collapse=', '))
cat('\n')
