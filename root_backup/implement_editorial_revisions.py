#!/usr/bin/env python3
"""
Implement Editorial Revisions for IPD Meta-Analysis Pro
Required revisions from Research Synthesis Methods review:
1. Add mathematical appendix with key formulae
2. Include citations for all implemented methods
3. Add explicit assumption statements for causal methods
4. Improve model diagnostics visualization
"""

import re

filepath = r'C:\Users\user\IPD-Meta-Pro\ipd-meta-pro.html'

# Read the file
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 70)
print("IMPLEMENTING EDITORIAL REVISIONS")
print("=" * 70)

# ============================================================================
# REVISION 1: Mathematical Appendix with Key Formulae
# ============================================================================

mathematical_appendix = '''
// ============================================================================
// EDITORIAL REVISION 1: MATHEMATICAL APPENDIX
// ============================================================================

const MATHEMATICAL_FORMULAE = {
    // Random Effects Meta-Analysis
    randomEffects: {
        title: "Random Effects Model",
        formula: "\\\\hat{\\\\theta} = \\\\frac{\\\\sum_{i=1}^{k} w_i^* \\\\theta_i}{\\\\sum_{i=1}^{k} w_i^*}",
        where: "w_i^* = 1/(\\\\sigma_i^2 + \\\\tau^2)",
        description: "Pooled effect estimate under random effects assumption"
    },

    // Tau-squared estimators
    tau2DL: {
        title: "DerSimonian-Laird Estimator",
        formula: "\\\\hat{\\\\tau}^2_{DL} = \\\\frac{Q - (k-1)}{\\\\sum w_i - \\\\frac{\\\\sum w_i^2}{\\\\sum w_i}}",
        where: "Q = \\\\sum_{i=1}^{k} w_i(\\\\theta_i - \\\\hat{\\\\theta}_{FE})^2",
        citation: "DerSimonian R, Laird N. Meta-analysis in clinical trials. Control Clin Trials. 1986;7(3):177-188."
    },

    tau2REML: {
        title: "REML Estimator",
        formula: "\\\\ell_{REML}(\\\\tau^2) = -\\\\frac{1}{2}\\\\sum_{i=1}^{k}\\\\log(\\\\sigma_i^2 + \\\\tau^2) - \\\\frac{1}{2}\\\\log(\\\\sum w_i^*) - \\\\frac{1}{2}Q^*",
        where: "Maximized iteratively using Fisher scoring",
        citation: "Viechtbauer W. Bias and efficiency of meta-analytic variance estimators. J Educ Behav Stat. 2005;30(3):261-293."
    },

    tau2PM: {
        title: "Paule-Mandel Estimator",
        formula: "Q^*(\\\\hat{\\\\tau}^2_{PM}) = k - 1",
        where: "Solved iteratively for tau-squared",
        citation: "Paule RC, Mandel J. Consensus values and weighting factors. J Res Natl Bur Stand. 1982;87(5):377-385."
    },

    // Heterogeneity
    I2: {
        title: "I-squared Statistic",
        formula: "I^2 = \\\\frac{Q - (k-1)}{Q} \\\\times 100\\\\%",
        where: "Q = Cochran's heterogeneity statistic, k = number of studies",
        interpretation: "0-25% low, 25-50% moderate, 50-75% substantial, >75% considerable",
        citation: "Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. Stat Med. 2002;21(11):1539-1558."
    },

    predictionInterval: {
        title: "Prediction Interval",
        formula: "\\\\hat{\\\\theta} \\\\pm t_{k-2, 1-\\\\alpha/2} \\\\sqrt{\\\\hat{\\\\tau}^2 + SE(\\\\hat{\\\\theta})^2}",
        where: "t = critical value from t-distribution with k-2 df",
        citation: "Riley RD, Higgins JPT, Deeks JJ. Interpretation of random effects meta-analyses. BMJ. 2011;342:d549."
    },

    // Publication Bias
    egger: {
        title: "Egger's Regression Test",
        formula: "\\\\frac{\\\\theta_i}{SE_i} = \\\\beta_0 + \\\\beta_1 \\\\times \\\\frac{1}{SE_i} + \\\\epsilon_i",
        where: "H0: beta_0 = 0 (no small-study effects)",
        citation: "Egger M, et al. Bias in meta-analysis detected by a simple, graphical test. BMJ. 1997;315(7109):629-634."
    },

    begg: {
        title: "Begg's Rank Correlation",
        formula: "\\\\tau_b = \\\\frac{n_c - n_d}{\\\\sqrt{(n_c + n_d + T_\\\\theta)(n_c + n_d + T_{var})}}",
        where: "Kendall's tau between effect sizes and variances",
        citation: "Begg CB, Mazumdar M. Operating characteristics of a rank correlation test for publication bias. Biometrics. 1994;50(4):1088-1101."
    },

    trimFill: {
        title: "Trim and Fill",
        formula: "k_0 = \\\\frac{4S_n - n}{2n + 3}",
        where: "S_n = rank-based estimator of missing studies",
        citation: "Duval S, Tweedie R. Trim and fill: A simple funnel-plot-based method. Biometrics. 2000;56(2):455-463."
    },

    pCurve: {
        title: "P-Curve Analysis",
        formula: "pp_i = \\\\frac{p_i}{0.05}",
        where: "pp = p-value of the p-value under null of no effect",
        citation: "Simonsohn U, Nelson LD, Simmons JP. P-curve: A key to the file-drawer. J Exp Psychol Gen. 2014;143(2):534-547."
    },

    // Survival Analysis
    coxPH: {
        title: "Cox Proportional Hazards",
        formula: "h(t|X) = h_0(t) \\\\exp(\\\\beta^T X)",
        where: "h0(t) = baseline hazard, X = covariates",
        citation: "Cox DR. Regression models and life-tables. J R Stat Soc B. 1972;34(2):187-220."
    },

    kaplanMeier: {
        title: "Kaplan-Meier Estimator",
        formula: "\\\\hat{S}(t) = \\\\prod_{t_i \\\\leq t} \\\\frac{n_i - d_i}{n_i}",
        where: "n_i = at risk at time t_i, d_i = events at time t_i",
        citation: "Kaplan EL, Meier P. Nonparametric estimation from incomplete observations. J Am Stat Assoc. 1958;53(282):457-481."
    },

    logRank: {
        title: "Log-Rank Test",
        formula: "\\\\chi^2 = \\\\frac{(O_1 - E_1)^2}{Var(O_1 - E_1)}",
        where: "O = observed events, E = expected events",
        citation: "Peto R, Peto J. Asymptotically efficient rank invariant test procedures. J R Stat Soc A. 1972;135(2):185-207."
    },

    // Causal Inference
    iptw: {
        title: "Inverse Probability of Treatment Weighting",
        formula: "w_i = \\\\frac{A_i}{e(X_i)} + \\\\frac{1-A_i}{1-e(X_i)}",
        where: "e(X) = P(A=1|X) = propensity score",
        citation: "Robins JM, Hernan MA, Brumback B. Marginal structural models and causal inference in epidemiology. Epidemiology. 2000;11(5):550-560."
    },

    aipw: {
        title: "Augmented IPW (Doubly Robust)",
        formula: "\\\\hat{\\\\psi}_{AIPW} = \\\\frac{1}{n}\\\\sum_{i=1}^{n}\\\\left[\\\\frac{A_iY_i}{e(X_i)} - \\\\frac{A_i - e(X_i)}{e(X_i)}\\\\hat{m}_1(X_i)\\\\right] - ...",
        where: "Combines outcome regression with IPW",
        citation: "Bang H, Robins JM. Doubly robust estimation in missing data and causal inference models. Biometrics. 2005;61(4):962-973."
    },

    tmle: {
        title: "Targeted Maximum Likelihood Estimation",
        formula: "\\\\hat{Q}^*(A,W) = expit(logit(\\\\hat{Q}^0(A,W)) + \\\\epsilon H(A,W))",
        where: "H = clever covariate, epsilon = targeting parameter",
        citation: "van der Laan MJ, Rose S. Targeted Learning. Springer; 2011."
    },

    // Network Meta-Analysis
    nmaModel: {
        title: "Network Meta-Analysis Model",
        formula: "\\\\theta_{jk} = \\\\mu_j - \\\\mu_k",
        where: "Consistency assumption: direct = indirect evidence",
        citation: "Lu G, Ades AE. Combination of direct and indirect evidence in mixed treatment comparisons. Stat Med. 2004;23(20):3105-3124."
    },

    sucra: {
        title: "SUCRA (Surface Under Cumulative Ranking)",
        formula: "SUCRA_j = \\\\frac{\\\\sum_{b=1}^{a-1} cum_j(b)}{a-1}",
        where: "cum_j(b) = cumulative probability of being in top b ranks",
        citation: "Salanti G, Ades AE, Ioannidis JP. Graphical methods and numerical summaries for presenting results from multiple-treatment meta-analysis. J Clin Epidemiol. 2011;64(2):163-171."
    },

    // Bayesian
    bayesianMA: {
        title: "Bayesian Random Effects",
        formula: "\\\\theta_i | \\\\mu, \\\\tau^2 \\\\sim N(\\\\mu, \\\\tau^2 + \\\\sigma_i^2)",
        where: "Prior: mu ~ N(0, 10^6), tau ~ HalfCauchy(0, 0.5)",
        citation: "Sutton AJ, Abrams KR. Bayesian methods in meta-analysis and evidence synthesis. Stat Methods Med Res. 2001;10(4):277-303."
    }
};

function showMathematicalAppendix() {
    const modal = document.createElement('div');
    modal.id = 'mathAppendixModal';
    modal.className = 'modal-overlay active';
    modal.style.cssText = 'display:flex; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.8); z-index:2000; overflow-y:auto; padding:2rem;';

    let html = '<div class="modal" style="max-width:900px; width:95%; max-height:90vh; overflow-y:auto; margin:auto; padding:2rem;">';
    html += '<div class="modal-header"><h2>Mathematical Appendix</h2>';
    html += '<button class="modal-close" onclick="document.getElementById(\\'mathAppendixModal\\').remove()">&times;</button></div>';

    html += '<div style="margin-bottom:1rem;" class="alert alert-info">';
    html += '<strong>Statistical Formulae & Citations</strong><br>';
    html += 'This appendix provides the mathematical foundations for all methods implemented in IPD Meta-Analysis Pro.';
    html += '</div>';

    const categories = {
        'Random Effects Meta-Analysis': ['randomEffects', 'tau2DL', 'tau2REML', 'tau2PM'],
        'Heterogeneity Assessment': ['I2', 'predictionInterval'],
        'Publication Bias': ['egger', 'begg', 'trimFill', 'pCurve'],
        'Survival Analysis': ['coxPH', 'kaplanMeier', 'logRank'],
        'Causal Inference': ['iptw', 'aipw', 'tmle'],
        'Network Meta-Analysis': ['nmaModel', 'sucra'],
        'Bayesian Methods': ['bayesianMA']
    };

    for (const [category, methods] of Object.entries(categories)) {
        html += '<div class="card" style="margin-bottom:1rem;">';
        html += '<h3 style="color:var(--accent-primary); border-bottom:1px solid var(--border-color); padding-bottom:0.5rem; margin-bottom:1rem;">' + category + '</h3>';

        for (const method of methods) {
            const f = MATHEMATICAL_FORMULAE[method];
            if (f) {
                html += '<div style="background:var(--bg-tertiary); padding:1rem; border-radius:8px; margin-bottom:1rem;">';
                html += '<h4 style="margin-bottom:0.5rem;">' + f.title + '</h4>';
                html += '<div style="background:var(--bg-secondary); padding:1rem; border-radius:4px; font-family:serif; font-size:1.1rem; margin:0.5rem 0;">';
                html += '<code style="color:var(--accent-info);">' + f.formula.replace(/\\\\/g, '\\\\') + '</code>';
                html += '</div>';
                if (f.where) {
                    html += '<p style="font-size:0.85rem; color:var(--text-secondary); margin:0.5rem 0;"><strong>Where:</strong> ' + f.where + '</p>';
                }
                if (f.interpretation) {
                    html += '<p style="font-size:0.85rem; color:var(--text-secondary); margin:0.5rem 0;"><strong>Interpretation:</strong> ' + f.interpretation + '</p>';
                }
                if (f.citation) {
                    html += '<p style="font-size:0.8rem; color:var(--accent-primary); font-style:italic; margin-top:0.5rem;">' + f.citation + '</p>';
                }
                html += '</div>';
            }
        }
        html += '</div>';
    }

    html += '<div style="text-align:center; margin-top:1rem;">';
    html += '<button class="btn btn-primary" onclick="exportMathAppendix()">Export as PDF</button> ';
    html += '<button class="btn btn-secondary" onclick="document.getElementById(\\'mathAppendixModal\\').remove()">Close</button>';
    html += '</div>';
    html += '</div>';

    modal.innerHTML = html;
    document.body.appendChild(modal);
}

function exportMathAppendix() {
    let text = "MATHEMATICAL APPENDIX - IPD META-ANALYSIS PRO\\n";
    text += "=".repeat(60) + "\\n\\n";

    for (const [key, f] of Object.entries(MATHEMATICAL_FORMULAE)) {
        text += f.title + "\\n";
        text += "-".repeat(40) + "\\n";
        text += "Formula: " + f.formula + "\\n";
        if (f.where) text += "Where: " + f.where + "\\n";
        if (f.citation) text += "Citation: " + f.citation + "\\n";
        text += "\\n";
    }

    const blob = new Blob([text], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'IPD_Mathematical_Appendix.txt';
    a.click();
}

'''

