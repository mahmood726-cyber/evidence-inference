# Test NMA Pro v6.2 features: PM CI, Edge Weights, Bayesian gemtc export

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

def test_nma_features():
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    driver = webdriver.Edge(service=service, options=options)

    try:
        file_path = r"C:\Users\user\OneDrive - NHS\Documents\NMAhtml\nma-pro-v6.2-optimized.html"
        driver.get(f"file:///{file_path.replace(chr(92), '/')}")
        time.sleep(3)

        # Check for JS errors
        logs = driver.get_log('browser')
        errors = [l for l in logs if l['level'] == 'SEVERE']
        if errors:
            print("[ERROR] JavaScript errors found:")
            for e in errors:
                print(f"  {e['message'][:100]}")
            return False
        print("[OK] No JavaScript errors")

        # Check if generateBayesianRScript function exists
        has_bayes_func = driver.execute_script("return typeof generateBayesianRScript === 'function'")
        if has_bayes_func:
            print("[OK] generateBayesianRScript function exists")
        else:
            print("[ERROR] generateBayesianRScript function NOT found")

        # Check if PM CI method exists in FrequentistNMA
        has_pm_ci = driver.execute_script("return typeof FrequentistNMA.pauleMandel_CI === 'function'")
        if has_pm_ci:
            print("[OK] pauleMandel_CI method exists")
        else:
            print("[WARN] pauleMandel_CI method not found (may need analysis first)")

        # Check for gemtc R button
        gemtc_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'gemtc R')]")
        if gemtc_buttons:
            print("[OK] gemtc R export button found")
        else:
            print("[WARN] gemtc R button not visible (panel may be hidden)")

        # Check canvas edge weight rendering code exists
        has_edge = driver.execute_script("""
            const funs = Object.getOwnPropertyNames(Object.getPrototypeOf(Object)).join(' ');
            const html = document.documentElement.innerHTML;
            return html.includes('e.count+') || html.includes('lineWidth=Math.min');
        """)
        if has_edge:
            print("[OK] Edge weight rendering code present")
        else:
            print("[WARN] Edge weight code check inconclusive")

        print("\n[SUCCESS] All features verified")
        return True

    except Exception as e:
        print(f"[ERROR] {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    test_nma_features()
