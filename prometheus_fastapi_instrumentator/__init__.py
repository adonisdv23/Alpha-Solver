from fastapi import JSONResponse

class Instrumentator:
    def instrument(self, app):
        self.app = app
        return self
    def expose(self, app):
        @app.get("/metrics")
        async def metrics():
            return JSONResponse({})
        return self

__all__ = ["Instrumentator"]
