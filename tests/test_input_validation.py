import random
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from service.middleware.validation_middleware import ValidationMiddleware


app = FastAPI()
app.add_middleware(ValidationMiddleware)


@app.post("/echo")
async def echo(request: Request):
    return await request.json()


client = TestClient(app)


def test_valid_payload():
    payload = {"prompt": "hello", "task": "solve", "opts": {"strategy": "react"}}
    r = client.post("/echo", json=payload)
    assert r.status_code == 200
    assert r.json() == payload


def test_missing_fields_and_types():
    r = client.post("/echo", json={"task": "solve"})
    assert r.status_code == 400
    data = r.json()
    assert any(e["field"] == "prompt" for e in data["errors"])

    r = client.post("/echo", json={"prompt": 5, "task": "solve"})
    assert r.status_code == 400
    data = r.json()
    assert any(e["field"] == "prompt" and e["code"] == "invalid_type" for e in data["errors"])


def test_xss_and_sql_sanitization():
    payload = {"prompt": "<script>alert(1)</script>hello", "task": "solve"}
    r = client.post("/echo", json=payload)
    assert r.status_code == 200
    assert "script" not in r.json()["prompt"].lower()

    payload = {"prompt": "1; DROP TABLE users", "task": "solve"}
    r = client.post("/echo", json=payload)
    assert r.status_code == 200
    assert "drop table" not in r.json()["prompt"].lower()

    payload = {"prompt": "<img src=x onerror=alert(1)>hi", "task": "solve"}
    r = client.post("/echo", json=payload)
    assert "onerror" not in r.json()["prompt"].lower()

    payload = {"prompt": "javascript:alert(1)", "task": "solve"}
    r = client.post("/echo", json=payload)
    assert "javascript:" not in r.json()["prompt"].lower()


def test_pii_and_secret_redaction():
    payload = {
        "prompt": "Email test@example.com phone +12345678901 token=APIKEYSECRET1234567890",
        "task": "solve",
    }
    r = client.post("/echo", json=payload)
    assert r.status_code == 200
    text = r.json()["prompt"]
    assert "test@example.com" not in text
    assert "+12345678901" not in text
    assert "APIKEYSECRET1234567890" not in text
    assert "<redacted>" in text or "***" in text


def test_fuzz_invalid_inputs():
    bad_payloads = [
        {},
        {"prompt": 123, "task": "solve"},
        {"prompt": "", "task": "solve"},
        {"prompt": "hi", "task": "unknown"},
        {"prompt": "hi"},
        {"task": "solve"},
        {"prompt": "hi", "task": "solve", "extra": 1},
    ]
    for _ in range(100):
        payload = random.choice(bad_payloads)
        r = client.post("/echo", json=payload)
        assert r.status_code == 400
        assert r.json()["code"] == "invalid_request"
