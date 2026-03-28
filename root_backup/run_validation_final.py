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
    "egger": {"t": 2.045, "pvalue": 0.0751},  # R reports t-statistic
    "begg": {"tau": 0.5111},
    "trimfill": {"k0": 2, "adjusted_effect": 0.4072},
    # NMA reference from R netmeta with log-OR data
    "nma_random": {"AB": 0.3246, "AC": 0.5384, "BC": 0.2138}
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

def cmp(js, r, name, abs_compare=False):
    try:
        if js is None or r is None:
            return {"name": name, "js": js, "r": r, "match": False, "diff": "N/A"}
        js_val = abs(float(js)) if abs_compare else float(js)
        r_val = abs(float(r)) if abs_compare else float(r)
        diff = abs(js_val - r_val) / max(abs(r_val), 1e-10)
        match = diff < tol
        return {"name": name, "js": round(float(js), 6), "r": r, "match": match, "diff": round(diff*100, 2)}
    except Exception as e:
        return {"name": name, "js": js, "r": r, "match": False, "diff": str(e)}

print("="*70)
print("NMA PRO v6.2 - FINAL VALIDATION")
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
print("  Egger result: t=%s, z=%s, p=%s" % (eg.get("t"), eg.get("zValue"), eg.get("pValue")))

# R's regtest reports t-statistic
egt = eg.get("t") or eg.get("zValue")
r = cmp(egt, R_REF["egger"]["t"], "egger_t")
results.append(r)
print("  [%s] Egger t: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

r = cmp(eg.get("pValue"), R_REF["egger"]["pvalue"], "egger_p")
results.append(r)
print("  [%s] Egger p: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

bg = driver.execute_script("return PublicationBias.beggTest(testEffects, testSEs)")
r = cmp(bg.get("tau"), R_REF["begg"]["tau"], "begg_tau")
results.append(r)
print("  [%s] Begg tau: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

tf = driver.execute_script("return PublicationBias.trimAndFill(testEffects, testSEs, 0)")
print("  TrimFill: k0=%s, adj=%s" % (tf.get("k0"), tf.get("adjustedEstimate")))

tfk = tf.get("k0") or tf.get("studiesAdded")
r = cmp(tfk, R_REF["trimfill"]["k0"], "tf_k0")
results.append(r)
print("  [%s] TF k0: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

r = cmp(tf.get("adjustedEstimate"), R_REF["trimfill"]["adjusted_effect"], "tf_adj")
results.append(r)
print("  [%s] TF adjusted: JS=%s, R=%s" % ("PASS" if r["match"] else "FAIL", r["js"], r["r"]))

# 4. NETWORK META-ANALYSIS (using pre-calculated log-OR values to match R)
print("\n[4] NETWORK META-ANALYSIS")
print("-"*50)

# Use pre-calculated effect sizes (yi) and variances (vi) to match R reference
nma = driver.execute_script('''
    // Use pre-calculated log-OR values matching R reference data
    const studies = [
        { study: "S1", treatment1: "A", treatment2: "B", yi: 0.3, vi: 0.01 },
        { study: "S2", treatment1: "A", treatment2: "B", yi: 0.4, vi: 0.0225 },
        { study: "S3", treatment1: "B", treatment2: "C", yi: 0.2, vi: 0.0144 },
        { study: "S4", treatment1: "B", treatment2: "C", yi: 0.25, vi: 0.0196 },
        { study: "S5", treatment1: "A", treatment2: "C", yi: 0.5, vi: 0.0324 },
        { study: "S6", treatment1: "A", treatment2: "C", yi: 0.55, vi: 0.04 }
    ];
    try {
        const result = FrequentistNMA.analyze(studies, {reference: "A", effectMeasure: "SMD"});
        return result;
    }
    catch(e) { return {error: e.message}; }
''')

if nma and not nma.get("error"):
    effects = nma.get("effects") or nma.get("treatmentEffects", {})
    print("  Effects: B=%s, C=%s" % (
        effects.get("B", {}).get("estimate") if effects else None,
        effects.get("C", {}).get("estimate") if effects else None
    ))

    ab = effects.get("B", {}).get("estimate") if effects else None
    r = cmp(ab, R_REF["nma_random"]["AB"], "nma_AB", abs_compare=True)
    results.append(r)
    print("  [%s] A vs B: |JS|=%s, |R|=%s" % ("PASS" if r["match"] else "FAIL", abs(r["js"]) if r["js"] else None, r["r"]))

    ac = effects.get("C", {}).get("estimate") if effects else None
    r = cmp(ac, R_REF["nma_random"]["AC"], "nma_AC", abs_compare=True)
    results.append(r)
    print("  [%s] A vs C: |JS|=%s, |R|=%s" % ("PASS" if r["match"] else "FAIL", abs(r["js"]) if r["js"] else None, r["r"]))

    # Indirect comparison B vs C = (A vs C) - (A vs B)
    if ab and ac:
        bc = ac - ab
        r = cmp(bc, R_REF["nma_random"]["BC"], "nma_BC", abs_compare=True)
        results.append(r)
        print("  [%s] B vs C: |JS|=%s, |R|=%s" % ("PASS" if r["match"] else "FAIL", abs(r["js"]) if r["js"] else None, r["r"]))

    tau2 = nma.get("tau2")
    print("  Tau2: %s (expected: 0)" % tau2)
else:
    print("  [SKIP] NMA: %s" % str(nma.get("error", "unknown"))[:80])

# SUMMARY
print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)

passed = sum(1 for x in results if x.get("match"))
total = len(results)
pct = 100*passed/total if total > 0 else 0

print("  PASSED: %d/%d (%.1f%%)" % (passed, total, pct))
print("  FAILED: %d/%d" % (total-passed, total))

if passed == total:
    overall = "PASS - All tests passed!"
elif pct >= 90:
    overall = "EXCELLENT - >90% tests passed"
elif pct >= 80:
    overall = "GOOD - >80% tests passed"
else:
    overall = "REVIEW NEEDED"

print("  Overall: %s" % overall)

# Save report
report = {
    "summary": {
        "passed": passed,
        "failed": total-passed,
        "total": total,
        "pass_rate": "%.1f%%" % pct
    },
    "details": results
}
with open("C:/Users/user/validation_report_final.json", "w") as f:
    json.dump(report, f, indent=2)

print("  Report: C:/Users/user/validation_report_final.json")
driver.quit()
