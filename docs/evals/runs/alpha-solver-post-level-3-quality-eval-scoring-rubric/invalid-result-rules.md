# Invalid-Result Rules

A future result should be marked **Invalid - Not scoreable** instead of receiving a numeric score if any rule below applies.

## Invalid triggers

- The result scores real outputs without an approved scoring-execution lane.
- The result runs benchmarks or claims benchmark findings without authorization.
- The result runs local model inference, calls hosted providers, exposes `/v1/solve`, exposes dashboards, adds fallback, or performs billing work outside scope.
- The result modifies runtime, provider, CLI, checker scripts, tests, Makefile, CI, source artifacts, Level 2 packets, Level 3 packets, or release-readiness ladder files when the lane is docs-only.
- The result claims Alpha Solver quality, superiority, readiness, production fitness, API readiness, dashboard readiness, provider readiness, billing readiness, or MVP readiness without permitted evidence.
- The result omits required selected-next or blocker fallback markers.
- The result contains contradictory selected-next state, such as both a no-further-lanes decision and a selected implementation lane.
- The result relies on source-artifact changes or preserved packet rewrites that were not authorized.
- The result cannot be traced to allowed evidence and does not clearly label uncertainty.

## Invalid-result disposition

Invalid results should be repaired through the approved fallback lane or a later approved corrective lane. Reviewers must not convert an invalid result into a low numeric score merely to preserve a scoring table.
