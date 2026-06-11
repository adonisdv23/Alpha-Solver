# Checks run

## Release-gate checker

```bash
python scripts/check_self_operator_release_gate.py \
  --repo-root . \
  --output docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply/release-gate-report.json
```

- First run (pre-fix): exit 1, `final_status: blocked_release_closeout_not_reviewed`,
  `earliest_missing_gate: p0_p1_defects_absent` — false positive, see
  `release-gate-report.md`.
- Final run (post-fix): exit 1, `final_status: blocked_missing_runbook_finalization`,
  `earliest_missing_gate: mvp_runbook_finalized_or_updated`.
- Determinism: run twice post-fix; byte-identical JSON output
  (sha256 `69674953f6c4ac776b6ec85431c64644adad3a535b27b0f56e040c3179e85242`).
- The non-zero exit is the checker's contract for any `blocked_*` final
  status and is the expected outcome of this lane, not a tooling failure.

## Focused tests (code changed)

```bash
python -m pytest -q tests/test_self_operator_release_gate.py
```

Result: 13 passed (12 pre-existing + 1 new regression test
`test_backticked_severity_vocabulary_does_not_block`).

## Required git checks

```bash
git status --short
```

```
 M alpha/self_operator/release_gate.py
 M tests/test_self_operator_release_gate.py
?? docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply/
```

```bash
git diff --name-only
```

```
alpha/self_operator/release_gate.py
tests/test_self_operator_release_gate.py
```

```bash
git diff --check
```

Result: clean (exit 0, no whitespace errors).

## Packet consistency

```bash
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-release-gate-apply
```

Result: `Local LLM packet consistency check passed (1 packet directories scanned).`
(exit 0).
