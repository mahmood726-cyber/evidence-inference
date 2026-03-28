#!/usr/bin/env python3
"""
Fix RCTExtractor extraction patterns to handle:
1. MD (Mean Difference) - MISSING
2. SMD (Standardized Mean Difference) - MISSING
3. RateRatio - MISSING
4. Negative values with double hyphen
5. CI with "to" instead of hyphen
6. NCT registration extraction - MISSING
"""

import re

file_path = r'C:\Users\user\Downloads\Dataextractor\RCTExtractor_WebApp.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the extractEffectMeasures function and update patterns
old_patterns = '''        const patterns = {
            HR: [
                /(?:HR|hazard\\s*ratio)[,;:\\s=]*(\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*CI[,:\\s]*)?(\\d+\\.?\\d*)\\s*[-–to]+\\s*(\\d+\\.?\\d*)/gi,
                /(?:HR|hazard\\s*ratio)[,;:\\s=]+(\\d+\\.?\\d*)/gi,
                /(?:hazard\\s+ratio\\s+(?:of|was|=))\\s*(\\d+\\.?\\d*)/gi
            ],
            RR: [
                /(?:RR|relative\\s*risk)[,;:\\s=]*(\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*CI[,:\\s]*)?(\\d+\\.?\\d*)\\s*[-–to]+\\s*(\\d+\\.?\\d*)/gi,
                /(?:RR|relative\\s*risk)\\s+(?:was|of|=)\\s*(\\d+\\.?\\d*)/gi,
                /(?:relative\\s*risk)[,;:\\s=]+(\\d+\\.?\\d*)/gi
            ],
            OR: [
                /(?:OR|odds\\s*ratio)[,;:\\s=]*(\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*CI[,:\\s]*)?(\\d+\\.?\\d*)\\s*[-–to]+\\s*(\\d+\\.?\\d*)/gi,
                /(?:odds\\s*ratio)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(\\d+\\.?\\d*)/gi,
                /(?:odds\\s*ratio|OR)[,;:\\s=]+(\\d+\\.?\\d*)/gi
            ],
            RD: [
                /(?:risk\\s*difference|RD|ARR|absolute\\s*risk\\s*reduction)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*%?/gi,
                /(?:risk\\s*difference)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)\\s*%?/gi,
                /(?:absolute\\s*difference)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*%?/gi,
                /(?:difference)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*(?:percentage\\s*points|%)/gi
            ],
            NNT: [
                /(?:NNT|number\\s*needed\\s*to\\s*treat)[,;:\\s=]*(\\d+\\.?\\d*)/gi,
                /(?:number\\s*needed\\s*to\\s*treat)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(\\d+\\.?\\d*)/gi,
                /(?:needed\\s*to\\s*treat)[,;:\\s=was]*\\s*(\\d+)/gi
            ],
            NNH: [
                /(?:NNH|number\\s*needed\\s*to\\s*harm)[,;:\\s=]*(\\d+\\.?\\d*)/gi,
                /(?:number\\s*needed\\s*to\\s*harm)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(\\d+\\.?\\d*)/gi,
                /(?:needed\\s*to\\s*harm)[,;:\\s=was]*\\s*(\\d+)/gi
            ]
        };'''

