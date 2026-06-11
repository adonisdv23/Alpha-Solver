# Redaction rules

Redaction rules binding the first supervised use. These apply the prep
packet's `redaction-and-secrets.md` to this lane's specific artifacts.

## Enforced redaction behavior

- All persisted pipeline payloads pass through
  `alpha/self_operator/redaction.py`: key/value and bearer-style matches are
  replaced with `[REDACTED_SELF_OPERATOR_SECRET]`, and mapping keys on the
  sensitive keyword list are redacted wholesale.
- Records must carry `redaction_status: "redacted"`; anything else fails
  validation and stops the run.

## Operator redaction review before any import

Before importing any artifact from the output root into the execution
lane's packet, the operator must confirm the artifact contains:

- no live keys or tokens;
- no provider output and no hosted model output;
- no external API responses;
- no browser data;
- no deployment or billing output;
- no Google Sheets data;
- no local environment values beyond what the artifact schema requires
  (home-directory paths, usernames, and hostnames are trimmed or
  generalized where they appear).

Given this target, every artifact is expected to contain only docs paths,
checker output, gate fields, and operator notes; anything outside that
expectation is itself a redaction finding.

## Failure handling

An artifact that cannot pass this review is not imported; that is a stop
condition (`blocked_by_redaction_issue`) handled per `stop-state-rules.md`.
The raw artifact stays preserved, unedited, below the output root.

## This packet lane

This lane accessed no credentials and no secrets, and no secret values
appear anywhere in this packet.
