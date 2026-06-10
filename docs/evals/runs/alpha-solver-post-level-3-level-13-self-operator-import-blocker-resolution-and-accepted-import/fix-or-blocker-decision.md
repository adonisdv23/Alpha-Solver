# Fix-or-blocker decision

Decision: narrow importer fix (classification `expected_synthetic_marker` selects the
fix branch of the lane contract).

## What was patched

`alpha/self_operator/result_import.py` only:

1. Source-mutation marker detection is now context-aware instead of a substring scan
   over the whole serialized payload. `find_source_mutation_markers` walks the payload
   and accepts a marker only in the exact shapes the dry-run harness emits when it
   refuses a proposed mutation:
   - `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED` as a finding `id` or a
     `finding_ids` entry whose containing object is blocked;
   - `source_artifact_mutation` as a `command_reason_codes` entry whose containing
     object is blocked;
   - `source_artifact_mutation` as a `reason_code` only inside a finding whose `id` is
     `SELF_OPERATOR_SOURCE_ARTIFACT_MUTATION_BLOCKED` and whose state is blocked.
   "Blocked" requires `stop_state == blocked`, a `gate_status`/`dry_run_status`
   beginning with `blocked`, or `allowed`/`allowed_for_local_dry_run` equal to `false`.
   Every other occurrence (including marker-bearing keys, free text, or a
   `source_artifact_mutation` reason code outside the canonical blocked finding) still
   raises `blocked_source_mutation_concern`.
2. The packet-level evidence-boundary check still requires `local-only` in
   `evidence-boundary.md`/`evidence-boundary-review.md` but now also reads the packet's
   dedicated `non-execution-proof.md` (already independently validated by the
   non-execution check) when looking for the non-execution phrase, instead of requiring
   the phrase to be duplicated inside the boundary files. A packet with no non-execution
   statement anywhere still blocks through both checks.

## True source-mutation blocking preserved

- A marker outside the canonical blocked-finding context still blocks
  (`test_blocks_mutation_marker_outside_blocked_finding_context`).
- A `source_artifact_mutation` reason code without the canonical blocked finding shape
  still blocks (pre-existing `test_rejects_source_artifact_mutation_markers`, unchanged
  and passing).
- An affirmative allowed/executed mutation record classifies as `true_violation` in the
  triage tool (`test_allowed_mutation_record_classifies_true_violation`).
- Boundary files without `local-only` still block
  (`test_blocks_boundary_missing_local_only_despite_proof_file`).
- The packet-level scan of `artifact-integrity-checks.md`/`stop-state-review.md`/
  `non-actions.md` for unblocked mutation language is unchanged.

## What was deliberately not done

- No #461 source artifact was modified, regenerated, or replaced.
- No artifact was fabricated.
- The importer was not patched to skip, whitelist tasks, downgrade statuses, or force
  acceptance; detection became shape-exact rather than disabled.
- The blocker branch (blocker review packet + Prompt 2 next lane) was not selected
  because the classification is `expected_synthetic_marker`, which the lane contract
  maps to the fix branch.
