# Find where FrequentistNMA object ends

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find FrequentistNMA definition
start = content.find('const FrequentistNMA={')
if start == -1:
    print('FrequentistNMA not found')
else:
    # Track braces to find the end (simplified - assumes no braces in strings mess it up)
    depth = 0
    i = start + len('const FrequentistNMA=')

    for pos in range(i, min(i + 150000, len(content))):
        char = content[pos]

        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                # Found the end
                line_num = content[:pos].count('\n') + 1
                snippet = content[pos:pos+30]
                print(f'FrequentistNMA ends at line {line_num}')
                print(f'Ending chars: {repr(snippet)}')

                # Check if properly terminated with };
                if content[pos:pos+2] == '};':
                    print('[OK] Properly terminated with };')
                elif content[pos:pos+1] == '}':
                    print('[WARNING] Ends with } but no semicolon')
                    # Check next non-whitespace
                    after_ws = content[pos+1:pos+50].lstrip()
                    print(f'After: {repr(after_ws[:30])}')
                break
    else:
        print(f'[ERROR] Object not properly closed. Final depth: {depth}')
