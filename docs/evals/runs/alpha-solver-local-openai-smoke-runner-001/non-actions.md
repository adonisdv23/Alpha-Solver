# Non-actions

This lane does not:

- Run OpenAI live calls in Codex.
- Require real OpenAI credentials in CI.
- Print, persist, commit, log, or expose API keys.
- Run local models in Codex.
- Pull or install local models.
- Call runtime endpoints against an external service during validation.
- Expose `/v1/solve` publicly.
- Build a UI.
- Mutate Google Sheets.
- Generate benchmark scores.
- Score outputs.
- Inspect raw Alpha or baseline outputs from prior eval packets.
- Unblind.
- Perform source-map work.
- Add broad dependencies.
- Implement release behavior.
