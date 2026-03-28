# ================================================================
# TruthCert-PairwisePro: Complete R Analysis Script
# Generated: 2026-01-11
# ================================================================
# This script reproduces the analysis in R/metafor
# IMPORTANT: Use these R results for publication
# ================================================================

# Install and load required packages
if (!require(metafor)) install.packages("metafor")
library(metafor)

# Optional packages for additional plots
if (!require(ggplot2)) install.packages("ggplot2")
library(ggplot2)

# ================================================================
# STUDY DATA (Binary Outcomes)
# ================================================================
dat <- data.frame(
  study = c("Aronson 1948",
           "Ferguson 1949",
           "Rosenthal 1960",
           "Hart 1977",
           "Frimodt-Moller 1973",
           "Stein 1953",
           "Vandiviere 1973",
           "TPT Madras 1980",
           "Coetzee 1968",
           "Rosenthal 1961",
           "Comstock 1974",
           "Comstock 1976",
           "Comstock 1969"),
  ai = c(4, 6, 3, 62, 33, 180, 8, 505, 29, 17, 186, 5, 27),
  bi = c(119, 300, 228, 13536, 5036, 1536, 2537, 87886, 7470, 1682, 50448, 2493, 16886),
  ci = c(11, 29, 11, 248, 47, 372, 10, 499, 45, 65, 141, 3, 29),
  di = c(128, 274, 209, 12619, 5761, 1293, 619, 87892, 7232, 1535, 27197, 2338, 17825),
  n1 = c(123, 306, 231, 13598, 5069, 1716, 2545, 88391, 7499, 1699, 50634, 2498, 16913),
  n2 = c(139, 303, 220, 12867, 5808, 1665, 629, 88391, 7277, 1600, 27338, 2341, 17854),
  year = c(1948, 1949, 1960, 1977, 1973, 1953, 1973, 1980, 1968, 1961, 1974, 1976, 1969)
)

# Calculate effect sizes (log Risk Ratio)
dat <- escalc(measure = "RR", ai = ai, bi = bi, ci = ci, di = di, data = dat)
# Alternative measures:
# escalc(measure = "OR", ...)  # Odds Ratio
# escalc(measure = "RD", ...)  # Risk Difference

# ================================================================
# MAIN META-ANALYSIS
# ================================================================

# Random-effects model with REML estimator
res <- rma(yi, vi, data = dat, method = "REML", slab = study)
print(res)

