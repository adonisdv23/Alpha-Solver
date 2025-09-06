# Artifacts

Alpha Solver writes run artifacts under `artifacts/` (or the path in
`ALPHA_ARTIFACTS_DIR`). These files make runs reproducible and auditable.

## Schema Versioning

Each artifact includes a `schema_version` field. The shortlist snapshot schema
is defined in [`schemas/shortlist_snapshot.schema.json`](../schemas/shortlist_snapshot.schema.json).
Version `v1` is the initial version.

## Shortlist Snapshots

Shortlists are saved under `artifacts/shortlists/` with the query, region, and
scores for the top `k` tools. Fields include `tool_id`, `score`, `confidence`,
optional `reason`, and detailed `explain` parts.

## Environment Snapshot

Capture details about the Python runtime, platform, selected environment
variables, and hashes of key files. Generate with:

```bash
python scripts/env_snapshot.py
```

Snapshots are written to `artifacts/env/env_snapshot_<timestamp>Z.json`.

## Session Trace

A session trace ties together the environment snapshot, regions, query source,
seed, shortlist paths, and timestamps. It is written to
`artifacts/run/run_<timestamp>Z.json`.

## Bundling

All artifacts and schema files can be bundled for sharing:

```bash
python scripts/bundle_artifacts.py
```

This creates `artifacts/bundles/bundle_<timestamp>Z.zip` and a matching
SHA256 checksum file alongside it.
