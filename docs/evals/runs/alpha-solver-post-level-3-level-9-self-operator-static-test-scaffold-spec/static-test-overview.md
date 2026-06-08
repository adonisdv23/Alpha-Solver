# Static test overview

The future static scaffold must be deterministic, offline, and read-only except for ordinary test temporary directories. It must scan authorized code and fixture text for prohibited Self Operator behavior and emit stable finding IDs.

Pass behavior: all prohibited behavior patterns are absent or explicitly blocked in inert fixtures.

Fail behavior: any prohibited behavior pattern produces a finding ID, affected path, short reason, and stop-state recommendation.
