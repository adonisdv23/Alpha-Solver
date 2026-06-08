# Provider Registry Capability Schema Packet

Lane: `ALPHA-SOLVER-POST-LEVEL-3-PROVIDER-REGISTRY-CAPABILITY-SCHEMA-PACKET-001`

## Objective

This docs-only packet defines a supporting provider registry and capability schema reference for future Alpha Solver provider orchestration work.

It records design requirements for:

- provider identity fields;
- capability labels;
- supported modes and surface compatibility;
- safety constraints;
- provenance requirements;
- local-vs-hosted labels;
- cost and quota labels; and
- disabled/default-off state requirements.

## Required preflight result

Current `main` contains the accepted Level 6 product-surface design packet in `docs/evals/runs/alpha-solver-post-level-3-level-6-product-surface-design/`.
That packet selected `ALPHA-SOLVER-POST-LEVEL-3-LEVEL-7-PROVIDER-ORCHESTRATION-DESIGN-PACKET-001` as the next design lane.

## Design status

This packet is a supporting reference only. It does not create a registry and does not decide provider orchestration behavior. Level 7 controls whether this reference is used, ignored, narrowed, or replaced.

## Evidence boundary

This packet is docs-only provider registry/capability schema design. It does not create a registry, modify provider code, call providers, configure credentials, add routing, add fallback, expose `/v1/solve`, expose dashboards, run models, run benchmarks, perform billing work, or promote evidence.

## Selected next action

`NO_FURTHER_PROVIDER_REGISTRY_CAPABILITY_SCHEMA_LANES_SELECTED`

## Blocker fallback lane

`ALPHA-SOLVER-POST-LEVEL-3-PROVIDER-REGISTRY-CAPABILITY-SCHEMA-FIX-001`

## Files in this packet

- `source-evidence-reviewed.md` records the preflight evidence reviewed.
- `registry-overview.md` summarizes the reference schema.
- `provider-identity-fields.md` defines provider identity fields.
- `capability-labels.md` defines capability labels.
- `mode-and-surface-compatibility.md` defines supported modes and surface compatibility labels.
- `local-vs-hosted-boundaries.md` defines local-vs-hosted boundaries.
- `cost-and-quota-labels.md` defines cost and quota labels.
- `disabled-default-off-state.md` defines default-off and disabled-state requirements.
- `non-actions.md` records explicit non-actions.
- `selected-next-action.md` records the closed selected next action.
- `blocker-fallback-lane.md` records the fallback lane.
- `checks-run.md` records validation commands.
