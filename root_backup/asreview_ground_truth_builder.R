# ASReview Ground Truth Dataset Builder
# Uses Pairwise70 Cochrane reviews as ground truth for training/validation

library(data.table)
library(httr)
library(jsonlite)

cat("=== ASReview Ground Truth Dataset Builder ===\n")
cat("Using Pairwise70 Cochrane Reviews as Ground Truth\n\n")

# ========================================
# STEP 1: Load study metadata
# ========================================
studies <- fread("C:/Users/user/pairwise70_study_metadata.csv")
cat("Loaded", nrow(studies), "study entries from", length(unique(studies$review_id)), "reviews\n\n")

# ========================================
# STEP 2: Get Cochrane review titles via API
# ========================================
get_cochrane_title <- function(doi) {
  tryCatch({
    # Use CrossRef API to get title from DOI
    url <- paste0("https://api.crossref.org/works/", URLencode(doi, reserved = TRUE))
    resp <- GET(url, timeout(10))
    if (status_code(resp) == 200) {
      data <- fromJSON(rawToChar(resp$content))
      return(data$message$title[1])
    }
    return(NA_character_)
  }, error = function(e) NA_character_)
}

# ========================================
# STEP 3: Build PubMed search queries
# ========================================
build_pubmed_query <- function(title, max_year) {
  # Clean title for search
  title_clean <- gsub("\\s+", " ", title)
  title_clean <- gsub("[^a-zA-Z0-9 ]", "", title_clean)

  # Extract key terms (first 5-7 meaningful words)
  words <- strsplit(tolower(title_clean), " ")[[1]]
  stopwords <- c("the", "a", "an", "of", "for", "in", "to", "and", "or", "with", "versus", "vs")
  key_terms <- words[!words %in% stopwords][1:min(5, length(words))]
  key_terms <- key_terms[!is.na(key_terms)]

  # Build query with date restriction
  query <- paste0(
    "(", paste(key_terms, collapse = " AND "), ")",
    " AND (randomized controlled trial[pt] OR clinical trial[pt])",
    " AND 1900:", max_year, "[dp]"
  )

  return(query)
}

# ========================================
# STEP 4: Search PubMed via E-utilities
# ========================================
search_pubmed <- function(query, retmax = 500) {
  tryCatch({
    base_url <- "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    resp <- GET(base_url, query = list(
      db = "pubmed",
      term = query,
      retmax = retmax,
      retmode = "json"
    ), timeout(30))

    if (status_code(resp) == 200) {
      data <- fromJSON(rawToChar(resp$content))
      pmids <- data$esearchresult$idlist
      count <- as.numeric(data$esearchresult$count)
      return(list(pmids = pmids, count = count))
    }
    return(list(pmids = NULL, count = 0))
  }, error = function(e) list(pmids = NULL, count = 0))
}

# ========================================
# STEP 5: Fetch article details from PubMed
# ========================================
fetch_pubmed_details <- function(pmids) {
  if (length(pmids) == 0) return(NULL)

  tryCatch({
    base_url <- "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    resp <- GET(base_url, query = list(
      db = "pubmed",
      id = paste(pmids, collapse = ","),
      retmode = "json"
    ), timeout(60))

    if (status_code(resp) == 200) {
      data <- fromJSON(rawToChar(resp$content))
      results <- data$result

      # Extract article info
      articles <- lapply(pmids, function(id) {
        art <- results[[as.character(id)]]
        if (!is.null(art)) {
          data.table(
            pmid = id,
            title = art$title %||% NA,
            authors = paste(sapply(art$authors, function(a) a$name), collapse = "; "),
            source = art$source %||% NA,
            pubdate = art$pubdate %||% NA,
            volume = art$volume %||% NA
          )
        }
      })

      return(rbindlist(articles, fill = TRUE))
    }
    return(NULL)
  }, error = function(e) NULL)
}

# ========================================
# STEP 6: Match search results to included studies
# ========================================
match_studies <- function(search_results, included_studies) {
  if (is.null(search_results) || nrow(search_results) == 0) {
    return(data.table(pmid = character(), matched = logical(), match_type = character()))
  }

  # Create matching patterns from included studies
  patterns <- sapply(included_studies, function(s) {
    # Extract author and year
    author <- gsub("\\s*(19|20)[0-9]{2}.*$", "", s)
    year <- gsub(".*\\b(19|20)([0-9]{2}).*", "\\1\\2", s)
    list(author = tolower(author), year = year)
  }, simplify = FALSE)

  # Try to match each search result
  search_results[, `:=`(
    matched = FALSE,
    match_type = NA_character_,
    matched_study = NA_character_
  )]

  for (i in seq_len(nrow(search_results))) {
    title_lower <- tolower(search_results$title[i])
    authors_lower <- tolower(search_results$authors[i])
    pubdate <- search_results$pubdate[i]

    for (p in patterns) {
      # Check author match in authors list or title
      author_match <- grepl(p$author, authors_lower, fixed = TRUE) ||
                      grepl(p$author, title_lower, fixed = TRUE)

      # Check year match
      year_match <- grepl(p$year, pubdate, fixed = TRUE)

      if (author_match && year_match) {
        search_results[i, `:=`(
          matched = TRUE,
          match_type = "author_year",
          matched_study = paste0(p$author, " ", p$year)
        )]
        break
      }
    }
  }

  return(search_results)
}

