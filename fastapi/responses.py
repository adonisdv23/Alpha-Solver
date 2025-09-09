from . import JSONResponse


class Response:
    def __init__(self, content: bytes, media_type: str = "text/plain", status_code: int = 200, headers=None):
        self.body = content
        self.media_type = media_type
        self.status_code = status_code
        self.headers = headers or {}


__all__ = ["JSONResponse", "Response"]
