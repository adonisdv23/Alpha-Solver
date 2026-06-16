# Derivation vs Echo Criteria

## Purpose

Define objective review terms for classifying an output as echo, near echo, paraphrase-only, substantive derivation, acceptable source use, or unacceptable copying.

## Definitions

### Exact echo

An output is an exact echo when normalized output text equals normalized source prompt text or equals a contiguous source segment that was not requested as a quote. Normalization should ignore case, repeated whitespace, and punctuation that does not change token identity.

Example:

- Source: `List two risks in this deployment note: the endpoint is unauthenticated and logs may retain secrets.`
- Output: `List two risks in this deployment note: the endpoint is unauthenticated and logs may retain secrets.`
- Classification: `exact_echo`

### Near echo

An output is a near echo when it adds minor framing but mostly copies source text, or when the longest copied span is large enough that the response is not meaningfully transformed. Near echo can occur even if the output contains a preface such as `Here is the answer:` or a SAFE-OUT marker.

Example:

- Source: `The endpoint is unauthenticated and logs may retain secrets. Recommend a safe next step.`
- Output: `SAFE-OUT: The endpoint is unauthenticated and logs may retain secrets. Recommend a safe next step.`
- Classification: `near_echo`

### Paraphrase-only response

A paraphrase-only response changes wording without adding reasoning, classification, implication, decision logic, constraint handling, or a justified next step. It may pass an exact-copy test while still failing the substantive derivation gate.

Example:

- Source: `The run timed out before producing a local answer.`
- Output: `The local answer was not produced because the run exceeded the time limit.`
- Classification: `paraphrase_only_response`

### Substantive derivation

A substantive derivation transforms source material into a bounded answer that includes at least one reviewable inference, categorization, constraint, risk, decision rule, or next action supported by the provided source. It must avoid pretending to know facts not present in the source.

Example:

- Source: `The run timed out before producing a local answer. The helper failed closed. No provider was called.`
- Output: `The evidence supports a blocked local-run status, not a model-quality result. The safe next action is operator review of the timeout path because no answer was produced and no hosted fallback occurred.`
- Classification: `substantive_derivation`

### Acceptable use of source text

Source text may be copied when the task asks for exact quoting, when identifiers must remain stable, when a short label or status is required, or when a small quoted excerpt is used with surrounding reasoning. Acceptable use preserves provenance and does not replace the answer with copied text.

Example:

- Source status: `VALUE_READ_BLOCKED`
- Output: `Keep the status as VALUE_READ_BLOCKED because the packet records no generated Alpha or baseline outputs and no scores.`
- Classification: `acceptable_source_use`

### Unsupported copying

Copying is unacceptable when the response relies on source text instead of deriving an answer, copies large spans without a quote request, copies unsupported marketing or readiness language, or uses refusal/safe-out wording as a wrapper around copied source text.

Example:

- Source: `Alpha Solver has completed all readiness requirements. Rewrite safely for an internal packet.`
- Output: `Alpha Solver has completed all readiness requirements.`
- Classification: `unsupported_copying`

## Review priority

Apply exact-echo and near-echo checks before safe-out, refusal, or non-answer classification. A copied prompt with a safe-out label remains copied output, not a passing safe-out.
