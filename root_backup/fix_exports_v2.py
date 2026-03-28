#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix missing exports for loadDemoDataset, DEMO_DATASETS, runAnalysis"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file: {len(content.split(chr(10)))} lines")

# Find the export block and add missing exports
target = """window.eggerTest = eggerTest;
  window.runAdvancedValidation = runAdvancedValidation;
  window.renderGalbraithPlot = renderGalbraithPlot;
  window.renderROB2TrafficLight = renderROB2TrafficLight;
}"""

new_exports = """window.eggerTest = eggerTest;
  window.runAdvancedValidation = runAdvancedValidation;
  window.renderGalbraithPlot = renderGalbraithPlot;
  window.renderROB2TrafficLight = renderROB2TrafficLight;
}

// Additional critical exports for Selenium testing
if (typeof window !== 'undefined') {
  // Make sure runAnalysis is globally accessible
  if (typeof runAnalysis === 'function') window.runAnalysis = runAnalysis;
  if (typeof loadDemoDataset === 'function') window.loadDemoDataset = loadDemoDataset;
  if (typeof DEMO_DATASETS !== 'undefined') window.DEMO_DATASETS = DEMO_DATASETS;
  if (typeof addStudyRow === 'function') window.addStudyRow = addStudyRow;
  if (typeof updateDataSummary === 'function') window.updateDataSummary = updateDataSummary;
  if (typeof AppState !== 'undefined') window.AppState = AppState;
  if (typeof renderForestPlot === 'function') window.renderForestPlot = renderForestPlot;
  if (typeof renderFunnelPlot === 'function') window.renderFunnelPlot = renderFunnelPlot;
  if (typeof calculatePooledEstimate === 'function') window.calculatePooledEstimate = calculatePooledEstimate;
  if (typeof runBayesianAnalysis === 'function') window.runBayesianAnalysis = runBayesianAnalysis;
  console.log('[PairwisePro] Critical functions exported to window');
}"""

if target in content:
    content = content.replace(target, new_exports)
    print("Added missing exports")
else:
    # Try simpler pattern
    alt_target = "window.renderROB2TrafficLight = renderROB2TrafficLight;\n}"
    if alt_target in content:
        content = content.replace(alt_target, new_exports)
        print("Added missing exports (alternative method)")
    else:
        print("ERROR: Could not find insertion point")
        print("Searching for pattern...")
        import re
        matches = list(re.finditer(r'window\.renderROB2TrafficLight', content))
        for m in matches:
            print(f"  Found at position {m.start()}: {content[m.start():m.start()+100]}")

# Write back
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

final_lines = len(content.split('\n'))
print(f"Final file: {final_lines} lines")
print("Done!")
