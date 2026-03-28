
#' @export
mafi_signals <- function(yi, vi, sei = NULL) {
  if (is.null(sei)) sei <- sqrt(vi)
  n <- length(yi)
  signals <- list(
    n_studies = n, re_estimate = NA, re_se = NA, re_pval = NA,
    tau2 = NA, i_squared = NA, egger_z = NA, egger_pval = NA,
    pet_intercept = NA, pet_intercept_se = NA, begg_tau = NA, begg_pval = NA,
    taf_k0 = NA, taf_k0_ratio = NA, taf_estimate = NA, taf_side = NA,
    sel_estimate = NA, sel_lrt_pval = NA, sel_estimate_05 = NA, sel_lrt_pval_05 = NA,
    sel_beta_estimate = NA, sel_beta_pval = NA, sel_min_pval = NA, sel_min_pval_adjusted = NA,
    obs_sig = NA, exp_sig = NA, excess_sig_ratio = NA, excess_sig_pval = NA,
    small_study_effect = NA, small_study_direction = NA, small_study_magnitude = NA,
    precision_effect_cor = NA
  )
  if (n < 5) { signals[["error"]] <- "Fewer than 5 studies"; class(signals) <- c("mafi_signals", "list"); return(signals) }
  tryCatch({
    re <- metafor::rma(yi = yi, vi = vi, method = "REML")
    theta <- as.numeric(re[["beta"]])
    signals[["re_estimate"]] <- theta; signals[["re_se"]] <- re[["se"]]; signals[["re_pval"]] <- re[["pval"]]
    signals[["tau2"]] <- re[["tau2"]]; signals[["i_squared"]] <- re[["I2"]]
    tryCatch({ egger <- metafor::regtest(re, model = "lm"); signals[["egger_z"]] <- as.numeric(egger[["zval"]]); signals[["egger_pval"]] <- egger[["pval"]] }, error = function(e) {})
    tryCatch({ pet <- metafor::rma(yi = yi, vi = vi, mods = ~ sei, method = "REML"); signals[["pet_intercept"]] <- as.numeric(pet[["beta"]][1]); signals[["pet_intercept_se"]] <- pet[["se"]][1] }, error = function(e) {})
    tryCatch({ begg <- metafor::ranktest(re); signals[["begg_tau"]] <- as.numeric(begg[["tau"]]); signals[["begg_pval"]] <- begg[["pval"]] }, error = function(e) {})
    tryCatch({ taf <- metafor::trimfill(re); signals[["taf_k0"]] <- taf[["k0"]]; signals[["taf_k0_ratio"]] <- taf[["k0"]]/n; signals[["taf_estimate"]] <- as.numeric(taf[["beta"]]); signals[["taf_side"]] <- taf[["side"]] }, error = function(e) {})
    tryCatch({
      re_ml <- metafor::rma(yi = yi, vi = vi, method = "ML"); sel_pvals <- c()
      tryCatch({ sel1 <- metafor::selmodel(re_ml, type = "stepfun", steps = c(0.025)); signals[["sel_estimate"]] <- as.numeric(sel1[["beta"]]); signals[["sel_lrt_pval"]] <- sel1[["LRTp"]]; sel_pvals <- c(sel_pvals, sel1[["LRTp"]]) }, error = function(e) {})
      tryCatch({ sel2 <- metafor::selmodel(re_ml, type = "stepfun", steps = c(0.05)); signals[["sel_estimate_05"]] <- as.numeric(sel2[["beta"]]); signals[["sel_lrt_pval_05"]] <- sel2[["LRTp"]]; sel_pvals <- c(sel_pvals, sel2[["LRTp"]]) }, error = function(e) {})
      if (n >= 10) tryCatch({ sel3 <- metafor::selmodel(re_ml, type = "beta"); signals[["sel_beta_estimate"]] <- as.numeric(sel3[["beta"]]); signals[["sel_beta_pval"]] <- sel3[["LRTp"]]; sel_pvals <- c(sel_pvals, sel3[["LRTp"]]) }, error = function(e) {})
      if (length(sel_pvals) > 0) { signals[["sel_min_pval"]] <- min(sel_pvals); signals[["sel_min_pval_adjusted"]] <- min(1, min(sel_pvals) * length(sel_pvals)) }
    }, error = function(e) {})
    tryCatch({
      z_crit <- qnorm(0.975); power <- pnorm(abs(theta)/sei - z_crit); power[power < 0.05] <- 0.05; power[power > 0.95] <- 0.95
      obs_sig <- sum(abs(yi/sei) > z_crit); exp_sig <- sum(power)
      signals[["obs_sig"]] <- obs_sig; signals[["exp_sig"]] <- exp_sig; signals[["excess_sig_ratio"]] <- obs_sig/max(exp_sig, 1)
      if (exp_sig >= 1 && exp_sig <= n-1) { bt <- binom.test(obs_sig, n, p = exp_sig/n, alternative = "greater"); signals[["excess_sig_pval"]] <- bt[["p.value"]] }
    }, error = function(e) {})
    tryCatch({
      tercile <- quantile(sei, c(1/3, 2/3)); small_idx <- sei > tercile[2]; large_idx <- sei < tercile[1]
      if (sum(small_idx) >= 2 && sum(large_idx) >= 2) {
        small_eff <- weighted.mean(yi[small_idx], 1/vi[small_idx]); large_eff <- weighted.mean(yi[large_idx], 1/vi[large_idx])
        signals[["small_study_effect"]] <- small_eff - large_eff; signals[["small_study_magnitude"]] <- abs(small_eff - large_eff)
        if (theta > 0) { signals[["small_study_direction"]] <- ifelse(small_eff > large_eff, "inflated", "deflated")
        } else if (theta < 0) { signals[["small_study_direction"]] <- ifelse(small_eff < large_eff, "inflated", "deflated")
        } else { signals[["small_study_direction"]] <- "neutral" }
      }
    }, error = function(e) {})
    tryCatch({ signals[["precision_effect_cor"]] <- if(theta >= 0) cor(1/sei, yi, method = "spearman") else cor(1/sei, -yi, method = "spearman") }, error = function(e) {})
  }, error = function(e) { signals[["error"]] <- as.character(e) })
  class(signals) <- c("mafi_signals", "list"); return(signals)
}
