Mahmood Ahmad
Tahir Heart Institute
author@example.com

Evidence Inference: Machine Learning Extraction of Treatment Effects from Clinical Trial Reports

Can machine learning models reliably infer comparative treatment effects from clinical trial reports to accelerate systematic review data extraction workflows? The Evidence Inference dataset contains annotated biomedical articles describing randomized trials with prompts asking whether an intervention significantly increased, decreased, or had no effect on an outcome relative to a comparator. Models train on prompt-article pairs with human-annotated labels and supporting evidence spans using full-text and abstract-only versions for prototyping and evaluation. The expanded 2.0 dataset increased annotations by 25 percent over the original NAACL 2019 release providing stronger baselines and error analysis across intervention-comparator-outcome triplets. Error inspection revealed that ambiguous reporting language and multi-arm trial structures accounted for most disagreements between model predictions and expert annotations. Automated evidence extraction can meaningfully reduce the manual burden of systematic review data collection when paired with human verification. The limitation of prompt-based extraction is that the framework assumes pre-identified intervention-comparator-outcome triplets rather than discovering them from unstructured text.

Outside Notes

Type: methods
Primary estimand: Classification accuracy
App: Evidence Inference v2.0
Data: Annotated RCT articles from BioNLP, NAACL 2019 + 2020 expansion
Code: https://github.com/jayded/evidence-inference
Version: 2.0
Validation: DRAFT

References

1. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.
2. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. BMJ. 2003;327(7414):557-560.
3. Cochrane Handbook for Systematic Reviews of Interventions. Version 6.4. Cochrane; 2023.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI (Claude, Anthropic) was used as a constrained synthesis engine operating on structured inputs and predefined rules for infrastructure generation, not as an autonomous author. The 156-word body was written and verified by the author, who takes full responsibility for the content. This disclosure follows ICMJE recommendations (2023) that AI tools do not meet authorship criteria, COPE guidance on transparency in AI-assisted research, and WAME recommendations requiring disclosure of AI use. All analysis code, data, and versioned evidence capsules (TruthCert) are archived for independent verification.
