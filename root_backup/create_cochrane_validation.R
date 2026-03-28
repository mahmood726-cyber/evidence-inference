# Create RCTExtractor validation from 500+ Cochrane Reviews
library(jsonlite)

data_dir <- "C:/Users/user/OneDrive - NHS/Documents/Pairwise70/data"
files <- list.files(data_dir, pattern = "\\.rda$", full.names = TRUE)
cat("Total Cochrane datasets:", length(files), "\n")

# Extract data from all files
all_trials <- list()
trial_count <- 0

for (f in files) {
    tryCatch({
        env <- new.env()
        load(f, envir = env)
        obj_name <- ls(env)[1]
        data <- get(obj_name, envir = env)

        # Get review ID from filename
        review_id <- gsub("_data\\.rda$", "", basename(f))

        # Check if has required columns
        if (!"Study" %in% names(data) || !"Mean" %in% names(data)) next

        # Get unique studies
        unique_studies <- unique(data$Study)

        for (study in unique_studies) {
            study_data <- data[data$Study == study, ][1, ]  # First row for this study

            # Skip if missing key data
            if (is.na(study_data$Mean) || is.na(study_data$CI.start) || is.na(study_data$CI.end)) next

            trial_count <- trial_count + 1

            # Determine effect type based on value range
            effect_val <- round(study_data$Mean, 2)
            ci_lo <- round(study_data$CI.start, 2)
            ci_hi <- round(study_data$CI.end, 2)

            # Classify as RR, OR, or MD
            effect_type <- "RR"  # Default for dichotomous
            if (!is.na(study_data$Experimental.mean)) {
                effect_type <- "MD"
            } else if (abs(effect_val) > 10) {
                effect_type <- "MD"
            }

            n_treatment <- study_data$Experimental.N
            n_control <- study_data$Control.N
            if (is.na(n_treatment)) n_treatment <- 100
            if (is.na(n_control)) n_control <- 100

            trial <- list(
                id = paste0("COCHRANE-", review_id, "-", sprintf("%03d", trial_count %% 1000)),
                review = review_id,
                study = study,
                outcome = study_data$Analysis.name,
                effect_type = effect_type,
                effect_value = effect_val,
                ci_lo = ci_lo,
                ci_hi = ci_hi,
                n_treatment = as.integer(n_treatment),
                n_control = as.integer(n_control),
                events_treatment = if(!is.na(study_data$Experimental.cases)) as.integer(study_data$Experimental.cases) else NULL,
                events_control = if(!is.na(study_data$Control.cases)) as.integer(study_data$Control.cases) else NULL,
                year = if(!is.na(study_data$Study.year)) as.integer(study_data$Study.year) else NULL,
                doi = study_data$review_doi
            )

            all_trials[[trial_count]] <- trial

            if (trial_count >= 10000) break
        }

        if (trial_count >= 10000) break
    }, error = function(e) {
        # Skip problematic files
    })
}

cat("Extracted", trial_count, "trials from Cochrane reviews\n")

# Save to JSON
output_path <- "C:/Users/user/cochrane_trials.json"
write_json(all_trials, output_path, auto_unbox = TRUE, pretty = FALSE)
cat("Saved to:", output_path, "\n")

# Print stats
effect_types <- sapply(all_trials, function(x) x$effect_type)
cat("\nEffect type distribution:\n")
print(table(effect_types))

# Print sample
cat("\nSample trials:\n")
for (i in 1:min(5, length(all_trials))) {
    t <- all_trials[[i]]
    cat(sprintf("%s: %s %s, 95%% CI %s-%s (n=%d vs %d)\n",
                t$id, t$effect_type, t$effect_value, t$ci_lo, t$ci_hi,
                t$n_treatment, t$n_control))
}
