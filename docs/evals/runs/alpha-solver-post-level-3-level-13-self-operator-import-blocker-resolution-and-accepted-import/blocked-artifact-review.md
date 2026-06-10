# Blocked artifact review

## Primary blocker: `blocked_source_mutation_concern`

Blocked artifacts (paths relative to the #461 execution packet):

| Artifact | SHA-256 | Ledger checksum | Marker occurrences | Occurrences outside blocked context |
| --- | --- | --- | --- | --- |
| `raw-artifacts/MLA-010/dry-run-result.json` | `ea35751e1e588290458d0f1a5478380eb5c70e612ce827de559bc86f4419cde4` | matched | 4 | 0 |
| `raw-artifacts/MLA-010/execution-gate-result.json` | `472e3bf91342fb02fc507624e0f02680b7681e9ce40a62951a2a88b1768e1d3e` | matched | 6 | 0 |
| `raw-artifacts/MLA-010/stop-state.json` | `e46aa635116743b3937fc956888c01e976c6e008017684311440d97db679b217` | matched | 3 | 0 |

Exact fields and markers causing the block (all 13 occurrences):

- `dry-run-result.json`
  - `$.execution_gate_summary.finding_ids[0]` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`
  - `$.preflight_summary.command_reason_codes[0]` = `source_artifact_mutation`
  - `$.preflight_summary.finding_ids[0]` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`
  - `$.stop_state_summary.finding_ids[0]` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`
- `execution-gate-result.json`
  - `$.findings[0].id` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`
  - `$.findings[0].reason_code` = `source_artifact_mutation`
  - `$.preflight_result_summary.finding_ids[0]` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`
  - `$.stop_state_record.findings[0].id` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`
  - `$.stop_state_record.findings[0].reason_code` = `source_artifact_mutation`
  - `$.stop_state_record.source_preflight_result_summary.finding_ids[0]` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`
- `stop-state.json`
  - `$.findings[0].id` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`
  - `$.findings[0].reason_code` = `source_artifact_mutation`
  - `$.source_preflight_result_summary.finding_ids[0]` = `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`

Context of every occurrence: a finding object whose `stop_state` is `blocked`
(`message`: `forbidden source-artifact mutation`, `severity`: `error`, `surface`:
`command_classification`), or a `finding_ids`/`command_reason_codes` list inside a
summary whose own state is blocked (`stop_state: blocked`, `gate_status:
blocked_by_failed_preflight`, `allowed: false`, or `allowed_for_local_dry_run: false`).
No occurrence records a performed mutation; every occurrence records the harness
refusing the proposed mutation.

The #463 importer's `_contains_source_mutation_marker` was a substring scan over the
entire serialized payload, so it could not distinguish "a mutation happened" from
"a proposed mutation was blocked", and flagged these refusal records.

## Secondary latent blocker: `blocked_evidence_boundary_failure`

The same committed #463 summary also records `evidence_boundary_status:
blocked_evidence_boundary_failure`. It was masked in the overall status by the
higher-ranked mutation concern and surfaced during the rerun for this lane.

- Cause: the importer required a literal `no execution` / `does not execute` /
  `not executed` phrase inside `evidence-boundary.md` + `evidence-boundary-review.md`.
  The #461 packet states `local-only` in `evidence-boundary.md` and places its
  non-execution statements in the dedicated `non-execution-proof.md`
  (`Proposed task commands were not executed.`), which the importer's own
  non-execution check already validates (`non_execution_status: present`).
- Assessment: importer text-heuristic false positive on a packet whose non-execution
  evidence is present in the canonical file; the boundary substance is intact.
- No #461 file was changed to clear this; the importer now also reads the packet's
  `non-execution-proof.md` for the non-execution phrase while still requiring
  `local-only` in the boundary files.
