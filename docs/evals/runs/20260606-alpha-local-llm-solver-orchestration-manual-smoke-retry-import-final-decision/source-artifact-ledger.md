# Source Artifact Ledger

## Imported artifact

- Source artifact directory: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-source-artifact-qwen25-3b-after-pass-one-fix/`
- Primary artifact: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-source-artifact-qwen25-3b-after-pass-one-fix/manual-smoke-redacted-output.json`
- Retry context: preserved manual smoke retry artifact for `qwen2.5:3b` after the pass-one gating fix.
- Prior imported final decision for comparison: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-import-final-decision/`

## Preserved files inspected

| File | Status | Notes |
| --- | --- | --- |
| `manual-smoke-redacted-output.json` | Present | Primary redacted JSON output parsed for interpretation. |
| `command-provenance.txt` | Present | Records safe command provenance and provider key presence booleans. |
| `python-script-provenance.json` | Present | Records executed runner path, byte count, and SHA-256. |
| `manual-smoke-command.sh` | Present | Preserved command wrapper. |
| `manual-smoke-runner.py` | Present | Preserved executed runner script. |
| `manual-smoke-runner.exit-status.txt` | Present | Records exit status `0`. |
| `manual-smoke-runner.stdout.txt` | Present | Records summarized runner completion output. |
| `manual-smoke-runner.stderr.txt` | Present | Present and empty. |
| `repo-status.txt` | Present | Records source-environment git status at artifact capture time. |

## Recorded provenance values

- Repo head recorded in artifact: `f7047a63ee07d0d14b7a9a47e6befe80a03e77fd`
- Executed script SHA-256 recorded in artifact: `206c6aad2a7c1d5b4ba84e26d29661c8735ece3946377cc99ca0262305a550c6`
- Command provenance recorded: yes, in both top-level JSON and `command-provenance.txt`.
- Safe environment summary recorded: `ALPHA_LOCAL_LLM_ENABLED=true`, `ALPHA_LOCAL_LLM_ENDPOINT_SUMMARY=http://127.0.0.1:<PORT>/<PATH>`, `ALPHA_LOCAL_LLM_MODEL=qwen2.5:3b`, `ALPHA_LOCAL_LLM_TIMEOUT_SECONDS=60`.
- Provider key presence booleans: `ANTHROPIC_API_KEY=false, DEEPSEEK_API_KEY=false, GEMINI_API_KEY=false, GOOGLE_API_KEY=false, OPENAI_API_KEY=false`.

## Ledger boundary

This ledger records only preserved repository artifacts. It does not reconstruct outputs, rerun the smoke, call a local model, call a hosted provider, update Google Sheets, or broaden the evidence boundary.
