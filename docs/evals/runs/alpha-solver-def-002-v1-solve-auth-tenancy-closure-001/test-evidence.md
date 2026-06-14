# Test Evidence

Required focused tests are in `tests/test_v1_solve_auth_tenancy_boundary.py`.

The intended validation set is local-only:

- `python -m pytest -q tests/test_v1_solve_auth_tenancy_boundary.py tests/test_api_auth_ratelimit.py tests/test_default_credentials_hardening.py`
- `python -m py_compile alpha/core/config.py service/app.py`
- `python scripts/check_local_llm_doc_paths.py`
- `python scripts/check_local_llm_evidence_boundaries.py`
- `python scripts/check_local_llm_packet_consistency.py`
- `git diff --check`

These checks do not require real credentials, live provider access, provider-backed tests, tokens, or deployment.
