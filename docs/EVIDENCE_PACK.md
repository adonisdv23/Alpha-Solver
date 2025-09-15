# Evidence Pack

## CLI Help

```bash
python alpha_solver_cli.py --help
```

```text
--multi-branch
```

## Basic Solve (LLM-only)

```python
from alpha.executors.math_exec import evaluate
print(evaluate("2+2")["result"])
```

```text
4.0
```

## Route with Budget Gate Verdict

```python
from service.gating.gates import evaluate_gates
decision, info = evaluate_gates(confidence=0.2, budget_tokens=100, policy_flags={})
print(decision, info["budget_verdict"])
```

```text
clarify low
```

## Policy/PII Redaction Before Log

```python
from service.logging.redactor import redact
print(redact("Contact me at a@b.com"))
```

```text
Contact me at a***@b***.com
```

## Replay 10/10

```python
from alpha.core.replay import ReplayHarness
h = ReplayHarness(base_dir="artifacts/replay_tmp")
for i in range(10):
    h.record({"i": i})
sid = h.save("demo")
session = h.load("demo")
h.load_for_replay("demo")
for ev in session.events:
    h.verify(ev)
print(len(session.events))
```

```text
10
```

## Tracing/Metrics Quick Check

```python
import logging
from service.otel import init_tracer, span, get_exported_spans, reset_exported_spans
logging.getLogger().setLevel(logging.ERROR)
reset_exported_spans(); init_tracer()
with span("demo", user_input="secret", answer=42):
    pass
spans = get_exported_spans()
print(len(spans), "answer" in spans[0].attributes, "user_input" in spans[0].attributes)
```

```text
1 True False
```

## MCP Adapter Call

```python
import os
from service.mcp.policy_auth import OAuthClientCredentials, attach_auth_headers
os.environ["CLIENT_ID"] = "id"
os.environ["CLIENT_SECRET"] = "secret"
provider = OAuthClientCredentials("https://auth", "CLIENT_ID", "CLIENT_SECRET")
req = attach_auth_headers({}, provider)
print(req["Authorization"])
```

```text
Bearer oauth-token-1
```
