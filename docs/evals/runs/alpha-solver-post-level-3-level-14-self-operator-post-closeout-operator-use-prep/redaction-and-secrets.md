# Redaction and secrets

Redaction expectations for any future supervised use, restating the
canonical runbook (section 8) and the enforced behavior of
`alpha/self_operator/redaction.py`.

## Enforced redaction behavior

- All persisted payloads pass through the redaction module: key/value and
  bearer-style matches are replaced with `[REDACTED_SELF_OPERATOR_SECRET]`,
  and mapping keys on the sensitive keyword list are redacted wholesale.
- Records must carry `redaction_status: "redacted"`; anything else fails
  validation (`SELF_OPERATOR_APPROVAL_REDACTION_REQUIRED`,
  `SELF_OPERATOR_STOP_STATE_REDACTION_REQUIRED`).

## Operator redaction review before any import

Before importing any artifact into repository evidence, the operator must
confirm the artifact contains:

- no live keys or tokens;
- no provider output and no hosted model output;
- no external API responses;
- no browser data;
- no deployment or billing output;
- no Google Sheets data.

The #461 packet's `redaction-review.md` is the canonical worked example of
this review. An artifact that cannot pass this review is not imported; that
is a stop condition (`blocked_by_redaction_issue`).

## Secrets boundary

- Credential or secret access, storage, display, or use remains forbidden in
  every operator-use lane (`forbidden-actions.md`).
- This prep lane accessed no credentials and no secrets, and no secret
  values appear anywhere in this packet.
