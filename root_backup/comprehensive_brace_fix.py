# Comprehensive fix for all brace issues caused by }}, -> }, regex

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The problematic regex changed }}, to }, everywhere
# This breaks:
# 1. Object method endings: }}return{x}}; -> }}return{x}; (missing } for object)
# 2. Nested structures: }}}; -> }}; (missing })
# 3. Function separators in objects

# Strategy: Find all }; patterns and check if they should be }};
# Also find all }, followed by methodName( and ensure proper structure

fixes_applied = []

# Fix 1: }; at end of lines inside object definitions (should be }};)
# Pattern: const X = { ... methodName(){...}; should end with }};

# Common patterns that got broken:
patterns = [
    # AppState already fixed above

    # Fix }, before methodName( - these need proper closing
    # checkConnectivity missing separator
    (r"\};\n(checkConnectivity\()", r"},\n\1"),
    (r"\}\n(checkConnectivity\()", r"},\n\1"),

    # General pattern: } followed by methodName( without comma
    # This catches methods that follow } without proper separator
]

# Let's find all places where } followed by word( occurs (method definitions)
# and check if there's a proper comma

method_pattern = re.compile(r'\}\n([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
for match in method_pattern.finditer(content):
    pos = match.start()
    method_name = match.group(1)

    # Check if the line before ends with },
    line_end = content.rfind('\n', 0, pos)
    if line_end > 0:
        prev_line_start = content.rfind('\n', 0, line_end)
        prev_line = content[prev_line_start+1:line_end+1]

        if not prev_line.rstrip().endswith(','):
            # Check if it ends with } (need to add comma)
            if prev_line.rstrip().endswith('}'):
                # This is a missing comma - but we can't fix blindly
                # Log it for manual review
                line_num = content[:pos].count('\n') + 1
                fixes_applied.append(f"Line {line_num}: {method_name}() may need comma separator")

# More targeted fixes based on known broken patterns
# The original regex }}, -> }, would break patterns like:
# ...code}}; -> ...code}; (AppState - fixed)
# ...code}}, -> ...code}, (method endings in objects)

# Let's look for all occurrences where }; appears and check context
# An object literal ends with };
# A block inside an object method ends with } then , or } then } then ;

# Extract JavaScript
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''

# Run node to find current error
with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)

if result.returncode != 0:
    # Parse error line
    error_match = re.search(r'temp_check\.js:(\d+)', result.stderr)
    if error_match:
        error_line = int(error_match.group(1))
        js_lines = main_script.split('\n')

        if error_line <= len(js_lines):
            print(f"Error at JS line {error_line}:")
            print(f"  {js_lines[error_line-1][:100]}...")

            # Check if the line before needs a comma
            if error_line > 1:
                prev_line = js_lines[error_line-2]
                print(f"Previous line ends with: ...{prev_line[-20:]}")

                # If previous line ends with } and current starts with methodName(
                if prev_line.rstrip().endswith('}'):
                    # Add comma to previous line
                    html_lines = content.split('\n')

                    # Find this pattern in HTML
                    pattern = prev_line.rstrip()[-50:] + '\n' + js_lines[error_line-1][:50]
                    fixed_pattern = prev_line.rstrip() + ',\n' + js_lines[error_line-1][:50]

                    if pattern in content:
                        content = content.replace(pattern, fixed_pattern)
                        fixes_applied.append(f"Added comma after line ending with }} before line {error_line}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 60)
print("BRACE FIX RESULTS")
print("=" * 60)
for fix in fixes_applied:
    print(f"  {fix}")

# Final check
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''
with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("\n[OK] JavaScript syntax is now valid!")
else:
    print(f"\n[NEXT ERROR]:")
    print(result.stderr[:400])
