# Alpha Solver Python SDK

Install locally:

```bash
pip install -e .
```

Usage:

```python
from alpha_client import AlphaClient

client = AlphaClient("http://localhost:8000")
print(client.solve(prompt="Explain 21*3 with brief rationale and answer.", strategy="react"))
```
