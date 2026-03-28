library(data.table)
d <- fread("C:/Users/user/asreview_pairwise70_groundtruth.csv")

cat("=== ASReview Ground Truth Dataset ===\n")
cat("Total records:", nrow(d), "\n")
cat("Included (1):", sum(d$label_included), "\n")
cat("Excluded (0):", sum(!d$label_included), "\n")
cat("Prevalence:", round(mean(d$label_included)*100, 1), "%\n")
cat("Reviews:", length(unique(d$review_id)), "\n")
cat("Has abstract:", sum(nchar(d$abstract) > 50), "\n\n")

cat("=== Sample INCLUDED records ===\n")
print(head(d[label_included == 1, .(record_id, title = substr(title, 1, 60))], 5))

cat("\n=== Sample EXCLUDED records ===\n")
print(head(d[label_included == 0, .(record_id, title = substr(title, 1, 60))], 5))

cat("\n=== Year Distribution ===\n")
print(table(d$year, useNA = "ifany"))
