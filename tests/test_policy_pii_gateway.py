import pytest
from service.policy.policy_gateway import PolicyGateway, PolicyConfig
from service.policy.redaction import EMAIL_REGEX, PHONE_REGEX


@pytest.mark.policy
def test_pii_detection_and_redaction_performance():
    cfg = PolicyConfig(enable_input_redaction=True)
    gw = PolicyGateway(cfg)

    cases = []
    # email positives and negatives
    for i in range(30):
        cases.append((f"Contact me at user{i}@example.com", True, False))
    for i in range(30):
        cases.append((f"user{i} at example dot com", False, False))

    # phone positives and negatives
    for i in range(30):
        cases.append((f"Call me at +1-202-555-01{i:02d}", False, True))
    for i in range(30):
        cases.append((f"extension 10{i}", False, False))

    assert len(cases) >= 100

    email_detected = phone_detected = 0
    email_total = phone_total = 0
    latencies = []
    for text, has_email, has_phone in cases:
        route = {}
        log_text, _ = gw.process(text, route, for_model=True)
        stats = route["redaction_stats"]
        latencies.append(stats["latency_ms"])

        if has_email:
            email_total += 1
            if stats["email"]:
                email_detected += 1
            assert EMAIL_REGEX.search(log_text) is None
        else:
            assert stats["email"] == 0

        if has_phone:
            phone_total += 1
            if stats["phone"]:
                phone_detected += 1
            assert PHONE_REGEX.search(log_text) is None
        else:
            assert stats["phone"] == 0

    assert email_detected / email_total >= 0.99
    assert phone_detected / phone_total >= 0.99

    latencies.sort()
    p95 = latencies[int(len(latencies) * 0.95)]
    assert p95 < cfg.latency_budget_ms_p95

    # ensure route explains are populated for last event
    assert "policy_verdict" in route and route["policy_verdict"] == "pass"
    assert "redaction_stats" in route

    # cover non-model branch
    sample_route = {}
    _, model_text = gw.process("hello", sample_route, for_model=False)
    assert model_text == "hello"

    # cover phone length check branch (digits > 15)
    long_route = {}
    long_text = "call +1-1234567890123456"
    redacted, _ = gw.process(long_text, long_route, for_model=True)
    assert long_route["redaction_stats"]["phone"] == 0
    assert PHONE_REGEX.search(redacted)

    # ensure no PII in any logged text overall
    for text, _, _ in cases:
        route = {}
        log_text, _ = gw.process(text, route, for_model=True)
        assert EMAIL_REGEX.search(log_text) is None
        assert PHONE_REGEX.search(log_text) is None
