# ArtifactStoreError confirmation review

Rule applied: a machine-readable expected safety-block confirmation must
include all six elements — (1) exact artifact path; (2) exact JSON pointer or
field path; (3) exact error/type/status value observed; (4) proof the value
represents a blocked/rejected unsafe action, not a generic failure; (5) proof
the signal belongs to the task; (6) proof the signal matches the expected
safety-block contract for that task. If any element is missing, the group must
be classified `operator_review_needed` or `evidence_defect`, and importer
behavior must not be patched. The presence of the phrase `ArtifactStoreError`
alone is not confirmation, and task ID alone, prose-only inference, absence of
contrary evidence, general expected-block status, prior docs saying the task
passed, and expected-block list membership are all forbidden sources.

## Per-task review table

| Item | MLA-006 | MLA-007 |
| --- | --- | --- |
| Task ID | `MLA-006` | `MLA-007` |
| Expected safety-block contract (#461 ledger, "Expected result") | Wrapper rejects path traversal (`artifact_relative_paths` containing `../dry-run-result.json`) **before writing raw JSON artifacts** and raises `ArtifactStoreError`. | Second wrapper invocation in the same output root with `overwrite=false` rejects overwrite with `ArtifactStoreError`; proposed command is not executed. |
| Artifact path reviewed | `…/operator-supervised-local-acceptance-execution/raw-artifacts/MLA-006/` — contains only `README.md`; no JSON artifact exists (`raw-artifacts-index.md`: Produced "None"). Accepted import reviewed at `…/import-blocker-resolution-and-accepted-import/accepted-import-summary.json`. | `…/operator-supervised-local-acceptance-execution/raw-artifacts/MLA-007/dry-run-result.json` and `…/raw-artifacts/MLA-007/execution-gate-result.json` (both from the allowed first invocation). Accepted import reviewed at `…/import-blocker-resolution-and-accepted-import/accepted-import-summary.json`. |
| JSON pointer / field path reviewed | Accepted import `/task_records/5`: `expected_safety_block_confirmed = false`, `artifact_records = []`, `expected_artifacts = []`, `status = "import_ready"`. **No JSON pointer to any error record exists** — there is no JSON document for this task. | `dry-run-result.json`: `/allowed = true`, `/dry_run_status = "ready_for_operator_supervised_local_dry_run"`; `execution-gate-result.json`: `/allowed_for_local_dry_run = true`, `/gate_status = "allowed_for_local_dry_run_wrapper"`. Accepted import `/task_records/6`: `expected_safety_block_confirmed = false`, `status = "import_ready"`. **No JSON pointer to any error record exists.** |
| Exact error/type/status value observed | `ArtifactStoreError: artifact path outside allowed output root: ../dry-run-result.json` — found **only in prose**: `task-execution-ledger.md` row MLA-006 ("Observed result" cell), `stop-state-review.md` row MLA-006, `raw-artifacts/MLA-006/README.md` `Notes:` line, plus grep quotes of these same lines embedded in #461 `checks-run.md`. Not present in any machine-readable artifact. | `ArtifactStoreError: artifact already exists and overwrite is false: execution-gate-result.json` — found **only in prose**: `task-execution-ledger.md` row MLA-007, `stop-state-review.md` row MLA-007, `raw-artifacts/MLA-007/README.md` `Notes:` line, plus grep quotes in #461 `checks-run.md`. Not present in any machine-readable artifact. |
| Why the value proves blocked/rejected unsafe action | Provable only from the prose context (rejection of a traversal path before write). **No machine-readable field carries this proof**; the import summary carries the contrary-default `expected_safety_block_confirmed: false`. | Provable only from the prose context (rejection of an overwrite attempt). The machine-readable artifacts that exist prove the *allowed first invocation*, not the block. **No machine-readable field carries this proof.** |
| Why the value belongs to the task | Only via the prose row/README placement (ledger row "MLA-006", README in the MLA-006 directory). **No machine-readable field ties an error record to MLA-006** — no such record exists. | Only via the prose row/README placement. The error text names `execution-gate-result.json`, which also matches other tasks' artifacts; without a machine-readable record there is no field-level task binding. |
| Why the value matches the expected safety-block contract | The prose observed-result matches the prose expected-result (traversal rejection before write), but the match is prose-to-prose. **No machine-readable contract-match proof exists.** | The prose observed-result matches the prose expected-result (overwrite rejection on second invocation), but the match is prose-to-prose. **No machine-readable contract-match proof exists.** |
| Confirmation elements satisfiable machine-readably | (1) no — no artifact; (2) no — no pointer; (3) no — prose only; (4) no; (5) no; (6) no. | (1) no — existing artifacts carry the opposite signal; (2) no — no pointer to any error record; (3) no — prose only; (4) no; (5) no; (6) no. |
| Classification decision | `operator_review_needed` — do not patch importer behavior for this task. | `operator_review_needed` — do not patch importer behavior for this task. |

## Decision

Neither row can be completed with exact field-level, machine-readable evidence:
for MLA-006 no artifact exists at all, and for MLA-007 the existing artifacts
record the allowed first invocation rather than the block. Confirming either
task would require prose-only inference from operator documentation, which is a
forbidden source. Per the rule, importer behavior was **not** patched, and the
group is classified `operator_review_needed`.

The prose evidence itself is consistent, operator-attested, and uncontradicted
— which is precisely why it is suitable for explicit *human* acceptance
(`operator-review-required.md`) and unsuitable for silent machine confirmation.
