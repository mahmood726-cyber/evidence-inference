#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix function name mismatches and add missing exports"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file: {len(content.split(chr(10)))} lines")
fixes_made = []

# 1. Create wrapper/alias functions for the expected names
wrapper_functions = '''
// =============================================================================
// FUNCTION ALIASES - Map expected names to actual implementations
// =============================================================================

// Three-Level Meta-Analysis alias
function threeLevelMetaAnalysis(yi, vi, cluster, options = {}) {
  // Use the existing threeLevelMA implementation
  if (typeof threeLevelMA === 'function') {
    return threeLevelMA(yi, vi, cluster);
  }
  // Fallback to threeLevel_MetaAnalysis if available
  if (typeof threeLevel_MetaAnalysis === 'function') {
    const data = yi.map((y, i) => ({
      yi: y,
      vi: vi[i],
      cluster: cluster ? cluster[i] : i
    }));
    return threeLevel_MetaAnalysis(data, options);
  }
  return { error: 'Three-level MA not available' };
}

// Dose-Response Meta-Analysis alias
function doseResponseMetaAnalysis(doses, yi, se, options = {}) {
  // Use existing doseResponseSpline if available
  if (typeof doseResponseSpline === 'function') {
    const studies = doses.map((d, i) => ({
      dose: d,
      yi: yi[i],
      se: se[i] || Math.sqrt(0.01)
    }));
    return doseResponseSpline(studies, options.nKnots || 3);
  }
  // Simple linear dose-response as fallback
  const k = doses.length;
  const validIdx = doses.map((d, i) => d > 0 && yi[i] !== 0).map((v, i) => v ? i : -1).filter(i => i >= 0);

  if (validIdx.length < 2) {
    return { error: 'Insufficient data for dose-response' };
  }

  // Simple weighted regression
  const x = validIdx.map(i => doses[i]);
  const y = validIdx.map(i => yi[i]);
  const w = validIdx.map(i => 1 / (se[i] * se[i] || 0.01));

  const sumW = w.reduce((a, b) => a + b, 0);
  const sumWX = x.reduce((acc, xi, i) => acc + w[i] * xi, 0);
  const sumWY = y.reduce((acc, yi, i) => acc + w[i] * yi, 0);
  const sumWXX = x.reduce((acc, xi, i) => acc + w[i] * xi * xi, 0);
  const sumWXY = x.reduce((acc, xi, i) => acc + w[i] * xi * y[i], 0);

  const slope = (sumWXY - sumWX * sumWY / sumW) / (sumWXX - sumWX * sumWX / sumW);
  const intercept = (sumWY - slope * sumWX) / sumW;

  return {
    linear: {
      slope: slope,
      intercept: intercept,
      se: Math.sqrt(1 / (sumWXX - sumWX * sumWX / sumW))
    },
    method: 'Linear dose-response (weighted regression)',
    k: validIdx.length
  };
}

// ROB 2.0 Assessment alias
function assessROB2(domains) {
  // domains = { D1: 'Low', D2: 'Some concerns', D3: 'Low', D4: 'Low', D5: 'High' }
  // or domains = ['Low', 'Some concerns', 'Low', 'Low', 'High']

  let domainValues;
  if (Array.isArray(domains)) {
    domainValues = domains;
  } else {
    domainValues = ['D1', 'D2', 'D3', 'D4', 'D5'].map(d => domains[d] || 'No information');
  }

  const domainLabels = [
    'Randomization process',
    'Deviations from interventions',
    'Missing outcome data',
    'Measurement of outcome',
    'Selection of reported result'
  ];

  // Determine overall risk using ROB 2.0 algorithm
  let overall;
  if (domainValues.includes('High')) {
    overall = 'High';
  } else if (domainValues.filter(v => v === 'Some concerns').length >= 2) {
    overall = 'High';  // Multiple some concerns = high
  } else if (domainValues.includes('Some concerns')) {
    overall = 'Some concerns';
  } else if (domainValues.every(v => v === 'Low')) {
    overall = 'Low';
  } else {
    overall = 'No information';
  }

  return {
    domains: domainLabels.map((label, i) => ({
      domain: `D${i + 1}`,
      label: label,
      judgment: domainValues[i]
    })),
    overall: overall,
    reference: 'Sterne JA et al. BMJ 2019;366:l4898'
  };
}

// ROBINS-I Assessment alias
function assessROBINS_I(domains) {
  // 7 domains for non-randomized studies
  let domainValues;
  if (Array.isArray(domains)) {
    domainValues = domains;
  } else {
    domainValues = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'].map(d => domains[d] || 'No information');
  }

  const domainLabels = [
    'Confounding',
    'Selection of participants',
    'Classification of interventions',
    'Deviations from interventions',
    'Missing data',
    'Measurement of outcomes',
    'Selection of reported result'
  ];

  // Determine overall risk
  let overall;
  if (domainValues.includes('Critical')) {
    overall = 'Critical';
  } else if (domainValues.includes('Serious')) {
    overall = 'Serious';
  } else if (domainValues.includes('Moderate')) {
    overall = 'Moderate';
  } else if (domainValues.every(v => v === 'Low')) {
    overall = 'Low';
  } else {
    overall = 'No information';
  }

  return {
    domains: domainLabels.map((label, i) => ({
      domain: `D${i + 1}`,
      label: label,
      judgment: domainValues[i]
    })),
    overall: overall,
    reference: 'Sterne JA et al. BMJ 2016;355:i4919'
  };
}

'''

