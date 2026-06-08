# Routing and Selection Requirements

## Routing boundary

This packet defines routing and selection requirements without enabling routing. No provider route is added, no existing route is modified, and no provider call is authorized by this packet.

## Required routing inputs

A future router must base selection only on allowlisted inputs such as:

- explicit operator or service configuration;
- request class and approved product-surface entrypoint;
- required capability set;
- model-set policy;
- tenant or environment policy where applicable;
- provider enabled/disabled state;
- credential availability state, not credential values;
- quota and budget state;
- circuit-breaker health state;
- safety-gate eligibility;
- provenance and observability requirements.

## Selection requirements

Future provider selection must be deterministic for identical allowed inputs. It must reject ambiguous provider choices unless a deterministic tie-breaker is specified. It must not silently switch providers, silently upgrade to hosted providers, or silently enable fallback. It must emit safe selection metadata sufficient for audit without exposing secrets or raw prompt content.

## Routing non-actions

This packet does not add provider routing, does not alter provider adapter behavior, does not expose `/v1/solve`, does not expose dashboard routes, and does not call providers. Routing remains a deferred implementation concern.
