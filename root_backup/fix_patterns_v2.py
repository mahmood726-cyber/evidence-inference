#!/usr/bin/env python3
"""
Fix RCTExtractor patterns - version 2
Handle real NEJM article formats like:
- "hazard ratio, 0.79; 95% confidence interval [CI], 0.66 to 0.95"
- "hazard ratio with apixaban, 0.79"
- "relative risk with dabigatran, 0.91"
"""

import re

file_path = r'C:\Users\user\Downloads\Dataextractor\RCTExtractor_WebApp.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and update the patterns - more flexible version
old_hr_pattern = '''            HR: [
                // HR 0.80; 95% CI, 0.73 to 0.87 OR HR 0.80; 95% CI 0.73-0.87
                /(?:HR|hazard\\s*ratio)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:HR|hazard\\s*ratio)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi,
                /(?:hazard\\s+ratio\\s+(?:of|was|=))\\s*(-?\\d+\\.?\\d*)/gi
            ],'''

new_hr_pattern = '''            HR: [
                // Flexible HR pattern for NEJM format: "hazard ratio with X, 0.79; 95% confidence interval [CI], 0.66 to 0.95"
                /(?:HR|hazard\\s*ratio)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                // Simple HR value: "HR 0.80" or "hazard ratio, 0.79"
                /(?:HR|hazard\\s*ratio)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi,
                // "hazard ratio of/was/= X"
                /(?:hazard\\s+ratio\\s+(?:of|was|=))\\s*(-?\\d+\\.?\\d*)/gi
            ],'''

if old_hr_pattern in content:
    content = content.replace(old_hr_pattern, new_hr_pattern)
    print("HR pattern updated")
else:
    print("HR pattern not found - trying to insert manually")
    # More aggressive search
    hr_section = re.search(r"HR:\s*\[\s*//.*?hazard.*?\],", content, re.DOTALL)
    if hr_section:
        print(f"Found HR section at {hr_section.start()}")

# Update RR pattern
old_rr_pattern = '''            RR: [
                // RR 0.91; 95% CI, 0.74 to 1.11 or relative risk, 0.66; 95% CI, 0.53 to 0.82
                /(?:RR|relative\\s*risk)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:RR|relative\\s*risk)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:relative\\s*risk)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],'''

new_rr_pattern = '''            RR: [
                // Flexible RR pattern: "relative risk with dabigatran, 0.91; 95% confidence interval [CI], 0.74 to 1.11"
                /(?:RR|relative\\s*risk)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:RR|relative\\s*risk)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:relative\\s*risk)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],'''

if old_rr_pattern in content:
    content = content.replace(old_rr_pattern, new_rr_pattern)
    print("RR pattern updated")
else:
    print("RR pattern not found")

# Update OR pattern
old_or_pattern = '''            OR: [
                // OR 0.84; 95% CI 0.71-0.99 or odds ratio of 2.3
                /(?:OR|odds\\s*ratio)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:odds\\s*ratio)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:odds\\s*ratio|OR)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],'''

new_or_pattern = '''            OR: [
                // Flexible OR pattern: "odds ratio with X, 0.84; 95% confidence interval [CI], 0.71-0.99"
                /(?:OR|odds\\s*ratio)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:odds\\s*ratio)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:odds\\s*ratio|OR)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],'''

if old_or_pattern in content:
    content = content.replace(old_or_pattern, new_or_pattern)
    print("OR pattern updated")
else:
    print("OR pattern not found")

# Update MD pattern
old_md_pattern = '''            MD: [
                // MD -14.8, 95% CI -15.5 to -14.1 or mean difference -2.3 (95% CI -4.1--0.5)
                /(?:MD|mean\\s*difference)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:MD|mean\\s*difference)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:mean\\s*difference)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],'''

new_md_pattern = '''            MD: [
                // Flexible MD pattern with confidence interval [CI] support
                /(?:MD|mean\\s*difference)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:MD|mean\\s*difference)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:mean\\s*difference)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],'''

if old_md_pattern in content:
    content = content.replace(old_md_pattern, new_md_pattern)
    print("MD pattern updated")
else:
    print("MD pattern not found")

# Update SMD pattern
old_smd_pattern = '''            SMD: [
                // SMD -0.31, 95% CI -0.49 to -0.13 or standardized mean difference
                /(?:SMD|standardized?\\s*mean\\s*difference)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:SMD|standardized?\\s*mean\\s*difference)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:standardized?\\s*mean\\s*difference)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi,
                // Hedges' g or Cohen's d
                /(?:hedges['']?\\s*g|cohen['']?s?\\s*d)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi
            ],'''

new_smd_pattern = '''            SMD: [
                // Flexible SMD pattern with confidence interval [CI] support
                /(?:SMD|standardized?\\s*mean\\s*difference)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:SMD|standardized?\\s*mean\\s*difference)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:standardized?\\s*mean\\s*difference)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi,
                // Hedges' g or Cohen's d
                /(?:hedges['']?\\s*g|cohen['']?s?\\s*d)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi
            ],'''

if old_smd_pattern in content:
    content = content.replace(old_smd_pattern, new_smd_pattern)
    print("SMD pattern updated")
else:
    print("SMD pattern not found")

# Update version
content = content.replace("version: '4.9.0-AI-Web'", "version: '4.9.1-AI-Web'")
print("Version updated to 4.9.1")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nPatterns updated for real NEJM article formats!")
print("Changes: Added support for 'confidence interval [CI]' and 'X with Y' formats")
