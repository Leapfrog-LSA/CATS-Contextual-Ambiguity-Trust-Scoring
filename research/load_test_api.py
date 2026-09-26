"""Load test for the CATS API's scoring endpoints (/evaluate and /batch).

Roadmap Fase 2 ("Rafforzare l'API"): measure how the deployment behaves under
load before anyone external depends on it. The script answers three questions:

* How long does one evaluation take as the message history grows (10 → 500
  messages, the schema maximum)?
* How does latency degrade and throughput scale as concurrent clients are added?
* How long does a /batch take, since items run sequentially within a request?

It only needs ``httpx``, already a runtime dependency. Message texts are real
feed items taken from a committed snapshot (``data/snapshots/``), so the NLP
cost is representative of Italian/English news text. With no snapshot it falls
back to synthetic Italian sentences and says so in the output.

Run the app first, with the app-level rate limit raised so the limiter does not
cap the measurement (the default is 30 requests per 60 s per API key)::

    REDIS_RATE_LIMIT_MAX=1000000 uvicorn cats.api.main:app --port 8000
    python research/load_test_api.py --api-key "$CATS_API_KEY"

Measure the app directly, not through the bundled nginx. nginx caps each client
IP at 30 requests/min (burst 10), so through it a single load generator mostly
measures 429s. That cap is a deliberate production control, documented in
docs/api.md → *Limits and errors*.

Results for 2026-09 are written up in docs/load_test_2026-09.md.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import httpx

ROOT = Path(__file__).resolve().parent.parent
SNAP_DIR = ROOT / "data" / "snapshots"

_SYNTHETIC = [
    "Il governo annuncia un nuovo piano economico per il prossimo anno.",
    "I sindacati chiedono un incontro urgente sul rinnovo dei contratti.",
    "Il parlamento discute la legge di bilancio tra forti tensioni.",
    "La banca centrale lascia invariati i tassi di interesse.",
    "Proteste in piazza a Roma contro la riforma delle pensioni.",
]


@dataclass
class Result:
    scenario: str
    concurrency: int
    requests: int
    ok: int
    errors: Dict[str, int]
    wall_s: float
    throughput_rps: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    max_ms: float
    messages_per_request: int
    extra: Dict[str, object] = field(default_factory=dict)


def load_texts(limit: int = 5000) -> tuple[List[str], str]:
    """Up to ``limit`` real message texts from the newest committed snapshot."""
    snapshots = sorted(SNAP_DIR.glob("labelled_sources_*.jsonl"))
    if not snapshots:
        return list(_SYNTHETIC), "synthetic (no snapshot found)"
    newest = snapshots[-1]
    texts: List[str] = []
    with newest.open(encoding="utf-8") as handle:
        records = sorted((json.loads(line) for line in handle if line.strip()), key=lambda r: str(r.get("source_id")))
    for record in records:
        for message in record.get("messages") or []:
            text = str(message.get("text") or "").strip()
            if text:
                texts.append(text[:10_000])
            if len(texts) >= limit:
                return texts, newest.name
    return texts or list(_SYNTHETIC), newest.name


def make_item(texts: Sequence[str], n_messages: int, offset: int, source_id: str) -> dict:
    """One /evaluate body: ``n_messages`` messages, hourly timestamps, real texts."""
    start = datetime(2026, 9, 1, tzinfo=timezone.utc)
    messages = [
        {
            "timestamp": (start + timedelta(hours=i)).isoformat().replace("+00:00", "Z"),
            "text": texts[(offset + i) % len(texts)],
        }
        for i in range(n_messages)
    ]
    return {"source_id": source_id, "messages": messages, "context": {"source_type": "news"}}


def _pct(sorted_ms: List[float], p: float) -> float:
    if not sorted_ms:
        return float("nan")
    k = min(len(sorted_ms) - 1, max(0, int(round(p * (len(sorted_ms) - 1)))))
    return sorted_ms[k]


async def run_scenario(
    client: httpx.AsyncClient,
    path: str,
    bodies: List[dict],
    concurrency: int,
    scenario: str,
    messages_per_request: int,
) -> Result:
    """Send every body once with at most ``concurrency`` requests in flight."""
    queue: asyncio.Queue = asyncio.Queue()
    for body in bodies:
        queue.put_nowait(body)
    latencies: List[float] = []
    errors: Dict[str, int] = {}

    async def worker() -> None:
        while True:
            try:
                body = queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            t0 = time.perf_counter()
            try:
                r = await client.post(path, json=body)
                code = str(r.status_code)
            except httpx.HTTPError as exc:
                code = type(exc).__name__
            elapsed = (time.perf_counter() - t0) * 1000
            if code == "200":
                latencies.append(elapsed)
            else:
                errors[code] = errors.get(code, 0) + 1

    t_start = time.perf_counter()
    await asyncio.gather(*(worker() for _ in range(concurrency)))
    wall = time.perf_counter() - t_start
    lat = sorted(latencies)
    return Result(
        scenario=scenario,
        concurrency=concurrency,
        requests=len(bodies),
        ok=len(lat),
        errors=errors,
        wall_s=round(wall, 2),
        throughput_rps=round(len(lat) / wall, 2) if wall else 0.0,
        p50_ms=round(_pct(lat, 0.50), 1),
        p95_ms=round(_pct(lat, 0.95), 1),
        p99_ms=round(_pct(lat, 0.99), 1),
        max_ms=round(lat[-1], 1) if lat else float("nan"),
        messages_per_request=messages_per_request,
    )


def render(results: List[Result]) -> str:
    lines = [
        "| scenario | conc. | req | ok | errors | wall s | req/s | msgs/s | p50 ms | p95 ms | p99 ms | max ms |",
        "|---|--:|--:|--:|---|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for r in results:
        errs = ", ".join(f"{k}×{v}" for k, v in sorted(r.errors.items())) or "—"
        msgs_s = round(r.throughput_rps * r.messages_per_request, 1)
        lines.append(
            f"| {r.scenario} | {r.concurrency} | {r.requests} | {r.ok} | {errs} | {r.wall_s} | "
            f"{r.throughput_rps} | {msgs_s} | {r.p50_ms} | {r.p95_ms} | {r.p99_ms} | {r.max_ms} |"
        )
    return "\n".join(lines)


async def main_async(args: argparse.Namespace) -> int:
    texts, text_source = load_texts()
    print(f"Message texts: {len(texts)} from {text_source}", file=sys.stderr)
    headers = {"Authorization": f"Bearer {args.api_key}"}
    timeout = httpx.Timeout(args.timeout)
    limits = httpx.Limits(max_connections=max(args.concurrency) + 4)
    results: List[Result] = []

    async with httpx.AsyncClient(base_url=args.base_url, headers=headers, timeout=timeout, limits=limits) as client:
        # Warm-up: first request pays lazy initialisation (model caches, DB pool).
        warm = await client.post("/v1/cats/evaluate", json=make_item(texts, 10, 0, "load:warmup"))
        if warm.status_code != 200:
            print(f"Warm-up failed: HTTP {warm.status_code} {warm.text[:200]}", file=sys.stderr)
            return 1

        for n in args.messages:
            for c in args.concurrency:
                bodies = [make_item(texts, n, i * n, f"load:eval:{n}:{c}:{i}") for i in range(args.requests)]
                res = await run_scenario(client, "/v1/cats/evaluate", bodies, c, f"/evaluate {n} msgs", n)
                results.append(res)
                print(f"  done: {res.scenario} c={c} ok={res.ok}/{res.requests} p50={res.p50_ms}ms", file=sys.stderr)

        for items in args.batch_items:
            bodies = [
                {
                    "items": [
                        make_item(texts, args.batch_messages, (j * items + k) * args.batch_messages, f"load:b:{j}:{k}")
                        for k in range(items)
                    ]
                }
                for j in range(args.batch_requests)
            ]
            size_kb = round(len(json.dumps(bodies[0]).encode()) / 1024, 1)
            res = await run_scenario(
                client,
                "/v1/cats/batch",
                bodies,
                1,
                f"/batch {items}×{args.batch_messages} msgs",
                items * args.batch_messages,
            )
            res.extra["body_kb"] = size_kb
            results.append(res)
            print(
                f"  done: {res.scenario} ok={res.ok}/{res.requests} p50={res.p50_ms}ms ({size_kb} KB)", file=sys.stderr
            )

    if any("429" in r.errors for r in results):
        print(
            "\nWARNING: 429 responses: the app's rate limiter capped the run. Restart the app with "
            "REDIS_RATE_LIMIT_MAX raised (see the module docstring).",
            file=sys.stderr,
        )
    print(render(results))
    if args.json:
        payload = {"text_source": text_source, "base_url": args.base_url, "results": [asdict(r) for r in results]}
        Path(args.json).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Load-test /evaluate and /batch on a running CATS API.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--messages", type=int, nargs="+", default=[10, 50, 200, 500], help="messages per /evaluate")
    parser.add_argument("--concurrency", type=int, nargs="+", default=[1, 4, 16], help="concurrent clients")
    parser.add_argument("--requests", type=int, default=12, help="requests per /evaluate scenario")
    parser.add_argument("--batch-items", type=int, nargs="*", default=[10, 50], help="items per /batch request")
    parser.add_argument("--batch-messages", type=int, default=20, help="messages per /batch item")
    parser.add_argument("--batch-requests", type=int, default=5, help="requests per /batch scenario")
    parser.add_argument("--timeout", type=float, default=300.0, help="per-request timeout, seconds")
    parser.add_argument("--json", default=None, help="also write the raw results to this JSON file")
    args = parser.parse_args(argv)
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
