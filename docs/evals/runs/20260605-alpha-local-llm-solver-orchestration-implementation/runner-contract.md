# Runner Contract

## Entry point

`alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration`

## Runtime boundary

The runner calls only the approved local runtime path, `run_configured_local_llm_runtime`, and therefore preserves:

- explicit local LLM opt-in;
- localhost or loopback endpoint validation;
- finite timeout validation;
- no hosted fallback;
- no provider-key requirement;
- `behavior_evidence=false`.

## Pass 1

Pass 1 asks the local backend for bounded structured gate inputs with these fields:

- `mode`
- `considerations`
- `assumptions`
- `confidence`
- `missing_information`
- `risk_flags`

Supported mode values are exactly:

- `direct`
- `clarify`
- `answer_with_assumptions`
- `block`

## Pass 1 parse and gate

The runner parses JSON first. A conservative section parser is available only for bounded label/value output without unsafe braces or oversized sections.

If Pass 1 is empty, echoed, malformed, unsafe, ambiguous, or has confidence that cannot be safely parsed for answer modes, the runner does not choose `direct` or `answer_with_assumptions`.

`answer_with_assumptions` is allowed only when confidence is parsed safely, assumptions are explicit and bounded, considerations are present, and risk remains low.

## Pass 2

Pass 2 is invoked only after a `direct` or allowed `answer_with_assumptions` gate. Runtime failure, timeout, empty output, prompt echo, system echo, malformed local runtime output, or other contract failure returns `failed_closed`.

## Normalized result

The result includes:

- `status`
- `provider_mode: local_llm`
- `orchestration_mode`
- `strategy`
- `pass_count`
- `mode`
- `considerations`
- `assumptions`
- `confidence`
- `final_answer`
- `metadata`
- `evidence_boundary`
- `behavior_evidence: false`
- `no_hosted_fallback: true`
- `no_provider_keys_required: true`
