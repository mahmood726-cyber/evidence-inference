#!/usr/bin/env python3
"""Enhance the R export function with complete analysis code"""

print("=" * 70)
print("ENHANCING R CODE EXPORT")
print("=" * 70)

# Read the current app.js
with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Find the generateMetaforCode function and replace it with enhanced version
enhanced_function = '''
    /**
     * Generate comprehensive R/metafor code for complete reproducible analysis
     * Includes all plots: forest, funnel, bubble, baujat, influence, galbraith, cumulative, L'Abbe
     * @returns {string} Complete R script
     */
    function generateMetaforCode() {
      const studies = AppState.studies;
      if (!studies || studies.length < 2) {
        showToast('Need at least 2 studies to export', 'error');
        return null;
      }

      const method = (AppState.settings && AppState.settings.tau2Method) || 'REML';
      const dataType = AppState.dataType || 'binary';
      const date = new Date().toISOString().split('T')[0];

      // Check if we have raw binary data or pre-calculated effects
      const hasBinaryData = studies[0].events_t !== undefined || studies[0].ai !== undefined;
      const hasPreCalc = studies[0].yi !== undefined;

      let code = `# ================================================================
# TruthCert-PairwisePro: Complete R Analysis Script
# Generated: ${date}
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

`;

      // Generate data frame based on data type
      if (hasBinaryData) {
        code += `# ================================================================
# STUDY DATA (Binary Outcomes)
# ================================================================
dat <- data.frame(
  study = c(${studies.map(s => '"' + (s.name || s.study || 'Study') + '"').join(',\\n           ')}),
  ai = c(${studies.map(s => s.events_t || s.ai || 0).join(', ')}),
  bi = c(${studies.map(s => (s.n_t || s.total1 || 0) - (s.events_t || s.ai || 0)).join(', ')}),
  ci = c(${studies.map(s => s.events_c || s.ci || 0).join(', ')}),
  di = c(${studies.map(s => (s.n_c || s.total2 || 0) - (s.events_c || s.ci || 0)).join(', ')}),
  n1 = c(${studies.map(s => s.n_t || s.total1 || 0).join(', ')}),
  n2 = c(${studies.map(s => s.n_c || s.total2 || 0).join(', ')})`;

        // Add year if available
        if (studies[0].year) {
          code += `,
  year = c(${studies.map(s => s.year || 2000).join(', ')})`;
        }
        code += `
)

# Calculate effect sizes (log Risk Ratio)
dat <- escalc(measure = "RR", ai = ai, bi = bi, ci = ci, di = di, data = dat)
# Alternative measures:
# escalc(measure = "OR", ...)  # Odds Ratio
# escalc(measure = "RD", ...)  # Risk Difference

`;
      } else if (hasPreCalc) {
        code += `# ================================================================
# STUDY DATA (Pre-calculated Effect Sizes)
# ================================================================
dat <- data.frame(
  study = c(${studies.map(s => '"' + (s.name || s.study || 'Study') + '"').join(',\\n           ')}),
  yi = c(${studies.map(s => (s.yi || 0).toFixed(6)).join(', ')}),
  vi = c(${studies.map(s => (s.vi || 0.01).toFixed(6)).join(', ')})`;

        if (studies[0].year) {
          code += `,
  year = c(${studies.map(s => s.year || 2000).join(', ')})`;
        }
        code += `
)

`;
      } else {
        // Continuous data
        code += `# ================================================================
# STUDY DATA (Continuous Outcomes)
# ================================================================
dat <- data.frame(
  study = c(${studies.map(s => '"' + (s.name || s.study || 'Study') + '"').join(',\\n           ')}),
  m1 = c(${studies.map(s => s.mean1 || s.m1 || 0).join(', ')}),
  sd1 = c(${studies.map(s => s.sd1 || 1).join(', ')}),
  n1 = c(${studies.map(s => s.n1 || s.total1 || 10).join(', ')}),
  m2 = c(${studies.map(s => s.mean2 || s.m2 || 0).join(', ')}),
  sd2 = c(${studies.map(s => s.sd2 || 1).join(', ')}),
  n2 = c(${studies.map(s => s.n2 || s.total2 || 10).join(', ')})
)

# Calculate standardized mean difference
dat <- escalc(measure = "SMD", m1i = m1, sd1i = sd1, n1i = n1,
              m2i = m2, sd2i = sd2, n2i = n2, data = dat)

`;
      }

      // Main analysis
      code += `# ================================================================
# MAIN META-ANALYSIS
# ================================================================

# Random-effects model with ${method} estimator
res <- rma(yi, vi, data = dat, method = "${method}", slab = study)
print(res)

# Summary statistics
cat("\\n=== Summary ===\\n")
cat("Pooled estimate:", coef(res), "\\n")
cat("95% CI:", res$ci.lb, "to", res$ci.ub, "\\n")
cat("SE:", res$se, "\\n")
cat("z-value:", res$zval, "\\n")
cat("p-value:", res$pval, "\\n")

# Back-transform if log scale (RR, OR, HR)
cat("\\nExponentiated (RR/OR/HR):", exp(coef(res)), "\\n")
cat("95% CI:", exp(res$ci.lb), "to", exp(res$ci.ub), "\\n")

# ================================================================
# HETEROGENEITY
# ================================================================
cat("\\n=== Heterogeneity ===\\n")
cat("tau^2 (between-study variance):", res$tau2, "\\n")
cat("tau (SD):", sqrt(res$tau2), "\\n")
cat("I^2 (inconsistency):", res$I2, "%\\n")
cat("H^2:", res$H2, "\\n")
cat("Q-statistic:", res$QE, "\\n")
cat("Q df:", res$k - 1, "\\n")
cat("Q p-value:", res$QEp, "\\n")

# Prediction interval (where future studies might fall)
pi <- predict(res)
cat("\\n95% Prediction Interval:", pi$pi.lb, "to", pi$pi.ub, "\\n")

# ================================================================
# HKSJ ADJUSTMENT (Recommended for k < 20)
# ================================================================
res_hksj <- rma(yi, vi, data = dat, method = "${method}", test = "knha", slab = study)
cat("\\n=== With Hartung-Knapp-Sidik-Jonkman Adjustment ===\\n")
print(res_hksj)

# ================================================================
# COMPARE ALL TAU^2 ESTIMATORS
# ================================================================
cat("\\n=== Tau^2 Estimator Comparison ===\\n")
estimators <- c("DL", "REML", "ML", "PM", "HS", "SJ", "HE", "EB")
for (m in estimators) {
  r <- try(rma(yi, vi, data = dat, method = m), silent = TRUE)
  if (!inherits(r, "try-error")) {
    cat(sprintf("%-6s: tau^2 = %.6f, pooled = %.4f\\n", m, r$tau2, coef(r)))
  }
}

# ================================================================
# FOREST PLOT
# ================================================================
cat("\\n=== Generating Forest Plot ===\\n")

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
cat("\\n=== Generating Funnel Plot ===\\n")

# Basic funnel plot
funnel(res, main = "Funnel Plot")

# Enhanced funnel plot with contours
funnel(res, level = c(90, 95, 99), shade = c("white", "gray75", "gray60"),
       refline = 0, legend = TRUE)

# ================================================================
# PUBLICATION BIAS TESTS
# ================================================================
cat("\\n=== Publication Bias Assessment ===\\n")

# Egger's regression test
cat("\\nEgger's Test:\\n")
regtest(res)

# Rank correlation test (Begg & Mazumdar)
cat("\\nRank Correlation Test:\\n")
ranktest(res)

# Trim and fill
cat("\\nTrim and Fill:\\n")
tf <- trimfill(res)
print(tf)
funnel(tf, main = "Funnel Plot with Trim and Fill")

# ================================================================
# INFLUENCE DIAGNOSTICS
# ================================================================
cat("\\n=== Influence Diagnostics ===\\n")

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
cat("\\n=== Baujat Plot ===\\n")
baujat(res, main = "Baujat Plot: Contribution to Heterogeneity")

# ================================================================
# GALBRAITH (RADIAL) PLOT
# ================================================================
cat("\\n=== Galbraith/Radial Plot ===\\n")
radial(res, main = "Radial Plot")

# ================================================================
# CUMULATIVE META-ANALYSIS
# ================================================================
cat("\\n=== Cumulative Meta-Analysis ===\\n")

# By publication year (if available)
${studies[0].year ? `cum <- cumul(res, order = dat$year)
print(cum)
forest(cum, xlab = "Cumulative Effect Size")` : `# Note: Year data not available for temporal cumulative analysis
cum <- cumul(res)
print(cum)
forest(cum, xlab = "Cumulative Effect Size")`}

# ================================================================
# L'ABBE PLOT (Binary outcomes only)
# ================================================================
${hasBinaryData ? `cat("\\n=== L'Abbe Plot ===\\n")
labbe(res, main = "L'Abbe Plot",
      xlab = "Event rate (Control)",
      ylab = "Event rate (Treatment)")` : `# L'Abbe plot requires binary outcome data`}

# ================================================================
# BUBBLE PLOT / META-REGRESSION
# ================================================================
${studies[0].year ? `cat("\\n=== Meta-Regression (Year as Moderator) ===\\n")

# Meta-regression with year
res_mr <- rma(yi, vi, mods = ~ year, data = dat, method = "${method}")
print(res_mr)

# Bubble plot
regplot(res_mr, xlab = "Publication Year",
        main = "Meta-Regression: Effect over Time")

# Test for time trend
cat("\\nTime trend coefficient:", coef(res_mr)[2], "\\n")
cat("p-value:", res_mr$pval[2], "\\n")` : `# Note: Add moderator variables for meta-regression bubble plot
# Example with simulated moderator:
# dat$moderator <- rnorm(nrow(dat))
# res_mr <- rma(yi, vi, mods = ~ moderator, data = dat)
# regplot(res_mr)`}

# ================================================================
# SENSITIVITY ANALYSES
# ================================================================
cat("\\n=== Sensitivity Analyses ===\\n")

# Fixed-effect model for comparison
res_fe <- rma(yi, vi, data = dat, method = "FE")
cat("\\nFixed-effect estimate:", coef(res_fe), "\\n")
cat("Random-effects estimate:", coef(res), "\\n")

# Profile likelihood CI for tau^2
profile(res, main = "Profile Likelihood for tau^2")

# ================================================================
# EXPORT RESULTS
# ================================================================
cat("\\n=== Export Results ===\\n")

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
cat("Results saved to meta_analysis_results.csv\\n")

# ================================================================
# SESSION INFO (for reproducibility)
# ================================================================
cat("\\n=== Session Info ===\\n")
sessionInfo()

# ================================================================
# END OF ANALYSIS
# Generated by TruthCert-PairwisePro
# For publication, cite: metafor package
# Viechtbauer, W. (2010). Conducting meta-analyses in R with the
# metafor package. Journal of Statistical Software, 36(3), 1-48.
# ================================================================
`;

      return code;
    }
'''

