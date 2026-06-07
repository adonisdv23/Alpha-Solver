# Checks run

## Repository/source inspection checks

- `sed -n '1,220p' AGENTS.md`
- `sed -n '1,240p' .specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`
- `sed -n '1,240p' .specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md`
- `rg -n "missing_information_too_broad|assumption_gate|answer_with_assumptions|clarify|pass_two|risk_flag" alpha/local_llm/orchestration_runner.py tests/test_local_llm_solver_orchestration_runner.py`
- `nl -ba alpha/local_llm/orchestration_runner.py | sed -n '663,916p'`
- `nl -ba tests/test_local_llm_solver_orchestration_runner.py | sed -n '1494,1567p'`
- `find docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-diagnostic-router-reset docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-source-artifact-qwen25-3b-after-diagnostic-router-reset docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-import-final-decision -maxdepth 2 -type f | sort`
- `sed -n '1,240p' docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-import-final-decision/final-decision.md`
- `sed -n '1,240p' docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-import-final-decision/smoke-retry-007-result-log.md`
- `python - <<'PY' ... parse manual-smoke-redacted-output.json and print prompt gate traces ... PY`
- `git log --oneline --decorate --all --max-count=30`

## Validation checks

- `git diff --cached --name-only`
- `git diff --cached --name-only | python - <<'PY' ... confirm only required docs directory changed ... PY`
- `git diff --cached --check`
- `python - <<'PY' ... confirm no source/test/runtime/provider/dashboard/API files changed ... PY`
- `python - <<'PY' ... confirm exactly one primary classification and exactly one selected next lane ... PY`
- `python - <<'PY' ... confirm no local model, hosted provider, or smoke rerun evidence introduced by this packet ... PY`

## Runtime/model call confirmations

No local model call was made. No hosted provider call was made. No smoke rerun occurred. No Google Sheets update was made.
