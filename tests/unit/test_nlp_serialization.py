"""The API runs coherence (spaCy / SBERT) on one dedicated thread.

spaCy's ``nlp()`` slows down sharply when several threads call it at once (the
2026-09 load test, docs/load_test_2026-09.md). The route therefore sends
coherence to a single-thread executor shared by every request. These tests pin
that behaviour without loading any model:
* coherence never overlaps across concurrent evaluations and runs on that
  thread;
* the other signals still run in parallel.
"""

import asyncio
import threading
import time

import cats.api.routes.evaluate as route


class _Probe:
    """Records how many calls overlap and which threads they ran on."""

    def __init__(self, name: str, delay: float = 0.03):
        self.name = name
        self.delay = delay
        self.active = 0
        self.peak = 0
        self.threads: set = set()
        self._lock = threading.Lock()

    def __call__(self, *args):
        with self._lock:
            self.active += 1
            self.peak = max(self.peak, self.active)
            self.threads.add(threading.current_thread().name)
        time.sleep(self.delay)
        with self._lock:
            self.active -= 1
        return (self.name, args[1:])  # args[0] is the message list


def _patch(monkeypatch):
    probes = {name: _Probe(name) for name in ("coherence", "volatility", "silence", "gaming")}
    monkeypatch.setattr(route, "compute_coherence", probes["coherence"])
    monkeypatch.setattr(route, "compute_volatility", probes["volatility"])
    monkeypatch.setattr(route, "compute_silence", probes["silence"])
    monkeypatch.setattr(route, "compute_gaming", probes["gaming"])
    return probes


async def test_signals_are_returned_in_order_with_source_type(monkeypatch):
    _patch(monkeypatch)
    results = await route._compute_behavioural_signals([], "news")
    assert results == [("coherence", ()), ("volatility", ()), ("silence", ("news",)), ("gaming", ())]


async def test_coherence_never_overlaps_across_concurrent_evaluations(monkeypatch):
    probes = _patch(monkeypatch)
    await asyncio.gather(*(route._compute_behavioural_signals([], "news") for _ in range(6)))
    assert probes["coherence"].peak == 1
    assert probes["coherence"].threads and all(t.startswith("cats-nlp") for t in probes["coherence"].threads)


async def test_other_signals_still_run_in_parallel(monkeypatch):
    # Only the NLP signal is serialised. Queuing everything behind one thread
    # would needlessly slow the cheap signals.
    probes = _patch(monkeypatch)
    await asyncio.gather(*(route._compute_behavioural_signals([], "news") for _ in range(6)))
    assert probes["volatility"].peak > 1
    assert not any(t.startswith("cats-nlp") for t in probes["volatility"].threads)
