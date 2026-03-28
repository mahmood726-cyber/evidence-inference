# Check all R packages for meta-analysis datasets

cat("Checking R packages for additional meta-analysis datasets:\n\n")

# meta package
if (require(meta, quietly = TRUE)) {
    d <- data(package = "meta")
    cat("meta package datasets:\n")
    print(d$results[, "Item"])
    cat("\n")
}

# netmeta package
if (require(netmeta, quietly = TRUE)) {
    d <- data(package = "netmeta")
    cat("netmeta package datasets:\n")
    print(d$results[, "Item"])
    cat("\n")
}

# metafor package (beyond metadat)
if (require(metafor, quietly = TRUE)) {
    d <- data(package = "metafor")
    cat("metafor package datasets:\n")
    print(d$results[, "Item"])
    cat("\n")
}

# dmetar package
if (require(dmetar, quietly = TRUE)) {
    d <- data(package = "dmetar")
    cat("dmetar package datasets:\n")
    print(d$results[, "Item"])
    cat("\n")
}

# Check CRAN for meta-analysis packages
cat("\nInstalled meta-analysis related packages:\n")
pkgs <- installed.packages()[, "Package"]
meta_pkgs <- pkgs[grepl("meta|rma|bayes", pkgs, ignore.case = TRUE)]
print(meta_pkgs)
