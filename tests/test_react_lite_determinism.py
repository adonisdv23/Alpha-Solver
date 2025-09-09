from alpha.reasoning.react_lite import run_react_lite
from alpha.reasoning.react_lite import run_react_lite


def test_react_lite_determinism():
    prompt = "2+2"
    seed = 1337
    results = [run_react_lite(prompt, seed) for _ in range(3)]
    first = results[0]
    for res in results[1:]:
        assert res["final_answer"] == first["final_answer"]
        assert res["trace"] == first["trace"]
        assert res["confidence"] == first["confidence"]
        assert res["confidence"] >= 0.70
