# Retention and Redaction

## Retention boundaries

Future product-surface observability should assign a retention class before storing trace records, decision logs, error logs, or evidence references.

Suggested retention classes for later Level 6 acceptance or revision:

- `ephemeral_diagnostic`: temporary troubleshooting record with short retention.
- `run_packet_review`: bounded review artifact tied to a run ID.
- `release_readiness_review`: bounded artifact retained for release-readiness decisions.
- `blocked_sensitive`: record blocked from normal retention because it contains or may contain sensitive content.
- `legal_or_security_hold`: explicitly approved retention override.

## Redaction requirements

- Redaction must occur before logs are used for broad review whenever sensitive content could be present.
- Raw secrets, API keys, provider credentials, session tokens, payment data, billing account data, and private user identifiers must not be stored in trace records, decision logs, or error logs.
- Prompt or response content should be summarized, hashed, omitted, or redacted unless a later accepted policy explicitly allows collection.
- Redaction state must be recorded on trace records, decision logs, error logs, and evidence references.
- Reviewers must be able to tell whether data is absent, redacted, summarized, blocked, or approved for retention.

## Level 6 control

Level 6 controls whether and how these retention and redaction classes are used, replaced, or rejected.
