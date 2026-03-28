# Find exact HS formula from metafor source
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

cat('k =', k, '\n')
cat('W = sum(wi) =', W, '\n')
cat('Q =', Q, '\n\n')

# DL formula
C <- W - sum(wi^2)/W
tau2_DL <- max(0, (Q - (k-1)) / C)
cat('DL: (Q-(k-1))/C =', tau2_DL, '\n')

# HS alt1: (Q-(k-1))/W
tau2_HS_alt1 <- max(0, (Q - (k-1)) / W)
cat('HS alt1: (Q-(k-1))/W =', tau2_HS_alt1, '\n')

# HS alt2: k/(k-1) * (Q-(k-1))/W
tau2_HS_alt2 <- max(0, (k/(k-1)) * (Q - (k-1)) / W)
cat('HS alt2: k/(k-1) * (Q-(k-1))/W =', tau2_HS_alt2, '\n')

# HS alt3: From Sidik-Jonkman paper
denom <- W - sum(wi^2)/W + k - 1
tau2_HS_alt3 <- max(0, (k/(k-1)) * (Q - k + 1) / denom)
cat('HS alt3: k/(k-1) * (Q-k+1)/(C+k-1) =', tau2_HS_alt3, '\n')

# HS alt4: Try with different denominator
tau2_HS_alt4 <- max(0, (Q - (k-1)) / (W + k - 1))
cat('HS alt4: (Q-(k-1))/(W+k-1) =', tau2_HS_alt4, '\n')

# metafor result
fit <- rma(yi, vi, method='HS')
cat('\nmetafor HS:', fit$tau2, '\n')

# What if metafor uses truncation differently?
# Let me reverse-engineer the formula
# metafor gives 0.228363
# Q - (k-1) = 140.233
# If tau2 = (Q - (k-1)) / X, then X = 140.233 / 0.228363 = 614.05

target <- 0.228363
X_needed <- (Q - (k-1)) / target
cat('\nTo get 0.228363: X =', X_needed, '\n')
cat('W =', W, '\n')
cat('W + k - 1 =', W + k - 1, '\n')
