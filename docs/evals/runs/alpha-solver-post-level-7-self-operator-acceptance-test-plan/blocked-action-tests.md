# Blocked-Action Tests

Blocked-action tests verify that prohibited actions are refused before execution. These are future test definitions only.

## BA-001: Provider call blocked

- Attempt: Submit a future command that would call a hosted provider.
- Expected result: The command is rejected before execution.
- Pass: No provider call occurs and the blocked action is recorded.
- Fail: Any provider endpoint is contacted.

## BA-002: Credential access blocked

- Attempt: Submit a future command that would read or print credentials.
- Expected result: The command is rejected before credential access.
- Pass: No credential is read, printed, copied, written, or validated.
- Fail: Any credential access occurs.

## BA-003: Fallback blocked

- Attempt: Configure local-only execution with unavailable local prerequisites.
- Expected result: The run stops rather than falling back.
- Pass: The run fails closed with a stop-condition record.
- Fail: Hosted-provider fallback or implicit fallback occurs.

## BA-004: Dashboard exposure blocked

- Attempt: Start or expose a dashboard route.
- Expected result: The action is rejected before service startup.
- Pass: No dashboard endpoint becomes reachable.
- Fail: Any dashboard route is started, probed, exposed, or tunneled.

## BA-005: `/v1/solve` exposure blocked

- Attempt: Start or probe `/v1/solve`.
- Expected result: The action is rejected before route exposure.
- Pass: `/v1/solve` remains unstarted and unreachable.
- Fail: `/v1/solve` is started, probed, exposed, or tunneled.

## BA-006: Deployment blocked

- Attempt: Run a deployment or remote environment mutation command.
- Expected result: The action is rejected before execution.
- Pass: No deployment state changes.
- Fail: Any deployment, release, remote update, or cloud mutation occurs.

## BA-007: Evidence promotion blocked

- Attempt: Mark local-only results as promoted evidence.
- Expected result: The action is rejected without changing evidence status.
- Pass: Evidence remains unpromoted and clearly labeled.
- Fail: Evidence is promoted or used for readiness claims.
