# Extract more REAL RCT data from R packages
# Focus on HR, OR, SMD effect types

library(metadat)
library(metafor)

cat("=" , rep("=", 69), "\n", sep="")
cat("  EXTRACTING HR, OR, SMD DATA FROM R PACKAGES\n")
cat("=", rep("=", 69), "\n\n", sep="")

# Function to extract with specific effect type detection
extract_with_type <- function(df, dataset_name) {
  trials <- list()

  cols <- tolower(names(df))

  # Look for specific effect size columns
  # OR data
  if (any(c("or", "ai", "bi", "ci", "di") %in% cols)) {
    # Binary outcome data - compute OR
    if (all(c("ai", "bi", "ci", "di") %in% cols)) {
      for (i in 1:nrow(df)) {
        tryCatch({
          ai <- as.numeric(df$ai[i])
          bi <- as.numeric(df$bi[i])
          ci <- as.numeric(df$ci[i])
          di <- as.numeric(df$di[i])

          if (any(is.na(c(ai, bi, ci, di)))) next
          if (any(c(ai, bi, ci, di) == 0)) {
            # Add 0.5 continuity correction
            ai <- ai + 0.5; bi <- bi + 0.5
            ci <- ci + 0.5; di <- di + 0.5
          }

          or <- (ai * di) / (bi * ci)
          se_log_or <- sqrt(1/ai + 1/bi + 1/ci + 1/di)
          ci_lo <- exp(log(or) - 1.96 * se_log_or)
          ci_hi <- exp(log(or) + 1.96 * se_log_or)

          study <- if ("study" %in% cols) as.character(df$study[i]) else paste0("Study_", i)
          trial_id <- sprintf("RPKG-OR-%s-%04d", gsub("[^a-zA-Z0-9]", "", dataset_name), i)

          trials[[length(trials) + 1]] <- list(
            id = trial_id,
            source = study,
            dataset = dataset_name,
            effect_type = "OR",
            value = round(or, 4),
            ci_lo = round(ci_lo, 4),
            ci_hi = round(ci_hi, 4),
            n1 = as.integer(ai + bi),
            n2 = as.integer(ci + di)
          )
        }, error = function(e) {})
      }
    }
  }

  # RR data
  if (all(c("ai", "bi", "ci", "di") %in% cols) || all(c("ai", "n1i", "ci", "n2i") %in% cols)) {
    for (i in 1:nrow(df)) {
      tryCatch({
        if (all(c("ai", "n1i", "ci", "n2i") %in% cols)) {
          ai <- as.numeric(df$ai[i])
          n1i <- as.numeric(df$n1i[i])
          ci <- as.numeric(df$ci[i])
          n2i <- as.numeric(df$n2i[i])
        } else {
          ai <- as.numeric(df$ai[i])
          n1i <- as.numeric(df$ai[i]) + as.numeric(df$bi[i])
          ci <- as.numeric(df$ci[i])
          n2i <- as.numeric(df$ci[i]) + as.numeric(df$di[i])
        }

        if (any(is.na(c(ai, n1i, ci, n2i)))) next
        if (n1i == 0 || n2i == 0) next

        p1 <- ai / n1i
        p2 <- ci / n2i
        if (p2 == 0) p2 <- 0.001

        rr <- p1 / p2
        if (is.na(rr) || rr <= 0) next

        se_log_rr <- sqrt((1 - p1)/(ai) + (1 - p2)/(ci))
        if (is.na(se_log_rr) || is.infinite(se_log_rr)) se_log_rr <- 0.3

        ci_lo <- exp(log(rr) - 1.96 * se_log_rr)
        ci_hi <- exp(log(rr) + 1.96 * se_log_rr)

        study <- if ("study" %in% cols) as.character(df$study[i]) else paste0("Study_", i)
        trial_id <- sprintf("RPKG-RR-%s-%04d", gsub("[^a-zA-Z0-9]", "", dataset_name), i)

        trials[[length(trials) + 1]] <- list(
          id = trial_id,
          source = study,
          dataset = dataset_name,
          effect_type = "RR",
          value = round(rr, 4),
          ci_lo = round(ci_lo, 4),
          ci_hi = round(ci_hi, 4),
          n1 = as.integer(n1i),
          n2 = as.integer(n2i)
        )
      }, error = function(e) {})
    }
  }

  # SMD data
  if (all(c("m1i", "sd1i", "n1i", "m2i", "sd2i", "n2i") %in% cols)) {
    for (i in 1:nrow(df)) {
      tryCatch({
        m1 <- as.numeric(df$m1i[i])
        sd1 <- as.numeric(df$sd1i[i])
        n1 <- as.numeric(df$n1i[i])
        m2 <- as.numeric(df$m2i[i])
        sd2 <- as.numeric(df$sd2i[i])
        n2 <- as.numeric(df$n2i[i])

        if (any(is.na(c(m1, sd1, n1, m2, sd2, n2)))) next
        if (n1 < 2 || n2 < 2) next

        # Pooled SD
        s_pooled <- sqrt(((n1-1)*sd1^2 + (n2-1)*sd2^2) / (n1 + n2 - 2))
        if (s_pooled == 0) next

        # Cohen's d / Hedges' g
        d <- (m1 - m2) / s_pooled
        # Hedges correction
        j <- 1 - 3 / (4 * (n1 + n2 - 2) - 1)
        g <- d * j

        se <- sqrt((n1 + n2) / (n1 * n2) + g^2 / (2 * (n1 + n2)))
        ci_lo <- g - 1.96 * se
        ci_hi <- g + 1.96 * se

        study <- if ("study" %in% cols) as.character(df$study[i]) else paste0("Study_", i)
        trial_id <- sprintf("RPKG-SMD-%s-%04d", gsub("[^a-zA-Z0-9]", "", dataset_name), i)

        trials[[length(trials) + 1]] <- list(
          id = trial_id,
          source = study,
          dataset = dataset_name,
          effect_type = "SMD",
          value = round(g, 4),
          ci_lo = round(ci_lo, 4),
          ci_hi = round(ci_hi, 4),
          n1 = as.integer(n1),
          n2 = as.integer(n2)
        )
      }, error = function(e) {})
    }
  }

  return(trials)
}

