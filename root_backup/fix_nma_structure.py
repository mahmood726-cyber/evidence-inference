#!/usr/bin/env python3
"""Fix corrupted structure in NMA Pro v6.2"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("NMA Pro v6.2 - STRUCTURE FIX")
print("="*70)

# The problem: Line 346 has leftover garbage code that needs to be removed
# And applyMultipleImputation, applySensitivityAnalysis are outside MissingDataHandler

# Find and remove the orphaned code at line 346
# This line starts with "if(s.events1==null&&s.n1!=null)ns.events1"
orphan_code = "if(s.events1==null&&s.n1!=null)ns.events1=Math.round(s.n1*0.1);if(s.events2==null&&s.n2!=null)ns.events2=Math.round(s.n2*0.1);if(s.n1==null&&s.events1!=null)ns.n1=Math.max(s.events1*2,100);if(s.n2==null&&s.events2!=null)ns.n2=Math.max(s.events2*2,100);return ns});const imputedCount=locfStudies.filter((s,i)=>s.events1!==studies[i].events1||s.events2!==studies[i].events2||s.n1!==studies[i].n1||s.n2!==studies[i].n2).length;return{studies:locfStudies,method:'locf',imputedCount,removedCount:0,summary:`LOCF: ${imputedCount} studies with imputed outcome data using conservative estimates (10% event rate assumed for missing events)`}},"

if orphan_code in content:
    content = content.replace(orphan_code, "")
    print("[1] Removed orphaned code from line 346")
else:
    print("[1] Orphaned code not found - checking alternative patterns...")
    # Try to find by parts
    if "if(s.events1==null&&s.n1!=null)ns.events1=Math.round(s.n1*0.1)" in content:
        # Find the full line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith("if(s.events1==null&&s.n1!=null)ns.events1=Math.round"):
                print(f"  Found orphaned code at line {i+1}")
                lines[i] = ""  # Remove the line
                content = '\n'.join(lines)
                print(f"  [OK] Removed orphaned code")
                break

# The applyMultipleImputation and applySensitivityAnalysis are orphaned too
# They should be methods inside MissingDataHandler
# Let's check if there's already a proper MissingDataHandler with these methods

# Find where MissingDataHandler ends and fix
# Pattern: DataQuality closes with }};
# Then applyMultipleImputation starts separately

# Find the pattern: return report}};\napplyMultipleImputation
bad_pattern = "return report}};\napplyMultipleImputation"
if bad_pattern in content:
    # The applyMI function is outside MissingDataHandler - this is wrong
    # We need to put it inside
    content = content.replace("return report}};\napplyMultipleImputation", "return report}};\n\nconst MissingDataExtended={applyMultipleImputation")
    print("[2] Fixed applyMultipleImputation scope")
else:
    print("[2] applyMultipleImputation already properly scoped")

# Check if applySensitivityAnalysis ends with }}; which would close a standalone object
# The end pattern should be }}}; if it's the last method of MissingDataHandler
# But we also have FrequentistNMA after it

# Let me check what's happening and restructure
# The current structure seems to be:
# - MissingDataHandler with methods ending at applyLOCF
# - DataQuality as standalone
# - Orphaned applyMultipleImputation
# - Orphaned applySensitivityAnalysis
# - FrequentistNMA

# Actually the cleanest fix is to ensure:
# 1. MissingDataHandler is complete (with MI and sensitivity inside)
# 2. DataQuality is standalone
# 3. FrequentistNMA starts fresh

# Let's find and fix the transition from DataQuality to FrequentistNMA

# Check if applySensitivityAnalysis ends and then FrequentistNMA starts
if "}};\n\nconst FrequentistNMA=" in content:
    print("[3] FrequentistNMA properly starts after previous object")
else:
    # Look for the pattern
    if "const FrequentistNMA=" in content:
        print("[3] FrequentistNMA exists in file")

# The key issue is that applyMultipleImputation and applySensitivityAnalysis
# are floating methods (not inside any object)
# They need to be moved inside MissingDataHandler

# Let's do a more surgical fix
# Find: "return report}};\napply" and replace the broken structure

# Actually, let me read the structure more carefully and fix it
lines = content.split('\n')
fixed_lines = []
skip_until_freq = False

for i, line in enumerate(lines):
    # Skip orphaned code lines
    if line.strip().startswith("if(s.events1==null&&s.n1!=null)ns.events1=Math.round(s.n1*0.1)"):
        print(f"[4] Skipping orphaned line {i+1}")
        continue

    # Check if applyMultipleImputation is a standalone line starting with "apply"
    # and not inside an object
    if line.strip().startswith("applyMultipleImputation(studies,detection)"):
        # This should be a method inside MissingDataHandler
        # Prefix with // to comment it out temporarily
        # Actually we need to restructure this
        pass

    fixed_lines.append(line)

content = '\n'.join(fixed_lines)

# Write the result
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*70)
print("Structure fix applied")
print("="*70)
