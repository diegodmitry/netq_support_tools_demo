from fastapi.testclient import TestClient

from app.main import app
from app.domain.auth.errors import AuthAPIError


def test_audit_logs_query_returns_external_payload(monkeypatch) -> None:
    client = TestClient(app)

    def fake_query(self, payload, request):
        from app.domain.audit_logs.schemas import (
            AuditLogsQueryMeta,
            AuditLogsQueryResponse,
            AuditLogsQuerySummary,
            ExternalResult,
            PayloadView,
        )

        return AuditLogsQueryResponse(
            query=AuditLogsQuerySummary(**payload.model_dump()),
            mode="external",
            result=ExternalResult(
                externalSystem=payload.queryType,
                externalId=payload.queryValue,
                payload=PayloadView(
                    contentType="application/xml",
                    formatted="<formatted />",
                    raw="<raw />",
                ),
            ),
            meta=AuditLogsQueryMeta(requestId="req-123"),
        )

    monkeypatch.setattr(
        "app.application.audit_logs.service.AuditLogsService.query",
        fake_query,
    )

    response = client.post(
        "/api/v1/audit-logs/query",
        json={
            "environment": "prod",
            "queryType": "TIBCO",
            "queryValue": "EXT-123",
            "source": "request-id",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "external"
    assert body["result"]["externalSystem"] == "TIBCO"
    assert body["result"]["externalId"] == "EXT-123"


def test_audit_logs_query_validates_required_fields() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/audit-logs/query",
        json={
            "environment": "prod",
            "queryType": "NETQ",
            "queryValue": "",
            "source": "request-id",
        },
    )

    assert response.status_code == 422


def test_audit_logs_query_returns_sapa_payload(monkeypatch) -> None:
    client = TestClient(app)

    def fake_query(self, payload, request):
        from app.domain.audit_logs.schemas import (
            AuditLogsQueryMeta,
            AuditLogsQueryResponse,
            AuditLogsQuerySummary,
            PayloadView,
            SapaResult,
        )

        return AuditLogsQueryResponse(
            query=AuditLogsQuerySummary(**payload.model_dump()),
            mode="sapa",
            result=SapaResult(
                sapaId=payload.queryValue,
                payload=PayloadView(
                    contentType="application/xml",
                    formatted="<formatted />",
                    raw="<raw />",
                ),
            ),
            meta=AuditLogsQueryMeta(requestId="req-456"),
        )

    monkeypatch.setattr(
        "app.application.audit_logs.service.AuditLogsService.query",
        fake_query,
    )

    response = client.post(
        "/api/v1/audit-logs/query",
        json={
            "environment": "prod",
            "queryType": "SAPA",
            "queryValue": "1700426781",
            "source": "sapa-id",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "sapa"
    assert body["result"]["sapaId"] == "1700426781"


def test_audit_logs_related_detail_returns_panel_payload(monkeypatch) -> None:
    client = TestClient(app)

    def fake_query_related_detail(self, payload, request):
        from app.domain.audit_logs.schemas import (
            AuditLogsQueryMeta,
            PayloadView,
            RelatedDetailQuerySummary,
            RelatedDetailResponse,
            RelatedDetailResult,
        )

        return RelatedDetailResponse(
            query=RelatedDetailQuerySummary(**payload.model_dump()),
            result=RelatedDetailResult(
                orderId=payload.orderId,
                panel=payload.panel,
                payload=PayloadView(
                    contentType="application/xml",
                    formatted="<formatted />",
                    raw="<raw />",
                ),
            ),
            meta=AuditLogsQueryMeta(requestId="req-789"),
        )

    monkeypatch.setattr(
        "app.application.audit_logs.service.AuditLogsService.query_related_detail",
        fake_query_related_detail,
    )

    response = client.post(
        "/api/v1/audit-logs/related-detail",
        json={
            "environment": "prod",
            "orderId": "ORDER-123",
            "panel": "left",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["result"]["orderId"] == "ORDER-123"
    assert body["result"]["panel"] == "left"


def test_audit_logs_query_returns_empty_result_error(monkeypatch) -> None:
    client = TestClient(app)

    def fake_query(self, payload, request):
        raise AuthAPIError(
            status_code=404,
            body={
                "error": {
                    "code": "AUDIT_RESULT_EMPTY",
                    "message": "No records were returned for the submitted query.",
                },
                "meta": {"requestId": "req-empty"},
            },
        )

    monkeypatch.setattr(
        "app.application.audit_logs.service.AuditLogsService.query",
        fake_query,
    )

    response = client.post(
        "/api/v1/audit-logs/query",
        json={
            "environment": "prod",
            "queryType": "TIBCO",
            "queryValue": "EXT-123",
            "source": "request-id",
        },
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "AUDIT_RESULT_EMPTY"


def test_audit_logs_query_returns_upstream_timeout_error(monkeypatch) -> None:
    client = TestClient(app)

    def fake_query(self, payload, request):
        raise AuthAPIError(
            status_code=502,
            body={
                "error": {
                    "code": "UPSTREAM_TIMEOUT",
                    "message": "Timeout while querying upstream service.",
                    "details": {"system": "audit-prod", "queryType": "TIBCO"},
                },
                "meta": {"requestId": "req-timeout"},
            },
        )

    monkeypatch.setattr(
        "app.application.audit_logs.service.AuditLogsService.query",
        fake_query,
    )

    response = client.post(
        "/api/v1/audit-logs/query",
        json={
            "environment": "prod",
            "queryType": "TIBCO",
            "queryValue": "EXT-123",
            "source": "request-id",
        },
    )

    assert response.status_code == 502
    body = response.json()
    assert body["error"]["code"] == "UPSTREAM_TIMEOUT"
    assert body["error"]["details"] == {
        "system": "audit-prod",
        "queryType": "TIBCO",
    }


def test_audit_logs_query_returns_large_payload(monkeypatch) -> None:
    client = TestClient(app)
    large_payload = "<root>" + ("X" * 15000) + "</root>"

    def fake_query(self, payload, request):
        from app.domain.audit_logs.schemas import (
            AuditLogsQueryMeta,
            AuditLogsQueryResponse,
            AuditLogsQuerySummary,
            ExternalResult,
            PayloadView,
        )

        return AuditLogsQueryResponse(
            query=AuditLogsQuerySummary(**payload.model_dump()),
            mode="external",
            result=ExternalResult(
                externalSystem=payload.queryType,
                externalId=payload.queryValue,
                payload=PayloadView(
                    contentType="application/xml",
                    formatted=large_payload,
                    raw=large_payload,
                ),
            ),
            meta=AuditLogsQueryMeta(requestId="req-large"),
        )

    monkeypatch.setattr(
        "app.application.audit_logs.service.AuditLogsService.query",
        fake_query,
    )

    response = client.post(
        "/api/v1/audit-logs/query",
        json={
            "environment": "prod",
            "queryType": "TIBCO",
            "queryValue": "EXT-123",
            "source": "request-id",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["result"]["payload"]["formatted"]) == len(large_payload)
