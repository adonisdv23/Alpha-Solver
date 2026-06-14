# Fake-Model Test Evidence

## Verdict

`LOCAL_COUNCIL_MODEL_JURY_DESIGNED_NOT_EXECUTED`

## What was captured

This packet captures fake-model test templates, expected role fields, disagreement matrix requirements, and stop conditions. It does not add executable harness code and does not run model inference.

## Fake role fixture templates

### Fake router output

```json
{
  "role": "router",
  "route": "constrained",
  "route_rationale": "The prompt has missing evidence and local-only constraints.",
  "required_roles": ["solver", "critic", "safety_boundary_reviewer", "evidence_auditor", "finalizer"],
  "missing_context": ["source artifact for claimed result"],
  "initial_risk_flags": ["missing_evidence"]
}
```

### Fake solver output

```json
{
  "role": "solver",
  "answer": "Draft a bounded response that states evidence is missing.",
  "assumptions": ["No hosted providers are available."],
  "confidence": "low",
  "evidence_used": ["operator prompt only"],
  "known_gaps": ["no local model output artifact"]
}
```

### Fake critic output

```json
{
  "role": "critic",
  "agreement_points": ["local-only boundary is required"],
  "disagreement_points": ["solver confidence may be overstated"],
  "ambiguity_flags": ["execution versus design scope could be confused"],
  "suggested_revision": "Use a design-only verdict and avoid execution claims."
}
```

### Fake safety / boundary reviewer output

```json
{
  "role": "safety_boundary_reviewer",
  "boundary_status": "constrained",
  "safety_flags": ["no hosted providers", "no private data", "no /v1/solve"],
  "stop_reasons": [],
  "allowed_response_shape": "design packet with non-claims"
}
```

### Fake evidence auditor output

```json
{
  "role": "evidence_auditor",
  "supported_claims": ["roles were defined", "rules were documented"],
  "unsupported_claims": ["real local model behavior was tested"],
  "missing_evidence": ["executable harness output", "local model transcripts"],
  "citation_or_artifact_gaps": ["no model stdout artifact"]
}
```

### Fake finalizer output

```json
{
  "role": "finalizer",
  "final_answer": "Local council model-jury design is captured, but not executed.",
  "agreement_summary": ["all roles preserve local-only boundary"],
  "disagreement_summary": ["confidence in behavior remains unresolved without execution"],
  "escalation_status": "no escalation for design; escalation required before real-model claims",
  "must_not_claim": ["no benchmark-value claim is supported", "no model-superiority claim is supported", "no production-readiness claim is supported"]
}
```

## Expected fake test assertions for a future harness

- All six roles are present.
- Every role emits its required fields.
- The disagreement matrix contains at least one explicit agreement and one explicit disagreement or `none_observed` marker.
- Strong disagreement maps to a taxonomy category.
- Unsupported material claims are excluded from the final answer.
- Finalizer `must_not_claim` records forbidden non-claims with immediate boundary wording: no council-quality claim is supported, no model-superiority claim is supported, no benchmark-value claim is supported, and no production-readiness claim is supported.
- These are forbidden non-claims from a docs-only, fake-fixture packet, not observed evidence.
- Any missing role, echo output, or boundary violation returns `STOP_INCONCLUSIVE`.

## Evidence limitation

Fake fixtures can test schema and stop-state mechanics only. They are not observed evidence for answer quality, local model reliability, benchmark value, model superiority, production readiness, provider readiness, or local model behavior.
