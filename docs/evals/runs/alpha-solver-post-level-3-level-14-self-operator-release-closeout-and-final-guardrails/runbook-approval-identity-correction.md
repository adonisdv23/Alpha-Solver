# Runbook approval-identity correction record

## Exact runbook section reviewed

`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md`,
section `## 5. Approval identity behavior` (the section 3 cross-reference to
it was reviewed and left unchanged, as it describes operator policy and
defers to section 5 for the enforced behavior).

## Exact implementation files reviewed

- `alpha/self_operator/execution_gate.py` — specifically
  `_validate_approval_identity`, `_approval_scope_identity`,
  `_proposed_scope_identity`, `_proposed_run_id`, and `_normalize_identity`.

## Whether correction was needed

Yes. The prior wording stated that the gate "requires the approval record to
match the proposed task identity and fails closed on mismatch" with
unconditional "must equal" bullets, and listed the
`task_identity` / `scope_identity` / `scope_summary` / `requested_action`
metadata fallback chain in a way that did not distinguish the approval side
from the proposed-task side. The implementation compares each identity
dimension only when **both** sides provide a non-empty comparable value, the
proposed-task side draws scope identity only from metadata
`task_identity` / `scope_identity` / `scope_summary` (with no
`requested_action` fallback and no other fallback), and the proposed-task
run ID is read only from `metadata.run_id`.

## Whether correction was applied

Yes, applied in this lane, limited to section 5 of the runbook.

## Before/after summary

- Before: section 5 presented `lane_id`, `run_id`, and scope identity as
  unconditionally enforced equality requirements, and the
  `requested_action` fallback was listed without stating it applies only to
  the approval side.
- After: section 5 states that each dimension is compared, and fails closed,
  only when both the approval record and the proposed task provide
  comparable values; that the approval-side fallback chain (including
  `requested_action`, else top-level `scope_summary`) is approval-only; that
  the proposed-task side draws only from proposed metadata
  `task_identity` / `scope_identity` / `scope_summary` with no
  `requested_action` or other fallback; that a missing proposed-task
  identity field means that dimension cannot be compared by the current gate
  and is not an automatic identity-mismatch block; and that operators must
  therefore provide explicit proposed-task `metadata.run_id` and explicit
  proposed-task scope identity metadata. The mismatch finding, gate status,
  and no-override rule are unchanged.

## Confirmation: no runtime behavior was changed

Confirmed. `alpha/self_operator/execution_gate.py` was not modified by this
lane; only the runbook's description of it changed. The full focused test
suites for the execution gate and release gate pass unchanged except for the
intentional closeout-path constant in `release_gate.py` (see
`checks-run.md`).

## Confirmation: no source evidence was mutated

Confirmed. No file in any prior evidence packet was changed except this
single allowed runbook wording correction; the superseded #453 skeleton and
all #461/#465/#470/#471/#472 artifacts are untouched.
