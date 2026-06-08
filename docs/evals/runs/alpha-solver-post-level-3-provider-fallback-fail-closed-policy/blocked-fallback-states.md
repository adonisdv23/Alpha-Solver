# Blocked fallback states

Fallback is blocked and must fail closed when any of the following states exists:

- missing provider provenance;
- missing credential boundary;
- missing cost boundary;
- ambiguous authorization;
- unsafe claim boundary;
- stale evidence;
- missing audit fields;
- unclear local-vs-hosted state;
- unknown provider identity;
- unknown model identity;
- unregistered capability boundary;
- unreviewed credential or secret handling;
- unavailable cost estimate or budget enforcement;
- circuit-breaker state that cannot be reconstructed;
- retry state that could duplicate provider work without operator approval;
- timeout state that could hide partial provider work;
- output safety state that cannot be tied to the selected provider path;
- product-surface state that could imply readiness or promotion;
- any requested fallback outside the accepted future lane scope.

A blocked fallback state must not be bypassed by convenience, availability, latency, quality expectations, credential presence, or operator urgency.
