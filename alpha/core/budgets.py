from __future__ import annotations

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


def compute_percentiles(values: Iterable[float]) -> Dict[str, float]:
    vals = sorted(values)
    if not vals:
        return {"p50": 0.0, "p95": 0.0, "p99": 0.0}
    def _pct(p: float) -> float:
        k = (len(vals) - 1) * p
        f = int(k)
        c = min(f + 1, len(vals) - 1)
        if f == c:
            return vals[int(k)]
        d0 = vals[f] * (c - k)
        d1 = vals[c] * (k - f)
        return d0 + d1
    return {"p50": _pct(0.5), "p95": _pct(0.95), "p99": _pct(0.99)}


def compute_cost_per_call(costs: Iterable[float]) -> float:
    costs = list(costs)
    return sum(costs) / len(costs) if costs else 0.0


@dataclass
class GateDecision:
    passed: bool
    reasons: List[str]


def gate_decision(report: Dict, config) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    metrics = report.get("metrics", {})
    latency = report.get("latency", {})
    metric_val = metrics.get(config.primary_metric, 0.0)
    if metric_val < config.min_accuracy:
        reasons.append(
            f"{config.primary_metric} {metric_val:.2f} < min {config.min_accuracy:.2f}"
        )
    if latency.get("p95", 0.0) > config.max_p95_ms:
        reasons.append(
            f"p95 {latency.get('p95',0.0):.1f}ms > max {config.max_p95_ms}ms"
        )
    if latency.get("p99", 0.0) > config.max_p99_ms:
        reasons.append(
            f"p99 {latency.get('p99',0.0):.1f}ms > max {config.max_p99_ms}ms"
        )
    if report.get("cost_per_call", 0.0) > config.max_cost_per_call:
        reasons.append(
            f"cost {report.get('cost_per_call',0.0):.4f} > max {config.max_cost_per_call:.4f}"
        )
    return (len(reasons) == 0, reasons)
