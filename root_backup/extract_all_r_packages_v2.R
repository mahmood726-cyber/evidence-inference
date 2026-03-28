# Extract datasets from ALL R packages with meta-analysis data
# Fixed NA handling

library(meta)
library(netmeta)

output_file <- "C:/Users/user/Downloads/Dataextractor/r_packages_additional.js"

all_trials <- list()
trial_id <- 1

# Helper function to add trial
add_trial <- function(source, study_id, effect_type, value, ci_lo, ci_hi) {
    if (is.null(value) || is.null(ci_lo) || is.null(ci_hi)) return(NULL)
    if (is.na(value) || is.na(ci_lo) || is.na(ci_hi)) return(NULL)
    if (!is.finite(value) || !is.finite(ci_lo) || !is.finite(ci_hi)) return(NULL)
    if (ci_lo >= ci_hi) return(NULL)

    trial_id <<- trial_id + 1
    list(
        id = paste0("RPKG_", trial_id - 1),
        source = source,
        effect_type = effect_type,
        value = round(value, 4),
        ci_lo = round(ci_lo, 4),
        ci_hi = round(ci_hi, 4),
        study = as.character(study_id)
    )
}

# Calculate OR from 2x2 table
calc_or <- function(a, b, c, d_val) {
    if (any(is.na(c(a, b, c, d_val)))) return(NULL)
    if (any(c(a, b, c, d_val) <= 0)) return(NULL)
    or <- (a * d_val) / (b * c)
    se_log_or <- sqrt(1/a + 1/b + 1/c + 1/d_val)
    list(or = or, ci_lo = exp(log(or) - 1.96 * se_log_or), ci_hi = exp(log(or) + 1.96 * se_log_or))
}

# Calculate RR from counts
calc_rr <- function(e1, n1, e2, n2) {
    if (any(is.na(c(e1, n1, e2, n2)))) return(NULL)
    if (e1 <= 0 || e2 <= 0) return(NULL)
    rr <- (e1 / n1) / (e2 / n2)
    se_log_rr <- sqrt(1/e1 - 1/n1 + 1/e2 - 1/n2)
    list(rr = rr, ci_lo = exp(log(rr) - 1.96 * se_log_rr), ci_hi = exp(log(rr) + 1.96 * se_log_rr))
}

# Calculate MD from means
calc_md <- function(m1, m2, sd1, sd2, n1, n2) {
    if (any(is.na(c(m1, m2, sd1, sd2, n1, n2)))) return(NULL)
    if (n1 <= 0 || n2 <= 0) return(NULL)
    md <- m1 - m2
    se <- sqrt(sd1^2/n1 + sd2^2/n2)
    list(md = md, ci_lo = md - 1.96 * se, ci_hi = md + 1.96 * se)
}

cat("Extracting from R packages...\n\n")

# ==================== meta package ====================
cat("meta package:\n")

