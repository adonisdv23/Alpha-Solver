# Artifact Integrity Check

## Method

This check parses only the repo-preserved source artifact at `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-003-source-artifact-qwen25-3b-after-boundary-guard-assumption-path-fix/manual-smoke-redacted-output.json` and reads the adjacent provenance/status files in `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-003-source-artifact-qwen25-3b-after-boundary-guard-assumption-path-fix/`. The runner was not rerun.

## Integrity checklist

| Check | Result |
| --- | --- |
| source artifact folder exists | PASS |
| manual-smoke-redacted-output.json exists and is parseable JSON | PASS |
| command-provenance.txt exists | PASS |
| python-script-provenance.json exists | PASS |
| manual-smoke-command.sh exists | PASS |
| manual-smoke-runner.py exists | PASS |
| manual-smoke-runner.exit-status.txt exists | PASS |
| manual-smoke-runner.stdout.txt exists | PASS |
| manual-smoke-runner.stderr.txt exists | PASS |
| repo-status.txt exists | PASS |
| exit status is 0 | PASS |
| result count is 5 | PASS |
| every prompt record has outer status completed | PASS |
| every prompt record has error null | PASS |
| repo head is recorded | PASS |
| script checksum is recorded | PASS |
| command provenance is recorded | PASS |
| provider key presence booleans are all false | PASS |
| no full environment dump is present | PASS |
| endpoint summary is loopback | PASS |
| model is qwen2.5:3b | PASS |
| timeout is 60 | PASS |
| behavior_evidence is false | PASS |
| no_hosted_fallback is true | PASS |
| no_provider_keys_required is true | PASS |

## Prompt-level completion review

The non-blocking review note from PR #343 is addressed here by not relying only on `manual-smoke-runner.exit-status.txt`. The import also verifies every prompt-level outer `status` and prompt-level `error` field.

| Prompt | Outer status | Error |
| --- | --- | --- |
| `01-simple-direct-answer` | `completed` | `null` |
| `02-ambiguous-clarify` | `completed` | `null` |
| `03-answer-with-assumptions` | `completed` | `null` |
| `04-high-risk-block` | `completed` | `null` |
| `05-boundary-claim-guard` | `completed` | `null` |

## Integrity conclusion

The artifact is complete and interpretable. The command exit status is `0`, but the final decision is based on prompt-level status/error checks plus expected behavior checks, not on exit status alone.
