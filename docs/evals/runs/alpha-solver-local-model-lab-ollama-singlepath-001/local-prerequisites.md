# Local prerequisites

Before any real local Ollama smoke run, the operator must confirm all items below on the local machine:

1. Ollama is already installed and running locally.
2. The exact model `gemma3:4b` is already available locally; do not pull or install a model as part of this lane.
3. The only endpoint used is `http://127.0.0.1:11434/api/chat`.
4. Hosted provider credentials and tokens are not used and are not required.
5. The prompt fixture is synthetic and contains no private, customer, production, or backlog spreadsheet data.
6. The run uses only the operator CLI path and does not expose `/v1/solve`, dashboard routes, or public API surfaces.
7. The result is captured only as local non-behavior/smoke evidence unless separate scoring approval exists.
