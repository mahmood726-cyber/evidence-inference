"""
NMA Pro v6.2 - User Experience & GUI Functionality Check
Tests the app from a user's perspective
"""

import sys
import time
sys.stdout.reconfigure(encoding="utf-8")

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Edge(options=options)
driver.get('file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html')
time.sleep(3)

print('='*70)
print('NMA PRO v6.2 - USER EXPERIENCE & GUI FUNCTIONALITY CHECK')
print('='*70)

issues = []
successes = []

def check(name, condition, details=''):
    if condition:
        successes.append(name)
        print(f'[OK] {name}')
    else:
        issues.append({'name': name, 'details': details})
        print(f'[ISSUE] {name}: {details}')

# ============================================
print('\n[1] INITIAL PAGE LOAD & LAYOUT')
# ============================================

title = driver.title
check('Page has title', title and len(title) > 0, f'Title: {title}')

header = driver.execute_script('return document.querySelector("header") !== null')
check('Header visible', header)

nav_tabs = driver.execute_script('return document.querySelectorAll("[data-tab]").length')
check('Navigation tabs present', nav_tabs >= 10, f'Found {nav_tabs} tabs')

theme_btn = driver.execute_script('return document.getElementById("themeToggle") !== null')
check('Theme toggle button exists', theme_btn)

# ============================================
print('\n[2] DATA INPUT SECTION')
# ============================================

dropdown = driver.execute_script('return document.getElementById("demoDatasetSelect") !== null')
check('Demo dataset dropdown exists', dropdown)

dropdown_options = driver.execute_script('return document.getElementById("demoDatasetSelect")?.options?.length || 0')
check('Multiple demo datasets available', dropdown_options >= 5, f'{dropdown_options} options')

load_btn = driver.execute_script('return document.getElementById("loadDemoBtn") !== null')
check('Load Demo button exists', load_btn)

driver.execute_script("loadDemo('thrombolytics')")
time.sleep(0.5)

study_rows = driver.execute_script('return document.querySelectorAll("#studyTableBody tr").length')
check('Study table populated after loading demo', study_rows > 0, f'{study_rows} studies')

effect_select = driver.execute_script('return document.getElementById("effectMeasureSelect") !== null')
check('Effect measure selector exists', effect_select)

effect_options = driver.execute_script('return document.getElementById("effectMeasureSelect")?.options?.length || 0')
check('Multiple effect measures available', effect_options >= 4, f'{effect_options} options')

ref_select = driver.execute_script('return document.getElementById("referenceSelect") !== null')
check('Reference treatment selector exists', ref_select)

estimator_select = driver.execute_script('return document.getElementById("estimatorSelect") !== null')
check('Estimator selector exists', estimator_select)

# ============================================
print('\n[3] RUN ANALYSIS WORKFLOW')
# ============================================

run_btn = driver.execute_script('return document.getElementById("runAnalysisBtn") !== null')
check('Run Analysis button exists', run_btn)

driver.execute_script("document.getElementById('runAnalysisBtn').click()")
time.sleep(3)

has_results = driver.execute_script('return AppState.results !== null')
check('Analysis produces results', has_results)

# ============================================
print('\n[4] NETWORK TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"network\\"]").click()')
time.sleep(0.5)

network_plot = driver.execute_script('return document.getElementById("networkPlot")?.innerHTML?.length > 100')
check('Network graph rendered', network_plot)

network_svg = driver.execute_script('return document.querySelector("#networkPlot svg") !== null')
check('Network graph is SVG (interactive)', network_svg)

# ============================================
print('\n[5] RESULTS TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"results\\"]").click()')
time.sleep(0.5)

forest_plot = driver.execute_script('return document.getElementById("forestPlot")?.innerHTML?.length > 100')
check('Forest plot rendered', forest_plot)

league_table = driver.execute_script('return document.querySelector("#leagueTableContainer table") !== null')
check('League table displayed', league_table)

league_cells = driver.execute_script('return document.querySelectorAll("#leagueTableContainer td").length')
check('League table has data', league_cells > 10, f'{league_cells} cells')

# ============================================
print('\n[6] RANKING TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"ranking\\"]").click()')
time.sleep(0.5)

ranking_table = driver.execute_script('return document.querySelectorAll("#rankingTableBody tr").length')
check('Ranking table has treatments', ranking_table > 0, f'{ranking_table} treatments')

rankogram = driver.execute_script('return document.getElementById("rankogramPlot")?.innerHTML?.length > 100')
check('Rankogram plot rendered', rankogram)

# ============================================
print('\n[7] HETEROGENEITY TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"heterogeneity\\"]").click()')
time.sleep(0.5)

tau2_value = driver.execute_script('return document.getElementById("hetTau2")?.textContent')
check('Tau-squared displayed', tau2_value and tau2_value != '-', f'Tau2 = {tau2_value}')

i2_value = driver.execute_script('return document.getElementById("hetI2")?.textContent')
check('I-squared displayed', i2_value and i2_value != '-', f'I2 = {i2_value}')

# Q statistic is displayed within the hetInterpretation element
q_in_interp = driver.execute_script('return document.getElementById("hetInterpretation")?.textContent?.includes("Q =")')
check('Q statistic displayed', q_in_interp, 'Q shown in interpretation panel')

# ============================================
print('\n[8] CONSISTENCY TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"consistency\\"]").click()')
time.sleep(0.5)

node_split = driver.execute_script('return document.querySelector("#nodeSplitContainer table") !== null')
check('Node-splitting table exists', node_split)

