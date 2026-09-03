# Prompt release directory

Add the exact, versioned prompts used in the study here. At minimum publish:

- MCQ system and user prompt templates;
- clinical-case system and user prompt templates for every configuration;
- automated-judge system prompt and scoring prompt;
- structured-output schema and retry/error-handling instructions;
- prompt version, checksum, language, model applicability, and change log.

## Published prompts

| File | Version | Language | Role | SHA-256 |
|---|---|---|---|---|
| `automated_judge_prompt.md` | 1.0.0 | English | Automated-judge system prompt: item-by-item binary (safety red-line) and graded (efficacy) scoring of model responses | `33d275ca0babe79844867ab75f6ee2821cac0e2ca69e97bda47a3e205999310c` |
| `Supplementary_Appendix_5.docx` | 1.0.0 | English | Source document (manuscript Supplementary Appendix 5) containing the prompt verbatim | `d4b4b2c6671ce5d24ae19341f1f2b73067f58665e5bd9403ff4cd5d66f871f34` |

Model applicability: the judge prompt scores responses from every evaluated
model (YuHub, DeepSeek, Qwen, and other compared models) on the 20
de-identified clinical cases in `cases_rubric_modelResponse.json`.

### Change log

- 2026-09-03 — v1.0.0: published the automated-judge system prompt (English),
  extracted verbatim from manuscript Supplementary Appendix 5.

## Still pending

The remaining study prompts (MCQ and clinical-case system/user templates for
every configuration, structured-output schema, and retry/error-handling
instructions) are not yet published. Creating plausible replacements would
misrepresent the methods, so these rows stay open until the exact artifacts
are supplied.
