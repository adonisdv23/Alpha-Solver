# Stop Conditions

Future product-surface work must stop if any of the following occur:

- required prior evidence is missing;
- evidence is stale or cannot be tied to an accepted packet;
- evidence contradicts the selected lane, accepted state, or claim boundary;
- claims imply API readiness, dashboard readiness, product readiness, MVP readiness, production readiness, provider readiness, billing readiness, benchmark performance, quality, or superiority without accepted evidence;
- default-off behavior is absent or ambiguous;
- operator controls are unclear, implicit, unaudited, or automatically enabled;
- `/v1/solve` exposure is proposed before readiness gates are satisfied;
- dashboard route or UI exposure is proposed before readiness gates are satisfied;
- provider, hosted, paid, fallback, billing, benchmark, or evidence-promotion behavior is proposed before explicit authorization;
- source artifacts would be modified or promoted;
- checks fail for reasons that cannot be explained as unrelated pre-existing conditions.

When a stop condition is triggered, use blocker fallback lane `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-6-PRODUCT-SURFACE-DESIGN-FIX-001` unless a narrower authorized fix lane is selected.
