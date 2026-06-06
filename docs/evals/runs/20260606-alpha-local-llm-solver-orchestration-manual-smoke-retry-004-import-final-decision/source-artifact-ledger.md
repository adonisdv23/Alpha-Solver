# Source Artifact Ledger

## Imported artifact set

| Item | Path | Import status |
| --- | --- | --- |
| Source directory | `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-004-source-artifact-qwen25-3b-after-retry-003-observed-failure-fix/` | Present |
| Redacted output | `manual-smoke-redacted-output.json` | Present and parseable |
| Command provenance | `command-provenance.txt` | Present |
| Python script provenance | `python-script-provenance.json` | Present and parseable |
| Smoke command | `manual-smoke-command.sh` | Present |
| Smoke runner | `manual-smoke-runner.py` | Present |
| Exit status | `manual-smoke-runner.exit-status.txt` | Present; value `0` |
| Runner stdout | `manual-smoke-runner.stdout.txt` | Present |
| Runner stderr | `manual-smoke-runner.stderr.txt` | Present |
| Repo status | `repo-status.txt` | Present |

## Preserved provenance facts

- Repo head in artifact: `e8b6b5aba3d1338b15893319702781e4d4070a8a`.
- Executed script checksum: `e05b510db4e03ea4d8732af98505d593b5e6a83615f4f23a9fb9ab35581cdb75`.
- Command provenance is present and records a safe, redacted environment summary rather than a full environment dump.
- Provider key presence booleans are all `false` for `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `GEMINI_API_KEY`, `GOOGLE_API_KEY`, and `OPENAI_API_KEY`.
- Endpoint summary is loopback: `http://127.0.0.1:<PORT>/<PATH>`.
- Model is `qwen2.5:3b`.
- Timeout is `60`.
- `behavior_evidence` is `false`.
- `no_hosted_fallback` is `true`.
- `no_provider_keys_required` is `true`.
