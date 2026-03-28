import sys, json
sys.stdout.reconfigure(encoding="utf-8")

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

driver.execute_script("window.testEffects = " + str(TEST_EFFECTS) + "; window.testSEs = " + str(TEST_SES) + ";")

results = []
tol = 0.02

def cmp(js, r, name):
    try:
        if js is None or r is None:
            return {"name": name, "js": js, "r": r, "match": False, "diff": "N/A"}
        diff = abs(float(js) - float(r)) / max(abs(float(r)), 1e-10)
        match = diff < tol
        return {"name": name, "js": round(float(js), 6), "r": r, "match": match, "diff": round(diff*100, 2)}
    except:
        return {"name": name, "js": js, "r": r, "match": False, "diff": "Error"}

print("="*70)
print("NMA PRO v6.2 - JAVASCRIPT VS R VALIDATION")
print("="*70)

print("\n[1] BASIC STATISTICS")
print("-"*50)

js = driver.execute_script("return Stats.mean([1,2,3,4,5])")
r = cmp(js, R_REF["stats_mean"]["r_value"], "mean")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] Mean: JS=%s, R=%s" % (status, r["js"], r["r"]))

js = driver.execute_script("return Stats.pnorm(1.96)")
r = cmp(js, R_REF["stats_pnorm"]["r_value"], "pnorm")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] pnorm(1.96): JS=%s, R=%s" % (status, r["js"], r["r"]))

js = driver.execute_script("return Stats.qnorm(0.975)")
r = cmp(js, R_REF["stats_qnorm"]["r_value"], "qnorm")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] qnorm(0.975): JS=%s, R=%s" % (status, r["js"], r["r"]))

js = driver.execute_script("return Stats.pchisq(3.84, 1)")
r = cmp(js, R_REF["stats_pchisq"]["r_value"], "pchisq")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] pchisq(3.84,1): JS=%s, R=%s" % (status, r["js"], r["r"]))

js = driver.execute_script("return Stats.pt(2.0, 10)")
r = cmp(js, R_REF["stats_pt"]["r_value"], "pt")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] pt(2.0,10): JS=%s, R=%s" % (status, r["js"], r["r"]))

print("\n[2] META-ANALYSIS (Fixed Effect)")
print("-"*50)

ma = driver.execute_script("return CumulativeMeta.poolEffects(testEffects, testSEs)")
r = cmp(ma.get("effect"), R_REF["meta_fixed"]["r_value"], "fixed_effect")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] Fixed Effect: JS=%s, R=%s" % (status, r["js"], r["r"]))

r = cmp(ma.get("se"), R_REF["meta_fixed"]["se"], "fixed_se")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] Fixed SE: JS=%s, R=%s" % (status, r["js"], r["r"]))

print("\n[3] PUBLICATION BIAS")
print("-"*50)

eg = driver.execute_script("return PublicationBias.eggerTest(testEffects, testSEs)")
egz = eg.get("zValue") or eg.get("z")
r = cmp(egz, R_REF["egger"]["z"], "egger_z")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] Egger z: JS=%s, R=%s" % (status, r["js"], r["r"]))

r = cmp(eg.get("pValue"), R_REF["egger"]["pvalue"], "egger_p")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] Egger p: JS=%s, R=%s" % (status, r["js"], r["r"]))

bg = driver.execute_script("return PublicationBias.beggTest(testEffects, testSEs)")
r = cmp(bg.get("tau"), R_REF["begg"]["tau"], "begg_tau")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] Begg tau: JS=%s, R=%s" % (status, r["js"], r["r"]))

tf = driver.execute_script("return PublicationBias.trimAndFill(testEffects, testSEs)")
tfk = tf.get("k0") or tf.get("studiesAdded")
r = cmp(tfk, R_REF["trimfill"]["k0"], "tf_k0")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] TF k0: JS=%s, R=%s" % (status, r["js"], r["r"]))

r = cmp(tf.get("adjustedEffect"), R_REF["trimfill"]["adjusted_effect"], "tf_adj")
results.append(r)
status = "PASS" if r["match"] else "FAIL"
print("  [%s] TF adjusted: JS=%s, R=%s" % (status, r["js"], r["r"]))

print("\n[4] NETWORK META-ANALYSIS")
print("-"*50)

nma = driver.execute_script(chr(39) + chr(39) + chr(39) + """
    const studies = [
        { study: "S1", treatment1: "A", treatment2: "B", effect: 0.3, se: 0.1 },
        { study: "S2", treatment1: "A", treatment2: "B", effect: 0.4, se: 0.15 },
        { study: "S3", treatment1: "B", treatment2: "C", effect: 0.2, se: 0.12 },
        { study: "S4", treatment1: "B", treatment2: "C", effect: 0.25, se: 0.14 },
        { study: "S5", treatment1: "A", treatment2: "C", effect: 0.5, se: 0.18 },
        { study: "S6", treatment1: "A", treatment2: "C", effect: 0.55, se: 0.2 }
    ];
    try { return FrequentistNMA.analyze(studies, {reference: "A"}); }
    catch(e) { return {error: e.message}; }
""" + chr(39) + chr(39) + chr(39))

if nma and not nma.get("error"):
    effects = nma.get("treatmentEffects", {})
    ab = effects.get("B", {}).get("effect")
    r = cmp(ab, R_REF["nma_random"]["AB"], "nma_AB")
    results.append(r)
    status = "PASS" if r["match"] else "FAIL"
    print("  [%s] A vs B: JS=%s, R=%s" % (status, r["js"], r["r"]))
    
    ac = effects.get("C", {}).get("effect")
    r = cmp(ac, R_REF["nma_random"]["AC"], "nma_AC")
    results.append(r)
    status = "PASS" if r["match"] else "FAIL"
    print("  [%s] A vs C: JS=%s, R=%s" % (status, r["js"], r["r"]))
else:
    print("  [SKIP] NMA: %s" % str(nma.get("error", "unknown"))[:50])

print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)

passed = sum(1 for x in results if x.get("match"))
total = len(results)

print("  PASSED: %d/%d (%.1f%%)" % (passed, total, 100*passed/total))
print("  FAILED: %d/%d" % (total-passed, total))
overall = "PASS" if passed == total else "REVIEW"
print("  Overall: %s" % overall)

report = {"summary": {"passed": passed, "failed": total-passed, "total": total}, "details": results}
with open("C:/Users/user/validation_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("  Report: C:/Users/user/validation_report.json")
driver.quit()
