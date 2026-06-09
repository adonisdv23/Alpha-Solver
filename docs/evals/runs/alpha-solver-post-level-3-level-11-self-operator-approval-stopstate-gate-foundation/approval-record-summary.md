# Approval record summary

`alpha/self_operator/approval.py` adds a local-only `ApprovalRecord` with schema version, lane ID, run ID, approved flag, operator confirmation, approval text, approver, timestamp, scope summary, evidence boundary, redaction status, and metadata.

Validation fails closed for missing/false approval, missing operator confirmation, missing hard-stop phrase, missing lane/run/evidence boundary/scope fields, unconfirmed redaction, and unredacted secret-like markers.

The hard-stop phrase is preserved exactly: `stop if explicit operator confirmation is missing`.
