
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

print("="*70)
print("NMA PRO v6.2 - FULL SELENIUM TEST")
print("="*70)

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Edge(options=options)
driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html")
time.sleep(3)

passed, failed = [], []

def test(name, cond):
    if cond:
        passed.append(name)
        print(f"  [OK] {name}")
    else:
        failed.append(name)
        print(f"  [FAIL] {name}")

def js(s):
    try: return driver.execute_script(s)
    except: return None

print("\n[SETUP] Loading data...")
js("loadSampleData()")
time.sleep(1)
js("runAnalysis()")
time.sleep(2)

test("Data loaded", js("return AppState.studies&&AppState.studies.length>0"))
test("Analysis complete", js("return AppState.results\!==null"))

print("\n[TABS] Testing all 16 tabs...")
tabs=["network","results","rankings","heterogeneity","consistency","bayesian","bias","regression","cnma","cstream","cinema","grade","sensitivity","cumulative","dose","export"]
for t in tabs:
    js(f"switchTab(\"{t}\")")
    time.sleep(0.3)
    test(f"Tab {t}", js(f"return document.getElementById(\"{t}\")\!==null"))

print("\n[PLOTS] Testing visualizations...")
js("switchTab(\"network\")")
time.sleep(0.5)
test("Network canvas", js("return document.querySelector(\"#networkPlot canvas\")\!==null"))

js("switchTab(\"results\")")
time.sleep(0.5)
test("Forest plot", js("return document.getElementById(\"forestPlot\")?.innerHTML.length>50"))

js("switchTab(\"rankings\")")
time.sleep(0.5)
test("Rankogram canvas", js("return document.querySelector(\"#rankogramPlot canvas\")\!==null"))
test("Ranking table rows", js("return document.querySelectorAll(\"#rankingTable tr\").length>1"))

js("switchTab(\"bias\")")
time.sleep(0.5)
test("Funnel plot", js("return document.getElementById(\"funnelPlot\")\!==null"))

js("switchTab(\"cumulative\")")
time.sleep(0.5)
test("Cumulative plot", js("return document.getElementById(\"cumulativePlot\")\!==null"))

print("\n[METHODS] Testing advanced NMA methods...")
test("FPNMA", js("return typeof FPNMA\!==\"undefined\""))
test("MLSNMA", js("return typeof MLSNMA\!==\"undefined\""))
test("FPNMA_FractionalPolynomial", js("return typeof FPNMA_FractionalPolynomial\!==\"undefined\""))
test("MLNMR", js("return typeof MLNMR\!==\"undefined\""))
test("PROSPERO", js("return typeof PROSPERO\!==\"undefined\""))

test("FPNMA runs", js("try{return FPNMA.analyze(AppState.studies,{reference:AppState.reference}).applicable\!==false}catch(e){return false}"))
test("MLSNMA runs", js("try{return MLSNMA.analyze(AppState.studies,{reference:AppState.reference}).applicable\!==false}catch(e){return false}"))
test("MLNMR runs", js("try{return MLNMR.analyze(AppState.studies,{reference:AppState.reference})\!==null}catch(e){return false}"))
test("Bayesian runs", js("try{r=BayesianNMA.analyze(AppState.studies,{reference:AppState.reference,nIter:200,burnin:50});return r.samples.tau2.length>0}catch(e){return false}"))

print("\n[ERRORS] Checking console...")
errors=[e for e in driver.get_log("browser") if e["level"]=="SEVERE"]
test("No JS errors", len(errors)==0)

driver.quit()

print("\n"+"="*70)
total=len(passed)+len(failed)
rate=len(passed)/total*100 if total else 0
print(f"PASSED: {len(passed)} | FAILED: {len(failed)}")
print(f"PASS RATE: {rate:.1f}%% ({len(passed)}/{total})")
if failed:
    print("Failed:", failed)
print("="*70)
