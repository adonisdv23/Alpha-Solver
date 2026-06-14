# Unknowns and Operator Decisions

Each reconstructed spec contains a per-spec unknown note. Common unknowns:

- Live provider/service integration is unknown unless represented by committed tests.
- Deployment, CI wiring, remote storage, Grafana import, central telemetry, and external pricing authority are unknown unless represented by source targets.
- Additional intents, prompt decks, scenarios, and production credentials require operator decision or new specs.
- Reconstruction does not assert implementation quality, completeness, or readiness.

Uncertain specs: all 22 have at least one bounded unknown because code/tests do not define every possible production behavior.
