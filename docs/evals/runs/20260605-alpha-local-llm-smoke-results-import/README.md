# Local LLM Smoke Results Import

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-001`

This folder imports the pasted `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md` evidence as a repo-safe, sanitized local smoke result package.

## Imported source evidence

- Source evidence file: `source-evidence/sanitized-smoke-execution-artifact.md`
- Evidence source: pasted evidence block supplied to Codex for this docs-only lane.
- Import status: completed as executed because the source evidence records `executed: true`.

## Required companion files

- `smoke-result-log.md` records the imported command fields and preserved result fields.
- `smoke-redaction-log.md` records sanitization and absence checks.
- `import-reviewer-checklist.md` records reviewer checks for this import.

## Evidence boundary

This import preserves local smoke evidence only. It does not expand the evidence boundary beyond the pasted execution artifact.

## Import caveat

The pasted artifact does not separately preserve the literal terminal command text or a numeric process exit code. Those fields are not marked complete, no numeric exit code is imported, and neither field is reconstructed. The import proceeds only because the artifact records `executed: true`, `exception: null`, completed timestamps, stdout-equivalent content, a sanitized request artifact, and a raw response artifact.
