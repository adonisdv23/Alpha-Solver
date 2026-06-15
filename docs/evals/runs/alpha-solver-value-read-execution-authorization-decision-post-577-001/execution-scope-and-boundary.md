# Execution Scope and Boundary

## Allowed future scope, only if separately authorized

A future lane may be allowed to generate Value Read Alpha and baseline outputs for the frozen packet cases, preserve raw outputs, prepare blinded scorer packets, lock blind scores, unblind only after score lock, and interpret results narrowly as simulation-only evidence.

## Forbidden scope in this lane

This lane forbids output generation, scoring, unblinding, provider calls, hosted model calls, local model runs, credentials, billing inspection, runtime endpoint use, dashboard use, public API exposure, Google Sheets mutation, dependency addition, routing changes, council changes, benchmarks, and readiness or value claims.

## Simulation/no-provider separation

Simulation/no-provider work may prepare prompts, paths, templates, and boundaries. It may not produce model outputs unless a later authorization explicitly defines the non-provider mechanism.

## Runtime/provider/local-model separation

Runtime, provider, hosted-model, and local-model execution are separate authorization categories. A future operator approval must name each allowed category explicitly. Silence is denial.
