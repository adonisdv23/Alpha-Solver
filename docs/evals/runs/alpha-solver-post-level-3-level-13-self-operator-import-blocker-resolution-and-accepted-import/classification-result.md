# Classification result

Classification of the MLA-010 source-artifact mutation concern:

```
expected_synthetic_marker
```

Recorded by the deterministic triage tool in `import-blocker-triage-result.json`
(`python scripts/triage_self_operator_import_blocker.py`).

## Safety rule applied

> If the MLA-010 marker appears in a source artifact in a way that could indicate true
> source mutation, default to inconclusive unless the packet contract explicitly allows
> that marker.

The default-to-inconclusive branch was not taken because the packet contract explicitly
expects this marker and no occurrence could indicate a performed mutation:

1. The #461 packet's `task-execution-ledger.md` MLA-010 row states the expected result
   `Wrapper does not execute proposed command; sentinel file remains absent; unsafe
   source mutation command is blocked.` and records status `PASS`. The blocked
   source-mutation outcome is the contracted expectation for MLA-010.
2. The marker strings are exactly the codes `alpha/self_operator/command_classification.py`
   emits when it refuses a command under the `forbidden source-artifact mutation` rule
   (reason code `source_artifact_mutation`, finding ID
   `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED`; the rule pattern includes `touch`,
   the MLA-010 fixture command). They are refusal records, not mutation records.
3. All 13 occurrences sit inside blocked-finding contexts (`stop_state: blocked`,
   `allowed: false`, `gate_status: blocked_by_failed_preflight`); zero occurrences sit
   outside that context (see `blocked-artifact-review.md`).
4. Recomputed SHA-256 checksums of all three MLA-010 artifacts match the #461
   `artifact-ledger.md` values, so the recorded artifacts were not altered after the
   ledger was written.
5. The #461 `non-execution-proof.md` confirms the MLA-010 mutation command was blocked
   instead of executed and that the sentinel file remained absent.

## Classifications rejected

- `true_violation`: no artifact records an allowed or executed mutation; checksums match.
- `malformed_artifact`: all three artifacts parse as JSON objects with required fields.
- `packet_generation_defect`: ledger rows, checksums, index rows, and artifact contents
  are mutually consistent.
- `importer_false_positive` (alone): the marker is genuinely present in the artifacts;
  the precise defect is that the importer treated the expected synthetic blocked-outcome
  marker as a mutation concern. The marker itself is expected, so
  `expected_synthetic_marker` is the more accurate single classification; the importer's
  context-insensitive substring scan is the mechanism that turned the expected marker
  into a block.
- `inconclusive`: not applicable because the packet contract explicitly expects the
  blocked source-mutation marker for MLA-010 (safety-rule exception satisfied).

This classification is an import-validation conclusion only. It does not interpret
acceptance success or failure and does not claim MVP or release readiness.
