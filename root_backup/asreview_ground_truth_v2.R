# ASReview Ground Truth v2 - Improved PubMed Search Strategy
# Uses broader search terms and fetches abstracts

library(data.table)
library(httr)
library(jsonlite)
library(xml2)

cat("=== ASReview Ground Truth v2 - Improved Search ===\n\n")

# ========================================
# Get Cochrane review title
# ========================================
get_cochrane_title <- function(doi) {
  tryCatch({
    url <- paste0("https://api.crossref.org/works/", URLencode(doi, reserved = TRUE))
    resp <- GET(url, timeout(15),
                add_headers(`User-Agent` = "ASReviewTraining/1.0 (mailto:research@example.com)"))
    if (status_code(resp) == 200) {
      data <- fromJSON(rawToChar(resp$content))
      return(list(
        title = data$message$title[1],
        subject = paste(data$message$subject, collapse = "; ")
      ))
    }
    return(NULL)
  }, error = function(e) NULL)
}

# ========================================
# Better PubMed query builder
# ========================================
build_pubmed_query_v2 <- function(title, max_year) {
  # Clean and extract key medical terms
  title_clean <- tolower(title)

  # Remove common non-informative words
  stopwords <- c("the", "a", "an", "of", "for", "in", "to", "and", "or", "with",
                 "versus", "vs", "adults", "children", "older", "people",
                 "treatment", "therapy", "intervention", "randomized", "controlled",
                 "trial", "review", "systematic", "cochrane", "years", "aged")

  words <- unlist(strsplit(gsub("[^a-z0-9 ]", " ", title_clean), "\\s+"))
  words <- words[nchar(words) > 3]
  key_terms <- words[!words %in% stopwords]

  # Take top 3-4 most specific terms
  key_terms <- unique(key_terms)[1:min(4, length(key_terms))]
  key_terms <- key_terms[!is.na(key_terms)]

  # Build broader query
  query <- paste0(
    "(", paste(key_terms, collapse = " OR "), ")",
    "[tiab] AND (randomized[tiab] OR RCT[tiab] OR clinical trial[pt])",
    " AND 1980:", max_year, "[dp]"
  )

  return(query)
}

# ========================================
# Fetch with abstracts using efetch
# ========================================
fetch_pubmed_full <- function(pmids, batch_size = 50) {
  if (length(pmids) == 0) return(NULL)

  all_articles <- list()

  for (i in seq(1, length(pmids), by = batch_size)) {
    batch <- pmids[i:min(i + batch_size - 1, length(pmids))]

    tryCatch({
      url <- "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

      resp <- GET(url, query = list(
        db = "pubmed",
        id = paste(batch, collapse = ","),
        rettype = "xml",
        retmode = "xml"
      ), timeout(60))

      if (status_code(resp) == 200) {
        xml_content <- read_xml(rawToChar(resp$content))
        articles <- xml_find_all(xml_content, "//PubmedArticle")

        for (art in articles) {
          pmid <- xml_text(xml_find_first(art, ".//PMID"))
          title <- xml_text(xml_find_first(art, ".//ArticleTitle"))
          abstract <- xml_text(xml_find_first(art, ".//AbstractText"))

          # Get authors
          authors_nodes <- xml_find_all(art, ".//Author")
          authors <- sapply(authors_nodes, function(a) {
            ln <- xml_text(xml_find_first(a, ".//LastName"))
            fn <- xml_text(xml_find_first(a, ".//ForeName"))
            if (!is.na(ln)) paste(ln, substr(fn, 1, 1)) else NA
          })
          authors <- paste(authors[!is.na(authors)], collapse = "; ")

          # Get publication year
          year <- xml_text(xml_find_first(art, ".//PubDate/Year"))
          if (is.na(year)) {
            medline_date <- xml_text(xml_find_first(art, ".//PubDate/MedlineDate"))
            year <- substr(medline_date, 1, 4)
          }

          # Get journal
          journal <- xml_text(xml_find_first(art, ".//Journal/Title"))

          all_articles[[pmid]] <- data.table(
            pmid = pmid,
            title = title,
            abstract = ifelse(is.na(abstract), "", abstract),
            authors = authors,
            year = as.numeric(year),
            journal = journal
          )
        }
      }

      Sys.sleep(0.4)  # Rate limiting
    }, error = function(e) {
      cat("  Batch error:", conditionMessage(e), "\n")
    })
  }

  if (length(all_articles) > 0) {
    return(rbindlist(all_articles, fill = TRUE))
  }
  return(NULL)
}

# ========================================
# Search PubMed
# ========================================
search_pubmed <- function(query, retmax = 500) {
  tryCatch({
    resp <- GET("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                query = list(db = "pubmed", term = query, retmax = retmax, retmode = "json"),
                timeout(30))

    if (status_code(resp) == 200) {
      data <- fromJSON(rawToChar(resp$content))
      return(list(
        pmids = data$esearchresult$idlist,
        count = as.numeric(data$esearchresult$count)
      ))
    }
    return(list(pmids = NULL, count = 0))
  }, error = function(e) list(pmids = NULL, count = 0))
}

