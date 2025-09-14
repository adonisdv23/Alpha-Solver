import time

from service.prompts.selector import choose_deck
from service.prompts.renderer import (
    compare_token_savings,
    load_decks,
    render,
    deck_sha,
    to_route_explain,
)


def test_choose_deck_intents_are_deterministic():
    deck, ctx = choose_deck({"task": "do"})
    assert deck == "generic"
    assert ctx == {"task": "do"}

    deck, ctx = choose_deck({"intent": "browse", "url": "u", "goal": "g", "fields": ["a"]})
    assert deck == "web_extract"
    assert ctx == {"url": "u", "goal": "g", "fields": ["a"]}

    deck, ctx = choose_deck({"intent": "sheet", "op": "append", "sheet": "s", "values": [1, 2]})
    assert deck == "sheets_ops"
    assert ctx == {"op": "append", "sheet": "s", "values": [1, 2]}

    deck, ctx = choose_deck({"clarify": True, "missing_fields": ["x", "y"]})
    assert deck == "policy_clarify"
    assert ctx == {"missing_fields": ["x", "y"]}


def test_render_substitutes_vars_and_joins():
    decks = load_decks()
    ctx = {"url": "http://a", "goal": "info", "fields": ["title", "body"]}
    rendered = render("web_extract", ctx, decks)
    assert "Extract only the essentials" in rendered["system"]
    assert "URL: http://a" in rendered["user"]
    assert "Return: title, body" in rendered["user"]


def test_deck_sha_is_stable():
    with open("service/prompts/decks.yaml", "r", encoding="utf-8") as f:
        text = f.read()
    sha1 = deck_sha(text)
    sha2 = deck_sha(text)
    assert sha1 == sha2


def test_route_explain_contains_deck_and_sha():
    decks = load_decks()
    rendered = render("generic", {"task": "t"}, decks)
    info = to_route_explain("generic", rendered["deck_sha"])
    assert info["prompt_deck"] == "generic"
    assert info["deck_sha"] == rendered["deck_sha"]


def test_token_savings_ge_20_percent_on_sample_set():
    baseline = [
        (
            "System: You are a highly verbose assistant that must respond with long, detailed explanations for every request. "
            "User: please complete task one with all reasoning shown."
        ),
        (
            "System: You are a highly verbose assistant that must respond with long, detailed explanations for every request. "
            "User: please complete task two with all reasoning shown."
        ),
    ]
    decks = load_decks()
    contexts = [{"task": "task one"}, {"task": "task two"}]
    new_prompts = []
    for ctx in contexts:
        deck, rctx = choose_deck(ctx)
        rendered = render(deck, rctx, decks)
        new_prompts.append(rendered["system"] + " " + rendered["user"])
    reduction = compare_token_savings(baseline, new_prompts)
    assert reduction >= 20.0


def test_p95_render_under_200ms():
    decks = load_decks()
    durations = []
    for i in range(100):
        ctx = {"task": f"do {i}"}
        deck, rctx = choose_deck(ctx)
        start = time.monotonic()
        render(deck, rctx, decks)
        durations.append(time.monotonic() - start)
    durations.sort()
    p95 = durations[int(len(durations) * 0.95)]
    assert p95 < 0.2