# ============================================================================
# REVISION 2: Complete Citations Database
# ============================================================================

citations_database = '''
// ============================================================================
// EDITORIAL REVISION 2: COMPREHENSIVE CITATIONS DATABASE
// ============================================================================

const CITATIONS = {
    // Core Meta-Analysis
    dersimonianLaird: {
        authors: "DerSimonian R, Laird N",
        year: 1986,
        title: "Meta-analysis in clinical trials",
        journal: "Control Clin Trials",
        volume: "7(3)",
        pages: "177-188",
        doi: "10.1016/0197-2456(86)90046-2"
    },

    higgins2002: {
        authors: "Higgins JPT, Thompson SG",
        year: 2002,
        title: "Quantifying heterogeneity in a meta-analysis",
        journal: "Stat Med",
        volume: "21(11)",
        pages: "1539-1558",
        doi: "10.1002/sim.1186"
    },

    hartungKnapp: {
        authors: "Hartung J, Knapp G",
        year: 2001,
        title: "A refined method for the meta-analysis of controlled clinical trials with binary outcome",
        journal: "Stat Med",
        volume: "20(24)",
        pages: "3875-3889",
        doi: "10.1002/sim.1009"
    },

    viechtbauer2005: {
        authors: "Viechtbauer W",
        year: 2005,
        title: "Bias and efficiency of meta-analytic variance estimators in the random-effects model",
        journal: "J Educ Behav Stat",
        volume: "30(3)",
        pages: "261-293",
        doi: "10.3102/10769986030003261"
    },

    pauleMandel: {
        authors: "Paule RC, Mandel J",
        year: 1982,
        title: "Consensus values and weighting factors",
        journal: "J Res Natl Bur Stand",
        volume: "87(5)",
        pages: "377-385",
        doi: "10.6028/jres.087.022"
    },

    sidikJonkman: {
        authors: "Sidik K, Jonkman JN",
        year: 2005,
        title: "Simple heterogeneity variance estimation for meta-analysis",
        journal: "J R Stat Soc C",
        volume: "54(2)",
        pages: "367-384",
        doi: "10.1111/j.1467-9876.2005.00489.x"
    },

    // Publication Bias
    egger1997: {
        authors: "Egger M, Davey Smith G, Schneider M, Minder C",
        year: 1997,
        title: "Bias in meta-analysis detected by a simple, graphical test",
        journal: "BMJ",
        volume: "315(7109)",
        pages: "629-634",
        doi: "10.1136/bmj.315.7109.629"
    },

    begg1994: {
        authors: "Begg CB, Mazumdar M",
        year: 1994,
        title: "Operating characteristics of a rank correlation test for publication bias",
        journal: "Biometrics",
        volume: "50(4)",
        pages: "1088-1101",
        doi: "10.2307/2533446"
    },

    duvalTweedie: {
        authors: "Duval S, Tweedie R",
        year: 2000,
        title: "Trim and fill: A simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis",
        journal: "Biometrics",
        volume: "56(2)",
        pages: "455-463",
        doi: "10.1111/j.0006-341X.2000.00455.x"
    },

    simonsohnPcurve: {
        authors: "Simonsohn U, Nelson LD, Simmons JP",
        year: 2014,
        title: "P-curve: A key to the file-drawer",
        journal: "J Exp Psychol Gen",
        volume: "143(2)",
        pages: "534-547",
        doi: "10.1037/a0033242"
    },

    ioannidisExcess: {
        authors: "Ioannidis JPA, Trikalinos TA",
        year: 2007,
        title: "An exploratory test for an excess of significant findings",
        journal: "Clin Trials",
        volume: "4(3)",
        pages: "245-253",
        doi: "10.1177/1740774507079441"
    },

    // IPD Methods
    stewartIPD: {
        authors: "Stewart LA, Tierney JF",
        year: 2002,
        title: "To IPD or not to IPD? Advantages and disadvantages of systematic reviews using individual patient data",
        journal: "Eval Health Prof",
        volume: "25(1)",
        pages: "76-97",
        doi: "10.1177/0163278702025001006"
    },

    rileyIPD: {
        authors: "Riley RD, Lambert PC, Abo-Zaid G",
        year: 2010,
        title: "Meta-analysis of individual participant data: rationale, conduct, and reporting",
        journal: "BMJ",
        volume: "340",
        pages: "c221",
        doi: "10.1136/bmj.c221"
    },

    burkeTwoStage: {
        authors: "Burke DL, Ensor J, Riley RD",
        year: 2017,
        title: "Meta-analysis using individual participant data: one-stage and two-stage approaches",
        journal: "Res Synth Methods",
        volume: "8(2)",
        pages: "204-214",
        doi: "10.1002/jrsm.1224"
    },

    // Survival Analysis
    cox1972: {
        authors: "Cox DR",
        year: 1972,
        title: "Regression models and life-tables",
        journal: "J R Stat Soc B",
        volume: "34(2)",
        pages: "187-220",
        doi: "10.1111/j.2517-6161.1972.tb00899.x"
    },

    kaplanMeier1958: {
        authors: "Kaplan EL, Meier P",
        year: 1958,
        title: "Nonparametric estimation from incomplete observations",
        journal: "J Am Stat Assoc",
        volume: "53(282)",
        pages: "457-481",
        doi: "10.1080/01621459.1958.10501452"
    },

    fineGray: {
        authors: "Fine JP, Gray RJ",
        year: 1999,
        title: "A proportional hazards model for the subdistribution of a competing risk",
        journal: "J Am Stat Assoc",
        volume: "94(446)",
        pages: "496-509",
        doi: "10.1080/01621459.1999.10474144"
    },

    // Causal Inference
    rosenbaumRubin: {
        authors: "Rosenbaum PR, Rubin DB",
        year: 1983,
        title: "The central role of the propensity score in observational studies for causal effects",
        journal: "Biometrika",
        volume: "70(1)",
        pages: "41-55",
        doi: "10.1093/biomet/70.1.41"
    },

    robinsIPTW: {
        authors: "Robins JM, Hernan MA, Brumback B",
        year: 2000,
        title: "Marginal structural models and causal inference in epidemiology",
        journal: "Epidemiology",
        volume: "11(5)",
        pages: "550-560",
        doi: "10.1097/00001648-200009000-00011"
    },

    bangRobins: {
        authors: "Bang H, Robins JM",
        year: 2005,
        title: "Doubly robust estimation in missing data and causal inference models",
        journal: "Biometrics",
        volume: "61(4)",
        pages: "962-973",
        doi: "10.1111/j.1541-0420.2005.00377.x"
    },

    vanderLaanTMLE: {
        authors: "van der Laan MJ, Rose S",
        year: 2011,
        title: "Targeted Learning: Causal Inference for Observational and Experimental Data",
        journal: "Springer",
        pages: "1-628",
        doi: "10.1007/978-1-4419-9782-1"
    },

    // Network Meta-Analysis
    luAdes: {
        authors: "Lu G, Ades AE",
        year: 2004,
        title: "Combination of direct and indirect evidence in mixed treatment comparisons",
        journal: "Stat Med",
        volume: "23(20)",
        pages: "3105-3124",
        doi: "10.1002/sim.1875"
    },

    salantiSUCRA: {
        authors: "Salanti G, Ades AE, Ioannidis JP",
        year: 2011,
        title: "Graphical methods and numerical summaries for presenting results from multiple-treatment meta-analysis",
        journal: "J Clin Epidemiol",
        volume: "64(2)",
        pages: "163-171",
        doi: "10.1016/j.jclinepi.2010.03.016"
    },

    diasNMA: {
        authors: "Dias S, Welton NJ, Sutton AJ, Ades AE",
        year: 2013,
        title: "Evidence synthesis for decision making 2: a generalized linear modeling framework",
        journal: "Med Decis Making",
        volume: "33(5)",
        pages: "607-617",
        doi: "10.1177/0272989X12458724"
    },

    // GRADE
    gradeCertainty: {
        authors: "Guyatt GH, Oxman AD, Vist GE, et al",
        year: 2008,
        title: "GRADE: an emerging consensus on rating quality of evidence and strength of recommendations",
        journal: "BMJ",
        volume: "336(7650)",
        pages: "924-926",
        doi: "10.1136/bmj.39489.470347.AD"
    },

    // Bayesian
    suttonBayesian: {
        authors: "Sutton AJ, Abrams KR",
        year: 2001,
        title: "Bayesian methods in meta-analysis and evidence synthesis",
        journal: "Stat Methods Med Res",
        volume: "10(4)",
        pages: "277-303",
        doi: "10.1177/096228020101000404"
    }
};

function formatCitation(key) {
    const c = CITATIONS[key];
    if (!c) return '';
    return c.authors + ' (' + c.year + '). ' + c.title + '. ' + c.journal + '; ' + c.volume + ':' + c.pages + '.';
}

function showCitationsList() {
    const modal = document.createElement('div');
    modal.id = 'citationsModal';
    modal.className = 'modal-overlay active';
    modal.style.cssText = 'display:flex; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.8); z-index:2000; overflow-y:auto; padding:2rem;';

    let html = '<div class="modal" style="max-width:800px; width:95%; max-height:90vh; overflow-y:auto; margin:auto; padding:2rem;">';
    html += '<div class="modal-header"><h2>References</h2>';
    html += '<button class="modal-close" onclick="document.getElementById(\\'citationsModal\\').remove()">&times;</button></div>';

    html += '<div style="font-size:0.9rem;">';

    const sortedCitations = Object.entries(CITATIONS).sort((a, b) => {
        return a[1].authors.localeCompare(b[1].authors);
    });

    for (const [key, c] of sortedCitations) {
        html += '<p style="margin-bottom:1rem; padding-left:2rem; text-indent:-2rem;">';
        html += '<strong>' + c.authors + '</strong> (' + c.year + '). ';
        html += c.title + '. ';
        html += '<em>' + c.journal + '</em>';
        if (c.volume) html += '; ' + c.volume;
        if (c.pages) html += ':' + c.pages;
        html += '.';
        if (c.doi) html += ' <a href="https://doi.org/' + c.doi + '" target="_blank" style="color:var(--accent-primary);">DOI</a>';
        html += '</p>';
    }

    html += '</div>';
    html += '<div style="text-align:center; margin-top:1rem;">';
    html += '<button class="btn btn-primary" onclick="exportCitations()">Export References</button> ';
    html += '<button class="btn btn-secondary" onclick="document.getElementById(\\'citationsModal\\').remove()">Close</button>';
    html += '</div></div>';

    modal.innerHTML = html;
    document.body.appendChild(modal);
}

function exportCitations() {
    let text = "REFERENCES - IPD META-ANALYSIS PRO\\n";
    text += "=".repeat(60) + "\\n\\n";

    const sortedCitations = Object.entries(CITATIONS).sort((a, b) => {
        return a[1].authors.localeCompare(b[1].authors);
    });

    for (const [key, c] of sortedCitations) {
        text += c.authors + " (" + c.year + "). " + c.title + ". " + c.journal;
        if (c.volume) text += "; " + c.volume;
        if (c.pages) text += ":" + c.pages;
        text += ".";
        if (c.doi) text += " DOI: " + c.doi;
        text += "\\n\\n";
    }

    const blob = new Blob([text], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'IPD_References.txt';
    a.click();
}

'''

