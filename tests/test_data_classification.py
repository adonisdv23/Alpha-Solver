from alpha.core import orchestrator


def _shortlist(prompt: str):
    return [{"id": "t1", "router_value": 1.0, "prompt": prompt, "reasons": {}}]


def test_enforcement_downgrades():
    plan = orchestrator.build_plan("q", "US", 1, _shortlist("contains secret"), None, seed=1)
    assert plan.steps[0].mode == "instructions_only"
    assert not plan.guards.policy_dryrun


def test_policy_dryrun_annotation():
    plan = orchestrator.build_plan("q", "US", 1, _shortlist("contains token"), None, seed=1, policy_dryrun=True)
    assert plan.steps[0].mode == "execute"
    assert plan.guards.policy_dryrun
    assert plan.guards.policy_notes
