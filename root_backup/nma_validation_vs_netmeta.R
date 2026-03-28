# NMA Pro v7.0 Validation Against R netmeta Package
# ================================================
# This script validates NMA Pro browser-based calculations against
# the gold-standard netmeta R package (Schwarzer et al.)
#
# Run this script and compare outputs with NMA Pro to verify accuracy

# Install required packages if not present
if (!require("netmeta")) install.packages("netmeta")
if (!require("meta")) install.packages("meta")
if (!require("jsonlite")) install.packages("jsonlite")

library(netmeta)
library(meta)
library(jsonlite)

cat("=" , rep("=", 69), "\n", sep="")
cat("NMA Pro v7.0 - VALIDATION AGAINST R netmeta\n")
cat("=" , rep("=", 69), "\n\n", sep="")

# ============================================================
# DATASET 1: Thrombolytics (Same as NMA Pro Demo)
# ============================================================

cat("DATASET 1: Thrombolytics\n")
cat("-" , rep("-", 40), "\n", sep="")

# Create the exact same data as NMA Pro demo
thrombo <- data.frame(
  study = c("Coll1988", "DeWood1990", "GISSI-2", "Guerci1987", "ISAM1986",
            "ISIS-3", "Neuhaus1992", "PRIMI1989", "White1989", "Topol1991"),
  treat1 = c("SK", "SK", "SK", "SK", "SK", "SK", "tPA", "SK", "SK", "tPA"),
  treat2 = c("tPA", "tPA", "tPA", "tPA", "Placebo", "tPA", "Acc-tPA", "APSAC", "APSAC", "APSAC"),
  event1 = c(8, 6, 887, 2, 32, 2859, 10, 7, 5, 10),
  n1 = c(54, 63, 10396, 61, 441, 13780, 100, 201, 135, 172),
  event2 = c(4, 4, 1017, 3, 8, 2855, 3, 13, 8, 14),
  n2 = c(56, 62, 10372, 77, 438, 13773, 100, 200, 135, 181)
)

# Convert to pairwise format
p1 <- pairwise(treat = list(treat1, treat2),
               event = list(event1, event2),
               n = list(n1, n2),
               data = thrombo,
               studlab = study,
               sm = "OR")

# Run network meta-analysis
net1 <- netmeta(TE, seTE, treat1, treat2, studlab,
                data = p1,
                sm = "OR",
                reference.group = "Placebo",
                common = FALSE,
                random = TRUE)

cat("\n--- Heterogeneity Statistics ---\n")
cat(sprintf("tau^2 (between-study variance): %.6f\n", net1$tau^2))
cat(sprintf("tau (SD): %.6f\n", net1$tau))
cat(sprintf("I^2: %.1f%%\n", net1$I2.random * 100))
cat(sprintf("Q statistic: %.4f\n", net1$Q))
cat(sprintf("df: %d\n", net1$df.Q))
cat(sprintf("p-value for Q: %.6f\n", net1$pval.Q))

cat("\n--- Treatment Effects vs Placebo (OR scale) ---\n")
# Get effects vs reference
effects <- exp(net1$TE.random[, "Placebo"])
ci_lower <- exp(net1$lower.random[, "Placebo"])
ci_upper <- exp(net1$upper.random[, "Placebo"])

for (t in names(effects)) {
  if (t != "Placebo") {
    cat(sprintf("%s vs Placebo: OR=%.4f (95%% CI: %.4f - %.4f)\n",
                t, effects[t], ci_lower[t], ci_upper[t]))
  }
}

cat("\n--- P-scores (Treatment Rankings) ---\n")
ranks <- netrank(net1, small.values = "undesirable")
print(ranks)

cat("\n--- League Table ---\n")
league <- netleague(net1, digits = 3)
print(league$random, quote = FALSE)


# ============================================================
# DATASET 2: Smoking Cessation (Classic NMA Example)
# ============================================================

cat("\n\n")
cat("DATASET 2: Smoking Cessation (Hasselblad 1998)\n")
cat("-" , rep("-", 40), "\n", sep="")

data(smokingcessation)
# Run pairwise
p2 <- pairwise(treat = list(treat1, treat2, treat3),
               event = list(event1, event2, event3),
               n = list(n1, n2, n3),
               data = smokingcessation,
               sm = "OR")

