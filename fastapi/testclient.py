import asyncio
from inspect import signature, iscoroutinefunction, _empty
from . import FastAPI, Request, JSONResponse, HTTPException
from opentelemetry import trace

class TestResponse:
    def __init__(self, response):
        self.status_code = getattr(response, "status_code", 200)
        self.headers = getattr(response, "headers", {})
        self._response = response
    def json(self):
        if hasattr(self._response, "json"):
            return self._response.json()
        return self._response
    @property
    def text(self):  # pragma: no cover - helper for tests
        body = getattr(self._response, "body", b"")
        if isinstance(body, (bytes, bytearray)):
            return body.decode()
        return str(body)

class TestClient:
    def __init__(self, app: FastAPI):
        self.app = app
    def _build_request(self, path, headers):
        return Request(headers=headers or {}, client="testclient", url=path)
    def _call(self, method, path, json=None, headers=None):
        request = self._build_request(path, headers)
        handler = self.app.routes[(method, path)]
        orig = getattr(handler, "__wrapped__", handler)
        async def call_endpoint(req):
            sig = signature(orig)
            kwargs = {}
            for name, param in sig.parameters.items():
                ann = param.annotation
                if isinstance(ann, str):
                    ann = orig.__globals__.get(ann, _empty)
                ann_name = getattr(ann, "__name__", "")
                if name == "request" or ann_name == "Request":
                    kwargs[name] = req
                else:
                    if ann is not _empty and ann_name not in ("dict", "str"):
                        kwargs[name] = ann(**(json or {}))
                    else:
                        kwargs[name] = json or {}
            result = await handler(**kwargs) if iscoroutinefunction(handler) else handler(**kwargs)
            if isinstance(result, dict):
                return JSONResponse(result)
            return result
        async def call_with_middlewares(req):
            async def next_handler(r):
                return await call_endpoint(r)
            for mw in reversed(self.app.middlewares):
                current = next_handler
                async def wrapper(r, mw=mw, current=current):
                    return await mw(r, current)
                next_handler = wrapper
            try:
                return await next_handler(req)
            except Exception as exc:
                handler = self.app.exception_handlers.get(type(exc))
                if handler:
                    return await handler(req, exc)
                if isinstance(exc, HTTPException):
                    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
                raise
        response = asyncio.run(call_with_middlewares(request))
        if isinstance(response, dict):
            response = JSONResponse(response)
        provider = trace.get_tracer_provider()
        if provider and hasattr(provider, "add_span"):
            provider.add_span(path)
        return TestResponse(response)
    def get(self, path, headers=None):
        return self._call("GET", path, headers=headers)
    def post(self, path, json=None, headers=None):
        return self._call("POST", path, json=json, headers=headers)

__all__ = ["TestClient"]
