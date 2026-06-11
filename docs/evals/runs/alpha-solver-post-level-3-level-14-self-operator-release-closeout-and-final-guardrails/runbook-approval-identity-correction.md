# Runbook approval identity correction

## Exact runbook section reviewed

`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md`, section `## 5. Approval identity behavior`.

## Exact implementation files reviewed

`alpha/self_operator/execution_gate.py`.

## Whether correction was needed

Correction was needed. The prior runbook wording implied broader proposed-task identity enforcement than the current gate implements.

## Whether correction was applied

Correction was applied in the canonical runbook file only.

## Before summary

The prior section said approval `lane_id`, approval `run_id`, and approval scope identity must match the proposed task identity and described `requested_action` in a way that could be read as part of proposed-task fallback behavior.

## After summary

The corrected section states that the gate fails closed on mismatches only when both sides provide comparable values, tells operators to provide explicit proposed-task `metadata.run_id`, tells operators to provide explicit proposed-task metadata scope identity, explains that missing proposed metadata identity fields cannot be compared by the current gate, and states that proposed task scope identity does not fall back to `requested_action`.

## Confirmations

- No runtime behavior was changed.
- No source evidence was mutated.
