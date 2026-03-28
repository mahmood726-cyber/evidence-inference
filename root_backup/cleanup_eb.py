#!/usr/bin/env python3
"""Clean up leftover code from EB function replacement"""

print("=" * 70)
print("CLEANING UP LEFTOVER EB CODE")
print("=" * 70)

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the EB function end (line 104162: "    }")
# Find calculateI2CI start (line 104642)
eb_end_idx = None
i2ci_start_idx = None

for i, line in enumerate(lines):
    # Find line with "    }" that's part of EB function (around line 104162)
    if i > 104100 and i < 104200 and line.strip() == '}' and 'converged: false' in lines[i-2]:
        eb_end_idx = i
        print(f"Found EB function end at line {i+1}")

    # Find calculateI2CI function
    if 'function calculateI2CI(Q, df, alpha = 0.05)' in line:
        i2ci_start_idx = i
        print(f"Found calculateI2CI at line {i+1}")
        break

if eb_end_idx and i2ci_start_idx:
    # Remove lines between EB end and calculateI2CI start
    # Keep the EB closing brace (line 104162), remove 104163 to 104641

    # Lines to remove: eb_end_idx+1 to i2ci_start_idx-1
    remove_start = eb_end_idx + 1  # First line to remove
    remove_end = i2ci_start_idx    # First line to keep

    garbage_lines = remove_end - remove_start
    print(f"Removing {garbage_lines} garbage lines ({remove_start+1} to {remove_end})")

    # Create new content
    new_lines = lines[:remove_start] + ['\n\n'] + lines[remove_end:]

    with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"Cleanup complete! Removed {garbage_lines} lines")
else:
    print("ERROR: Could not find boundaries")
    print(f"eb_end_idx: {eb_end_idx}, i2ci_start_idx: {i2ci_start_idx}")

print("=" * 70)
