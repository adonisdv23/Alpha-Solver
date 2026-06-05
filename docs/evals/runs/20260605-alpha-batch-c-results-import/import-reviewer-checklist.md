# Import Reviewer Checklist

Lane ID: `ALPHA-BATCH-C-RESULTS-IMPORT-001`

- [x] Required source evidence file exists in the repository.
- [x] Source artifact was used instead of memory, summaries, planning notes, score tables, uploaded files, or prior prompts.
- [x] `BC-001` through `BC-012` task IDs are preserved.
- [x] `BC-001` through `BC-012` prompts are present.
- [x] `BC-001` through `BC-012` raw outputs are present.
- [x] Scorer-facing sanitized entries are present for `BC-001` through `BC-012`.
- [x] Source cleanup/provenance notes are recorded as provenance only and are not scored.
- [x] Export wrapper material removed before PR #317 is not scored.
- [x] No raw output is edited, improved, rewritten, normalized, reconstructed, or inferred.
- [x] No private URL, exporter link, provider key, secret, credential, or sensitive wrapper material is introduced.
