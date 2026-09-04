# Reproducibility scripts

The current analysis entry points are implemented as the `yuhub_repro` Python package under `src/` and exposed through the `yuhub-repro` / `oncofert-llm-repro` command-line interfaces.

Use this directory for study-exact one-off scripts that are needed for reproducibility but do not belong in the reusable package, such as de-identified data-conversion utilities, graph import scripts, release validation scripts, or manuscript table/figure regeneration wrappers.

Do not add production credentials, private endpoints, or scripts that depend on unavailable internal infrastructure without documenting those dependencies.
