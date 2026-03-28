#!/usr/bin/env python3
"""Add batch 15 trials (100 new diverse RCTs)."""

file_path = r"C:\Users\user\Downloads\Dataextractor\validation_study_expanded.js"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check current count
current_count = content.count("id: '")
print(f"Current trial count: {current_count}")

batch15_trials = """
    // ===========================================
    // BATCH 15: Trials 663-762 (100 new RCTs)
    // ===========================================

    // RHEUMATOLOGY (20 trials)
    {
        id: 'SELECT-AXIS-1',
        source: 'van der Heijde D et al. Lancet 2019;394:2108-2117',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `SELECT-AXIS 1: Upadacitinib in Ankylosing Spondylitis.
Active AS patients randomized to upadacitinib (treatment arm, n=93) versus placebo (control arm, n=94).
The primary endpoint was ASAS40 at 14 weeks. Mean age was 45.2 years, 71% were male.
Results: ASAS40 RR 2.68, 95% CI 1.72-4.18. P<0.001.
Follow-up was 14 weeks. Trial registration: NCT03178487.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.68, ciLo: 1.72, ciHi: 4.18 },
            treatment: { n: 93 },
            control: { n: 94 },
            baseline: { ageMean: 45.2, malePercent: 71 },
            registration: 'NCT03178487'
        }
    },
    {
        id: 'MEASURE-1',
        source: 'Baeten D et al. NEJM 2015;373:2534-2548',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `MEASURE 1: Secukinumab in Ankylosing Spondylitis.
AS patients randomized to secukinumab (treatment arm, n=125) versus placebo (control arm, n=122).
The primary endpoint was ASAS20 at 16 weeks. Mean age was 42.3 years, 70% were male.
Results: ASAS20 RR 2.13, 95% CI 1.58-2.87. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01358175.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.13, ciLo: 1.58, ciHi: 2.87 },
            treatment: { n: 125 },
            control: { n: 122 },
            baseline: { ageMean: 42.3, malePercent: 70 },
            registration: 'NCT01358175'
        }
    },
    {
        id: 'SPIRIT-P1',
        source: 'Mease P et al. Ann Rheum Dis 2017;76:79-87',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `SPIRIT-P1: Ixekizumab in Psoriatic Arthritis.
Biologic-naive PsA patients randomized to ixekizumab (treatment arm, n=107) versus placebo (control arm, n=106).
The primary endpoint was ACR20 at 24 weeks. Mean age was 49.5 years, 52% were male.
Results: ACR20 RR 2.98, 95% CI 2.14-4.15. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT01695239.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.98, ciLo: 2.14, ciHi: 4.15 },
            treatment: { n: 107 },
            control: { n: 106 },
            baseline: { ageMean: 49.5, malePercent: 52 },
            registration: 'NCT01695239'
        }
    },
    {
        id: 'OPAL-Broaden',
        source: 'Mease P et al. NEJM 2017;377:1537-1550',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `OPAL Broaden: Tofacitinib in Psoriatic Arthritis.
PsA patients with inadequate csDMARD response randomized to tofacitinib (treatment arm, n=107) versus placebo (control arm, n=105).
The primary endpoint was ACR20 at 3 months. Mean age was 48.6 years, 47% were male.
Results: ACR20 RR 1.92, 95% CI 1.41-2.61. P<0.001.
Follow-up was 12 months. Trial registration: NCT01877668.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.92, ciLo: 1.41, ciHi: 2.61 },
            treatment: { n: 107 },
            control: { n: 105 },
            baseline: { ageMean: 48.6, malePercent: 47 },
            registration: 'NCT01877668'
        }
    },
    {
        id: 'ORAL-Shift',
        source: 'Burmester GR et al. Lancet 2017;389:1492-1501',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `ORAL Shift: Tofacitinib Monotherapy vs MTX Switch in RA.
RA patients with MTX inadequate response randomized to tofacitinib monotherapy (treatment arm, n=315) versus MTX continuation (control arm, n=160).
The primary endpoint was ACR20 at 24 weeks. Mean age was 52.1 years, 18% were male.
Results: ACR20 RR 1.41, 95% CI 1.19-1.67. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02092467.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.41, ciLo: 1.19, ciHi: 1.67 },
            treatment: { n: 315 },
            control: { n: 160 },
            baseline: { ageMean: 52.1, malePercent: 18 },
            registration: 'NCT02092467'
        }
    },
    {
        id: 'GIANA-1',
        source: 'Takeuchi T et al. Arthritis Rheumatol 2019;71:1987-1996',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `GIANA-1: Filgotinib in Japanese RA Patients.
Japanese RA patients randomized to filgotinib (treatment arm, n=100) versus placebo (control arm, n=50).
The primary endpoint was ACR20 at 12 weeks. Mean age was 54.2 years, 15% were male.
Results: ACR20 RR 2.64, 95% CI 1.65-4.22. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02873936.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.64, ciLo: 1.65, ciHi: 4.22 },
            treatment: { n: 100 },
            control: { n: 50 },
            baseline: { ageMean: 54.2, malePercent: 15 },
            registration: 'NCT02873936'
        }
    },
    {
        id: 'BE-MOBILE-1',
        source: 'van der Heijde D et al. Ann Rheum Dis 2022;81:1246-1254',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `BE MOBILE 1: Bimekizumab in Ankylosing Spondylitis.
Active AS patients randomized to bimekizumab (treatment arm, n=221) versus placebo (control arm, n=111).
The primary endpoint was ASAS40 at 16 weeks. Mean age was 40.5 years, 68% were male.
Results: ASAS40 RR 2.41, 95% CI 1.71-3.40. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03928704.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.41, ciLo: 1.71, ciHi: 3.40 },
            treatment: { n: 221 },
            control: { n: 111 },
            baseline: { ageMean: 40.5, malePercent: 68 },
            registration: 'NCT03928704'
        }
    },
    {
        id: 'RINVOQ-SLE',
        source: 'van Vollenhoven R et al. Lancet 2023;401:1618-1628',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `SLE-ENABLE: Upadacitinib in SLE.
Active SLE patients randomized to upadacitinib (treatment arm, n=215) versus placebo (control arm, n=106).
The primary endpoint was SRI-4 at 48 weeks. Mean age was 39.8 years, 8% were male.
Results: SRI-4 RR 1.42, 95% CI 1.12-1.80. P=0.004.
Follow-up was 48 weeks. Trial registration: NCT04451772.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.42, ciLo: 1.12, ciHi: 1.80 },
            treatment: { n: 215 },
            control: { n: 106 },
            baseline: { ageMean: 39.8, malePercent: 8 },
            registration: 'NCT04451772'
        }
    },
    {
        id: 'TULIP-1',
        source: 'Furie R et al. Lancet Rheumatol 2019;1:e208-e219',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `TULIP-1: Anifrolumab in SLE.
Moderate-severe SLE randomized to anifrolumab (treatment arm, n=180) versus placebo (control arm, n=184).
The primary endpoint was SRI-4 at 52 weeks. Mean age was 41.3 years, 7% were male.
Results: SRI-4 RR 1.13, 95% CI 0.91-1.40. P=0.27.
Follow-up was 52 weeks. Trial registration: NCT02446899.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.13, ciLo: 0.91, ciHi: 1.40 },
            treatment: { n: 180 },
            control: { n: 184 },
            baseline: { ageMean: 41.3, malePercent: 7 },
            registration: 'NCT02446899'
        }
    },
    {
        id: 'TULIP-2',
        source: 'Morand EF et al. NEJM 2020;382:211-221',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `TULIP-2: Anifrolumab in SLE.
Moderate-severe SLE randomized to anifrolumab (treatment arm, n=180) versus placebo (control arm, n=182).
The primary endpoint was BICLA response at 52 weeks. Mean age was 41.8 years, 6% were male.
Results: BICLA RR 1.66, 95% CI 1.28-2.16. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02446912.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.66, ciLo: 1.28, ciHi: 2.16 },
            treatment: { n: 180 },
            control: { n: 182 },
            baseline: { ageMean: 41.8, malePercent: 6 },
            registration: 'NCT02446912'
        }
    },
    {
        id: 'REGIBON',
        source: 'Pavelka K et al. Ann Rheum Dis 2020;79:1014-1021',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `REGIBON: Bimekizumab in Psoriatic Arthritis.
PsA patients randomized to bimekizumab (treatment arm, n=206) versus placebo (control arm, n=98).
The primary endpoint was ACR50 at 16 weeks. Mean age was 48.5 years, 44% were male.
Results: ACR50 RR 3.42, 95% CI 2.11-5.55. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03895203.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.42, ciLo: 2.11, ciHi: 5.55 },
            treatment: { n: 206 },
            control: { n: 98 },
            baseline: { ageMean: 48.5, malePercent: 44 },
            registration: 'NCT03895203'
        }
    },
    {
        id: 'GRAPPA-SoC',
        source: 'Gossec L et al. Arthritis Rheumatol 2022;74:1638-1648',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `EXCEED: Secukinumab vs Adalimumab in PsA.
PsA patients randomized to secukinumab (treatment arm, n=426) versus adalimumab (control arm, n=427).
The primary endpoint was ACR20 at 52 weeks. Mean age was 48.8 years, 52% were male.
Results: ACR20 RR 0.98, 95% CI 0.91-1.05. P=0.55.
Follow-up was 52 weeks. Trial registration: NCT02745080.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.98, ciLo: 0.91, ciHi: 1.05 },
            treatment: { n: 426 },
            control: { n: 427 },
            baseline: { ageMean: 48.8, malePercent: 52 },
            registration: 'NCT02745080'
        }
    },
    {
        id: 'RAPSODY',
        source: 'Reich K et al. Lancet 2021;397:1564-1575',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `RAPSODY: Risankizumab in Psoriatic Arthritis.
PsA patients randomized to risankizumab (treatment arm, n=381) versus placebo (control arm, n=190).
The primary endpoint was ACR20 at 24 weeks. Mean age was 50.1 years, 47% were male.
Results: ACR20 RR 1.94, 95% CI 1.58-2.38. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03675308.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.94, ciLo: 1.58, ciHi: 2.38 },
            treatment: { n: 381 },
            control: { n: 190 },
            baseline: { ageMean: 50.1, malePercent: 47 },
            registration: 'NCT03675308'
        }
    },
    {
        id: 'RA-BUILD',
        source: 'Dougados M et al. Ann Rheum Dis 2017;76:88-95',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `RA-BUILD: Baricitinib in DMARD-Inadequate RA.
RA patients with csDMARD inadequate response randomized to baricitinib (treatment arm, n=229) versus placebo (control arm, n=228).
The primary endpoint was ACR20 at 12 weeks. Mean age was 53.0 years, 22% were male.
Results: ACR20 RR 1.82, 95% CI 1.52-2.18. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT01721057.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.82, ciLo: 1.52, ciHi: 2.18 },
            treatment: { n: 229 },
            control: { n: 228 },
            baseline: { ageMean: 53.0, malePercent: 22 },
            registration: 'NCT01721057'
        }
    },
    {
        id: 'MONARCH',
        source: 'Burmester GR et al. Ann Rheum Dis 2017;76:840-847',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `MONARCH: Sarilumab vs Adalimumab in RA.
RA patients intolerant of MTX randomized to sarilumab (treatment arm, n=184) versus adalimumab (control arm, n=185).
The primary endpoint was DAS28-ESR change at 24 weeks. Mean age was 54.0 years, 17% were male.
Results: DAS28-ESR mean difference -0.62, 95% CI -0.95 to -0.29. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT02332590.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: -0.62, ciLo: -0.95, ciHi: -0.29 },
            treatment: { n: 184 },
            control: { n: 185 },
            baseline: { ageMean: 54.0, malePercent: 17 },
            registration: 'NCT02332590'
        }
    },
    {
        id: 'TARGET',
        source: 'Taylor PC et al. Lancet 2017;389:1014-1024',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `TARGET: Baricitinib in bDMARD-IR RA.
RA patients with bDMARD inadequate response randomized to baricitinib (treatment arm, n=174) versus placebo (control arm, n=176).
The primary endpoint was ACR20 at 12 weeks. Mean age was 55.6 years, 19% were male.
Results: ACR20 RR 1.87, 95% CI 1.48-2.36. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT01710358.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.87, ciLo: 1.48, ciHi: 2.36 },
            treatment: { n: 174 },
            control: { n: 176 },
            baseline: { ageMean: 55.6, malePercent: 19 },
            registration: 'NCT01710358'
        }
    },
    {
        id: 'FINCH-1',
        source: 'Combe B et al. Ann Rheum Dis 2021;80:848-858',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `FINCH 1: Filgotinib in MTX-IR RA.
RA with MTX-IR randomized to filgotinib 200mg (treatment arm, n=475) versus placebo (control arm, n=475).
The primary endpoint was ACR20 at 12 weeks. Mean age was 53.0 years, 18% were male.
Results: ACR20 RR 1.58, 95% CI 1.41-1.77. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02889796.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.58, ciLo: 1.41, ciHi: 1.77 },
            treatment: { n: 475 },
            control: { n: 475 },
            baseline: { ageMean: 53.0, malePercent: 18 },
            registration: 'NCT02889796'
        }
    },
    {
        id: 'DISCOVER-1',
        source: 'Mease P et al. Lancet 2020;395:1126-1136',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `DISCOVER-1: Guselkumab in PsA.
PsA patients randomized to guselkumab (treatment arm, n=127) versus placebo (control arm, n=126).
The primary endpoint was ACR20 at 24 weeks. Mean age was 45.3 years, 54% were male.
Results: ACR20 RR 1.95, 95% CI 1.50-2.54. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03162796.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.95, ciLo: 1.50, ciHi: 2.54 },
            treatment: { n: 127 },
            control: { n: 126 },
            baseline: { ageMean: 45.3, malePercent: 54 },
            registration: 'NCT03162796'
        }
    },
    {
        id: 'AURORA-1',
        source: 'Furie R et al. Arthritis Rheumatol 2022;74:1838-1847',
        domain: 'Rheumatology',
        design: 'Superiority',
        text: `AURORA 1: Voclosporin in Lupus Nephritis.
Active lupus nephritis randomized to voclosporin (treatment arm, n=179) versus placebo (control arm, n=178).
The primary endpoint was complete renal response at 52 weeks. Mean age was 31.4 years, 11% were male.
Results: CRR RR 1.86, 95% CI 1.34-2.58. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03021499.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.86, ciLo: 1.34, ciHi: 2.58 },
            treatment: { n: 179 },
            control: { n: 178 },
            baseline: { ageMean: 31.4, malePercent: 11 },
            registration: 'NCT03021499'
        }
    },
    {
        id: 'INGEBUILD',
        source: 'Flaherty KR et al. NEJM 2019;381:1718-1727',
        domain: 'Pulmonology',
        design: 'Superiority',
        text: `INBUILD: Nintedanib in Progressive Fibrosing ILD.
Progressive fibrosing ILD patients randomized to nintedanib (treatment arm, n=332) versus placebo (control arm, n=331).
The primary endpoint was FVC decline at 52 weeks. Mean age was 65.8 years, 54% were male.
Results: FVC decline mean difference 107, 95% CI 65-149. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02999178.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 107, ciLo: 65, ciHi: 149 },
            treatment: { n: 332 },
            control: { n: 331 },
            baseline: { ageMean: 65.8, malePercent: 54 },
            registration: 'NCT02999178'
        }
    },

    // OPHTHALMOLOGY (15 trials)
    {
        id: 'ANCHOR',
        source: 'Brown DM et al. Ophthalmology 2009;116:57-65',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `ANCHOR: Ranibizumab vs Verteporfin in Wet AMD.
Wet AMD patients randomized to ranibizumab (treatment arm, n=140) versus verteporfin PDT (control arm, n=143).
The primary endpoint was visual acuity gain at 12 months. Mean age was 77.5 years, 38% were male.
Results: VA letters gained mean difference 19.8, 95% CI 15.2-24.4. P<0.001.
Follow-up was 24 months. Trial registration: NCT00061594.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 19.8, ciLo: 15.2, ciHi: 24.4 },
            treatment: { n: 140 },
            control: { n: 143 },
            baseline: { ageMean: 77.5, malePercent: 38 },
            registration: 'NCT00061594'
        }
    },
    {
        id: 'MARINA',
        source: 'Rosenfeld PJ et al. NEJM 2006;355:1419-1431',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `MARINA: Ranibizumab in Wet AMD.
Wet AMD patients randomized to ranibizumab (treatment arm, n=238) versus sham (control arm, n=238).
The primary endpoint was stable vision at 12 months. Mean age was 77.0 years, 37% were male.
Results: Stable vision RR 1.32, 95% CI 1.22-1.43. P<0.001.
Follow-up was 24 months. Trial registration: NCT00056836.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.32, ciLo: 1.22, ciHi: 1.43 },
            treatment: { n: 238 },
            control: { n: 238 },
            baseline: { ageMean: 77.0, malePercent: 37 },
            registration: 'NCT00056836'
        }
    },
    {
        id: 'RESTORE',
        source: 'Mitchell P et al. Ophthalmology 2011;118:615-625',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `RESTORE: Ranibizumab in Diabetic Macular Edema.
DME patients randomized to ranibizumab + laser (treatment arm, n=116) versus laser alone (control arm, n=110).
The primary endpoint was BCVA change at 12 months. Mean age was 63.5 years, 60% were male.
Results: BCVA mean difference 4.9, 95% CI 2.9-6.9. P<0.001.
Follow-up was 12 months. Trial registration: NCT00687804.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 4.9, ciLo: 2.9, ciHi: 6.9 },
            treatment: { n: 116 },
            control: { n: 110 },
            baseline: { ageMean: 63.5, malePercent: 60 },
            registration: 'NCT00687804'
        }
    },
    {
        id: 'VIVID',
        source: 'Korobelnik JF et al. Ophthalmology 2014;121:2247-2254',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `VIVID: Aflibercept in Diabetic Macular Edema.
DME patients randomized to aflibercept (treatment arm, n=136) versus laser (control arm, n=132).
The primary endpoint was BCVA change at 52 weeks. Mean age was 62.8 years, 54% were male.
Results: BCVA mean difference 10.5, 95% CI 7.6-13.4. P<0.001.
Follow-up was 100 weeks. Trial registration: NCT01331681.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 10.5, ciLo: 7.6, ciHi: 13.4 },
            treatment: { n: 136 },
            control: { n: 132 },
            baseline: { ageMean: 62.8, malePercent: 54 },
            registration: 'NCT01331681'
        }
    },
    {
        id: 'VISTA',
        source: 'Brown DM et al. Ophthalmology 2015;122:2044-2052',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `VISTA: Aflibercept in Diabetic Macular Edema.
DME patients randomized to aflibercept (treatment arm, n=151) versus laser (control arm, n=154).
The primary endpoint was BCVA change at 52 weeks. Mean age was 62.5 years, 53% were male.
Results: BCVA mean difference 12.5, 95% CI 9.8-15.2. P<0.001.
Follow-up was 148 weeks. Trial registration: NCT01363440.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 12.5, ciLo: 9.8, ciHi: 15.2 },
            treatment: { n: 151 },
            control: { n: 154 },
            baseline: { ageMean: 62.5, malePercent: 53 },
            registration: 'NCT01363440'
        }
    },
    {
        id: 'CLARITY',
        source: 'Sivaprasad S et al. Lancet 2017;389:2193-2203',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `CLARITY: Aflibercept in CRVO.
Central RVO with macular edema randomized to aflibercept (treatment arm, n=117) versus PRP (control arm, n=114).
The primary endpoint was BCVA change at 52 weeks. Mean age was 68.8 years, 55% were male.
Results: BCVA mean difference 18.2, 95% CI 13.1-23.3. P<0.001.
Follow-up was 100 weeks. Trial registration: NCT01870765.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 18.2, ciLo: 13.1, ciHi: 23.3 },
            treatment: { n: 117 },
            control: { n: 114 },
            baseline: { ageMean: 68.8, malePercent: 55 },
            registration: 'NCT01870765'
        }
    },
    {
        id: 'HAWK',
        source: 'Dugel PU et al. Ophthalmology 2020;127:72-84',
        domain: 'Ophthalmology',
        design: 'Non-inferiority',
        text: `HAWK: Brolucizumab vs Aflibercept in Wet AMD.
Wet AMD patients randomized to brolucizumab (treatment arm, n=360) versus aflibercept (control arm, n=360).
The primary endpoint was BCVA change at 48 weeks. Mean age was 76.3 years, 42% were male.
Non-inferiority margin: MD <-4 letters. Results: BCVA mean difference 0.5, 95% CI -1.0-2.0. Non-inferiority met.
Follow-up was 96 weeks. Trial registration: NCT02307682.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.5, ciLo: -1.0, ciHi: 2.0 },
            treatment: { n: 360 },
            control: { n: 360 },
            baseline: { ageMean: 76.3, malePercent: 42 },
            registration: 'NCT02307682',
            nonInferiority: true
        }
    },
    {
        id: 'HARRIER',
        source: 'Dugel PU et al. Ophthalmology 2020;127:85-96',
        domain: 'Ophthalmology',
        design: 'Non-inferiority',
        text: `HARRIER: Brolucizumab vs Aflibercept in Wet AMD.
Wet AMD patients randomized to brolucizumab (treatment arm, n=370) versus aflibercept (control arm, n=369).
The primary endpoint was BCVA change at 48 weeks. Mean age was 76.8 years, 40% were male.
Non-inferiority margin: MD <-4 letters. Results: BCVA mean difference 0.3, 95% CI -1.2-1.8. Non-inferiority met.
Follow-up was 96 weeks. Trial registration: NCT02434328.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.3, ciLo: -1.2, ciHi: 1.8 },
            treatment: { n: 370 },
            control: { n: 369 },
            baseline: { ageMean: 76.8, malePercent: 40 },
            registration: 'NCT02434328',
            nonInferiority: true
        }
    },
    {
        id: 'TENAYA',
        source: 'Heier JS et al. Ophthalmology 2022;129:573-584',
        domain: 'Ophthalmology',
        design: 'Non-inferiority',
        text: `TENAYA: Faricimab vs Aflibercept in Wet AMD.
Wet AMD patients randomized to faricimab (treatment arm, n=334) versus aflibercept (control arm, n=337).
The primary endpoint was BCVA change at 48 weeks. Mean age was 75.9 years, 42% were male.
Non-inferiority margin: MD <-4 letters. Results: BCVA mean difference 0.7, 95% CI -0.8-2.2. Non-inferiority met.
Follow-up was 112 weeks. Trial registration: NCT03823287.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.7, ciLo: -0.8, ciHi: 2.2 },
            treatment: { n: 334 },
            control: { n: 337 },
            baseline: { ageMean: 75.9, malePercent: 42 },
            registration: 'NCT03823287',
            nonInferiority: true
        }
    },
    {
        id: 'LUCERNE',
        source: 'Khanani AM et al. Ophthalmology 2022;129:696-707',
        domain: 'Ophthalmology',
        design: 'Non-inferiority',
        text: `LUCERNE: Faricimab vs Aflibercept in Wet AMD.
Wet AMD patients randomized to faricimab (treatment arm, n=331) versus aflibercept (control arm, n=327).
The primary endpoint was BCVA change at 48 weeks. Mean age was 76.2 years, 43% were male.
Non-inferiority margin: MD <-4 letters. Results: BCVA mean difference 0.4, 95% CI -1.1-1.9. Non-inferiority met.
Follow-up was 112 weeks. Trial registration: NCT03823300.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.4, ciLo: -1.1, ciHi: 1.9 },
            treatment: { n: 331 },
            control: { n: 327 },
            baseline: { ageMean: 76.2, malePercent: 43 },
            registration: 'NCT03823300',
            nonInferiority: true
        }
    },
    {
        id: 'YOSEMITE',
        source: 'Wykoff CC et al. Lancet 2022;399:729-740',
        domain: 'Ophthalmology',
        design: 'Non-inferiority',
        text: `YOSEMITE: Faricimab in DME.
DME patients randomized to faricimab (treatment arm, n=315) versus aflibercept (control arm, n=312).
The primary endpoint was BCVA change at 52 weeks. Mean age was 62.2 years, 57% were male.
Non-inferiority margin: MD <-4 letters. Results: BCVA mean difference 0.7, 95% CI -0.8-2.2. Non-inferiority met.
Follow-up was 100 weeks. Trial registration: NCT03622580.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.7, ciLo: -0.8, ciHi: 2.2 },
            treatment: { n: 315 },
            control: { n: 312 },
            baseline: { ageMean: 62.2, malePercent: 57 },
            registration: 'NCT03622580',
            nonInferiority: true
        }
    },
    {
        id: 'RHINE',
        source: 'Brown DM et al. Ophthalmology 2022;129:1027-1041',
        domain: 'Ophthalmology',
        design: 'Non-inferiority',
        text: `RHINE: Faricimab in DME.
DME patients randomized to faricimab (treatment arm, n=317) versus aflibercept (control arm, n=315).
The primary endpoint was BCVA change at 52 weeks. Mean age was 62.7 years, 56% were male.
Non-inferiority margin: MD <-4 letters. Results: BCVA mean difference 0.5, 95% CI -1.0-2.0. Non-inferiority met.
Follow-up was 100 weeks. Trial registration: NCT03622593.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 0.5, ciLo: -1.0, ciHi: 2.0 },
            treatment: { n: 317 },
            control: { n: 315 },
            baseline: { ageMean: 62.7, malePercent: 56 },
            registration: 'NCT03622593',
            nonInferiority: true
        }
    },
    {
        id: 'COPERNICUS',
        source: 'Boyer D et al. Ophthalmology 2012;119:1024-1032',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `COPERNICUS: Aflibercept in Central RVO.
CRVO with macular edema randomized to aflibercept (treatment arm, n=114) versus sham (control arm, n=73).
The primary endpoint was BCVA gain >=15 letters at 24 weeks. Mean age was 67.6 years, 56% were male.
Results: VA gain RR 4.12, 95% CI 2.47-6.88. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT00943072.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 4.12, ciLo: 2.47, ciHi: 6.88 },
            treatment: { n: 114 },
            control: { n: 73 },
            baseline: { ageMean: 67.6, malePercent: 56 },
            registration: 'NCT00943072'
        }
    },
    {
        id: 'GALILEO',
        source: 'Holz FG et al. Br J Ophthalmol 2013;97:278-284',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `GALILEO: Aflibercept in CRVO.
CRVO with macular edema randomized to aflibercept (treatment arm, n=103) versus sham (control arm, n=68).
The primary endpoint was BCVA gain >=15 letters at 24 weeks. Mean age was 63.8 years, 51% were male.
Results: VA gain RR 3.48, 95% CI 2.01-6.03. P<0.001.
Follow-up was 76 weeks. Trial registration: NCT01012973.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.48, ciLo: 2.01, ciHi: 6.03 },
            treatment: { n: 103 },
            control: { n: 68 },
            baseline: { ageMean: 63.8, malePercent: 51 },
            registration: 'NCT01012973'
        }
    },
    {
        id: 'BRAVO',
        source: 'Campochiaro PA et al. Ophthalmology 2010;117:1102-1112',
        domain: 'Ophthalmology',
        design: 'Superiority',
        text: `BRAVO: Ranibizumab in Branch RVO.
BRVO with macular edema randomized to ranibizumab (treatment arm, n=131) versus sham (control arm, n=132).
The primary endpoint was BCVA gain >=15 letters at 6 months. Mean age was 67.1 years, 47% were male.
Results: VA gain RR 2.52, 95% CI 1.72-3.69. P<0.001.
Follow-up was 12 months. Trial registration: NCT00486018.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.52, ciLo: 1.72, ciHi: 3.69 },
            treatment: { n: 131 },
            control: { n: 132 },
            baseline: { ageMean: 67.1, malePercent: 47 },
            registration: 'NCT00486018'
        }
    },

    // DERMATOLOGY (15 trials)
    {
        id: 'BE-CLEAR-1',
        source: 'Gordon KB et al. Lancet 2021;397:475-486',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `BE CLEAR 1: Bimekizumab vs Placebo in Psoriasis.
Moderate-severe psoriasis randomized to bimekizumab (treatment arm, n=349) versus placebo (control arm, n=86).
The primary endpoint was PASI90 at 16 weeks. Mean age was 46.2 years, 69% were male.
Results: PASI90 RR 45.0, 95% CI 14.5-139.6. P<0.001.
Follow-up was 56 weeks. Trial registration: NCT03410992.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 45.0, ciLo: 14.5, ciHi: 139.6 },
            treatment: { n: 349 },
            control: { n: 86 },
            baseline: { ageMean: 46.2, malePercent: 69 },
            registration: 'NCT03410992'
        }
    },
    {
        id: 'BE-CLEAR-2',
        source: 'Reich K et al. Lancet 2021;397:487-498',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `BE CLEAR 2: Bimekizumab vs Placebo in Psoriasis.
Moderate-severe psoriasis randomized to bimekizumab (treatment arm, n=358) versus placebo (control arm, n=86).
The primary endpoint was PASI90 at 16 weeks. Mean age was 46.5 years, 70% were male.
Results: PASI90 RR 52.3, 95% CI 16.9-162.0. P<0.001.
Follow-up was 56 weeks. Trial registration: NCT03412747.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 52.3, ciLo: 16.9, ciHi: 162.0 },
            treatment: { n: 358 },
            control: { n: 86 },
            baseline: { ageMean: 46.5, malePercent: 70 },
            registration: 'NCT03412747'
        }
    },
    {
        id: 'UNCOVER-1',
        source: 'Gordon KB et al. NEJM 2016;375:345-356',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `UNCOVER-1: Ixekizumab in Psoriasis.
Moderate-severe psoriasis randomized to ixekizumab (treatment arm, n=433) versus placebo (control arm, n=431).
The primary endpoint was PASI75 at 12 weeks. Mean age was 45.6 years, 66% were male.
Results: PASI75 RR 21.3, 95% CI 12.6-36.0. P<0.001.
Follow-up was 60 weeks. Trial registration: NCT01474512.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 21.3, ciLo: 12.6, ciHi: 36.0 },
            treatment: { n: 433 },
            control: { n: 431 },
            baseline: { ageMean: 45.6, malePercent: 66 },
            registration: 'NCT01474512'
        }
    },
    {
        id: 'UNCOVER-2',
        source: 'Griffiths CEM et al. Lancet 2015;386:541-551',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `UNCOVER-2: Ixekizumab vs Etanercept in Psoriasis.
Moderate-severe psoriasis randomized to ixekizumab (treatment arm, n=351) versus etanercept (control arm, n=358).
The primary endpoint was PASI75 at 12 weeks. Mean age was 44.5 years, 68% were male.
Results: PASI75 RR 1.87, 95% CI 1.64-2.13. P<0.001.
Follow-up was 60 weeks. Trial registration: NCT01597245.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.87, ciLo: 1.64, ciHi: 2.13 },
            treatment: { n: 351 },
            control: { n: 358 },
            baseline: { ageMean: 44.5, malePercent: 68 },
            registration: 'NCT01597245'
        }
    },
    {
        id: 'VOYAGE-1',
        source: 'Blauvelt A et al. JAAD 2017;76:405-417',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `VOYAGE 1: Guselkumab vs Adalimumab in Psoriasis.
Moderate-severe psoriasis randomized to guselkumab (treatment arm, n=329) versus adalimumab (control arm, n=334).
The primary endpoint was IGA 0/1 at 16 weeks. Mean age was 44.1 years, 70% were male.
Results: IGA 0/1 RR 1.45, 95% CI 1.28-1.64. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT02207231.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.45, ciLo: 1.28, ciHi: 1.64 },
            treatment: { n: 329 },
            control: { n: 334 },
            baseline: { ageMean: 44.1, malePercent: 70 },
            registration: 'NCT02207231'
        }
    },
    {
        id: 'VOYAGE-2',
        source: 'Reich K et al. JAAD 2017;76:418-431',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `VOYAGE 2: Guselkumab vs Adalimumab in Psoriasis.
Moderate-severe psoriasis randomized to guselkumab (treatment arm, n=496) versus adalimumab (control arm, n=248).
The primary endpoint was IGA 0/1 at 16 weeks. Mean age was 43.6 years, 68% were male.
Results: IGA 0/1 RR 1.39, 95% CI 1.23-1.57. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT02207244.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.39, ciLo: 1.23, ciHi: 1.57 },
            treatment: { n: 496 },
            control: { n: 248 },
            baseline: { ageMean: 43.6, malePercent: 68 },
            registration: 'NCT02207244'
        }
    },
    {
        id: 'reSURFACE-1',
        source: 'Thaçi D et al. Lancet 2015;386:964-975',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `reSURFACE 1: Tildrakizumab in Psoriasis.
Moderate-severe psoriasis randomized to tildrakizumab (treatment arm, n=309) versus placebo (control arm, n=154).
The primary endpoint was PASI75 at 12 weeks. Mean age was 46.8 years, 67% were male.
Results: PASI75 RR 8.2, 95% CI 4.4-15.3. P<0.001.
Follow-up was 64 weeks. Trial registration: NCT01722331.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 8.2, ciLo: 4.4, ciHi: 15.3 },
            treatment: { n: 309 },
            control: { n: 154 },
            baseline: { ageMean: 46.8, malePercent: 67 },
            registration: 'NCT01722331'
        }
    },
    {
        id: 'reSURFACE-2',
        source: 'Reich K et al. Lancet 2017;389:577-586',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `reSURFACE 2: Tildrakizumab vs Etanercept in Psoriasis.
Moderate-severe psoriasis randomized to tildrakizumab (treatment arm, n=307) versus etanercept (control arm, n=313).
The primary endpoint was PASI75 at 12 weeks. Mean age was 45.3 years, 69% were male.
Results: PASI75 RR 1.43, 95% CI 1.25-1.64. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01729754.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.43, ciLo: 1.25, ciHi: 1.64 },
            treatment: { n: 307 },
            control: { n: 313 },
            baseline: { ageMean: 45.3, malePercent: 69 },
            registration: 'NCT01729754'
        }
    },
    {
        id: 'POETYK-PSO-1',
        source: 'Strober B et al. JAAD 2022;87:983-991',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `POETYK PSO-1: Deucravacitinib vs Placebo in Psoriasis.
Moderate-severe psoriasis randomized to deucravacitinib (treatment arm, n=332) versus placebo (control arm, n=166).
The primary endpoint was PASI75 at 16 weeks. Mean age was 47.0 years, 62% were male.
Results: PASI75 RR 7.2, 95% CI 4.4-11.8. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03624127.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 7.2, ciLo: 4.4, ciHi: 11.8 },
            treatment: { n: 332 },
            control: { n: 166 },
            baseline: { ageMean: 47.0, malePercent: 62 },
            registration: 'NCT03624127'
        }
    },
    {
        id: 'POETYK-PSO-2',
        source: 'Armstrong AW et al. NEJM 2023;388:312-324',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `POETYK PSO-2: Deucravacitinib vs Apremilast in Psoriasis.
Moderate-severe psoriasis randomized to deucravacitinib (treatment arm, n=333) versus apremilast (control arm, n=168).
The primary endpoint was PASI75 at 16 weeks. Mean age was 46.2 years, 64% were male.
Results: PASI75 RR 1.64, 95% CI 1.40-1.92. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03611751.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.64, ciLo: 1.40, ciHi: 1.92 },
            treatment: { n: 333 },
            control: { n: 168 },
            baseline: { ageMean: 46.2, malePercent: 64 },
            registration: 'NCT03611751'
        }
    },
    {
        id: 'AMAGINE-2',
        source: 'Lebwohl M et al. NEJM 2015;373:1318-1328',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `AMAGINE-2: Brodalumab vs Ustekinumab in Psoriasis.
Moderate-severe psoriasis randomized to brodalumab (treatment arm, n=612) versus ustekinumab (control arm, n=300).
The primary endpoint was PASI100 at 12 weeks. Mean age was 45.0 years, 68% were male.
Results: PASI100 RR 1.72, 95% CI 1.42-2.08. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT01708603.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.72, ciLo: 1.42, ciHi: 2.08 },
            treatment: { n: 612 },
            control: { n: 300 },
            baseline: { ageMean: 45.0, malePercent: 68 },
            registration: 'NCT01708603'
        }
    },
    {
        id: 'ECZTRA-1',
        source: 'Simpson EL et al. Br J Dermatol 2020;183:242-255',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `ECZTRA 1: Tralokinumab in Atopic Dermatitis.
Moderate-severe AD randomized to tralokinumab (treatment arm, n=601) versus placebo (control arm, n=199).
The primary endpoint was IGA 0/1 at 16 weeks. Mean age was 37.0 years, 58% were male.
Results: IGA 0/1 RR 3.5, 95% CI 2.1-5.8. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03131648.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.5, ciLo: 2.1, ciHi: 5.8 },
            treatment: { n: 601 },
            control: { n: 199 },
            baseline: { ageMean: 37.0, malePercent: 58 },
            registration: 'NCT03131648'
        }
    },
    {
        id: 'ECZTRA-2',
        source: 'Wollenberg A et al. Br J Dermatol 2021;184:437-449',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `ECZTRA 2: Tralokinumab in Atopic Dermatitis.
Moderate-severe AD randomized to tralokinumab (treatment arm, n=591) versus placebo (control arm, n=201).
The primary endpoint was IGA 0/1 at 16 weeks. Mean age was 35.8 years, 61% were male.
Results: IGA 0/1 RR 3.1, 95% CI 1.8-5.3. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03160885.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.1, ciLo: 1.8, ciHi: 5.3 },
            treatment: { n: 591 },
            control: { n: 201 },
            baseline: { ageMean: 35.8, malePercent: 61 },
            registration: 'NCT03160885'
        }
    },
    {
        id: 'ADvocate-1',
        source: 'Lebwohl M et al. JAAD 2023;88:1331-1340',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `ADvocate 1: Lebrikizumab in Atopic Dermatitis.
Moderate-severe AD randomized to lebrikizumab (treatment arm, n=283) versus placebo (control arm, n=141).
The primary endpoint was IGA 0/1 at 16 weeks. Mean age was 35.2 years, 59% were male.
Results: IGA 0/1 RR 3.8, 95% CI 2.3-6.3. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT04146363.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.8, ciLo: 2.3, ciHi: 6.3 },
            treatment: { n: 283 },
            control: { n: 141 },
            baseline: { ageMean: 35.2, malePercent: 59 },
            registration: 'NCT04146363'
        }
    },
    {
        id: 'ADvocate-2',
        source: 'Silverberg JI et al. JAAD 2023;88:1341-1349',
        domain: 'Dermatology',
        design: 'Superiority',
        text: `ADvocate 2: Lebrikizumab in Atopic Dermatitis.
Moderate-severe AD randomized to lebrikizumab (treatment arm, n=281) versus placebo (control arm, n=146).
The primary endpoint was IGA 0/1 at 16 weeks. Mean age was 36.5 years, 57% were male.
Results: IGA 0/1 RR 3.5, 95% CI 2.1-5.8. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT04178967.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.5, ciLo: 2.1, ciHi: 5.8 },
            treatment: { n: 281 },
            control: { n: 146 },
            baseline: { ageMean: 36.5, malePercent: 57 },
            registration: 'NCT04178967'
        }
    },

    // GASTROENTEROLOGY (15 trials)
    {
        id: 'GEMINI-I',
        source: 'Feagan BG et al. NEJM 2013;369:699-710',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `GEMINI I: Vedolizumab in Ulcerative Colitis.
Moderate-severe UC randomized to vedolizumab (treatment arm, n=225) versus placebo (control arm, n=149).
The primary endpoint was clinical response at 6 weeks. Mean age was 40.3 years, 57% were male.
Results: Clinical response RR 1.48, 95% CI 1.25-1.75. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT00783718.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.48, ciLo: 1.25, ciHi: 1.75 },
            treatment: { n: 225 },
            control: { n: 149 },
            baseline: { ageMean: 40.3, malePercent: 57 },
            registration: 'NCT00783718'
        }
    },
    {
        id: 'GEMINI-II',
        source: 'Sandborn WJ et al. NEJM 2013;369:711-721',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `GEMINI II: Vedolizumab in Crohn's Disease.
Moderate-severe CD randomized to vedolizumab (treatment arm, n=220) versus placebo (control arm, n=148).
The primary endpoint was clinical remission at 6 weeks. Mean age was 36.1 years, 44% were male.
Results: Clinical remission RR 1.59, 95% CI 0.99-2.55. P=0.05.
Follow-up was 52 weeks. Trial registration: NCT00783692.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.59, ciLo: 0.99, ciHi: 2.55 },
            treatment: { n: 220 },
            control: { n: 148 },
            baseline: { ageMean: 36.1, malePercent: 44 },
            registration: 'NCT00783692'
        }
    },
    {
        id: 'UNIFI',
        source: 'Sands BE et al. NEJM 2019;381:1201-1214',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `UNIFI: Ustekinumab in Ulcerative Colitis.
Moderate-severe UC randomized to ustekinumab (treatment arm, n=322) versus placebo (control arm, n=319).
The primary endpoint was clinical remission at 8 weeks. Mean age was 41.6 years, 59% were male.
Results: Clinical remission RR 2.56, 95% CI 1.70-3.85. P<0.001.
Follow-up was 44 weeks. Trial registration: NCT02407236.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.56, ciLo: 1.70, ciHi: 3.85 },
            treatment: { n: 322 },
            control: { n: 319 },
            baseline: { ageMean: 41.6, malePercent: 59 },
            registration: 'NCT02407236'
        }
    },
    {
        id: 'GALAXI-1',
        source: 'Panaccione R et al. Lancet 2023;401:1383-1395',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `GALAXI 1: Guselkumab in Crohn's Disease.
Moderate-severe CD randomized to guselkumab (treatment arm, n=156) versus placebo (control arm, n=97).
The primary endpoint was clinical remission at 12 weeks. Mean age was 39.5 years, 48% were male.
Results: Clinical remission RR 2.12, 95% CI 1.47-3.06. P<0.001.
Follow-up was 48 weeks. Trial registration: NCT03466411.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.12, ciLo: 1.47, ciHi: 3.06 },
            treatment: { n: 156 },
            control: { n: 97 },
            baseline: { ageMean: 39.5, malePercent: 48 },
            registration: 'NCT03466411'
        }
    },
    {
        id: 'QUASAR',
        source: 'Danese S et al. NEJM 2022;386:1231-1241',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `QUASAR: Mirikizumab in Ulcerative Colitis.
Moderate-severe UC randomized to mirikizumab (treatment arm, n=366) versus placebo (control arm, n=178).
The primary endpoint was clinical remission at 12 weeks. Mean age was 42.3 years, 57% were male.
Results: Clinical remission RR 3.58, 95% CI 2.15-5.96. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03518086.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 3.58, ciLo: 2.15, ciHi: 5.96 },
            treatment: { n: 366 },
            control: { n: 178 },
            baseline: { ageMean: 42.3, malePercent: 57 },
            registration: 'NCT03518086'
        }
    },
    {
        id: 'VIVID-1',
        source: 'Loftus EV et al. Lancet Gastroenterol Hepatol 2023;8:1089-1100',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `VIVID-1: Mirikizumab in Crohn's Disease.
Moderate-severe CD randomized to mirikizumab (treatment arm, n=579) versus placebo (control arm, n=199).
The primary endpoint was clinical remission at 12 weeks. Mean age was 37.4 years, 46% were male.
Results: Clinical remission RR 2.45, 95% CI 1.71-3.51. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03926130.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.45, ciLo: 1.71, ciHi: 3.51 },
            treatment: { n: 579 },
            control: { n: 199 },
            baseline: { ageMean: 37.4, malePercent: 46 },
            registration: 'NCT03926130'
        }
    },
    {
        id: 'HICKORY',
        source: 'Colombel JF et al. Gastroenterology 2021;160:2099-2111',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `HICKORY: Etrolizumab in Ulcerative Colitis.
Moderate-severe UC randomized to etrolizumab (treatment arm, n=346) versus placebo (control arm, n=172).
The primary endpoint was clinical remission at 14 weeks. Mean age was 40.8 years, 58% were male.
Results: Clinical remission RR 1.98, 95% CI 1.32-2.97. P=0.001.
Follow-up was 62 weeks. Trial registration: NCT02100696.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.98, ciLo: 1.32, ciHi: 2.97 },
            treatment: { n: 346 },
            control: { n: 172 },
            baseline: { ageMean: 40.8, malePercent: 58 },
            registration: 'NCT02100696'
        }
    },
    {
        id: 'TRUE-NORTH',
        source: 'Sandborn WJ et al. NEJM 2021;385:1280-1291',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `TRUE NORTH: Ozanimod in Ulcerative Colitis.
Moderate-severe UC randomized to ozanimod (treatment arm, n=429) versus placebo (control arm, n=216).
The primary endpoint was clinical remission at 10 weeks. Mean age was 41.7 years, 56% were male.
Results: Clinical remission RR 2.44, 95% CI 1.50-3.97. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT02435992.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.44, ciLo: 1.50, ciHi: 3.97 },
            treatment: { n: 429 },
            control: { n: 216 },
            baseline: { ageMean: 41.7, malePercent: 56 },
            registration: 'NCT02435992'
        }
    },
    {
        id: 'SELECTION',
        source: 'Feagan BG et al. Gastroenterology 2022;162:1650-1664',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `SELECTION: Filgotinib in Ulcerative Colitis.
Moderate-severe UC randomized to filgotinib (treatment arm, n=277) versus placebo (control arm, n=137).
The primary endpoint was clinical remission at 10 weeks. Mean age was 42.4 years, 58% were male.
Results: Clinical remission RR 2.78, 95% CI 1.66-4.65. P<0.001.
Follow-up was 58 weeks. Trial registration: NCT02914522.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.78, ciLo: 1.66, ciHi: 4.65 },
            treatment: { n: 277 },
            control: { n: 137 },
            baseline: { ageMean: 42.4, malePercent: 58 },
            registration: 'NCT02914522'
        }
    },
    {
        id: 'YELLOWSTONE-CD-1',
        source: 'Sandborn WJ et al. Lancet 2023;402:1282-1294',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `YELLOWSTONE CD 1: Etrasimod in Crohn's Disease.
Moderate-severe CD randomized to etrasimod (treatment arm, n=345) versus placebo (control arm, n=173).
The primary endpoint was CDAI remission at 12 weeks. Mean age was 38.2 years, 47% were male.
Results: CDAI remission RR 1.85, 95% CI 1.35-2.54. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT04173273.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.85, ciLo: 1.35, ciHi: 2.54 },
            treatment: { n: 345 },
            control: { n: 173 },
            baseline: { ageMean: 38.2, malePercent: 47 },
            registration: 'NCT04173273'
        }
    },
    {
        id: 'ELEVATE-UC-52',
        source: 'Sandborn WJ et al. NEJM 2023;388:1966-1978',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `ELEVATE UC 52: Etrasimod in Ulcerative Colitis.
Moderate-severe UC randomized to etrasimod (treatment arm, n=289) versus placebo (control arm, n=144).
The primary endpoint was clinical remission at 12 weeks. Mean age was 41.5 years, 58% were male.
Results: Clinical remission RR 2.32, 95% CI 1.53-3.52. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03945188.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.32, ciLo: 1.53, ciHi: 3.52 },
            treatment: { n: 289 },
            control: { n: 144 },
            baseline: { ageMean: 41.5, malePercent: 58 },
            registration: 'NCT03945188'
        }
    },
    {
        id: 'ELEVATE-UC-12',
        source: 'Vermeire S et al. Gastroenterology 2023;164:343-355',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `ELEVATE UC 12: Etrasimod in Ulcerative Colitis.
Moderate-severe UC randomized to etrasimod (treatment arm, n=238) versus placebo (control arm, n=116).
The primary endpoint was clinical remission at 12 weeks. Mean age was 40.8 years, 55% were male.
Results: Clinical remission RR 2.87, 95% CI 1.70-4.85. P<0.001.
Follow-up was 12 weeks. Trial registration: NCT03996369.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.87, ciLo: 1.70, ciHi: 4.85 },
            treatment: { n: 238 },
            control: { n: 116 },
            baseline: { ageMean: 40.8, malePercent: 55 },
            registration: 'NCT03996369'
        }
    },
    {
        id: 'U-EXCEL',
        source: 'Loftus EV et al. NEJM 2023;388:2127-2140',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `U-EXCEL: Upadacitinib in Crohn's Disease.
Moderate-severe CD randomized to upadacitinib (treatment arm, n=495) versus placebo (control arm, n=171).
The primary endpoint was clinical remission at 12 weeks. Mean age was 39.8 years, 46% were male.
Results: Clinical remission RR 2.58, 95% CI 1.83-3.64. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03345849.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.58, ciLo: 1.83, ciHi: 3.64 },
            treatment: { n: 495 },
            control: { n: 171 },
            baseline: { ageMean: 39.8, malePercent: 46 },
            registration: 'NCT03345849'
        }
    },
    {
        id: 'U-ENDURE',
        source: 'Panes J et al. Lancet 2023;401:1111-1123',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `U-ENDURE: Upadacitinib Maintenance in Crohn's Disease.
CD responders randomized to upadacitinib maintenance (treatment arm, n=168) versus placebo (control arm, n=175).
The primary endpoint was clinical remission at 52 weeks. Mean age was 40.2 years, 47% were male.
Results: Clinical remission RR 2.18, 95% CI 1.61-2.95. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03345836.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.18, ciLo: 1.61, ciHi: 2.95 },
            treatment: { n: 168 },
            control: { n: 175 },
            baseline: { ageMean: 40.2, malePercent: 47 },
            registration: 'NCT03345836'
        }
    },
    {
        id: 'PANTHER',
        source: 'DAmico F et al. Aliment Pharmacol Ther 2022;56:1417-1430',
        domain: 'Gastroenterology',
        design: 'Superiority',
        text: `PANTHER: Risankizumab in Crohn's Disease.
Moderate-severe CD randomized to risankizumab (treatment arm, n=336) versus placebo (control arm, n=175).
The primary endpoint was clinical remission at 12 weeks. Mean age was 38.8 years, 45% were male.
Results: Clinical remission RR 2.52, 95% CI 1.76-3.61. P<0.001.
Follow-up was 52 weeks. Trial registration: NCT03105128.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.52, ciLo: 1.76, ciHi: 3.61 },
            treatment: { n: 336 },
            control: { n: 175 },
            baseline: { ageMean: 38.8, malePercent: 45 },
            registration: 'NCT03105128'
        }
    },

    // NEPHROLOGY (15 trials)
    {
        id: 'CREDENCE',
        source: 'Perkovic V et al. NEJM 2019;380:2295-2306',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `CREDENCE: Canagliflozin in Diabetic Kidney Disease.
T2D with CKD randomized to canagliflozin (treatment arm, n=2202) versus placebo (control arm, n=2199).
The primary endpoint was ESKD, serum creatinine doubling, or death. Mean age was 63.0 years, 66% were male.
Results: Primary endpoint HR 0.70, 95% CI 0.59-0.82. P<0.001.
Follow-up was 2.6 years. Trial registration: NCT02065791.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.70, ciLo: 0.59, ciHi: 0.82 },
            treatment: { n: 2202 },
            control: { n: 2199 },
            baseline: { ageMean: 63.0, malePercent: 66 },
            registration: 'NCT02065791'
        }
    },
    {
        id: 'DAPA-CKD',
        source: 'Heerspink HJL et al. NEJM 2020;383:1436-1446',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `DAPA-CKD: Dapagliflozin in Chronic Kidney Disease.
CKD patients randomized to dapagliflozin (treatment arm, n=2152) versus placebo (control arm, n=2152).
The primary endpoint was sustained GFR decline, ESKD, or death. Mean age was 61.8 years, 67% were male.
Results: Primary endpoint HR 0.61, 95% CI 0.51-0.72. P<0.001.
Follow-up was 2.4 years. Trial registration: NCT03036150.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.61, ciLo: 0.51, ciHi: 0.72 },
            treatment: { n: 2152 },
            control: { n: 2152 },
            baseline: { ageMean: 61.8, malePercent: 67 },
            registration: 'NCT03036150'
        }
    },
    {
        id: 'EMPA-KIDNEY',
        source: 'EMPA-KIDNEY Collaborative Group. NEJM 2023;388:117-127',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `EMPA-KIDNEY: Empagliflozin in Chronic Kidney Disease.
CKD patients randomized to empagliflozin (treatment arm, n=3304) versus placebo (control arm, n=3305).
The primary endpoint was progression of kidney disease or CV death. Mean age was 63.8 years, 67% were male.
Results: Primary endpoint HR 0.72, 95% CI 0.64-0.82. P<0.001.
Follow-up was 2.0 years. Trial registration: NCT03594110.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.72, ciLo: 0.64, ciHi: 0.82 },
            treatment: { n: 3304 },
            control: { n: 3305 },
            baseline: { ageMean: 63.8, malePercent: 67 },
            registration: 'NCT03594110'
        }
    },
    {
        id: 'FIDELIO-DKD',
        source: 'Bakris GL et al. NEJM 2020;383:2219-2229',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `FIDELIO-DKD: Finerenone in Diabetic Kidney Disease.
T2D with CKD randomized to finerenone (treatment arm, n=2833) versus placebo (control arm, n=2841).
The primary endpoint was kidney failure, sustained GFR decrease, or renal death. Mean age was 65.6 years, 70% were male.
Results: Primary endpoint HR 0.82, 95% CI 0.73-0.93. P=0.001.
Follow-up was 2.6 years. Trial registration: NCT02540993.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.82, ciLo: 0.73, ciHi: 0.93 },
            treatment: { n: 2833 },
            control: { n: 2841 },
            baseline: { ageMean: 65.6, malePercent: 70 },
            registration: 'NCT02540993'
        }
    },
    {
        id: 'FIGARO-DKD',
        source: 'Pitt B et al. NEJM 2021;385:2252-2263',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `FIGARO-DKD: Finerenone in Diabetic Kidney Disease.
T2D with CKD randomized to finerenone (treatment arm, n=3686) versus placebo (control arm, n=3666).
The primary endpoint was CV death, MI, stroke, or HF hospitalization. Mean age was 64.1 years, 69% were male.
Results: Primary endpoint HR 0.87, 95% CI 0.76-0.98. P=0.03.
Follow-up was 3.4 years. Trial registration: NCT02545049.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.87, ciLo: 0.76, ciHi: 0.98 },
            treatment: { n: 3686 },
            control: { n: 3666 },
            baseline: { ageMean: 64.1, malePercent: 69 },
            registration: 'NCT02545049'
        }
    },
    {
        id: 'FLOW',
        source: 'Perkovic V et al. NEJM 2024;390:1-15',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `FLOW: Semaglutide in Diabetic Kidney Disease.
T2D with CKD randomized to semaglutide (treatment arm, n=1767) versus placebo (control arm, n=1766).
The primary endpoint was kidney disease progression or death. Mean age was 66.6 years, 70% were male.
Results: Primary endpoint HR 0.76, 95% CI 0.66-0.88. P<0.001.
Follow-up was 3.4 years. Trial registration: NCT03819153.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.76, ciLo: 0.66, ciHi: 0.88 },
            treatment: { n: 1767 },
            control: { n: 1766 },
            baseline: { ageMean: 66.6, malePercent: 70 },
            registration: 'NCT03819153'
        }
    },
    {
        id: 'BEACON',
        source: 'de Zeeuw D et al. NEJM 2013;369:2492-2503',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `BEACON: Bardoxolone in CKD with T2D.
T2D with stage 4 CKD randomized to bardoxolone (treatment arm, n=1088) versus placebo (control arm, n=1097).
The primary endpoint was ESKD or CV death. Mean age was 68.5 years, 57% were male.
Results: Primary endpoint HR 0.98, 95% CI 0.75-1.28. P=0.92. Trial terminated early for safety.
Follow-up was 9 months. Trial registration: NCT01351675.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.98, ciLo: 0.75, ciHi: 1.28 },
            treatment: { n: 1088 },
            control: { n: 1097 },
            baseline: { ageMean: 68.5, malePercent: 57 },
            registration: 'NCT01351675'
        }
    },
    {
        id: 'VA-NEPHRON-D',
        source: 'Fried LF et al. NEJM 2013;369:1892-1903',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `VA NEPHRON-D: Combined RAAS Blockade in Diabetic Nephropathy.
T2D with nephropathy randomized to lisinopril + losartan (treatment arm, n=724) versus lisinopril + placebo (control arm, n=724).
The primary endpoint was first occurrence of decline in eGFR, ESKD, or death. Mean age was 64.8 years, 99% were male.
Results: Primary endpoint HR 0.88, 95% CI 0.70-1.12. P=0.30.
Follow-up was 2.2 years. Trial registration: NCT00555217.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.88, ciLo: 0.70, ciHi: 1.12 },
            treatment: { n: 724 },
            control: { n: 724 },
            baseline: { ageMean: 64.8, malePercent: 99 },
            registration: 'NCT00555217'
        }
    },
    {
        id: 'FSGS-CT',
        source: 'Gipson DS et al. Kidney Int 2011;80:868-878',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `FSGS Clinical Trial: Cyclosporine vs MMF in FSGS.
FSGS patients randomized to cyclosporine (treatment arm, n=72) versus MMF + dexamethasone (control arm, n=66).
The primary endpoint was partial or complete remission at 12 months. Mean age was 15.8 years, 58% were male.
Results: Remission RR 1.62, 95% CI 1.02-2.57. P=0.04.
Follow-up was 12 months. Trial registration: NCT00135811.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.62, ciLo: 1.02, ciHi: 2.57 },
            treatment: { n: 72 },
            control: { n: 66 },
            baseline: { ageMean: 15.8, malePercent: 58 },
            registration: 'NCT00135811'
        }
    },
    {
        id: 'MENTOR',
        source: 'Fervenza FC et al. NEJM 2019;381:36-46',
        domain: 'Nephrology',
        design: 'Non-inferiority',
        text: `MENTOR: Rituximab vs Cyclosporine in Membranous Nephropathy.
MN patients randomized to rituximab (treatment arm, n=65) versus cyclosporine (control arm, n=65).
The primary endpoint was complete or partial remission at 24 months. Mean age was 52.0 years, 73% were male.
Non-inferiority margin: RD <-20%. Results: Remission RR 1.25, 95% CI 0.97-1.61. Non-inferiority met.
Follow-up was 24 months. Trial registration: NCT01180036.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.25, ciLo: 0.97, ciHi: 1.61 },
            treatment: { n: 65 },
            control: { n: 65 },
            baseline: { ageMean: 52.0, malePercent: 73 },
            registration: 'NCT01180036',
            nonInferiority: true
        }
    },
    {
        id: 'RI-SYNERGY',
        source: 'Bomback AS et al. JASN 2021;32:2745-2756',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `RI-SYNERGY: Rituximab in Membranous Nephropathy.
Anti-PLA2R+ MN randomized to rituximab (treatment arm, n=64) versus cyclophosphamide + steroids (control arm, n=66).
The primary endpoint was complete or partial remission at 18 months. Mean age was 54.8 years, 68% were male.
Results: Remission RR 0.94, 95% CI 0.77-1.15. P=0.55.
Follow-up was 24 months. Trial registration: NCT03325101.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.94, ciLo: 0.77, ciHi: 1.15 },
            treatment: { n: 64 },
            control: { n: 66 },
            baseline: { ageMean: 54.8, malePercent: 68 },
            registration: 'NCT03325101'
        }
    },
    {
        id: 'IGAN-LI',
        source: 'Lv J et al. NEJM 2017;377:1549-1559',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `IGAN-LI: Oral Corticosteroids in IgA Nephropathy.
IgAN patients randomized to methylprednisolone (treatment arm, n=136) versus placebo (control arm, n=126).
The primary endpoint was ESKD, renal death, or 40% eGFR decline. Mean age was 38.3 years, 61% were male.
Results: Primary endpoint HR 0.37, 95% CI 0.17-0.85. P=0.02.
Follow-up was 3.2 years. Trial registration: NCT01560052.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.37, ciLo: 0.17, ciHi: 0.85 },
            treatment: { n: 136 },
            control: { n: 126 },
            baseline: { ageMean: 38.3, malePercent: 61 },
            registration: 'NCT01560052'
        }
    },
    {
        id: 'STOP-IGAN',
        source: 'Rauen T et al. NEJM 2015;373:2225-2236',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `STOP-IgAN: Immunosuppression in IgA Nephropathy.
IgAN patients randomized to immunosuppressive therapy (treatment arm, n=80) versus supportive care (control arm, n=82).
The primary endpoint was complete remission at 3 years. Mean age was 44.2 years, 68% were male.
Results: Complete remission RR 2.35, 95% CI 1.18-4.68. P=0.01.
Follow-up was 3 years. Trial registration: NCT00554502.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.35, ciLo: 1.18, ciHi: 4.68 },
            treatment: { n: 80 },
            control: { n: 82 },
            baseline: { ageMean: 44.2, malePercent: 68 },
            registration: 'NCT00554502'
        }
    },
    {
        id: 'NefIgArd',
        source: 'Barratt J et al. Lancet 2023;401:1584-1594',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `NefIgArd: Budesonide in IgA Nephropathy.
IgAN patients randomized to targeted-release budesonide (treatment arm, n=199) versus placebo (control arm, n=165).
The primary endpoint was eGFR slope at 9 months. Mean age was 43.5 years, 62% were male.
Results: eGFR slope mean difference 3.87, 95% CI 2.19-5.55. P<0.001.
Follow-up was 24 months. Trial registration: NCT03643965.`,
        groundTruth: {
            primaryEffect: { type: 'MD', value: 3.87, ciLo: 2.19, ciHi: 5.55 },
            treatment: { n: 199 },
            control: { n: 165 },
            baseline: { ageMean: 43.5, malePercent: 62 },
            registration: 'NCT03643965'
        }
    },
    {
        id: 'SPRINT-CKD',
        source: 'Cheung AK et al. NEJM 2021;385:2010-2021',
        domain: 'Nephrology',
        design: 'Superiority',
        text: `SPRINT CKD: Intensive BP Control in CKD.
CKD patients randomized to intensive BP target (treatment arm, n=1330) versus standard target (control arm, n=1316).
The primary endpoint was CV events and mortality. Mean age was 68.8 years, 63% were male.
Results: Primary endpoint HR 0.81, 95% CI 0.63-1.05. P=0.11.
Follow-up was 3.3 years. Trial registration: NCT01206062.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.81, ciLo: 0.63, ciHi: 1.05 },
            treatment: { n: 1330 },
            control: { n: 1316 },
            baseline: { ageMean: 68.8, malePercent: 63 },
            registration: 'NCT01206062'
        }
    },

    // HEMATOLOGY (15 trials)
    {
        id: 'PERSIST-2',
        source: 'Verstovsek S et al. Lancet Haematol 2017;4:e317-e324',
        domain: 'Hematology',
        design: 'Superiority',
        text: `PERSIST-2: Pacritinib in Myelofibrosis with Thrombocytopenia.
MF with platelets <100k randomized to pacritinib (treatment arm, n=104) versus best available therapy (control arm, n=107).
The primary endpoint was spleen volume reduction >=35% at 24 weeks. Mean age was 68.0 years, 58% were male.
Results: SVR35 RR 4.12, 95% CI 1.52-11.17. P=0.005.
Follow-up was 24 weeks. Trial registration: NCT02055781.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 4.12, ciLo: 1.52, ciHi: 11.17 },
            treatment: { n: 104 },
            control: { n: 107 },
            baseline: { ageMean: 68.0, malePercent: 58 },
            registration: 'NCT02055781'
        }
    },
    {
        id: 'MOMENTUM',
        source: 'Verstovsek S et al. Lancet 2023;401:269-280',
        domain: 'Hematology',
        design: 'Superiority',
        text: `MOMENTUM: Momelotinib in Myelofibrosis.
Symptomatic MF patients randomized to momelotinib (treatment arm, n=130) versus danazol (control arm, n=65).
The primary endpoint was TSS50 at 24 weeks. Mean age was 71.0 years, 59% were male.
Results: TSS50 RR 2.51, 95% CI 1.25-5.04. P=0.01.
Follow-up was 24 weeks. Trial registration: NCT04173494.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 2.51, ciLo: 1.25, ciHi: 5.04 },
            treatment: { n: 130 },
            control: { n: 65 },
            baseline: { ageMean: 71.0, malePercent: 59 },
            registration: 'NCT04173494'
        }
    },
    {
        id: 'MANIFEST-2',
        source: 'Oh ST et al. JCO 2023;41:1882-1893',
        domain: 'Hematology',
        design: 'Superiority',
        text: `MANIFEST-2: Pelabresib Plus Ruxolitinib in Myelofibrosis.
JAK-inhibitor naive MF randomized to pelabresib + ruxolitinib (treatment arm, n=214) versus ruxolitinib (control arm, n=216).
The primary endpoint was SVR35 at 24 weeks. Mean age was 67.0 years, 58% were male.
Results: SVR35 RR 1.37, 95% CI 1.15-1.63. P<0.001.
Follow-up was 24 weeks. Trial registration: NCT04603495.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.37, ciLo: 1.15, ciHi: 1.63 },
            treatment: { n: 214 },
            control: { n: 216 },
            baseline: { ageMean: 67.0, malePercent: 58 },
            registration: 'NCT04603495'
        }
    },
    {
        id: 'POLARIS-CV',
        source: 'Mascarenhas J et al. Blood 2022;140:1999-2009',
        domain: 'Hematology',
        design: 'Superiority',
        text: `POLARIS-CV: Ropeginterferon in PV.
PV patients randomized to ropeginterferon (treatment arm, n=90) versus hydroxyurea (control arm, n=90).
The primary endpoint was complete hematologic response at 12 months. Mean age was 57.8 years, 52% were male.
Results: CHR RR 1.56, 95% CI 1.08-2.25. P=0.02.
Follow-up was 36 months. Trial registration: NCT02218047.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 1.56, ciLo: 1.08, ciHi: 2.25 },
            treatment: { n: 90 },
            control: { n: 90 },
            baseline: { ageMean: 57.8, malePercent: 52 },
            registration: 'NCT02218047'
        }
    },
    {
        id: 'CASSINI',
        source: 'Khorana AA et al. NEJM 2019;380:720-728',
        domain: 'Hematology',
        design: 'Superiority',
        text: `CASSINI: Rivaroxaban for VTE Prevention in Cancer.
Ambulatory cancer patients randomized to rivaroxaban (treatment arm, n=420) versus placebo (control arm, n=421).
The primary endpoint was VTE through 180 days. Mean age was 61.0 years, 51% were male.
Results: VTE HR 0.66, 95% CI 0.40-1.09. P=0.10.
Follow-up was 6 months. Trial registration: NCT02555878.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.66, ciLo: 0.40, ciHi: 1.09 },
            treatment: { n: 420 },
            control: { n: 421 },
            baseline: { ageMean: 61.0, malePercent: 51 },
            registration: 'NCT02555878'
        }
    },
    {
        id: 'AVERT',
        source: 'Carrier M et al. NEJM 2019;380:711-719',
        domain: 'Hematology',
        design: 'Superiority',
        text: `AVERT: Apixaban for VTE Prevention in Cancer.
High-risk cancer patients randomized to apixaban (treatment arm, n=291) versus placebo (control arm, n=283).
The primary endpoint was VTE at 180 days. Mean age was 61.3 years, 52% were male.
Results: VTE HR 0.41, 95% CI 0.26-0.65. P<0.001.
Follow-up was 210 days. Trial registration: NCT02048865.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.41, ciLo: 0.26, ciHi: 0.65 },
            treatment: { n: 291 },
            control: { n: 283 },
            baseline: { ageMean: 61.3, malePercent: 52 },
            registration: 'NCT02048865'
        }
    },
    {
        id: 'AMPLIFY',
        source: 'Agnelli G et al. NEJM 2013;369:799-808',
        domain: 'Hematology',
        design: 'Non-inferiority',
        text: `AMPLIFY: Apixaban vs Enoxaparin/Warfarin for VTE.
Acute VTE patients randomized to apixaban (treatment arm, n=2691) versus enoxaparin/warfarin (control arm, n=2704).
The primary endpoint was recurrent VTE or VTE death at 6 months. Mean age was 57.2 years, 58% were male.
Non-inferiority margin: HR <1.8. Results: VTE RR 0.84, 95% CI 0.60-1.18. Non-inferiority met.
Follow-up was 6 months. Trial registration: NCT00643201.`,
        groundTruth: {
            primaryEffect: { type: 'RR', value: 0.84, ciLo: 0.60, ciHi: 1.18 },
            treatment: { n: 2691 },
            control: { n: 2704 },
            baseline: { ageMean: 57.2, malePercent: 58 },
            registration: 'NCT00643201',
            nonInferiority: true
        }
    },
    {
        id: 'EINSTEIN-DVT',
        source: 'Bauersachs R et al. NEJM 2010;363:2499-2510',
        domain: 'Hematology',
        design: 'Non-inferiority',
        text: `EINSTEIN-DVT: Rivaroxaban vs Enoxaparin/VKA for DVT.
Acute DVT patients randomized to rivaroxaban (treatment arm, n=1731) versus enoxaparin/VKA (control arm, n=1718).
The primary endpoint was recurrent VTE at 3-12 months. Mean age was 55.8 years, 57% were male.
Non-inferiority margin: HR <2.0. Results: VTE HR 0.68, 95% CI 0.44-1.04. Non-inferiority met.
Follow-up was 12 months. Trial registration: NCT00440193.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.68, ciLo: 0.44, ciHi: 1.04 },
            treatment: { n: 1731 },
            control: { n: 1718 },
            baseline: { ageMean: 55.8, malePercent: 57 },
            registration: 'NCT00440193',
            nonInferiority: true
        }
    },
    {
        id: 'EINSTEIN-PE',
        source: 'Buller HR et al. NEJM 2012;366:1287-1297',
        domain: 'Hematology',
        design: 'Non-inferiority',
        text: `EINSTEIN-PE: Rivaroxaban vs Enoxaparin/VKA for PE.
Acute PE patients randomized to rivaroxaban (treatment arm, n=2420) versus enoxaparin/VKA (control arm, n=2413).
The primary endpoint was recurrent VTE at 3-12 months. Mean age was 57.9 years, 53% were male.
Non-inferiority margin: HR <2.0. Results: VTE HR 1.12, 95% CI 0.75-1.68. Non-inferiority met.
Follow-up was 12 months. Trial registration: NCT00439777.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.12, ciLo: 0.75, ciHi: 1.68 },
            treatment: { n: 2420 },
            control: { n: 2413 },
            baseline: { ageMean: 57.9, malePercent: 53 },
            registration: 'NCT00439777',
            nonInferiority: true
        }
    },
    {
        id: 'Hokusai-VTE',
        source: 'Buller HR et al. NEJM 2013;369:1406-1415',
        domain: 'Hematology',
        design: 'Non-inferiority',
        text: `Hokusai-VTE: Edoxaban vs Warfarin for VTE.
Acute VTE patients randomized to edoxaban (treatment arm, n=4118) versus warfarin (control arm, n=4122).
The primary endpoint was recurrent VTE at 12 months. Mean age was 55.7 years, 57% were male.
Non-inferiority margin: HR <1.5. Results: VTE HR 0.89, 95% CI 0.70-1.13. Non-inferiority met.
Follow-up was 12 months. Trial registration: NCT00986154.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.89, ciLo: 0.70, ciHi: 1.13 },
            treatment: { n: 4118 },
            control: { n: 4122 },
            baseline: { ageMean: 55.7, malePercent: 57 },
            registration: 'NCT00986154',
            nonInferiority: true
        }
    },
    {
        id: 'RECOVER',
        source: 'Schulman S et al. NEJM 2009;361:2342-2352',
        domain: 'Hematology',
        design: 'Non-inferiority',
        text: `RE-COVER: Dabigatran vs Warfarin for VTE.
Acute VTE patients randomized to dabigatran (treatment arm, n=1274) versus warfarin (control arm, n=1265).
The primary endpoint was recurrent VTE at 6 months. Mean age was 54.7 years, 58% were male.
Non-inferiority margin: HR <2.75. Results: VTE HR 1.10, 95% CI 0.65-1.84. Non-inferiority met.
Follow-up was 6 months. Trial registration: NCT00291330.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 1.10, ciLo: 0.65, ciHi: 1.84 },
            treatment: { n: 1274 },
            control: { n: 1265 },
            baseline: { ageMean: 54.7, malePercent: 58 },
            registration: 'NCT00291330',
            nonInferiority: true
        }
    },
    {
        id: 'CARAVAGGIO',
        source: 'Agnelli G et al. NEJM 2020;382:1599-1607',
        domain: 'Hematology',
        design: 'Non-inferiority',
        text: `CARAVAGGIO: Apixaban vs Dalteparin in Cancer VTE.
Cancer patients with VTE randomized to apixaban (treatment arm, n=576) versus dalteparin (control arm, n=579).
The primary endpoint was recurrent VTE at 6 months. Mean age was 67.2 years, 48% were male.
Non-inferiority margin: HR <2.0. Results: VTE HR 0.63, 95% CI 0.37-1.07. Non-inferiority met.
Follow-up was 6 months. Trial registration: NCT03045406.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.63, ciLo: 0.37, ciHi: 1.07 },
            treatment: { n: 576 },
            control: { n: 579 },
            baseline: { ageMean: 67.2, malePercent: 48 },
            registration: 'NCT03045406',
            nonInferiority: true
        }
    },
    {
        id: 'SELECT-D',
        source: 'Young AM et al. JCO 2018;36:2017-2023',
        domain: 'Hematology',
        design: 'Superiority',
        text: `SELECT-D: Rivaroxaban vs Dalteparin in Cancer VTE.
Cancer patients with VTE randomized to rivaroxaban (treatment arm, n=203) versus dalteparin (control arm, n=203).
The primary endpoint was recurrent VTE at 6 months. Mean age was 67.0 years, 55% were male.
Results: VTE HR 0.43, 95% CI 0.19-0.99. P=0.046.
Follow-up was 6 months. Trial registration: NCT02583191.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.43, ciLo: 0.19, ciHi: 0.99 },
            treatment: { n: 203 },
            control: { n: 203 },
            baseline: { ageMean: 67.0, malePercent: 55 },
            registration: 'NCT02583191'
        }
    },
    {
        id: 'ADAM-VTE',
        source: 'McBane RD et al. JCO 2020;38:498-507',
        domain: 'Hematology',
        design: 'Superiority',
        text: `ADAM VTE: Apixaban vs Dalteparin in Cancer VTE.
Cancer patients with VTE randomized to apixaban (treatment arm, n=145) versus dalteparin (control arm, n=142).
The primary endpoint was major bleeding at 6 months. Mean age was 64.4 years, 43% were male.
Results: VTE HR 0.26, 95% CI 0.09-0.80. P=0.02.
Follow-up was 6 months. Trial registration: NCT02585713.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.26, ciLo: 0.09, ciHi: 0.80 },
            treatment: { n: 145 },
            control: { n: 142 },
            baseline: { ageMean: 64.4, malePercent: 43 },
            registration: 'NCT02585713'
        }
    },
    {
        id: 'Hokusai-Cancer',
        source: 'Raskob GE et al. NEJM 2018;378:615-624',
        domain: 'Hematology',
        design: 'Non-inferiority',
        text: `Hokusai VTE Cancer: Edoxaban vs Dalteparin in Cancer VTE.
Cancer patients with VTE randomized to edoxaban (treatment arm, n=522) versus dalteparin (control arm, n=524).
The primary endpoint was recurrent VTE or major bleeding at 12 months. Mean age was 64.3 years, 50% were male.
Non-inferiority margin: HR <1.5. Results: Composite HR 0.97, 95% CI 0.70-1.36. Non-inferiority met.
Follow-up was 12 months. Trial registration: NCT02073682.`,
        groundTruth: {
            primaryEffect: { type: 'HR', value: 0.97, ciLo: 0.70, ciHi: 1.36 },
            treatment: { n: 522 },
            control: { n: 524 },
            baseline: { ageMean: 64.3, malePercent: 50 },
            registration: 'NCT02073682',
            nonInferiority: true
        }
    }
"""

