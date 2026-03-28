"""Add UI elements for release features to TruthCert HTML"""

html_path = r'C:\Truthcert1\TruthCert-PairwisePro-v1.0-fast.html'

# Read the HTML file
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Save/Load and Undo/Redo buttons after theme toggle (before Help button)
old_theme_toggle = '''<button class="btn btn--ghost theme-toggle" id="themeToggle" title="Toggle light/dark mode" aria-label="Toggle theme">
            <span class="theme-toggle__icon theme-toggle__icon--dark">'''

new_theme_toggle = '''<!-- Save/Load Buttons -->
          <button class="btn btn--ghost btn--sm" id="saveBtn" onclick="saveProject('TruthCert_Project_' + Date.now(), true)" title="Save project (Ctrl+S to quick save)">Save</button>
          <label class="btn btn--ghost btn--sm" title="Load project file" style="cursor:pointer;">Load
            <input type="file" accept=".json,.truthcert" onchange="loadProject(this.files[0])" style="display:none;">
          </label>

          <!-- Undo/Redo Buttons -->
          <button class="btn btn--ghost btn--sm" id="undoBtn" onclick="UndoManager.undo()" title="Undo (Ctrl+Z)" disabled>Undo</button>
          <button class="btn btn--ghost btn--sm" id="redoBtn" onclick="UndoManager.redo()" title="Redo (Ctrl+Y)" disabled>Redo</button>

          <button class="btn btn--ghost theme-toggle" id="themeToggle" title="Toggle light/dark mode" aria-label="Toggle theme">
            <span class="theme-toggle__icon theme-toggle__icon--dark">'''

html = html.replace(old_theme_toggle, new_theme_toggle)

# 2. Add Quick Start button before Help button
old_help_btn = '''<button class="btn btn-ghost" onclick="openHelpSystem()" title="Help & Documentation"'''
new_help_btn = '''<button class="btn btn--outline btn--sm" onclick="showQuickStartWizard()" title="Quick Start Wizard" style="margin-right:var(--space-2);">Quick Start</button>
      <button class="btn btn-ghost" onclick="openHelpSystem()" title="Help & Documentation"'''

html = html.replace(old_help_btn, new_help_btn)

# 3. Add CSS for new features before </style>
new_css = '''
    /* Quick Start Wizard */
    .quick-start-modal {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.8);
      z-index: 1000;
      align-items: center;
      justify-content: center;
    }
    .quick-start-modal.active { display: flex; }
    .quick-start-content {
      background: var(--surface-raised);
      border-radius: var(--radius-xl);
      max-width: 600px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      padding: var(--space-6);
    }
    .quick-start-step { display: none; }
    .quick-start-step.active { display: block; }
    .quick-start-nav {
      display: flex;
      justify-content: space-between;
      margin-top: var(--space-4);
      padding-top: var(--space-4);
      border-top: 1px solid var(--border-subtle);
    }
    .quick-start-progress {
      display: flex;
      justify-content: center;
      gap: var(--space-2);
      margin-bottom: var(--space-4);
    }
    .quick-start-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--border-default);
    }
    .quick-start-dot.active { background: var(--color-accent-500); }
    .quick-start-dot.completed { background: var(--color-success-500); }

    /* Toast Notifications */
    #toast-container {
      position: fixed;
      top: 80px;
      right: 20px;
      z-index: 9999;
    }
    .toast {
      background: var(--surface-overlay);
      color: var(--text-primary);
      padding: var(--space-3) var(--space-4);
      border-radius: var(--radius-md);
      margin-bottom: var(--space-2);
      box-shadow: var(--shadow-lg);
      animation: slideIn 0.3s ease;
      min-width: 200px;
    }
    .toast.success { border-left: 4px solid var(--color-success-500); }
    .toast.error { border-left: 4px solid var(--color-danger-500); }
    .toast.info { border-left: 4px solid var(--color-info-500); }
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    /* Mobile Responsiveness Improvements */
    @media (max-width: 768px) {
      .app-header__inner {
        flex-wrap: wrap;
        gap: var(--space-2);
      }
      .app-controls {
        flex-wrap: wrap;
        justify-content: center;
        width: 100%;
      }
      .select-wrapper { min-width: 120px; }
      .btn--lg { padding: var(--space-2) var(--space-3); font-size: var(--text-sm); }
      .tab-btn { padding: var(--space-2) var(--space-2); font-size: var(--text-xs); }
      .tab-btn span:first-child { display: none; }
      .card { padding: var(--space-3); }
      .grid { grid-template-columns: 1fr !important; }
      #undoBtn, #redoBtn, #saveBtn { display: none; }
      .data-table { font-size: var(--text-xs); }
      .data-table th, .data-table td { padding: var(--space-1) var(--space-2); }
      .js-plot { min-height: 250px; }
    }

    @media (max-width: 480px) {
      .app-logo__text { display: none; }
      .app-logo__badge { font-size: var(--text-sm); padding: var(--space-1) var(--space-2); }
      .container { padding: 0 var(--space-2); }
      .tab-navigation { overflow-x: auto; -webkit-overflow-scrolling: touch; }
      .tab-navigation__list { flex-wrap: nowrap; }
    }
'''

