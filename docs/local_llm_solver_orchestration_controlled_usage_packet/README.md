# Local LLM Solver Orchestration Controlled Usage Packet

## Lane

```text
ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CONTROLLED-USAGE-PACKET-001
```

## Objective

This packet defines how a future controlled usage run may be prepared, executed, captured, and reviewed for the Level 2 local LLM solver orchestration operator CLI wrapper.

This packet is documentation only. It does not execute the controlled usage run and does not start the operator-run lane.

## Prior lane completed

```text
ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-OPERATOR-CLI-WRAPPER-IMPLEMENTATION-001
```

## Command identity

The stable wrapper command identity is:

```text
python -m alpha.local_llm.operator_cli
```

The future controlled usage command shape must use this wrapper identity only, with local-only explicit settings:

```bash
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt-file ./controlled-usage-prompt.txt \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "<exact-local-model-name>" \
  --timeout-seconds "<finite-positive-timeout>"
```

## Required verification completed before this packet

Repo evidence was inspected before creating this packet and showed:

- The wrapper command identity is recorded as `python -m alpha.local_llm.operator_cli`.
- The wrapper is Level 2 operator-only, non-production, local-only, default-off, and requires explicit opt-in.
- The wrapper requires a loopback endpoint, an exact local model name, and a finite positive timeout through the existing local runtime validation path.
- The wrapper does not accept hosted-provider-key CLI flags or API-key CLI arguments.
- Existing local runtime metadata preserves `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.
- Existing source docs state that the runner is not imported by `/v1/solve` or dashboard preview routes.
- Prior lane documentation selected this controlled usage packet lane as the next lane.

## Evidence boundary

This packet does not create or promote evidence. It is not:

- local model quality evidence;
- benchmark evidence;
- readiness evidence;
- provider-orchestration evidence;
- hosted provider evidence;
- `/v1/solve` evidence;
- dashboard evidence;
- evidence-model promotion.

The packet describes future operator artifacts that may be collected only in a separately approved controlled usage operator-run lane.

## Packet files

- `allowed-scope.md` defines the allowed Level 2 operator usability scope.
- `blocked-actions.md` lists actions outside this lane.
- `preflight-checklist.md` defines required checks before a future controlled usage run.
- `operator-runbook.md` provides the future run sequence without starting it here.
- `artifact-capture-template.md` defines required artifact fields.
- `result-review-checklist.md` defines review checks for future run results.
- `stop-conditions.md` defines immediate stop conditions.
- `evidence-boundary.md` preserves the non-evidence boundary.
- `selected-next-lane.md` records the exactly one selected next lane for continuity only.
- `blocker-fallback-lane.md` records the fallback lane.
- `checks-run.md` records packet-authoring checks.
