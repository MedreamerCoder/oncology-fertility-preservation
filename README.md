# YuHub oncofertility decision-support study

This repository contains the public study artifacts and reproducibility tools for
the manuscript **“Development and validation of a retrieval-augmented generative
artificial intelligence system for oncofertility decision support.”**

YuHub is a clinician-supervised research system. Nothing in this repository is
medical advice, and the material must not be used for autonomous diagnosis,
treatment selection, or treatment delay.

## What is currently included

- `cases_rubric_modelResponse.json`: 20 de-identified clinical cases, their
  individualized consequence-weighted rubrics, and responses from YuHub,
  DeepSeek, and Qwen.
- `src/yuhub_repro/`: data validation, weighted scoring, case-level statistics,
  MCQ analysis, usability summaries, ICCs, and clustered bootstrap confidence
  intervals.
- `workflow/reference_architecture.yaml`: a manuscript-derived, non-executable
  architecture map that distinguishes documented behavior from unreleased
  implementation details.
- `templates/`: machine-readable input templates for ratings, MCQ runs, and
  usability/literacy records.
- `docs/`: artifact manifest, data dictionary, reproducibility guide, and the
  author release checklist.

## Important provenance note

The evaluation utilities in this repository were reconstructed from the
statistical methods reported in the manuscript. The reference workflow and
retrieval modules document the disclosed architecture; they are **not** a
substitute for the exact sanitized Dify export, retrieval configuration, prompt
set, model-version log, or frozen knowledge-base manifest used in the study.
Those source artifacts must be supplied by the study authors before the
repository can substantiate every statement in the manuscript's Data and Code
Availability sections. See [`docs/ARTIFACT_MANIFEST.md`](docs/ARTIFACT_MANIFEST.md).

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

Each analysis writes tidy CSV outputs plus a JSON summary containing the random
seed, bootstrap count, input hash, software versions, and statistical results.

## Expected public-release layout

```text
.
|-- cases_rubric_modelResponse.json
|-- docs/
|-- prompts/                  # exact prompts still required from authors
|-- src/yuhub_repro/
|-- templates/
|-- tests/
`-- workflow/
    |-- reference_architecture.yaml
    `-- dify/                 # exact sanitized Dify DSL export still required
```

## Reproducibility and privacy

- Never commit API keys, database credentials, private endpoints, raw clinical
  records, direct identifiers, free-text dates, or image metadata.
- Keep evaluator identities pseudonymous in public files.
- Record the exact foundation-model identifiers, provider, access date,
  temperature, seed (when supported), and system prompt for every run.
- Do not publish the 315-document corpus or six books unless redistribution is
  licensed. Publish a provenance manifest and acquisition instructions instead.

## Citation and license

Citation metadata and a software/data license must be approved by the authors
before public release. They are intentionally not invented here; see the release
checklist.
