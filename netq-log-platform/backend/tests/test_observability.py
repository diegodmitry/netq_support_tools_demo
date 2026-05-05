import json
import logging

from fastapi.testclient import TestClient

from app.core.observability import JsonFormatter
from app.main import app


def test_metrics_endpoint_exposes_prometheus_style_metrics() -> None:
    client = TestClient(app)

    client.get("/health")
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "netq_http_requests_total" in response.text
    assert "netq_http_request_duration_seconds_sum" in response.text


def test_request_id_is_returned_in_response_headers() -> None:
    client = TestClient(app)

    response = client.get("/health", headers={"X-Request-ID": "test-request-id"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-id"


def test_structured_request_logs_include_request_context(caplog) -> None:
    client = TestClient(app)

    with caplog.at_level(logging.INFO, logger="netq.request"):
        response = client.get("/ready", headers={"X-Request-ID": "req-123"})

    assert response.status_code == 200
    log_record = next(record for record in caplog.records if record.name == "netq.request")
    payload = json.loads(JsonFormatter().format(log_record))

    assert payload["event"] == "http.request.completed"
    assert payload["request_id"] == "req-123"
    assert payload["method"] == "GET"
    assert payload["path"] == "/ready"
    assert payload["status_code"] == 200
