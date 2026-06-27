from contextlib import asynccontextmanager
import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from cats.core.config import settings
from cats.core.db import AsyncSessionLocal
from cats.core.security import init_jwt_keys, init_redis
from cats.signals.coherence import init_nlp
from cats.audit.logger import init_redis_logger, purge_expired_audits
from cats.api.routes.evaluate import router as evaluate_router

# N-06: JSON structured logging
structlog.configure(processors=[
    structlog.stdlib.filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.JSONRenderer(),
])
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup", env=settings.environment)
    init_jwt_keys()                              # S-01
    await init_redis()                           # S-03
    await init_redis_logger(settings.redis_url)  # I-03
    init_nlp(settings.spacy_model)               # N-01: singleton

    # Q-03: max_instances=1 prevents overlapping purge jobs
    sched = AsyncIOScheduler()
    sched.add_job(_purge_job, "cron", hour=2, minute=0,
                  max_instances=1, coalesce=True, misfire_grace_time=3600)
    sched.start()
    yield
    sched.shutdown()
    logger.info("shutdown")


async def _purge_job():
    async with AsyncSessionLocal() as db:
        await purge_expired_audits(db)


app = FastAPI(title="CATS API", version="1.0.0", lifespan=lifespan)
app.include_router(evaluate_router, prefix="/v1/cats", tags=["cats"])


# A-03: RFC 7807 Problem Details
@app.exception_handler(RequestValidationError)
async def _val_err(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={
        "type": "about:blank", "title": "Validation Error",
        "status": 422, "detail": exc.errors(), "instance": str(request.url),
    })


@app.exception_handler(Exception)
async def _generic_err(request: Request, exc: Exception):
    logger.error("unhandled", error=str(exc), path=str(request.url))
    return JSONResponse(status_code=500, content={
        "type": "about:blank", "title": "Internal Server Error",
        "status": 500, "detail": "Unexpected error", "instance": str(request.url),
    })


# Q-02: deep health check
@app.get("/health")
async def health():
    from cats.core.security import redis_client
    from cats.core.db import engine
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
    return {"note": "Prometheus metrics — integrate prometheus-client here"}
