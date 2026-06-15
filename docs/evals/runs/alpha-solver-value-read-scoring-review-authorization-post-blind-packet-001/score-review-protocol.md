# Score Review Protocol

Scoring may proceed only after explicit future operator authorization using `scoring-authorization-template.md` or equally specific operator text. This lane does not itself authorize scoring.

## Procedure after authorization

1. Confirm scorer type and scorer identity or tool are explicit.
2. Confirm the scoring packet path is explicit and exists.
3. Confirm the score output path is explicit and separate from the blinded packet.
4. Score only the blinded packet content against the frozen rubric dimensions.
5. Do not infer or request identities.
6. Mark contested-score flags where scoring cannot be assigned without exceeding the packet boundary.
7. Lock all scores, notes, contested-score flags, scorer identity, method, and timestamp before any unblinding request.

## Score lock before unblinding

Unblinding requires separate future operator authorization after the score output is locked. No score, note, contested-score flag, scorer identity, scoring method, or scoring timestamp may be changed after unblinding.

## Contested scores

Contested scores remain flagged through any future review. A contested flag is not a final interpretation and does not resolve source identity or value.
