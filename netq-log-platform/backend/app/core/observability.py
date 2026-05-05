import contextvars
import json
import logging
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from threading import Lock

from fastapi import Request, Response

request_id_context: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id",
    default=None,
)


class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get() or "-"
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        if hasattr(record, "event"):
            payload["event"] = record.event
        if hasattr(record, "method"):
            payload["method"] = record.method
        if hasattr(record, "path"):
            payload["path"] = record.path
        if hasattr(record, "status_code"):
            payload["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            payload["duration_ms"] = record.duration_ms
        return json.dumps(payload, ensure_ascii=True)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    handler.addFilter(RequestContextFilter())

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.INFO)


@dataclass
class MetricsSnapshot:
    total_requests: int
    in_progress_requests: int
    total_exceptions: int
    request_duration_seconds_sum: float


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = Lock()
        self._total_requests = 0
        self._in_progress_requests = 0
        self._total_exceptions = 0
        self._request_duration_seconds_sum = 0.0

    def begin_request(self) -> None:
        with self._lock:
            self._in_progress_requests += 1

    def complete_request(self, duration_seconds: float) -> None:
        with self._lock:
            self._total_requests += 1
            self._in_progress_requests -= 1
            self._request_duration_seconds_sum += duration_seconds

    def fail_request(self, duration_seconds: float) -> None:
        with self._lock:
            self._total_requests += 1
            self._in_progress_requests -= 1
            self._total_exceptions += 1
            self._request_duration_seconds_sum += duration_seconds

    def snapshot(self) -> MetricsSnapshot:
        with self._lock:
            return MetricsSnapshot(
                total_requests=self._total_requests,
                in_progress_requests=self._in_progress_requests,
                total_exceptions=self._total_exceptions,
                request_duration_seconds_sum=self._request_duration_seconds_sum,
            )

    def render_prometheus(self) -> str:
        snapshot = self.snapshot()
        lines = [
            "# HELP netq_http_requests_total Total HTTP requests handled.",
            "# TYPE netq_http_requests_total counter",
            f"netq_http_requests_total {snapshot.total_requests}",
            "# HELP netq_http_requests_in_progress In-flight HTTP requests.",
            "# TYPE netq_http_requests_in_progress gauge",
            f"netq_http_requests_in_progress {snapshot.in_progress_requests}",
            "# HELP netq_http_request_exceptions_total Total unhandled HTTP exceptions.",
            "# TYPE netq_http_request_exceptions_total counter",
            f"netq_http_request_exceptions_total {snapshot.total_exceptions}",
            "# HELP netq_http_request_duration_seconds_sum Total request duration in seconds.",
            "# TYPE netq_http_request_duration_seconds_sum counter",
            f"netq_http_request_duration_seconds_sum {snapshot.request_duration_seconds_sum}",
        ]
        return "\n".join(lines) + "\n"


metrics_registry = MetricsRegistry()
request_logger = logging.getLogger("netq.request")


async def observability_middleware(
    request: Request,
    call_next: Callable[[Request], Response],
) -> Response:
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    token = request_id_context.set(request_id)
    started_at = time.perf_counter()
    metrics_registry.begin_request()

    try:
        response = await call_next(request)
    except Exception:
        duration_seconds = time.perf_counter() - started_at
        metrics_registry.fail_request(duration_seconds)
        request_logger.exception(
            "Unhandled request exception",
            extra={
                "event": "http.request.failed",
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round(duration_seconds * 1000, 2),
                "status_code": 500,
            },
        )
        request_id_context.reset(token)
        raise

    duration_seconds = time.perf_counter() - started_at
    metrics_registry.complete_request(duration_seconds)
    response.headers["X-Request-ID"] = request_id
    request_logger.info(
        "Request completed",
        extra={
            "event": "http.request.completed",
            "method": request.method,
            "path": request.url.path,
            "duration_ms": round(duration_seconds * 1000, 2),
            "status_code": response.status_code,
        },
    )
    request_id_context.reset(token)
    return response
