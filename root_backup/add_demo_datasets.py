#!/usr/bin/env python3
"""Add missing demo datasets to TruthCert-PairwisePro"""

def main():
    print("=" * 70)
    print("ADDING MISSING DEMO DATASETS")
    print("=" * 70)

    with open('C:/Truthcert1/app.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # New demo datasets to add
    new_datasets = '''
  // Binary Risk Ratio dataset
  BINARY_RR: {
    name: "Aspirin for MI Prevention (Risk Ratio)",
    source: "Classic aspirin trials meta-analysis",
    category: "binary",
    dataType: "binary",
    measure: "RR",
    teaching_point: "Risk ratio is often more intuitive for clinical interpretation",
    studies: [
      { name: "UK-TIA 1988", events_t: 102, n_t: 815, events_c: 117, n_c: 806 },
      { name: "AMIS 1980", events_t: 239, n_t: 2267, events_c: 254, n_c: 2257 },
      { name: "CDP 1976", events_t: 44, n_t: 758, events_c: 64, n_c: 771 },
      { name: "PARIS I 1980", events_t: 85, n_t: 810, events_c: 99, n_c: 406 },
      { name: "ISIS-2 1988", events_t: 791, n_t: 8587, events_c: 1029, n_c: 8600 },
      { name: "RISC 1990", events_t: 5, n_t: 397, events_c: 18, n_c: 399 }
    ]
  },

  // Binary Risk Difference dataset
  BINARY_RD: {
    name: "Antibiotic Prophylaxis (Risk Difference)",
    source: "Surgical prophylaxis trials",
    category: "binary",
    dataType: "binary",
    measure: "RD",
    teaching_point: "Risk difference gives absolute risk reduction (ARR), useful for NNT calculation",
    studies: [
      { name: "Adams 2005", events_t: 3, n_t: 120, events_c: 12, n_c: 118 },
      { name: "Baker 2008", events_t: 5, n_t: 200, events_c: 18, n_c: 198 },
      { name: "Chen 2010", events_t: 2, n_t: 85, events_c: 8, n_c: 82 },
      { name: "Davis 2012", events_t: 8, n_t: 310, events_c: 25, n_c: 305 },
      { name: "Evans 2014", events_t: 4, n_t: 150, events_c: 14, n_c: 148 },
      { name: "Foster 2016", events_t: 6, n_t: 225, events_c: 19, n_c: 220 },
      { name: "Garcia 2018", events_t: 1, n_t: 95, events_c: 7, n_c: 92 },
      { name: "Harris 2020", events_t: 9, n_t: 280, events_c: 22, n_c: 275 }
    ]
  },

  // Continuous SMD dataset
  CONTINUOUS_SMD: {
    name: "CBT for Depression (SMD)",
    source: "Cognitive Behavioral Therapy trials",
    category: "continuous",
    dataType: "continuous",
    measure: "SMD",
    teaching_point: "Standardized mean difference allows combining studies with different depression scales (BDI, HDRS, etc.)",
    studies: [
      { name: "Beck 1979", mean_t: 12.3, sd_t: 8.5, n_t: 30, mean_c: 18.7, sd_c: 9.2, n_c: 28 },
      { name: "Hollon 1992", mean_t: 10.1, sd_t: 7.8, n_t: 45, mean_c: 15.8, sd_c: 8.1, n_c: 43 },
      { name: "DeRubeis 2005", mean_t: 8.9, sd_t: 6.5, n_t: 60, mean_c: 13.2, sd_c: 7.0, n_c: 58 },
      { name: "Dimidjian 2006", mean_t: 11.5, sd_t: 7.2, n_t: 52, mean_c: 17.1, sd_c: 8.4, n_c: 50 },
      { name: "Cuijpers 2013", mean_t: 9.8, sd_t: 6.8, n_t: 75, mean_c: 14.5, sd_c: 7.5, n_c: 72 },
      { name: "Hofmann 2017", mean_t: 7.5, sd_t: 5.9, n_t: 88, mean_c: 12.8, sd_c: 6.7, n_c: 85 },
      { name: "Cuijpers 2019", mean_t: 10.2, sd_t: 7.1, n_t: 65, mean_c: 15.9, sd_c: 7.8, n_c: 62 },
      { name: "Luo 2020", mean_t: 8.1, sd_t: 6.2, n_t: 110, mean_c: 13.5, sd_c: 6.9, n_c: 108 },
      { name: "Zhang 2021", mean_t: 9.5, sd_t: 6.5, n_t: 95, mean_c: 14.2, sd_c: 7.3, n_c: 92 },
      { name: "Wang 2022", mean_t: 8.8, sd_t: 5.8, n_t: 120, mean_c: 13.9, sd_c: 6.5, n_c: 118 }
    ]
  },

  // Generic pre-calculated effect sizes dataset
  GENERIC_EFFECTS: {
    name: "Pre-calculated Effects (Generic)",
    source: "Various published meta-analyses",
    category: "generic",
    dataType: "generic",
    measure: "GEN",
    teaching_point: "When effect sizes and variances are already calculated, use generic input format",
    studies: [
      { name: "Study 1", yi: -0.52, vi: 0.045, sei: 0.212 },
      { name: "Study 2", yi: -0.38, vi: 0.032, sei: 0.179 },
      { name: "Study 3", yi: -0.71, vi: 0.058, sei: 0.241 },
      { name: "Study 4", yi: -0.25, vi: 0.028, sei: 0.167 },
      { name: "Study 5", yi: -0.45, vi: 0.041, sei: 0.202 },
      { name: "Study 6", yi: -0.62, vi: 0.052, sei: 0.228 },
      { name: "Study 7", yi: -0.19, vi: 0.025, sei: 0.158 },
      { name: "Study 8", yi: -0.55, vi: 0.048, sei: 0.219 },
      { name: "Study 9", yi: -0.33, vi: 0.035, sei: 0.187 },
      { name: "Study 10", yi: -0.48, vi: 0.039, sei: 0.197 }
    ]
  },

  // Meta-regression dataset with continuous moderator
  METAREG_DOSE: {
    name: "Dose-Response Meta-Regression",
    source: "Simulated dose-response RCTs",
    category: "binary",
    dataType: "binary",
    measure: "OR",
    teaching_point: "Meta-regression examines how a continuous moderator (dose) affects treatment effect",
    studies: [
      { name: "Low Dose A", events_t: 15, n_t: 100, events_c: 22, n_c: 100, dose: 10 },
      { name: "Low Dose B", events_t: 18, n_t: 120, events_c: 28, n_c: 118, dose: 15 },
      { name: "Medium Dose A", events_t: 12, n_t: 95, events_c: 24, n_c: 92, dose: 25 },
      { name: "Medium Dose B", events_t: 10, n_t: 110, events_c: 25, n_c: 108, dose: 30 },
      { name: "Medium Dose C", events_t: 14, n_t: 130, events_c: 32, n_c: 128, dose: 35 },
      { name: "High Dose A", events_t: 8, n_t: 105, events_c: 26, n_c: 102, dose: 50 },
      { name: "High Dose B", events_t: 6, n_t: 115, events_c: 28, n_c: 112, dose: 60 },
      { name: "High Dose C", events_t: 5, n_t: 125, events_c: 30, n_c: 120, dose: 75 },
      { name: "Very High A", events_t: 4, n_t: 90, events_c: 22, n_c: 88, dose: 100 },
      { name: "Very High B", events_t: 3, n_t: 100, events_c: 25, n_c: 98, dose: 120 }
    ]
  },

  // DTA - Diagnostic Test Accuracy dataset
  DTA_DIAGNOSTIC: {
    name: "Rapid Antigen Test (DTA)",
    source: "COVID-19 rapid test validation studies",
    category: "dta",
    dataType: "dta",
    measure: "DTA",
    teaching_point: "DTA meta-analysis uses 2x2 tables (TP, FP, FN, TN) to pool sensitivity and specificity",
    studies: [
      { name: "Albert 2020", tp: 85, fp: 5, fn: 15, tn: 195 },
      { name: "Bravo 2020", tp: 72, fp: 8, fn: 18, tn: 202 },
      { name: "Corona 2021", tp: 91, fp: 3, fn: 9, tn: 197 },
      { name: "Delta 2021", tp: 78, fp: 12, fn: 22, tn: 188 },
      { name: "Echo 2021", tp: 88, fp: 4, fn: 12, tn: 196 },
      { name: "Foxtrot 2021", tp: 82, fp: 6, fn: 18, tn: 194 },
      { name: "Golf 2022", tp: 95, fp: 2, fn: 5, tn: 198 },
      { name: "Hotel 2022", tp: 76, fp: 10, fn: 24, tn: 190 },
      { name: "India 2022", tp: 89, fp: 5, fn: 11, tn: 195 },
      { name: "Juliet 2022", tp: 84, fp: 7, fn: 16, tn: 193 },
      { name: "Kilo 2023", tp: 92, fp: 4, fn: 8, tn: 196 },
      { name: "Lima 2023", tp: 80, fp: 9, fn: 20, tn: 191 }
    ]
  }'''

    # Find the location to insert - before the closing of DEMO_DATASETS
    # The pattern is "MULTI_OUTCOME: {" ... "}]" then "\n  }" then "\n};"

    # Find the end of MULTI_OUTCOME dataset
    marker = '''    }]
  }
};'''

    if marker in content:
        # Insert new datasets before the final }};
        new_content = content.replace(marker, '''    }]
  },
''' + new_datasets + '''
};''')

        with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("\n[OK] Added 6 new demo datasets:")
        print("  - BINARY_RR: Aspirin for MI Prevention (Risk Ratio)")
        print("  - BINARY_RD: Antibiotic Prophylaxis (Risk Difference)")
        print("  - CONTINUOUS_SMD: CBT for Depression (SMD)")
        print("  - GENERIC_EFFECTS: Pre-calculated Effects")
        print("  - METAREG_DOSE: Dose-Response Meta-Regression")
        print("  - DTA_DIAGNOSTIC: Rapid Antigen Test (DTA)")
    else:
        # Try alternative marker
        marker2 = '  }\n};'
        if marker2 in content:
            idx = content.rfind(marker2)
            new_content = content[:idx] + '  },\n' + new_datasets + '\n};'
            with open('C:/Truthcert1/app.js', 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("\n[OK] Added datasets using alternative marker")
        else:
            print("\n[ERROR] Could not find insertion point")
            print("  Searching for DEMO_DATASETS closing...")

            # Find MULTI_OUTCOME and work from there
            if 'MULTI_OUTCOME:' in content:
                print("  Found MULTI_OUTCOME")
                # Find the end
                idx = content.find('MULTI_OUTCOME:')
                # Find the next }; after MULTI_OUTCOME
                end_idx = content.find('};', idx)
                if end_idx > 0:
                    print(f"  Found closing at position {end_idx}")
                    # Check context
                    context = content[end_idx-50:end_idx+10]
                    print(f"  Context: {repr(context)}")

    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    main()
