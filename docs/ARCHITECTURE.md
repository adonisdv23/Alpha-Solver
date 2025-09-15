# Architecture

Alpha Solver routes user requests through scoring, gates, and optional MCP tools before reaching an LLM. Key steps:

- Input → router selects a path.
- **RES-03 scoring** evaluates candidates.
- **RES-04 gates** enforce allow/deny.
- Low confidence triggers **Clarify (NEW-009/010)**.
- `use_mcp` (**MCP-002**) calls tools via adapters (**RES-05/AS-145**).
- LLM invocation.
- **RES-07 observability** logs events for replay.
- **Budget guard (NEW-012)** checks cost before output.

```
user input
    │
    ▼
[RES-03 scoring] → [RES-04 gates] ── low conf? ──► [Clarify (NEW-009/010)]
    │                                  │
    ├─ use_mcp (MCP-002) ─► [MCP tools via adapters (RES-05/AS-145)]
    │
    ▼
[LLM call] ─► [RES-07 observability + replay] ─► [Budget guard (NEW-012)] ─► output
```

## Module map

- **RES-03**: scoring heuristics.
- **RES-04**: gates/policy enforcement.
- **RES-05/AS-145**: MCP adapters for external tools.
- **RES-07**: observability and replay hooks.
- **MCP-002**: toggle for MCP usage.
- **NEW-009/010**: clarify step on low confidence.
- **NEW-012**: cost budget guard.
- **NEW-015**: determinism harness ensuring stable outputs.

