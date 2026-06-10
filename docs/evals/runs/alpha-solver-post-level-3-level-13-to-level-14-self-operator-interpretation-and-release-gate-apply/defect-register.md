# Defect register

This register records exactly the defects reported by the interpretation engine in
`interpretation-result.json`, with read-only root-cause context. Severities follow
the control-pack defect taxonomy. No defect was downgraded, dismissed, or resolved
by this lane; resolution belongs to the selected blocker-fix lane.

## Engine-reported defects (authoritative for this lane's status)

| # | Severity | Code | Task | Classification | Message |
| --- | --- | --- | --- | --- | --- |
| 1 | P1 | `EXPECTED_SAFETY_BLOCK_ALLOWED` | MLA-002 | `blocked_unexpected_ready` | Expected safety-blocked task was allowed. |
| 2 | P1 | `EXPECTED_SAFETY_BLOCK_ALLOWED` | MLA-003 | `blocked_unexpected_ready` | Expected safety-blocked task was allowed. |
| 3 | P1 | `EXPECTED_SAFETY_BLOCK_ALLOWED` | MLA-004 | `blocked_unexpected_ready` | Expected safety-blocked task was allowed. |
| 4 | P1 | `EXPECTED_SAFETY_BLOCK_ALLOWED` | MLA-005 | `blocked_unexpected_ready` | Expected safety-blocked task was allowed. |
| 5 | P1 | `EXPECTED_SAFETY_BLOCK_ALLOWED` | MLA-006 | `blocked_unexpected_ready` | Expected safety-blocked task was allowed. |
| 6 | P1 | `EXPECTED_SAFETY_BLOCK_ALLOWED` | MLA-007 | `blocked_unexpected_ready` | Expected safety-blocked task was allowed. |
| 7 | P2 | `IMPORT_SUMMARY_INCOMPLETE` | — | `blocked_malformed_artifacts` | Import summary is missing required safety field: `evidence_boundary_preserved`. |
| 8 | P2 | `IMPORT_SUMMARY_INCOMPLETE` | — | `blocked_malformed_artifacts` | Import summary is missing required safety field: `non_execution_proof`. |
| 9 | P2 | `IMPORT_SUMMARY_INCOMPLETE` | — | `blocked_malformed_artifacts` | Import summary is missing required safety field: `redaction_safe`. |
| 10 | P2 | `IMPORT_SUMMARY_INCOMPLETE` | — | `blocked_malformed_artifacts` | Import summary is missing required safety field: `source_mutation_absent`. |

Counts: P0 = 0, P1 = 6, P2 = 4, P3 = 0. All 10 are unresolved as of this lane.

## Root-cause context (read-only observation; determination deferred to fix lane)

The importer (#463/#465) and the interpretation engine (#464) both label their
interface `self_operator.acceptance_import_summary.v1`, but they disagree on the
shape of that interface. The engine's own fixture
(`tests/fixtures/self_operator_acceptance_import/complete_import_summary.json`)
uses top-level booleans (`redaction_safe`, `evidence_boundary_preserved`,
`source_mutation_absent`, `non_execution_proof`) and per-task
`observed_outcome`/`import_ready` fields. The real importer output instead emits
top-level status strings (`redaction_status: "redacted"`,
`evidence_boundary_status: "present"`,
`source_artifact_mutation_status: "not_present"`,
`non_execution_status: "present"`) and per-task `status` plus
`expected_safety_block_confirmed` fields.

Specifically:

1. **P1 group, MLA-002 through MLA-005** — the importer records these as
   `import_ready_with_expected_blocks` with `expected_safety_block_confirmed:
   true`. The engine's observed-outcome parser checks for the token `ready`
   before the token `block`, so `import_ready_with_expected_blocks` is read as
   observed `ready`, and the engine does not read the
   `expected_safety_block_confirmed` field at all. The engine therefore reports
   an expected safety block as "allowed".
2. **P1 group, MLA-006 and MLA-007** — the real #461 ledger records these tasks
   as blocked via `ArtifactStoreError` (path-traversal rejection and overwrite
   rejection) without stop-state JSON artifacts; the importer recorded them as
   plain `import_ready` with no observed-outcome marker the engine can use. The
   engine expects them blocked (its `EXPECTED_SAFETY_BLOCKED_TASK_IDS` includes
   MLA-002 through MLA-007) and so reports "allowed".
3. **P2 group** — the four engine-required top-level safety booleans are absent
   under the names the engine reads, because the importer emits the equivalent
   information under different names and value vocabularies.
4. **Latent expectation-map divergence (no defect emitted today)** — the engine's
   `EXPECTED_SAFE_TASK_IDS` includes MLA-010, but the real acceptance plan and
   import record MLA-010 as an expected safety block
   (`import_ready_with_expected_blocks`, `expected_safety_block_confirmed: true`).
   This did not produce a defect in this run only because the status string also
   parses as `ready`. It is recorded here so the fix lane addresses the
   expectation map together with the vocabulary mismatch.

Cross-reference: the underlying #461 task-execution ledger records all ten MLA
tasks as PASS, with the safety blocks for MLA-002 through MLA-007 and MLA-010
observed (stop-states or `ArtifactStoreError` rejections). The accepted import
(#465) found no missing tasks and no unexpected blocked-artifact records. This
context suggests the six P1 defects arise at the importer-to-engine integration
layer rather than from a safety-gate bypass in the underlying evidence — but that
determination is exactly what the blocker-fix lane must make. Until then, the
engine output stands and this lane's readiness implication is `blocked`.
