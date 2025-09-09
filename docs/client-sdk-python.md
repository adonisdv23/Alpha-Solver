# Python Client SDK

A tiny wrapper around the HTTP API.

## Install

No extra dependencies are required; the client uses the Python standard library.

## Usage

```python
from clients.python.alpha_client import AlphaClient

client = AlphaClient("http://localhost:8000", "changeme")
result = client.solve("2+2?", strategy="react", context={"seed": 42})
print(result["final_answer"], result["confidence"])
```

## Error handling

`AlphaClient.solve` raises `RuntimeError` for non-retryable HTTP errors. Requests are retried with exponential backoff for `429` and `5xx` responses up to three attempts.

## Timeouts

`timeout` controls the socket timeout (seconds).
