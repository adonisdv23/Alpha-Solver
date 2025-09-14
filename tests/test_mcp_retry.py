import asyncio
import pytest

from service.mcp.retry_backoff import call_with_retries
from service.mcp.error_taxonomy import ErrorClass


def test_retry_on_retryable_errors():
    class FlakyTool:
        def __init__(self):
            self.calls = 0

        async def __call__(self, *, idempotency_key=None):
            self.calls += 1
            if self.calls < 2:
                raise TimeoutError("temp")
            return "ok"

    tool = FlakyTool()
    result, meta = asyncio.run(call_with_retries(tool, timeout=5, seed=1))
    assert result == "ok"
    assert meta["attempts"] == 2
    assert len(meta["delays"]) == 1


def test_no_retry_on_nonretryable():
    def fail(*, idempotency_key=None):
        raise ValueError("bad")

    async def run():
        await call_with_retries(fail, timeout=1)

    with pytest.raises(ValueError) as exc:
        asyncio.run(run())
    assert exc.value.retry_meta["attempts"] == 1


def test_respects_max_retries():
    class AlwaysFail:
        def __init__(self):
            self.calls = 0

        async def __call__(self, *, idempotency_key=None):
            self.calls += 1
            raise TimeoutError("fail")

    tool = AlwaysFail()

    async def run():
        await call_with_retries(tool, timeout=5, max_retries=1, seed=0)

    with pytest.raises(TimeoutError) as exc:
        asyncio.run(run())
    assert tool.calls == 2
    assert exc.value.retry_meta["attempts"] == 2


def test_deterministic_delays_with_seed():
    class FailTwice:
        def __init__(self):
            self.calls = 0

        async def __call__(self, *, idempotency_key=None):
            self.calls += 1
            if self.calls < 3:
                raise TimeoutError("temp")
            return "ok"

    tool1 = FailTwice()
    res1, meta1 = asyncio.run(
        call_with_retries(tool1, timeout=10, seed=42, max_retries=5)
    )
    tool2 = FailTwice()
    res2, meta2 = asyncio.run(
        call_with_retries(tool2, timeout=10, seed=42, max_retries=5)
    )
    assert meta1["delays"] == meta2["delays"]


def test_honors_timeout_budget():
    async def slow(*, idempotency_key=None):
        await asyncio.sleep(1)
        return "ok"

    with pytest.raises(TimeoutError) as exc:
        asyncio.run(call_with_retries(slow, timeout=0.5))
    assert exc.value.retry_meta["attempts"] == 1
    assert exc.value.retry_meta["delays"] == []


def test_route_explain_fields_present():
    class FlakyTool:
        def __init__(self):
            self.calls = 0

        async def __call__(self, *, idempotency_key=None):
            self.calls += 1
            if self.calls < 2:
                raise TimeoutError("temp")
            return "ok"

    result, meta = asyncio.run(call_with_retries(FlakyTool(), timeout=5, seed=0))
    for key in ("attempts", "delays", "last_error_class", "last_error_code"):
        assert key in meta
    assert meta["last_error_class"] == ErrorClass.TIMEOUT.value
    assert meta["last_error_code"] is None


def test_idempotency_guard():
    class CounterTool:
        def __init__(self):
            self.counter = 0
            self.seen = set()

        async def __call__(self, *, idempotency_key=None):
            if idempotency_key not in self.seen:
                self.counter += 1
                self.seen.add(idempotency_key)
                if self.counter == 1:
                    raise TimeoutError("fail once")
            return self.counter

    tool = CounterTool()
    result, meta = asyncio.run(
        call_with_retries(tool, timeout=5, idempotency_key="k1", seed=0)
    )
    assert tool.counter == 1
    assert result == 1
    assert meta["attempts"] == 2
