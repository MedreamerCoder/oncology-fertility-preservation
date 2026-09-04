# OncoFert-LLM

Public study artifacts and reproducibility utilities for the manuscript:

> **A specialty clinical generative AI framework with harm-aware benchmarking for oncofertility decision support**

OncoFert-LLM is a clinician-supervised research decision-support system for oncofertility. The repository is intended for transparent reporting, independent audit, and reproducibility work. It is **not** medical advice and must not be used for autonomous diagnosis, treatment selection, or treatment delay.

## Repository scope

The study describes a workflow-orchestrated, knowledge-graph-enhanced retrieval-augmented generation framework that combines intent recognition, clinical-variable extraction, missing-information detection, multi-path retrieval, jurisdiction-specific regulatory retrieval, and patient-value clarification. The public repository focuses on the study artifacts and evaluation pipeline rather than production deployment code.

## What is included

- `cases_rubric_modelResponse.json` — 20 de-identified clinical cases, individualized consequence-weighted scoring rubrics, and model responses.
- `prompts/automated_judge_prompt.md` — released automated-judge prompt used for case scoring.
- `workflow/reference_architecture.yaml` — manuscript-derived reference architecture.
- `workflow/dify/生育力保存-V20260129.yml` — Dify DSL export currently present in the repository; authors should verify that it is the exact sanitized workflow version used for the reported study before marking the workflow artifact as fully released.
- `src/yuhub_repro/` — reproducibility utilities for validation, weighted scoring, case-level analyses, MCQ analyses, usability summaries, ICCs, and clustered bootstrap confidence intervals.
- `templates/` — machine-readable templates for ratings, MCQ runs, and usability/literacy records.
- `metadata/` — templates/manifests for model-run and knowledge-base provenance metadata.
- `docs/` — artifact manifest, data dictionary, reproducibility notes, and release checklist.
- `tests/` and `.github/workflows/tests.yml` — basic automated tests and CI.

## Quick start

Python 3.11 is recommended.

```bash
python -m venv .venv
python -m pip install -e .
python -m yuhub_repro validate cases_rubric_modelResponse.json
python -m yuhub_repro summarize cases_rubric_modelResponse.json
```

Create analysis-ready templates:

```bash
python -m yuhub_repro make-ratings-template \
  cases_rubric_modelResponse.json templates/case_ratings.csv
python -m yuhub_repro make-mcq-template templates/mcq_responses.csv
```

After filling the templates with the original evaluator records:

```bash
python -m yuhub_repro analyze-cases templates/case_ratings.csv results/cases
python -m yuhub_repro analyze-mcq templates/mcq_responses.csv results/mcq
python -m yuhub_repro analyze-usability templates/usability_literacy.csv results/usability
```

Each analysis writes tidy CSV outputs plus a JSON summary containing the random seed, bootstrap count, input hash, software versions, and statistical results.

## Recommended repository layout

```text
.
├── README.md
├── SECURITY.md
├── cases_rubric_modelResponse.json
├── docs/
│   ├── ARTIFACT_MANIFEST.md
│   ├── AUTHOR_RELEASE_CHECKLIST.md
│   ├── DATA_DICTIONARY.md
│   └── REPRODUCIBILITY.md
├── metadata/
├── prompts/
├── src/
│   └── yuhub_repro/
├── templates/
├── tests/
└── workflow/
    ├── reference_architecture.yaml
    └── dify/
        └── 生育力保存-V20260129.yml
```

The Python module retains the legacy internal name `yuhub_repro` for compatibility with the existing analysis code. The study-facing project name is **OncoFert-LLM**.

## Reproducibility status

The manuscript states that study prompts, the 50-item MCQ benchmark, the 20 clinical cases with individualized rubrics, complete model outputs, workflow definitions, retrieval pipeline, and evaluation scripts are available in this repository. The current release already contains several of these artifacts, while some study-exact inputs remain incomplete or require author verification. See [`docs/ARTIFACT_MANIFEST.md`](docs/ARTIFACT_MANIFEST.md) for the current status.

Do not replace missing study artifacts with reconstructed or plausible substitutes and label them as original. If an exact artifact cannot be released, the repository and manuscript availability statement should say so explicitly.

## Privacy and safety

- Never commit API keys, database credentials, private endpoints, raw clinical records, direct identifiers, free-text dates, or image metadata that could re-identify a patient.
- Keep evaluator identities pseudonymous in public files.
- Record exact model identifiers, providers, access dates, generation parameters, and prompts for every released benchmark run.
- Do not redistribute the 315-document knowledge corpus or six textbooks unless redistribution is licensed. Publish provenance metadata and acquisition instructions instead.
- Keep all recommendations framed as clinician-supervised decision support.

## Citation and license

Citation metadata, software licensing, and data-use terms should be approved by the study authors before final public release. Add `CITATION.cff`, the manuscript DOI/preprint link, and the approved license when available.
