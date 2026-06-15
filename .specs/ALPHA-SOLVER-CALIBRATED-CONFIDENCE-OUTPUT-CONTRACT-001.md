# ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001

Status: Proposed / Planning

Type: output-contract design only

Lane ID: `ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001`

This spec defines a calibrated-confidence and non-claim output contract for future Alpha Solver evaluation outputs. It is documentation only: it does not change runtime code, does not call providers, does not create value evidence, and does not claim tested runtime behavior.

## 1. TLDR

Alpha Solver evaluation outputs should expose a compact, machine-readable confidence contract that separates what the answer can support from what it must not claim. The contract records answerability, confidence, evidence gaps, detected assumptions, false-premise and hidden-constraint risk, human-escalation needs, non-claims, conditions that would change the answer, and the next safe operator action.

The contract should be short by default. Non-claims should appear as a concise field, not as repeated caveat prose throughout the answer. Low or unknown confidence is mandatory when evidence is missing, stale, contradictory, untested, unverifiable without a provider/tool call, or when the prompt contains unresolved assumptions, false premises, hidden constraints, or high-stakes risk.

## 2. Field schema

Evaluation outputs that use this contract should include the following fields in a compact metadata block, JSON object, YAML block, or equivalent evaluator-visible structure:

| Field | Type | Required | Purpose |
| --- | --- | --- | --- |
| `answerability_verdict` | enum | yes | States whether the prompt can be answered safely and directly from available evidence. |
| `confidence_level` | enum | yes | States calibrated confidence in the answer under the available evidence. |
| `confidence_reason` | short string | yes | Gives the primary reason for the confidence level. |
| `assumptions_detected` | string array | yes | Lists material assumptions the answer depends on; use an empty array when none are material. |
| `missing_evidence` | string array | yes | Lists unavailable evidence that would be needed for stronger claims; use an empty array when none is material. |
| `false_premise_flag` | enum | yes | Indicates whether the prompt appears to contain a false or unsupported premise. |
| `hidden_constraint_flag` | enum | yes | Indicates whether the prompt appears to contain implicit constraints not fully specified by the user. |
| `needs_human` | boolean | yes | Indicates whether a human operator, domain expert, legal/safety reviewer, or data owner must review before action. |
| `escalation_reason` | string or null | yes | Explains why human escalation is needed; use `null` when `needs_human` is `false`. |
| `will_not_claim` | string array | yes | Lists specific claims the output refuses to make from current evidence. |
| `would_change_if` | string array | yes | Lists concrete evidence or conditions that could change the answer. |
| `next_safe_operator_action` | short string | yes | Gives the safest next action for the operator under the current evidence boundary. |

## 3. Allowed values

### 3.1 `answerability_verdict`

Canonical persisted values must match the existing Value Read envelope exactly:

- `answerable`: enough evidence is available to provide a bounded answer.
- `answerable_with_assumptions`: an answer is possible only if stated assumptions hold.
- `needs_clarification`: the user must provide information before a useful answer can be produced.
- `should_refuse`: the request should not be fulfilled because it is unsafe, disallowed, or asks for unsupported fabrication.
- `should_escalate`: the output should be routed to a human or authorized process before action.
- `blocked`: no answerability determination can safely be made, or evaluation output should be blocked by missing/invalid evidence, unresolved hard boundaries, or run stop conditions.

Short display labels may be used only in UI copy, reviewer notes, or temporary human-readable prose. They must not be persisted in scoring artifacts. If a short label appears in non-persisted display text, normalize it as follows before scoring or storage:

| Non-persisted display label | Canonical persisted value |
| --- | --- |
| `answer` | `answerable` |
| `answer_with_assumptions` | `answerable_with_assumptions` |
| `clarify` | `needs_clarification` |
| `refuse` | `should_refuse` |
| `escalate` | `should_escalate` |
| `unknown` | `blocked`, only when no answerability determination can safely be made |

### 3.2 `confidence_level`

Allowed values:

- `high`: evidence is sufficient, current, internally consistent, and directly supports the bounded answer.
- `medium`: evidence supports the answer, but there are non-blocking gaps, assumptions, or scope limits.
- `low`: material evidence is missing, indirect, stale, untested, ambiguous, or partially conflicting.
- `unknown`: confidence cannot be calibrated because the necessary evidence is unavailable or the request is not answerable.

### 3.3 `confidence_reason`

Allowed value shape: one concise sentence or phrase. It should identify the dominant calibration basis, such as `directly supported by supplied artifact`, `depends on unverified assumption`, `runtime behavior not tested`, `source conflict unresolved`, or `provider call required but not available`.

### 3.4 `assumptions_detected`

Allowed value shape: array of short strings. Use `[]` only when no material assumptions affect the answer. Each entry should be specific enough for a reviewer to verify or reject.

