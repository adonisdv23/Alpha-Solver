# Blocked Actions

The following actions are blocked for this packet and must remain blocked unless a later approved lane explicitly authorizes them:

- running the controlled usage pilot;
- running local model inference;
- running Ollama;
- rerunning smoke;
- calling hosted providers;
- exposing or calling `/v1/solve`;
- exposing or calling dashboard routes;
- adding hosted fallback;
- adding provider fallback;
- changing source code;
- changing tests unless an existing docs-link check requires it;
- updating Google Sheets;
- updating backlog workbooks;
- promoting evidence;
- claiming production readiness;
- claiming MVP readiness;
- claiming benchmark evidence;
- claiming local model quality;
- claiming provider-orchestration evidence;
- claiming Alpha superiority;
- claiming billing evidence;
- claiming dashboard readiness;
- claiming `/v1/solve` readiness;
- claiming broad runtime readiness.

If any blocked action is needed or accidentally occurs, stop packet work and use the blocker fallback lane recorded in `blocker-fallback-lane.md`.