# Find the old generateMetaforCode function and replace it
import re

# Pattern to match the function
pattern = r'function generateMetaforCode\(\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}'

# Check if the function exists
if 'function generateMetaforCode' in content:
    # Find the function start
    start_idx = content.find('function generateMetaforCode')
    if start_idx != -1:
        # Find matching braces
        brace_count = 0
        end_idx = start_idx
        found_start = False
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                brace_count += 1
                found_start = True
            elif content[i] == '}':
                brace_count -= 1
                if found_start and brace_count == 0:
                    end_idx = i + 1
                    break

        # Replace the function
        old_func = content[start_idx:end_idx]
        print(f"Found generateMetaforCode function ({len(old_func)} chars)")
        print(f"Replacing with enhanced version ({len(enhanced_function)} chars)")

        content = content[:start_idx] + enhanced_function.strip() + content[end_idx:]

        # Write back
        with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
            f.write(content)

        print("\nSUCCESS: Enhanced R export function installed!")
        print("\nNew features:")
        print("  - Forest plot (basic and enhanced with event counts)")
        print("  - Funnel plot (with contour-enhanced version)")
        print("  - Publication bias tests (Egger, Begg, Trim-and-Fill)")
        print("  - Influence diagnostics and leave-one-out")
        print("  - Baujat plot (heterogeneity contribution)")
        print("  - Galbraith/Radial plot")
        print("  - Cumulative meta-analysis")
        print("  - L'Abbe plot (for binary data)")
        print("  - Bubble plot / Meta-regression")
        print("  - All tau^2 estimators comparison")
        print("  - HKSJ adjustment")
        print("  - Prediction intervals")
        print("  - CSV export of results")
        print("  - Session info for reproducibility")
else:
    print("ERROR: generateMetaforCode function not found in app.js")
    print("Will add new function...")

    # Find a good place to add it (near other export functions)
    insert_pos = content.find('function exportToR')
    if insert_pos != -1:
        content = content[:insert_pos] + enhanced_function + '\n\n    ' + content[insert_pos:]
        with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Added generateMetaforCode function!")

print("\n" + "=" * 70)
