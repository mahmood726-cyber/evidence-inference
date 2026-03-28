"""Check data structure for publication bias modules"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time
import json

options = Options()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(2)

driver.execute_script("loadDemoDataset('thrombolytics')")
time.sleep(0.3)
driver.execute_script("document.getElementById('runAnalysisBtn').click()")
time.sleep(2)

# Check structure of processed data
result = driver.execute_script("""
    const processed = AppState.results?.processed;
    if (!processed) return {error: 'No processed data'};

    // Get first item to see structure
    if (Array.isArray(processed)) {
        return {
            isArray: true,
            length: processed.length,
            firstItem: processed[0],
            keys: Object.keys(processed[0] || {})
        };
    } else {
        return {
            isArray: false,
            keys: Object.keys(processed),
            sample: JSON.stringify(processed).substring(0, 500)
        };
    }
""")
print('Processed data structure:')
print(json.dumps(result, indent=2))

# Check InfluenceDiagnostics methods
inf_methods = driver.execute_script("""
    if (typeof InfluenceDiagnostics === 'undefined') return {error: 'Not found'};
    return Object.keys(InfluenceDiagnostics);
""")
print('\nInfluenceDiagnostics methods:', inf_methods)

# Check TrimAndFill module
taf_methods = driver.execute_script("""
    if (typeof TrimAndFill === 'undefined') return {error: 'Not found'};
    return Object.keys(TrimAndFill);
""")
print('TrimAndFill methods:', taf_methods)

# Check EggersTest module
egger_methods = driver.execute_script("""
    if (typeof EggersTest === 'undefined') return {error: 'Not found'};
    return Object.keys(EggersTest);
""")
print('EggersTest methods:', egger_methods)

# Try to understand what the modules expect
print('\n--- Testing module expectations ---')

# Test with direct yi/vi extraction
test_result = driver.execute_script("""
    const processed = AppState.results?.processed;
    if (!processed || !Array.isArray(processed)) return {error: 'Not array'};

    // Extract yi and vi arrays
    const yi = processed.map(p => p.yi);
    const vi = processed.map(p => p.vi);

    return {
        yi: yi,
        vi: vi,
        hasYi: yi.every(y => y !== undefined),
        hasVi: vi.every(v => v !== undefined)
    };
""")
print('\nExtracted yi/vi:', json.dumps(test_result, indent=2))

driver.quit()
