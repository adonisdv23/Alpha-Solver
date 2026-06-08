# Forbidden implementation scope

The future first-code lane must not perform any of the following:

- implement runtime Self Operator behavior;
- modify provider, API, dashboard, CLI, routing, SAFE-OUT, MCP, budget, determinism, replay, observability, or SolverEnvelope behavior;
- call providers or hosted models;
- make external API calls;
- configure or inspect credentials;
- automate browsers;
- deploy, release, bill, meter, or perform payment work;
- expose `/v1/solve`, dashboards, routes, or service endpoints;
- implement fallback or hosted fallback;
- modify source artifacts or promote evidence.
