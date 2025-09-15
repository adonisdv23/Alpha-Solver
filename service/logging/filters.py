import logging
from typing import Iterable, Set, Any

from .redactor import redact, ERROR_COUNTER

_BUILTINS = {
    'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
    'module', 'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName',
    'created', 'msecs', 'relativeCreated', 'thread', 'threadName', 'processName',
    'process'
}

class RedactionFilter(logging.Filter):
    """Logging filter that redacts secrets from records."""

    def __init__(self, allowlist: Iterable[str] | None = None) -> None:
        super().__init__()
        self.allowlist: Set[str] = set(allowlist or [])

    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover - integration
        try:
            if isinstance(record.msg, (str, dict)):
                record.msg = redact(record.msg, self.allowlist)
            for key, value in list(record.__dict__.items()):
                if key in _BUILTINS or key in self.allowlist:
                    continue
                if isinstance(value, (str, dict)):
                    record.__dict__[key] = redact(value, self.allowlist)
        except Exception:
            ERROR_COUNTER.inc()
        return True


def install(logger: logging.Logger | None = None, allowlist: Iterable[str] | None = None) -> RedactionFilter:
    """Install the redaction filter on *logger* (root by default)."""
    log = logger or logging.getLogger()
    filt = RedactionFilter(allowlist)
    log.addFilter(filt)
    return filt

__all__ = ["RedactionFilter", "install"]
