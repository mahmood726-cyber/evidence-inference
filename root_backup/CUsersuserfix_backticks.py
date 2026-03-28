import re
filepath = r"C:\Users\user\IPD-Meta-Pro\ipd-meta-pro.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()
original_len = len(content)
# Replace the escape sequence
target = chr(96) + " + " + chr(34) + chr(96) + chr(34) + " + " + chr(96)
content = content.replace(target, chr(96))
with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Fixed backticks. Removed {original_len - len(content)} chars")
