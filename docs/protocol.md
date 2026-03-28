        # Evidence Inference: Protocol Registration

        **Author:** Mahmood Ahmad, Royal Free Hospital, London, UK
        **ORCID:** 0009-0003-7781-4478
        **Registration Date:** 2026-03-28
        **Repository:** https://github.com/jayded/evidence-inference.git

        ## Objective

        We have recently collected additional data for this task (https://arxiv.org/abs/2005.04177), which we will present at BioNLP 2020. The data is available at: http://evidence-inference.ebm-nlp.com/download/. We are still working on cleaning the code for release of the new models here, but expect this to be available within a week or so of this writing (6/15/2020).

        ## Methods

        This project employs a deterministic, TruthCert-certified pipeline for evidence synthesis. All analytical choices are pre-specified in this protocol document prior to data analysis. The implementation uses versioned code with fixed random seeds where applicable, structured input schemas, and automated validation against reference outputs. Provenance is recorded via hash-linked evidence locators in accordance with the TruthCert framework. Statistical methods follow established meta-analytic guidelines (Cochrane Handbook, PRISMA 2020) and are validated against reference implementations in R (metafor, meta) or Python with tolerance ≤ 1×10⁻⁶.

        ## Availability

        - Code: https://github.com/jayded/evidence-inference.git
        - Dashboard: https://jayded.github.io/evidence-inference/

        ---

        **AI Disclosure Statement**

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI is used as a constrained synthesis engine operating on structured inputs and predefined rules, rather than as an autonomous author. Deterministic components of the pipeline, together with versioned, reproducible evidence capsules (TruthCert), are designed to support transparent and auditable outputs. All results and text were reviewed and verified by the author, who takes full responsibility for the content. The workflow operationalises key transparency and reporting principles consistent with CONSORT-AI/SPIRIT-AI, including explicit input specification, predefined schemas, logged human-AI interaction, and reproducible outputs.
