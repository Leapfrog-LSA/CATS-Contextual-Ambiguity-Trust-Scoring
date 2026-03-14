from datetime import datetime
from typing import List
from cats.signals.types import Message, SilenceResult


def compute_silence(
    messages: List[Message],
    source_type: str = "social",
    anomaly_threshold_hours: float = 72.0,
) -> SilenceResult:
    if len(messages) < 2:
        return SilenceResult(
            name="silence", value=0.0, confidence=0.0,
            metadata={"reason": "insufficient_messages"},
        )
    ts   = sorted(datetime.fromisoformat(m.timestamp.replace("Z", "+00:00")) for m in messages)
    gaps = [(ts[i] - ts[i - 1]).total_seconds() / 3600 for i in range(1, len(ts))]
    anomalies = sum(1 for g in gaps if g > anomaly_threshold_hours)
    max_gap   = max(gaps) if gaps else 0.0
    score     = min((anomalies / len(gaps)) * 100, 100.0) if gaps else 0.0
    return SilenceResult(
        name="silence",
        value=score,
        confidence=min(len(messages) / 30, 1.0),
        metadata={"threshold_h": anomaly_threshold_hours, "source_type": source_type},
        anomalous_gaps=anomalies,
        max_gap_hours=max_gap,
    )
