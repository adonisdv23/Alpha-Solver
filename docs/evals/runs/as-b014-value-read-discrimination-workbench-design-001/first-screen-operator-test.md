# First-Screen Operator Test

## 30-second comprehension check

Give an operator the first screen and 30 seconds. Without opening advanced details, the operator must answer five questions.

## Five questions

1. What packet am I looking at?
2. Is it complete enough to review?
3. What is the comparison state?
4. What is the next safe action?
5. What claims are blocked?

## Pass criteria

- The operator correctly names the packet id and path.
- The operator identifies missing artifacts or confirms completeness from displayed statuses.
- The operator distinguishes Alpha/routed and plain/baseline side status.
- The operator states exactly one next safe action.
- The operator names blocked claims without inferring readiness, value, or superiority.

## Fail criteria

- The operator thinks the workbench can run providers, local models, `/v1/solve`, scoring, unblinding, or final interpretation.
- The operator cannot identify the current packet.
- The operator mistakes route metadata for output quality proof.
- The operator believes a broad value/readiness/superiority claim is available.
- The operator sees a menu of vague actions instead of one safe action.

## Confusion risks

- Treating artifact completeness as quality evidence.
- Treating route/expert preview as proof of output value.
- Treating locked scores as final interpretation.
- Treating historical final interpretation as authorization for new interpretation.
- Treating Operator Console support docs as a real-run cockpit.

## Stop conditions

Stop if the screen implies execution, provider/model calls, `/v1/solve`, scoring, unblinding, source identity reveal, final interpretation, Google Sheets mutation, or broad claims.
