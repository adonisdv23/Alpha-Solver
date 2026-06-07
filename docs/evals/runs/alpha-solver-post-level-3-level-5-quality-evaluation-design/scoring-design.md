# Scoring Design

## Scoring dimensions

Future evaluation execution packets should define a rubric that can include these dimensions when applicable:

- **Correctness**: the answer satisfies the task requirements and avoids material errors.
- **Completeness**: the answer covers required parts without omitting necessary constraints.
- **Evidence fidelity**: the answer distinguishes source-supported statements from inference or speculation.
- **Boundary compliance**: the answer avoids forbidden claims, unauthorized actions, and evidence promotion.
- **Reasoning clarity**: the answer explains key reasoning steps at the level required by the task.
- **Actionability**: the answer gives usable next steps when the task calls for operational guidance.
- **Reproducibility support**: the answer preserves commands, inputs, outputs, or references needed to audit the result when applicable.
- **Safety and deferral behavior**: the answer stops or defers when evidence is missing, contradictory, stale, overbroad, or non-reproducible.

## Required scale

A future lane must freeze a numeric or categorical scale before execution. The default recommended design is a 0-4 integer scale per dimension:

- **0**: fails the dimension or violates the boundary.
- **1**: materially weak; major omissions or errors.
- **2**: partially acceptable; meaningful gaps remain.
- **3**: acceptable; minor issues only.
- **4**: strong; satisfies the dimension clearly and reproducibly.

Any future lane may adjust the scale only before task execution and must document why the adjustment is necessary.

## Reviewer requirements

Future scoring must require:

- at least two independent reviewers for scored quality claims;
- reviewer access to the frozen rubric, task prompt, allowed context, and raw output;
- reviewer conflict-of-interest disclosure for task authorship or implementation work;
- no reviewer editing of raw outputs;
- preservation of individual scores before reconciliation;
- a reviewer note when a score depends on inference rather than direct evidence.

## Disagreement handling

A future lane must define disagreement thresholds before scoring. The recommended default is:

- if reviewers differ by more than one point on any dimension, require adjudication;
- adjudication must record the disputed dimension, reviewer rationales, final score, and reason for final score;
- unresolved disagreement invalidates the affected dimension for claim support;
- rubric ambiguity discovered during scoring must be logged as a defect and may stop interpretation if material.

## Pass/fail criteria requirements

This packet does not set pass/fail thresholds for Alpha Solver quality. A later execution lane must define thresholds before execution and must state which claims, if any, those thresholds are authorized to support.