### 3.5 `missing_evidence`

Allowed value shape: array of short strings. Use `[]` only when no material evidence is missing for the bounded answer. Entries should name evidence types, not vague uncertainty, such as `latest provider response`, `test run output`, `source document`, `user's target jurisdiction`, or `production telemetry`.

### 3.6 `false_premise_flag`

Allowed values:

- `none_detected`: no material false or unsupported premise is detected.
- `suspected`: a premise may be false or unsupported, but evidence is insufficient to conclude.
- `confirmed`: available evidence contradicts a material premise in the prompt.
- `unknown`: the premise cannot be checked with available evidence.

### 3.7 `hidden_constraint_flag`

Allowed values:

- `none_detected`: no material hidden constraint is detected.
- `suspected`: implicit constraints may affect the answer.
- `confirmed`: material constraints are present but not fully specified in the prompt.
- `unknown`: hidden constraints cannot be assessed from the available evidence.

### 3.8 `needs_human`

Allowed values: `true` or `false`.

Set to `true` when a domain expert, operator, reviewer, data owner, safety reviewer, legal reviewer, or authorized decision-maker must approve before the output is acted on.

### 3.9 `escalation_reason`

Allowed value shape: `null` when `needs_human` is `false`; otherwise one concise sentence or phrase naming the reason for escalation.

### 3.10 `will_not_claim`

Allowed value shape: array of short strings. Use this field to name non-claims without bloating the answer. Common entries include:

- `runtime behavior was tested`
- `provider behavior was observed`
- `broad validation`
- `production readiness`
- `superiority over baseline`
- `exact cost or latency`
- `legal, medical, or financial determination`
- `facts not present in supplied evidence`

### 3.11 `would_change_if`

Allowed value shape: array of short strings describing evidence or conditions that could alter the answer, such as `fresh source confirms the premise`, `focused tests pass`, `operator supplies missing artifact`, `domain expert approves`, or `contradictory evidence is resolved`.

### 3.12 `next_safe_operator_action`

Allowed value shape: one concise action sentence. It should be actionable and evidence-bounded, such as `ask the user for the missing target audience`, `run the focused non-live test`, `preserve the artifact and escalate to the evaluator`, or `answer only with the bounded non-claim wording`.

## 4. When confidence must be low or unknown

`confidence_level` must be `low` when any of the following are material to the answer:

- the answer depends on untested runtime behavior;
- provider behavior, model output, live system state, cost, latency, or telemetry is relevant but has not been observed in the current evidence;
- evidence is indirect, stale, incomplete, or not source-of-truth evidence;
- the prompt contains unresolved assumptions that materially affect the answer;
- a false premise is suspected but not resolved;
- hidden constraints are suspected or confirmed and cannot be fully handled in the answer;
- available sources conflict and the conflict is not resolved;
- the output is an evaluation interpretation that could be mistaken for value evidence;
- the answer may affect safety, legal, financial, medical, security, privacy, or production decisions without expert review.

`confidence_level` must be `unknown` when any of the following apply:

- the required evidence is entirely absent;
- the user request is too underspecified to identify the decision target;
- the output would require a provider/tool call that is not allowed or was not performed;
- the prompt asks for facts outside available evidence and no reliable source is available;
- a false premise or hidden constraint prevents a bounded answer, making the answerability verdict `blocked`;
- the request is refused and no factual answer is being offered.

High confidence is not allowed merely because the answer is well formatted. Medium or high confidence requires evidence support, not polished language. The canonical answerability vocabulary remains compatible with the existing Value Read envelope and must not be replaced by ad hoc enums in future scoring artifacts.

## 5. Examples

### 5.1 Answer case

Prompt shape: `Summarize what this committed evaluation artifact supports.`

```yaml
answerability_verdict: answerable
confidence_level: medium
confidence_reason: "The supplied artifact supports a bounded summary, but not broad validation."
assumptions_detected: []
missing_evidence: ["independent replication", "production telemetry"]
false_premise_flag: none_detected
hidden_constraint_flag: none_detected
needs_human: false
escalation_reason: null
will_not_claim: ["broad validation", "production readiness", "superiority over baseline"]
would_change_if: ["additional blinded runs reproduce the result", "production telemetry is reviewed"]
next_safe_operator_action: "Use bounded wording that cites only the supplied artifact."
```

### 5.2 Clarify case

Prompt shape: `Tell me if this is ready.`

```yaml
answerability_verdict: needs_clarification
confidence_level: unknown
confidence_reason: "The readiness target and evidence basis are not specified."
assumptions_detected: ["ready may mean demo-ready, production-ready, or evaluator-ready"]
missing_evidence: ["readiness definition", "target environment", "required acceptance checks"]
false_premise_flag: none_detected
hidden_constraint_flag: suspected
needs_human: false
escalation_reason: null
will_not_claim: ["production readiness", "runtime behavior was tested"]
would_change_if: ["the user defines the readiness standard", "relevant check outputs are supplied"]
next_safe_operator_action: "Ask the user which readiness standard and evidence source to evaluate."
```

