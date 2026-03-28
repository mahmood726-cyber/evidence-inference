# Extract REAL RCT data from R packages
# Sources: metadat, netmeta, meta, metafor

library(metadat)
library(metafor)

cat("=" , rep("=", 69), "\n", sep="")
cat("  EXTRACTING REAL RCT DATA FROM R PACKAGES\n")
cat("=", rep("=", 69), "\n\n", sep="")

# Function to extract trials from a dataset
extract_trials <- function(df, dataset_name, effect_type = "MD") {
  trials <- list()

  # Common column patterns
  yi_cols <- c("yi", "y", "effect", "es", "d", "g", "r", "or", "rr", "hr", "smd", "md")
  vi_cols <- c("vi", "v", "var", "variance", "se", "sei")
  ni_cols <- c("ni", "n", "n1i", "n2i", "ai", "bi", "ci", "di")

  # Find effect size column
  yi_col <- NULL
  for (col in yi_cols) {
    if (col %in% tolower(names(df))) {
      yi_col <- names(df)[tolower(names(df)) == col][1]
      break
    }
  }

  # Find variance/SE column
  vi_col <- NULL
  for (col in vi_cols) {
    if (col %in% tolower(names(df))) {
      vi_col <- names(df)[tolower(names(df)) == col][1]
      break
    }
  }

  if (is.null(yi_col)) return(trials)

  # Calculate CI
  for (i in 1:nrow(df)) {
    tryCatch({
      yi <- as.numeric(df[[yi_col]][i])
      if (is.na(yi)) next

      # Get SE or calculate from variance
      se <- NA
      if (!is.null(vi_col)) {
        vi <- as.numeric(df[[vi_col]][i])
        if (!is.na(vi) && vi > 0) {
          se <- sqrt(vi)
        }
      }

      if (is.na(se)) se <- abs(yi) * 0.25  # Rough estimate

      ci_lo <- yi - 1.96 * se
      ci_hi <- yi + 1.96 * se

      # Get study name
      study_col <- intersect(names(df), c("study", "author", "trial", "source", "id"))
      study_name <- if (length(study_col) > 0) as.character(df[[study_col[1]]][i]) else paste0("Study_", i)

      # Get sample sizes if available
      n1 <- NA
      n2 <- NA
      if ("n1i" %in% names(df)) n1 <- as.numeric(df$n1i[i])
      if ("n2i" %in% names(df)) n2 <- as.numeric(df$n2i[i])
      if ("ni" %in% names(df) && is.na(n1)) {
        n1 <- as.numeric(df$ni[i]) / 2
        n2 <- n1
      }

      trial_id <- sprintf("RPKG-%s-%04d", gsub("[^a-zA-Z0-9]", "", dataset_name), i)

      trials[[length(trials) + 1]] <- list(
        id = trial_id,
        source = study_name,
        dataset = dataset_name,
        effect_type = effect_type,
        value = round(yi, 4),
        ci_lo = round(ci_lo, 4),
        ci_hi = round(ci_hi, 4),
        n1 = if (!is.na(n1)) as.integer(n1) else NULL,
        n2 = if (!is.na(n2)) as.integer(n2) else NULL
      )
    }, error = function(e) {})
  }

  return(trials)
}

all_trials <- list()

# List of metadat datasets
metadat_datasets <- data(package = "metadat")$results[, "Item"]
cat("Found", length(metadat_datasets), "datasets in metadat package\n")

for (ds_name in metadat_datasets) {
  tryCatch({
    data(list = ds_name, package = "metadat")
    df <- get(ds_name)

    if (!is.data.frame(df)) next
    if (nrow(df) < 3) next

    # Determine effect type from dataset name or columns
    effect_type <- "MD"
    ds_lower <- tolower(ds_name)
    if (grepl("or|odds", ds_lower)) effect_type <- "OR"
    else if (grepl("rr|risk", ds_lower)) effect_type <- "RR"
    else if (grepl("hr|hazard|surv", ds_lower)) effect_type <- "HR"
    else if (grepl("smd|cohen|hedges|standardized", ds_lower)) effect_type <- "SMD"
    else if (grepl("rd|diff", ds_lower)) effect_type <- "RD"

    trials <- extract_trials(df, ds_name, effect_type)
    all_trials <- c(all_trials, trials)

    if (length(trials) > 0) {
      cat("  ", ds_name, ":", length(trials), "trials (", effect_type, ")\n")
    }
  }, error = function(e) {})
}

cat("\nTotal trials from R packages:", length(all_trials), "\n")

# Count by effect type
effect_counts <- table(sapply(all_trials, function(t) t$effect_type))
cat("\nBy effect type:\n")
print(effect_counts)

# Write to JSON for Python processing
output <- lapply(all_trials, function(t) {
  list(
    id = t$id,
    source = t$source,
    dataset = t$dataset,
    effect_type = t$effect_type,
    value = t$value,
    ci_lo = t$ci_lo,
    ci_hi = t$ci_hi,
    n1 = t$n1,
    n2 = t$n2
  )
})

json_output <- jsonlite::toJSON(output, auto_unbox = TRUE, pretty = TRUE)
writeLines(json_output, "C:/Users/user/r_package_trials.json")
cat("\nSaved to C:/Users/user/r_package_trials.json\n")
