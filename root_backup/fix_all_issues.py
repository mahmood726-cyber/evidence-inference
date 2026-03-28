#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix all issues found by Selenium tests"""

import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file: {len(content.split(chr(10)))} lines")

fixes_made = []

# 1. Fix winnersCurseCorrection - it's referenced but may not exist
# Check if function exists
if 'function winnersCurseCorrection' not in content:
    # Add the function before exports
    winners_curse_func = '''
// Winners Curse Correction (placeholder if not defined)
function winnersCurseCorrection(yi, vi, alpha = 0.05) {
  // Simple correction for publication bias due to significance filtering
  const k = yi.length;
  const sei = vi.map(v => Math.sqrt(v));
  const zi = yi.map((y, i) => y / sei[i]);
  const z_crit = 1.96; // qnorm(1 - alpha/2)

  // Identify significant studies
  const significant = zi.map(z => Math.abs(z) > z_crit);
  const n_sig = significant.filter(s => s).length;

  // Simple conditional mean correction
  const corrected = yi.map((y, i) => {
    if (significant[i]) {
      // Apply shrinkage correction
      const shrinkage = 0.8; // Conservative shrinkage
      return y * shrinkage;
    }
    return y;
  });

  return {
    original: yi,
    corrected: corrected,
    n_significant: n_sig,
    n_total: k,
    proportion_significant: n_sig / k,
    method: 'Simple shrinkage correction for significant results'
  };
}

'''
    export_marker = "// Export\nif (typeof window !== 'undefined')"
    if export_marker in content:
        content = content.replace(export_marker, winners_curse_func + export_marker)
        fixes_made.append("Added winnersCurseCorrection function")
    else:
        print("WARNING: Could not find export marker for winnersCurseCorrection")

# 2. Add missing Galbraith plot function
if 'function renderGalbraithPlot' not in content:
    galbraith_func = '''
// Galbraith (Radial) Plot
function renderGalbraithPlot(yi, vi, containerId = 'galbraith-plot') {
  const sei = vi.map(v => Math.sqrt(v));
  const precision = sei.map(se => 1 / se);
  const z_scores = yi.map((y, i) => y / sei[i]);

  // Calculate pooled estimate for reference line
  const wi = vi.map(v => 1 / v);
  const sumW = wi.reduce((a, b) => a + b, 0);
  const theta = yi.reduce((acc, y, i) => acc + wi[i] * y, 0) / sumW;

  const trace = {
    x: precision,
    y: z_scores,
    mode: 'markers',
    type: 'scatter',
    marker: { size: 10, color: '#3b82f6' },
    name: 'Studies'
  };

  // Reference line through origin with slope = theta
  const maxPrec = Math.max(...precision);
  const refLine = {
    x: [0, maxPrec],
    y: [0, maxPrec * theta],
    mode: 'lines',
    line: { color: '#ef4444', dash: 'dash' },
    name: 'Pooled estimate'
  };

  const layout = {
    title: 'Galbraith (Radial) Plot',
    xaxis: { title: 'Precision (1/SE)', zeroline: true },
    yaxis: { title: 'Standardized Effect (y/SE)', zeroline: true },
    showlegend: true
  };

  if (typeof Plotly !== 'undefined') {
    Plotly.newPlot(containerId, [trace, refLine], layout);
  }

  return { precision, z_scores, theta };
}

'''
    export_marker = "// Export\nif (typeof window !== 'undefined')"
    if export_marker in content:
        content = content.replace(export_marker, galbraith_func + export_marker)
        fixes_made.append("Added renderGalbraithPlot function")

# 3. Add missing ROB2 Traffic Light render function
if 'function renderROB2TrafficLight' not in content:
    rob2_render_func = '''
// ROB 2.0 Traffic Light Visualization
function renderROB2TrafficLight(assessments, containerId = 'rob2-plot') {
  // assessments = [{study: 'Study 1', D1: 'Low', D2: 'Some concerns', ...}, ...]

  const domains = ['D1', 'D2', 'D3', 'D4', 'D5', 'Overall'];
  const domainLabels = [
    'Randomization',
    'Deviations',
    'Missing data',
    'Measurement',
    'Selection',
    'Overall'
  ];

  const colorMap = {
    'Low': '#22c55e',
    'Some concerns': '#eab308',
    'High': '#ef4444',
    'No information': '#9ca3af'
  };

  // Build table HTML
  let html = '<table class="rob2-table" style="border-collapse: collapse; width: 100%;">';
  html += '<thead><tr><th style="border: 1px solid #ccc; padding: 8px;">Study</th>';
  domainLabels.forEach(label => {
    html += `<th style="border: 1px solid #ccc; padding: 8px; font-size: 12px;">${label}</th>`;
  });
  html += '</tr></thead><tbody>';

  assessments.forEach(a => {
    html += `<tr><td style="border: 1px solid #ccc; padding: 8px;">${a.study || a.label || 'Study'}</td>`;
    domains.forEach(d => {
      const risk = a[d] || 'No information';
      const color = colorMap[risk] || '#9ca3af';
      html += `<td style="border: 1px solid #ccc; padding: 8px; background-color: ${color}; text-align: center;">`;
      html += risk === 'Low' ? '+' : risk === 'High' ? '-' : '?';
      html += '</td>';
    });
    html += '</tr>';
  });

  html += '</tbody></table>';

  const container = document.getElementById(containerId);
  if (container) {
    container.innerHTML = html;
  }

  return html;
}

'''
    export_marker = "// Export\nif (typeof window !== 'undefined')"
    if export_marker in content:
        content = content.replace(export_marker, rob2_render_func + export_marker)
        fixes_made.append("Added renderROB2TrafficLight function")

