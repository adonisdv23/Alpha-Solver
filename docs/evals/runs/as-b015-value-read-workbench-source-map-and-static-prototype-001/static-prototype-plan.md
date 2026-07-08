# Static Prototype Plan

## Prototype purpose

Create a static, non-interactive representation of the Value Read / discrimination workbench first screen so an operator can understand source status, comparison posture, route context, claim boundaries, and one next safe action before any runtime or UI implementation.

## First-screen layout

1. Header: lane/packet id, selected next state, and non-runtime banner.
2. Current packet card.
3. Artifact completeness card.
4. Comparison state card.
5. Route/expert context card.
6. Claim boundary card.
7. One next safe action card.
8. Blocked actions footer.

## Static data assumptions

The mockup uses static fixture text copied from committed source-map tables. It does not parse packets, watch files, execute commands, call providers, or fetch external data. Unknown fields are displayed as `unknown`, `packet family only`, or `future_required`.

## Source-map inputs

Inputs are `source-map-table.md`, `field-inventory.md`, `status-taxonomy.md`, `data-readiness-rules.md`, and `claim-boundary-map.md`.

## Display sections

- Current packet identity and lifecycle.
- Completeness status for required artifact categories.
- Alpha/routed versus plain/baseline comparison status.
- Route/expert/SAFE-OUT/confidence diagnostic status.
- Claim and non-action boundaries.
- One next safe operator action.

## Collapsed details

Static collapsed details may be represented as Markdown headings or placeholder sections, not interactive UI. Details include source file inventory, packet lineage, long rubrics, route metadata, raw outputs, and check logs.

## Copyable fields

Packet id, packet path, lifecycle state, missing artifact list, claim boundary statement, selected next state, recommended next lane, and next safe action.

## Blocked actions

Provider calls, hosted/local model calls, `/v1/solve`, routes, POST routes, write paths, runtime jobs, scoring, unblinding, source identity reveal, final interpretation, Google Sheets mutation, and broad claims remain blocked.

## Operator comprehension target

Within 30 seconds, an operator can answer: what am I reviewing, is it complete, what can I safely do next, and what can I not claim.

## Future implementation lane needs

A future implementation would need explicit operator approval, a parser/inventory for committed packet sources, a fixture/source adapter, a claim-boundary rendering contract, preservation checks for registries, and no runtime/provider/scoring behavior unless separately authorized.