# ========================================
# Match articles to included studies
# ========================================
match_to_included <- function(articles, included_studies) {
  if (is.null(articles) || nrow(articles) == 0) return(NULL)

  # Parse included studies to author + year patterns
  patterns <- lapply(included_studies, function(s) {
    author <- tolower(gsub("\\s*(19|20)[0-9]{2}.*$", "", s))
    author <- gsub("[^a-z]", "", author)  # Keep only letters
    year <- gsub(".*\\b(19|20)([0-9]{2}).*", "\\1\\2", s)
    list(author = author, year = as.numeric(year), original = s)
  })

  articles[, `:=`(included = 0L, matched_to = NA_character_)]

  for (i in seq_len(nrow(articles))) {
    art_authors <- tolower(gsub("[^a-z; ]", "", articles$authors[i]))
    art_year <- articles$year[i]

    for (p in patterns) {
      if (!is.na(art_year) && art_year == p$year) {
        if (grepl(p$author, art_authors)) {
          articles[i, `:=`(included = 1L, matched_to = p$original)]
          break
        }
      }
    }
  }

  return(articles)
}

# ========================================
# Process one review
# ========================================
process_review <- function(review_id, review_data) {
  cat("\n=== Processing:", review_id, "===\n")

  doi <- unique(review_data$review.doi)[1]
  if (is.na(doi)) {
    cat("  No DOI\n")
    return(NULL)
  }

  # Get title
  info <- get_cochrane_title(doi)
  if (is.null(info)) {
    cat("  Could not fetch review info\n")
    return(NULL)
  }
  cat("Title:", substr(info$title, 1, 70), "...\n")

  # Get included studies
  included <- unique(review_data$Study)
  years <- as.numeric(gsub(".*\\b(19|20)([0-9]{2}).*", "\\1\\2", included))
  max_year <- max(years, na.rm = TRUE)
  cat("Included studies:", length(included), "| Year range:",
      min(years, na.rm = TRUE), "-", max_year, "\n")

  # Build query
  query <- build_pubmed_query_v2(info$title, max_year)
  cat("Query:", substr(query, 1, 100), "...\n")

  # Search
  search <- search_pubmed(query, retmax = 300)
  cat("PubMed hits:", search$count, "| Fetching:", min(300, search$count), "\n")

  if (length(search$pmids) == 0) {
    return(NULL)
  }

  # Fetch full records with abstracts
  articles <- fetch_pubmed_full(search$pmids[1:min(300, length(search$pmids))])

  if (is.null(articles) || nrow(articles) == 0) {
    cat("  No articles fetched\n")
    return(NULL)
  }

  # Match to included
  articles <- match_to_included(articles, included)

  n_matched <- sum(articles$included)
  recall <- n_matched / length(included)
  prevalence <- n_matched / nrow(articles)

  cat("Matched:", n_matched, "/", length(included),
      "| Recall:", round(recall * 100, 1), "%",
      "| Prevalence:", round(prevalence * 100, 2), "%\n")

  return(list(
    review_id = review_id,
    title = info$title,
    n_included = length(included),
    n_searched = search$count,
    n_fetched = nrow(articles),
    n_matched = n_matched,
    recall = recall,
    prevalence = prevalence,
    articles = articles
  ))
}

# ========================================
# MAIN
# ========================================
rds_dir <- "C:/Users/user/OneDrive - NHS/Documents/Pairwise70/analysis/output/cleaned_rds"
rds_files <- list.files(rds_dir, pattern = "\\.rds$", full.names = TRUE)

cat("Processing", min(10, length(rds_files)), "reviews...\n")

results <- list()
for (i in 1:min(10, length(rds_files))) {
  d <- readRDS(rds_files[i])
  review_id <- gsub("_data\\.rds$", "", basename(rds_files[i]))

  result <- process_review(review_id, d)
  if (!is.null(result)) {
    results[[review_id]] <- result
  }

  Sys.sleep(1)  # Rate limit
}

# ========================================
# Create ASReview dataset
# ========================================
cat("\n\n=== CREATING ASREVIEW DATASET ===\n")

if (length(results) > 0) {
  # Summary
  summary_dt <- rbindlist(lapply(results, function(r) {
    data.table(
      review = r$review_id,
      included = r$n_included,
      fetched = r$n_fetched,
      matched = r$n_matched,
      recall_pct = round(r$recall * 100, 1),
      prevalence_pct = round(r$prevalence * 100, 2)
    )
  }))

  cat("\n--- Summary ---\n")
  print(summary_dt)

  cat("\nMean recall:", round(mean(summary_dt$recall_pct), 1), "%\n")
  cat("Mean prevalence:", round(mean(summary_dt$prevalence_pct), 2), "%\n")

  # Combine all articles
  all_articles <- rbindlist(lapply(results, function(r) {
    r$articles[, review_id := r$review_id]
    return(r$articles)
  }), fill = TRUE)

  cat("\nTotal articles:", nrow(all_articles), "\n")
  cat("  Included (label=1):", sum(all_articles$included), "\n")
  cat("  Excluded (label=0):", sum(!all_articles$included), "\n")

  # ASReview format
  asreview_dt <- all_articles[, .(
    record_id = pmid,
    title = title,
    abstract = abstract,
    authors = authors,
    year = year,
    journal = journal,
    label_included = included,
    review_source = review_id
  )]

  fwrite(asreview_dt, "C:/Users/user/asreview_pairwise70_groundtruth.csv")
  cat("\nSaved: C:/Users/user/asreview_pairwise70_groundtruth.csv\n")

  # Also save as RIS for ASReview import
  cat("\nDataset ready for ASReview training!\n")
  cat("Labels: 1 = included in Cochrane review, 0 = not included\n")
}

cat("\n=== COMPLETE ===\n")
