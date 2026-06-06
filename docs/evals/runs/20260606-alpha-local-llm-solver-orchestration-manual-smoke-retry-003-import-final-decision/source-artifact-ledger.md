# Source Artifact Ledger

## Source of truth references inspected

- `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`
- `.specs/LOCAL-LLM-SOLVER-ORCHESTRATION-001.md`
- `alpha/local_llm/provider_adapter.py`
- `alpha/local_llm/orchestration_runner.py`
- `tests/test_local_llm_solver_orchestration_runner.py`
- `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-boundary-guard-assumption-path-fix/`
- `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-003-source-artifact-qwen25-3b-after-boundary-guard-assumption-path-fix/`

## Imported artifact location

- Source artifact directory exists: yes.
- Primary JSON artifact: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-003-source-artifact-qwen25-3b-after-boundary-guard-assumption-path-fix/manual-smoke-redacted-output.json`.
- Import decision directory: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-003-import-final-decision/`.

## Source files present in preserved artifact directory

- `command-provenance.txt`
- `manual-smoke-command.sh`
- `manual-smoke-redacted-output.json`
- `manual-smoke-runner.exit-status.txt`
- `manual-smoke-runner.py`
- `manual-smoke-runner.stderr.txt`
- `manual-smoke-runner.stdout.txt`
- `python-script-provenance.json`
- `repo-status.txt`

## Recorded provenance values

- Repo head: `8a1973fd0727e47d0f706eadd504f2b4244c97de`
- Script checksum: `ed44356851081586098bd0e1ab4fe2860f604688853d1ac75e28e384a8cad0c4`
- Command provenance safe environment:
  - `ALPHA_LOCAL_LLM_ENABLED=true`
  - `ALPHA_LOCAL_LLM_ENDPOINT_SUMMARY=http://127.0.0.1:<PORT>/<PATH>`
  - `ALPHA_LOCAL_LLM_MODEL=qwen2.5:3b`
  - `ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=60`
- Provider key presence booleans:
  - `ANTHROPIC_API_KEY`: `false`
  - `DEEPSEEK_API_KEY`: `false`
  - `GEMINI_API_KEY`: `false`
  - `GOOGLE_API_KEY`: `false`
  - `OPENAI_API_KEY`: `false`

## Evidence handling

The import records only the preserved artifact's redacted output and provenance. It does not reconstruct output, call a local model, call a hosted provider, rerun the smoke, update Google Sheets, or modify runtime surfaces.
