import json
import logging
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from service.validation.sanitizer import sanitize
from service.validation.validator import ValidationError, validate_request

logger = logging.getLogger("service.middleware.validation")


class ValidationMiddleware(BaseHTTPMiddleware):
    """Sanitize and validate incoming JSON requests before handlers."""

    async def dispatch(self, request: Request, call_next: Callable):  # type: ignore[override]
        try:
            payload = await request.json()
        except Exception:
            return JSONResponse(
                status_code=400,
                content={"code": "invalid_json", "errors": [{"field": "<body>", "reason": "invalid json", "code": "invalid_json"}]},
            )

        sanitized = sanitize(payload)
        try:
            validate_request(sanitized)
        except ValidationError as exc:
            return JSONResponse(status_code=400, content={"code": "invalid_request", "errors": exc.errors})

        request._body = json.dumps(sanitized).encode("utf-8")
        return await call_next(request)


__all__ = ["ValidationMiddleware"]
