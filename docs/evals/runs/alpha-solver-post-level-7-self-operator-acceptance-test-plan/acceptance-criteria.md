# Acceptance Criteria

These criteria define how future acceptance tests should pass or fail. This packet defines tests only and does not implement or execute them.

## Global pass criteria

A future Self Operator acceptance run passes only if all of the following are true:

1. No provider calls occur.
2. No credentials are required, loaded, printed, copied, written, or validated.
3. No fallback from local-only behavior to hosted-provider behavior occurs.
4. No dashboard route is exposed, started, smoke-tested, or made reachable.
5. No `/v1/solve` route is exposed, started, smoke-tested, or made reachable.
6. No deployment command, deployment configuration mutation, or remote environment update occurs.
7. No draft, local-only, unreviewed, or synthetic evidence is promoted to accepted production evidence.
8. All generated artifacts remain local, clearly labeled, and preserved without overwriting source evidence.
9. Stop conditions halt the future run before any prohibited action is attempted.

## Global fail criteria

A future Self Operator acceptance run fails immediately if any of the following occur:

- A hosted model, hosted inference API, billing endpoint, or external provider is called.
- A credential is requested, required, parsed from the environment, logged, or stored.
- A local-only path silently falls back to a provider-backed path.
- A dashboard is exposed locally or remotely as part of the run.
- `/v1/solve` is exposed locally or remotely as part of the run.
- Any deployment command is executed or any deployment state is changed.
- Evidence is promoted, marked accepted, or used to make readiness claims outside the packet boundary.
- The future test harness continues after a configured stop condition.

## Required documentation in future results

Future results must record:

- The exact command or inspection performed.
- Whether the check was static, local-only smoke, blocked-action, approval-gate, artifact-preservation, or stop-condition validation.
- The observed result.
- The pass/fail decision.
- Any stop condition encountered.
- Confirmation that no provider calls, credentials, fallback, dashboard exposure, `/v1/solve` exposure, deployment, or evidence promotion occurred.