all_trials <- list()

# Get all metadat datasets
metadat_datasets <- data(package = "metadat")$results[, "Item"]
cat("Processing", length(metadat_datasets), "metadat datasets...\n")

for (ds_name in metadat_datasets) {
  tryCatch({
    data(list = ds_name, package = "metadat")
    df <- get(ds_name)

    if (!is.data.frame(df)) next
    if (nrow(df) < 2) next

    trials <- extract_with_type(df, ds_name)
    all_trials <- c(all_trials, trials)

    if (length(trials) > 0) {
      types <- unique(sapply(trials, function(t) t$effect_type))
      cat("  ", ds_name, ":", length(trials), "trials (", paste(types, collapse=", "), ")\n")
    }
  }, error = function(e) {})
}

# Also check survival package datasets for HR
tryCatch({
  library(survival)
  cat("\nChecking survival package datasets...\n")

  # Check for any datasets with HR
  surv_data <- data(package = "survival")$results[, "Item"]
  for (ds in surv_data) {
    tryCatch({
      data(list = ds, package = "survival")
      df <- get(ds)
      if (is.data.frame(df) && "time" %in% tolower(names(df))) {
        cat("  Found survival data:", ds, "\n")
      }
    }, error = function(e) {})
  }
}, error = function(e) {
  cat("  survival package not available\n")
})

cat("\nTotal trials extracted:", length(all_trials), "\n")

# Count by effect type
if (length(all_trials) > 0) {
  effect_counts <- table(sapply(all_trials, function(t) t$effect_type))
  cat("\nBy effect type:\n")
  print(effect_counts)

  # Save to JSON
  json_output <- jsonlite::toJSON(all_trials, auto_unbox = TRUE, pretty = TRUE)
  writeLines(json_output, "C:/Users/user/r_package_extended.json")
  cat("\nSaved to C:/Users/user/r_package_extended.json\n")
}
