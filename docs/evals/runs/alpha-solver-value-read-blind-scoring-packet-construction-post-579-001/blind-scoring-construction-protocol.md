# Blind Scoring Construction Protocol

## Scope

This protocol converts preserved post-578 raw manual no-provider outputs into scorer-facing blinded material. The conversion is documentation-only and is limited to packet construction.

## Conversion steps

1. Confirm the selected 10 case IDs from the post-578 pilot subset.
2. Confirm that each selected case has one preserved raw output in the source Alpha folder and one preserved raw output in the source baseline folder.
3. Copy response text into a scorer-facing packet as `Response A` and `Response B` only.
4. Remove source headings and raw file paths from the scorer-facing packet because those labels reveal identity.
5. Neutralize identity-revealing terms in scorer-facing text when necessary so the scorer sees only the task material and response substance.
6. Add blank scoring fields using the frozen rubric dimensions.
7. Keep the unblinding map outside the repository and outside the PR body.

## Identity boundary

Scorer-facing files must not identify which response came from the source Alpha folder or which response came from the source baseline folder. The scorer must not infer, request, reconstruct, or use response identity.

## Not scoring

This lane does not perform scoring. All scoring fields remain blank. Score filling, score lock, unblinding, and interpretation require separate future operator authorization.
