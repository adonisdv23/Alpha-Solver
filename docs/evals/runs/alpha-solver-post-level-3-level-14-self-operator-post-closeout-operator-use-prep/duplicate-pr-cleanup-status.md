# Duplicate PR cleanup status

Live PR state re-verified via the GitHub API on 2026-06-11 by this lane,
before any edit, and cross-checked against the merged repair packet
(`docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-merged-closeout-gate-path-repair/live-pr-state-reviewed.md`).

## Live state

| PR | State | Merged | Detail |
| --- | --- | --- | --- |
| #473 | closed | no | Closed unmerged 2026-06-11T15:00:24Z; superseded duplicate closeout attempt; head not on `main`. |
| #474 | closed | yes | Merged 2026-06-11T15:00:00Z by the operator; squash commit `a0d53f7` carried the closeout packet onto `main`. The merged repair packet records that #474 was merged by mistake because it did not align the release-gate closeout path. |
| #475 | closed | no | Closed unmerged 2026-06-11T15:00:25Z; it was the corrected closeout replacement and explicitly recorded both #473 and #474 as superseded; its gate-path fix was ported onto `main` by #476. |
| #476 | closed | yes | Merged 2026-06-11T15:29:35Z; gate-path repair lane (`...MERGED-CLOSEOUT-GATE-PATH-REPAIR-001`) that diagnosed the mistake, ported the #475 alignment, and recorded the deterministic full-root gate proof. Current `main` tip `12f7503` is its squash commit. |

## Cleanup state

`resolved_and_recorded_on_main`. No duplicate closeout PR remains open. The
duplicate set (#473, #474, #475) is fully adjudicated on `main`: one merged
carrier of the closeout content (#474), two closed unmerged duplicates
(#473, #475), and a merged repair (#476) that records the diagnosis and
restores a single consistent, gate-recognized closeout.

## Deviation from this lane's stated prerequisite

This lane's charter expected #475 merged and #473/#474 closed without merge
or explicitly recorded as superseded. The live state is role-swapped: #474
is the merged PR and #475 is closed unmerged. The prerequisite is treated as
satisfied through its explicit-record branch, because:

- the closeout content and the #475 gate-path correction are both on
  current `main` (#474 plus #476);
- the supersession and the merge mistake are explicitly recorded on `main`
  in the merged repair packet (`mistake-summary.md`,
  `live-pr-state-reviewed.md`);
- the closeout final status, the deterministic gate proof, and the selected
  next lane (this lane) are all recorded on `main` and were re-verified live
  by this lane (`checks-run.md`).

No earlier evidence was recreated to resolve this deviation; it is recorded
here only.

## PR handling boundary

This lane did not approve, merge, close, reopen, or delete any PR or
branch; it only read live PR states.
