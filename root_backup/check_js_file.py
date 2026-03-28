#!/usr/bin/env python3
"""Check JS file for issues."""

import re

file_path = r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'File size: {len(content):,} bytes')

# Check for basic structure
has_const = 'const GROUND_TRUTH_CASES' in content
has_closing = '];' in content
ids = re.findall(r"id:\s*'([^']+)'", content)

print(f'Has const declaration: {has_const}')
print(f'Has closing bracket: {has_closing}')
print(f'Trial count: {len(ids)}')

# Check for backticks
backticks = content.count('`')
print(f'Backtick count: {backticks} (should be even: {backticks % 2 == 0})')

# Look for issues in text fields - unbalanced backticks
text_matches = re.findall(r"text:\s*`([^`]*)`", content)
print(f'Text fields found: {len(text_matches)}')

# Check for syntax issues
single_quotes = content.count("'")
double_quotes = content.count('"')
print(f'Single quotes: {single_quotes}, Double quotes: {double_quotes}')

# Sample trials
print('\n--- Sample trials ---')
for id in ids[:3]:
    print(f'  {id}')

print(f'\nLast 3 IDs: {ids[-3:]}')
