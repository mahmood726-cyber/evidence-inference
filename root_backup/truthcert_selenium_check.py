import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

file_path = r"C:\Truthcert1\TruthCert-PairwisePro-v1.0-bundle.html"
file_url = Path(file_path).as_uri()

options = webdriver.EdgeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1400,900")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 45)

report = {
    "clicked": [],
    "errors": [],
    "plots": [],
    "console": [],
    "events": [],
    "analysis": {"run": False, "full_run": False},
}

try:
    driver.get(file_url)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    driver.execute_script(
        """
        window.__seleniumEvents = [];
        window.alert = (msg) => {
          console.log("ALERT:" + msg);
          window.__seleniumEvents.push({type: "alert", msg: String(msg)});
        };
        window.confirm = (msg) => {
          console.log("CONFIRM:" + msg);
          window.__seleniumEvents.push({type: "confirm", msg: String(msg)});
          return false;
        };
        window.prompt = (msg, defVal) => {
          console.log("PROMPT:" + msg);
          window.__seleniumEvents.push({type: "prompt", msg: String(msg)});
          return "1";
        };
        """
    )

    def dismiss_overlays():
        driver.execute_script(
            """
            const ids = ["quickStartModal", "keyboardShortcutsModal", "forestSettingsPanel", "funnelSettingsPanel"];
            ids.forEach(id => {
              const el = document.getElementById(id);
              if (!el) return;
              el.classList.remove("active");
              el.classList.add("hidden");
            });
            document.querySelectorAll('.quick-start-modal, .modal, .overlay').forEach(el => {
              el.classList.remove('active');
              el.classList.add('hidden');
            });
            """
        )

    dismiss_overlays()

    def ensure_demo_loaded():
        driver.execute_script("if (window.loadDemoDataset) loadDemoDataset('BCG');")
        wait.until(lambda d: d.execute_script("return window.AppState && AppState.studies && AppState.studies.length > 0"))

    def run_analysis():
        dismiss_overlays()
        driver.execute_script("document.getElementById('runAnalysisBtn')?.click();")
        wait.until(lambda d: d.execute_script("return window.AppState && AppState.results && AppState.results.pooled"))
        report["analysis"]["run"] = True

    def run_full_analysis():
        dismiss_overlays()
        driver.execute_script("if (window.runFullAnalysis) runFullAnalysis();")
        try:
            wait.until(lambda d: d.execute_script("return window.AppState && AppState.results && AppState.results.fullAnalysisComplete === true"))
            report["analysis"]["full_run"] = True
        except Exception as e:
            report["errors"].append({"step": "run_full_analysis", "error": repr(e)})

    ensure_demo_loaded()
    run_analysis()
    run_full_analysis()

    def assign_button_ids(scope_selector=None):
        return driver.execute_script(
            """
            const scope = arguments[0] ? document.querySelector(arguments[0]) : document;
            if (!scope) return [];
            window.__selBtnCounter = window.__selBtnCounter || 0;
            const btns = Array.from(scope.querySelectorAll('button'));
            return btns.map(b => {
              if (!b.dataset.selId) b.dataset.selId = String(++window.__selBtnCounter);
              const hidden = b.offsetParent === null;
              return {id: b.dataset.selId, text: (b.textContent||'').trim(), disabled: b.disabled, hidden};
            });
            """,
            scope_selector,
        )

    def safe_click(sel_id):
        try:
            el = driver.find_element(By.CSS_SELECTOR, f"button[data-sel-id='{sel_id}']")
            if not el.is_displayed() or not el.is_enabled():
                return False, "not_displayed_or_disabled"
            try:
                el.click()
            except Exception:
                driver.execute_script("arguments[0].click();", el)
            dismiss_overlays()
            return True, ""
        except Exception as e:
            return False, repr(e)

    tabs = driver.find_elements(By.CSS_SELECTOR, ".tab-btn")
    tab_names = [t.get_attribute("data-tab") for t in tabs if t.get_attribute("data-tab")]

    clicked_ids = set()

    for name in tab_names:
        try:
            driver.find_element(By.CSS_SELECTOR, f".tab-btn[data-tab='{name}']").click()
            driver.execute_script("if (window.onTabActivate) onTabActivate(arguments[0]);", name)
            time.sleep(0.5)
            btns = assign_button_ids(f"#panel-{name}")
            for b in btns:
                if b["hidden"] or b["disabled"] or b["id"] in clicked_ids:
                    continue
                ok, err = safe_click(b["id"])
                clicked_ids.add(b["id"])
                report["clicked"].append({"tab": name, "id": b["id"], "text": b["text"], "ok": ok, "error": err})
                if not ok:
                    report["errors"].append({"tab": name, "id": b["id"], "text": b["text"], "error": err})
                time.sleep(0.15)
        except Exception as e:
            report["errors"].append({"tab": name, "error": repr(e)})

    all_btns = assign_button_ids(None)
    for b in all_btns:
        if b["hidden"] or b["disabled"] or b["id"] in clicked_ids:
            continue
        ok, err = safe_click(b["id"])
        clicked_ids.add(b["id"])
        report["clicked"].append({"tab": "global", "id": b["id"], "text": b["text"], "ok": ok, "error": err})
        if not ok:
            report["errors"].append({"tab": "global", "id": b["id"], "text": b["text"], "error": err})
        time.sleep(0.15)

    plot_status = driver.execute_script(
        """
        const plotContainers = Array.from(document.querySelectorAll('.plot-container'));
        const byId = Array.from(document.querySelectorAll('div[id$="Plot"], div[id$="plot"]'));
        const unique = new Map();
        for (const el of plotContainers.concat(byId)) {
          if (!el || !el.id) continue;
          if (!unique.has(el.id)) unique.set(el.id, el);
        }
        const results = [];
        for (const [id, el] of unique.entries()) {
          const hasPlotly = !!el.querySelector('.js-plotly-plot');
          const hasSvg = !!el.querySelector('svg');
          const hasCanvas = !!el.querySelector('canvas');
          const hasChildren = el.children.length > 0;
          results.push({id, hasPlotly, hasSvg, hasCanvas, hasChildren});
        }
        return results;
        """
    )
    report["plots"] = plot_status

    report["events"] = driver.execute_script("return window.__seleniumEvents || [];")

    try:
        report["console"] = driver.get_log("browser")
    except WebDriverException:
        report["console"] = []

finally:
    try:
        driver.quit()
    except WebDriverException:
        pass

print(json.dumps(report, indent=2))
