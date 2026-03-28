#!/usr/bin/env python3
"""
Fix RCTExtractor patterns - version 3
Handle multi-word drug/group names like:
- "hazard ratio in the LCZ696 group, 0.80"
- "hazard ratio for the primary endpoint, 0.74"
"""

import re

file_path = r'C:\Users\user\Downloads\Dataextractor\RCTExtractor_WebApp.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update HR pattern to handle multi-word phrases like "in the LCZ696 group"
old_hr_pattern = '''            HR: [
                // Flexible HR pattern for NEJM format: "hazard ratio with X, 0.79; 95% confidence interval [CI], 0.66 to 0.95"
                /(?:HR|hazard\\s*ratio)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,'''

new_hr_pattern = '''            HR: [
                // Flexible HR pattern for NEJM format: handles "hazard ratio in the X group, 0.79; 95% CI..."
                /(?:HR|hazard\\s*ratio)(?:\\s+(?:with|for|in|of)(?:\\s+the)?(?:\\s+[\\w-]+)+)?[,;:\\s]+(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,'''

if old_hr_pattern in content:
    content = content.replace(old_hr_pattern, new_hr_pattern)
    print("HR pattern updated for multi-word phrases")
else:
    print("HR pattern not found - trying regex search")
    # Try to find and replace more flexibly
    hr_section = re.search(r'HR: \[\s*// Flexible HR pattern.*?\],', content, re.DOTALL)
    if hr_section:
        print(f"Found HR section at position {hr_section.start()}")

# Update RR pattern similarly
old_rr_pattern = '''            RR: [
                // Flexible RR pattern: "relative risk with dabigatran, 0.91; 95% confidence interval [CI], 0.74 to 1.11"
                /(?:RR|relative\\s*risk)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,'''

new_rr_pattern = '''            RR: [
                // Flexible RR pattern: handles "relative risk with dabigatran" or "in the X group"
                /(?:RR|relative\\s*risk)(?:\\s+(?:with|for|in|of)(?:\\s+the)?(?:\\s+[\\w-]+)+)?[,;:\\s]+(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,'''

if old_rr_pattern in content:
    content = content.replace(old_rr_pattern, new_rr_pattern)
    print("RR pattern updated for multi-word phrases")
else:
    print("RR pattern not found")

# Update OR pattern similarly
old_or_pattern = '''            OR: [
                // Flexible OR pattern: "odds ratio with X, 0.84; 95% confidence interval [CI], 0.71-0.99"
                /(?:OR|odds\\s*ratio)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,'''

new_or_pattern = '''            OR: [
                // Flexible OR pattern: handles "odds ratio with X" or "in the X group"
                /(?:OR|odds\\s*ratio)(?:\\s+(?:with|for|in|of)(?:\\s+the)?(?:\\s+[\\w-]+)+)?[,;:\\s]+(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,'''

if old_or_pattern in content:
    content = content.replace(old_or_pattern, new_or_pattern)
    print("OR pattern updated for multi-word phrases")
else:
    print("OR pattern not found")

# Update version
content = content.replace("version: '4.9.1-AI-Web'", "version: '4.9.2-AI-Web'")
print("Version updated to 4.9.2")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nPatterns updated for multi-word group/drug names!")
print("Now handles: 'hazard ratio in the LCZ696 group, 0.80'")
