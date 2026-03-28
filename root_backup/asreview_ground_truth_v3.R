# ASReview Ground Truth v3 - Targeted Author+Year Search
# Strategy: Find the actual included studies, then sample topic-related excluded studies

library(data.table)
library(httr)
library(jsonlite)
library(xml2)

cat("=== ASReview Ground Truth v3 - Targeted Search ===\n\n")

# ========================================
# Search PubMed for specific author + year
# ========================================
search_author_year <- function(author, year) {
  # Clean author name
  author_clean <- gsub("[^a-zA-Z ]", "", author)
  author_first <- strsplit(author_clean, " ")[[1]][1]

  query <- paste0(author_first, "[Author] AND ", year, "[dp]")

  tryCatch({
    resp <- GET("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                query = list(db = "pubmed", term = query, retmax = 20, retmode = "json"),
                timeout(15))

    if (status_code(resp) == 200) {
      data <- fromJSON(rawToChar(resp$content))
      return(data$esearchresult$idlist)
    }
    return(NULL)
  }, error = function(e) NULL)
}

# ========================================
# Fetch article details
# ========================================
fetch_articles <- function(pmids) {
  if (length(pmids) == 0) return(NULL)

  tryCatch({
    resp <- GET("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
                query = list(
                  db = "pubmed",
                  id = paste(pmids, collapse = ","),
                  rettype = "xml"
                ), timeout(60))

    if (status_code(resp) == 200) {
      xml_content <- read_xml(rawToChar(resp$content))
      articles <- xml_find_all(xml_content, "//PubmedArticle")

      results <- lapply(articles, function(art) {
        pmid <- xml_text(xml_find_first(art, ".//PMID"))
        title <- xml_text(xml_find_first(art, ".//ArticleTitle"))
        abstract <- paste(xml_text(xml_find_all(art, ".//AbstractText")), collapse = " ")

        authors_nodes <- xml_find_all(art, ".//Author/LastName")
        first_author <- xml_text(authors_nodes[1])

        year <- xml_text(xml_find_first(art, ".//PubDate/Year"))
        if (is.na(year) || year == "") {
          year <- substr(xml_text(xml_find_first(art, ".//PubDate/MedlineDate")), 1, 4)
        }

        data.table(
          pmid = pmid,
          title = title,
          abstract = ifelse(is.na(abstract), "", abstract),
          first_author = first_author,
          year = as.numeric(year)
        )
      })

      return(rbindlist(results, fill = TRUE))
    }
    return(NULL)
  }, error = function(e) NULL)
}

# ========================================
# Get review topic and search for excluded candidates
# ========================================
get_topic_search <- function(doi, max_year) {
  # Get title from CrossRef
  tryCatch({
    url <- paste0("https://api.crossref.org/works/", URLencode(doi, reserved = TRUE))
    resp <- GET(url, timeout(15))

    if (status_code(resp) == 200) {
      data <- fromJSON(rawToChar(resp$content))
      title <- data$message$title[1]

      # Extract key medical terms
      title_lower <- tolower(title)
      words <- unlist(strsplit(gsub("[^a-z ]", " ", title_lower), "\\s+"))
      stopwords <- c("the", "a", "an", "for", "in", "of", "to", "and", "or", "with",
                     "versus", "adults", "children", "people", "patients")
      key_terms <- unique(words[nchar(words) > 4 & !words %in% stopwords])[1:3]

      if (length(key_terms) > 0) {
        query <- paste0(
          "(", paste(key_terms, collapse = " AND "), ")",
          " AND (randomized controlled trial[pt])",
          " AND 1990:", max_year, "[dp]"
        )
        return(list(title = title, query = query))
      }
    }
    return(NULL)
  }, error = function(e) NULL)
}

