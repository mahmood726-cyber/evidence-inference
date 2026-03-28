# Get exact BCG data values
library(metafor)
data(dat.bcg)
dat <- escalc(measure="RR", ai=tpos, bi=tneg, ci=cpos, di=cneg, data=dat.bcg)

cat("BCG Dataset - exact yi values:\n")
cat("yi <- c(", paste(sprintf("%.6f", dat$yi), collapse=", "), ")\n\n")

cat("BCG Dataset - exact vi values:\n")
cat("vi <- c(", paste(sprintf("%.6f", dat$vi), collapse=", "), ")\n\n")

cat("Number of studies: k =", length(dat$yi), "\n")
