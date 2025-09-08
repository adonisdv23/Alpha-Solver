_provider = None

def set_tracer_provider(provider):
    global _provider
    _provider = provider


def get_tracer_provider():
    return _provider

__all__ = ["set_tracer_provider", "get_tracer_provider"]