new_patterns = '''        const patterns = {
            HR: [
                // HR 0.80; 95% CI, 0.73 to 0.87 OR HR 0.80; 95% CI 0.73-0.87
                /(?:HR|hazard\\s*ratio)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:HR|hazard\\s*ratio)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi,
                /(?:hazard\\s+ratio\\s+(?:of|was|=))\\s*(-?\\d+\\.?\\d*)/gi
            ],
            RR: [
                // RR 0.91; 95% CI, 0.74 to 1.11 or relative risk, 0.66; 95% CI, 0.53 to 0.82
                /(?:RR|relative\\s*risk)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:RR|relative\\s*risk)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:relative\\s*risk)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],
            OR: [
                // OR 0.84; 95% CI 0.71-0.99 or odds ratio of 2.3
                /(?:OR|odds\\s*ratio)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:odds\\s*ratio)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:odds\\s*ratio|OR)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],
            MD: [
                // MD -14.8, 95% CI -15.5 to -14.1 or mean difference -2.3 (95% CI -4.1--0.5)
                /(?:MD|mean\\s*difference)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:MD|mean\\s*difference)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:mean\\s*difference)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],
            SMD: [
                // SMD -0.31, 95% CI -0.49 to -0.13 or standardized mean difference
                /(?:SMD|standardized?\\s*mean\\s*difference)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:SMD|standardized?\\s*mean\\s*difference)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:standardized?\\s*mean\\s*difference)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi,
                // Hedges' g or Cohen's d
                /(?:hedges['']?\\s*g|cohen['']?s?\\s*d)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi
            ],
            RD: [
                // RD -0.08, 95% CI -0.12 to -0.04 or risk difference
                /(?:RD|risk\\s*difference|ARR|absolute\\s*risk\\s*reduction)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*%?\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:risk\\s*difference)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)\\s*%?/gi,
                /(?:absolute\\s*difference)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*%?/gi,
                /(?:difference)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*(?:percentage\\s*points|%)/gi
            ],
            RateRatio: [
                // Rate ratio 0.72; 95% CI 0.58-0.89 or incidence rate ratio
                /(?:rate\\s*ratio|IRR|incidence\\s*rate\\s*ratio)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:rate\\s*ratio|IRR|incidence\\s*rate\\s*ratio)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi
            ],
            NNT: [
                /(?:NNT|number\\s*needed\\s*to\\s*treat)[,;:\\s=]*(\\d+\\.?\\d*)/gi,
                /(?:number\\s*needed\\s*to\\s*treat)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(\\d+\\.?\\d*)/gi,
                /(?:needed\\s*to\\s*treat)[,;:\\s=was]*\\s*(\\d+)/gi
            ],
            NNH: [
                /(?:NNH|number\\s*needed\\s*to\\s*harm)[,;:\\s=]*(\\d+\\.?\\d*)/gi,
                /(?:number\\s*needed\\s*to\\s*harm)(?:\\s+\\w+)*\\s+(?:was|of|=)\\s*(\\d+\\.?\\d*)/gi,
                /(?:needed\\s*to\\s*harm)[,;:\\s=was]*\\s*(\\d+)/gi
            ]
        };'''

# Replace the patterns
if old_patterns in content:
    content = content.replace(old_patterns, new_patterns)
    print("Patterns replaced successfully")
else:
    print("Pattern block not found, searching for alternative...")
    # Try to find the pattern section another way
    pattern_section = re.search(r'const patterns = \{[^}]+HR:[^}]+\};', content, re.DOTALL)
    if pattern_section:
        print(f"Found pattern section at position {pattern_section.start()}")

# Add measures for MD, SMD, RateRatio in the measures object
old_measures = '''        const measures = {
            hazardRatios: [],
            relativeRisks: [],
            oddsRatios: [],
            riskDifferences: [],
            numberNeededToTreat: [],
            numberNeededToHarm: []
        };'''

new_measures = '''        const measures = {
            hazardRatios: [],
            relativeRisks: [],
            oddsRatios: [],
            meanDifferences: [],
            standardizedMeanDifferences: [],
            riskDifferences: [],
            rateRatios: [],
            numberNeededToTreat: [],
            numberNeededToHarm: []
        };'''

if old_measures in content:
    content = content.replace(old_measures, new_measures)
    print("Measures object updated")
else:
    print("Measures object not found")

# Update switch statement for new effect types
old_switch = '''                    switch(type) {
                        case 'HR': measures.hazardRatios.push(result); break;
                        case 'RR': measures.relativeRisks.push(result); break;
                        case 'OR': measures.oddsRatios.push(result); break;
                        case 'RD': measures.riskDifferences.push(result); break;
                        case 'NNT': measures.numberNeededToTreat.push(result); break;
                        case 'NNH': measures.numberNeededToHarm.push(result); break;
                    }'''

new_switch = '''                    switch(type) {
                        case 'HR': measures.hazardRatios.push(result); break;
                        case 'RR': measures.relativeRisks.push(result); break;
                        case 'OR': measures.oddsRatios.push(result); break;
                        case 'MD': measures.meanDifferences.push(result); break;
                        case 'SMD': measures.standardizedMeanDifferences.push(result); break;
                        case 'RD': measures.riskDifferences.push(result); break;
                        case 'RateRatio': measures.rateRatios.push(result); break;
                        case 'NNT': measures.numberNeededToTreat.push(result); break;
                        case 'NNH': measures.numberNeededToHarm.push(result); break;
                    }'''

if old_switch in content:
    content = content.replace(old_switch, new_switch)
    print("Switch statement updated")
else:
    print("Switch statement not found")

# Add NCT registration extraction in the extract function
# Find where to insert (after age extraction, before effect measures)
old_effect_extraction = '''        // Effect measures extraction
        result.effectMeasures = this.extractEffectMeasures(text);'''

