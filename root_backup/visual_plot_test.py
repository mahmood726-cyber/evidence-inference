#!/usr/bin/env python3
"""Visual Plot Test for NMA Pro v6.2"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.add_argument('--start-maximized')

driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(3)

# Setup test data
setup = """
window.testEffects = [0.5, 0.3, 0.8, 0.2, 0.6, 0.4, 0.7, 0.35, 0.55, 0.45];
window.testSEs = [0.1, 0.15, 0.2, 0.12, 0.18, 0.14, 0.22, 0.11, 0.16, 0.13];
window.testLabels = ['Study 1', 'Study 2', 'Study 3', 'Study 4', 'Study 5', 'Study 6', 'Study 7', 'Study 8', 'Study 9', 'Study 10'];
window.testNMAStudies = [
    { study: 'S1', treatment1: 'A', treatment2: 'B', effect: 0.3, se: 0.1 },
    { study: 'S2', treatment1: 'A', treatment2: 'B', effect: 0.4, se: 0.15 },
    { study: 'S3', treatment1: 'B', treatment2: 'C', effect: 0.2, se: 0.12 },
    { study: 'S4', treatment1: 'B', treatment2: 'C', effect: 0.25, se: 0.14 },
    { study: 'S5', treatment1: 'A', treatment2: 'C', effect: 0.5, se: 0.18 },
    { study: 'S6', treatment1: 'A', treatment2: 'C', effect: 0.55, se: 0.2 }
];
'Data ready';
"""
driver.execute_script(setup)
print("[OK] Test data initialized")

# Create display container
container_code = """
let container = document.createElement('div');
container.id = 'plot-test';
container.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:white;z-index:99999;overflow:auto;padding:20px;font-family:Arial,sans-serif;';
document.body.appendChild(container);
container.innerHTML = '<h1 style="text-align:center;color:#2c3e50;">NMA Pro v6.2 - Plot Display Test</h1>';
container.innerHTML += '<div id="plot-grid" style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;max-width:1400px;margin:0 auto;"></div>';
'Container created';
"""
driver.execute_script(container_code)

# Generate and display each plot
plots_to_test = [
    ("Baujat Plot", "DiagnosticPlots.baujatPlot(testEffects, testSEs, testLabels)"),
    ("Galbraith Plot", "DiagnosticPlots.galbraithPlot(testEffects, testSEs, testLabels)"),
    ("Contour Funnel", "DiagnosticPlots.contourFunnelPlot(testEffects, testSEs)"),
    ("Evidence Flow", "EvidenceFlow.analyze(testNMAStudies)"),
]

for name, code in plots_to_test:
    try:
        result = driver.execute_script(f"""
        try {{
            const result = {code};
            const svg = result.svg || result;
            const grid = document.getElementById('plot-grid');

            const div = document.createElement('div');
            div.style.cssText = 'border:2px solid #ccc;border-radius:8px;padding:15px;background:#fafafa;';
            div.innerHTML = '<h3 style="margin:0 0 10px 0;color:#333;">{name}</h3>';

            if (typeof svg === 'string' && svg.includes('<svg')) {{
                div.innerHTML += '<div style="background:white;text-align:center;">' + svg + '</div>';
                div.innerHTML += '<p style="color:green;font-weight:bold;margin:10px 0 0 0;">[OK] Rendered</p>';
            }} else {{
                div.innerHTML += '<div style="background:#f0f0f0;padding:20px;overflow:auto;max-height:300px;"><pre>' + JSON.stringify(result, null, 2).substring(0, 800) + '</pre></div>';
                div.innerHTML += '<p style="color:blue;margin:10px 0 0 0;">[OK] Data generated (no SVG)</p>';
            }}

            grid.appendChild(div);
            return 'OK';
        }} catch(e) {{
            const grid = document.getElementById('plot-grid');
            const div = document.createElement('div');
            div.style.cssText = 'border:2px solid #c00;border-radius:8px;padding:15px;background:#fee;';
            div.innerHTML = '<h3 style="margin:0 0 10px 0;color:#c00;">{name}</h3>';
            div.innerHTML += '<p style="color:#c00;">ERROR: ' + e.message + '</p>';
            grid.appendChild(div);
            return 'ERROR: ' + e.message;
        }}
        """)
        print(f"[{'OK' if result == 'OK' else 'X'}] {name}: {result}")
    except Exception as e:
        print(f"[X] {name}: {e}")

# Add L'Abbe plot separately (more complex)
labbe_code = """
try {
    const labbe = DiagnosticPlots.labbePlot(
        [20, 30, 25, 15, 22, 28, 18, 32, 26, 21],
        [100, 150, 120, 80, 110, 140, 90, 160, 130, 100],
        [15, 22, 18, 12, 16, 20, 14, 24, 19, 17],
        [100, 150, 120, 80, 110, 140, 90, 160, 130, 100],
        testLabels
    );
    const svg = labbe.svg || labbe;
    const grid = document.getElementById('plot-grid');
    const div = document.createElement('div');
    div.style.cssText = 'border:2px solid #ccc;border-radius:8px;padding:15px;background:#fafafa;';
    div.innerHTML = '<h3 style="margin:0 0 10px 0;color:#333;">L\\'Abbe Plot</h3>';
    if (typeof svg === 'string' && svg.includes('<svg')) {
        div.innerHTML += '<div style="background:white;text-align:center;">' + svg + '</div>';
        div.innerHTML += '<p style="color:green;font-weight:bold;margin:10px 0 0 0;">[OK] Rendered</p>';
    } else {
        div.innerHTML += '<div style="background:#f0f0f0;padding:20px;overflow:auto;max-height:300px;"><pre>' + JSON.stringify(labbe, null, 2).substring(0, 800) + '</pre></div>';
    }
    grid.appendChild(div);
    return 'OK';
} catch(e) {
    return 'ERROR: ' + e.message;
}
"""
result = driver.execute_script(labbe_code)
print(f"[{'OK' if result == 'OK' else 'X'}] L'Abbe Plot: {result}")

# Add Publication Bias summary
pub_bias_code = """
try {
    const pb = PublicationBias.analyze(testEffects, testSEs);
    const grid = document.getElementById('plot-grid');
    const div = document.createElement('div');
    div.style.cssText = 'border:2px solid #ccc;border-radius:8px;padding:15px;background:#fafafa;';
    div.innerHTML = '<h3 style="margin:0 0 10px 0;color:#333;">Publication Bias Tests</h3>';

    let table = '<table style="width:100%;border-collapse:collapse;background:white;">';
    table += '<tr><td style="padding:8px;border:1px solid #ddd;"><b>Egger p-value:</b></td><td style="padding:8px;border:1px solid #ddd;">' + (pb.egger?.pValue?.toFixed(4) || 'N/A') + '</td></tr>';
    table += '<tr><td style="padding:8px;border:1px solid #ddd;"><b>Begg p-value:</b></td><td style="padding:8px;border:1px solid #ddd;">' + (pb.begg?.pValue?.toFixed(4) || 'N/A') + '</td></tr>';
    table += '<tr><td style="padding:8px;border:1px solid #ddd;"><b>Trim-Fill adjusted:</b></td><td style="padding:8px;border:1px solid #ddd;">' + (pb.trimFill?.adjustedEffect?.toFixed(4) || 'N/A') + '</td></tr>';
    table += '<tr><td style="padding:8px;border:1px solid #ddd;"><b>PET-PEESE:</b></td><td style="padding:8px;border:1px solid #ddd;">' + (pb.petPeese?.estimate?.toFixed(4) || 'N/A') + '</td></tr>';
    table += '</table>';

    div.innerHTML += table;
    div.innerHTML += '<p style="color:green;font-weight:bold;margin:10px 0 0 0;">[OK] All bias tests computed</p>';
    grid.appendChild(div);
    return 'OK';
} catch(e) {
    return 'ERROR: ' + e.message;
}
"""
result = driver.execute_script(pub_bias_code)
print(f"[{'OK' if result == 'OK' else 'X'}] Publication Bias: {result}")

# Add close button
driver.execute_script("""
const container = document.getElementById('plot-test');
const btn = document.createElement('button');
btn.textContent = 'Close Test View';
btn.style.cssText = 'display:block;margin:30px auto;padding:15px 40px;font-size:18px;background:#3498db;color:white;border:none;border-radius:5px;cursor:pointer;';
btn.onclick = function() { container.remove(); };
container.appendChild(btn);
""")

print("\n>>> Plots displayed in browser")
print(">>> Taking screenshot...")

time.sleep(2)
driver.save_screenshot('C:/Users/user/nma_visual_plots.png')
print("[OK] Screenshot saved: C:/Users/user/nma_visual_plots.png")

print("\n>>> Browser will remain open for 20 seconds for inspection...")
time.sleep(20)

driver.quit()
print("\nTest complete.")
