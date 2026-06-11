# Checks run

This file records the required checks for the closeout lane. Final command outputs were refreshed after the packet and tests were added.

## Required checks

```bash
git status --short
```

Result: pass. The command showed only the allowed runbook correction file, the new closeout packet directory, and the new guardrail test file as changed.

```bash
git diff --name-only
```

Result: pass. Changed paths were within the allowed file list.

```bash
git diff --check
```

Result: pass. No whitespace errors were reported.

```bash
python -m pytest -q tests/test_self_operator_closeout_guardrails.py
```

Result: pass. The focused closeout guardrail test file passed.

```bash
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails
```

Result: pass. Packet consistency passed for one packet directory.

```bash
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|autonomous|MVP ready|release ready|broad user ready|/v1/solve|deployment|billing|credential|secret|provider call|hosted model" docs alpha scripts tests
```

Result: pass. Hits were reviewed in `forbidden-claim-scan-results.md`; final scan decision is `pass`.

```bash
rg -n "approval identity|run_id|scope identity|requested_action|fails closed|mismatch|metadata.run_id" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md alpha/self_operator/execution_gate.py
```

Result: pass. The focused runbook/implementation wording check confirmed that the canonical runbook now describes comparable-value enforcement and the proposed-task metadata limitation.

## Additional prerequisite checks

```bash
git show -s --format='%H %D%n%s' HEAD
```

Result: pass. HEAD is `bbc856aa7d038a332a5ec0549866d06d7f08a0fa`, subject `docs(self-operator): finalize runbook and boundary review (#472)`, confirming PR #472 content is present on current `main` checkout.

```bash
for p in docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-runbook-finalization-and-boundary-review docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply; do test -e "$p" && echo "EXISTS $p" || echo "MISSING $p"; done
```

Result: pass. All three prerequisite artifacts existed before edits.

## Non-execution confirmations

- No runtime behavior was changed.
- No source evidence was mutated.