# Fleiss1993bin - binary outcomes
tryCatch({
    data(Fleiss1993bin, package = "meta")
    cat("  Fleiss1993bin:", nrow(Fleiss1993bin), "studies\n")
    for (i in 1:nrow(Fleiss1993bin)) {
        d <- Fleiss1993bin[i, ]
        res <- calc_or(d$event.e, d$n.e - d$event.e, d$event.c, d$n.c - d$event.c)
        if (!is.null(res)) {
            t <- add_trial("Fleiss1993bin", d$study, "OR", res$or, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# Fleiss1993cont
tryCatch({
    data(Fleiss1993cont, package = "meta")
    cat("  Fleiss1993cont:", nrow(Fleiss1993cont), "studies\n")
    for (i in 1:nrow(Fleiss1993cont)) {
        d <- Fleiss1993cont[i, ]
        res <- calc_md(d$mean.e, d$mean.c, d$sd.e, d$sd.c, d$n.e, d$n.c)
        if (!is.null(res)) {
            t <- add_trial("Fleiss1993cont", d$study, "MD", res$md, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# Pagliaro1992
tryCatch({
    data(Pagliaro1992, package = "meta")
    cat("  Pagliaro1992:", nrow(Pagliaro1992), "studies\n")
    for (i in 1:nrow(Pagliaro1992)) {
        d <- Pagliaro1992[i, ]
        res <- calc_or(d$event.e, d$n.e - d$event.e, d$event.c, d$n.c - d$event.c)
        if (!is.null(res)) {
            t <- add_trial("Pagliaro1992", d$study, "OR", res$or, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# smoking
tryCatch({
    data(smoking, package = "meta")
    cat("  smoking:", nrow(smoking), "studies\n")
    for (i in 1:nrow(smoking)) {
        d <- smoking[i, ]
        res <- calc_rr(d$event.e, d$n.e, d$event.c, d$n.c)
        if (!is.null(res)) {
            t <- add_trial("smoking", d$study, "RR", res$rr, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# cisapride
tryCatch({
    data(cisapride, package = "meta")
    cat("  cisapride:", nrow(cisapride), "studies\n")
    for (i in 1:nrow(cisapride)) {
        d <- cisapride[i, ]
        res <- calc_md(d$mean.cisa, d$mean.plac, d$sd.cisa, d$sd.plac, d$n.cisa, d$n.plac)
        if (!is.null(res)) {
            t <- add_trial("cisapride", d$study, "MD", res$md, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# caffeine
tryCatch({
    data(caffeine, package = "meta")
    cat("  caffeine:", nrow(caffeine), "studies\n")
    for (i in 1:nrow(caffeine)) {
        d <- caffeine[i, ]
        res <- calc_md(d$mean.e, d$mean.c, d$sd.e, d$sd.c, d$n.e, d$n.c)
        if (!is.null(res)) {
            t <- add_trial("caffeine", d$study, "MD", res$md, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# lungcancer
tryCatch({
    data(lungcancer, package = "meta")
    cat("  lungcancer:", nrow(lungcancer), "studies\n")
    for (i in 1:nrow(lungcancer)) {
        d <- lungcancer[i, ]
        res <- calc_or(d$d.smokers, d$d.nonsmokers, d$h.smokers, d$h.nonsmokers)
        if (!is.null(res)) {
            t <- add_trial("lungcancer", d$study, "OR", res$or, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# ==================== netmeta package ====================
cat("\nnetmeta package:\n")

# smokingcessation
tryCatch({
    data(smokingcessation, package = "netmeta")
    cat("  smokingcessation:", nrow(smokingcessation), "comparisons\n")
    for (i in 1:nrow(smokingcessation)) {
        d <- smokingcessation[i, ]
        res <- calc_or(d$event1, d$n1 - d$event1, d$event2, d$n2 - d$event2)
        if (!is.null(res)) {
            t <- add_trial("smokingcessation", paste0(d$study, "-", d$treat1, "-", d$treat2), "OR", res$or, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# parkinson
tryCatch({
    data(parkinson, package = "netmeta")
    cat("  parkinson:", nrow(parkinson), "comparisons\n")
    for (i in 1:nrow(parkinson)) {
        d <- parkinson[i, ]
        res <- calc_md(d$mean1, d$mean2, d$sd1, d$sd2, d$n1, d$n2)
        if (!is.null(res)) {
            t <- add_trial("parkinson", paste0(d$study, "-", d$treat1, "-", d$treat2), "MD", res$md, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# Senn2013
tryCatch({
    data(Senn2013, package = "netmeta")
    cat("  Senn2013:", nrow(Senn2013), "comparisons\n")
    for (i in 1:nrow(Senn2013)) {
        d <- Senn2013[i, ]
        if (!is.na(d$TE) && !is.na(d$seTE) && is.finite(d$TE) && is.finite(d$seTE)) {
            md <- d$TE
            ci_lo <- md - 1.96 * d$seTE
            ci_hi <- md + 1.96 * d$seTE
            t <- add_trial("Senn2013", paste0(d$study, "-", d$treat1, "-", d$treat2), "MD", md, ci_lo, ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# Woods2010
tryCatch({
    data(Woods2010, package = "netmeta")
    cat("  Woods2010:", nrow(Woods2010), "comparisons\n")
    for (i in 1:nrow(Woods2010)) {
        d <- Woods2010[i, ]
        if (!is.na(d$TE) && !is.na(d$seTE) && is.finite(d$TE) && is.finite(d$seTE)) {
            hr <- exp(d$TE)
            ci_lo <- exp(d$TE - 1.96 * d$seTE)
            ci_hi <- exp(d$TE + 1.96 * d$seTE)
            t <- add_trial("Woods2010", paste0(d$study, "-", d$treat1, "-", d$treat2), "HR", hr, ci_lo, ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# dietaryfat
tryCatch({
    data(dietaryfat, package = "netmeta")
    cat("  dietaryfat:", nrow(dietaryfat), "comparisons\n")
    for (i in 1:nrow(dietaryfat)) {
        d <- dietaryfat[i, ]
        if (!is.na(d$TE) && !is.na(d$seTE) && is.finite(d$TE) && is.finite(d$seTE)) {
            rr <- exp(d$TE)
            ci_lo <- exp(d$TE - 1.96 * d$seTE)
            ci_hi <- exp(d$TE + 1.96 * d$seTE)
            t <- add_trial("dietaryfat", paste0(d$study, "-", d$treat1, "-", d$treat2), "RR", rr, ci_lo, ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

# Dong2013
tryCatch({
    data(Dong2013, package = "netmeta")
    cat("  Dong2013:", nrow(Dong2013), "comparisons\n")
    for (i in 1:nrow(Dong2013)) {
        d <- Dong2013[i, ]
        res <- calc_or(d$death1, d$randomized1 - d$death1, d$death2, d$randomized2 - d$death2)
        if (!is.null(res)) {
            t <- add_trial("Dong2013", paste0(d$id, "-", d$treatment1, "-", d$treatment2), "OR", res$or, res$ci_lo, res$ci_hi)
            if (!is.null(t)) all_trials[[length(all_trials) + 1]] <- t
        }
    }
}, error = function(e) cat("  Error:", e$message, "\n"))

cat("\n")
cat("Total additional trials extracted:", length(all_trials), "\n")

if (length(all_trials) > 0) {
    # Count by type
    types <- sapply(all_trials, function(x) x$effect_type)
    cat("\nBy effect type:\n")
    print(table(types))

    # Write JavaScript file
    cat("\nWriting JavaScript file...\n")

    js_lines <- c(
        "// Additional R Package Meta-Analysis Datasets",
        paste0("// Total: ", length(all_trials), " trials"),
        "",
        "const R_PACKAGES_ADDITIONAL = ["
    )

    for (t in all_trials) {
        text <- paste0(t$id, ": ", t$source, " - ", t$study, ". Results: ", t$effect_type, " ",
                       sprintf("%.2f", t$value), ", 95% CI ", sprintf("%.2f", t$ci_lo), "-", sprintf("%.2f", t$ci_hi), ".")
        text <- gsub("'", "\\\\'", text)
        text <- gsub("[\r\n]", " ", text)

        js_lines <- c(js_lines, paste0(
            "    { id: '", t$id, "', text: '", text, "', groundTruth: { primaryEffect: { type: '",
            t$effect_type, "', value: ", t$value, ", ciLo: ", t$ci_lo, ", ciHi: ", t$ci_hi, " } } },"
        ))
    }

    js_lines <- c(js_lines, "];", "",
        "if (typeof module !== 'undefined' && module.exports) {",
        "    module.exports = { R_PACKAGES_ADDITIONAL };",
        "}"
    )

    writeLines(js_lines, output_file)
    cat("Saved to", output_file, "\n")
}