# ============================================================================
# REVISION 3: Causal Methods Assumption Statements
# ============================================================================

causal_assumptions = '''
// ============================================================================
// EDITORIAL REVISION 3: CAUSAL INFERENCE ASSUMPTION STATEMENTS
// ============================================================================

const CAUSAL_ASSUMPTIONS = {
    propensityScore: {
        method: "Propensity Score Methods",
        assumptions: [
            {
                name: "Positivity (Overlap)",
                formal: "0 < P(A=1|X) < 1 for all X",
                plain: "Every patient has some probability of receiving either treatment",
                diagnostic: "Check propensity score distributions for both groups overlap",
                violation: "Extreme propensity scores (<0.01 or >0.99) indicate positivity violations"
            },
            {
                name: "Unconfoundedness (No Unmeasured Confounding)",
                formal: "Y(a) \\\\perp A | X for a \\\\in {0,1}",
                plain: "Treatment assignment is independent of potential outcomes given covariates",
                diagnostic: "Cannot be tested directly; use sensitivity analysis (E-value)",
                violation: "Residual confounding biases treatment effect estimates"
            },
            {
                name: "Consistency",
                formal: "Y = Y(A) when treatment A is received",
                plain: "The observed outcome equals the potential outcome under received treatment",
                diagnostic: "Requires well-defined interventions",
                violation: "Multiple versions of treatment or measurement error"
            },
            {
                name: "Correct Model Specification",
                formal: "e(X) correctly specified",
                plain: "The propensity score model includes all confounders with correct functional form",
                diagnostic: "Check covariate balance after weighting/matching",
                violation: "Residual imbalance indicates model misspecification"
            }
        ]
    },

    iptw: {
        method: "Inverse Probability of Treatment Weighting",
        assumptions: [
            {
                name: "Positivity",
                formal: "0 < P(A=1|X) < 1",
                plain: "All covariate patterns must have patients in both treatment groups",
                diagnostic: "Examine weight distribution; truncate extreme weights",
                violation: "Extreme weights inflate variance and bias"
            },
            {
                name: "No Unmeasured Confounding",
                formal: "Y(a) \\\\perp A | X",
                plain: "All confounders are measured and included",
                diagnostic: "Sensitivity analysis required",
                violation: "Biased causal effect estimates"
            },
            {
                name: "Correct PS Model",
                formal: "Propensity model correctly specified",
                plain: "Logistic model includes correct covariates and functional forms",
                diagnostic: "AUC, calibration plots, balance diagnostics",
                violation: "Poor covariate balance after weighting"
            }
        ],
        additionalNotes: "IPTW is sensitive to positivity violations. Consider stabilized weights or truncation."
    },

    aipw: {
        method: "Augmented IPW (Doubly Robust)",
        assumptions: [
            {
                name: "Positivity",
                formal: "0 < P(A=1|X) < 1",
                plain: "Overlap in treatment propensities",
                diagnostic: "Weight distributions",
                violation: "Extreme weights"
            },
            {
                name: "No Unmeasured Confounding",
                formal: "Y(a) \\\\perp A | X",
                plain: "All confounders measured",
                diagnostic: "E-value sensitivity analysis",
                violation: "Biased estimates"
            },
            {
                name: "At Least One Model Correct",
                formal: "Either PS model OR outcome model correctly specified",
                plain: "Doubly robust: consistent if either model is correct",
                diagnostic: "Compare with single-model estimates",
                violation: "Both models wrong leads to bias"
            }
        ],
        advantages: "Doubly robust: requires only one of the two models to be correctly specified for consistency."
    },

    tmle: {
        method: "Targeted Maximum Likelihood Estimation",
        assumptions: [
            {
                name: "Positivity",
                formal: "P(A=1|W) > delta > 0",
                plain: "Bounded away from deterministic treatment",
                diagnostic: "Practical positivity: check g(W) distribution",
                violation: "Truncate or use collaborative TMLE"
            },
            {
                name: "No Unmeasured Confounding",
                formal: "Y(a) \\\\perp A | W",
                plain: "Exchangeability given measured covariates",
                diagnostic: "Cannot verify; requires domain knowledge",
                violation: "Sensitivity analysis (E-value, bounds)"
            },
            {
                name: "Correct Specification (or data-adaptive)",
                formal: "Q and g converge to truth",
                plain: "Can use machine learning for flexible estimation",
                diagnostic: "Cross-validation for model selection",
                violation: "Use Super Learner for robustness"
            }
        ],
        advantages: "Semi-parametric efficient; can use machine learning; targets specific causal parameter."
    },

    gcomputation: {
        method: "G-Computation (Standardization)",
        assumptions: [
            {
                name: "No Unmeasured Confounding",
                formal: "Y(a) \\\\perp A | X",
                plain: "All confounders measured",
                diagnostic: "Domain expertise required",
                violation: "Biased causal effects"
            },
            {
                name: "Correct Outcome Model",
                formal: "E[Y|A,X] correctly specified",
                plain: "Outcome regression includes all confounders correctly",
                diagnostic: "Model fit diagnostics, residual plots",
                violation: "Biased if model misspecified"
            },
            {
                name: "Positivity (weaker form)",
                formal: "Support of X under A=1 and A=0 overlap",
                plain: "Can extrapolate from outcome model",
                diagnostic: "Check covariate distributions",
                violation: "Extrapolation may be unreliable"
            }
        ],
        additionalNotes: "G-computation is model-based; less sensitive to positivity but more to outcome model."
    },

    iv: {
        method: "Instrumental Variable Analysis",
        assumptions: [
            {
                name: "Relevance",
                formal: "Cov(Z, A) \\\\neq 0",
                plain: "Instrument predicts treatment",
                diagnostic: "F-statistic > 10 for strong instruments",
                violation: "Weak instrument bias toward null"
            },
            {
                name: "Independence (Exogeneity)",
                formal: "Z \\\\perp U",
                plain: "Instrument independent of unmeasured confounders",
                diagnostic: "Cannot test; requires domain knowledge",
                violation: "Invalid IV, biased estimates"
            },
            {
                name: "Exclusion Restriction",
                formal: "Z affects Y only through A",
                plain: "No direct effect of instrument on outcome",
                diagnostic: "Cannot test; theoretical justification required",
                violation: "Direct effects bias IV estimates"
            },
            {
                name: "Monotonicity (for LATE)",
                formal: "A_i(z=1) >= A_i(z=0) for all i",
                plain: "No defiers: no one does opposite of instrument",
                diagnostic: "Check for plausibility",
                violation: "LATE interpretation unclear"
            }
        ]
    }
};

function showCausalAssumptions(method = null) {
    const modal = document.createElement('div');
    modal.id = 'causalAssumptionsModal';
    modal.className = 'modal-overlay active';
    modal.style.cssText = 'display:flex; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.8); z-index:2000; overflow-y:auto; padding:2rem;';

    let html = '<div class="modal" style="max-width:900px; width:95%; max-height:90vh; overflow-y:auto; margin:auto; padding:2rem;">';
    html += '<div class="modal-header"><h2>Causal Inference Assumptions</h2>';
    html += '<button class="modal-close" onclick="document.getElementById(\\'causalAssumptionsModal\\').remove()">&times;</button></div>';

    html += '<div class="alert alert-warning" style="margin-bottom:1rem;">';
    html += '<strong>Important:</strong> Causal inference methods require careful consideration of identifiability assumptions. ';
    html += 'Violations can lead to biased treatment effect estimates. Review assumptions before interpreting results.';
    html += '</div>';

    const methodsToShow = method ? [method] : Object.keys(CAUSAL_ASSUMPTIONS);

    for (const m of methodsToShow) {
        const data = CAUSAL_ASSUMPTIONS[m];
        if (!data) continue;

        html += '<div class="card" style="margin-bottom:1rem;">';
        html += '<h3 style="color:var(--accent-primary); margin-bottom:1rem;">' + data.method + '</h3>';

        if (data.advantages) {
            html += '<div class="alert alert-success" style="margin-bottom:1rem;"><strong>Key Advantage:</strong> ' + data.advantages + '</div>';
        }

        html += '<table class="results-table" style="width:100%;">';
        html += '<thead><tr><th>Assumption</th><th>Formal Statement</th><th>Diagnostic</th><th>If Violated</th></tr></thead>';
        html += '<tbody>';

        for (const a of data.assumptions) {
            html += '<tr>';
            html += '<td><strong>' + a.name + '</strong><br><span style="font-size:0.8rem; color:var(--text-muted);">' + a.plain + '</span></td>';
            html += '<td><code style="font-size:0.8rem;">' + a.formal + '</code></td>';
            html += '<td style="font-size:0.85rem;">' + a.diagnostic + '</td>';
            html += '<td style="font-size:0.85rem; color:var(--accent-danger);">' + a.violation + '</td>';
            html += '</tr>';
        }

        html += '</tbody></table>';

        if (data.additionalNotes) {
            html += '<p style="margin-top:1rem; font-size:0.9rem; font-style:italic; color:var(--text-secondary);"><strong>Note:</strong> ' + data.additionalNotes + '</p>';
        }

        html += '</div>';
    }

    html += '<div style="text-align:center; margin-top:1rem;">';
    html += '<button class="btn btn-secondary" onclick="document.getElementById(\\'causalAssumptionsModal\\').remove()">Close</button>';
    html += '</div></div>';

    modal.innerHTML = html;
    document.body.appendChild(modal);
}

// Add assumption check to causal analysis functions
function checkCausalAssumptions(psScores, treatment) {
    const results = {
        positivity: { passed: true, details: [] },
        overlap: { passed: true, details: [] },
        balance: { passed: true, details: [] }
    };

    // Check positivity
    const treated = psScores.filter((_, i) => treatment[i] === 1);
    const control = psScores.filter((_, i) => treatment[i] === 0);

    const minTreated = Math.min(...treated);
    const maxTreated = Math.max(...treated);
    const minControl = Math.min(...control);
    const maxControl = Math.max(...control);

    // Check for extreme propensity scores
    const extremeCount = psScores.filter(p => p < 0.01 || p > 0.99).length;
    if (extremeCount > psScores.length * 0.05) {
        results.positivity.passed = false;
        results.positivity.details.push('Warning: ' + extremeCount + ' observations (' + (extremeCount/psScores.length*100).toFixed(1) + '%) have extreme propensity scores (<0.01 or >0.99)');
    }

    // Check overlap
    const overlapMin = Math.max(minTreated, minControl);
    const overlapMax = Math.min(maxTreated, maxControl);
    const overlapRange = overlapMax - overlapMin;
    const totalRange = Math.max(maxTreated, maxControl) - Math.min(minTreated, minControl);

    if (overlapRange / totalRange < 0.5) {
        results.overlap.passed = false;
        results.overlap.details.push('Warning: Limited overlap in propensity score distributions');
    }

    return results;
}

'''

