# Unblinding Review Protocol

This protocol is for a future pass only. No unblinding is performed by this packet.

## Preconditions for a future pass

1. Confirm the future pass has explicit operator authorization.
2. Confirm the locked blind score output is present and unchanged from the selected source-of-truth file.
3. Confirm the future pass has an approved source-identity map custody method.
4. Confirm the future pass will not inspect raw Alpha or baseline outputs unless a specific, bounded discrepancy review is separately authorized.

## Future review sequence

1. Record the score-output file path and checksum or equivalent immutable identifier.
2. Record that all case scores are accepted as locked before source identities are reviewed.
3. Review source identities using the approved custody method.
4. Attach source labels to locked score rows without changing scores or scorer notes.
5. Record any mismatch, missing identity, ambiguous identity, or custody defect as a stop condition.

## Prohibited in the future pass unless separately authorized

- Changing scores, notes, contested-score flags, scorer identity/tool, scoring method, or score-lock confirmation.
- Inferring identities from raw outputs or style clues.
- Re-running Alpha, baseline, providers, local models, endpoints, dashboards, or `/v1/solve`.
- Creating claims before final interpretation protocol steps are complete.
