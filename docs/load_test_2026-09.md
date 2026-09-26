# API load test — 26 September 2026

Roadmap Fase 2, "Rafforzare l'API": measure how `/evaluate` and `/batch` behave
under load before anyone external depends on the deployment. Reproducible with
[`research/load_test_api.py`](../research/load_test_api.py).

## Summary

1. **Concurrent requests collapse throughput.**

   | 10-message evaluations | Throughput | Median latency |
   |---|--:|--:|
   | 1 client | 9.3 req/s | 0.10 s |
   | 4 clients | 1.3 req/s | 3.0 s |

   With 16 clients sending 200-message histories, 8 of 12 requests did not
   finish within 300 s.

   The cause is reproduced outside the API. spaCy's `nlp()` called from
   several threads at once runs about 9× slower than the same calls made one
   after another. The API calls it from a shared thread pool. Serialising
   the spaCy calls restores the sequential speed. It is a scheduling fix,
   so the scores do not change. It is **not** applied here.
2. **One evaluation costs about 25–40 µs per character of text**, almost all
   of it in `coherence` (spaCy NER). A 10-message request takes about 0.1 s.
   A 500-message request takes 6–19 s, depending on how long the texts are.
3. **The proxy times out before the app finishes large requests that the
   proxy itself accepts.** A 1.68 MB body, under the 2 MB cap, took 36.9 s on
   the app. Sent through nginx, it got `504` after 30 s (`proxy_read_timeout`).
4. **Resources:** about 1.1 GB RSS after start-up (the spaCy model), 1.35 GB at
   peak. A single uvicorn worker (as in the `Dockerfile`) never used more
   than ~1.5 of the 4 cores.

None of this changes a score. These are capacity and operability findings. The
recommendations are at the end, and each one is a separate change.

## Setup

| | |
|---|---|
| Machine | 4 vCPU Intel Xeon @ 2.10 GHz, 16 GB RAM (cloud container) |
| Software | Python 3.11.15, spaCy 3.8.16 (`it_core_news_lg`), FastAPI 0.141.1, uvicorn 0.53.0 |
| App | `uvicorn cats.api.main:app`, one worker as in the `Dockerfile`, local Postgres 16 and Redis 7, default `COHERENCE_BACKEND=ner` |
| Rate limit | App limit raised (`REDIS_RATE_LIMIT_MAX=1000000`) so the limiter does not cap the measurement |
| Client | `research/load_test_api.py` on the same machine over loopback, direct to the app. nginx caps each IP at 30 req/min, so through it a single load generator mostly measures `429`s. That cap is a deliberate production control |
| Payload | Real feed texts from `data/snapshots/labelled_sources_2026-09-26.jsonl` (3 898 texts, ≤ 10 000 chars each), hourly timestamps, `source_type: news` |

Command (single-client runs):

```bash
REDIS_RATE_LIMIT_MAX=1000000 uvicorn cats.api.main:app --port 8000
python research/load_test_api.py --api-key "$CATS_API_KEY" \
    --messages 10 50 200 500 --concurrency 1 --requests 6 \
    --batch-items 10 50 --batch-requests 3
```

Samples are small (6–12 requests per scenario), so p95/p99 are close to the
maximum. Read them as orders of magnitude, not precise percentiles.

## Results

### One client at a time

| Scenario | Requests | req/s | msgs/s | p50 | p95 / max |
|---|--:|--:|--:|--:|--:|
| `/evaluate` 10 msgs | 6 | 8.76 | 88 | 0.09 s | 0.16 s |
| `/evaluate` 50 msgs | 6 | 1.85 | 93 | 0.53 s | 0.72 s |
| `/evaluate` 200 msgs | 6 | 0.19 | 38 | 2.1 s | 16.2 s |
| `/evaluate` 500 msgs | 6 | 0.11 | 55 | 5.9 s | 19.4 s |
| `/batch` 10 items × 20 msgs (95 KB) | 3 | 0.52 | 104 | 1.9 s | 2.0 s |
| `/batch` 50 items × 20 msgs (580 KB) | 3 | 0.06 | 60 | 15.3 s | 24.9 s |

The long tail at 200/500 messages follows the **amount of text**, not the
message count. Timing `coherence` alone on six 200-message histories:

| Text in the request | `coherence` time | Cost per character |
|--:|--:|--:|
| 43k chars | 1.8 s | 41 µs/char |
| 57k chars | 2.1 s | 37 µs/char |
| 151k chars | 4.5 s | 30 µs/char |
| 624k chars (long articles) | 15.8 s | 25 µs/char |

Per-signal cost for 500 messages, measured in process:

| Signal | Time |
|---|--:|
| `coherence` | 4.7 s |
| `volatility` | 0.12 s |
| `gaming` | 0.01 s |
| `silence` | < 1 ms |
| language detection | 0.01 s |

`/batch` scores its items one after another, so its time is roughly the sum of
its items.

### Concurrent clients

| Scenario | Clients | req/s | p50 | p95 |
|---|--:|--:|--:|--:|
| `/evaluate` 10 msgs | 1 | 9.29 | 0.10 s | 0.15 s |
| `/evaluate` 10 msgs | 4 | **1.26** | **3.0 s** | 3.8 s |
| `/evaluate` 50 msgs | 1 | 2.01 | 0.50 s | 0.62 s |
| `/evaluate` 50 msgs | 4 | **0.21** | **18.6 s** | 25.1 s |

With purely CPU-bound work and no contention, throughput should stay flat as
clients are added, and latency should grow about linearly with them. Instead,
throughput fell about 7–10×.

