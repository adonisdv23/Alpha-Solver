# Likely static test files

These paths are likely candidates for a future first-code static test scaffold lane. They are identified only as proposed paths and are not created by this packet.

## Future first-code lane may modify

- `tests/self_operator/test_static_guardrails.py`
- `tests/self_operator/test_forbidden_surfaces.py`
- `tests/self_operator/test_artifact_schema_static.py`
- `tests/self_operator/test_preflight_static.py`
- `tests/self_operator/test_approval_stopstate_static.py`

## Restrictions

The future tests must be static or local-only checks. They must not import provider clients, call providers, call external APIs, open browsers, deploy, bill, expose routes, run models, mutate source artifacts, or promote evidence.
