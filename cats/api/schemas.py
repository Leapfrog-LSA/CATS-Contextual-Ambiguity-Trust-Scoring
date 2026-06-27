from pydantic import BaseModel, Field, field_validator
from typing import Any, Dict, List, Optional


class MessageSchema(BaseModel):
    timestamp: str = Field(..., description="ISO 8601 UTC (e.g. 2024-01-15T10:00:00Z)")
    text: str = Field(..., min_length=1, max_length=10_000)
    metadata: Optional[Dict[str, Any]] = None

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        from datetime import datetime
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("timestamp must be ISO 8601 UTC")
        return v


class EvaluateRequest(BaseModel):
    source_id: str = Field(..., min_length=1, max_length=256)
    messages: List[MessageSchema] = Field(..., min_length=1, max_length=500)
    context: Optional[Dict[str, Any]] = None


class EvaluateResponse(BaseModel):
    trace_id: str
    score: float
    band: str
    requires_review: bool
    signals: List[Dict[str, Any]]


class ExplainResponse(BaseModel):
    trace_id: str
    explanation: Dict[str, Any]


class ContestRequest(BaseModel):
    reason: str = Field(..., min_length=10, max_length=2000)


class ContestResponse(BaseModel):
    contest_id: int
    status: str


class StatsResponse(BaseModel):
    total_evaluations: int
    average_score: float
    band_distribution: Dict[str, int]


class HealthResponse(BaseModel):
    status: str
    checks: Dict[str, str]
    version: str = "1.0.0"
