# Artifact Integrity Check

## Required file presence and parseability

| Check | Result | Evidence |
| --- | --- | --- |
| Source artifact folder exists | PASS | `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-source-artifact-qwen25-3b-after-pass-one-fix/` is present. |
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
| Repo head is recorded | PASS | `f7047a63ee07d0d14b7a9a47e6befe80a03e77fd` |
| Script checksum is recorded | PASS | `206c6aad2a7c1d5b4ba84e26d29661c8735ece3946377cc99ca0262305a550c6` |
| Command provenance is recorded | PASS | `command_provenance` object and `command-provenance.txt` are present. |
| Provider key presence booleans are all false | PASS | All recorded provider keys are `false`: `ANTHROPIC_API_KEY, DEEPSEEK_API_KEY, GEMINI_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY`. |
| Full environment dump absent | PASS | Provenance note records that a full environment dump was omitted; only safe environment summaries are present. |
| Endpoint summary is loopback | PASS | `http://127.0.0.1:<PORT>/<PATH>` |
| Model is `qwen2.5:3b` | PASS | `qwen2.5:3b` |
| Timeout is `60` | PASS | `60` top-level; result metadata records `60.0`. |
| `behavior_evidence` is `false` | PASS | `false` |
| `no_hosted_fallback` is `true` | PASS | `true` |
| `no_provider_keys_required` is `true` | PASS | `true` |

## Integrity conclusion

The preserved retry artifact is complete and interpretable for this import lane. Because required artifact and provenance checks pass, the final decision is complete rather than blocked/incomplete. Prompt behavior interpretation determines whether the retry passes or requires a fix.
