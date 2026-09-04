# Prompt release directory

This directory contains versioned prompts that were actually used in the study and are approved for public release. Do not add reconstructed or approximate prompts and label them as original study artifacts.

## Published prompts

| File | Version | Language | Role | SHA-256 |
|---|---|---|---|---|
| `automated_judge_prompt.md` | 1.0.0 | English | Automated-judge system prompt for item-by-item binary safety scoring and graded effectiveness scoring of model responses | `33d275ca0babe79844867ab75f6ee2821cac0e2ca69e97bda47a3e205999310c` |

The source DOCX used during manuscript preparation was intentionally removed from the repository after the Markdown prompt was published. The Markdown file above is therefore the public prompt artifact currently retained in version control.

Model applicability: the judge prompt scores responses from OncoFert-LLM, DeepSeek, Qwen, and the other evaluated configurations on the de-identified clinical cases in `data/clinical_cases/cases_rubric_modelResponse.json`.

## Still pending

The repository still needs the exact, versioned study prompts for:

- MCQ system and user templates;
- clinical-case system and user templates for each evaluated configuration;
- structured-output schemas used during benchmark generation;
- retry and error-handling instructions where applicable;
- prompt version, checksum, language, model applicability, and change log for each released prompt.

If any exact prompt cannot be released, document that limitation explicitly in `docs/ARTIFACT_MANIFEST.md` and reconcile the manuscript availability statement.

## Change log

- 2026-09-03 — v1.0.0: published `automated_judge_prompt.md` from Supplementary Appendix 5.
- 2026-09-03 — removed the source DOCX after the prompt was preserved in Markdown.
