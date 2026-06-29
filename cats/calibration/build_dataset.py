"""Build a calibration dataset from labelled sources.

The calibrator (:mod:`cats.calibration`) consumes records of the shape::

    {"source_type": "news",
     "signals": {"coherence": 71.2, "volatility": 30.0, "silence": 10.0, "gaming": 12.0},
     "label": 85.0}

Producing the ``signals`` block by hand is impractical: the four values come
out of the same pipeline that ``/evaluate`` runs. This module bridges the gap.
Given *labelled sources* — each a list of timestamped messages plus a
ground-truth reliability ``label`` — it runs the exact CATS signal pipeline
(normalise → coherence/volatility/silence/gaming) and emits the ready-to-load
``.jsonl``.

Input format (``--input``), one source per record, ``.json`` (array or
``{"sources": [...]}``) or ``.jsonl``::

    {"source_id": "twitter:acme",
     "source_type": "social",
     "label": 80.0,
     "messages": [
        {"timestamp": "2026-01-01T08:00:00Z", "text": "..."},
        {"timestamp": "2026-01-01T09:00:00Z", "text": "..."}
     ]}

``source_id`` is optional (used only for diagnostics). ``source_type`` is
optional and falls back to ``--source-type``. ``label`` must be numeric.

Usage::

    python -m cats.calibration.build_dataset --input sources.jsonl --out train.jsonl

The four signals share the runtime's behaviour, so the coherence backend
honours ``CATS_*`` settings. The spaCy NER model is loaded once up front (unless
``--no-init-nlp``); without it, coherence degrades to a neutral, zero-confidence
value exactly as it does at request time.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import structlog

from cats.pipeline.normalizer import normalize_messages
from cats.signals.coherence import compute_coherence
from cats.signals.gaming import compute_gaming
from cats.signals.silence import compute_silence
from cats.signals.types import SignalResult
from cats.signals.volatility import compute_volatility

logger = structlog.get_logger()

DEFAULT_SOURCE_TYPE = "social"


@dataclass
class BuildStats:
    written: int = 0
    skipped: int = 0
    per_source_type: Optional[Dict[str, int]] = None

    def __post_init__(self) -> None:
        if self.per_source_type is None:
            self.per_source_type = {}


def _read_source_records(path: Path) -> List[dict]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in raw.splitlines() if line.strip()]
    data = json.loads(raw)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("sources"), list):
        return data["sources"]
    raise ValueError("JSON input must be a list or an object with a 'sources' list")


def compute_signals(messages: List[dict], source_type: str) -> Dict[str, float]:
    """Run the 4-signal pipeline for one source, mirroring ``/evaluate``.

    ``messages`` is a list of ``{"timestamp", "text", ["metadata"]}`` dicts.
    Returns the signal-name -> value mapping the calibrator expects.
    """
    msgs = normalize_messages(messages)
    if not msgs:
        raise ValueError("no valid messages after normalisation")
    signals: List[SignalResult] = [
        compute_coherence(msgs),
        compute_volatility(msgs),
        compute_silence(msgs, source_type),
        compute_gaming(msgs),
    ]
    return {s.name: round(s.value, 4) for s in signals}


def build_record(source: dict, default_source_type: str) -> dict:
    """Turn one labelled-source record into a calibration sample.

    Raises ``ValueError`` / ``KeyError`` for malformed sources so the caller can
    skip them with a diagnostic.
    """
    if "label" not in source:
        raise ValueError("missing 'label'")
    label = float(source["label"])
    messages = source.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("missing or empty 'messages'")
    source_type = str(source.get("source_type") or default_source_type)
    signals = compute_signals(messages, source_type)
    return {"source_type": source_type, "signals": signals, "label": label}


def build_dataset(
    sources: List[dict],
    default_source_type: str = DEFAULT_SOURCE_TYPE,
) -> tuple[List[dict], BuildStats]:
    """Build calibration samples from labelled sources, skipping bad records."""
    records: List[dict] = []
    stats = BuildStats()
    assert stats.per_source_type is not None  # for type checkers
    for i, source in enumerate(sources):
        sid = source.get("source_id", f"#{i}") if isinstance(source, dict) else f"#{i}"
        try:
            record = build_record(source, default_source_type)
        except (ValueError, KeyError, TypeError) as exc:
            logger.warning("build_dataset_skip", source=sid, error=str(exc))
            stats.skipped += 1
            continue
        records.append(record)
        stats.written += 1
        st = record["source_type"]
        stats.per_source_type[st] = stats.per_source_type.get(st, 0) + 1
    return records, stats


def _write_jsonl(records: List[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _maybe_init_nlp() -> None:
    """Load the spaCy NER model so coherence runs at full fidelity.

    Without it the coherence signal degrades to a neutral, zero-confidence value
    (same behaviour as a request when the model is unavailable), which would bias
    calibration — so warn loudly rather than fail.
    """
    from cats.signals import coherence

    try:
        coherence.init_nlp()
    except Exception as exc:  # spaCy / model missing
        logger.warning(
            "build_dataset_nlp_unavailable",
            error=str(exc),
            hint="run `make nlp-download`; coherence will be neutral/0-confidence",
        )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m cats.calibration.build_dataset",
        description="Run the CATS signal pipeline over labelled sources to produce a calibration .jsonl.",
    )
    parser.add_argument("--input", required=True, type=Path, help="labelled sources (.json or .jsonl)")
    parser.add_argument("--out", required=True, type=Path, help="output calibration dataset (.jsonl)")
    parser.add_argument(
        "--source-type",
        default=DEFAULT_SOURCE_TYPE,
        help=f"fallback source_type for records that omit it (default: {DEFAULT_SOURCE_TYPE})",
    )
    parser.add_argument(
        "--no-init-nlp",
        action="store_true",
        help="skip loading the spaCy model (coherence will be neutral/0-confidence)",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        parser.error(f"input file not found: {args.input}")

    if not args.no_init_nlp:
        _maybe_init_nlp()

    sources = _read_source_records(args.input)
    if not sources:
        parser.error(f"no source records found in {args.input}")

    records, stats = build_dataset(sources, default_source_type=args.source_type)
    if not records:
        print("No valid records produced; nothing written.", file=sys.stderr)
        return 1

    _write_jsonl(records, args.out)

    print(f"Wrote {stats.written} sample(s) to {args.out} ({stats.skipped} skipped).")
    print("Per source_type:")
    for st, n in sorted((stats.per_source_type or {}).items()):
        print(f"  {st:12s} {n}")
    print(
        "\nNext: temporal train/holdout split, then\n"
        f"  python -m cats.calibration --dataset {args.out} --out calibrated_weights.json --metric spearman"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
