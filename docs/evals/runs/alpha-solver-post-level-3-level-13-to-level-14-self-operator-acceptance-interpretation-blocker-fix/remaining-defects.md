# Remaining defects

## Unresolved blockers after this lane

Two P1 blockers remain. The fixed engine, run read-only against the unmodified
accepted import summary, reports:

```
P1 EXPECTED_SAFETY_BLOCK_UNCONFIRMED MLA-006 — Expected safety block is not confirmed by the import summary.
P1 EXPECTED_SAFETY_BLOCK_UNCONFIRMED MLA-007 — Expected safety block is not confirmed by the import summary.
```

Readiness implication: still `blocked` (p0=0, p1=2, p2=0, p3=0).

## Why this lane did not resolve them

- The accepted import summary records MLA-006 with no artifact records
  (`artifact_records: []`, `expected_artifacts: []`) and MLA-007 with only
  dry-run and execution-gate artifacts; both carry
  `expected_safety_block_confirmed: false`. The importer's v1 contract derives
  block confirmation solely from a valid `stop-state.json` artifact, and the
  real #461 execution produced these two blocks as `ArtifactStoreError`
  rejections (path-traversal and overwrite) **without** stop-state artifacts —
  by design of those scenarios. The confirmation exists only in the #461
  task-execution ledger prose, which the import summary does not carry in
  machine-readable form.
- Making the engine treat "no contrary marker" as a confirmed block would
  fabricate confirmation the input does not contain, and would make a genuinely
  allowed task indistinguishable from a blocked one. Forbidden.
- Mutating or regenerating the accepted import summary is forbidden in this lane
  (source evidence; `evidence_defect` rules), and the importer
  (`alpha/self_operator/result_import.py`) is outside the allowed file scope of
  this lane's `tooling_false_positive` classification.

## Routing for the remaining group

The remaining group has its own shared root cause, distinct from the engine
parsing defects fixed here: **the importer's v1 representation cannot record
expected-block confirmation for tasks blocked via `ArtifactStoreError` without
stop-state artifacts (MLA-006, MLA-007).**

Routed to the next blocker-fix iteration (see `selected-next-lane.md`), which
must process it as its own single blocker group and classify it there. Plausible
classifications for that lane to evaluate (not decided here): a focused importer
tooling fix in the import-tooling lane family
(`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-13-SELF-OPERATOR-LOCAL-ACCEPTANCE-RESULT-IMPORT-TOOLING-FIX-001`
is the import lane's own declared fallback) followed by a re-import, or
`operator_review_needed` if the operator prefers to accept ledger-level
confirmation explicitly. Resolution is **not** claimed or pre-empted here.

## Pre-existing repository issues observed (unrelated to this lane)

- 36 test modules fail pytest collection on a clean checkout (missing optional
  third-party dependencies such as `starlette`); reproduced identically with and
  without this lane's changes.
- `tests/test_adapters_playwright_hardened.py` (4),
  `tests/test_scenarios.py` (5), and `tests/test_tag_release.py` (1) fail on a
  clean `origin/main` worktree in this environment (missing deps / sandbox git
  commit signing); reproduced before this lane's changes.

These are reported for transparency; they are not part of the processed blocker
group and were not touched.
