# Data dictionary

## `data/clinical_cases/cases_rubric_modelResponse.json`

The top-level object contains `merged_cases`, a list of 20 cases.

| Field | Type | Meaning |
|---|---|---|
| `case_ID` | string | Stable pseudonymous case identifier |
| `complexity` | string | Author-assigned case complexity label |
| `disease` | string | De-identified disease description |
| `case_detail` | string | De-identified clinical context supplied to a model |
| `patient_question` | string | Simulated patient query |
| `scoring_rubric.binary_checks` | array | Binary atomic criteria scored 0 or 1 |
| `scoring_rubric.graded_rules` | array | Graded atomic criteria scored 0, 0.6, 0.8, or 1 |
| `answers` | object | Model-name to complete response text |

Each rubric item has a category identifier, a clinical criterion, a type (`safety` or `effectiveness`), a harm-based weight from 1 to 5, and criterion-specific score descriptors. Category identifiers are not guaranteed to be unique within a case; `OF-2025-010`, for example, contains two distinct atomic items mapped to `E-12`. The public file contains responses but does not contain evaluator scores.

## `data/ratings/case_ratings.csv`

One row is one evaluator's score for one atomic criterion of one case-model response. Required columns are:

`case_id`, `answer_model`, `evaluator_group`, `evaluator_id`, `criterion_kind`, `criterion_id`, `criterion_instance`, `criterion_type`, `weight`, `score`, `notes`.

- `evaluator_group`: `automated` or `expert`.
- `evaluator_id`: stable pseudonym such as `auto_01` or `expert_01`.
- `criterion_kind`: `binary` or `graded`.
- `criterion_id`: the manuscript framework category (not necessarily unique within a case).
- `criterion_instance`: stable per-case atomic-item key generated from kind, position, and category, for example `G02:E-12`.
- `score`: `0` or `1` for binary items; `0`, `0.6`, `0.8`, or `1` for graded items.
- `notes`: optional, scrubbed of identifiers.

## `data/mcq/mcq_items.csv`

One row per question: `question_id`, `stem`, `option_a` through `option_e`, `correct_option`, `source`, and `source_version`.

## `data/mcq/mcq_responses.csv`

One row per question-model-run: `question_id`, `model`, `run`, `selected_option`, `correct_option`, `is_correct`, `provider_model_id`, `temperature`, `seed`, and `run_timestamp_utc`.

## `data/usability/usability_literacy.csv`

Long-form records with `participant_id`, `participant_group`, `instrument`, `timepoint`, `item_id`, and `score`. Use `instrument` values `SUS`, `NPS`, or `FP_LITERACY`. Do not publish direct identifiers or free text.

## `metadata/model_runs.csv`

One row should correspond to one immutable model/run configuration. Record provider, exact model identifier, configuration label, access/run date, generation parameters, prompt version/checksum, and any provider run identifier available for audit.

## `knowledge_base/manifest.csv`

One row should correspond to one knowledge-base source document or book. The public manifest should contain provenance metadata only (for example title, issuing organization, version/date, URL/DOI, language, checksum, acquisition date, inclusion reason, and redistribution status) unless redistribution of the source text is explicitly permitted.
