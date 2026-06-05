# Redaction and Anomaly Log

## Source evidence

`docs/evals/runs/20260605-alpha-local-llm-runtime-smoke-execution-retry/source-evidence/ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-RETRY-002.md`

## Redaction status

No private URLs, provider key values, secrets, or credentials were imported. The source artifact records that provider keys were unset before execution and records the endpoint only as localhost / loopback.

## Anomalies and caveats preserved

- Attempt 001 failed before runtime due missing repo-root `PYTHONPATH`; this is a runner/import-path failure, not a local LLM runtime failure.
- Source repo status sections listed an untracked prior smoke artifact at repo root.
- Source repo status sections listed untracked manual-artifact folders from prior local attempts.

## Narrow interpretation of caveats

The untracked artifact entries are local artifact hygiene caveats. They are preserved and not hidden. They are not treated as invalidating the successful attempt 002 retry smoke result because the source artifact preserves complete attempt 002 command/script provenance, precheck success, smoke execution, and smoke exit code `0`.

## Exclusions

Terminal wrapper noise is not imported as smoke evidence. No output was reconstructed.
