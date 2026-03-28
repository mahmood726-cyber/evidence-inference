#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding="utf-8")

import json
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

with open("C:/Users/user/r_validation_results.json", "r") as f:
    R_REF = json.load(f)

TEST_EFFECTS = [0.5, 0.3, 0.8, 0.2, 0.6, 0.4, 0.7, 0.35, 0.55, 0.45]
TEST_SES = [0.1, 0.15, 0.2, 0.12, 0.18, 0.14, 0.22, 0.11, 0.16, 0.13]

options = Options()
options.add_argument("--headless")
driver = webdriver.Edge(options=options)
driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html")
time.sleep(3)

driver.execute_script(f"""
window.testEffects = {TEST_EFFECTS};
window.testSEs = {TEST_SES};
""")

results = []
tol = 0.01

def cmp(js, r, name):
    try:
        diff = abs(float(js) - float(r)) / max(abs(float(r)), 1e-10)
        match = diff < tol
        return {"name": name, "js": js, "r": r, "match": match, "diff": f"{diff*100:.4f}%"}
    except:
        return {"name": name, "js": js, "r": r, "match": False, "diff": "N/A"}

print("="*70)
print("NMA PRO v6.2 - JAVASCRIPT VS R VALIDATION")
print("="*70)

# Stats
print("
[1] BASIC STATISTICS")
print("-"*50)

js = driver.execute_script("return Stats.mean([1,2,3,4,5])")
r = cmp(js, R_REF["stats_mean"]["r_value"], "mean")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] Mean: JS={r["js"]}, R={r["r"]}")

js = driver.execute_script("return Stats.sd([1,2,3,4,5])")
r = cmp(js, R_REF["stats_sd"]["r_value"], "sd")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] SD: JS={r["js"]:.6f}, R={r["r"]}")

js = driver.execute_script("return Stats.pnorm(1.96)")
r = cmp(js, R_REF["stats_pnorm"]["r_value"], "pnorm")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] pnorm: JS={r["js"]:.6f}, R={r["r"]}")

js = driver.execute_script("return Stats.qnorm(0.975)")
r = cmp(js, R_REF["stats_qnorm"]["r_value"], "qnorm")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] qnorm: JS={r["js"]:.6f}, R={r["r"]}")

js = driver.execute_script("return Stats.chiSquareCDF(3.84, 1)")
r = cmp(js, R_REF["stats_pchisq"]["r_value"], "pchisq")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] pchisq: JS={r["js"]:.6f}, R={r["r"]}")

js = driver.execute_script("return Stats.tCDF(2.0, 10)")
r = cmp(js, R_REF["stats_pt"]["r_value"], "pt")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] pt: JS={r["js"]:.6f}, R={r["r"]}")

# Meta-analysis
print("
[2] META-ANALYSIS")
print("-"*50)

ma = driver.execute_script("return MetaAnalysis.randomEffects(testEffects, testSEs, {method: "REML"})")
r = cmp(ma.get("pooledEffect"), R_REF["meta_pooled"]["r_value"], "pooled")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] Pooled: JS={r["js"]:.6f}, R={r["r"]}")

r = cmp(ma.get("se"), R_REF["meta_pooled"]["se"], "se")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] SE: JS={r["js"]:.6f}, R={r["r"]}")

r = cmp(ma.get("tau2"), R_REF["meta_tau2"]["r_value"], "tau2")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] Tau2: JS={r["js"]:.6f}, R={r["r"]}")

r = cmp(ma.get("I2"), R_REF["meta_I2"]["r_value"], "I2")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] I2: JS={r["js"]:.4f}%, R={r["r"]}%")

r = cmp(ma.get("Q"), R_REF["meta_Q"]["r_value"], "Q")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] Q: JS={r["js"]:.4f}, R={r["r"]}")

fe = driver.execute_script("return MetaAnalysis.fixedEffect(testEffects, testSEs)")
r = cmp(fe.get("pooledEffect"), R_REF["meta_fixed"]["r_value"], "fixed")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] Fixed: JS={r["js"]:.6f}, R={r["r"]}")

# Publication Bias
print("
[3] PUBLICATION BIAS")
print("-"*50)

eg = driver.execute_script("return PublicationBias.eggerTest(testEffects, testSEs)")
r = cmp(eg.get("zValue") or eg.get("z"), R_REF["egger"]["z"], "egger_z")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] Egger z: JS={r["js"]:.4f}, R={r["r"]}")

r = cmp(eg.get("pValue"), R_REF["egger"]["pvalue"], "egger_p")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] Egger p: JS={r["js"]:.4f}, R={r["r"]}")

bg = driver.execute_script("return PublicationBias.beggTest(testEffects, testSEs)")
r = cmp(bg.get("tau"), R_REF["begg"]["tau"], "begg_tau")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] Begg tau: JS={r["js"]:.4f}, R={r["r"]}")

tf = driver.execute_script("return PublicationBias.trimAndFill(testEffects, testSEs)")
r = cmp(tf.get("k0") or tf.get("studiesAdded"), R_REF["trimfill"]["k0"], "tf_k0")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] TF k0: JS={r["js"]}, R={r["r"]}")

r = cmp(tf.get("adjustedEffect"), R_REF["trimfill"]["adjusted_effect"], "tf_adj")
results.append(r)
print(f"  [{"PASS" if r["match"] else "FAIL"}] TF adj: JS={r["js"]:.6f}, R={r["r"]}")

# Summary
print("
" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)

passed = sum(1 for x in results if x["match"])
total = len(results)

print(f"
  PASSED: {passed}/{total} ({100*passed/total:.1f}%)")
print(f"  FAILED: {total-passed}/{total}")
print(f"
  Result: {"PASS" if passed == total else "NEEDS REVIEW"}")

report = {"passed": passed, "total": total, "details": results}
with open("C:/Users/user/validation_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"
  Report: C:/Users/user/validation_report.json")

driver.quit()
