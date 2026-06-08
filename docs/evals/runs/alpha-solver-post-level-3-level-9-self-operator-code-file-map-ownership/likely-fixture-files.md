# Likely inert fixture files

The future first-code lane may create inert fixtures only if needed by static tests. Likely candidate paths are listed for planning only:

- `tests/fixtures/self_operator_static/forbidden_provider_call.py.txt`
- `tests/fixtures/self_operator_static/forbidden_external_api.py.txt`
- `tests/fixtures/self_operator_static/forbidden_credentials.py.txt`
- `tests/fixtures/self_operator_static/forbidden_browser_deploy_billing.py.txt`
- `tests/fixtures/self_operator_static/forbidden_fallback_promotion.py.txt`
- `tests/fixtures/self_operator_static/missing_approval_artifacts.json`

Fixtures must be inert text or JSON. They must not contain executable secrets, provider outputs, external API responses, browser data, deployment output, billing data, or evidence-promotion labels.
