# Clarifier Templates

This document describes the `clarifier_v1` template deck. The clarifier triggers
when model confidence falls below `clarify_conf_threshold` or when required fields
are missing. A single concise question (<=120 chars) is asked and the user's
answer is merged back into the request payload.

## How it works
1. Detect ambiguity via confidence, missing fields or intent flags.
2. Render a clarifying question using `templates.yaml`.
3. Merge the answer into the payload and re-run routing.

```python
from service.clarify import router_hooks
from service.clarify import clarifier
```

## Templates
Templates are stored in `service/clarify/templates.yaml`. Each entry defines
`id`, `intent`, `system`, `user` and optional `variables` with defaults.
The deck currently covers:
- summarize
- extract
- rewrite
- plan
- codegen
- classify
- cite
- web_extract
- ask_missing_fields
- disambiguate_intent
- reduce_scope_low_budget
- pick_tool_first
- generic_clarify

## Examples
```
You're missing: intent. Please provide them briefly.
```
```
I can do summarize or extract. Which do you want?
```

## Failure modes
If no answer is provided or the clarifier cannot generate a question, routing
continues without modification. The `route_explain` payload records whether the
clarifier triggered and if the answer was used.
