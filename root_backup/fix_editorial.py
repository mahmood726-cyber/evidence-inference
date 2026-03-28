import re

with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix 1: Add reference to DL
old = "DerSimonian-Laird moment-based estimator\n     * Fast, simple"
new = "DerSimonian-Laird moment-based estimator\n     *\n     * @reference DerSimonian R, Laird N. Control Clin Trials 1986;7:177-188.\n     *\n     * Fast, simple"
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("1. DL reference added")

# Fix 2: Add reference to SJ
old = "Sidik-Jonkman two-step estimator\n     */"
new = "Sidik-Jonkman two-step estimator\n     *\n     * @reference Sidik K, Jonkman JN. JRSS-C 2005;54:367-384.\n     */"
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("2. SJ reference added")

# Fix 3: Add reference to HE
old = "Hedges estimator (unweighted)\n     */"
new = "Hedges estimator (unweighted)\n     *\n     * @reference Hedges LV, Olkin I. Statistical Methods for Meta-Analysis. 1985.\n     */"
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("3. HE reference added")

# Fix 4: Add reference to EB
old = "Empirical Bayes estimator\n     */"
new = "Empirical Bayes estimator\n     *\n     * @reference Morris CN. JASA 1983;78:47-55.\n     */"
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("4. EB reference added")

# Fix 5: OIS power configurable
old = "const alpha = 0.05, power = 0.80;"
new = "const alpha = config.alpha || 0.05;\n      const power = config.power || 0.80;  // Configurable: 0.80 (default), 0.90, 0.95"
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("5. OIS power configurable")

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Applied {fixes} fixes")

