import os

def build():
    print("Building IPD Meta-Analysis Pro...")
    
    # Read HTML
    with open('src/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Read CSS
    with open('src/css/styles.css', 'r', encoding='utf-8') as f:
        css = f.read()
        
    # Read JS
    with open('src/js/app.js', 'r', encoding='utf-8') as f:
        js = f.read()
        
    # Inject CSS
    # Look for the link tag we created during migration
    if '<link rel="stylesheet" href="css/styles.css">' in html:
        html = html.replace('<link rel="stylesheet" href="css/styles.css">', f'<style>{css}</style>')
    else:
        # Fallback if link tag not found (maybe manual edit?)
        print("Warning: CSS link tag not found in HTML. Appending style to head.")
        html = html.replace('</head>', f'<style>{css}</style></head>')
        
    # Inject JS
    if '<script src="js/app.js"></script>' in html:
        html = html.replace('<script src="js/app.js"></script>', f'<script>{js}</script>')
    else:
         print("Warning: JS script tag not found in HTML. Appending script to body end.")
         html = html.replace('</body>', f'<script>{js}</script></body>')
         
    # Write output
    output_path = 'IPD-Meta-Pro/ipd-meta-pro.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Build complete! Output written to {output_path}")

if __name__ == '__main__':
    build()
