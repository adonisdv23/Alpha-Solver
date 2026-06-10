# Downstream interpretation impact

## The consumption requirement

Downstream tooling must consume this operator decision **explicitly** before
interpretation can pass for MLA-006 and MLA-007. Concretely, for the next lane:

- Inputs: the unchanged #465 accepted import summary
  (`accepted-import-summary.json`, sha256
  `a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c`)
  **plus** this packet's `operator-decision.json`
  (`schema self_operator.expected_safety_block_operator_review.v1`).
- The decision artifact may satisfy the expected-block confirmation for
  exactly the tasks in `accepted_tasks` (`MLA-006`, `MLA-007`), with
  confirmation type `operator_ledger_level_acceptance` — a distinct,
  explicitly-labeled confirmation source, never conflated with
  machine-readable artifact confirmation
  (`machine_readable_artifact_confirmation: false`).
- Silent or implicit behavior remains forbidden: an interpretation run that
  is not given the decision artifact must keep reporting both P1
  `EXPECTED_SAFETY_BLOCK_UNCONFIRMED` defects, exactly as #468's
  verification did.

## What this lane did not do

- It did **not** run interpretation (no engine invocation of any kind; no
  interpretation retry).
- It did **not** modify `alpha/self_operator/result_import.py`,
  `alpha/self_operator/acceptance_interpretation.py`, any test, or any
  script. Teaching the engine to consume operator-decision artifacts is the
  next lane's work, done under that lane's own scope and tests.
- It did **not** run the release gate, which stays forbidden while the P1
  blockers remain open in the machine-readable record.

## Current engine behavior (unchanged, for the record)

On current `main`, the engine has no notion of an operator-decision input.
Given the accepted import alone it returns `blocked` (p0=0, p1=2) — the
result most recently verified read-only by #468. Nothing in this lane changes
that behavior; this packet only supplies the decision artifact that the next
lane is required to consume.
