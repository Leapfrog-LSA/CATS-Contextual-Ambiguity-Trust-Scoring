"""Prometheus metrics for the CATS API.

Metrics are registered on prometheus_client's default registry and exposed at
``GET /metrics`` (see cats.api.main). HTTP request count/latency are recorded by
a middleware; evaluation counters and the score histogram are updated in the
scoring path.

With several uvicorn workers each process has its own counters, so a scrape
would see only the worker that answered it. Setting ``PROMETHEUS_MULTIPROC_DIR``
(as the ``Dockerfile`` does) switches prometheus_client to its multiprocess
mode: every worker writes its values to that directory and ``render_latest``
aggregates them.
"""

import os

from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest, multiprocess

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


def render_latest() -> bytes:
    """Metrics in the Prometheus text format, aggregated across workers when needed.

    Reads ``PROMETHEUS_MULTIPROC_DIR`` from the process environment, not from
    ``cats.core.config``: prometheus_client itself picks its storage from that
    variable at import time, so this branch must follow the same source.
    """
    if os.environ.get("PROMETHEUS_MULTIPROC_DIR"):
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        return generate_latest(registry)
    return generate_latest()
