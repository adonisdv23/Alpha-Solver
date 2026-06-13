# P2-002: #492 / F-1 correction primary evidence

Status: resolved with in-repository primary evidence. The Council evidence packet attested that #492 corrected stale F-1 status wording; the before/after text below shows the correction itself.

## Sources

- Commit `448cf34b6cf54831f0574360eeb49b23a90dedcd` — "docs(self-operator): correct Council bundle F-1 status (#492)".
- Correction packet: `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-bundle-f1-status-correction/` (in particular `stale-status-correction.md` and `changed-file-scope-proof.md`).
- Corrected files: `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/README.md` and `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/current-state-snapshot.md`.

## Before and after wording (from the commit diff)

Stale wording removed (README, with the snapshot file carrying the equivalent lane-specific sentence):

> F-1 remains open for the future checker-scope extension lane.

Corrected wording added:

> The earlier F-1-open wording reflected the post-#488, pre-#489, and pre-#490 state and is superseded by the post-#490 verification annex. After #489 and #490, F-1/N-1 are recorded as resolved pending targeted Fable delta re-audit confirmation; the targeted Fable delta re-audit remains the routed next validation step.

The commit also added a clearly labeled `Post-#491 F-1 status correction` section to both files, preserving the boundary statements that Council had not run, manual operator review had not happened, and no readiness claim was made.

## Substantive adequacy assessment

The correction is substantively what the Council evidence packet attested: it replaces an unqualified F-1-open statement with a qualified historical statement plus the current recorded status (F-1/N-1 resolved **pending targeted Fable delta re-audit confirmation**). The correction does not overstate: it records resolution as pending a named confirmation step rather than as final.

Residual limitation: the wording "resolved pending targeted Fable delta re-audit confirmation" depends on the prior targeted Fable delta audit, whose full text is not in the repository. That audit reported no P0/P1 blockers; reliance on that summary is recorded as a deferral (see `deferral-register.md` DEF-003) and must be cited only as "reported no P0/P1 blockers".
