# Authorization Method

Before any scoring can occur, all of the following must be true:

1. The operator accepts the blinded scorer packet from PR #619 for scoring.
2. The operator explicitly authorizes a blind scoring pass in a later lane after this prep lane is merged.
3. The scorer must not inspect source artifacts, source folders, route metadata, an A/B identity key, a source map, closed duplicate PR #618, or any unblinding material.
4. Scoring must use only the approved scorer-facing packet and the scoring protocol recorded for the later scoring lane.

If any condition cannot be satisfied, scoring must not begin.
