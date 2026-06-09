# Importer summary

Public API:

- `AcceptanceArtifactRecord`
- `AcceptanceTaskImportRecord`
- `AcceptanceImportSummary`
- `import_acceptance_execution_packet(packet_dir: Path, output_dir: Path) -> AcceptanceImportSummary`
- `write_acceptance_import_summary(summary: AcceptanceImportSummary, output_path: Path) -> Path`

Importer behavior:

- Reads local packet files only.
- Discovers MLA-001 through MLA-010.
- Normalizes artifact records by task and artifact name.
- Parses JSON artifacts when present.
- Calculates SHA-256 checksums and compares ledger checksums when available.
- Validates task IDs, lane IDs, run IDs, schema versions, redaction status, evidence-boundary markers, and non-execution confirmation.
- Detects missing artifacts, malformed JSON, path traversal/out-of-packet artifacts, checksum mismatches, source-artifact mutation markers, redaction failures, evidence-boundary failures, and missing non-execution proof.
- Produces deterministic JSON with `sort_keys=True` and stable record ordering.
- Does not interpret pass/fail results as readiness and does not claim MVP readiness.
