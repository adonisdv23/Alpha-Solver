# Likely static test files

The future first-code lane may modify only static test files explicitly authorized by its Level 10 scope. Likely candidate paths are listed for planning only and are not created by this packet:

- `tests/test_self_operator_static_guardrails.py`
- `tests/test_self_operator_forbidden_behavior_static.py`
- `tests/test_self_operator_artifact_schema_static.py`
- `tests/test_self_operator_approval_stopstate_static.py`

These paths are candidates for static tests that detect prohibited Self Operator behavior. They must remain offline and deterministic.