# Insert before export section
export_marker = "// Export\nif (typeof window !== 'undefined')"
if export_marker in content:
    content = content.replace(export_marker, wrapper_functions + export_marker)
    fixes_made.append("Added threeLevelMetaAnalysis wrapper function")
    fixes_made.append("Added doseResponseMetaAnalysis wrapper function")
    fixes_made.append("Added assessROB2 function")
    fixes_made.append("Added assessROBINS_I function")
else:
    print("ERROR: Could not find export marker")

# 2. Add window exports for the new functions
new_exports = '''
  window.threeLevelMetaAnalysis = threeLevelMetaAnalysis;
  window.doseResponseMetaAnalysis = doseResponseMetaAnalysis;
  window.assessROB2 = assessROB2;
  window.assessROBINS_I = assessROBINS_I;
  window.eggerTest = eggerTest;'''

# Find a good place to insert exports
# Look for existing validation exports
if 'window.validateROB2 = validateROB2;' in content:
    content = content.replace(
        'window.validateROB2 = validateROB2;',
        'window.validateROB2 = validateROB2;' + new_exports
    )
    fixes_made.append("Added window exports for new functions")
elif 'window.runAdvancedValidation = runAdvancedValidation;' in content:
    content = content.replace(
        'window.runAdvancedValidation = runAdvancedValidation;',
        'window.runAdvancedValidation = runAdvancedValidation;' + new_exports
    )
    fixes_made.append("Added window exports for new functions")

# 3. Make sure winnersCurseCorrection exists
if 'function winnersCurseCorrection' not in content:
    winners_func = '''
// Winners' Curse Correction
function winnersCurseCorrection(yi, vi, alpha = 0.05) {
  const k = yi.length;
  const sei = vi.map(v => Math.sqrt(v));
  const zi = yi.map((y, i) => y / sei[i]);
  const z_crit = 1.96;

  const significant = zi.map(z => Math.abs(z) > z_crit);
  const n_sig = significant.filter(s => s).length;

  const corrected = yi.map((y, i) => {
    if (significant[i]) {
      return y * 0.85; // Shrinkage
    }
    return y;
  });

  return {
    original: yi,
    corrected: corrected,
    n_significant: n_sig,
    n_total: k,
    method: 'Simple shrinkage correction'
  };
}

'''
    if export_marker in content:
        content = content.replace(export_marker, winners_func + export_marker)
        fixes_made.append("Added winnersCurseCorrection function")

# Write back
with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

final_lines = len(content.split('\n'))
print(f"Final file: {final_lines} lines")
print(f"\nFixes made ({len(fixes_made)}):")
for fix in fixes_made:
    print(f"  - {fix}")

print("\nDone!")
