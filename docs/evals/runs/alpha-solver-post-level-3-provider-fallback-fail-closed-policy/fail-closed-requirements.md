# Fail-closed requirements

Fail-closed means the system stops safely rather than selecting or invoking another provider path when fallback authorization, safety, provenance, cost, credentials, or audit conditions are incomplete.

A future fallback-capable design must fail closed when:

- fallback authorization is missing, stale, ambiguous, or outside the current lane scope;
- provider provenance is missing or cannot distinguish the selected provider path;
- credential boundaries are missing, unclear, or not operator-approved;
- cost boundaries are missing, exceeded, or cannot be enforced before provider use;
- local-vs-hosted state is unclear;
- safety and claim gates do not authorize the proposed output or provider path;
- audit fields needed to reconstruct the attempted route are unavailable;
- evidence is stale or cannot be tied to the current packet/lane;
- stop conditions are met.

Safe failure behavior must be explicit, bounded, and non-promotional. It should produce a blocked/failed state for operator review rather than call providers, expose `/v1/solve`, run local models, run hosted models, run Ollama, run benchmarks, perform billing work, or promote evidence.
