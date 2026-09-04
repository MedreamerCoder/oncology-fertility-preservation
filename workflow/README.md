# Workflow release directory

This directory separates the study-facing workflow artifact from the simplified reference architecture used for review and documentation.

## Files

- `reference_architecture.yaml` — non-executable architecture map reconstructed from the manuscript.
- `dify/生育力保存-V20260129.yml` — Dify DSL export currently present in the repository.

## Verification required before final release

The Dify export should be treated as a candidate study artifact until the authors confirm that it is the exact workflow version used for the reported experiments and that sanitization did not alter the scientific logic.

Before marking it as fully released:

1. confirm the workflow/export date and study run period;
2. confirm node IDs, node types, prompts, model identifiers, variables, branching logic, retrieval settings, error paths, and version metadata against the study system;
3. remove credentials, internal-only endpoints, database connection strings, user identifiers, and other sensitive deployment details;
4. validate the sanitized DSL in a clean Dify deployment;
5. record the verified status in `docs/ARTIFACT_MANIFEST.md` and, ideally, add a checksum/version note here.

Do not replace the exact workflow with a reconstructed approximation while describing it as the original study artifact.
