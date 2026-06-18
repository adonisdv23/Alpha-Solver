# Defects and caveats

- The packet is built from manual prompt-contract simulation artifacts only.
- The scorer-facing task statement is limited to task ID and task-family summary because the committed output artifacts do not include full original task prompts in each output file.
- Routed source route metadata is intentionally excluded from the scorer-facing packet.
- This lane does not score, unblind, interpret, compute winners, compute totals, execute runtime, call providers, run hosted/local models, execute tools, browse, mutate Sheets, deploy, or make readiness, benchmark, production/public, quality, security/privacy, autonomous-readiness, or superiority claims.
