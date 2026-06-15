# Blind Scorer Packet Instructions

Use `scorer-packet.md` only after a future operator authorization explicitly names the scorer, scope, scorer-packet path, score-output path, no-unblinding boundary, and stop conditions.

## Scoring boundaries

- Score only the blank fields provided in the scorer packet.
- Do not score outside the 10 listed cases.
- Do not add final interpretation or aggregate claims.
- Do not call providers, run local models, use runtime endpoints, inspect dashboards, use public APIs, or mutate Google Sheets.

## No identity inference rule

Do not infer, request, reconstruct, or use which response is from which source arm. Treat `Response A` and `Response B` as anonymous.

## No unblinding rule

Do not unblind during scoring. Scores must be locked before any separately authorized future unblinding lane.

## Contested-score flag rule

If a dimension cannot be scored cleanly because the prompt, response, or evidence boundary is ambiguous, leave a concise note in the contested-score flag field and do not resolve identity.
