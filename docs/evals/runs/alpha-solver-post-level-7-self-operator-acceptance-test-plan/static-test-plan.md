# Static Test Plan

Static tests inspect files and configuration only. They must not start services, call models, call providers, run dashboard routes, run `/v1/solve`, deploy, or promote evidence.

## ST-001: Provider-call prohibition scan

- Method: Inspect future Self Operator commands, scripts, and docs for provider invocation paths.
- Pass: No future acceptance command can invoke hosted providers, billing APIs, model APIs, or external inference endpoints.
- Fail: Any command can invoke a hosted provider or external inference endpoint.

## ST-002: Credential prohibition scan

- Method: Inspect future commands and environment requirements for credential access.
- Pass: No provider keys, service account files, API tokens, cloud credentials, or dashboard secrets are required or read.
- Fail: Any credential is required, read, validated, printed, copied, or written.

## ST-003: Fallback prohibition scan

- Method: Inspect configuration for local-to-provider fallback behavior.
- Pass: Local-only mode fails closed when local prerequisites are absent.
- Fail: Local-only mode silently switches to hosted-provider behavior.

## ST-004: Dashboard exposure scan

- Method: Inspect future commands for dashboard server startup, route probing, preview exposure, or tunnel creation.
- Pass: No dashboard endpoint is started, exposed, or probed.
- Fail: Any dashboard route is started, exposed, probed, tunneled, or advertised.

## ST-005: `/v1/solve` exposure scan

- Method: Inspect future commands for API server startup or `/v1/solve` probing.
- Pass: `/v1/solve` is not started, exposed, or probed.
- Fail: `/v1/solve` is started, exposed, probed, tunneled, or advertised.

## ST-006: Deployment prohibition scan

- Method: Inspect future commands for cloud deployment, remote update, or production configuration mutation.
- Pass: No deployment or remote environment mutation command is present.
- Fail: Any deployment, release, cloud update, remote secret update, or production state mutation command is present.

## ST-007: Evidence-promotion prohibition scan

- Method: Inspect future result templates for status labels and promotion language.
- Pass: Results remain draft/local-only/unpromoted unless a separate approved evidence-promotion lane exists.
- Fail: Results are labeled promoted, accepted production evidence, deployment-ready evidence, or final runtime acceptance evidence.
