# Local LLM Solver Orchestration Smoke Retry 005 Import Final Decision

- Lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-MANUAL-SMOKE-RETRY-005-IMPORT-FINAL-DECISION-001`
- Source artifact path: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-005-source-artifact-qwen25-3b-after-retry-004-observed-failure-fix/`
- Primary artifact: `docs/evals/runs/20260606-alpha-local-llm-solver-orchestration-manual-smoke-retry-005-source-artifact-qwen25-3b-after-retry-004-observed-failure-fix/manual-smoke-redacted-output.json`
- Final decision: `MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_005_FAIL_REQUIRES_FIX`
- Selected next lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-005-OBSERVED-FAILURE-FIX-001`

This import is limited to one repo-preserved manual local solver orchestration smoke retry 005 artifact. It is not local model quality evidence, hosted provider evidence, /v1/solve readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, broad runtime readiness evidence, or billing evidence.

## Integrity check result

Decision support status: `COMPLETE_ENOUGH_TO_INTERPRET`.

| Check | Observed value | Result |
|---|---|---|
| Source artifact folder exists | yes | pass |
| Redacted JSON exists | yes | pass |
| Redacted JSON parseable | yes | pass |
| Command provenance exists | yes | pass |
| Python script provenance exists | yes | pass |
| Manual command exists | yes | pass |
| Manual runner exists | yes | pass |
| Exit status file exists | yes | pass |
| Stdout file exists | yes | pass |
| Stderr file exists | yes | pass |
| Repo status file exists | yes | pass |
| Exit status | `0` | pass |
| Result count | `5` | pass |
| Every prompt outer status | `completed` | pass |
| Every prompt error | `null` | pass |
| Repo head recorded | `42605eedef63f09e73d002976d9cba744213dc62` | pass |
| Script checksum recorded | `c008ba0efcf570adf5686a9144b6166ec1803fbf27053b19e48dd8ec200ccee7` | pass |
| Command provenance recorded | yes | pass |
| Provider key presence booleans | all false | pass |
| Full environment dump present | no; only safe env summary is preserved | pass |
| Endpoint summary | `http://127.0.0.1:<PORT>/<PATH>` | pass |
| Endpoint class | loopback summary | pass |
| Model | `qwen2.5:3b` | pass |
| Timeout | `60` | pass |
| `behavior_evidence` | `false` | pass |
| `no_hosted_fallback` | `true` | pass |
| `no_provider_keys_required` | `true` | pass |

## Interpretation boundary

Exit status `0` means only that the smoke runner completed and captured outputs. It does not establish that the prompt-level smoke expectations passed.
