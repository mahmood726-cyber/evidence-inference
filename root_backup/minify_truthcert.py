"""
Minify TruthCert-PairwisePro for production
Creates a minified version of app.js
"""
import re
import os

# Paths
APP_JS = r'C:\Truthcert1\app.js'
APP_JS_MIN = r'C:\Truthcert1\app.min.js'
HTML_FILE = r'C:\Truthcert1\TruthCert-PairwisePro-v1.0-fast.html'
HTML_PROD = r'C:\Truthcert1\TruthCert-PairwisePro-v1.0-production.html'

def minify_js(code):
    """Basic JavaScript minification"""
    # Remove single-line comments (but not URLs with //)
    code = re.sub(r'(?<!:)//(?!/)[^\n]*', '', code)

    # Remove multi-line comments
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)

    # Remove console.log statements (optional, comment out if needed for debugging)
    code = re.sub(r'console\.log\([^)]*\);?', '', code)

    # Reduce multiple spaces to single space
    code = re.sub(r'[ \t]+', ' ', code)

    # Remove spaces around operators (careful version)
    code = re.sub(r' ?([\{\}\[\]\(\);,]) ?', r'\1', code)
    code = re.sub(r' ?([\+\-\*\/=<>!&\|:]) ?', r'\1', code)

    # Remove newlines but keep some for safety
    lines = code.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    code = '\n'.join(lines)

    # More aggressive: join lines that are safe to join
    code = re.sub(r'\n+', '\n', code)

    return code

def minify_css(css):
    """Basic CSS minification"""
    # Remove comments
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)

    # Remove whitespace
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};:,])\s*', r'\1', css)
    css = re.sub(r';\s*}', '}', css)

    return css.strip()

print("=" * 60)
print("TruthCert-PairwisePro Minification")
print("=" * 60)

# Read original app.js
with open(APP_JS, 'r', encoding='utf-8') as f:
    original_js = f.read()

original_size = len(original_js)
print(f"\nOriginal app.js: {original_size:,} bytes ({original_size/1024:.1f} KB)")

# Minify
minified_js = minify_js(original_js)
minified_size = len(minified_js)
print(f"Minified app.min.js: {minified_size:,} bytes ({minified_size/1024:.1f} KB)")
print(f"Reduction: {(1 - minified_size/original_size)*100:.1f}%")

# Save minified JS
with open(APP_JS_MIN, 'w', encoding='utf-8') as f:
    f.write(minified_js)

print(f"\nSaved: {APP_JS_MIN}")

# Create production HTML
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

original_html_size = len(html)

# Replace app.js reference with app.min.js
html_prod = html.replace('src="app.js"', 'src="app.min.js"')

# Minify inline CSS
def minify_style_tag(match):
    css = match.group(1)
    return '<style>' + minify_css(css) + '</style>'

html_prod = re.sub(r'<style>([\s\S]*?)</style>', minify_style_tag, html_prod)

# Remove HTML comments (except IE conditionals)
html_prod = re.sub(r'<!--(?!\[if)[\s\S]*?-->', '', html_prod)

# Reduce whitespace
html_prod = re.sub(r'\n\s*\n', '\n', html_prod)

minified_html_size = len(html_prod)

with open(HTML_PROD, 'w', encoding='utf-8') as f:
    f.write(html_prod)

print(f"\nOriginal HTML: {original_html_size:,} bytes ({original_html_size/1024:.1f} KB)")
print(f"Minified HTML: {minified_html_size:,} bytes ({minified_html_size/1024:.1f} KB)")
print(f"Reduction: {(1 - minified_html_size/original_html_size)*100:.1f}%")
print(f"\nSaved: {HTML_PROD}")

# Calculate total production size
total_original = original_size + original_html_size
total_minified = minified_size + minified_html_size

print(f"\n" + "=" * 60)
print(f"TOTAL PRODUCTION SIZE")
print(f"=" * 60)
print(f"Original: {total_original:,} bytes ({total_original/1024:.1f} KB)")
print(f"Minified: {total_minified:,} bytes ({total_minified/1024:.1f} KB)")
print(f"Total Reduction: {(1 - total_minified/total_original)*100:.1f}%")
print(f"=" * 60)

# Create a combined single-file version for distribution
print("\nCreating single-file distribution...")

# Read minified JS
with open(APP_JS_MIN, 'r', encoding='utf-8') as f:
    min_js = f.read()

# Read minified HTML
with open(HTML_PROD, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Embed JS inline (replace script src with inline script)
script_tag = '<script src="app.min.js"></script>'
if script_tag in html_content:
    inline_html = html_content.replace(
        script_tag,
        '<script>' + min_js + '</script>'
    )
else:
    # Try the original reference
    script_tag = '<script src="app.js"></script>'
    if script_tag in html_content:
        inline_html = html_content.replace(
            script_tag,
            '<script>' + min_js + '</script>'
        )
    else:
        inline_html = html_content

single_file_path = r'C:\Truthcert1\TruthCert-PairwisePro-v1.0-dist.html'
with open(single_file_path, 'w', encoding='utf-8') as f:
    f.write(inline_html)

single_size = len(inline_html)
print(f"Single-file dist: {single_size:,} bytes ({single_size/1024:.1f} KB)")
print(f"Saved: {single_file_path}")

print("\n" + "=" * 60)
print("MINIFICATION COMPLETE")
print("=" * 60)
print("\nProduction files created:")
print(f"  1. app.min.js ({minified_size/1024:.1f} KB)")
print(f"  2. TruthCert-PairwisePro-v1.0-production.html")
print(f"  3. TruthCert-PairwisePro-v1.0-dist.html (single file)")
print("=" * 60)
