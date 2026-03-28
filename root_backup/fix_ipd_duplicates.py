#!/usr/bin/env python3
"""Remove duplicate enhancement blocks from IPD app"""

import re

filepath = r'C:\Users\user\IPD-Meta-Pro\ipd-meta-pro.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and remove the second occurrence of the enhancement block
# The pattern to find: everything from second "// IPD META-ANALYSIS PRO - ENHANCEMENTS" to second "// END OF ENHANCEMENTS"

# Split by the enhancement header
parts = content.split('// ============================================================================\n// IPD META-ANALYSIS PRO - ENHANCEMENTS FOR 100/100 SCORE\n// ============================================================================')

if len(parts) > 2:
    # We have duplicates - keep only the first occurrence
    # parts[0] = before first enhancement
    # parts[1] = first enhancement block
    # parts[2] = second enhancement block (duplicate) - we want to remove this

    # Find the end marker in parts[1]
    end_marker = '// ============================================================================\n// END OF ENHANCEMENTS\n// ============================================================================'

    if end_marker in parts[1]:
        # parts[1] contains the full first enhancement block
        # Reconstruct without the duplicate

        # The end of parts[2] should have the closing </script>
        closing_part = parts[2].split(end_marker)[-1] if end_marker in parts[2] else parts[2]

        # Reconstruct
        content = (parts[0] +
                   '// ============================================================================\n// IPD META-ANALYSIS PRO - ENHANCEMENTS FOR 100/100 SCORE\n// ============================================================================' +
                   parts[1].split(end_marker)[0] + end_marker +
                   '\n\n' +
                   closing_part.lstrip())

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print("[OK] Removed duplicate enhancement blocks")
    else:
        print("[WARN] Could not find end marker in first block")
else:
    print("[OK] No duplicates found")

# Verify line count
with open(filepath, 'r', encoding='utf-8') as f:
    lines = len(f.readlines())
    print(f"File now has {lines} lines")
