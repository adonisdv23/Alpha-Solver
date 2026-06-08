# Explicit Enablement

## Enablement rule

Future product surfaces may only be enabled through explicit enablement. Explicit enablement means a deliberate, recorded decision that identifies the surface, scope, operator, reviewer, environment, time window, rollback route, audit destination, and confirmation gates satisfied.

## Minimum enablement record

A future enablement record should identify:

- the exact product surface or route being enabled;
- the environment and audience receiving access;
- the operator requesting enablement;
- the reviewer or approver accepting the risk;
- the configuration key or deployment mechanism used;
- the start time and any expiration time;
- the evidence boundary that remains in force;
- the rollback or disablement procedure;
- the audit log destination.

## Non-implicit enablement

The following must not count as explicit enablement:

- merging documentation;
- merging dormant code;
- setting unrelated environment variables;
- having provider credentials present;
- running local tests;
- opening a dashboard internally;
- creating a backlog item;
- referencing a lane in planning docs.

## Adoption authority

Level 6 controls whether and how explicit enablement rules are adopted.
