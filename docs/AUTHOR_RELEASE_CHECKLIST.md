# Author release checklist

Use this checklist before creating the archival release/tag associated with the manuscript.

- [ ] Confirm all 20 case records have passed a second privacy review.
- [ ] Add the exact 50-item MCQ benchmark, answer key, and versioned sources.
- [ ] Add all 750 MCQ response rows (50 items × 5 configurations × 3 runs), or document any deviation from this expected structure.
- [ ] Add all original atomic automated-judge and expert scores.
- [ ] Add the remaining exact system/user prompts used for MCQ and clinical-case benchmark generation.
- [ ] Add immutable model identifiers, providers, access dates, generation parameters, and run IDs; reconcile manuscript model names with provider records.
- [ ] Verify `workflow/dify/生育力保存-V20260129.yml` is the exact sanitized Dify workflow used for the reported experiments; record its checksum/export date and validate it in a clean Dify deployment.
- [ ] Confirm the Dify export contains no credentials, internal-only URLs, user identifiers, database connection strings, or other sensitive deployment information.
- [ ] Add/verify retrieval configuration: embedding model/version, chunking, index settings, top-k, filters, gte-rerank version, prompt assembly, and fallback behavior.
- [ ] Add Neo4j constraints/schema and de-identified graph import code.
- [ ] Publish a knowledge-base provenance manifest with title, organization, version/date, URL/DOI, language, checksum, acquisition date, inclusion reason, and redistribution status for all 315 documents and six books.
- [ ] Add raw item-level SUS, NPS, and literacy data after privacy review.
- [ ] Run all tests and all analyses in a clean Python 3.11 environment.
- [ ] Compare generated tables/statistics with the manuscript and resolve every discrepancy.
- [ ] Choose and add software and data licenses approved by all rightsholders.
- [ ] Add `CITATION.cff`, manuscript DOI/preprint URL, contact details, release tag, and an archived DOI (for example, Zenodo) after approval.
- [ ] Have a clinician confirm the safety disclaimer and intended-use statement.
- [ ] Revise the manuscript availability statements if any promised artifact cannot be released exactly as described.
