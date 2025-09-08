import time
from functools import wraps
from inspect import iscoroutinefunction
from .errors import RateLimitExceeded

class Limiter:
    def __init__(self, key_func):
        self.key_func = key_func
    def limit(self, rule: str):
        amount = int(rule.split('/')[0])
        window = 60
        def decorator(func):
            counts = {}
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = kwargs.get('request') or (args[0] if args else None)
                key = self.key_func(request)
                now = time.time()
                start, count = counts.get(key, (now, 0))
                if now - start >= window:
                    start, count = now, 0
                if count >= amount:
                    raise RateLimitExceeded()
                counts[key] = (start, count + 1)
                if iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)
            return wrapper
        return decorator

__all__ = ["Limiter", "RateLimitExceeded"]
