# Extract datasets from ALL R packages with meta-analysis data

library(meta)
library(netmeta)

output_file <- "C:/Users/user/Downloads/Dataextractor/r_packages_additional.js"

all_trials <- list()
trial_id <- 1

# Helper function to add trial
add_trial <- function(source, study_id, effect_type, value, ci_lo, ci_hi) {
    if (is.na(value) || is.na(ci_lo) || is.na(ci_hi)) return(NULL)
    if (ci_lo >= ci_hi) return(NULL)

    list(
        id = paste0("RPKG_", trial_id),
        source = source,
        effect_type = effect_type,
        value = round(value, 4),
        ci_lo = round(ci_lo, 4),
        ci_hi = round(ci_hi, 4),
        study = study_id
    )
}

cat("Extracting from R packages...\n\n")

# ==================== meta package ====================
cat("meta package:\n")

# Fleiss1993bin - binary outcomes
data(Fleiss1993bin, package = "meta")
cat("  Fleiss1993bin:", nrow(Fleiss1993bin), "studies\n")
for (i in 1:nrow(Fleiss1993bin)) {
    # Calculate OR from 2x2 table
    d <- Fleiss1993bin[i, ]
    if (!is.na(d$event.e) && !is.na(d$event.c)) {
        a <- d$event.e; b <- d$n.e - d$event.e
        c <- d$event.c; d_val <- d$n.c - d$event.c
        if (a > 0 && b > 0 && c > 0 && d_val > 0) {
            or <- (a * d_val) / (b * c)
            se_log_or <- sqrt(1/a + 1/b + 1/c + 1/d_val)
            ci_lo <- exp(log(or) - 1.96 * se_log_or)
            ci_hi <- exp(log(or) + 1.96 * se_log_or)
            t <- add_trial("Fleiss1993bin", d$study, "OR", or, ci_lo, ci_hi)
            if (!is.null(t)) {
                all_trials[[trial_id]] <- t
                trial_id <<- trial_id + 1
            }
        }
    }
}

# Fleiss1993cont - continuous outcomes
data(Fleiss1993cont, package = "meta")
cat("  Fleiss1993cont:", nrow(Fleiss1993cont), "studies\n")
for (i in 1:nrow(Fleiss1993cont)) {
    d <- Fleiss1993cont[i, ]
    if (!is.na(d$mean.e) && !is.na(d$mean.c) && !is.na(d$sd.e) && !is.na(d$sd.c)) {
        md <- d$mean.e - d$mean.c
        se <- sqrt(d$sd.e^2/d$n.e + d$sd.c^2/d$n.c)
        ci_lo <- md - 1.96 * se
        ci_hi <- md + 1.96 * se
        t <- add_trial("Fleiss1993cont", d$study, "MD", md, ci_lo, ci_hi)
        if (!is.null(t)) {
            all_trials[[trial_id]] <- t
            trial_id <<- trial_id + 1
        }
    }
}

# Pagliaro1992
data(Pagliaro1992, package = "meta")
cat("  Pagliaro1992:", nrow(Pagliaro1992), "studies\n")
for (i in 1:nrow(Pagliaro1992)) {
    d <- Pagliaro1992[i, ]
    if (!is.na(d$event.e) && !is.na(d$event.c)) {
        a <- d$event.e; b <- d$n.e - d$event.e
        c <- d$event.c; d_val <- d$n.c - d$event.c
        if (a > 0 && b > 0 && c > 0 && d_val > 0) {
            or <- (a * d_val) / (b * c)
            se_log_or <- sqrt(1/a + 1/b + 1/c + 1/d_val)
            ci_lo <- exp(log(or) - 1.96 * se_log_or)
            ci_hi <- exp(log(or) + 1.96 * se_log_or)
            t <- add_trial("Pagliaro1992", d$study, "OR", or, ci_lo, ci_hi)
            if (!is.null(t)) {
                all_trials[[trial_id]] <- t
                trial_id <<- trial_id + 1
            }
        }
    }
}

# amlodipine
data(amlodipine, package = "meta")
cat("  amlodipine:", nrow(amlodipine), "studies\n")
for (i in 1:nrow(amlodipine)) {
    d <- amlodipine[i, ]
    if (!is.na(d$n.amlo) && !is.na(d$n.plac)) {
        a <- d$deat.amlo; b <- d$n.amlo - d$deat.amlo
        c <- d$deat.plac; d_val <- d$n.plac - d$deat.plac
        if (!is.na(a) && !is.na(c) && a > 0 && b > 0 && c > 0 && d_val > 0) {
            or <- (a * d_val) / (b * c)
            se_log_or <- sqrt(1/a + 1/b + 1/c + 1/d_val)
            ci_lo <- exp(log(or) - 1.96 * se_log_or)
            ci_hi <- exp(log(or) + 1.96 * se_log_or)
            t <- add_trial("amlodipine", d$study, "OR", or, ci_lo, ci_hi)
            if (!is.null(t)) {
                all_trials[[trial_id]] <- t
                trial_id <<- trial_id + 1
            }
        }
    }
}

