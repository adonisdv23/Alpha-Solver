# Test coverage summary

Static tests added:

- `tests/test_self_operator_static_guardrails.py`
  - clean fixture has no findings;
  - provider, external API, credential, browser, deployment, billing, route, fallback, hosted fallback, and evidence-promotion fixtures produce expected IDs;
  - finding objects are stable and JSON serializable;
  - the Level 10 prompt pack contains `stop if explicit operator confirmation is missing`.
- `tests/test_self_operator_approval_stopstate_static.py`
  - missing explicit operator confirmation returns `SELF_OPERATOR_APPROVAL_GATE_REQUIRED`;
  - missing stop state returns `SELF_OPERATOR_STOP_STATE_REQUIRED`.
- `tests/test_self_operator_artifact_schema_static.py`
  - incomplete artifact JSON returns `SELF_OPERATOR_ARTIFACT_SCHEMA_INCOMPLETE`.
- `tests/test_self_operator_forbidden_behavior_static.py`
  - fixture files are inert `.py.txt` or `.json` files;
  - scanner reads text without mutating or executing fixtures.
