# Artifact contract summary

Deterministic artifact names:

- `dry-run-result.json`
- `execution-gate-result.json`
- `stop-state.json` when blocked

JSON shape summaries:

- `dry-run-result.json` stores the `DryRunResult` schema with wrapper status, summaries, artifact paths, output-root summary, evidence boundary, redaction status, non-execution confirmation, and metadata.
- `execution-gate-result.json` stores the corrected execution gate result and remains the source-of-truth gate artifact.
- `stop-state.json` stores the blocked stop-state record when the gate does not allow local dry-run readiness.

Output-root rules:

- The caller must provide `output_root`.
- All artifact writes go through existing artifact-store path resolution.
- Path traversal and writes outside `output_root` are rejected.
- Artifact paths recorded by the wrapper are relative artifact paths, not raw absolute output-root paths.

No-overwrite behavior:

- Overwrites are rejected by default.
- Callers must explicitly opt in with `overwrite=True` for replacement.

Redaction behavior:

- Artifacts are serialized through existing redaction helpers.
- Secret-like keys and marker strings are redacted in persisted JSON.
