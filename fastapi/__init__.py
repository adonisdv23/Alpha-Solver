import json
from types import SimpleNamespace
from inspect import iscoroutinefunction

class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class Request:
    def __init__(self, headers=None, client=None, url=""):
        self.headers = headers or {}
        self.client = SimpleNamespace(host=client) if client else None
        self.url = SimpleNamespace(path=url)
        self.state = SimpleNamespace()

class JSONResponse:
    def __init__(self, content, status_code: int = 200, headers=None):
        self._content = json.dumps(content)
        self.status_code = status_code
        self.headers = headers or {}

    def json(self):
        return json.loads(self._content)

class Depends:
    def __init__(self, dependency):
        self.dependency = dependency


class FastAPI:
    def __init__(self, title: str = "", version: str = ""):
        self.title = title
        self.version = version
        self.routes = {}
        self.middlewares = []
        self.exception_handlers = {}
        self.state = SimpleNamespace()
        # minimal OpenAPI route for tests
        self.get("/openapi.json")(lambda: {"openapi": "3.0.0"})

    def get(self, path, dependencies=None):
        return self._route("GET", path, dependencies)

    def post(self, path, dependencies=None):
        return self._route("POST", path, dependencies)

    def _route(self, method, path, dependencies=None):
        deps = [d.dependency if isinstance(d, Depends) else d for d in (dependencies or [])]

        def decorator(func):
            async def wrapped(*args, **kwargs):
                req = kwargs.get("request")
                for dep in deps:
                    if iscoroutinefunction(dep):
                        await dep(req)
                    else:
                        dep(req)
                return (
                    await func(*args, **kwargs)
                    if iscoroutinefunction(func)
                    else func(*args, **kwargs)
                )

            wrapped.__wrapped__ = func
            self.routes[(method, path)] = wrapped
            return wrapped

        return decorator

    def add_middleware(self, mw_cls, **kwargs):
        async def wrapper(request, call_next):
            return await call_next(request)

        self.middlewares.append(wrapper)

    def middleware(self, kind):
        assert kind == "http"
        def decorator(func):
            self.middlewares.append(func)
            return func
        return decorator

    def exception_handler(self, exc_type):
        def decorator(func):
            self.exception_handlers[exc_type] = func
            return func
        return decorator

class trace:
    _provider = None
    @classmethod
    def set_tracer_provider(cls, provider):
        cls._provider = provider
    @classmethod
    def get_tracer_provider(cls):
        return cls._provider
