# Module ownership boundaries

## Static scaffold ownership

The first-code lane may own only static tests and inert fixtures created for Self Operator guardrails. Ownership is limited to proving that forbidden behaviors remain blocked.

## Runtime ownership

Runtime modules are owned by later explicit runtime lanes. The first-code lane may inspect public contracts and docs but may not change runtime modules.

## Provider and external integration ownership

Provider adapters, external API clients, hosted fallback paths, credential loading, billing integrations, browser automation, deployments, and route exposure are outside Self Operator first-code ownership.

## Evidence ownership

Evidence packets and source artifacts are preserved records. Self Operator implementation lanes may reference them but must not mutate or promote them without separate authorization.
