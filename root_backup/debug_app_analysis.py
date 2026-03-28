"""Debug why analysis results aren't rendering in NMA Pro"""

import sys
import time
import json
sys.stdout.reconfigure(encoding="utf-8")

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
driver = webdriver.Edge(options=options)
driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html")
time.sleep(3)

print("="*70)
print("NMA PRO v6.2 - DEBUG ANALYSIS")
print("="*70)

# 1. Load demo data
print("\n[1] LOADING DEMO DATA")
driver.execute_script("document.getElementById('loadDemoBtn').click()")
time.sleep(1)

studies = driver.execute_script("return AppState.studies")
print(f"  Studies loaded: {len(studies)}")
print(f"  First study: {studies[0]['name']} ({studies[0]['treatment1']} vs {studies[0]['treatment2']})")

# 2. Get console errors
logs = driver.get_log('browser')
if logs:
    print("\n[2] CONSOLE ERRORS BEFORE ANALYSIS:")
    for log in logs[-10:]:
        print(f"  {log['level']}: {log['message'][:100]}")
else:
    print("\n[2] No console errors before analysis")

# 3. Run analysis directly via JS (bypassing button)
print("\n[3] RUNNING ANALYSIS DIRECTLY VIA JS")

result = driver.execute_script("""
    try {
        const processedStudies = AppState.studies;
        const treatments = new Set();
        processedStudies.forEach(s => {
            treatments.add(s.treatment1);
            treatments.add(s.treatment2);
        });
        const reference = Array.from(treatments).sort()[0];
        AppState.reference = reference;
        AppState.effectMeasure = 'OR';

        // Run FrequentistNMA
        const nmaResult = FrequentistNMA.analyze(processedStudies, {
            reference: reference,
            effectMeasure: 'OR'
        });

        AppState.results = nmaResult;

        return {
            success: true,
            reference: reference,
            treatments: nmaResult.treatments,
            hasEffects: !!nmaResult.effects,
            effectKeys: nmaResult.effects ? Object.keys(nmaResult.effects) : [],
            tau2: nmaResult.tau2,
            hasLeagueTable: !!nmaResult.leagueTable,
            hasHet: !!nmaResult.heterogeneity
        };
    } catch(e) {
        return {success: false, error: e.message, stack: e.stack};
    }
""")

print(f"  Success: {result.get('success')}")
if result.get('success'):
    print(f"  Reference: {result.get('reference')}")
    print(f"  Treatments: {result.get('treatments')}")
    print(f"  Has effects: {result.get('hasEffects')}")
    print(f"  Effect keys: {result.get('effectKeys')}")
    print(f"  Tau2: {result.get('tau2')}")
    print(f"  Has league table: {result.get('hasLeagueTable')}")
    print(f"  Has heterogeneity: {result.get('hasHet')}")
else:
    print(f"  Error: {result.get('error')}")
    print(f"  Stack: {result.get('stack', '')[:500]}")

# 4. Check effects structure
print("\n[4] CHECKING EFFECTS STRUCTURE")
effects_check = driver.execute_script("""
    if (!AppState.results || !AppState.results.effects) return {error: 'No effects'};
    const e = AppState.results.effects;
    const keys = Object.keys(e);
    const sample = keys.length > 0 ? e[keys[0]] : null;
    return {
        keys: keys,
        sampleKey: keys[0],
        sampleValue: sample
    };
""")
print(f"  Effects: {effects_check}")

# 5. Try rendering network plot
print("\n[5] RENDERING NETWORK PLOT")
render_result = driver.execute_script("""
    try {
        if (!AppState.results) return {error: 'No results'};
        renderNetworkGraph(AppState.studies, AppState.results.treatments);
        return {success: true};
    } catch(e) {
        return {error: e.message, stack: e.stack};
    }
""")
print(f"  Result: {render_result}")

# 6. Try rendering forest plot
print("\n[6] RENDERING FOREST PLOT")
forest_result = driver.execute_script("""
    try {
        if (!AppState.results) return {error: 'No results'};
        renderForestPlot(AppState.results);
        return {success: true};
    } catch(e) {
        return {error: e.message, stack: e.stack};
    }
""")
print(f"  Result: {forest_result}")

# 7. Try rendering league table
print("\n[7] RENDERING LEAGUE TABLE")
league_result = driver.execute_script("""
    try {
        if (!AppState.results || !AppState.results.leagueTable) return {error: 'No league table'};
        renderLeagueTable(AppState.results.leagueTable, 'OR');
        return {success: true};
    } catch(e) {
        return {error: e.message, stack: e.stack};
    }
""")
print(f"  Result: {league_result}")

# 8. Check console errors after rendering
logs = driver.get_log('browser')
if logs:
    print("\n[8] CONSOLE ERRORS AFTER RENDERING:")
    for log in logs[-10:]:
        print(f"  {log['level']}: {log['message'][:150]}")
else:
    print("\n[8] No new console errors")

# 9. Check if Plotly is available
print("\n[9] CHECKING PLOTLY")
plotly_check = driver.execute_script("return {available: typeof Plotly !== 'undefined', version: typeof Plotly !== 'undefined' ? Plotly.version : 'N/A'}")
print(f"  Plotly available: {plotly_check.get('available')}")
print(f"  Version: {plotly_check.get('version')}")

# 10. Check if network plot div exists and has content
print("\n[10] CHECKING PLOT CONTAINERS")
containers = driver.execute_script("""
    return {
        networkPlot: {
            exists: !!document.getElementById('networkPlot'),
            innerHTML: document.getElementById('networkPlot')?.innerHTML?.substring(0, 200)
        },
        forestPlot: {
            exists: !!document.getElementById('forestPlot'),
            innerHTML: document.getElementById('forestPlot')?.innerHTML?.substring(0, 200)
        },
        leagueTableContainer: {
            exists: !!document.getElementById('leagueTableContainer'),
            innerHTML: document.getElementById('leagueTableContainer')?.innerHTML?.substring(0, 200)
        }
    };
""")
for name, data in containers.items():
    print(f"  {name}: exists={data['exists']}, content={data['innerHTML'][:80] if data['innerHTML'] else 'empty'}...")

driver.quit()
print("\n" + "="*70)
print("DEBUG COMPLETE")
print("="*70)
