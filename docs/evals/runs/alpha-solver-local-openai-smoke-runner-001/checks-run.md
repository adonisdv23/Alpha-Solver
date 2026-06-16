# Checks run

Implementation validation for `ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001`.

Initial implementation checks:

- `python -m pytest -q tests/test_operator_smoke_runner.py` passed with 7 tests.
- `python -m pytest -q tests/test_operator_smoke_runner.py tests/test_local_llm_provider_adapter.py::test_ollama_backend_rejects_non_local_endpoints_before_transport_invocation tests/providers/test_openai_provider.py::test_missing_openai_api_key_is_safe tests/providers/test_openai_provider.py::test_openai_api_key_can_come_from_environment` passed with 20 tests.
- `git diff --check` passed.
- `python scripts/check_narrative_claim_safety.py .specs/ALPHA-SOLVER-LOCAL-OPENAI-SMOKE-RUNNER-001.md .specs/INDEX.md docs/CURRENT_STATE.md docs/LANE_REGISTRY.md docs/EVIDENCE_INDEX.md docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/*.md` passed.
- Source-of-truth consistency check passed for `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001` in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, and `docs/EVIDENCE_INDEX.md`.
- Secret-safety check passed for changed docs and tests, confirming no API key value, sensitive auth header label, or bearer token string appears in changed docs/tests/snapshots.

Follow-up checks after direct-script and guardrail fixes:

- `make check-local-llm-orchestration-guardrails` passed.
- `env -u PYTHONPATH -u ALPHA_LIVE_OPENAI -u OPENAI_API_KEY MODEL_PROVIDER=openai python tools/operator_smoke_runner.py --mode openai --prompt "Reply with one concise sentence that does not echo this prompt."` returned sanitized JSON with `reason: live_openai_opt_in_required` and no import failure.
- `python -m pytest -q tests/test_operator_smoke_runner.py` passed with 9 tests.
- `python -m pytest -q tests/test_operator_smoke_runner.py tests/test_local_llm_provider_adapter.py::test_ollama_backend_rejects_non_local_endpoints_before_transport_invocation tests/providers/test_openai_provider.py::test_missing_openai_api_key_is_safe tests/providers/test_openai_provider.py::test_openai_api_key_can_come_from_environment` passed with 22 tests.
- `python -m pytest -q` passed.
- `git diff --check` passed.
- `python scripts/check_narrative_claim_safety.py docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/result-capture-template.md docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/selected-next-lane.md docs/evals/runs/alpha-solver-local-openai-smoke-runner-001/checks-run.md` passed.
- Source-of-truth consistency check passed for `OPERATOR_REVIEW_REQUIRED_AFTER_LOCAL_OPENAI_SMOKE_RUNNER_001` in `docs/CURRENT_STATE.md`, `docs/LANE_REGISTRY.md`, and `docs/EVIDENCE_INDEX.md`.
- Secret-safety check passed for changed docs and tests, confirming no API key value, sensitive auth header label, or bearer token string appears in changed docs/tests/snapshots.

No OpenAI live call was run. No local model call was run.