An earlier full run went further before it was stopped. Its client timeout was
300 s, and the requests that timed out kept the server busy, which contaminated
the scenarios after them. It showed:

| Scenario | Median latency | Requests finished |
|---|--:|--:|
| 10 msgs, 16 clients | 10.5 s | all |
| 50 msgs, 16 clients | 83.5 s | all |
| 200 msgs, 4 clients | 91.8 s | 11 of 12 |
| 200 msgs, 16 clients | — | 4 of 12 within 300 s |

The 500-message and batch scenarios under concurrency were not measured. The
result would only restate the collapse above.

### Root cause: spaCy called from several threads at once

`/evaluate` computes its four signals with `loop.run_in_executor(None, …)`,
which uses the default thread pool (8 threads on this machine). That pool is
shared by all in-flight requests, so concurrent requests run spaCy `nlp()`
calls in parallel threads.

Same 12 `coherence` calls (10 messages each) in process, outside the API:

| Execution | Time |
|---|--:|
| sequential, 1 thread | 1.0 s |
| 4 threads | 9.5 s |
| 8 threads | 15.5 s |
| 4 threads, spaCy calls behind a lock | **1.02 s** |
| `volatility` (TextBlob), 1 thread → 4 threads | 0.09 s → 0.03 s (speeds up, as it should) |

Ruled out: BLAS/OpenMP oversubscription. Setting `OMP_NUM_THREADS`,
`OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` and `BLIS_NUM_THREADS` to 1 left both
the API numbers and the in-process numbers unchanged.

### Proxy timeout vs. body cap

| Request (200 msgs × 7 500 chars, 1.68 MB body, under the 2 MB cap) | Result |
|---|---|
| direct to the app | `200` after 36.9 s |
| through the bundled nginx | `504` after 30.0 s (`proxy_read_timeout 30s`) |

At 25–40 µs per character, anything above roughly 0.8–1.2 M characters of text
in one request cannot complete through the proxy. The 2 MB cap allows about
2 M characters. Whether the app still persists the evaluation after nginx gives
up was not checked.

### Memory and CPU

The app process measured about 1.1 GB RSS after start-up (spaCy
`it_core_news_lg` loaded) and 1.35 GB at peak during the runs. CPU peaked at
~150% of one core: a single worker cannot use the 4 cores.

## Update — recommendation 1 applied (26 Sep 2026)

`cats/api/routes/evaluate.py` now runs `coherence` on a dedicated
single-thread executor shared by every request (`_NLP_EXECUTOR`). The other
three signals stay on the default pool.

Same machine, same script and parameters as the concurrency table above:

| Scenario | Clients | Before: req/s | After: req/s | Before: p50 | After: p50 |
|---|--:|--:|--:|--:|--:|
| `/evaluate` 10 msgs | 1 | 9.29 | 9.83 | 0.10 s | 0.10 s |
| `/evaluate` 10 msgs | 4 | 1.26 | **10.45** | 3.0 s | **0.37 s** |
| `/evaluate` 10 msgs | 16 | — | **10.28** | 10.5 s ¹ | **0.67 s** |
| `/evaluate` 50 msgs | 1 | 2.01 | 1.92 | 0.50 s | 0.48 s |
| `/evaluate` 50 msgs | 4 | 0.21 | **1.93** | 18.6 s | **1.9 s** |
| `/evaluate` 50 msgs | 16 | — | **1.99** | 83.5 s ¹ | **3.7 s** |

¹ From the aborted full run, where only the median was recorded.

- **Throughput now stays flat as clients are added**, and latency grows about
  linearly with the queue, which is what one serialised NLP thread should
  give.
- **Scores are unchanged.** Four fixed payloads (5, 30, 120 and 300
  messages) gave byte-identical responses before and after: score, band,
  and every signal value and confidence.

Capacity is still bounded by one NLP thread per process, about 100 messages/s
on this machine. Recommendation 2, more workers, is the way to use the other
cores.

## Recommendations

1. **Done, see the update above.** Serialise the spaCy calls: run `coherence` on a dedicated
   single-thread executor in `cats/api/routes/evaluate.py`, or put a lock
   around `nlp()` in `cats/signals/coherence.py`, which is a maintainer-gated
   file.
   - Scores are unchanged: it is scheduling only.
   - The in-process test above says concurrent throughput returns to the
     single-client rate, about 9 req/s at 10 messages, instead of 1.3 req/s.
   - Re-run this test after the change to confirm it end to end.
2. **Scale with processes, not threads.** Several uvicorn workers use the other
   cores, at about 1.1 GB of RAM each for the spaCy model. Size them after
   step 1.
3. **Make the proxy timeout and the request limits agree.** Either raise
   `proxy_read_timeout` above the worst case the body cap allows, or cap the
   total text per request, so that an accepted request can finish. This is a
   product decision: long synchronous requests versus a lower documented cap.
4. **Cheaper NER.** Batch the NER with `nlp.pipe` and disable the pipeline
   components coherence does not use. This touches `cats/signals/coherence.py`,
   which is maintainer-gated. It must be shown to give identical entities before
   it ships.

## Limitations

- **One machine, loopback, no network.** Postgres and Redis were local.
  Production latency adds the network and the proxy.
- **Default NER backend only.** The calibrated weights assume
  `COHERENCE_BACKEND=sbert` (see `calibration.md`), which has a different cost
  profile. This test did not measure it.
- **Small samples.** Samples of 6–12 requests per scenario make the tail
  percentiles approximate.
- **Messages per second assumes one text mix.** It depends on text length:
  news items from one snapshot.
