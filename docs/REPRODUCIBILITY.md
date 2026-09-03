# Reproducibility guide

## Environment

Use Python 3.11 and install the pinned major-version ranges in `pyproject.toml`.
For an archival release, generate and publish an exact lock file from the clean
environment used to rerun the analyses.

## Case evaluation

1. Validate `cases_rubric_modelResponse.json`.
2. Generate `templates/case_ratings.csv` from the JSON.
3. Insert the original atomic evaluator scores. Do not infer ratings from the
   prose results or regenerate them with a different judge model.
4. Run `analyze-cases`. The analysis computes normalized weighted binary,
   graded, and harmonized overall scores for every evaluator; evaluator-group
   consensus; Friedman tests; paired Wilcoxon comparisons with Holm adjustment;
   average-measures absolute-agreement and consistency ICCs; automated-versus-
   expert bias, MAE, and the proportion within 0.10; and case-clustered bootstrap
   confidence intervals.

## MCQ evaluation

Use the exact item wording, answer key, response, run number, and provider model
identifier. The analyzer reports per-run and aggregate accuracy, a Friedman test,
paired sign-flip permutation comparisons, Holm-adjusted p values, paired
bootstrap confidence intervals, and across-run answer stability.

## Usability and literacy

Provide item-level long-form records. The analyzer applies standard SUS scoring,
computes NPS from 0–10 recommendation ratings, and performs a paired t test on
participant-level pre/post literacy totals.

## Randomness and audit trail

All stochastic procedures accept `--seed`. The JSON output records the seed,
bootstrap count, input SHA-256, Python version, and package versions. Preserve
the raw immutable source files and publish generated outputs in a separate
versioned release directory.

## Known non-reconstructable inputs

The current public JSON does not contain the MCQ benchmark, the evaluator-level
ratings, usability/literacy records, exact prompts, model run metadata, the Dify
DSL export, or the frozen retrieval/knowledge-graph configuration. Manuscript
summary statistics cannot be used to recreate those raw inputs.
