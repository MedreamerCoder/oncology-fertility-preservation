# Public artifact manifest

This manifest maps statements in the manuscript to the files needed for an
independent audit. “Included” means present in this repository bundle. “Author
action required” means the material cannot be reconstructed faithfully from the
manuscript or the existing public JSON.

| Manuscript commitment | Status | Public artifact |
|---|---|---|
| 20 de-identified clinical cases | Included | `cases_rubric_modelResponse.json` |
| Individualized scoring rubrics | Included | `cases_rubric_modelResponse.json` |
| YuHub, DeepSeek, and Qwen case answers | Included | `cases_rubric_modelResponse.json` |
| Validation and weighted-scoring code | Included (reconstructed) | `src/yuhub_repro/` |
| Case comparison, ICC, bias, and bootstrap code | Included (reconstructed) | `src/yuhub_repro/case_analysis.py` |
| MCQ analysis code | Included (reconstructed) | `src/yuhub_repro/mcq_analysis.py` |
| Usability/literacy analysis code | Included (reconstructed) | `src/yuhub_repro/usability.py` |
| 50-item MCQ benchmark and answer key | **Author action required** | Replace `templates/mcq_items.csv` with the approved de-identified source file |
| All three runs for five MCQ configurations | **Author action required** | Fill `templates/mcq_responses.csv` from original run logs |
| Atomic scores from three automated judges | **Author action required** | Fill `templates/case_ratings.csv` |
| Atomic scores from three blinded experts | **Author action required** | Fill `templates/case_ratings.csv` using pseudonymous evaluator IDs |
| Exact automated-review prompts | **Author action required** | Add versioned files under `prompts/` |
| Exact study prompts for every benchmark | **Author action required** | Add versioned files under `prompts/` |
| Model/version/parameter/run metadata | **Author action required** | Add `metadata/model_runs.csv` and provider documentation |
| Pre/post literacy item-level data | **Author action required** | Fill `templates/usability_literacy.csv` |
| SUS and recommendation-likelihood item-level data | **Author action required** | Fill `templates/usability_literacy.csv` |
| Exact Dify workflow definitions | **Author action required** | Export sanitized DSL to `workflow/dify/` |
| Retrieval pipeline configuration | Partially documented | `workflow/reference_architecture.yaml`; exact configuration still required |
| Graph schema and import code | **Author action required** | Add schema/constraints and de-identified import scripts |
| Frozen knowledge-base provenance | **Author action required** | Add document-level manifest; do not redistribute copyrighted texts without permission |
| License and citation metadata | **Author decision required** | Add `LICENSE`, `CITATION.cff`, and data-use terms |

## Release rule

Do not change an “Author action required” row to “Included” until the file is the
exact artifact used in the reported study (or the manuscript is revised to state
that it is a reconstructed example). A plausible substitute is not reproducible
evidence.
