"""Prometheus metrics for the CATS API.

Metrics are registered on prometheus_client's default registry and exposed at
``GET /metrics`` (see cats.api.main). HTTP request count/latency are recorded by
a middleware; evaluation counters and the score histogram are updated in the
scoring path.
"""

from prometheus_client import Counter, Histogram

# HTTP-level metrics (labelled by the matched route template to bound cardinality).
HTTP_REQUESTS = Counter(
    "cats_http_requests_total",
    "Total HTTP requests handled",
    ["method", "path", "status"],
)
HTTP_LATENCY = Histogram(
    "cats_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

# Domain metrics.
EVALUATIONS = Counter(
    "cats_evaluations_total",
    "Total source evaluations scored, by band",
    ["band"],
)
TRUST_SCORE = Histogram(
    "cats_trust_score",
    "Distribution of computed trust scores (0-100)",
    buckets=(0, 20, 40, 60, 80, 100),
)
