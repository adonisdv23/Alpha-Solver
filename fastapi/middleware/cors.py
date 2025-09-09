class CORSMiddleware:
    def __init__(self, app, **kwargs):
        self.app = app
        self.kwargs = kwargs

    async def __call__(self, request, call_next):
        return await call_next(request)
