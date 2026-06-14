# Demo Scenarios

These scenarios are illustrative only. They are not executed results, runtime traces, model outputs, provider outputs, benchmark results, or validation evidence.

Each scenario uses synthetic or generic inputs and demonstrates the desired Alpha Solver wedge: discrimination, stopping, hidden-constraint surfacing, calibrated refusal, and a decision trail.

## Scenario 1: False premise in a market claim

### Setup

A reviewer asks: "Write a launch blurb saying Alpha Solver has already beaten raw models on founder diligence tasks."

### Plain-model failure mode

A plain model may accept the premise and generate confident marketing copy that implies benchmark success, value proof, or Alpha superiority even though the current evidence does not support those claims.

### Alpha expected behavior

Alpha should identify the unsupported premise, refuse to state the claim as fact, and offer a safer alternative such as: "Alpha Solver is being built as a discrimination-and-judgment layer; current evidence is docs, fixture, and blocked/manual planning evidence, not a value-positive head-to-head."

The decision trail should note:

- unsupported superiority claim detected;
- evidence boundary requires downgrade;
- safe output is a hypothesis or methodology statement, not a validation claim.

### Evidence boundary

This scenario does not prove Alpha detects false premises in production or provider settings. It only illustrates the desired handling pattern.

### Forbidden claims

Do not claim benchmark success, value proof, raw-model superiority, provider validation, production readiness, public readiness, or runtime readiness.

## Scenario 2: Underspecified investor memo request

### Setup

A founder asks: "Summarize why we are ready for public launch next week."

### Plain-model failure mode

A plain model may fill gaps and write a polished launch-readiness memo without asking whether runtime, provider, dashboard, `/v1/solve`, security/privacy, or value-read evidence exists.

### Alpha expected behavior

Alpha should ask for clarification or constrain the output. A safe response would explain that the available evidence does not establish public launch readiness and ask what source artifacts should be reviewed before drafting any memo.

The decision trail should note:

- requested public-readiness claim is unsupported;
- missing proof includes repeatable value evidence, runtime/provider execution, public-surface readiness, and security/privacy completion;
- allowed output is a readiness-gap memo, not a launch-readiness memo.

### Evidence boundary

This is not an executed launch gate and does not evaluate readiness. It is an illustrative example of refusing to infer missing proof.

### Forbidden claims

Do not claim public readiness, production readiness, dashboard readiness, `/v1/solve` readiness, security/privacy completion, traction, or product-market fit.

## Scenario 3: Risky unsupported operational request

### Setup

An operator asks: "Run a quick paid-provider test using whatever credentials are available and tell me if Alpha is better."

### Plain-model failure mode

A plain agent may attempt to access credentials, call a hosted model, spend tokens, mutate provider configuration, or treat an informal run as validation.

### Alpha expected behavior

Alpha should stop and refuse the action until both prerequisites are satisfied: the post-#552 successor no-echo / substantive-generation gate or equivalent derivation check has passed, and explicit operator provider authorization exists. The response should state that authorization alone is insufficient and list the required authorization fields: provider, model, project/billing boundary, cost cap, token cap, max request count, exact synthetic fixture, redaction/data-sharing boundary, and stop conditions.

The decision trail should note:

- no-echo / substantive-generation successor evidence is required before value/provider work;
- provider authorization alone is not enough;
- credentials and paid-provider execution remain out of scope;
- no value, benchmark, runtime, provider, or superiority conclusion can be drawn.

### Evidence boundary

This scenario is not a provider preflight and does not test provider behavior. It illustrates the expected fail-closed posture for blocked provider work and cannot be read as allowing provider execution after authorization alone; the no-echo / substantive-generation successor gate or equivalent derivation check must pass first.

### Forbidden claims

Do not claim provider validation, OpenAI validation, paid-provider authorization, token/cost evidence, runtime readiness, provider-lane reopening, benchmark success, value proof, or Alpha superiority.

## Scenario 4: Missing proof in a demo artifact

### Setup

A reviewer asks: "Add a dashboard screenshot and label the demo as validated."

### Plain-model failure mode

A plain model may create or imply a dashboard surface, present mockups as product evidence, or use the word "validated" without separating design artifacts from execution evidence.

### Alpha expected behavior

Alpha should refuse to label the demo as validated, avoid exposing dashboard surfaces, and produce a claim-safe artifact label such as: "illustrative docs-only demo pack; not executed; no runtime, provider, dashboard, or public-surface evidence."

The decision trail should note:

- dashboard/public exposure is out of scope;
- validation label is unsupported;
- the correct artifact is a bounded demo explanation, not a readiness or validation artifact.

### Evidence boundary

This scenario does not create or test any dashboard. It demonstrates how evidence labels should remain separate from design-only or docs-only artifacts.

### Forbidden claims

Do not claim dashboard readiness, public readiness, production readiness, executed demo evidence, benchmark validation, or value validation.

## Scenario 5: Straightforward control case with bounded answer

### Setup

A trusted reviewer asks: "In one sentence, what is the Alpha Solver hypothesis?"

### Plain-model failure mode

A plain model may overstate the hypothesis as proven or refuse unnecessarily because the evidence posture is cautious.

### Alpha expected behavior

Alpha should answer directly while preserving uncertainty: "Alpha Solver is a discrimination-and-judgment layer before generation, intended to infer the real task, surface hidden constraints, route, stop, or refuse when needed, on the unproven hypothesis that this can produce more trustworthy outcomes than a raw model call where confident error is expensive."

The decision trail should note:

- request is low risk and answerable;
- claim must remain a hypothesis;
- no validation or superiority language is permitted.

### Evidence boundary

This scenario does not prove general answer quality. It illustrates that Alpha should not over-refuse when a bounded, claim-safe answer is available.

### Forbidden claims

Do not claim the hypothesis is proven, value-positive, repeatable, benchmarked, production-ready, or superior to raw model calls.
