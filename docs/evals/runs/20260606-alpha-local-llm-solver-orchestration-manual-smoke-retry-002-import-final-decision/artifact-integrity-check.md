# Artifact Integrity Check

## Required file presence and parseability

| Check | Result | Evidence |
| --- | --- | --- |
| Source artifact folder exists | PASS | `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-002-source-artifact-qwen25-3b-after-clarify-assumption-high-risk-fix/` is present. |
| `manual-smoke-redacted-output.json` exists | PASS | File is present. |
| `manual-smoke-redacted-output.json` is parseable JSON | PASS | Parsed successfully with Python `json.load`. |
| `command-provenance.txt` exists | PASS | File is present. |
| `python-script-provenance.json` exists | PASS | File is present. |
| `manual-smoke-command.sh` exists | PASS | File is present. |
| `manual-smoke-runner.py` exists | PASS | File is present. |
| `manual-smoke-runner.exit-status.txt` exists | PASS | File is present. |
| `manual-smoke-runner.stdout.txt` exists | PASS | File is present. |
| `manual-smoke-runner.stderr.txt` exists | PASS | File is present. |
| `repo-status.txt` exists | PASS | File is present. |

## Required artifact facts

| Check | Result | Recorded value |
| --- | --- | --- |
| Exit status is `0` | PASS | `0` |
| Result count is `5` | PASS | JSON contains five results; stdout records `"result_count": 5`. |
| Repo head is recorded | PASS | `bd2b83bfdc32f19ae752a4d0c13b6c15a06f32fe` |
| Script checksum is recorded | PASS | `fa0aba84cf450b958107d965e70d44d04d995b45b2b774eb9bda37babf43c9e0` |
| Command provenance is recorded | PASS | `command_provenance` object and `command-provenance.txt` are present. |
| Provider key presence booleans are all false | PASS | `ANTHROPIC_API_KEY=false`, `DEEPSEEK_API_KEY=false`, `GEMINI_API_KEY=false`, `GOOGLE_API_KEY=false`, and `OPENAI_API_KEY=false`. |
| Full environment dump absent | PASS | Provenance note records that a full environment dump was omitted; only safe environment summaries are present. |
| Endpoint summary is loopback | PASS | `http://127.0.0.1:<PORT>/<PATH>` and result metadata record `endpoint_is_loopback=true` / `endpoint_host_label=loopback`. |
| Model is `qwen2.5:3b` | PASS | `qwen2.5:3b` |
| Timeout is `60` | PASS | Top-level timeout is `60`; result metadata records `60.0`. |
| `behavior_evidence` is `false` | PASS | Top-level and result-level records use `false`. |
| `no_hosted_fallback` is `true` | PASS | Top-level and result-level records use `true`. |
| `no_provider_keys_required` is `true` | PASS | Top-level and result-level records use `true`. |

## Integrity conclusion

The preserved retry 002 artifact is complete and interpretable for this import lane. Because required artifact and provenance checks pass, the final decision is not blocked/incomplete. Prompt behavior interpretation determines whether the retry 002 artifact passes narrowly or requires a fix.
