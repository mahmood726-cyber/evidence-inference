#!/usr/bin/env python3
"""Debug NMA Pro - test with correct field names"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.alert import Alert
import time
import sys

# Set UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

print("="*70)
print("NMA Pro v6.2 - DEBUG SESSION v2")
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

# Test with CORRECT field names
print("\n[1] Testing FrequentistNMA with CORRECT field names...")
result = js("""
try {
    // Use treatment1/treatment2 as expected by code
    var studies = [
        {id:1, study:'S1', treatment1:'A', treatment2:'B', events1:20, n1:100, events2:10, n2:100},
        {id:2, study:'S2', treatment1:'A', treatment2:'C', events1:25, n1:100, events2:15, n2:100},
        {id:3, study:'S3', treatment1:'B', treatment2:'C', events1:12, n1:100, events2:18, n2:100}
    ];
    var result = FrequentistNMA.analyze(studies, {reference: 'A', effectMeasure: 'OR'});
    return {
        success: true,
        tau2: result.tau2,
        tau: result.tau,
        treatments: result.treatments,
        effectA: result.effects ? result.effects.effects['A'] : null,
        effectB: result.effects ? result.effects.effects['B'] : null,
        effectC: result.effects ? result.effects.effects['C'] : null
    };
} catch(e) {
    return {success: false, error: e.message, stack: e.stack ? e.stack.substring(0, 800) : ''};
}
""")
print(f"  Result: {result}")

if result and result.get('success'):
    print("\n  [PASS] FrequentistNMA.analyze works with correct field names!")
    print(f"  Tau2: {result.get('tau2')}")
    print(f"  Treatments: {result.get('treatments')}")
else:
    print("\n  [FAIL] FrequentistNMA.analyze still fails")

# Test BayesianNMA
print("\n[2] Testing BayesianNMA...")
bayes_result = js("""
try {
    var studies = [
        {id:1, study:'S1', treatment1:'A', treatment2:'B', events1:20, n1:100, events2:10, n2:100},
        {id:2, study:'S2', treatment1:'A', treatment2:'C', events1:25, n1:100, events2:15, n2:100},
        {id:3, study:'S3', treatment1:'B', treatment2:'C', events1:12, n1:100, events2:18, n2:100}
    ];
    var result = BayesianNMA.analyze(studies, {reference: 'A', nIter: 100, nBurnin: 50, nChains: 2});
    return {
        success: true,
        hasEffects: !!result.effects,
        hasDiagnostics: !!result.diagnostics
    };
} catch(e) {
    return {success: false, error: e.message};
}
""")
print(f"  Result: {bayes_result}")

# Test data loading into AppState
print("\n[3] Testing AppState data loading and UI update...")
ui_result = js("""
try {
    // Load data
    AppState.studies = [
        {id:1, name:'Study 1', treatment1:'A', treatment2:'B', events1:20, n1:100, events2:10, n2:100},
        {id:2, name:'Study 2', treatment1:'A', treatment2:'C', events1:25, n1:100, events2:15, n2:100},
        {id:3, name:'Study 3', treatment1:'B', treatment2:'C', events1:12, n1:100, events2:18, n2:100},
        {id:4, name:'Study 4', treatment1:'A', treatment2:'B', events1:30, n1:120, events2:15, n2:120}
    ];
    AppState.reference = 'A';
    AppState.effectMeasure = 'OR';
    AppState.estimator = 'REML';

    // Check if updateUI exists
    var hasUpdateUI = typeof updateUI === 'function';
    var hasRunAnalysis = typeof runAnalysis === 'function';
    var hasPerformAnalysis = typeof performAnalysis === 'function';

    return {
        studiesLoaded: AppState.studies.length,
        reference: AppState.reference,
        hasUpdateUI: hasUpdateUI,
        hasRunAnalysis: hasRunAnalysis,
        hasPerformAnalysis: hasPerformAnalysis
    };
} catch(e) {
    return {error: e.message};
}
""")
print(f"  Result: {ui_result}")

# Try runAnalysis if it exists
print("\n[4] Testing runAnalysis function...")
analysis_result = js("""
try {
    if (typeof runAnalysis === 'function') {
        var result = runAnalysis();
        return {called: true, resultType: typeof result};
    } else if (typeof performAnalysis === 'function') {
        var result = performAnalysis();
        return {called: true, fn: 'performAnalysis', resultType: typeof result};
    } else {
        // Check what analysis functions exist
        var funcs = [];
        if (typeof FrequentistNMA !== 'undefined') funcs.push('FrequentistNMA');
        if (typeof analyze !== 'undefined') funcs.push('analyze');
        return {called: false, availableFuncs: funcs};
    }
} catch(e) {
    return {error: e.message, stack: e.stack ? e.stack.substring(0, 500) : ''};
}
""")
print(f"  Result: {analysis_result}")

# Check what buttons exist
print("\n[5] Available buttons...")
buttons = js("""
var btns = document.querySelectorAll('button');
var results = [];
btns.forEach(function(b) {
    var text = b.textContent.trim().substring(0, 40);
    if (text && !text.includes('undefined')) {
        results.push({text: text, id: b.id || 'no-id', onclick: b.onclick ? 'yes' : 'no'});
    }
});
return results.slice(0, 20);
""")
if buttons:
    for b in buttons:
        print(f"  - {b}")

# Check tabs
print("\n[6] Tab navigation elements...")
tabs = js("""
var tabs = document.querySelectorAll('[role="tab"], .nav-link, [data-tab], .tab-button');
var results = [];
tabs.forEach(function(t) {
    results.push({
        text: t.textContent.trim().substring(0, 30),
        id: t.id || '',
        dataTab: t.getAttribute('data-tab') || '',
        ariaSelected: t.getAttribute('aria-selected') || ''
    });
});
return results;
""")
if tabs:
    for t in tabs:
        print(f"  - {t}")

# Check for JavaScript errors
print("\n[7] Browser console errors...")
try:
    errors = driver.get_log("browser")
    severe = [e for e in errors if e["level"] == "SEVERE"]
    if severe:
        for e in severe[:5]:
            msg = e['message'][:150]
            print(f"  [SEVERE] {msg}")
    else:
        print("  No SEVERE errors")
except Exception as e:
    print(f"  Could not get logs: {e}")

driver.quit()
print("\n" + "="*70)
