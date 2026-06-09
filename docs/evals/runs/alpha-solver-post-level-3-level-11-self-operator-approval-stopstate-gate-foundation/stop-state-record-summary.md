# Stop-state record summary

`alpha/self_operator/stop_state.py` adds a local-only `StopStateRecord` with schema version, lane ID, run ID, stop state, reason code, message, findings, blocked surfaces, preflight and approval summaries, artifact paths, evidence boundary, redaction status, and metadata.

Validation rejects missing lane/run/stop-state/reason/evidence fields, malformed findings, unsafe artifact paths, unconfirmed redaction, and unredacted secret-like markers. The write helper delegates to the existing artifact store and remains output-root bounded.
