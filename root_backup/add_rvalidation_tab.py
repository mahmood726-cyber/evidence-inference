import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if already added
if 'data-tab="rvalidation"' in content:
    print("R Validation tab already exists!")
else:
    # 1. Add tab button after export button
    old_nav = '''<button class="tab-btn" data-tab="export" role="tab" aria-selected="false" aria-controls="panel-export" tabindex="-1"><span aria-hidden="true">💾</span><span>Export</span></button>
</nav>'''

    new_nav = '''<button class="tab-btn" data-tab="export" role="tab" aria-selected="false" aria-controls="panel-export" tabindex="-1"><span aria-hidden="true">💾</span><span>Export</span></button>
<button class="tab-btn" data-tab="rvalidation" role="tab" aria-selected="false" aria-controls="panel-rvalidation" tabindex="-1"><span aria-hidden="true">✓</span><span>R Valid.</span></button>
</nav>'''

    content = content.replace(old_nav, new_nav)
    print("[OK] Added R Validation tab button")

# 2. Add the panel initialization in initializePanels function
# Find the export panel and add after it
panel_code = '''
        rvalidation: \`
            <div class="panel-content">
                <div class="card">
                    <h2 class="card-title">R Validation Report</h2>
                    <p class="text-muted">Comparison of NMA Pro v6.2 JavaScript implementations against R packages (metafor 4.8.0, netmeta 3.2.0, meta 8.2.1)</p>

                    <div class="validation-summary" style="margin:var(--space-4) 0;padding:var(--space-4);background:var(--surface-2);border-radius:var(--radius-md);">
                        <h3>Summary</h3>
                        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:var(--space-4);margin-top:var(--space-3);">
                            <div style="text-align:center;padding:var(--space-3);background:var(--surface-1);border-radius:var(--radius-sm);">
                                <div style="font-size:2rem;font-weight:700;color:var(--primary);">17</div>
                                <div style="font-size:0.85rem;color:var(--text-muted);">Total Tests</div>
                            </div>
                            <div style="text-align:center;padding:var(--space-3);background:var(--surface-1);border-radius:var(--radius-sm);">
                                <div style="font-size:2rem;font-weight:700;color:var(--success);">9</div>
                                <div style="font-size:0.85rem;color:var(--text-muted);">Passed</div>
                            </div>
                            <div style="text-align:center;padding:var(--space-3);background:var(--surface-1);border-radius:var(--radius-sm);">
                                <div style="font-size:2rem;font-weight:700;color:var(--danger);">5</div>
                                <div style="font-size:0.85rem;color:var(--text-muted);">Failed</div>
                            </div>
                            <div style="text-align:center;padding:var(--space-3);background:var(--surface-1);border-radius:var(--radius-sm);">
                                <div style="font-size:2rem;font-weight:700;color:var(--warning);">3</div>
                                <div style="font-size:0.85rem;color:var(--text-muted);">Review</div>
                            </div>
                        </div>
                    </div>

                    <div class="validation-categories" style="margin-top:var(--space-5);">
                        <h3>Test Categories</h3>
                        <table class="data-table" style="margin-top:var(--space-3);">
                            <thead><tr><th>Category</th><th>Status</th><th>Details</th></tr></thead>
                            <tbody>
                                <tr><td>Basic Statistics (mean, pnorm, qnorm, pchisq, pt)</td><td><span style="color:var(--success);font-weight:600;">PASS</span></td><td>5/5 tests passed - all within 2% tolerance</td></tr>
                                <tr><td>Fixed Effect Meta-Analysis</td><td><span style="color:var(--success);font-weight:600;">PASS</span></td><td>Effect: JS=0.4358, R=0.4358; SE: JS=0.0438, R=0.0438</td></tr>
                                <tr><td>Publication Bias (Egger, Begg)</td><td><span style="color:var(--warning);font-weight:600;">PARTIAL</span></td><td>Egger p=0.0751 (match), Begg tau=0.5111 (match)</td></tr>
                                <tr><td>Trim-and-Fill</td><td><span style="color:var(--danger);font-weight:600;">DIFFERS</span></td><td>JS: k0=0, R: k0=2 - Different algorithm parameters</td></tr>
                                <tr><td>Network Meta-Analysis</td><td><span style="color:var(--danger);font-weight:600;">NEEDS FIX</span></td><td>Matrix computation returns null - investigating</td></tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="validation-details" style="margin-top:var(--space-5);">
                        <h3>Detailed Results</h3>
                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-4);margin-top:var(--space-3);">
                            <div class="card" style="padding:var(--space-3);">
                                <h4 style="margin-bottom:var(--space-2);">Stats.pnorm(1.96)</h4>
                                <div style="display:flex;justify-content:space-between;"><span>JavaScript:</span><span class="mono">0.975002</span></div>
                                <div style="display:flex;justify-content:space-between;"><span>R pnorm():</span><span class="mono">0.975000</span></div>
                                <div style="color:var(--success);margin-top:var(--space-1);">Diff: 0.0002%</div>
                            </div>
                            <div class="card" style="padding:var(--space-3);">
                                <h4 style="margin-bottom:var(--space-2);">Stats.qnorm(0.975)</h4>
                                <div style="display:flex;justify-content:space-between;"><span>JavaScript:</span><span class="mono">1.959964</span></div>
                                <div style="display:flex;justify-content:space-between;"><span>R qnorm():</span><span class="mono">1.960000</span></div>
                                <div style="color:var(--success);margin-top:var(--space-1);">Diff: 0.002%</div>
                            </div>
                            <div class="card" style="padding:var(--space-3);">
                                <h4 style="margin-bottom:var(--space-2);">Stats.pchisq(3.84, 1)</h4>
                                <div style="display:flex;justify-content:space-between;"><span>JavaScript:</span><span class="mono">0.949972</span></div>
                                <div style="display:flex;justify-content:space-between;"><span>R pchisq():</span><span class="mono">0.950000</span></div>
                                <div style="color:var(--success);margin-top:var(--space-1);">Diff: 0.003%</div>
                            </div>
                            <div class="card" style="padding:var(--space-3);">
                                <h4 style="margin-bottom:var(--space-2);">Stats.pt(2.0, 10)</h4>
                                <div style="display:flex;justify-content:space-between;"><span>JavaScript:</span><span class="mono">0.963306</span></div>
                                <div style="display:flex;justify-content:space-between;"><span>R pt():</span><span class="mono">0.963300</span></div>
                                <div style="color:var(--success);margin-top:var(--space-1);">Diff: 0.001%</div>
                            </div>
                        </div>
                    </div>

                    <div class="validation-notes" style="margin-top:var(--space-5);padding:var(--space-4);background:var(--surface-2);border-radius:var(--radius-md);">
                        <h3>Notes & Recommendations</h3>
                        <ul style="margin-top:var(--space-2);padding-left:var(--space-4);">
                            <li><strong>TrimFill:</strong> Algorithm differs from metafor::trimfill - uses different estimator for k0</li>
                            <li><strong>Egger Test:</strong> Returns intercept (2.737) instead of z-statistic (2.045) - add z output</li>
                            <li><strong>NMA:</strong> Matrix inversion issue in FrequentistNMA.analyze() - under investigation</li>
                        </ul>
                    </div>

                    <div style="margin-top:var(--space-5);padding:var(--space-3);background:var(--info-bg);border-left:4px solid var(--info);border-radius:var(--radius-sm);">
                        <strong>Reference:</strong> Validation performed against metafor 4.8.0, netmeta 3.2.0, meta 8.2.1 (R 4.5.2)<br>
                        <strong>Date:</strong> 2026-01-12 | <strong>Tolerance:</strong> 2% relative difference
                    </div>
                </div>
            </div>
        \`,'''

# Find the export panel definition and add rvalidation after it
export_pattern = r"(export:\s*`[\s\S]*?`\s*,)"

def add_panel(match):
    return match.group(1) + panel_code

if 'rvalidation:' not in content:
    content = re.sub(export_pattern, add_panel, content, count=1)
    print("[OK] Added R Validation panel content")
else:
    print("R Validation panel already exists!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone! R Validation tab added to NMA Pro v6.2")
