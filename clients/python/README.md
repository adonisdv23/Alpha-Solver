# Alpha Solver Python SDK

Install locally:

```bash
pip install -e .
```

Usage:

```python
from alpha_solver_sdk import AlphaClient
client = AlphaClient("http://localhost:8000", api_key="changeme")
print(client.solve("2+2?", strategy="react"))
```
