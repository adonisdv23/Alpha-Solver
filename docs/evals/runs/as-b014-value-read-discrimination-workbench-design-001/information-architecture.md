# Information Architecture

## First-screen layout in words

The first screen is a source-truth review panel, not a cockpit. It should answer:

```text
What am I reviewing?
Is it complete?
What can I safely do next?
What can I not claim?
```

## Primary cards

1. **Current packet**: packet id, packet path, packet type, lifecycle state, current decision needed, next safe action.
2. **Artifact completeness**: case packet, raw outputs, blind packet, scoring, interpretation, route metadata, receipt/capture, missing artifacts.
3. **Comparison state**: Alpha/routed side, plain/baseline side, source identity state, scoring state, interpretation state, claim boundary.
4. **Route and expert context**: task interpretation, route/expert/persona, SAFE-OUT, confidence, shortlist/fallback, missing route metadata.
5. **Claim and safety boundary**: blocked claims and whether scoring, unblinding, or final interpretation is authorized or blocked.
6. **Operator next action**: one next safe action, why safe, what it produces, what it does not authorize.

## Secondary details

- Source file list.
- Packet lineage.
- Known defects and caveats.
- Historical selected-next states.
- Check results.

## Hidden advanced details

- Full scoring rubric text.
- Full route metadata records.
- Full raw output content.
- Historical registry context.
- Capture/preflight logs.

## Above the fold

- Current packet identity and path.
- Lifecycle state.
- Completeness verdict.
- Comparison state.
- One next safe action.
- Top blocked claims.

## Not above the fold

- Long raw outputs.
- Full rubrics.
- Full route traces.
- Historical lane archaeology.
- Any provider/model/run controls.

## Copyable

- Packet id and path.
- Lifecycle state.
- Missing artifacts list.
- Claim boundary statement.
- Next safe action.
- Non-actions/non-claims summary.

## Collapsed

- Source file inventories.
- Detailed route metadata.
- Rubrics and scorer instructions.
- Historical evidence chains.

## Never shown as a button/action until separately authorized

- Run provider.
- Run local model.
- Invoke `/v1/solve`.
- Score outputs.
- Unblind results.
- Reveal source identities.
- Perform final interpretation.
- Mutate Google Sheets or external ledgers.
- Create or expose a new route, POST route, write path, queue, runner, scheduler, worker, or background job.
