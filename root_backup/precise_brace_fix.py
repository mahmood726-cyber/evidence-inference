# Precisely fix brace issues by tracking balance

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract JS
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''
lines = main_script.split('\n')

# Find all object definitions and their methods
# Track which lines have too many or too few braces

# First, let's look at the problematic transpose line (257)
print("Analyzing line 257 and surroundings:")
for i in range(254, 262):
    if i < len(lines):
        line = lines[i]
        opens = line.count('{')
        closes = line.count('}')
        print(f"Line {i+1}: opens={opens} closes={closes} | ...{line[-50:]}")

print("\n" + "=" * 60)

# The issue: we've added too many }}, - we have }}}} now in some places
# We need to reduce these back

# Pattern: look for }}}, and change to }},
# or }}}} and change to }}}

# Find lines ending with excessive closing braces
fixes_made = []
for i, line in enumerate(lines):
    stripped = line.rstrip()
    # Count consecutive } at end
    brace_count = 0
    for c in reversed(stripped):
        if c == '}':
            brace_count += 1
        elif c == ',':
            continue  # comma is ok after }
        else:
            break

    if brace_count >= 4:
        print(f"Line {i+1}: Too many closing braces ({brace_count}): ...{stripped[-50:]}")

# Let's fix specific patterns that are clearly wrong
# Looking at the error: transpose ends with }}}}, which is wrong

# The pattern }}}}, should become }}},
over_braced = [
    (r'\}\}\}\}\},', '}}}},'),  # 4 } + , -> 3 } + ,
    (r'\}\}\}\}\}', '}}}}'),     # 5 } -> 4 }
]

# Actually, let me look at what the correct structure should be
# An object method: methodName(){...},
# Nested: methodName(){...if(){...}...},
# So method ending should be }, or }},

# Find all lines that end with more than 2 } before comma
for i, line in enumerate(lines):
    stripped = line.rstrip()
    if stripped.endswith('}}}},'):
        # This is 4 } - probably too many
        # Check the next line to see what it expects
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\(', next_line):
                # Next line is a method definition
                # Current should end with }}, not }}}},
                print(f"Line {i+1}: Reducing excessive braces")
                lines[i] = line[:-5] + '},\n' if line.endswith('\n') else line[:-4] + '},'

# Rebuild
fixed_script = '\n'.join(lines)

# Put back into HTML
content = content.replace(main_script, fixed_script)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Test
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''
with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("\n[OK] JavaScript syntax is valid!")
else:
    print(f"\n[NEXT ERROR]:")
    print(result.stderr[:500])
