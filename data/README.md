# Study data

This directory separates study inputs by analysis domain.

- `clinical_cases/` — de-identified case repository, individualized rubrics, and model responses.
- `mcq/` — the 50-item multiple-choice benchmark and original model response runs. Files currently present are templates until replaced with the approved study-exact records.
- `ratings/` — atomic ratings from automated judges and blinded experts. The current CSV is a template until the original evaluator records are inserted.
- `usability/` — item-level SUS, NPS, and fertility-preservation literacy records. The current CSV is a template until approved de-identified source data are supplied.

Do not commit direct identifiers, raw clinical records, free-text dates, or other fields that could enable re-identification. See `docs/DATA_DICTIONARY.md` and `docs/ARTIFACT_MANIFEST.md` before replacing any template with source data.
