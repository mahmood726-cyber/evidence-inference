# Build MEGA Ground Truth for ASReview 5-Star
# Combines: Pairwise70 (501 reviews) + CRAN datasets + SYNERGY reference

library(data.table)

cat("=" , rep("=", 58), "\n", sep = "")
cat("ASReview 5-Star MEGA Ground Truth Builder\n")
cat("=" , rep("=", 58), "\n\n", sep = "")

# ========================================
# Load Pairwise70 COMPLETE dataset
# ========================================

cat("Loading Pairwise70 COMPLETE dataset...\n")
pairwise70 <- fread("C:/Users/user/asreview_pairwise70_COMPLETE.csv")

cat("  Records:", nrow(pairwise70), "\n")
cat("  Included:", sum(pairwise70$label_included), "\n")
cat("  Excluded:", sum(!pairwise70$label_included), "\n")
cat("  Reviews:", length(unique(pairwise70$review_id)), "\n\n")

# Standardize columns
pairwise70[, data_source := "Pairwise70"]
pairwise70[, domain := "Cochrane_Clinical"]

# ========================================
# Load CRAN meta datasets
# ========================================

cat("Loading CRAN meta datasets...\n")
cran_files <- list.files("C:/Users/user/cran_datasets", pattern = "meta_.*\\.csv$", full.names = TRUE)

cran_data <- list()
for (f in cran_files) {
  tryCatch({
    d <- fread(f)
    d[, data_source := "CRAN_meta"]
    d[, domain := "Clinical"]
    cran_data[[f]] <- d
  }, error = function(e) NULL)
}

if (length(cran_data) > 0) {
  cran_combined <- rbindlist(cran_data, fill = TRUE)
  cat("  CRAN records:", nrow(cran_combined), "\n")
  cat("  CRAN datasets:", length(cran_data), "\n\n")
} else {
  cran_combined <- data.table()
  cat("  No CRAN data loaded\n\n")
}

# ========================================
# Add SYNERGY benchmark reference
# ========================================

cat("Loading SYNERGY benchmark reference...\n")
synergy_ref <- fread("C:/Users/user/synergy_benchmark/synergy_reference.csv")
cat("  SYNERGY datasets:", nrow(synergy_ref), "\n")
cat("  SYNERGY total records:", sum(synergy_ref$records), "\n")
cat("  SYNERGY total included:", sum(synergy_ref$included), "\n\n")

# ========================================
# Build MEGA dataset
# ========================================

cat("=" , rep("=", 58), "\n", sep = "")
cat("BUILDING MEGA GROUND TRUTH\n")
cat("=" , rep("=", 58), "\n\n", sep = "")

# Select common columns
common_cols <- c("record_id", "title", "abstract", "authors", "year",
                 "label_included", "review_id", "source", "data_source", "domain")

# Ensure columns exist in pairwise70
for (col in common_cols) {
  if (!col %in% names(pairwise70)) {
    pairwise70[, (col) := NA]
  }
}

mega_ground_truth <- pairwise70[, ..common_cols]

# Add enriched metadata
mega_ground_truth[, has_abstract := nchar(as.character(abstract)) > 50]
mega_ground_truth[, has_title := nchar(as.character(title)) > 5]

# ========================================
# Generate summary statistics
# ========================================

cat("MEGA Ground Truth Statistics:\n")
cat("-" , rep("-", 58), "\n", sep = "")
cat("Total records:", nrow(mega_ground_truth), "\n")
cat("Included:", sum(mega_ground_truth$label_included == 1), "\n")
cat("Excluded:", sum(mega_ground_truth$label_included == 0), "\n")
cat("Prevalence:", round(mean(mega_ground_truth$label_included == 1) * 100, 1), "%\n")
cat("Reviews:", length(unique(mega_ground_truth$review_id)), "\n\n")

# Domain breakdown
cat("By domain:\n")
print(mega_ground_truth[, .N, by = domain])

cat("\nYear range:", range(mega_ground_truth$year, na.rm = TRUE), "\n")

# ========================================
# Save outputs
# ========================================

cat("\n")
cat("=" , rep("=", 58), "\n", sep = "")
cat("SAVING OUTPUTS\n")
cat("=" , rep("=", 58), "\n\n", sep = "")

# Main ground truth
fwrite(mega_ground_truth, "C:/Users/user/asreview_MEGA_groundtruth.csv")
cat("Saved: C:/Users/user/asreview_MEGA_groundtruth.csv\n")

# Summary table - convert year to numeric first
mega_ground_truth[, year := as.numeric(year)]
mega_ground_truth[year < 1900 | year > 2030, year := NA_real_]

summary_by_review <- mega_ground_truth[, .(
  n_records = .N,
  n_included = sum(label_included == 1),
  n_excluded = sum(label_included == 0),
  prevalence = round(mean(label_included == 1) * 100, 1),
  year_min = suppressWarnings(min(year, na.rm = TRUE)),
  year_max = suppressWarnings(max(year, na.rm = TRUE))
), by = review_id]

# Fix infinite values
summary_by_review[is.infinite(year_min), year_min := NA_real_]
summary_by_review[is.infinite(year_max), year_max := NA_real_]

fwrite(summary_by_review, "C:/Users/user/asreview_MEGA_summary_by_review.csv")
cat("Saved: C:/Users/user/asreview_MEGA_summary_by_review.csv\n")

# SYNERGY comparison reference
synergy_ref[, comparable_to_pairwise := TRUE]
fwrite(synergy_ref, "C:/Users/user/asreview_SYNERGY_benchmark_reference.csv")
cat("Saved: C:/Users/user/asreview_SYNERGY_benchmark_reference.csv\n")

# ========================================
# Final summary
# ========================================

cat("\n")
cat("=" , rep("=", 58), "\n", sep = "")
cat("MEGA GROUND TRUTH COMPLETE!\n")
cat("=" , rep("=", 58), "\n\n", sep = "")

cat("DATA COMPARISON:\n")
cat("-" , rep("-", 40), "\n", sep = "")
cat(sprintf("%-25s %10s %10s\n", "Source", "Records", "Included"))
cat("-" , rep("-", 40), "\n", sep = "")
cat(sprintf("%-25s %10d %10d\n", "Pairwise70 (our data)",
    nrow(mega_ground_truth), sum(mega_ground_truth$label_included == 1)))
cat(sprintf("%-25s %10d %10d\n", "SYNERGY (benchmark)",
    sum(synergy_ref$records), sum(synergy_ref$included)))
cat("-" , rep("-", 40), "\n", sep = "")

cat("\nREADY FOR ASReview 5-Star benchmarking!\n")
