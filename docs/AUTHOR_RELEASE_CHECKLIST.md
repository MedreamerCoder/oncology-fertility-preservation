# Author release checklist

- [ ] Confirm all 20 case records have passed a second privacy review.
- [ ] Add the exact 50-item MCQ benchmark, answer key, and versioned sources.
- [ ] Add all 750 MCQ response rows (50 items × 5 configurations × 3 runs), or
      document any deviation from this expected structure.
- [ ] Add all original atomic automated-judge and expert scores.
- [ ] Add the exact system/user prompts and scoring prompt from the study.
- [ ] Add immutable model identifiers, providers, access dates, parameters, and
      run IDs; reconcile model names with provider records.
- [ ] Export the exact Dify workflow as sanitized DSL; remove credentials,
      internal URLs, user identifiers, and database connection strings.
- [ ] Add retrieval configuration: embedding model/version, chunking, index
      settings, top-k, filters, gte-rerank version, prompt assembly, and fallback.
- [ ] Add Neo4j constraints/schema and de-identified graph import code.
- [ ] Publish a knowledge-base provenance manifest with title, organization,
      version/date, URL/DOI, language, checksum, acquisition date, inclusion
      reason, and redistribution status for all 315 documents and six books.
- [ ] Add raw item-level SUS, NPS, and literacy data after privacy review.
- [ ] Run all tests and all analyses in a clean Python 3.11 environment.
- [ ] Compare generated tables to the manuscript and resolve every discrepancy.
- [ ] Choose and add software and data licenses approved by all rightsholders.
- [ ] Add `CITATION.cff`, manuscript DOI/preprint URL, contact details, release
      tag, and an archived DOI (for example, Zenodo) after approval.
- [ ] Have a clinician confirm the safety disclaimer and intended-use statement.
- [ ] Revise the manuscript's availability statements if any promised artifact
      cannot be released.