# ========================================
# Process one review
# ========================================
process_review <- function(review_id, review_data) {
  cat("\n=== Processing:", review_id, "===\n")

  # Parse included studies
  studies <- unique(review_data$Study)
  cat("Included studies:", length(studies), "\n")

  # Search for each included study
  included_articles <- list()

  for (study in studies[1:min(20, length(studies))]) {  # Limit for speed
    # Parse author and year
    author <- gsub("\\s*(19|20)[0-9]{2}.*$", "", study)
    year_match <- regmatches(study, regexpr("(19|20)[0-9]{2}", study))
    year <- if (length(year_match) > 0) year_match else NA

    if (!is.na(year) && nchar(author) > 1) {
      pmids <- search_author_year(author, year)

      if (length(pmids) > 0) {
        articles <- fetch_articles(pmids[1:min(3, length(pmids))])
        if (!is.null(articles) && nrow(articles) > 0) {
          articles[, `:=`(
            included = 1L,
            original_study = study,
            source = "included"
          )]
          included_articles[[study]] <- articles
        }
      }
    }
    Sys.sleep(0.35)  # Rate limit
  }

  n_found <- length(included_articles)
  cat("Found PubMed records for:", n_found, "studies\n")

  if (n_found == 0) {
    return(NULL)
  }

  included_dt <- rbindlist(included_articles, fill = TRUE)

  # Get topic search for excluded studies
  doi <- unique(review_data$review.doi)[1]
  years <- as.numeric(gsub(".*\\b(19|20)([0-9]{2}).*", "\\1\\2", studies))
  max_year <- max(years, na.rm = TRUE)

  topic_info <- get_topic_search(doi, max_year)

  excluded_dt <- NULL
  if (!is.null(topic_info)) {
    cat("Topic query:", substr(topic_info$query, 1, 80), "...\n")

    # Search for topic-related studies
    resp <- GET("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                query = list(
                  db = "pubmed",
                  term = topic_info$query,
                  retmax = 100,
                  retmode = "json"
                ), timeout(30))

    if (status_code(resp) == 200) {
      data <- fromJSON(rawToChar(resp$content))
      topic_pmids <- data$esearchresult$idlist

      # Remove already-found included PMIDs
      topic_pmids <- setdiff(topic_pmids, included_dt$pmid)

      if (length(topic_pmids) > 0) {
        excluded_dt <- fetch_articles(topic_pmids[1:min(50, length(topic_pmids))])
        if (!is.null(excluded_dt)) {
          excluded_dt[, `:=`(
            included = 0L,
            original_study = NA_character_,
            source = "topic_search"
          )]
          cat("Excluded candidates:", nrow(excluded_dt), "\n")
        }
      }
    }
  }

  # Combine
  if (!is.null(excluded_dt) && nrow(excluded_dt) > 0) {
    all_articles <- rbind(included_dt, excluded_dt, fill = TRUE)
  } else {
    all_articles <- included_dt
  }

  all_articles[, review_id := review_id]

  prevalence <- sum(all_articles$included) / nrow(all_articles)
  cat("Total records:", nrow(all_articles),
      "| Included:", sum(all_articles$included),
      "| Prevalence:", round(prevalence * 100, 1), "%\n")

  return(all_articles)
}

# ========================================
# MAIN
# ========================================
rds_dir <- "C:/Users/user/OneDrive - NHS/Documents/Pairwise70/analysis/output/cleaned_rds"
rds_files <- list.files(rds_dir, pattern = "\\.rds$", full.names = TRUE)

cat("Processing sample of", min(15, length(rds_files)), "reviews...\n")

all_results <- list()

for (i in 1:min(15, length(rds_files))) {
  d <- readRDS(rds_files[i])
  review_id <- gsub("_data\\.rds$", "", basename(rds_files[i]))

  result <- tryCatch(
    process_review(review_id, d),
    error = function(e) {
      cat("  Error:", conditionMessage(e), "\n")
      NULL
    }
  )

  if (!is.null(result) && nrow(result) > 0) {
    all_results[[review_id]] <- result
  }

  Sys.sleep(0.5)
}

# ========================================
# Create final dataset
# ========================================
cat("\n\n=== FINAL DATASET ===\n")

if (length(all_results) > 0) {
  final_dt <- rbindlist(all_results, fill = TRUE)

  cat("Total articles:", nrow(final_dt), "\n")
  cat("  Included (label=1):", sum(final_dt$included), "\n")
  cat("  Excluded (label=0):", sum(!final_dt$included), "\n")
  cat("  Reviews covered:", length(unique(final_dt$review_id)), "\n")

  # Clean for ASReview format
  asreview_dt <- final_dt[, .(
    record_id = pmid,
    title = title,
    abstract = abstract,
    authors = first_author,
    year = year,
    label_included = included,
    review_id = review_id
  )]

  # Remove duplicates
  asreview_dt <- unique(asreview_dt, by = "record_id")

  cat("\nAfter deduplication:", nrow(asreview_dt), "unique articles\n")
  cat("  Included:", sum(asreview_dt$label_included), "\n")
  cat("  Excluded:", sum(!asreview_dt$label_included), "\n")
  cat("  Prevalence:", round(mean(asreview_dt$label_included) * 100, 1), "%\n")

  # Save
  fwrite(asreview_dt, "C:/Users/user/asreview_pairwise70_groundtruth.csv")
  cat("\nSaved: C:/Users/user/asreview_pairwise70_groundtruth.csv\n")

  # Also show sample
  cat("\n--- Sample Records ---\n")
  print(head(asreview_dt[, .(record_id, title = substr(title, 1, 50), label_included)], 10))
}

cat("\n=== COMPLETE ===\n")
cat("Ground truth dataset ready for ASReview training!\n")
