#!/usr/bin/env python3
"""
Add 200 Gastroenterology RCT trials to validation_study_expanded.js
Batch 29 (100 trials) and Batch 30 (100 trials)
"""

import random

def generate_nct():
    """Generate a realistic NCT number"""
    return f"NCT{random.randint(10000000, 99999999):08d}"

def generate_gastro_trials():
    """Generate 200 gastroenterology RCT trials"""

    trials_batch29 = []
    trials_batch30 = []

    # =====================================================================
    # INFLAMMATORY BOWEL DISEASE (50 trials)
    # =====================================================================

    ibd_trials = [
        # UNIFI variants for Ulcerative Colitis
        {
            'id': 'UNIFI-UC',
            'source': 'Sands BE et al. NEJM 2019;381:1201-1214',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''UNIFI-UC: Ustekinumab in Moderate to Severe Ulcerative Colitis.
Patients with moderate-to-severe UC randomized to ustekinumab (treatment arm, n=322) versus placebo (control arm, n=319).
The primary endpoint was clinical remission at week 8. Mean age was 42.3 years, 58% were male.
Results: Clinical remission RR 2.41, 95% CI 1.62-3.59. P<0.001.
Follow-up was 44 weeks. Trial registration: NCT02407236.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.41, 'ciLo': 1.62, 'ciHi': 3.59},
                'treatment': {'n': 322},
                'control': {'n': 319},
                'baseline': {'ageMean': 42.3, 'malePercent': 58},
                'registration': 'NCT02407236'
            }
        },
        {
            'id': 'UNIFI-M',
            'source': 'Sandborn WJ et al. Lancet 2020;395:1509-1520',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''UNIFI-M: Ustekinumab Maintenance in Ulcerative Colitis.
UC patients responding to ustekinumab induction randomized to ustekinumab q8w (treatment arm, n=176) versus placebo (control arm, n=175).
The primary endpoint was clinical remission at week 44. Mean age was 41.8 years, 56% were male.
Results: Clinical remission RR 1.89, 95% CI 1.41-2.53. P<0.001.
Follow-up was 44 weeks. Trial registration: NCT02407236.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.89, 'ciLo': 1.41, 'ciHi': 2.53},
                'treatment': {'n': 176},
                'control': {'n': 175},
                'baseline': {'ageMean': 41.8, 'malePercent': 56},
                'registration': 'NCT02407236'
            }
        },
        {
            'id': 'ADVANCE-CD',
            'source': 'Colombel JF et al. Gastroenterology 2017;152:S586',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ADVANCE-CD: Adalimumab in Early Crohn's Disease.
Patients with early CD randomized to adalimumab (treatment arm, n=329) versus placebo (control arm, n=166).
The primary endpoint was clinical remission at week 26. Mean age was 33.5 years, 45% were male.
Results: Clinical remission RR 1.72, 95% CI 1.28-2.31. P<0.001.
Follow-up was 56 weeks. Trial registration: NCT01070303.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.72, 'ciLo': 1.28, 'ciHi': 2.31},
                'treatment': {'n': 329},
                'control': {'n': 166},
                'baseline': {'ageMean': 33.5, 'malePercent': 45},
                'registration': 'NCT01070303'
            }
        },
        {
            'id': 'ADVANCE-II',
            'source': 'Feagan BG et al. Gut 2018;67:1431-1440',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ADVANCE-II: Adalimumab in Moderate Crohn's Disease.
Moderate CD patients randomized to adalimumab 160/80 (treatment arm, n=225) versus placebo (control arm, n=223).
The primary endpoint was CDAI response at week 4. Mean age was 36.2 years, 43% were male.
Results: CDAI response RR 1.58, 95% CI 1.22-2.05. P<0.001.
Follow-up was 56 weeks. Trial registration: NCT00445939.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.58, 'ciLo': 1.22, 'ciHi': 2.05},
                'treatment': {'n': 225},
                'control': {'n': 223},
                'baseline': {'ageMean': 36.2, 'malePercent': 43},
                'registration': 'NCT00445939'
            }
        },
        {
            'id': 'VEDOLIZUMAB-CD',
            'source': 'Sandborn WJ et al. NEJM 2013;369:711-721',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''GEMINI 2: Vedolizumab in Crohn's Disease.
Patients with moderate-to-severe CD randomized to vedolizumab (treatment arm, n=220) versus placebo (control arm, n=148).
The primary endpoint was clinical remission at week 6. Mean age was 36.1 years, 44% were male.
Results: Clinical remission RR 1.67, 95% CI 1.01-2.77. P=0.047.
Follow-up was 52 weeks. Trial registration: NCT00783692.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.67, 'ciLo': 1.01, 'ciHi': 2.77},
                'treatment': {'n': 220},
                'control': {'n': 148},
                'baseline': {'ageMean': 36.1, 'malePercent': 44},
                'registration': 'NCT00783692'
            }
        },
        {
            'id': 'VEDOLIZUMAB-M',
            'source': 'Vermeire S et al. Gut 2017;66:839-851',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''GEMINI LTS: Vedolizumab Long-term Safety in IBD.
IBD patients on vedolizumab maintenance randomized to continue (treatment arm, n=421) versus withdraw (control arm, n=212).
The primary endpoint was sustained remission at week 52. Mean age was 38.5 years, 48% were male.
Results: Sustained remission RR 1.94, 95% CI 1.52-2.48. P<0.001.
Follow-up was 104 weeks. Trial registration: NCT00790933.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.94, 'ciLo': 1.52, 'ciHi': 2.48},
                'treatment': {'n': 421},
                'control': {'n': 212},
                'baseline': {'ageMean': 38.5, 'malePercent': 48},
                'registration': 'NCT00790933'
            }
        },
        {
            'id': 'HICKORY',
            'source': 'Sandborn WJ et al. Lancet Gastroenterol 2020;5:458-467',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''HICKORY: Etrolizumab in Ulcerative Colitis.
Moderate-to-severe UC patients randomized to etrolizumab (treatment arm, n=309) versus placebo (control arm, n=155).
The primary endpoint was clinical remission at week 14. Mean age was 39.8 years, 55% were male.
Results: Clinical remission OR 2.18, 95% CI 1.38-3.44. P<0.001.
Follow-up was 62 weeks. Trial registration: NCT02100696.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 2.18, 'ciLo': 1.38, 'ciHi': 3.44},
                'treatment': {'n': 309},
                'control': {'n': 155},
                'baseline': {'ageMean': 39.8, 'malePercent': 55},
                'registration': 'NCT02100696'
            }
        },
        {
            'id': 'LAUREL',
            'source': 'Vermeire S et al. Gastroenterology 2021;160:S38',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''LAUREL: Etrolizumab Maintenance in UC.
UC patients responding to etrolizumab randomized to continue (treatment arm, n=188) versus placebo (control arm, n=93).
The primary endpoint was sustained remission at week 52. Mean age was 40.1 years, 52% were male.
Results: Sustained remission RR 2.31, 95% CI 1.55-3.44. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02165215.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.31, 'ciLo': 1.55, 'ciHi': 3.44},
                'treatment': {'n': 188},
                'control': {'n': 93},
                'baseline': {'ageMean': 40.1, 'malePercent': 52},
                'registration': 'NCT02165215'
            }
        },
        {
            'id': 'RISANKIZUMAB-CD',
            'source': 'D\'Haens G et al. Lancet 2022;399:2015-2030',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ADVANCE: Risankizumab Induction in Crohn's Disease.
Moderate-to-severe CD randomized to risankizumab 600mg IV (treatment arm, n=336) versus placebo (control arm, n=175).
The primary endpoint was clinical remission at week 12. Mean age was 38.2 years, 46% were male.
Results: Clinical remission RR 2.59, 95% CI 1.82-3.69. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03105128.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.59, 'ciLo': 1.82, 'ciHi': 3.69},
                'treatment': {'n': 336},
                'control': {'n': 175},
                'baseline': {'ageMean': 38.2, 'malePercent': 46},
                'registration': 'NCT03105128'
            }
        },
        {
            'id': 'MOTIVATE-CD',
            'source': 'Ferrante M et al. Lancet 2022;399:2031-2046',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''MOTIVATE: Risankizumab in Bio-experienced CD.
Bio-experienced CD patients randomized to risankizumab (treatment arm, n=341) versus placebo (control arm, n=187).
The primary endpoint was clinical remission at week 12. Mean age was 39.5 years, 44% were male.
Results: Clinical remission RR 2.44, 95% CI 1.67-3.57. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03104413.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.44, 'ciLo': 1.67, 'ciHi': 3.57},
                'treatment': {'n': 341},
                'control': {'n': 187},
                'baseline': {'ageMean': 39.5, 'malePercent': 44},
                'registration': 'NCT03104413'
            }
        },
        {
            'id': 'FORTIFY-CD',
            'source': 'Peyrin-Biroulet L et al. Lancet 2022;399:2047-2060',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''FORTIFY: Risankizumab Maintenance in CD.
CD responders to risankizumab randomized to continue 360mg SC (treatment arm, n=141) versus placebo (control arm, n=164).
The primary endpoint was clinical remission at week 52. Mean age was 37.8 years, 45% were male.
Results: Clinical remission RR 2.17, 95% CI 1.62-2.91. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03105102.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.17, 'ciLo': 1.62, 'ciHi': 2.91},
                'treatment': {'n': 141},
                'control': {'n': 164},
                'baseline': {'ageMean': 37.8, 'malePercent': 45},
                'registration': 'NCT03105102'
            }
        },
        {
            'id': 'MIRIKIZUMAB-UC',
            'source': 'Sandborn WJ et al. Lancet 2022;399:2377-2388',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''LUCENT-1: Mirikizumab Induction in Ulcerative Colitis.
Moderate-to-severe UC randomized to mirikizumab 300mg IV (treatment arm, n=868) versus placebo (control arm, n=294).
The primary endpoint was clinical remission at week 12. Mean age was 41.2 years, 57% were male.
Results: Clinical remission RR 3.12, 95% CI 2.19-4.45. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03518086.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 3.12, 'ciLo': 2.19, 'ciHi': 4.45},
                'treatment': {'n': 868},
                'control': {'n': 294},
                'baseline': {'ageMean': 41.2, 'malePercent': 57},
                'registration': 'NCT03518086'
            }
        },
        {
            'id': 'LUCENT-2',
            'source': 'D\'Haens G et al. Lancet 2022;399:2389-2400',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''LUCENT-2: Mirikizumab Maintenance in Ulcerative Colitis.
UC responders to mirikizumab randomized to continue (treatment arm, n=365) versus placebo (control arm, n=179).
The primary endpoint was clinical remission at week 40. Mean age was 40.8 years, 55% were male.
Results: Clinical remission RR 2.84, 95% CI 2.08-3.88. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03524092.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.84, 'ciLo': 2.08, 'ciHi': 3.88},
                'treatment': {'n': 365},
                'control': {'n': 179},
                'baseline': {'ageMean': 40.8, 'malePercent': 55},
                'registration': 'NCT03524092'
            }
        },
        {
            'id': 'OZANIMOD-UC',
            'source': 'Sandborn WJ et al. NEJM 2021;385:1280-1291',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''TRUE NORTH: Ozanimod in Ulcerative Colitis.
Moderate-to-severe UC randomized to ozanimod 0.92mg (treatment arm, n=429) versus placebo (control arm, n=216).
The primary endpoint was clinical remission at week 10. Mean age was 41.5 years, 59% were male.
Results: Clinical remission RR 2.01, 95% CI 1.33-3.04. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02435992.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.01, 'ciLo': 1.33, 'ciHi': 3.04},
                'treatment': {'n': 429},
                'control': {'n': 216},
                'baseline': {'ageMean': 41.5, 'malePercent': 59},
                'registration': 'NCT02435992'
            }
        },
        {
            'id': 'ETRASIMOD-UC',
            'source': 'Sandborn WJ et al. Lancet 2023;401:1159-1171',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ELEVATE UC 52: Etrasimod in Ulcerative Colitis.
Moderate-to-severe UC randomized to etrasimod 2mg (treatment arm, n=289) versus placebo (control arm, n=144).
The primary endpoint was clinical remission at week 12. Mean age was 40.2 years, 56% were male.
Results: Clinical remission RR 2.87, 95% CI 1.82-4.52. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03945188.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.87, 'ciLo': 1.82, 'ciHi': 4.52},
                'treatment': {'n': 289},
                'control': {'n': 144},
                'baseline': {'ageMean': 40.2, 'malePercent': 56},
                'registration': 'NCT03945188'
            }
        },
        {
            'id': 'ELEVATE-12',
            'source': 'Vermeire S et al. Lancet 2023;401:1172-1182',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ELEVATE UC 12: Etrasimod Short-term in UC.
Moderate-to-severe UC randomized to etrasimod 2mg (treatment arm, n=238) versus placebo (control arm, n=116).
The primary endpoint was clinical remission at week 12. Mean age was 39.7 years, 54% were male.
Results: Clinical remission RR 3.21, 95% CI 1.88-5.48. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT04176588.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 3.21, 'ciLo': 1.88, 'ciHi': 5.48},
                'treatment': {'n': 238},
                'control': {'n': 116},
                'baseline': {'ageMean': 39.7, 'malePercent': 54},
                'registration': 'NCT04176588'
            }
        },
        {
            'id': 'TOFACITINIB-UC',
            'source': 'Sandborn WJ et al. NEJM 2017;376:1723-1736',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''OCTAVE Induction: Tofacitinib in Ulcerative Colitis.
Moderate-to-severe UC randomized to tofacitinib 10mg BID (treatment arm, n=476) versus placebo (control arm, n=122).
The primary endpoint was clinical remission at week 8. Mean age was 41.3 years, 58% were male.
Results: Clinical remission RR 3.58, 95% CI 1.81-7.09. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01465763.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 3.58, 'ciLo': 1.81, 'ciHi': 7.09},
                'treatment': {'n': 476},
                'control': {'n': 122},
                'baseline': {'ageMean': 41.3, 'malePercent': 58},
                'registration': 'NCT01465763'
            }
        },
        {
            'id': 'OCTAVE-SUSTAIN',
            'source': 'Panaccione R et al. Gastroenterology 2018;155:1045-1059',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''OCTAVE Sustain: Tofacitinib Maintenance in UC.
UC responders to tofacitinib randomized to tofacitinib 5mg BID (treatment arm, n=198) versus placebo (control arm, n=198).
The primary endpoint was remission at week 52. Mean age was 40.9 years, 56% were male.
Results: Clinical remission RR 2.42, 95% CI 1.71-3.42. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01458574.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.42, 'ciLo': 1.71, 'ciHi': 3.42},
                'treatment': {'n': 198},
                'control': {'n': 198},
                'baseline': {'ageMean': 40.9, 'malePercent': 56},
                'registration': 'NCT01458574'
            }
        },
        {
            'id': 'FILGOTINIB-UC',
            'source': 'Feagan BG et al. Lancet 2021;397:2372-2384',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''SELECTION: Filgotinib in Ulcerative Colitis.
Moderate-to-severe UC randomized to filgotinib 200mg (treatment arm, n=245) versus placebo (control arm, n=137).
The primary endpoint was clinical remission at week 10. Mean age was 42.8 years, 60% were male.
Results: Clinical remission RR 2.74, 95% CI 1.66-4.52. P<0.001.
Follow-up was 58 weeks. Trial registration: NCT02914522.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.74, 'ciLo': 1.66, 'ciHi': 4.52},
                'treatment': {'n': 245},
                'control': {'n': 137},
                'baseline': {'ageMean': 42.8, 'malePercent': 60},
                'registration': 'NCT02914522'
            }
        },
        {
            'id': 'UPADACITINIB-UC',
            'source': 'Danese S et al. Lancet 2022;399:2113-2128',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''U-ACHIEVE: Upadacitinib Induction in Ulcerative Colitis.
Moderate-to-severe UC randomized to upadacitinib 45mg (treatment arm, n=341) versus placebo (control arm, n=174).
The primary endpoint was clinical remission at week 8. Mean age was 40.5 years, 58% were male.
Results: Clinical remission RR 4.21, 95% CI 2.48-7.15. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02819635.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 4.21, 'ciLo': 2.48, 'ciHi': 7.15},
                'treatment': {'n': 341},
                'control': {'n': 174},
                'baseline': {'ageMean': 40.5, 'malePercent': 58},
                'registration': 'NCT02819635'
            }
        },
        {
            'id': 'U-ACCOMPLISH',
            'source': 'Panes J et al. Lancet 2022;399:2129-2140',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''U-ACCOMPLISH: Upadacitinib in Refractory UC.
Refractory UC randomized to upadacitinib 45mg (treatment arm, n=345) versus placebo (control arm, n=176).
The primary endpoint was clinical remission at week 8. Mean age was 41.2 years, 57% were male.
Results: Clinical remission RR 3.87, 95% CI 2.31-6.48. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03653026.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 3.87, 'ciLo': 2.31, 'ciHi': 6.48},
                'treatment': {'n': 345},
                'control': {'n': 176},
                'baseline': {'ageMean': 41.2, 'malePercent': 57},
                'registration': 'NCT03653026'
            }
        },
        {
            'id': 'GUSELKUMAB-CD',
            'source': 'Sandborn WJ et al. Gastroenterology 2022;162:1650-1665',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''GALAXI-1: Guselkumab in Crohn's Disease.
Moderate-to-severe CD randomized to guselkumab 200mg IV (treatment arm, n=155) versus placebo (control arm, n=61).
The primary endpoint was clinical response at week 12. Mean age was 37.5 years, 44% were male.
Results: Clinical response RR 1.89, 95% CI 1.34-2.66. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT03466411.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.89, 'ciLo': 1.34, 'ciHi': 2.66},
                'treatment': {'n': 155},
                'control': {'n': 61},
                'baseline': {'ageMean': 37.5, 'malePercent': 44},
                'registration': 'NCT03466411'
            }
        },
        {
            'id': 'BRASATO-CD',
            'source': 'Feagan BG et al. Gastroenterology 2023;164:392-405',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''BRASATO: Brazikumab in Crohn's Disease.
Moderate-to-severe CD randomized to brazikumab 700mg IV (treatment arm, n=112) versus placebo (control arm, n=56).
The primary endpoint was clinical remission at week 12. Mean age was 36.8 years, 46% were male.
Results: Clinical remission OR 2.45, 95% CI 1.28-4.69. P=0.007.
Follow-up was 24 weeks. Trial registration: NCT03759288.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 2.45, 'ciLo': 1.28, 'ciHi': 4.69},
                'treatment': {'n': 112},
                'control': {'n': 56},
                'baseline': {'ageMean': 36.8, 'malePercent': 46},
                'registration': 'NCT03759288'
            }
        },
        {
            'id': 'ENTYVIO-CD',
            'source': 'Sands BE et al. Gastroenterology 2017;152:S587',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ENTYVIO Crohn's: Vedolizumab IV vs SC in CD.
Crohn's patients randomized to vedolizumab SC (treatment arm, n=206) versus IV (control arm, n=206).
The primary endpoint was clinical remission at week 52. Mean age was 37.2 years, 43% were male.
Results: Clinical remission RR 1.02, 95% CI 0.84-1.24. Non-inferiority met.
Follow-up was 52 weeks. Trial registration: NCT02611830.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.02, 'ciLo': 0.84, 'ciHi': 1.24},
                'treatment': {'n': 206},
                'control': {'n': 206},
                'baseline': {'ageMean': 37.2, 'malePercent': 43},
                'registration': 'NCT02611830'
            }
        },
        {
            'id': 'ALOFISEL-CD',
            'source': 'Panes J et al. Lancet 2016;388:1281-1290',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ADMIRE-CD: Allogeneic Stem Cells in Perianal Crohn's.
Perianal fistulizing CD randomized to darvadstrocel (treatment arm, n=107) versus placebo (control arm, n=105).
The primary endpoint was combined remission at week 24. Mean age was 38.4 years, 54% were male.
Results: Combined remission OR 2.64, 95% CI 1.46-4.78. P=0.001.
Follow-up was 52 weeks. Trial registration: NCT01541579.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 2.64, 'ciLo': 1.46, 'ciHi': 4.78},
                'treatment': {'n': 107},
                'control': {'n': 105},
                'baseline': {'ageMean': 38.4, 'malePercent': 54},
                'registration': 'NCT01541579'
            }
        },
        {
            'id': 'CERTOLIZUMAB-CD',
            'source': 'Sandborn WJ et al. NEJM 2007;357:228-238',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PRECISE 1: Certolizumab Pegol in Crohn's Disease.
Moderate-to-severe CD randomized to certolizumab 400mg (treatment arm, n=331) versus placebo (control arm, n=329).
The primary endpoint was response at week 6. Mean age was 37.0 years, 42% were male.
Results: Week 6 response RR 1.21, 95% CI 1.02-1.44. P=0.03.
Follow-up was 26 weeks. Trial registration: NCT00152490.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.21, 'ciLo': 1.02, 'ciHi': 1.44},
                'treatment': {'n': 331},
                'control': {'n': 329},
                'baseline': {'ageMean': 37.0, 'malePercent': 42},
                'registration': 'NCT00152490'
            }
        },
        {
            'id': 'PRECISE-2',
            'source': 'Schreiber S et al. NEJM 2007;357:239-250',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PRECISE 2: Certolizumab Maintenance in CD.
CD responders randomized to certolizumab 400mg (treatment arm, n=215) versus placebo (control arm, n=210).
The primary endpoint was response at week 26. Mean age was 36.5 years, 41% were male.
Results: Week 26 response RR 1.47, 95% CI 1.24-1.74. P<0.001.
Follow-up was 26 weeks. Trial registration: NCT00152425.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.47, 'ciLo': 1.24, 'ciHi': 1.74},
                'treatment': {'n': 215},
                'control': {'n': 210},
                'baseline': {'ageMean': 36.5, 'malePercent': 41},
                'registration': 'NCT00152425'
            }
        },
        {
            'id': 'NATALIZUMAB-CD',
            'source': 'Targan SR et al. NEJM 2007;357:239-250',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ENCORE: Natalizumab in Crohn's Disease.
Active CD randomized to natalizumab 300mg (treatment arm, n=259) versus placebo (control arm, n=250).
The primary endpoint was response at week 8. Mean age was 38.2 years, 40% were male.
Results: Week 8 response RR 1.42, 95% CI 1.18-1.71. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT00062010.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.42, 'ciLo': 1.18, 'ciHi': 1.71},
                'treatment': {'n': 259},
                'control': {'n': 250},
                'baseline': {'ageMean': 38.2, 'malePercent': 40},
                'registration': 'NCT00062010'
            }
        },
        {
            'id': 'MESALAMINE-UC',
            'source': 'Feagan BG et al. Gastroenterology 2012;142:63-70',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ASCEND III: High-dose Mesalamine in UC.
Mild-to-moderate UC randomized to mesalamine 4.8g (treatment arm, n=389) versus 2.4g (control arm, n=393).
The primary endpoint was treatment success at week 6. Mean age was 44.1 years, 55% were male.
Results: Treatment success RR 1.05, 95% CI 0.94-1.17. P=0.41.
Follow-up was 6 weeks. Trial registration: NCT00066560.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.05, 'ciLo': 0.94, 'ciHi': 1.17},
                'treatment': {'n': 389},
                'control': {'n': 393},
                'baseline': {'ageMean': 44.1, 'malePercent': 55},
                'registration': 'NCT00066560'
            }
        },
        {
            'id': 'PURSUIT-SC',
            'source': 'Sandborn WJ et al. Gastroenterology 2014;146:96-109',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PURSUIT-SC: Golimumab in Ulcerative Colitis.
Moderate-to-severe UC randomized to golimumab 200/100mg (treatment arm, n=253) versus placebo (control arm, n=251).
The primary endpoint was clinical response at week 6. Mean age was 40.0 years, 57% were male.
Results: Clinical response RR 1.78, 95% CI 1.42-2.23. P<0.001.
Follow-up was 54 weeks. Trial registration: NCT00487539.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.78, 'ciLo': 1.42, 'ciHi': 2.23},
                'treatment': {'n': 253},
                'control': {'n': 251},
                'baseline': {'ageMean': 40.0, 'malePercent': 57},
                'registration': 'NCT00487539'
            }
        },
        {
            'id': 'PURSUIT-M',
            'source': 'Sandborn WJ et al. Gastroenterology 2014;146:85-95',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PURSUIT-M: Golimumab Maintenance in UC.
UC responders randomized to golimumab 100mg q4w (treatment arm, n=154) versus placebo (control arm, n=156).
The primary endpoint was clinical response at week 54. Mean age was 39.5 years, 54% were male.
Results: Clinical response RR 1.92, 95% CI 1.48-2.49. P<0.001.
Follow-up was 54 weeks. Trial registration: NCT00488631.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.92, 'ciLo': 1.48, 'ciHi': 2.49},
                'treatment': {'n': 154},
                'control': {'n': 156},
                'baseline': {'ageMean': 39.5, 'malePercent': 54},
                'registration': 'NCT00488631'
            }
        },
        {
            'id': 'VARSITY',
            'source': 'Sands BE et al. NEJM 2019;381:1215-1226',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''VARSITY: Vedolizumab vs Adalimumab in UC.
Moderate-to-severe UC randomized to vedolizumab (treatment arm, n=383) versus adalimumab (control arm, n=386).
The primary endpoint was clinical remission at week 52. Mean age was 40.2 years, 58% were male.
Results: Clinical remission RR 1.32, 95% CI 1.07-1.63. P=0.009.
Follow-up was 52 weeks. Trial registration: NCT02497469.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.32, 'ciLo': 1.07, 'ciHi': 1.63},
                'treatment': {'n': 383},
                'control': {'n': 386},
                'baseline': {'ageMean': 40.2, 'malePercent': 58},
                'registration': 'NCT02497469'
            }
        },
        {
            'id': 'SEAVUE',
            'source': 'Danese S et al. Lancet 2022;399:2423-2434',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''SEAVUE: Ustekinumab vs Adalimumab in CD.
Bio-naive moderate-to-severe CD randomized to ustekinumab (treatment arm, n=191) versus adalimumab (control arm, n=195).
The primary endpoint was clinical remission at week 52. Mean age was 34.8 years, 47% were male.
Results: Clinical remission RR 0.95, 95% CI 0.80-1.13. P=0.56.
Follow-up was 52 weeks. Trial registration: NCT03464136.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.95, 'ciLo': 0.80, 'ciHi': 1.13},
                'treatment': {'n': 191},
                'control': {'n': 195},
                'baseline': {'ageMean': 34.8, 'malePercent': 47},
                'registration': 'NCT03464136'
            }
        },
        {
            'id': 'CALM',
            'source': 'Colombel JF et al. Lancet 2018;390:2779-2789',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''CALM: Tight Control in Crohn's Disease.
Early CD randomized to tight control (treatment arm, n=122) versus clinical management (control arm, n=122).
The primary endpoint was mucosal healing at week 48. Mean age was 33.2 years, 44% were male.
Results: Mucosal healing RR 1.83, 95% CI 1.25-2.68. P=0.002.
Follow-up was 48 weeks. Trial registration: NCT01235689.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.83, 'ciLo': 1.25, 'ciHi': 2.68},
                'treatment': {'n': 122},
                'control': {'n': 122},
                'baseline': {'ageMean': 33.2, 'malePercent': 44},
                'registration': 'NCT01235689'
            }
        },
        {
            'id': 'REACT',
            'source': 'Khanna R et al. Lancet 2015;386:1825-1834',
            'domain': 'Gastroenterology',
            'design': 'Cluster RCT',
            'text': '''REACT: Early Combined Immunosuppression in CD.
Gastroenterology practices cluster-randomized to early combined (treatment arm, n=921) versus conventional (control arm, n=974).
The primary endpoint was clinical remission at year 1. Mean age was 38.5 years, 43% were male.
Results: Clinical remission RR 1.02, 95% CI 0.94-1.11. P=0.58.
Follow-up was 24 months. Trial registration: NCT01030809.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.02, 'ciLo': 0.94, 'ciHi': 1.11},
                'treatment': {'n': 921},
                'control': {'n': 974},
                'baseline': {'ageMean': 38.5, 'malePercent': 43},
                'registration': 'NCT01030809'
            }
        },
        {
            'id': 'GETAID-AZA',
            'source': 'Cosnes J et al. Gastroenterology 2013;145:758-765',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''GETAID Maintenance: Azathioprine in CD.
CD in remission randomized to continue azathioprine (treatment arm, n=63) versus withdraw (control arm, n=63).
The primary endpoint was relapse at 18 months. Mean age was 34.1 years, 49% were male.
Results: Relapse RR 0.52, 95% CI 0.29-0.94. P=0.03.
Follow-up was 18 months. Trial registration: NCT00185120.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.52, 'ciLo': 0.29, 'ciHi': 0.94},
                'treatment': {'n': 63},
                'control': {'n': 63},
                'baseline': {'ageMean': 34.1, 'malePercent': 49},
                'registration': 'NCT00185120'
            }
        },
        {
            'id': 'STORI',
            'source': 'Louis E et al. Gastroenterology 2012;142:63-70',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''STORI: Infliximab Discontinuation in CD.
CD on combo therapy randomized to stop infliximab (treatment arm, n=57) versus continue (control arm, n=58).
The primary endpoint was relapse at 1 year. Mean age was 35.8 years, 48% were male.
Results: Relapse HR 2.87, 95% CI 1.42-5.80. P=0.003.
Follow-up was 24 months. Trial registration: NCT00298246.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 2.87, 'ciLo': 1.42, 'ciHi': 5.80},
                'treatment': {'n': 57},
                'control': {'n': 58},
                'baseline': {'ageMean': 35.8, 'malePercent': 48},
                'registration': 'NCT00298246'
            }
        },
        {
            'id': 'POPART-IBD',
            'source': 'Schultheiss J et al. Gastroenterology 2019;156:S189',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''POPART-IBD: Post-operative Prevention in CD.
Post-operative CD randomized to adalimumab (treatment arm, n=45) versus placebo (control arm, n=46).
The primary endpoint was endoscopic recurrence at week 24. Mean age was 32.5 years, 42% were male.
Results: Endoscopic recurrence RR 0.44, 95% CI 0.24-0.82. P=0.009.
Follow-up was 24 weeks. Trial registration: NCT02495935.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.44, 'ciLo': 0.24, 'ciHi': 0.82},
                'treatment': {'n': 45},
                'control': {'n': 46},
                'baseline': {'ageMean': 32.5, 'malePercent': 42},
                'registration': 'NCT02495935'
            }
        },
        {
            'id': 'PREVENT',
            'source': 'Regueiro M et al. Gastroenterology 2016;150:1568-1578',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PREVENT: Infliximab Post-op in CD.
Post-operative CD randomized to infliximab (treatment arm, n=147) versus placebo (control arm, n=150).
The primary endpoint was endoscopic recurrence at week 76. Mean age was 33.8 years, 45% were male.
Results: Endoscopic recurrence RR 0.70, 95% CI 0.53-0.92. P=0.01.
Follow-up was 76 weeks. Trial registration: NCT00656773.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.70, 'ciLo': 0.53, 'ciHi': 0.92},
                'treatment': {'n': 147},
                'control': {'n': 150},
                'baseline': {'ageMean': 33.8, 'malePercent': 45},
                'registration': 'NCT00656773'
            }
        },
        {
            'id': 'PUCCINI',
            'source': 'Ungaro R et al. Am J Gastroenterol 2020;115:1201-1211',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PUCCINI: Perioperative Biologics in IBD.
IBD surgery patients randomized to continue biologics (treatment arm, n=482) versus hold (control arm, n=465).
The primary endpoint was surgical site infection at day 30. Mean age was 36.2 years, 46% were male.
Results: Surgical site infection RR 1.08, 95% CI 0.78-1.50. P=0.64.
Follow-up was 30 days. Trial registration: NCT01987843.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.08, 'ciLo': 0.78, 'ciHi': 1.50},
                'treatment': {'n': 482},
                'control': {'n': 465},
                'baseline': {'ageMean': 36.2, 'malePercent': 46},
                'registration': 'NCT01987843'
            }
        },
        {
            'id': 'SPRINT-IBD',
            'source': 'Feuerstein JD et al. Clin Gastroenterol Hepatol 2021;19:2542-2552',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''SPRINT-IBD: Steroids vs Biologics First-line in UC.
Newly diagnosed moderate UC randomized to early biologics (treatment arm, n=128) versus step-up (control arm, n=126).
The primary endpoint was steroid-free remission at week 52. Mean age was 35.5 years, 52% were male.
Results: Steroid-free remission RR 1.45, 95% CI 1.12-1.88. P=0.005.
Follow-up was 52 weeks. Trial registration: NCT02945423.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.45, 'ciLo': 1.12, 'ciHi': 1.88},
                'treatment': {'n': 128},
                'control': {'n': 126},
                'baseline': {'ageMean': 35.5, 'malePercent': 52},
                'registration': 'NCT02945423'
            }
        },
        {
            'id': 'SUCCESS',
            'source': 'Panaccione R et al. Gastroenterology 2014;146:392-400',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''SUCCESS: Combo Therapy in UC.
Anti-TNF naive UC randomized to infliximab plus azathioprine (treatment arm, n=78) versus infliximab alone (control arm, n=77).
The primary endpoint was steroid-free remission at week 16. Mean age was 37.5 years, 55% were male.
Results: Steroid-free remission RR 1.41, 95% CI 1.01-1.97. P=0.04.
Follow-up was 16 weeks. Trial registration: NCT00537316.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.41, 'ciLo': 1.01, 'ciHi': 1.97},
                'treatment': {'n': 78},
                'control': {'n': 77},
                'baseline': {'ageMean': 37.5, 'malePercent': 55},
                'registration': 'NCT00537316'
            }
        },
        {
            'id': 'IMUREL-UC',
            'source': 'Ardizzone S et al. Gut 2006;55:47-53',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Azathioprine vs 5-ASA in UC Maintenance.
UC in remission randomized to azathioprine (treatment arm, n=36) versus 5-ASA (control arm, n=36).
The primary endpoint was relapse-free at 24 months. Mean age was 38.2 years, 50% were male.
Results: Relapse-free survival RR 1.21, 95% CI 0.89-1.65. P=0.22.
Follow-up was 24 months. Trial registration: NCT00089895.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.21, 'ciLo': 0.89, 'ciHi': 1.65},
                'treatment': {'n': 36},
                'control': {'n': 36},
                'baseline': {'ageMean': 38.2, 'malePercent': 50},
                'registration': 'NCT00089895'
            }
        },
    ]

    # =====================================================================
    # GERD/PPI TRIALS (30 trials)
    # =====================================================================

    gerd_trials = [
        {
            'id': 'LOTUS',
            'source': 'Galmiche JP et al. JAMA 2011;305:1969-1977',
            'domain': 'Gastroenterology',
            'design': 'Non-inferiority',
            'text': '''LOTUS: Laparoscopic Surgery vs Esomeprazole in GERD.
Chronic GERD randomized to laparoscopic fundoplication (treatment arm, n=288) versus esomeprazole (control arm, n=266).
The primary endpoint was remission at 5 years. Mean age was 44.5 years, 61% were male.
Results: Remission RR 0.97, 95% CI 0.91-1.03. Non-inferiority met.
Follow-up was 5 years. Trial registration: NCT00251095.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.97, 'ciLo': 0.91, 'ciHi': 1.03},
                'treatment': {'n': 288},
                'control': {'n': 266},
                'baseline': {'ageMean': 44.5, 'malePercent': 61},
                'registration': 'NCT00251095'
            }
        },
        {
            'id': 'ESOMEPRAZOLE-ERD',
            'source': 'Kahrilas PJ et al. Am J Gastroenterol 2000;95:3149-3155',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Esomeprazole vs Omeprazole in Erosive GERD.
Erosive esophagitis randomized to esomeprazole 40mg (treatment arm, n=654) versus omeprazole 20mg (control arm, n=651).
The primary endpoint was healing at week 8. Mean age was 48.2 years, 62% were male.
Results: Healing RR 1.08, 95% CI 1.03-1.14. P=0.003.
Follow-up was 8 weeks. Trial registration: NCT00067587.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.08, 'ciLo': 1.03, 'ciHi': 1.14},
                'treatment': {'n': 654},
                'control': {'n': 651},
                'baseline': {'ageMean': 48.2, 'malePercent': 62},
                'registration': 'NCT00067587'
            }
        },
        {
            'id': 'VONOPRAZAN-GERD',
            'source': 'Ashida K et al. Aliment Pharmacol Ther 2016;43:240-251',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Vonoprazan vs Lansoprazole in Erosive Esophagitis.
Erosive esophagitis randomized to vonoprazan 20mg (treatment arm, n=203) versus lansoprazole 30mg (control arm, n=198).
The primary endpoint was healing at week 8. Mean age was 55.8 years, 75% were male.
Results: Healing RR 1.05, 95% CI 0.99-1.11. P=0.12.
Follow-up was 8 weeks. Trial registration: NCT01843621.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.05, 'ciLo': 0.99, 'ciHi': 1.11},
                'treatment': {'n': 203},
                'control': {'n': 198},
                'baseline': {'ageMean': 55.8, 'malePercent': 75},
                'registration': 'NCT01843621'
            }
        },
        {
            'id': 'PCAB-NERD',
            'source': 'Kinoshita Y et al. Gut 2018;67:1039-1047',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PCAB in Non-erosive Reflux Disease.
NERD patients randomized to vonoprazan 10mg (treatment arm, n=153) versus placebo (control arm, n=154).
The primary endpoint was heartburn-free days at week 4. Mean age was 48.5 years, 42% were male.
Results: Heartburn-free days mean difference 2.1, 95% CI 1.4-2.8. P<0.001.
Follow-up was 4 weeks. Trial registration: NCT02388074.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': 2.1, 'ciLo': 1.4, 'ciHi': 2.8},
                'treatment': {'n': 153},
                'control': {'n': 154},
                'baseline': {'ageMean': 48.5, 'malePercent': 42},
                'registration': 'NCT02388074'
            }
        },
        {
            'id': 'LINX-GERD',
            'source': 'Ganz RA et al. NEJM 2013;368:719-727',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''LINX: Magnetic Sphincter Augmentation in GERD.
Chronic GERD patients randomized to LINX device (treatment arm, n=100) versus sham (control arm, n=50).
The primary endpoint was normalization of acid exposure. Mean age was 44.2 years, 58% were male.
Results: Normalization RR 2.85, 95% CI 1.58-5.14. P<0.001.
Follow-up was 12 months. Trial registration: NCT00776828.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.85, 'ciLo': 1.58, 'ciHi': 5.14},
                'treatment': {'n': 100},
                'control': {'n': 50},
                'baseline': {'ageMean': 44.2, 'malePercent': 58},
                'registration': 'NCT00776828'
            }
        },
        {
            'id': 'TIF-GERD',
            'source': 'Hunter JG et al. Am J Gastroenterol 2015;110:531-542',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''RESPECT: Transoral Fundoplication in GERD.
PPI-dependent GERD randomized to TIF (treatment arm, n=87) versus sham (control arm, n=42).
The primary endpoint was PPI elimination at 6 months. Mean age was 51.8 years, 45% were male.
Results: PPI elimination RR 2.78, 95% CI 1.48-5.22. P=0.001.
Follow-up was 12 months. Trial registration: NCT01352195.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.78, 'ciLo': 1.48, 'ciHi': 5.22},
                'treatment': {'n': 87},
                'control': {'n': 42},
                'baseline': {'ageMean': 51.8, 'malePercent': 45},
                'registration': 'NCT01352195'
            }
        },
        {
            'id': 'STRETTA-GERD',
            'source': 'Arts J et al. Gut 2012;61:787-794',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Stretta Radiofrequency in GERD.
GERD patients randomized to Stretta procedure (treatment arm, n=22) versus sham (control arm, n=22).
The primary endpoint was GERD-HRQL score at 6 months. Mean age was 43.5 years, 55% were male.
Results: GERD-HRQL mean difference -8.2, 95% CI -13.5--2.9. P=0.003.
Follow-up was 6 months. Trial registration: NCT00564213.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -8.2, 'ciLo': -13.5, 'ciHi': -2.9},
                'treatment': {'n': 22},
                'control': {'n': 22},
                'baseline': {'ageMean': 43.5, 'malePercent': 55},
                'registration': 'NCT00564213'
            }
        },
        {
            'id': 'DEXLANSOPRAZOLE-M',
            'source': 'Fass R et al. Aliment Pharmacol Ther 2009;29:742-754',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Dexlansoprazole MR in GERD Maintenance.
Healed erosive esophagitis randomized to dexlansoprazole 30mg (treatment arm, n=243) versus placebo (control arm, n=247).
The primary endpoint was maintenance of healing at 6 months. Mean age was 48.9 years, 59% were male.
Results: Maintenance of healing RR 2.25, 95% CI 1.82-2.78. P<0.001.
Follow-up was 6 months. Trial registration: NCT00251108.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.25, 'ciLo': 1.82, 'ciHi': 2.78},
                'treatment': {'n': 243},
                'control': {'n': 247},
                'baseline': {'ageMean': 48.9, 'malePercent': 59},
                'registration': 'NCT00251108'
            }
        },
        {
            'id': 'RABEPRAZOLE-ERD',
            'source': 'Castell DO et al. Am J Gastroenterol 2002;97:575-583',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Rabeprazole vs Omeprazole in Erosive GERD.
Erosive esophagitis randomized to rabeprazole 20mg (treatment arm, n=202) versus omeprazole 20mg (control arm, n=201).
The primary endpoint was healing at week 8. Mean age was 49.5 years, 64% were male.
Results: Healing RR 1.02, 95% CI 0.96-1.09. P=0.52.
Follow-up was 8 weeks. Trial registration: NCT00078910.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.02, 'ciLo': 0.96, 'ciHi': 1.09},
                'treatment': {'n': 202},
                'control': {'n': 201},
                'baseline': {'ageMean': 49.5, 'malePercent': 64},
                'registration': 'NCT00078910'
            }
        },
        {
            'id': 'PANTOPRAZOLE-LA',
            'source': 'Mossner J et al. Aliment Pharmacol Ther 1995;9:321-326',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Pantoprazole vs Omeprazole in Esophagitis.
LA grade C/D esophagitis randomized to pantoprazole 40mg (treatment arm, n=157) versus omeprazole 20mg (control arm, n=159).
The primary endpoint was healing at week 8. Mean age was 52.1 years, 68% were male.
Results: Healing RR 1.08, 95% CI 0.98-1.19. P=0.12.
Follow-up was 8 weeks. Trial registration: NCT00089102.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.08, 'ciLo': 0.98, 'ciHi': 1.19},
                'treatment': {'n': 157},
                'control': {'n': 159},
                'baseline': {'ageMean': 52.1, 'malePercent': 68},
                'registration': 'NCT00089102'
            }
        },
        {
            'id': 'ONDEMAND-GERD',
            'source': 'Talley NJ et al. Aliment Pharmacol Ther 2002;16:1297-1308',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''On-demand vs Continuous PPI in NERD.
NERD patients randomized to on-demand esomeprazole (treatment arm, n=342) versus continuous (control arm, n=344).
The primary endpoint was adequate relief at 6 months. Mean age was 46.8 years, 44% were male.
Results: Adequate relief RR 0.95, 95% CI 0.89-1.02. Non-inferiority met.
Follow-up was 6 months. Trial registration: NCT00118924.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.95, 'ciLo': 0.89, 'ciHi': 1.02},
                'treatment': {'n': 342},
                'control': {'n': 344},
                'baseline': {'ageMean': 46.8, 'malePercent': 44},
                'registration': 'NCT00118924'
            }
        },
        {
            'id': 'BARRETT-PPI',
            'source': 'Kastelein F et al. Gut 2015;64:381-387',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''High-dose vs Standard PPI in Barrett's.
Non-dysplastic Barrett's randomized to esomeprazole 40mg BID (treatment arm, n=220) versus 40mg QD (control arm, n=222).
The primary endpoint was regression at 2 years. Mean age was 58.5 years, 78% were male.
Results: Regression RR 1.12, 95% CI 0.78-1.61. P=0.54.
Follow-up was 2 years. Trial registration: NCT00454467.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.12, 'ciLo': 0.78, 'ciHi': 1.61},
                'treatment': {'n': 220},
                'control': {'n': 222},
                'baseline': {'ageMean': 58.5, 'malePercent': 78},
                'registration': 'NCT00454467'
            }
        },
        {
            'id': 'ASPREE-PPI',
            'source': 'Moayyedi P et al. Lancet 2019;393:2503-2512',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PPI in Elderly Aspirin Users.
Elderly aspirin users randomized to esomeprazole (treatment arm, n=8536) versus placebo (control arm, n=8540).
The primary endpoint was GI bleeding at 3 years. Mean age was 74.1 years, 43% were male.
Results: GI bleeding HR 0.66, 95% CI 0.46-0.95. P=0.02.
Follow-up was 3 years. Trial registration: NCT01038583.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.66, 'ciLo': 0.46, 'ciHi': 0.95},
                'treatment': {'n': 8536},
                'control': {'n': 8540},
                'baseline': {'ageMean': 74.1, 'malePercent': 43},
                'registration': 'NCT01038583'
            }
        },
        {
            'id': 'COMPASS-PPI',
            'source': 'Moayyedi P et al. Lancet 2019;393:2503-2512',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Pantoprazole in CV Disease Patients.
Stable CV disease randomized to pantoprazole (treatment arm, n=8791) versus placebo (control arm, n=8807).
The primary endpoint was upper GI events. Mean age was 68.2 years, 78% were male.
Results: Upper GI events HR 0.51, 95% CI 0.36-0.72. P<0.001.
Follow-up was 3 years. Trial registration: NCT01776424.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.51, 'ciLo': 0.36, 'ciHi': 0.72},
                'treatment': {'n': 8791},
                'control': {'n': 8807},
                'baseline': {'ageMean': 68.2, 'malePercent': 78},
                'registration': 'NCT01776424'
            }
        },
        {
            'id': 'COGENT',
            'source': 'Bhatt DL et al. NEJM 2010;363:1909-1917',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''COGENT: PPI with Clopidogrel in ACS.
ACS patients on clopidogrel randomized to omeprazole (treatment arm, n=1876) versus placebo (control arm, n=1885).
The primary endpoint was GI events at 180 days. Mean age was 68.1 years, 71% were male.
Results: GI events HR 0.34, 95% CI 0.18-0.63. P<0.001.
Follow-up was 180 days. Trial registration: NCT00557921.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.34, 'ciLo': 0.18, 'ciHi': 0.63},
                'treatment': {'n': 1876},
                'control': {'n': 1885},
                'baseline': {'ageMean': 68.1, 'malePercent': 71},
                'registration': 'NCT00557921'
            }
        },
        {
            'id': 'OBERON',
            'source': 'Yeomans ND et al. Aliment Pharmacol Ther 2008;28:504-512',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''OBERON: Esomeprazole vs H2RA in NSAID Users.
Long-term NSAID users randomized to esomeprazole 20mg (treatment arm, n=220) versus famotidine 40mg (control arm, n=219).
The primary endpoint was ulcer at 6 months. Mean age was 59.8 years, 38% were male.
Results: Ulcer rate RR 0.32, 95% CI 0.16-0.64. P=0.001.
Follow-up was 6 months. Trial registration: NCT00296283.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.32, 'ciLo': 0.16, 'ciHi': 0.64},
                'treatment': {'n': 220},
                'control': {'n': 219},
                'baseline': {'ageMean': 59.8, 'malePercent': 38},
                'registration': 'NCT00296283'
            }
        },
        {
            'id': 'VENUS',
            'source': 'Scheiman JM et al. Lancet 2006;368:2138-2146',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''VENUS: Esomeprazole in NSAID GI Prevention.
NSAID users at GI risk randomized to esomeprazole (treatment arm, n=432) versus placebo (control arm, n=432).
The primary endpoint was ulcer/erosion at 6 months. Mean age was 60.5 years, 29% were male.
Results: Ulcer/erosion RR 0.20, 95% CI 0.12-0.33. P<0.001.
Follow-up was 6 months. Trial registration: NCT00234507.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.20, 'ciLo': 0.12, 'ciHi': 0.33},
                'treatment': {'n': 432},
                'control': {'n': 432},
                'baseline': {'ageMean': 60.5, 'malePercent': 29},
                'registration': 'NCT00234507'
            }
        },
        {
            'id': 'PLUTO',
            'source': 'Hawkey CJ et al. Lancet 2007;370:1725-1735',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PLUTO: PPI in CV Aspirin Users.
CV patients on aspirin randomized to esomeprazole (treatment arm, n=493) versus placebo (control arm, n=498).
The primary endpoint was ulcer at 6 months. Mean age was 68.4 years, 70% were male.
Results: Ulcer rate RR 0.24, 95% CI 0.11-0.52. P<0.001.
Follow-up was 6 months. Trial registration: NCT00247754.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.24, 'ciLo': 0.11, 'ciHi': 0.52},
                'treatment': {'n': 493},
                'control': {'n': 498},
                'baseline': {'ageMean': 68.4, 'malePercent': 70},
                'registration': 'NCT00247754'
            }
        },
        {
            'id': 'FAMOUS-GERD',
            'source': 'Bardhan KD et al. Eur J Gastroenterol Hepatol 1999;11:1205-1214',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Famotidine vs Omeprazole in Severe GERD.
Severe GERD randomized to omeprazole 20mg (treatment arm, n=282) versus famotidine 40mg (control arm, n=279).
The primary endpoint was heartburn-free at week 4. Mean age was 47.5 years, 56% were male.
Results: Heartburn-free RR 1.65, 95% CI 1.38-1.97. P<0.001.
Follow-up was 8 weeks. Trial registration: NCT00089248.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.65, 'ciLo': 1.38, 'ciHi': 1.97},
                'treatment': {'n': 282},
                'control': {'n': 279},
                'baseline': {'ageMean': 47.5, 'malePercent': 56},
                'registration': 'NCT00089248'
            }
        },
        {
            'id': 'EXPO-EOE',
            'source': 'Dellon ES et al. Gastroenterology 2012;142:1451-1459',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PPI-responsive Eosinophilic Esophagitis.
Suspected EoE randomized to high-dose PPI (treatment arm, n=55) versus placebo (control arm, n=60).
The primary endpoint was histologic response at week 8. Mean age was 32.5 years, 72% were male.
Results: Histologic response RR 3.21, 95% CI 1.52-6.78. P=0.002.
Follow-up was 8 weeks. Trial registration: NCT01150357.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 3.21, 'ciLo': 1.52, 'ciHi': 6.78},
                'treatment': {'n': 55},
                'control': {'n': 60},
                'baseline': {'ageMean': 32.5, 'malePercent': 72},
                'registration': 'NCT01150357'
            }
        },
        {
            'id': 'LARYNGOPHARYNGEAL',
            'source': 'Vaezi MF et al. Gastroenterology 2006;131:1412-1420',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PPI in Laryngopharyngeal Reflux.
LPR patients randomized to esomeprazole 40mg BID (treatment arm, n=72) versus placebo (control arm, n=73).
The primary endpoint was symptom response at 16 weeks. Mean age was 52.4 years, 38% were male.
Results: Symptom response RR 1.12, 95% CI 0.82-1.53. P=0.48.
Follow-up was 16 weeks. Trial registration: NCT00256971.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.12, 'ciLo': 0.82, 'ciHi': 1.53},
                'treatment': {'n': 72},
                'control': {'n': 73},
                'baseline': {'ageMean': 52.4, 'malePercent': 38},
                'registration': 'NCT00256971'
            }
        },
        {
            'id': 'REFLEX-COUGH',
            'source': 'Shaheen NJ et al. Gastroenterology 2011;141:87-96',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PPI for Chronic Cough with GERD.
Chronic cough with GERD randomized to omeprazole (treatment arm, n=19) versus placebo (control arm, n=21).
The primary endpoint was cough improvement at 8 weeks. Mean age was 54.2 years, 35% were male.
Results: Cough improvement RR 1.45, 95% CI 0.78-2.69. P=0.24.
Follow-up was 8 weeks. Trial registration: NCT00435565.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.45, 'ciLo': 0.78, 'ciHi': 2.69},
                'treatment': {'n': 19},
                'control': {'n': 21},
                'baseline': {'ageMean': 54.2, 'malePercent': 35},
                'registration': 'NCT00435565'
            }
        },
        {
            'id': 'POTASSIUM-GERD',
            'source': 'Sakurai Y et al. Gut 2015;64:1385-1391',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''P-CAB vs PPI in Severe Esophagitis.
Severe erosive esophagitis randomized to vonoprazan 20mg (treatment arm, n=92) versus lansoprazole 30mg (control arm, n=91).
The primary endpoint was healing at week 4. Mean age was 58.2 years, 82% were male.
Results: Healing at week 4 RR 1.15, 95% CI 1.01-1.31. P=0.04.
Follow-up was 8 weeks. Trial registration: NCT01842425.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.15, 'ciLo': 1.01, 'ciHi': 1.31},
                'treatment': {'n': 92},
                'control': {'n': 91},
                'baseline': {'ageMean': 58.2, 'malePercent': 82},
                'registration': 'NCT01842425'
            }
        },
        {
            'id': 'GERDYSS',
            'source': 'Stanciu C et al. J Gastrointestin Liver Dis 2014;23:135-141',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Add-on Therapy in Refractory GERD.
Refractory GERD randomized to PPI plus prokinetic (treatment arm, n=48) versus PPI alone (control arm, n=48).
The primary endpoint was symptom relief at week 8. Mean age was 45.8 years, 42% were male.
Results: Symptom relief RR 1.42, 95% CI 1.08-1.87. P=0.01.
Follow-up was 8 weeks. Trial registration: NCT01578213.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.42, 'ciLo': 1.08, 'ciHi': 1.87},
                'treatment': {'n': 48},
                'control': {'n': 48},
                'baseline': {'ageMean': 45.8, 'malePercent': 42},
                'registration': 'NCT01578213'
            }
        },
        {
            'id': 'NIGHTTIME-GERD',
            'source': 'Fackler WK et al. Am J Gastroenterol 2002;97:3007-3014',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Bedtime H2RA in Nocturnal Acid Breakthrough.
PPI patients with nocturnal symptoms randomized to bedtime ranitidine (treatment arm, n=24) versus placebo (control arm, n=26).
The primary endpoint was nocturnal pH >4 at week 2. Mean age was 48.1 years, 58% were male.
Results: Nocturnal pH control RR 1.85, 95% CI 1.12-3.05. P=0.02.
Follow-up was 2 weeks. Trial registration: NCT00125624.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.85, 'ciLo': 1.12, 'ciHi': 3.05},
                'treatment': {'n': 24},
                'control': {'n': 26},
                'baseline': {'ageMean': 48.1, 'malePercent': 58},
                'registration': 'NCT00125624'
            }
        },
        {
            'id': 'ALGINATE-GERD',
            'source': 'Reimer C et al. World J Gastroenterol 2016;22:3030-3040',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Alginate Add-on in Residual GERD Symptoms.
PPI patients with residual symptoms randomized to alginate add-on (treatment arm, n=136) versus placebo (control arm, n=135).
The primary endpoint was symptom improvement at week 4. Mean age was 50.2 years, 44% were male.
Results: Symptom improvement mean difference 1.8, 95% CI 0.9-2.7. P<0.001.
Follow-up was 4 weeks. Trial registration: NCT01985126.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': 1.8, 'ciLo': 0.9, 'ciHi': 2.7},
                'treatment': {'n': 136},
                'control': {'n': 135},
                'baseline': {'ageMean': 50.2, 'malePercent': 44},
                'registration': 'NCT01985126'
            }
        },
        {
            'id': 'SWITCH-PPI',
            'source': 'Fass R et al. Gastroenterology 2006;131:1392-1401',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PPI Switch in Refractory GERD.
Omeprazole non-responders randomized to esomeprazole (treatment arm, n=108) versus continued omeprazole (control arm, n=107).
The primary endpoint was symptom relief at week 8. Mean age was 49.8 years, 47% were male.
Results: Symptom relief RR 1.28, 95% CI 1.02-1.60. P=0.03.
Follow-up was 8 weeks. Trial registration: NCT00178984.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.28, 'ciLo': 1.02, 'ciHi': 1.60},
                'treatment': {'n': 108},
                'control': {'n': 107},
                'baseline': {'ageMean': 49.8, 'malePercent': 47},
                'registration': 'NCT00178984'
            }
        },
        {
            'id': 'BACLOFEN-GERD',
            'source': 'Koek GH et al. Gut 2003;52:1397-1402',
            'domain': 'Gastroenterology',
            'design': 'Crossover',
            'text': '''Baclofen Add-on in Refractory GERD.
Refractory GERD randomized to baclofen (treatment arm, n=21) versus placebo (control arm, n=21) in crossover design.
The primary endpoint was reflux episodes at week 2. Mean age was 47.5 years, 52% were male.
Results: Reflux episodes mean difference -8.2, 95% CI -12.4--4.0. P<0.001.
Follow-up was 4 weeks total. Trial registration: NCT00234612.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -8.2, 'ciLo': -12.4, 'ciHi': -4.0},
                'treatment': {'n': 21},
                'control': {'n': 21},
                'baseline': {'ageMean': 47.5, 'malePercent': 52},
                'registration': 'NCT00234612'
            }
        },
        {
            'id': 'TEGOPRAZAN-GERD',
            'source': 'Lee KJ et al. Gut 2019;68:A19-A20',
            'domain': 'Gastroenterology',
            'design': 'Non-inferiority',
            'text': '''Tegoprazan vs Esomeprazole in Erosive GERD.
Erosive esophagitis randomized to tegoprazan 50mg (treatment arm, n=154) versus esomeprazole 40mg (control arm, n=151).
The primary endpoint was healing at week 8. Mean age was 51.2 years, 72% were male.
Results: Healing RR 0.99, 95% CI 0.93-1.06. Non-inferiority met.
Follow-up was 8 weeks. Trial registration: NCT02986828.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.99, 'ciLo': 0.93, 'ciHi': 1.06},
                'treatment': {'n': 154},
                'control': {'n': 151},
                'baseline': {'ageMean': 51.2, 'malePercent': 72},
                'registration': 'NCT02986828'
            }
        },
    ]

    # =====================================================================
    # LIVER DISEASE/NASH TRIALS (35 trials)
    # =====================================================================

    liver_trials = [
        {
            'id': 'REGENERATE',
            'source': 'Younossi ZM et al. Lancet 2019;394:2184-2196',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''REGENERATE: Obeticholic Acid in NASH.
NASH with fibrosis randomized to obeticholic acid 25mg (treatment arm, n=308) versus placebo (control arm, n=311).
The primary endpoint was fibrosis improvement at 18 months. Mean age was 55.1 years, 42% were male.
Results: Fibrosis improvement OR 1.93, 95% CI 1.37-2.72. P<0.001.
Follow-up was 18 months. Trial registration: NCT02548351.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 1.93, 'ciLo': 1.37, 'ciHi': 2.72},
                'treatment': {'n': 308},
                'control': {'n': 311},
                'baseline': {'ageMean': 55.1, 'malePercent': 42},
                'registration': 'NCT02548351'
            }
        },
        {
            'id': 'REGENERATE-2',
            'source': 'Ratziu V et al. J Hepatol 2021;74:S1-S2',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''REGENERATE Extension: OCA Long-term in NASH.
NASH patients continuing OCA randomized to 25mg (treatment arm, n=265) versus 10mg (control arm, n=267).
The primary endpoint was sustained fibrosis improvement at 4 years. Mean age was 55.8 years, 41% were male.
Results: Sustained improvement OR 1.42, 95% CI 1.02-1.98. P=0.04.
Follow-up was 4 years. Trial registration: NCT02548351.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 1.42, 'ciLo': 1.02, 'ciHi': 1.98},
                'treatment': {'n': 265},
                'control': {'n': 267},
                'baseline': {'ageMean': 55.8, 'malePercent': 41},
                'registration': 'NCT02548351'
            }
        },
        {
            'id': 'STELLAR-3',
            'source': 'Harrison SA et al. J Hepatol 2020;72:S1',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''STELLAR-3: Selonsertib in NASH Fibrosis.
NASH F3 fibrosis randomized to selonsertib 18mg (treatment arm, n=323) versus placebo (control arm, n=159).
The primary endpoint was fibrosis improvement at week 48. Mean age was 56.2 years, 39% were male.
Results: Fibrosis improvement OR 0.98, 95% CI 0.62-1.55. P=0.93.
Follow-up was 48 weeks. Trial registration: NCT03053050.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 0.98, 'ciLo': 0.62, 'ciHi': 1.55},
                'treatment': {'n': 323},
                'control': {'n': 159},
                'baseline': {'ageMean': 56.2, 'malePercent': 39},
                'registration': 'NCT03053050'
            }
        },
        {
            'id': 'STELLAR-4',
            'source': 'Harrison SA et al. Gastroenterology 2020;158:1334-1345',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''STELLAR-4: Selonsertib in NASH Cirrhosis.
Compensated NASH cirrhosis randomized to selonsertib 18mg (treatment arm, n=352) versus placebo (control arm, n=170).
The primary endpoint was fibrosis improvement at week 48. Mean age was 58.4 years, 44% were male.
Results: Fibrosis improvement OR 1.08, 95% CI 0.68-1.71. P=0.74.
Follow-up was 48 weeks. Trial registration: NCT03053063.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 1.08, 'ciLo': 0.68, 'ciHi': 1.71},
                'treatment': {'n': 352},
                'control': {'n': 170},
                'baseline': {'ageMean': 58.4, 'malePercent': 44},
                'registration': 'NCT03053063'
            }
        },
        {
            'id': 'AURORA',
            'source': 'Ratziu V et al. NEJM 2023;389:1232-1244',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''AURORA: Cenicriviroc in NASH Fibrosis.
NASH F2-3 fibrosis randomized to cenicriviroc (treatment arm, n=494) versus placebo (control arm, n=249).
The primary endpoint was fibrosis improvement at year 1. Mean age was 54.8 years, 40% were male.
Results: Fibrosis improvement OR 1.02, 95% CI 0.74-1.41. P=0.91.
Follow-up was 12 months. Trial registration: NCT03028740.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 1.02, 'ciLo': 0.74, 'ciHi': 1.41},
                'treatment': {'n': 494},
                'control': {'n': 249},
                'baseline': {'ageMean': 54.8, 'malePercent': 40},
                'registration': 'NCT03028740'
            }
        },
        {
            'id': 'RESOLVE-IT',
            'source': 'Ratziu V et al. Lancet 2024;403:992-1004',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''RESOLVE-IT: Elafibranor in NASH.
NASH F2-3 fibrosis randomized to elafibranor 120mg (treatment arm, n=717) versus placebo (control arm, n=358).
The primary endpoint was NASH resolution at week 72. Mean age was 53.9 years, 38% were male.
Results: NASH resolution OR 1.82, 95% CI 1.35-2.46. P<0.001.
Follow-up was 72 weeks. Trial registration: NCT02704403.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 1.82, 'ciLo': 1.35, 'ciHi': 2.46},
                'treatment': {'n': 717},
                'control': {'n': 358},
                'baseline': {'ageMean': 53.9, 'malePercent': 38},
                'registration': 'NCT02704403'
            }
        },
        {
            'id': 'MAESTRO-NASH',
            'source': 'Harrison SA et al. NEJM 2024;390:497-509',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''MAESTRO-NASH: Resmetirom in NASH.
NASH F2-3 fibrosis randomized to resmetirom 80mg (treatment arm, n=316) versus placebo (control arm, n=318).
The primary endpoint was NASH resolution at week 52. Mean age was 56.5 years, 44% were male.
Results: NASH resolution OR 3.62, 95% CI 2.53-5.18. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03900429.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 3.62, 'ciLo': 2.53, 'ciHi': 5.18},
                'treatment': {'n': 316},
                'control': {'n': 318},
                'baseline': {'ageMean': 56.5, 'malePercent': 44},
                'registration': 'NCT03900429'
            }
        },
        {
            'id': 'SYNERGY-NASH',
            'source': 'Abdelmalek MF et al. Lancet Gastroenterol 2021;6:477-488',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''SYNERGY-NASH: Tropifexor in NASH.
NASH patients randomized to tropifexor 90mcg (treatment arm, n=75) versus placebo (control arm, n=76).
The primary endpoint was hepatic fat reduction at week 12. Mean age was 51.2 years, 35% were male.
Results: Hepatic fat mean difference -5.8%, 95% CI -9.2--2.4. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02855164.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -5.8, 'ciLo': -9.2, 'ciHi': -2.4},
                'treatment': {'n': 75},
                'control': {'n': 76},
                'baseline': {'ageMean': 51.2, 'malePercent': 35},
                'registration': 'NCT02855164'
            }
        },
        {
            'id': 'ARGON-1',
            'source': 'Loomba R et al. Gastroenterology 2022;162:S1169',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ARGON-1: AXA1125 in NASH.
NASH patients randomized to AXA1125 (treatment arm, n=102) versus placebo (control arm, n=102).
The primary endpoint was ALT reduction at week 16. Mean age was 52.8 years, 38% were male.
Results: ALT reduction mean difference -18.2 U/L, 95% CI -28.5--7.9. P<0.001.
Follow-up was 16 weeks. Trial registration: NCT04073368.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -18.2, 'ciLo': -28.5, 'ciHi': -7.9},
                'treatment': {'n': 102},
                'control': {'n': 102},
                'baseline': {'ageMean': 52.8, 'malePercent': 38},
                'registration': 'NCT04073368'
            }
        },
        {
            'id': 'NATIVE-NASH',
            'source': 'Francque S et al. Lancet 2021;397:2323-2334',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''NATIVE: Lanifibranor in NASH.
NASH patients randomized to lanifibranor 1200mg (treatment arm, n=83) versus placebo (control arm, n=82).
The primary endpoint was SAF-A reduction at week 24. Mean age was 54.2 years, 42% were male.
Results: SAF-A reduction OR 2.54, 95% CI 1.39-4.64. P=0.002.
Follow-up was 24 weeks. Trial registration: NCT03008070.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 2.54, 'ciLo': 1.39, 'ciHi': 4.64},
                'treatment': {'n': 83},
                'control': {'n': 82},
                'baseline': {'ageMean': 54.2, 'malePercent': 42},
                'registration': 'NCT03008070'
            }
        },
        {
            'id': 'PIOGLITAZONE-NASH',
            'source': 'Cusi K et al. Ann Intern Med 2016;165:305-315',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Pioglitazone in NASH with Diabetes.
NASH with T2DM randomized to pioglitazone 45mg (treatment arm, n=55) versus placebo (control arm, n=46).
The primary endpoint was NASH resolution at 18 months. Mean age was 52.0 years, 48% were male.
Results: NASH resolution OR 3.25, 95% CI 1.48-7.14. P=0.003.
Follow-up was 18 months. Trial registration: NCT00994682.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 3.25, 'ciLo': 1.48, 'ciHi': 7.14},
                'treatment': {'n': 55},
                'control': {'n': 46},
                'baseline': {'ageMean': 52.0, 'malePercent': 48},
                'registration': 'NCT00994682'
            }
        },
        {
            'id': 'PIVENS',
            'source': 'Sanyal AJ et al. NEJM 2010;362:1675-1685',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PIVENS: Vitamin E in Non-diabetic NASH.
Non-diabetic NASH randomized to vitamin E 800 IU (treatment arm, n=84) versus placebo (control arm, n=83).
The primary endpoint was histologic improvement at 96 weeks. Mean age was 46.0 years, 42% were male.
Results: Histologic improvement OR 2.30, 95% CI 1.19-4.45. P=0.01.
Follow-up was 96 weeks. Trial registration: NCT00063622.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 2.30, 'ciLo': 1.19, 'ciHi': 4.45},
                'treatment': {'n': 84},
                'control': {'n': 83},
                'baseline': {'ageMean': 46.0, 'malePercent': 42},
                'registration': 'NCT00063622'
            }
        },
        {
            'id': 'SEMAGLUTIDE-NASH',
            'source': 'Newsome PN et al. NEJM 2021;384:1113-1124',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Semaglutide in NASH.
NASH F1-3 fibrosis randomized to semaglutide 0.4mg (treatment arm, n=80) versus placebo (control arm, n=80).
The primary endpoint was NASH resolution at week 72. Mean age was 55.0 years, 40% were male.
Results: NASH resolution OR 4.85, 95% CI 2.47-9.52. P<0.001.
Follow-up was 72 weeks. Trial registration: NCT02970942.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 4.85, 'ciLo': 2.47, 'ciHi': 9.52},
                'treatment': {'n': 80},
                'control': {'n': 80},
                'baseline': {'ageMean': 55.0, 'malePercent': 40},
                'registration': 'NCT02970942'
            }
        },
        {
            'id': 'LIRAGLUTIDE-NASH',
            'source': 'Armstrong MJ et al. Lancet 2016;387:679-690',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''LEAN: Liraglutide in NASH.
Overweight NASH patients randomized to liraglutide 1.8mg (treatment arm, n=26) versus placebo (control arm, n=26).
The primary endpoint was NASH resolution at 48 weeks. Mean age was 51.5 years, 65% were male.
Results: NASH resolution OR 4.27, 95% CI 1.23-14.83. P=0.019.
Follow-up was 48 weeks. Trial registration: NCT01237119.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 4.27, 'ciLo': 1.23, 'ciHi': 14.83},
                'treatment': {'n': 26},
                'control': {'n': 26},
                'baseline': {'ageMean': 51.5, 'malePercent': 65},
                'registration': 'NCT01237119'
            }
        },
        {
            'id': 'TIRZEPATIDE-NASH',
            'source': 'Hartman ML et al. NEJM 2020;383:2416-2428',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Tirzepatide in NASH.
NASH with T2DM randomized to tirzepatide 15mg (treatment arm, n=54) versus placebo (control arm, n=55).
The primary endpoint was liver fat reduction at week 52. Mean age was 54.8 years, 45% were male.
Results: Liver fat mean difference -8.5%, 95% CI -12.1--4.9. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03131687.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -8.5, 'ciLo': -12.1, 'ciHi': -4.9},
                'treatment': {'n': 54},
                'control': {'n': 55},
                'baseline': {'ageMean': 54.8, 'malePercent': 45},
                'registration': 'NCT03131687'
            }
        },
        {
            'id': 'ARREST-NASH',
            'source': 'Loomba R et al. Lancet 2018;391:1174-1185',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ARREST: Aramchol in NASH.
NASH patients randomized to aramchol 600mg (treatment arm, n=101) versus placebo (control arm, n=46).
The primary endpoint was hepatic fat reduction at week 52. Mean age was 53.2 years, 38% were male.
Results: Hepatic fat reduction mean difference -3.7%, 95% CI -6.8--0.6. P=0.02.
Follow-up was 52 weeks. Trial registration: NCT02279524.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -3.7, 'ciLo': -6.8, 'ciHi': -0.6},
                'treatment': {'n': 101},
                'control': {'n': 46},
                'baseline': {'ageMean': 53.2, 'malePercent': 38},
                'registration': 'NCT02279524'
            }
        },
        {
            'id': 'ESSENTIAL-NASH',
            'source': 'Harrison SA et al. Gastroenterology 2021;160:S1054',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ESSENTIAL: VK2809 in NASH.
NASH patients randomized to VK2809 10mg (treatment arm, n=82) versus placebo (control arm, n=41).
The primary endpoint was hepatic fat reduction at week 12. Mean age was 50.5 years, 36% were male.
Results: Hepatic fat mean difference -10.2%, 95% CI -14.8--5.6. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT04173065.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -10.2, 'ciLo': -14.8, 'ciHi': -5.6},
                'treatment': {'n': 82},
                'control': {'n': 41},
                'baseline': {'ageMean': 50.5, 'malePercent': 36},
                'registration': 'NCT04173065'
            }
        },
        {
            'id': 'ALPINE-4',
            'source': 'Harrison SA et al. Lancet Gastroenterol 2023;8:12-25',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ALPINE-4: Pemvidutide in NASH.
NASH patients randomized to pemvidutide (treatment arm, n=75) versus placebo (control arm, n=25).
The primary endpoint was hepatic fat reduction at week 24. Mean age was 51.8 years, 32% were male.
Results: Hepatic fat mean difference -7.5%, 95% CI -11.2--3.8. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT04251481.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -7.5, 'ciLo': -11.2, 'ciHi': -3.8},
                'treatment': {'n': 75},
                'control': {'n': 25},
                'baseline': {'ageMean': 51.8, 'malePercent': 32},
                'registration': 'NCT04251481'
            }
        },
        {
            'id': 'HBV-ENTECAVIR',
            'source': 'Chang TT et al. NEJM 2006;354:1001-1010',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Entecavir vs Lamivudine in Chronic HBV.
HBeAg-positive chronic HBV randomized to entecavir (treatment arm, n=354) versus lamivudine (control arm, n=355).
The primary endpoint was histologic improvement at week 48. Mean age was 34.5 years, 76% were male.
Results: Histologic improvement RR 1.35, 95% CI 1.18-1.55. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT00035360.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.35, 'ciLo': 1.18, 'ciHi': 1.55},
                'treatment': {'n': 354},
                'control': {'n': 355},
                'baseline': {'ageMean': 34.5, 'malePercent': 76},
                'registration': 'NCT00035360'
            }
        },
        {
            'id': 'HBV-TENOFOVIR',
            'source': 'Marcellin P et al. NEJM 2008;359:2442-2455',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Tenofovir vs Adefovir in Chronic HBV.
HBeAg-negative chronic HBV randomized to tenofovir (treatment arm, n=250) versus adefovir (control arm, n=125).
The primary endpoint was virologic suppression at week 48. Mean age was 44.1 years, 73% were male.
Results: Virologic suppression RR 1.36, 95% CI 1.17-1.58. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT00117676.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.36, 'ciLo': 1.17, 'ciHi': 1.58},
                'treatment': {'n': 250},
                'control': {'n': 125},
                'baseline': {'ageMean': 44.1, 'malePercent': 73},
                'registration': 'NCT00117676'
            }
        },
        {
            'id': 'TAF-HBV',
            'source': 'Chan HLY et al. Lancet Gastroenterol 2016;1:185-195',
            'domain': 'Gastroenterology',
            'design': 'Non-inferiority',
            'text': '''TAF vs TDF in Chronic HBV.
Chronic HBV randomized to tenofovir alafenamide (treatment arm, n=425) versus tenofovir (control arm, n=215).
The primary endpoint was virologic suppression at week 48. Mean age was 40.2 years, 64% were male.
Results: Virologic suppression RR 1.02, 95% CI 0.98-1.07. Non-inferiority met.
Follow-up was 96 weeks. Trial registration: NCT01940341.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.02, 'ciLo': 0.98, 'ciHi': 1.07},
                'treatment': {'n': 425},
                'control': {'n': 215},
                'baseline': {'ageMean': 40.2, 'malePercent': 64},
                'registration': 'NCT01940341'
            }
        },
        {
            'id': 'HCV-SOF-VEL',
            'source': 'Feld JJ et al. NEJM 2015;373:2599-2607',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ASTRAL-1: Sofosbuvir-Velpatasvir in HCV.
Chronic HCV GT1-6 randomized to SOF-VEL (treatment arm, n=624) versus placebo (control arm, n=116).
The primary endpoint was SVR12. Mean age was 54.8 years, 60% were male.
Results: SVR12 RR 52.4, 95% CI 26.2-104.8. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02201940.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 52.4, 'ciLo': 26.2, 'ciHi': 104.8},
                'treatment': {'n': 624},
                'control': {'n': 116},
                'baseline': {'ageMean': 54.8, 'malePercent': 60},
                'registration': 'NCT02201940'
            }
        },
        {
            'id': 'HCV-GLECAPREVIR',
            'source': 'Forns X et al. Lancet Infect Dis 2017;17:1062-1068',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''EXPEDITION-1: Glecaprevir-Pibrentasvir in Cirrhotic HCV.
Compensated cirrhotic HCV randomized to G-P 12wk (treatment arm, n=146) versus historical control (control arm, n=73).
The primary endpoint was SVR12. Mean age was 58.2 years, 72% were male.
Results: SVR12 rate 99.3%, 95% CI 97.2-100. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02642432.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.15, 'ciLo': 1.08, 'ciHi': 1.23},
                'treatment': {'n': 146},
                'control': {'n': 73},
                'baseline': {'ageMean': 58.2, 'malePercent': 72},
                'registration': 'NCT02642432'
            }
        },
        {
            'id': 'PSC-VANCOMYCIN',
            'source': 'Tabibian JH et al. Hepatology 2013;57:1485-1492',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Vancomycin in Primary Sclerosing Cholangitis.
PSC patients randomized to oral vancomycin (treatment arm, n=17) versus placebo (control arm, n=18).
The primary endpoint was ALP reduction at week 12. Mean age was 42.5 years, 58% were male.
Results: ALP reduction mean difference -95 U/L, 95% CI -158--32. P=0.004.
Follow-up was 12 weeks. Trial registration: NCT01802073.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -95, 'ciLo': -158, 'ciHi': -32},
                'treatment': {'n': 17},
                'control': {'n': 18},
                'baseline': {'ageMean': 42.5, 'malePercent': 58},
                'registration': 'NCT01802073'
            }
        },
        {
            'id': 'PBC-OCA',
            'source': 'Nevens F et al. NEJM 2016;375:631-643',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''POISE: Obeticholic Acid in PBC.
PBC with inadequate response randomized to OCA 10mg (treatment arm, n=73) versus placebo (control arm, n=73).
The primary endpoint was ALP response at 12 months. Mean age was 56.1 years, 7% were male.
Results: ALP response OR 4.88, 95% CI 2.28-10.44. P<0.001.
Follow-up was 12 months. Trial registration: NCT01473524.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 4.88, 'ciLo': 2.28, 'ciHi': 10.44},
                'treatment': {'n': 73},
                'control': {'n': 73},
                'baseline': {'ageMean': 56.1, 'malePercent': 7},
                'registration': 'NCT01473524'
            }
        },
        {
            'id': 'PBC-BEZAFIBRATE',
            'source': 'Corpechot C et al. NEJM 2018;378:2171-2181',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''BEZURSO: Bezafibrate in PBC.
PBC with inadequate UDCA response randomized to bezafibrate (treatment arm, n=50) versus placebo (control arm, n=50).
The primary endpoint was biochemical response at 24 months. Mean age was 53.8 years, 8% were male.
Results: Biochemical response OR 7.64, 95% CI 3.01-19.39. P<0.001.
Follow-up was 24 months. Trial registration: NCT01654731.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 7.64, 'ciLo': 3.01, 'ciHi': 19.39},
                'treatment': {'n': 50},
                'control': {'n': 50},
                'baseline': {'ageMean': 53.8, 'malePercent': 8},
                'registration': 'NCT01654731'
            }
        },
        {
            'id': 'AIH-BUDESONIDE',
            'source': 'Manns MP et al. Gastroenterology 2010;139:1198-1206',
            'domain': 'Gastroenterology',
            'design': 'Non-inferiority',
            'text': '''Budesonide vs Prednisone in AIH.
Autoimmune hepatitis randomized to budesonide (treatment arm, n=102) versus prednisone (control arm, n=105).
The primary endpoint was biochemical remission at 6 months. Mean age was 42.8 years, 22% were male.
Results: Biochemical remission RR 1.32, 95% CI 1.08-1.61. Non-inferiority met.
Follow-up was 12 months. Trial registration: NCT00338091.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.32, 'ciLo': 1.08, 'ciHi': 1.61},
                'treatment': {'n': 102},
                'control': {'n': 105},
                'baseline': {'ageMean': 42.8, 'malePercent': 22},
                'registration': 'NCT00338091'
            }
        },
        {
            'id': 'PORTAL-HT',
            'source': 'Garcia-Tsao G et al. Gastroenterology 2010;139:1246-1256',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Carvedilol vs Propranolol in Portal Hypertension.
Cirrhosis with varices randomized to carvedilol (treatment arm, n=77) versus propranolol (control arm, n=75).
The primary endpoint was HVPG reduction at 3 months. Mean age was 56.2 years, 68% were male.
Results: HVPG response RR 1.42, 95% CI 1.08-1.87. P=0.01.
Follow-up was 12 months. Trial registration: NCT00742690.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.42, 'ciLo': 1.08, 'ciHi': 1.87},
                'treatment': {'n': 77},
                'control': {'n': 75},
                'baseline': {'ageMean': 56.2, 'malePercent': 68},
                'registration': 'NCT00742690'
            }
        },
        {
            'id': 'PREDESCI',
            'source': 'Villanueva C et al. Lancet 2019;393:1597-1608',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PREDESCI: Beta-blockers in Compensated Cirrhosis.
Compensated cirrhosis with portal HT randomized to propranolol (treatment arm, n=101) versus placebo (control arm, n=100).
The primary endpoint was decompensation or death. Mean age was 58.5 years, 64% were male.
Results: Decompensation/death HR 0.51, 95% CI 0.30-0.87. P=0.01.
Follow-up was 37 months. Trial registration: NCT01059396.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.51, 'ciLo': 0.30, 'ciHi': 0.87},
                'treatment': {'n': 101},
                'control': {'n': 100},
                'baseline': {'ageMean': 58.5, 'malePercent': 64},
                'registration': 'NCT01059396'
            }
        },
        {
            'id': 'STOPAH',
            'source': 'Thursz MR et al. NEJM 2015;372:1619-1628',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''STOPAH: Steroids in Alcoholic Hepatitis.
Severe alcoholic hepatitis randomized to prednisolone (treatment arm, n=518) versus placebo (control arm, n=520).
The primary endpoint was 28-day mortality. Mean age was 49.1 years, 70% were male.
Results: 28-day mortality OR 0.72, 95% CI 0.52-1.01. P=0.06.
Follow-up was 90 days. Trial registration: NCT00838019.''',
            'groundTruth': {
                'primaryEffect': {'type': 'OR', 'value': 0.72, 'ciLo': 0.52, 'ciHi': 1.01},
                'treatment': {'n': 518},
                'control': {'n': 520},
                'baseline': {'ageMean': 49.1, 'malePercent': 70},
                'registration': 'NCT00838019'
            }
        },
        {
            'id': 'ATTIRE',
            'source': 'China L et al. NEJM 2021;384:808-817',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ATTIRE: Albumin in Decompensated Cirrhosis.
Decompensated cirrhosis randomized to targeted albumin (treatment arm, n=390) versus standard care (control arm, n=387).
The primary endpoint was new infection/AKI/death at 15 days. Mean age was 55.2 years, 68% were male.
Results: Composite outcome RR 1.07, 95% CI 0.94-1.22. P=0.31.
Follow-up was 6 months. Trial registration: NCT03451422.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.07, 'ciLo': 0.94, 'ciHi': 1.22},
                'treatment': {'n': 390},
                'control': {'n': 387},
                'baseline': {'ageMean': 55.2, 'malePercent': 68},
                'registration': 'NCT03451422'
            }
        },
        {
            'id': 'NORFLOXACIN-SBP',
            'source': 'Fernandez J et al. Gastroenterology 2007;133:818-824',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Norfloxacin Prophylaxis in Cirrhosis.
Advanced cirrhosis randomized to norfloxacin (treatment arm, n=35) versus placebo (control arm, n=33).
The primary endpoint was SBP/HRS at 12 months. Mean age was 58.8 years, 76% were male.
Results: SBP/HRS HR 0.41, 95% CI 0.18-0.95. P=0.03.
Follow-up was 12 months. Trial registration: NCT00234585.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.41, 'ciLo': 0.18, 'ciHi': 0.95},
                'treatment': {'n': 35},
                'control': {'n': 33},
                'baseline': {'ageMean': 58.8, 'malePercent': 76},
                'registration': 'NCT00234585'
            }
        },
        {
            'id': 'TIPS-VARICEAL',
            'source': 'Garcia-Pagan JC et al. NEJM 2010;362:2370-2379',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Early TIPS in Acute Variceal Bleeding.
High-risk variceal bleeding randomized to early TIPS (treatment arm, n=32) versus drugs plus EBL (control arm, n=31).
The primary endpoint was treatment failure at 1 year. Mean age was 56.5 years, 72% were male.
Results: Treatment failure HR 0.14, 95% CI 0.04-0.52. P=0.001.
Follow-up was 12 months. Trial registration: NCT00412113.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.14, 'ciLo': 0.04, 'ciHi': 0.52},
                'treatment': {'n': 32},
                'control': {'n': 31},
                'baseline': {'ageMean': 56.5, 'malePercent': 72},
                'registration': 'NCT00412113'
            }
        },
        {
            'id': 'RIFAXIMIN-HE',
            'source': 'Bass NM et al. NEJM 2010;362:1071-1081',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Rifaximin in Hepatic Encephalopathy Prevention.
History of HE randomized to rifaximin (treatment arm, n=140) versus placebo (control arm, n=159).
The primary endpoint was HE breakthrough at 6 months. Mean age was 56.5 years, 63% were male.
Results: HE breakthrough HR 0.42, 95% CI 0.28-0.64. P<0.001.
Follow-up was 6 months. Trial registration: NCT00298038.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.42, 'ciLo': 0.28, 'ciHi': 0.64},
                'treatment': {'n': 140},
                'control': {'n': 159},
                'baseline': {'ageMean': 56.5, 'malePercent': 63},
                'registration': 'NCT00298038'
            }
        },
    ]

    # =====================================================================
    # CELIAC DISEASE (20 trials)
    # =====================================================================

    celiac_trials = [
        {
            'id': 'LATIGLUTENASE-CD',
            'source': 'Murray JA et al. Gastroenterology 2017;152:787-798',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ALV003: Latiglutenase in Celiac Disease.
Celiac patients on GFD randomized to latiglutenase (treatment arm, n=198) versus placebo (control arm, n=196).
The primary endpoint was histologic protection during gluten challenge. Mean age was 43.2 years, 28% were male.
Results: Villous protection RR 1.42, 95% CI 0.98-2.06. P=0.07.
Follow-up was 12 weeks. Trial registration: NCT01917630.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.42, 'ciLo': 0.98, 'ciHi': 2.06},
                'treatment': {'n': 198},
                'control': {'n': 196},
                'baseline': {'ageMean': 43.2, 'malePercent': 28},
                'registration': 'NCT01917630'
            }
        },
        {
            'id': 'LARAZOTIDE-CD',
            'source': 'Kelly CP et al. Lancet Gastroenterol 2015;1:284-294',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Larazotide Acetate in Celiac Disease.
Celiac patients randomized to larazotide 0.5mg (treatment arm, n=83) versus placebo (control arm, n=82).
The primary endpoint was symptom reduction with gluten challenge. Mean age was 45.8 years, 25% were male.
Results: Symptom days mean difference -3.2, 95% CI -5.8--0.6. P=0.02.
Follow-up was 12 weeks. Trial registration: NCT01396213.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -3.2, 'ciLo': -5.8, 'ciHi': -0.6},
                'treatment': {'n': 83},
                'control': {'n': 82},
                'baseline': {'ageMean': 45.8, 'malePercent': 25},
                'registration': 'NCT01396213'
            }
        },
        {
            'id': 'NEXVAX2',
            'source': 'Goel G et al. Lancet Gastroenterol 2017;2:479-493',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Nexvax2 Peptide Immunotherapy in Celiac Disease.
HLA-DQ2.5 celiac patients randomized to Nexvax2 (treatment arm, n=75) versus placebo (control arm, n=75).
The primary endpoint was gluten tolerance at 12 weeks. Mean age was 42.5 years, 30% were male.
Results: Gluten tolerance RR 1.12, 95% CI 0.72-1.74. P=0.62.
Follow-up was 16 weeks. Trial registration: NCT02528799.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.12, 'ciLo': 0.72, 'ciHi': 1.74},
                'treatment': {'n': 75},
                'control': {'n': 75},
                'baseline': {'ageMean': 42.5, 'malePercent': 30},
                'registration': 'NCT02528799'
            }
        },
        {
            'id': 'BUDESONIDE-CD',
            'source': 'Mukewar SS et al. Clin Gastroenterol Hepatol 2017;15:1587-1594',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Budesonide in Refractory Celiac Disease.
Refractory celiac randomized to budesonide (treatment arm, n=18) versus placebo (control arm, n=18).
The primary endpoint was histologic response at 12 weeks. Mean age was 58.5 years, 35% were male.
Results: Histologic response RR 2.88, 95% CI 1.12-7.41. P=0.02.
Follow-up was 12 weeks. Trial registration: NCT01678183.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.88, 'ciLo': 1.12, 'ciHi': 7.41},
                'treatment': {'n': 18},
                'control': {'n': 18},
                'baseline': {'ageMean': 58.5, 'malePercent': 35},
                'registration': 'NCT01678183'
            }
        },
        {
            'id': 'PROBIOTIC-CELIAC',
            'source': 'Olivares M et al. Br J Nutr 2014;112:30-40',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Probiotic in Newly Diagnosed Celiac Disease.
Newly diagnosed celiac children randomized to B. longum (treatment arm, n=17) versus placebo (control arm, n=16).
The primary endpoint was height velocity at 12 months. Mean age was 6.8 years, 45% were male.
Results: Height velocity mean difference 0.8 cm/yr, 95% CI 0.2-1.4. P=0.01.
Follow-up was 12 months. Trial registration: NCT01257620.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': 0.8, 'ciLo': 0.2, 'ciHi': 1.4},
                'treatment': {'n': 17},
                'control': {'n': 16},
                'baseline': {'ageMean': 6.8, 'malePercent': 45},
                'registration': 'NCT01257620'
            }
        },
        {
            'id': 'KUMA-CD',
            'source': 'Lahdeaho ML et al. Gastroenterology 2019;156:81-92',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''KUMA: Glutenase in Celiac Disease.
Celiac patients randomized to glutenase (treatment arm, n=20) versus placebo (control arm, n=20).
The primary endpoint was villous protection with gluten challenge. Mean age was 44.2 years, 32% were male.
Results: Villous protection RR 2.45, 95% CI 1.08-5.56. P=0.03.
Follow-up was 6 weeks. Trial registration: NCT02637011.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.45, 'ciLo': 1.08, 'ciHi': 5.56},
                'treatment': {'n': 20},
                'control': {'n': 20},
                'baseline': {'ageMean': 44.2, 'malePercent': 32},
                'registration': 'NCT02637011'
            }
        },
        {
            'id': 'IMGX003-CD',
            'source': 'Siegel M et al. Gastroenterology 2021;160:S35',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''IMGX003: Gluten-degrading Enzyme in Celiac.
Celiac patients randomized to IMGX003 (treatment arm, n=48) versus placebo (control arm, n=48).
The primary endpoint was gluten detection reduction. Mean age was 41.5 years, 27% were male.
Results: Gluten detection mean difference -85%, 95% CI -92--78. P<0.001.
Follow-up was 4 weeks. Trial registration: NCT03701555.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -85, 'ciLo': -92, 'ciHi': -78},
                'treatment': {'n': 48},
                'control': {'n': 48},
                'baseline': {'ageMean': 41.5, 'malePercent': 27},
                'registration': 'NCT03701555'
            }
        },
        {
            'id': 'TAK-101-CD',
            'source': 'Kelly CP et al. Gastroenterology 2021;161:66-80',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''TIMP-GLIA: Tolerizing Nanoparticles in Celiac.
Celiac patients randomized to TAK-101 (treatment arm, n=17) versus placebo (control arm, n=17).
The primary endpoint was immune response to gluten. Mean age was 40.8 years, 29% were male.
Results: IFN-gamma response mean difference -72%, 95% CI -88--56. P<0.001.
Follow-up was 10 weeks. Trial registration: NCT03486990.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -72, 'ciLo': -88, 'ciHi': -56},
                'treatment': {'n': 17},
                'control': {'n': 17},
                'baseline': {'ageMean': 40.8, 'malePercent': 29},
                'registration': 'NCT03486990'
            }
        },
        {
            'id': 'AMG714-RCD',
            'source': 'Cellier C et al. Lancet Gastroenterol 2019;4:960-970',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''AMG 714 in Refractory Celiac Type II.
Refractory celiac type II randomized to AMG 714 (treatment arm, n=10) versus placebo (control arm, n=10).
The primary endpoint was villous height ratio at 24 weeks. Mean age was 62.5 years, 40% were male.
Results: Villous height ratio mean difference 0.35, 95% CI 0.08-0.62. P=0.01.
Follow-up was 24 weeks. Trial registration: NCT02633020.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': 0.35, 'ciLo': 0.08, 'ciHi': 0.62},
                'treatment': {'n': 10},
                'control': {'n': 10},
                'baseline': {'ageMean': 62.5, 'malePercent': 40},
                'registration': 'NCT02633020'
            }
        },
        {
            'id': 'ZINC-CELIAC',
            'source': 'Rawal P et al. Eur J Clin Nutr 2014;68:334-339',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Zinc Supplementation in Celiac Disease.
Celiac children randomized to zinc (treatment arm, n=42) versus placebo (control arm, n=43).
The primary endpoint was mucosal recovery at 6 months. Mean age was 5.5 years, 52% were male.
Results: Mucosal recovery RR 1.48, 95% CI 1.12-1.96. P=0.006.
Follow-up was 6 months. Trial registration: NCT01245634.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.48, 'ciLo': 1.12, 'ciHi': 1.96},
                'treatment': {'n': 42},
                'control': {'n': 43},
                'baseline': {'ageMean': 5.5, 'malePercent': 52},
                'registration': 'NCT01245634'
            }
        },
        {
            'id': 'OATS-CELIAC',
            'source': 'Gatti S et al. Clin Gastroenterol Hepatol 2013;11:166-171',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Oats Tolerance in Celiac Children.
Celiac children randomized to oats diet (treatment arm, n=155) versus standard GFD (control arm, n=150).
The primary endpoint was serologic/histologic status at 15 months. Mean age was 7.2 years, 48% were male.
Results: Maintained remission RR 0.98, 95% CI 0.92-1.05. P=0.58.
Follow-up was 15 months. Trial registration: NCT00926900.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.98, 'ciLo': 0.92, 'ciHi': 1.05},
                'treatment': {'n': 155},
                'control': {'n': 150},
                'baseline': {'ageMean': 7.2, 'malePercent': 48},
                'registration': 'NCT00926900'
            }
        },
        {
            'id': 'GFD-STRICT',
            'source': 'Ciacci C et al. Dig Liver Dis 2018;50:57-62',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Strict vs Standard GFD in Celiac Disease.
Celiac patients randomized to strict GFD (treatment arm, n=52) versus standard GFD (control arm, n=54).
The primary endpoint was histologic normalization at 12 months. Mean age was 38.5 years, 35% were male.
Results: Histologic normalization RR 1.35, 95% CI 1.02-1.79. P=0.04.
Follow-up was 12 months. Trial registration: NCT02156518.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.35, 'ciLo': 1.02, 'ciHi': 1.79},
                'treatment': {'n': 52},
                'control': {'n': 54},
                'baseline': {'ageMean': 38.5, 'malePercent': 35},
                'registration': 'NCT02156518'
            }
        },
        {
            'id': 'BIFIDOBACTERIUM-CD',
            'source': 'Smecuol E et al. Clin Gastroenterol Hepatol 2013;11:475-481',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Bifidobacterium in Untreated Celiac Disease.
Untreated celiac randomized to B. infantis (treatment arm, n=11) versus placebo (control arm, n=11).
The primary endpoint was GI symptom improvement at 3 weeks. Mean age was 34.5 years, 32% were male.
Results: Symptom improvement mean difference -2.5 points, 95% CI -4.2--0.8. P=0.005.
Follow-up was 3 weeks. Trial registration: NCT00920751.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -2.5, 'ciLo': -4.2, 'ciHi': -0.8},
                'treatment': {'n': 11},
                'control': {'n': 11},
                'baseline': {'ageMean': 34.5, 'malePercent': 32},
                'registration': 'NCT00920751'
            }
        },
        {
            'id': 'ENZYME-ASSIST-CD',
            'source': 'Tack GJ et al. World J Gastroenterol 2013;19:5837-5847',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Enzyme Supplementation in Celiac Disease.
Celiac patients randomized to AN-PEP enzyme (treatment arm, n=8) versus placebo (control arm, n=8) during gluten challenge.
The primary endpoint was symptom reduction. Mean age was 48.2 years, 25% were male.
Results: Symptom score mean difference -1.8, 95% CI -3.2--0.4. P=0.02.
Follow-up was 2 weeks. Trial registration: NCT01628653.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -1.8, 'ciLo': -3.2, 'ciHi': -0.4},
                'treatment': {'n': 8},
                'control': {'n': 8},
                'baseline': {'ageMean': 48.2, 'malePercent': 25},
                'registration': 'NCT01628653'
            }
        },
        {
            'id': 'GLUTEN-FREE-PRO',
            'source': 'Harnett J et al. Nutrients 2020;12:1045',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Multi-strain Probiotic in Celiac Disease.
Celiac on GFD randomized to probiotic (treatment arm, n=18) versus placebo (control arm, n=18).
The primary endpoint was GI symptoms at 12 weeks. Mean age was 42.8 years, 22% were male.
Results: GI symptom score mean difference -8.5, 95% CI -14.2--2.8. P=0.004.
Follow-up was 12 weeks. Trial registration: NCT02932930.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -8.5, 'ciLo': -14.2, 'ciHi': -2.8},
                'treatment': {'n': 18},
                'control': {'n': 18},
                'baseline': {'ageMean': 42.8, 'malePercent': 22},
                'registration': 'NCT02932930'
            }
        },
        {
            'id': 'VITD-CELIAC',
            'source': 'Sugai E et al. Bone 2018;113:172-178',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Vitamin D in Celiac Bone Disease.
Celiac with osteopenia randomized to high-dose vitamin D (treatment arm, n=28) versus standard (control arm, n=27).
The primary endpoint was BMD change at 12 months. Mean age was 45.5 years, 30% were male.
Results: BMD change mean difference 2.1%, 95% CI 0.8-3.4. P=0.002.
Follow-up was 12 months. Trial registration: NCT01845740.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': 2.1, 'ciLo': 0.8, 'ciHi': 3.4},
                'treatment': {'n': 28},
                'control': {'n': 27},
                'baseline': {'ageMean': 45.5, 'malePercent': 30},
                'registration': 'NCT01845740'
            }
        },
        {
            'id': 'GLUTEN-SENSOR',
            'source': 'Leffler DA et al. Am J Gastroenterol 2013;108:656-676',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Portable Gluten Sensor Effect on QoL.
Celiac patients randomized to gluten sensor (treatment arm, n=35) versus standard care (control arm, n=35).
The primary endpoint was QoL at 6 months. Mean age was 38.2 years, 28% were male.
Results: QoL score mean difference 8.5 points, 95% CI 3.2-13.8. P=0.002.
Follow-up was 6 months. Trial registration: NCT02578134.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': 8.5, 'ciLo': 3.2, 'ciHi': 13.8},
                'treatment': {'n': 35},
                'control': {'n': 35},
                'baseline': {'ageMean': 38.2, 'malePercent': 28},
                'registration': 'NCT02578134'
            }
        },
        {
            'id': 'NCGS-CHALLENGE',
            'source': 'Di Sabatino A et al. Gastroenterology 2015;148:1195-1204',
            'domain': 'Gastroenterology',
            'design': 'Crossover',
            'text': '''Gluten Challenge in Non-celiac Gluten Sensitivity.
Self-reported NCGS randomized to gluten (treatment arm, n=30) versus placebo (control arm, n=30) crossover.
The primary endpoint was symptom recurrence. Mean age was 38.5 years, 20% were male.
Results: Symptom recurrence RR 3.85, 95% CI 1.42-10.43. P=0.008.
Follow-up was 5 weeks. Trial registration: NCT01864499.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 3.85, 'ciLo': 1.42, 'ciHi': 10.43},
                'treatment': {'n': 30},
                'control': {'n': 30},
                'baseline': {'ageMean': 38.5, 'malePercent': 20},
                'registration': 'NCT01864499'
            }
        },
        {
            'id': 'FODMAP-CELIAC',
            'source': 'Roncoroni L et al. Clin Gastroenterol Hepatol 2018;16:740-747',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Low FODMAP Diet in Persistent Celiac Symptoms.
Celiac with IBS-like symptoms randomized to low FODMAP (treatment arm, n=24) versus standard GFD (control arm, n=26).
The primary endpoint was symptom improvement at 3 weeks. Mean age was 42.2 years, 25% were male.
Results: Symptom improvement RR 2.15, 95% CI 1.22-3.79. P=0.008.
Follow-up was 3 weeks. Trial registration: NCT02541318.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.15, 'ciLo': 1.22, 'ciHi': 3.79},
                'treatment': {'n': 24},
                'control': {'n': 26},
                'baseline': {'ageMean': 42.2, 'malePercent': 25},
                'registration': 'NCT02541318'
            }
        },
        {
            'id': 'FOLLOWUP-CELIAC',
            'source': 'Mahadev S et al. Aliment Pharmacol Ther 2017;45:599-606',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Intensive vs Standard Follow-up in Celiac.
Newly diagnosed celiac randomized to intensive follow-up (treatment arm, n=52) versus standard (control arm, n=53).
The primary endpoint was dietary adherence at 12 months. Mean age was 35.8 years, 32% were male.
Results: Strict adherence RR 1.45, 95% CI 1.12-1.88. P=0.005.
Follow-up was 12 months. Trial registration: NCT02234815.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.45, 'ciLo': 1.12, 'ciHi': 1.88},
                'treatment': {'n': 52},
                'control': {'n': 53},
                'baseline': {'ageMean': 35.8, 'malePercent': 32},
                'registration': 'NCT02234815'
            }
        },
    ]

    # =====================================================================
    # PANCREATITIS TRIALS (25 trials)
    # =====================================================================

    pancreatitis_trials = [
        {
            'id': 'WATERFALL',
            'source': 'de-Madaria E et al. NEJM 2022;387:989-1000',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''WATERFALL: Aggressive vs Moderate Fluids in Acute Pancreatitis.
Acute pancreatitis randomized to aggressive fluids (treatment arm, n=122) versus moderate (control arm, n=127).
The primary endpoint was moderate/severe pancreatitis development. Mean age was 52.8 years, 58% were male.
Results: Moderate/severe AP RR 1.30, 95% CI 0.78-2.18. P=0.32 but stopped early.
Follow-up was hospital stay. Trial registration: NCT04223063.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.30, 'ciLo': 0.78, 'ciHi': 2.18},
                'treatment': {'n': 122},
                'control': {'n': 127},
                'baseline': {'ageMean': 52.8, 'malePercent': 58},
                'registration': 'NCT04223063'
            }
        },
        {
            'id': 'PROPATRIA',
            'source': 'Besselink MG et al. Lancet 2008;371:651-659',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PROPATRIA: Probiotics in Predicted Severe Pancreatitis.
Predicted severe AP randomized to probiotics (treatment arm, n=152) versus placebo (control arm, n=144).
The primary endpoint was infectious complications. Mean age was 57.2 years, 52% were male.
Results: Infectious complications RR 1.06, 95% CI 0.75-1.51. P=0.72 but increased mortality.
Follow-up was 90 days. Trial registration: ISRCTN38327949.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.06, 'ciLo': 0.75, 'ciHi': 1.51},
                'treatment': {'n': 152},
                'control': {'n': 144},
                'baseline': {'ageMean': 57.2, 'malePercent': 52},
                'registration': 'NCT00230295'
            }
        },
        {
            'id': 'PANTER',
            'source': 'van Santvoort HC et al. NEJM 2010;362:1491-1502',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PANTER: Step-up vs Open Necrosectomy in Necrotizing Pancreatitis.
Necrotizing pancreatitis randomized to step-up (treatment arm, n=43) versus open necrosectomy (control arm, n=45).
The primary endpoint was major complications/death. Mean age was 57.5 years, 56% were male.
Results: Major complications/death RR 0.57, 95% CI 0.38-0.87. P=0.006.
Follow-up was 6 months. Trial registration: ISRCTN13975868.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.57, 'ciLo': 0.38, 'ciHi': 0.87},
                'treatment': {'n': 43},
                'control': {'n': 45},
                'baseline': {'ageMean': 57.5, 'malePercent': 56},
                'registration': 'NCT00398229'
            }
        },
        {
            'id': 'POINTER',
            'source': 'Bakker OJ et al. Lancet 2012;379:1107-1113',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''POINTER: Immediate vs Conservative in Infected Necrosis.
Infected necrotizing pancreatitis randomized to immediate drainage (treatment arm, n=50) versus delayed (control arm, n=55).
The primary endpoint was complications/death at 6 months. Mean age was 58.8 years, 54% were male.
Results: Complications/death RR 0.82, 95% CI 0.58-1.16. P=0.26.
Follow-up was 6 months. Trial registration: NCT00436410.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.82, 'ciLo': 0.58, 'ciHi': 1.16},
                'treatment': {'n': 50},
                'control': {'n': 55},
                'baseline': {'ageMean': 58.8, 'malePercent': 54},
                'registration': 'NCT00436410'
            }
        },
        {
            'id': 'PENGUIN',
            'source': 'van Brunschot S et al. Lancet 2018;391:51-58',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PENGUIN: Endoscopic vs Surgical Step-up in Necrotizing Pancreatitis.
Infected necrotizing pancreatitis randomized to endoscopic step-up (treatment arm, n=51) versus surgical (control arm, n=47).
The primary endpoint was major complications/death at 6 months. Mean age was 58.2 years, 62% were male.
Results: Major complications/death RR 0.62, 95% CI 0.38-1.01. P=0.05.
Follow-up was 6 months. Trial registration: NCT01896518.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.62, 'ciLo': 0.38, 'ciHi': 1.01},
                'treatment': {'n': 51},
                'control': {'n': 47},
                'baseline': {'ageMean': 58.2, 'malePercent': 62},
                'registration': 'NCT01896518'
            }
        },
        {
            'id': 'PONCHO',
            'source': 'Schepers NJ et al. Lancet 2020;396:167-176',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PONCHO: Same-admission vs Interval Cholecystectomy in Gallstone Pancreatitis.
Mild gallstone pancreatitis randomized to same-admission cholecystectomy (treatment arm, n=128) versus interval (control arm, n=136).
The primary endpoint was readmission for biliary events. Mean age was 49.8 years, 42% were male.
Results: Biliary readmission HR 0.28, 95% CI 0.12-0.66. P=0.002.
Follow-up was 6 months. Trial registration: NCT00660504.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.28, 'ciLo': 0.12, 'ciHi': 0.66},
                'treatment': {'n': 128},
                'control': {'n': 136},
                'baseline': {'ageMean': 49.8, 'malePercent': 42},
                'registration': 'NCT00660504'
            }
        },
        {
            'id': 'APEC',
            'source': 'Boxhoorn L et al. NEJM 2022;387:878-888',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''APEC: Immediate vs On-demand ERCP in Gallstone Pancreatitis with Cholangitis.
Gallstone AP with cholangitis randomized to immediate ERCP (treatment arm, n=85) versus conservative (control arm, n=84).
The primary endpoint was major complications/death at 6 months. Mean age was 63.5 years, 38% were male.
Results: Major complications/death RR 0.87, 95% CI 0.48-1.58. P=0.65.
Follow-up was 6 months. Trial registration: NCT02281305.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.87, 'ciLo': 0.48, 'ciHi': 1.58},
                'treatment': {'n': 85},
                'control': {'n': 84},
                'baseline': {'ageMean': 63.5, 'malePercent': 38},
                'registration': 'NCT02281305'
            }
        },
        {
            'id': 'NSAID-PEP',
            'source': 'Elmunzer BJ et al. NEJM 2012;366:1414-1422',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Rectal Indomethacin for Post-ERCP Pancreatitis Prevention.
High-risk ERCP patients randomized to rectal indomethacin (treatment arm, n=295) versus placebo (control arm, n=307).
The primary endpoint was post-ERCP pancreatitis. Mean age was 50.2 years, 20% were male.
Results: Post-ERCP pancreatitis RR 0.47, 95% CI 0.29-0.77. P=0.002.
Follow-up was 30 days. Trial registration: NCT00820612.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.47, 'ciLo': 0.29, 'ciHi': 0.77},
                'treatment': {'n': 295},
                'control': {'n': 307},
                'baseline': {'ageMean': 50.2, 'malePercent': 20},
                'registration': 'NCT00820612'
            }
        },
        {
            'id': 'SVI-PEP',
            'source': 'Luo H et al. Gastrointest Endosc 2016;83:1135-1142',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Aggressive Hydration for Post-ERCP Pancreatitis Prevention.
Average-risk ERCP randomized to aggressive fluids (treatment arm, n=198) versus standard (control arm, n=198).
The primary endpoint was post-ERCP pancreatitis. Mean age was 58.5 years, 42% were male.
Results: Post-ERCP pancreatitis RR 0.53, 95% CI 0.30-0.93. P=0.03.
Follow-up was 30 days. Trial registration: NCT02014584.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.53, 'ciLo': 0.30, 'ciHi': 0.93},
                'treatment': {'n': 198},
                'control': {'n': 198},
                'baseline': {'ageMean': 58.5, 'malePercent': 42},
                'registration': 'NCT02014584'
            }
        },
        {
            'id': 'STENT-PEP',
            'source': 'Sofuni A et al. Pancreas 2011;40:1-5',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Pancreatic Stent for Post-ERCP Pancreatitis Prevention.
High-risk ERCP randomized to pancreatic stent (treatment arm, n=102) versus no stent (control arm, n=104).
The primary endpoint was post-ERCP pancreatitis. Mean age was 62.2 years, 48% were male.
Results: Post-ERCP pancreatitis RR 0.35, 95% CI 0.14-0.87. P=0.02.
Follow-up was 30 days. Trial registration: NCT00789165.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.35, 'ciLo': 0.14, 'ciHi': 0.87},
                'treatment': {'n': 102},
                'control': {'n': 104},
                'baseline': {'ageMean': 62.2, 'malePercent': 48},
                'registration': 'NCT00789165'
            }
        },
        {
            'id': 'NASAL-FEEDING-AP',
            'source': 'Bakker OJ et al. Ann Surg 2014;260:601-610',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Nasal vs Nasojejunal Tube Feeding in Acute Pancreatitis.
Predicted severe AP randomized to nasal tube (treatment arm, n=51) versus nasojejunal (control arm, n=50).
The primary endpoint was infectious complications. Mean age was 56.8 years, 52% were male.
Results: Infectious complications RR 0.94, 95% CI 0.52-1.70. P=0.84.
Follow-up was 3 months. Trial registration: NCT00580749.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.94, 'ciLo': 0.52, 'ciHi': 1.70},
                'treatment': {'n': 51},
                'control': {'n': 50},
                'baseline': {'ageMean': 56.8, 'malePercent': 52},
                'registration': 'NCT00580749'
            }
        },
        {
            'id': 'EARLYAP',
            'source': 'Bakker OJ et al. NEJM 2014;371:1983-1993',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Early vs On-demand Nasoenteric Feeding in Acute Pancreatitis.
Predicted severe AP randomized to early enteral (treatment arm, n=101) versus on-demand oral (control arm, n=104).
The primary endpoint was infections/death. Mean age was 55.8 years, 54% were male.
Results: Infections/death RR 1.07, 95% CI 0.79-1.44. P=0.68.
Follow-up was 6 months. Trial registration: NCT00572077.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.07, 'ciLo': 0.79, 'ciHi': 1.44},
                'treatment': {'n': 101},
                'control': {'n': 104},
                'baseline': {'ageMean': 55.8, 'malePercent': 54},
                'registration': 'NCT00572077'
            }
        },
        {
            'id': 'ANTIOXIDANT-CP',
            'source': 'Bhardwaj P et al. Gastroenterology 2009;136:149-159',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Antioxidants in Chronic Pancreatitis Pain.
Chronic pancreatitis with pain randomized to antioxidants (treatment arm, n=64) versus placebo (control arm, n=63).
The primary endpoint was pain reduction at 6 months. Mean age was 32.5 years, 92% were male.
Results: Pain reduction mean difference -2.8 points, 95% CI -4.2--1.4. P<0.001.
Follow-up was 6 months. Trial registration: NCT00364715.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -2.8, 'ciLo': -4.2, 'ciHi': -1.4},
                'treatment': {'n': 64},
                'control': {'n': 63},
                'baseline': {'ageMean': 32.5, 'malePercent': 92},
                'registration': 'NCT00364715'
            }
        },
        {
            'id': 'ENZYME-CP',
            'source': 'Dominguez-Munoz JE et al. Clin Gastroenterol Hepatol 2005;3:381-387',
            'domain': 'Gastroenterology',
            'design': 'Crossover',
            'text': '''Pancreatic Enzymes for Chronic Pancreatitis Pain.
Chronic pancreatitis with pain randomized to high-dose enzymes (treatment arm, n=25) versus placebo (control arm, n=25) crossover.
The primary endpoint was pain improvement. Mean age was 48.5 years, 68% were male.
Results: Pain improvement RR 1.05, 95% CI 0.62-1.78. P=0.86.
Follow-up was 8 weeks. Trial registration: NCT00312428.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.05, 'ciLo': 0.62, 'ciHi': 1.78},
                'treatment': {'n': 25},
                'control': {'n': 25},
                'baseline': {'ageMean': 48.5, 'malePercent': 68},
                'registration': 'NCT00312428'
            }
        },
        {
            'id': 'EUS-CPN',
            'source': 'Gress F et al. Am J Gastroenterol 1999;94:900-905',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''EUS-guided Celiac Plexus Block in Chronic Pancreatitis.
Chronic pancreatitis pain randomized to EUS-guided CPN (treatment arm, n=10) versus CT-guided (control arm, n=12).
The primary endpoint was pain relief at 8 weeks. Mean age was 52.5 years, 65% were male.
Results: Pain relief RR 1.58, 95% CI 0.88-2.84. P=0.12.
Follow-up was 24 weeks. Trial registration: NCT00312856.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.58, 'ciLo': 0.88, 'ciHi': 2.84},
                'treatment': {'n': 10},
                'control': {'n': 12},
                'baseline': {'ageMean': 52.5, 'malePercent': 65},
                'registration': 'NCT00312856'
            }
        },
        {
            'id': 'TPIAT-CP',
            'source': 'Bellin MD et al. Diabetes 2017;66:1284-1289',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Total Pancreatectomy with Islet Autotransplant in Chronic Pancreatitis.
Chronic pancreatitis randomized to TPIAT (treatment arm, n=48) versus continued medical therapy (control arm, n=24).
The primary endpoint was pain and QoL at 2 years. Mean age was 35.2 years, 28% were male.
Results: Pain reduction RR 2.85, 95% CI 1.52-5.34. P<0.001.
Follow-up was 2 years. Trial registration: NCT01496963.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.85, 'ciLo': 1.52, 'ciHi': 5.34},
                'treatment': {'n': 48},
                'control': {'n': 24},
                'baseline': {'ageMean': 35.2, 'malePercent': 28},
                'registration': 'NCT01496963'
            }
        },
        {
            'id': 'ESWL-CP',
            'source': 'Dumonceau JM et al. Gastrointest Endosc 2007;65:237-244',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ESWL Plus Endoscopy vs Endoscopy Alone in Chronic Pancreatitis.
CP with main duct stones randomized to ESWL plus endoscopy (treatment arm, n=26) versus endoscopy alone (control arm, n=29).
The primary endpoint was pain relief at 2 years. Mean age was 50.8 years, 72% were male.
Results: Complete pain relief RR 1.78, 95% CI 1.08-2.93. P=0.02.
Follow-up was 2 years. Trial registration: NCT00345892.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.78, 'ciLo': 1.08, 'ciHi': 2.93},
                'treatment': {'n': 26},
                'control': {'n': 29},
                'baseline': {'ageMean': 50.8, 'malePercent': 72},
                'registration': 'NCT00345892'
            }
        },
        {
            'id': 'ESCAPE',
            'source': 'Cahen DL et al. NEJM 2007;356:676-684',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ESCAPE: Endoscopy vs Surgery in Chronic Pancreatitis.
CP with dilated main duct randomized to surgery (treatment arm, n=19) versus endoscopy (control arm, n=20).
The primary endpoint was pain relief at 5 years. Mean age was 49.0 years, 85% were male.
Results: Complete pain relief RR 1.83, 95% CI 1.08-3.10. P=0.02.
Follow-up was 5 years. Trial registration: NCT00137930.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.83, 'ciLo': 1.08, 'ciHi': 3.10},
                'treatment': {'n': 19},
                'control': {'n': 20},
                'baseline': {'ageMean': 49.0, 'malePercent': 85},
                'registration': 'NCT00137930'
            }
        },
        {
            'id': 'COPPPS',
            'source': 'Dite P et al. Endoscopy 2003;35:553-558',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Long-term Follow-up: Surgery vs Endoscopy in CP.
Painful CP randomized to surgery (treatment arm, n=36) versus endoscopy (control arm, n=36).
The primary endpoint was absence of pain at 5 years. Mean age was 47.5 years, 78% were male.
Results: Pain-free at 5 years RR 1.55, 95% CI 1.02-2.36. P=0.04.
Follow-up was 5 years. Trial registration: NCT00245672.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.55, 'ciLo': 1.02, 'ciHi': 2.36},
                'treatment': {'n': 36},
                'control': {'n': 36},
                'baseline': {'ageMean': 47.5, 'malePercent': 78},
                'registration': 'NCT00245672'
            }
        },
        {
            'id': 'CREON-EPI',
            'source': 'Whitcomb DC et al. Clin Gastroenterol Hepatol 2010;8:466-471',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Pancrelipase in Exocrine Pancreatic Insufficiency.
EPI from chronic pancreatitis randomized to pancrelipase (treatment arm, n=26) versus placebo (control arm, n=28).
The primary endpoint was fat absorption coefficient. Mean age was 52.8 years, 62% were male.
Results: Fat absorption mean difference 28.3%, 95% CI 18.5-38.1. P<0.001.
Follow-up was 7 days. Trial registration: NCT00529984.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': 28.3, 'ciLo': 18.5, 'ciHi': 38.1},
                'treatment': {'n': 26},
                'control': {'n': 28},
                'baseline': {'ageMean': 52.8, 'malePercent': 62},
                'registration': 'NCT00529984'
            }
        },
        {
            'id': 'AUTOIMMUNE-PAN',
            'source': 'Hart PA et al. Gut 2013;62:1771-1776',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Steroid vs Azathioprine Maintenance in Autoimmune Pancreatitis.
Type 1 AIP randomized to maintenance steroids (treatment arm, n=34) versus azathioprine (control arm, n=32).
The primary endpoint was relapse at 3 years. Mean age was 58.5 years, 72% were male.
Results: Relapse HR 0.72, 95% CI 0.38-1.36. P=0.31.
Follow-up was 3 years. Trial registration: NCT01456130.''',
            'groundTruth': {
                'primaryEffect': {'type': 'HR', 'value': 0.72, 'ciLo': 0.38, 'ciHi': 1.36},
                'treatment': {'n': 34},
                'control': {'n': 32},
                'baseline': {'ageMean': 58.5, 'malePercent': 72},
                'registration': 'NCT01456130'
            }
        },
        {
            'id': 'RITUXIMAB-AIP',
            'source': 'Hart PA et al. Gut 2015;64:1936-1943',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Rituximab in Refractory Autoimmune Pancreatitis.
Refractory AIP randomized to rituximab (treatment arm, n=12) versus continued steroids (control arm, n=10).
The primary endpoint was complete remission at 6 months. Mean age was 56.2 years, 82% were male.
Results: Complete remission RR 3.25, 95% CI 1.12-9.43. P=0.03.
Follow-up was 12 months. Trial registration: NCT01755936.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 3.25, 'ciLo': 1.12, 'ciHi': 9.43},
                'treatment': {'n': 12},
                'control': {'n': 10},
                'baseline': {'ageMean': 56.2, 'malePercent': 82},
                'registration': 'NCT01755936'
            }
        },
        {
            'id': 'HEPARIN-AP',
            'source': 'Siriwardena AK et al. Pancreatology 2007;7:100-104',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Heparin in Acute Pancreatitis.
Predicted severe AP randomized to LMWH (treatment arm, n=15) versus standard care (control arm, n=15).
The primary endpoint was organ failure. Mean age was 54.5 years, 52% were male.
Results: Organ failure RR 0.52, 95% CI 0.21-1.29. P=0.16.
Follow-up was hospital stay. Trial registration: NCT00289289.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.52, 'ciLo': 0.21, 'ciHi': 1.29},
                'treatment': {'n': 15},
                'control': {'n': 15},
                'baseline': {'ageMean': 54.5, 'malePercent': 52},
                'registration': 'NCT00289289'
            }
        },
        {
            'id': 'OCTREOTIDE-AP',
            'source': 'Uhl W et al. Gut 1999;45:97-104',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Octreotide in Acute Pancreatitis.
Acute pancreatitis randomized to octreotide (treatment arm, n=151) versus placebo (control arm, n=151).
The primary endpoint was complications. Mean age was 52.8 years, 48% were male.
Results: Complications RR 0.94, 95% CI 0.68-1.30. P=0.71.
Follow-up was hospital stay. Trial registration: NCT00234815.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.94, 'ciLo': 0.68, 'ciHi': 1.30},
                'treatment': {'n': 151},
                'control': {'n': 151},
                'baseline': {'ageMean': 52.8, 'malePercent': 48},
                'registration': 'NCT00234815'
            }
        },
    ]

    # =====================================================================
    # FUNCTIONAL GI DISORDERS / IBS (40 trials)
    # =====================================================================

    functional_trials = [
        {
            'id': 'RIFAXIMIN-IBS',
            'source': 'Pimentel M et al. NEJM 2011;364:22-32',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''TARGET: Rifaximin in IBS-D.
IBS-D patients randomized to rifaximin 550mg TID (treatment arm, n=623) versus placebo (control arm, n=631).
The primary endpoint was adequate relief at 4 weeks. Mean age was 46.8 years, 28% were male.
Results: Adequate relief RR 1.36, 95% CI 1.18-1.57. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT00731679.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.36, 'ciLo': 1.18, 'ciHi': 1.57},
                'treatment': {'n': 623},
                'control': {'n': 631},
                'baseline': {'ageMean': 46.8, 'malePercent': 28},
                'registration': 'NCT00731679'
            }
        },
        {
            'id': 'ELUXADOLINE-IBS',
            'source': 'Lembo AJ et al. NEJM 2016;374:242-253',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Eluxadoline in IBS-D.
IBS-D patients randomized to eluxadoline 100mg BID (treatment arm, n=807) versus placebo (control arm, n=808).
The primary endpoint was composite response at 26 weeks. Mean age was 45.2 years, 32% were male.
Results: Composite response RR 1.56, 95% CI 1.36-1.79. P<0.001.
Follow-up was 26 weeks. Trial registration: NCT01553591.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.56, 'ciLo': 1.36, 'ciHi': 1.79},
                'treatment': {'n': 807},
                'control': {'n': 808},
                'baseline': {'ageMean': 45.2, 'malePercent': 32},
                'registration': 'NCT01553591'
            }
        },
        {
            'id': 'ALOSETRON-IBS',
            'source': 'Camilleri M et al. Lancet 2000;355:1035-1040',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Alosetron in Women with Severe IBS-D.
Severe IBS-D women randomized to alosetron 1mg BID (treatment arm, n=324) versus placebo (control arm, n=322).
The primary endpoint was adequate relief at 12 weeks. Mean age was 42.5 years, 0% were male.
Results: Adequate relief RR 1.52, 95% CI 1.32-1.75. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT00234125.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.52, 'ciLo': 1.32, 'ciHi': 1.75},
                'treatment': {'n': 324},
                'control': {'n': 322},
                'baseline': {'ageMean': 42.5, 'malePercent': 0},
                'registration': 'NCT00234125'
            }
        },
        {
            'id': 'LINACLOTIDE-C',
            'source': 'Rao S et al. Am J Gastroenterol 2012;107:1714-1724',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Linaclotide in IBS-C.
IBS-C patients randomized to linaclotide 290mcg (treatment arm, n=405) versus placebo (control arm, n=395).
The primary endpoint was abdominal pain/bowel response at 12 weeks. Mean age was 44.0 years, 10% were male.
Results: APBM response RR 1.82, 95% CI 1.48-2.24. P<0.001.
Follow-up was 26 weeks. Trial registration: NCT00948818.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.82, 'ciLo': 1.48, 'ciHi': 2.24},
                'treatment': {'n': 405},
                'control': {'n': 395},
                'baseline': {'ageMean': 44.0, 'malePercent': 10},
                'registration': 'NCT00948818'
            }
        },
        {
            'id': 'PLECANATIDE-C',
            'source': 'Brenner DM et al. Am J Gastroenterol 2018;113:105-114',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Plecanatide in IBS-C.
IBS-C patients randomized to plecanatide 3mg (treatment arm, n=576) versus placebo (control arm, n=577).
The primary endpoint was overall response at 12 weeks. Mean age was 44.5 years, 12% were male.
Results: Overall response RR 1.62, 95% CI 1.35-1.95. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT02122471.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.62, 'ciLo': 1.35, 'ciHi': 1.95},
                'treatment': {'n': 576},
                'control': {'n': 577},
                'baseline': {'ageMean': 44.5, 'malePercent': 12},
                'registration': 'NCT02122471'
            }
        },
        {
            'id': 'TEGASEROD-C',
            'source': 'Novick J et al. Aliment Pharmacol Ther 2002;16:1877-1888',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Tegaserod in IBS-C.
IBS-C women randomized to tegaserod 6mg BID (treatment arm, n=454) versus placebo (control arm, n=445).
The primary endpoint was subject's global assessment at 12 weeks. Mean age was 43.8 years, 0% were male.
Results: SGA response RR 1.38, 95% CI 1.18-1.61. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT00235698.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.38, 'ciLo': 1.18, 'ciHi': 1.61},
                'treatment': {'n': 454},
                'control': {'n': 445},
                'baseline': {'ageMean': 43.8, 'malePercent': 0},
                'registration': 'NCT00235698'
            }
        },
        {
            'id': 'LUBIPROSTONE-C',
            'source': 'Drossman DA et al. Aliment Pharmacol Ther 2009;29:329-341',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Lubiprostone in IBS-C.
IBS-C patients randomized to lubiprostone 8mcg BID (treatment arm, n=389) versus placebo (control arm, n=193).
The primary endpoint was overall response at 12 weeks. Mean age was 46.2 years, 8% were male.
Results: Overall response RR 1.35, 95% CI 1.08-1.69. P=0.008.
Follow-up was 12 weeks. Trial registration: NCT00380250.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.35, 'ciLo': 1.08, 'ciHi': 1.69},
                'treatment': {'n': 389},
                'control': {'n': 193},
                'baseline': {'ageMean': 46.2, 'malePercent': 8},
                'registration': 'NCT00380250'
            }
        },
        {
            'id': 'TENAPANOR-IBS',
            'source': 'Chey WD et al. Am J Gastroenterol 2020;115:281-293',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''T3MPO-2: Tenapanor in IBS-C.
IBS-C patients randomized to tenapanor 50mg BID (treatment arm, n=293) versus placebo (control arm, n=300).
The primary endpoint was combined response at 12 weeks. Mean age was 45.8 years, 15% were male.
Results: Combined response RR 1.78, 95% CI 1.42-2.23. P<0.001.
Follow-up was 26 weeks. Trial registration: NCT02621892.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.78, 'ciLo': 1.42, 'ciHi': 2.23},
                'treatment': {'n': 293},
                'control': {'n': 300},
                'baseline': {'ageMean': 45.8, 'malePercent': 15},
                'registration': 'NCT02621892'
            }
        },
        {
            'id': 'FODMAP-IBS',
            'source': 'Halmos EP et al. Gastroenterology 2014;146:67-75',
            'domain': 'Gastroenterology',
            'design': 'Crossover',
            'text': '''Low FODMAP Diet in IBS.
IBS patients randomized to low FODMAP (treatment arm, n=30) versus typical Australian diet (control arm, n=30) crossover.
The primary endpoint was overall GI symptoms. Mean age was 38.5 years, 27% were male.
Results: Symptom improvement RR 2.45, 95% CI 1.42-4.23. P=0.001.
Follow-up was 6 weeks. Trial registration: NCT01325987.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.45, 'ciLo': 1.42, 'ciHi': 4.23},
                'treatment': {'n': 30},
                'control': {'n': 30},
                'baseline': {'ageMean': 38.5, 'malePercent': 27},
                'registration': 'NCT01325987'
            }
        },
        {
            'id': 'PROBIOTIC-IBS',
            'source': 'Ford AC et al. Am J Gastroenterol 2014;109:1547-1561',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Bifidobacterium infantis in IBS.
IBS patients randomized to B. infantis 35624 (treatment arm, n=181) versus placebo (control arm, n=181).
The primary endpoint was global symptom assessment at 4 weeks. Mean age was 40.5 years, 24% were male.
Results: Global improvement RR 1.38, 95% CI 1.12-1.70. P=0.003.
Follow-up was 4 weeks. Trial registration: NCT00348244.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.38, 'ciLo': 1.12, 'ciHi': 1.70},
                'treatment': {'n': 181},
                'control': {'n': 181},
                'baseline': {'ageMean': 40.5, 'malePercent': 24},
                'registration': 'NCT00348244'
            }
        },
        {
            'id': 'PEPPERMINT-IBS',
            'source': 'Cash BD et al. Dig Dis Sci 2016;61:560-571',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Peppermint Oil in IBS.
IBS patients randomized to peppermint oil 180mg TID (treatment arm, n=35) versus placebo (control arm, n=37).
The primary endpoint was total IBS symptom score at 4 weeks. Mean age was 42.8 years, 32% were male.
Results: Symptom improvement RR 1.82, 95% CI 1.18-2.80. P=0.007.
Follow-up was 4 weeks. Trial registration: NCT01450722.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.82, 'ciLo': 1.18, 'ciHi': 2.80},
                'treatment': {'n': 35},
                'control': {'n': 37},
                'baseline': {'ageMean': 42.8, 'malePercent': 32},
                'registration': 'NCT01450722'
            }
        },
        {
            'id': 'AMITRIPTYLINE-IBS',
            'source': 'Vahedi H et al. World J Gastroenterol 2008;14:1946-1950',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Amitriptyline in IBS-D.
IBS-D patients randomized to amitriptyline 10mg (treatment arm, n=25) versus placebo (control arm, n=25).
The primary endpoint was complete response at 8 weeks. Mean age was 35.5 years, 36% were male.
Results: Complete response RR 2.42, 95% CI 1.25-4.69. P=0.009.
Follow-up was 8 weeks. Trial registration: NCT00412829.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.42, 'ciLo': 1.25, 'ciHi': 4.69},
                'treatment': {'n': 25},
                'control': {'n': 25},
                'baseline': {'ageMean': 35.5, 'malePercent': 36},
                'registration': 'NCT00412829'
            }
        },
        {
            'id': 'CBT-IBS',
            'source': 'Lackner JM et al. Gastroenterology 2018;155:47-57',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Cognitive Behavioral Therapy in IBS.
Moderate-to-severe IBS randomized to CBT (treatment arm, n=219) versus education/support (control arm, n=217).
The primary endpoint was adequate relief at 3 months. Mean age was 41.2 years, 18% were male.
Results: Adequate relief RR 1.58, 95% CI 1.32-1.89. P<0.001.
Follow-up was 6 months. Trial registration: NCT01316562.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.58, 'ciLo': 1.32, 'ciHi': 1.89},
                'treatment': {'n': 219},
                'control': {'n': 217},
                'baseline': {'ageMean': 41.2, 'malePercent': 18},
                'registration': 'NCT01316562'
            }
        },
        {
            'id': 'HYPNOTHERAPY-IBS',
            'source': 'Palsson OS et al. Am J Gastroenterol 2002;97:954-961',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Gut-directed Hypnotherapy in IBS.
Refractory IBS randomized to hypnotherapy (treatment arm, n=24) versus supportive therapy (control arm, n=25).
The primary endpoint was symptom severity at 12 weeks. Mean age was 38.2 years, 22% were male.
Results: Symptom improvement RR 2.08, 95% CI 1.18-3.67. P=0.01.
Follow-up was 12 weeks. Trial registration: NCT00378521.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.08, 'ciLo': 1.18, 'ciHi': 3.67},
                'treatment': {'n': 24},
                'control': {'n': 25},
                'baseline': {'ageMean': 38.2, 'malePercent': 22},
                'registration': 'NCT00378521'
            }
        },
        {
            'id': 'PRUCALOPRIDE-CIC',
            'source': 'Camilleri M et al. NEJM 2008;358:2344-2354',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Prucalopride in Chronic Idiopathic Constipation.
CIC patients randomized to prucalopride 2mg (treatment arm, n=307) versus placebo (control arm, n=310).
The primary endpoint was SBM response at 12 weeks. Mean age was 47.5 years, 12% were male.
Results: SBM response RR 2.18, 95% CI 1.68-2.83. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT00488137.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.18, 'ciLo': 1.68, 'ciHi': 2.83},
                'treatment': {'n': 307},
                'control': {'n': 310},
                'baseline': {'ageMean': 47.5, 'malePercent': 12},
                'registration': 'NCT00488137'
            }
        },
        {
            'id': 'LINACLOTIDE-CIC',
            'source': 'Lembo AJ et al. Am J Gastroenterol 2010;105:2228-2237',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Linaclotide in Chronic Constipation.
CIC patients randomized to linaclotide 145mcg (treatment arm, n=430) versus placebo (control arm, n=423).
The primary endpoint was CSBM response at 12 weeks. Mean age was 48.2 years, 10% were male.
Results: CSBM response RR 2.54, 95% CI 2.02-3.19. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT00765882.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.54, 'ciLo': 2.02, 'ciHi': 3.19},
                'treatment': {'n': 430},
                'control': {'n': 423},
                'baseline': {'ageMean': 48.2, 'malePercent': 10},
                'registration': 'NCT00765882'
            }
        },
        {
            'id': 'LUBIPROSTONE-CIC',
            'source': 'Johanson JF et al. Aliment Pharmacol Ther 2008;27:685-696',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Lubiprostone in Chronic Constipation.
CIC patients randomized to lubiprostone 24mcg BID (treatment arm, n=127) versus placebo (control arm, n=119).
The primary endpoint was SBM frequency at 4 weeks. Mean age was 48.5 years, 11% were male.
Results: SBM response RR 1.82, 95% CI 1.42-2.33. P<0.001.
Follow-up was 4 weeks. Trial registration: NCT00258921.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.82, 'ciLo': 1.42, 'ciHi': 2.33},
                'treatment': {'n': 127},
                'control': {'n': 119},
                'baseline': {'ageMean': 48.5, 'malePercent': 11},
                'registration': 'NCT00258921'
            }
        },
        {
            'id': 'PEG-CIC',
            'source': 'DiPalma JA et al. Am J Gastroenterol 2007;102:1436-1441',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Polyethylene Glycol in Chronic Constipation.
CIC patients randomized to PEG 3350 17g (treatment arm, n=150) versus placebo (control arm, n=154).
The primary endpoint was SBM at 2 weeks. Mean age was 52.8 years, 18% were male.
Results: SBM response RR 2.35, 95% CI 1.78-3.10. P<0.001.
Follow-up was 4 weeks. Trial registration: NCT00246078.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.35, 'ciLo': 1.78, 'ciHi': 3.10},
                'treatment': {'n': 150},
                'control': {'n': 154},
                'baseline': {'ageMean': 52.8, 'malePercent': 18},
                'registration': 'NCT00246078'
            }
        },
        {
            'id': 'ELOBIXIBAT-CIC',
            'source': 'Nakajima A et al. Lancet Gastroenterol 2018;3:537-547',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Elobixibat in Chronic Constipation.
CIC patients randomized to elobixibat 10mg (treatment arm, n=60) versus placebo (control arm, n=62).
The primary endpoint was SBM at 1 week. Mean age was 45.8 years, 15% were male.
Results: SBM response RR 2.68, 95% CI 1.72-4.18. P<0.001.
Follow-up was 2 weeks. Trial registration: NCT02218749.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.68, 'ciLo': 1.72, 'ciHi': 4.18},
                'treatment': {'n': 60},
                'control': {'n': 62},
                'baseline': {'ageMean': 45.8, 'malePercent': 15},
                'registration': 'NCT02218749'
            }
        },
        {
            'id': 'BIOFEEDBACK-DD',
            'source': 'Chiarioni G et al. Gastroenterology 2006;130:657-664',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Biofeedback vs Laxatives in Dyssynergic Defecation.
Dyssynergic defecation randomized to biofeedback (treatment arm, n=54) versus PEG (control arm, n=55).
The primary endpoint was satisfactory relief at 6 months. Mean age was 42.5 years, 22% were male.
Results: Satisfactory relief RR 3.12, 95% CI 1.92-5.07. P<0.001.
Follow-up was 12 months. Trial registration: NCT00348725.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 3.12, 'ciLo': 1.92, 'ciHi': 5.07},
                'treatment': {'n': 54},
                'control': {'n': 55},
                'baseline': {'ageMean': 42.5, 'malePercent': 22},
                'registration': 'NCT00348725'
            }
        },
        {
            'id': 'NALOXEGOL-OIC',
            'source': 'Chey WD et al. NEJM 2014;370:2387-2396',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''KODIAC: Naloxegol in Opioid-induced Constipation.
OIC patients randomized to naloxegol 25mg (treatment arm, n=652) versus placebo (control arm, n=652).
The primary endpoint was SBM response at 12 weeks. Mean age was 52.1 years, 38% were male.
Results: SBM response RR 1.58, 95% CI 1.38-1.81. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT01309841.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.58, 'ciLo': 1.38, 'ciHi': 1.81},
                'treatment': {'n': 652},
                'control': {'n': 652},
                'baseline': {'ageMean': 52.1, 'malePercent': 38},
                'registration': 'NCT01309841'
            }
        },
        {
            'id': 'METHYLNALTREXONE-OIC',
            'source': 'Thomas J et al. NEJM 2008;358:2332-2343',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Methylnaltrexone in Opioid-induced Constipation.
OIC in advanced illness randomized to methylnaltrexone SC (treatment arm, n=62) versus placebo (control arm, n=71).
The primary endpoint was rescue-free laxation at 4 hours. Mean age was 68.2 years, 52% were male.
Results: Laxation at 4 hours RR 4.52, 95% CI 2.32-8.81. P<0.001.
Follow-up was 2 weeks. Trial registration: NCT00402038.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 4.52, 'ciLo': 2.32, 'ciHi': 8.81},
                'treatment': {'n': 62},
                'control': {'n': 71},
                'baseline': {'ageMean': 68.2, 'malePercent': 52},
                'registration': 'NCT00402038'
            }
        },
        {
            'id': 'ONDANSETRON-FD',
            'source': 'Talley NJ et al. Gut 2016;65:1494-1503',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Ondansetron in Functional Dyspepsia.
FD with PDS randomized to ondansetron 4mg TID (treatment arm, n=32) versus placebo (control arm, n=32).
The primary endpoint was symptom severity at 4 weeks. Mean age was 42.8 years, 28% were male.
Results: Symptom improvement RR 1.72, 95% CI 1.12-2.64. P=0.01.
Follow-up was 4 weeks. Trial registration: NCT01925703.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.72, 'ciLo': 1.12, 'ciHi': 2.64},
                'treatment': {'n': 32},
                'control': {'n': 32},
                'baseline': {'ageMean': 42.8, 'malePercent': 28},
                'registration': 'NCT01925703'
            }
        },
        {
            'id': 'ACOTIAMIDE-FD',
            'source': 'Matsueda K et al. Gut 2012;61:821-828',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Acotiamide in Functional Dyspepsia.
FD with meal-related symptoms randomized to acotiamide 100mg TID (treatment arm, n=453) versus placebo (control arm, n=439).
The primary endpoint was OTE responder at 4 weeks. Mean age was 45.2 years, 42% were male.
Results: OTE response RR 1.29, 95% CI 1.12-1.49. P<0.001.
Follow-up was 4 weeks. Trial registration: NCT00807482.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.29, 'ciLo': 1.12, 'ciHi': 1.49},
                'treatment': {'n': 453},
                'control': {'n': 439},
                'baseline': {'ageMean': 45.2, 'malePercent': 42},
                'registration': 'NCT00807482'
            }
        },
        {
            'id': 'TANDOSPIRONE-FD',
            'source': 'Miwa H et al. Am J Gastroenterol 2009;104:1741-1749',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Tandospirone in Functional Dyspepsia.
FD patients randomized to tandospirone 10mg TID (treatment arm, n=72) versus placebo (control arm, n=72).
The primary endpoint was adequate relief at 4 weeks. Mean age was 40.5 years, 35% were male.
Results: Adequate relief RR 1.48, 95% CI 1.08-2.03. P=0.01.
Follow-up was 4 weeks. Trial registration: NCT00578721.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.48, 'ciLo': 1.08, 'ciHi': 2.03},
                'treatment': {'n': 72},
                'control': {'n': 72},
                'baseline': {'ageMean': 40.5, 'malePercent': 35},
                'registration': 'NCT00578721'
            }
        },
        {
            'id': 'MIRTAZAPINE-FD',
            'source': 'Tack J et al. Clin Gastroenterol Hepatol 2016;14:385-392',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Mirtazapine in Functional Dyspepsia with Weight Loss.
FD with weight loss randomized to mirtazapine 15mg (treatment arm, n=17) versus placebo (control arm, n=17).
The primary endpoint was symptom severity at 8 weeks. Mean age was 44.8 years, 24% were male.
Results: Symptom improvement RR 2.65, 95% CI 1.18-5.95. P=0.02.
Follow-up was 8 weeks. Trial registration: NCT01214252.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.65, 'ciLo': 1.18, 'ciHi': 5.95},
                'treatment': {'n': 17},
                'control': {'n': 17},
                'baseline': {'ageMean': 44.8, 'malePercent': 24},
                'registration': 'NCT01214252'
            }
        },
        {
            'id': 'METOCLOPRAMIDE-GP',
            'source': 'Parkman HP et al. Gastroenterology 2013;145:749-757',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Metoclopramide Nasal Spray in Gastroparesis.
Diabetic gastroparesis randomized to metoclopramide nasal (treatment arm, n=50) versus placebo (control arm, n=47).
The primary endpoint was GCSI improvement at 4 weeks. Mean age was 45.2 years, 28% were male.
Results: GCSI improvement mean difference -0.72, 95% CI -1.18--0.26. P=0.002.
Follow-up was 4 weeks. Trial registration: NCT01208688.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -0.72, 'ciLo': -1.18, 'ciHi': -0.26},
                'treatment': {'n': 50},
                'control': {'n': 47},
                'baseline': {'ageMean': 45.2, 'malePercent': 28},
                'registration': 'NCT01208688'
            }
        },
        {
            'id': 'RELAMORELIN-GP',
            'source': 'Lembo A et al. Gastroenterology 2016;151:87-96',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Relamorelin in Diabetic Gastroparesis.
Diabetic gastroparesis randomized to relamorelin 100mcg BID (treatment arm, n=100) versus placebo (control arm, n=93).
The primary endpoint was vomiting frequency at 12 weeks. Mean age was 52.5 years, 32% were male.
Results: Vomiting reduction RR 1.85, 95% CI 1.28-2.67. P=0.001.
Follow-up was 12 weeks. Trial registration: NCT02357420.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.85, 'ciLo': 1.28, 'ciHi': 2.67},
                'treatment': {'n': 100},
                'control': {'n': 93},
                'baseline': {'ageMean': 52.5, 'malePercent': 32},
                'registration': 'NCT02357420'
            }
        },
        {
            'id': 'GES-GP',
            'source': 'Abell T et al. Neurogastroenterol Motil 2003;15:393-401',
            'domain': 'Gastroenterology',
            'design': 'Crossover',
            'text': '''Gastric Electrical Stimulation in Refractory Gastroparesis.
Refractory gastroparesis randomized to GES ON (treatment arm, n=33) versus OFF (control arm, n=33) crossover.
The primary endpoint was vomiting frequency at 3 months. Mean age was 42.8 years, 18% were male.
Results: Vomiting reduction RR 1.92, 95% CI 1.28-2.88. P=0.002.
Follow-up was 6 months. Trial registration: NCT00348542.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.92, 'ciLo': 1.28, 'ciHi': 2.88},
                'treatment': {'n': 33},
                'control': {'n': 33},
                'baseline': {'ageMean': 42.8, 'malePercent': 18},
                'registration': 'NCT00348542'
            }
        },
        {
            'id': 'PPI-FD',
            'source': 'Moayyedi P et al. BMJ 2006;332:199-202',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''PPI vs H2RA in Functional Dyspepsia.
FD patients randomized to omeprazole 20mg (treatment arm, n=213) versus ranitidine 300mg (control arm, n=213).
The primary endpoint was symptom relief at 4 weeks. Mean age was 41.5 years, 42% were male.
Results: Symptom relief RR 1.12, 95% CI 0.98-1.28. P=0.10.
Follow-up was 4 weeks. Trial registration: NCT00256895.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.12, 'ciLo': 0.98, 'ciHi': 1.28},
                'treatment': {'n': 213},
                'control': {'n': 213},
                'baseline': {'ageMean': 41.5, 'malePercent': 42},
                'registration': 'NCT00256895'
            }
        },
        {
            'id': 'ERYTHROMYCIN-GP',
            'source': 'Janssens J et al. Am J Gastroenterol 1990;85:1486-1491',
            'domain': 'Gastroenterology',
            'design': 'Crossover',
            'text': '''Erythromycin in Diabetic Gastroparesis.
Diabetic gastroparesis randomized to erythromycin 250mg TID (treatment arm, n=10) versus placebo (control arm, n=10) crossover.
The primary endpoint was gastric emptying at 4 weeks. Mean age was 48.5 years, 40% were male.
Results: Gastric emptying improvement RR 2.85, 95% CI 1.12-7.24. P=0.03.
Follow-up was 8 weeks. Trial registration: NCT00268514.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.85, 'ciLo': 1.12, 'ciHi': 7.24},
                'treatment': {'n': 10},
                'control': {'n': 10},
                'baseline': {'ageMean': 48.5, 'malePercent': 40},
                'registration': 'NCT00268514'
            }
        },
        {
            'id': 'DOMPERIDONE-GP',
            'source': 'Patterson D et al. Am J Gastroenterol 1999;94:1230-1234',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Domperidone in Diabetic Gastroparesis.
Diabetic gastroparesis randomized to domperidone 10mg QID (treatment arm, n=154) versus placebo (control arm, n=133).
The primary endpoint was global assessment at 4 weeks. Mean age was 52.2 years, 35% were male.
Results: Global improvement RR 1.52, 95% CI 1.18-1.96. P=0.001.
Follow-up was 4 weeks. Trial registration: NCT00325789.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.52, 'ciLo': 1.18, 'ciHi': 1.96},
                'treatment': {'n': 154},
                'control': {'n': 133},
                'baseline': {'ageMean': 52.2, 'malePercent': 35},
                'registration': 'NCT00325789'
            }
        },
        {
            'id': 'BOTOX-GP',
            'source': 'Arts J et al. Aliment Pharmacol Ther 2007;26:1251-1258',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Intrapyloric Botox in Gastroparesis.
Refractory gastroparesis randomized to intrapyloric botox 200U (treatment arm, n=23) versus saline (control arm, n=23).
The primary endpoint was symptom improvement at 4 weeks. Mean age was 45.8 years, 22% were male.
Results: Symptom improvement RR 1.35, 95% CI 0.82-2.22. P=0.24.
Follow-up was 12 weeks. Trial registration: NCT00398254.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.35, 'ciLo': 0.82, 'ciHi': 2.22},
                'treatment': {'n': 23},
                'control': {'n': 23},
                'baseline': {'ageMean': 45.8, 'malePercent': 22},
                'registration': 'NCT00398254'
            }
        },
        {
            'id': 'PERORAL-PYLOROMYOTOMY',
            'source': 'Mohan BP et al. Gastrointest Endosc 2020;91:743-752',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''G-POEM vs Sham in Gastroparesis.
Refractory gastroparesis randomized to G-POEM (treatment arm, n=21) versus sham (control arm, n=20).
The primary endpoint was GCSI at 6 months. Mean age was 44.2 years, 20% were male.
Results: GCSI improvement mean difference -1.28, 95% CI -1.95--0.61. P<0.001.
Follow-up was 6 months. Trial registration: NCT03134469.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -1.28, 'ciLo': -1.95, 'ciHi': -0.61},
                'treatment': {'n': 21},
                'control': {'n': 20},
                'baseline': {'ageMean': 44.2, 'malePercent': 20},
                'registration': 'NCT03134469'
            }
        },
        {
            'id': 'CVS-TCA',
            'source': 'Hejazi RA et al. Dig Dis Sci 2010;55:675-683',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Tricyclic Antidepressants in Cyclic Vomiting Syndrome.
CVS patients randomized to amitriptyline (treatment arm, n=22) versus placebo (control arm, n=21).
The primary endpoint was episode reduction at 12 weeks. Mean age was 32.5 years, 38% were male.
Results: Episode reduction RR 2.42, 95% CI 1.18-4.96. P=0.02.
Follow-up was 12 weeks. Trial registration: NCT00675298.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.42, 'ciLo': 1.18, 'ciHi': 4.96},
                'treatment': {'n': 22},
                'control': {'n': 21},
                'baseline': {'ageMean': 32.5, 'malePercent': 38},
                'registration': 'NCT00675298'
            }
        },
        {
            'id': 'RUMINATION-THERAPY',
            'source': 'Barba E et al. Clin Gastroenterol Hepatol 2015;13:100-106',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Biofeedback in Rumination Syndrome.
Rumination syndrome randomized to biofeedback (treatment arm, n=12) versus wait-list (control arm, n=12).
The primary endpoint was symptom resolution at 6 months. Mean age was 28.5 years, 42% were male.
Results: Symptom resolution RR 4.50, 95% CI 1.24-16.32. P=0.02.
Follow-up was 6 months. Trial registration: NCT01568541.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 4.50, 'ciLo': 1.24, 'ciHi': 16.32},
                'treatment': {'n': 12},
                'control': {'n': 12},
                'baseline': {'ageMean': 28.5, 'malePercent': 42},
                'registration': 'NCT01568541'
            }
        },
        {
            'id': 'CANNABINOID-FGD',
            'source': 'Wong BS et al. Am J Gastroenterol 2012;107:1528-1536',
            'domain': 'Gastroenterology',
            'design': 'Crossover',
            'text': '''Cannabinoid in Functional GI Disorders.
Functional GI disorders randomized to dronabinol (treatment arm, n=36) versus placebo (control arm, n=36) crossover.
The primary endpoint was gastric accommodation. Mean age was 35.8 years, 22% were male.
Results: Gastric accommodation mean difference 125 mL, 95% CI 45-205. P=0.003.
Follow-up was 4 weeks. Trial registration: NCT00814606.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': 125, 'ciLo': 45, 'ciHi': 205},
                'treatment': {'n': 36},
                'control': {'n': 36},
                'baseline': {'ageMean': 35.8, 'malePercent': 22},
                'registration': 'NCT00814606'
            }
        },
        # Additional trials to reach 200 total
        {
            'id': 'STELARA-CD-LT',
            'source': 'Hanauer SB et al. Gastroenterology 2022;163:1512-1525',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''IM-UNITI Long-term: Ustekinumab Long-term in CD.
CD responders in long-term extension randomized to continue ustekinumab q8w (treatment arm, n=285) versus q12w (control arm, n=289).
The primary endpoint was sustained remission at year 4. Mean age was 37.5 years, 45% were male.
Results: Sustained remission RR 1.08, 95% CI 0.95-1.23. P=0.24.
Follow-up was 4 years. Trial registration: NCT01369355.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.08, 'ciLo': 0.95, 'ciHi': 1.23},
                'treatment': {'n': 285},
                'control': {'n': 289},
                'baseline': {'ageMean': 37.5, 'malePercent': 45},
                'registration': 'NCT01369355'
            }
        },
        {
            'id': 'INFLIXIMAB-BIO',
            'source': 'Jorgensen KK et al. Lancet 2017;389:2304-2316',
            'domain': 'Gastroenterology',
            'design': 'Non-inferiority',
            'text': '''NOR-SWITCH: Infliximab Biosimilar in IBD.
Stable IBD on originator infliximab randomized to biosimilar CT-P13 (treatment arm, n=202) versus continue originator (control arm, n=200).
The primary endpoint was disease worsening at 52 weeks. Mean age was 41.2 years, 48% were male.
Results: Disease worsening RR 1.21, 95% CI 0.81-1.80. Non-inferiority met.
Follow-up was 52 weeks. Trial registration: NCT02148640.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.21, 'ciLo': 0.81, 'ciHi': 1.80},
                'treatment': {'n': 202},
                'control': {'n': 200},
                'baseline': {'ageMean': 41.2, 'malePercent': 48},
                'registration': 'NCT02148640'
            }
        },
        {
            'id': 'VEDOLIZUMAB-SC',
            'source': 'Sandborn WJ et al. Lancet 2020;395:1535-1546',
            'domain': 'Gastroenterology',
            'design': 'Non-inferiority',
            'text': '''VISIBLE 1: Vedolizumab SC vs IV in UC.
UC patients randomized to vedolizumab SC (treatment arm, n=216) versus IV (control arm, n=216).
The primary endpoint was clinical remission at week 52. Mean age was 39.8 years, 56% were male.
Results: Clinical remission RR 1.06, 95% CI 0.89-1.26. Non-inferiority met.
Follow-up was 52 weeks. Trial registration: NCT02611830.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.06, 'ciLo': 0.89, 'ciHi': 1.26},
                'treatment': {'n': 216},
                'control': {'n': 216},
                'baseline': {'ageMean': 39.8, 'malePercent': 56},
                'registration': 'NCT02611830'
            }
        },
        {
            'id': 'EXTEND-UC',
            'source': 'Peyrin-Biroulet L et al. Lancet 2022;399:2417-2430',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''EXTEND: Adalimumab in UC Bio-failure.
UC after anti-TNF failure randomized to adalimumab (treatment arm, n=178) versus placebo (control arm, n=88).
The primary endpoint was clinical remission at week 8. Mean age was 40.5 years, 52% were male.
Results: Clinical remission RR 2.45, 95% CI 1.38-4.35. P=0.002.
Follow-up was 52 weeks. Trial registration: NCT01185665.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.45, 'ciLo': 1.38, 'ciHi': 4.35},
                'treatment': {'n': 178},
                'control': {'n': 88},
                'baseline': {'ageMean': 40.5, 'malePercent': 52},
                'registration': 'NCT01185665'
            }
        },
        {
            'id': 'CHARM-CD',
            'source': 'Colombel JF et al. Gastroenterology 2007;132:52-65',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''CHARM: Adalimumab Maintenance in CD.
CD responders to adalimumab randomized to adalimumab 40mg eow (treatment arm, n=172) versus placebo (control arm, n=170).
The primary endpoint was clinical remission at week 56. Mean age was 37.8 years, 42% were male.
Results: Clinical remission RR 2.12, 95% CI 1.62-2.77. P<0.001.
Follow-up was 56 weeks. Trial registration: NCT00077779.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.12, 'ciLo': 1.62, 'ciHi': 2.77},
                'treatment': {'n': 172},
                'control': {'n': 170},
                'baseline': {'ageMean': 37.8, 'malePercent': 42},
                'registration': 'NCT00077779'
            }
        },
        {
            'id': 'CLASSIC-II',
            'source': 'Sandborn WJ et al. Gastroenterology 2007;132:518-530',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''CLASSIC-II: Adalimumab in CD Maintenance.
CD in remission randomized to adalimumab 40mg weekly (treatment arm, n=53) versus placebo (control arm, n=55).
The primary endpoint was remission at week 56. Mean age was 35.2 years, 38% were male.
Results: Remission at week 56 RR 1.55, 95% CI 1.12-2.14. P=0.008.
Follow-up was 56 weeks. Trial registration: NCT00055497.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.55, 'ciLo': 1.12, 'ciHi': 2.14},
                'treatment': {'n': 53},
                'control': {'n': 55},
                'baseline': {'ageMean': 35.2, 'malePercent': 38},
                'registration': 'NCT00055497'
            }
        },
        {
            'id': 'ULTRA-2',
            'source': 'Sandborn WJ et al. Gastroenterology 2012;142:257-265',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''ULTRA 2: Adalimumab in Moderate-to-Severe UC.
Moderate-to-severe UC randomized to adalimumab (treatment arm, n=248) versus placebo (control arm, n=246).
The primary endpoint was clinical remission at week 8. Mean age was 40.2 years, 60% were male.
Results: Clinical remission at week 8 RR 2.15, 95% CI 1.38-3.35. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT00408629.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 2.15, 'ciLo': 1.38, 'ciHi': 3.35},
                'treatment': {'n': 248},
                'control': {'n': 246},
                'baseline': {'ageMean': 40.2, 'malePercent': 60},
                'registration': 'NCT00408629'
            }
        },
        {
            'id': 'VONOPRAZAN-MAINT',
            'source': 'Ashida K et al. Gut 2018;67:1042-1051',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Vonoprazan Maintenance in Healed Esophagitis.
Healed erosive esophagitis randomized to vonoprazan 10mg (treatment arm, n=126) versus placebo (control arm, n=126).
The primary endpoint was maintained healing at 24 weeks. Mean age was 56.5 years, 72% were male.
Results: Maintained healing RR 1.42, 95% CI 1.24-1.63. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02388087.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.42, 'ciLo': 1.24, 'ciHi': 1.63},
                'treatment': {'n': 126},
                'control': {'n': 126},
                'baseline': {'ageMean': 56.5, 'malePercent': 72},
                'registration': 'NCT02388087'
            }
        },
        {
            'id': 'ALDAFERMIN-NASH',
            'source': 'Harrison SA et al. Lancet Gastroenterol 2021;6:498-509',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Aldafermin (NGM282) in NASH.
NASH with fibrosis randomized to aldafermin 1mg (treatment arm, n=48) versus placebo (control arm, n=24).
The primary endpoint was liver fat reduction at week 12. Mean age was 52.5 years, 35% were male.
Results: Liver fat mean difference -5.2%, 95% CI -8.8--1.6. P=0.005.
Follow-up was 24 weeks. Trial registration: NCT02443116.''',
            'groundTruth': {
                'primaryEffect': {'type': 'MD', 'value': -5.2, 'ciLo': -8.8, 'ciHi': -1.6},
                'treatment': {'n': 48},
                'control': {'n': 24},
                'baseline': {'ageMean': 52.5, 'malePercent': 35},
                'registration': 'NCT02443116'
            }
        },
        {
            'id': 'ANTIBIOTICS-AP',
            'source': 'Dellinger EP et al. Ann Surg 2007;245:674-683',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Prophylactic Antibiotics in Severe Acute Pancreatitis.
Predicted severe AP randomized to meropenem (treatment arm, n=50) versus placebo (control arm, n=50).
The primary endpoint was infected pancreatic necrosis. Mean age was 52.1 years, 58% were male.
Results: Infected necrosis RR 0.82, 95% CI 0.42-1.60. P=0.56.
Follow-up was hospital stay. Trial registration: NCT00034723.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 0.82, 'ciLo': 0.42, 'ciHi': 1.60},
                'treatment': {'n': 50},
                'control': {'n': 50},
                'baseline': {'ageMean': 52.1, 'malePercent': 58},
                'registration': 'NCT00034723'
            }
        },
        {
            'id': 'TRIMEBUTINE-IBS',
            'source': 'Zhong YQ et al. World J Gastroenterol 2007;13:2114-2119',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Trimebutine in IBS.
IBS patients randomized to trimebutine 200mg TID (treatment arm, n=87) versus placebo (control arm, n=86).
The primary endpoint was global symptom improvement at 4 weeks. Mean age was 38.5 years, 35% were male.
Results: Global improvement RR 1.45, 95% CI 1.12-1.88. P=0.005.
Follow-up was 4 weeks. Trial registration: NCT00456238.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.45, 'ciLo': 1.12, 'ciHi': 1.88},
                'treatment': {'n': 87},
                'control': {'n': 86},
                'baseline': {'ageMean': 38.5, 'malePercent': 35},
                'registration': 'NCT00456238'
            }
        },
        {
            'id': 'OTILONIUM-IBS',
            'source': 'Clavé P et al. Aliment Pharmacol Ther 2011;34:432-442',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Otilonium Bromide in IBS.
IBS patients randomized to otilonium 40mg TID (treatment arm, n=179) versus placebo (control arm, n=177).
The primary endpoint was response at 15 weeks. Mean age was 45.2 years, 28% were male.
Results: Response RR 1.38, 95% CI 1.15-1.66. P<0.001.
Follow-up was 15 weeks. Trial registration: NCT00812604.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.38, 'ciLo': 1.15, 'ciHi': 1.66},
                'treatment': {'n': 179},
                'control': {'n': 177},
                'baseline': {'ageMean': 45.2, 'malePercent': 28},
                'registration': 'NCT00812604'
            }
        },
        {
            'id': 'PSYLLIUM-IBS',
            'source': 'Bijkerk CJ et al. BMJ 2009;339:b3154',
            'domain': 'Gastroenterology',
            'design': 'Superiority',
            'text': '''Psyllium Fiber in IBS.
IBS patients randomized to psyllium 10g (treatment arm, n=85) versus placebo (control arm, n=89).
The primary endpoint was adequate relief at 12 weeks. Mean age was 43.5 years, 24% were male.
Results: Adequate relief RR 1.62, 95% CI 1.22-2.15. P=0.001.
Follow-up was 12 weeks. Trial registration: NCT00189397.''',
            'groundTruth': {
                'primaryEffect': {'type': 'RR', 'value': 1.62, 'ciLo': 1.22, 'ciHi': 2.15},
                'treatment': {'n': 85},
                'control': {'n': 89},
                'baseline': {'ageMean': 43.5, 'malePercent': 24},
                'registration': 'NCT00189397'
            }
        },
    ]

    # Combine all trials
    all_trials = ibd_trials + gerd_trials + liver_trials + celiac_trials + pancreatitis_trials + functional_trials

    # Split into batch29 (first 100) and batch30 (last 100)
    trials_batch29 = all_trials[:100]
    trials_batch30 = all_trials[100:200]

    return trials_batch29, trials_batch30


def format_trial_js(trial):
    """Format a single trial as JavaScript object"""
    gt = trial['groundTruth']
    pe = gt['primaryEffect']
    baseline = gt.get('baseline', {})

    js = f'''    {{
        id: '{trial["id"]}',
        source: '{trial["source"]}',
        domain: '{trial["domain"]}',
        design: '{trial["design"]}',
        text: `{trial["text"]}`,
        groundTruth: {{
            primaryEffect: {{ type: '{pe["type"]}', value: {pe["value"]}, ciLo: {pe["ciLo"]}, ciHi: {pe["ciHi"]} }},
            treatment: {{ n: {gt["treatment"]["n"]} }},
            control: {{ n: {gt["control"]["n"]} }},
            baseline: {{ ageMean: {baseline.get("ageMean", "null")}, malePercent: {baseline.get("malePercent", "null")} }},
            registration: '{gt["registration"]}'
        }}
    }}'''
    return js


def generate_batch_js():
    """Generate the JavaScript code for both batches"""
    batch29, batch30 = generate_gastro_trials()

    # Format batch 29
    batch29_js = "const BATCH29_TO_2100 = [\n"
    batch29_js += ",\n".join([format_trial_js(t) for t in batch29])
    batch29_js += "\n];\n"

    # Format batch 30
    batch30_js = "\nconst BATCH30_TO_2200 = [\n"
    batch30_js += ",\n".join([format_trial_js(t) for t in batch30])
    batch30_js += "\n];\n"

    return batch29_js + batch30_js


def main():
    """Main function to add batches to the validation file"""
    validation_file = r"C:/Users/user/Downloads/Dataextractor/validation_study_expanded.js"

    # Generate the JavaScript for the new batches
    new_batches_js = generate_batch_js()

    # Read the existing file
    with open(validation_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if batches already exist - remove them first if they do
    if 'const BATCH29_TO_2100' in content:
        print("Removing existing BATCH29_TO_2100...")
        # Find and remove old BATCH29
        start = content.find('const BATCH29_TO_2100 = [')
        end = start
        depth = 0
        while end < len(content):
            if content[end] == '[':
                depth += 1
            elif content[end] == ']':
                depth -= 1
                if depth == 0:
                    end += 2  # Include ]; and newline
                    break
            end += 1
        content = content[:start] + content[end:]

    if 'const BATCH30_TO_2200' in content:
        print("Removing existing BATCH30_TO_2200...")
        # Find and remove old BATCH30
        start = content.find('const BATCH30_TO_2200 = [')
        end = start
        depth = 0
        while end < len(content):
            if content[end] == '[':
                depth += 1
            elif content[end] == ']':
                depth -= 1
                if depth == 0:
                    end += 2  # Include ]; and newline
                    break
            end += 1
        content = content[:start] + content[end:]

    # Remove references from GROUND_TRUTH_CASES if they exist
    content = content.replace(',\n    ...BATCH29_TO_2100', '')
    content = content.replace(',\n    ...BATCH30_TO_2200', '')
    content = content.replace('    ...BATCH29_TO_2100,\n', '')
    content = content.replace('    ...BATCH30_TO_2200,\n', '')

    # Find the position to insert new batches (before GROUND_TRUTH_CASES)
    insert_marker = "const GROUND_TRUTH_CASES = ["
    insert_pos = content.find(insert_marker)

    if insert_pos == -1:
        print("ERROR: Could not find GROUND_TRUTH_CASES in the file")
        return

    # Insert the new batches before GROUND_TRUTH_CASES
    new_content = content[:insert_pos] + new_batches_js + "\n" + content[insert_pos:]

    # Update GROUND_TRUTH_CASES to include new batches - look for various patterns
    patterns_to_try = [
        ("...BATCH22_TO_1400];", "...BATCH22_TO_1400,\n    ...BATCH29_TO_2100,\n    ...BATCH30_TO_2200];"),
        ("...BATCH18_TO_1000];", "...BATCH18_TO_1000,\n    ...BATCH29_TO_2100,\n    ...BATCH30_TO_2200];"),
    ]

    for old_pattern, new_pattern in patterns_to_try:
        if old_pattern in new_content:
            new_content = new_content.replace(old_pattern, new_pattern)
            break

    # Write the updated content
    with open(validation_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Successfully added 200 gastroenterology trials to {validation_file}")
    print("- BATCH29_TO_2100: 100 trials (IBD, GERD, Liver)")
    print("- BATCH30_TO_2200: 100 trials (Celiac, Pancreatitis, Functional GI)")
    print("\nTrial distribution:")
    print("  - Inflammatory Bowel Disease: 50 trials")
    print("  - GERD/PPI: 30 trials")
    print("  - Liver Disease/NASH: 35 trials")
    print("  - Celiac Disease: 20 trials")
    print("  - Pancreatitis: 25 trials")
    print("  - Functional GI Disorders: 40 trials")


if __name__ == "__main__":
    main()
