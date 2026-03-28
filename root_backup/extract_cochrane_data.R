# Extract Cochrane Pairwise data for RCTExtractor validation
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

        # Extract study-level data
        if ("study" %in% names(data) || "study_id" %in% names(data) || "author" %in% names(data)) {
            study_col <- if ("study" %in% names(data)) "study"
                        else if ("study_id" %in% names(data)) "study_id"
                        else "author"

            for (i in 1:nrow(data)) {
                trial_count <- trial_count + 1

                trial <- list(
                    id = paste0(review_id, "-", i),
                    review = review_id,
                    study = as.character(data[[study_col]][i])
                )

                # Extract effect data if available
                if ("TE" %in% names(data)) trial$effect <- data$TE[i]
                if ("yi" %in% names(data)) trial$effect <- data$yi[i]
                if ("seTE" %in% names(data)) trial$se <- data$seTE[i]
                if ("sei" %in% names(data)) trial$se <- data$sei[i]
                if ("vi" %in% names(data)) trial$var <- data$vi[i]

                # Extract counts if available
                if ("n.e" %in% names(data)) trial$n_treatment <- data$n.e[i]
                if ("n.c" %in% names(data)) trial$n_control <- data$n.c[i]
                if ("event.e" %in% names(data)) trial$events_treatment <- data$event.e[i]
                if ("event.c" %in% names(data)) trial$events_control <- data$event.c[i]
                if ("mean.e" %in% names(data)) trial$mean_treatment <- data$mean.e[i]
                if ("mean.c" %in% names(data)) trial$mean_control <- data$mean.c[i]
                if ("sd.e" %in% names(data)) trial$sd_treatment <- data$sd.e[i]
                if ("sd.c" %in% names(data)) trial$sd_control <- data$sd.c[i]

                # Get comparison and outcome
                if ("comparison" %in% names(data)) trial$comparison <- as.character(data$comparison[i])
                if ("outcome" %in% names(data)) trial$outcome <- as.character(data$outcome[i])

                all_trials[[trial_count]] <- trial
            }
        }
    }, error = function(e) {
        # Skip problematic files
    })

    if (trial_count >= 5000) break  # Limit for now
}

cat("Extracted", trial_count, "trials from Cochrane reviews\n")

# Save to JSON
output_path <- "C:/Users/user/cochrane_trials.json"
write_json(all_trials, output_path, auto_unbox = TRUE, pretty = TRUE)
cat("Saved to:", output_path, "\n")

# Print sample
cat("\nSample trial:\n")
print(all_trials[[1]])
