# Default-Off Requirements

## Required default state

Future product-surface capabilities must be disabled by default. A fresh checkout, default configuration, missing configuration, partial configuration, local developer run, test run, or documentation-only packet must not expose user-facing product surfaces.

## Default-off coverage

Default-off behavior must cover, at minimum:

- user-facing UI surfaces;
- API routes intended for external or product use;
- dashboard panels intended for operator or customer use;
- provider-backed execution paths;
- local or hosted model execution paths;
- billing or metering paths;
- evidence-promotion paths;
- automatic retries, fallbacks, or escalations that could create cost, exposure, or evidence-boundary changes.

## Unsafe default examples

Future work must reject defaults that:

- infer enablement from installed dependencies;
- infer enablement from available credentials;
- infer enablement from an open network port;
- expose placeholder or experimental screens to users;
- call providers or models before a recorded enablement decision;
- treat missing configuration as permissive.

## Required failure posture

When required enablement state is absent, malformed, ambiguous, stale, or contradictory, future product-surface work must fail closed. The expected behavior is no product exposure, no provider call, no model run, no billing action, and no evidence promotion.

## Adoption authority

Level 6 controls whether and how these default-off requirements are adopted.
