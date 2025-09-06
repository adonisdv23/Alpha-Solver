import pytest
from alpha.core.governance import CircuitBreaker, GovernanceError


def test_circuit_breaker_trips():
    cb = CircuitBreaker(max_errors=1, window=100)
    cb.record_error()
    with pytest.raises(GovernanceError):
        cb.record_error()
