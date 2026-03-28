# Add missing Bayesian R export button

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# Add button to Bayesian MCMC Analysis panel
old_bayes_panel = '<span class="card__title"> Bayesian MCMC Analysis</span><div class="flex gap-2"><select class="select" id="bayesPriorSelect">'
new_bayes_panel = '<span class="card__title"> Bayesian MCMC Analysis</span><div class="flex gap-2"><button class="btn btn--sm btn--ghost" id="exportBayesRBtn" title="Export R script for gemtc validation">gemtc R</button><select class="select" id="bayesPriorSelect">'

if old_bayes_panel in content and 'exportBayesRBtn' not in old_bayes_panel:
    content = content.replace(old_bayes_panel, new_bayes_panel)
    changes.append("Added gemtc R export button to Bayesian panel")
elif 'exportBayesRBtn' in content:
    changes.append("Bayesian export button already exists")
else:
    changes.append("Could not find Bayesian panel pattern")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("=" * 60)
print("ADD BAYESIAN EXPORT BUTTON")
print("=" * 60)
for c in changes:
    print(f"  [OK] {c}")
print("=" * 60)
