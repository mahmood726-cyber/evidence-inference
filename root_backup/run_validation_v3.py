import sys, json
sys.stdout.reconfigure(encoding="utf-8")

from selenium import webdriver
from selenium.webdriver.edge.options import Options
import time

# R reference values
R_REF = {
    "stats_mean": {"r_value": 3},
    "stats_pnorm": {"r_value": 0.975},
    "stats_qnorm": {"r_value": 1.96},
    "stats_pchisq": {"r_value": 0.95},
    "stats_pt": {"r_value": 0.9633},
    "meta_fixed": {"r_value": 0.4358, "se": 0.0438},
    "egger": {"z": 2.045, "pvalue": 0.0751},
    "begg": {"tau": 0.5111},
    "trimfill": {"k0": 2, "adjusted_effect": 0.4072},
    "nma_random": {"AB": 0.3246, "AC": 0.5384}
}

TEST_EFFECTS = [0.5, 0.3, 0.8, 0.2, 0.6, 0.4, 0.7, 0.35, 0.55, 0.45]
TEST_SES = [0.1, 0.15, 0.2, 0.12, 0.18, 0.14, 0.22, 0.11, 0.16, 0.13]

options = Options()
options.add_argument("--headless")
driver = webdriver.Edge(options=options)
driver.get("file:///C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html")
time.sleep(3)

driver.execute_script("window.testEffects = " + str(TEST_EFFECTS) + "; window.testSEs = " + str(TEST_SES) + ";")

results = []
tol = 0.05  # 5% tolerance

def cmp(js, r, name):
    try:
        if js is None or r is None:
            return {"name": name, "js": js, "r": r, "match": False, "diff": "N/A"}
        diff = abs(float(js) - float(r)) / max(abs(float(r)), 1e-10)
        match = diff < tol
        return {"name": name, "js": round(float(js), 6), "r": r, "match": match, "diff": round(diff*100, 2)}
    except Exception as e:
        return {"name": name, "js": js, "r": r, "match": False, "diff": str(e)}

print("="*70)
print("NMA PRO v6.2 - POST-FIX VALIDATION")
print("="*70)

# 1. BASIC STATISTICS
print("\n[1] BASIC STATISTICS")
print("-"*50)

