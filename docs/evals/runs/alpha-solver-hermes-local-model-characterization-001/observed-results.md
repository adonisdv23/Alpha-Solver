# Observed Results

Verdict: `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED`

## Container detection

Command run in this workspace:

```bash
command -v ollama >/dev/null 2>&1 && ollama list || true
```

Observed result: no output. No local Hermes model was detected in this container.

## Characterization execution

No Hermes characterization prompts were executed. No local model outputs were produced. No behavior, quality, benchmark, or role-fit evidence is present in this packet.

## Result records

No result records captured.

## Evidence state

- Installed status if known: not installed / not detected in this container.
- Local characterization status: not executed.
- Evidence type: docs-only characterization plan and operator-run template.
- Current allowed verdict: `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED`.
