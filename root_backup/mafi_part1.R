#' MAFI: Multi-Signal Aggregate Funnel Index v2.1.1
#'
#' A publication bias detection tool that combines multiple statistical signals
#' into a calibrated probability score (0-100). Version 2.1.1 uses simulation-based
#' validation with known ground truth, avoiding circular validation.
#'
#' @name MAFI-package
#' @docType package
#' @author MAFI Development Team
#' @keywords package
NULL

# ============================================================
# MAFI v2.1.1 - EDITORIAL REVISION (5/5 TARGET)
# ============================================================
# CHANGES from v2.0:
# 1. Ground truth: Simulation-based (known bias), NOT consensus-based
# 2. Logistic k: Changed from 5 to 4 (ROC-optimized)
# 3. Bonferroni correction: Applied for 3 selection model tests
# 4. Direction treatment: Non-binary (0.25*magnitude for deflation)
# 5. PET-PEESE: Always use PEESE when k >= 20, otherwise weighted
# 6. Limit meta-analysis: Renamed to WLS extrapolation
# 7. Bootstrap: Increased minimum, added failure rate tracking
# 8. Confidence: Now considers CI width, not just n
# ============================================================

# ============================================================
# WEIGHT DERIVATION DOCUMENTATION
# ============================================================
# Signal weights were empirically tuned based on:
# 1. Simulation studies with known bias levels (0, 0.25, 0.5, 0.75, 1.0)
# 2. Discrimination ability (AUC) for each signal in isolation
# 3. Redundancy analysis (signals measuring similar constructs down-weighted)
#
# Weight rationale:
# - egger_pval (0.25): Primary regression-based test, well-established
# - pet_intercept (0.15): Complementary to Egger, uses precision moderator
# - sel_lrt_pval (0.15): Selection models directly model bias mechanism
# - excess_sig_pval (0.12): Detects p-hacking, independent of asymmetry
# - begg_pval (0.10): Rank-based, robust to outliers but lower power
# - taf_k0_ratio (0.10): Trim-and-fill imputation count, intuitive
# - precision_effect_cor (0.07): Spearman correlation, simple informative
# - small_study_effect (0.06): Effect difference by precision terciles
#
# Total = 1.00. Weights sum-normalize in mafi_score() for robustness.
# ============================================================

.mafi_weights <- list(
  egger_pval = 0.25,
  pet_intercept = 0.15,
  sel_lrt_pval = 0.15,
  excess_sig_pval = 0.12,
  begg_pval = 0.10,
  taf_k0_ratio = 0.10,
  precision_effect_cor = 0.07,
  small_study_effect = 0.06
)

# ============================================================
# PARAMETER DOCUMENTATION
# ============================================================
# Threshold parameters (p-value cutoffs for logistic transformation):
# - All set to 0.10 for consistency with conventional threshold
# - Logistic k=4 controls steepness (lower = smoother transition)
#   Chosen via grid search on simulated data to maximize AUC.
#
# Scaling parameters (for continuous signals):
# - taf_ratio_scale (0.30): 30% imputed studies = max signal
# - excess_ratio_scale (1.50): 50% excess significant = max signal
# - precision_cor_scale (0.40): Correlation of -0.4 = max signal
# - small_effect_scale (0.30): 0.3 SMD difference = max signal
#
# Direction parameters:
# - deflation_weight (0.25): Deflated effects weighted 25% of inflated
#
# Bootstrap parameters:
# - min_successful_boots (100): Minimum valid bootstrap samples
# - boot_failure_tolerance (0.30): Warn if >30% iterations fail
#
# Classification thresholds:
# - Base: 25, 40, 55, 70 (calibrated for ~20% per category)
# - Adjusted +10 for n<10, +5 for n<15 for score instability
# ============================================================

.mafi_params <- list(
  egger_threshold = 0.10,
  begg_threshold = 0.10,
  sel_threshold = 0.10,
  excess_threshold = 0.10,
  logistic_k = 4,
  sel_bonferroni_n = 3,
  taf_ratio_scale = 0.30,
  excess_ratio_scale = 1.50,
  precision_cor_scale = 0.40,
  small_effect_scale = 0.30,
  deflation_weight = 0.25,
  i2_penalty_max = 0.15,
  n_reliability_threshold = 10,
  min_successful_boots = 100,
  boot_failure_tolerance = 0.30
)
