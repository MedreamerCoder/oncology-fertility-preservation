# Public artifact manifest

This manifest maps manuscript commitments to the files needed for an independent audit. “Included” means that the public artifact is present in this repository. “Verification required” means a candidate file is present but the authors still need to confirm that it is the exact sanitized artifact used for the reported study. “Author action required” means the study-exact material is not yet publicly available.

| Manuscript commitment | Status | Public artifact / action |
|---|---|---|
| 20 de-identified clinical cases | Included | `data/clinical_cases/cases_rubric_modelResponse.json` |
| Individualized scoring rubrics | Included | `data/clinical_cases/cases_rubric_modelResponse.json` |
| OncoFert-LLM, DeepSeek, and Qwen case answers | Included | `data/clinical_cases/cases_rubric_modelResponse.json` |
| Validation and weighted-scoring code | Included (reconstructed) | `src/repro/` |
| Case comparison, ICC, bias, and bootstrap code | Included (reconstructed) | `src/repro/case_analysis.py` |
| MCQ analysis code | Included (reconstructed) | `src/repro/mcq_analysis.py` |
| Usability/literacy analysis code | Included (reconstructed) | `src/repro/usability.py` |
| 50-item MCQ benchmark and answer key | **Author action required** | Replace the placeholder `data/mcq/mcq_items.csv` with the approved de-identified source file |
| All three runs for five MCQ configurations | **Author action required** | Fill `data/mcq/mcq_responses.csv` from original run logs |
| Atomic scores from three automated judges | **Author action required** | Fill `data/ratings/case_ratings.csv` from original evaluator records |
| Atomic scores from three blinded experts | **Author action required** | Fill `data/ratings/case_ratings.csv` using pseudonymous evaluator IDs |
| Exact automated-review prompt | Included | `prompts/automated_judge_prompt.md` |
| Exact study prompts for every benchmark | **Author action required** | Add versioned files under `prompts/` |
| Model/version/parameter/run metadata | **Author action required** | Complete `metadata/model_runs.csv` and provider/version documentation |
| Pre/post literacy item-level data | **Author action required** | Fill `data/usability/usability_literacy.csv` |
| SUS and recommendation-likelihood item-level data | **Author action required** | Fill `data/usability/usability_literacy.csv` |
| Exact Dify workflow definitions | **Verification required** | `workflow/dify/生育力保存-V20260129.yml` is present; confirm that it is the exact sanitized DSL used for the reported study and document the export/version date |
| Retrieval pipeline configuration | Partially documented | `workflow/reference_architecture.yaml`; exact embedding, chunking, top-k, filters, reranking, prompt assembly, and fallback settings still require author confirmation |
| Graph schema and import code | **Author action required** | Add Neo4j schema/constraints and de-identified import scripts under `knowledge_base/` or `scripts/` |
| Frozen knowledge-base provenance | **Author action required** | Complete `knowledge_base/manifest.csv`; do not redistribute copyrighted texts without permission |
| Citation metadata | Included (partial) | `CITATION.cff` contains manuscript-derived title/authors; add final DOI/journal or preprint/release metadata when available |
| Software/data license | **Author decision required** | Add `LICENSE` and any separate data-use terms after rightsholder approval |

## Release rule

Do not change an “Author action required” row to “Included” until the file is the exact artifact used in the reported study, or the manuscript is revised to state that the published file is reconstructed. Likewise, change “Verification required” to “Included” only after the authors have confirmed provenance, sanitization, and version identity.
