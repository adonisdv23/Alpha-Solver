# Non-Promotional Metrics

## Purpose

This file defines metrics that may support future review without promoting quality, safety, production readiness, cost savings, latency, or provider performance claims.

## Allowed non-promotional metric categories

| Metric category | Non-promotional use |
| --- | --- |
| Provenance completeness | Count records with present, missing, redacted, blocked, or unknown provenance fields. |
| Trace link completeness | Count whether request, trace, parent trace, response, usage, and stop-condition links are present. |
| Provider call state counts | Count not-called, blocked, attempted, succeeded, failed, retried, and unknown provider states. |
| Usage source state counts | Count not-created, estimated, provider-reported, reconciled, disputed, partial, stale, or unknown usage states. |
| Cost label counts | Count cost label distribution without claiming savings or billing accuracy. |
| Quota label counts | Count quota label distribution without claiming capacity, availability, or production readiness. |
| Budget stop counts | Count stop conditions and post-stop review outcomes. |
| Redaction state counts | Count absent, redacted, summarized, hashed, omitted, blocked, or approved retention states. |
| Review blocker counts | Count records blocked by missing provenance, missing usage state, unknown quota state, or unknown cost state. |

## Prohibited metric claims

- Metrics must not be described as proof of model quality, solver quality, safety, accuracy, reliability, latency, throughput, cost savings, quota sufficiency, or production readiness.
- Metrics must not compare providers for promotional ranking.
- Metrics must not imply billing accuracy unless reconciled billing evidence is approved by a future Level 7-controlled implementation.
- Metrics must not treat missing or unknown provenance as success.
- Metrics must not promote prior Level 3 evidence beyond its accepted non-promotional boundary.

## Reporting labels

Future reports should label metrics as one of:

- `design_only_metric`: defined for future review but not measured.
- `dry_run_metric`: computed without enforcement or billing impact.
- `review_metric`: used for internal review without promotional claims.
- `blocked_metric`: blocked because required evidence or redaction is missing.
- `superseded_metric`: replaced by a later Level 7 decision.

## Level 7 control

Level 7 controls whether and how these metrics are measured, reported, or rejected.
