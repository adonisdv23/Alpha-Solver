# Live PR state reviewed

Reviewed via the GitHub API on 2026-06-11 before any edit in this lane.

| PR | State | Merged | Evidence |
| --- | --- | --- | --- |
| #473 | closed | no | `state: closed`, `merged: false`, `closed_at: 2026-06-11T15:00:24Z`; head `b362a957e45c6490e29d430865e83f6d38040ab0` (`codex/create-pr-for-self-operator-closeout`) is not on `main`. |
| #474 | closed | yes | `state: closed`, `merged: true`, `merged_at: 2026-06-11T15:00:00Z`, merged by `adonisdv23`; squash commit `a0d53f7` is the current `main` tip. |
| #475 | closed | no | `state: closed`, `merged: false`, `closed_at: 2026-06-11T15:00:25Z`; head `bdde23ec9991d564babba8cb576bd1974d56a2cf` (`claude/self-operator-release-closeout-3zqql9`) is not on `main`. |

All three PRs targeted base `main` at
`bbc856aa7d038a332a5ec0549866d06d7f08a0fa` (#472 merged).

## Confirmations required by this lane

- Current `main` includes PR #474: confirmed (`a0d53f7` = squash merge of #474).
- PR #473 is closed and unmerged: confirmed.
- PR #475 is closed and unmerged: confirmed.

## Why this repair is not based on the #475 branch

The #475 branch was treated as the source reference only. It cannot be
cleanly rebased onto current `main`: #474 (now on `main`) and #475 both
created `tests/test_self_operator_closeout_guardrails.py` and overlapping
files under the `...-release-closeout-and-final-guardrails/` packet with
different content, which guarantees rebase conflicts. Per the lane charter,
this repair was developed on a new branch from current `main`
(`claude/loving-franklin-mdjgb1`), porting the missing #475 corrections.

## PR handling boundary

This lane did not approve, merge, close, reopen, or delete any PR or branch;
it only read their live states.
