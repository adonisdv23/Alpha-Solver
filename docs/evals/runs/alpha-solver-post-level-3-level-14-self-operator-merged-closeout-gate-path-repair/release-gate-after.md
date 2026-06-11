# Release gate after the repair

Run from the repo root on 2026-06-11, after aligning `CLOSEOUT_PACKET` in
`alpha/self_operator/release_gate.py` to the merged closeout packet path:

```bash
python scripts/check_self_operator_release_gate.py \
  --repo-root . \
  --output docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails/post-closeout-release-gate-report.json
```

- Exit code: `0`
- `final_status`: `eligible_for_release_closeout_review`
- `ready`: `true`
- `earliest_missing_gate`: `none`
- `release_closeout_review_complete`: `pass` — the checker now finds the
  closeout packet at
  `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails`.
- All eleven gates: `pass` (including `p0_p1_defects_absent`, which now also
  scans the newly recognized closeout packet directory and remains clean).
- Checker summary line: `11/11 gates pass; eligible for release closeout
  review, with no readiness claim.`

The machine-readable report is preserved in the closeout packet at
`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails/post-closeout-release-gate-report.json`,
with its narrative companion `post-closeout-release-gate-report.md` in the
same directory.

This is a deterministic gate result over local evidence-packet presence and
defect markers only. It is not a readiness claim of any kind.