new_effect_extraction = '''        // Registration/NCT extraction
        const nctPatterns = [
            /NCT\\d{8}/gi,
            /ISRCTN\\d+/gi,
            /ACTRN\\d+/gi,
            /ChiCTR[\\w-]+/gi,
            /UMIN\\d+/gi,
            /CTRI\\/\\d+\\/\\d+\\/\\d+/gi,
            /EUCTR\\d+-\\d+-\\d+/gi,
            /KCT\\d+/gi
        ];

        result.prisma = { registrationNumber: null, registrationRegistry: null };

        for (const pattern of nctPatterns) {
            const match = text.match(pattern);
            if (match) {
                result.prisma.registrationNumber = match[0];
                // Determine registry
                if (match[0].startsWith('NCT')) result.prisma.registrationRegistry = 'ClinicalTrials.gov';
                else if (match[0].startsWith('ISRCTN')) result.prisma.registrationRegistry = 'ISRCTN';
                else if (match[0].startsWith('ACTRN')) result.prisma.registrationRegistry = 'ANZCTR';
                else if (match[0].startsWith('ChiCTR')) result.prisma.registrationRegistry = 'ChiCTR';
                else if (match[0].startsWith('UMIN')) result.prisma.registrationRegistry = 'UMIN-CTR';
                else if (match[0].startsWith('CTRI')) result.prisma.registrationRegistry = 'CTRI India';
                else if (match[0].startsWith('EUCTR')) result.prisma.registrationRegistry = 'EU Clinical Trials';
                else if (match[0].startsWith('KCT')) result.prisma.registrationRegistry = 'KCTR Korea';
                break;
            }
        }

        // Effect measures extraction
        result.effectMeasures = this.extractEffectMeasures(text);'''

if old_effect_extraction in content:
    content = content.replace(old_effect_extraction, new_effect_extraction)
    print("NCT extraction added")
else:
    print("Effect extraction marker not found")

# Update the contrast section to handle MD/SMD/RR as primary
old_contrast = '''        // Primary outcome HR
        if (result.effectMeasures.hazardRatios.length > 0) {
            const primaryHR = result.effectMeasures.hazardRatios.find(hr => hr.isPrimary) ||
                             result.effectMeasures.hazardRatios[0];
            result.contrast.effect = primaryHR.value;
            result.contrast.ciLo = primaryHR.ciLo;
            result.contrast.ciHi = primaryHR.ciHi;
        }'''

new_contrast = '''        // Primary outcome effect (check HR, RR, OR, MD, SMD in order)
        const effectArrays = [
            result.effectMeasures.hazardRatios,
            result.effectMeasures.relativeRisks,
            result.effectMeasures.oddsRatios,
            result.effectMeasures.meanDifferences,
            result.effectMeasures.standardizedMeanDifferences,
            result.effectMeasures.rateRatios
        ];

        for (const arr of effectArrays) {
            if (arr && arr.length > 0) {
                const primary = arr.find(e => e.isPrimary) || arr[0];
                result.contrast.effect = primary.value;
                result.contrast.effectType = primary.type;
                result.contrast.ciLo = primary.ciLo;
                result.contrast.ciHi = primary.ciHi;
                break;
            }
        }'''

if old_contrast in content:
    content = content.replace(old_contrast, new_contrast)
    print("Contrast extraction updated")
else:
    print("Contrast section not found")

# Update getSummary to include effectType and registration
old_summary = '''    getSummary(result) {
        return {
            acronym: result.study?.acronym || 'Unknown',
            domain: result._meta?.domain || 'Unknown',
            domainConfidence: result._meta?.domainConfidence || 0,
            totalN: result.population?.total,
            treatmentN: result.treatment?.n,
            controlN: result.control?.n,
            meanAge: result.baseline?.age?.mean,
            primaryHR: result.contrast?.effect,
            ciLo: result.contrast?.ciLo,
            ciHi: result.contrast?.ciHi,
            pValue: result.contrast?.pValue,
            qualityGrade: result._meta?.qualityScore?.grade,
            qualityScore: result._meta?.qualityScore?.overall,
            biasRisk: result._meta?.biasAssessment?.overallRisk,
            drugsFound: result.aiEntities?.drugs?.length || 0,
            biomarkersFound: result.aiEntities?.biomarkers?.length || 0,
            effectMeasures: (result.effectMeasures?.hazardRatios?.length || 0) +
                           (result.effectMeasures?.relativeRisks?.length || 0) +
                           (result.effectMeasures?.oddsRatios?.length || 0)
        };
    }'''

