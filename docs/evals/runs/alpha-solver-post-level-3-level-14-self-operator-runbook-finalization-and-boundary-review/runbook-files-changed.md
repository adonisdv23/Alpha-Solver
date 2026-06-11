# Runbook files changed

All changes are new documentation files; no existing file was modified or
deleted. Three directories were created.

## 1. Canonical runbook packet (gate evidence for `mvp_runbook_finalized_or_updated`)

`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/`

- `README.md`
- `mvp-operator-runbook.md` (the canonical finalized runbook)
- `evidence-boundary.md`
- `non-actions.md`
- `selected-next-lane.md`
- `blocker-fallback-lane.md`

## 2. Evidence-boundary review packet (gate evidence for `evidence_boundary_review_complete`)

`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-evidence-boundary-review/`

- `README.md`
- `evidence-boundary-review.md` (the canonical review record)
- `evidence-boundary.md`
- `non-actions.md`
- `selected-next-lane.md`
- `blocker-fallback-lane.md`

## 3. This lane packet

`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-runbook-finalization-and-boundary-review/`
with the fifteen files listed in its `README.md`.

## Scope rationale for the two gate-packet directories

The lane contract names two allowed surfaces: the canonical runbook file(s)
and this lane packet directory. The canonical runbook location is not
free-form: the deterministic release-gate checker on `main`
(`alpha/self_operator/release_gate.py`, merged in #462 and applied in #471)
defines the runbook-finalization and boundary-review evidence packets at the
two exact paths above, and the accepted #471 gate evidence
(`.../alpha-solver-post-level-3-level-14-self-operator-release-gate-apply/selected-next-lane.md`)
states that this lane "may produce the MVP runbook finalization packet and
the evidence-boundary review packet the checker requires."

The two gate-packet directories are therefore treated as the canonical
runbook surface and the canonical boundary-review surface of this lane —
not as out-of-scope additions. No other paths were touched: no application
code, no tests, no scripts, no specs, no prior packet, no workflow files
(verified in `forbidden-surface-scan.md` and `checks-run.md`).

## Files deliberately not changed

- `.../alpha-solver-post-level-3-level-12-to-level-14-self-operator-runbook-review-skeleton/operator-runbook-skeleton.md`
  (superseded, preserved unchanged).
- Every packet of the accepted evidence chain (#461, #463/#465,
  #464/#466/#467/#469/#470, #471).
- `alpha/self_operator/*`, `scripts/*`, `tests/*`.
