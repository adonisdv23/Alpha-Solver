# Test Evidence

Lane ID: `ALPHA-SOLVER-DEF-002-DEFAULT-CREDENTIALS-HARDENING-001`

Verdict: `DEF_002_RR_03_DEFAULT_CREDENTIALS_HARDENED`

## Focused tests run

```bash
python -m pytest -q tests/test_default_credentials_hardening.py tests/ui/test_auth.py tests/test_api_keys.py
```

Coverage includes:

- `_load_service_auth_keys()` has no built-in fallback.
- Compose files no longer inject `changeme` as an active API-key default.
- Explicit synthetic keys still work.
- Missing keys fail closed for protected API routes.
- Dashboard auth tests still pass with synthetic dashboard credentials.
- API-key middleware tests still pass with synthetic keys.

## Syntax checks run

```bash
python -m py_compile alpha/core/config.py alpha/webapp/routes/auth.py service/app.py
```

## Static docs checks run

```bash
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_packet_consistency.py
```

## Boundary

No providers were called. No tokens were used. No real credentials were accessed or printed.
