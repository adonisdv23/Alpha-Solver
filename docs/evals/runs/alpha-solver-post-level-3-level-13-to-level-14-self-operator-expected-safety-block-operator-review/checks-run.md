# Checks run

All commands run from the repository root on branch
`claude/amazing-lovelace-ybhdq9` (based on `main` commit `8248308`, which
contains merged PRs #465, #466, #467, and #468; `origin/main` fetched and
identical to the baseline, 0/0 divergence).

## Always-run scope checks

Run after all packet files except this one were written:

```
$ git status --short
?? docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-expected-safety-block-operator-review/

$ git diff --name-only
(empty — no tracked file modified; exit 0)

$ git diff --check
(clean; exit 0)
```

The only change in the working tree is this new packet directory. No tracked
file (code, test, fixture, script, or existing packet) was modified. This
file (`checks-run.md`) was added to the same untracked packet directory after
these checks ran, which does not change their result.

## Packet consistency

```
$ python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-expected-safety-block-operator-review
Local LLM packet consistency check passed (1 packet directories scanned).
(exit 0)

$ python scripts/check_local_llm_packet_consistency.py
Local LLM packet consistency check passed (117 packet directories scanned).
(exit 0)
```

Both runs were repeated after this `checks-run.md` was added; results
unchanged (pass, exit 0).

## Decision-artifact validity

```
$ python -m json.tool docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-expected-safety-block-operator-review/operator-decision.json > /dev/null
operator-decision.json: valid JSON
```

`operator-decision.json` is a static, deterministic record: no timestamps, no
environment-dependent values.

## Source non-mutation proof

```
$ sha256sum docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json
a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c
```

Identical before and after this lane, and identical to the baseline recorded
in the #467 and #468 packets.

## Checks intentionally not run

- `python -m pytest` — not run: docs-only lane, no code changed, and code
  changes are forbidden in this lane.
- `scripts/interpret_self_operator_acceptance.py` — not run: interpretation
  (including any retry) is forbidden in this lane; consumption of the
  decision artifact belongs to the selected next lane.
- `scripts/import_self_operator_acceptance_results.py` — not run: importer
  unchanged; no re-import is part of this lane.
- `scripts/check_self_operator_release_gate.py` (release gate) — not run:
  forbidden in this lane, and P1 blockers remain open in the machine-readable
  record.
