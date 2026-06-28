import asyncio
import uuid
from functools import partial

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.api.schemas import (
    ContestRequest,
    ContestResponse,
    EvaluateRequest,
    EvaluateResponse,
    ExplainResponse,
    StatsResponse,
)
from cats.audit.logger import log_contest, log_evaluation
from cats.core.db import get_db
from cats.core.models import TrustScore
from cats.core.security import api_key_bearer, get_client_ip
from cats.pipeline.normalizer import normalize_messages
from cats.scoring.engine import aggregate_score, determine_band, requires_human_review
from cats.scoring.explainer import generate_explanation
from cats.scoring.weights import get_dynamic_weights
from cats.signals.coherence import compute_coherence
from cats.signals.gaming import compute_gaming
from cats.signals.silence import compute_silence
from cats.signals.types import SignalResult
from cats.signals.volatility import compute_volatility

logger = structlog.get_logger()
router = APIRouter()


@router.post("/evaluate", response_model=EvaluateResponse, dependencies=[Depends(api_key_bearer)])
async def evaluate(req: EvaluateRequest, request: Request, db: AsyncSession = Depends(get_db)):
    trace_id = str(uuid.uuid4())
    msgs = normalize_messages([m.model_dump() for m in req.messages])
    context = req.context or {}

    loop = asyncio.get_running_loop()
    raw_signals = await asyncio.gather(
        loop.run_in_executor(None, compute_coherence, msgs),
        loop.run_in_executor(None, compute_volatility, msgs),
        loop.run_in_executor(None, partial(compute_silence, msgs, context.get("source_type", "social"))),
        loop.run_in_executor(None, compute_gaming, msgs),
    )
    signals: list[SignalResult] = list(raw_signals)
    weights = get_dynamic_weights(context)
    score = aggregate_score(signals, weights)
    band = determine_band(score)
    review = requires_human_review(score, band, signals)

    db.add(
        TrustScore(
            trace_id=trace_id,
            source_id=req.source_id,
            score=score,
            band=band,
            signals={s.name: {"value": s.value, "confidence": s.confidence} for s in signals},
            weights=weights,
            context_data=context,
        )
    )
    await log_evaluation(
        db, trace_id, {"source_id": req.source_id, "score": score, "band": band}, ip=get_client_ip(request)
    )
    await db.commit()

    return EvaluateResponse(
        trace_id=trace_id,
        score=score,
        band=band,
        requires_review=review,
        signals=[
            {"name": s.name, "value": s.value, "confidence": s.confidence, "metadata": s.metadata} for s in signals
        ],
    )


@router.get("/explain/{trace_id}", response_model=ExplainResponse, dependencies=[Depends(api_key_bearer)])
async def explain(trace_id: str, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(TrustScore).where(TrustScore.trace_id == trace_id))
    ts = r.scalars().first()
    if not ts:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trace ID not found")
    sigs = [SignalResult(name=n, value=d["value"], confidence=d["confidence"]) for n, d in ts.signals.items()]
    return ExplainResponse(trace_id=trace_id, explanation=generate_explanation(ts.score, ts.band, sigs, ts.weights))


@router.post("/contest/{trace_id}", response_model=ContestResponse, dependencies=[Depends(api_key_bearer)])
async def contest(trace_id: str, body: ContestRequest, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(TrustScore).where(TrustScore.trace_id == trace_id))
    if not r.scalars().first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trace ID not found")
    cid = await log_contest(db, trace_id, body.reason)  # D-02: returns cid
    return ContestResponse(contest_id=cid, status="pending")


@router.post("/review/{trace_id}", dependencies=[Depends(api_key_bearer)])
async def review(trace_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(TrustScore).where(TrustScore.trace_id == trace_id))
    if not r.scalars().first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Trace ID not found")
    await log_evaluation(db, trace_id, {"event": "human_review_requested"}, ip=get_client_ip(request))
    await db.commit()
    return {"message": "Review logged", "trace_id": trace_id}


@router.get("/stats", response_model=StatsResponse, dependencies=[Depends(api_key_bearer)])
async def stats(db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count(TrustScore.id)))
    avg = await db.scalar(select(func.avg(TrustScore.score)))
    bands_raw = await db.execute(select(TrustScore.band, func.count(TrustScore.id)).group_by(TrustScore.band))
    return StatsResponse(
        total_evaluations=total or 0,
        average_score=avg or 0.0,
        band_distribution={r[0]: r[1] for r in bands_raw.all()},
    )