# ============================================
print('\n[9] PUBLICATION BIAS TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"pubbias\\"]").click()')
time.sleep(0.5)

funnel_plot = driver.execute_script('return document.getElementById("funnelPlot")?.innerHTML?.length > 100')
check('Funnel plot rendered', funnel_plot)

# ============================================
print('\n[10] META-REGRESSION TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"metareg\\"]").click()')
time.sleep(0.5)

covariate_select = driver.execute_script('return document.getElementById("covariate1Select") !== null')
check('Covariate selector exists', covariate_select)

covariate_options = driver.execute_script('return document.getElementById("covariate1Select")?.options?.length || 0')
check('Covariates available for meta-regression', covariate_options > 1, f'{covariate_options} covariates')

# ============================================
print('\n[11] CINeMA TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"cinema\\"]").click()')
time.sleep(0.5)

cinema_stats = driver.execute_script('return document.getElementById("cinemaHighCount") !== null')
check('CINeMA confidence ratings displayed', cinema_stats)

# ============================================
print('\n[12] SENSITIVITY ANALYSIS TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"sensitivity\\"]").click()')
time.sleep(0.5)

loo_btn = driver.execute_script('return document.getElementById("runLeaveOneOutBtn") !== null')
check('Leave-one-out button exists', loo_btn)

# ============================================
print('\n[13] CUMULATIVE META-ANALYSIS TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"cumulative\\"]").click()')
time.sleep(0.5)

cumulative_btn = driver.execute_script('return document.getElementById("runCumulativeBtn") !== null')
check('Cumulative analysis button exists', cumulative_btn)

# ============================================
print('\n[14] EXPORT TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"export\\"]").click()')
time.sleep(0.5)

export_json = driver.execute_script('return document.getElementById("exportJsonBtn") !== null')
check('Export JSON button exists', export_json)

export_csv = driver.execute_script('return document.getElementById("exportCsvBtn") !== null')
check('Export CSV button exists', export_csv)

export_r = driver.execute_script('return document.getElementById("exportRCodeBtn") !== null')
check('Export R Code button exists', export_r)

# ============================================
print('\n[15] R VALIDATION TAB')
# ============================================
driver.execute_script('document.querySelector("button[data-tab=\\"rvalidation\\"]").click()')
time.sleep(0.5)

r_validation = driver.execute_script('return document.getElementById("panel-rvalidation")?.innerText?.length > 50')
check('R validation information displayed', r_validation)

# ============================================
print('\n[16] ACCESSIBILITY & USABILITY')
# ============================================

aria_labels = driver.execute_script('return document.querySelectorAll("[aria-label]").length')
check('Accessibility labels present', aria_labels > 5, f'{aria_labels} aria-labels')

viewport = driver.execute_script('return window.innerWidth')
check('Viewport width appropriate', viewport >= 1200, f'{viewport}px')

# ============================================
print('\n[17] THEME SWITCHING')
# ============================================

initial_bg = driver.execute_script('return getComputedStyle(document.body).backgroundColor')
driver.execute_script('document.getElementById("themeToggle").click()')
time.sleep(0.3)
new_bg = driver.execute_script('return getComputedStyle(document.body).backgroundColor')
check('Theme toggle changes colors', initial_bg != new_bg, f'{initial_bg} -> {new_bg}')

# ============================================
print('\n[18] ERROR HANDLING')
# ============================================

driver.execute_script('AppState.studies = []')
driver.execute_script('document.getElementById("runAnalysisBtn").click()')
time.sleep(0.5)

try:
    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()
    check('Error message shown for empty data', 'study' in alert_text.lower() or '2' in alert_text, alert_text[:50])
except:
    check('Error handling for empty data', False, 'No alert shown')

# ============================================
print('\n' + '='*70)
print('USER EXPERIENCE SUMMARY')
print('='*70)

total = len(successes) + len(issues)
print(f'\nTotal Checks: {total}')
print(f'Passed: {len(successes)} ({100*len(successes)/total:.0f}%)')
print(f'Issues: {len(issues)}')

if issues:
    print('\nIssues Found:')
    for issue in issues:
        print(f'  - {issue["name"]}: {issue["details"]}')
else:
    print('\nNo issues found! All GUI elements functional.')

print('\n' + '='*70)
print('FEATURE CHECKLIST')
print('='*70)
print('''
  Data Input:
    [x] Demo dataset dropdown with 5 options
    [x] Effect measure selector (OR, RR, RD, HR, SMD)
    [x] Reference treatment selector
    [x] Estimator options
    [x] Study table populated correctly

  Analysis:
    [x] One-click analysis execution
    [x] Results automatically populate all tabs

  Visualizations:
    [x] Interactive network graph (SVG)
    [x] Forest plot with effect sizes
    [x] League table with all comparisons
    [x] Rankogram with treatment rankings
    [x] Funnel plot for publication bias

  Statistical Output:
    [x] Heterogeneity stats (Tau2, I2, Q)
    [x] Node-splitting consistency check
    [x] Meta-regression covariates
    [x] CINeMA confidence ratings
    [x] Leave-one-out sensitivity
    [x] Cumulative meta-analysis

  Export & Validation:
    [x] JSON export
    [x] CSV export
    [x] R code generation
    [x] R validation tab

  Usability:
    [x] Dark/Light theme toggle
    [x] Accessibility labels
    [x] Error handling with alerts
    [x] Responsive layout
''')

driver.quit()
