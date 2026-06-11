# Release gate before the repair

Run from the repo root on 2026-06-11 at `main` state `a0d53f7` (PR #474
merged), before any edit in this lane:

```bash
python scripts/check_self_operator_release_gate.py --repo-root . --output /tmp/release-gate-before.json
```

- Exit code: `1`
- `final_status`: `blocked_release_closeout_not_reviewed`
- `ready`: `false`
- `earliest_missing_gate`: `release_closeout_review_complete`
- `release_closeout_review_complete`: `missing` — the checker looked for
  `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout`,
  which does not exist; the packet #474 actually merged lives at
  `...-release-closeout-and-final-guardrails/`.
- All ten other gates: `pass`.
- Checker summary line: `10/11 gates pass; final status is
  blocked_release_closeout_not_reviewed. This is not a readiness claim.`

Closeout gate entry from the captured before-report:

```json
{
  "evidence_path": "docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout",
  "gate_id": "release_closeout_review_complete",
  "reason": "Required evidence packet directory is absent.",
  "required_next_action": "Complete release closeout review only after all preceding gates pass.",
  "status": "missing"
}
```

The before-report was written to a temporary path on purpose: the closeout
packet's `post-closeout-release-gate-report.json` slot is reserved for the
post-repair proof and must not be occupied by a blocked pre-repair report.
