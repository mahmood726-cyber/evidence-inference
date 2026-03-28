# Extract trials from metadat R package
# Output: JSON file with real RCT trials

library(jsonlite)

# Install/load metadat
if (!require(metadat, quietly = TRUE)) {
  install.packages("metadat", repos = "https://cloud.r-project.org")
  library(metadat)
}

cat("=" , rep("=", 79), "\n", sep="")
cat("  EXTRACTING TRIALS FROM METADAT PACKAGE\n")
cat("=", rep("=", 79), "\n\n", sep="")

# List all datasets
all_datasets <- data(package = "metadat")$results[, "Item"]
cat("Found", length(all_datasets), "datasets in metadat\n\n")

all_trials <- list()
trial_count <- 0

# Process key datasets with binary outcomes (RR, OR)
binary_datasets <- c("dat.bcg", "dat.colditz1994", "dat.hackshaw1998",
                     "dat.yusuf1985", "dat.linde2015", "dat.hart1999")

# Process key datasets with continuous outcomes (MD, SMD)
continuous_datasets <- c("dat.normand1999", "dat.berkey1998", "dat.senn2013",
                         "dat.konstantopoulos2011", "dat.raudenbush1985")

process_dataset <- function(dataset_name) {
  tryCatch({
    # Load dataset
    data(list = dataset_name, package = "metadat", envir = environment())
    df <- get(dataset_name)

    if (!is.data.frame(df)) return(NULL)

    cat("Processing:", dataset_name, "- Rows:", nrow(df), "\n")

    trials <- list()

    for (i in 1:nrow(df)) {
      row <- df[i, ]

      # Try to extract effect and CI
      effect_val <- NA
      ci_lo <- NA
      ci_hi <- NA
      effect_type <- "MD"
      n_treat <- 100
      n_ctrl <- 100
      study <- paste0(dataset_name, "_", i)

      # Check for different column naming conventions
      if ("yi" %in% names(row)) effect_val <- as.numeric(row$yi)
      if ("vi" %in% names(row)) {
        # Calculate CI from variance
        se <- sqrt(as.numeric(row$vi))
        if (!is.na(effect_val) && !is.na(se)) {
          ci_lo <- effect_val - 1.96 * se
          ci_hi <- effect_val + 1.96 * se
        }
      }

      # Binary outcome columns (tpos, tneg, cpos, cneg)
      if (all(c("tpos", "tneg", "cpos", "cneg") %in% names(row))) {
        tpos <- as.numeric(row$tpos)
        tneg <- as.numeric(row$tneg)
        cpos <- as.numeric(row$cpos)
        cneg <- as.numeric(row$cneg)

        n_treat <- tpos + tneg
        n_ctrl <- cpos + cneg

        # Calculate RR
        if (n_treat > 0 && n_ctrl > 0 && (tpos + cpos) > 0) {
          p_treat <- tpos / n_treat
          p_ctrl <- cpos / n_ctrl

          if (p_ctrl > 0 && p_treat > 0) {
            effect_val <- log(p_treat / p_ctrl)  # log RR
            # SE for log RR
            se <- sqrt(1/tpos - 1/n_treat + 1/cpos - 1/n_ctrl)
            ci_lo <- effect_val - 1.96 * se
            ci_hi <- effect_val + 1.96 * se

            # Convert back from log scale
            effect_val <- exp(effect_val)
            ci_lo <- exp(ci_lo)
            ci_hi <- exp(ci_hi)
            effect_type <- "RR"
          }
        }
      }

      # OR columns
      if ("or" %in% names(row)) {
        effect_val <- as.numeric(row$or)
        effect_type <- "OR"
        if ("or.lb" %in% names(row)) ci_lo <- as.numeric(row$or.lb)
        if ("or.ub" %in% names(row)) ci_hi <- as.numeric(row$or.ub)
      }

      # Continuous outcome columns
      if (all(c("n1i", "m1i", "sd1i", "n2i", "m2i", "sd2i") %in% names(row))) {
        n_treat <- as.numeric(row$n1i)
        n_ctrl <- as.numeric(row$n2i)
        m1 <- as.numeric(row$m1i)
        m2 <- as.numeric(row$m2i)
        sd1 <- as.numeric(row$sd1i)
        sd2 <- as.numeric(row$sd2i)

        effect_val <- m1 - m2  # Mean difference
        se <- sqrt(sd1^2/n_treat + sd2^2/n_ctrl)
        ci_lo <- effect_val - 1.96 * se
        ci_hi <- effect_val + 1.96 * se
        effect_type <- "MD"
      }

      # Author/study name
      if ("author" %in% names(row)) study <- as.character(row$author)
      if ("study" %in% names(row)) study <- as.character(row$study)
      if ("trial" %in% names(row)) study <- as.character(row$trial)

      # Sample sizes from ni column
      if ("ni" %in% names(row)) {
        ni <- as.numeric(row$ni)
        n_treat <- ceiling(ni / 2)
        n_ctrl <- floor(ni / 2)
      }

      # Skip invalid entries
      if (is.na(effect_val) || is.na(ci_lo) || is.na(ci_hi)) next
      if (ci_lo >= ci_hi) next
      if (!is.finite(effect_val) || !is.finite(ci_lo) || !is.finite(ci_hi)) next

      trial <- list(
        id = paste0("METADAT-", dataset_name, "-", sprintf("%03d", i)),
        study = study,
        source_dataset = dataset_name,
        effect_type = effect_type,
        effect_value = round(effect_val, 4),
        ci_lo = round(ci_lo, 4),
        ci_hi = round(ci_hi, 4),
        n_treatment = as.integer(n_treat),
        n_control = as.integer(n_ctrl),
        domain = "General Medicine",
        source = "metadat"
      )

      trials[[length(trials) + 1]] <- trial
    }

    return(trials)

  }, error = function(e) {
    cat("Error processing", dataset_name, ":", e$message, "\n")
    return(NULL)
  })
}

# Process all available datasets
all_trials <- list()

for (ds in all_datasets) {
  trials <- process_dataset(ds)
  if (!is.null(trials) && length(trials) > 0) {
    all_trials <- c(all_trials, trials)
  }
}

cat("\n--- EXTRACTION COMPLETE ---\n")
cat("Total trials extracted:", length(all_trials), "\n")

# Count by effect type
effect_counts <- table(sapply(all_trials, function(x) x$effect_type))
cat("\nEffect type distribution:\n")
for (et in names(effect_counts)) {
  cat(" ", et, ":", effect_counts[et], "\n")
}

# Save to JSON
output_path <- "C:/Users/user/metadat_trials.json"
json_output <- toJSON(all_trials, auto_unbox = TRUE, pretty = TRUE)
writeLines(json_output, output_path)
cat("\nSaved to:", output_path, "\n")

cat("\n", rep("=", 80), "\n", sep="")
cat("  METADAT EXTRACTION COMPLETE\n")
cat(rep("=", 80), "\n", sep="")
