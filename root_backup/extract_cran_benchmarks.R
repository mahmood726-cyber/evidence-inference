# Extract CRAN Benchmark Datasets for ASReview 5-Star
# Phase 1.3: Add metafor and meta package datasets

library(data.table)

cat("=" , rep("=", 58), "\n", sep = "")
cat("CRAN Benchmark Datasets Extraction\n")
cat("=" , rep("=", 58), "\n\n", sep = "")

# ========================================
# Load metafor package datasets
# ========================================

cat("Loading metafor package...\n")
library(metafor)

# Get all dataset names from metafor
metafor_datasets <- data(package = "metafor")$results[, "Item"]
cat("metafor datasets available:", length(metafor_datasets), "\n\n")

all_metafor <- list()

for (ds_name in metafor_datasets) {
  tryCatch({
    # Load the dataset
    data(list = ds_name, package = "metafor")
    d <- get(ds_name)

    if (is.data.frame(d)) {
      n_rows <- nrow(d)

      # Create standardized record
      metafor_record <- data.table(
        dataset_name = ds_name,
        n_studies = n_rows,
        package = "metafor",
        source = "CRAN",
        has_author = "author" %in% tolower(names(d)),
        has_year = "year" %in% tolower(names(d)),
        has_yi = "yi" %in% names(d),
        has_vi = "vi" %in% names(d)
      )

      all_metafor[[ds_name]] <- metafor_record

      # Also save the actual dataset
      if (n_rows >= 5) {
        # Standardize columns
        d$dataset_name <- ds_name
        d$source <- "metafor"
        d$label_included <- 1L  # All studies in metafor are included

        fwrite(as.data.table(d),
               paste0("C:/Users/user/cran_datasets/metafor_", ds_name, ".csv"))
      }
    }
  }, error = function(e) {
    cat("  Error loading", ds_name, ":", conditionMessage(e), "\n")
  })
}

cat("Processed metafor datasets:", length(all_metafor), "\n")

# ========================================
# Load meta package datasets
# ========================================

cat("\nLoading meta package...\n")

tryCatch({
  library(meta)

  meta_datasets <- data(package = "meta")$results[, "Item"]
  cat("meta datasets available:", length(meta_datasets), "\n")

  for (ds_name in meta_datasets) {
    tryCatch({
      data(list = ds_name, package = "meta")
      d <- get(ds_name)

      if (is.data.frame(d)) {
        meta_record <- data.table(
          dataset_name = ds_name,
          n_studies = nrow(d),
          package = "meta",
          source = "CRAN",
          has_author = "author" %in% tolower(names(d)),
          has_year = "year" %in% tolower(names(d)),
          has_yi = FALSE,
          has_vi = FALSE
        )

        all_metafor[[paste0("meta_", ds_name)]] <- meta_record

        # Save the dataset
        d$dataset_name <- ds_name
        d$source <- "meta"
        d$label_included <- 1L

        fwrite(as.data.table(d),
               paste0("C:/Users/user/cran_datasets/meta_", ds_name, ".csv"))
      }
    }, error = function(e) NULL)
  }
}, error = function(e) {
  cat("meta package not installed\n")
})

# ========================================
# Summary
# ========================================

dir.create("C:/Users/user/cran_datasets", showWarnings = FALSE)

if (length(all_metafor) > 0) {
  cran_summary <- rbindlist(all_metafor, fill = TRUE)

  cat("\n")
  cat("=" , rep("=", 58), "\n", sep = "")
  cat("CRAN BENCHMARK SUMMARY\n")
  cat("=" , rep("=", 58), "\n", sep = "")

  cat("Total datasets:", nrow(cran_summary), "\n")
  cat("Total studies:", sum(cran_summary$n_studies), "\n")
  cat("metafor datasets:", sum(cran_summary$package == "metafor"), "\n")
  cat("meta datasets:", sum(cran_summary$package == "meta", na.rm = TRUE), "\n")

  # Save summary
  fwrite(cran_summary, "C:/Users/user/cran_datasets/cran_summary.csv")
  cat("\nSaved to: C:/Users/user/cran_datasets/\n")

  # Print top datasets by size
  cat("\nTop 10 datasets by size:\n")
  print(cran_summary[order(-n_studies)][1:10])
}

cat("\n")
cat("=" , rep("=", 58), "\n", sep = "")
cat("CRAN extraction complete!\n")
cat("=" , rep("=", 58), "\n", sep = "")
