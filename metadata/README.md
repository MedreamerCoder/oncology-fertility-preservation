# Model-run metadata

Replace the empty CSV template in this directory with the exact study records. Do not put credentials, internal endpoints, patient identifiers, or copyrighted full text in metadata files.

- `model_runs.csv` records one immutable row per model/run configuration, including the exact provider model identifier, access/run date, generation parameters, prompt version/checksum, configuration label, and provider run identifier when available.
- Knowledge-base source provenance is maintained separately in `knowledge_base/manifest.csv` so model-run metadata and corpus provenance remain clearly separated.
