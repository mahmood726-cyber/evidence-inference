# Get exact reference values for BCG dataset
library(metafor)
data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

yi <- dat$yi
vi <- dat$vi

cat("=== EXACT REFERENCE VALUES FOR TEST SUITE ===\n\n")

res_dl <- rma(yi, vi, method="DL")
res_reml <- rma(yi, vi, method="REML")
res_ml <- rma(yi, vi, method="ML")
res_hs <- rma(yi, vi, method="HS")
res_sj <- rma(yi, vi, method="SJ")
res_he <- rma(yi, vi, method="HE")

cat(sprintf("DL: %.6f\n", res_dl$tau2))
cat(sprintf("REML: %.6f\n", res_reml$tau2))
cat(sprintf("ML: %.6f\n", res_ml$tau2))
cat(sprintf("HS: %.6f\n", res_hs$tau2))
cat(sprintf("SJ: %.6f\n", res_sj$tau2))
cat(sprintf("HE: %.6f\n", res_he$tau2))
cat(sprintf("theta_DL: %.6f\n", res_dl$b[1]))
cat(sprintf("Q: %.6f\n", res_dl$QE))
cat(sprintf("I2: %.2f\n", res_dl$I2))

# HKSJ CI
res_hksj <- rma(yi, vi, method="REML", test="knha")
cat(sprintf("HKSJ_lower: %.6f\n", res_hksj$ci.lb))
cat(sprintf("HKSJ_upper: %.6f\n", res_hksj$ci.ub))

cat("\n=== JavaScript format ===\n")
cat("ref: {\n")
cat(sprintf("  DL: %.6f,\n", res_dl$tau2))
cat(sprintf("  REML: %.6f,\n", res_reml$tau2))
cat(sprintf("  ML: %.6f,\n", res_ml$tau2))
cat(sprintf("  HS: %.6f,\n", res_hs$tau2))
cat(sprintf("  SJ: %.6f,\n", res_sj$tau2))
cat(sprintf("  HE: %.6f,\n", res_he$tau2))
cat(sprintf("  theta_DL: %.6f,\n", res_dl$b[1]))
cat(sprintf("  Q: %.3f,\n", res_dl$QE))
cat(sprintf("  I2: %.2f,\n", res_dl$I2))
cat(sprintf("  HKSJ_lower: %.3f,\n", res_hksj$ci.lb))
cat(sprintf("  HKSJ_upper: %.3f\n", res_hksj$ci.ub))
cat("}\n")
