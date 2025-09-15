import re
from typing import Any, Dict, List

from service.policy.redaction import redact

SCRIPT_RE = re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL)
EVENT_HANDLER_RE = re.compile(r'on\w+\s*=\s*"?[^"]*"?', re.IGNORECASE)
JS_PROTO_RE = re.compile(r'javascript:', re.IGNORECASE)
SQL_INJECTION_RE = re.compile(r"(?i)(--|;|/\*|\*/|drop table|union select|insert into|delete from|update)")
SECRET_RE = re.compile(r"(?i)(api|secret|token|key)[\s:=]+[A-Za-z0-9\-]{16,}")
CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")
WHITESPACE_RE = re.compile(r"\s+")


def _clean_str(s: str) -> str:
    s = SCRIPT_RE.sub("", s)
    s = EVENT_HANDLER_RE.sub("", s)
    s = JS_PROTO_RE.sub("", s)
    s = SQL_INJECTION_RE.sub("", s)
    s = SECRET_RE.sub("<redacted>", s)
    s, _ = redact(s, {"email": True, "phone": True})
    s = CONTROL_RE.sub("", s)
    s = WHITESPACE_RE.sub(" ", s).strip()
    return s


def sanitize(data: Any) -> Any:
    if isinstance(data, str):
        return _clean_str(data)
    if isinstance(data, list):
        return [sanitize(i) for i in data]
    if isinstance(data, dict):
        return {k: sanitize(v) for k, v in data.items()}
    return data


__all__ = ["sanitize"]
