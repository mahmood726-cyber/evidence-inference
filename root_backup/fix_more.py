with open("C:/Truthcert1/app.js", "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix 6: Z-curve k>=10 documentation
old = "Run Z-Curve Analysis\n     */\n    function runZCurveAnalysis"
new = """Run Z-Curve Analysis
     *
     * @reference Brunner J, Schimmack U. Meta-Psychology 2020;4:MP.2018.874.
     *
     * Requirements: k >= 10 studies
     * Rationale: Mixture model fitting requires sufficient data points
     * for stable parameter estimation.
     */
    function runZCurveAnalysis"""
if old in content:
    content = content.replace(old, new)
    fixes += 1
    print("6. Z-curve k>=10 documented")

# Fix 7: Copas regulatory warning
if "Copas:" not in content:
    old = """recommendation: 'For exact IPD-MA, use ipdmeta or metafor'
      }
    };"""
    new = """recommendation: 'For exact IPD-MA, use ipdmeta or metafor'
      },
      'Copas': {
        method: 'Copas selection model',
        approximation: 'Simplified likelihood; assumes specific selection mechanism',
        accuracy: 'Sensitive to model assumptions',
        recommendation: 'REGULATORY NOTICE: Not validated for regulatory submissions. Use metafor::selmodel().'
      }
    };"""
    if old in content:
        content = content.replace(old, new)
        fixes += 1
        print("7. Copas warning added")

with open("C:/Truthcert1/app.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Applied {fixes} more fixes")

