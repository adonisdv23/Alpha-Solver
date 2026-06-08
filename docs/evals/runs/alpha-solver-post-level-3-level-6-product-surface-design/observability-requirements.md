# Observability Requirements

## Future product-surface observability

Future product-surface implementation must define observability before code changes. Required design elements include:

- request and response correlation identifiers;
- operator action logs;
- evidence-boundary labels in logs and artifacts;
- stop-condition logging;
- provider/local runtime provenance when applicable;
- latency and resource metrics that do not imply benchmark quality;
- error taxonomy metrics for missing evidence, stale evidence, contradictory evidence, unsafe defaults, unclear controls, and blocked claims;
- redaction and retention status;
- audit-export requirements for reviewer inspection.

## Non-promotional metrics rule

Observability may support debugging, audit, and safety review. It must not be presented as benchmark performance, quality superiority, product readiness, provider readiness, or production readiness unless a later accepted lane explicitly authorizes that evidence boundary.
