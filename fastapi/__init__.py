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
    def __init__(self, content, status_code: int = 200):
        self._content = json.dumps(content)
        self.status_code = status_code
        self.headers = {}
    def json(self):
        return json.loads(self._content)

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
    def get(self, path):
        return self._route("GET", path)
    def post(self, path):
        return self._route("POST", path)
    def _route(self, method, path):
        def decorator(func):
            self.routes[(method, path)] = func
            return func
        return decorator
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
