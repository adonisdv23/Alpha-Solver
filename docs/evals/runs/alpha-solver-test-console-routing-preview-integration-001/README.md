# ALPHA-SOLVER-TEST-CONSOLE-ROUTING-PREVIEW-INTEGRATION-001

This packet records the local-only Operator console routing-preview integration.

The lane wires the existing metadata-only model and tool routing previews into `tools/operator_test_console.py` so an Operator can enter a task and preview a route recommendation before choosing whether to run a separate bounded smoke check.

## Selected next state

`OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_PREVIEW_INTEGRATION_001`

## Evidence boundary

The preview is metadata-only. It does not call providers, run hosted models, run local models, pull local models, execute tools, browse, call GitHub at runtime, mutate files, persist results, add telemetry, expose `/v1/solve`, or create readiness, benchmark, production/public, provider, local-model, tool-quality, security/privacy, or Alpha-superiority claims.
