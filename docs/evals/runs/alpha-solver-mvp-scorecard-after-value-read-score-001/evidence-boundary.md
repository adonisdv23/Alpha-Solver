# Evidence Boundary

## Evidence accepted

This packet accepts only committed repository evidence for the score state:

- The post-581 score output records case-level blind scores, notes, preference labels, contested-score flags, scorer identity/tool, scorer type, scoring method, timestamp, and score-lock confirmation.
- The post-581 scoring log records that scoring used the authorized blinded scorer packet and did not access, request, infer, reconstruct, expose, or create source identity or an identity map.
- The post-581 checks record successful verification of PR #581 merge status, selected-state preconditions, score-output consistency, source-identity boundary, and packet consistency.

## Evidence not accepted

This packet does not accept or create:

- unblinded source identities;
- A/B-to-source mappings;
- final interpretation;
- score changes;
- provider or local-model execution evidence;
- runtime endpoint evidence;
- dashboard/public API exposure evidence;
- Google Sheets or external-ledger evidence;
- readiness, value, benchmark, security/privacy, or Alpha-superiority evidence.

## Source identity boundary

No source identities are revealed, inferred, reconstructed, or used in this packet. If a separate operator-approved source-identity review exists later, it must be cited in a separate authorized lane before any identity-dependent interpretation is made.
