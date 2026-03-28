#!/usr/bin/env python3
"""Debug NMA Pro issues"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.alert import Alert
import time

print("="*70)
print("NMA Pro v6.2 - DEBUG SESSION")
print("="*70)

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Edge(options=options)
driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html")
time.sleep(4)

def js(s):
    try:
        try: Alert(driver).dismiss()
        except: pass
        return driver.execute_script(s)
    except Exception as e:
        print(f"  Error: {e}")
        return None

# Check what tab IDs actually exist
print("\n[1] Finding actual tab IDs...")
tab_ids = js("""
var elements = document.querySelectorAll('[id]');
var ids = [];
elements.forEach(function(el) {
    if (el.id && (el.id.includes('Tab') || el.classList.contains('tab-content') || el.classList.contains('tab-pane'))) {
        ids.push(el.id);
    }
});
return ids;
""")
print(f"  Tab-related IDs: {tab_ids}")

# Check all div IDs
print("\n[2] All main container IDs...")
all_ids = js("""
var divs = document.querySelectorAll('div[id], section[id]');
var ids = [];
divs.forEach(function(d) { if(d.id) ids.push(d.id); });
return ids.slice(0, 30);
""")
print(f"  Container IDs: {all_ids}")

# Test FrequentistNMA directly
print("\n[3] Testing FrequentistNMA...")
print("  FrequentistNMA exists:", js("return typeof FrequentistNMA !== 'undefined'"))
print("  FrequentistNMA.analyze exists:", js("return typeof FrequentistNMA.analyze === 'function'"))

# Load data and try analysis
print("\n[4] Loading test data...")
js("""
AppState.studies = [
    {id:1, study:'S1', treat1:'A', treat2:'B', effect:0.5, se:0.2},
    {id:2, study:'S2', treat1:'A', treat2:'C', effect:0.3, se:0.25},
    {id:3, study:'S3', treat1:'B', treat2:'C', effect:-0.2, se:0.18}
];
AppState.reference = 'A';
""")
print("  Studies:", js("return AppState.studies ? AppState.studies.length : 0"))

print("\n[5] Attempting analysis with error capture...")
result = js("""
try {
    var result = FrequentistNMA.analyze(AppState.studies, {reference: 'A'});
    return {success: true, tau2: result.tau2, treatments: result.treatments};
} catch(e) {
    return {success: false, error: e.message, stack: e.stack ? e.stack.substring(0, 500) : ''};
}
""")
print(f"  Result: {result}")

# Check browser console errors
print("\n[6] Browser console errors...")
errors = driver.get_log("browser")
for e in errors:
    if e["level"] in ["SEVERE", "WARNING"]:
        print(f"  [{e['level']}] {e['message'][:100]}")

# Try clicking the run analysis button
print("\n[7] Finding Run Analysis button...")
buttons = js("""
var btns = document.querySelectorAll('button');
var results = [];
btns.forEach(function(b) {
    if (b.textContent.toLowerCase().includes('run') || b.textContent.toLowerCase().includes('analysis')) {
        results.push({text: b.textContent.trim(), onclick: b.onclick ? 'has onclick' : 'no onclick'});
    }
});
return results;
""")
print(f"  Run buttons: {buttons}")

# Check if there's an analyze function
print("\n[8] Global analyze functions...")
print("  runAnalysis:", js("return typeof runAnalysis"))
print("  analyze:", js("return typeof analyze"))
print("  performAnalysis:", js("return typeof performAnalysis"))

driver.quit()
print("\n" + "="*70)