# Summary statistics
cat("
=== Summary ===
")
cat("Pooled estimate:", coef(res), "
")
cat("95% CI:", res$ci.lb, "to", res$ci.ub, "
")
cat("SE:", res$se, "
")
cat("z-value:", res$zval, "
")
cat("p-value:", res$pval, "
")

# Back-transform if log scale (RR, OR, HR)
cat("
Exponentiated (RR/OR/HR):", exp(coef(res)), "
")
cat("95% CI:", exp(res$ci.lb), "to", exp(res$ci.ub), "
")

# ================================================================
# HETEROGENEITY
# ================================================================
cat("
=== Heterogeneity ===
")
cat("tau^2 (between-study variance):", res$tau2, "
")
cat("tau (SD):", sqrt(res$tau2), "
")
cat("I^2 (inconsistency):", res$I2, "%
")
cat("H^2:", res$H2, "
")
cat("Q-statistic:", res$QE, "
")
cat("Q df:", res$k - 1, "
")
cat("Q p-value:", res$QEp, "
")

# Prediction interval (where future studies might fall)
pi <- predict(res)
cat("
95% Prediction Interval:", pi$pi.lb, "to", pi$pi.ub, "
")

# ================================================================
# HKSJ ADJUSTMENT (Recommended for k < 20)
# ================================================================
res_hksj <- rma(yi, vi, data = dat, method = "REML", test = "knha", slab = study)
cat("
=== With Hartung-Knapp-Sidik-Jonkman Adjustment ===
")
print(res_hksj)

# ================================================================
# COMPARE ALL TAU^2 ESTIMATORS
# ================================================================
cat("
=== Tau^2 Estimator Comparison ===
")
estimators <- c("DL", "REML", "ML", "PM", "HS", "SJ", "HE", "EB")
for (m in estimators) {
  r <- try(rma(yi, vi, data = dat, method = m), silent = TRUE)
  if (!inherits(r, "try-error")) {
    cat(sprintf("%-6s: tau^2 = %.6f, pooled = %.4f
", m, r$tau2, coef(r)))
  }
}

# ================================================================
# FOREST PLOT
# ================================================================
cat("
=== Generating Forest Plot ===
")

# Basic forest plot
forest(res, header = TRUE, xlim = c(-4, 3),
       xlab = "Effect Size (log scale)")

# Enhanced forest plot with more details
forest(res, header = TRUE,
       atransf = exp,  # Back-transform to RR/OR scale
       at = log(c(0.1, 0.25, 0.5, 1, 2, 4)),
       xlim = c(-6, 4),
       ilab = cbind(dat$ai, dat$n1, dat$ci, dat$n2),
       ilab.xpos = c(-4.5, -3.5, -2.5, -1.5),
       cex = 0.8,
       xlab = "Risk Ratio")

# Add column headers
text(c(-4.5, -3.5, -2.5, -1.5), res$k + 2,
     c("Events", "Total", "Events", "Total"), cex = 0.7)
text(c(-4, -2), res$k + 3, c("Treatment", "Control"), cex = 0.8)

# ================================================================
# FUNNEL PLOT
# ================================================================
cat("
=== Generating Funnel Plot ===
")

# Basic funnel plot
funnel(res, main = "Funnel Plot")

# Enhanced funnel plot with contours
funnel(res, level = c(90, 95, 99), shade = c("white", "gray75", "gray60"),
       refline = 0, legend = TRUE)

# ================================================================
# PUBLICATION BIAS TESTS
# ================================================================
cat("
=== Publication Bias Assessment ===
")

# Egger's regression test
cat("
Egger's Test:
")
regtest(res)

# Rank correlation test (Begg & Mazumdar)
cat("
Rank Correlation Test:
")
ranktest(res)

# Trim and fill
cat("
Trim and Fill:
")
tf <- trimfill(res)
print(tf)
funnel(tf, main = "Funnel Plot with Trim and Fill")

# ================================================================
# INFLUENCE DIAGNOSTICS
# ================================================================
cat("
=== Influence Diagnostics ===
")

# Leave-one-out analysis
loo <- leave1out(res)
print(loo)

# Forest plot of leave-one-out
forest(loo, xlab = "Pooled Estimate (excluding study)")

# Influence plot
inf <- influence(res)
plot(inf)

# ================================================================
# BAUJAT PLOT (Contribution to heterogeneity)
# ================================================================
cat("
=== Baujat Plot ===
")
baujat(res, main = "Baujat Plot: Contribution to Heterogeneity")

# ================================================================
# GALBRAITH (RADIAL) PLOT
# ================================================================
cat("
=== Galbraith/Radial Plot ===
")
radial(res, main = "Radial Plot")

# ================================================================
# CUMULATIVE META-ANALYSIS
# ================================================================
cat("
=== Cumulative Meta-Analysis ===
")

# By publication year (if available)
cum <- cumul(res, order = dat$year)
print(cum)
forest(cum, xlab = "Cumulative Effect Size")

# ================================================================
# L'ABBE PLOT (Binary outcomes only)
# ================================================================
cat("
=== L'Abbe Plot ===
")
labbe(res, main = "L'Abbe Plot",
      xlab = "Event rate (Control)",
      ylab = "Event rate (Treatment)")

# ================================================================
# BUBBLE PLOT / META-REGRESSION
# ================================================================
cat("
=== Meta-Regression (Year as Moderator) ===
")

# Meta-regression with year
res_mr <- rma(yi, vi, mods = ~ year, data = dat, method = "REML")
print(res_mr)

# Bubble plot
regplot(res_mr, xlab = "Publication Year",
        main = "Meta-Regression: Effect over Time")

# Test for time trend
cat("
Time trend coefficient:", coef(res_mr)[2], "
")
cat("p-value:", res_mr$pval[2], "
")

# ================================================================
# SENSITIVITY ANALYSES
# ================================================================
cat("
=== Sensitivity Analyses ===
")

# Fixed-effect model for comparison
res_fe <- rma(yi, vi, data = dat, method = "FE")
cat("
Fixed-effect estimate:", coef(res_fe), "
")
cat("Random-effects estimate:", coef(res), "
")

# Profile likelihood CI for tau^2
profile(res, main = "Profile Likelihood for tau^2")

# ================================================================
# EXPORT RESULTS
# ================================================================
cat("
=== Export Results ===
")

# Create results summary table
results_table <- data.frame(
  Statistic = c("Pooled Effect", "95% CI Lower", "95% CI Upper",
                "Tau^2", "I^2 (%)", "Q", "p-value"),
  Value = c(coef(res), res$ci.lb, res$ci.ub,
            res$tau2, res$I2, res$QE, res$QEp)
)
print(results_table)

# Save to CSV
write.csv(results_table, "meta_analysis_results.csv", row.names = FALSE)
write.csv(dat, "study_data.csv", row.names = FALSE)
cat("Results saved to meta_analysis_results.csv
")

# ================================================================
# SESSION INFO (for reproducibility)
# ================================================================
cat("
=== Session Info ===
")
sessionInfo()

# ================================================================
# END OF ANALYSIS
# Generated by TruthCert-PairwisePro
# For publication, cite: metafor package
# Viechtbauer, W. (2010). Conducting meta-analyses in R with the
# metafor package. Journal of Statistical Software, 36(3), 1-48.
# ================================================================
