# Extract study-level metadata from Pairwise70 for PubMed search validation
# This creates ground truth data for ASReview training

library(data.table)

cat("=== Pairwise70 Metadata Extraction for ASReview Training ===\n\n")

# Get all RDS files
rds_dir <- "C:/Users/user/OneDrive - NHS/Documents/Pairwise70/analysis/output/cleaned_rds"
rds_files <- list.files(rds_dir, pattern = "\\.rds$", full.names = TRUE)

cat("Found", length(rds_files), "Cochrane review datasets\n\n")

# Function to extract unique studies from a dataset
extract_studies <- function(file_path) {
  d <- readRDS(file_path)

  # Get review ID from filename
  review_id <- gsub("_data\\.rds$", "", basename(file_path))

  # Extract study info
  if ("Study" %in% names(d)) {
    studies <- unique(d$Study)
    years <- if ("Study year" %in% names(d)) d$`Study year` else NA

    # Parse author and year from Study column (format: "Author 2020" or "Author 2020a")
    parsed <- data.table(
      review_id = review_id,
      study_label = studies,
      raw_text = studies
    )

    # Extract year from study label
    parsed[, year := as.numeric(gsub(".*\\b(19|20)([0-9]{2}).*", "\\1\\2", raw_text))]
    parsed[, author := gsub("\\s*(19|20)[0-9]{2}.*$", "", raw_text)]

    return(parsed)
  }
  return(NULL)
}

# Process first 10 reviews as sample
sample_files <- head(rds_files, 10)
all_studies <- rbindlist(lapply(sample_files, function(f) {
  tryCatch(extract_studies(f), error = function(e) NULL)
}), fill = TRUE)

cat("=== Sample Dataset Structure ===\n")
cat("Total unique studies extracted:", nrow(all_studies), "\n")
cat("Reviews sampled:", length(unique(all_studies$review_id)), "\n\n")

cat("=== First 20 Studies ===\n")
print(head(all_studies[, .(review_id, author, year, study_label)], 20))

cat("\n=== Year Distribution ===\n")
print(table(all_studies$year, useNA = "ifany"))

cat("\n=== Column Names in First Dataset ===\n")
d1 <- readRDS(rds_files[1])
print(names(d1))

# Check for DOI/PMID columns
cat("\n=== Looking for identifiers ===\n")
id_cols <- grep("doi|pmid|pubmed|url", names(d1), ignore.case = TRUE, value = TRUE)
cat("ID columns found:", paste(id_cols, collapse = ", "), "\n")

if (length(id_cols) > 0) {
  cat("\nSample values:\n")
  for (col in id_cols) {
    cat(paste0(col, ": "), head(unique(d1[[col]]), 3), "\n")
  }
}

# Save full extraction
cat("\n=== Processing ALL reviews ===\n")
all_studies_full <- rbindlist(lapply(rds_files, function(f) {
  tryCatch(extract_studies(f), error = function(e) NULL)
}), fill = TRUE)

cat("Total reviews:", length(unique(all_studies_full$review_id)), "\n")
cat("Total study entries:", nrow(all_studies_full), "\n")
cat("Unique studies:", nrow(unique(all_studies_full[, .(author, year)])), "\n")

# Save to CSV for PubMed searching
fwrite(all_studies_full, "C:/Users/user/pairwise70_study_metadata.csv")
cat("\nSaved to: C:/Users/user/pairwise70_study_metadata.csv\n")
