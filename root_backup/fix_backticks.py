# -*- coding: utf-8 -*-
"""Fix escaped backticks in meta-engine.js"""

import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

filepath = "C:/Users/user/Downloads/new app/src/analysis/meta-engine.js"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# The Python script wrote \` instead of ` for template literals
# We need to replace \` with ` but be careful about legitimate escape sequences

# Replace the escaped backtick pattern from Python output
original_len = len(content)
content = content.replace('\\`', '`')

print(f"Original length: {original_len}")
print(f"New length: {len(content)}")
print(f"Replacements made: {original_len - len(content)}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Backticks fixed successfully")
