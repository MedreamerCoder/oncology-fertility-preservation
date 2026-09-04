# Reproducibility guide

## Environment

Use Python 3.11 and install the pinned major-version ranges in `pyproject.toml`. For an archival release, generate and publish an exact lock file from the clean environment used to rerun the analyses.

## Case evaluation

1. Validate `data/clinical_cases/cases_rubric_modelResponse.json`.
2. Generate or refresh `data/ratings/case_ratings.csv` from the case JSON.
3. Insert the original atomic evaluator scores. Do not infer ratings from the prose results or regenerate them with a different judge model.
4. Run `analyze-cases` with the case JSON supplied through `--cases`. The analysis computes normalized weighted binary, graded, and harmonized overall scores for every evaluator; evaluator-group consensus; Friedman tests; paired Wilcoxon comparisons with Holm adjustment; average-measures absolute-agreement and consistency ICCs; automated-versus-expert bias, MAE, and the proportion within 0.10; and case-clustered bootstrap confidence intervals.

Example:

```bash
python -m yuhub_repro analyze-cases \
  data/ratings/case_ratings.csv results/cases \
  --cases data/clinical_cases/cases_rubric_modelResponse.json
```

## MCQ evaluation

Use the exact item wording, answer key, response, run number, and provider model identifier. Store the approved benchmark in `data/mcq/mcq_items.csv` and the original response logs in `data/mcq/mcq_responses.csv`. The analyzer reports per-run and aggregate accuracy, a Friedman test, paired sign-flip permutation comparisons, Holm-adjusted p values, paired bootstrap confidence intervals, and across-run answer stability.

## Usability and literacy

Provide item-level long-form records in `data/usability/usability_literacy.csv`. The analyzer applies standard SUS scoring, computes NPS from 0–10 recommendation ratings, and performs a paired t test on participant-level pre/post literacy totals.

## Randomness and audit trail

All stochastic procedures accept `--seed`. The JSON output records the seed, bootstrap count, input SHA-256, Python version, and package versions. Preserve raw immutable source files under `data/` and publish generated outputs separately. The `results/` directory is reserved for generated analysis outputs and is ignored by Git except for its documentation file.

## Workflow and retrieval provenance

A Dify YAML export is currently present at `workflow/dify/生育力保存-V20260129.yml`, but its provenance and sanitization still require author verification before it can be described as the exact study workflow. `workflow/reference_architecture.yaml` is a manuscript-derived reference map and is not a substitute for study-exact retrieval settings.

## Known non-reconstructable or unverified inputs

The current public repository does not yet contain the approved 50-item MCQ benchmark, original evaluator-level ratings, original usability/literacy records, all benchmark prompts, complete model-run metadata, the fully documented retrieval configuration, Neo4j schema/import scripts, or the complete frozen knowledge-base provenance manifest. The Dify workflow candidate is present but remains unverified. Manuscript summary statistics cannot be used to recreate missing raw inputs.
