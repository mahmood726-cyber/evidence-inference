#!/usr/bin/env python3
"""
Enhance RCTExtractor v4.9.2 -> v5.0.0
- B: Improved MD/SMD extraction
- C: Add P-values, sample sizes, follow-up duration, event rates
"""

import re

file_path = r'C:\Users\user\Downloads\Dataextractor\RCTExtractor_WebApp.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("  Enhancing RCTExtractor v4.9.2 -> v5.0.0")
print("=" * 60)

# ============================================================
# B: IMPROVED MD/SMD PATTERNS
# ============================================================

# Find the existing MD pattern section and replace with enhanced version
old_md_pattern = '''            MD: [
                // Flexible MD pattern with confidence interval [CI] support
                /(?:MD|mean\\s*difference)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:MD|mean\\s*difference)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:mean\\s*difference)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi
            ],'''

new_md_pattern = '''            MD: [
                // Enhanced MD patterns for continuous outcomes
                // "mean difference 2.5 (95% CI 1.2 to 3.8)" or "MD -14.8, 95% CI -15.5 to -14.1"
                /(?:MD|mean\\s*difference)(?:\\s+(?:with|for|in|of|between)(?:\\s+[\\w-]+)+)?[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*(?:kg|mm|points?|mmHg|bpm|ml|L|mg|%)?\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                // "between-group difference of 3.2 (95% CI 1.8-4.6)"
                /(?:between[\\s-]*group\\s+difference|absolute\\s+difference|difference\\s+(?:in|of|between))\\s*(?:was|of|=)?\\s*(-?\\d+\\.?\\d*)\\s*(?:kg|mm|points?|mmHg|%)?\\s*[,;]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                // "change of 0.24 kg (95% CI..." or "reduction of 2.3 points (95% CI..."
                /(?:change|reduction|improvement|decrease|increase)\\s+(?:in\\s+)?(?:[\\w\\s]+)?(?:was|of|=)?\\s*(-?\\d+\\.?\\d*)\\s*(?:kg|mm|points?|mmHg|bpm|ml|L|mg)?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                // "weighted mean difference -0.31" or "mean difference was 3.2"
                /(?:weighted\\s+)?(?:mean\\s+difference|MD)\\s+(?:was|of|=)?\\s*(-?\\d+\\.?\\d*)/gi,
                // "difference −1.6%, 95% CI −7.6 to 4.4%"
                /difference\\s+(-?\\d+\\.?\\d*)\\s*%?\\s*[,;]?\\s*95%?\\s*CI\\s*(-?\\d+\\.?\\d*)\\s*(?:[-–]|to)\\s*(-?\\d+\\.?\\d*)/gi
            ],'''

if old_md_pattern in content:
    content = content.replace(old_md_pattern, new_md_pattern)
    print("[B] MD patterns enhanced")
else:
    print("[B] MD pattern not found - searching...")
    # Try partial match
    if "MD: [" in content and "mean\\s*difference" in content:
        print("    Found MD section but pattern differs")

# Enhanced SMD pattern
old_smd_pattern = '''            SMD: [
                // Flexible SMD pattern with confidence interval [CI] support
                /(?:SMD|standardized?\\s*mean\\s*difference)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:SMD|standardized?\\s*mean\\s*difference)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:standardized?\\s*mean\\s*difference)[,;:\\s=]+(-?\\d+\\.?\\d*)/gi,
                // Hedges' g or Cohen's d
                /(?:hedges['']?\\s*g|cohen['']?s?\\s*d)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi
            ],'''

new_smd_pattern = '''            SMD: [
                // Enhanced SMD/effect size patterns
                /(?:SMD|standardized?\\s*mean\\s*difference)(?:\\s+(?:with|for|in|of)\\s+[\\w-]+)?[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)(?:\\s*\\[CI\\])?[,;:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                // "effect size d = 0.67" or "effect size of 0.45"
                /effect\\s*size\\s*(?:d\\s*)?[=:]?\\s*(-?\\d+\\.?\\d*)\\s*[,;]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)?[,;:\\s]*)?(-?\\d+\\.?\\d*)?\\s*(?:[-–]|\\s+to\\s+)?\\s*(-?\\d+\\.?\\d*)?/gi,
                // "Cohen's d = 0.52" or "Hedges' g = 0.48"
                /(?:cohen['']?s?\\s*d|hedges['']?\\s*g|glass['']?s?\\s*[Δδd])\\s*[=:]?\\s*(-?\\d+\\.?\\d*)\\s*[,;]?\\s*(?:\\(?95%?\\s*(?:CI)?[,;:\\s]*)?(-?\\d+\\.?\\d*)?\\s*(?:[-–]|\\s+to\\s+)?\\s*(-?\\d+\\.?\\d*)?/gi,
                // Simple SMD value
                /(?:SMD|standardized?\\s*mean\\s*difference)\\s+(?:was|of|=)?\\s*(-?\\d+\\.?\\d*)/gi
            ],'''

