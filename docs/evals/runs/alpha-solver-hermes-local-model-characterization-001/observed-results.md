# Observed Results

Verdict: `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED`

## Environment observation

The repository environment did not expose `ollama` on `PATH` during this lane. Therefore, no Hermes-style local model could be confirmed as installed, and no local characterization run was executed.

## Commands/checks performed

```bash
command -v ollama && ollama list
```

Observed outcome: no `ollama` executable was reported.

```bash
python -m alpha.local_llm.multi_model_smoke_harness --help
```

Observed outcome: the approved local harness help text was available.

## Result table

| Model | Installed status | Run status | Verdict | Notes |
| --- | --- | --- | --- | --- |
| Hermes-style local model | Not installed / not observable in this environment | Not executed | `HERMES_CHARACTERIZATION_BLOCKED_MODEL_NOT_INSTALLED` | Docs-only plan and operator template captured. |

## Evidence state

No model output was produced. No prompt fixture result was scored. No local endpoint was called. No hosted provider was called.
