# OncoFert-LLM

Public study artifacts and reproducibility utilities for the manuscript:

> **A specialty clinical generative AI framework with harm-aware benchmarking for oncofertility decision support**

OncoFert-LLM is a clinician-supervised research decision-support system for oncofertility. This repository is intended for transparent reporting, independent audit, and reproducibility work. It is **not** medical advice and must not be used for autonomous diagnosis, treatment selection, or treatment delay.

## Repository scope

The study describes a workflow-orchestrated, knowledge-graph-enhanced retrieval-augmented generation framework that combines intent recognition, clinical-variable extraction, missing-information detection, multi-path retrieval, jurisdiction-specific regulatory retrieval, and patient-value clarification. The public repository focuses on study artifacts, evaluation data, workflow documentation, and reproducibility utilities rather than production deployment code.

## Repository layout

```text
.
├── CITATION.cff
├── README.md
├── SECURITY.md
├── data/
│   ├── clinical_cases/
│   │   └── cases_rubric_modelResponse.json
│   ├── mcq/
│   │   ├── mcq_items.csv
│   │   └── mcq_responses.csv
│   ├── ratings/
│   │   └── case_ratings.csv
│   └── usability/
│       └── usability_literacy.csv
├── docs/
│   ├── ARTIFACT_MANIFEST.md
│   ├── AUTHOR_RELEASE_CHECKLIST.md
│   ├── DATA_DICTIONARY.md
│   └── REPRODUCIBILITY.md
├── knowledge_base/
│   └── manifest.csv
├── metadata/
│   └── model_runs.csv
├── prompts/
├── results/
├── scripts/
├── src/
│   └── repro/
├── tests/
└── workflow/
    ├── reference_architecture.yaml
    └── dify/
        └── 生育力保存-V20260129.yml
```

The Python package used by the reproducibility utilities is `repro`. The study-facing project name is **OncoFert-LLM**.

## What is included

- `data/clinical_cases/cases_rubric_modelResponse.json` — 20 de-identified clinical cases, individualized consequence-weighted scoring rubrics, and model responses.
- `prompts/automated_judge_prompt.md` — released automated-judge prompt used for case scoring.
- `workflow/reference_architecture.yaml` — manuscript-derived reference architecture.
- `workflow/dify/生育力保存-V20260129.yml` — Dify DSL export currently present in the repository; authors should verify that it is the exact sanitized workflow version used for the reported study before marking the workflow artifact as fully released.
- `src/repro/` — reproducibility utilities for validation, weighted scoring, case-level analyses, MCQ analyses, usability summaries, ICCs, and clustered bootstrap confidence intervals.
- `data/mcq/`, `data/ratings/`, and `data/usability/` — structured locations for study-exact benchmark and evaluator records; current CSV files are templates until replaced with approved source data.
- `knowledge_base/manifest.csv` — provenance-manifest template for the frozen knowledge base; source documents themselves should not be redistributed unless licensed.
- `metadata/model_runs.csv` — model/provider/run metadata template.
- `CITATION.cff` — citation metadata derived from the current manuscript title and author list; add the final DOI/publication metadata when available.
- `docs/` — artifact manifest, data dictionary, reproducibility notes, and release checklist.
- `tests/` and `.github/workflows/tests.yml` — automated tests and CI.

## Quick start

Python 3.11 is recommended.

```bash
python -m venv .venv
python -m pip install -e .
python -m repro validate data/clinical_cases/cases_rubric_modelResponse.json
python -m repro summarize data/clinical_cases/cases_rubric_modelResponse.json
```

Create or refresh analysis-ready templates:

```bash
python -m repro make-ratings-template \
  data/clinical_cases/cases_rubric_modelResponse.json data/ratings/case_ratings.csv
python -m repro make-mcq-template data/mcq/mcq_responses.csv
```

After replacing/filling the templates with the original study records:

```bash
python -m repro analyze-cases \
  data/ratings/case_ratings.csv results/cases \
  --cases data/clinical_cases/cases_rubric_modelResponse.json
python -m repro analyze-mcq data/mcq/mcq_responses.csv results/mcq
python -m repro analyze-usability data/usability/usability_literacy.csv results/usability
```

Each analysis writes tidy CSV outputs plus a JSON summary containing the random seed, bootstrap count, input hash, software versions, and statistical results.

## Reproducibility status

The manuscript states that study prompts, the 50-item MCQ benchmark, the 20 clinical cases with individualized rubrics, complete model outputs, workflow definitions, retrieval pipeline, and evaluation scripts are available in this repository. The current release contains several of these artifacts, while some study-exact inputs remain incomplete or require author verification. See [`docs/ARTIFACT_MANIFEST.md`](docs/ARTIFACT_MANIFEST.md) for the current status.

Do not replace missing study artifacts with reconstructed or plausible substitutes and label them as original. If an exact artifact cannot be released, the repository and manuscript availability statement should say so explicitly.

## Privacy and safety

- Never commit API keys, database credentials, private endpoints, raw clinical records, direct identifiers, free-text dates, or image metadata that could re-identify a patient.
- Keep evaluator identities pseudonymous in public files.
- Record exact model identifiers, providers, access dates, generation parameters, and prompts for every released benchmark run.
- Do not redistribute the 315-document knowledge corpus or six textbooks unless redistribution is licensed. Publish provenance metadata and acquisition instructions instead.
- Keep all recommendations framed as clinician-supervised decision support.

## Citation and license

`CITATION.cff` now contains the manuscript-derived title and author list. Update it with the final DOI, journal/preprint information, and archival release metadata once available. The software license and any separate data-use terms still require author/rightsholder approval and are intentionally not invented here.
