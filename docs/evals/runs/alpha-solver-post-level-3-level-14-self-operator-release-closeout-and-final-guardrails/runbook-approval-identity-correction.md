# Runbook approval identity correction

## Exact runbook section reviewed

`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md`, section `## 5. Approval identity behavior`.

## Exact implementation files reviewed

- `alpha/self_operator/execution_gate.py`
- `alpha/self_operator/preflight.py`

## Whether correction was needed

Correction was needed. The pre-closeout check found that the canonical runbook overstated approval identity enforcement by saying approval identity must match proposed identity without explaining that `run_id` and scope identity are compared only when comparable values are present on both sides.

## Whether correction was applied

Correction was applied in the canonical runbook file only.

## Before / after summary

Before:

- The runbook implied `lane_id`, `run_id`, and scope identity were always enforced as required comparisons.
- The runbook described approval metadata `requested_action` in a way that could be read as a proposed-task fallback.
- The runbook did not tell operators that missing proposed metadata fields prevent that dimension from being compared by the current gate.

After:

- The runbook states that the gate fails closed on mismatches only when both sides provide comparable identity fields.
- The runbook tells operators to provide explicit proposed-task `metadata.run_id`.
- The runbook tells operators to provide explicit proposed-task metadata scope identity.
- The runbook states that if proposed metadata identity fields are missing, that dimension cannot be compared by the current gate.
- The runbook does not imply that missing proposed identity fields always produce approval identity mismatch.
- The runbook does not imply `requested_action` is a proposed-task fallback.

## Confirmations

- No runtime behavior was changed.
- No source evidence was mutated.
- The correction file changed only the allowed canonical runbook file.
