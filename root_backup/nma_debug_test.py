# Debug test to check browser console for errors
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

try:
    driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v7.0-optimized.html")
    time.sleep(3)

    # Check console logs
    logs = driver.get_log('browser')
    print("="*60)
    print("BROWSER CONSOLE LOGS:")
    print("="*60)
    for log in logs:
        print(f"[{log['level']}] {log['message'][:200]}")

    # Load demo
    print("\n\nLoading demo data...")
    driver.find_element(By.ID, "loadDemoBtn").click()
    time.sleep(1)

    # Run analysis
    print("Running analysis...")
    driver.find_element(By.ID, "runAnalysisBtn").click()
    time.sleep(10)

    # Check console again
    logs = driver.get_log('browser')
    print("\n" + "="*60)
    print("CONSOLE AFTER ANALYSIS:")
    print("="*60)
    for log in logs:
        print(f"[{log['level']}] {log['message'][:200]}")

    # Check if results visible
    print("\n\nChecking results...")
    try:
        forest = driver.find_element(By.ID, "forestPlot")
        print(f"Forest plot content length: {len(forest.get_attribute('innerHTML'))}")
    except Exception as e:
        print(f"Forest plot error: {e}")

    # Check ranking table
    try:
        ranking = driver.find_element(By.ID, "rankingTableBody")
        rows = ranking.find_elements(By.TAG_NAME, "tr")
        print(f"Ranking table rows: {len(rows)}")
    except Exception as e:
        print(f"Ranking error: {e}")

    # Take screenshot
    driver.save_screenshot("C:/Users/user/nma_debug_screenshot.png")
    print("\nScreenshot saved to nma_debug_screenshot.png")

    time.sleep(5)

finally:
    driver.quit()
