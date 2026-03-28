library(metafor)
data(dat.bcg)
d <- escalc(measure='RR', ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)
yi <- d$yi
vi <- d$vi

cat("=== EB ESTIMATOR INVESTIGATION ===\n\n")

# metafor EB result
res_eb <- rma(yi, vi, method="EB")
cat(sprintf("metafor EB tau2: %.6f\n", res_eb$tau2))

# The EB estimator in metafor uses the method from Morris (1983)
# It's an empirical Bayes estimator that iteratively estimates tau2

# Let's also check if there's a closed-form solution or if it's iterative
cat("\nmetafor uses Paule-Mandel style iteration for EB\n")
cat("The EB estimate should be close to PM:\n")

res_pm <- rma(yi, vi, method="PM")
cat(sprintf("metafor PM tau2: %.6f\n", res_pm$tau2))

# Morris EB formula (approximate)
# Start with DL estimate
dl <- rma(yi, vi, method="DL")
tau2_init <- dl$tau2
cat(sprintf("\nDL starting point: %.6f\n", tau2_init))

# The exact EB formula is complex - let me trace what metafor does
cat("\n=== Comparing all methods ===\n")
methods <- c("DL", "PM", "EB", "REML", "ML")
for(m in methods) {
  res <- rma(yi, vi, method=m)
  cat(sprintf("%s: %.6f\n", m, res$tau2))
}