# lungcancer
data(lungcancer, package = "meta")
cat("  lungcancer:", nrow(lungcancer), "studies\n")
for (i in 1:nrow(lungcancer)) {
    d <- lungcancer[i, ]
    if (!is.na(d$d.smokers) && !is.na(d$d.nonsmokers)) {
        # This is case-control, calculate OR
        a <- d$d.smokers; b <- d$d.nonsmokers
        c <- d$h.smokers; d_val <- d$h.nonsmokers
        if (!is.na(c) && !is.na(d_val) && a > 0 && b > 0 && c > 0 && d_val > 0) {
            or <- (a * d_val) / (b * c)
            se_log_or <- sqrt(1/a + 1/b + 1/c + 1/d_val)
            ci_lo <- exp(log(or) - 1.96 * se_log_or)
            ci_hi <- exp(log(or) + 1.96 * se_log_or)
            t <- add_trial("lungcancer", d$study, "OR", or, ci_lo, ci_hi)
            if (!is.null(t)) {
                all_trials[[trial_id]] <- t
                trial_id <<- trial_id + 1
            }
        }
    }
}

# smoking
data(smoking, package = "meta")
cat("  smoking:", nrow(smoking), "studies\n")
for (i in 1:nrow(smoking)) {
    d <- smoking[i, ]
    if (!is.na(d$event.e) && !is.na(d$event.c)) {
        a <- d$event.e; b <- d$n.e - d$event.e
        c <- d$event.c; d_val <- d$n.c - d$event.c
        if (a > 0 && b > 0 && c > 0 && d_val > 0) {
            rr <- (a / d$n.e) / (c / d$n.c)
            se_log_rr <- sqrt(1/a - 1/d$n.e + 1/c - 1/d$n.c)
            ci_lo <- exp(log(rr) - 1.96 * se_log_rr)
            ci_hi <- exp(log(rr) + 1.96 * se_log_rr)
            t <- add_trial("smoking", d$study, "RR", rr, ci_lo, ci_hi)
            if (!is.null(t)) {
                all_trials[[trial_id]] <- t
                trial_id <<- trial_id + 1
            }
        }
    }
}

# cisapride
data(cisapride, package = "meta")
cat("  cisapride:", nrow(cisapride), "studies\n")
for (i in 1:nrow(cisapride)) {
    d <- cisapride[i, ]
    if (!is.na(d$mean.cisa) && !is.na(d$mean.plac)) {
        md <- d$mean.cisa - d$mean.plac
        se <- sqrt(d$sd.cisa^2/d$n.cisa + d$sd.plac^2/d$n.plac)
        ci_lo <- md - 1.96 * se
        ci_hi <- md + 1.96 * se
        t <- add_trial("cisapride", d$study, "MD", md, ci_lo, ci_hi)
        if (!is.null(t)) {
            all_trials[[trial_id]] <- t
            trial_id <<- trial_id + 1
        }
    }
}

# caffeine
data(caffeine, package = "meta")
cat("  caffeine:", nrow(caffeine), "studies\n")
for (i in 1:nrow(caffeine)) {
    d <- caffeine[i, ]
    if (!is.na(d$mean.e) && !is.na(d$mean.c)) {
        md <- d$mean.e - d$mean.c
        se <- sqrt(d$sd.e^2/d$n.e + d$sd.c^2/d$n.c)
        ci_lo <- md - 1.96 * se
        ci_hi <- md + 1.96 * se
        t <- add_trial("caffeine", d$study, "MD", md, ci_lo, ci_hi)
        if (!is.null(t)) {
            all_trials[[trial_id]] <- t
            trial_id <<- trial_id + 1
        }
    }
}

# ==================== netmeta package ====================
cat("\nnetmeta package:\n")

# smokingcessation (network meta-analysis)
data(smokingcessation, package = "netmeta")
cat("  smokingcessation:", nrow(smokingcessation), "comparisons\n")
for (i in 1:nrow(smokingcessation)) {
    d <- smokingcessation[i, ]
    if (!is.na(d$event1) && !is.na(d$event2)) {
        a <- d$event1; b <- d$n1 - d$event1
        c <- d$event2; d_val <- d$n2 - d$event2
        if (a > 0 && b > 0 && c > 0 && d_val > 0) {
            or <- (a * d_val) / (b * c)
            se_log_or <- sqrt(1/a + 1/b + 1/c + 1/d_val)
            ci_lo <- exp(log(or) - 1.96 * se_log_or)
            ci_hi <- exp(log(or) + 1.96 * se_log_or)
            t <- add_trial("smokingcessation", paste0(d$study, "-", d$treat1, "-", d$treat2), "OR", or, ci_lo, ci_hi)
            if (!is.null(t)) {
                all_trials[[trial_id]] <- t
                trial_id <<- trial_id + 1
            }
        }
    }
}

