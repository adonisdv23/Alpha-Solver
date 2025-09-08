def get_remote_address(request):
    return request.client.host if request and request.client else "unknown"

__all__ = ["get_remote_address"]
