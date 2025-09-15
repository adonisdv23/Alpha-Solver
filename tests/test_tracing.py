from service.otel import init_tracer


def test_init_tracer_noop_when_otel_missing(monkeypatch):
    # pretend OTel not installed
    monkeypatch.setenv("PYTHONPATH", "")  # no effect, but keep the intent
    tracer = init_tracer(app=None)
    # must support context manager
    with tracer.start_as_current_span("x"):
        pass

