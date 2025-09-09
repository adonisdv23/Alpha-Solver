from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

class Instrumentator:
    def instrument(self, app):
        self.app = app
        return self
    def expose(self, app, endpoint: str = "/metrics"):
        @app.get(endpoint)
        async def metrics():
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
        return self

__all__ = ["Instrumentator"]