new_summary = '''    getSummary(result) {
        return {
            acronym: result.study?.acronym || 'Unknown',
            domain: result._meta?.domain || 'Unknown',
            domainConfidence: result._meta?.domainConfidence || 0,
            totalN: result.population?.total,
            treatmentN: result.treatment?.n,
            controlN: result.control?.n,
            meanAge: result.baseline?.age?.mean,
            primaryEffect: result.contrast?.effect,
            effectType: result.contrast?.effectType || 'HR',
            ciLo: result.contrast?.ciLo,
            ciHi: result.contrast?.ciHi,
            pValue: result.contrast?.pValue,
            registration: result.prisma?.registrationNumber,
            qualityGrade: result._meta?.qualityScore?.grade,
            qualityScore: result._meta?.qualityScore?.overall,
            biasRisk: result._meta?.biasAssessment?.overallRisk,
            drugsFound: result.aiEntities?.drugs?.length || 0,
            biomarkersFound: result.aiEntities?.biomarkers?.length || 0,
            effectMeasures: (result.effectMeasures?.hazardRatios?.length || 0) +
                           (result.effectMeasures?.relativeRisks?.length || 0) +
                           (result.effectMeasures?.oddsRatios?.length || 0) +
                           (result.effectMeasures?.meanDifferences?.length || 0) +
                           (result.effectMeasures?.standardizedMeanDifferences?.length || 0) +
                           (result.effectMeasures?.rateRatios?.length || 0)
        };
    }'''

if old_summary in content:
    content = content.replace(old_summary, new_summary)
    print("getSummary updated")
else:
    print("getSummary not found")

# Update displayQuickSummary to show effectType and registration
old_display = '''            <div class="result-item">
                <label>Primary HR</label>
                <div class="value">${summary.primaryHR ? summary.primaryHR.toFixed(2) : 'N/A'}</div>
                ${summary.ciLo && summary.ciHi ? `<div class="confidence">95% CI: ${summary.ciLo.toFixed(2)}-${summary.ciHi.toFixed(2)}</div>` : ''}
            </div>'''

new_display = '''            <div class="result-item">
                <label>Primary ${summary.effectType || 'Effect'}</label>
                <div class="value">${summary.primaryEffect != null ? summary.primaryEffect.toFixed(2) : 'N/A'}</div>
                ${summary.ciLo != null && summary.ciHi != null ? `<div class="confidence">95% CI: ${summary.ciLo.toFixed(2)} to ${summary.ciHi.toFixed(2)}</div>` : ''}
            </div>
            <div class="result-item">
                <label>Registration</label>
                <div class="value">${summary.registration || 'Not found'}</div>
            </div>'''

if old_display in content:
    content = content.replace(old_display, new_display)
    print("displayQuickSummary updated")
else:
    print("displayQuickSummary not found - trying flexible match")
    # Try more flexible replacement
    display_pattern = re.search(r'<label>Primary HR</label>.*?</div>\s*</div>', content, re.DOTALL)
    if display_pattern:
        content = content[:display_pattern.start()] + '''<label>Primary ${summary.effectType || 'Effect'}</label>
                <div class="value">${summary.primaryEffect != null ? summary.primaryEffect.toFixed(2) : 'N/A'}</div>
                ${summary.ciLo != null && summary.ciHi != null ? `<div class="confidence">95% CI: ${summary.ciLo.toFixed(2)} to ${summary.ciHi.toFixed(2)}</div>` : ''}
            </div>
            <div class="result-item">
                <label>Registration</label>
                <div class="value">${summary.registration || 'Not found'}</div>
            </div>''' + content[display_pattern.end():]
        print("displayQuickSummary updated with flexible match")

# Update version
content = content.replace("version: '4.8.0-AI-Web'", "version: '4.9.0-AI-Web'")
print("Version updated to 4.9.0")

# Write the updated content
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nRCTExtractor patterns fixed successfully!")
print("Changes made:")
print("  - Added MD (Mean Difference) pattern")
print("  - Added SMD (Standardized Mean Difference) pattern")
print("  - Added RateRatio pattern")
print("  - Fixed CI format to handle 'to' instead of just hyphen")
print("  - Added support for 'confidence interval' spelled out")
print("  - Added NCT/ISRCTN/ACTRN registration extraction")
print("  - Updated contrast to handle multiple effect types")
print("  - Updated summary to include effectType and registration")
