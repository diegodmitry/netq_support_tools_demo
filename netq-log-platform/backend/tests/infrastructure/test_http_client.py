import httpx
import pytest

from app.core.config import Settings
from app.core.observability import request_id_context
from app.infrastructure.http.client import IntegrationHttpClient
from app.infrastructure.http.errors import (
    IntegrationHTTPStatusError,
    IntegrationTimeoutError,
)


def test_http_client_retries_on_timeout_and_propagates_request_id() -> None:
    attempts = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise httpx.ReadTimeout("timeout", request=request)
        assert request.headers["X-Request-ID"] == "req-123"
        return httpx.Response(200, text="ok")

    settings = Settings(_env_file=None, outbound_http_max_retries=1)
    client = IntegrationHttpClient(
        settings,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        sleep=lambda _seconds: None,
    )

    token = request_id_context.set("req-123")
    try:
        response = client.request(method="GET", url="https://example.test/audit")
    finally:
        request_id_context.reset(token)

    assert attempts["count"] == 2
    assert response.status_code == 200
    assert response.body == "ok"


def test_http_client_raises_timeout_after_retry_exhaustion() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("timeout", request=request)

    settings = Settings(_env_file=None, outbound_http_max_retries=1)
    client = IntegrationHttpClient(
        settings,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        sleep=lambda _seconds: None,
    )

    with pytest.raises(IntegrationTimeoutError, match="timed out"):
        client.request(method="GET", url="https://example.test/audit")


def test_http_client_raises_http_status_error_for_unexpected_response() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="failure")

    settings = Settings(_env_file=None, outbound_http_max_retries=0)
    client = IntegrationHttpClient(
        settings,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(IntegrationHTTPStatusError) as exc_info:
        client.request(method="GET", url="https://example.test/audit")

    assert exc_info.value.status_code == 500
    assert exc_info.value.body == "failure"
