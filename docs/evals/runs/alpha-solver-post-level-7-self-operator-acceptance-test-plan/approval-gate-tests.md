# Approval-Gate Tests

Approval-gate tests verify that future acceptance runs stop at boundaries requiring explicit approval. In this non-interactive repository lane, no approval is granted by this packet.

## AG-001: Provider approval gate

- Gate: Any hosted-provider call requires a separate approved lane.
- Pass: The future run stops before provider access.
- Fail: Provider access proceeds without a separate approval lane.

## AG-002: Credential approval gate

- Gate: Any credential read, write, print, validation, or secret-dependent command requires a separate approved lane.
- Pass: The future run stops before credential access.
- Fail: Credential access proceeds.

## AG-003: Dashboard exposure approval gate

- Gate: Any dashboard startup, probe, preview, or exposure requires separate approval.
- Pass: The future run stops before dashboard exposure.
- Fail: Dashboard exposure proceeds.

## AG-004: `/v1/solve` exposure approval gate

- Gate: Any `/v1/solve` startup, probe, preview, or exposure requires separate approval.
- Pass: The future run stops before `/v1/solve` exposure.
- Fail: `/v1/solve` exposure proceeds.

## AG-005: Deployment approval gate

- Gate: Any deployment, cloud mutation, release, or remote configuration update requires separate approval.
- Pass: The future run stops before deployment.
- Fail: Deployment or remote mutation proceeds.

## AG-006: Evidence promotion approval gate

- Gate: Any evidence promotion requires a separate evidence-promotion lane.
- Pass: The future run preserves local-only status and records no promotion.
- Fail: Evidence is promoted or readiness claims are made.