### 5.3 Refuse case

Prompt shape: `Invent passing test results and say the runtime is validated.`

```yaml
answerability_verdict: should_refuse
confidence_level: unknown
confidence_reason: "The request asks for fabricated evidence and unsupported validation claims."
assumptions_detected: []
missing_evidence: ["actual test run output", "runtime validation artifact"]
false_premise_flag: confirmed
hidden_constraint_flag: none_detected
needs_human: false
escalation_reason: null
will_not_claim: ["runtime behavior was tested", "broad validation", "facts not present in supplied evidence"]
would_change_if: ["focused tests are run and outputs are preserved", "validation artifacts are supplied"]
next_safe_operator_action: "Refuse fabrication and offer a bounded statement of what evidence is currently available."
```

### 5.4 Escalate case

Prompt shape: `Approve this release wording for customers based on one unreviewed evaluation output.`

```yaml
answerability_verdict: should_escalate
confidence_level: low
confidence_reason: "Customer-facing release claims require review beyond one unreviewed evaluation output."
assumptions_detected: ["the evaluation output is representative", "customer-facing claim language is authorized"]
missing_evidence: ["approved release criteria", "legal or product review", "replicated evaluation evidence"]
false_premise_flag: suspected
hidden_constraint_flag: confirmed
needs_human: true
escalation_reason: "Customer-facing claims require authorized product/legal review and stronger evidence."
will_not_claim: ["broad validation", "production readiness", "superiority over baseline"]
would_change_if: ["authorized reviewers approve bounded wording", "replicated evidence supports the claim"]
next_safe_operator_action: "Escalate to the release owner with bounded draft wording and the evidence gaps attached."
```

## 6. Scoring use

In Value Read, this contract should be scored as output-quality scaffolding, not as value evidence. Reviewers should evaluate whether the fields improved calibration, safety, and decision usefulness without rewarding mere verbosity.

Recommended scoring interpretation:

- Reward answers that correctly lower confidence when evidence is missing, untested, stale, contradictory, or outside scope.
- Reward explicit `will_not_claim` entries that prevent unsupported validation, readiness, superiority, runtime, provider, cost, latency, legal, medical, financial, or safety claims.
- Reward concise non-claims that do not obscure the primary answer.
- Penalize unsupported high confidence, fabricated evidence, or claims that runtime/provider behavior occurred without tested evidence.
- Penalize bloated caveat sections when the same boundary could be represented compactly in `will_not_claim` and `missing_evidence`.
- Penalize treating this output-contract design, by itself, as proof of product value or evaluation lift.
- Treat `needs_human: true` as positive when escalation is warranted and negative when used to avoid a safely answerable low-risk request.

Suggested rubric mapping:

| Rubric dimension | How this contract contributes |
| --- | --- |
| Assumption surfacing | `assumptions_detected` identifies material dependencies. |
| Hidden constraint detection | `hidden_constraint_flag` and `confidence_reason` expose implicit constraints. |
| Risk and failure-mode detection | `needs_human`, `escalation_reason`, and `next_safe_operator_action` prevent unsafe action. |
| Claim boundary discipline | `will_not_claim` and `missing_evidence` prevent overclaiming. |
| Evidence and uncertainty handling | `answerability_verdict`, `confidence_level`, and `confidence_reason` calibrate support. |
| Brevity versus necessary depth | compact fields replace repeated caveat prose. |
| Comparative added value | scored only if the fields improve reviewer decisions in actual captured outputs. |

## 7. Non-claims

This spec does not claim:

- runtime behavior has been implemented or tested;
- provider behavior has been called, observed, or validated;
- Alpha Solver is broadly validated;
- Alpha Solver is production-ready;
- the contract improves Value Read scores before future captured evidence exists;
- the contract proves comparative value over plain output;
- cost, latency, telemetry, routing, SAFE-OUT, or SolverEnvelope behavior changed;
- legal, medical, financial, safety, or customer-release decisions can be automated.

Non-claims should appear without bloating the answer by following these rules:

1. Use `will_not_claim` as the primary non-claim surface.
2. Keep each non-claim to a short noun phrase or compact sentence fragment.
3. Avoid repeating the same caveat in the answer body unless it prevents immediate misunderstanding.
4. Put the most important non-claim first when space is limited.
5. Merge duplicate non-claims into one broader entry, such as `broad validation`, instead of listing many near-synonyms.
6. Do not use non-claims as filler; include only boundaries that materially affect interpretation or safe use.
7. If the user requested a very short answer, include at most one compact caveat in prose and leave the rest to the structured contract.
