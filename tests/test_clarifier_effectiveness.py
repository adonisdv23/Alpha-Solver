import random
import yaml

from service.clarify.router_hooks import maybe_clarify

INTENTS = [
    "summarize",
    "extract",
    "rewrite",
    "plan",
    "codegen",
    "classify",
    "cite",
    "web_extract",
]


class Cfg:
    clarify_conf_threshold = 0.55


def route(payload):
    return payload.get("intent", "unknown")


def test_clarifier_improves_accuracy():
    random.seed(0)
    with open("service/clarify/templates.yaml", "r", encoding="utf-8") as f:
        templates = yaml.safe_load(f)
    cfg = Cfg()
    scenarios = []
    for i in range(30):
        correct = random.choice(INTENTS)
        if i < 15:
            base_payload = {"confidence": 0.4, "missing_fields": ["intent"], "clarify_answer": correct}
            payload = dict(base_payload)
        else:
            base_payload = {"confidence": 0.9, "intent": correct}
            payload = dict(base_payload)
        scenarios.append((base_payload, payload, correct))

    baseline = 0
    after = 0
    for base_payload, payload, correct in scenarios:
        if route(base_payload) == correct:
            baseline += 1
        clarified, explain = maybe_clarify(payload, cfg, templates)
        if route(clarified) == correct:
            after += 1
    baseline_acc = baseline / len(scenarios)
    after_acc = after / len(scenarios)
    assert after_acc >= baseline_acc + 0.05


def test_deterministic_run():
    with open("service/clarify/templates.yaml", "r", encoding="utf-8") as f:
        templates = yaml.safe_load(f)
    cfg = Cfg()
    payload = {"confidence": 0.4, "missing_fields": ["intent"], "clarify_answer": "summarize"}
    res1, expl1 = maybe_clarify(payload, cfg, templates)
    res2, expl2 = maybe_clarify(payload, cfg, templates)
    assert res1 == res2
    assert expl1 == expl2


def test_threshold_behavior_and_failure_mode():
    with open("service/clarify/templates.yaml", "r", encoding="utf-8") as f:
        templates = yaml.safe_load(f)
    cfg = Cfg()
    low = {"confidence": 0.4, "missing_fields": ["intent"], "clarify_answer": "summarize"}
    high = {"confidence": 0.9, "missing_fields": ["intent"], "clarify_answer": "summarize"}
    no_answer = {"confidence": 0.4, "missing_fields": ["intent"], "clarify_answer": ""}

    clarified_low, explain_low = maybe_clarify(low, cfg, templates)
    clarified_high, explain_high = maybe_clarify(high, cfg, templates)
    clarified_none, explain_none = maybe_clarify(no_answer, cfg, templates)

    assert explain_low["clarify"]["triggered"]
    assert not explain_high["clarify"]["triggered"]
    assert "intent" not in clarified_none
    assert explain_none["clarify"]["triggered"]
