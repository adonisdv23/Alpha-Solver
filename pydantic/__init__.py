class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)
    def dict(self):
        return self.__dict__


def Field(default=None, **kwargs):
    return default


__all__ = ["BaseModel", "Field"]
