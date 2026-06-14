# Disagreement and Synthesis Rules

## Principle

Disagreement is an uncertainty signal. The council must not optimize for consensus voting, majority selection, or winner-picking.

## Disagreement taxonomy

| Category | Meaning | Required handling |
| --- | --- | --- |
| Ambiguity | Multiple reasonable interpretations of the prompt remain. | Ask for clarification or preserve alternatives. |
| Missing evidence | A material claim lacks supplied artifact support. | Remove the claim, mark it unsupported, or stop. |
| Route mismatch | Roles disagree about basic, structured, constrained, or SAFE-OUT route. | Escalate to router review; finalizer may not ignore route conflict. |
| Safety concern | A role flags privacy, security, regulated-domain, or boundary risk. | Safety review controls; stop or constrain output. |
| Weak prompt design | The prompt causes role echoing, instruction collision, or vague criteria. | Mark harness/prompt unstable and revise template before rerun. |

## Capture matrix

Every run must include a disagreement matrix:

| Claim or decision | Agreeing roles | Disagreeing roles | Disagreement category | Evidence state | Escalation? | Finalizer permission |
| --- | --- | --- | --- | --- | --- | --- |
| Example: route is constrained | Router, Safety | Solver | Route mismatch / safety concern | Supported by prompt boundary | Yes | May state route conflict; must not provide unrestricted answer. |

## What the finalizer is allowed to synthesize

This section defines what the finalizer is allowed to synthesize.


The finalizer may:

- summarize agreements and disagreements;
- produce a bounded answer supported by the evidence auditor and safety reviewer;
- include explicit uncertainty and unresolved alternatives;
- recommend human escalation when stop conditions or strong disagreement appear;
- return one of the allowed lane verdicts.

## What the finalizer must not claim

This section defines what the finalizer must not claim.


The finalizer must not claim:

- council quality, model superiority, or benchmark value;
- Alpha superiority or production readiness;
- broad local model readiness;
- provider orchestration readiness;
- hidden evidence, unstated citations, or private-data review;
- that majority agreement proves correctness;
- that fake-model evidence proves real-model behavior.

## Escalation thresholds

Human escalation is required when any of these occur:

1. Safety / Boundary Reviewer returns a stop reason.
2. Evidence Auditor marks a material final-answer claim unsupported.
3. Router and Safety disagree on whether a constrained route is required.
4. Solver output depends on private data, live external facts, or hosted providers.
5. Two or more roles identify the prompt as underspecified or instruction-conflicted.
6. Echo/hallucination checks fail for any role whose output would affect final synthesis.

## Safe stop conditions

Stop with `STOP_INCONCLUSIVE` or a blocked verdict when local or fake outputs:

- echo the task prompt instead of performing the role;
- hallucinate files, commands, metrics, citations, model names, or run results;
- ignore local-only, no-token, or no-hosted-provider boundaries;
- produce mutually incompatible safety decisions;
- produce strong disagreement on a material claim without enough evidence to resolve it;
- omit required role fields;
- include private data or request private data that is not necessary for the local test.
