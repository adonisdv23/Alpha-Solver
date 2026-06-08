# Fallback audit requirements

Any future authorized fallback design must define audit records before fallback can be used.

Required audit fields for a future design include:

- lane or packet authorizing fallback;
- operator opt-in identifier and timestamp;
- requested route and selected route;
- source provider, target provider, model identities, and capability boundaries;
- local-vs-hosted classification before and after fallback;
- credential boundary acknowledgement;
- cost boundary acknowledgement, budget state, and estimated cost exposure;
- timeout, retry, and circuit-breaker states;
- safety and claim-gate state;
- blocked-state checks performed;
- final outcome: selected, blocked, failed closed, or stopped;
- evidence packet references used for the decision.

Audit gaps are blocked fallback states. A future design must prefer no provider call over incomplete audit reconstruction.
