# Checks run

All commands run from the repo root on branch `claude/sharp-cori-4qempe`
(based on `main` `fd568aa`). Note: in this environment `pytest` is provided
by a uv tool install, so `python -m pytest` is invoked through that tool's
interpreter; the module/arguments are identical to
`python -m pytest -q tests/test_self_operator_acceptance_interpretation.py`.

## Prerequisite checks (read-only, before any edit)

```text
$ git fetch origin main && git rev-parse HEAD origin/main
fd568aaf50aa143aa55878430c30b8f5fe2d38cd
fd568aaf50aa143aa55878430c30b8f5fe2d38cd

# PR #469: GitHub API -> state=closed, merged=true, merged_at=2026-06-10T22:54:35Z, base=main

$ git ls-tree origin/main -- docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-expected-safety-block-operator-review/operator-decision.json
100644 blob 879fb6b7531e17baf244a6bb049b33db83952ec9  ...accepted-import-summary.json
100644 blob a3d1864f05fc29251c1547a7d5e3f916ec024841  ...operator-decision.json

# Decision-unaware baseline (output to /tmp, read-only; matches #468):
$ python scripts/interpret_self_operator_acceptance.py --import-summary ...accepted-import-summary.json --output /tmp/baseline-interpretation.json
interpretation=blocked tasks=10 defects=2 p0=0 p1=2 non_claim='does not claim MVP readiness'
(exit 1; defects: P1 MLA-006 EXPECTED_SAFETY_BLOCK_UNCONFIRMED, P1 MLA-007 EXPECTED_SAFETY_BLOCK_UNCONFIRMED)
```

## Required git checks (after edits, before commit)

```text
$ git status --short
 M alpha/self_operator/acceptance_interpretation.py
 M scripts/interpret_self_operator_acceptance.py
 M tests/test_self_operator_acceptance_interpretation.py
?? docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-operator-decision-interpretation-apply/

$ git diff --name-only
alpha/self_operator/acceptance_interpretation.py
scripts/interpret_self_operator_acceptance.py
tests/test_self_operator_acceptance_interpretation.py

$ git diff --check
(no output; clean)
```

## Focused tests

```text
$ python -m pytest -q tests/test_self_operator_acceptance_interpretation.py
.................................                                        [100%]
(33 passed: 21 pre-existing unchanged + 12 new operator-decision tests)

$ python -m pytest -q tests/test_self_operator_release_gate.py tests/test_self_operator_result_import.py tests/test_self_operator_import_blocker_triage.py
..........................................                               [100%]
(42 passed; neighboring self-operator suites unaffected)
```

## Interpretation command (this lane's apply run)

```text
$ python scripts/interpret_self_operator_acceptance.py \
    --import-summary docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json \
    --operator-decision docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-expected-safety-block-operator-review/operator-decision.json \
    --output docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-operator-decision-interpretation-apply/interpretation-result.json
interpretation=eligible_for_later_release_review tasks=10 defects=0 p0=0 p1=0 operator_decision=consumed confirmation_type=operator_ledger_level_acceptance machine_readable_artifact_confirmation=false non_claim='does not claim MVP readiness'
(exit 0)
```

## Determinism check

```text
# command re-run; outputs byte-identical
$ diff run1.json interpretation-result.json
(no output)
$ sha256sum run1.json interpretation-result.json
dd3385e97239ddbd3b8829b409faaf73895ea28ccc1d646fe0d69a4e0e3c7dd6  (both)
```

## Source non-mutation proof

```text
$ sha256sum docs/evals/runs/alpha-solver-post-level-3-level-13-self-operator-import-blocker-resolution-and-accepted-import/accepted-import-summary.json
a54ebd46e8533b17738b302e6177b282348f811d7f6b694f75bea7ba2cf8285c  (matches #467/#468/#469 recorded baseline)
$ sha256sum docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-expected-safety-block-operator-review/operator-decision.json
db074b7b15b7b8cf5bd9636cbede0ed37ec447e8397a9a8ef2af0729ebacb30e  (unchanged)
# git status shows no modification under any existing docs/evals/runs packet
```

## Packet consistency

```text
$ python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-13-to-level-14-self-operator-operator-decision-interpretation-apply
Local LLM packet consistency check passed (1 packet directories scanned).

$ python scripts/check_local_llm_packet_consistency.py
Local LLM packet consistency check passed (118 packet directories scanned).
```

## Not run (by lane rule)

- Release gate (`alpha/self_operator/release_gate.py` / release-gate lane
  checks): forbidden in this lane and not invoked.
