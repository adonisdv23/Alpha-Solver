# Checks run

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | Passed | Showed only allowed helper, test, fixture, docs packet, and package-registration changes. |
| `git diff --name-only` | Passed | Before staging, tracked output showed `pyproject.toml`; untracked allowed files were visible in `git status --short`. |
| `git diff --check` | Passed | No whitespace errors. |
| GitHub `tests / test` workflow: `Lint (ruff only)` | Failed before lint fix | The workflow command `pip install ruff==0.5.7` then `ruff check alpha` reported `F401` for unused `typing.Sequence` in `alpha/self_operator/preflight.py`. |
| `ruff check alpha` | Passed after lint fix | Re-ran with `ruff 0.5.7`; all checks passed after removing the unused import. Evidence boundary unchanged. |
| `python -m pytest -q tests/test_self_operator_artifact_schema.py tests/test_self_operator_artifact_store.py tests/test_self_operator_preflight.py tests/test_self_operator_command_classification.py` | Passed | 33 passed. |
| `python -m pytest -q tests/test_self_operator_static_guardrails.py tests/test_self_operator_approval_stopstate_static.py tests/test_self_operator_artifact_schema_static.py tests/test_self_operator_forbidden_behavior_static.py` | Passed | 16 passed. |
| `make check-local-llm-orchestration-guardrails` | Passed | Evidence-boundary, doc-path/link, and packet-consistency checks passed. |
| `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-11-self-operator-local-artifact-preflight-foundation` | Passed | 1 packet directory scanned. |
| `rg -n "stop if explicit operator confirmation is missing\|ALPHA-SOLVER-POST-LEVEL-3-LEVEL-11-SELF-OPERATOR-APPROVAL-RECORD-CODE-SCAFFOLD-001\|source-artifact mutation\|evidence promotion" docs tests` | Passed | Required text tokens were present. |
| `python -m pytest -q` | Failed | 5 failures outside this lane: three `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses[...]` failures expected `gpt-5` but observed `gpt-5-mini`; `tests/test_cost_tracking.py::test_cost_tracking` expected `artifacts/costs.csv` to exist; `tests/test_security.py::test_a3_1_prompt_subset_passes_solve_input_validation` expected monkeypatched `final_answer == "ok"` but received a rewritten release-note response. This full-suite run also exercised existing provider/API tests in the environment, which is outside the intended local-only lane boundary and is recorded here as a validation deviation rather than hidden. |

No acceptance execution was run. No new test performs network, provider, browser, deployment, billing, credential, or Google Sheets access; the provider/API activity came from existing full-suite tests invoked by the required full-suite command.
