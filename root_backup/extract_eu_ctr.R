# Extract data from EU Clinical Trials Register using ctrdata R package

# Install and load required packages
if (!require(ctrdata, quietly = TRUE)) {
    install.packages("ctrdata", repos = "https://cloud.r-project.org")
}
library(ctrdata)

cat("Checking ctrdata package functions...\n")
print(ls("package:ctrdata"))

# Check available databases
cat("\nChecking database connections...\n")

# Try to query EU CTR for some trials
tryCatch({
    cat("Attempting EU CTR query...\n")
    # Query for completed trials with results
    q <- ctrGetQueryUrl(
        url = paste0(
            "https://www.clinicaltrialsregister.eu/ctr-search/search?query=&status=completed&resultsstatus=trials-with-results"
        )
    )
    cat("Query URL parsed successfully\n")
    print(q)
}, error = function(e) {
    cat("EU CTR query error:", conditionMessage(e), "\n")
})

# Also check for local data or databases
cat("\n\nChecking for any pre-existing database connections...\n")
cat("ctrdata version:", as.character(packageVersion("ctrdata")), "\n")