# ============================================================================
# REVISION 4: Model Diagnostics Visualization
# ============================================================================

model_diagnostics = '''
// ============================================================================
// EDITORIAL REVISION 4: IMPROVED MODEL DIAGNOSTICS VISUALIZATION
// ============================================================================

function showModelDiagnostics() {
    if (!APP.results) {
        showNotification('Run analysis first', 'warning');
        return;
    }

    const modal = document.createElement('div');
    modal.id = 'diagnosticsModal';
    modal.className = 'modal-overlay active';
    modal.style.cssText = 'display:flex; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.8); z-index:2000; overflow-y:auto; padding:2rem;';

    let html = '<div class="modal" style="max-width:1100px; width:95%; max-height:90vh; overflow-y:auto; margin:auto; padding:2rem;">';
    html += '<div class="modal-header"><h2>Model Diagnostics</h2>';
    html += '<button class="modal-close" onclick="document.getElementById(\\'diagnosticsModal\\').remove()">&times;</button></div>';

    html += '<div class="grid-2" style="gap:1rem;">';

    // Residual Plot
    html += '<div class="card"><h4>Standardized Residuals</h4>';
    html += '<canvas id="residualPlot" width="450" height="300"></canvas>';
    html += '<p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem;">Residuals should be randomly scattered around zero with no patterns.</p></div>';

    // Q-Q Plot
    html += '<div class="card"><h4>Normal Q-Q Plot</h4>';
    html += '<canvas id="qqPlot" width="450" height="300"></canvas>';
    html += '<p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem;">Points should follow the diagonal line for normally distributed residuals.</p></div>';

    // Influence Plot
    html += '<div class="card"><h4>Influence Diagnostics</h4>';
    html += '<canvas id="influenceDiagPlot" width="450" height="300"></canvas>';
    html += '<p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem;">Identifies influential studies (Cooks distance, leverage).</p></div>';

    // Funnel Asymmetry
    html += '<div class="card"><h4>Funnel Plot Asymmetry</h4>';
    html += '<canvas id="asymmetryPlot" width="450" height="300"></canvas>';
    html += '<p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem;">Egger regression line (dashed) tests for small-study effects.</p></div>';

    html += '</div>';

    // Diagnostic statistics table
    html += '<div class="card" style="margin-top:1rem;"><h4>Diagnostic Statistics</h4>';
    html += '<table class="results-table"><thead><tr>';
    html += '<th>Diagnostic</th><th>Statistic</th><th>P-value</th><th>Interpretation</th>';
    html += '</tr></thead><tbody id="diagnosticStats"></tbody></table></div>';

    // Normality tests
    html += '<div class="card" style="margin-top:1rem;"><h4>Residual Normality Tests</h4>';
    html += '<table class="results-table"><thead><tr>';
    html += '<th>Test</th><th>Statistic</th><th>P-value</th><th>Result</th>';
    html += '</tr></thead><tbody id="normalityStats"></tbody></table></div>';

    html += '<div style="text-align:center; margin-top:1rem;">';
    html += '<button class="btn btn-primary" onclick="exportDiagnostics()">Export Diagnostics</button> ';
    html += '<button class="btn btn-secondary" onclick="document.getElementById(\\'diagnosticsModal\\').remove()">Close</button>';
    html += '</div></div>';

    modal.innerHTML = html;
    document.body.appendChild(modal);

    // Draw diagnostic plots
    setTimeout(() => {
        drawResidualPlot();
        drawQQPlot();
        drawInfluenceDiagnostics();
        drawAsymmetryPlot();
        populateDiagnosticStats();
        populateNormalityTests();
    }, 100);
}

function drawResidualPlot() {
    const canvas = document.getElementById('residualPlot');
    if (!canvas || !APP.results) return;

    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const padding = 50;

    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--bg-secondary');
    ctx.fillRect(0, 0, w, h);

    const studies = APP.results.studies || [];
    if (studies.length === 0) return;

    // Calculate standardized residuals
    const pooled = APP.results.pooled.effect;
    const residuals = studies.map(s => {
        const resid = s.effect - pooled;
        const stdResid = resid / Math.sqrt(s.variance + (APP.results.heterogeneity.tau2 || 0));
        return { x: s.effect, y: stdResid, study: s.study };
    });

    const xMin = Math.min(...residuals.map(r => r.x)) - 0.1;
    const xMax = Math.max(...residuals.map(r => r.x)) + 0.1;
    const yMin = Math.min(...residuals.map(r => r.y), -3);
    const yMax = Math.max(...residuals.map(r => r.y), 3);

    // Draw axes
    ctx.strokeStyle = getComputedStyle(document.body).getPropertyValue('--border-color');
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, h - padding);
    ctx.lineTo(w - padding, h - padding);
    ctx.stroke();

    // Draw zero line
    const zeroY = h - padding - ((0 - yMin) / (yMax - yMin)) * (h - 2 * padding);
    ctx.strokeStyle = '#ef4444';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(padding, zeroY);
    ctx.lineTo(w - padding, zeroY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw +/- 2 SD lines
    ctx.strokeStyle = '#f59e0b';
    ctx.setLineDash([3, 3]);
    const plus2Y = h - padding - ((2 - yMin) / (yMax - yMin)) * (h - 2 * padding);
    const minus2Y = h - padding - ((-2 - yMin) / (yMax - yMin)) * (h - 2 * padding);
    ctx.beginPath();
    ctx.moveTo(padding, plus2Y);
    ctx.lineTo(w - padding, plus2Y);
    ctx.moveTo(padding, minus2Y);
    ctx.lineTo(w - padding, minus2Y);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw points
    ctx.fillStyle = '#6366f1';
    for (const r of residuals) {
        const x = padding + ((r.x - xMin) / (xMax - xMin)) * (w - 2 * padding);
        const y = h - padding - ((r.y - yMin) / (yMax - yMin)) * (h - 2 * padding);
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
    }

    // Labels
    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--text-primary');
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Fitted Values', w / 2, h - 10);
    ctx.save();
    ctx.translate(15, h / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Standardized Residuals', 0, 0);
    ctx.restore();
}

function drawQQPlot() {
    const canvas = document.getElementById('qqPlot');
    if (!canvas || !APP.results) return;

    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const padding = 50;

    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--bg-secondary');
    ctx.fillRect(0, 0, w, h);

    const studies = APP.results.studies || [];
    if (studies.length === 0) return;

    // Calculate standardized residuals
    const pooled = APP.results.pooled.effect;
    const residuals = studies.map(s => {
        const resid = s.effect - pooled;
        return resid / Math.sqrt(s.variance + (APP.results.heterogeneity.tau2 || 0));
    }).sort((a, b) => a - b);

    // Calculate theoretical quantiles
    const n = residuals.length;
    const theoretical = residuals.map((_, i) => {
        const p = (i + 0.5) / n;
        return MathUtils.normQuantile ? MathUtils.normQuantile(p) : qnorm(p);
    });

    const minVal = Math.min(...residuals, ...theoretical, -3);
    const maxVal = Math.max(...residuals, ...theoretical, 3);

    // Draw axes
    ctx.strokeStyle = getComputedStyle(document.body).getPropertyValue('--border-color');
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, h - padding);
    ctx.lineTo(w - padding, h - padding);
    ctx.stroke();

    // Draw diagonal reference line
    ctx.strokeStyle = '#ef4444';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    const x1 = padding + ((minVal - minVal) / (maxVal - minVal)) * (w - 2 * padding);
    const y1 = h - padding - ((minVal - minVal) / (maxVal - minVal)) * (h - 2 * padding);
    const x2 = padding + ((maxVal - minVal) / (maxVal - minVal)) * (w - 2 * padding);
    const y2 = h - padding - ((maxVal - minVal) / (maxVal - minVal)) * (h - 2 * padding);
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw points
    ctx.fillStyle = '#6366f1';
    for (let i = 0; i < n; i++) {
        const x = padding + ((theoretical[i] - minVal) / (maxVal - minVal)) * (w - 2 * padding);
        const y = h - padding - ((residuals[i] - minVal) / (maxVal - minVal)) * (h - 2 * padding);
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
    }

    // Labels
    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--text-primary');
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Theoretical Quantiles', w / 2, h - 10);
    ctx.save();
    ctx.translate(15, h / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Sample Quantiles', 0, 0);
    ctx.restore();
}

function drawInfluenceDiagnostics() {
    const canvas = document.getElementById('influenceDiagPlot');
    if (!canvas || !APP.results) return;

    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const padding = 50;

    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--bg-secondary');
    ctx.fillRect(0, 0, w, h);

    const studies = APP.results.studies || [];
    if (studies.length === 0) return;

    // Calculate influence measures
    const n = studies.length;
    const pooled = APP.results.pooled.effect;
    const tau2 = APP.results.heterogeneity.tau2 || 0;

    const influences = studies.map((s, i) => {
        const wi = 1 / (s.variance + tau2);
        const sumW = studies.reduce((sum, st) => sum + 1 / (st.variance + tau2), 0);
        const leverage = wi / sumW;

        // Leave-one-out effect
        const otherStudies = studies.filter((_, j) => j !== i);
        const sumWOther = otherStudies.reduce((sum, st) => sum + 1 / (st.variance + tau2), 0);
        const pooledLOO = otherStudies.reduce((sum, st) => sum + st.effect / (st.variance + tau2), 0) / sumWOther;

        const dfbeta = pooled - pooledLOO;
        const resid = s.effect - pooled;
        const stdResid = resid / Math.sqrt(s.variance + tau2);

        // Cook's distance approximation
        const cooksD = (stdResid * stdResid * leverage) / (1 - leverage);

        return { study: s.study, leverage, cooksD, stdResid };
    });

    const maxLev = Math.max(...influences.map(i => i.leverage)) * 1.1;
    const maxCook = Math.max(...influences.map(i => i.cooksD)) * 1.1;

    // Draw axes
    ctx.strokeStyle = getComputedStyle(document.body).getPropertyValue('--border-color');
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, h - padding);
    ctx.lineTo(w - padding, h - padding);
    ctx.stroke();

    // Draw threshold lines
    const avgLev = 1 / n;
    const levThreshold = 2 * avgLev;
    const cookThreshold = 4 / n;

    // Leverage threshold
    const threshX = padding + (levThreshold / maxLev) * (w - 2 * padding);
    ctx.strokeStyle = '#f59e0b';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(threshX, padding);
    ctx.lineTo(threshX, h - padding);
    ctx.stroke();

    // Cook's threshold
    const threshY = h - padding - (cookThreshold / maxCook) * (h - 2 * padding);
    ctx.beginPath();
    ctx.moveTo(padding, threshY);
    ctx.lineTo(w - padding, threshY);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw points
    for (const inf of influences) {
        const x = padding + (inf.leverage / maxLev) * (w - 2 * padding);
        const y = h - padding - (inf.cooksD / maxCook) * (h - 2 * padding);

        // Color by influence
        if (inf.leverage > levThreshold || inf.cooksD > cookThreshold) {
            ctx.fillStyle = '#ef4444';
        } else {
            ctx.fillStyle = '#6366f1';
        }

        ctx.beginPath();
        ctx.arc(x, y, 6, 0, 2 * Math.PI);
        ctx.fill();
    }

    // Labels
    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--text-primary');
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Leverage (Hat Values)', w / 2, h - 10);
    ctx.save();
    ctx.translate(15, h / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText("Cook's Distance", 0, 0);
    ctx.restore();
}

function drawAsymmetryPlot() {
    const canvas = document.getElementById('asymmetryPlot');
    if (!canvas || !APP.results) return;

    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const padding = 50;

    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--bg-secondary');
    ctx.fillRect(0, 0, w, h);

    const studies = APP.results.studies || [];
    if (studies.length === 0) return;

    // Prepare data for Egger plot
    const data = studies.map(s => ({
        x: 1 / Math.sqrt(s.variance),  // precision
        y: s.effect / Math.sqrt(s.variance)  // standardized effect
    }));

    const xMin = 0;
    const xMax = Math.max(...data.map(d => d.x)) * 1.1;
    const yMin = Math.min(...data.map(d => d.y)) - 0.5;
    const yMax = Math.max(...data.map(d => d.y)) + 0.5;

    // Draw axes
    ctx.strokeStyle = getComputedStyle(document.body).getPropertyValue('--border-color');
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, h - padding);
    ctx.lineTo(w - padding, h - padding);
    ctx.stroke();

    // Fit regression line (Egger's test)
    const n = data.length;
    const sumX = data.reduce((s, d) => s + d.x, 0);
    const sumY = data.reduce((s, d) => s + d.y, 0);
    const sumXY = data.reduce((s, d) => s + d.x * d.y, 0);
    const sumX2 = data.reduce((s, d) => s + d.x * d.x, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    // Draw regression line
    ctx.strokeStyle = '#ef4444';
    ctx.setLineDash([5, 5]);
    ctx.lineWidth = 2;
    ctx.beginPath();
    const lineY1 = intercept + slope * xMin;
    const lineY2 = intercept + slope * xMax;
    const y1 = h - padding - ((lineY1 - yMin) / (yMax - yMin)) * (h - 2 * padding);
    const y2 = h - padding - ((lineY2 - yMin) / (yMax - yMin)) * (h - 2 * padding);
    ctx.moveTo(padding, y1);
    ctx.lineTo(w - padding, y2);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.lineWidth = 1;

    // Draw points
    ctx.fillStyle = '#6366f1';
    for (const d of data) {
        const x = padding + ((d.x - xMin) / (xMax - xMin)) * (w - 2 * padding);
        const y = h - padding - ((d.y - yMin) / (yMax - yMin)) * (h - 2 * padding);
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
    }

    // Labels
    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue('--text-primary');
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Precision (1/SE)', w / 2, h - 10);
    ctx.save();
    ctx.translate(15, h / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Standardized Effect', 0, 0);
    ctx.restore();

    // Show intercept (Egger test)
    ctx.fillStyle = '#ef4444';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Intercept: ' + intercept.toFixed(3), padding + 10, padding + 20);
}

function populateDiagnosticStats() {
    const tbody = document.getElementById('diagnosticStats');
    if (!tbody || !APP.results) return;

    const studies = APP.results.studies || [];
    const n = studies.length;
    const het = APP.results.heterogeneity;

    let html = '';

    // Cochran's Q
    html += '<tr><td>Cochran\\'s Q</td>';
    html += '<td>' + (het.Q || 0).toFixed(2) + '</td>';
    html += '<td>' + (het.pQ || 0).toFixed(4) + '</td>';
    html += '<td>' + ((het.pQ || 1) < 0.1 ? '<span style="color:var(--accent-warning);">Significant heterogeneity</span>' : 'No significant heterogeneity') + '</td></tr>';

    // I-squared
    html += '<tr><td>I<sup>2</sup></td>';
    html += '<td>' + (het.I2 || 0).toFixed(1) + '%</td>';
    html += '<td>-</td>';
    const i2Interp = (het.I2 || 0) < 25 ? 'Low' : (het.I2 || 0) < 50 ? 'Moderate' : (het.I2 || 0) < 75 ? 'Substantial' : 'Considerable';
    html += '<td>' + i2Interp + ' heterogeneity</td></tr>';

    // Tau-squared
    html += '<tr><td>&tau;<sup>2</sup></td>';
    html += '<td>' + (het.tau2 || 0).toFixed(4) + '</td>';
    html += '<td>-</td>';
    html += '<td>Between-study variance</td></tr>';

    tbody.innerHTML = html;
}

function populateNormalityTests() {
    const tbody = document.getElementById('normalityStats');
    if (!tbody || !APP.results) return;

    const studies = APP.results.studies || [];
    const pooled = APP.results.pooled.effect;
    const tau2 = APP.results.heterogeneity.tau2 || 0;

    const residuals = studies.map(s => {
        const resid = s.effect - pooled;
        return resid / Math.sqrt(s.variance + tau2);
    });

    // Shapiro-Wilk approximation
    const n = residuals.length;
    const sorted = [...residuals].sort((a, b) => a - b);
    const mean = residuals.reduce((a, b) => a + b, 0) / n;
    const variance = residuals.reduce((a, b) => a + (b - mean) ** 2, 0) / (n - 1);

    // Simple skewness and kurtosis
    const skewness = residuals.reduce((a, b) => a + ((b - mean) / Math.sqrt(variance)) ** 3, 0) / n;
    const kurtosis = residuals.reduce((a, b) => a + ((b - mean) / Math.sqrt(variance)) ** 4, 0) / n - 3;

    let html = '';

    // Skewness test
    const skewSE = Math.sqrt(6 / n);
    const skewZ = skewness / skewSE;
    const skewP = 2 * (1 - (MathUtils.normCDF ? MathUtils.normCDF(Math.abs(skewZ)) : normCDF(Math.abs(skewZ))));
    html += '<tr><td>Skewness</td>';
    html += '<td>' + skewness.toFixed(3) + '</td>';
    html += '<td>' + skewP.toFixed(4) + '</td>';
    html += '<td>' + (skewP < 0.05 ? '<span style="color:var(--accent-warning);">Significant skew</span>' : 'Acceptable') + '</td></tr>';

    // Kurtosis test
    const kurtSE = Math.sqrt(24 / n);
    const kurtZ = kurtosis / kurtSE;
    const kurtP = 2 * (1 - (MathUtils.normCDF ? MathUtils.normCDF(Math.abs(kurtZ)) : normCDF(Math.abs(kurtZ))));
    html += '<tr><td>Excess Kurtosis</td>';
    html += '<td>' + kurtosis.toFixed(3) + '</td>';
    html += '<td>' + kurtP.toFixed(4) + '</td>';
    html += '<td>' + (kurtP < 0.05 ? '<span style="color:var(--accent-warning);">Non-normal kurtosis</span>' : 'Acceptable') + '</td></tr>';

    tbody.innerHTML = html;
}

function exportDiagnostics() {
    let text = "MODEL DIAGNOSTICS REPORT\\n";
    text += "=".repeat(50) + "\\n\\n";
    text += "Generated: " + new Date().toISOString() + "\\n\\n";

    if (APP.results) {
        const het = APP.results.heterogeneity;
        text += "HETEROGENEITY STATISTICS\\n";
        text += "-".repeat(30) + "\\n";
        text += "Q = " + (het.Q || 0).toFixed(2) + " (p = " + (het.pQ || 0).toFixed(4) + ")\\n";
        text += "I2 = " + (het.I2 || 0).toFixed(1) + "%\\n";
        text += "tau2 = " + (het.tau2 || 0).toFixed(4) + "\\n\\n";
    }

    const blob = new Blob([text], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'Model_Diagnostics.txt';
    a.click();
}

'''

