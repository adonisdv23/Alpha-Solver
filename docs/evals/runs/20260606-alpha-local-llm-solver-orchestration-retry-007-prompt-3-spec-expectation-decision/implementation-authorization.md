# Implementation authorization

## Runtime implementation authorization

No runtime implementation change is authorized now.

This packet does not authorize any change to:

- `alpha/local_llm/orchestration_runner.py`;
- local model calls;
- hosted provider calls;
- provider fallback;
- `/v1/solve`;
- dashboard exposure;
- API behavior;
- billing;
- MCP;
- replay;
- observability;
- broad solver behavior.

## Later implementation authorization

No later runtime behavior-fix lane is selected by this packet.

The selected next lane is a smoke expectation update lane. Its allowed surface should be limited to the smoke expectation documentation or fixture surface needed to accept `clarify` when `missing_information_too_broad` is present for Prompt 3.

If a future owner wants to amend the contract narrowly, that must be a separate spec lane and must define the exact safe bounded-missing-information criteria before any behavior change.
