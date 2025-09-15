# Evidence Pack

Curated examples demonstrating Alpha Solver features. Each code block is runnable and prints an expected value marked by `# EXPECT:`.

## 1. Basic solve

```python
from alpha_solver_entry import _tree_of_thought
print(_tree_of_thought("hello")["final_answer"])
# EXPECT: hello
```

## 2. Budget guard verdict

```python
from service.budget.simulator import simulate, load_cost_models
from service.budget.guard import BudgetGuard
items = [{"prompt_tokens": 10, "completion_tokens": 0, "latency_ms": 10}]
cost_models = load_cost_models()
sim = simulate(items, cost_models, provider="openai", model="gpt-4o")
guard = BudgetGuard(max_cost_usd=1.0, max_tokens=20)
print(guard.check(sim)["budget_verdict"])
# EXPECT: ok
```

## 3. PII redaction before log

```python
from service.validation.sanitizer import sanitize
print(sanitize({"msg": "Email me at test@example.com"}))
# EXPECT: {'msg': 'Email me at t***@e***.com'}
```

## 4. Replay deterministic run

```python
from service.replay.player import Player
from service.replay.recorder import stable_hash
hash_input = {"snapshot": {"version": 1}, "route_explain": {"scores": None, "gate_decisions": None, "plan_winner": None, "budget_verdict": None}}
record = {"seed": 1, "payload": {"x": 1}, "snapshot": {"version": 1}, "route_explain": {}, "hash": stable_hash(hash_input)}
def run(payload, seed):
    return "ok", {}
player = Player(snapshot_fn=lambda: {"version": 1})
print(player.replay(record, run)["hash"])
# EXPECT: 737cd2bd81c43faee4c5eeac6a4c4f854c14abc27fdcd294c562fa3b590961f2
```

## 5. Metrics exporter

```python
from service.metrics.exporter import MetricsExporter
exp = MetricsExporter()
exp.record_event(decision="allow", budget_verdict="ok", tokens=5, cost_usd=0.01)
client = exp.test_client()
resp = client.get("/metrics")
print("alpha_solver_route_decision_total" in resp.text)
# EXPECT: True
```

## 6. CLI help

```python
import subprocess, sys
out = subprocess.run([sys.executable, "alpha_solver_cli.py", "--help"], capture_output=True, text=True).stdout
print("--max-width" in out)
# EXPECT: True
```
