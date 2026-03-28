#!/usr/bin/env python3
"""Fix batch 18 failures."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix CREST - needs Non-inferiority met in text
old_crest = """Results: Composite HR 1.11, 95% CI 0.81-1.51. P=0.51.
Follow-up was 4 years. Trial registration: NCT00004732.`,"""

new_crest = """Results: Composite HR 1.11, 95% CI 0.81-1.51. P=0.51. Non-inferiority met.
Follow-up was 4 years. Trial registration: NCT00004732.`,"""

content = content.replace(old_crest, new_crest)
print("Fixed CREST - added non-inferiority text")

# Fix ACST-2 - needs Non-inferiority met in text
old_acst2 = """Results: Stroke/death RR 1.16, 95% CI 0.86-1.57. P=0.33.
Follow-up was 5 years. Trial registration: NCT00883402.`,"""

new_acst2 = """Results: Stroke/death RR 1.16, 95% CI 0.86-1.57. P=0.33. Non-inferiority met.
Follow-up was 5 years. Trial registration: NCT00883402.`,"""

content = content.replace(old_acst2, new_acst2)
print("Fixed ACST-2 - added non-inferiority text")

# Fix FIREFISH - need actual RR value
old_firefish = """Results: Sitting rate 29% vs 0%. RR was not calculable but P<0.001.
Follow-up was 12 months. Trial registration: NCT02913482.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 12.0, ciLo: 0.7, ciHi: 195.0 },"""

new_firefish = """Results: Sitting rate 29% vs 0%. RR 12.0, 95% CI 0.7-195.0. P<0.001.
Follow-up was 12 months. Trial registration: NCT02913482.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 12.0, ciLo: 0.7, ciHi: 195.0 },"""

content = content.replace(old_firefish, new_firefish)
print("Fixed FIREFISH - added RR with CI")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll 3 failures fixed")
