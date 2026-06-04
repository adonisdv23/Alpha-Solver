# Results Import Hard Blockers

Lane ID: `ALPHA-LIMITED-OPERATOR-TEST-RESULTS-IMPORT-REVIEW-GATE-001`

If any blocker applies to the future `ALPHA-LIMITED-OPERATOR-TEST-RESULTS-IMPORT-001` PR, do not approve the PR until the blocker is removed.

## Hard blockers

- **No actual operator evidence:** The PR imports rows, ratings, notes, snippets, or defects without actual evidence provided by Adonis or an approved substitute operator.
- **Fabricated rows:** The PR creates task rows from the template, task list, memory, expectations, or planning status rather than from tasks actually run.
- **Inferred ratings:** Missing ratings are inferred, averaged, normalized, backfilled, translated, or converted to another scale.
- **Imported tasks not actually run:** The PR includes rows for skipped, planned, unexecuted, or unevidenced tasks.
- **Missing stop-condition status:** Any imported task row lacks a recorded stop-condition status.
- **Unsupported validation/readiness/superiority claims:** The PR claims benchmark success, validation, MVP readiness, production readiness, runtime readiness, Alpha superiority, broad generalization, exact billing accuracy, self-healing, adaptive learning, self-optimization, autonomous optimization, or provider orchestration.
- **Raw-output/operator-map boundary violation:** The PR inspects, imports, quotes, summarizes, or depends on raw outputs, operator-only maps, sanitized scorer-facing packets, full unredacted traces, private data, secrets, or raw provider payloads.
- **Runtime/provider/model/routing changes:** The PR changes runtime APIs, provider adapters, model configuration, routing, capture scripts, or other protected runtime surfaces.
- **`/v1/solve` use:** The PR uses, measures, modifies, or claims behavior for `/v1/solve`.
- **Batch C start:** The PR starts Batch C, modifies Batch C materials, or frames the import as authorization to start Batch C.
- **Google Sheets treated as proof:** Spreadsheet status is used as the evidence source instead of actual operator-provided feedback.