html = html.replace('</style>', new_css + '\n  </style>')

# 4. Add Quick Start Wizard Modal and Toast Container before </body>
quick_start_html = '''
  <!-- Quick Start Wizard Modal -->
  <div id="quickStartModal" class="quick-start-modal">
    <div class="quick-start-content">
      <div class="quick-start-progress">
        <div class="quick-start-dot active" data-step="1"></div>
        <div class="quick-start-dot" data-step="2"></div>
        <div class="quick-start-dot" data-step="3"></div>
        <div class="quick-start-dot" data-step="4"></div>
      </div>

      <!-- Step 1: Welcome -->
      <div class="quick-start-step active" data-step="1">
        <h2 style="text-align:center; margin-bottom: var(--space-4);">Welcome to TruthCert-PairwisePro</h2>
        <p style="margin-bottom: var(--space-4);">This wizard will help you get started with your first meta-analysis in 4 easy steps.</p>
        <div style="background: var(--surface-highlight); padding: var(--space-4); border-radius: var(--radius-lg);">
          <h4>What you will learn:</h4>
          <ul style="margin-top: var(--space-2); padding-left: var(--space-4);">
            <li>How to enter or load study data</li>
            <li>How to run a meta-analysis</li>
            <li>How to interpret the TruthCert verdict</li>
            <li>How to use advanced features</li>
          </ul>
        </div>
      </div>

      <!-- Step 2: Data Input -->
      <div class="quick-start-step" data-step="2">
        <h2 style="text-align:center; margin-bottom: var(--space-4);">Step 1: Enter Your Data</h2>
        <p style="margin-bottom: var(--space-4);">You can enter data manually or load a demo dataset to see how it works.</p>
        <div style="display: grid; gap: var(--space-3);">
          <div style="background: var(--surface-highlight); padding: var(--space-3); border-radius: var(--radius-md);">
            <strong>Option A: Manual Entry</strong>
            <p style="font-size: var(--text-sm); margin-top: var(--space-1);">Click "Add Row" in the Data tab and enter study details (events, totals).</p>
          </div>
          <div style="background: var(--surface-highlight); padding: var(--space-3); border-radius: var(--radius-md);">
            <strong>Option B: Demo Dataset</strong>
            <p style="font-size: var(--text-sm); margin-top: var(--space-1);">Click "Demo" dropdown and select BCG Vaccine or another dataset.</p>
          </div>
          <div style="background: var(--surface-highlight); padding: var(--space-3); border-radius: var(--radius-md);">
            <strong>Option C: Import File</strong>
            <p style="font-size: var(--text-sm); margin-top: var(--space-1);">Use Import CSV/Excel to load your own data file.</p>
          </div>
        </div>
        <button class="btn btn--accent" onclick="loadDemoDataset('BCG'); nextQuickStartStep();" style="margin-top: var(--space-4); width: 100%;">Load BCG Demo Dataset</button>
      </div>

      <!-- Step 3: Run Analysis -->
      <div class="quick-start-step" data-step="3">
        <h2 style="text-align:center; margin-bottom: var(--space-4);">Step 2: Run Analysis</h2>
        <p style="margin-bottom: var(--space-4);">Once your data is loaded, click the Run Analysis button.</p>
        <div style="background: var(--surface-highlight); padding: var(--space-4); border-radius: var(--radius-lg);">
          <h4>The analysis will compute:</h4>
          <ul style="margin-top: var(--space-2); padding-left: var(--space-4);">
            <li><strong>Pooled Effect:</strong> Combined treatment effect across studies</li>
            <li><strong>Heterogeneity:</strong> I-squared and tau-squared statistics</li>
            <li><strong>Forest Plot:</strong> Visual display of all studies</li>
            <li><strong>Publication Bias:</strong> Egger test and funnel plot</li>
            <li><strong>TruthCert Verdict:</strong> Evidence quality assessment</li>
          </ul>
        </div>
        <button class="btn btn--accent" onclick="runAnalysis(); setTimeout(nextQuickStartStep, 1500);" style="margin-top: var(--space-4); width: 100%;">Run Analysis Now</button>
      </div>

      <!-- Step 4: Interpret Results -->
      <div class="quick-start-step" data-step="4">
        <h2 style="text-align:center; margin-bottom: var(--space-4);">Step 3: Interpret Results</h2>
        <p style="margin-bottom: var(--space-4);">Navigate through the tabs to explore your results.</p>
        <div style="display: grid; gap: var(--space-2);">
          <div style="padding: var(--space-2); border-left: 3px solid var(--color-success-500);">
            <strong>Analysis Tab:</strong> Forest and funnel plots, pooled effect</div>
          <div style="padding: var(--space-2); border-left: 3px solid var(--color-info-500);">
            <strong>DDMA Tab:</strong> Bayesian analysis with posterior probability</div>
          <div style="padding: var(--space-2); border-left: 3px solid var(--color-warning-500);">
            <strong>Bias Tab:</strong> Publication bias assessment</div>
          <div style="padding: var(--space-2); border-left: 3px solid var(--color-accent-500);">
            <strong>Verdict Tab:</strong> TruthCert evidence quality certification</div>
          <div style="padding: var(--space-2); border-left: 3px solid var(--color-purple);">
            <strong>HTA Tab:</strong> Cost-effectiveness analysis (enter costs first)</div>
        </div>
        <button class="btn btn--accent" onclick="closeQuickStartWizard(); goToTab('verdict');" style="margin-top: var(--space-4); width: 100%;">Finish and View Verdict</button>
      </div>

      <div class="quick-start-nav">
        <button class="btn btn--ghost" onclick="prevQuickStartStep()">Back</button>
        <button class="btn btn--ghost" onclick="closeQuickStartWizard()">Skip Tutorial</button>
        <button class="btn btn--primary" onclick="nextQuickStartStep()">Next</button>
      </div>
    </div>
  </div>

  <!-- Toast Container -->
  <div id="toast-container"></div>

<script>
// Quick Start Wizard Functions
let currentQuickStartStep = 1;
const totalQuickStartSteps = 4;

function showQuickStartWizard() {
  currentQuickStartStep = 1;
  updateQuickStartUI();
  document.getElementById('quickStartModal').classList.add('active');
}

function closeQuickStartWizard() {
  document.getElementById('quickStartModal').classList.remove('active');
}

function nextQuickStartStep() {
  if (currentQuickStartStep < totalQuickStartSteps) {
    currentQuickStartStep++;
    updateQuickStartUI();
  }
}

function prevQuickStartStep() {
  if (currentQuickStartStep > 1) {
    currentQuickStartStep--;
    updateQuickStartUI();
  }
}

function updateQuickStartUI() {
  document.querySelectorAll('.quick-start-step').forEach((step, idx) => {
    step.classList.toggle('active', idx + 1 === currentQuickStartStep);
  });
  document.querySelectorAll('.quick-start-dot').forEach((dot, idx) => {
    dot.classList.remove('active', 'completed');
    if (idx + 1 === currentQuickStartStep) {
      dot.classList.add('active');
    } else if (idx + 1 < currentQuickStartStep) {
      dot.classList.add('completed');
    }
  });
}

function showToast(message, type) {
  type = type || 'info';
  var container = document.getElementById('toast-container');
  if (!container) return;
  var toast = document.createElement('div');
  toast.className = 'toast ' + type;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(function() {
    toast.style.opacity = '0';
    setTimeout(function() { toast.remove(); }, 300);
  }, 3000);
}

// Check for autosave on load
document.addEventListener('DOMContentLoaded', function() {
  if (typeof checkAutosave === 'function') {
    var autosave = checkAutosave();
    if (autosave && autosave.available) {
      var age = Math.round(autosave.age);
      if (confirm('Found autosaved project from ' + age + ' minutes ago. Load it?')) {
        loadAutosave();
      }
    }
  }

  // Initialize UndoManager
  if (typeof UndoManager !== 'undefined') {
    UndoManager.saveState('Initial state');
  }

  // Show quick start for first-time users
  if (!localStorage.getItem('truthcert_visited')) {
    localStorage.setItem('truthcert_visited', 'true');
    setTimeout(showQuickStartWizard, 1000);
  }
});

// Close modal on escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeQuickStartWizard();
  }
});

// Close modal on background click
document.getElementById('quickStartModal').addEventListener('click', function(e) {
  if (e.target === this) {
    closeQuickStartWizard();
  }
});
</script>
'''

html = html.replace('</body>', quick_start_html + '\n</body>')

# Write updated HTML
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("UI elements added successfully!")
print("- Save/Load buttons")
print("- Undo/Redo buttons")
print("- Quick Start wizard")
print("- Toast notifications")
print("- Mobile responsive CSS")
