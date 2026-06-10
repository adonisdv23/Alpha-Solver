# Checks run

All commands run from the repository root on branch
`claude/kind-franklin-67fe2d` (based on `main` commit `837b988`, which contains
merged PRs #465, #466, and #467).

## Always-run scope checks

```
$ git status --short
?? docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-acceptance-interpretation-blocker-fix-retry/

$ git diff --name-only
(empty — no tracked file modified)

$ git diff --check
(clean)
```

The only change in the working tree is this new packet directory. No tracked
file (code, test, fixture, script, or existing packet) was modified.

## Verification interpretation (read-only; unchanged accepted import)

Run because this lane needed a machine-readable record of the current blocker
state. The input is the **unchanged** #465 accepted import summary (no
corrected import summary exists in this lane); the output is written only into
this packet. This is not the release gate, and the release gate was not run.

```
$ python scripts/interpret_self_operator_acceptance.py \
    --import-summary docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json \
    --output docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-acceptance-interpretation-blocker-fix-retry/verification-interpretation-result.json
interpretation=blocked tasks=10 defects=2 p0=0 p1=2 non_claim='does not claim MVP readiness'
(exit code 1 — the documented blocked exit; expected)
```

Defects reported (exactly the routed group, nothing else):

```
P1 EXPECTED_SAFETY_BLOCK_UNCONFIRMED MLA-006 — Expected safety block is not confirmed by the import summary.
P1 EXPECTED_SAFETY_BLOCK_UNCONFIRMED MLA-007 — Expected safety block is not confirmed by the import summary.
```

Determinism rerun to a scratch path was byte-identical:

```
$ python scripts/interpret_self_operator_acceptance.py --import-summary <same> --output /tmp/verify-rerun.json
interpretation=blocked tasks=10 defects=2 p0=0 p1=2 non_claim='does not claim MVP readiness'  (exit 1)
$ cmp /tmp/verify-rerun.json .../verification-interpretation-result.json
byte-identical
```

## Source non-mutation proof

```
$ sha256sum docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json
a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c
```

Identical before and after this lane, and identical to the baseline recorded in
#467's packet.

## Conditional checks (run read-only as verification; no code changed)

The importer and interpretation engine were not changed, so these runs are
verification of current `main` behavior, not regression gates for a change:

```
$ python -m pytest -q tests/test_self_operator_result_import.py
19 passed

$ python -m pytest -q tests/test_self_operator_acceptance_interpretation.py
21 passed
```

## Packet consistency

```
$ python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-acceptance-interpretation-blocker-fix-retry
Local LLM packet consistency check passed (1 packet directories scanned).

$ python scripts/check_local_llm_packet_consistency.py
Local LLM packet consistency check passed (116 packet directories scanned).
```

## Checks intentionally not run

- `scripts/import_self_operator_acceptance_results.py` — not run: importer
  unchanged, classification is `operator_review_needed`, and a re-import would
  duplicate the accepted #465 output byte-for-byte without confirming anything.
- `scripts/check_self_operator_release_gate.py` (release gate) — not run:
  forbidden in this lane, and P1 blockers remain open.

## Environment note

`pytest` was not preinstalled on this environment's default interpreter and was
installed for the read-only verification runs above; this installed nothing
into the repository.
