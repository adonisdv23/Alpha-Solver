# Non-Actions and Evidence Boundary

## Evidence boundary

Evidence boundary: Docs-only schema design. This does not create database tables, queues, jobs, API routes, dashboard routes, runtime execution, provider calls, or evidence promotion.

## Explicit non-actions

This packet does not:

- create production database schema;
- create migrations, ORM models, tables, indexes, or persistence code;
- create queues, workers, schedulers, jobs, or runtime task execution;
- create or expose API routes;
- create or expose dashboard routes;
- call local models, hosted providers, or external provider APIs;
- add provider fallback or hosted fallback;
- run benchmark, smoke, or model-quality evidence collection;
- promote any evidence beyond this docs-only schema design boundary;
- update backlog workbooks or external planning ledgers;
- change source code, tests, runtime behavior, deployment behavior, or environment expectations.

## Evidence-boundary labels

Candidate labels defined by this packet:

- `DOCS_ONLY_SCHEMA_DESIGN`: candidate schema vocabulary only.
- `OPERATOR_ONLY_LOCAL_EXECUTION_COMPATIBLE`: fields are intended to be usable by an operator recording local work.
- `FUTURE_AUDIT_COMPATIBLE`: fields are intended to support future audit review without implying implementation.
