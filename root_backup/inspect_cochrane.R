# Inspect single Cochrane file
data_dir <- "C:/Users/user/OneDrive - NHS/Documents/Pairwise70/data"
files <- list.files(data_dir, pattern = "\\.rda$", full.names = TRUE)

# Load first file
f <- files[1]
cat("Loading:", basename(f), "\n\n")

env <- new.env()
load(f, envir = env)

cat("Objects in file:\n")
print(ls(env))

obj_name <- ls(env)[1]
data <- get(obj_name, envir = env)

cat("\nClass:", class(data), "\n")
cat("Type:", typeof(data), "\n")

if (is.data.frame(data)) {
    cat("Columns:", paste(names(data), collapse=", "), "\n")
    cat("Rows:", nrow(data), "\n\n")
    cat("Structure:\n")
    str(data)
    cat("\n\nFirst 3 rows:\n")
    print(head(data, 3))
} else if (is.list(data)) {
    cat("List elements:", names(data), "\n")
    cat("\nStructure:\n")
    str(data, max.level = 2)
}
