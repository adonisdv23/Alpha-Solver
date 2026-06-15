# ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001

Lane ID: `ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001`

This packet defines a single-model, single-path local Ollama lab lane for a tiny controlled task subset. It is intentionally narrower than the existing multi-model smoke harness and the local solver orchestration validation ladder.

## Fixed local lane choices

- Exact local model name: `gemma3:4b`
- Approved endpoint: `http://127.0.0.1:11434/api/chat`
- Prompt source: synthetic fixture only
- Execution surface: operator-only local CLI path
- Evidence status: local non-behavior/smoke evidence only, unless a separate approved scoring lane changes that status

## Operator-local helper script

The helper script `scripts/run_local_ollama_singlepath_operator.sh` is operator-local only. It must be run by the human operator on the same machine where Ollama is already installed and serving `http://127.0.0.1:11434`. The script preserves the packet boundary: it checks only for the exact first-column model tag `gemma3:4b`, refuses suffix variants, does not run `ollama pull`, does not install models, does not call hosted providers, and runs only the committed synthetic singlepath command against `http://127.0.0.1:11434/api/chat`.

## Packet files

- `local-prerequisites.md` records prerequisites that must be confirmed locally before any real Ollama run.
- `operator-run-template.md` gives the exact operator command template.
- `evidence-packet.md` gives the smoke evidence capture template.
- `evidence-boundary.md` records blocked surfaces and non-actions.
- `non-claims.md` records claims this packet does not make.
- `checks-run.md` records validation for this docs/scaffold lane.
- `local-run-artifact-2026-06-15.md` records the blocked operator-local Ollama singlepath attempt verdict.

## Closed follow-on state

No follow-on lane is started by this packet.

`NO_FURTHER_LOCAL_MODEL_LAB_OLLAMA_SINGLEPATH_LANES_SELECTED`
