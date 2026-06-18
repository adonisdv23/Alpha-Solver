# Scoring Protocol for Future Lane

A later scoring lane must follow this blind procedure:

1. Use the PR #619 scorer-facing packet only.
2. Preserve task IDs `RVP-001` through `RVP-012` exactly.
3. Score Response A and Response B independently on each frozen rubric dimension.
4. Record blank-to-filled scores only during the future scoring lane.
5. Record preference, rationale, caveat, and contested-score flags only during the future scoring lane.
6. Do not unblind during scoring.
7. Do not compute final interpretation during scoring.

The future scoring lane must stop rather than proceed if blind scoring cannot be completed without source identities, source artifacts, route metadata, or unblinding material.
