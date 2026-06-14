# Test evidence

Targeted and relevant checks run in this lane:

- `python -m pytest tests/test_cors_boundary.py -q` — passed after adding
  review-blocker coverage for post-import `SERVICE_CORS_ALLOW_CREDENTIALS=false`,
  wildcard origins with credentials disabled, wildcard rejection with credentials
  enabled, and common truthy credential values.
- `python -m pytest tests/test_api_auth_ratelimit.py tests/test_health_ready.py tests/ui/test_auth.py tests/ui/test_expert_preview_real_app.py -q` — passed.
- `python -m compileall alpha/core/config.py service/app.py tests/test_cors_boundary.py` — passed.
- `git diff --check` — passed.
- Static evidence packet check for required files and bounded verdict text — passed.
- `python scripts/check_local_llm_doc_paths.py` — passed.
- `python scripts/check_local_llm_evidence_boundaries.py` — passed.
- `python scripts/check_local_llm_packet_consistency.py` — passed.

Broader checks:

- `python -m pytest -q` was run and failed in pre-existing/non-CORS areas:
  provider model expectation drift in `tests/test_api_endpoints.py`, provider-state
  contamination around `tests/test_cost_tracking.py`, and a security prompt test
  receiving a non-mocked provider-shaped answer. This full-suite run is not used
  as RR-01 closure evidence.
- A narrower retry with provider credentials removed passed the cost/security
  subset but still failed the same provider model expectation assertions in
  `tests/test_api_endpoints.py::test_solve_openai_provider_errors_return_safe_responses`.

No successful provider call is required for this CORS lane, and no public surface
was intentionally exposed by these tests.
