from service.adapters.playwright_adapter import PlaywrightAdapter
from service.adapters.gsheets_adapter import GSheetsAdapter
from service.scenarios.runner import load_pack, run_step, run_scenario, run_all, replay
from service.scenarios.rubric import Rubric


def _adapters():
    return {"playwright": PlaywrightAdapter(), "gsheets": GSheetsAdapter()}


def test_pack_loads_30_plus_scenarios():
    scenarios = load_pack()
    assert len(scenarios) >= 30


def test_run_single_scenario_pass_rate():
    scenarios = load_pack()
    res = run_scenario(scenarios[0], adapters=_adapters(), rubric=Rubric())
    assert res["passed"]
    assert res["passed_steps"] == res["total_steps"] == len(scenarios[0]["steps"])


def test_runner_uses_adapters_and_returns_values():
    step = load_pack()[0]["steps"][0]
    res = run_step(step, adapters=_adapters(), rubric=Rubric())
    assert res["ok"]
    assert res["value"] == "Example Domain"
    route = res["route_explain"]
    assert route["adapter"] == "playwright"
    assert "latency_ms" in route


def test_rubric_equals_contains_regex_and_type():
    r = Rubric()
    assert r.judge({"equals": 5}, 5)[0]
    assert r.judge({"contains": "ell"}, "hello")[0]
    assert r.judge({"regex": "^he"}, "hello")[0]
    assert r.judge({"type": "number"}, 3.14)[0]


def test_record_then_replay_is_identical_10_of_10():
    scenarios = load_pack()[:10]
    run_res = run_all(scenarios, adapters=_adapters(), rubric=Rubric())
    events = []
    for sc in run_res["results"]:
        for d in sc["details"]:
            events.append({"expect": d["expect"], "value": d["value"], "ok": d["ok"]})
    replay_res = replay(events, rubric=Rubric())
    assert [e["ok"] for e in replay_res["events"]] == [e["ok"] for e in events]


def test_summary_includes_pass_rate_and_counts():
    scenarios = load_pack()[:3]
    res = run_all(scenarios, adapters=_adapters(), rubric=Rubric())
    summary = res["summary"]
    assert summary["total"] == 3
    assert summary["passed"] == 3
    assert summary["pass_rate"] == 1.0


def test_route_explain_fields_present():
    scn = load_pack()[0]
    res = run_scenario(scn, adapters=_adapters(), rubric=Rubric())
    for d in res["details"]:
        route = d["route_explain"]
        for key in ["decision", "adapter", "latency_ms", "judged"]:
            assert key in route
