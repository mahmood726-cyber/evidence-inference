# Fix all method separator issues
# Pattern: ...},[newline]methodName( needs to become ...}},[newline]methodName( in many cases

import re
import subprocess

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract JS
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
main_script = max(scripts, key=len) if scripts else ''

# Find all method definitions and check brace balance
method_pattern = re.compile(r'\n([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{')

fixes = []
for match in method_pattern.finditer(main_script):
    method_name = match.group(1)
    pos = match.start()

    # Check what's immediately before this method
    before = main_script[max(0, pos-10):pos]

    # If it ends with }, the previous method is closed
    # If it ends with just , then the previous return/statement is done but function isn't closed
    if before.strip().endswith(',') and not before.strip().endswith('},'):
        # Need to add }
        # Find this in original content and fix
        method_start = match.group(0)  # includes newline
        # Look for the pattern in original HTML
        search_pattern = before[-20:] + method_start[:30]
        if search_pattern in content:
            # Insert } before the newline+method
            fix_from = before[-20:] + '\n' + method_name
            fix_to = before[-20:].rstrip() + '},\n' + method_name

            # Only fix if the pattern ends with }, and we're adding another }
            if before.rstrip().endswith('},'):
                # Already has },
                pass
            else:
                fixes.append((method_name, pos))

# Instead of trying complex regex, let's iterate and fix one at a time
# by running node check after each fix

max_iterations = 20
for iteration in range(max_iterations):
    # Extract JS
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    main_script = max(scripts, key=len) if scripts else ''

    with open('C:/Users/user/temp_check.js', 'w', encoding='utf-8') as f:
        f.write(main_script)

    result = subprocess.run(['node', '-c', 'C:/Users/user/temp_check.js'],
                           capture_output=True, text=True)

    if result.returncode == 0:
        print(f"\n[OK] JavaScript syntax is valid after {iteration} fixes!")
        break

    # Parse error
    error_match = re.search(r'temp_check\.js:(\d+)', result.stderr)
    if not error_match:
        print("Could not parse error location")
        print(result.stderr[:300])
        break

    error_line = int(error_match.group(1))
    js_lines = main_script.split('\n')

    if error_line > len(js_lines):
        print(f"Error line {error_line} exceeds file length")
        break

    current_line = js_lines[error_line-1]
    prev_line = js_lines[error_line-2] if error_line > 1 else ''

    print(f"Fix {iteration+1}: Error at line {error_line}")
    print(f"  Current: {current_line[:60]}...")
    print(f"  Previous ends with: ...{prev_line[-30:]}")

    # If previous line ends with }, and current starts with methodName(
    # We need to add another } to the previous line
    if prev_line.rstrip().endswith('},'):
        # The method before this one is already properly closed
        # So the issue is something else
        print("  Previous already ends with },")

        # Check if previous line should end with }}, instead
        # This happens when there's a nested return statement
        fix_target = prev_line.rstrip() + '\n' + current_line[:50]
        fix_result = prev_line.rstrip()[:-1] + '},\n' + current_line[:50]

        if fix_target in content:
            content = content.replace(fix_target, fix_result)
            print("  Fixed: Changed }, to }},")
        else:
            print(f"  Could not find pattern to fix")
            print(f"  Looking for: {fix_target[:80]}")
            break
    elif prev_line.rstrip().endswith('},'):
        print("  Already has },")
    else:
        # Previous line doesn't end with }, - need to check what it ends with
        print(f"  Previous line ending: {repr(prev_line.rstrip()[-10:])}")

        # If ends with just } need to add ,
        if prev_line.rstrip().endswith('}'):
            fix_target = prev_line.rstrip() + '\n' + current_line[:50]
            fix_result = prev_line.rstrip() + '},\n' + current_line[:50]

            if fix_target in content:
                content = content.replace(fix_target, fix_result)
                print("  Fixed: Added }, after }}")
            else:
                # Try shorter match
                fix_target2 = prev_line.rstrip()[-30:] + '\n' + current_line[:30]
                fix_result2 = prev_line.rstrip()[-30:] + '},\n' + current_line[:30]
                if fix_target2 in content:
                    content = content.replace(fix_target2, fix_result2)
                    print(f"  Fixed with shorter match")
                else:
                    print(f"  Could not find pattern")
                    break

# Save
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone!")
