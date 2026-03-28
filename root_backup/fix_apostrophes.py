#!/usr/bin/env python3
"""
Fix all source lines with apostrophes by changing single quotes to double quotes
"""

import re

with open(r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_count = 0
for i, line in enumerate(lines):
    # Check if this is a source line with single quotes
    if "source: '" in line:
        # Extract the content between the quotes
        match = re.match(r"(\s*source: ')([^']*'[^']*)',", line)
        if match:
            # This line has an apostrophe inside single quotes - problematic
            indent = line[:len(line) - len(line.lstrip())]
            # Find the full source value (may have apostrophes in it)
            start_idx = line.find("source: '") + len("source: '")
            # Find the ending ', by searching from the end
            end_idx = line.rfind("',")
            if end_idx > start_idx:
                content = line[start_idx:end_idx]
                if "'" in content:
                    # Change single quotes to double quotes for the whole source field
                    new_line = indent + 'source: "' + content + '",\n'
                    lines[i] = new_line
                    fixed_count += 1
                    print(f'Fixed line {i+1}: {content[:50]}...')

print(f'\nTotal fixed: {fixed_count} lines')

with open(r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('File saved')
