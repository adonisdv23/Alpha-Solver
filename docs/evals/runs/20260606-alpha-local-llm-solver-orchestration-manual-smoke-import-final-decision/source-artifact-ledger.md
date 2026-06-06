# Source Artifact Ledger

## Imported source artifact

- Source artifact directory: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-source-artifact-qwen25-3b/`
- Primary redacted output: `manual-smoke-redacted-output.json`
- Command provenance: `command-provenance.txt`
- Python script provenance: `python-script-provenance.json`
- Preserved command script: `manual-smoke-command.sh`
- Preserved runner script: `manual-smoke-runner.py`
- Exit status: `manual-smoke-runner.exit-status.txt`
- Captured stdout: `manual-smoke-runner.stdout.txt`
- Captured stderr: `manual-smoke-runner.stderr.txt`
- Preserved repo status: `repo-status.txt`

## Recorded top-level artifact facts

- Manual smoke target: `alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration`
- Required provider mode: `local_llm`
- Expected orchestration mode: `non_production_local_solver_orchestration`
- Expected strategy: `local_expert_two_pass`
- Model: `qwen2.5:3b`
- Timeout: `60`
- Local endpoint summary: `http://127.0.0.1:<PORT>/<PATH>`
- Result count: `5`
- Behavior evidence: `false`
- No hosted fallback: `true`
- No provider keys required: `true`

## Provenance recorded by source artifact

- Repo head recorded in the source artifact: `173abd2a36aa981cac1d1b4c169f085069c158f5`
- Script SHA-256 recorded in the source artifact: `c7d9bc8b2e6de71adb885b7e5f9f4e180db5626c7455bcb55a7608d4d465a412`
- Script byte count recorded in the source artifact: `9185`
- Command provenance records no full environment dump and only safe environment summaries.
- Provider key presence booleans in the source artifact are all `false` for `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`, and `DEEPSEEK_API_KEY`.

## Preservation statement

This lane did not rerun the smoke, call a local model, call a hosted provider, reconstruct output, update Google Sheets, or modify source/test/runtime/provider/dashboard files. Interpretation is based only on repo-preserved artifacts.
