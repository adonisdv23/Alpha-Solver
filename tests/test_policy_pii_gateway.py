from service.policy.policy_gateway import PolicyGateway, PolicyConfig


def test_email_masking():
    cfg = PolicyConfig(enable_input_redaction=True, detectors={"email": True, "phone": False})
    gw = PolicyGateway(cfg)
    route = {}
    log_text, model_text = gw.process("Reach me at alice@example.com", route, for_model=True)
    assert "alice@example.com" not in log_text
    assert log_text == model_text
    assert route["redaction_stats"]["email"] == 1

    route = {}
    log_text, model_text = gw.process("No emails here", route, for_model=True)
    assert log_text == "No emails here"
    assert route["redaction_stats"]["email"] == 0


def test_phone_masking():
    cfg = PolicyConfig(enable_input_redaction=True, detectors={"email": False, "phone": True})
    gw = PolicyGateway(cfg)
    route = {}
    log_text, model_text = gw.process("Call +1-234-567-1234 now", route, for_model=True)
    assert "+1-234-567-1234" not in log_text
    assert log_text == model_text
    assert route["redaction_stats"]["phone"] == 1

    route = {}
    log_text, model_text = gw.process("Number 123 is short", route, for_model=True)
    assert "Number 123 is short" == log_text
    assert route["redaction_stats"]["phone"] == 0


def test_fail_closed_blocks_raw_logging(monkeypatch):
    cfg = PolicyConfig()
    gw = PolicyGateway(cfg)

    def boom(text, detectors):
        raise RuntimeError("detector fail")

    from service.policy import redaction

    monkeypatch.setattr(redaction, "redact", boom)
    route = {}
    log_text, model_text = gw.process("secret text", route, for_model=True)
    assert "secret text" not in log_text
    assert route["policy_verdict"] == "error"
    assert "error" in route["redaction_stats"]


def test_latency_budget_p95_under_50ms():
    cfg = PolicyConfig()
    gw = PolicyGateway(cfg)
    latencies = []
    for _ in range(1000):
        route = {}
        gw.process("Hello there", route, for_model=False)
        latencies.append(route["redaction_stats"]["latency_ms"])
    latencies.sort()
    p95 = latencies[int(len(latencies) * 0.95)]
    assert p95 < 50


def test_route_explain_fields_present():
    cfg = PolicyConfig()
    gw = PolicyGateway(cfg)
    route = {}
    gw.process("hi", route, for_model=True)
    assert "policy_verdict" in route
    assert "redaction_stats" in route
