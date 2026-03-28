"""Fix the effects.effects[t] bug in NMA Pro"""

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences before fix
count_before = content.count('effects.effects[')
print(f"Found {count_before} occurrences of 'effects.effects['")

# Fix all instances where we destructure effects from results then access effects.effects
# The pattern is: const{effects,...}=results; ... effects.effects[t]
# This should be just effects[t] since effects is already the effects object

# Replace effects.effects[ with effects[
content = content.replace('effects.effects[', 'effects[')

count_after = content.count('effects.effects[')
print(f"After fix: {count_after} occurrences")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed {count_before - count_after} occurrences")
print("Done!")
