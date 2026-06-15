# Local prerequisites

Before any real local Ollama smoke run, the operator must confirm all items below on the local machine:

1. Ollama is already installed and running locally.
2. The first `ollama list` column equals `gemma3:4b` exactly; suffix variants such as `gemma3:4b-it-qat` do not satisfy this lane, and the lane does not authorize `ollama pull`, model installation, tag substitution, registry sweeps, or fallback models.
3. The only endpoint used is `http://127.0.0.1:11434/api/chat`.
4. Hosted provider credentials and tokens are not used and are not required.
5. The prompt fixture is synthetic and contains no private, customer, production, or backlog spreadsheet data.
6. The run uses only the operator CLI path and does not expose `/v1/solve`, dashboard routes, or public API surfaces.
7. The result is captured only as local non-behavior/smoke evidence unless separate scoring approval exists.
