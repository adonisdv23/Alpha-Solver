# Audit and Traceability Requirements

## Audit trail display requirements

A future dashboard audit display must show:

- Packet lane identifier.
- Packet path.
- Source artifact links.
- Selected next action or selected next lane.
- Blocker fallback lane.
- Evidence boundary summary.
- Non-actions summary.
- Checks recorded for the packet.
- Commit or artifact provenance when available.
- Whether the displayed state is accepted, draft, historical, closed, or blocked.

## Traceability requirements

Every dashboard statement must trace to a file, packet, or accepted source artifact. If a dashboard cannot trace a statement to an authoritative source, it must display the statement as unavailable or blocked rather than infer it.

## Historical-state preservation

A future dashboard must preserve historical closed decisions. It must not replace a closed `NO_FURTHER_*_LANES_SELECTED` action with a later planning lane unless the source artifact explicitly records that transition.

## Audit mutation boundary

This packet defines display requirements only. It does not create audit-write APIs, dashboard routes, UI code, mutation controls, runtime hooks, provider calls, model calls, benchmark runs, billing work, `/v1/solve` exposure, or evidence promotion.
