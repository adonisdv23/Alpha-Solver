# Capability Matching

## Purpose

Capability matching ensures that provider selection follows task requirements and safety requirements rather than convenience, availability, or implicit defaults.

## Capability matching requirements

A future provider selection policy must define a capability matrix before runtime use. The matrix should include:

- supported task families;
- supported input and output formats;
- context-window limits;
- structured-output guarantees;
- tool-use permissions and prohibitions;
- data-locality and egress characteristics;
- deterministic or reproducibility controls;
- logging and retention behavior;
- safety filtering and refusal behavior;
- rate-limit and quota constraints;
- cost/billing profile;
- operational maturity and known limitations.

## Match outcomes

Capability matching should produce one of these outcomes:

1. **Eligible**: all mandatory task, safety, operator, and budget requirements are met.
2. **Eligible with constraints**: requirements are met only with recorded constraints that the operator can review before execution.
3. **Ineligible**: one or more mandatory requirements are not met.
4. **Unknown**: required capability evidence is absent, stale, or unverifiable.
5. **Stop**: no provider is safely selectable.

## Unknown capability rule

Unknown capability must not be treated as eligible capability. If a task requires a capability and the provider capability is unknown, the safe outcome is ineligible or stop, not optimistic routing.

## No capability bypass

Capability matching must not be bypassed by provider availability, cached success, manual convenience, or hidden fallback. Any future override must be explicit, operator-visible, bounded, and auditable.
