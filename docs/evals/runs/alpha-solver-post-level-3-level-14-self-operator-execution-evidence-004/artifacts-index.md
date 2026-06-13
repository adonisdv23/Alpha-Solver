# Artifacts index

| File | SHA-256 | Notes |
|---|---|---|
| `candidate-task.json` | `723bba3f4598b9285618fb4b61941958c15f4fbad8b8bdea3fd630b10cf2f6ed` | Representative candidate task fixture. |
| `operator-approval-artifact.json` | `86d237bd87d4bf35f5d99cd4273e2521c2dead3b82eebf165a9640884b442c5e` | Real operator approval artifact preserved from the prompt. |
| `expected-safety-block-operator-review.json` | `b3da7200819ac027070ae1dca5aeac247d07a7d4a7b87a0c69e34fd953e7d90f` | Local expected-safety-block review artifact accepted by interpreter. |
| `artifacts/execution-gate-result.json` | `64a244d225c09afa574f90ba071af94f0bdc568e23df0b90c4c642543388f5c5` | Gate accepted approval and identity. |
| `artifacts/dry-run-result.json` | `62dcb2d50008675f3db438a9a362c8c9e6b80edac983981c8b4cda7ad20c365a` | Wrapper readiness artifact; proposed commands not executed. |
| `artifacts/result-import-summary.json` | `190e0b63bfa55ea2653829523b6e4f0fa3021f9f00a21bf71428644f9e344d3e` | Imported existing local acceptance packet. |
| `artifacts/acceptance-interpretation.json` | `dd3385e97239ddbd3b8829b409faaf73895ea28ccc1d646fe0d69a4e0e3c7dd6` | Interpretation consumed operator review and produced bounded local output. |

The dry-run wrapper artifact contains internal reusable harness metadata values for `selected_next_lane` and `blocker_fallback_lane`. Those are wrapper metadata, not this packet's controlling selected next lane. This packet's controlling next lane is recorded in `selected-next-lane.md`.
