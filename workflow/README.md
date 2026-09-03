# Workflow release directory

`reference_architecture.yaml` is a non-executable map reconstructed from the
manuscript. It is useful for review, but it is not the study's Dify definition.

Before public release, export the exact Dify workflow DSL into `workflow/dify/`
and sanitize it. Remove secrets and internal addresses while preserving node
IDs, node types, prompts, model identifiers, variables, branching logic,
retrieval settings, error paths, and version metadata. Validate the sanitized
export in a clean Dify deployment before publishing it.
