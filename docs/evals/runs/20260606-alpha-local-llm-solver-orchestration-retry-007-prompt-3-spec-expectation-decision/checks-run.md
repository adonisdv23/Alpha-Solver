# Checks run

## Repository inspection commands

- `find .. -name AGENTS.md -print`
- `git status --short --branch`
- `git branch --show-current`
- `sed -n '1,220p' AGENTS.md`
- `rg -n "missing_information_too_broad|answer_with_assumptions|clarify|bounded|Prompt 3|prompt 3|expectation mismatch|spec review" .specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md .specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md alpha/local_llm/orchestration_runner.py tests/test_local_llm_solver_orchestration_runner.py docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-diagnostic-router-reset docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-007-import-final-decision docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-retry-007-diagnostic-classification`
- `rg -n "def _assumption_gate_failed_reason_codes|missing_information_too_broad|bounded_local_python_cli_startup_plan|shape_answer_with_assumptions|blocked_assumption_gate_failed|def _apply_gate" alpha/local_llm/orchestration_runner.py .specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md .specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md tests/test_local_llm_solver_orchestration_runner.py`
- `sed -n '650,920p' alpha/local_llm/orchestration_runner.py`
- `sed -n '1230,1620p' tests/test_local_llm_solver_orchestration_runner.py`
- `rg -n "missing-information|missing information|missing_information|assumption|answer_with_assumptions|clarify|block|fail closed|fail-closed|bounded" .specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md .specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`
- `find docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-retry-007-diagnostic-classification -maxdepth 1 -type f -print | sort`

## Scope and decision checks

- `git diff --name-only`
- `git diff --cached --name-only`
- `python - <<'PY' ... confirm staged changed files are limited to the required Prompt 3 decision docs path ... PY`
- `python - <<'PY' ... confirm exactly one decision path and exactly one selected next lane ... PY`
- `python - <<'PY' ... confirm no forbidden runtime/source/test/provider/dashboard/API files changed in staged changes ... PY`
- `git diff --cached --check`

## Non-execution confirmations

- No local model command was run.
- No hosted provider command was run.
- No smoke command was run.
