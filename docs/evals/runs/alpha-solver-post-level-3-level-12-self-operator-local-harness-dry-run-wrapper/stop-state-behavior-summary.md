# Stop-state behavior summary

Blocked paths produce a stop-state artifact when the execution gate returns a stop-state record. Covered blocked paths include missing approval, false approval, missing operator confirmation, approval identity mismatch, failed preflight, unsafe artifact path, evidence-boundary issue, redaction issue, and operator-review-required flows.

The stop-state artifact is persisted under caller-provided `output_root` as `stop-state.json` by default. It includes the gate reason code, blocked surfaces, findings, approval summary, preflight summary, evidence boundary, and redaction status.
