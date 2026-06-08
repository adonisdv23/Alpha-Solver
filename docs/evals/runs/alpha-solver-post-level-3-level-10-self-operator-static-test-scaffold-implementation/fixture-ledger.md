# Fixture ledger

All fixtures are inert local text/JSON files under `tests/fixtures/self_operator_static/`.

- `clean_noop.py.txt`: clean no-op text fixture; expected no findings.
- `forbidden_provider_call.py.txt`: placeholder provider-call surface.
- `forbidden_external_api.py.txt`: placeholder external API surface with no real endpoint.
- `forbidden_credentials.py.txt`: placeholder credential names only; no real values.
- `forbidden_browser_deploy_billing.py.txt`: placeholder browser, deployment, and billing tokens; no real output/data.
- `forbidden_routes_cli_dashboard.py.txt`: placeholder route, CLI, and dashboard exposure tokens.
- `forbidden_fallback_promotion.py.txt`: placeholder fallback, hosted fallback, and evidence-promotion tokens.
- `missing_operator_confirmation.json`: complete inert artifact-shaped JSON with explicit confirmation set false.
- `incomplete_artifact_schema.json`: inert JSON missing required schema/stop-state fields.
- `expected_static_findings.json`: expected finding-ID ledger for fixture tests.