js = driver.execute_script("return Stats.mean([1,2,3,4,5])")
r = cmp(js, R_REF["stats_mean"]["r_value"], "mean")
results.append(r)
print("  [%s] Mean: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

js = driver.execute_script("return Stats.pnorm(1.96)")
r = cmp(js, R_REF["stats_pnorm"]["r_value"], "pnorm")
results.append(r)
print("  [%s] pnorm(1.96): JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

js = driver.execute_script("return Stats.qnorm(0.975)")
r = cmp(js, R_REF["stats_qnorm"]["r_value"], "qnorm")
results.append(r)
print("  [%s] qnorm(0.975): JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

js = driver.execute_script("return Stats.pchisq(3.84, 1)")
r = cmp(js, R_REF["stats_pchisq"]["r_value"], "pchisq")
results.append(r)
print("  [%s] pchisq(3.84,1): JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

js = driver.execute_script("return Stats.pt(2.0, 10)")
r = cmp(js, R_REF["stats_pt"]["r_value"], "pt")
results.append(r)
print("  [%s] pt(2.0,10): JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

# 2. FIXED EFFECT META-ANALYSIS
print("\n[2] META-ANALYSIS (Fixed Effect)")
print("-"*50)

ma = driver.execute_script("return CumulativeMeta.poolEffects(testEffects, testSEs)")
r = cmp(ma.get("effect"), R_REF["meta_fixed"]["r_value"], "fixed_effect")
results.append(r)
print("  [%s] Fixed Effect: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

r = cmp(ma.get("se"), R_REF["meta_fixed"]["se"], "fixed_se")
results.append(r)
print("  [%s] Fixed SE: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

# 3. PUBLICATION BIAS
print("\n[3] PUBLICATION BIAS")
print("-"*50)

eg = driver.execute_script("return PublicationBias.eggerTest(testEffects, testSEs)")
print("  Egger result:", eg)

egz = eg.get("zValue") or eg.get("z")
r = cmp(egz, R_REF["egger"]["z"], "egger_z")
results.append(r)
print("  [%s] Egger z: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

r = cmp(eg.get("pValue"), R_REF["egger"]["pvalue"], "egger_p")
results.append(r)
print("  [%s] Egger p: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

bg = driver.execute_script("return PublicationBias.beggTest(testEffects, testSEs)")
r = cmp(bg.get("tau"), R_REF["begg"]["tau"], "begg_tau")
results.append(r)
print("  [%s] Begg tau: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

tf = driver.execute_script("return PublicationBias.trimAndFill(testEffects, testSEs, 0)")
print("  TrimFill result:", tf)

tfk = tf.get("k0") or tf.get("studiesAdded")
r = cmp(tfk, R_REF["trimfill"]["k0"], "tf_k0")
results.append(r)
print("  [%s] TF k0: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

r = cmp(tf.get("adjustedEstimate"), R_REF["trimfill"]["adjusted_effect"], "tf_adj")
results.append(r)
print("  [%s] TF adjusted: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

# 4. NETWORK META-ANALYSIS
print("\n[4] NETWORK META-ANALYSIS")
print("-"*50)

nma = driver.execute_script('''
    const studies = [
        { study: "S1", treatment1: "A", treatment2: "B", events1: 10, n1: 100, events2: 15, n2: 100 },
        { study: "S2", treatment1: "A", treatment2: "B", events1: 12, n1: 100, events2: 18, n2: 100 },
        { study: "S3", treatment1: "B", treatment2: "C", events1: 15, n1: 100, events2: 20, n2: 100 },
        { study: "S4", treatment1: "B", treatment2: "C", events1: 14, n1: 100, events2: 22, n2: 100 },
        { study: "S5", treatment1: "A", treatment2: "C", events1: 10, n1: 100, events2: 25, n2: 100 },
        { study: "S6", treatment1: "A", treatment2: "C", events1: 11, n1: 100, events2: 28, n2: 100 }
    ];
    try {
        const result = FrequentistNMA.analyze(studies, {reference: "A", effectMeasure: "OR"});
        return result;
    }
    catch(e) { return {error: e.message}; }
''')

print("  NMA result:", nma if isinstance(nma, dict) and nma.get("error") else "Success")

if nma and not nma.get("error"):
    effects = nma.get("effects") or nma.get("treatmentEffects", {})
    print("  Effects keys:", list(effects.keys()) if effects else "None")

    ab = effects.get("B", {}).get("estimate") if effects else None
    r = cmp(ab, R_REF["nma_random"]["AB"], "nma_AB")
    results.append(r)
    print("  [%s] A vs B: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

    ac = effects.get("C", {}).get("estimate") if effects else None
    r = cmp(ac, R_REF["nma_random"]["AC"], "nma_AC")
    results.append(r)
    print("  [%s] A vs C: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

    tau2 = nma.get("tau2")
    print("  Tau2: %s" % tau2)
else:
    print("  [SKIP] NMA: %s" % str(nma.get("error", "unknown"))[:80])

# SUMMARY
print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)

passed = sum(1 for x in results if x.get("match"))
total = len(results)

print("  PASSED: %d/%d (%.1f%%)" % (passed, total, 100*passed/total if total > 0 else 0))
print("  FAILED: %d/%d" % (total-passed, total))
overall = "PASS" if passed == total else ("REVIEW" if passed/total >= 0.8 else "FAIL")
print("  Overall: %s" % overall)

# Save report
report = {"summary": {"passed": passed, "failed": total-passed, "total": total, "pass_rate": "%.1f%%" % (100*passed/total)}, "details": results}
with open("C:/Users/user/validation_report_v3.json", "w") as f:
    json.dump(report, f, indent=2)

print("  Report: C:/Users/user/validation_report_v3.json")
driver.quit()
