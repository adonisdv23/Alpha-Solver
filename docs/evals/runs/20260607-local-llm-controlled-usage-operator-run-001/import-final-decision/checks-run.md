# Checks Run

## Required checks

The following checks were run for this docs-only import/final-decision packet:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `python -m json.tool docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/source-artifact/cli_stdout.json >/tmp/alpha_cli_stdout_check.json`
- `cat docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/source-artifact/exit_code.txt`
- `rg "CONTROLLED_USAGE_OPERATOR_RUN_ACCEPTED_AS_LEVEL_2_OPERATOR_USABILITY_ARTIFACT" docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/import-final-decision`
- `rg "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CONTROLLED-USAGE-CLOSEOUT-001" docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/import-final-decision`
- `rg "ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CONTROLLED-USAGE-IMPORT-FINAL-DECISION-FIX-001" docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/import-final-decision`
- `rg "local model quality|benchmark evidence|production readiness|MVP readiness|provider-orchestration evidence|Alpha superiority|billing evidence|dashboard readiness|/v1/solve readiness|broad runtime readiness|evidence-model promotion" docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/import-final-decision`
- `git diff --name-only -- docs/evals/runs/20260607-local-llm-controlled-usage-operator-run-001/source-artifact`
- `git diff --name-only -- alpha tests`

## Non-actions

No local model inference, Ollama run, smoke rerun, hosted provider call, `/v1/solve` call, dashboard route call, provider fallback, hosted fallback, evidence promotion, Google Sheets update, or backlog workbook action was run.
