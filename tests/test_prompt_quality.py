import time
import yaml
from service.prompts.quality.evaluator import QualityEvaluator, rubrics_sha
from service.prompts.quality.report import batch_compare


RUBRICS_PATH = "service/prompts/quality/rubrics.yaml"
with open(RUBRICS_PATH, "r", encoding="utf-8") as f:
    RUBRICS_TEXT = f.read()
RUBRICS = yaml.safe_load(RUBRICS_TEXT)
RUBRICS_SHA = rubrics_sha(RUBRICS_TEXT)


def make_evaluator():
    return QualityEvaluator(RUBRICS, RUBRICS_TEXT)


def test_rubrics_sha_stable():
    assert RUBRICS_SHA == "fd2e588b1725e4df7d5aca764caf89ac8cc5366ea18949a4182fd316c51e7daf"


def test_evaluator_scores_keywords_brevity_structure_safety():
    evaluator = make_evaluator()
    context = {
        "must_include": ["alpha", "beta"],
        "require_headings": True,
        "require_bullets": True,
        "required_fields": ["Name"],
    }
    good_response = "# Heading\nName: Foo\n- alpha\n- beta"
    res = evaluator.score(good_response, context=context)
    assert res["scores"] == {
        "correctness": 2,
        "brevity": 2,
        "structure": 2,
        "safety": 2,
    }
    unsafe_response = good_response + "\njohn@example.com"
    res2 = evaluator.score(unsafe_response, context=context)
    assert res2["scores"]["safety"] == 0


def test_compare_selects_winner_and_route_explain_has_shas():
    evaluator = make_evaluator()
    context = {"must_include": ["alpha"], "prompt_deck_sha": "deck123"}
    baseline = "This lacks keyword."
    variant = "# H\n- alpha"
    out = evaluator.compare(baseline, variant, context=context)
    assert out["winner"] == "variant"
    assert out["route_explain"]["prompt_deck_sha"] == "deck123"
    assert out["route_explain"]["rubrics_sha"] == RUBRICS_SHA


def test_batch_compare_reports_win_rate_ge_10pct_on_sample():
    evaluator = make_evaluator()
    pairs = []
    for i in range(10):
        ctx = {"must_include": ["alpha"]}
        if i < 2:
            baseline = ""
            variant = "alpha"
        else:
            baseline = "alpha"
            variant = ""
        pairs.append({"id": str(i), "baseline": baseline, "variant": variant, "context": ctx})
    result = batch_compare(pairs, evaluator, deck_sha="deckX", rubrics_sha_str=RUBRICS_SHA)
    assert result["total"] == 10
    assert result["wins"] >= 1
    assert result["win_rate"] >= 0.1
    assert result["route_explain"]["prompt_deck_sha"] == "deckX"
    assert result["route_explain"]["rubrics_sha"] == RUBRICS_SHA


def test_performance_p95_under_2s_for_100():
    evaluator = make_evaluator()
    pairs = []
    for i in range(100):
        ctx = {"must_include": ["alpha"]}
        baseline = "alpha" if i % 2 == 0 else ""
        variant = "alpha"
        pairs.append({"id": str(i), "baseline": baseline, "variant": variant, "context": ctx})
    start = time.monotonic()
    batch_compare(pairs, evaluator, deck_sha="deckY", rubrics_sha_str=RUBRICS_SHA)
    duration = time.monotonic() - start
    assert duration < 2


def test_no_pii_in_outputs():
    evaluator = make_evaluator()
    pairs = [
        {
            "id": "1",
            "baseline": "safe",
            "variant": "alpha",
            "context": {"pii_raw": "secret", "api_token": "tok", "must_include": []},
        }
    ]
    result = batch_compare(pairs, evaluator, deck_sha="deckZ", rubrics_sha_str=RUBRICS_SHA)
    text = str(result)
    assert "pii_raw" not in text
    assert "secret" not in text
    assert "api_token" not in text
    assert "tok" not in text
