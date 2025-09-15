import importlib.util
import sys
from pathlib import Path

try:
    import prometheus_client as prom
    if not hasattr(prom, "CollectorRegistry"):
        raise ImportError
except Exception:  # pragma: no cover - fallback if stub present
    for path in sys.path:
        if "site-packages" not in path:
            continue
        candidate = Path(path) / "prometheus_client" / "__init__.py"
        if candidate.exists():
            spec = importlib.util.spec_from_file_location("prometheus_client", candidate)
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            sys.modules["prometheus_client"] = module
            spec.loader.exec_module(module)  # type: ignore
            prom = module
            break
    else:  # pragma: no cover - real package not found
        raise

Counter = prom.Counter
Histogram = prom.Histogram
CollectorRegistry = prom.CollectorRegistry
generate_latest = prom.generate_latest
CONTENT_TYPE_LATEST = prom.CONTENT_TYPE_LATEST
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from starlette.testclient import TestClient
from threading import Lock

_lock = Lock()
_REGISTRY = CollectorRegistry()
_METRICS_CREATED = False
ROUTE_DECISION = None
BUDGET_VERDICT = None
TOKENS = None
COST_USD = None
LATENCY_MS = None


def _ensure_metrics():
    global _METRICS_CREATED, ROUTE_DECISION, BUDGET_VERDICT, TOKENS, COST_USD, LATENCY_MS
    if _METRICS_CREATED:
        return
    with _lock:
        if _METRICS_CREATED:
            return
        ROUTE_DECISION = Counter("alpha_solver_route_decision_total", "route decisions", ["decision"], registry=_REGISTRY)
        BUDGET_VERDICT = Counter("alpha_solver_budget_verdict_total", "budget verdicts", ["budget_verdict"], registry=_REGISTRY)
        TOKENS = Counter("alpha_solver_tokens_total", "tokens used", registry=_REGISTRY)
        COST_USD = Counter("alpha_solver_cost_usd_total", "cost (USD)", registry=_REGISTRY)
        LATENCY_MS = Histogram("alpha_solver_latency_ms", "latency ms",
                               buckets=[5,10,25,50,100,250,500,1000,2000],
                               registry=_REGISTRY)
        _METRICS_CREATED = True


class MetricsExporter:
    def __init__(self, namespace: str = "alpha_solver"):
        self.namespace = namespace
        _ensure_metrics()

    def asgi_app(self):
        _ensure_metrics()

        async def metrics(_request):
            return Response(generate_latest(_REGISTRY), media_type=CONTENT_TYPE_LATEST)

        return Starlette(routes=[Route("/metrics", metrics)])

    # Back-compat alias some callers may use
    def app(self):
        return self.asgi_app()

    def test_client(self) -> TestClient:
        return TestClient(self.asgi_app())

    @staticmethod
    def _redact(d: dict) -> dict:
        return {k: v for k, v in d.items()
                if k != "pii_raw" and not (k.endswith("_token") or k.endswith("_secret"))}

    def record_event(self, *, decision: str, confidence: float | None = None, budget_verdict: str | None = None,
                     latency_ms: float | None = None, tokens: int | None = None, cost_usd: float | None = None,
                     policy_verdict: str | None = None):
        _ensure_metrics()
        # enforce small, fixed-label cardinality
        d = decision or "unknown"
        ROUTE_DECISION.labels(decision=d).inc()
        if budget_verdict:
            BUDGET_VERDICT.labels(budget_verdict=budget_verdict).inc()
        if tokens is not None:
            TOKENS.inc(tokens)
        if cost_usd is not None:
            COST_USD.inc(cost_usd)
        if latency_ms is not None:
            LATENCY_MS.observe(latency_ms)


__all__ = ["MetricsExporter", "_REGISTRY"]

