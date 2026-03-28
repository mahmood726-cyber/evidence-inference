#!/usr/bin/env python3
"""Add validation UI function to TruthCert-PairwisePro"""

def main():
    print("Adding validation UI function...")

    with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
        content = f.read()

    validation_ui_code = '''

// =============================================================================
// VALIDATION UI FUNCTION
// =============================================================================

function runExtendedValidationUI() {
  const resultsDiv = document.getElementById('validationResults');
  if (!resultsDiv) {
    console.error('validationResults div not found');
    return;
  }

  resultsDiv.innerHTML = '<div style="text-align: center; padding: 20px;"><span class="spinner"></span> Running validation tests...</div>';

  // Run tests
  setTimeout(() => {
    try {
      const results = runAutomatedTests();

      let html = '<div style="border-radius: 8px; padding: 12px; margin-bottom: 12px; background: ' +
                 (results.failed === 0 ? 'var(--success-bg, #d4edda)' : 'var(--warning-bg, #fff3cd)') + ';">';
      html += '<div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">';
      html += results.failed === 0 ? '✓ All Tests Passed' : '⚠ Some Tests Failed';
      html += '</div>';
      html += '<div>Passed: <strong>' + results.passed + '</strong> / ' + (results.passed + results.failed) + '</div>';
      html += '<div>Pass Rate: <strong>' + Math.round(100 * results.passed / (results.passed + results.failed)) + '%</strong></div>';
      html += '</div>';

      html += '<table style="width: 100%; border-collapse: collapse; font-size: 13px;">';
      html += '<thead><tr style="background: var(--surface-overlay, #f8f9fa);">';
      html += '<th style="padding: 8px; text-align: left; border-bottom: 1px solid var(--border-color, #dee2e6);">Test</th>';
      html += '<th style="padding: 8px; text-align: left; border-bottom: 1px solid var(--border-color, #dee2e6);">Result</th>';
      html += '<th style="padding: 8px; text-align: left; border-bottom: 1px solid var(--border-color, #dee2e6);">Value</th>';
      html += '<th style="padding: 8px; text-align: left; border-bottom: 1px solid var(--border-color, #dee2e6);">Expected</th>';
      html += '</tr></thead><tbody>';

      results.tests.forEach(function(test) {
        const rowBg = test.passed ? '' : 'background: var(--danger-bg, #f8d7da);';
        const statusIcon = test.passed ? '<span style="color: green;">✓</span>' : '<span style="color: red;">✗</span>';
        const value = test.value !== undefined ? (typeof test.value === 'number' ? test.value.toFixed(6) : test.value) : '-';
        const expected = test.expected !== undefined ? (typeof test.expected === 'number' ? test.expected.toFixed(6) : test.expected) : '-';
        html += '<tr style="' + rowBg + '">';
        html += '<td style="padding: 8px; border-bottom: 1px solid var(--border-color, #dee2e6);">' + test.name + '</td>';
        html += '<td style="padding: 8px; border-bottom: 1px solid var(--border-color, #dee2e6);">' + statusIcon + ' ' + (test.passed ? 'PASS' : 'FAIL') + '</td>';
        html += '<td style="padding: 8px; border-bottom: 1px solid var(--border-color, #dee2e6); font-family: monospace;">' + value + '</td>';
        html += '<td style="padding: 8px; border-bottom: 1px solid var(--border-color, #dee2e6); font-family: monospace;">' + expected + '</td>';
        html += '</tr>';
      });

      html += '</tbody></table>';

      html += '<div style="margin-top: 12px; padding: 12px; background: var(--surface-overlay, #f8f9fa); border-radius: 8px; font-size: 12px;">';
      html += '<strong>Validation Notes:</strong><br>';
      html += '• Reference: metafor R package v4.6-0<br>';
      html += '• Test Dataset: BCG Vaccine (dat.bcg)<br>';
      html += '• Tolerance: 0.001 for effect sizes, 0.01 for p-values<br>';
      html += '• Validated: ' + new Date().toISOString().split('T')[0];
      html += '</div>';

      resultsDiv.innerHTML = html;

    } catch (e) {
      resultsDiv.innerHTML = '<div style="color: red; padding: 12px;">Error running validation: ' + e.message + '</div>';
      console.error('Validation error:', e);
    }
  }, 100);
}

// Export
if (typeof window !== 'undefined') {
  window.runExtendedValidationUI = runExtendedValidationUI;
}
'''

    # Check if already added
    if 'runExtendedValidationUI' in content:
        print("runExtendedValidationUI already exists - skipping")
        return

    # Append
    content = content + validation_ui_code

    with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
        f.write(content)

    print("OK - Added runExtendedValidationUI function")

if __name__ == '__main__':
    main()
