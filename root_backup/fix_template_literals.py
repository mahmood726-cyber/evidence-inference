# -*- coding: utf-8 -*-
"""Fix escaped template literal placeholders in meta-engine.js"""

import sys
import re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

filepath = "C:/Users/user/Downloads/new app/src/analysis/meta-engine.js"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# The Python script wrote \${ instead of ${ for template literals
# Replace \${ with ${
original_len = len(content)

# Count occurrences
count1 = content.count('\\${')
print(f"Found {count1} instances of \\${{")

# Replace
content = content.replace('\\${', '${')

print(f"Replacements made: {count1}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Template literals fixed successfully")
