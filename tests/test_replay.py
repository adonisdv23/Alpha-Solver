from alpha.core.replay import ReplayHarness


def test_replay_roundtrip(tmp_path):
    harness = ReplayHarness(tmp_path)
    harness.record({"step": 1})
    session_id = harness.save()
    session = harness.load(session_id)
    events = list(harness.replay(session))
    assert events == [{"step": 1}]
