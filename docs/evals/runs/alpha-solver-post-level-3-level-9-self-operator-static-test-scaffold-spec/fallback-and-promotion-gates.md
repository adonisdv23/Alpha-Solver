# Fallback and promotion gates

The future static scaffold must block fallback behavior and evidence promotion.

## Blocked fallback

- Local fallback that masks failure.
- Hosted fallback.
- Any silent downgrade from blocked action to alternate execution.

## Blocked promotion

- Labels or metadata that promote generated artifacts into accepted evidence.
- Source-artifact mutation or generated evidence promotion.

Expected finding IDs include `SELF_OPERATOR_FALLBACK_BLOCKED`, `SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED`, and `SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED`.