net2 <- netmeta(TE, seTE, treat1, treat2, studlab,
                data = p2,
                sm = "OR",
                reference.group = "A",
                common = FALSE,
                random = TRUE)

cat("\n--- Heterogeneity Statistics ---\n")
cat(sprintf("tau^2: %.6f\n", net2$tau^2))
cat(sprintf("I^2: %.1f%%\n", net2$I2.random * 100))
cat(sprintf("Q: %.4f (df=%d, p=%.6f)\n", net2$Q, net2$df.Q, net2$pval.Q))

cat("\n--- P-scores ---\n")
ranks2 <- netrank(net2, small.values = "undesirable")
print(ranks2)


# ============================================================
# DATASET 3: Parkinson's Disease
# ============================================================

cat("\n\n")
cat("DATASET 3: Parkinson's Disease\n")
cat("-" , rep("-", 40), "\n", sep="")

data(parkinson)

net3 <- netmeta(TE, seTE, treat1, treat2, studlab,
                data = parkinson,
                sm = "MD",
                reference.group = "1",
                common = FALSE,
                random = TRUE)

cat("\n--- Heterogeneity Statistics ---\n")
cat(sprintf("tau^2: %.6f\n", net3$tau^2))
cat(sprintf("I^2: %.1f%%\n", net3$I2.random * 100))
cat(sprintf("Q: %.4f (df=%d, p=%.6f)\n", net3$Q, net3$df.Q, net3$pval.Q))

cat("\n--- P-scores ---\n")
ranks3 <- netrank(net3, small.values = "desirable")
print(ranks3)


# ============================================================
# VALIDATION SUMMARY
# ============================================================

cat("\n\n")
cat("=" , rep("=", 69), "\n", sep="")
cat("VALIDATION REFERENCE VALUES\n")
cat("=" , rep("=", 69), "\n", sep="")

cat("\nThese values should match NMA Pro v7.0 outputs:\n\n")

cat("THROMBOLYTICS DATASET:\n")
cat(sprintf("  tau^2 = %.6f\n", net1$tau^2))
cat(sprintf("  I^2 = %.1f%%\n", net1$I2.random * 100))
cat(sprintf("  Q = %.4f (df=%d)\n", net1$Q, net1$df.Q))
cat("  P-scores:\n")
for (i in 1:nrow(ranks$ranking)) {
  cat(sprintf("    %s: %.4f\n", rownames(ranks$ranking)[i], ranks$ranking$`P-score`[i]))
}

cat("\nSMOKING CESSATION DATASET:\n")
cat(sprintf("  tau^2 = %.6f\n", net2$tau^2))
cat(sprintf("  I^2 = %.1f%%\n", net2$I2.random * 100))

cat("\nPARKINSON DATASET:\n")
cat(sprintf("  tau^2 = %.6f\n", net3$tau^2))
cat(sprintf("  I^2 = %.1f%%\n", net3$I2.random * 100))

cat("\n")
cat("=" , rep("=", 69), "\n", sep="")
cat("Run NMA Pro with same datasets and compare values.\n")
cat("Acceptable tolerance: tau^2 within 5%, I^2 within 1%, P-scores within 0.01\n")
cat("=" , rep("=", 69), "\n", sep="")


# ============================================================
# EXPORT VALIDATION DATA AS JSON FOR NMA PRO
# ============================================================

validation_data <- list(
  thrombolytics = list(
    tau2 = net1$tau^2,
    tau = net1$tau,
    I2 = net1$I2.random * 100,
    Q = net1$Q,
    df = net1$df.Q,
    pQ = net1$pval.Q,
    pscores = as.list(setNames(ranks$ranking$`P-score`, rownames(ranks$ranking)))
  ),
  smoking = list(
    tau2 = net2$tau^2,
    I2 = net2$I2.random * 100,
    Q = net2$Q
  ),
  parkinson = list(
    tau2 = net3$tau^2,
    I2 = net3$I2.random * 100,
    Q = net3$Q
  )
)

# Save validation reference
write(toJSON(validation_data, pretty = TRUE, auto_unbox = TRUE),
      "nma_validation_reference.json")

cat("\nValidation reference saved to: nma_validation_reference.json\n")
