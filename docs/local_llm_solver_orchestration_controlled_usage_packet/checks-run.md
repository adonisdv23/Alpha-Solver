# Checks Run

## Packet-authoring verification commands

The following checks are intended for this docs-only packet authoring lane:

```bash
git status --short
git diff --name-only
git diff --check
rg -n "production readiness|MVP readiness|benchmark evidence|local model quality|provider orchestration|provider-orchestration|Alpha superiority|billing evidence|dashboard readiness|/v1/solve readiness|broad runtime readiness|evidence-model promotion" docs/local_llm_solver_orchestration_controlled_usage_packet
find docs/local_llm_solver_orchestration_controlled_usage_packet -type f -maxdepth 1 | sort
git diff --name-only | rg '^(alpha/|tests/)' || true
```

## Non-actions

This packet authoring lane does not run local model inference, does not run Ollama, does not rerun smoke, does not call hosted providers, does not expose or call `/v1/solve`, does not expose or call dashboard routes, does not add hosted fallback, does not add provider fallback, does not update Google Sheets, does not update backlog workbooks, and does not promote evidence.
