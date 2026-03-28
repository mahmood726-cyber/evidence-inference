#!/usr/bin/env python3
"""Extract all functions, buttons, and canvas elements from IPD app"""

import re

filepath = r'C:\Users\user\IPD-Meta-Pro\ipd-meta-pro.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all function names
functions = re.findall(r'function\s+(\w+)\s*\(', content)
unique_functions = sorted(set(functions))

# Extract all onclick handlers
onclick_handlers = re.findall(r'onclick=["\']([^"\']+)["\']', content)
unique_onclick = sorted(set(onclick_handlers))

# Extract all button elements with their text/id
buttons = re.findall(r'<button[^>]*(?:id=["\']([^"\']*)["\'])?[^>]*>([^<]*)</button>', content, re.IGNORECASE)

# Extract all canvas elements
canvases = re.findall(r'<canvas[^>]*id=["\']([^"\']*)["\'][^>]*>', content)

# Extract all div IDs that might be plot containers
plot_divs = re.findall(r'<div[^>]*id=["\']([^"\']*(?:plot|chart|graph|canvas|forest|funnel)[^"\']*)["\']', content, re.IGNORECASE)

print("=" * 70)
print("IPD META-ANALYSIS PRO - ELEMENT EXTRACTION")
print("=" * 70)

print(f"\n[FUNCTIONS] Total: {len(unique_functions)}")
print("-" * 50)
for i, func in enumerate(unique_functions, 1):
    print(f"  {i:3}. {func}")

print(f"\n[ONCLICK HANDLERS] Total: {len(unique_onclick)}")
print("-" * 50)
for i, handler in enumerate(unique_onclick[:50], 1):  # First 50
    print(f"  {i:3}. {handler[:60]}...")

print(f"\n[CANVAS ELEMENTS] Total: {len(canvases)}")
print("-" * 50)
for i, canvas in enumerate(canvases, 1):
    print(f"  {i:3}. {canvas}")

print(f"\n[PLOT DIVS] Total: {len(plot_divs)}")
print("-" * 50)
for i, div in enumerate(plot_divs, 1):
    print(f"  {i:3}. {div}")

# Save to file for use in test
with open(r'C:\Users\user\ipd_elements.txt', 'w', encoding='utf-8') as f:
    f.write("FUNCTIONS:\n")
    for func in unique_functions:
        f.write(f"{func}\n")
    f.write("\nONCLICK_HANDLERS:\n")
    for handler in unique_onclick:
        f.write(f"{handler}\n")
    f.write("\nCANVAS_IDS:\n")
    for canvas in canvases:
        f.write(f"{canvas}\n")
    f.write("\nPLOT_DIVS:\n")
    for div in plot_divs:
        f.write(f"{div}\n")

print(f"\n[OK] Elements saved to ipd_elements.txt")