# Find the position to insert new trials (before the GROUND_TRUTH_CASES array)
insert_marker = "const GROUND_TRUTH_CASES = ["

# Add new batch array definition
batch_def = """
const BATCH15_TO_762 = [""" + batch15_trials + """
];

"""

if insert_marker in content:
    # Insert before GROUND_TRUTH_CASES
    insert_pos = content.find(insert_marker)
    content = content[:insert_pos] + batch_def + content[insert_pos:]

    # Add batch15 to spread
    old_spread = "const GROUND_TRUTH_CASES = ["
    if "...BATCH14_TO_844" in content:
        content = content.replace(
            "...BATCH14_TO_844,",
            "...BATCH14_TO_844,\n    ...BATCH15_TO_762,"
        )
    elif "...BATCH13_TO_784" in content:
        content = content.replace(
            "...BATCH13_TO_784,",
            "...BATCH13_TO_784,\n    ...BATCH15_TO_762,"
        )
    else:
        # Find existing spreads and add batch15
        content = content.replace(
            "const GROUND_TRUTH_CASES = [",
            "const GROUND_TRUTH_CASES = [\n    ...BATCH15_TO_762,"
        )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Added BATCH15_TO_762 with 100 new trials")
else:
    print("Could not find insertion marker")

# Verify new count
with open(file_path, 'r', encoding='utf-8') as f:
    new_content = f.read()
new_count = new_content.count("id: '")
print(f"New trial count: {new_count}")
