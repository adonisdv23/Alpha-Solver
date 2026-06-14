# Non-Actions

This lane intentionally did not:

- implement runtime code;
- implement an endpoint;
- implement a CLI bridge;
- implement a UI;
- mount routes on `service.app`;
- expose `/v1/solve` or any other route;
- expose anything publicly;
- deploy anything;
- change CORS;
- call hosted providers;
- use provider tokens;
- access credentials;
- call local Ollama or any local model;
- bypass Alpha Solver routing;
- allow a sidecar to call models directly as Alpha Solver evidence;
- ingest private files, uploads, RAG corpora, memory, workspace data, or embeddings;
- update Google Sheets or backlog workbooks;
- claim operator-console readiness, UI readiness, runtime readiness, public readiness, provider readiness, production readiness, model quality, benchmark validation, value evidence, or Alpha superiority.
