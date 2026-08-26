from datetime import datetime
from typing import Dict, List, Optional

from cats.signals.types import Message, SilenceResult

# Per-source-type anomaly thresholds (hours). All values are 96h (retuned
# from 72h 2026-08-26, see docs/silence_retune_2026-08.md): a threshold sweep
# on the committed calibration snapshots
# (research/gaming_volatility_diagnosis_spike.py) found rho strengthens
# monotonically from 24h to 96h then plateaus (96/120/168h are identical),
# so 96h is the smallest threshold that reaches the plateau on both splits.
# Changing any value alters silence scores and requires recalibration
# (docs/calibration.md).
SOURCE_TYPE_THRESHOLDS: Dict[str, float] = {
    "social": 96.0,
    "news": 96.0,
    "default": 96.0,
}


def threshold_for(source_type: str) -> float:
    return SOURCE_TYPE_THRESHOLDS.get(source_type, SOURCE_TYPE_THRESHOLDS["default"])


def compute_silence(
    messages: List[Message],
    source_type: str = "social",
    anomaly_threshold_hours: Optional[float] = None,
) -> SilenceResult:
    threshold = anomaly_threshold_hours if anomaly_threshold_hours is not None else threshold_for(source_type)
    if len(messages) < 2:
        return SilenceResult(
            name="silence",
            value=0.0,
            confidence=0.0,
            metadata={"reason": "insufficient_messages"},
        )
    ts = sorted(datetime.fromisoformat(m.timestamp.replace("Z", "+00:00")) for m in messages)
    gaps = [(ts[i] - ts[i - 1]).total_seconds() / 3600 for i in range(1, len(ts))]
    anomalies = sum(1 for g in gaps if g > threshold)
    max_gap = max(gaps) if gaps else 0.0
    score = min((anomalies / len(gaps)) * 100, 100.0) if gaps else 0.0
    return SilenceResult(
        name="silence",
        value=score,
        confidence=min(len(messages) / 30, 1.0),
        metadata={"threshold_h": threshold, "source_type": source_type},
        anomalous_gaps=anomalies,
        max_gap_hours=max_gap,
    )