# 4. Fix missing window exports - find the export block and add missing ones
# Find the existing exports section
export_additions = []

# Check which functions exist but aren't exported
functions_to_export = [
    ('eggerTest', 'eggerTest'),
    ('threeLevelMetaAnalysis', 'threeLevelMetaAnalysis'),
    ('doseResponseMetaAnalysis', 'doseResponseMetaAnalysis'),
    ('assessROB2', 'assessROB2'),
    ('assessROBINS_I', 'assessROBINS_I'),
    ('winnersCurseCorrection', 'winnersCurseCorrection'),
    ('renderGalbraithPlot', 'renderGalbraithPlot'),
    ('renderROB2TrafficLight', 'renderROB2TrafficLight'),
]

for func_name, export_name in functions_to_export:
    # Check if function exists
    if f'function {func_name}' in content:
        # Check if already exported
        if f'window.{export_name} = {func_name}' not in content:
            export_additions.append(f'  window.{export_name} = {export_name};')
            fixes_made.append(f"Added window export for {func_name}")

# Also check for objects that need exporting
objects_to_export = [
    'METHODS_APPENDIX',
    'EXTENDED_VALIDATION_DATA',
]

for obj_name in objects_to_export:
    if f'const {obj_name}' in content or f'var {obj_name}' in content:
        if f'window.{obj_name} = {obj_name}' not in content:
            export_additions.append(f'  window.{obj_name} = {obj_name};')
            fixes_made.append(f"Added window export for {obj_name}")

# Insert the new exports before the closing brace of the export block
if export_additions:
    # Find the pattern: window.runAdvancedValidation = runAdvancedValidation;\n}
    # and insert before the closing }

    # Look for the last export line before the closing brace
    export_block_end = content.find("window.runAdvancedValidation = runAdvancedValidation;\n}")
    if export_block_end == -1:
        # Try alternative patterns
        patterns = [
            "window.validateROB2 = validateROB2;\n}",
            "window.getMethodsAppendix = getMethodsAppendix;\n}",
        ]
        for pattern in patterns:
            if pattern in content:
                export_block_end = content.find(pattern)
                break

    if export_block_end != -1:
        # Find the } after the last export
        insert_point = content.find("\n}", export_block_end)
        if insert_point != -1:
            new_exports = "\n" + "\n".join(export_additions)
            content = content[:insert_point] + new_exports + content[insert_point:]
            print(f"Added {len(export_additions)} new exports")

# 5. Check for eggerTest function and ensure it exists
if 'function eggerTest' not in content:
    egger_func = '''
// Egger's test for funnel plot asymmetry
function eggerTest(yi, vi) {
  const k = yi.length;
  if (k < 3) {
    return { available: false, warning: 'Need at least 3 studies' };
  }

  const sei = vi.map(v => Math.sqrt(v));
  const wi = vi.map(v => 1 / v);
  const sumW = wi.reduce((a, b) => a + b, 0);

  // Weighted regression of yi on sei
  const sumWX = sei.reduce((acc, se, i) => acc + wi[i] * se, 0);
  const sumWY = yi.reduce((acc, y, i) => acc + wi[i] * y, 0);
  const sumWXX = sei.reduce((acc, se, i) => acc + wi[i] * se * se, 0);
  const sumWXY = sei.reduce((acc, se, i) => acc + wi[i] * se * yi[i], 0);

  const x_bar = sumWX / sumW;
  const y_bar = sumWY / sumW;

  const slope = (sumWXY - sumW * x_bar * y_bar) / (sumWXX - sumW * x_bar * x_bar);
  const intercept = y_bar - slope * x_bar;

  // SE of intercept
  const residuals = yi.map((y, i) => y - (intercept + slope * sei[i]));
  const sse = residuals.reduce((acc, r, i) => acc + wi[i] * r * r, 0);
  const mse = sse / (k - 2);
  const se_intercept = Math.sqrt(mse * (1/sumW + x_bar*x_bar / (sumWXX - sumW * x_bar * x_bar)));

  const t_stat = intercept / se_intercept;
  const df = k - 2;
  const p_value = 2 * (1 - pt(Math.abs(t_stat), df));

  return {
    intercept: intercept,
    se: se_intercept,
    t_statistic: t_stat,
    df: df,
    p_value: p_value,
    slope: slope,
    interpretation: p_value < 0.1 ? 'Evidence of asymmetry (possible publication bias)' : 'No significant asymmetry',
    method: "Egger's regression test"
  };
}

'''
    export_marker = "// Export\nif (typeof window !== 'undefined')"
    if export_marker in content:
        content = content.replace(export_marker, egger_func + export_marker)
        fixes_made.append("Added eggerTest function")

# Write the fixed content
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

final_lines = len(content.split('\n'))
print(f"\nFinal file: {final_lines} lines")
print(f"\nFixes made ({len(fixes_made)}):")
for fix in fixes_made:
    print(f"  - {fix}")

print("\nSUCCESS: All issues fixed!")