# ============================================================================
# ADD HEADER BUTTONS FOR NEW FEATURES
# ============================================================================

header_buttons = '''
            <button class="btn btn-secondary" onclick="showMathematicalAppendix()" title="Statistical Formulae">Formulae</button>
            <button class="btn btn-secondary" onclick="showCitationsList()" title="References">References</button>
            <button class="btn btn-secondary" onclick="showCausalAssumptions()" title="Causal Assumptions">Assumptions</button>
            <button class="btn btn-secondary" onclick="showModelDiagnostics()" title="Model Diagnostics">Diagnostics</button>
'''

# ============================================================================
# APPLY REVISIONS
# ============================================================================

# Find the closing </script> tag to insert new code before it
script_end = content.rfind('</script>')
if script_end == -1:
    print("[ERROR] Could not find </script> tag")
else:
    # Insert all revisions before </script>
    all_revisions = mathematical_appendix + citations_database + causal_assumptions + model_diagnostics

    content = content[:script_end] + '\n' + all_revisions + '\n' + content[script_end:]
    print("[OK] Added Mathematical Appendix")
    print("[OK] Added Citations Database")
    print("[OK] Added Causal Assumptions")
    print("[OK] Added Model Diagnostics")

# Add header buttons after MASEM button
masem_button = 'onclick="showMediationAnalysis()" title="Meta-Analytic SEM Mediation">MASEM</button>'
if masem_button in content:
    content = content.replace(masem_button, masem_button + header_buttons)
    print("[OK] Added header buttons for new features")
else:
    print("[WARN] Could not find MASEM button to add new buttons")

# Write the updated file
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Count lines
with open(filepath, 'r', encoding='utf-8') as f:
    lines = len(f.readlines())

print("\n" + "=" * 70)
print("EDITORIAL REVISIONS COMPLETE")
print("=" * 70)
print(f"File: {filepath}")
print(f"Lines: {lines}")
print("\nNew Features Added:")
print("  1. Mathematical Appendix - showMathematicalAppendix()")
print("  2. Citations Database - showCitationsList()")
print("  3. Causal Assumptions - showCausalAssumptions()")
print("  4. Model Diagnostics - showModelDiagnostics()")
print("\nNew Header Buttons:")
print("  - Formulae")
print("  - References")
print("  - Assumptions")
print("  - Diagnostics")
