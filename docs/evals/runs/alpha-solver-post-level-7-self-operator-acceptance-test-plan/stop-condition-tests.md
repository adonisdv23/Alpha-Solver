# Stop-Condition Tests

Stop-condition tests verify that future acceptance runs halt before prohibited or approval-gated actions.

## SC-001: Network/provider stop condition

- Trigger: A future command would access a hosted provider, billing endpoint, or external inference endpoint.
- Pass: The run stops before network/provider access.
- Fail: The run continues and contacts an external endpoint.

## SC-002: Credential stop condition

- Trigger: A future command would read, print, copy, write, or validate credentials.
- Pass: The run stops before credential access.
- Fail: Any credential access occurs.

## SC-003: Fallback stop condition

- Trigger: Local-only prerequisites are absent or invalid.
- Pass: The run stops with no fallback.
- Fail: The run continues through hosted-provider or implicit fallback behavior.

## SC-004: Dashboard stop condition

- Trigger: A future command would start, probe, expose, tunnel, or advertise a dashboard route.
- Pass: The run stops before dashboard exposure.
- Fail: Any dashboard route becomes reachable or is probed.

## SC-005: `/v1/solve` stop condition

- Trigger: A future command would start, probe, expose, tunnel, or advertise `/v1/solve`.
- Pass: The run stops before `/v1/solve` exposure.
- Fail: `/v1/solve` becomes reachable or is probed.

## SC-006: Deployment stop condition

- Trigger: A future command would deploy, release, mutate cloud state, or update remote configuration.
- Pass: The run stops before deployment or mutation.
- Fail: Deployment or remote mutation occurs.

## SC-007: Evidence-promotion stop condition

- Trigger: A future command or summary would promote evidence or make readiness claims outside the approved boundary.
- Pass: The run stops before promotion and records the boundary violation.
- Fail: Evidence is promoted or readiness claims are made.
