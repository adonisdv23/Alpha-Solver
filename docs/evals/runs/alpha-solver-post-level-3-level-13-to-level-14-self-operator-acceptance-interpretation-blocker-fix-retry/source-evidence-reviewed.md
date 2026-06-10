# Source evidence reviewed (all read-only, none mutated)

## #461 operator-supervised execution packet

`docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-operator-supervised-local-acceptance-execution/`

- `task-execution-ledger.md` — rows 10 (MLA-006) and 11 (MLA-007). Expected
  results: "Wrapper rejects traversal before writing raw JSON artifacts and
  raises ArtifactStoreError" (MLA-006); "Second wrapper invocation rejects
  overwrite with ArtifactStoreError; proposed command is not executed"
  (MLA-007). Observed results (prose cells):
  `exception=ArtifactStoreError: artifact path outside allowed output root: ../dry-run-result.json`
  and `... second invocation blocked with ArtifactStoreError: artifact already
  exists and overwrite is false: execution-gate-result.json`. MLA-006 raw
  artifact paths: "None produced".
- `stop-state-review.md` — MLA-006/MLA-007 rows; review note: "rejected before
  producing new stop-state JSON where applicable".
- `raw-artifacts-index.md` — MLA-006: Produced artifacts "None", all three
  artifacts listed as missing-expected, status PASS (pre-write rejection is the
  designed behavior). MLA-007: produced `dry-run-result.json;
  execution-gate-result.json`, missing-expected `stop-state.json`, status PASS.
- `raw-artifacts/MLA-006/` — contains only `README.md` (expected-artifact
  clause: "unless the wrapper rejected before write"; produced list: `None`;
  checksum list: `None`; error text appears only in the prose `Notes:` line).
- `raw-artifacts/MLA-007/README.md` — produced list of two artifacts with
  sha256 checksums; the overwrite-rejection text appears only in the prose
  `Notes:` line.
- `raw-artifacts/MLA-007/dry-run-result.json` — first (allowed) invocation:
  `/allowed = true`, `/dry_run_status = "ready_for_operator_supervised_local_dry_run"`,
  `/reason_code = "ready_for_local_dry_run_wrapper"`. Contains no error record.
- `raw-artifacts/MLA-007/execution-gate-result.json` — first (allowed)
  invocation: `/allowed_for_local_dry_run = true`,
  `/gate_status = "allowed_for_local_dry_run_wrapper"`. Contains no error record.
- `artifact-ledger.md` — structured rows exist only for produced artifacts
  (MLA-007 two rows; no MLA-006 rows); no error/type/status column exists.
- `checks-run.md` — every `ArtifactStoreError` occurrence (lines 78, 79, 127,
  128, 216, 264) is an embedded grep audit quoting the same prose lines above;
  no machine-readable record.
- `blocked-or-failed-tasks.md`, `defect-log.md`, `operator-confirmation.md`,
  `artifact-integrity-checks.md`, `evidence-boundary.md`,
  `non-execution-proof.md` — packet-internal consistency context: no FAIL /
  BLOCKED / NOT RUN tasks, no defects, operator confirmation PRESENT, integrity
  checks PASS.

## #465 accepted import summary

`docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json`
(sha256 `a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c`, unchanged)

- `/task_records/5` (MLA-006): `status = "import_ready"`,
  `expected_safety_block_confirmed = false`, `artifact_records = []`,
  `expected_artifacts = []`, `missing_artifacts = []`, `findings = []`.
- `/task_records/6` (MLA-007): `status = "import_ready"`,
  `expected_safety_block_confirmed = false`, two artifact records (both from
  the allowed first invocation, checksums matched), no error record.
- Top level: `status = "import_ready_with_expected_blocks"`,
  `schema_version = "self_operator.acceptance_import_summary.v1"`.

## #466 Prompt 3 interpretation packet (PR #466, merged into `main`)

`docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-interpretation-and-release-gate-apply/`

- `defect-register.md` and `interpretation-result.json` — original 10-defect
  blocked result including the MLA-006/MLA-007 P1 rows; root-cause note that the
  #461 ledger records the blocks as `ArtifactStoreError` rejections without
  stop-state JSON.

## #467 Prompt 4 blocker-fix packet (PR #467, merged into `main`)

`docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-acceptance-interpretation-blocker-fix/`

- `remaining-defects.md` — the two remaining P1
  `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` blockers and why #467 could not resolve
  them (importer outside that lane's allowed scope; confirmation exists only in
  ledger prose).
- `selected-next-lane.md` — hands this retry lane the remaining group with the
  explicit branch "route it to a focused import-tooling fix lane or to operator
  review".
- `blocker-review.md`, `fixes-applied.md`, `evidence-boundary.md`,
  `checks-run.md` — scope and verification context for the engine fix.

## Code and tests (read-only; current `main`)

- `alpha/self_operator/result_import.py` — confirmation rule at the
  `expected_safety_block_confirmed` assignment: `stop_state_present and
  bool(expected_artifacts)`; confirmation derives solely from a validated
  `stop-state.json` artifact. Inputs read: raw-artifact JSON files plus the
  structured `raw-artifacts-index.md` / `artifact-ledger.md` tables (paths,
  checksums, schema/lane/run IDs). The importer never reads the
  task-execution-ledger "Observed result" prose, stop-state-review rows, or
  raw-artifact README `Notes:` lines, and its ledger parsing carries no
  error/type/status field.
- `alpha/self_operator/acceptance_interpretation.py` — MLA-006/MLA-007 are in
  `EXPECTED_SAFETY_BLOCKED_TASK_IDS`; `_observed_outcome` maps their importer
  records (`status = "import_ready"`, `expected_safety_block_confirmed =
  false`, no `allowed` boolean) to `unconfirmed`; the
  expected-blocked + unconfirmed branch raises P1
  `EXPECTED_SAFETY_BLOCK_UNCONFIRMED`. This is truthful reporting of the input,
  not an engine parsing defect.
- `tests/test_self_operator_result_import.py` — importer coverage including
  `test_actual_461_packet_imports_with_expected_blocks` and
  `test_handles_actual_461_packet_if_present_without_mutating_it` (the real
  packet imports with expected blocks and is not mutated); no test asserts
  block confirmation without a stop-state, consistent with the v1 contract.
- `tests/test_self_operator_acceptance_interpretation.py` — engine coverage
  including `test_importer_vocabulary_unconfirmed_expected_block_still_blocks`
  (an unconfirmed expected block must keep blocking; added by #467).
