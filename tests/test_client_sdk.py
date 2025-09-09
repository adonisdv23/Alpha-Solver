import json
import threading
import time
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from clients.python.alpha_client import AlphaClient


class MockHandler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802 - required by BaseHTTPRequestHandler
        self.server.calls.append(self.headers.get("X-API-Key"))  # type: ignore[attr-defined]
        self.server.attempt += 1  # type: ignore[attr-defined]
        if self.server.attempt == 1:  # type: ignore[attr-defined]
            self.send_response(429)
            self.end_headers()
            return
        if self.server.attempt == 2:
            self.send_response(500)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Request-ID", "req-1")
        self.end_headers()
        self.wfile.write(json.dumps({"final_answer": "ok"}).encode())


def _start_server(handler_cls):
    server = HTTPServer(("localhost", 0), handler_cls)
    server.calls = []  # type: ignore[attr-defined]
    server.attempt = 0  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_client_retries_and_headers(monkeypatch):
    server = _start_server(MockHandler)
    monkeypatch.setattr(time, "sleep", lambda s: None)
    client = AlphaClient(f"http://localhost:{server.server_port}", "key")
    result = client.solve("hi", strategy="react")
    assert result["final_answer"] == "ok"
    assert result["request_id"] == "req-1"
    assert server.calls[0] == "key"
    server.shutdown()


class FailHandler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        self.send_response(500)
        self.end_headers()


def test_client_fail_after_retries(monkeypatch):
    server = _start_server(FailHandler)
    monkeypatch.setattr(time, "sleep", lambda s: None)
    client = AlphaClient(f"http://localhost:{server.server_port}", "k")
    try:
        client.solve("hi")
    except RuntimeError:
        pass
    else:
        assert False, "expected RuntimeError"
    server.shutdown()
