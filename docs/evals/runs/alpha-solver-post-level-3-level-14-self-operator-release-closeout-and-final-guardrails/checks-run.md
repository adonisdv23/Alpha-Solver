# Checks run

All commands were run from the repo root on 2026-06-11, after this lane's
edits. Results recorded after the final green run.

## Repository state checks

```bash
git status --short
git diff --name-only
git diff --check
```

Result: only this lane's allowed files changed (`alpha/self_operator/release_gate.py`,
`tests/test_self_operator_release_gate.py`,
`tests/test_self_operator_closeout_guardrails.py`, the runbook section 5
correction, and this packet directory); no whitespace errors.

## Focused test suites

```bash
python -m pytest -q tests/test_self_operator_closeout_guardrails.py
python -m pytest -q tests/test_self_operator_release_gate.py
python -m pytest -q tests/test_self_operator_execution_gate.py
```

Result: pass (the execution-gate suite was run as well because the runbook
correction documents that gate's behavior; the gate's code is unchanged).

## Packet consistency

```bash
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails
```

Result: pass.

## Deterministic forbidden-claim scan

```bash
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|autonomous|MVP ready|release ready|broad user ready|/v1/solve|deployment|billing|credential|secret|provider call|hosted model" docs alpha scripts tests
```

Result: every hit reviewed and classified in
`forbidden-claim-scan-results.md`; zero `forbidden_claim` hits; decision
`pass`.

## Focused runbook/implementation wording check

```bash
rg -n "approval identity|run_id|scope identity|requested_action|fails closed|mismatch|metadata.run_id" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-mvp-runbook-finalization/mvp-operator-runbook.md alpha/self_operator/execution_gate.py
```

Result: reviewed; the corrected section 5 wording matches the
implementation's comparable-fields behavior, and the implementation's
proposed-task identity helpers contain no `requested_action` fallback.

## Post-closeout release gate (full root)

```bash
python scripts/check_self_operator_release_gate.py \
  --repo-root . \
  --output docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-closeout-and-final-guardrails/post-closeout-release-gate-report.json
```

Result: exit 0; `release_closeout_review_complete: pass`; final status
`eligible_for_release_closeout_review` (see
`post-closeout-release-gate-report.md`).
