# Extract real RCT data from additional R packages
# Check: meta, netmeta, dmetar, gemtc, NMAoutlier

library(jsonlite)

all_trials <- list()
counter <- 0

cat("=" , rep("=", 69), "\n", sep="")
cat("  EXTRACTING DATA FROM ADDITIONAL R PACKAGES\n")
cat("=", rep("=", 69), "\n\n", sep="")

# Function to extract from data frame
extract_from_df <- function(df, pkg_name, ds_name) {
  trials <- list()
  cols <- tolower(names(df))

  # Look for pre-computed effect sizes
  for (i in 1:nrow(df)) {
    tryCatch({
      # Try different column naming conventions
      val <- NULL; lo <- NULL; hi <- NULL; et <- "ES"

      # Check for TE (treatment effect) columns - common in meta/netmeta
      if ("te" %in% cols && "lower" %in% cols && "upper" %in% cols) {
        val <- as.numeric(df$TE[i])
        lo <- as.numeric(df$lower[i])
        hi <- as.numeric(df$upper[i])
      } else if ("effect" %in% cols && "lower" %in% cols && "upper" %in% cols) {
        val <- as.numeric(df$effect[i])
        lo <- as.numeric(df$lower[i])
        hi <- as.numeric(df$upper[i])
      } else if ("yi" %in% cols && "vi" %in% cols) {
        yi <- as.numeric(df$yi[i])
        vi <- as.numeric(df$vi[i])
        if (!is.na(vi) && vi > 0) {
          se <- sqrt(vi)
          val <- yi
          lo <- yi - 1.96 * se
          hi <- yi + 1.96 * se
        }
      }

      if (!is.null(val) && !is.null(lo) && !is.null(hi)) {
        if (!is.na(val) && !is.na(lo) && !is.na(hi) && lo < hi) {
          study <- if ("study" %in% cols) as.character(df$study[i])
                   else if ("studlab" %in% cols) as.character(df$studlab[i])
                   else paste0("Study_", i)

          trials[[length(trials) + 1]] <- list(
            id = sprintf("%s-%s-%04d", pkg_name, gsub("[^a-zA-Z0-9]", "", ds_name), i),
            source = study,
            dataset = ds_name,
            effect_type = et,
            value = round(val, 4),
            ci_lo = round(lo, 4),
            ci_hi = round(hi, 4),
            n1 = NA,
            n2 = NA
          )
        }
      }
    }, error = function(e) {})
  }

  return(trials)
}

# Try meta package
tryCatch({
  library(meta)
  cat("Checking meta package...\n")
  ds <- data(package = "meta")$results[, "Item"]
  for (d in ds) {
    tryCatch({
      data(list = d, package = "meta")
      df <- get(d)
      if (is.data.frame(df) && nrow(df) >= 2) {
        trials <- extract_from_df(df, "META", d)
        if (length(trials) > 0) {
          all_trials <<- c(all_trials, trials)
          counter <<- counter + length(trials)
          cat("  ", d, ": ", length(trials), " trials\n", sep="")
        }
      }
    }, error = function(e) {})
  }
}, error = function(e) {
  cat("meta package not available\n")
})

# Try netmeta package
tryCatch({
  library(netmeta)
  cat("\nChecking netmeta package...\n")
  ds <- data(package = "netmeta")$results[, "Item"]
  for (d in ds) {
    tryCatch({
      data(list = d, package = "netmeta")
      df <- get(d)
      if (is.data.frame(df) && nrow(df) >= 2) {
        trials <- extract_from_df(df, "NETMETA", d)
        if (length(trials) > 0) {
          all_trials <<- c(all_trials, trials)
          counter <<- counter + length(trials)
          cat("  ", d, ": ", length(trials), " trials\n", sep="")
        }
      }
    }, error = function(e) {})
  }
}, error = function(e) {
  cat("netmeta package not available\n")
})

# Try dmetar package
tryCatch({
  if (!require(dmetar, quietly = TRUE)) {
    cat("\nInstalling dmetar...\n")
    install.packages("dmetar", repos = "https://cloud.r-project.org", quiet = TRUE)
    library(dmetar)
  }
  cat("\nChecking dmetar package...\n")
  ds <- data(package = "dmetar")$results[, "Item"]
  for (d in ds) {
    tryCatch({
      data(list = d, package = "dmetar")
      df <- get(d)
      if (is.data.frame(df) && nrow(df) >= 2) {
        trials <- extract_from_df(df, "DMETAR", d)
        if (length(trials) > 0) {
          all_trials <<- c(all_trials, trials)
          counter <<- counter + length(trials)
          cat("  ", d, ": ", length(trials), " trials\n", sep="")
        }
      }
    }, error = function(e) {})
  }
}, error = function(e) {
  cat("dmetar package not available\n")
})

cat("\n")
cat("Total additional trials:", length(all_trials), "\n")

if (length(all_trials) > 0) {
  # Save
  output_path <- "C:/Users/user/additional_r_packages.json"
  json_output <- toJSON(all_trials, auto_unbox = TRUE, pretty = TRUE)
  writeLines(json_output, output_path)
  cat("Saved to", output_path, "\n")
}
