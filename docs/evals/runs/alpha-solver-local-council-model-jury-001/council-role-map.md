# Council Role Map

## Required local council roles

| Role | Purpose | Required output fields | Must not do |
| --- | --- | --- | --- |
| Router | Classifies the prompt route and decides whether the council should proceed, ask for clarification, or stop. | `route`, `route_rationale`, `required_roles`, `missing_context`, `initial_risk_flags` | Must not solve the task or hide ambiguity behind a route label. |
| Solver | Produces the first-pass task answer or work product within the router boundary. | `answer`, `assumptions`, `confidence`, `evidence_used`, `known_gaps` | Must not claim evidence it did not receive or use hosted-provider knowledge. |
| Critic | Reviews the solver output for logical gaps, false premises, weak assumptions, and alternate interpretations. | `agreement_points`, `disagreement_points`, `ambiguity_flags`, `suggested_revision` | Must not rewrite disagreement as a winner-take-all vote. |
| Safety / Boundary Reviewer | Checks user boundary, SAFE-OUT needs, privacy, security, regulated-domain risk, and forbidden surfaces. | `boundary_status`, `safety_flags`, `stop_reasons`, `allowed_response_shape` | Must not relax hard boundaries to make a result easier to finalize. |
| Evidence Auditor | Checks whether claims are supported by provided artifacts, cited files, or permitted local context. | `supported_claims`, `unsupported_claims`, `missing_evidence`, `citation_or_artifact_gaps` | Must not infer proof from role agreement alone. |
| Finalizer | Synthesizes only what the prior roles support and preserves disagreement as uncertainty. | `final_answer`, `agreement_summary`, `disagreement_summary`, `escalation_status`, `must_not_claim` | Must not claim council quality, model superiority, benchmark value, production readiness, or validation. |

## Required council/jury outputs

Every captured council run must include:

1. Where roles agree.
2. Where roles disagree.
3. Whether each disagreement indicates ambiguity, missing evidence, route mismatch, safety concern, or weak prompt design.
4. Whether disagreement should trigger human escalation.
5. What the finalizer is allowed to synthesize.
6. What the finalizer must not claim.

## Role sequencing

1. Router decides route and whether the prompt is eligible for council handling.
2. Solver produces first-pass output only within router constraints.
3. Critic reviews solver output and route fit.
4. Safety / Boundary Reviewer checks stop conditions independently of answer quality.
5. Evidence Auditor maps claims to artifacts and marks gaps.
6. Finalizer creates a bounded synthesis or stops inconclusive.

## Human escalation triggers by role

- Router: task is underspecified, route is contested, or local-only constraints conflict with the request.
- Solver: answer depends on missing private data, current external facts, or non-local execution.
- Critic: major alternative interpretations remain unresolved.
- Safety / Boundary Reviewer: unsafe request, privacy risk, regulated-domain risk, or boundary violation appears.
- Evidence Auditor: material claims lack evidence.
- Finalizer: disagreement remains strong enough that a stable answer would overstate support.
