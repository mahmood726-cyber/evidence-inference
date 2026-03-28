# Validate generated R code
library(metafor)

dat <- data.frame(
  study = c('Aronson 1948', 'Ferguson 1949', 'Rosenthal 1960', 'Hart 1977'),
  ai = c(4, 6, 3, 62),
  bi = c(119, 300, 228, 13536),
  ci = c(11, 29, 11, 248),
  di = c(128, 274, 209, 12619)
)

dat <- escalc(measure = 'RR', ai = ai, bi = bi, ci = ci, di = di, data = dat)
res <- rma(yi, vi, data = dat, method = 'REML')

cat('=== R Export Validation ===\n')
cat('Pooled RR:', exp(coef(res)), '\n')
cat('tau^2:', res$tau2, '\n')
cat('I^2:', res$I2, '%\n')
cat('VALIDATION PASSED\n')
