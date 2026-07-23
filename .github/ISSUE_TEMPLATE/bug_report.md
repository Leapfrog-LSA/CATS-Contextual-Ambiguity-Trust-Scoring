---
name: Bug report
about: Something in CATS isn't working as documented
title: "[Bug] "
labels: bug
assignees: ''
---

**Describe the bug**
A clear, concise description of what's wrong.

**To reproduce**
Steps to reproduce, ideally a minimal `cats.lite.score(...)` call or API
request that triggers it:

```python
from cats.lite import score

result = score([...], source_type="news")
```

**Expected behavior**
What you expected to happen instead.

**Actual behavior**
What actually happened — error message, wrong score, wrong signal value,
stack trace, etc.

**Environment**
- CATS version (`cats.__version__` or `pip show cats-scoring`):
- Install surface: `cats.lite` library / full API deployment (Docker) / dev checkout
- Python version:
- OS:

**Additional context**
Anything else relevant — logs, `/health` output, whether the spaCy model /
optional SBERT/BERT backends were installed.