if old_smd_pattern in content:
    content = content.replace(old_smd_pattern, new_smd_pattern)
    print("[B] SMD patterns enhanced")
else:
    print("[B] SMD pattern not found")

# ============================================================
# C: ADD NEW EXTRACTION FIELDS
# ============================================================

# Find the effectPatterns object and add new fields
# First, find where RateRatio ends and add new patterns

old_rate_ratio_end = '''            RateRatio: [
                /(?:rate\\s*ratio|IRR|incidence\\s*rate\\s*ratio)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:rate\\s*ratio|IRR)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi
            ]'''

new_rate_ratio_end = '''            RateRatio: [
                /(?:rate\\s*ratio|IRR|incidence\\s*rate\\s*ratio)[,;:\\s=]*(-?\\d+\\.?\\d*)\\s*[;,]?\\s*(?:\\(?95%?\\s*(?:CI|confidence\\s*interval)[,:\\s]*)?(-?\\d+\\.?\\d*)\\s*(?:[-–]|\\s+to\\s+)\\s*(-?\\d+\\.?\\d*)/gi,
                /(?:rate\\s*ratio|IRR)\\s+(?:was|of|=)\\s*(-?\\d+\\.?\\d*)/gi
            ],
            // NEW: P-value patterns
            Pvalue: [
                // "P<0.001" or "P = 0.03" or "p-value = 0.045"
                /[Pp][-\\s]*(?:value)?\\s*[=<>]\\s*(0?\\.\\d+|<\\s*0?\\.\\d+)/g,
                // "P<.001" format
                /[Pp]\\s*[<>=]\\s*\\.?(\\d+)/g
            ],
            // NEW: Sample size patterns
            SampleSize: [
                // "n=234" or "N = 1,234" or "(n=500)"
                /[Nn]\\s*[=:]\\s*([\\d,]+)/g,
                // "234 patients" or "1,234 participants"
                /([\\d,]+)\\s*(?:patients|participants|subjects|individuals)/gi,
                // "enrolled 500 patients" or "randomized 1000 patients"
                /(?:enrolled|randomized|recruited|included)\\s*([\\d,]+)\\s*(?:patients|participants)?/gi
            ],
            // NEW: Follow-up duration patterns
            FollowUp: [
                // "median follow-up of 2.4 years" or "mean follow-up 18 months"
                /(?:median|mean)?\\s*follow[\\s-]*up\\s*(?:of|was|:)?\\s*([\\d.]+)\\s*(years?|months?|weeks?|days?)/gi,
                // "followed for 24 months" or "follow-up period of 3 years"
                /follow(?:ed)?[\\s-]*(?:up)?\\s*(?:for|period\\s*of)?\\s*([\\d.]+)\\s*(years?|months?|weeks?|days?)/gi
            ],
            // NEW: Event rate patterns
            EventRate: [
                // "event rate 15.2%" or "mortality rate of 8.5%"
                /(?:event|mortality|death|hospitalization)\\s*rate\\s*(?:of|was|:)?\\s*([\\d.]+)\\s*%/gi,
                // "occurred in 234 patients (15.2%)"
                /occurred\\s+in\\s+[\\d,]+\\s*(?:patients)?\\s*\\(([\\d.]+)\\s*%\\)/gi,
                // "incidence of 12.5%"
                /incidence\\s*(?:of|was|:)?\\s*([\\d.]+)\\s*%/gi
            ],
            // NEW: Absolute risk reduction
            ARR: [
                // "absolute risk reduction 3.2%" or "ARR 2.5%"
                /(?:ARR|absolute\\s*risk\\s*reduction)\\s*(?:of|was|:)?\\s*([\\d.]+)\\s*%?\\s*(?:\\(?95%?\\s*CI[,:\\s]*)?([\\d.]+)?\\s*(?:[-–]|to)?\\s*([\\d.]+)?/gi
            ],
            // NEW: Number needed to treat (enhanced)
            NNT: [
                /(?:NNT|number\\s*needed\\s*to\\s*treat)\\s*(?:of|was|=|:)?\\s*(\\d+)\\s*(?:\\(?95%?\\s*CI[,:\\s]*)?(\\d+)?\\s*(?:[-–]|to)?\\s*(\\d+)?/gi
            ],
            // NEW: NNH (Number needed to harm)
            NNH: [
                /(?:NNH|number\\s*needed\\s*to\\s*harm)\\s*(?:of|was|=|:)?\\s*(\\d+)\\s*(?:\\(?95%?\\s*CI[,:\\s]*)?(\\d+)?\\s*(?:[-–]|to)?\\s*(\\d+)?/gi
            ]'''