# parkinson
data(parkinson, package = "netmeta")
cat("  parkinson:", nrow(parkinson), "comparisons\n")
for (i in 1:nrow(parkinson)) {
    d <- parkinson[i, ]
    if (!is.na(d$mean1) && !is.na(d$mean2) && !is.na(d$sd1) && !is.na(d$sd2)) {
        md <- d$mean1 - d$mean2
        se <- sqrt(d$sd1^2/d$n1 + d$sd2^2/d$n2)
        ci_lo <- md - 1.96 * se
        ci_hi <- md + 1.96 * se
        t <- add_trial("parkinson", paste0(d$study, "-", d$treat1, "-", d$treat2), "MD", md, ci_lo, ci_hi)
        if (!is.null(t)) {
            all_trials[[trial_id]] <- t
            trial_id <<- trial_id + 1
        }
    }
}

# Senn2013
data(Senn2013, package = "netmeta")
cat("  Senn2013:", nrow(Senn2013), "comparisons\n")
for (i in 1:nrow(Senn2013)) {
    d <- Senn2013[i, ]
    if (!is.na(d$TE) && !is.na(d$seTE)) {
        md <- d$TE
        ci_lo <- md - 1.96 * d$seTE
        ci_hi <- md + 1.96 * d$seTE
        t <- add_trial("Senn2013", paste0(d$study, "-", d$treat1, "-", d$treat2), "MD", md, ci_lo, ci_hi)
        if (!is.null(t)) {
            all_trials[[trial_id]] <- t
            trial_id <<- trial_id + 1
        }
    }
}

# Woods2010
data(Woods2010, package = "netmeta")
cat("  Woods2010:", nrow(Woods2010), "comparisons\n")
for (i in 1:nrow(Woods2010)) {
    d <- Woods2010[i, ]
    if (!is.na(d$TE) && !is.na(d$seTE)) {
        # HR on log scale
        hr <- exp(d$TE)
        ci_lo <- exp(d$TE - 1.96 * d$seTE)
        ci_hi <- exp(d$TE + 1.96 * d$seTE)
        t <- add_trial("Woods2010", paste0(d$study, "-", d$treat1, "-", d$treat2), "HR", hr, ci_lo, ci_hi)
        if (!is.null(t)) {
            all_trials[[trial_id]] <- t
            trial_id <<- trial_id + 1
        }
    }
}

# dietaryfat
data(dietaryfat, package = "netmeta")
cat("  dietaryfat:", nrow(dietaryfat), "comparisons\n")
for (i in 1:nrow(dietaryfat)) {
    d <- dietaryfat[i, ]
    if (!is.na(d$TE) && !is.na(d$seTE)) {
        # RR on log scale
        rr <- exp(d$TE)
        ci_lo <- exp(d$TE - 1.96 * d$seTE)
        ci_hi <- exp(d$TE + 1.96 * d$seTE)
        t <- add_trial("dietaryfat", paste0(d$study, "-", d$treat1, "-", d$treat2), "RR", rr, ci_lo, ci_hi)
        if (!is.null(t)) {
            all_trials[[trial_id]] <- t
            trial_id <<- trial_id + 1
        }
    }
}

# Baker2009
data(Baker2009, package = "netmeta")
cat("  Baker2009:", nrow(Baker2009), "comparisons\n")
for (i in 1:nrow(Baker2009)) {
    d <- Baker2009[i, ]
    if (!is.na(d$lnOR) && !is.na(d$selnOR)) {
        or <- exp(d$lnOR)
        ci_lo <- exp(d$lnOR - 1.96 * d$selnOR)
        ci_hi <- exp(d$lnOR + 1.96 * d$selnOR)
        t <- add_trial("Baker2009", paste0(d$study, "-", d$treatment, "-vs-placebo"), "OR", or, ci_lo, ci_hi)
        if (!is.null(t)) {
            all_trials[[trial_id]] <- t
            trial_id <<- trial_id + 1
        }
    }
}

# Dong2013
data(Dong2013, package = "netmeta")
cat("  Dong2013:", nrow(Dong2013), "comparisons\n")
for (i in 1:nrow(Dong2013)) {
    d <- Dong2013[i, ]
    if (!is.na(d$death1) && !is.na(d$death2) && !is.na(d$randomized1) && !is.na(d$randomized2)) {
        a <- d$death1; b <- d$randomized1 - d$death1
        c <- d$death2; d_val <- d$randomized2 - d$death2
        if (a > 0 && b > 0 && c > 0 && d_val > 0) {
            or <- (a * d_val) / (b * c)
            se_log_or <- sqrt(1/a + 1/b + 1/c + 1/d_val)
            ci_lo <- exp(log(or) - 1.96 * se_log_or)
            ci_hi <- exp(log(or) + 1.96 * se_log_or)
            t <- add_trial("Dong2013", paste0(d$id, "-", d$treatment1, "-", d$treatment2), "OR", or, ci_lo, ci_hi)
            if (!is.null(t)) {
                all_trials[[trial_id]] <- t
                trial_id <<- trial_id + 1
            }
        }
    }
}

cat("\n")
cat("Total additional trials extracted:", length(all_trials), "\n")

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