# ========================================
# STEP 7: Process sample reviews
# ========================================
process_review <- function(review_id, study_data) {
  cat("\n--- Processing:", review_id, "---\n")

  # Get review DOI
  doi <- unique(study_data$review.doi)[1]
  if (is.na(doi)) {
    cat("  No DOI found\n")
    return(NULL)
  }

  # Get review title
  title <- get_cochrane_title(doi)
  if (is.na(title)) {
    cat("  Could not fetch title\n")
    return(NULL)
  }
  cat("  Title:", substr(title, 1, 60), "...\n")

  # Get included studies
  included <- unique(study_data$study_label)
  max_year <- max(study_data$year, na.rm = TRUE)
  cat("  Included studies:", length(included), "| Max year:", max_year, "\n")

  # Build and run PubMed search
  query <- build_pubmed_query(title, max_year)
  cat("  Query:", substr(query, 1, 80), "...\n")

  search_result <- search_pubmed(query, retmax = 200)
  cat("  PubMed hits:", search_result$count, "\n")

  if (length(search_result$pmids) > 0) {
    # Fetch details
    details <- fetch_pubmed_details(search_result$pmids[1:min(100, length(search_result$pmids))])

    if (!is.null(details)) {
      # Match to included studies
      matched <- match_studies(details, included)

      n_matched <- sum(matched$matched)
      recall <- n_matched / length(included)
      precision <- n_matched / nrow(matched)

      cat("  Matched:", n_matched, "/", length(included),
          "(Recall:", round(recall * 100, 1), "%)\n")

      return(list(
        review_id = review_id,
        title = title,
        n_included = length(included),
        n_searched = search_result$count,
        n_fetched = nrow(details),
        n_matched = n_matched,
        recall = recall,
        precision = precision,
        details = matched
      ))
    }
  }

  return(NULL)
}

# ========================================
# MAIN: Process sample reviews
# ========================================
cat("\n=== Processing Sample Reviews ===\n")

# Get unique reviews with their DOIs
rds_dir <- "C:/Users/user/OneDrive - NHS/Documents/Pairwise70/analysis/output/cleaned_rds"
rds_files <- list.files(rds_dir, pattern = "\\.rds$", full.names = TRUE)

# Process first 5 reviews as demonstration
results <- list()
for (i in 1:5) {
  d <- readRDS(rds_files[i])
  review_id <- gsub("_data\\.rds$", "", basename(rds_files[i]))

  # Merge with study metadata
  d_studies <- data.table(
    review_id = review_id,
    study_label = d$Study,
    year = as.numeric(gsub(".*\\b(19|20)([0-9]{2}).*", "\\1\\2", d$Study)),
    review.doi = d$review.doi
  )
  d_studies <- unique(d_studies)

  result <- process_review(review_id, d_studies)
  if (!is.null(result)) {
    results[[review_id]] <- result
  }

  Sys.sleep(0.5)  # Be nice to APIs
}

# ========================================
# Summary Statistics
# ========================================
cat("\n\n=== SUMMARY ===\n")
if (length(results) > 0) {
  summary_dt <- rbindlist(lapply(results, function(r) {
    data.table(
      review = r$review_id,
      included = r$n_included,
      searched = r$n_searched,
      matched = r$n_matched,
      recall = round(r$recall * 100, 1)
    )
  }))

  print(summary_dt)

  cat("\nOverall recall:", round(mean(summary_dt$recall), 1), "%\n")
  cat("This forms GROUND TRUTH for ASReview training\n")

  # Save for ASReview format
  cat("\n=== Creating ASReview Training Dataset ===\n")

  all_articles <- rbindlist(lapply(results, function(r) {
    if (!is.null(r$details)) {
      r$details[, review_id := r$review_id]
      return(r$details)
    }
    return(NULL)
  }), fill = TRUE)

  if (nrow(all_articles) > 0) {
    # ASReview format: title, abstract, label
    asreview_data <- all_articles[, .(
      title = title,
      abstract = "",  # Would need separate fetch
      authors = authors,
      year = as.numeric(gsub(".*([0-9]{4}).*", "\\1", pubdate)),
      included = as.integer(matched),
      review_id = review_id,
      pmid = pmid
    )]

    fwrite(asreview_data, "C:/Users/user/asreview_training_sample.csv")
    cat("Saved ASReview training sample:", nrow(asreview_data), "articles\n")
    cat("  Included (label=1):", sum(asreview_data$included), "\n")
    cat("  Excluded (label=0):", sum(!asreview_data$included), "\n")
  }
}

cat("\n=== DONE ===\n")
cat("Ground truth dataset created from Pairwise70 Cochrane reviews\n")
cat("This provides validated inclusion/exclusion labels for ASReview training\n")
