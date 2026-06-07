# Safe Wording

## Safe wording for docs-only design packets

Use wording that describes intent, scope, constraints, and future requirements without implying execution:

- "This packet defines proposed evaluation boundaries."
- "This is docs-only planning guidance."
- "No model inference, benchmark execution, provider call, dashboard exposure, `/v1/solve` exposure, billing work, or scoring was performed."
- "This packet does not establish quality evidence, benchmark evidence, Alpha superiority, MVP readiness, production readiness, provider readiness, dashboard readiness, `/v1/solve` readiness, billing readiness, fallback readiness, or evidence-promotion authority."
- "Level 2 and Level 3 evidence remains local-only and non-promotional."
- "Future execution is required before any result claim can be made."
- "This glossary is a supporting reference only and does not authorize any claim."

## Safe wording for future execution packets

Future execution packets may use bounded wording only when actual execution occurred and artifacts are preserved:

- "In this local run, using the documented sample and rubric, the observed outputs were scored as follows."
- "This result is limited to the captured artifact set and does not establish general quality."
- "This comparison is limited to the named baseline, prompt set, scorer, run date, and evaluation protocol."
- "The evidence is not a benchmark unless the packet executed the benchmark protocol."
- "The evidence does not establish Alpha superiority beyond the tested method and sample."
- "The evidence does not establish MVP readiness or production readiness unless the required readiness gates are included and passed."
- "Provider observations are limited to the provider configuration tested in this packet."
- "Dashboard and `/v1/solve` observations are limited to the explicitly exercised routes and environment."
- "Billing observations are limited to the explicitly tested billing controls and do not imply commercial readiness."

## Safe claim template

A safe future execution claim should include all of these components:

1. The exact run or packet name.
2. The execution date or artifact timestamp.
3. The task set or sample boundary.
4. The method, scorer, rubric, or acceptance gate.
5. The observed result.
6. The non-generalization boundary.
7. The blocked downstream claims that remain blocked.

Example pattern:

> In `[packet]`, on `[date]`, `[method]` was run against `[sample]` and produced `[bounded observation]`. This supports only `[narrow conclusion]` and does not establish benchmark evidence, Alpha superiority, MVP readiness, production readiness, provider readiness, dashboard readiness, `/v1/solve` readiness, billing readiness, fallback readiness, or evidence promotion.
