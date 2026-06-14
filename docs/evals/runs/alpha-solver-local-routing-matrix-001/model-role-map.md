# Model Role Map

Candidate roles are local-only experiment roles. Families are mapped as candidates from the prior catalog without claiming performance, reliability, safety, or superiority.

## Canonical role glossary

Use these canonical role IDs in routing artifacts. Aliases are documentation conveniences only; future execution records should store the canonical ID.

| Canonical role ID | Purpose | Candidate model-family type | Required evidence before use | Stop condition | Forbidden claims |
| --- | --- | --- | --- | --- | --- |
| `router` | Select the task category and ordered route, including selected and rejected route rationale. | Broad instruction-following generalist families such as Llama, Qwen, or Mistral/Nemo. | Frozen routing task bank, expected route labels, selected/rejected rationale, uncertainty, misroute log. | Missing label schema, low confidence without escalation, prompt echo, empty output, hosted key present, non-loopback endpoint. | Routing success, production routing readiness, autonomous routing reliability. |
| `classifier` | Apply a frozen label set when the task is primarily classification rather than multi-role solving. | Smaller or broad generalist families with deterministic label-following behavior, such as Llama, Qwen, Gemma, or Mistral/Nemo. | Label schema, gold labels, confidence/ambiguity threshold, confusion log. | Output outside schema, ambiguous task above threshold, high-impact classification requiring human review. | Reliable automation, production classifier readiness, fairness or safety validation. |
| `first_pass_solver` | Produce an initial answer, plan, or option set for non-blocked non-summary tasks. | Generalist or reasoning-capable families such as Llama, Qwen, Gemma, Mistral/Nemo, Hermes, or DeepSeek-R1 related. | Prompt/output logs, non-echo checks, task-category fit, rubric for task-fit and calibration. | Unsafe request, missing critical constraints, empty output, unsupported high-confidence claim. | Answer correctness, model quality, value, superiority. |
| `first_pass_summarizer` | Compress or restate supplied content while preserving verdicts, boundaries, and source claims. | Concise generalist/summarizer candidates such as Llama, Qwen, Gemma, or Mistral/Nemo. | Source artifact hash or path, summary output, fidelity checklist, no-new-claims review. | Adds unsupported claims, changes verdict, omits evidence boundary, source unavailable. | Lossless summary, legal/compliance reliability, new evidence. |
| `planner` | Sequence work, dependencies, validations, stop conditions, and non-actions before execution. | Generalist planning candidates such as Llama, Qwen, Mistral/Nemo, or Hermes. | Lane instructions, dependency list, proposed steps, validation plan, explicit non-actions. | Required authorization missing, dependency unmet, broad eval requested, model-call precondition unmet. | That planned work has been executed, implementation readiness, success guarantee. |
| `code_reviewer` | Review code-oriented outputs for repo fit, testability, scope, and implementation risk. | Code-oriented or code-capable families such as Qwen Coder, Qwen, DeepSeek-R1 related, or Llama. | Code prompt, file paths, patch plan or diff, test expectations, human/code-review checklist. | Security-sensitive code, behavior change without spec, failing tests not understood, broad refactor pressure. | Code correctness, merge readiness, security validation. |
| `critic` | Identify gaps, contradictions, hallucination risk, weak reasoning, or missing constraints in another output. | Critique/reasoning candidates such as DeepSeek-R1 related, Hermes, Qwen, Qwen Coder, or Llama. | Paired first-pass/critique artifacts, issue taxonomy, calibrated flags, disagreement handling. | Fabricates issues, fails to cite input evidence, cannot distinguish uncertainty from error. | Judge reliability, truth verification, benchmark validity. |
| `evidence_audit_critic` | Compare claims to artifacts and identify unsupported, contradicted, or overbroad claims. | Critique/audit-capable families such as DeepSeek-R1 related, Hermes, Qwen, or Llama. | Claim list, source artifacts, citation map, unsupported-claim register, conflict log. | Missing artifacts, uncited claims, conflict between sources, pressure to convert gaps into validation. | Validation, readiness, superiority, benchmark or value evidence. |
| `safety_boundary_reviewer` | Check safety, privacy, credential, refusal, and evidence-overclaim boundaries before content is finalized. | Boundary-check candidates such as Gemma, Llama, Qwen, or other generalist safety-review candidates. | Gold boundary prompts, expected labels, fail-closed reason codes, no-private-data confirmation. | Unsafe compliance, credential/API-token request, private data exposure risk, hosted key present. | Safety validation, policy completeness, production readiness. |
| `final_synthesizer` | Merge selected route output, critique, safety/boundary notes, and evidence caveats into final user-facing text. | Strong generalist/synthesis candidates such as Llama, Qwen, Gemma, Mistral/Nemo, or Hermes. | Source-linked synthesis inputs, claim-preservation checklist, final non-claims, unresolved-risk notes. | Inconsistent source packets, missing verdict, unsupported unifying claim, high-stakes unresolved conflict. | Final-answer superiority, new evidence, resolved contradictions without support. |

## Alias table

| Alias used in earlier draft or human prose | Canonical role ID |
| --- | --- |
| Router | `router` |
| router/classifier | `router` + `classifier` |
| Classification-only | `classifier` |
| first-pass solver | `first_pass_solver` |
| Direct solver | `first_pass_solver` |
| Direct first-pass-only route | `first_pass_solver` only |
| first-pass summarizer | `first_pass_summarizer` |
| summarizer-only route | `first_pass_summarizer` only |
| planner | `planner` |
| planning | `planner` |
| code reviewer | `code_reviewer` |
| critic | `critic` |
| critic review | `critic` |
| evidence audit critic | `evidence_audit_critic` |
| safety reviewer | `safety_boundary_reviewer` |
| safety-only route | `safety_boundary_reviewer` only |
| safety_boundary_reviewer | `safety_boundary_reviewer` |
| final synthesizer | `final_synthesizer` |
| judge candidate | No canonical execution role in this matrix; future judge work belongs to the selected council/model-jury lane and is rejected here as out of scope. |
| judge-only route | No canonical execution role in this matrix; rejected as out of scope for this packet. |
| full council | No canonical execution role in this matrix; future council work is gated by `ALPHA-SOLVER-LOCAL-COUNCIL-MODEL-JURY-001`. |
