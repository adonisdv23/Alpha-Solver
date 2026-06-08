# Proposed fixtures

Fixtures should be inert text or JSON examples that static tests parse without executing. Shapes:

- `forbidden_provider_call.py.txt`: contains text resembling a provider client call.
- `forbidden_external_api.py.txt`: contains text resembling an HTTP request.
- `forbidden_credentials.py.txt`: contains text resembling credential access.
- `forbidden_browser_deploy_billing.py.txt`: contains text resembling browser automation, deployment, or billing commands.
- `forbidden_fallback_promotion.py.txt`: contains text resembling fallback or evidence promotion.
- `missing_approval_artifacts.json`: contains a minimal artifact record missing approval fields.

Fixtures must not include real secrets, provider outputs, external API responses, browser data, deployment output, billing data, or evidence-promotion labels.