if old_rate_ratio_end in content:
    content = content.replace(old_rate_ratio_end, new_rate_ratio_end)
    print("[C] Added P-value, SampleSize, FollowUp, EventRate, ARR, NNT, NNH patterns")
else:
    print("[C] RateRatio section not found exactly - trying alternate")
    # Try to find RateRatio and add after it
    if "RateRatio:" in content:
        print("    Found RateRatio section")

# ============================================================
# Update the extraction function to handle new fields
# ============================================================

# Find the extractEffectMeasures function and update the switch statement
old_switch_case = '''                    case 'NNH':
                        if (match[1]) {
                            result.effectMeasures.push({
                                type: type,
                                value: parseFloat(match[1]),
                                ciLow: match[2] ? parseFloat(match[2]) : null,
                                ciHigh: match[3] ? parseFloat(match[3]) : null
                            });
                        }
                        break;'''

new_switch_case = '''                    case 'NNH':
                        if (match[1]) {
                            result.effectMeasures.push({
                                type: type,
                                value: parseFloat(match[1]),
                                ciLow: match[2] ? parseFloat(match[2]) : null,
                                ciHigh: match[3] ? parseFloat(match[3]) : null
                            });
                        }
                        break;
                    case 'Pvalue':
                        if (match[1]) {
                            const pval = match[1].replace('<', '').trim();
                            if (!result.pValues) result.pValues = [];
                            result.pValues.push(parseFloat(pval) || match[1]);
                        }
                        break;
                    case 'SampleSize':
                        if (match[1]) {
                            const n = parseInt(match[1].replace(/,/g, ''));
                            if (!result.sampleSizes) result.sampleSizes = [];
                            if (n > 0 && n < 1000000) result.sampleSizes.push(n);
                        }
                        break;
                    case 'FollowUp':
                        if (match[1] && match[2]) {
                            if (!result.followUp) result.followUp = [];
                            result.followUp.push({
                                duration: parseFloat(match[1]),
                                unit: match[2].toLowerCase()
                            });
                        }
                        break;
                    case 'EventRate':
                        if (match[1]) {
                            if (!result.eventRates) result.eventRates = [];
                            result.eventRates.push(parseFloat(match[1]));
                        }
                        break;
                    case 'ARR':
                        if (match[1]) {
                            result.effectMeasures.push({
                                type: 'ARR',
                                value: parseFloat(match[1]),
                                ciLow: match[2] ? parseFloat(match[2]) : null,
                                ciHigh: match[3] ? parseFloat(match[3]) : null
                            });
                        }
                        break;'''

if old_switch_case in content:
    content = content.replace(old_switch_case, new_switch_case)
    print("[C] Updated switch statement for new fields")
else:
    print("[C] Switch case not found - may need manual update")

# ============================================================
# Update getSummary to include new fields
# ============================================================

old_summary = '''            // Build summary
            const summary = {
                studyName: result.studyName,
                registration: result.registration,
                effectType: effectType,
                effectValue: effectValue,
                effectCI: effectCI,'''

new_summary = '''            // Build summary
            const summary = {
                studyName: result.studyName,
                registration: result.registration,
                effectType: effectType,
                effectValue: effectValue,
                effectCI: effectCI,
                pValue: result.pValues && result.pValues.length > 0 ? result.pValues[0] : null,
                sampleSize: result.sampleSizes && result.sampleSizes.length > 0 ? Math.max(...result.sampleSizes) : null,
                followUp: result.followUp && result.followUp.length > 0 ? result.followUp[0] : null,'''

if old_summary in content:
    content = content.replace(old_summary, new_summary)
    print("[C] Updated getSummary with new fields")
else:
    print("[C] getSummary section not found")

# ============================================================
# Update version
# ============================================================
content = content.replace("version: '4.9.2-AI-Web'", "version: '5.0.0-Enhanced'")
content = content.replace("version: '4.9.1-AI-Web'", "version: '5.0.0-Enhanced'")
content = content.replace("version: '4.9.0-AI-Web'", "version: '5.0.0-Enhanced'")
print("\n[VERSION] Updated to 5.0.0-Enhanced")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 60)
print("  Enhancement complete!")
print("  New features:")
print("  - Enhanced MD/SMD extraction (continuous outcomes)")
print("  - P-value extraction")
print("  - Sample size extraction")
print("  - Follow-up duration extraction")
print("  - Event rate extraction")
print("  - ARR/NNT/NNH extraction")
print("=" * 60)
