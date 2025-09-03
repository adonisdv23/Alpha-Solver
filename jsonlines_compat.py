import json
import builtins
from typing import Iterator

_open = builtins.open

class _Writer:
    def __init__(self, path, mode='a'):
        self._f = _open(path, mode, encoding='utf-8')
    def write(self, obj):
        self._f.write(json.dumps(obj) + "\n")
    def close(self):
        self._f.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        self.close()

class _Reader:
    def __init__(self, f):
        self._f = f
    def __iter__(self) -> Iterator:
        for line in self._f:
            line = line.strip()
            if line:
                yield json.loads(line)
    def close(self):
        self._f.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        self.close()

class Reader(_Reader):
    pass

class Writer(_Writer):
    pass

def open(path, mode='r'):
    if 'r' in mode:
        f = _open(path, mode, encoding='utf-8')
        return _Reader(f)
    else:
        return _Writer(path, mode)
