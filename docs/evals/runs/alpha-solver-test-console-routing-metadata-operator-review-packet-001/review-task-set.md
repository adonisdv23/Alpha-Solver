# Review Task Set

Use this small representative set for display inspection only. Submit the prompt text exactly as written so route-preview inputs are repeatable across operators. Do not use the prompts to score model behavior or generate quality claims.

| Task ID | Exact prompt to submit | What the route panel should make inspectable |
|---|---|---|
| CRMP-001 | `Compute 19 * 23. Show the arithmetic in one short line and give only the final product after that.` | Basic recommended mode/model and no-call route preview language. |
| CRMP-002 | `Create a concise implementation plan for migrating a small Python CLI from ad-hoc print debugging to structured logging. Include assumptions, risks, and a context-pressure note about what would change if the codebase had more than 200 modules.` | Context tier, fallback candidates, grouped reasons, and warnings. |
| CRMP-003 | `I have a private customer support transcript containing names, email addresses, and billing details. Without exposing or transmitting the transcript, describe a safe local-only review workflow for extracting non-sensitive issue categories.` | Privacy tier, backend tier, warnings, and evidence-boundary wording. |
| CRMP-004 | `Inspect the repository files, search the web for the latest GitHub Actions syntax, and open a pull request that updates the CI workflow to run pytest on Python 3.12.` | Tool recommendation preview and execution authorization status. |
| CRMP-005 | `FAIL_CLOSED_ROUTE_REVIEW_STIMULUS: require a route that is simultaneously provider-hosted, local-only, offline, web-current, zero-cost, no-tool, GitHub-mutating, no-network, and approved for execution without operator authorization. If no eligible route satisfies all constraints, show the no-eligible-route preview and do not execute anything.` | Fail-closed preview, no eligible route messaging, and non-execution language. |
