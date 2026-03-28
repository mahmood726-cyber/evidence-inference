#!/usr/bin/env python3
"""
Fix duplicates and properly add BATCH27_TO_1900 and BATCH28_TO_2000
"""

import re

# Read the file
with open(r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all the BATCH27 and BATCH28 definitions and remove duplicates
# Keep only the first definition of each batch

# Count occurrences
print("Analyzing file...")
batch27_count = content.count('const BATCH27_TO_1900')
batch28_count = content.count('const BATCH28_TO_2000')
print(f"BATCH27_TO_1900 occurrences: {batch27_count}")
print(f"BATCH28_TO_2000 occurrences: {batch28_count}")

# Find and keep track of duplicate batch definitions
duplicated_batches = []
for batch_name in ['BATCH27_TO_1900', 'BATCH28_TO_2000', 'BATCH23_TO_1500', 'BATCH24_TO_1600',
                   'BATCH25_TO_1700', 'BATCH26_TO_1800', 'BATCH29_TO_2100', 'BATCH30_TO_2200']:
    pattern = f'const {batch_name}'
    count = content.count(pattern)
    if count > 1:
        duplicated_batches.append((batch_name, count))
        print(f"  {batch_name}: {count} occurrences (duplicate!)")

if duplicated_batches:
    print("\nRemoving duplicate batch definitions...")

    # For each duplicated batch, find all occurrences and keep only the first one
    for batch_name, count in duplicated_batches:
        # Find all occurrences
        pattern = rf'// =+\n// {batch_name}.*?(?=// =+\nconst|\Z)'

        # Find the start of each const BATCH_NAME = [ ... ];
        const_pattern = rf'const {batch_name} = \['
        matches = list(re.finditer(const_pattern, content))

        if len(matches) > 1:
            print(f"  Removing {len(matches)-1} duplicate(s) of {batch_name}")

            # Find the end of each duplicate (ends with ];)
            for match in matches[1:]:  # Skip the first one
                start = match.start()
                # Find the matching closing ];
                # Count brackets to find the right closing
                bracket_count = 0
                in_string = False
                string_char = None
                i = start
                while i < len(content):
                    char = content[i]

                    # Handle string detection
                    if char in ['"', "'", '`'] and (i == 0 or content[i-1] != '\\'):
                        if not in_string:
                            in_string = True
                            string_char = char
                        elif char == string_char:
                            in_string = False
                            string_char = None

                    if not in_string:
                        if char == '[':
                            bracket_count += 1
                        elif char == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                # Found the end
                                end = i + 2  # Include ];
                                # Remove this duplicate
                                # Find the section header before it
                                section_start = content.rfind('// =============', 0, start)
                                if section_start != -1 and content[section_start:start].strip().startswith('//'):
                                    # Include the section header
                                    start = section_start

                                # Mark for removal
                                content = content[:start] + content[end:]
                                print(f"    Removed duplicate at position {start}")
                                break
                    i += 1

# Now check if BATCH27_TO_1900 and BATCH28_TO_2000 are in GROUND_TRUTH_CASES
if '...BATCH27_TO_1900' not in content or '...BATCH28_TO_2000' not in content:
    print("\nAdding BATCH27_TO_1900 and BATCH28_TO_2000 to GROUND_TRUTH_CASES...")

    # Find the end of GROUND_TRUTH_CASES array (look for the ]; after all the ...BATCH entries)
    # Pattern to find the last batch spread in GROUND_TRUTH_CASES

    # Find ...BATCH24_TO_1600]; or similar ending
    pattern = r'(\.\.\.[A-Z0-9_]+)\];(\s*\n\s*// =+\n// EXPANDED VALIDATION)'
    match = re.search(pattern, content)

    if match:
        old_ending = match.group(0)
        last_batch = match.group(1)
        after_section = match.group(2)

        if '...BATCH27_TO_1900' not in content:
            new_ending = f"{last_batch},\n    ...BATCH27_TO_1900,\n    ...BATCH28_TO_2000];{after_section}"
            content = content.replace(old_ending, new_ending)
            print("  Added BATCH27_TO_1900 and BATCH28_TO_2000 to GROUND_TRUTH_CASES")

# Write the fixed file
with open(r'C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFile updated successfully!")
