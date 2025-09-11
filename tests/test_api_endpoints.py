from fastapi.testclient import TestClient

from service.app import app


client = TestClient(app)


def _post(body):
    # test helper: force a known API key and disable rate limit noise
    app.state.config.api_key = "dev-secret"
    prev = app.state.config.ratelimit.enabled
    app.state.config.ratelimit.enabled = False
    try:
        return client.post(
            "/v1/solve",
            headers={"X-API-Key": "dev-secret"},
            json=body,
        )
    finally:
        app.state.config.ratelimit.enabled = prev


def test_solve_react_ok():
    r = _post({"query": "2+2", "strategy": "react"})
    assert r.status_code == 200
    j = r.json()
    assert isinstance(j["final_answer"], str)
    assert j.get("meta", {}).get("strategy") in {"react", "cot", "tot"}


def test_solve_cot_ok():
    r = _post({"query": "2+2", "strategy": "cot"})
    assert r.status_code == 200
    j = r.json()
    assert "final_answer" in j
    assert j.get("meta", {}).get("strategy") in {"react", "cot", "tot"}


def test_solve_missing_query_422():
    r = _post({"strategy": "react"})
    assert r.status_code == 422


def test_solve_get_405():
    r = client.get("/v1/solve", headers={"X-API-Key": "dev-secret"})
    assert r.status_code in (405, 404)


def test_arithmetic_sanity_or_safe_out():
    r = _post({"query": "What is 17 + 28? Show steps.", "strategy": "react"})
    assert r.status_code == 200
    j = r.json()
    # Either we include the correct result OR we SAFE-OUT
    assert ("45" in j["final_answer"]) or j["final_answer"].startswith("SAFE-OUT")


def test_openapi_advertises_solve_post():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    j = r.json()
    assert "/v1/solve" in j.get("paths", {})
    assert "post" in j["paths"]["/v1/solve"]

