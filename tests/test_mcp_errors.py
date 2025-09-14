import json
import asyncio

from service.mcp.error_taxonomy import (
    ErrorClass,
    map_exception,
    to_route_explain,
    is_retryable,
    MCPError,
)


class Dummy429(Exception):
    status_code = 429


class DummyAuth(Exception):
    def __init__(self, status_code):
        self.status_code = status_code


class SandboxViolation(Exception):
    pass


def test_timeout_maps_retryable():
    err = map_exception(TimeoutError("timeout"))
    assert err.cls == ErrorClass.TIMEOUT
    assert is_retryable(err)


def test_connectivity_maps_retryable():
    err = map_exception(ConnectionError("net"))
    assert err.cls == ErrorClass.CONNECTIVITY
    assert is_retryable(err)


def test_rate_limit_429_retryable():
    err = map_exception(Dummy429("rate"))
    assert err.cls == ErrorClass.RATE_LIMIT
    assert err.code == "429"
    assert is_retryable(err)


def test_auth_nonretryable():
    err = map_exception(DummyAuth(401))
    assert err.cls == ErrorClass.AUTH
    assert not is_retryable(err)


def test_schema_validation_nonretryable():
    err = map_exception(ValueError("bad schema"))
    assert err.cls == ErrorClass.SCHEMA_VALIDATION
    assert not is_retryable(err)


def test_sandbox_violation_nonretryable():
    err = map_exception(SandboxViolation("violate"))
    assert err.cls == ErrorClass.SANDBOX_VIOLATION
    assert not is_retryable(err)


def test_cancelled_nonretryable():
    err = map_exception(asyncio.CancelledError())
    assert err.cls == ErrorClass.CANCELLED
    assert not is_retryable(err)


def test_unknown_default():
    err = map_exception(RuntimeError("boom"))
    assert err.cls == ErrorClass.UNKNOWN
    assert not is_retryable(err)


def test_to_route_explain_truncates_message():
    long_msg = "x" * 120
    err = MCPError(cls=ErrorClass.UNKNOWN, message=long_msg, root="R")
    expl = to_route_explain(err)
    assert expl["message"] == long_msg[:100]


def test_to_json_is_serializable():
    err = map_exception(RuntimeError("boom"))
    json_str = json.dumps(err.to_json())
    assert isinstance(json_str, str)
