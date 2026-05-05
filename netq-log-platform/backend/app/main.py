from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse

from app.api.router import api_router
from app.core.config import get_settings
from app.core.observability import (
    configure_logging,
    metrics_registry,
    observability_middleware,
)
from app.domain.auth.errors import AuthAPIError

settings = get_settings()
configure_logging()

app = FastAPI(
    title="netq-log-platform backend",
    version="0.1.0",
    openapi_url=f"{settings.api_prefix}/openapi.json",
)
app.middleware("http")(observability_middleware)
app.include_router(api_router, prefix=settings.api_prefix)


@app.exception_handler(AuthAPIError)
async def auth_api_error_handler(_: Request, exc: AuthAPIError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc.body),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def readiness() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> PlainTextResponse:
    return PlainTextResponse(
        metrics_registry.render_prometheus(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
