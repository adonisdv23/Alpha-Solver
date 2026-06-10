# Regression test notes

## Coverage for the exact MLA-010 marker

`tests/test_self_operator_result_import.py` (importer behavior):

- `test_accepts_exact_mla_010_blocked_mutation_marker_shapes`: a synthetic packet whose
  MLA-010 artifacts replicate the exact #461 shapes (blocked finding with
  `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED` / `source_artifact_mutation`,
  blocked `finding_ids` and `command_reason_codes` lists) imports as
  `import_ready_with_expected_blocks` with no findings.
- `test_blocks_mutation_marker_outside_blocked_finding_context`: the same canonical
  packet plus one marker string outside the blocked-finding context blocks with
  `blocked_source_mutation_concern`.
- `test_rejects_source_artifact_mutation_markers` (pre-existing, unchanged): a
  `source_artifact_mutation` reason code without the canonical blocked finding shape
  still blocks. This is the true-mutation guard.
- `test_actual_461_packet_imports_with_expected_blocks`: the real #461 packet imports as
  `import_ready_with_expected_blocks` with `source_artifact_mutation_status:
  not_present` and `evidence_boundary_status: present`.
- `test_handles_actual_461_packet_if_present_without_mutating_it` (pre-existing,
  unchanged): importing the real packet does not modify any packet file.

Evidence-boundary fix coverage:

- `test_accepts_boundary_non_execution_phrase_from_proof_file`: boundary files with
  `local-only` but without a literal non-execution phrase pass when
  `non-execution-proof.md` carries the phrase.
- `test_blocks_boundary_missing_local_only_despite_proof_file`: boundary files without
  `local-only` still block even when the proof file is present.
- `test_detects_missing_evidence_boundary` (pre-existing, unchanged): empty boundary
  files still block.

## Triage tool coverage

`tests/test_self_operator_import_blocker_triage.py`:

- canonical blocked-marker packet classifies `expected_synthetic_marker`;
- marker outside blocked context defaults to `inconclusive` (safety rule);
- missing packet-contract expectation defaults to `inconclusive` (safety rule);
- malformed MLA-010 JSON classifies `malformed_artifact`;
- ledger checksum mismatch defaults to `inconclusive`;
- an affirmative allowed/executed mutation record classifies `true_violation` with the
  do-not-patch follow-up;
- missing expected artifact defaults to `inconclusive`;
- a blocked packet without any marker classifies `importer_false_positive`;
- triage is read-only and its JSON output is deterministic;
- the real #461 packet classifies `expected_synthetic_marker` without any file change;
- CLI `--help` smoke test.

## Results

- `python -m pytest -q tests/test_self_operator_import_blocker_triage.py` — 11 passed.
- `python -m pytest -q tests/test_self_operator_result_import.py` — 19 passed
  (14 pre-existing tests unchanged and passing, 5 added).
- Full-suite comparison: the set of failing tests under `python -m pytest -q
  --continue-on-collection-errors` is byte-identical on unmodified `main` and on this
  branch (24 pre-existing failures from missing optional dependencies such as
  `fastapi`/`httpx`/`anyio`/`starlette` and sandbox subprocess constraints; none related
  to this change).
