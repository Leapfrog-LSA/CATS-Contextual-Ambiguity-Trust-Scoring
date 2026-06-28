"""Labelled dataset loading for weight calibration.

A calibration dataset is a list of records, each carrying the four CATS signal
values for one evaluation plus a ground-truth ``label`` expressing how reliable
that source actually was (higher = more reliable). Labels only need to be
*ordinally* meaningful, since calibration optimises rank agreement.

Supported formats:
  * ``.jsonl`` — one JSON object per line
  * ``.json``  — a JSON array, or an object with a top-level ``samples`` list

Each record:
    {"source_type": "social",
     "signals": {"coherence": 71.2, "volatility": 55.0, "silence": 0.0, "gaming": 12.8},
     "label": 80.0}
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Union

SIGNAL_NAMES = ("coherence", "volatility", "silence", "gaming")


@dataclass
class LabeledSample:
    source_type: str
    signals: Dict[str, float]  # signal name -> value in [0, 100]
    label: float  # ground-truth reliability; higher = more reliable

    def __post_init__(self) -> None:
        missing = [s for s in SIGNAL_NAMES if s not in self.signals]
        if missing:
            raise ValueError(f"sample missing signal(s): {missing}")


def _read_records(path: Path) -> List[dict]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in raw.splitlines() if line.strip()]
    data = json.loads(raw)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("samples"), list):
        return data["samples"]
    raise ValueError("JSON dataset must be a list or an object with a 'samples' list")


def load_dataset(path: Union[str, Path]) -> List[LabeledSample]:
    samples = [
        LabeledSample(
            source_type=str(r.get("source_type", "unknown")),
            signals={k: float(v) for k, v in r["signals"].items()},
            label=float(r["label"]),
        )
        for r in _read_records(Path(path))
    ]
    if not samples:
        raise ValueError("dataset is empty")
    return samples
