# Blocked State Copy

## Required blocked action text

A blocked action must use copy equivalent to:

> Blocked: the Self Operator cannot continue because the requested action crosses an approval, evidence, safety, provider, credential, or path boundary.

## Required blocked state fields

- Blocked state label.
- Plain-language reason.
- Boundary or rule that prevented continuation.
- Whether any artifacts were created before the block.
- Artifact or log location, if available.
- Required operator decision or fallback lane.

## Required fallback copy

For unresolved acceptance packet issues, the UX packet records this fallback lane:

`ALPHA-SOLVER-POST-LEVEL-3-LEVEL-8-SELF-OPERATOR-OPERATOR-UX-ACCEPTANCE-FIX-001`

## Provider boundary block

If a task would require a provider call not explicitly approved, the required blocked copy is:

> Blocked: this action would require a provider call or credential use that is outside the approved boundary. No provider call was made. Route to an approved provider lane before retrying.
