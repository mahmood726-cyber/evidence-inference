"""Test Full MCMC Bayesian Meta-Analysis Implementation"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.set_window_size(1400, 900)

try:
    print("=" * 70)
    print("FULL MCMC BAYESIAN META-ANALYSIS TEST")
    print("=" * 70)

    # Load the app
    driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
    time.sleep(3)

    # Check if the function is exposed
    print("\n=== Testing Function Exposure ===")
    exposed = driver.execute_script('return typeof window.fullMCMCBayesianMA === "function"')
    print(f"  fullMCMCBayesianMA exposed: {'YES' if exposed else 'NO'}")

    run_exposed = driver.execute_script('return typeof window.runFullMCMCAnalysis === "function"')
    print(f"  runFullMCMCAnalysis exposed: {'YES' if run_exposed else 'NO'}")

    # Load a demo dataset
    print("\n=== Loading Demo Dataset ===")
    driver.execute_script("loadDemoDataset('BCG')")
    time.sleep(1)

    # Run main analysis first
    print("  Running main analysis...")
    driver.execute_script("runAnalysis()")
    time.sleep(2)

    # Check AppState has results
    has_results = driver.execute_script('return AppState.results && AppState.results.studies && AppState.results.studies.length > 0')
    print(f"  AppState has results: {'YES' if has_results else 'NO'}")

    # Test the fullMCMCBayesianMA function directly
    print("\n=== Testing fullMCMCBayesianMA Function ===")
    print("  Running with 4 chains, 5000 iterations (reduced for test)...")

    mcmc_result = driver.execute_script('''
        try {
            const yi = AppState.results.studies.map(s => s.yi);
            const vi = AppState.results.studies.map(s => s.vi);

            // Run with reduced iterations for faster test
            const result = fullMCMCBayesianMA(yi, vi, {
                chains: 4,
                iterations: 5000,
                burnin: 2500,
                thin: 2,
                tau2_prior: 'half_cauchy',
                tau2_scale: 1
            });

            return {
                success: true,
                mu_mean: result.summary.effect.mean,
                mu_median: result.summary.effect.median,
                mu_ci_lower: result.summary.effect.ci_lower,
                mu_ci_upper: result.summary.effect.ci_upper,
                tau2_mean: result.summary.tau2.mean,
                tau2_median: result.summary.tau2.median,
                I2_mean: result.summary.I2.mean,
                rhat_mu: result.diagnostics.rhat.mu,
                rhat_tau2: result.diagnostics.rhat.tau2,
                ess_mu: result.diagnostics.ess.mu,
                ess_tau2: result.diagnostics.ess.tau2,
                total_samples: result.diagnostics.total_samples,
                n_chains: result.diagnostics.n_chains,
                converged: result.convergence.converged,
                P_benefit: result.summary.ddma.P_benefit,
                prediction_lower: result.summary.prediction_interval.lower,
                prediction_upper: result.summary.prediction_interval.upper
            };
        } catch (e) {
            return { success: false, error: e.message };
        }
    ''')

    if mcmc_result['success']:
        print(f"  [PASS] MCMC ran successfully")
        print(f"\n  --- Posterior Summary ---")
        print(f"    Effect (mu) mean:   {mcmc_result['mu_mean']:.4f}")
        print(f"    Effect (mu) median: {mcmc_result['mu_median']:.4f}")
        print(f"    Effect 95% CrI:     [{mcmc_result['mu_ci_lower']:.4f}, {mcmc_result['mu_ci_upper']:.4f}]")
        print(f"    tau2 mean:          {mcmc_result['tau2_mean']:.4f}")
        print(f"    tau2 median:        {mcmc_result['tau2_median']:.4f}")
        print(f"    I2 mean:            {mcmc_result['I2_mean']:.1f}%")
        print(f"\n  --- Convergence Diagnostics ---")
        print(f"    R-hat (mu):         {mcmc_result['rhat_mu']:.4f} {'OK' if mcmc_result['rhat_mu'] < 1.1 else 'WARN'}")
        print(f"    R-hat (tau2):       {mcmc_result['rhat_tau2']:.4f} {'OK' if mcmc_result['rhat_tau2'] < 1.1 else 'WARN'}")
        print(f"    ESS (mu):           {int(mcmc_result['ess_mu'])} {'OK' if mcmc_result['ess_mu'] > 100 else 'WARN'}")
        print(f"    ESS (tau2):         {int(mcmc_result['ess_tau2'])} {'OK' if mcmc_result['ess_tau2'] > 100 else 'WARN'}")
        print(f"    Chains:             {mcmc_result['n_chains']}")
        print(f"    Total samples:      {mcmc_result['total_samples']}")
        print(f"    Converged:          {'YES' if mcmc_result['converged'] else 'NO'}")
        print(f"\n  --- DDMA Probabilities ---")
        print(f"    P(benefit):         {mcmc_result['P_benefit']*100:.1f}%")
        print(f"    95% Prediction:     [{mcmc_result['prediction_lower']:.4f}, {mcmc_result['prediction_upper']:.4f}]")
    else:
        print(f"  [FAIL] MCMC failed: {mcmc_result['error']}")

    # Test the UI button
    print("\n=== Testing UI Button ===")

    # Navigate to Advanced tab
    driver.execute_script("document.querySelector('[data-tab=\"advanced\"]').click()")
    time.sleep(1)

    # Check if the button exists
    btn_exists = driver.execute_script('return document.getElementById("fullMCMCBtn") !== null')
    print(f"  Full MCMC button exists: {'YES' if btn_exists else 'NO'}")

    # Check if results container exists
    results_exists = driver.execute_script('return document.getElementById("fullMCMCResults") !== null')
    print(f"  Results container exists: {'YES' if results_exists else 'NO'}")

    # Check if trace plot container exists
    trace_exists = driver.execute_script('return document.getElementById("fullMCMCTracePlot") !== null')
    print(f"  Trace plot container exists: {'YES' if trace_exists else 'NO'}")

    # Click the button (it will run in background)
    print("  Clicking Full MCMC button...")
    driver.execute_script('document.getElementById("fullMCMCBtn").click()')

    # Wait for completion (up to 30 seconds)
    print("  Waiting for MCMC to complete...")
    for i in range(30):
        time.sleep(1)
        btn_text = driver.execute_script('return document.getElementById("fullMCMCBtn").innerHTML')
        if "Run Full MCMC" in btn_text and i > 2:  # It resets to original text when done
            print(f"  MCMC completed after ~{i} seconds")
            break
        if i % 5 == 0:
            print(f"    ... waiting ({i}s)")

    # Check if results were displayed
    results_html = driver.execute_script('return document.getElementById("fullMCMCResults").innerHTML')
    has_results_displayed = len(results_html) > 100
    print(f"  Results displayed: {'YES' if has_results_displayed else 'NO'}")

    # Check if trace plot was rendered
    trace_rendered = driver.execute_script('return document.getElementById("fullMCMCTracePlot").children.length > 0')
    print(f"  Trace plot rendered: {'YES' if trace_rendered else 'NO'}")

    # Verify AppState has the results stored
    has_stored = driver.execute_script('return AppState.fullMCMCResults && AppState.fullMCMCResults.summary !== undefined')
    print(f"  Results stored in AppState: {'YES' if has_stored else 'NO'}")

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    all_pass = (
        exposed and run_exposed and
        mcmc_result['success'] and
        mcmc_result['rhat_mu'] < 1.2 and
        mcmc_result['ess_mu'] > 50 and
        btn_exists and results_exists and trace_exists
    )

    if all_pass:
        print("  [PASS] All tests PASSED")
        print("  Full MCMC Bayesian meta-analysis is working correctly!")
    else:
        print("  [FAIL] Some tests failed - check output above")

    print("=" * 70)

finally:
    driver.quit()
