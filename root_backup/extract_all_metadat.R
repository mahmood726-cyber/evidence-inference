# Extract ALL possible real data from metadat package
# Comprehensive extraction including all effect types

library(metadat)
library(metafor)
library(jsonlite)

cat("=" , rep("=", 69), "\n", sep="")
cat("  COMPREHENSIVE METADAT EXTRACTION\n")
cat("=", rep("=", 69), "\n\n", sep="")

all_trials <- list()
trial_counter <- 0

# Get all datasets
datasets <- data(package = "metadat")$results[, "Item"]
cat("Found", length(datasets), "datasets in metadat\n\n")

for (ds_name in datasets) {
  tryCatch({
    data(list = ds_name, package = "metadat")
    df <- get(ds_name)

    if (!is.data.frame(df)) next
    if (nrow(df) < 2) next

    cols <- tolower(names(df))
    extracted <- 0

    # Method 1: Pre-computed effect sizes (yi, vi)
    if ("yi" %in% cols && "vi" %in% cols) {
      for (i in 1:nrow(df)) {
        tryCatch({
          yi <- as.numeric(df$yi[i])
          vi <- as.numeric(df$vi[i])

          if (is.na(yi) || is.na(vi) || vi <= 0) next

          se <- sqrt(vi)
          ci_lo <- yi - 1.96 * se
          ci_hi <- yi + 1.96 * se

          # Determine effect type based on column names or values
          effect_type <- "ES"  # Generic effect size
          if ("measure" %in% cols) {
            measure <- as.character(df$measure[i])
            if (grepl("OR", measure, ignore.case = TRUE)) effect_type <- "OR"
            else if (grepl("RR", measure, ignore.case = TRUE)) effect_type <- "RR"
            else if (grepl("HR", measure, ignore.case = TRUE)) effect_type <- "HR"
            else if (grepl("SMD", measure, ignore.case = TRUE)) effect_type <- "SMD"
            else if (grepl("MD", measure, ignore.case = TRUE)) effect_type <- "MD"
          }

          # Check if log scale (ratios > 0 typically)
          if (effect_type == "ES") {
            if (abs(yi) < 3 && yi != 0) {
              # Could be log OR/RR/HR - check if CI suggests ratio
              if (ci_lo > -3 && ci_hi < 3) {
                # Likely log-transformed ratio
                if (yi > 0 || ci_lo > -5) {
                  effect_type <- "logOR"
                }
              }
            }
          }

          study <- if ("study" %in% cols) as.character(df$study[i])
                   else if ("author" %in% cols) as.character(df$author[i])
                   else if ("trial" %in% cols) as.character(df$trial[i])
                   else paste0("Study_", i)

          trial_counter <- trial_counter + 1
          trial_id <- sprintf("META-%s-%04d", gsub("[^a-zA-Z0-9]", "", ds_name), i)

          all_trials[[trial_counter]] <- list(
            id = trial_id,
            source = study,
            dataset = ds_name,
            effect_type = effect_type,
            value = round(yi, 4),
            ci_lo = round(ci_lo, 4),
            ci_hi = round(ci_hi, 4),
            n1 = NA,
            n2 = NA
          )
          extracted <- extracted + 1
        }, error = function(e) {})
      }
    }

    # Method 2: 2x2 tables (ai, bi, ci, di) -> OR and RR
    if (all(c("ai", "bi", "ci", "di") %in% cols)) {
      for (i in 1:nrow(df)) {
        tryCatch({
          ai <- as.numeric(df$ai[i])
          bi <- as.numeric(df$bi[i])
          ci_val <- as.numeric(df$ci[i])
          di <- as.numeric(df$di[i])

          if (any(is.na(c(ai, bi, ci_val, di)))) next

          # Add continuity correction if needed
          if (any(c(ai, bi, ci_val, di) == 0)) {
            ai <- ai + 0.5; bi <- bi + 0.5
            ci_val <- ci_val + 0.5; di <- di + 0.5
          }

          # OR
          or <- (ai * di) / (bi * ci_val)
          if (!is.na(or) && or > 0 && is.finite(or)) {
            se_log_or <- sqrt(1/ai + 1/bi + 1/ci_val + 1/di)
            ci_lo <- exp(log(or) - 1.96 * se_log_or)
            ci_hi <- exp(log(or) + 1.96 * se_log_or)

            study <- if ("study" %in% cols) as.character(df$study[i])
                     else if ("author" %in% cols) as.character(df$author[i])
                     else paste0("Study_", i)

            trial_counter <- trial_counter + 1
            trial_id <- sprintf("META-OR-%s-%04d", gsub("[^a-zA-Z0-9]", "", ds_name), i)

            all_trials[[trial_counter]] <- list(
              id = trial_id,
              source = study,
              dataset = ds_name,
              effect_type = "OR",
              value = round(or, 4),
              ci_lo = round(ci_lo, 4),
              ci_hi = round(ci_hi, 4),
              n1 = as.integer(ai + bi),
              n2 = as.integer(ci_val + di)
            )
            extracted <- extracted + 1
          }
        }, error = function(e) {})
      }
    }

    # Method 3: Continuous data (m1i, sd1i, n1i, m2i, sd2i, n2i) -> SMD
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
          if (sd1 <= 0 || sd2 <= 0) next

          # Pooled SD and Hedges' g
          s_pooled <- sqrt(((n1-1)*sd1^2 + (n2-1)*sd2^2) / (n1 + n2 - 2))
          if (s_pooled == 0) next

          d <- (m1 - m2) / s_pooled
          j <- 1 - 3 / (4 * (n1 + n2 - 2) - 1)
          g <- d * j

          se <- sqrt((n1 + n2) / (n1 * n2) + g^2 / (2 * (n1 + n2)))
          ci_lo <- g - 1.96 * se
          ci_hi <- g + 1.96 * se

          study <- if ("study" %in% cols) as.character(df$study[i])
                   else if ("author" %in% cols) as.character(df$author[i])
                   else paste0("Study_", i)

          trial_counter <- trial_counter + 1
          trial_id <- sprintf("META-SMD-%s-%04d", gsub("[^a-zA-Z0-9]", "", ds_name), i)

          all_trials[[trial_counter]] <- list(
            id = trial_id,
            source = study,
            dataset = ds_name,
            effect_type = "SMD",
            value = round(g, 4),
            ci_lo = round(ci_lo, 4),
            ci_hi = round(ci_hi, 4),
            n1 = as.integer(n1),
            n2 = as.integer(n2)
          )
          extracted <- extracted + 1
        }, error = function(e) {})
      }
    }

    # Method 4: Direct effect sizes with CI
    for (eff_col in c("or", "rr", "hr", "smd", "md", "effect", "estimate")) {
      if (eff_col %in% cols) {
        ci_cols <- list(
          c("lower", "upper"),
          c("ci.lb", "ci.ub"),
          c("ci_lower", "ci_upper"),
          c("lower_ci", "upper_ci"),
          c("lcl", "ucl")
        )

        for (ci_pair in ci_cols) {
          if (all(tolower(ci_pair) %in% cols)) {
            for (i in 1:nrow(df)) {
              tryCatch({
                val <- as.numeric(df[[eff_col]][i])
                lo <- as.numeric(df[[ci_pair[1]]][i])
                hi <- as.numeric(df[[ci_pair[2]]][i])

                if (any(is.na(c(val, lo, hi)))) next
                if (lo >= hi) next

                effect_type <- toupper(eff_col)
                if (effect_type == "EFFECT" || effect_type == "ESTIMATE") {
                  if (val > 0 && lo > 0) effect_type <- "OR"
                  else effect_type <- "ES"
                }

                study <- if ("study" %in% cols) as.character(df$study[i])
                         else if ("author" %in% cols) as.character(df$author[i])
                         else paste0("Study_", i)

                trial_counter <- trial_counter + 1
                trial_id <- sprintf("META-%s-%s-%04d", effect_type, gsub("[^a-zA-Z0-9]", "", ds_name), i)

                all_trials[[trial_counter]] <- list(
                  id = trial_id,
                  source = study,
                  dataset = ds_name,
                  effect_type = effect_type,
                  value = round(val, 4),
                  ci_lo = round(lo, 4),
                  ci_hi = round(hi, 4),
                  n1 = NA,
                  n2 = NA
                )
                extracted <- extracted + 1
              }, error = function(e) {})
            }
            break
          }
        }
      }
    }

    if (extracted > 0) {
      cat("  ", ds_name, ": ", extracted, " trials\n", sep="")
    }

  }, error = function(e) {})
}

cat("\n")
cat("Total trials extracted:", length(all_trials), "\n")

# Count by effect type
if (length(all_trials) > 0) {
  types <- sapply(all_trials, function(t) t$effect_type)
  type_counts <- table(types)
  cat("\nBy effect type:\n")
  print(type_counts)

  # Save to JSON
  output_path <- "C:/Users/user/metadat_comprehensive.json"
  json_output <- toJSON(all_trials, auto_unbox = TRUE, pretty = TRUE)
  writeLines(json_output, output_path)
  cat("\nSaved to", output_path, "\n")
}
