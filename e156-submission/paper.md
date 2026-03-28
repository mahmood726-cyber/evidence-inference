Mahmood Ahmad
Tahir Heart Institute
mahmood.ahmad2@nhs.net

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

1. Marshall IJ, Noel-Storr A, Kuber J, et al. Machine learning for identifying randomized controlled trials: an evaluation and practitioner's guide. Res Synth Methods. 2018;9(4):602-614.
2. Jonnalagadda SR, Goyal P, Huffman MD. Automating data extraction in systematic reviews: a systematic review. Syst Rev. 2015;4:78.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI is used as a constrained synthesis engine operating on structured inputs and predefined rules, rather than as an autonomous author. Deterministic components of the pipeline, together with versioned, reproducible evidence capsules (TruthCert), are designed to support transparent and auditable outputs. All results and text were reviewed and verified by the author, who takes full responsibility for the content. The workflow operationalises key transparency and reporting principles consistent with CONSORT-AI/SPIRIT-AI, including explicit input specification, predefined schemas, logged human-AI interaction, and reproducible outputs.
