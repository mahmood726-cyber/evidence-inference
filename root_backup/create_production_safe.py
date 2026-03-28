"""Create safe production bundle for TruthCert-PairwisePro"""

html_path = r'C:\Truthcert1\TruthCert-PairwisePro-v1.0-fast.html'
js_path = r'C:\Truthcert1\app.js'
output_path = r'C:\Truthcert1\TruthCert-PairwisePro-v1.0-bundle.html'

# Read files
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Simple safe minification of JS (only remove comments, keep structure)
import re

def safe_minify_js(code):
    # NO minification - the code contains embedded JS in string literals
    # (Web Workers) that cannot be safely parsed with regex
    # Just return the code as-is
    return code

js_clean = safe_minify_js(js)

# Replace the script src with inline script
html_bundle = html.replace(
    '<script src="app.js"></script>',
    '<script>\n' + js_clean + '\n</script>'
)

# NOTE: Do NOT remove HTML comments - some contain conditional IE stuff

# Save bundle
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_bundle)

original_size = len(html) + len(js)
bundle_size = len(html_bundle)

print("=" * 60)
print("TruthCert-PairwisePro Production Bundle")
print("=" * 60)
print(f"Original HTML: {len(html):,} bytes")
print(f"Original JS: {len(js):,} bytes")
print(f"Total Original: {original_size:,} bytes ({original_size/1024:.1f} KB)")
print(f"Bundle Size: {bundle_size:,} bytes ({bundle_size/1024:.1f} KB)")
print(f"Reduction: {(1 - bundle_size/original_size)*100:.1f}%")
print(f"\nSaved: {output_path}")
print("=" * 60)
