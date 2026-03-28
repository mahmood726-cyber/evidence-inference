library(metafor)
data(dat.bcg)
d <- escalc(measure='RR', ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)
yi <- d$yi
vi <- d$vi

cat('=== METAFOR 4.8-0 REFERENCE VALUES ===\n\n')

# All tau2 methods
methods <- c('DL', 'REML', 'ML', 'HS', 'SJ', 'HE', 'EB', 'PM')
for(m in methods) {
  res <- rma(yi, vi, method=m)
  cat(sprintf('%s: tau2=%.6f, theta=%.6f\n', m, res$tau2, res$beta[1]))
}

# HKSJ
res_hksj <- rma(yi, vi, method='REML', test='knha')
cat(sprintf('\nHKSJ: CI=[%.3f, %.3f]\n', res_hksj$ci.lb, res_hksj$ci.ub))

# I2
res_dl <- rma(yi, vi, method='DL')
cat(sprintf('I2: %.2f%%\n', res_dl$I2))
cat(sprintf('Q: %.3f\n', res_dl$QE))

cat('\n=== VALIDATION COMPLETE ===\n')
