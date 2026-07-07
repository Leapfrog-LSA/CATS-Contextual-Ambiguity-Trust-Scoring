from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Message:
    timestamp: str  # ISO 8601 UTC
    text: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SignalResult:
    name: str
    value: float  # 0-100
    confidence: float  # 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CoherenceResult(SignalResult):
    entity_overlap: float = 0.0
    jaccard_similarity: float = 0.0


@dataclass
class VolatilityResult(SignalResult):
    sentiment_spikes: int = 0
    max_delta: float = 0.0


@dataclass
class SilenceResult(SignalResult):
    anomalous_gaps: int = 0
    max_gap_hours: float = 0.0


@dataclass
class GamingResult(SignalResult):
    repetition_score: float = 0.0
    ttr_score: float = 0.0
    burst_score: float = 0.0
    vocab_score: float = 0.0


@dataclass
class DomainProvenanceResult(SignalResult):
    # `value` is a 0-100 red-flag score (higher = more impersonation/clone
    # signals) — a higher-is-worse signal, to be inverted at aggregation like
    # volatility/silence/gaming when/if it is wired into scoring.
    suspicious_tld: bool = False
    free_host: bool = False
    typosquat: bool = False
    brand_on_bad_tld: bool = False
    host: str = ""
