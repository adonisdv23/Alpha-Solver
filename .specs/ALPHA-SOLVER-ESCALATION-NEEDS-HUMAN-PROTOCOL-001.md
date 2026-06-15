# ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001 · Needs-Human Escalation Protocol

Status: `SPEC_OK`

Type: documentation-only evaluation protocol

Lane ID: `ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001`

## Purpose

Define a docs-only protocol for identifying when an Alpha Solver evaluation output should be marked as needing human review before action. The protocol gives operators, reviewers, and future Value Read scoring work a shared vocabulary for escalation triggers, non-escalation guards, safe next actions, and non-claims.

## Scope

This spec covers only documentation and evaluation-protocol guidance for future Alpha Solver artifacts. It applies to operator-facing review packets, synthetic examples, and future scoring designs that need to represent a needs-human outcome without claiming that any runtime path has implemented or executed that outcome.

The protocol aligns with `ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001`. Future Value Read scoring artifacts must use the canonical answerability vocabulary from that contract. A needs-human case maps to:

```yaml
answerability_verdict: should_escalate
needs_human: true
```

This spec does not introduce a competing canonical answerability enum.

## Required behavior

When a future evaluator or operator packet applies this protocol, it should:

1. Identify the specific escalation trigger or triggers.
2. Confirm that a do-not-fire guard does not make escalation unnecessary.
3. Use `answerability_verdict: should_escalate` when mapping to canonical answerability artifacts.
4. Set `needs_human: true` only when a human operator, domain expert, legal/safety reviewer, data owner, or authorized decision-maker must review before action.
5. Provide a bounded `escalation_reason` that names the concrete reason for escalation.
6. Provide `next_safe_operator_action` as an action a human operator can take without making unsupported claims.
7. Record `blocked_claims_or_actions` and `missing_context_or_evidence` when those fields help prevent unsupported downstream claims.
8. Penalize over-escalation in future scoring when the task is answerable with safe assumptions, general information, refusal, or a simple clarification.

Allowed escalation-specific fields include:

- `needs_human: true`
- `escalation_reason`
- `escalation_triggers`
- `next_safe_operator_action`
- `blocked_claims_or_actions`
- `missing_context_or_evidence`

These fields are supplemental. The canonical answerability value remains `should_escalate`.

## Explicit design-only boundary

This lane is design-only and documentation-only. It does not implement runtime routing, policy routing, model routing, provider routing, SAFE-OUT behavior, dashboard behavior, public API behavior, or any `/v1/solve` behavior.

This lane does not call providers, use tokens, access credentials, mutate Google Sheets, inspect billing pages, run hosted models, run local models, expose `/v1/solve`, expose dashboard behavior, or expose public API behavior.

This lane does not create executed evidence. It does not prove Value Read success, provider validation, production readiness, public readiness, security/privacy completion, benchmark success, Alpha superiority, runtime behavior, cost behavior, latency behavior, or provider behavior.

## Evidence boundary

The companion packet at `docs/evals/runs/alpha-solver-escalation-needs-human-protocol-001/README.md` is an operator-facing design and evidence-boundary packet. It is not a run result, not an execution trace, not a benchmark artifact, and not evidence that Alpha Solver has performed needs-human escalation in production or evaluation runtime.

## Non-claims

This spec does not claim:

- runtime routing exists for needs-human escalation;
- provider calls were made;
- tokens were used;
- credentials were accessed;
- Google Sheets were read or mutated;
- `/v1/solve` exposes needs-human behavior;
- dashboard or public API behavior exists for this protocol;
- Value Read success or readiness has been achieved;
- provider validation has been completed;
- production, public, security, or privacy readiness has been completed;
- benchmark success or Alpha superiority has been demonstrated.
