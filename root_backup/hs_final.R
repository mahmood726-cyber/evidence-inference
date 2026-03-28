# Find exact HS formula
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

# metafor target
target <- 0.228363

# The needed X is 614.0794
# W = 609.7007
# Difference = 4.38

cat('Looking for formula where X = 614.0794\n\n')
cat('W =', W, '\n')
cat('sum(wi^2)/W =', sum(wi^2)/W, '\n')
cat('sum(wi^2) =', sum(wi^2), '\n')
cat('C = W - sum(wi^2)/W =', C, '\n')
cat('k =', k, '\n')

# Try different combinations
cat('\nTrying combinations:\n')
cat('W + sum(vi) =', W + sum(vi), '\n')
cat('W + k/sum(vi) =', W + k/sum(vi), '\n')
cat('W * (1 + 1/(k-1)) =', W * (1 + 1/(k-1)), '\n')
cat('W * k/(k-1) - (k-1) =', W * k/(k-1) - (k-1), '\n')

# Try: tau2 = (Q - k) / (W + (k-1))
# No wait... let me think about this differently

# What if it's (Q - (k-1)) / (W * correction_factor)?
correction <- (Q - (k-1)) / target / W
cat('\nCorrection factor for W:', correction, '\n')
# 1.0072... so it's W * 1.0072 = 614.08

# What equals 1.0072?
cat('1 + 1/k =', 1 + 1/k, '\n')
cat('1 + 1/(k-1) =', 1 + 1/(k-1), '\n')
cat('1 + vi[1]/sum(vi) =', 1 + vi[1]/sum(vi), '\n')

# Let me try the formula from the metafor paper directly
# HS uses: tau2 = (Q - (k-1)) / W when estimating pooled effect with unit weights
# But with a bias correction factor

# Actually, looking at the metafor source code again:
# For method="HS", the formula is derived from the Q statistic
# but uses a different C constant

# Try: C_HS = W + something
C_needed <- (Q - (k-1)) / target
cat('\nC_needed =', C_needed, '\n')
cat('W =', W, '\n')
cat('Difference =', C_needed - W, '\n')

# What's close to 4.38?
cat('\nsum(wi) / k =', sum(wi) / k, '\n')
cat('mean(vi) * k =', mean(vi) * k, '\n')
cat('k / mean(wi) =', k / mean(wi), '\n')

# Let me check if it's based on prediction intervals
# From Sidik & Jonkman 2007:
# C_HS = sum(wi) - sum(wi^2)/sum(wi) + k - 1
C_SJ <- C + k - 1
tau2_SJ <- (Q - (k-1)) / C_SJ
cat('\nSJ C_HS =', C_SJ, '-> tau2 =', tau2_SJ, '\n')

# metafor result for verification
fit <- rma(yi, vi, method='HS')
cat('\nmetafor HS:', fit$tau2, '\n')

# What about the original Schmidt & Hunter formula?
# They use sample sizes as weights, which we don't have
# For inverse-variance weights, the formula might be different

# Let me try: tau2 = (Q - k) / W (using k instead of k-1)
tau2_try1 <- (Q - k) / W
cat('\n(Q - k) / W =', tau2_try1, '\n')

# Or: tau2 = (Q - (k-1)) / (W + correction)
# where correction makes it match
needed_add <- C_needed - W
cat('Need to add to W:', needed_add, '\n')
