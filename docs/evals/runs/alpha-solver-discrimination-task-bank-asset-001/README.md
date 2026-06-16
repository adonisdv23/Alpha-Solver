# Discrimination Task Bank Asset Feasibility Study

Lane:
`ALPHA-SOLVER-DISCRIMINATION-TASK-BANK-ASSET-001`

## Purpose

This docs-only feasibility study examines whether Alpha Solver should later create a reusable discrimination task bank for false-premise, hidden-constraint, should-stop, confidence, and claim-boundary tasks.

The proposed asset would support future evaluation design by standardizing task intent, ideal behavior fields, baseline failure-mode fields, repeatability controls, current-fact freeze metadata, and stop criteria before any implementation or scoring lane is authorized.

## Feasibility verdict

`FEASIBLE_WITH_GUARDED_NEXT_STEP`

A reusable task bank appears feasible as a documentation-first asset if the first follow-up remains cheap, manual, and non-executing: draft five representative task cards, one per taxonomy family, and review them against the fields and kill conditions in this packet.

This verdict is not a claim that Alpha Solver is ready, valuable, superior, safer, or more accurate. It only says the task-bank concept is coherent enough to justify one small follow-up design check.

## Required deliverables

- `task-taxonomy.md` defines the task families and intended discrimination signals.
- `30-task-outline.md` sketches a non-frozen 30-task candidate outline.
- `ideal-behavior-fields.md` defines fields a future ideal-response record should contain.
- `baseline-failure-mode-fields.md` defines fields a future baseline-failure record should contain.
- `repeatability-plan.md` defines controls for stable task reuse.
- `kill-conditions.md` defines conditions that should stop or cancel the asset.
- `non-actions.md` records actions intentionally not taken.
- `non-claims.md` records claims intentionally not made.
- `checks-run.md` records the checks performed for this docs-only packet.

## Boundaries

This packet does not create output artifacts, generate model responses, score responses, call providers, run local models, modify runtime behavior, expose dashboards, expose public APIs, call `/v1/solve`, update Google Sheets, or update global source-of-truth files. Current-fact task reuse is conditioned on preserving the frozen as-of date and source snapshot or creating a new task revision.
