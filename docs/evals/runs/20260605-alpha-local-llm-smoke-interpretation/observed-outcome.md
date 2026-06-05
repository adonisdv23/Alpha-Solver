# Observed Outcome

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-INTERPRETATION-001`

## Preserved observed fields

- Execution marker: `executed: true`
- Endpoint pattern: `http://127.0.0.1:11434/api/chat`
- Timeout: `120.0`
- Adapter exception field: `null`
- Adapter output field: `output_text: "OK"`
- Adapter status field: `status: "non_evidence"`
- Adapter reason field: `reason: "local_llm_provider_adapter_wiring_only"`
- Adapter behavior evidence field: `behavior_evidence: false`
- Metadata behavior evidence field: `behavior_evidence: false`
- Raw assistant content: `OK`
- Raw response completion marker: `done: true`
- Raw response caveat: `done_reason: "length"`
- Literal terminal command: not separately preserved in the pasted artifact; not reconstructed
- Numeric process exit code: not separately preserved in the pasted artifact; no numeric exit code imported

## Observed outcome statement

The smoke evidence shows a completed command with a non-exception adapter return. The adapter result is non-evidence wiring output, not behavioral evidence.
