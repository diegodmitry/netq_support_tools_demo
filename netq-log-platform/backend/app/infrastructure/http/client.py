import logging
import time
from dataclasses import dataclass
from typing import Any

import httpx

from app.core.config import Settings
from app.core.observability import request_id_context
from app.infrastructure.http.errors import (
    IntegrationHTTPStatusError,
    IntegrationTimeoutError,
    IntegrationTransportError,
)

logger = logging.getLogger("netq.integration.http")


@dataclass
class HttpResponsePayload:
    status_code: int
    body: str
    headers: dict[str, str]


class IntegrationHttpClient:
    def __init__(
        self,
        settings: Settings,
        *,
        client: httpx.Client | None = None,
        sleep: Any = None,
    ) -> None:
        self.settings = settings
        self.client = client or httpx.Client(follow_redirects=True)
        self.sleep = sleep or time.sleep

    def request(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        content: str | None = None,
        auth: tuple[str, str] | None = None,
        timeout_seconds: float | None = None,
        max_retries: int | None = None,
    ) -> HttpResponsePayload:
        effective_timeout = timeout_seconds or self.settings.outbound_http_timeout_seconds
        retry_count = (
            max_retries if max_retries is not None else self.settings.outbound_http_max_retries
        )
        base_headers = self._build_headers(headers)

        for attempt in range(retry_count + 1):
            try:
                response = self.client.request(
                    method=method,
                    url=url,
                    headers=base_headers,
                    params=params,
                    content=content,
                    auth=auth,
                    timeout=effective_timeout,
                )
            except httpx.TimeoutException as exc:
                if attempt == retry_count:
                    raise IntegrationTimeoutError("Integration request timed out.") from exc
                self._sleep_before_retry(attempt)
                continue
            except httpx.HTTPError as exc:
                if attempt == retry_count:
                    raise IntegrationTransportError("Integration transport error.") from exc
                self._sleep_before_retry(attempt)
                continue

            if response.status_code in {502, 503, 504} and attempt < retry_count:
                self._sleep_before_retry(attempt)
                continue

            if response.status_code >= 400:
                raise IntegrationHTTPStatusError(response.status_code, response.text)

            logger.info(
                "Outbound integration request succeeded",
                extra={
                    "event": "integration.http.success",
                    "method": method.upper(),
                    "path": url,
                    "status_code": response.status_code,
                },
            )
            return HttpResponsePayload(
                status_code=response.status_code,
                body=response.text,
                headers=dict(response.headers),
            )

        raise IntegrationTransportError("Integration request failed after retries.")

    def _build_headers(self, headers: dict[str, str] | None) -> dict[str, str]:
        base_headers = dict(headers or {})
        request_id = request_id_context.get()
        if request_id and "X-Request-ID" not in base_headers:
            base_headers["X-Request-ID"] = request_id
        return base_headers

    def _sleep_before_retry(self, attempt: int) -> None:
        backoff = self.settings.outbound_http_retry_backoff_seconds * (attempt + 1)
        self.sleep(backoff)
