"""Tests for distributed tracing helpers."""

from __future__ import annotations

from collections import defaultdict

from service import otel


def _simulate_request(i: int) -> None:
    req_id = f"req-{i}"
    with otel.span(
        "alpha.router",
        request_id=req_id,
        tenant_id="tenant",
        decision="allow",
        budget_verdict="under",
        cost_usd=0.01,
        tokens=10,
        user_input="hello world",
        secret="token",
    ):
        with otel.span("alpha.gates"):
            with otel.span("alpha.adapter"):
                pass


def test_trace_coverage_and_structure():
    tracer = otel.init_tracer()
    otel.reset_exported_spans()

    for i in range(100):
        _simulate_request(i)

    spans = otel.get_exported_spans()
    names = [s.name for s in spans]
    router_spans = [s for s in spans if s.name == "alpha.router"]

    # ≥95% of requests traced (we trace all so allow some leeway)
    assert len(router_spans) >= 95

    # ensure attributes present and sensitive attrs redacted
    sample = router_spans[0]
    attrs = sample.attributes
    for key in [
        "request_id",
        "tenant_id",
        "decision",
        "budget_verdict",
        "cost_usd",
        "tokens",
        "latency_ms",
    ]:
        assert key in attrs
    assert "user_input" not in attrs
    assert "secret" not in attrs

    # verify span hierarchy router->gates->adapter
    span_by_id = {s.context.span_id: s for s in spans}
    children = defaultdict(list)
    for s in spans:
        if s.parent is not None:
            children[s.parent.span_id].append(s)

    for r in router_spans:
        gate_spans = [s for s in children.get(r.context.span_id, []) if s.name == "alpha.gates"]
        assert gate_spans, "router span missing gates child"
        for g in gate_spans:
            adapter_spans = [
                s
                for s in children.get(g.context.span_id, [])
                if s.name == "alpha.adapter"
            ]
            assert adapter_spans, "gates span missing adapter child"

    # trace export succeeded locally
    assert spans, "no spans exported"

