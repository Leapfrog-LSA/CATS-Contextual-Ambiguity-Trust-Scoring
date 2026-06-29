import logging
import time
from contextlib import asynccontextmanager

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from cats.api.routes.evaluate import router as evaluate_router
from cats.audit.logger import purge_expired_audits
from cats.core.config import settings
from cats.core.db import AsyncSessionLocal
from cats.core.metrics import HTTP_LATENCY, HTTP_REQUESTS
from cats.core.security import init_jwt_keys, init_redis
from cats.signals.coherence import init_nlp

# N-06: JSON structured logging. Use structlog-native processors + a filtering
# bound logger so level filtering works without a stdlib logging backend (the
# stdlib `filter_by_level` processor calls isEnabledFor(), which PrintLogger
# lacks, and would crash on every log call).
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, settings.log_level.upper(), logging.INFO)),
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup", env=settings.environment)
    init_jwt_keys()  # S-01
    await init_redis()  # S-03
    init_nlp(settings.spacy_model)  # N-01: singleton

    # Q-03: max_instances=1 prevents overlapping purge jobs
    sched = AsyncIOScheduler()
    sched.add_job(_purge_job, "cron", hour=2, minute=0, max_instances=1, coalesce=True, misfire_grace_time=3600)
    sched.start()
    yield
    sched.shutdown()
    logger.info("shutdown")


async def _purge_job():
    async with AsyncSessionLocal() as db:
        await purge_expired_audits(db)


app = FastAPI(title="CATS API", version="1.2.0", lifespan=lifespan)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(evaluate_router, prefix="/v1/cats", tags=["cats"])


# N-07: Prometheus request metrics. Label by the matched route template (not the
# raw path) to keep label cardinality bounded.
@app.middleware("http")
async def _prometheus_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    route = request.scope.get("route")
    path = getattr(route, "path", None) or "unmatched"
    HTTP_REQUESTS.labels(request.method, path, response.status_code).inc()
    HTTP_LATENCY.labels(request.method, path).observe(time.perf_counter() - start)
    return response


# A-03: RFC 7807 Problem Details
@app.exception_handler(RequestValidationError)
async def _val_err(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "type": "about:blank",
            "title": "Validation Error",
            "status": 422,
            "detail": exc.errors(),
            "instance": str(request.url),
        },
    )


@app.exception_handler(Exception)
async def _generic_err(request: Request, exc: Exception):
    logger.error("unhandled", error=str(exc), path=str(request.url))
    return JSONResponse(
        status_code=500,
        content={
            "type": "about:blank",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "Unexpected error",
            "instance": str(request.url),
        },
    )


# Q-02: deep health check
@app.get("/health")
async def health():
    from cats.core.db import engine
    from cats.core.security import redis_client
    from cats.signals.coherence import nlp

    checks: dict = {"api": "ok"}
    try:
        await redis_client.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error:{e}"
    try:
        from sqlalchemy import text

        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error:{e}"
    checks["nlp"] = "ok" if nlp else "not_loaded"

    overall = "healthy" if all(v == "ok" for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
