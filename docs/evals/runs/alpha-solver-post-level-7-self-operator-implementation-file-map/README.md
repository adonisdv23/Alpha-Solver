# Self Operator MVP implementation file map packet

## Objective

This docs-only packet maps likely repository areas for future Self Operator MVP work. It is an implementation file map only: it identifies files, modules, tests, docs, scripts, artifacts, and CI paths that a future authorized lane may need to inspect or modify, without modifying those files now.

## Evidence boundary

This packet is documentation only. It does not modify runtime, tests, scripts, CI, API routes, provider code, dashboard routes, credentials, generated artifacts, source artifacts, or solver behavior.

## Packet files

- `source-evidence-reviewed.md` records local source evidence reviewed while creating the map.
- `likely-runtime-files.md` separates runtime files a future lane may inspect from runtime files it may modify later only with authorization.
- `likely-test-files.md` maps focused candidate tests and test areas.
- `likely-doc-files.md` maps candidate docs, specs, and operator guides.
- `forbidden-files.md` lists files and surfaces that must not change without explicit authorization.
- `implementation-scope-rules.md` defines narrow scope rules for any later implementation lane.
- `open-questions.md` captures questions a future lane must resolve before changing behavior.
- `non-actions.md` records what this packet deliberately did not do.
- `selected-next-action.md` records the selected next action decision.
- `blocker-fallback-lane.md` records the fallback lane if this packet is blocked or needs repair.
- `checks-run.md` records the requested checks.

## File-map summary

A future Self Operator MVP lane will likely begin by inspecting the local LLM operator CLI and orchestration modules, entrypoint documentation, local orchestration specs, local LLM guardrail scripts, packet consistency checks, CI guardrails, and focused local LLM tests. Modification authority is not granted by this packet; future modifications must be tied to a separate approved spec or lane.
